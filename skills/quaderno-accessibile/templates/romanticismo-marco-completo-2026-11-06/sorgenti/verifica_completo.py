#!/usr/bin/env python3
"""Regressione editoriale, geometria e collegamenti effettivi; non certifica PDF/UA."""
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
import fitz, json, re, copy, hashlib
R=Path(__file__).resolve().parent.parent
H=R/'MARCO_HISTORICO_ROMANTICISMO_COMPLETO.html'; P=R/'MARCO_HISTORICO_ROMANTICISMO_COMPLETO.pdf'
OLD=BeautifulSoup((R/'qa/BASELINE.html').read_text(encoding='utf-8'),'html.parser')
NEW=BeautifulSoup(H.read_text(encoding='utf-8'),'html.parser')
DATA=json.loads((R/'sorgenti/NUEVOS_CONTENIDOS.json').read_text(encoding='utf8'))
errors=[]
def check(ok,msg):
 if not ok: errors.append(msg)
def clipstr(x): return re.sub(r'>\s+<','><',str(x))
def stripped(x):
 z=copy.copy(x)
 for s in z.select('sup.note-ref'):s.decompose()
 return clipstr(z)
for sid in ['sec1','sec2','sec3','sec4','sec5','sec6']:
 a=OLD.select_one('#'+sid);b=NEW.select_one('#'+sid)
 for selector in ['.opening','.blk','.summary','.timeline','.map-details']:
  check([stripped(x) for x in a.select(selector)]==[stripped(x) for x in b.select(selector)],'Elemento originale alterato: '+sid+' '+selector)
for sid in ['sec3','sec5']:
 el=NEW.select_one('#'+sid); children=el.find_all(recursive=False); summ=children.index(el.select_one(':scope > .summary'))
 paras=el.select(':scope > .blk');last=children.index(paras[-1])
 if sid=='sec3': order=last<children.index(el.select_one('.map-details'))<summ
 else: order=last<children.index(el.select_one('.timeline'))<children.index(el.select_one('.map-details'))<summ
 check(order,'Schemi non prima della sintesi: '+sid)
check('EL SIGLO XIX EN UNA LÍNEA · SÍNTESIS FINAL' not in NEW.get_text(' ',strip=True),'Scritta fotografata ancora presente')
check(len(NEW.select('#sec5 .timeline .year'))==7,'Linea del tempo alterata')
check(not NEW.select('#mapa .timeline, #mapa .map-details'),'Schemi duplicati alla fine')
check(len(NEW.select('#verifica .quiz-card'))==10,'Non ci sono esattamente 10 domande')
check(all(len(c.select('td'))==4 for c in NEW.select('#verifica .quiz-card')),'Alternative diverse da quattro')
check(len(DATA['quiz'])==10 and all(q['answer'] in 'ABCD' and len(q['options'])==4 for q in DATA['quiz']),'Chiave interna incompleta')
check(len(NEW.select('#mapa .map-node'))==12,'Numero box mappa alterato')
chapter_nodes=[e['data-chapter'] for e in NEW.select('#mapa [data-chapter]')]
check(chapter_nodes==['sec1','sec2','sec3','sec4','sec5','sec6'],'Manca un box dedicato a ciascuna unità')
all_titles=[e.get_text(' ',strip=True) for e in NEW.select('#mapa .node-title')]
for name in ['TRADICIÓN','LIBERALES','EL PÉNDULO','FERNANDO VII','ISABEL II','ALFONSO XII']:
 check(name in all_titles,'Manca un nodo: '+name)
check(len(NEW.select('#referencias .ref-entry'))==5,'Numero riferimenti inatteso')
for n in range(1,6):
 check(NEW.select_one('#rif-'+str(n)) is not None,'Manca riferimento '+str(n))
 check(NEW.select('sup.note-ref a[href="#rif-'+str(n)+'"]'),'Manca richiamo per la fonte '+str(n))
check(len(NEW.select('sup.note-ref a'))==13,'Numero di note inatteso')

# Misure effettive dei blocchi WeasyPrint, confrontate con annotazioni PDF.
doc=HTML(filename=str(H),base_url=str(R)).render();pdf=fitz.open(P)
check(len(doc.pages)==len(pdf),'HTML e PDF hanno paginazioni diverse')
anchors={}; anchor_coords={}; mapboxes={}; linkboxes=[]; summary_weights=set()
for pi,page in enumerate(doc.pages):
 pageno=pi+1
 for name,pt in page.anchors.items():
  anchors.setdefault(name,pageno);anchor_coords.setdefault(name,pt)
 root=page._page_box;parent={}
 for b in root.descendants():
  for child in getattr(b,'children',[]): parent[child]=b
 for b in root.descendants():
  e=getattr(b,'element',None)
  if e is None: continue
  kind=type(b).__name__;cls=e.get('class','').split(); ident=e.get('id','')
  if kind=='BlockBox' and 'map-node' in cls and ident not in mapboxes:
   x,y,w,h=b.border_box_x(),b.border_box_y(),b.border_width(),b.border_height()
   imgs=[v for v in b.descendants() if 'ReplacedBox' in type(v).__name__]
   lines=[v for v in b.descendants() if type(v).__name__=='LineBox']
   outside=[v for v in lines if v.position_y+v.height>y+h+0.25 or v.position_y<y-0.25 or v.position_x<x-0.25 or v.position_x+v.width>x+w+0.25]
   data={'page':pageno,'box_mm':[round(w*25.4/96,3),round(h*25.4/96,3)],'images_mm':[[round(v.width*25.4/96,3),round(v.height*25.4/96,3)] for v in imgs],'outside_lines':len(outside)}
   mapboxes[ident]=data
   check(data['box_mm']==[78,78] and data['images_mm']==[[52,29.373]] and not outside,'Nodo mappa irregolare o testo fuori dai bordi: '+ident+' '+str(data))
  if kind=='TextBox' and b.text.strip():
   cur=b
   while cur:
    el=getattr(cur,'element',None)
    if el is not None and 'summary' in el.get('class','').split(): summary_weights.add(str(b.style['font_weight']));break
    cur=parent.get(cur)
   if e.tag=='a' and e.get('href') and e.get('href').startswith('#rif-'):
    rr=fitz.Rect(b.position_x*.75,b.position_y*.75,(b.position_x+b.width)*.75,(b.position_y+b.height)*.75)
    linkboxes.append((pageno,e.get('href')[1:],rr,b.text))
check(len(mapboxes)==12,'Non sono misurabili tutti i nodi')
check(summary_weights=={'400'},'Gli specchietti contengono grassetto')
alllinks=[]
for i,p in enumerate(pdf):
 for l in p.get_links():
  if l.get('from') is not None:
   rr=l['from']; alllinks.append((i+1,l)); check(rr.width>0 and rr.height>0,'Link con area nulla')
checks=[]
for pageno,ref,rect,text in linkboxes:
 target=anchors.get(ref)
 matches=[l for pg,l in alllinks if pg==pageno and l.get('page',-1)==target-1 and l['from'].intersects(rect)]
 # La destinazione /XYZ del PDF è espressa dal basso; WeasyPrint misura dal margine alto.
 expected_y=pdf[target-1].rect.height-anchor_coords[ref][1]*.75 if target else None
 matches=[l for l in matches if l.get('to') is not None and abs(l['to'].y-expected_y)<1.0]
 ok=bool(matches) and target is not None
 checks.append({'page':pageno,'label':text,'reference':ref,'destination_page':target,'passed':ok})
 check(ok,'Richiamo bibliografico senza destinazione corretta o area: '+str(checks[-1]))
check(len(checks)==13,'Numero di note misurate errato: '+str(len(checks)))
for ref in DATA['references']:
 url=ref['url']; links=[l for pg,l in alllinks if l.get('uri')==url and pg==anchors['rif-'+str(ref['id'])]]
 check(bool(links),'Collegamento esterno mancante o errato: '+url)
index=[]
for row in NEW.select('.index-row'):
 a=row.select_one('.index-label a');name=a['href'][1:];dest=anchors.get(name)
 occurrences=[l for pg,l in alllinks if pg==1 and l.get('page',-1)==dest-1]
 check(dest is not None and len(occurrences)>=2,'Link indice mancante: '+name)
 index.append({'name':name,'target_page':dest,'link_count':len(occurrences)})
check(len(index)==9,'Numero voci indice non corretto')
# Il numero stampato si confronta con la destinazione reale leggendo la riga in pagina 1.
page1=pdf[0].get_text('text')
for idx in index:check(str(idx['target_page']) in page1,'Numero pagina indice mancante: '+idx['name'])
result={'passed':not errors,'pdf_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'pages':len(pdf),'sections_original_elements_preserved':not any(x.startswith('Elemento originale alterato') for x in errors),'quiz_questions':10,'options_per_question':4,'map_nodes':len(mapboxes),'chapter_nodes':chapter_nodes,'map_geometry':mapboxes,'notes':checks,'reference_count':len(DATA['references']),'index':index,'summary_weights':sorted(summary_weights),'errors':errors,'limits':'Controlli geometrici e di regressione, non sostituiscono revisione delle fonti, correttezza dei quesiti, visione PDF o validazione PDF/UA.'}
(R/'qa/QA_COMPLETO.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:result[k] for k in ['passed','pdf_sha256','pages','sections_original_elements_preserved','quiz_questions','map_nodes','chapter_nodes','notes','index','summary_weights','errors']},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)

