"""Build responsive gallery WebP variants without changing source photographs.

Run before build.py after adding gallery photos. Outputs and the manifest are
checked in, so the normal HTML build does not depend on Pillow at deploy time.
"""
from pathlib import Path
import json
import runpy
from PIL import Image, ImageOps


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / 'assets' / 'gallery'
WIDTHS = (480, 960, 1600)


def main():
    data = runpy.run_path(str(HERE / 'build.py'))
    sources = set()
    for name in ('RAZOVOE_GALLERY', 'DR_GALLERY', 'VP_GALLERY', 'KP_GALLERY', 'GF_GALLERY'):
        sources.update(data[name])
    for page in data['RENTAL_PAGES'].values():
        sources.update(page['gallery'])
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for index, name in enumerate(sorted(sources), 1):
        source = HERE / 'assets' / 'img' / name
        with Image.open(source) as original:
            image = ImageOps.exif_transpose(original)
            width, height = image.size
            variants = []
            for target_width in sorted({min(value, width) for value in WIDTHS}):
                target_height = max(1, round(height * target_width / width))
                filename = source.stem + '-%d.webp' % target_width
                target = OUTPUT / filename
                image.resize((target_width, target_height), Image.Resampling.LANCZOS).save(
                    target, format='WEBP', quality=82, method=4)
                variants.append({'src': 'assets/gallery/' + filename,
                                 'width': target_width, 'height': target_height})
            fallback = min(variants, key=lambda item: abs(item['width'] - 960))
            manifest[name] = {'width': width, 'height': height,
                              'src': fallback['src'], 'variants': variants}
        if index % 15 == 0:
            print('Gallery sources prepared: %d/%d' % (index, len(sources)), flush=True)
    (OUTPUT / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Responsive galleries ready: %d photos' % len(manifest), flush=True)


if __name__ == '__main__':
    main()
