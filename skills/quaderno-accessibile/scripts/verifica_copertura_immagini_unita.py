#!/usr/bin/env python3
"""Verificare copertina, immagini a ogni unità e assenza di immagini nelle fonti.
Richiedere titoli marcati data-editorial-unit; gli alt e lo stile richiedono anche QA visivo.
Non modificare HTML/PDF, non generare immagini e non certificare PDF/UA.
"""
from pathlib import Path
from urllib.parse import urlparse, unquote
import argparse,json
from bs4 import BeautifulSoup


def check(source,unit_selector='[data-editorial-unit]',sources_selector='#fonti,#sources,[data-unit-kind="sources"]',cover_selector='#indice img.editorial-image'):
    path=Path(source).resolve();soup=BeautifulSoup(path.read_text(),'html.parser')
    errors=[];warnings=[];records=[]
    images=soup.find_all('img');units=soup.select(unit_selector);covers=soup.select(cover_selector)
    source_regions=soup.select(sources_selector)
    source_img_ids={id(im) for region in source_regions for im in region.find_all('img')}
    if not covers:errors.append('Immagine clay adulta di copertina assente')
    if len(covers)>1:errors.append('Più immagini di copertina: controllare il selettore o il modello')
    if not units:errors.append('Nessuna unità dichiarata: marcare i titoli con data-editorial-unit o fornire --units')
    if not source_regions:warnings.append('Sezione fonti non individuata: verificare --sources o dichiararne l’assenza')
    for region in source_regions:
        if region.find('img'):errors.append('Immagine vietata nella sezione fonti: '+str(region.get('id','senza-id')))
    for n,im in enumerate(images,1):
        ident=im.get('id',f'immagine-{n}')
        if not im.get('alt','').strip():errors.append('Alt assente: '+ident)
        src=im.get('src','');url=urlparse(src)
        if not src:errors.append('Sorgente immagine assente: '+ident)
        elif url.scheme in ('http','https'):warnings.append('Asset remoto, includerlo nei sorgenti: '+ident)
        elif url.scheme!='data' and not (path.parent/unquote(src)).is_file():errors.append('File immagine mancante: '+src)
        declaration=im.get('data-illustration-style')
        if declaration and declaration!='clay-adulto' and id(im) not in source_img_ids:
            errors.append('Stile dichiarato non clay adulto: '+ident+' ('+declaration+')')
    seen=set()
    for n,unit in enumerate(units,1):
        ident=unit.get('data-editorial-unit') or unit.get('id') or f'unita-{n}'
        if ident in seen:errors.append('Identificatore di unità duplicato: '+ident)
        seen.add(ident)
        if any(unit is r or r in unit.parents for r in source_regions):continue
        image=unit.find_next_sibling()
        if image is None or image.name!='img':
            errors.append('Immagine non presente subito dopo il titolo: '+ident);continue
        if id(image) in source_img_ids:errors.append('Unità collegata a immagine nelle fonti: '+ident)
        lang=unit.get('lang')
        if not lang:
            parent=unit.find_parent(attrs={'lang':True});lang=parent.get('lang') if parent else None
        records.append({'unit':ident,'title':unit.get_text(' ',strip=True),'image':image.get('src'),'alt':image.get('alt'),'lang':lang,'image_id':image.get('id')})
    return {'html':str(path),'cover_images':len(covers),'units_declared':len(units),'units_illustrated':len(records),'total_images':len(images),'source_images':len(source_img_ids),'units':records,'errors':errors,'warnings':warnings,'passed':not errors,'limits':'Copertura e struttura, non riconoscimento visivo clay né controllo semantico della lingua degli alt. Affiancare verifica_immagini_indice.py, confronto testo/enfasi e ispezione PDF/Word.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html');ap.add_argument('--units',default='[data-editorial-unit]');ap.add_argument('--sources',default='#fonti,#sources,[data-unit-kind="sources"]');ap.add_argument('--cover',default='#indice img.editorial-image');ap.add_argument('--report');ap.add_argument('--strict',action='store_true')
    args=ap.parse_args();r=check(args.html,args.units,args.sources,args.cover)
    if args.report:
        out=Path(args.report);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False,indent=2))
    if args.strict and not r['passed']:raise SystemExit(1)

