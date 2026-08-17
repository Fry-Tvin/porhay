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
SRC = os.path.join(os.path.dirname(HERE), 'porhai-eds', 'images')

# файл -> ширина отображения в вёрстке (умножаем на 2 под плотные экраны)
DISPLAY_WIDTH = {
    'tild6631-6164-4662-a432-643636393437__f8b680e9-d185-4e5c-a.png': 335,
    'tild6631-6530-4933-a263-616162353439__rectangle_10.png': 335,
    'tild3662-3462-4531-b130-666539343532__rectangle_13.png': 335,
    'tild3463-6130-4836-a539-636430646232__vector.png': 511,
    'tild6139-6135-4965-b164-663136663630__6c636ea6-a060-4fcf-9.png': 196,
    'tild6364-3665-4162-a166-633932326531__9a1357ad-f456-47ed-8.png': 162,
    'tild3866-3833-4662-a438-323839343863__ellipse_46.png': 196,
    'tild6136-3362-4834-b234-663035363664__ellipse_45.png': 162,
    'tild3632-3630-4962-b133-326461616532__ellipse_39.png': 196,
    'tild3764-6136-4033-a235-646232373930__ellipse_38.png': 162,
    'tild6262-3832-4039-a364-343835613338__ellipse_34-1.png': 196,
    'tild3138-3237-4938-b536-343663643239__ellipse_35-1.png': 162,
    'tild3939-6462-4031-a365-626561303136__ellipse_34.png': 196,
    'tild3434-6363-4566-a530-396430336365__ellipse_37.png': 162,
    'tild3932-6239-4463-b232-616230636431__ellipse_43.png': 196,
    'tild3831-6137-4662-a462-383763353036__ellipse_34.png': 162,
}
RETINA = 2
QUALITY = 82


def collect():
    html = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
    srcs = set(re.findall(r'src="([^"]+)"', html)) | set(re.findall(r'url\(([^)]+)\)', html))
    return sorted({os.path.basename(s) for s in srcs if 'assets/img/' in s})


def find_source(name):
    """Готовые файлы в assets/img называются по исходнику, но .png/.jpg
    из экспорта у svg сохраняют расширение, а у растра меняют на .webp —
    ищем исходник в экспорте по имени без расширения."""
    stem = os.path.splitext(name)[0]
    if name.lower().endswith('.svg'):
        p = os.path.join(SRC, name)
        return p if os.path.exists(p) else None
    for ext in ('.png', '.jpg', '.jpeg'):
        p = os.path.join(SRC, stem + ext)
        if os.path.exists(p):
            return p
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    total_before = total_after = 0
    rows = []

    for name in collect():
        src = find_source(name)
        if not src:
            print('  пропуск (нет исходника в экспорте):', name)
            continue

        before = os.path.getsize(src)

        if name.lower().endswith('.svg'):
            dst = os.path.join(OUT, name)
            shutil.copy2(src, dst)
            after = os.path.getsize(dst)
        else:
            im = Image.open(src)
            target = DISPLAY_WIDTH.get(os.path.basename(src))
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
