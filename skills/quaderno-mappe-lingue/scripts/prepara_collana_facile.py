#!/usr/bin/env python3.11
"""Preparare inventario e asset della collana senza toccare i quaderni originali.
Uso: prepara_collana_facile.py [--workdir DIR] [--languages en fr es]
Opzioni sorgente: --en-html FILE --en-pdf FILE, analoghe --fr-* e --es-*.
LF_WORKDIR configura la cartella anche per gli script di build/verifica.
"""
import argparse
import json
import os
from pathlib import Path
import shutil

from bs4 import BeautifulSoup
import pymupdf as fitz

DEFAULTS={
 'en':('/home/user/inglese_build/inglese_accessibile_v3.html',
       '/home/user/inglese_build/Mappe_concettuali_grammatica_inglese_inclusivo_v3.pdf'),
 'fr':('/home/user/mappe-fr/mappe_fr.html','/home/user/mappe-fr/Quaderno_fr.pdf'),
 'es':('/home/user/mappe-es/mappe_es.html','/home/user/mappe-es/Quaderno_es.pdf')
}


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--workdir',default=os.environ.get('LF_WORKDIR','/home/user/facile_edizione'))
 ap.add_argument('--languages',nargs='+',choices=DEFAULTS,default=list(DEFAULTS))
 for lang,(html,pdf) in DEFAULTS.items():
  ap.add_argument(f'--{lang}-html',default=html)
  ap.add_argument(f'--{lang}-pdf',default=pdf)
 args=ap.parse_args()
 work=Path(args.workdir).expanduser().resolve()
 assets=Path(__file__).resolve().parents[1]/'templates'/'collana-facile'
 inventory={}
 # Validare tutte le origini prima di scrivere output o copiare immagini.
 for lang in args.languages:
  html=Path(getattr(args,f'{lang}_html')).expanduser().resolve()
  pdf=Path(getattr(args,f'{lang}_pdf')).expanduser().resolve()
  if not html.is_file() or not pdf.is_file():
   ap.error(f'{lang}: manca HTML/PDF base ({html}; {pdf}); recuperare gli originali, non ricostruire a memoria.')
  soup=BeautifulSoup(html.read_text(encoding='utf-8'),'html.parser')
  if soup.select_one('#lf-copertina') is not None:
   ap.error(f'{lang}: origine già nella veste FACILE; usare il sorgente base per non duplicare pagine editoriali.')
  maps=soup.select('section.pg .blk[id]')
  if not maps or soup.style is None:
   ap.error(f'{lang}: struttura HTML non supportata; richieste section.pg, .blk[id] e style.')
  ids=[m['id'] for m in maps]
  if len(set(ids))!=len(ids):
   ap.error(f'{lang}: ancore duplicate nelle mappe.')
  with fitz.open(pdf) as doc:
   bookmarks={''.join(title.split()).casefold() for _,title,_ in doc.get_toc()}
   for m in maps:
    title=m.h2.get_text(' ',strip=True)
    if ''.join(title.split()).casefold() not in bookmarks:
     ap.error(f'{lang}: mappa {title!r} non trovata nei segnalibri del PDF. Sincronizzare HTML e PDF base.')
   pages=len(doc)
  inventory[lang]={'html':str(html),'pdf':str(pdf),'pages':pages,'map_count':len(maps),
   'maps':[{'id':m['id'],'title':m.h2.get_text(' ',strip=True),
            'color':m.select_one('.banner').get('style','')} for m in maps]}
 work.mkdir(parents=True,exist_ok=True)
 dest=work/'inventory.json'
 if dest.exists():
  old=json.loads(dest.read_text(encoding='utf-8'))
  if old!=inventory:
   backup=work/'inventory.precedente.json'
   if not backup.exists(): shutil.copy2(dest,backup)
 dest.write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
 for lang in args.languages:
  name=f'cover_{lang}.png'
  if not (work/name).exists(): shutil.copy2(assets/name,work/name)
 preview=work/'Copertine_Facile.png'
 if not preview.exists(): shutil.copy2(assets/preview.name,preview)
 for lang,item in inventory.items():
  print(lang,':',item['map_count'],'mappe;',item['pages'],'pagine base')
 print('Inventario pronto:',dest)
 print('Sorgenti e immagini approvate esistenti NON modificati.')


if __name__=='__main__':
 main()

