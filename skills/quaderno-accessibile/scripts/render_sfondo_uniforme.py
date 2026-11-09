#!/usr/bin/env python3
"""Render PDF con box a tinta unita: nessun foro even-odd nei bordi a fondo opaco.
Non cambiare CSS, dimensioni, testo, immagini, tag o spaziatura. La sola correzione
è il disegno delle superfici: forma esterna del colore bordo e forma interna del
colore di sfondo, chiuse esplicitamente e riempite separatamente.
"""
from pathlib import Path
import argparse,json
from collections import Counter
from weasyprint import HTML
from weasyprint.draw import border
from weasyprint.draw.color import get_color

def render(source,output):
 source=Path(source).resolve();output=Path(output).resolve()
 if output.exists():raise FileExistsError('Destinazione esistente: usare un nome nuovo.')
 previous=border.draw_rounded_border;counts=Counter()
 def solid_surfaces(stream,box,style,color):
  bg=get_color(box.style,'background_color')
  has_image=any(k!='none' for k,v in box.style['background_image'])
  if style!='solid' or getattr(bg,'alpha',0)!=1 or has_image:
   return previous(stream,box,style,color)
  # Una sola superficie chiusa per ciascun riempimento, senza fori o trasparenze.
  stream.set_color(color)
  border.rounded_box(stream,box.rounded_border_box());stream.close();stream.fill()
  stream.set_color(bg)
  border.rounded_box(stream,box.rounded_padding_box());stream.close();stream.fill()
  e=getattr(box,'element',None);counts[e.get('class','') if e is not None else 'anonymous']+=1
 border.draw_rounded_border=solid_surfaces
 try:HTML(filename=str(source)).write_pdf(str(output),pdf_variant='pdf/ua-1')
 finally:border.draw_rounded_border=previous
 return {'source':source.name,'output':output.name,'corrected_opaque_borders':sum(counts.values()),'by_class':dict(counts),'method':'opaque outer and inner closed shapes with nonzero fill; no even-odd compound border'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',help='HTML sorgente con font/immagini locali');p.add_argument('output',help='PDF di destinazione NUOVO');a=p.parse_args();print(json.dumps(render(a.source,a.output),ensure_ascii=False,indent=2))

