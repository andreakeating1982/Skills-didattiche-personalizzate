#!/usr/bin/env python3
"""QA reale di guide lunghe: LineBox, bianco esterno, crema interno, titoli sotto immagini.
Usare con HTML completo; --pdf per verificare un PDF già generato dal medesimo HTML.
Senza --pdf rende <nome>_verificato.pdf. --strict: exit 1 se uno dei controlli fallisce.
Dipendenze: beautifulsoup4, weasyprint, pymupdf.
"""
from pathlib import Path
from collections import defaultdict
import argparse, json
from bs4 import BeautifulSoup
from weasyprint import HTML
import pymupdf


def check(source, pdf=None):
    source = Path(source).resolve()
    soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
    targets = soup.find_all(['p','h3','h4'])
    for i, node in enumerate(targets, 1):
        if not node.get('id'):
            node['id'] = f'qa-line-{i:04d}'
    cards = soup.select('.text-chunk') or soup.select('.blk')
    for i, card in enumerate(cards, 1):
        if not card.get('id'):
            card['id'] = f'qa-card-{i:04d}'
    doc = HTML(string=str(soup), base_url=str(source.parent)).render()
    line_counts, locations = defaultdict(int), defaultdict(set)
    for page_i, page in enumerate(doc.pages, 1):
        for box in page._page_box.descendants():
            element = getattr(box, 'element', None)
            if type(box).__name__ == 'LineBox' and element is not None:
                eid = element.get('id')
                if eid:
                    line_counts[eid] += 1
                    locations[eid].add(page_i)
    errors, paragraph_info, card_info = [], [], []
    for p in soup.find_all('p'):
        pid = p['id']
        n = line_counts.get(pid, 0)
        paragraph_info.append({'id':pid,'lines':n,'pages':sorted(locations[pid])})
        if n > 5:
            errors.append(f'Paragrafo {pid}: {n} righe, oltre 5')
        if len(locations[pid]) > 1:
            errors.append(f'Paragrafo {pid} spezzato tra pagine')
    for card in cards:
        ids = [n['id'] for n in card.find_all(['p','h3','h4'])]
        n = sum(line_counts[x] for x in ids)
        pages = set().union(*(locations[x] for x in ids)) if ids else set()
        card_info.append({'id':card['id'],'lines_with_subheading':n,'pages':sorted(pages)})
        if n > 5:
            errors.append(f'Box {card["id"]}: {n} righe incluso sottotitolo, oltre 5')
        if len(pages) > 1:
            errors.append(f'Box {card["id"]} spezzato tra pagine')
        for image in card.find_all('img'):
            next_tag = image.find_next_sibling()
            if next_tag is not None and next_tag.name in ['h3','h4','figcaption']:
                errors.append(f'Titolo/didascalia sotto immagine in {card["id"]}')
    if pdf:
        pdf_path = Path(pdf).resolve()
    else:
        pdf_path = source.with_name(source.stem+'_verificato.pdf')
        doc.write_pdf(str(pdf_path), pdf_variant='pdf/ua-1')
    final = pymupdf.open(pdf_path)
    if len(final) != len(doc.pages):
        errors.append('Numero pagine HTML e PDF diverso: verificare che il PDF corrisponda al sorgente')
    margin_samples, box_samples = [], []
    for i, page in enumerate(final, 1):
        pix = page.get_pixmap(dpi=96)
        for x,y in [(5,5),(5,pix.height//2),(pix.width-6,pix.height//2),(pix.width//2,pix.height-6)]:
            rgb = pix.pixel(x,y)[:3]
            margin_samples.append({'page':i,'point':[x,y],'rgb':list(rgb)})
            if rgb != (255,255,255):
                errors.append(f'Pagina {i}: margine NON bianco a ({x},{y}), RGB {rgb}')
    card_ids = {c['id'] for c in cards}
    for i,page in enumerate(doc.pages):
        if i >= len(final):
            break
        pix = final[i].get_pixmap(dpi=96)
        for box in page._page_box.descendants():
            el = getattr(box,'element',None)
            if type(box).__name__ != 'BlockBox' or el is None or el.get('id') not in card_ids:
                continue
            left, top = box.border_box_x(), box.border_box_y()
            y = round(top+box.border_height()/2)
            x_in, x_out = round(left+6),round(left-5)
            if not (0 <= x_out < pix.width and 0 <= x_in < pix.width and 0 <= y < pix.height):
                errors.append(f'Box {el.get("id")}: campionamento fuori pagina')
                continue
            inside, outside = pix.pixel(x_in,y)[:3],pix.pixel(x_out,y)[:3]
            box_samples.append({'card':el.get('id'),'page':i+1,'inside':list(inside),'outside':list(outside)})
            if outside != (255,255,255):
                errors.append(f'Esterno box {el.get("id")} NON bianco: {outside}')
            if not (inside[0]>250 and 244<=inside[1]<=252 and 232<=inside[2]<=243):
                errors.append(f'Interno box {el.get("id")} non crema al punto campionato: {inside}')
    return {
        'html':str(source),'pdf':str(pdf_path),'pages':len(final),
        'max_paragraph_lines':max((p['lines'] for p in paragraph_info),default=0),
        'max_card_lines_including_subheading':max((c['lines_with_subheading'] for c in card_info),default=0),
        'paragraphs':paragraph_info,'cards':card_info,
        'margin_samples':margin_samples,'box_samples':box_samples,
        'errors':errors,'passed':not errors,
        'note':'QA impaginazione, non certificazione PDF/UA. Verificare tutte le pagine anche visivamente.'
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html')
    ap.add_argument('--pdf')
    ap.add_argument('--report')
    ap.add_argument('--strict',action='store_true')
    args=ap.parse_args()
    report=check(args.html,args.pdf)
    path=Path(args.report) if args.report else Path(args.html).with_suffix('.qa.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['paragraphs','cards','margin_samples','box_samples']},ensure_ascii=False,indent=2))
    print('Rapporto:',path)
    if args.strict and not report['passed']:
        raise SystemExit(1)

if __name__=='__main__':
    main()

