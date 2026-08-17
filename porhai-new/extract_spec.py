# -*- coding: utf-8 -*-
"""
Снимает спецификацию вёрстки с экспорта Тильды в JSON.

Зачем: чтобы верстать секции по числам, а не «на глаз». Тильда кладёт
в страницу полный CSS каждого блока вместе со всеми брейкпоинтами
(1919 / 1199 / 959 / 639 / 479), поэтому спека получается точнее,
чем замеры в браузере, и снимается без браузера вообще.

Запуск:  python extract_spec.py
Итог:    spec/pageNNNNNN.json + spec/_index.json
"""
import os, re, json, html, sys
from collections import OrderedDict

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'porhai-eds'))
OUT = os.path.join(HERE, 'spec')

BREAKPOINTS = ['base', '1919', '1199', '959', '639', '479']

# Ловушка Тильды: медиазапросы в CSS названы по max-width (1919, 1199, …),
# а координаты в разметке — по ширине сетки макета (res-1200, res-960, …).
# Это одни и те же брейкпоинты под разными именами.
GRID_OF = {'1919': '1200', '1199': '960', '959': '640', '639': '480', '479': '320'}

# читаемые названия типов блоков Тильды, которые реально встречаются
RECORD_KIND = {
    '396': 'зеро-блок (свободное позиционирование)',
    '257': 'меню, фиксированное сверху',
    '451': 'мобильное меню',
    '702': 'форма в поп-апе',
    '549': 'плитка шагов',
    '604': 'слайдер',
    '979': 'галерея',
    '595': 'сетка логотипов',
    '668': 'аккордеон (FAQ)',
    '555': 'контакты с картой',
    '992': 'подвал',
    '898': 'плавающая кнопка связи',
    '750': 'поп-ап',
    '215': 'якорь',
    '131': 'произвольный код',
    '270': 'служебный блок',
    '360': 'служебный блок',
}


def split_css(css):
    """Разбирает CSS на (брейкпоинт -> {селектор: {свойство: значение}})."""
    out = {bp: {} for bp in BREAKPOINTS}

    def harvest(chunk, bp):
        for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', chunk):
            sel = sel.strip()
            if not sel or not body.strip():
                continue
            props = out[bp].setdefault(sel, {})
            for decl in body.split(';'):
                if ':' in decl:
                    k, _, v = decl.partition(':')
                    props[k.strip()] = v.strip()

    # вырезаем медиа-блоки, остаток — базовые правила
    pos, rest = 0, []
    for m in re.finditer(r'@media[^{]*\{', css):
        start = m.start()
        rest.append(css[pos:start])
        # ищем парную закрывающую скобку
        depth, i = 0, m.end() - 1
        while i < len(css):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        inner = css[m.end():i]
        width = re.search(r'max-width\s*:\s*(\d+)px', m.group(0))
        bp = width.group(1) if width and width.group(1) in BREAKPOINTS else 'base'
        harvest(inner, bp)
        pos = i + 1
    rest.append(css[pos:])
    harvest(''.join(rest), 'base')
    return out


def clean_text(s):
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).replace('‌', '').strip()


def parse_page(path):
    raw = open(path, encoding='utf-8', errors='replace').read()
    recs = [(m.group(1), m.group(2), m.start()) for m in re.finditer(
        r'<div id="(rec\d+)" class="r [^"]*" [^>]*data-record-type="(\d+)"', raw)]

    blocks = []
    for n, (rid, rtype, pos) in enumerate(recs):
        end = recs[n + 1][2] if n + 1 < len(recs) else len(raw)
        seg = raw[pos:end]
        css = ''.join(re.findall(r'<style[^>]*>(.*?)</style>', seg, re.S))
        rules = split_css(css)

        block = OrderedDict()
        block['id'] = rid
        block['type'] = rtype
        block['kind'] = RECORD_KIND.get(rtype, 'блок ' + rtype)
        block['order'] = n + 1

        # высота и фон артборда по брейкпоинтам
        heights, bg = OrderedDict(), None
        for bp in BREAKPOINTS:
            for sel, props in rules[bp].items():
                if 't396__artboard' in sel:
                    h = props.get('height') or props.get('min-height')
                    if h:
                        heights[bp] = h
                    if props.get('background-color'):
                        bg = props['background-color']
        if heights:
            block['height'] = heights
        if bg:
            block['background'] = bg

        # элементы зеро-блока
        els = []
        for m in re.finditer(r"<div class='t396__elem tn-elem[^']*'\s+data-elem-id='(\d+)'"
                             r"\s+data-elem-type='(\w+)'([^>]*)>", seg):
            eid, etype, attrs = m.group(1), m.group(2), m.group(3)
            fields = dict(re.findall(r'data-field-([\w-]+)-value="([^"]*)"', attrs))

            el = OrderedDict()
            el['id'] = eid
            el['type'] = etype
            # координаты по брейкпоинтам: left/top/width/height (+ res-NNN варианты)
            geo = OrderedDict()
            for key in ('top', 'left', 'width', 'height', 'fontsize'):
                base = fields.get(key)
                if base not in (None, ''):
                    geo.setdefault('base', {})[key] = base
                for bp in BREAKPOINTS[1:]:
                    v = fields.get('%s-res-%s' % (key, GRID_OF[bp]))
                    if v not in (None, ''):
                        geo.setdefault(bp, {})[key] = v
            if geo:
                el['geometry'] = geo
            if fields.get('axisx'):
                el['anchor'] = (fields.get('axisx', ''), fields.get('axisy', ''))
            if fields.get('filewidth'):
                el['source_size'] = [fields.get('filewidth'), fields.get('fileheight')]

            # анимации: appear — появление при прокрутке,
            # sbs — раскадровка, привязанная к прокрутке (mx/my сдвиг,
            # ro поворот, op прозрачность, sx/sy масштаб, di прогресс в %)
            anim = OrderedDict()
            appear = {k: fields_anim for k, fields_anim in (
                ('style', re.search(r'data-animate-style="([^"]*)"', attrs)),
                ('duration', re.search(r'data-animate-duration="([^"]*)"', attrs)),
                ('delay', re.search(r'data-animate-delay="([^"]*)"', attrs)),
                ('distance', re.search(r'data-animate-distance="([^"]*)"', attrs)),
            ) if fields_anim}
            if appear:
                anim['appear'] = {k: m.group(1) for k, m in appear.items()}
            sbs = re.search(r"data-animate-sbs-opts=\"([^\"]*)\"", attrs)
            if sbs:
                ev = re.search(r'data-animate-sbs-event="([^"]*)"', attrs)
                anim['scroll'] = {'event': ev.group(1) if ev else 'scroll',
                                  'keyframes': sbs.group(1).replace("'", '"')}
            if anim:
                el['animation'] = anim

            # стили элемента и его содержимого
            styles = OrderedDict()
            for bp in BREAKPOINTS:
                got = {}
                for sel, props in rules[bp].items():
                    if 'data-elem-id="%s"' % eid in sel or "data-elem-id='%s'" % eid in sel:
                        target = 'atom' if '.tn-atom' in sel else 'elem'
                        got.setdefault(target, {}).update(props)
                if got:
                    styles[bp] = got
            if styles:
                el['styles'] = styles

            # содержимое
            body = seg[m.end(): seg.find('</div>', seg.find('</div>', m.end()) + 6) + 6]
            img = re.search(r"(?:data-original|src)=['\"]([^'\"]+)['\"]", body)
            if img:
                el['image'] = os.path.basename(img.group(1))
            txt = clean_text(body)
            if txt:
                el['text'] = txt
            href = re.search(r"href=['\"]([^'\"]+)['\"]", body)
            if href:
                el['href'] = href.group(1)
            els.append(el)

        if els:
            block['elements'] = els
        else:
            # обычный блок Тильды — снимаем только текст и картинки
            texts = [clean_text(t) for t in re.findall(
                r'<div class="[^"]*t-(?:title|descr|text|name)[^"]*"[^>]*>(.*?)</div>', seg, re.S)]
            texts = [t for t in texts if t]
            if texts:
                block['texts'] = texts
            imgs = re.findall(r"(?:data-original|src)=['\"]([^'\"]+\.(?:jpg|png|svg|webp))['\"]", seg)
            if imgs:
                block['images'] = sorted({os.path.basename(i) for i in imgs})
        blocks.append(block)
    return blocks


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for name in sorted(os.listdir(SRC)):
        if not re.fullmatch(r'page\d+\.html', name):
            continue
        blocks = parse_page(os.path.join(SRC, name))
        dst = os.path.join(OUT, name.replace('.html', '.json'))
        with open(dst, 'w', encoding='utf-8') as f:
            json.dump(blocks, f, ensure_ascii=False, indent=1)
        n_el = sum(len(b.get('elements', [])) for b in blocks)
        index.append({'page': name, 'blocks': len(blocks), 'elements': n_el,
                      'spec': os.path.basename(dst)})
        print('%-22s %2d блоков, %3d элементов -> %s'
              % (name, len(blocks), n_el, os.path.basename(dst)))
    with open(os.path.join(OUT, '_index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    print('\nвсего блоков:', sum(i['blocks'] for i in index))


if __name__ == '__main__':
    main()
