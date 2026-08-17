# -*- coding: utf-8 -*-
"""
Сборка index.html для РЦ «Порхай».

Раскладка декоративных лент снята с оригинального сайта на Тильде
(отрисованные координаты, а не атрибуты разметки) и вынесена в данные,
чтобы 8 одинаковых лент не дублировались в разметке восемь раз.

Запуск:  python build.py
"""
import os

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

# Мелкие цветные кляксы: (x %, y px, ширина px, ключ файла, поворот °)
CONFETTI = [
    (7.08, -42, 16, 'd4abbe9e', -19), (10.58, -9, 16, '24e3675d', 0),
    (16.50, -39, 16, 'ceeef3f3', 0), (24.00, -20, 16, 'ba8b36e1', 0),
    (33.83, 1, 16, '13fdaa4f', 0), (36.91, -32, 16, 'a5847e0b', 0),
    (44.41, -7, 16, 'c5a30fb3', -13), (54.49, -33, 16, 'fe3676d5', -28),
    (59.66, 5, 16, '4bfa8c73', -10), (68.91, -36, 16, 'ce4b55ff', -13),
    (73.40, -15, 16, '8c2a0952', 0), (78.82, -17, 16, '9cae1dcb', -12),
    (86.49, -39, 16, 'd4abbe9e', -32), (90.49, -7, 16, '24e3675d', 0),
    (95.90, -37, 16, 'ceeef3f3', -20),
]


def band(flip=False):
    """Лента-разделитель. flip=True — кляксы свисают вниз (вариант Б)."""
    out = ['<div class="band" aria-hidden="true"><div class="band__inner">']
    for x, y in BUBBLES:
        out.append('<span class="band__bubble" style="left:%s%%;top:%dpx"></span>' % (x, y))
    for x, y, w, key, rot in CONFETTI:
        yy = -y + 6 if flip else y
        rr = rot + 180 if flip else rot
        style = 'left:%s%%;top:%dpx;width:%dpx' % (x, yy, w)
        if rr:
            style += ';transform:rotate(%ddeg)' % rr
        out.append('<span class="band__bit" style="%s"><img src="%s%s" alt=""></span>'
                   % (style, IMG, BIT[key]))
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

CARDS = [
    ('tild6631-6164-4662-a432-643636393437__f8b680e9-d185-4e5c-a.webp',
     '3 сухих бассейна: Белый бассейн, «Попкорн» и «Арбуз»'),
    ('tild6631-6530-4933-a263-616162353439__rectangle_10.webp',
     'Cтильные фотозоны и Ростовые фигуры'),
    ('tild3662-3462-4531-b130-666539343532__rectangle_13.webp',
     'Наша волшебная комната с фонариками'),
]

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


def build():
    nav = ''.join('<li><a class="nav__link" href="%s">%s</a></li>' % (h, t) for t, h in NAV)

    decor = ''.join(
        '<span class="decor" style="left:%s%%;top:%s%%;width:%dpx">'
        '<img src="%s%s" alt=""></span>' % (x, y, w, IMG, f)
        for f, x, y, w in HERO_DECOR)
    decor += ('<span class="decor decor--dot" style="left:44.5%;top:76.4%;'
              'width:59px;height:59px"></span>')
    decor += ('<span class="decor decor--dot" style="left:50.8%;top:76.4%;'
              'width:59px;height:59px"></span>')

    cards = ''.join(
        '<figure class="card">'
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
        for img, cap in CARDS)

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
        <img class="hero__flag" src="{IMG}tild3236-6461-4137-a165-663934353632__b8bca4c5-59d4-4e8a-a.svg" alt="" width="154" height="113">
        <h1 class="hero__title">Развлекательный центр для всей семьи</h1>
        <p class="hero__text"><b>Проведение мероприятий во Владивостоке</b>: от дней
          рождений и выпускных до взрослых корпоративов и романтических свиданий</p>
        <a class="btn btn--yellow hero__cta" href="#zayavka">Записаться</a>
      </div>
      <div class="hero__art">
        <img src="{IMG}tild6638-3864-4939-b336-646563633937__svg.svg" alt="" width="511" height="511">
        <img src="{IMG}tild6466-3632-4763-b135-636461656535__svg2.svg" alt="" width="511" height="511">
        <img src="{IMG}tild3463-6130-4836-a539-636430646232__vector.webp" alt="Дети в бассейне с шариками" width="496" height="497">
      </div>
      {decor}
    </div>
  </section>

  {band()}

  <section class="section">
    <div class="stage">
      <div class="section__head">
        <h2 class="section__title">Мы делаем ваш праздник ярче</h2>
        <p class="section__lead">В «Порхай» есть всё необходимое, чтобы вам осталось
          только наслаждаться идеальным праздником без нервов и траты времени на
          организационные моменты</p>
      </div>
      <div class="cards">{cards}</div>
    </div>
  </section>

  {band(flip=True)}

  <section class="section section--mint">
    <div class="stage">
      <div class="section__head">
        <h2 class="section__title">Организуйте праздник в 4 шага:</h2>
      </div>
    </div>
  </section>
</main>

<script>
// Шапка становится плотной после прокрутки первого экрана.
(function () {{
  var h = document.getElementById('header');
  var onScroll = function () {{ h.classList.toggle('is-stuck', window.scrollY > 40); }};
  onScroll();
  addEventListener('scroll', onScroll, {{ passive: true }});
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
