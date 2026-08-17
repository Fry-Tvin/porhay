# -*- coding: utf-8 -*-
"""
Собирает автономный одностраничник: CSS, шрифт и картинки вшиваются
в один HTML-файл. Нужен только чтобы показать результат без сервера —
на боевой сайт идёт обычная сборка из build.py.

Запуск:  python make_standalone.py
"""
import os, re, base64, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

MIME = {'.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}


def datauri(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (MIME.get(ext, 'application/octet-stream'),
                                      base64.b64encode(f.read()).decode())


def main():
    html = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
    css = open(os.path.join(HERE, 'assets', 'style.css'), encoding='utf-8').read()

    # Локальных копий шрифта пока нет — в демо оставляем только адрес CDN,
    # чтобы Evolventa подхватилась и типографика была настоящей.
    css = re.sub(r"\s*url\('fonts/[^']+'\) format\('woff2?'\),", '', css)

    # картинки -> data URI
    used = set(re.findall(r'src="(assets/img/[^"]+)"', html))
    used |= set(re.findall(r'url\((assets/img/[^)]+)\)', html))
    for rel in sorted(used):
        p = os.path.join(HERE, rel.replace('/', os.sep))
        if not os.path.exists(p):
            print('  нет файла:', rel)
            continue
        html = html.replace(rel, datauri(p))

    html = html.replace('<link rel="stylesheet" href="assets/style.css">',
                        '<style>\n%s\n</style>' % css)

    out = os.path.join(HERE, 'porhai-glavnaya-demo.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print('готово:', os.path.basename(out), '—', round(os.path.getsize(out) / 1024), 'КБ')


if __name__ == '__main__':
    main()
