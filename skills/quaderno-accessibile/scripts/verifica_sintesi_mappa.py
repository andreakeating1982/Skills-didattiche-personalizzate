#!/usr/bin/env python3
"""Verificare copertura su unità esplicite; non equiparare le fonti alle unità."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,json,re
LABEL=re.compile(r'^(?:IN SINTESI|IN SHORT|IN BRIEF|SUMMARY)(?:\s*[·:–—\-]\s*.+)?$',re.I)

def summaries(unit):
 labels=[]
 for e in unit.find_all(['h1','h2','h3','h4','strong','b','p','td','div']):
  if LABEL.fullmatch(e.get_text(' ',strip=True)) and not any(LABEL.fullmatch(x.get_text(' ',strip=True)) for x in e.find_all(['h1','h2','h3','h4','strong','b','p','td','div'])):labels.append(e)
 result=[]
 for e in labels:
  wrapper=next((p for p in e.parents if p is not unit and set(p.get('class',[]))&{'sintesi','added-summary','synth','synthesis','summary','sintesi-box'}),None)
  if wrapper is None:wrapper=e.parent
  if not any(x is wrapper for x in result):result.append(wrapper)
 return result

def check(html,manifest):
 s=BeautifulSoup(Path(html).read_text(),'html.parser');cfg=json.loads(Path(manifest).read_text()) if not isinstance(manifest,dict) else manifest;errors=[];units=[];maps=[]
 if not cfg.get('unit_ids'):errors.append({'issue':'unit_manifest_empty'})
 if not cfg.get('final_map_ids'):errors.append({'issue':'final_map_manifest_empty'})
 for uid in cfg.get('unit_ids',[]):
  sec=s.find(id=uid)
  if not sec:errors.append({'issue':'unit_missing','id':uid});continue
  found=summaries(sec);units.append({'id':uid,'summaries':len(found)})
  if len(found)!=1:errors.append({'issue':'summary_count','id':uid,'actual':len(found),'expected':1})
  for x in found:
   heading=x.find(['h1','h2','h3','h4']) or x.select_one('.s-head,.sintesi-title,.synth-title')
   text=x.get_text(' ',strip=True)
   if heading is not None:text=text.replace(heading.get_text(' ',strip=True),'',1)
   if len(re.sub(r'\s+','',text))<20:errors.append({'issue':'summary_empty','id':uid})
 for mid in cfg.get('final_map_ids',[]):
  sec=s.find(id=mid)
  if sec is None:errors.append({'issue':'final_map_missing','id':mid});continue
  maps.append({'id':mid,'text_chars':len(sec.get_text(' ',strip=True))})
  if len(sec.get_text(' ',strip=True))<100:errors.append({'issue':'final_map_empty','id':mid})
  if sec.find_parent(id='fonti') is not None:errors.append({'issue':'map_nested_in_sources','id':mid})
 for e in s.select('[data-summary-for]'):
  uid=e['data-summary-for'];parent=e.find_parent(id=uid)
  if parent is None:errors.append({'issue':'summary_outside_its_unit','id':uid})
 return {'passed':not errors,'units_checked':len(units),'maps_checked':len(maps),'units':units,'maps':maps,'errors':errors,'limits':'Copertura strutturale; verificare separatamente contenuti, lingua, relazioni della mappa, righe reali e resa PDF.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('html');p.add_argument('manifest');p.add_argument('--report');args=p.parse_args();r=check(args.html,args.manifest)
 if args.report:Path(args.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

