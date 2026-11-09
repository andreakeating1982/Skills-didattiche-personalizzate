#!/usr/bin/env python3
"""Restyling conservativo del quaderno di letteratura spagnola allegato.
Il testo delle unità e le attività sono estratti dall'originale e non riscritti.
La mappa esistente viene riorganizzata in parole chiave, secondo il modello.
"""
from pathlib import Path
from html import escape
from bs4 import BeautifulSoup
import re,json,ast
R=Path(__file__).resolve().parent
C=json.loads((R/'dati_editoriali.json').read_text(encoding='utf8'))
B=json.loads((R/'contenuti_estratti.json').read_text(encoding='utf8'))
Q=json.loads((R/'quiz_referencias.json').read_text(encoding='utf8'))
base=(R/'stili_base.py').read_text(encoding='utf8')
css=ast.literal_eval(re.search(r"CSS=(\'\'\'.*?\'\'\')",base,re.S).group(1))
css+='''
.ref-inline{margin-top:4mm;font-size:14pt}
.source-label{font-weight:700}
.summary-table th{text-transform:uppercase}
.map-group-page{break-before:page;page-break-before:always}
.map-group-title{font-size:14pt;line-height:1.45}
.map-node{padding:2mm 3mm 1mm}
.map-node img{margin:0 auto 1mm}
.map-node .node-title,.map-node .node-word{font-size:14pt;line-height:1.85}
'''
# Breaks occur only at complete sentences / natural boundaries, preserving the text.
splits={
 'sec3':[(3,'periodo.' )],
 'sec4':[(2,'inalcanzable:')],
}
def original_para(key):
 arr=B[key]
 parts=[]
 for i,s in enumerate(arr,1):
  point=next((tok for j,tok in splits.get(key,[]) if j==i),None)
  if point:
   assert s.count(point)==1
   a,b=s.split(point,1)
   parts.extend([a+point,b.strip()])
  else:parts.append(s)
 return parts
P=['<!DOCTYPE html>','<html lang="es"><head><meta charset="utf-8"/>',
 '<meta name="author" content="Laboratorio didattico inclusivo"/>',
 '<meta name="description" content="Cuaderno de literatura española: la literatura del Romanticismo en España."/>',
 '<title>'+escape(C['title'])+'</title><style>'+css+'</style></head><body>']
P.append('<section class="cover" id="indice"><h1>'+escape(C['title'])+'</h1>')
P.append('<img class="cover-image" src="media/original_p01_xref77.png" alt="Un diorama reúne escenas y autores del Romanticismo español."/>')
P.append('<h2 class="index-heading">ÍNDICE</h2><nav class="index-box" aria-label="Índice del cuaderno"><table class="index-table" role="presentation"><tbody>')
for i,s in enumerate(C['sections'],1):
 label=escape(s['title']); url='#'+s['id']
 P.append(f'<tr class="index-row c{i}"><td class="index-icon"><span class="index-badge">{i}</span></td><td class="index-label"><a href="{url}">{label}</a></td><td class="index-pg"><a href="{url}" aria-label="Página de {label}"></a></td></tr>')
P.append('<tr class="index-row cm"><td class="index-icon"><span class="index-badge">V</span></td><td class="index-label"><a href="#verifica">VERIFICACIÓN DE COMPRENSIÓN</a></td><td class="index-pg"><a href="#verifica" aria-label="Página de la verificación"></a></td></tr>')
P.append('<tr class="index-row cm"><td class="index-icon"><span class="index-badge">M</span></td><td class="index-label"><a href="#mapa">MAPA CONCEPTUAL FINAL</a></td><td class="index-pg"><a href="#mapa" aria-label="Página del mapa conceptual final"></a></td></tr>')
P.append('<tr class="index-row cm"><td class="index-icon"><span class="index-badge">R</span></td><td class="index-label"><a href="#referencias">REFERENCIAS BIBLIOGRÁFICAS</a></td><td class="index-pg"><a href="#referencias" aria-label="Página de las referencias"></a></td></tr>')
P.append('</tbody></table></nav></section>')
for i,s in enumerate(C['sections'],1):
 P.append(f'<section class="section c{i}" id="{s["id"]}" data-editorial-unit="{s["id"]}">')
 P.append(f'<div class="opening"><h2>{i} · {escape(s["title"])}</h2><img class="illustration" src="media/{escape(s["image"])}" alt="{escape(s["alt"],quote=True)}"/></div>')
 for j,txt in enumerate(original_para(s['id']),1):
  note_map={('sec1',2):(1,2),('sec1',5):(4,),('sec2',1):(1,),('sec2',3):(1,2),('sec3',3):(1,),('sec3',5):(1,3),('sec4',1):(2,),('sec4',6):(1,2)}
  notes=''.join(f'<sup class="note-ref"><a href="#rif-{n}" aria-label="Referencia bibliográfica {n}">[{n}]</a></sup>' for n in note_map.get((s['id'],j),()))
  P.append(f'<div class="blk" data-semantic-box="" id="{s["id"]}-p{j:02d}"><p>{txt}{notes}</p></div>')
 if s['summary']:
  P.append(f'<div class="summary" data-support-profile="summary" id="{s["id"]}-resumen"><div class="summary-title">EN RESUMEN</div><table class="summary-table"><tbody>')
  for label,text in s['summary']:
   P.append('<tr><th scope="row">'+escape(label.upper())+'</th><td>'+escape(text)+'</td></tr>')
  P.append('</tbody></table></div>')
 P.append('</section>')
# Verificación: diez preguntas, cuatro opciones y clave interna no publicada.
P.append('<section class="section quiz-section cm" id="verifica"><h2>VERIFICACIÓN DE COMPRENSIÓN</h2><p class="quiz-intro blk" data-semantic-box="">Elige una sola respuesta para cada pregunta.</p>')
for n,q in enumerate(Q['quiz'],1):
 P.append(f'<div class="quiz-card" data-question="{n}"><div class="quiz-question">{n}. {escape(q["q"])}</div><table class="quiz-options" role="presentation"><tbody>')
 for i in (0,2):
  P.append('<tr>'+''.join('<td>'+escape(x)+'</td>' for x in q['options'][i:i+2])+'</tr>')
 P.append('</tbody></table></div>')
P.append('</section>')
P.append('<section class="section map-section cm" data-support-profile="map" id="mapa"><h2>MAPA CONCEPTUAL FINAL</h2>')
P.append('<h3 class="map-main-subtitle">'+escape(C['title'])+'</h3>')
for gi,g in enumerate(C['maps']):
 P.append('<div class="map-group'+(' map-group-page' if gi==2 else '')+'"><h3 class="map-group-title">'+escape(g['group'])+'</h3>')
 for row in (g['nodes'][0:2],):
  P.append('<div class="map-row">')
  for node in row:
   P.append('<div class="map-node" style="--node-color:'+g['color']+'"><img src="media/'+escape(node['image'])+'" alt="'+escape(node['alt'],quote=True)+'"/><div class="node-title">'+escape(node['title'])+'</div>')
   for line in node['lines']: P.append('<div class="node-word">'+escape(line)+'</div>')
   P.append('</div>')
  P.append('</div>')
 P.append('</div>')
P.append('</section>')
P.append('<section class="section refs-section cm" id="referencias"><h2>REFERENCIAS BIBLIOGRÁFICAS</h2>')
for ref in Q['references']:
 n=ref['id']
 if n==1:
  author,title=ref['text'].split(' Horizontes.',1)
  P.append(f'<div class="ref-entry blk" data-bibliography-entry="" data-bibliography-box="" id="rif-1"><p>[1] {escape(author)}</p></div>')
  book,place=title.split(', Milano:',1)
  P.append(f'<div class="ref-entry blk" data-bibliography-box=""><p><em>Horizontes.{escape(book)}</em>, Milano:{escape(place)}</p></div>')
 else:
  P.append(f'<div class="ref-entry blk" data-bibliography-entry="" data-bibliography-box="" id="rif-{n}"><p>[{n}] {escape(ref["text"])} <a href="{escape(ref["url"],quote=True)}">Consultar el recurso</a>.</p></div>')
P.append('</section></body></html>')
html=R/'LITERATURA_ROMANTICISMO_SEMPLIFICATA.html'
html.write_text('\n'.join(P),encoding='utf8')
print('Generated',html)

