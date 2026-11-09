#!/usr/bin/env python3
"""Controlla bibliografia e singoli collegamenti nel PDF, non l'attendibilità delle fonti.

Richiede HTML con id sezione (default bibliografia) e, per i rimandi,
<a class="cite-ref" href="#id-della-fonte">. Opzionale --pdf per controllare
ogni annotazione e la sua superficie cliccabile effettiva. Nessuna rete.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup


def check(html, pdf=None, bibliography_id='bibliografia'):
    path = Path(html).resolve()
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    errors, warnings, citations, external_links = [], [], [], []
    bibliography = soup.find(id=bibliography_id)
    if bibliography is None:
        return {'passed': False, 'bibliography_id': bibliography_id, 'entries': 0,
                'citations': [], 'external_urls': [], 'errors': [{'issue': 'bibliografia_non_trovata'}],
                'warnings': [], 'limits': 'Verifica strutturale: non certifica attendibilità o reale consultazione delle fonti.'}
    entries = bibliography.select('.ref-entry') or bibliography.select('li')
    if not entries:
        warnings.append({'issue': 'voci_non_identificate_automaticamente', 'note': 'Leggere manualmente la bibliografia.'})
    for index, a in enumerate(soup.select('a.cite-ref'), 1):
        href = a.get('href', '').strip()
        label = a.get_text(' ', strip=True)
        parent = a.find_parent(id=True)
        a['data-qa-citation-index'] = str(index)  # Solo nel DOM in memoria, mai nel file dell'utente.
        entry = {'index': index, 'label': label, 'href': href,
                 'origin_id': parent.get('id') if parent else None, 'target': None}
        if not href.startswith('#') or len(href) == 1:
            errors.append({'issue': 'rimando_non_interno', 'index': index, 'href': href})
        else:
            target = href[1:]
            entry['target'] = target
            matches = soup.find_all(id=target)
            if len(matches) != 1:
                errors.append({'issue': 'destinazione_non_univoca_o_assente', 'index': index,
                               'target': target, 'count': len(matches)})
            elif bibliography.find(id=target) is None:
                errors.append({'issue': 'destinazione_fuori_bibliografia', 'index': index, 'target': target})
        if not label:
            errors.append({'issue': 'testo_rimando_mancante', 'index': index})
        citations.append(entry)
    for a in bibliography.select('a[href]'):
        href = a.get('href', '').strip()
        if urlsplit(href).scheme not in ('http', 'https'):
            continue
        index = len(external_links) + 1
        a['data-qa-external-index'] = str(index)
        external_links.append({'index': index, 'uri': href, 'label': a.get_text(' ', strip=True)})
    external = sorted({x['uri'] for x in external_links})
    pdf_result = None
    if pdf is not None:
        import pymupdf
        from weasyprint import HTML
        # Gli attributi data-* distinguono anche due link uguali nello stesso box.
        document = HTML(string=str(soup), base_url=str(path.parent)).render()
        expected = {'internal': {}, 'external': {}}
        for pnum, page in enumerate(document.pages):
            for kind, target, coords, box in page.links:
                element = getattr(box, 'element', None)
                if element is None:
                    continue
                for typ, attr in [('internal', 'data-qa-citation-index'), ('external', 'data-qa-external-index')]:
                    token = element.get(attr)
                    if not token or kind != typ:
                        continue
                    rect = pymupdf.Rect(*(v * .75 for v in coords))
                    expected[typ].setdefault(int(token), []).append((pnum, rect))
        with pymupdf.open(str(pdf)) as target_pdf:
            if len(document.pages) != len(target_pdf):
                errors.append({'issue': 'numero_pagine_html_pdf_diverso', 'html': len(document.pages), 'pdf': len(target_pdf)})
            try:
                named = target_pdf.resolve_names()
            except AttributeError:
                named = {}
                warnings.append({'issue': 'destinazioni_pdf_non_analizzabili_con_versione_pymupdf'})
            pdf_links = [page.get_links() for page in target_pdf]
            used = {'internal': set(), 'external': set()}

            def match_segments(typ, index, target, dest=None):
                regions = expected[typ].get(index, [])
                matches, weak = [], False
                if not regions:
                    return False, matches, weak
                for pnum, expected_rect in regions:
                    found = None
                    if pnum >= len(pdf_links) or expected_rect.width <= 1 or expected_rect.height <= 1:
                        return False, matches, weak
                    # Mezzo punto di tolleranza evita falsi negativi da arrotondamento PDF.
                    expanded = pymupdf.Rect(expected_rect.x0-.5, expected_rect.y0-.5,
                                            expected_rect.x1+.5, expected_rect.y1+.5)
                    for i, link in enumerate(pdf_links[pnum]):
                        if (pnum, i) in used[typ]:
                            continue
                        region = link.get('from')
                        if region is None or region.width <= 1 or region.height <= 1 or not expanded.intersects(region):
                            continue
                        if typ == 'external':
                            if link.get('kind') != pymupdf.LINK_URI or link.get('uri') != target:
                                continue
                        else:
                            if link.get('kind') not in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED) or link.get('page') != dest['page']:
                                continue
                            actual_name = link.get('nameddest')
                            if actual_name and actual_name != target:
                                continue
                            if not actual_name:
                                actual_to, expected_to = link.get('to'), dest.get('to')
                                if actual_to is not None and expected_to is not None:
                                    if abs(actual_to.x - expected_to.x) > 2 or abs(actual_to.y - expected_to.y) > 2:
                                        continue
                                else:
                                    weak = True
                        found = (i, region)
                        break
                    if found is None:
                        return False, matches, weak
                    i, region = found
                    used[typ].add((pnum, i))
                    matches.append({'page': pnum + 1, 'width_pt': round(region.width, 2),
                                    'height_pt': round(region.height, 2)})
                return True, matches, weak

            for entry in citations:
                target = entry['target']
                if not target:
                    continue
                dest = named.get(target)
                if not dest or 'page' not in dest:
                    errors.append({'issue': 'destinazione_pdf_assente', 'target': target})
                    continue
                ok, matches, weak = match_segments('internal', entry['index'], target, dest)
                entry['pdf_link_ok'], entry['pdf_regions'] = ok, matches
                if not ok:
                    errors.append({'issue': 'rimando_pdf_assente_o_area_nulla', 'index': entry['index'],
                                   'origin_id': entry['origin_id'], 'target': target})
                elif weak:
                    warnings.append({'issue': 'destinazione_verificata_per_pagina_non_per_ancora', 'target': target})
            for entry in external_links:
                ok, matches, _ = match_segments('external', entry['index'], entry['uri'])
                entry['pdf_link_ok'], entry['pdf_regions'] = ok, matches
                if not ok:
                    errors.append({'issue': 'link_esterno_pdf_assente_o_area_nulla', 'index': entry['index'], 'uri': entry['uri']})
            pdf_result = {'pages': len(target_pdf), 'external_uris_expected': len(external),
                          'external_uris_found': len({x['uri'] for x in external_links if x.get('pdf_link_ok')})}
    return {'passed': not errors, 'bibliography_id': bibliography_id, 'entries': len(entries),
            'citations': citations, 'external_urls': external, 'external_links': external_links,
            'pdf': pdf_result, 'errors': errors, 'warnings': warnings,
            'limits': ('I link non dimostrano la lettura della fonte, la qualità bibliografica o la corrispondenza '
                       'tra citazione e affermazione. Nessuna richiesta web, verifica di contenuto o certificazione PDF/UA.')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html')
    parser.add_argument('--pdf', help='PDF corrispondente renderizzato dallo stesso HTML')
    parser.add_argument('--bibliography-id', default='bibliografia')
    parser.add_argument('--report')
    args = parser.parse_args()
    result = check(args.html, args.pdf, args.bibliography_id)
    out = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        Path(args.report).write_text(out, encoding='utf-8')
    print(out, end='')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

