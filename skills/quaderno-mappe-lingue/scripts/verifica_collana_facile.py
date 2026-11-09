#!/usr/bin/env python3.11
from pathlib import Path
import json,re,hashlib,difflib,collections,os,sys
import pymupdf as fitz
import numpy as np
from bs4 import BeautifulSoup

R=Path(os.environ.get('LF_WORKDIR','/home/user/facile_edizione')).expanduser().resolve()
inventory=json.loads((R/'inventory.json').read_text())
report={}

def clean(s):
 return re.sub(r'\s+','',s).casefold()

def first_map_page(doc,title):
 target=clean(title)
 for level,text,p in doc.get_toc():
  if clean(text)==target: return p-1
 raise ValueError(('map1 not found',title,doc.get_toc()[:15]))

languages=sys.argv[1:] or ['en','fr','es']
if any(lang not in ('en','fr','es') for lang in languages):
 raise SystemExit('Specificare soltanto en, fr, es')
for lang in languages:
 man=json.loads((R/f'{lang}_manifest.json').read_text())
 old=fitz.open(man['source_pdf']); new=fitz.open(man['pdf'])
 old_start=first_map_page(old,inventory[lang]['maps'][0]['title'])
 new_start=first_map_page(new,inventory[lang]['maps'][0]['title'])
 old_maps=len(old)-old_start; new_maps=len(new)-new_start
 details={'pages':len(new),'map_count':man['map_count'],'map_pages_original':old_maps,
  'map_pages_new':new_maps,'maps_start_page':new_start+1,
  'html_maps_byte_identical':man['map_html_byte_identical'],'pixel_identical_pages':0,
  'text_identical_pages':0,'pixel_differences':[],'invalid_links':[],'internal_links':0,
  'front_pages':[],'metadata':new.metadata,'bookmarks':len(new.get_toc()),
  'index_page_number_errors':[],'unique_map_destinations':0}
 print('\n===',lang,'pages',len(new),'map1',new_start+1,'map pages',new_maps,'===',flush=True)
 assert old_maps==new_maps,(lang,'changed map page count',old_maps,new_maps)
 for i in range(old_maps):
  a=old[old_start+i]; b=new[new_start+i]
  area=fitz.Rect(0,0,a.rect.width,a.rect.height-55)
  sa=a.get_text(clip=area); sb=b.get_text(clip=area)
  if sa==sb: details['text_identical_pages']+=1
  else:
   (R/f'{lang}_text_diff_{i+1}.txt').write_text('\n'.join(difflib.unified_diff(sa.splitlines(),sb.splitlines())))
  # Prova visiva su OGNI pagina delle mappe, esclusi soli footer/paginazione.
  pix_a=a.get_pixmap(matrix=fitz.Matrix(1,1),clip=area,alpha=False)
  pix_b=b.get_pixmap(matrix=fitz.Matrix(1,1),clip=area,alpha=False)
  if pix_a.samples==pix_b.samples: details['pixel_identical_pages']+=1
  else:
   aa=np.frombuffer(pix_a.samples,dtype=np.uint8); bb=np.frombuffer(pix_b.samples,dtype=np.uint8)
   if aa.shape==bb.shape:
    mismatch=float(np.mean(aa!=bb)); maxdiff=int(np.max(np.abs(aa.astype(np.int16)-bb.astype(np.int16))))
   else: mismatch=1.; maxdiff=255
   details['pixel_differences'].append({'old_page':old_start+i+1,'new_page':new_start+i+1,'channel_mismatch_ratio':mismatch,'max_difference':maxdiff})
 map_destinations=set()
 for i,p in enumerate(new):
  for link in p.get_links():
   if link['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and 'page' in link:
    details['internal_links']+=1
    if not 0<=link.get('page',-1)<len(new): details['invalid_links'].append({'from_page':i+1,'link':str(link)})
    name=link.get('nameddest','')
    if re.fullmatch(r'm\d+',name):
     map_destinations.add(name)
     if 5<=i<new_start and link['from'].x0>500:
      box=fitz.Rect(link['from']); box.x0-=1; box.y0-=1; box.x1+=1; box.y1+=1
      actual=p.get_textbox(box).strip()
      expected=str(link['page']+1)
      if actual!=expected: details['index_page_number_errors'].append({'page':i+1,'map':name,'printed':actual,'expected':expected})
  if i<new_start:
   blocks=p.get_text('blocks')
   main=[b for b in blocks if b[1]<p.rect.height-55 and str(b[4]).strip() and b[6]==0]
   text=p.get_text()
   details['front_pages'].append({'page':i+1,'top':text[:100].replace('\n',' | '),
    'last_text_y':max([b[3] for b in main],default=0),'text_length':len(text)})
 assert details['text_identical_pages']==old_maps,(lang,'map text changed',details['text_identical_pages'],old_maps)
 assert details['pixel_identical_pages']==old_maps,(lang,'map appearance changed',details['pixel_differences'][:3])
 details['unique_map_destinations']=len(map_destinations)
 assert len(map_destinations)==man['map_count'],(lang,'missing map links',len(map_destinations))
 assert not details['invalid_links'],(lang,'invalid links')
 assert not details['index_page_number_errors'],(lang,'wrong printed page numbers',details['index_page_number_errors'][:3])
 # Anteprime copertina, guide, legenda, indice e due pagine originali.
 previews=[0,1,2,3,4,5,new_start,len(new)-1]
 if lang=='en':
  for _,text,p in new.get_toc():
   if 'ASKING FOR AND GIVING DIRECTIONS' in text: previews.append(p-1)
 for i in sorted(set(previews)):
  new[i].get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(R/f'{lang}_pagina_{i+1:02d}.png')
 report[lang]=details
 print('PIXELS IDENTICAL',details['pixel_identical_pages'],'/',old_maps,
       'TEXT IDENTICAL',details['text_identical_pages'],'LINKS',details['internal_links'],flush=True)
 for p in details['front_pages']: print('FRONT',p,flush=True)
 print('DIFFERENCES',details['pixel_differences'][:3],flush=True)
 print('TOC FIRST',new.get_toc()[:8],flush=True)
(R/'verifica_completa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('\nREPORT',R/'verifica_completa.json',flush=True)

