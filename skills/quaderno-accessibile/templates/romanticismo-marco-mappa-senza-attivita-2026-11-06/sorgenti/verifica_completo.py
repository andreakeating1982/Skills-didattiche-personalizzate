#!/usr/bin/env python3
"""Regressione editoriale, geometria e collegamenti effettivi; non certifica PDF/UA."""
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
import fitz, json, re, copy, hashlib
R=Path(__file__).resolve().parent.parent
H=R/'MARCO_HISTORICO_ROMANTICISMO_MAPPA_CORRETTA.html'; P=R/'MARCO_HISTORICO_ROMANTICISMO_MAPPA_CORRETTA.pdf'
OLD=BeautifulSoup((R/'qa/BASELINE_COMPLETA_PRECEDENTE.html').read_text(encoding='utf-8'),'html.parser')
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
for sid in ['sec1','sec2','sec3','sec4','sec5','sec6','verifica','referencias']:
 a=OLD.select_one('#'+sid);b=NEW.select_one('#'+sid)
 check(clipstr(a)==clipstr(b),'Sezione alterata: '+sid)
check(clipstr(OLD.select_one('#indice'))==clipstr(NEW.select_one('#indice')),'Indice HTML cambiato')
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
check(len(NEW.select('#mapa .map-node'))==11,'Numero box mappa alterato')
chapter_nodes=[e['data-chapter'] for e in NEW.select('#mapa [data-chapter]')]
check(chapter_nodes==['sec1','sec2','sec3','sec4','sec5'],'Manca un box dedicato a una sezione storica')
maptext=NEW.select_one('#mapa').get_text(' ',strip=True).upper()
for forbidden in ['ACTIVIDAD','AUDIO','LÍNEA DEL TIEMPO 3D','FECHAS Y HECHOS']:
 check(forbidden not in maptext,'Riferimento alle attività nella mappa: '+forbidden)
check(not NEW.select('#mapa [data-chapter="sec6"]'),'Riquadro dell’attività ancora presente')
check('ACTIVIDAD' in NEW.select_one('#sec6').get_text(' ',strip=True).upper(),'Attività originale erroneamente eliminata dal corpo')
def signature(node):
 return (node.select_one('.node-title').get_text(' ',strip=True),tuple(x.get_text(' ',strip=True) for x in node.select('.node-word')),node.img.get('src'),node.img.get('alt'),node.get('style'))
oldnodes={signature(n)[0]:signature(n) for n in OLD.select('#mapa .map-node')}
newnodes={signature(n)[0]:signature(n) for n in NEW.select('#mapa .map-node')}
check(set(oldnodes)-set(newnodes)=={'ACTIVIDAD 3D'},'Rimossi nodi non autorizzati o attività rimasta')
check(all(oldnodes[n]==s for n,s in newnodes.items()),'Parole o immagini di un altro nodo modificate')
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
check(len(mapboxes)==11,'Non sono misurabili tutti i nodi')
check([sum(1 for b in mapboxes.values() if b['page']==p) for p in (17,18,19)]==[4,4,3],'Distribuzione mappa inattesa')
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
# Righe dell'indice: associare ogni etichetta al numero sulla stessa riga PDF.
page1=pdf[0].get_text('dict')
lines=[]
for block in page1['blocks']:
 for line in block.get('lines',[]):
  text=''.join(span['text'] for span in line['spans']).strip()
  if text: lines.append((line['bbox'],text))
for row,idx in zip(NEW.select('.index-row'),index):
 label=row.select_one('.index-label a').get_text(' ',strip=True)
 matched=[b for b,t in lines if t==label]
 if not matched:
  check(False,'Etichetta indice non trovata nel PDF: '+label);continue
 linebox=matched[0]; y=(linebox[1]+linebox[3])/2
 nums=[t for b,t in lines if abs((b[1]+b[3])/2-y)<2 and b[0]>linebox[2] and t.isdigit()]
 check(str(idx['target_page']) in nums,'Numero errato sulla riga: '+label+' / '+str(nums))
result={'passed':not errors,'pdf_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'pages':len(pdf),'sections_original_elements_preserved':not any(x.startswith('Sezione alterata') for x in errors),'quiz_questions':10,'options_per_question':4,'map_nodes':len(mapboxes),'chapter_nodes':chapter_nodes,'map_geometry':mapboxes,'notes':checks,'reference_count':len(DATA['references']),'index':index,'summary_weights':sorted(summary_weights),'errors':errors,'limits':'Controlli geometrici e di regressione, non sostituiscono revisione delle fonti, correttezza dei quesiti, visione PDF o validazione PDF/UA.'}
(R/'qa/QA_MAPPA_CORRETTA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:result[k] for k in ['passed','pdf_sha256','pages','sections_original_elements_preserved','quiz_questions','map_nodes','chapter_nodes','notes','index','summary_weights','errors']},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)

