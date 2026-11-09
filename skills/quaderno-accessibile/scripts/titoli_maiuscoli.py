#!/usr/bin/env python3
"""Preparare e verificare titoli editoriali in MAIUSCOLO senza alterare il corpo.
Uso: titoli_maiuscoli.py input.html --output nuovo.html
     titoli_maiuscoli.py nuovo.html --check --report titoli.json [--pdf nuovo.pdf]
Aggiungere data-editorial-title a eventuali etichette non semantiche mancanti.
"""
from pathlib import Path
import argparse,json,re,unicodedata
from bs4 import BeautifulSoup,NavigableString,Comment

SELECTORS = ('h1,h2,h3,h4,h5,h6,.subtitle,.part-label,.s-head,.map-root,.map-ghead,.m-node .t,'
             '[data-editorial-title],#indice .ind-label a,#indice .it a,'
             '#indice a.ind-title,.summary-table td:first-child,.sintesi td.lb,th')

def title_nodes(soup):
    selected=soup.select(SELECTORS)
    ids={id(x) for x in selected}
    return [x for x in selected if not any(id(p) in ids for p in x.parents)]

def transform(html):
    soup=BeautifulSoup(html,'html.parser'); changes=[]
    nodes=title_nodes(soup)
    if soup.title:nodes.append(soup.title)
    for n in nodes:
        before=n.get_text()
        for t in list(n.descendants):
            if isinstance(t,NavigableString) and not isinstance(t,Comment):
                # Codice/formule/nomi di unita' sensibili al case: marcare esplicitamente.
                if any(getattr(p,'attrs',{}).get('data-preserve-case') is not None for p in [t.parent,*t.parents]):continue
                t.replace_with(str(t).upper())
        after=n.get_text()
        if before!=after:changes.append({'tag':n.name,'id':n.get('id'),'before':before,'after':after})
    return str(soup),changes

def compact(text):
    return re.sub(r'\s+','',unicodedata.normalize('NFKC',text)).replace('\u00ad','')

def check(html,pdf=None):
    soup=BeautifulSoup(html,'html.parser'); errors=[];titles=[]
    for n in title_nodes(soup):
        text=n.get_text(' ',strip=True)
        c=BeautifulSoup(str(n),'html.parser')
        for x in c.select('[data-preserve-case]'):x.decompose()
        if any(ch.islower() for ch in c.get_text()):errors.append('Titolo non maiuscolo: '+text)
        titles.append({'tag':n.name,'text':text})
    if soup.title and soup.title.get_text()!=soup.title.get_text().upper():errors.append('Metadato title non maiuscolo')
    bookmarks=[]
    if pdf:
        import pymupdf
        doc=pymupdf.open(pdf); full=compact(' '.join(p.get_text() for p in doc))
        for t in titles:
            if compact(t['text']) not in full:errors.append('Titolo non rintracciato nel PDF: '+t['text'])
        bookmarks=doc.get_toc()
        for b in bookmarks:
            if any(ch.islower() for ch in b[1]):errors.append('Segnalibro non maiuscolo: '+b[1])
    return {'titles_count':len(titles),'titles':titles,'bookmarks_count':len(bookmarks),'errors':errors,'passed':not errors,
            'note':'Verifica testo e segnalibri; controllare separatamente linee reali, flusso, geometrie e immagini.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('html');ap.add_argument('--output');ap.add_argument('--check',action='store_true');ap.add_argument('--pdf');ap.add_argument('--report');args=ap.parse_args()
    path=Path(args.html);text=path.read_text()
    if args.check:
        report=check(text,args.pdf)
        if args.report:Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(0 if report['passed'] else 1)
    if not args.output:ap.error('Usare --output per preservare il sorgente approvato')
    html,changes=transform(text);Path(args.output).write_text(html)
    print(json.dumps({'output':args.output,'changed':len(changes)},ensure_ascii=False))

if __name__=='__main__':main()

