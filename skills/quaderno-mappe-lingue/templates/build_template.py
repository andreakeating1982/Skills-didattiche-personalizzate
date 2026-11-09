# -*- coding: utf-8 -*-
"""Quaderno inclusivo di mappe concettuali di grammatica — build generica.

Uso:
    1. Sostituisci il contenuto tra i marcatori INIZIO/FINE CONTENUTO.
    2. python build_<codice>.py                 -> genera il file HTML
    3. python scripts/render_quaderno.py <html> <pdf> --base <cartella build>
    4. python scripts/verify_quaderno.py <pdf>  -> controlla riempimento/coppie

Font richiesto: OpenDyslexic (installato in ~/.fonts dallo scaffold
scripts/nuovo_quaderno.py). Icone clay in icons/ (template/icons della skill).
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

TITOLO = "{{TITOLO}}"                 # es. MAPPE CONCETTUALI DI GRAMMATICA FRANCESE
CODICE_LINGUA = "{{CODICE}}"          # codice ISO: fr, es, en, de...
NOME_FILE = "{{NOME_FILE}}"           # es. mappe_francesi.html

# ---------------- Palette (una famiglia grammaticale = un colore) ----------------
ROSSO="#C62828"; ARANCIO="#E65100"; AMBRA="#9A6A00"; VERDE="#2E7D32"; LIME="#558B2F"
TEAL="#00695C"; PETROLIO="#00838F"; BLU="#1565C0"; INDACO="#303F9F"; VIOLA="#6A1B9A"
MAGENTA="#AD1457"; MARRONE="#6D4C41"

# ---------------- Struttura: PAGES = pagine logiche, ogni pagina = 1 o 2 mappe ----------------
PAGES = []
_cur = []
def B_(title, color, icon, caption, content):
    """Una mappa: title (MAIUSCOLE), color (palette), icon (numero icNN),
    caption (testo del box IN PRATICA), content (lista di blocchi)."""
    _cur.append(dict(title=title, color=color, icon=icon, caption=caption, content=content))
def PAGE():
    """Chiude la pagina logica corrente (1 o 2 mappe)."""
    global _cur
    PAGES.append(_cur); _cur = []

# ================ INIZIO CONTENUTO (sostituire con le mappe reali) ================
B_("ESERCIZIO A – AFFERMATIVO",BLU,1,"Didascalia semplice di una frase che riassume la mappa.",
 [("F",["soggetto","verbo"]),("X","Frase di esempio nella lingua studiata."),
  ("P",[("io","parlo"),("tu","parli")]),
  ("N","Nota breve per lo studente.")])
B_("ESERCIZIO A – NEGATIVO",BLU,2,"Seconda didascalia, breve e concreta.",
 [("F",["soggetto","non","verbo"]),("X","Frase negativa di esempio.")])
PAGE()
B_("ESEMPIO CON TABELLA",VERDE,21,"Le tabelle hanno al massimo 4 righe per la leggibilità.",
 [("T",(["soggetto","forma piena","forma contratta"],
   [("io","je suis","j'suis"),("tu","tu es","t'es")]))])
PAGE()
# ================ FINE CONTENUTO ================

# ---------------- Renderer ----------------
def esc(s):
    return s

def render_content(content, color):
    out = []
    for item in content:
        t = item[0]
        if t == "F":
            parts = item[1]
            boxes = [f'<span class="fbox" style="border-color:{color};background:{color}14;">{esc(p)}</span>' for p in parts]
            joined = boxes[0]
            for b in boxes[1:]:
                joined += f'<span class="plus" style="color:{color};">+</span>' + b
            out.append('<div class="formula">' + joined + '</div>')
        elif t == "X":
            out.append(f'<p class="ex" style="color:{BLU};">{esc(item[1])}</p>')
        elif t == "P":
            rows = []
            for a, bb in item[1]:
                rows.append(f'<tr><td class="pleft" style="color:{color};">{esc(a)}</td>'
                            f'<td class="parr" style="color:{color};">➜</td><td class="pright">{esc(bb)}</td></tr>')
            out.append('<table class="ptab">' + "".join(rows) + '</table>')
        elif t == "T":
            headers, rows = item[1]
            html_rows = []
            ths = "".join(f'<th style="background:{color};">{esc(h)}</th>' for h in headers)
            html_rows.append(f'<tr>{ths}</tr>')
            for r in rows:
                tds = "".join(f'<td>{esc(c)}</td>' for c in r)
                html_rows.append(f'<tr>{tds}</tr>')
            out.append(f'<table class="tab" style="border-color:{color};">' + "".join(html_rows) + '</table>')
        elif t == "R":
            for term, desc in item[1]:
                out.append(f'<p class="rule"><span class="rt" style="color:{color};">{esc(term)}</span> → {esc(desc)}</p>')
        elif t == "N":
            out.append(f'<p class="note"><span class="ndot" style="background:{color};"></span>{esc(item[1])}</p>')
    return "\n".join(out)

CSS = """
@page {
  size: A4;
  margin: 1.5cm 1.5cm 1.7cm 1.5cm;
  @bottom-center {
    content: counter(page);
    font-family: 'OpenDyslexic','DejaVu Sans',sans-serif;
    font-size: 14pt; font-weight: 700; color: #26211b;
  }
}
@page :first { margin: 1.1cm 1.5cm 1.5cm 1.5cm; @bottom-center { content: none; } }
* { box-sizing: border-box; }
body { font-family:'OpenDyslexic','DejaVu Sans','Liberation Sans',sans-serif;
  font-size: 14pt; line-height: 1.42; color:#111; background:#fff; margin:0; text-align:left; }
h1,h2 { margin:0; page-break-after:avoid; }
a { text-decoration: underline; }

/* ---------- COPERTINA + INDICE (una colonna) ---------- */
h1.title-banner { border-radius:12px; padding:10px 14px; color:#fff; background:#5e35b1;
  font-weight:800; font-size:14pt; line-height:1.4; margin:2px 0 8px; }
img.cover { width:42%; display:block; margin:6px auto 10px; border-radius:12px; }
.indice-banner { margin:8px 0 2px; }
.hint { font-size:14pt; color:#333; margin:4px 0 10px; }
table.indice { width:100%; border-collapse:separate; border-spacing:0 6px; margin:4px 0; }
.indice td { vertical-align:middle; padding:0 6px; }
.ind-num { display:inline-block; width:30px; height:30px; border-radius:50%; color:#fff;
  font-weight:800; font-size:14pt; line-height:30px; text-align:center; margin-right:10px; }
.ind-title { font-size:14pt; font-weight:700; line-height:1.35; color:#111; }
.ind-pag { text-align:right; font-size:14pt; font-weight:800; white-space:nowrap; width:44px; }
.ind-pag a { text-decoration:none; color:#111; }
.ind-pag a::after { content: target-counter(attr(href), page); }

/* ---------- PAGINE DELLE MAPPE ---------- */
section.pg { page-break-before: always; }
.blk { page-break-inside:avoid; }
.blk + .blk { margin-top:20px; }
.mapcard { border:2.5px solid #888; border-radius:14px; background:#fff; padding:5px 12px;
  page-break-inside:avoid; }
.banner { border-radius:12px; padding:3px 10px; margin-bottom:8px; color:#fff; page-break-after:avoid; overflow:hidden; }
.banner h2 { font-size:14pt; font-weight:800; line-height:1.3; color:#fff; text-align:left; margin-left:58px; }
img.bicon { float:left; width:48px; height:48px; border-radius:50%; background:#fff; border:2.5px solid #fff; }
.bnum { display:inline-block; background:rgba(255,255,255,.25); border-radius:8px; padding:0 8px; margin-right:8px; }
.formula { margin:5px 0 4px; }
.fbox { display:inline-block; border:2.5px solid; border-radius:10px; padding:1px 12px;
  font-weight:700; margin:2px 0; }
.plus { font-weight:800; margin:0 8px; }
.ex { font-weight:700; margin:3px 0; }
table.ptab { width:100%; border-collapse:collapse; margin:3px 0; }
.ptab td { padding:1px 8px; font-size:14pt; }
.pleft { font-weight:800; width:42%; }
.parr { font-weight:800; width:40px; text-align:center; }
table.tab { width:100%; border-collapse:collapse; margin:4px 0; }
.tab th { color:#fff; font-weight:800; padding:2px 10px; border:1.5px solid rgba(0,0,0,.08); text-align:left; }
.tab td { border:1.5px solid #cfc8ba; padding:1px 10px; }
p.rule { margin:3px 0; }
.rt { font-weight:800; }
p.note { margin:4px 0 1px; }
.ndot { display:inline-block; width:16px; height:16px; border-radius:50%; margin-right:9px; }
.pratica { border:2.5px solid #eadfc8; border-radius:12px; background:#fdf8ec;
  padding:4px 12px 5px; margin-top:10px; page-break-inside:avoid; }
.pratica .lb { font-weight:800; }
"""

# ---------------- HTML ----------------
out = [f"""<!DOCTYPE html>
<html lang="{CODICE_LINGUA}">
<head>
<meta charset="utf-8">
<title>{TITOLO} &middot; Quaderno accessibile</title>
<meta name="author" content="Laboratorio didattico inclusivo">
<meta name="description" content="Quaderno inclusivo ad alta leggibilit&agrave; (PDF/UA-1), edizione semplificata per disabilit&agrave; intellettiva: mappe di grammatica in font OpenDyslexic 14pt, tabelle ridotte, frasi brevi, due argomenti per pagina, indice cliccabile.">
<style>{CSS}</style>
</head>
<body>
<h1 class="title-banner">{TITOLO}</h1>
<img class="cover" src="media/cover.png" alt="Illustrazione in plastilina: un libro di grammatica aperto sulla scrivania con oggetti scolastici colorati.">
<h2 class="banner indice-banner" style="background:#1f3864;">INDICE</h2>
<p class="hint">Tocca il titolo di una mappa per andare direttamente alla sua pagina.</p>
<table class="indice">
"""]

num = 0
entries = []
for page in PAGES:
    anchors = []
    for b in page:
        num += 1
        anchors.append((num, b))
    entries.append(anchors)

for anchors in entries:
    for n, b in anchors:
        bid = f"m{n:02d}"
        out.append(f'<tr><td><span class="ind-num" style="background:{b["color"]};">{n}</span>'
                   f'<a class="ind-title" href="#{bid}">{esc(b["title"])}</a></td>'
                   f'<td class="ind-pag"><a href="#{bid}"></a></td></tr>')
out.append("</table>")

num = 0
for page in PAGES:
    out.append('<section class="pg">')
    for b in page:
        num += 1
        bid = f"m{num:02d}"
        c = b["color"]
        out.append(f'<div class="blk" id="{bid}">')
        out.append(f'<div class="banner" style="background:{c};">'
                   f'<img class="bicon" src="icons/ic{b["icon"]:02d}.png" alt="">'
                   f'<h2><span class="bnum">{num}</span>{esc(b["title"])}</h2></div>')
        out.append(f'<div class="mapcard" style="border-color:{c};">')
        out.append(render_content(b["content"], c))
        out.append('</div>')
        out.append(f'<div class="pratica" style="border-color:{c}55;"><span class="lb" style="color:{c};">IN PRATICA &#10148;</span> '
                   f'<span>{esc(b["caption"])}</span></div>')
        out.append('</div>')
    out.append('</section>')

out.append("</body></html>")

with open(os.path.join(BASE, NOME_FILE), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"HTML scritto: {os.path.join(BASE, NOME_FILE)} — {num} mappe in {len(PAGES)} pagine")
