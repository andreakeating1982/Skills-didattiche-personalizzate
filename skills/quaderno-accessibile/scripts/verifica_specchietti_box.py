#!/usr/bin/env python3
"""QA: sintesi senza grassetto, mappe con box 78x78mm/parole chiave/immagini52mm. Nessuna API."""
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
from collections import defaultdict
import argparse,json,re
TITLE='MAPPA CONCETTUALE FINALE'

def check(html,manifest):
 h=Path(html).resolve();s=BeautifulSoup(h.read_text(),'html.parser');cfg=json.loads(Path(manifest).read_text()) if not isinstance(manifest,dict) else manifest;errors=[];summaries=[];maps=[];allids={};fragments=defaultdict(set);styles=defaultdict(set);texts=defaultdict(set);pitches=defaultdict(list)
 units=cfg.get('unit_ids',[]);mids=cfg.get('final_map_ids',[]);geometry={};image_geometry={};summary_weights=set();seen_geometry=set();map_node_ids=set()
 if not units or not mids:errors.append({'issue':'empty_manifest'})
 for uid in units:
  sec=s.find(id=uid);found=sec.select('.lf-summary') if sec else []
  if len(found)!=1:errors.append({'issue':'summary_count','unit':uid,'count':len(found)});continue
  su=found[0];rows=su.select('tbody > tr');labels=su.select('thead th');columns=all(len(r.find_all(['th','td'],recursive=False))==2 for r in rows)
  if not rows or not columns or len(labels)!=1:errors.append({'issue':'summary_not_two_column_table','unit':uid})
  if su.find_next_sibling():errors.append({'issue':'summary_not_at_end_of_unit','unit':uid})
  if su.select('strong,b'):errors.append({'issue':'summary_bold_markup','unit':uid})
  summaries.append({'id':uid,'rows':len(rows)})
  allids[su['id']]='summary'
  for r in rows:
   allids[r['id']]='summary_row'
   for cell in r.find_all(['th','td'],recursive=False):allids[cell['id']]='summary_cell'
 for mid in mids:
  sec=s.find(id=mid)
  if not sec or 'lf-simple-map' not in sec.get('class',[]):errors.append({'issue':'map_not_simple_boxes','id':mid});continue
  title=sec.find(['h1','h2'],recursive=False)
  if not title or title.get_text(' ',strip=True)!=TITLE:errors.append({'issue':'map_title_not_standard','id':mid})
  if re.search('[↓↑↔➜➝]',sec.get_text()):errors.append({'issue':'graphical_connector_in_map','id':mid})
  if sec.select('svg,.map-stem,.added-map-relation,.added-map-grid'):errors.append({'issue':'old_map_connectors','id':mid})
  nodes=sec.select('.lf-map-card')
  if not nodes:errors.append({'issue':'no_map_boxes','id':mid})
  for node in nodes:
   allids[node['id']]='map_box';map_node_ids.add(node['id'])
   if node.get('colspan'):errors.append({'issue':'map_box_full_width_colspan','id':node['id']})
   if not node.select('p.lf-map-keywords'):errors.append({'issue':'map_keywords_not_explicit','id':node['id']})
   for field in node.select('h4,p'):
    lines=field.find_all('span',recursive=False) or [field]
    for line in lines:
     t=line.get_text(' ',strip=True)
     # Non limitare il numero delle espressioni o delle parole: i titoli delle opere
     # restano integrali. Punteggiatura e geometria non sostituiscono il giudizio umano.
     if not t or re.search(r'[.!?;]',t):errors.append({'issue':'map_sentence_or_too_many_words','id':node['id'],'text':t})
     if t!=t.upper():errors.append({'issue':'map_keywords_not_uppercase','id':node['id'],'text':t})
   ims=node.select('img.lf-map-image')
   if len(ims)!=1 or not ims[0].get('alt','').strip():errors.append({'issue':'map_box_image_missing_or_no_alt','id':node['id']})
   elif not ims[0].get('src','').startswith(('https://','http://','data:','file:')) and not (h.parent/ims[0]['src']).is_file():errors.append({'issue':'map_box_image_file_missing','id':node['id']})
  maps.append({'id':mid,'boxes':len(nodes)})
 # Il CSS può essere sovrascritto: misurare lo stile renderizzato, non soltanto il sorgente.
 doc=HTML(filename=str(h)).render();expected_size=cfg.get('body_font_size_px');expected_lh=cfg.get('body_line_height');measured=[]
 for pn,page in enumerate(doc.pages,1):
  parents={}
  for b in page._page_box.descendants():
   for child in getattr(b,'children',[]):parents[child]=b
  for b in page._page_box.descendants():
   e=getattr(b,'element',None)
   if e is None:continue
   if e.get('id') in allids and type(b).__name__ in ('BlockBox','TableCellBox','TableRowBox'):fragments[e.get('id')].add(pn)
   eid=e.get('id');kind=type(b).__name__
   if eid in map_node_ids and kind in ('BlockBox','TableCellBox'):
    token=(eid,pn)
    if token not in seen_geometry:
     seen_geometry.add(token);w=b.border_width()*25.4/96;hh=b.border_height()*25.4/96;geometry[eid]={'width_mm':w,'height_mm':hh,'page':pn}
     if abs(w-78)>.1 or abs(hh-78)>.1:errors.append({'issue':'map_box_not_standard_78mm_square','id':eid,'width_mm':w,'height_mm':hh})
     x,y=b.border_box_x(),b.border_box_y();right=x+b.border_width();bottom=y+b.border_height()
     for sub in b.descendants():
      typ=type(sub).__name__
      if 'ReplacedBox' in typ:
       iw=sub.width*25.4/96;ih=sub.height*25.4/96;image_geometry[eid]={'width_mm':iw,'height_mm':ih}
       if abs(iw-52)>.1 or abs(ih-29.373)>.1:errors.append({'issue':'map_image_not_standard_52mm','id':eid,'width_mm':iw,'height_mm':ih})
      if typ=='LineBox' and (sub.position_y+sub.height>bottom-2 or sub.position_x<x-1 or sub.position_x+sub.width>right+1):errors.append({'issue':'map_content_outside_box','id':eid,'page':pn})
   if type(b).__name__!='TextBox' or not b.text.strip():continue
   cur=b;support=None
   while cur is not None:
    el=getattr(cur,'element',None)
    if el is not None and ('lf-summary' in el.get('class','').split() or 'lf-simple-map' in el.get('class','').split()):support=el;break
    cur=parents.get(cur)
   if support is None:continue
   fs=b.style['font_size'];lh=b.style['line_height'];numeric=float(lh) if isinstance(lh,(float,int)) else lh[1] if isinstance(lh,tuple) and lh[0]=='NUMBER' else None
   if expected_size is not None and abs(fs-expected_size)>.001:errors.append({'issue':'support_font_size_not_body','page':pn,'text':b.text,'actual':fs,'expected':expected_size})
   if expected_lh is not None and (numeric is None or abs(numeric-expected_lh)>.001):errors.append({'issue':'support_line_height_not_body','page':pn,'text':b.text,'actual':str(lh),'expected':expected_lh})
   if 'lf-summary' in support.get('class','').split():
    weight=b.style['font_weight'];summary_weights.add(weight)
    if weight!=400:errors.append({'issue':'summary_font_not_regular_400','page':pn,'text':b.text,'actual':weight})
   measured.append((round(fs,5),numeric));texts[support.get('id')].add(pn)
 for id,kind in allids.items():
  pages=sorted(fragments[id])
  if not pages:errors.append({'issue':'support_not_rendered','id':id,'kind':kind})
  if kind in ('summary_row','summary_cell','map_box') and len(pages)>1:errors.append({'issue':'row_or_box_split','id':id,'pages':pages})
 return {'passed':not errors,'pages':len(doc.pages),'units_checked':len(summaries),'summary_rows':sum(x['rows'] for x in summaries),'maps_checked':len(maps),'map_boxes':sum(x['boxes'] for x in maps),'map_images':len(s.select('.lf-map-card img.lf-map-image')),'summaries':summaries,'maps':maps,'measured_typography':sorted(set(measured)),'summary_font_weights':sorted(summary_weights),'map_geometry':geometry,'map_image_geometry':image_geometry,'support_pages':{k:sorted(v) for k,v in texts.items()},'errors':errors,'limits':'Sintesi: tutte le righe necessarie, mai grassetto (anche titoli/celle). Mappe: 78x78mm e immagini52mm; numero di box/pagine libero, solo parole chiave. Non esiste un numero massimo fisso di parole chiave: verificare spazi e leggibilità. Il controllo strutturale non è una prova semantica: leggere ogni nodo per escludere frasi o contenuti estranei. Interlinea/dimensione confrontate col corpo; niente cinque righe ai supporti. Nessuna certificazione PDF/UA indipendente.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('html');p.add_argument('manifest');p.add_argument('--report');a=p.parse_args();r=check(a.html,a.manifest)
 if a.report:Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

