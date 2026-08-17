# -*- coding: utf-8 -*-
"""
Сборка index.html для РЦ «Порхай».

Раскладка декоративных лент снята с оригинального сайта на Тильде
(отрисованные координаты, а не атрибуты разметки) и вынесена в данные,
чтобы 8 одинаковых лент не дублировались в разметке восемь раз.

Запуск:  python build.py
"""
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))

# Картинки берём из assets/img — их готовит optimize_images.py:
# растр пережат в WebP, SVG скопированы как есть.
IMG = 'assets/img/'

# --- Кляксы ---------------------------------------------------------------
# Две «фигмовские» ссылки в оригинале битые; локальные копии тех же файлов
# лежат в экспорте и подставлены здесь.
BIT = {
    'ce4b55ff': 'tild3830-3337-4132-a433-353037316233__ce4b55ff-1348-4ed2-9.svg',
    '8c2a0952': 'tild6662-3064-4664-b965-643135646265__8c2a0952-fd23-43da-9.svg',
    '4bfa8c73': 'tild3162-3239-4861-b565-653635356432__4bfa8c73-aa86-483a-8.svg',
    'fe3676d5': 'tild3834-3936-4439-a337-323138313739__fe3676d5-445c-4737-8.svg',
    'c5a30fb3': 'tild6536-3738-4935-b361-306331313263__c5a30fb3-9dbb-4893-a.svg',
    'a5847e0b': 'tild3164-3665-4062-b633-303131646633__a5847e0b-2475-42f8-b.svg',
    '13fdaa4f': 'tild3532-3435-4063-b765-393834336438__13fdaa4f-9832-485a-8.svg',
    'ba8b36e1': 'tild6364-3530-4265-b262-303639303264__ba8b36e1-c9cf-4b27-8.svg',
    'ceeef3f3': 'tild3761-6330-4363-a139-333735393763__ceeef3f3-f388-4101-8.svg',
    '24e3675d': 'tild3265-6337-4265-b431-656532336431__24e3675d-1861-4ae3-a.svg',
    'd4abbe9e': 'tild3461-3035-4434-a665-336137363631__d4abbe9e-b405-4115-a.svg',
    '9cae1dcb': 'tild6463-3538-4461-a236-353162633838__9cae1dcb-d946-42c5-9.svg',
}

# Белые круги ленты: (левый край в % ширины макета, смещение вверх в px)
BUBBLES = [
    (-2.75, -29), (3.25, -54), (9.58, -29), (15.00, -62), (21.75, -38),
    (28.33, -20), (35.08, -50), (42.74, -29), (50.32, -46), (57.57, -18),
    (63.99, -46), (69.90, -29), (76.57, -27), (82.65, -53), (88.90, -27),
    (94.23, -60),
]

# Мелкие цветные чёрточки на шариках:
# (x %, y px, ширина px, ключ файла, начальный поворот °, дрейф по X px, доворот °)
# Дрейф и доворот — из раскадровки оригинала: за ~200px прокрутки чёрточка
# уезжает вправо на mx и проворачивается на ro, затем возвращается.
CONFETTI = [
    (7.08, -42, 16, 'd4abbe9e', -19, 21, 35), (10.58, -9, 16, '24e3675d', 0, 24, 25),
    (16.50, -39, 16, 'ceeef3f3', 0, 45, 85), (24.00, -20, 16, 'ba8b36e1', 0, 25, 100),
    (33.83, 1, 16, '13fdaa4f', 0, 24, -15), (36.91, -32, 16, 'a5847e0b', 0, 21, 35),
    (44.41, -7, 16, 'c5a30fb3', -13, 45, 85), (54.49, -33, 16, 'fe3676d5', -28, 25, 40),
    (59.66, 5, 16, '4bfa8c73', -10, 24, 25), (68.91, -36, 16, 'ce4b55ff', -13, 21, 35),
    (73.40, -15, 16, '8c2a0952', 0, 45, 85), (78.82, -17, 16, '9cae1dcb', -12, 24, 25),
    (86.49, -39, 16, 'd4abbe9e', -32, 25, 100), (90.49, -7, 16, '24e3675d', 0, 21, 35),
    (95.90, -37, 16, 'ceeef3f3', -20, 45, 60),
]

# Шарики тоже дрейфуют — слабее, чем чёрточки.
BUBBLE_DRIFT = (24, 25)


def band(flip=False):
    """Лента-разделитель: шарики и чёрточки на них.

    flip=True — чёрточки свисают вниз (вариант Б).
    data-drift="mx,ro" — дрейф по прокрутке, читается скриптом внизу страницы.
    """
    out = ['<div class="band" aria-hidden="true"><div class="band__inner">']
    bmx, bro = BUBBLE_DRIFT
    for i, (x, y) in enumerate(BUBBLES):
        out.append('<span class="band__bubble" style="left:%s%%;top:%dpx" '
                   'data-drift="%d,%d"></span>'
                   % (x, y, bmx if i % 2 else -bmx, bro if i % 2 else -bro))
    for x, y, w, key, rot, mx, ro in CONFETTI:
        yy = -y + 6 if flip else y
        rr = rot + 180 if flip else rot
        # Статичный поворот — на картинке, дрейф — на обёртке,
        # чтобы скрипт не затирал поворот и наоборот.
        out.append('<span class="band__bit" style="left:%s%%;top:%dpx;width:%dpx" '
                   'data-drift="%d,%d"><img src="%s%s" alt="" '
                   'style="transform:rotate(%ddeg)"></span>'
                   % (x, yy, w, mx, ro, IMG, BIT[key], rr))
    out.append('</div></div>')
    return ''.join(out)


# --- Данные страницы ------------------------------------------------------
NAV = [
    ('Разовое посещение', '/razovoe'),
    ('Аренда залов', '#zaly'),
    ('Праздник под ключ', '#pod-kluch'),
    ('Для групп', '#dlyagrupp'),
    ('Отзывы', '#otziv'),
    ('Скидки от партнёров', '/partner'),
    ('Контакты', '#kontakt'),
]

# Неразрывные пробелы — как в оригинале: они держат переносы строк.
# «Cтильные» начинается с латинской C — опечатка исходника, переносим как есть.
CARDS = [
    ('tild6631-6164-4662-a432-643636393437__f8b680e9-d185-4e5c-a.webp',
     '3 сухих бассейна: Белый бассейн, «Попкорн» и&nbsp;«Арбуз»'),
    ('tild6631-6530-4933-a263-616162353439__rectangle_10.webp',
     'Cтильные фотозоны и&nbsp;Ростовые&nbsp;фигуры'),
    ('tild3662-3462-4531-b130-666539343532__rectangle_13.webp',
     'Наша волшебная комната с&nbsp;фонариками'),
]

# Плитка «4 шага»: (файл иконки, текст)
STEPS = [
    ('tild3731-6636-4962-b130-626633363163__frame_11.svg', 'Бронируйте зал на&nbsp;нужную дату'),
    ('tild3463-6661-4338-a662-623335396263__frame_12.svg', 'Выбирайте тематику и&nbsp;программу'),
    ('tild3266-3436-4062-a439-646530363831__frame_13.svg', 'Закажите любимые угощения и&nbsp;сладости'),
    ('tild3139-3761-4734-b865-326566393261__frame_14.svg', 'Приходите в&nbsp;назначенный день с&nbsp;хорошим настроением'),
]

# Стрелка между шагами — инлайновая SVG из оригинала, обводка бирюзовая.
STEP_ARROW = ('<span class="step__arrow" aria-hidden="true">'
              '<svg viewBox="0 0 40 18.7" stroke="#38a2a5" fill="none" xmlns="http://www.w3.org/2000/svg">'
              '<path d="M4.2 9.4h32.1"/><path d="M31.3 13.4l5-4-5-4"/></svg></span>')

# Варианты аренды залов: три карточки. Цены актуальные (content/prices.md),
# не из экспорта. «White Room» — так зал называют сейчас; в экспорте было
# «White Box». Вместимость «Комбо+» — «до 50 человек» (совпадает по всему
# сайту), в экспорте было «50–55».
TARIFFS = [
    dict(color='#ecbdc7', big='tild6139-6135-4965-b164-663136663630__6c636ea6-a060-4fcf-9.webp',
         small='tild6364-3665-4162-a166-633932326531__9a1357ad-f456-47ed-8.webp', href='/whiteroom',
         title='White Room',
         desc='Самый глубокий белый бассейн с&nbsp;шариками и&nbsp;разными активностями&nbsp;— качели, канаты, обручи, скалодром',
         note='НЕТ ДОСТУПА К&nbsp;ФОТОЗОНАМ',
         price='Стоимость от&nbsp;5 000 ₽/час'),
    dict(color='#dffffe', big='tild3866-3833-4662-a438-323839343863__ellipse_46.webp',
         small='tild6136-3362-4834-b234-663035363664__ellipse_45.webp', href='/loftbox',
         title='Loft Box',
         desc='Отдельный банкетный зал + средний и&nbsp;маленький бассейны + все фотозоны музея',
         note='НЕТ ДОСТУПА К&nbsp;БЕЛОМУ БАССЕЙНУ',
         price='Стоимость от&nbsp;5 000 ₽/час'),
    dict(color='#ffedb5', big='tild3632-3630-4962-b133-326461616532__ellipse_39.webp',
         small='tild3764-6136-4033-a235-646232373930__ellipse_38.webp', href='/combo',
         title='Комбо +',
         desc='Для больших компаний свыше 25 человек, мы предлагаем к&nbsp;аренде АБСОЛЮТНО ВЕСЬ ЦЕНТР',
         note='Вместимость до&nbsp;50 человек',
         price='Стоимость от&nbsp;8 000 ₽/час'),
]

# Праздники «под ключ»: тот же карточный компонент, что и у аренды залов
# (те же рамки, те же 3 цвета). Цены дня рождения актуальные из content/prices.md
# — на главной показываем самый дешёвый пакет «Мини» (16 500 ₽, 15 гостей).
# Выпускной и корпоратив не трогаем — заказчик просил оставить как есть.
KEYS = [
    dict(color='#ecbdc7', big='tild6262-3832-4039-a364-343835613338__ellipse_34-1.webp',
         small='tild3138-3237-4938-b536-343663643239__ellipse_35-1.webp', href='/denrozhdeniya',
         title='День рождения',
         desc='Мы&nbsp;собрали всё необходимое для&nbsp;вашего дня рождения, вам останется только наполнить праздник угощениями для&nbsp;гостей',
         note='Включено 15 гостей',
         price='Стоимость от&nbsp;16 500 ₽'),
    dict(color='#dffffe', big='tild3939-6462-4031-a365-626561303136__ellipse_34.webp',
         small='tild3434-6363-4566-a530-396430336365__ellipse_37.webp', href='/vypusknye',
         title='Выпускной',
         desc='Идеальный пакет для выпускного, чтобы ваш праздник прошёл легко, без&nbsp;суеты и&nbsp;лишний траты времени на&nbsp;организацию',
         note='Вместимость 50 человек',
         price='Стоимость от&nbsp;1090 ₽/чел.'),
    dict(color='#ffedb5', big='tild3932-6239-4463-b232-616230636431__ellipse_43.webp',
         small='tild3831-6137-4662-a462-383763353036__ellipse_34.webp', href='/korporativ',
         title='Корпоратив',
         desc='Организуйте свой лучший корпоратив&nbsp;— с&nbsp;игрой в&nbsp;мафию или играми на&nbsp;сплочение, различными мастер-классами или любым другим наполнением по&nbsp;вашему желанию',
         note=None,
         price=None),
]

# Предложения для организованных групп: 7 карточек, каждая открывает
# попап с описанием и фотогалереей (см. GROUP_POPUPS ниже). Кольца вокруг
# круглой иконки — те же цвета, что и в остальном сайте (teal/yellow),
# но проще: два простых кольца без поворота, поэтому сделаны в CSS,
# а не 14 одинаковых svg-файлов из экспорта.
GROUPS = [
    ('tild3264-3831-4631-a235-303430646239__3f3c7f25-e958-4518-8.webp', 'Mafiya', 'Игра «Мафия»'),
    ('tild3066-3637-4838-a235-633265353436__ellipse_36.webp', 'krio', 'Крио-кухня'),
    ('tild6335-6163-4236-a465-323639363531__cb2e96ba-a32c-4830-8.webp', 'pati', 'Супер-челлендж-пати'),
    ('tild3865-3862-4661-b934-376639373363__ellipse_40.webp', 'Tusovka', 'Тусовка в Порхай'),
    ('tild6362-3035-4330-b534-613931393031__1a18bade-be51-4fee-b.webp', 'Uensdej', 'Квест «Уэнсдей»'),
    ('tild3364-6338-4161-a236-616238343631__0652da47-ebbd-433f-b.webp', 'CashFlow', 'Игра «Денежный поток»'),
    ('tild3362-3134-4335-a661-393762393637__ellipse_36.webp', 'Masterklass', 'Мастер-классы'),
]

# Содержимое поп-апов — дословно из экспорта (rec569429744 и другие,
# см. data-tooltip-hook в оригинальном HTML для сопоставления записи с ключом
# попапа). Цены в подзаголовках «Тусовки» и «CashFlow» не входили
# в присланный прайс-лист — перенесены как есть, требуют подтверждения
# у заказчика наравне с остальными ценами из экспорта 2023 года.
POPUPS = {
    'Mafiya': dict(
        title='Игра «Мафия» для детей и взрослых в «Порхай!»',
        subtitle='➕ веселье в «Порхай»',
        body='Приглашаем организованные группы весело провести время за\xa0увлекательной и\xa0полезной игрой!\n⠀\nИгра в\xa0Мафию учит логике и\xa0развивает чувство интуиции. А\xa0наблюдать за\xa0тем, как дети играют в\xa0эту игру\xa0— одно удовольствие. Они порой строят нереальные догадки и\xa0фантастические версии!\n\nА\xa0чтобы точно закрепить впечатления, все детки после игры отправятся покорять бассейны с\xa0тысячами шариков, побывают во\xa0всех фотозонах и\xa0волшебной комнате с\xa0фонариками.\n\nНе\xa0упустите возможность оригинально и\xa0не\xa0банально провести время со\xa0своими близкими\xa0— за\xa0интересной игрой и\xa0еще плюсом повеселитесь в\xa0«Порхай!» Приходи вместе с\xa0классом, секцией или просто компанией друзей!',
        images=['tild3034-6462-4234-a366-343963363266__photo_2022-04-02_09-.webp', 'tild3363-6532-4061-a461-656664306430__photo_2022-02-09_14-.webp', 'tild3435-3961-4536-b934-356332386638__photo_2022-02-09_14-.webp', 'tild3663-3337-4561-b666-656561373137__photo_2022-02-09_14-.webp', 'tild3730-6166-4566-b135-656661646165__photo_2022-02-09_14-.webp', 'tild3736-3433-4730-b935-613436343130__photo_2022-04-02_09-.webp', 'tild3738-3932-4438-a434-363239373636__photo_2022-04-02_09-.webp', 'tild3762-6238-4136-b936-346462366363__photo_2022-04-02_09-.webp', 'tild3836-6264-4333-a337-316465363462__photo_2022-04-02_09-.webp', 'tild3862-3538-4634-b332-313863363132__photo_2022-04-02_09-.webp', 'tild6137-6337-4338-a432-623564666266__photo_2022-04-02_09-.webp', 'tild6261-3733-4231-b335-393063373765__photo_2022-04-02_09-.webp', 'tild6466-6562-4265-a665-663462306564__photo_2022-04-02_09-.webp'],
    ),
    'krio': dict(
        title='Крио-кухня',
        subtitle='В формате мастер-класса\n\nНа нашей кухне всё шипит белым паром',
        body='Крио-мороженое\nКогда дети готовят крио-мороженое наша лаборатория окутывается красивым белым азотным паром.\nСахарная вата\nДети сами себе делают сладости на\xa0настоящем аппарате для\xa0приготовления сахарной ваты.\nКосмические кукурузные палочки\nОт\xa0которых идёт пар изо рта.\nЖидкий азот\nДети знакомятся со\xa0свойствами жидкого азота и\xa0проводят эксперименты\n\n120 минут для\xa0компании от\xa010 до\xa015 человек\n\nПосле мастер-класса детки отправляется веселиться в\xa0«Порхай». Где их\xa0ждут посещение трёх бассейнов, все фотозоны, все ростовые фигуры, наша Волшебная комната с\xa0фонариками.',
        images=['tild3363-6264-4365-a633-313836626231__photo_2023-01-11_11-.webp', 'tild3863-3835-4564-b333-653138373030__photo_2023-01-11_11-.webp', 'tild6365-3065-4765-a163-333266326165__photo_2022-07-10_10-.webp', 'tild6366-6265-4966-a434-333638613830__img_1845.webp', 'tild6463-6164-4437-a531-633433656132__img_1854.webp', 'tild6563-3330-4135-a262-356165356362__img_1840.webp'],
    ),
    'pati': dict(
        title='Супер челлендж пати«Порхай»',
        subtitle='120 минут для компаний от 10 до 15 человек',
        body='В одной программе собрано три самых популярных Челленджа!\nКажется нащупал\nУгадай, что налито\nОткуси, лизни, ничего\n\nПосле мастер-класса детки отправляется веселиться в\xa0«Порхай». Где их\xa0ждут посещение трёх бассейнов, все фотозоны, все ростовые фигуры, наша Волшебная комната с\xa0фонариками.\n\nУверены, вы не заметите, как пролетит время.',
        images=['tild3033-6438-4739-b435-623830336236__photo_2022-03-08_18-.webp', 'tild3138-3263-4161-b433-303063356165__img_1741.webp', 'tild3162-6464-4433-b463-643239373939__photo_2022-03-08_18-.webp', 'tild3166-6663-4532-a130-653161633635__photo_2022-04-06_11-.webp', 'tild3565-3736-4731-b735-386630323239__img_1763_1.webp', 'tild3666-3664-4433-b738-316235633136__photo_2022-03-08_18-.webp', 'tild3765-3939-4263-b939-663938323165__photo_2022-03-08_18-.webp', 'tild3834-3265-4661-a666-643537663665__photo_2022-03-08_18-.webp', 'tild3938-3563-4038-a366-383638636238__img_1750.webp', 'tild6130-3035-4264-a636-656330396637__photo_2022-03-08_18-.webp', 'tild6361-6334-4435-b931-373731366631__photo_2022-03-08_18-.webp', 'tild6564-6264-4538-b931-366533666439__photo_2022-03-08_18-.webp', 'tild6661-3965-4733-a531-356137343939__photo_2022-03-08_18-.webp', 'tild6666-3433-4263-a431-333431323931__photo_2022-03-08_18-.webp'],
    ),
    'Tusovka': dict(
        title='Тусовка в «Порхай»',
        subtitle='1 час - 400₽\n2 час - 600₽\nДля групп более 35 человек условия ещё выгоднее',
        body='Идеальное время посетить новое место повеселиться с\xa0друзьями и\xa0сделать кучу крутых фото.\nПриглашаем организованной группы от\xa015 человек (детские центры, летние площадки, группы продлённого дня, лагеря и т д) и\xa0дарим специальные выгодные условия для\xa0детей и\xa0взрослых.\n\nВас ждут:\nТри сухих бассейна\n200 тыс. шаров\n15 супер стильных фотозон\n\nТребуется предварительная запись.\n\nНаполни жизнь забываемых впечатлениями!\nБудут в\xa0восторге все и\xa0дети и\xa0взрослые!',
        images=['tild3033-3535-4432-b934-623538626236__ce4a9472.webp', 'tild3434-6261-4939-a531-636466396534__photo_2023-03-22_08-.webp', 'tild3665-3565-4266-a364-623438653965__photo_2023-03-22_08-.webp', 'tild3666-3735-4564-a239-633633633564__photo_2023-03-22_08-.webp', 'tild3761-3331-4330-a565-343532356566__photo_2023-03-22_15-.webp', 'tild3932-6334-4333-b361-366633613733__photo_2023-03-22_15-.webp', 'tild6236-6632-4638-b762-646661363963__iii_7472_2.webp', 'tild6566-6539-4433-a235-643430353264__ce4a1064.webp', 'tild6662-3663-4234-a435-333737616630__iii_1669_2.webp', 'tild6663-6331-4334-a332-666631363433__iii_9551_3.webp'],
    ),
    'Uensdej': dict(
        title='Интерактивная квест-программа с проектором «Уэнсдей»',
        subtitle='➕ веселье в «Порхай»',
        body='Герои получают таинственные письма с указанием того, что нужно делать. Следуя подсказкам, они перемещаются по школе, используя карту, преодолевает разные испытания и получает магические артефакты!\n\nВ программе\n- таинственная библиотека\n- лодочный турнир\n- семейное древо Адамс\n- зажигательные танцы на школьном балу\n- эксперименты в школьной лаборатории\n- современные хиты в классической обработке в музыкальном зале\n- спиритический сеанс\n- уничтожение Монстра\nИ чтобы наверняка закрепить впечатление, после программы направимся покорять бассейны с шариками.\n\nСкучать времени не будет!',
        images=['tild3039-6162-4133-b238-616331356634__photo_2023-03-08_13-.webp', 'tild3063-3461-4735-b462-666439343430__photo_2023-03-08_13-.webp', 'tild3232-3138-4733-b964-316361306436__photo_2023-03-08_13-.webp', 'tild3435-3130-4065-b234-636633663431__photo_2023-03-08_13-.webp', 'tild3562-3664-4566-a339-656532366637__photo_2023-03-08_13-.webp', 'tild3664-3830-4435-a135-356532306138__photo_2023-03-08_14-.webp', 'tild3732-6565-4839-a530-303136326263__photo_2023-03-08_14-.webp', 'tild3933-6538-4339-a432-633330643638__photo_2023-03-08_13-.webp', 'tild6665-3735-4336-b130-393465336431__photo_2023-03-08_13-.webp'],
    ),
    'CashFlow': dict(
        title='CASHFLOW или Денежный Поток\xa0для вашей компании',
        subtitle='Длительность: 3 часа. Тренинг + игра\nВозрастное ограничение 16+\n\n4 человека - 2 500₽/чел\n6 человек - 2 000₽/чел',
        body='Приглашаем на легендарный ТРЕНИНГ-игру Роберта Кийосаки «Денежный поток», где Вы проработаете свой денежный запрос.\n\nПриходите своей компанией 4-6 человек и прокачайте финансы!\n\nИгру проведет успешный предприниматель, инвестор, эксперт в построении бизнес-процессов Компании, лучший предприниматель в сфере торговли 2021 год. Проведено более двухсот игр с 2015 года.\n\nСвои знания, навыки, умения передаются участникам через игру. Сначала будет мини-тренинг, разъяснение правил, потом сама игра, подведение итогов и обратная связь от ведущего-эксперта.\n\nВ тренинг-игре Вы увидите, как относитесь к деньгам, откуда они приходят, куда уходят, и какие действия нужно совершать для улучшения финансового положения.\n\nС нас чай и конфетки, с вас - хорошее настроение! ;)',
        images=['tild3163-3464-4535-a332-613432396135__photo_2023-03-28_10-.webp'],
    ),
    'Masterklass': dict(
        title='Рисование на футболках',
        subtitle='➕ веселье в «Порхай»',
        body='Приглашаем на творческий мастер-класс всех желающих в наш уютный центр. \n\nПроведение мастер-класса возможно с выездом (на вашей территории) \nВместе узнаем о разных техниках и материалах. Получим классный опыт и впечатления, и самостоятельно распишем футболку по выбранному дизайну. \nА потом повеселимся в «Порхай»\n\nПосле мастер-класса детки отправляется веселиться в\xa0«Порхай». Где их\xa0ждут посещение трёх бассейнов, все фотозоны, все ростовые фигуры, наша Волшебная комната с\xa0фонариками.',
        images=['tild3038-3633-4632-b333-306465396435__photo_54451060745721.webp', 'tild3238-6463-4062-a662-393861356366__photo_54451060745721.webp', 'tild6133-3638-4431-b866-373733373432__photo_54451060745721.webp', 'tild6437-3864-4439-a531-633735313838__photo_54451060745721.webp'],
    ),
}

# Скриншоты отзывов (rec560770489) — прокручиваемая лента без JS-библиотек,
# управление стрелками через element.scrollBy(). Первый файл содержит
# замазанный номер телефона клиента (content/redacted/), это утечка чужих
# персональных данных, поэтому её убираем сразу, без согласования.
REVIEWS = [
    'tild3036-3364-4462-b836-333063396135__photo_2023-02-19_16-.webp',
    'tild3139-6336-4961-b439-303832396662__photo_2023-02-19_16-.webp',
    'tild3163-6263-4363-a433-383636653234__photo_2023-02-19_16-.webp',
    'tild3361-3033-4665-b330-393038343138__photo_2023-03-04_15-.webp',
    'tild3430-3334-4834-b366-336632383438__photo_2023-02-19_16-.webp',
    'tild3466-3335-4161-a431-386532613936__photo_2023-02-19_16-.webp',
    'tild3563-3461-4264-b765-373436643066__photo_2023-02-19_16-.webp',
    'tild3633-3365-4631-b939-353134393532__photo_2023-03-04_15-.webp',
    'tild3738-3338-4363-b964-386430623832__photo_2023-03-04_15-.webp',
    'tild3765-3630-4364-b138-326637333838__image_12.webp',
    'tild3930-3739-4433-b834-663964383238__photo_2023-02-19_16-.webp',
    'tild6138-6134-4864-b033-663261373635__photo_2023-02-19_16-.webp',
    'tild6164-3362-4166-b439-363838303633__photo_2023-02-19_16-.webp',
    'tild6164-3464-4537-a438-333232386339__photo_2023-02-19_16-.webp',
    'tild6632-3632-4031-b365-613162316631__photo_2023-02-19_16-.webp',
    'tild6665-3130-4561-a331-616633663930__photo_2023-02-19_16-.webp',
]

# Стрелка слайдера — та же ломаная, что и в оригинальном компоненте Тильды.
SLIDER_ARROW = ('<svg viewBox="0 0 15.3 29" xmlns="http://www.w3.org/2000/svg">'
                 '<polyline points="0.5,0.5 14.5,14.5 0.5,28.5" fill="none" '
                 'stroke="#4a4a4a" stroke-width="1"/></svg>')

# Мелкий декор первого экрана: (файл, left %, top %, ширина px)
HERO_DECOR = [
    ('tild3534-3832-4661-b631-393736383835__ff62ebf0-cb8e-41b8-8.svg', 13.0, 21.0, 11),
    ('tild6430-6664-4638-b164-373838316663__9e60bd35-1afd-4268-a.svg', 46.4, 18.2, 9),
    ('tild6331-3265-4661-b832-386631333031__53d644a3-b7fc-4a28-9.svg', 48.9, 22.1, 21),
    ('tild3132-3335-4036-b163-623161396662__5e37f9cb-5a6c-42d1-8.svg', 51.2, 21.9, 13),
    ('tild3664-6130-4535-b065-643335633265__561c4767-307a-46f9-9.svg', 61.0, 8.8, 34),
    ('tild3030-6331-4237-b732-626334633432__ca4acacb-b7aa-4c69-8.svg', 42.8, 66.7, 8),
    ('tild3965-3136-4931-b931-366132373463__1ec79619-150c-43cf-a.svg', 49.2, 70.1, 23),
    ('tild3735-3661-4434-b232-356665616664__62cd18bc-e6e5-46d3-a.svg', 89.9, 14.5, 12),
]


def render_tariff_cards(cards):
    """Карточка с двойной рамкой (teal+yellow) и парой круглых фото —
    общий компонент для «Варианты аренды залов» и «Праздники под ключ».
    note/price необязательны — у карточки «Корпоратив» их нет в оригинале."""
    out = []
    for n, t in enumerate(cards):
        note = '<p class="tariff__note">%s</p>' % t['note'] if t['note'] else ''
        price = '<p class="tariff__price">%s</p>' % t['price'] if t['price'] else ''
        out.append(
            '<article class="tariff" style="background:%s" data-anim="zoomin" data-anim-dur="1" data-anim-delay="%.1f">'
            '<span class="tariff__frame tariff__frame--teal"><img src="%stild3031-6236-4236-a561-356461643236__e19497dc-0442-4f7b-b.svg" alt=""></span>'
            '<span class="tariff__frame tariff__frame--yellow"><img src="%stild3934-3735-4063-b837-356461626263__04c0fbd0-c82b-48fb-a.svg" alt=""></span>'
            '<span class="tariff__photo tariff__photo--big"><img src="%s%s" alt="" width="196" height="196"></span>'
            '<span class="tariff__photo tariff__photo--small"><img src="%s%s" alt="" width="162" height="162"></span>'
            '<h3 class="tariff__title">%s</h3>'
            '<p class="tariff__desc">%s</p>'
            '%s%s'
            '<a class="tariff__more" href="%s">Подробнее'
            '<img src="%stild6461-6262-4664-a333-343239356263__arrow_7.svg" alt="" width="20" height="11"></a>'
            '</article>'
            % (t['color'], n * 0.1, IMG, IMG, IMG, t['big'], IMG, t['small'], t['title'], t['desc'],
               note, price, t['href'], IMG))
    return ''.join(out)


def text_to_html(text):
    """Пустая строка внутри текста — абзац, одиночный перенос — <br>."""
    paras = text.split('\n\n')
    return ''.join('<p>%s</p>' % escape(p).replace('\n', '<br>') for p in paras if p.strip())


def render_popups(popups):
    """Поп-ап карточки-программы: заголовок, подзаголовок, текст, галерея.
    Открывается по клику на ссылку href="#popup:KEY" (см. скрипт внизу
    страницы), <dialog> даёт фокус-ловушку и закрытие по Esc бесплатно."""
    out = []
    for key, p in popups.items():
        gallery = ''.join(
            '<img src="%s%s" alt="" loading="lazy" width="260" height="195">' % (IMG, img)
            for img in p['images'])
        out.append(
            '<dialog class="popup" id="popup-%s" aria-label="%s">'
            '<div class="popup__box">'
            '<button class="popup__close" type="button" data-popup-close>Назад</button>'
            '<h3 class="popup__title">%s</h3>'
            '<div class="popup__subtitle">%s</div>'
            '<div class="popup__text">%s</div>'
            '<div class="popup__gallery">%s</div>'
            '</div>'
            '</dialog>'
            % (key, escape(p['title']), escape(p['title']), text_to_html(p['subtitle']),
               text_to_html(p['body']), gallery))
    return ''.join(out)


def build():
    nav = ''.join('<li><a class="nav__link" href="%s">%s</a></li>' % (h, t) for t, h in NAV)

    # Мелкий декор первого экрана мерцает по кругу: прозрачность 1 -> 0,15 -> 1
    # с поворотом на 25°. Длительности в оригинале у всех разные.
    twinkle = [2000, 2000, 1500, 1100, 2000, 3200, 2600, 2600]
    decor = ''.join(
        '<span class="decor" style="left:%s%%;top:%s%%;width:%dpx" data-twinkle="%d">'
        '<img src="%s%s" alt=""></span>' % (x, y, w, twinkle[i % len(twinkle)], IMG, f)
        for i, (f, x, y, w) in enumerate(HERO_DECOR))
    decor += ('<span class="decor decor--dot" style="left:44.5%;top:76.4%;'
              'width:59px;height:59px"></span>')
    decor += ('<span class="decor decor--dot" style="left:50.8%;top:76.4%;'
              'width:59px;height:59px"></span>')

    cards = ''.join(
        '<figure class="card" data-anim="zoomin" data-anim-dur="1.3" data-anim-delay="%.2f">' % (n * 0.15) +
        '<span class="card__frame card__frame--teal">'
        '<img src="%stild3665-3464-4535-b763-386533363061__svg4.svg" alt=""></span>'
        '<span class="card__frame card__frame--yellow">'
        '<img src="%stild6338-3565-4263-b539-323163613235__svg3.svg" alt=""></span>'
        '<span class="card__photo" style="background-image:url(%s%s)" role="img" '
        'aria-label="%s"></span>'
        '<span class="card__plate">'
        '<img src="%stild3661-3566-4834-a234-336436346262__photo.webp" alt=""></span>'
        '<figcaption class="card__caption">%s</figcaption>'
        '</figure>' % (IMG, IMG, IMG, img, cap.replace('"', '&quot;'), IMG, cap)
        for n, (img, cap) in enumerate(CARDS))

    steps = ''.join(
        '<div class="step" data-anim="zoomin" data-anim-dur="1" data-anim-delay="%.2f">%s'
        '<span class="step__icon"><img src="%s%s" alt="" '
        'width="120" height="120"></span><p class="step__title">%s</p></div>'
        % (n * 0.15, STEP_ARROW if n else '', IMG, icon, title)
        for n, (icon, title) in enumerate(STEPS))

    tariffs = render_tariff_cards(TARIFFS)
    keys = render_tariff_cards(KEYS)

    groups = ''.join(
        '<a class="group" href="#popup:%s" data-anim="zoomin" data-anim-dur="1.2" data-anim-delay="%.1f">'
        '<span class="group__icon"><img src="%s%s" alt="" width="134" height="134"></span>'
        '<h3 class="group__title">%s</h3>'
        '<span class="group__more">Подробнее'
        '<img src="%stild6461-6262-4664-a333-343239356263__arrow_7.svg" alt="" width="20" height="11"></span>'
        '</a>'
        % (popup, n * 0.1, IMG, img, title, IMG)
        for n, (img, popup, title) in enumerate(GROUPS))

    popups = render_popups(POPUPS)

    reviews = ''.join(
        '<img src="%s%s" alt="" loading="lazy" width="260">' % (IMG, img)
        for img in REVIEWS)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Развлекательный центр «Порхай»</title>
<meta name="description" content="Проведение различных мероприятий: от дней рождений и выпускных до взрослых корпоративов и романтических свиданий, во Владивостоке">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<script>document.documentElement.className+=' js'</script>

<header class="header" id="header">
  <div class="stage header__inner">
    <a class="header__logo" href="/" aria-label="Порхай — на главную">
      <img src="{IMG}tild3166-3639-4666-b462-333535343563__photo.svg" alt="Порхай" width="150" height="46">
    </a>
    <nav class="nav" aria-label="Основная навигация">
      <ul class="nav__list">{nav}</ul>
    </nav>
    <a class="btn btn--teal header__cta" href="#zayavka">Забронировать зал</a>
    <button class="burger" type="button" aria-label="Меню" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<main>
  <section class="hero">
    <div class="stage hero__stage">
      <div class="hero__content">
        <img class="hero__flag" src="{IMG}tild3236-6461-4137-a165-663934353632__b8bca4c5-59d4-4e8a-a.svg" alt="" width="154" height="113" data-anim="zoomin" data-anim-dur="1" data-anim-delay=".6">
        <h1 class="hero__title" data-anim="fadeinright" data-anim-dur="1.7">Развлекательный центр для всей семьи</h1>
        <p class="hero__text" data-anim="fadeinright" data-anim-dur="1.7" data-anim-delay=".2">Проведение мероприятий <b>во&nbsp;Владивостоке</b>: от&nbsp;дней рождений и&nbsp;выпускных до&nbsp;взрослых корпоративов и&nbsp;романтических свиданий</p>
        <a class="btn btn--yellow hero__cta" href="#zayavka" data-anim="zoomin" data-anim-dur="2.4" data-anim-delay=".4">Записаться</a>
      </div>
      <div class="hero__art">
        <img src="{IMG}tild6638-3864-4939-b336-646563633937__svg.svg" alt="" width="511" height="511" data-drift="20,0">
        <img src="{IMG}tild6466-3632-4763-b135-636461656535__svg2.svg" alt="" width="511" height="511" data-drift="-20,0">
        <img src="{IMG}tild3463-6130-4836-a539-636430646232__vector.webp" alt="Дети в бассейне с шариками" width="496" height="497">
      </div>
      {decor}
    </div>
  </section>

  {band()}

  <section class="section">
    <div class="stage">
      <div class="section__head">
        <h2 class="section__title" data-anim="fadeinup" data-anim-dur="1">Мы делаем ваш праздник ярче</h2>
        <p class="section__lead" data-anim="fadeinup" data-anim-dur="1" data-anim-delay=".15">В «Порхай» есть всё необходимое, чтобы вам осталось только наслаждаться идеальным праздником без нервов и&nbsp;траты времени на&nbsp;организационные моменты</p>
      </div>
      <div class="cards">{cards}</div>
    </div>
  </section>

  {band(flip=True)}

  <section class="section section--mint section--steps">
    <div class="stage">
      <div class="section__head">
        <h2 class="section__title">Организуйте праздник в 4 шага:</h2>
      </div>
      <div class="steps">{steps}</div>
    </div>
  </section>

  {band()}

  <section class="section section--tariffs" id="zaly">
    <div class="stage">
      <div class="section__head">
        <h2 class="section__title" data-anim="fadeinup" data-anim-dur="1">Варианты аренды залов</h2>
        <p class="section__lead" data-anim="fadeinup" data-anim-dur="1" data-anim-delay=".15">Без организации мероприятия и&nbsp;шоу-программы</p>
      </div>
      <div class="tariffs">{tariffs}</div>
    </div>
  </section>

  <section class="section section--tariffs section--keys" id="pod-kluch">
    <div class="stage">
      <div class="section__head">
        <h2 class="section__title" data-anim="fadeinup" data-anim-dur="1">Праздники «под ключ»</h2>
        <p class="section__lead" data-anim="fadeinup" data-anim-dur="1" data-anim-delay=".15">Аниматор/шоу-программа и&nbsp;фотограф включены в&nbsp;стоимость</p>
      </div>
      <div class="tariffs">{keys}</div>
    </div>
  </section>

  {band(flip=True)}

  <section class="section section--groups section--mint" id="dlyagrupp">
    <div class="stage">
      <h2 class="section__title" data-anim="fadeinup" data-anim-dur="1">Предложения для организованных групп</h2>
      <div class="groups">{groups}</div>
    </div>
  </section>

  {band()}

  <section class="section" id="otziv">
    <div class="stage">
      <h2 class="section__title" data-anim="fadeinup" data-anim-dur="1">Отзывы ❤️</h2>
      <div class="reviews">
        <button class="reviews__arrow reviews__arrow--prev" type="button" aria-label="Предыдущий отзыв">{SLIDER_ARROW}</button>
        <div class="reviews__track">{reviews}</div>
        <button class="reviews__arrow reviews__arrow--next" type="button" aria-label="Следующий отзыв">{SLIDER_ARROW}</button>
      </div>
    </div>
  </section>
</main>

{popups}

<script>
(function () {{
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.getElementById('header');

  // 1. Появление при прокрутке: fadeinright / fadeinup / zoomin.
  var appear = [].slice.call(document.querySelectorAll('[data-anim]'));
  function show(el) {{
    el.style.transitionDuration = (el.dataset.animDur || 1) + 's';
    el.style.transitionDelay = (el.dataset.animDelay || 0) + 's';
    el.classList.add('is-in');
  }}
  if (reduce || !('IntersectionObserver' in window)) {{
    appear.forEach(function (el) {{ el.classList.add('is-in'); }});
  }} else {{
    var seen = false;
    var io = new IntersectionObserver(function (list) {{
      list.forEach(function (e) {{
        if (!e.isIntersecting) return;
        seen = true;
        show(e.target);
        io.unobserve(e.target);
      }});
    }}, {{ rootMargin: '0px 0px -12% 0px' }});
    appear.forEach(function (el) {{ io.observe(el); }});
    // Страховка: если наблюдатель за три секунды не отдал ни одного события,
    // показываем всё как есть. Пустая страница хуже, чем несыгравшая анимация.
    setTimeout(function () {{
      if (seen) return;
      appear.forEach(function (el) {{ el.classList.add('is-in'); }});
    }}, 3000);
  }}

  // 2. Мерцание мелкого декора: прозрачность 1 -> 0,15 -> 1 с поворотом.
  if (!reduce && document.body.animate) {{
    [].slice.call(document.querySelectorAll('[data-twinkle]')).forEach(function (el) {{
      el.animate([
        {{ opacity: 1, transform: 'rotate(0deg)' }},
        {{ opacity: .15, transform: 'rotate(25deg)' }},
        {{ opacity: 1, transform: 'rotate(0deg)' }}
      ], {{ duration: +el.dataset.twinkle * 2, iterations: Infinity, easing: 'ease-in-out' }});
    }});
  }}

  // 3. Дрейф по прокрутке: шарики и чёрточки уезжают вправо и проворачиваются,
  //    пока проходят через экран, затем возвращаются.
  var drift = [].slice.call(document.querySelectorAll('[data-drift]'));
  var queued = false;
  function paint() {{
    queued = false;
    var vh = innerHeight;
    for (var i = 0; i < drift.length; i++) {{
      var el = drift[i], r = el.getBoundingClientRect();
      if (r.bottom < -240 || r.top > vh + 240) continue;
      var p = 1 - (r.top + r.height / 2) / (vh + r.height);
      var wave = Math.sin(Math.max(0, Math.min(1, p)) * Math.PI);
      var d = el.dataset.drift.split(',');
      el.style.transform = 'translateX(' + (d[0] * wave).toFixed(2) + 'px)'
                         + ' rotate(' + (d[1] * wave).toFixed(2) + 'deg)';
    }}
  }}
  function onScroll() {{
    header.classList.toggle('is-stuck', scrollY > 40);
    if (!queued && !reduce) {{ queued = true; requestAnimationFrame(paint); }}
  }}
  onScroll();
  if (!reduce) paint();
  addEventListener('scroll', onScroll, {{ passive: true }});
  addEventListener('resize', onScroll, {{ passive: true }});

  // 4. Поп-апы программ: открываются по ссылкам href="#popup:KEY".
  //    <dialog> сам даёт фокус-ловушку и закрытие по Esc.
  document.querySelectorAll('a[href^="#popup:"]').forEach(function (a) {{
    a.addEventListener('click', function (e) {{
      e.preventDefault();
      var dlg = document.getElementById('popup-' + a.getAttribute('href').split(':')[1]);
      if (dlg) dlg.showModal();
    }});
  }});
  document.querySelectorAll('.popup').forEach(function (dlg) {{
    dlg.querySelector('[data-popup-close]').addEventListener('click', function () {{ dlg.close(); }});
    dlg.addEventListener('click', function (e) {{ if (e.target === dlg) dlg.close(); }});
  }});

  // 5. Лента отзывов: стрелки листают на ширину видимой области.
  var track = document.querySelector('.reviews__track');
  if (track) {{
    document.querySelector('.reviews__arrow--prev').addEventListener('click', function () {{
      track.scrollBy({{ left: -track.clientWidth * .8, behavior: 'smooth' }});
    }});
    document.querySelector('.reviews__arrow--next').addEventListener('click', function () {{
      track.scrollBy({{ left: track.clientWidth * .8, behavior: 'smooth' }});
    }});
  }}
}})();
</script>
</body>
</html>
"""
    path = os.path.join(HERE, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('index.html собран:', len(html), 'байт')


if __name__ == '__main__':
    build()
