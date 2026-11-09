#!/usr/bin/env python3
"""Ritaglia le figure da un'immagine 2D (linea del tempo, cartellone, mappa...)
e prepara le texture per il diorama 3D: rimozione sfondo con flood fill dai
bordi, pulizia bordi, targhette 2:1, insegna opzionale, meta.json e provino.

La funzione cutout() e' quella verificata sul progetto reale
(/home/user/modello3d/): il confronto e' FISSO sul bianco del seme
(FLOODFILL_FIXED_RANGE), cosi' le parti chiare DENTRO la figura (camicie
bianche, pergamene, marmo) restano al loro posto.

Uso:
  python3 ritaglia_figure.py --source source.png \
      --cols 90-225,245-405,439-576,605-775,803-940,961-1098,1146-1308 \
      --band 366-542 --centers 11.45,23.62,36.88,50.15,63.34,74.82,89.17 \
      --events "1808|Guerra de Independencia,1812|Constitución de Cádiz,..." \
      --out-dir tex --up 3 [--font Caladea-Bold.ttf] [--no-title]
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BORDEAUX = (122, 31, 43)
DARKBROWN = (44, 24, 16)
CREAM = (243, 228, 205)
GOLD = (201, 162, 39)


def cutout(rgb_crop: Image.Image, tol=16, pad=6, erode=3):
    """Ritaglio dello sfondo con flood fill dai bordi + sfumatura dei colori."""
    rgb = np.asarray(rgb_crop).astype(np.uint8)
    h, w = rgb.shape[:2]

    # cornice bianca di servizio: garantisce un seme di sfondo pulito
    big = np.full((h + 2 * pad, w + 2 * pad, 3), 255, np.uint8)
    big[pad:pad + h, pad:pad + w] = rgb

    ff = np.zeros((big.shape[0] + 2, big.shape[1] + 2), np.uint8)
    flags = (4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
             | (255 << 8))
    cv2.floodFill(big.copy(), ff, (0, 0), 0, (tol,) * 3, (tol,) * 3, flags)
    bg = ff[1:-1, 1:-1][pad:pad + h, pad:pad + w] > 0
    mask = (~bg).astype(np.uint8)

    # via l'ultimo velo di pixel quasi bianchi del bordo sfumato
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=erode)

    # sacche di sfondo chiuse fra i piedi: bianco PIATTO, a differenza delle
    # parti bianche vere della figura che hanno sempre un minimo di ombreggiatura
    nearwhite = (rgb.min(axis=2) >= 255 - tol).astype(np.uint8)
    enclosed = (nearwhite & mask).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(enclosed, 8)
    for j in range(1, n):
        if stats[j, cv2.CC_STAT_AREA] < 28:
            continue
        sel = lab == j
        px = rgb[sel]
        flat = float((px.min(axis=1) >= 253).mean())
        if flat > 0.80 and float(px.std()) < 3.0:
            mask[sel] = 0

    # chiude i buchi lasciati da riflessi molto chiari dentro la figura
    k3 = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k3, iterations=2)

    # tiene solo i pezzi veri: via i granelli isolati
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    keep = np.zeros_like(mask)
    for j in range(1, n):
        if stats[j, cv2.CC_STAT_AREA] >= 45:
            keep[lab == j] = 1
    mask = keep

    # colori "sbavati" verso l'esterno: niente aloni bianchi sui bordi
    bleed = rgb.copy()
    m = mask.copy()
    for _ in range(8):
        dil_col = cv2.dilate(bleed * m[..., None], k3)
        dil_m = cv2.dilate(m, k3)
        new = (dil_m > 0) & (m == 0)
        bleed[new] = dil_col[new]
        m = dil_m

    alpha = cv2.GaussianBlur(mask * 255, (3, 3), 0)
    out = np.dstack([bleed, alpha]).astype(np.uint8)
    return Image.fromarray(out, "RGBA"), mask


def make_label(anno, testo, idx, out_dir, font_bold):
    """Targhetta 2:1. La larghezza sul modello e' vincolata dalla distanza fra
    le scene: per ingrandire il testo si alza la targa invece di allargarla."""
    S = 2                                  # texture 2048x1024: testo nitido
    W, H = 1024 * S, 512 * S
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([6 * S, 6 * S, W - 6 * S, H - 6 * S], radius=38 * S,
                        fill=CREAM + (255,), outline=GOLD + (255,), width=10 * S)
    d.rounded_rectangle([30 * S, 30 * S, W - 30 * S, H - 30 * S], radius=24 * S,
                        outline=GOLD + (110,), width=3 * S)

    f_year = ImageFont.truetype(font_bold, 210 * S)
    bb = d.textbbox((0, 0), anno, font=f_year)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], 44 * S), anno, font=f_year,
           fill=BORDEAUX + (255,))
    d.line([(W * 0.24, 274 * S), (W * 0.76, 274 * S)], fill=GOLD + (200,),
           width=5 * S)

    fs = 104 * S
    f_text = ImageFont.truetype(font_bold, fs)
    words, lines, cur = testo.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textbbox((0, 0), t, font=f_text)[2] > W - 70 * S and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    while len(lines) > 2 and fs > 60 * S:
        fs -= 8 * S
        f_text = ImageFont.truetype(font_bold, fs)
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textbbox((0, 0), t, font=f_text)[2] > W - 70 * S and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        lines.append(cur)
    if len(lines) > 1 and fs > 76 * S:
        fs = 76 * S
        f_text = ImageFont.truetype(font_bold, fs)

    total = len(lines) * fs + (len(lines) - 1) * 6 * S
    top, bot = 296 * S, H - 44 * S
    y = top + (bot - top - total) / 2
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=f_text)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), ln, font=f_text,
               fill=DARKBROWN + (255,))
        y += fs + 6 * S
    img.save(os.path.join(out_dir, f"label_{idx}.png"))


def make_title(out_dir, font_bold):
    W, H = 2048, 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([6, 6, W - 6, H - 6], radius=34,
                        fill=(250, 248, 245, 255), outline=BORDEAUX + (255,),
                        width=11)
    d.rounded_rectangle([32, 32, W - 32, H - 32], radius=22,
                        outline=GOLD + (255,), width=5)
    f_eb = ImageFont.truetype(font_bold, 50)
    eb = "E S P A Ñ A   ·   S I G L O   X I X"
    bb = d.textbbox((0, 0), eb, font=f_eb)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], 70), eb, font=f_eb,
           fill=BORDEAUX + (255,))
    f_t = ImageFont.truetype(font_bold, 110)
    for i, ln in enumerate(["Marco histórico del", "Romanticismo en España"]):
        bb = d.textbbox((0, 0), ln, font=f_t)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], 166 + i * 128), ln,
               font=f_t, fill=DARKBROWN + (255,))
    img.save(os.path.join(out_dir, "title.png"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Ritaglio figure + texture per diorama 3D")
    ap.add_argument("--source", required=True, help="Immagine sorgente (PNG)")
    ap.add_argument("--cols", required=True, help="Colonne X delle figure, es. 90-225,245-405")
    ap.add_argument("--band", required=True, help="Fascia verticale delle figure, es. 366-542")
    ap.add_argument("--centers", required=True, help="Centri percentuali, es. 11.45,23.62")
    ap.add_argument("--events", required=True, help="Eventi: 'ANNO|Nome,ANNO|Nome,...'")
    ap.add_argument("--out-dir", default="tex", help="Cartella texture di output")
    ap.add_argument("--up", type=int, default=3, help="Sovracampionamento (default 3)")
    ap.add_argument("--font", default=None, help="Font Bold (default: Caladea-Bold.ttf nella cartella)")
    ap.add_argument("--no-title", action="store_true", help="Non generare l'insegna del titolo")
    args = ap.parse_args()

    base = Path(args.source).resolve().parent
    out_dir = str((base / args.out_dir))
    os.makedirs(out_dir, exist_ok=True)
    font_bold = args.font or str(base / "Caladea-Bold.ttf")

    cols = [tuple(map(int, c.split("-"))) for c in args.cols.split(",")]
    y0, y1 = map(int, args.band.split("-"))
    centers = [float(c) for c in args.centers.split(",")]
    events = [(e.split("|")[0], e.split("|")[1]) for e in args.events.split(",")]
    if not (len(cols) == len(centers) == len(events)):
        raise SystemExit("cols / centers / events devono avere la stessa lunghezza")
    up = args.up

    src = Image.open(args.source).convert("RGB")
    band_h = (y1 - y0) * up
    meta = {"band_h": band_h, "up": up, "figures": [], "events": events}
    provini = []

    for i, (x0, x1) in enumerate(cols):
        crop = src.crop((x0 - 5, y0, x1 + 5, y1))
        crop = crop.resize((crop.width * up, crop.height * up), Image.LANCZOS)
        rgba, mask = cutout(crop)

        cols_nz = np.nonzero(mask.sum(axis=0) > 0)[0]
        lx, rx = int(cols_nz[0]), int(cols_nz[-1])
        rgba = rgba.crop((max(0, lx - 2), 0, min(rgba.width, rx + 3), band_h))
        mask = mask[:, max(0, lx - 2):min(mask.shape[1], rx + 3)]

        rows_nz = np.nonzero(mask.sum(axis=1) > 0)[0]
        p = os.path.join(out_dir, f"figura_{i}.png")
        rgba.save(p)
        meta["figures"].append({
            "file": f"figura_{i}.png", "w": rgba.width, "h": rgba.height,
            "top": int(rows_nz[0]), "bottom": int(rows_nz[-1]),
            "center_pct": centers[i],
            "area_pct": round(float(mask.mean()) * 100, 1),
        })
        print(f"figura_{i}: {rgba.width}x{rgba.height} "
              f"contenuto y {rows_nz[0]}-{rows_nz[-1]} "
              f"riempimento {mask.mean()*100:.1f}%")
        provini.append(rgba)

    for i, (a, t) in enumerate(events):
        make_label(a, t, i, out_dir, font_bold)
    if not args.no_title:
        make_title(out_dir, font_bold)

    # provino unico su fondo a scacchi per controllare i ritagli
    provini = [p.resize((p.width // up, p.height // up), Image.LANCZOS)
               for p in provini]
    cw = sum(p.width for p in provini) + 20 * len(provini)
    sheet = Image.new("RGBA", (cw, band_h // up + 20), (0, 0, 0, 0))
    chk = Image.new("RGBA", sheet.size, (255, 255, 255, 255))
    dch = ImageDraw.Draw(chk)
    for yy in range(0, sheet.height, 16):
        for xx in range(0, sheet.width, 16):
            if (xx // 16 + yy // 16) % 2:
                dch.rectangle([xx, yy, xx + 15, yy + 15], fill=(205, 205, 215, 255))
    x = 10
    for p in provini:
        sheet.paste(p, (x, 10), p)
        x += p.width + 20
    Image.alpha_composite(chk, sheet).save(str(base / "provino_ritagli.png"))

    with open(base / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("OK — texture, provino_ritagli.png e meta.json pronti")


if __name__ == "__main__":
    main()
