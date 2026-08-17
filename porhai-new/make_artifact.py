# -*- coding: utf-8 -*-
"""
Готовит страницу для публикации по ссылке: всё содержимое вшивается
в один файл без обёртки <html>/<head>/<body> — её добавляет площадка.

Шрифт вшивается, если файлы лежат в assets/fonts. Если их нет, остаётся
ссылка на CDN (на опубликованной странице она будет заблокирована,
и текст отрисуется системным шрифтом).

Запуск:  python make_artifact.py
"""
import os, re, base64, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

MIME = {'.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.woff': 'font/woff', '.woff2': 'font/woff2'}

FONTS = ['Evolventa-Regular.woff', 'Evolventa-Bold.woff']


def datauri(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (MIME.get(ext, 'application/octet-stream'),
                                      base64.b64encode(f.read()).decode())


def main():
    html = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
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
    title = re.search(r'<title>(.*?)</title>', html, re.S)
    title = title.group(1) if title else 'Порхай'
    body = re.search(r'<body[^>]*>(.*)</body>', html, re.S).group(1)

    # charset должен попасть в первый килобайт файла, иначе кириллица
    # рискует отрисоваться в чужой кодировке
    out = ('<meta charset="utf-8">\n<title>%s</title>\n<style>\n%s\n</style>\n%s\n'
           % (title, css, body))

    path = os.path.join(HERE, 'porhai-artifact.html')
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
