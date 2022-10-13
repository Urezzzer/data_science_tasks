import pymorphy2
import razdel
from string import punctuation

stop_words = ['с', 'в', 'под', 'для', 'от', '...', 'cbn-быть', 'камаз-евро', 'верхний', 'высокий', 'г-образный', 'жёлтый', 'зелёный',
              'красный', 'левый', 'синий', 'наружный', 'неподвижный', 'передний', 'п-образный', 'правый', 'т-смарт',
              'т-flex',
              'уралец', 'маз', 'камаз', 'медный', 'металлический', 'люкс', 'лобовой', 'коммунальный', 'вс-т', 'влево',
              'вправо',
              'задний', 'передний', 'ведущий', 'ведомый', 'болгария', 'греция', 'боковой', 'кабинный', 'азотировать',
              'аналог',
              'замедлительный', 'ямз', 'мом', 'торможение', 'прямой', 'простой', 'проходной', 'синтая',
              'призматический',
              'тупой', 'упираться', 'самоустанавливаться', 'радиальный', 'шариковый', 'плунжерный', 'подъёмный',
              'трактор',
              'раструбный', 'раструструбный', 'подвижный', 'русич', 'мпа', 'торцевой', 'лодочный', 'четверной',
              'универсальный',
              'ход', 'оцинк', 'стопорный', 'круглый', 'сечение', 'квадрат', 'цвет', 'накал', 'нижний', 'верхний',
              'солнечный',
              'конический', 'файтереть', 'номерной', 'рубашка', 'сцепление', 'давление', 'поворотный', 'рулевой',
              'гладкий',
              'сталь', 'нержавеющий', 'поворот', 'меш', 'всасывать', 'червячный', 'регулировочный',
              'сельскохозяйственный',
              'пку', 'профильный', 'повышать', 'понижать', 'шаровыя', 'распределительный', 'промежуточный', 'первичный',
              'бульдозерный', 'ротационный', 'проч', 'пенька', 'ниточный', 'впускной', 'закалённый', 'мотоблок',
              'голый', 'клапанный',
              'новый', 'капот', 'штанга', 'цифровой', 'стремянка', 'секция', 'электрический', 'тарелка', 'резьбовой',
              'скаут',
              'универсал', 'сменный', 'средний', 'подключение', 'площадка', 'наружний', 'продольный', 'модификация',
              'сетка',
              'стрельчатый', 'прерывание', 'непрерывный', 'ходовой', 'приводной', 'средний', 'реверсивный',
              'соединительный',
              'кпс', 'ксп', 'стык', 'отверстый', 'маслосъёмный', 'раздвижной', 'предохранительный', 'тарелка', 'тсн',
              'подогрев',
              'хранение', 'урал', 'охлаждать', 'полевой', 'уралец', 'сеновязальный', 'джутовый', 'внешний', 'стальной',
              'грубый',
              'система', 'охлаждение', 'коса', 'напорный', 'дистанционный', 'крестовидный', 'гидравлический',
              'дизельный',
              'двойной', 'толщина', 'жечь', 'крестовина', 'имбусовый', 'байонетный', 'навесный', 'усиленный',
              'разбрасывать',
              'жсу', 'год', 'мех', 'большой', 'малый', 'резьба', 'переходной', 'бум', 'бумажный', 'маслоналивной',
              'плоский',
              'внешний', 'внешн', 'грубый', 'серия', 'распорный', 'стальной', 'бумага', 'подрулевой', 'внутренний',
              'раздаточный',
              'роликовый', 'квт', 'градус', 'бобина', 'тонкий', 'зил', 'линейный', 'прозрачный', 'короткий',
              'форкамерный']
morph = pymorphy2.MorphAnalyzer()


def preproc(sentence):
    if 'Втулка' in sentence:
        sentence += ' Втулка'
    if 'Пластина' in sentence:
        sentence += ' Пластина'
    tokens = [_.text.lower() for _ in list(razdel.tokenize(str(sentence)))]
    unique_tokens = set()

    final_sentence = []

    for token in tokens:
        if len(token) > 2 and not any([char.isdigit() for char in token]):
            parsed_token = morph.parse(token)[0]
            if str(parsed_token.tag) != 'LATN' \
                    and parsed_token.normal_form not in punctuation \
                    and parsed_token.normal_form not in stop_words:

                token = str(parsed_token.normal_form)
                if token in ['u-болт', 'болт-скоба']:
                    token = 'болт'
                elif token == 'гидробак':
                    token = 'бак'
                elif token == 'полуось':
                    token = 'ось'
                elif token == 'проводы':
                    token = 'провод'
                elif token == 'фильтровать':
                    token = 'фильтр'
                elif 'пресс' in token:
                    token = 'пресс'
                elif 'хладон' in token:
                    token = 'баллон'
                elif 'поршневой' in token:
                    token = 'поршень'
                elif 'гайка' in token:
                    token = 'гайка'
                elif 'фреон' in token:
                    token = 'газ'
                elif 'трактор' in token:
                    token = 'трактор'
                elif 'датчик' in token:
                    token = 'датчик'
                elif 'ремкомплект' in token:
                    token = 'ремень'
                elif 'упак' in token:
                    token = 'упаковка'
                elif 'переходный' in token:
                    token = 'переходник'
                elif 'упл' in token:
                    token = 'уплотнитель'
                elif 'компл' in token:
                    token = 'комплект'
                elif 'стартер' in token:
                    token = 'стартер'
                elif 'шатунно-поршневой' in token:
                    token = 'шатун'
                elif 'форсунка-распылитель' in token:
                    token = 'форсунка'
                elif 'фиттинг' in token:
                    token = 'фитинг'
                elif 'всасывать' in token:
                    token = 'вентилятор'
                elif 'валик' in token:
                    token = 'вал'
                elif 'агретирование' in token:
                    token = 'навеска'
                elif 'агрегатирование' in token:
                    token = 'навеска'
                elif 'гидронасос' in token:
                    token = 'гидравлический насос'
                elif 'шарикоподшипник' in token:
                    token = 'подшипник'
                elif 'ролик-натяжитель' in token:
                    token = 'ролик натяжитель'

                if token not in unique_tokens:
                    final_sentence.append(token)
                    unique_tokens.add(token)

    if 'головка' in ' '.join(final_sentence) and 'блок' in ' '.join(final_sentence) \
            and 'цилиндр' in ' '.join(final_sentence):
        final_sentence.append('гбц')

    if final_sentence:
        if 'прокладка' in final_sentence:
            final_sentence = ['прокладка'] + final_sentence
        elif len(final_sentence) > 1 and final_sentence[1] == 'противоскольжение':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'винт':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'крепление':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'вентилятор':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'зажигание':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'фара':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'шланг':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'штуцер':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'лемех':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'форсунка':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'управление':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'предохранитель':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'сальник':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'уплотнение':
            final_sentence = [final_sentence[1]]
        elif len(final_sentence) > 1 and final_sentence[1] == 'нож' and final_sentence[0] == 'вал':
            final_sentence = ['вал_нож']
        elif len(final_sentence) > 1 and final_sentence[1] == 'нож':
            final_sentence = [final_sentence[1]]
        elif 'гбц' in final_sentence:
            final_sentence = ['гбц']

    if not final_sentence:
        final_sentence = ['другое']
    return final_sentence
