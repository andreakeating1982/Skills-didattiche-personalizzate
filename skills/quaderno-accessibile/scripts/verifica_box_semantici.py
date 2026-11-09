#!/usr/bin/env python3
"""Misurare i box per nuclei di significato; la decisione semantica richiede lettura.
Conta LineBox reali del contenitore (incluse intestazioni e testo inline).
Uso: verifica_box_semantici.py guida.html --report box.json --strict
Non modifica il sorgente, non certifica coerenza semantica o PDF/UA.
"""
from pathlib import Path
from collections import defaultdict
import argparse,json
from bs4 import BeautifulSoup
from weasyprint import HTML

CARD='.blk,.text-chunk,[data-semantic-box]'
STRUCTURED='.summary-table td,.sintesi td,.m-node,.map-card'

def check(source):
    source=Path(source).resolve();s=BeautifulSoup(source.read_text(),'html.parser')
    # Specchietti e mappe finali hanno un numero libero di righe; profilo utente foto1/foto2.
    candidates=[c for c in s.select(CARD) if not c.has_attr('data-support-profile') and not c.find_parent(attrs={'data-support-profile':True})]
    # Un contenitore fisico contato una volta, mai il wrapper .blk e il suo figlio.
    cards=[c for c in candidates if not any(p in candidates for p in c.parents)]
    structured=[c for c in s.select(STRUCTURED) if not c.has_attr('data-support-profile') and not c.find_parent(attrs={'data-support-profile':True})]
    structured=[c for c in structured if not any(p in cards for p in c.parents)]
    objects=cards+structured
    for i,e in enumerate(objects,1):
        if not e.get('id'):e['id']=f'qa-semantic-{i:04d}'
    keys={e['id'] for e in objects};geometry=defaultdict(list)
    doc=HTML(string=str(s),base_url=str(source.parent)).render()
    for pn,page in enumerate(doc.pages,1):
        for b in page._page_box.descendants():
            e=getattr(b,'element',None)
            if e is None or e.get('id') not in keys or type(b).__name__ not in ('BlockBox','TableCellBox'):continue
            # Un solo box esterno per id/pagina; non contare i figli ricorsivamente due volte.
            if any(x['page']==pn for x in geometry[e.get('id')]):continue
            ls=[x for x in b.descendants() if type(x).__name__=='LineBox']
            geometry[e.get('id')].append({'page':pn,'lines':len(ls)})
    errors=[];rows=[]
    for e in objects:
        id=e['id'];places=geometry[id];n=sum(x['lines'] for x in places)
        row={'id':id,'kind':'card' if e in cards else 'structured_cell_or_node','lines':n,'pages':[x['page'] for x in places],
             'paragraphs':len(e.find_all('p')),'text':e.get_text(' ',strip=True),
             'editorial_reason':e.get('data-box-reason'),'contains_image':bool(e.find('img'))}
        rows.append(row)
        if row['text'] and not places:errors.append(f'{id}: contenitore testuale non trovato nel rendering')
        if n>5:errors.append(f'{id}: {n} righe reali complessive, oltre cinque')
        if len(places)>1:errors.append(f'{id}: box/cella/nodo spezzato su piu pagine')
    return {'html':str(source),'pages':len(doc.pages),'cards':len(cards),'structured_units':len(structured),
            'max_lines':max((x['lines'] for x in rows),default=0),'units':rows,'errors':errors,'passed':not errors,
            'limits':'Misura geometrica. La coerenza semantica e i confini richiedono lettura editoriale; il controllo non decide accorpamenti e non certifica PDF/UA.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('html');p.add_argument('--report');p.add_argument('--strict',action='store_true');a=p.parse_args()
    report=check(a.html)
    if a.report:Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='units'},ensure_ascii=False,indent=2))
    if a.strict and not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()

