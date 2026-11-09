#!/usr/bin/env python3
from pathlib import Path
from weasyprint import HTML
import pymupdf as fitz, json, math
R=Path(__file__).resolve().parent.parent; H=R/'MARCO_HISTORICO_ROMANTICISMO_COMPLETO.html'; P=R/'MARCO_HISTORICO_ROMANTICISMO_COMPLETO.pdf'
doc=HTML(filename=str(H),base_url=str(R)).render();pdf=fitz.open(P)
anchors={k:(i+1,fitz.Point(v[0]*.75,v[1]*.75)) for i,p in enumerate(doc.pages) for k,v in p.anchors.items()}
for k in [f'rif-{i}' for i in range(1,6)]:
 print(k,anchors[k][0],round(anchors[k][1].x,1),round(anchors[k][1].y,1))
for pno,page in enumerate(pdf,1):
 for l in page.get_links():
  if l.get('page')==20 and pno!=1:
   print('LINK',pno,'rect',tuple(round(v,1) for v in l['from']),'to',tuple(round(v,1) for v in l['to']))

