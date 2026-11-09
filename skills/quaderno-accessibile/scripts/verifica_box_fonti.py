#!/usr/bin/env python3
"""Verifica i box color crema dei riferimenti bibliografici in un HTML stampabile.

Contrassegnare ciascuna voce con `.ref-entry` o `[data-bibliography-entry]`;
per i gruppi di scene usare `.scene-entry`. Ogni testo di tali voci deve essere
in `.blk` o `[data-bibliography-box]`, di norma #fffaf0. Il controllo misura le
righe e il colore effettivi nel rendering WeasyPrint, senza modificare l'HTML.
Non sostituisce la lettura delle fonti, l'ispezione visiva del PDF o il test
separato dei collegamenti con verifica_fonti_bibliografia.py.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from weasyprint import HTML

ENTRY_SELECTOR = '.ref-entry, .scene-entry, [data-bibliography-entry]'
CARD_SELECTOR = '.blk, [data-bibliography-box]'
LIMITS = ('Sono controllate le sole voci identificate dal selettore. '
          'La verifica non valuta provenienza, correttezza scientifica, ordine, '
          'contenuti non classificati, link nel PDF o conformità PDF/UA. '
          'Ispezionare sempre il PDF e controllare separatamente i collegamenti.')


def check(source, bibliography_id='bibliografia', entry_selector=ENTRY_SELECTOR,
          card_selector=CARD_SELECTOR, color='#fffaf0', max_lines=5):
    """Restituire un rapporto; aggiungere attributi solo al DOM in memoria."""
    path = Path(source).resolve()
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise ValueError('Il colore deve essere #rrggbb, ad esempio #fffaf0')
    if max_lines < 1:
        raise ValueError('max_lines deve essere positivo')
    expected = tuple(int(color[i:i+2], 16) / 255 for i in (1, 3, 5))
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    errors, warnings = [], []
    bibliography = soup.find(id=bibliography_id)
    result = {'html': str(path), 'bibliography_id': bibliography_id,
              'entry_selector': entry_selector, 'card_selector': card_selector,
              'expected_color': color.lower(), 'max_lines_allowed': max_lines,
              'entries': 0, 'cards': [], 'errors': errors, 'warnings': warnings,
              'passed': False, 'limits': LIMITS}
    if bibliography is None:
        errors.append({'issue': 'bibliografia_non_trovata', 'id': bibliography_id})
        return result

    targets = bibliography.select(entry_selector)
    target_ids = {id(x) for x in targets}
    # Non contare lo stesso elemento testuale più volte quando un gruppo è annidato.
    targets = [x for x in targets if not any(id(p) in target_ids for p in x.parents)]
    result['entries'] = len(targets)
    if not targets:
        errors.append({'issue': 'voci_bibliografiche_non_identificate',
                       'suggestion': 'Marcare le voci o passare --entry-selector.'})
        return result
    card_candidates = bibliography.select(card_selector)
    candidate_ids = {id(x) for x in card_candidates}
    used, used_ids, missing = [], set(), set()
    for target in targets:
        for text in target.find_all(string=True):
            if not str(text).strip() or text.parent.name in ('script', 'style'):
                continue
            parent, card = text.parent, None
            while parent is not None and parent is not bibliography:
                if id(parent) in candidate_ids:
                    card = parent
                    break
                parent = parent.parent
            if card is None:
                key = id(text)
                if key not in missing:
                    errors.append({'issue': 'contenuto_fuori_box',
                                   'entry': target.get('id'), 'text': str(text).strip()[:160]})
                    missing.add(key)
            elif id(card) not in used_ids:
                used.append(card)
                used_ids.add(id(card))

    # Eventuali paragrafi fuori dalle voci richiedono una lettura: possono essere
    # intestazioni, attribuzioni oppure riferimenti non marcati automaticamente.
    effective_target_ids = {id(x) for x in targets}
    for paragraph in bibliography.select('p, li'):
        if not paragraph.get_text(' ', strip=True):
            continue
        ancestors = [paragraph, *paragraph.parents]
        if not any(id(x) in effective_target_ids for x in ancestors):
            warnings.append({'issue': 'paragrafo_non_classificato',
                             'text': paragraph.get_text(' ', strip=True)[:160]})

    if not used:
        errors.append({'issue': 'nessun_box_contenente_fonti'})
        return result
    tokens = {}
    for index, card in enumerate(used, 1):
        token = f'bibliography-qa-{index}'
        card['data-bibliography-qa-token'] = token
        tokens[token] = card
    document = HTML(string=str(soup), base_url=str(path.parent)).render()
    geometries = {token: [] for token in tokens}
    rendered_types = {'BlockBox', 'TableCellBox', 'FlexBox', 'GridBox', 'InlineBlockBox'}
    for page_number, page in enumerate(document.pages, 1):
        for box in page._page_box.descendants():
            element = getattr(box, 'element', None)
            if element is None or type(box).__name__ not in rendered_types:
                continue
            token = element.get('data-bibliography-qa-token')
            if token not in geometries:
                continue
            actual = box.style.get('background_color')
            if hasattr(actual, 'to') and getattr(actual, 'space', None) != 'srgb':
                try:
                    actual = actual.to('srgb')
                except (TypeError, ValueError, NotImplementedError):
                    pass
            coords = getattr(actual, 'coordinates', ())
            alpha = getattr(actual, 'alpha', None)
            is_cream = (len(coords) == 3 and alpha is not None and alpha >= .99
                        and all(abs(v - e) <= 1.1/255 for v, e in zip(coords, expected)))
            line_boxes = [d for d in box.descendants() if type(d).__name__ == 'LineBox']
            geometries[token].append({'page': page_number, 'lines': len(line_boxes),
                                      'color': str(actual), 'cream': is_cream,
                                      'width_px': round(box.border_width(), 2),
                                      'height_px': round(box.border_height(), 2)})

    for token, card in tokens.items():
        places = geometries[token]
        lines = sum(p['lines'] for p in places)
        row = {'id': card.get('id') or token, 'pages': [p['page'] for p in places],
               'lines': lines, 'fragments': places}
        result['cards'].append(row)
        if not places:
            errors.append({'issue': 'box_non_renderizzato', 'id': row['id']})
            continue
        if len(places) > 1:
            errors.append({'issue': 'box_frammentato', 'id': row['id'], 'pages': row['pages']})
        if lines > max_lines:
            errors.append({'issue': 'oltre_limite_righe', 'id': row['id'], 'lines': lines})
        if any(not p['cream'] for p in places):
            errors.append({'issue': 'sfondo_non_conforme', 'id': row['id'],
                           'actual': [p['color'] for p in places], 'expected': color.lower()})
        if any(p['width_px'] <= 0 or p['height_px'] <= 0 for p in places):
            errors.append({'issue': 'box_area_nulla', 'id': row['id']})
    result['pages'] = len(document.pages)
    result['max_lines_observed'] = max((r['lines'] for r in result['cards']), default=0)
    result['passed'] = not errors
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html')
    parser.add_argument('--bibliography-id', default='bibliografia')
    parser.add_argument('--entry-selector', default=ENTRY_SELECTOR)
    parser.add_argument('--card-selector', default=CARD_SELECTOR)
    parser.add_argument('--color', default='#fffaf0')
    parser.add_argument('--max-lines', type=int, default=5)
    parser.add_argument('--report')
    args = parser.parse_args()
    result = check(args.html, args.bibliography_id, args.entry_selector,
                   args.card_selector, args.color, args.max_lines)
    content = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        Path(args.report).write_text(content, encoding='utf-8')
    print(content, end='')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

