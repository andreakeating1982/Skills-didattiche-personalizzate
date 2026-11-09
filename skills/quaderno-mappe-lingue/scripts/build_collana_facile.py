#!/usr/bin/env python3.11
"""Collana FACILE: nuove pagine editoriali, mappe originali VERBATIM.
Nessun sorgente preesistente viene modificato.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape as E
import json,re,hashlib,shutil,math,os
from weasyprint import HTML

ROOT=Path(os.environ.get('LF_WORKDIR','/home/user/facile_edizione')).expanduser().resolve()
INV=json.loads((ROOT/'inventory.json').read_text())
CFG={
 'en':dict(title='INGLESE FACILE',grammar='INGLESE',language='inglese',prefix='Inglese_Facile',
           picture='Un docente adulto in plastilina presenta un libro aperto, il Big Ben e un autobus londinese.',index_pages=4),
 'fr':dict(title='FRANCESE FACILE',grammar='FRANCESE',language='francese',prefix='Francese_Facile',
           picture='Un docente adulto in plastilina presenta libri, la Torre Eiffel e un rametto di lavanda.',index_pages=4),
 'es':dict(title='SPAGNOLO FACILE',grammar='SPAGNOLA',language='spagnolo',prefix='Spagnolo_Facile',
           picture='Un docente adulto in plastilina presenta un libro, una torre e un arco spagnoli e una piastrella decorata.',index_pages=3)
}
PALETTE={'#C62828':'Rosso','#E65100':'Arancione','#9A6A00':'Ambra','#2E7D32':'Verde',
 '#558B2F':'Verde chiaro','#00695C':'Verde acqua','#00838F':'Petrolio','#1565C0':'Blu',
 '#303F9F':'Indaco','#6A1B9A':'Viola','#AD1457':'Magenta','#6D4C41':'Marrone'}

FRONT_CSS='''
/* Le regole seguenti non modificano .pg, .blk, .mapcard o le mappe. */
@page { @bottom-right { content: element(lf-back); vertical-align:middle; } }
@page lf-cover { size:A4; margin:13mm 15mm 16mm;
 @bottom-center { content:none; } @bottom-right { content:none; } }
@page lf-cover:first { margin:13mm 15mm 16mm;
 @bottom-center { content:none; } @bottom-right { content:none; } }
@page lf-front { size:A4; margin:13mm 15mm 18mm;
 @bottom-center { font-size:11pt; font-weight:normal; color:#30343b; } }
@page lf-index { size:A4; margin:13mm 15mm 18mm;
 @bottom-center { font-size:11pt; font-weight:normal; color:#30343b; } }
.lf-back { position:running(lf-back); font-size:10pt; color:#1f536e; text-align:right; }
.lf-back a { color:#1f536e; text-decoration:none; }
.lf-front { color:#2e2018; line-height:1.42; font-size:14pt; }
.lf-cover { page:lf-cover; break-after:page; }
.lf-guide { page:lf-front; break-after:page; }
.lf-cover-title { color:white; background:#934a30; border-radius:11pt; padding:9pt 12pt;
 font-size:30pt; font-weight:bold; text-align:center; line-height:1.4; margin:0 0 8pt; }
.lf-subtitle { font-size:15pt; font-weight:bold; line-height:1.5; text-align:center; margin:4pt 0 0; }
.lf-cover-illustration { display:block; width:100%; height:auto; border-radius:12pt; margin:18pt auto 22pt; }
.lf-owner { border:1.2pt solid #ddd5ca; border-radius:11pt; padding:14pt 17pt; line-height:1.7; }
.lf-owner p { margin:3pt 0; }
.lf-owner .lf-name { margin:12pt 0; }
.lf-heading { background:#934a30; color:#fff; border-radius:9pt; padding:7pt 12pt;
 font-size:18pt; font-weight:bold; line-height:1.4; margin:0 0 12pt; }
.lf-card { background:#fbf7ee; border:1pt solid #e6ddce; border-radius:10pt; padding:10pt 12pt;
 margin:0 0 10pt; break-inside:avoid; }
.lf-card h3 { font-size:14pt; font-weight:bold; margin:0 0 3pt; color:#2e2018; }
.lf-card p { margin:0; }
.lf-smallnote { font-size:11.5pt; line-height:1.45; margin:10pt 0 0; }
.lf-year { width:100%; border-collapse:separate; border-spacing:0 9pt; margin:0; }
.lf-year tr { break-inside:avoid; }
.lf-year th { width:73pt; vertical-align:top; text-align:left; font-size:13pt; color:#fff;
 background:#934a30; padding:9pt 10pt; border-radius:9pt 0 0 9pt; }
.lf-year td { vertical-align:top; background:#fbf7ee; padding:9pt 12pt; border-radius:0 9pt 9pt 0; font-size:13pt; }
.lf-year strong { display:block; color:#111; margin:0 0 2pt; }
.lf-legend-intro { margin:0 0 10pt; }
.lf-colors { width:100%; border-collapse:collapse; margin:5pt 0 10pt; }
.lf-colors tr { break-inside:avoid; }
.lf-colors td { padding:6pt 7pt; border-bottom:1pt solid #e5dfd6; vertical-align:middle; font-size:12pt; }
.lf-colors td:nth-child(1) { width:135pt; font-size:13pt; font-weight:bold; }
.lf-swatch { display:inline-block; width:16pt; height:16pt; border-radius:4pt; margin-right:7pt; vertical-align:middle; }
.lf-colors a { color:#2e2018; text-decoration:none; }
.lf-index { page:lf-index; break-after:page; color:#182126; }
.lf-index-hint { background:#1f536e; color:#fff; border-radius:7pt; padding:5pt 9pt;
 font-size:11.5pt; margin:0 0 8pt; }
.lf-index-range { font-size:12pt; margin:0 0 10pt; }
.lf-toc { border-collapse:collapse; width:100%; }
.lf-toc tr { break-inside:avoid; }
.lf-toc td { vertical-align:top; padding:3pt 3pt; font-size:14pt; line-height:1.3; border-bottom:.6pt solid #e8e0d4; }
.lf-toc td.lf-toc-num { width:31pt; font-weight:bold; color:#934a30; }
.lf-toc td.lf-toc-title { padding-left:4pt; }
.lf-toc td.lf-toc-page { width:37pt; text-align:right; white-space:nowrap; font-weight:bold; }
.lf-toc a { color:#182126; text-decoration:none; }
.lf-toc-page a::after { content:target-counter(attr(href),page); }
'''


def card(title,text):
 return f'<article class="lf-card"><h3>{E(title)}</h3><p>{text}</p></article>'

def page(title,content,extra=''):
 return f'<section class="lf-front lf-guide" {extra}><h2 class="lf-heading">{E(title)}</h2>{content}</section>'


def front_pages(lang,cfg,maps):
 title=cfg['title']; lingua=cfg['language']; grammar=cfg['grammar']
 parts=[f'''<div class="lf-back"><a href="#lf-indice">Torna all’indice ↑</a></div>
<section class="lf-front lf-cover" id="lf-copertina">
<h1 class="lf-cover-title">{title}</h1>
<p class="lf-subtitle">IL QUADERNO DI GRAMMATICA {grammar}<br>
Schede, mappe e strumenti di lettura<br>Un percorso adattabile in cinque anni</p>
<img class="lf-cover-illustration" src="{ROOT}/cover_{lang}.png" alt="{E(cfg['picture'])}">
<div class="lf-owner"><p>Questo quaderno appartiene a</p>
<p class="lf-name">________________________________</p>
<p>Classe __________ &nbsp; Anno __________</p></div>
</section>''']
 p2=card('Leggo un’idea','Ogni mappa presenta un argomento. Posso ascoltare la lettura del docente, coprire le righe che non sto leggendo e fare una pausa.')
 p2+=card('Guardo lo schema','Leggo prima il titolo, poi le parole-guida e l’esempio. Il colore e l’icona aiutano a ritrovare la scheda, ma non sono gli unici segnali.')
 p2+=card('Seguo tre passi e provo','<strong>1.</strong> Guardo un esempio. <strong>2.</strong> Lo ripeto con un aiuto. <strong>3.</strong> Provo una frase simile. Posso scrivere, parlare o indicare, secondo gli aiuti concordati.')
 p2+=card('Uso la tabella, non tutta la memoria','Cerco soltanto la forma che mi serve. Non devo imparare tutte le righe insieme. Il box <strong>IN PRATICA</strong> mi aiuta a ricordare l’idea principale.')
 p2+='<p class="lf-smallnote">Posso tornare alla stessa mappa più volte. Per controllare una risposta confronto l’esempio e chiedo un riscontro al docente. L’indice collega ogni titolo alla sua pagina.</p>'
 parts.append(page('Una scheda alla volta',p2))
 years={
 'en':[
 ('Capire la frase semplice','Riprendo pronomi, be e have. Uso articoli, plurali, presente e preposizioni per parlare di me e dell’ambiente.'),
 ('Raccontare e orientarmi','Riprendo il presente e incontro il passato. Chiedo indicazioni, descrivo luoghi e confronto persone o cose.'),
 ('Collegare tempi e significati','Confronto passato e present perfect. Scelgo espressioni di tempo, obblighi, possibilità e consigli.'),
 ('Costruire messaggi più articolati','Riprendo le forme del futuro, i pronomi relativi e i condizionali presenti nel quaderno. Li riconosco in brevi testi.'),
 ('Comprendere, motivare, collegare','Uso le mappe come strumenti di consultazione. Controllo una scelta grammaticale e la spiego con poche parole.')],
 'fr':[
 ('Capire la frase semplice','Leggo suoni, articoli, pronomi e accordi. Riprendo il presente e costruisco brevi frasi affermative e negative.'),
 ('Raccontare e orientarmi','Riprendo domande, preposizioni e pronomi. Confronto i tempi del passato e incontro il futuro.'),
 ('Collegare tempi e significati','Uso comparativi, condizionale e pronomi. Riconosco chi compie l’azione e collego due frasi.'),
 ('Leggere periodi più articolati','Riprendo congiuntivo, ipotesi, passivo e discorso indiretto con esempi e schemi già disponibili.'),
 ('Comprendere, motivare, collegare','Uso connettivi e rapporti di tempo, causa e scopo. Torno alle mappe per controllare le mie scelte nei testi.')],
 'es':[
 ('Capire la frase semplice','Leggo suoni, articoli, nomi e pronomi. Riprendo il presente e distinguo ser, estar, tener e haber.'),
 ('Raccontare e orientarmi','Confronto i tempi del passato. Uso preposizioni, domande e verbi frequenti per raccontare esperienze.'),
 ('Collegare tempi e significati','Riprendo futuro, condizionale, imperativo e pronomi. Confronto le forme con l’aiuto delle tabelle.'),
 ('Leggere periodi più articolati','Incontro e riprendo congiuntivo, ipotesi, passivo e discorso indiretto negli esempi del quaderno.'),
 ('Comprendere, motivare, collegare','Uso connettivi e rapporti di causa, conseguenza e concessione. Controllo una scelta e spiego il significato.')]
 }
 p3='<table class="lf-year">'
 for n,(heading,desc) in enumerate(years[lang],1):
  p3+=f'<tr><th>Anno {n}</th><td><strong>{E(heading)}</strong>{E(desc)}</td></tr>'
 p3+='</table>'
 p3+=card('Un percorso flessibile','Queste tappe sono una proposta, non una scansione obbligatoria. Una mappa può servire in anni diversi e può essere ripresa più volte.')
 p3+='<p class="lf-smallnote">Il quaderno è una raccolta di strumenti grammaticali, non un corso completo né l’intero curricolo del liceo linguistico. Il docente sceglie tempi, testi, lessico, ascolto, conversazione e attività culturali in base alla classe e agli obiettivi individuali.</p>'
 parts.append(page('Cinque anni: come orientarsi',p3))
 p4=card('PEI e PDP hanno funzioni diverse','Per la disabilità intellettiva il PEI definisce obiettivi, aiuti e valutazione. Per i DSA il PDP può prevedere strumenti compensativi e misure dispensative: non riduce automaticamente gli obiettivi.')
 p4+=card('Non una certificazione di obiettivi minimi','La progressione proposta è flessibile. Non è un elenco ministeriale unico di «minimi». Una scheda, da sola, non determina voto, sufficienza o tipo di percorso PEI.')
 p4+=card('Ridurre il carico, non il significato','Presentare una scena o una frase chiara. Mostrare un esempio, svolgerne uno insieme e proporre un breve tentativo. Lavorare su una sola tabella alla volta; accettare risposte orali o indicate quando previsto.')
 p4+=card('Grammatica dentro la comunicazione',f'Le mappe di {lingua} si usano per capire e costruire messaggi. Si riprendono negli ascolti, nei dialoghi e nei testi: non sostituiscono lessico, pronuncia, cultura o letteratura.')
 p4+='<p class="lf-smallnote">OpenDyslexic è una scelta grafica, non una terapia né un vantaggio garantito. Verificare con ogni studente dimensione, contrasto, spaziatura e densità preferiti.</p>'
 parts.append(page('Per chi accompagna lo studio',p4))
 p5='<p class="lf-legend-intro">Nelle mappe già presenti, colori e icone aiutano a orientarsi. Lo stesso colore può ricomparire in argomenti diversi: leggo sempre il titolo e le parole-guida.</p><table class="lf-colors">'
 bycolor={}
 for m in maps:
  color=re.search(r'background\s*:\s*(#[0-9a-fA-F]{6})',m.select_one('.banner').get('style','')).group(1).upper()
  bycolor.setdefault(color,m)
 for color,name in PALETTE.items():
  if color not in bycolor: continue
  m=bycolor[color]; title=m.h2.get_text(' ',strip=True); number=m.select_one('.bnum').get_text(strip=True)
  short=title[len(number):].strip()
  p5+=f'<tr><td><span class="lf-swatch" style="background:{color}"></span>{name}</td><td><a href="#{m["id"]}">Mappa {number} · {E(short)}</a></td></tr>'
 p5+='</table>'
 p5+=card('Non devo ricordare tutto insieme','Cerco nell’indice l’argomento che mi serve. Il numero, il titolo e l’esempio restano i miei punti di riferimento, anche se il colore non mi aiuta.')
 p5+='<p class="lf-smallnote">Le mappe mantengono testi, immagini, ordine e impaginazione delle versioni precedenti. Questa nuova veste aggiunge una guida all’uso e una navigazione coordinata.</p>'
 parts.append(page('Colori e parole-guida',p5))
 return '\n'.join(parts)


def make_indices(maps,n_pages):
 # Gruppi contigui equilibrati: non viene cambiato l'ordine delle mappe.
 chunks=[]
 for j in range(n_pages):
  start=round(j*len(maps)/n_pages); stop=round((j+1)*len(maps)/n_pages)
  chunks.append(maps[start:stop])
 out=[]
 for j,chunk in enumerate(chunks):
  extra=' id="lf-indice"' if j==0 else ''
  out.append(f'<section class="lf-front lf-index"{extra}>')
  if j==0: out.append('<p class="lf-index-hint">Titoli e numeri di pagina sono collegamenti.</p>')
  out.append(f'<h2 class="lf-heading">Indice delle mappe · {j+1}/{n_pages}</h2>')
  out.append(f'<p class="lf-index-range">Mappe {chunk[0].select_one(".bnum").get_text(strip=True)}–{chunk[-1].select_one(".bnum").get_text(strip=True)} · nell’ordine originale</p><table class="lf-toc">')
  for m in chunk:
   n=m.select_one('.bnum').get_text(strip=True); t=m.h2.get_text(' ',strip=True)[len(n):].strip()
   out.append(f'<tr><td class="lf-toc-num">{n}</td><td class="lf-toc-title"><a href="#{m["id"]}">{E(t)}</a></td><td class="lf-toc-page"><a href="#{m["id"]}" aria-label="Pagina della mappa {n}"></a></td></tr>')
  out.append('</table></section>')
 return '\n'.join(out)


def build(lang,render=True):
 cfg=CFG[lang]; old=INV[lang]
 source=Path(old['html']); original=source.read_text()
 soup=BeautifulSoup(original,'html.parser')
 maps=soup.select('section.pg .blk[id]')
 # Copia letterale dall'inizio della prima pagina delle mappe alla fine dell'ultima.
 start=original.index('<section class="pg">')
 end=original.rindex('</body>')
 map_html=original[start:end]
 orig_css=soup.style.string
 front=front_pages(lang,cfg,maps)
 toc=make_indices(maps,cfg['index_pages'])
 path=ROOT/f'{cfg["prefix"]}.html'
 result=f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">
<title>{cfg['title']} · Quaderno di grammatica</title>
<meta name="author" content="Laboratorio didattico inclusivo">
<meta name="description" content="Schede, mappe e strumenti di lettura. Un percorso adattabile in cinque anni. Tutte le mappe preesistenti sono conservate senza modifiche.">
<style>{orig_css}\n{FRONT_CSS}</style></head><body>{front}\n{toc}\n{map_html}</body></html>'''
 path.write_text(result)
 # Verifica byte-identica della sezione mappe e delle singole schede.
 assert result[result.index('<section class="pg">'):result.rindex('</body>')]==map_html
 new=BeautifulSoup(result,'html.parser').select('section.pg .blk[id]')
 assert len(maps)==len(new)
 assert all(str(a)==str(b) for a,b in zip(maps,new))
 snap=ROOT/'originali'; snap.mkdir(exist_ok=True)
 shutil.copy2(source,snap/f'{lang}_sorgente.html')
 manifest={'language':lang,'title':cfg['title'],'source_html':str(source),'source_pdf':old['pdf'],
           'map_count':len(maps),'map_html_sha256':hashlib.sha256(map_html.encode()).hexdigest(),
           'map_html_byte_identical':True,'original_css_unchanged':True,
           'html':str(path),'pdf':str(ROOT/f'{cfg["prefix"]}.pdf')}
 (ROOT/f'{lang}_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print('HTML OK',lang,len(maps),'mappe byte-identiche',flush=True)
 if render:
  HTML(filename=str(path),base_url=str(source.parent)).write_pdf(manifest['pdf'],pdf_variant='pdf/ua-1')
  print('PDF OK',manifest['pdf'],flush=True)
 return manifest

if __name__=='__main__':
 import sys
 langs=[x for x in sys.argv[1:] if x in CFG] or list(CFG)
 for lang in langs: build(lang,render='--html-only' not in sys.argv)

