#!/usr/bin/env python3
"""Audit non distruttivo dei titoli: centratura reale e colori attesi opzionali.
Non modifica HTML/PDF, non verifica semantica, contrasto o conformità PDF/UA.
Uso: verifica_titoli_centrati.py file.html --expectations titoli.json --report qa.json --strict
"""
from pathlib import Path
import argparse
import json
import re
from weasyprint import HTML


def is_title(el, parents):
    if el is None:
        return False
    # Un th che racchiude un vero h1-h6 è un contenitore, non un secondo titolo.
    # Controllare il titolo interno (con ID/colore), evitando falsi positivi sul wrapper.
    if el.tag == 'th' and any(x.tag in ('h1','h2','h3','h4','h5','h6') for x in el.iter() if x is not el):
        return False
    if el.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'th'):
        return True
    if el.get('data-editorial-title') is not None:
        return True
    classes = el.get('class', '').split()
    if 'map-ghead' in classes:
        return True
    parent = parents.get(el)
    if 't' in classes and parent is not None:
        if 'm-node' in parent.get('class', '').split():
            return True
    if el.tag == 'td' and parent is not None:
        row = parent
        cells = [x for x in row if x.tag in ('td', 'th')]
        if not cells or cells[0] is not el:
            return False
        ancestor = parent
        while ancestor is not None:
            if 'summary-table' in ancestor.get('class', '').split():
                return True
            ancestor = parents.get(ancestor)
        return False
    return False


def hex_color(style):
    color = style['color'].to('srgb')
    return '#' + ''.join(f'{max(0, min(255, round(v * 255))):02x}' for v in color.coordinates)


def alignment(style):
    try:
        return style['text_align_all']
    except KeyError:
        return style['text_align']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('--expectations', type=Path, help='JSON con titles: [{id, expected_color}]')
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--tolerance-pt', type=float, default=0.2)
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    expected = {}
    if args.expectations:
        payload = json.loads(args.expectations.read_text())
        for row in payload['titles']:
            key = row['id']
            if key in expected:
                raise ValueError(f'ID atteso duplicato: {key}')
            color = row['expected_color'].lower()
            if not re.fullmatch(r'#[0-9a-f]{6}', color):
                raise ValueError(f'Colore non valido per {key}: {color}')
            expected[key] = color
    document = HTML(filename=str(args.html.resolve())).render()
    parents = {}
    for page in document.pages:
        for box in page._page_box.descendants():
            el = getattr(box, 'element', None)
            if el is not None:
                for child in el:
                    parents[child] = el
    records = {}
    errors = []
    max_deviation = 0.0
    measured = 0
    for page_number, page in enumerate(document.pages, 1):
        for box in page._page_box.descendants():
            el = getattr(box, 'element', None)
            if not is_title(el, parents) or type(box).__name__ not in ('BlockBox', 'TableCellBox'):
                continue
            # An element can continue on another page: retain all fragments.
            if el not in records:
                records[el] = {'id': el.get('id'), 'text': ' '.join(''.join(el.itertext()).split()),
                               'fragments': []}
            key = el.get('id')
            actual_align = alignment(box.style)
            if actual_align != 'center':
                errors.append({'id': key, 'page': page_number, 'issue': 'not_center_aligned',
                               'actual': actual_align})
            center = box.content_box_x() + box.width / 2
            fragment = {'page': page_number, 'align': actual_align, 'lines': []}
            colors = set()
            for child in box.descendants():
                if type(child).__name__ == 'TextBox' and child.text.strip():
                    colors.add(hex_color(child.style))
                if type(child).__name__ != 'LineBox':
                    continue
                text = ''.join(x.text for x in child.descendants() if type(x).__name__ == 'TextBox')
                if not text.strip():
                    continue
                deviation = ((child.position_x + child.width / 2) - center) * .75
                max_deviation = max(max_deviation, abs(deviation))
                measured += 1
                fragment['lines'].append({'text': text, 'center_deviation_pt': round(deviation, 6)})
                if abs(deviation) > args.tolerance_pt:
                    errors.append({'id': key, 'page': page_number, 'issue': 'line_not_centered',
                                   'text': text, 'deviation_pt': round(deviation, 6)})
            fragment['colors'] = sorted(colors)
            if key in expected and colors != {expected[key]}:
                errors.append({'id': key, 'page': page_number, 'issue': 'unexpected_color',
                               'expected': expected[key], 'actual': sorted(colors)})
            records[el]['fragments'].append(fragment)
    found = {x['id'] for x in records.values() if x['id']}
    for key in sorted(set(expected) - found):
        errors.append({'id': key, 'issue': 'expected_title_missing_in_rendering'})
    if not records:
        errors.append({'issue': 'no_title_containers_found'})
    if args.expectations:
        for record in records.values():
            if record['id'] not in expected:
                errors.append({'id': record['id'], 'issue': 'title_without_color_expectation',
                               'text': record['text']})
    report = {'html': str(args.html), 'pages': len(document.pages), 'titles': len(records),
              'title_lines_measured': measured, 'max_center_deviation_pt': round(max_deviation, 6),
              'color_expectations_supplied': bool(args.expectations),
              'color_verification': 'performed' if args.expectations else 'not_requested',
              'errors': errors, 'passed': not errors, 'details': list(records.values()),
              'limits': 'Audit geometrico/CSS. Controllare separatamente testo, enfasi, indice, immagini, '
                        'leggibilità e resa visiva. Non certifica contrasto, semantica o PDF/UA.'}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != 'details'}, ensure_ascii=False, indent=2))
    if args.strict and errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

