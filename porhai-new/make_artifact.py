# -*- coding: utf-8 -*-
"""
Готовит страницу для публикации по ссылке: всё содержимое вшивается
в один файл без обёртки <html>/<head>/<body> — её добавляет площадка.

Шрифт вшивается, если файлы лежат в assets/fonts. Если их нет, остаётся
ссылка на CDN (на опубликованной странице она будет заблокирована,
и текст отрисуется системным шрифтом).

Каждая страница публикуется отдельным артефактом — ссылки между
страницами (шапка/подвал/меню) внутри артефакта не работают, это
ограничение площадки (нет роутинга для нескольких файлов в одной
публикации), не баг вёрстки.

Запуск:  python make_artifact.py [имя.html]   (по умолчанию index.html)
"""
import os, re, base64, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

MIME = {'.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.woff': 'font/woff', '.woff2': 'font/woff2'}

FONTS = ['Evolventa-Regular.woff', 'Evolventa-Bold.woff']

# Короткие имена для заголовка артефакта (title в <head> у самих страниц —
# длинные SEO-формулировки, для галереи артефактов нужны короткие).
SHORT_TITLE = {
    'index': 'Порхай',
    'privacy': 'Порхай: политика конфиденциальности',
    'razovoe': 'Порхай: разовое посещение',
    'whiteroom': 'Порхай: White Room',
    'loftbox': 'Порхай: Loft Box',
    'combo': 'Порхай: Комбо+',
    'denrozhdeniya': 'Порхай: день рождения',
    'vypusknye': 'Порхай: выпускной',
    'korporativ': 'Порхай: корпоратив',
    'partner': 'Порхай: партнёры',
    'pakety': 'Порхай: все пакеты',
    'podarok': 'Порхай: подарок',
    '404': 'Порхай: страница 404',
}


def datauri(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (MIME.get(ext, 'application/octet-stream'),
                                      base64.b64encode(f.read()).decode())


def main():
    page = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
    html = open(os.path.join(HERE, page), encoding='utf-8').read()
    css = open(os.path.join(HERE, 'assets', 'style.css'), encoding='utf-8').read()

    # --- шрифт ---
    fdir = os.path.join(HERE, 'assets', 'fonts')
    embedded = 0
    for name in FONTS:
        p = os.path.join(fdir, name)
        if os.path.exists(p):
            css = css.replace("url('fonts/%s')" % name, "url('%s')" % datauri(p))
            embedded += 1

    # --- картинки ---
    used = set(re.findall(r'src="(assets/img/[^"]+)"', html))
    used |= set(re.findall(r'url\((assets/img/[^)]+)\)', html))
    for rel in sorted(used):
        p = os.path.join(HERE, rel.replace('/', os.sep))
        if os.path.exists(p):
            html = html.replace(rel, datauri(p))

    # --- снимаем обёртку документа ---
    stem = os.path.splitext(page)[0]
    title = SHORT_TITLE.get(stem, 'Порхай')
    body = re.search(r'<body[^>]*>(.*)</body>', html, re.S).group(1)

    # charset должен попасть в первый килобайт файла, иначе кириллица
    # рискует отрисоваться в чужой кодировке
    out = ('<meta charset="utf-8">\n<title>%s</title>\n<style>\n%s\n</style>\n%s\n'
           % (title, css, body))

    out_name = 'porhai-artifact.html' if stem == 'index' else 'porhai-artifact-%s.html' % stem
    path = os.path.join(HERE, out_name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)
    print('готово:', os.path.basename(path), '—', round(len(out.encode()) / 1024), 'КБ')
    print('шрифт вшит:', 'да (%d файла)' % embedded if embedded else 'НЕТ — останется CDN')
    left = set(re.findall(r'https?://[^"\')\s]+', out))
    print('внешних ссылок осталось:', len(left))
    for u in sorted(left):
        print('   ', u[:95])


if __name__ == '__main__':
    main()
