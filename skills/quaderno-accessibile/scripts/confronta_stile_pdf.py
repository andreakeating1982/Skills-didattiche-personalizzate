#!/usr/bin/env python3
"""Confrontare due PDF senza modificarli: testo/enfasi, tipografia, box e immagini.
Uso: python3 confronta_stile_pdf.py originale.pdf revisione.pdf --report confronto.json
L'allineamento/lo stile iconografico richiedono anche ispezione visiva e sorgenti CSS.
"""
from pathlib import Path
from collections import Counter
import argparse,json,re,difflib
import pymupdf


def norm(t):return re.sub(r'\s+',' ',t).strip()
def hex_color(rgb):
    if rgb is None:return None
    if len(rgb)==1:rgb=rgb*3
    return '#'+''.join(f'{max(0,min(255,round(x*255))):02x}' for x in rgb[:3])

def inventory(file,body_pt=13):
    doc=pymupdf.open(file);fonts=Counter();styles=Counter();pages=[];body=[];bold_runs=[];boxes=[];banners=[];images=[]
    for pn,page in enumerate(doc,1):
        spans=[s for b in page.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
        for s in spans:
            bold=bool(s.get('flags',0)&16) or 'bold' in s['font'].lower()
            fonts[s['font']]+=len(s['text']);styles[(round(s['size'],2),f'#{s["color"]:06x}',bold)]+=len(s['text'])
            if abs(s['size']-body_pt)<.04:
                body.extend((c,bold,s['color']) for c in s['text'] if not c.isspace())
                if bold and s['text'].strip():bold_runs.append({'page':pn,'text':s['text'],'color':f'#{s["color"]:06x}'})
        body_lines=[line for block in page.get_text('dict')['blocks'] if block['type']==0 for line in block['lines'] if any(abs(s['size']-body_pt)<.04 for s in line['spans'])]
        page_boxes=[];page_banners=[]
        for d in page.get_drawings():
            color=hex_color(d.get('fill'));r=d['rect'];item={'page':pn,'rect_pt':[round(x,3) for x in r],'color':color,'height_pt':round(r.height,3),'width_pt':round(r.width,3)}
            if color=='#fffaf0' and r.width>200 and r.height>20:
                contained=sorted({round(line['bbox'][1],3) for line in body_lines if r.y0<=line['bbox'][1] and line['bbox'][3]<=r.y1})
                item['body_lines']=len(contained)
                item['leading_pt']=sorted({round(b-a,3) for a,b in zip(contained,contained[1:])})
                page_boxes.append(item);boxes.append(item)
            elif color and color not in ('#ffffff','#000000','#111111','#161616','#e6d5ae') and r.width>400 and 18<r.height<150:
                page_banners.append(item);banners.append(item)
        for im in page.get_image_info():
            r=pymupdf.Rect(im['bbox']);images.append({'page':pn,'width_mm':round(r.width*25.4/72,3),'height_mm':round(r.height*25.4/72,3),'pixels':[im['width'],im['height']]})
        starts=[s['bbox'][1] for s in spans if abs(s['size']-body_pt)<.04]
        steps=Counter()
        for b in page.get_text('dict')['blocks']:
            if b['type']!=0:continue
            lines=[l for l in b['lines'] if any(abs(s['size']-body_pt)<.04 for s in l['spans'])]
            for a,b in zip(lines,lines[1:]):
                step=b['bbox'][1]-a['bbox'][1]
                if 0<step<40:steps[round(step,2)]+=1
        pages.append({'page':pn,'text_chars':len(page.get_text()),'body_lines_step_pt':dict(steps),'cream_boxes':len(page_boxes),
                      'banners':page_banners,'text_start_x_pt':round(min((s['bbox'][0] for s in spans if abs(s['size']-body_pt)<.04),default=0),3)})
    return {'file':str(Path(file).resolve()),'page_count':len(doc),'fonts_char_counts':dict(fonts),'styles':[{'pt':k[0],'color':k[1],'bold':k[2],'characters':v} for k,v in styles.items()],
            'body_text':''.join(c for c,b,col in body),'body_bold_mask':[b for c,b,col in body],'body_colors':[col for c,b,col in body],
            'body_bold_characters':sum(b for c,b,col in body),'bold_runs':bold_runs,'cream_boxes':boxes,'banners':banners,'images':images,'pages':pages,
            'pdf_links':sum(len(p.get_links()) for p in doc),'pdf_bookmarks':len(doc.get_toc())}

def compare(a,b,body_pt=13):
    old=inventory(a,body_pt);new=inventory(b,body_pt);sm=difflib.SequenceMatcher(None,old['body_text'],new['body_text'],autojunk=False)
    text_changes=[];emphasis_changes=[];matching=0;color_changes=0
    for tag,a1,a2,b1,b2 in sm.get_opcodes():
        if tag!='equal':
            text_changes.append({'operation':tag,'old':old['body_text'][a1:a2],'new':new['body_text'][b1:b2]});continue
        matching+=a2-a1
        differences=[j for j in range(a2-a1) if old['body_bold_mask'][a1+j]!=new['body_bold_mask'][b1+j]]
        if differences:emphasis_changes.append({'old_position':a1,'new_position':b1,'characters_changed':len(differences),'matching_text':old['body_text'][a1:a2]})
        color_changes+=sum(old['body_colors'][a1+j]!=new['body_colors'][b1+j] for j in range(a2-a1))
    for item in (old,new):
        item.pop('body_bold_mask');item.pop('body_colors')
    return {'original':old,'revised':new,'body_comparison':{'matching_nonspace_characters':matching,'text_changes':text_changes,'bold_changes_in_equal_text':emphasis_changes,'color_changes_in_equal_text':color_changes,
             'bold_preserved_in_equal_text':not emphasis_changes},'limits':'Per il corpo filtra i font per misura: controllare body_pt e verificare a parte titoli, indice, caption e fonti. Non certifica PDF/UA né stile clay adulto.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('original');p.add_argument('revised');p.add_argument('--body-pt',type=float,default=13);p.add_argument('--report');args=p.parse_args()
    result=compare(args.original,args.revised,args.body_pt)
    if args.report:
        path=Path(args.report);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({'pages':[result['original']['page_count'],result['revised']['page_count']],
         'bold_body_characters':[result['original']['body_bold_characters'],result['revised']['body_bold_characters']],
         'body_comparison':result['body_comparison'],'images':[result['original']['images'],result['revised']['images']],
         'banner_colors':[[b['color'] for b in result[k]['banners']] for k in ('original','revised')],
         'cream_boxes':[len(result['original']['cream_boxes']),len(result['revised']['cream_boxes'])],
         'body_card_max_lines':[max((b['body_lines'] for b in result[k]['cream_boxes']),default=0) for k in ('original','revised')],
         'leading_pt':[sorted({n for b in result[k]['cream_boxes'] for n in b['leading_pt']}) for k in ('original','revised')],
         'font_styles':[result['original']['styles'],result['revised']['styles']]},ensure_ascii=False,indent=2))

