#!/usr/bin/env python3
"""Controlli regressione: schema/cronologia spostati, resto uguale alla versione approvata."""
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
import hashlib,json,re,unicodedata
import fitz

R=Path(__file__).resolve().parent.parent
OLD=BeautifulSoup((R/'qa/PRECEDENTE.html').read_text(encoding='utf8'),'html.parser')
H=R/'MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.html';s=BeautifulSoup(H.read_text(encoding='utf8'),'html.parser')
P=R/'MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.pdf';p=fitz.open(P)
d=HTML(filename=str(H),base_url=str(R)).render()
errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def norm(t):return re.sub(r'\s+','',unicodedata.normalize('NFKC',t or ''))
def gettext(el):return el.get_text(' ',strip=True)

old_units=OLD.select('section[data-editorial-unit]');new_units=s.select('section[data-editorial-unit]')
check([x['id'] for x in old_units]==[x['id'] for x in new_units],'Ordine/numero unità modificati')
for a,b in zip(old_units,new_units):
 for sel in ['.opening','.blk','.summary']:
  before=[str(x) for x in a.select(sel)];after=[str(x) for x in b.select(sel)]
  check(before==after,f'Elementi {sel} modificati nell’unità {a["id"]}')
check(str(OLD.select_one('.cover-image'))==str(s.select_one('.cover-image')),'Immagine di copertina modificata')
check([str(x) for x in OLD.select('.map-node')]==[str(x) for x in s.select('.map-node')],'Schede della mappa modificate')
check(len(s.select('.map-node'))==6,'Numero schede finali diverso da sei')
check([gettext(x) for x in OLD.select('.index-label')]==[gettext(x) for x in s.select('.index-label')],'Titoli indice modificati')
old_tables=OLD.select('.map-details');new_tables=s.select('.map-details')
check(len(old_tables)==len(new_tables)==2,'Numero tabelle variato')
for a,b in zip(old_tables,new_tables):
 # La serializzazione può cambiare soltanto gli a capo fra tag HTML.
 check(re.sub(r'>\s+<','><',str(a))==re.sub(r'>\s+<','><',str(b)),'Contenuto o struttura tabella alterati')
old_t=OLD.select_one('.timeline');new_t=s.select_one('.timeline')
check(len(OLD.select('.timeline'))==len(s.select('.timeline'))==1,'Linea del tempo assente o duplicata')
check([str(x) for x in old_t.select('.year')]==[str(x) for x in new_t.select('.year')],'Date/eventi o ordine della cronologia cambiati')
check(len(new_t.select('.year'))==7,'Numero eventi cronologici non corretto')
check(not s.select('#mapa .timeline, #mapa .map-details'),'In fondo restano schemi/linea del tempo')
checks_order={}
for sid in ['sec3','sec5']:
 unit=s.select_one('#'+sid);children=[x for x in unit.find_all(recursive=False) if getattr(x,'name',None)]
 def order_of(c):return children.index(c)
 paragraphs=unit.select(':scope > .blk');summary=unit.select_one(':scope > .summary')
 lastpara=order_of(paragraphs[-1]);summ=order_of(summary)
 if sid=='sec3':
  target=unit.select_one('table.map-details');order=order_of(target)
  ok=lastpara<order<summ and target.get('aria-label')=='DOS IDEAS DE ESPAÑA EN LUCHA'
  checks_order[sid]={'ordine':['ultimo testo','schema delle idee','EN RESUMEN'],'passed':ok}
 else:
  timeline=unit.select_one('.timeline');target=unit.select_one('table.map-details');to=order_of(timeline);order=order_of(target)
  ok=lastpara<to<order<summ and target.get('aria-label')=='LOS PROTAGONISTAS DEL SIGLO'
  checks_order[sid]={'ordine':['ultimo testo','linea del tempo','schema dei protagonisti','EN RESUMEN'],'passed':ok}
 check(ok,'Posizione dello schema/timeline scorretta nella '+sid)

# Misura tipografia reale, grafica dei riquadri e destinazioni effettive.
anchors={};mapnodes={};tables={};timeline_location=[];summ_weight=set();index_cells=[]
def rect(b):
 return fitz.Rect(b.border_box_x()*.75,b.border_box_y()*.75,(b.border_box_x()+b.border_width())*.75,(b.border_box_y()+b.border_height())*.75)
for page_no,page in enumerate(d.pages,1):
 for name in page.anchors:anchors.setdefault(name,page_no)
 parent={}
 for b in page._page_box.descendants():
  for ch in getattr(b,'children',[]):parent[ch]=b
 for b in page._page_box.descendants():
  e=getattr(b,'element',None)
  if e is None:continue
  kind=type(b).__name__;id=e.get('id','');cls=e.get('class','').split()
  if kind=='BlockBox' and id.startswith('map-node-') and id not in mapnodes:
   x,y,w,h=b.border_box_x(),b.border_box_y(),b.border_width(),b.border_height()
   imgs=[z for z in b.descendants() if 'ReplacedBox' in type(z).__name__];lines=[z for z in b.descendants() if type(z).__name__=='LineBox']
   outside=[str(z) for z in lines if z.position_y+z.height>y+h-1 or z.position_x<x-1 or z.position_x+z.width>x+w+1]
   mapnodes[id]={'page':page_no,'box_mm':[round(w*25.4/96,3),round(h*25.4/96,3)],'images_mm':[[round(z.width*25.4/96,3),round(z.height*25.4/96,3)] for z in imgs],'overflow':len(outside)}
  if kind=='TableBox' and 'map-details' in cls:
   label=e.get('aria-label');tables.setdefault(label,[]).append({'page':page_no,'rect':list(rect(b))})
  if kind=='BlockBox' and 'timeline' in cls:timeline_location.append({'page':page_no,'rect':list(rect(b))})
  if kind=='TableCellBox' and 'index-pg' in cls:index_cells.append((page_no,rect(b)))
  if kind=='TextBox' and b.text.strip():
   cur=b
   while cur:
    ce=getattr(cur,'element',None)
    if ce is not None and 'summary' in ce.get('class','').split():summ_weight.add(str(b.style['font_weight']));break
    cur=parent.get(cur)
for k,v in mapnodes.items():
 check(v['box_mm']==[78.0,78.0] and v['images_mm']==[[52.0,29.373]] and v['overflow']==0,'Scheda fuori bordo/alterata: '+k)
check(len(mapnodes)==6,'Non tutti i nodi sono misurabili')
check(summ_weight=={'400'},'Specchietti EN RESUMEN con grassetto')
check(len(timeline_location)==1,'Linea del tempo spezzata o non misurabile')
for key,val in tables.items():check(len(val)==1,'Tabella spezzata: '+key)
check(set(tables)=={'DOS IDEAS DE ESPAÑA EN LUCHA','LOS PROTAGONISTAS DEL SIGLO'},'Schemi non misurabili')

ids=['sec1','sec2','sec3','sec4','sec5','sec6','mapa'];pages=[anchors.get(i) for i in ids]
check(len(p)==len(d.pages),'PDF e HTML hanno pagine differenti')
check(len(index_cells)==len(ids) and all(pages),'Indice non misurabile')
index=[]
for (pno,r),id,target in zip(index_cells,ids,pages):
 actual=p[pno-1].get_text('text',clip=r).strip();ok=actual==str(target)
 check(ok,f'Indice di {id} segna {actual!r}, destinazione {target}')
 index.append({'id':id,'printed':actual,'target':target,'passed':ok})
links=[x for x in p[0].get_links() if x.get('from') is not None and x['from'].width>0 and x['from'].height>0 and x.get('page',-1)>=0]
check(sorted({x['page']+1 for x in links})==sorted(pages),'Collegamenti del PDF non corrispondono alle voci')
for n,page in enumerate(p,1):
 words=page.get_text('words');foot=[w[4] for w in words if w[1]>page.rect.height-45 and abs((w[0]+w[2])/2-page.rect.width/2)<25]
 check((not foot) if n==1 else str(n) in foot,f'Numerazione non corretta pagina {n}')
report={'passed':not errors,'previous_delivered_pdf_sha256':'e45d9dd11d07247c8ba7325dd8d70c039ab37ebf275b371aa39f06e4e03bd57d','revised_pdf_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'pages':len(p),'body_blocks':len(s.select('.blk')),'en_resumen':len(s.select('.summary')),'all_body_and_summaries_identical_in_html':not any('Elementi' in e for e in errors),
 'moved_tables_unchanged':not any('tabell' in e.lower() for e in errors),'order':checks_order,'table_geometry':tables,'timeline_geometry':timeline_location,'six_map_cards':mapnodes,'index':index,'summary_weight':sorted(summ_weight),'active_index_links':len(links),'errors':errors,
 'limits':'Il confronto di regressione copre le strutture HTML, geometria, indice, numeri e pesi effettivi; non sostituisce il controllo visivo o la validazione indipendente PDF/UA.'}
(R/'qa/QA_REVISIONE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:report[k] for k in ['passed','revised_pdf_sha256','pages','body_blocks','en_resumen','order','table_geometry','timeline_geometry','summary_weight','active_index_links','errors']},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)

