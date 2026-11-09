#!/usr/bin/env python3
"""Rimuovere i soli marcatori ornamentali dei vecchi paragrafi .bullet.
Conservare frecce semantiche, formule, icone nelle immagini e veri controlli.
Uso: script.py input.html --output nuovo.html [--report modifiche.json]
Il CSS esterno richiede rimozione delle regole .bullet/.mark o override mirato.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,json

DECORATIVE=set('✔✓➜➔➞➟➠➤➢➣✅☑')

def clean(html):
    soup=BeautifulSoup(html,'html.parser');removed=[];paragraphs=[]
    for marker in list(soup.select('p.bullet > span.mark')):
        text=marker.get_text(strip=True)
        if text and all(ch in DECORATIVE for ch in text):
            removed.append({'paragraph_id':marker.parent.get('id'),'symbol':text})
            marker.decompose()
    for p in soup.select('p.bullet'):
        if not p.select_one('.mark'):
            p['class']=[c for c in p.get('class',[]) if c!='bullet']
            if not p['class']:del p['class']
            paragraphs.append(p.get('id'))
    return str(soup),{'removed_count':len(removed),'removed':removed,'unindented_paragraphs':paragraphs}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('html');p.add_argument('--output',required=True);p.add_argument('--report');a=p.parse_args()
    src=Path(a.html);out=Path(a.output)
    if src.resolve()==out.resolve():p.error('Salvare con nuovo nome, conservare il sorgente')
    html,report=clean(src.read_text());out.write_text(html)
    if a.report:Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

