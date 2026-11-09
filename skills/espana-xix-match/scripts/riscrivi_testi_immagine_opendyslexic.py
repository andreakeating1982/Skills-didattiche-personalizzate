#!/usr/bin/env python3
"""Ridisegna i testi di timeline.png con OpenDyslexic, senza cambiare la
geometria dell'immagine (stesse fasce, stesse dimensioni finali):
  - frase di istruzioni in alto  -> OpenDyslexic-Regular grigio
  - anni viola sotto i nodi      -> OpenDyslexic-Bold (colore campionato)
  - titoli degli eventi          -> OpenDyslexic-Regular (colore campionato)

Uso (root = cartella dell'app scaffold web-static, default espana-xix-match):

    python3 riscrivi_testi_immagine_opendyslexic.py [root] [file_output]

Esempio per una NUOVA app clonata in /home/user/mia-app:

    python3 riscrivi_testi_immagine_opendyslexic.py /home/user/mia-app

Il file di output predefinito è client/public/timeline.png della root (si può
passare un secondo argomento per scrivere su un file temporaneo e ispezionarlo
prima di promuoverlo).

Prima di lanciarlo adattare le liste CX (posizioni % dei nodi), YEARS e
TITLES ai dati della nuova linea del tempo. I testi interni alle vignette in
creta (trama 3D) restano intatti.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/espana-xix-match"
OUT = sys.argv[2] if len(sys.argv) > 2 else f"{ROOT}/client/public/timeline.png"
PUB = f"{ROOT}/client/public"
SRC = f"{PUB}/timeline.png"  # sorgente: l'immagine attuale (serve per colori e geometria)

OD_REG = f"{PUB}/fonts/OpenDyslexic-Regular.ttf"
OD_BOLD = f"{PUB}/fonts/OpenDyslexic-Bold.ttf"

# ── DA ADATTARE ALLA NUOVA LINEA DEL TEMPO ────────────────────────────────────
# Posizione % (x) dei nodi/colonne degli eventi, anni e titoli come in events.ts
CX = [10.7, 24.1, 37.0, 50.2, 63.2, 76.3, 89.4]
YEARS = ["1808", "1812", "1833", "1868", "1873", "1875", "1898"]
TITLES = [
    "Guerra de Independencia",
    "Constitución de Cádiz",
    "I Guerra Carlista",
    "La Gloriosa",
    "Primera República",
    "Restauración borbónica",
    "Desastre del 98",
]
INSTR = "Escucha el audio y pulsa en el mapa el acontecimiento histórico correspondiente."
# ───────────────────────────────────────────────────────────────────────────────

im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()
d = ImageDraw.Draw(im)


def dark_in(x, y, thr=235):
    r, g, b = px[x, y]
    return r < thr and g < thr and b < thr


def core_color(x0, y0, x1, y1):
    """Colore 'pieno' dei glifi (pixel ben scuri)."""
    core = []
    for y in range(max(0, y0), min(H - 1, y1) + 1):
        for x in range(max(0, x0), min(W - 1, x1) + 1):
            r, g, b = px[x, y]
            if r < 170 and g < 170 and b < 170:
                core.append((r, g, b))
    if not core:
        return (60, 60, 60)
    core.sort(key=lambda c: c[0] + c[1] + c[2])
    return core[len(core) // 2]


def ink_x_extent(xc, y0, y1, half=90):
    xs = []
    for y in range(y0, y1 + 1):
        for x in range(max(0, xc - half), min(W, xc + half)):
            if dark_in(x, y):
                xs.append(x)
    return (min(xs), max(xs)) if xs else None


# ── 1) Istruzione in alto: cancella la riga e ridisegna centrata ─────────────
def instr_rows():
    rows = [y for y in range(0, int(H * 0.40)) if any(
        dark_in(x, y) for x in range(0, W, 3))]
    return (rows[0], rows[-1]) if rows else (40, 70)


inst_y0, inst_y1 = instr_rows()
ext = ink_x_extent(W // 2, inst_y0, inst_y1, half=700)
inst_maxw = (ext[1] - ext[0]) if ext else 1010
inst_color = core_color(0, inst_y0, W, inst_y1)
inst_yc = (inst_y0 + inst_y1) / 2
d.rectangle([0, inst_y0 - 1, W, inst_y1 + 1], fill=(255, 255, 255))
size = 34
while size > 12:
    f = ImageFont.truetype(OD_REG, size)
    if d.textlength(INSTR, font=f) <= inst_maxw + 4:
        break
    size -= 1
inst_font = ImageFont.truetype(OD_REG, size)
d.text((W / 2, inst_yc), INSTR, font=inst_font, fill=inst_color, anchor="mm")
print(f"istruzione: maxw orig {inst_maxw} colore {inst_color} -> font {size}")

# ── 2) Etichette in basso: anni + titoli per ogni evento ─────────────────────
# Fasce tipiche misurate su timeline 1376x821: anno 660..689 (centro ~674),
# titoli 700..760 (blocco centrato ~730). Se l'immagine ha proporzioni diverse
# vengono rilevate in automatico come ultimo blocco di testo sotto la freccia.
# (per semplicità si usano qui le fasce note; per un layout nuovo misurarle)
YEAR_Y0, YEAR_Y1 = 660, 689
TITLE_Y0, TITLE_Y1 = 700, 760
TITLE_YC = 730
WHITE = (255, 255, 255)

for i, xc_pct in enumerate(CX):
    xc = int(xc_pct / 100 * W)
    prev_cx = 0 if i == 0 else CX[i - 1] / 100 * W
    next_cx = W if i == len(CX) - 1 else CX[i + 1] / 100 * W
    left_b = (xc - prev_cx) / 2
    right_b = (next_cx - xc) / 2
    budget = int(min(left_b, right_b) * 2) - 12

    # campiona colore ed estensione PRIMA di cancellare
    year_color = core_color(max(0, xc - 90), YEAR_Y0, min(W, xc + 90), YEAR_Y1)
    title_color = core_color(max(0, xc - budget // 2), TITLE_Y0, min(W, xc + budget // 2), TITLE_Y1)
    y_ext = ink_x_extent(xc, YEAR_Y0, YEAR_Y1)
    y_maxw = (y_ext[1] - y_ext[0] + 8) if y_ext else 100

    # cancella l'area etichette di questo evento
    er_x0, er_x1 = max(0, xc - budget // 2 - 14), min(W, xc + budget // 2 + 14)
    d.rectangle([er_x0, YEAR_Y0 - 10, er_x1, TITLE_Y1 + 10], fill=WHITE)

    # anno
    ys = 36
    while ys > 14:
        fy = ImageFont.truetype(OD_BOLD, ys)
        if d.textlength(YEARS[i], font=fy) <= y_maxw:
            break
        ys -= 1
    fy = ImageFont.truetype(OD_BOLD, ys)
    d.text((xc, (YEAR_Y0 + YEAR_Y1) / 2), YEARS[i], font=fy, fill=year_color, anchor="mm")

    # titolo: wrap in max 2 righe, blocco centrato verticalmente su TITLE_YC;
    # se l'ultima riga resta un token corto (es. "98") si prova a riassorbirla.
    ts = 21
    words = TITLES[i].split()
    chosen = None
    while ts >= 13:
        ft = ImageFont.truetype(OD_REG, ts)
        tmp = []
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if not cur or d.textlength(t, font=ft) <= budget:
                cur = t
            else:
                tmp.append(cur)
                cur = w
        if cur:
            tmp.append(cur)
        if len(tmp) == 2 and len(tmp[1].split()) == 1 and len(tmp[1]) <= 3:
            merged = tmp[0] + " " + tmp[1]
            if d.textlength(merged, font=ft) <= budget:
                tmp = [merged]
        if len(tmp) <= 2:
            chosen = (ts, tmp)
            break
        ts -= 1
    ts, lines = chosen if chosen else (21, [TITLES[i]])
    ft = ImageFont.truetype(OD_REG, ts)
    lineh = ts * 1.34
    n = len(lines)
    block_h = n * lineh
    top = TITLE_YC - block_h / 2
    for j, line in enumerate(lines):
        d.text((xc, top + lineh * (j + 0.5)), line, font=ft, fill=title_color, anchor="mm")
    print(f"evento {xc_pct}%: anno size {ys} | titolo size {ts} righe {n}")

im.save(OUT, "PNG")
print("salvata", OUT, im.size)
