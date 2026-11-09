#!/usr/bin/env python3
"""QA del flusso prima-pagina-prima e delle fonti finali nelle guide del blog.

Non modifica file sorgente e non verifica veridicita/autori/URL delle citazioni.
Richiede beautifulsoup4, weasyprint e pymupdf. Affiancare verifica_blocchi_blog.py
per righe, colori e font; ispezionare tutte le pagine anche visivamente.

Esempio:
  python3 verifica_flusso_fonti_blog.py guida.html --pdf guida.pdf \
    --unita sec1,sec2,sec3 --report flusso.json --strict
"""
from pathlib import Path
from collections import defaultdict
import argparse
import json
import re

from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
import pymupdf


def check(html, pdf=None, units=None, sources_selector='#fonti',
          note_selector='.source-card, .source-note, [data-bibliographic-note]',
          without_sources=False, card_selector='.text-chunk, .sintesi'):
    source = Path(html).resolve()
    soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
    errors, warnings, summary = [], [], []
    if units:
        nodes = [soup.find(id=x) for x in units]
        missing = [x for x, node in zip(units, nodes) if node is None]
        if missing:
            errors.append('Unita inesistenti: ' + ', '.join(missing))
        nodes = [x for x in nodes if x is not None]
    else:
        nodes = [x for x in soup.select('.sec')
                 if re.fullmatch(r'(sec|sezione)\d+', x.get('id', ''))]
    if not nodes:
        errors.append('Nessuna unita identificata; specificare --unita id1,id2,...')

    mapping = {}
    for unit in nodes:
        cards = unit.select(card_selector)
        selected = {id(x) for x in cards}
        # Evitare doppi conteggi quando una sintesi contiene schede annidate.
        cards = [x for x in cards
                 if not any(id(a) in selected for a in x.parents if a is not unit)]
        for n, card in enumerate(cards, 1):
            if not card.get('id'):
                card['id'] = f'qa-flow-{unit["id"]}-{n:03d}'
        mapping[unit['id']] = [x['id'] for x in cards]

    sources = soup.select_one(sources_selector) if not without_sources else None
    if not without_sources and sources is None:
        errors.append('Pagina finale delle fonti non trovata: ' + sources_selector)
    if sources is not None:
        if not sources.get('id'):
            sources['id'] = 'qa-final-sources'
        for n, node in enumerate(sources.find_all(['p', 'h2', 'h3', 'td', 'a']), 1):
            if not node.get('id'):
                node['id'] = f'qa-source-content-{n:03d}'
        for note in soup.select(note_selector):
            if note is not sources and sources not in note.parents:
                errors.append('Nota bibliografica rimasta fuori dalla pagina finale: '
                              + note.get('id', note.name))

    # Un titolo da tenere con il box seguente e' parte del gruppo indivisibile:
    # non confrontare il solo box con lo spazio disponibile nella pagina prima.
    heading_ids=set()
    for n,heading in enumerate(soup.select('h1,h2,h3,h4,h5,h6,.part-label'),1):
        if not heading.get('id'):heading['id']=f'qa-keep-heading-{n:03d}'
        heading_ids.add(heading['id'])
    preceding_headings={}
    for cards in mapping.values():
        for cid in cards:
            node=soup.find(id=cid);before=[]
            for sibling in node.previous_siblings:
                if not getattr(sibling,'name',None):
                    if str(sibling).strip():break
                    continue
                if sibling.get('id') not in heading_ids:break
                before.insert(0,sibling['id'])
            preceding_headings[cid]=before
    wanted = set(mapping) | {x for cards in mapping.values() for x in cards} | heading_ids
    if sources is not None:
        wanted.add(sources['id'])
        wanted.update(x['id'] for x in sources.select('[id]'))
    rendered = HTML(string=str(soup), base_url=str(source.parent)).render()
    geometry = defaultdict(dict)
    seen_pages = defaultdict(set)
    for page_number, page in enumerate(rendered.pages, 1):
        for box in page._page_box.descendants():
            el = getattr(box, 'element', None)
            if el is None:
                continue
            eid = el.get('id')
            if eid not in wanted:
                continue
            if type(box).__name__ in ['LineBox', 'BlockBox', 'TableBox', 'InlineBox']:
                seen_pages[eid].add(page_number)
            if type(box).__name__ == 'BlockBox' and page_number not in geometry[eid]:
                geometry[eid][page_number] = {
                    'top': float(box.border_box_y()),
                    'height': float(box.border_height()),
                    'bottom': float(box.border_box_y() + box.border_height()),
                    'margin_top': float(box.margin_top),
                    'margin_bottom': float(box.margin_bottom),
                    'page_bottom': float(page._page_box.content_box_y()
                                         + page._page_box.height),
                }

    def natural_height_without_page_start_trimming(cid, actual_height):
        # WeasyPrint puo scartare il margine superiore di un h3 annidato quando
        # l'intero box passa a inizio pagina. Non e lo stesso ingombro che avrebbe
        # in coda alla pagina precedente. Controfattuale SOLO per il controllo:
        # mantenere i margini interni, senza modificare sorgente o PDF consegnati.
        selector='[id='+json.dumps(cid)+'] * { margin-break:keep !important; }'
        restored=HTML(string=str(soup),base_url=str(source.parent)).render(
            stylesheets=[CSS(string=selector)])
        for page in restored.pages:
            for box in page._page_box.descendants():
                el=getattr(box,'element',None)
                if type(box).__name__=='BlockBox' and el is not None and el.get('id')==cid:
                    return max(actual_height,float(box.border_height()))
        return actual_height

    for uid, card_ids in mapping.items():
        if not card_ids:
            warnings.append(f'{uid}: nessun box discorsivo/sintesi; verifica separata')
            continue
        missing = [cid for cid in card_ids if not geometry[cid]]
        if missing:
            errors.append(f'{uid}: box non misurabili: ' + ', '.join(missing))
            continue
        for cid in card_ids:
            if len(seen_pages[cid]) != 1:
                errors.append(f'{uid}: box {cid} spezzato tra pagine')
        ordered_pages = [min(geometry[cid]) for cid in card_ids]
        if ordered_pages != sorted(ordered_pages):
            errors.append(f'{uid}: ordine dei box non conservato')
        start = min(seen_pages[uid]) if seen_pages[uid] else min(ordered_pages)
        if min(ordered_pages) != start:
            errors.append(f'{uid}: titolo isolato prima del primo box')
        counts = {str(p): ordered_pages.count(p) for p in sorted(set(ordered_pages))}
        transitions = []
        for i in range(1, len(card_ids)):
            p_before, p_after = ordered_pages[i-1], ordered_pages[i]
            if p_before == p_after:
                continue
            previous = geometry[card_ids[i-1]][p_before]
            following = geometry[card_ids[i]][p_after]
            free = previous['page_bottom'] - previous['bottom']
            group=[geometry[hid][p_after] for hid in preceding_headings.get(card_ids[i],[])
                   if p_after in geometry[hid]]+[following]
            needed=group[0]['height']+max(previous['margin_bottom'],group[0]['margin_top'])
            for left,right in zip(group,group[1:]):
                needed+=right['height']+max(left['margin_bottom'],right['margin_top'])
            could_fit = needed <= free - 1.0  # tolleranza di un pixel CSS
            before_margin_restoration=needed
            restored_internal_margin=0.0
            if could_fit:
                natural_height=natural_height_without_page_start_trimming(
                    card_ids[i],following['height'])
                restored_internal_margin=natural_height-following['height']
                needed+=restored_internal_margin
                could_fit=needed <= free - 1.0
            transitions.append({
                'from_page': p_before, 'to_page': p_after,
                'next_card': card_ids[i], 'free_px': round(free, 2),
                'required_px': round(needed, 2), 'could_fit_before': could_fit,
                'kept_headings':preceding_headings.get(card_ids[i],[]),
                'required_px_before_margin_restoration':round(before_margin_restoration,2),
                'restored_internal_margin_px':round(restored_internal_margin,2),
            })
            if could_fit:
                errors.append(f'{uid}: {card_ids[i]} anticipato a pagina {p_after}, '
                              f'ma richiede {needed:.1f}px con {free:.1f}px disponibili')
        summary.append({'unit': uid, 'start_page': start,
                        'boxes_by_page': counts, 'transitions': transitions})

    sources_report = None
    if sources is not None:
        descendants = [sources] + list(sources.select('[id]'))
        source_pages = sorted(set().union(*(seen_pages[x['id']] for x in descendants)))
        sources_report = {'id': sources['id'], 'pages': source_pages}
        # Una bibliografia completa puo' richiedere piu' pagine finali contigue.
        expected = list(range(source_pages[0],len(rendered.pages)+1)) if source_pages else []
        if not source_pages or source_pages != expected:
            errors.append('Le fonti devono occupare l’ultima pagina o un gruppo di pagine finali contigue: '
                          + str(source_pages))
        if any(x.get_text(strip=True) for x in sources.find_next_siblings()):
            errors.append('Contenuti presenti dopo la sezione finale delle fonti')

    pdf_pages = None
    if pdf:
        with pymupdf.open(Path(pdf).resolve()) as final:
            pdf_pages = len(final)
            if pdf_pages != len(rendered.pages):
                errors.append('Numero pagine PDF diverso dal sorgente HTML verificato')
            if sources_report and not final[-1].get_text().strip():
                errors.append('Ultima pagina PDF senza testo')
    return {
        'html': str(source), 'pdf': str(Path(pdf).resolve()) if pdf else None,
        'pages': len(rendered.pages), 'pdf_pages': pdf_pages, 'units': summary,
        'sources': sources_report, 'errors': errors, 'warnings': warnings,
        'passed': not errors,
        'limits': 'Controllo geometrico per blocchi normali nel flusso; '
                  'non valida bibliografia, font, colori o accessibilita PDF/UA. '
                  'Per float, griglie e regole keep complesse verificare il renderer. '
                  'Con --pdf controlla numero pagine, non identita completa HTML/PDF.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html')
    parser.add_argument('--pdf')
    parser.add_argument('--unita', help='ID delle unita separati da virgola')
    parser.add_argument('--selettore-box', default='.text-chunk, .sintesi',
                        help='Selettore CSS dei blocchi indivisibili; es. .blk, .lf-summary')
    parser.add_argument('--selettore-fonti', default='#fonti')
    parser.add_argument('--selettore-note',
                        default='.source-card, .source-note, [data-bibliographic-note]')
    parser.add_argument('--senza-fonti', action='store_true',
                        help='Solo flusso, quando non e richiesta una bibliografia')
    parser.add_argument('--report')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    result = check(args.html, args.pdf,
                   [x.strip() for x in args.unita.split(',') if x.strip()]
                   if args.unita else None,
                   args.selettore_fonti, args.selettore_note, args.senza_fonti,
                   args.selettore_box)
    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2),
                          encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.strict and not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

