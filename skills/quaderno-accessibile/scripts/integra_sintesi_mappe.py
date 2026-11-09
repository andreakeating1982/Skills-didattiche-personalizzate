#!/usr/bin/env python3
"""Integrare specchietti/tabella e mappe/box secondo foto1/foto2 da contenuti espliciti."""
from pathlib import Path
import argparse,json,re
from bs4 import BeautifulSoup
from specchietti_box import CSS,TITLE,summary,concept_map

def apply(source,config):
 s=BeautifulSoup(source,'html.parser');size=config.get('body_font_size_px');lh=config.get('body_line_height')
 if not isinstance(size,(int,float)) or not isinstance(lh,(int,float)):raise ValueError('Dichiarare body_font_size_px e body_line_height misurati nel corpo.')
 ty=f'--body-size:{size}px;--body-leading:{lh};';report={'summaries_replaced':[],'maps_replaced':[]}
 old=s.find('style',id='specchietti-box-foto')
 if old:old.decompose()
 style=s.new_tag('style',id='specchietti-box-foto');style.string=CSS;s.head.append(style)
 for u in config.get('summaries',[]):
  if not u.get('rows'):raise ValueError('Servono righe esplicite [PAROLA CHIAVE, SPIEGAZIONE], non text compatto: '+u['id'])
  sec=s.find(id=u['id'])
  if sec is None:raise ValueError('Unità non trovata: '+u['id'])
  existing=sec.select('.lf-summary')
  if not existing:
   labels=[e for e in sec.find_all(['h3','h4','div']) if re.fullmatch(r'(?:IN SINTESI|IN SHORT)(?:\s*[·:–—-].*)?',e.get_text(' ',strip=True),re.I)]
   for e in labels:
    p=next((p for p in e.parents if p is not sec and any(c in p.get('class',[]) for c in ('sintesi','synth','added-summary'))),None)
    if p is not None and not any(p is q for q in existing):existing.append(p)
  for e in existing:e.decompose()
  sec.append(summary(s,u['id'],u['rows'],u['color'],ty,u.get('lang','it'),u.get('label')));report['summaries_replaced'].append(u['id'])
 for m in config.get('maps',[]):
  node=concept_map(s,m['id'],m,ty,m.get('lang','it'));old=s.find(id=m['id'])
  if old:old.replace_with(node)
  else:
   fonti=s.find(id='fonti')
   if fonti:fonti.insert_before(node)
   else:s.body.append(node)
  for a in s.select(f'#indice a[href="#{m["id"]}"]'):
   if a.get_text(strip=True):a.string=TITLE
  report['maps_replaced'].append(m['id'])
 return str(s),report

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('html');p.add_argument('config');p.add_argument('output');a=p.parse_args();src=Path(a.html).resolve();out=Path(a.output).resolve()
 if src==out or out.exists():p.error('Usare un output NUOVO. Il sorgente e i file esistenti non vengono sovrascritti.')
 text,report=apply(src.read_text(),json.loads(Path(a.config).read_text()));out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text);print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

