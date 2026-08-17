# -*- coding: utf-8 -*-
"""
Пережимает растровые картинки, которые использует index.html, в WebP
под реальный размер отображения (с запасом x2 под retina).

SVG не трогает — они и так по 300–400 байт.
Запуск:  python optimize_images.py
"""
import os, re, sys, shutil
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets', 'img')

# файл -> ширина отображения в вёрстке (умножаем на 2 под плотные экраны)
DISPLAY_WIDTH = {
    'tild6631-6164-4662-a432-643636393437__f8b680e9-d185-4e5c-a.png': 335,
    'tild6631-6530-4933-a263-616162353439__rectangle_10.png': 335,
    'tild3662-3462-4531-b130-666539343532__rectangle_13.png': 335,
    'tild3463-6130-4836-a539-636430646232__vector.png': 511,
}
RETINA = 2
QUALITY = 82


def collect():
    html = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
    srcs = set(re.findall(r'src="([^"]+)"', html)) | set(re.findall(r'url\(([^)]+)\)', html))
    return sorted({s for s in srcs if 'images/' in s})


def main():
    os.makedirs(OUT, exist_ok=True)
    total_before = total_after = 0
    rows = []

    for rel in collect():
        src = os.path.join(HERE, rel.replace('/', os.sep))
        name = os.path.basename(src)
        if not os.path.exists(src):
            print('  пропуск (нет файла):', name)
            continue

        before = os.path.getsize(src)

        if name.lower().endswith('.svg'):
            dst = os.path.join(OUT, name)
            shutil.copy2(src, dst)
            after = os.path.getsize(dst)
        else:
            im = Image.open(src)
            target = DISPLAY_WIDTH.get(name)
            if target:
                target *= RETINA
                if im.width > target:
                    h = round(im.height * target / im.width)
                    im = im.resize((target, h), Image.LANCZOS)
            if im.mode in ('P', 'LA'):
                im = im.convert('RGBA')
            dst = os.path.join(OUT, os.path.splitext(name)[0] + '.webp')
            im.save(dst, 'WEBP', quality=QUALITY, method=6)
            after = os.path.getsize(dst)

        total_before += before
        total_after += after
        if before > 40_000:
            rows.append((name, before, after))

    rows.sort(key=lambda r: -r[1])
    print('%-46s %10s %10s %s' % ('файл', 'было', 'стало', 'экономия'))
    for name, b, a in rows:
        print('%-46s %7.0f КБ %7.0f КБ  −%d%%'
              % (name[:46], b / 1024, a / 1024, round((1 - a / b) * 100)))
    print('-' * 82)
    print('ИТОГО: %.2f МБ → %.2f МБ  (−%d%%)'
          % (total_before / 1048576, total_after / 1048576,
             round((1 - total_after / total_before) * 100)))


if __name__ == '__main__':
    main()
