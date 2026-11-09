#!/usr/bin/env python3
"""Rimpagina il quaderno allegato nel modello Rosalía/Bécquer, senza riscrivere il corpo."""
from pathlib import Path
from html import escape
import json,sys
from weasyprint import HTML

R=Path(__file__).resolve().parent.parent
C=json.loads((R/'sorgenti'/'CONTENUTI_ORIGINALI.json').read_text(encoding='utf8'))
# Eventuali divisioni ai confini delle frasi, determinate dopo un controllo delle righe.
SPLIT={}
# La mappa originale contiene descrizioni più lunghe: restano integralmente nelle tabelle.
# Nei riquadri illustrati si ripetono soltanto parole chiave ricavate da quelle descrizioni.
MAP_KEYWORDS={
 'TRADICIÓN':['CARLISTAS','TRONO FUERTE','RELIGIÓN'],
 'LIBERALES':['ISABELINOS','CONSTITUCIÓN','NACIÓN · DERECHOS'],
 'EL PÉNDULO':['MONARQUÍA','REPÚBLICA','RESTAURACIÓN'],
 'FERNANDO VII':['1814','CONSTITUCIÓN','ABSOLUTISMO'],
 'ISABEL II':['1833','GUERRA CARLISTA','DERROCADA · 1868'],
 'ALFONSO XII':['1875','RESTAURACIÓN','REGENCIA · 1898'],
}

CSS='''
@font-face{font-family:OpenDyslexic;src:url(media/OpenDyslexic-Regular.otf);font-weight:400}
@font-face{font-family:OpenDyslexic;src:url(media/OpenDyslexic-Bold.otf);font-weight:700}
@page{size:A4;margin:17mm 18mm 19mm;@bottom-center{content:counter(page);font:700 11pt OpenDyslexic;color:#233348}}
@page:first{@bottom-center{content:none}}
*{box-sizing:border-box}
body{font-family:OpenDyslexic,sans-serif;font-size:14pt;line-height:1.85;color:#151515;margin:0}
h1,h2,h3{font-weight:700;line-height:1.45;text-align:center}
h1{background:#243c5a;color:#fff;font-size:20pt;margin:0 0 3mm;padding:3mm;border-radius:3mm}
h2{font-size:15pt} h3{font-size:13pt}
p{margin:0}strong{font-weight:700;color:#101010}
.cover{break-after:page;page-break-after:always}
.cover-image,.illustration{width:112mm;height:63.25mm;object-fit:contain;display:block;margin:3mm auto 4mm;break-inside:avoid}
.cover-image{margin:3mm auto 3mm}
.index-heading{font-size:15pt;background:#243c5a;color:white;border-radius:3mm;padding:2mm 3mm;margin:2mm 0}
.index-box{background:#fffaf0;border:1.1pt solid #e6d5ae;border-radius:3mm;padding:3mm 4mm;line-height:1.35}
.index-table{width:100%;border-collapse:collapse;table-layout:fixed}
.index-row td{height:12mm;vertical-align:middle;padding:1mm 0;font-size:12pt;font-weight:700;line-height:1.35}
.index-icon{width:11mm}.index-label{padding-left:1mm!important}.index-pg{width:11mm;text-align:right}
.index-label a{color:#111;text-decoration:none}.index-pg a{color:var(--color);text-decoration:none}
.index-pg a::after{content:target-counter(attr(href),page)}
.index-badge{display:block;background:var(--color);color:white;border-radius:50%;width:7.6mm;height:7.6mm;line-height:7.6mm;text-align:center;font-size:11pt}
.section{break-before:page;page-break-before:always}
.opening{break-inside:avoid;page-break-inside:avoid}
.section h2{background:var(--color);color:white;margin:0 0 3mm;padding:2.5mm 4mm;border-radius:3mm;break-after:avoid}
.subheading{color:var(--color);margin:5mm 0 3mm;break-after:avoid}
.blk{background:#fffaf0;border:1.1pt solid #e6d5ae;border-radius:3mm;padding:2.1mm 3.7mm;margin:0 0 2.5mm;break-inside:avoid;page-break-inside:avoid}
.summary{margin:5mm 0;break-inside:avoid;page-break-inside:avoid}
.summary-title{font-size:14pt;line-height:1.85;text-align:center;background:var(--color);color:white;border-radius:2mm 2mm 0 0;padding:1.5mm;font-weight:400;break-after:avoid}
.summary-table{width:100%;border-collapse:collapse;background:#fffaf0;font-size:14pt;line-height:1.85;font-weight:400;table-layout:fixed}
.summary-table th,.summary-table td{font-family:OpenDyslexic,sans-serif;font-weight:400;text-align:left;vertical-align:top;border:1px solid #ddd0c0;padding:2mm 2.5mm;overflow-wrap:normal}
.summary-table th{width:36%;color:var(--color)}
.summary-table tr{break-inside:avoid;page-break-inside:avoid}
.timeline{margin:3mm 0 5mm;padding:1mm 3mm 2mm 4mm;background:#fffaf0;border:1pt solid #e6d5ae;border-radius:3mm;break-inside:avoid;page-break-inside:avoid}
.year{position:relative;display:flex;align-items:center;gap:4mm;padding:2mm 0;break-inside:avoid;line-height:1.55}
.year:not(:last-child)::before{content:'';position:absolute;left:10.3mm;top:7mm;height:100%;width:1.2mm;background:var(--color)}
.date-badge{position:relative;background:var(--color);color:white;border-radius:7mm;font-size:12pt;font-weight:700;line-height:1.5;padding:1.5mm 3mm;min-width:21mm;text-align:center}
.event{flex:1;color:#161616}
.map-section h2{background:none;color:#243c5a;text-align:center;padding:0;margin:0 0 4mm;font-size:16pt;break-after:avoid}
.map-main-subtitle{color:#243c5a;margin:0 0 3mm;break-after:avoid}
.map-group-title{color:#243c5a;margin:4mm 0 3mm;text-align:center;break-after:avoid}
.map-details{width:100%;border-collapse:collapse;table-layout:fixed;background:#fffaf0;line-height:1.85;margin:0 0 5mm}
.map-details th,.map-details td{border:1px solid #ddd0c0;padding:2mm 2.5mm;text-align:left;vertical-align:top;font:400 14pt/1.85 OpenDyslexic,sans-serif}
.map-details th{width:36%;color:#243c5a}.map-details tr{break-inside:avoid;page-break-inside:avoid}
.map-row{display:flex;justify-content:center;gap:6mm;margin:0 0 6mm;break-inside:avoid;page-break-inside:avoid}
.map-node{width:78mm;height:78mm;flex:none;border:1pt solid var(--node-color);border-radius:3mm;background:#fffaf0;text-align:center;overflow:visible;padding:3mm 3mm 2mm;break-inside:avoid;line-height:1.85}
.map-node img{width:52mm;height:29.373mm;object-fit:contain;display:block;margin:0 auto 1mm}
.node-title{font-weight:700;color:var(--node-color);font-size:14pt;line-height:1.85}
.node-word{font-weight:400;color:#171717;font-size:14pt;line-height:1.85}
.c1{--color:#b23c47}.c2{--color:#1a5fb4}.c3{--color:#257041}.c4{--color:#9b4f12}.c5{--color:#744394}.c6{--color:#14696e}.cm{--color:#243c5a}
'''

def div_box(sid,n,paragraph):
    id=f'{sid}-p{n:02d}'
    return f'<div class="blk" data-semantic-box="" id="{id}" data-source-page="{paragraph["source_page"]}"><p>{paragraph["html"]}</p></div>'

def render_timeline(m):
    # La cronologia completa conclude la trattazione del secolo (unità 5).
    out=['<h3 class="map-group-title">EL SIGLO XIX EN UNA LÍNEA</h3>',
         '<div class="timeline" role="list" aria-label="Cronología de la historia española del siglo XIX" style="--color:#243c5a">']
    for year,event in m['timeline']:
        out.append(f'<div class="year" role="listitem"><span class="date-badge">{escape(year)}</span><span class="event">{escape(event)}</span></div>')
    out.append('</div>')
    return ''.join(out)

def render_details(group):
    # Un intero schema resta leggibile e intatto come nella versione approvata.
    out=['<h3 class="map-group-title">'+escape(group['title'])+'</h3>',
         '<table class="map-details" aria-label="'+escape(group['title'],quote=True)+'"><tbody>']
    for node in group['nodes']:
        out.append('<tr><th scope="row">'+escape(node['title'])+'</th><td>'+escape(node['words'])+'</td></tr>')
    out.append('</tbody></table>')
    return ''.join(out)

def render():
    parts=['<!DOCTYPE html>','<html lang="es"><head><meta charset="utf-8"/>',
      '<meta name="author" content="Laboratorio didattico inclusivo"/>',
      '<meta name="description" content="Cuaderno accesible sobre el marco histórico del Romanticismo en España."/>',
      '<title>'+escape(C['title'])+'</title><style>'+CSS+'</style></head><body>']
    parts.append('<section class="cover" id="indice"><h1>'+escape(C['title'])+'</h1>')
    parts.append('<img class="cover-image" src="media/originale_p06_xref92.png" alt="Un monarca a caballo ante un paisaje de barcos y edificios evoca la España del siglo XIX."/>')
    parts.append('<h2 class="index-heading">ÍNDICE</h2><nav class="index-box" aria-label="Índice del cuaderno"><table class="index-table" role="presentation"><tbody>')
    for s in C['sections']:
        label=escape(s['title']);href='#'+s['id']
        parts.append(f'<tr class="index-row c{s["number"]}"><td class="index-icon"><span class="index-badge">{s["number"]}</span></td><td class="index-label"><a href="{href}">{label}</a></td><td class="index-pg"><a href="{href}" aria-label="Página de {label}"></a></td></tr>')
    label=escape(C['map']['original_title']);parts.append(f'<tr class="index-row cm"><td class="index-icon"><span class="index-badge">M</span></td><td class="index-label"><a href="#mapa">{label}</a></td><td class="index-pg"><a href="#mapa" aria-label="Página de {label}"></a></td></tr></tbody></table></nav></section>')
    for s in C['sections']:
        parts.append(f'<section class="section c{s["number"]}" id="{s["id"]}" data-editorial-unit="{s["id"]}">')
        parts.append(f'<div class="opening"><h2>{s["number"]} · {escape(s["title"])}</h2><img class="illustration" src="media/{s["image"]}" alt="{escape(s["alt"],quote=True)}"/></div>')
        for i,p in enumerate(s['paragraphs'],1):parts.append(div_box(s['id'],i,p))
        # Gli schemi nelle fotografie sono spostati, non duplicati o riscritti.
        # L'opposizione carlisti/liberali appartiene all'unità 3.
        if s['id']=='sec3':
            parts.append(render_details(C['map']['groups'][0]))
        # La storia dell'Ottocento si conclude nell'unità 5: qui i due
        # supporti riassuntivi sull'intero secolo precedono EN RESUMEN.
        if s['id']=='sec5':
            parts.append(render_timeline(C['map']))
            parts.append(render_details(C['map']['groups'][1]))
        if s['summary_rows']:
            parts.append(f'<div class="summary" data-support-profile="summary" id="{s["id"]}-resumen"><div class="summary-title">EN RESUMEN</div><table class="summary-table"><tbody>')
            for j,row in enumerate(s['summary_rows'],1):
                parts.append(f'<tr id="{s["id"]}-row{j}"><th scope="row">{escape(row["label"].upper())}</th><td>{escape(row["value"])}</td></tr>')
            parts.append('</tbody></table></div>')
        parts.append('</section>')
    m=C['map'];parts.append('<section class="section map-section cm" data-support-profile="map" id="mapa"><h2>MAPA CONCEPTUAL FINAL</h2>')
    parts.append('<h3 class="map-main-subtitle">'+escape(m['original_title'])+'</h3><h3 class="map-main-subtitle">'+escape(m['subtitle'])+'</h3>')
    colors=['#b23c47','#1a5fb4','#9b4f12','#744394','#744394','#744394'];count=0
    for g in m['groups']:
        parts.append('<h3 class="map-group-title">'+escape(g['title'])+'</h3>')
        for r in range(0,len(g['nodes']),2):
            parts.append('<div class="map-row">')
            for node in g['nodes'][r:r+2]:
                count+=1
                keys=''.join('<div class="node-word">'+escape(k)+'</div>' for k in MAP_KEYWORDS[node['title']])
                parts.append(f'<div class="map-node" data-map-node="" id="map-node-{count}" style="--node-color:{colors[count-1]}"><img src="media/{node["image"]}" alt="{escape(node["alt"],quote=True)}"/><div class="node-title">{escape(node["title"])}</div>{keys}</div>')
            parts.append('</div>')
    parts.append('</section></body></html>')
    path=R/'MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.html'
    path.write_text('\n'.join(parts)+'\n',encoding='utf8')
    return path

if __name__=='__main__':
    src=render();dest=R/'MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.pdf'
    HTML(filename=str(src),base_url=str(R)).write_pdf(str(dest),pdf_variant='pdf/ua-1')
    print(json.dumps({'html':str(src),'draft_pdf':str(dest),'bytes':dest.stat().st_size},ensure_ascii=False,indent=2))

