import cv2
import numpy as np
import pandas as pd
from joblib import load
from tqdm.auto import tqdm
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from sklearn.neighbors import NearestNeighbors

from preprocess import preproc

queries = pd.read_csv('data/queries.csv')
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

test['item_nm'] = test['item_nm'].apply(preproc)
test['item_nm'] = test['item_nm'].apply(lambda x: x[0])

base_model = load_model('weights/EfficientNetV2B2_v7.h5')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)
model.trainable = False


def extract_features(path, model=model):
    img = cv2.imread(path)
    img = tf.keras.layers.Resizing(240, 240)(img)
    x = np.expand_dims(img, axis=0)

    feature = model.predict(x, verbose=0)[0]

    return feature / np.linalg.norm(feature)


test_embeddings = []

for idx in tqdm(test.idx):
    test_embeddings.append(extract_features(f'data/test/{idx}.png'))

test_embeddings = np.array(test_embeddings)

queries_embeddings = []

for idx in tqdm(queries.idx):
    queries_embeddings.append(extract_features(f'data/queries/{idx}.png'))

queries_embeddings = np.array(queries_embeddings)

mapper = load('weights/PCA_400_v7_rbf.joblib')

test_embedded = mapper.transform(test_embeddings)
queries_embedded = mapper.transform(queries_embeddings)

k_neigh = len(test_embedded)

neigh = NearestNeighbors(n_neighbors=k_neigh, metric='cosine', algorithm='brute')
neigh.fit(test_embedded)

distances, idxs = neigh.kneighbors(queries_embedded, k_neigh, return_distance=True)

pred_data = pd.DataFrame()
pred_data['score'] = distances.flatten()
pred_data['database_idx'] = [test.idx.iloc[x] for x in idxs.flatten()]
pred_data.loc[:, 'query_idx'] = np.repeat(queries.idx, k_neigh).values

pred_data.score = pred_data.score.apply(lambda x: 1 - x)

# Нормализация по всему датасету
pred_data.score = (pred_data.score - pred_data.score.min(axis=0)) / \
                  (pred_data.score.max(axis=0) - pred_data.score.min(axis=0))

submit = pred_data.groupby(by='query_idx').apply(lambda dft: dft.nlargest(1, 'score')).merge(test,
                                                                                             left_on='database_idx',
                                                                                             right_on='idx')

submit.drop(['score', 'idx', 'database_idx'], inplace=True, axis=1)

submit = pred_data.merge(submit, how='left', on='query_idx')
submit = submit.rename({'item_nm': 'key'}, axis=1)
submit = submit.merge(test, left_on='database_idx', right_on='idx').drop(['idx'], axis=1)

submit['marker'] = submit.apply(lambda x: str(x.key) in str(x.item_nm), axis=1)
submit['score_2'] = submit.apply(lambda x: (x.score + x.marker) / 2 - 0.05 if x.marker else x.score / 2 - 0.05, axis=1)


submit['score_2'] = submit['score_2'].apply(lambda x: 1. if x > 1. else x)
submit['score_2'] = submit['score_2'].apply(lambda x: 0. if x < 0. else x)

submit.drop(['item_nm', 'key', 'marker', 'score'], inplace=True, axis=1)
submit = submit.sort_values(['query_idx', 'score_2'], ascending=[True, False]).reset_index(drop=True)
submit = submit.rename({'score_2': 'score'}, axis=1)

submit = submit[['score', 'database_idx', 'query_idx']]

submit.to_csv('data/submission.csv', index=False)
