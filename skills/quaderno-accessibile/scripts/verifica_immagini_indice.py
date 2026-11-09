#!/usr/bin/env python3
"""Controllare dimensioni reali delle illustrazioni e badge colorati dell'indice.
Non valuta automaticamente lo stile clay adulto: effettuare anche ispezione visiva.
Uso: python3 verifica_immagini_indice.py guida.html --pdf guida.pdf --report qa.json --strict
"""
from pathlib import Path
from collections import defaultdict
import argparse,json,re,math
from bs4 import BeautifulSoup
from weasyprint import HTML
import pymupdf


def rgb(color):
    if isinstance(color,str):
        if color.startswith('#'):
            c=color.lstrip('#')
            if len(c)==3:c=''.join(x*2 for x in c)
            return tuple(int(c[i:i+2],16) for i in (0,2,4))
        return None
    if hasattr(color,'to'):
        try:
            c=color.to('srgb')
            if hasattr(c,'coordinates'):return tuple(round(x*255) for x in c.coordinates[:3])
        except Exception:pass
    if hasattr(color,'red'):return tuple(round(x*255) for x in (color.red,color.green,color.blue))
    # tinycss2/WeasyPrint versions differ; report unmeasurable values instead of guessing.
    numbers=re.findall(r'[-+]?\d*\.?\d+',repr(color).split('srgb')[-1]) if 'srgb' in repr(color) else []
    return tuple(round(float(n)*255) for n in numbers[:3]) if len(numbers)>=3 else None

def contrast(c):
    def lin(x):
        x=x/255
        return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
    luminance=sum(w*lin(x) for w,x in zip((.2126,.7152,.0722),c))
    return 1.05/(luminance+.05)

def check(source,pdf=None):
    path=Path(source).resolve();soup=BeautifulSoup(path.read_text(),'html.parser')
    images=soup.find_all('img')
    badges=soup.select('#indice .ind-num, #indice .badge')
    errors=[]
    for i,img in enumerate(images):
        if not img.get('id'):img['id']=f'qa-image-{i+1}'
        if not img.get('alt','').strip():errors.append(f'Alt assente: {img["id"]}')
    for i,badge in enumerate(badges):
        if not badge.get('id'):badge['id']=f'qa-badge-{i+1}'
    doc=HTML(string=str(soup),base_url=str(path.parent)).render()
    img_ids={i['id'] for i in images};badge_ids={b['id'] for b in badges}
    geometry={};badge_geometry={};anchors={};locations=defaultdict(set)
    for page_n,page in enumerate(doc.pages,1):
        for key in page.anchors:anchors.setdefault(key,page_n)
        for box in page._page_box.descendants():
            e=getattr(box,'element',None)
            if e is None:continue
            eid=e.get('id');kind=type(box).__name__
            if eid in img_ids and 'ReplacedBox' in kind:
                geometry[eid]={'id':eid,'page':page_n,'width_mm':float(box.width)*25.4/96,
                               'height_mm':float(box.height)*25.4/96,
                               'object_fit':box.style['object_fit'],
                               'bbox_pt':[float(box.content_box_x())*.75,float(box.content_box_y())*.75,
                                          float(box.content_box_x()+box.width)*.75,float(box.content_box_y()+box.height)*.75]}
                locations[eid].add(page_n)
            if eid in badge_ids and kind=='BlockBox':
                badge_geometry[eid]={'id':eid,'page':page_n,'background':rgb(box.style['background_color']),
                                     'width_px':float(box.width),'height_px':float(box.height)}
    if len(geometry)!=len(images):errors.append('Non tutte le immagini sono misurabili nel renderer')
    if geometry:
        vals=list(geometry.values());w=vals[0]['width_mm'];h=vals[0]['height_mm']
        for im in vals:
            if abs(im['width_mm']-w)>.2 or abs(im['height_mm']-h)>.2:
                errors.append('Immagine di grandezza differente: '+im['id'])
            if len(locations[im['id']])!=1:errors.append('Immagine spezzata: '+im['id'])
    if not badges:errors.append('Numeri colorati assenti nell’indice')
    rows=[];numeric_colors=[]
    for badge in badges:
        bid=badge['id'];label=badge.get_text(strip=True)
        row=badge.find_parent('tr');bg=badge_geometry.get(bid,{}).get('background')
        if bg is None:errors.append('Colore non misurabile: '+bid)
        elif contrast(bg)<4.5:errors.append('Contrasto del badge con bianco inferiore a 4.5: '+label)
        if label.isdigit() and bg:numeric_colors.append(bg)
        links=row.select('a[href^="#"]') if row else []
        targets={l['href'][1:] for l in links}
        if len(targets)!=1:errors.append('Destinazioni indice incoerenti: '+label)
        target=next(iter(targets),None);target_el=soup.find(id=target) if target else None
        if target_el is None:errors.append('Destinazione mancante: '+str(target))
        if target and target not in anchors:errors.append('Ancora PDF assente: '+target)
        swatch=re.search(r'--section-color\s*:\s*(#[0-9a-fA-F]{6})',(target_el.get('style','') if target_el else ''))
        if swatch and bg and rgb(swatch[1])!=bg:errors.append('Colore badge diverso dalla sezione: '+label)
        rows.append({'label':label,'background_rgb':bg,'target':target,'target_page':anchors.get(target),
                     'contrast_white':round(contrast(bg),2) if bg else None})
    if len(numeric_colors)>1 and len(set(numeric_colors))==1:
        errors.append('Tutti i numeri di capitolo hanno lo stesso colore: ripristinare la palette delle sezioni')
    pdf_images=[];auxiliary_images=[]
    if pdf:
        final=pymupdf.open(Path(pdf).resolve())
        for pn,page in enumerate(final,1):
            for image in page.get_image_info():
                rect=pymupdf.Rect(image['bbox'])
                record={'page':pn,'width_mm':rect.width*25.4/72,'height_mm':rect.height*25.4/72}
                inside=any(im['page']==pn and pymupdf.Rect(im['bbox_pt']).contains(rect)
                           for im in geometry.values())
                # Un emoji a colori puo' comparire come minuscolo raster aggiuntivo.
                # Non confonderlo con le illustrazioni, ma segnalarlo per QA visivo.
                if not inside and record['width_mm']<=10 and record['height_mm']<=10:
                    auxiliary_images.append(record)
                else:pdf_images.append(record)
        if len(final)!=len(doc.pages):errors.append('Numero di pagine diverso tra HTML e PDF')
        if len(pdf_images)!=len(images):errors.append('Numero di immagini diverso tra HTML e PDF')
        if pdf_images:
            first=pdf_images[0]
            for im in pdf_images:
                if abs(im['width_mm']-first['width_mm'])>.2 or abs(im['height_mm']-first['height_mm'])>.2:
                    errors.append('Dimensioni PDF effettive diverse tra le immagini')
    return {'html':str(path),'pdf':str(Path(pdf).resolve()) if pdf else None,'pages':len(doc.pages),
            'images':list(geometry.values()),'pdf_images':pdf_images,'auxiliary_images_for_visual_check':auxiliary_images,'index':rows,'errors':errors,'passed':not errors,
            'limits':'Misure effettive, colori e destinazioni delle illustrazioni; piccoli raster esterni fino a 10mm possono essere emoji/icone e sono elencati a parte, da verificare visivamente. Non verifica stile clay adulto, leggibilità globale o conformità PDF/UA.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('html');ap.add_argument('--pdf');ap.add_argument('--report');ap.add_argument('--strict',action='store_true');args=ap.parse_args()
    result=check(args.html,args.pdf)
    if args.report:
        out=Path(args.report);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.strict and not result['passed']:raise SystemExit(1)

