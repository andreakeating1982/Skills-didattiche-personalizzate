#!/usr/bin/env python3
"""Controllare inizi pagina obbligatori, non soltanto la presenza del CSS.
Uso: verifica_inizi_pagina.py file.html --manifest sezioni.json --report qa.json --strict
Il manifest contiene sections: ["sec1", "sec2", "mappa", "fonti", "appendice"].
Nessuna modifica al documento; verificare separatamente indice e resa PDF.
"""
import argparse
import json
from pathlib import Path
from weasyprint import HTML


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', type=Path)
    p.add_argument('--manifest', required=True, type=Path)
    p.add_argument('--report', required=True, type=Path)
    p.add_argument('--tolerance-pt', type=float, default=1)
    p.add_argument('--strict', action='store_true')
    args = p.parse_args()
    required = json.loads(args.manifest.read_text())['sections']
    if len(required) != len(set(required)):
        raise ValueError('ID di sezione duplicati nel manifest')
    doc = HTML(filename=str(args.html.resolve())).render()
    errors, starts, details = [], {}, []
    # Ricostruire i genitori dagli elementi, compatibile con ElementTree del renderer.
    parents = {}
    for page in doc.pages:
        for box in page._page_box.descendants():
            el = getattr(box, 'element', None)
            if el is not None:
                for child in el:
                    parents[child] = el
    for pn, page in enumerate(doc.pages, 1):
        for box in page._page_box.descendants():
            el = getattr(box, 'element', None)
            if el is None or el.get('id') not in required or type(box).__name__ != 'BlockBox':
                continue
            key = el.get('id')
            if key in starts:
                continue  # Una sezione multipagina ha più frammenti: conta il primo.
            starts[key] = pn
            margin_top = page._page_box.content_box_y()
            section_top = box.border_box_y()
            displacement = (section_top - margin_top) * .75
            row = {'id': key, 'page': pn, 'top_displacement_pt': round(displacement, 6)}
            if abs(displacement) > args.tolerance_pt:
                errors.append({'id': key, 'page': pn, 'issue': 'section_not_at_page_top',
                               'displacement_pt': round(displacement, 6)})
            try:
                row['computed_break_before'] = box.style['break_before']
            except KeyError:
                row['computed_break_before'] = 'unavailable'
            foreign = []
            for other in page._page_box.descendants():
                oe = getattr(other, 'element', None)
                # Footer/counter boxes hanno element=None e non sono contenuto precedente.
                if oe is None or type(other).__name__ not in ('TextBox', 'InlineReplacedBox', 'BlockReplacedBox'):
                    continue
                if type(other).__name__ == 'TextBox' and not other.text.strip():
                    continue
                ancestor = oe
                inside = False
                while ancestor is not None:
                    if ancestor is el:
                        inside = True
                        break
                    ancestor = parents.get(ancestor)
                if not inside:
                    foreign.append(getattr(other, 'text', '') or oe.tag)
            if foreign:
                errors.append({'id': key, 'page': pn, 'issue': 'other_section_content_on_start_page',
                               'examples': foreign[:5]})
            row['other_section_content'] = foreign[:5]
            details.append(row)
    for key in required:
        if key not in starts:
            errors.append({'id': key, 'issue': 'section_not_found'})
    page_to_ids = {}
    for key, page in starts.items():
        page_to_ids.setdefault(page, []).append(key)
    for page, keys in page_to_ids.items():
        if len(keys) > 1:
            errors.append({'page': page, 'issue': 'multiple_section_starts_on_same_page', 'ids': keys})
    in_order = [starts[x] for x in required if x in starts]
    if in_order != sorted(in_order):
        errors.append({'issue': 'section_order_changed'})
    report = {'html': str(args.html), 'pages': len(doc.pages), 'required_sections': required,
              'section_starts': details, 'errors': errors, 'passed': not errors,
              'limits': 'Audit di primo frammento, posizione e contenuti estranei nel renderer. '
                        'Non controlla automaticamente i numeri dell’indice, il PDF esportato o la semantica.'}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.strict and errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

