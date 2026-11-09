#!/usr/bin/env python3
"""Verificare UNA immagine subito dopo il banner di ogni unità dichiarata.
Manifest: unit_sections, images_per_unit=1, cover_selector, forbidden_image_sections.
Controllare DOM e geometria renderizzata; non riconosce stile/pertinenza né certifica PDF/UA.
"""
from pathlib import Path
import argparse,json
from bs4 import BeautifulSoup
from weasyprint import HTML


def check(html,manifest):
    html=Path(html).resolve();cfg=json.loads(Path(manifest).read_text());s=BeautifulSoup(html.read_text(),'html.parser')
    ids=cfg['unit_sections'];errors=[];records=[];wanted={};expected=cfg.get('images_per_unit',1)
    if len(ids)!=len(set(ids)):raise ValueError('Unità duplicate nel manifest')
    for sid in ids:
        sec=s.find(id=sid)
        if sec is None:errors.append({'id':sid,'issue':'missing_unit'});continue
        h=sec.find(['h1','h2','h3'],recursive=False);ims=sec.select('img')
        if len(ims)!=expected:errors.append({'id':sid,'issue':'wrong_image_count','expected':expected,'actual':len(ims)})
        if h is None:errors.append({'id':sid,'issue':'missing_direct_banner'});continue
        im=h.find_next_sibling()
        if im is None or im.name!='img':errors.append({'id':sid,'issue':'image_not_immediately_after_banner'});continue
        if not im.get('alt','').strip():errors.append({'id':sid,'issue':'empty_alt'})
        if not (html.parent/im.get('src','')).is_file():errors.append({'id':sid,'issue':'missing_local_image'})
        # IDs aggiunti solo nella copia in memoria per misure deterministiche.
        h['id']=h.get('id') or sid+'-qa-banner';im['id']=im.get('id') or sid+'-qa-image'
        wanted[sid]=(h['id'],im['id']);records.append({'unit':sid,'image':im.get('src'),'image_count':len(ims)})
    for sid in cfg.get('forbidden_image_sections',[]):
        el=s.find(id=sid)
        if el is not None and el.select('img'):errors.append({'id':sid,'issue':'forbidden_images'})
    covers=s.select(cfg.get('cover_selector','#indice img'))
    if len(covers)!=1:errors.append({'issue':'cover_count_not_one','actual':len(covers)})
    if len(s.select('img'))!=len(ids)*expected+len(covers):errors.append({'issue':'images_outside_declared_units_or_cover'})
    doc=HTML(string=str(s),base_url=str(html.parent)).render();geometry={}
    all_ids={x for pair in wanted.values() for x in pair}
    for pn,page in enumerate(doc.pages,1):
        for b in page._page_box.descendants():
            el=getattr(b,'element',None)
            if el is None or el.get('id') not in all_ids:continue
            if type(b).__name__!='BlockBox' and 'ReplacedBox' not in type(b).__name__:continue
            geometry.setdefault(el.get('id'),{'page':pn,'top':float(b.border_box_y()),'bottom':float(b.border_box_y()+b.border_height()),'width':float(b.width),'height':float(b.height)})
    for row in records:
        sid=row['unit'];head,img=wanted[sid];hb=geometry.get(head);ib=geometry.get(img)
        if not hb or not ib:errors.append({'id':sid,'issue':'banner_or_image_not_rendered'});continue
        row.update(page=hb['page'],image_page=ib['page'],gap_pt=round((ib['top']-hb['bottom'])*.75,3),image_size_mm=[round(ib[k]*25.4/96,3) for k in ('width','height')])
        if hb['page']!=ib['page']:errors.append({'id':sid,'issue':'banner_image_on_different_pages'})
        if ib['top']<hb['bottom']-.1:errors.append({'id':sid,'issue':'image_overlaps_banner'})
    return {'html':str(html),'pages':len(doc.pages),'units_required':len(ids),'cover_images':len(covers),'images_total':len(s.select('img')),'units':records,'errors':errors,'passed':not errors,'limits':'Verifica DOM e renderer; affiancare QA del PDF esportato, stile clay, pertinenza, testi, indice e nuovi inizi pagina.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('html');p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--strict',action='store_true');a=p.parse_args()
    r=check(a.html,a.manifest);out=Path(a.report);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
    if a.strict and not r['passed']:raise SystemExit(1)

