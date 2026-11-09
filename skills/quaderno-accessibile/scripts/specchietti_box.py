#!/usr/bin/env python3
"""Rendere sintesi tabellari e mappe a box da dati editoriali espliciti. Nessuna API."""
from bs4 import BeautifulSoup
from pathlib import Path
import json,argparse,re
TITLE='MAPPA CONCETTUALE FINALE'
CSS='''
/* Standard approvato 2 novembre 2026: sintesi SENZA grassetto; mappe 78x78mm, solo parole chiave, immagini 52mm. */
.lf-summary,.lf-simple-map{font-family:OpenDyslexic!important;font-size:var(--body-size)!important;line-height:var(--body-leading)!important;color:#111!important}
.lf-summary *,.lf-simple-map *{font-family:OpenDyslexic!important;font-size:var(--body-size)!important;line-height:var(--body-leading)!important;box-sizing:border-box}
.lf-summary{margin:14px 0 10px!important;border:1.2pt solid var(--summary-color);border-radius:9px;background:#fffaf0!important;break-inside:avoid}
.lf-summary-table{width:100%!important;table-layout:fixed!important;border-collapse:collapse!important;border-spacing:0!important;border:0!important;background:#fffaf0!important;margin:0!important;padding:0!important;break-inside:avoid}
.lf-summary-table thead{display:table-header-group}
.lf-summary-table tr{break-inside:avoid!important}
.lf-summary-table th,.lf-summary-table td{border:0!important;padding:8px 11px!important;background:#fffaf0!important;vertical-align:middle!important}
.lf-summary-table thead th{background:var(--summary-color)!important;color:#fff!important;padding:5px 10px!important}
.lf-summary-table h4{margin:0!important;padding:0!important;background:transparent!important;color:#fff!important;text-align:center!important;font-weight:400!important;break-after:avoid!important}
.lf-summary-table tbody th{color:var(--summary-color)!important;text-align:center!important;font-weight:400!important;border-top:1px solid #ded7c5!important;overflow-wrap:anywhere}
.lf-summary-table tbody td{color:#111!important;text-align:left!important;font-weight:400!important;border-top:1px solid #ded7c5!important}
.lf-summary-table p{margin:0!important;padding:0!important;color:#111!important;background:transparent!important;text-align:left!important}
.lf-summary,.lf-summary *{font-weight:400!important}
.lf-simple-map{break-before:page!important;page-break-before:always!important;background:white!important}
.lf-simple-map .lf-map-title,.lf-simple-map .lf-map-root,.lf-simple-map .lf-map-group-title{background:transparent!important;color:#243c5a!important;border:0!important;border-radius:0!important;text-align:center!important;padding:0!important;margin:0 0 4mm!important;font-weight:700!important;break-after:avoid!important}
.lf-simple-map .lf-map-title{font-size:var(--body-size)!important;margin-bottom:2mm!important}
.lf-simple-map .lf-map-newpage{break-before:page!important;page-break-before:always!important}
.lf-simple-map .lf-map-row{display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:6mm!important;margin:0 0 6mm!important;break-inside:avoid!important;page-break-inside:avoid!important}
.lf-simple-map .lf-map-card{display:block!important;box-sizing:border-box!important;width:78mm!important;min-width:78mm!important;max-width:78mm!important;height:78mm!important;min-height:78mm!important;max-height:78mm!important;flex:0 0 78mm!important;background:#fffaf0!important;border:1pt solid var(--card-color)!important;border-radius:3mm!important;padding:4mm 3mm!important;margin:0!important;text-align:center!important;break-inside:avoid!important;page-break-inside:avoid!important;overflow:visible!important}
.lf-simple-map .lf-map-card img.lf-map-image{display:block!important;width:52mm!important;height:29.373mm!important;max-width:none!important;object-fit:contain!important;margin:0 auto 1mm!important;padding:0!important;border:0!important;border-radius:1mm!important}
.lf-simple-map .lf-map-card h4{display:block!important;min-height:0!important;background:transparent!important;color:var(--card-color)!important;font-weight:700!important;text-align:center!important;margin:0 0 1mm!important;padding:0!important;font-size:var(--body-size)!important;line-height:var(--body-leading)!important}
.lf-simple-map .lf-map-card h4 span,.lf-simple-map .lf-map-keywords span{display:block!important;white-space:nowrap!important}
.lf-simple-map .lf-map-keywords{display:block!important;color:#111!important;text-align:center!important;font-weight:400!important;margin:0!important;padding:0!important;font-size:var(--body-size)!important;line-height:var(--body-leading)!important}
'''

def tag(s,name,text=None,**attrs):
 e=s.new_tag(name,attrs=attrs)
 if text is not None:e.string=text
 return e

def summary(s,uid,rows,color,typography,lang='it',label=None):
 if not rows:raise ValueError('Sintesi priva di righe: '+uid)
 box=tag(s,'div',id=uid+'-specchietto',**{'class':'lf-summary','data-summary-for':uid,'data-support-profile':'foto1-tabella','lang':lang,'style':f'--summary-color:{color};{typography}'})
 table=tag(s,'table',**{'class':'lf-summary-table'});box.append(table);colgroup=tag(s,'colgroup');colgroup.append(tag(s,'col',style='width:31%'));colgroup.append(tag(s,'col',style='width:69%'));table.append(colgroup)
 head=tag(s,'thead');tr=tag(s,'tr');th=tag(s,'th',colspan='2');h=tag(s,'h4',label or ('IN SHORT' if lang=='en' else 'IN SINTESI'),id=uid+'-sintesi-titolo',**{'data-editorial-title':''});th.append(h);tr.append(th);head.append(tr);table.append(head);body=tag(s,'tbody');table.append(body)
 for i,(key,text) in enumerate(rows,1):
  tr=tag(s,'tr',id=f'{uid}-sintesi-riga-{i}');th=tag(s,'th',key.upper(),scope='row',id=f'{uid}-sintesi-chiave-{i}',**{'data-editorial-title':''});td=tag(s,'td',id=f'{uid}-sintesi-valore-{i}')
  frag=BeautifulSoup(text,'html.parser')
  # Togliere solo l'enfasi dei riepiloghi; non cambiare i neretti del corpo.
  for bold in frag.select('strong,b'):bold.unwrap()
  for x in list(frag.contents):td.append(x.extract())
  tr.append(th);tr.append(td);body.append(tr)
 return box

def keyword_lines(value,max_lines=None,max_words=None):
 """Non imporre limiti arbitrari alle parole chiave; verificare semantica e geometria."""
 lines=[value] if isinstance(value,str) else value
 if not isinstance(lines,list) or not lines or (max_lines is not None and len(lines)>max_lines):raise ValueError('Usare PAROLE CHIAVE esplicite e non paragrafi.')
 for line in lines:
  if not isinstance(line,str) or not line.strip() or re.search(r'[.!?;<>\n]',line) or (max_words is not None and len(re.findall(r'\w+',line))>max_words):raise ValueError('La mappa accetta PAROLE CHIAVE, non frasi: '+str(line))
 return [x.strip().upper() for x in lines]

def append_lines(s,parent,lines):
 for line in lines:parent.append(tag(s,'span',line))

def concept_map(s,mid,data,typography,lang='it'):
 if data.get('intro') or data.get('notes'):raise ValueError('Niente frasi introduttive/note discorsive nella mappa: conservare i dettagli nel corpo o nelle sintesi, usare qui solo parole chiave.')
 sec=tag(s,'section',id=mid,lang=lang,**{'class':'lf-simple-map','data-final-concept-map':'','data-support-profile':'box-standard-keywords-20261102','style':typography})
 sec.append(tag(s,'h2',TITLE,id=mid+'-titolo',**{'class':'lf-map-title','data-editorial-title':'','lang':'it'}))
 if data.get('root'):sec.append(tag(s,'h3',keyword_lines(data['root'],1,5)[0],id=mid+'-radice',**{'class':'lf-map-root','data-editorial-title':''}))
 palette=['#b23c47','#257041','#14696e','#795548','#744394','#1a5fb4']
 for gi,g in enumerate(data['groups'],1):
  color=g.get('color') or palette[(gi-1)%len(palette)]
  group=tag(s,'div',id=f'{mid}-gruppo-{gi}',**{'class':'lf-map-group'+(' lf-map-newpage' if gi>1 and g.get('new_page',True) else '')});sec.append(group)
  group.append(tag(s,'h3',keyword_lines(g['title'],1,5)[0],id=f'{mid}-gruppo-{gi}-titolo',**{'class':'lf-map-group-title','data-editorial-title':''}))
  if not g.get('nodes'):raise ValueError('Gruppo della mappa privo di nodi.')
  for n in range(0,len(g['nodes']),2):
   row=tag(s,'div',**{'class':'lf-map-row'});group.append(row)
   for ni,node in enumerate(g['nodes'][n:n+2],n+1):
    # Nuovo schema esplicito; compatibilità con [TITOLO,PAROLA CHIAVE] solo se breve.
    if isinstance(node,dict):title=node['title'];keywords=node['keywords'];asset=node.get('image');nodecolor=node.get('color',color)
    else:title,keywords=node;asset=None;nodecolor=color
    titles=keyword_lines(title,2,4);keys=keyword_lines(keywords)
    if asset is None:
     assets=g.get('images',[]);asset=assets[ni-1] if ni<=len(assets) else None
    if not asset or not asset.get('src') or not asset.get('alt'):raise ValueError('Ogni box della mappa richiede una immagine clay esplicativa con src e alt.')
    bid=f'{mid}-gruppo-{gi}-box-{ni}';card=tag(s,'article',id=bid,**{'class':'lf-map-card','style':'--card-color:'+nodecolor,'aria-labelledby':bid+'-titolo'})
    card.append(tag(s,'img',src=asset['src'],alt=asset['alt'],id=bid+'-immagine',**{'class':'lf-map-image'}))
    heading=tag(s,'h4',id=bid+'-titolo',**{'data-editorial-title':''});append_lines(s,heading,titles);card.append(heading)
    paragraph=tag(s,'p',**{'class':'lf-map-keywords'});append_lines(s,paragraph,keys);card.append(paragraph);row.append(card)
 return sec

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('config');p.add_argument('output');a=p.parse_args();out=Path(a.output)
 if out.exists():p.error('Scegliere un output nuovo; nessuna sovrascrittura.')
 c=json.loads(Path(a.config).read_text());s=BeautifulSoup('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>','html.parser');style=tag(s,'style');style.string=CSS;s.head.append(style);ty=f"--body-size:{c['body_font_size_px']}px;--body-leading:{c['body_line_height']};"
 for u in c.get('summaries',[]):s.body.append(summary(s,u['id'],u['rows'],u['color'],ty,u.get('lang','it')))
 for m in c.get('maps',[]):s.body.append(concept_map(s,m['id'],m,ty,m.get('lang','it')))
 out.write_text(str(s))
if __name__=='__main__':main()

