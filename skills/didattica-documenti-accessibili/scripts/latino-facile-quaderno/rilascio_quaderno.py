#!/usr/bin/env python3
"""Rilascia una nuova versione del quaderno PDF «Latino Facile».

Uso:
  python3 rilascio_quaderno.py <NN>                # rigenera master + compila quaderno-unico-vNN.pdf + QA
  QUADERNO_BASE=/percorso python3 rilascio_quaderno.py <NN>

Sicuro: NON sovrascrive un PDF esistente con lo stesso numero (usa --force per forzare).
QA stampata: numero pagine, md5, dimensione, diff testo pagina-per-pagina vs la versione
precedente (v<NN-1> piu' alta esistente), rect dell'immagine di copertina su pagina 1.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys

BASE = os.environ.get("QUADERNO_BASE", "/home/user/quaderno-unico")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nn", help="numero versione, es. 16")
    ap.add_argument("--force", action="store_true", help="sovrascrive un PDF esistente")
    ap.add_argument("--no-master", action="store_true",
                    help="salta build_quaderno.py (usa il master gia' rigenerato)")
    args = ap.parse_args()
    if not re.fullmatch(r"\d+", args.nn):
        sys.exit("ERRORE: NN deve essere numerico (es. 16)")
    out = os.path.join(BASE, "quaderno-unico-v%s.pdf" % args.nn)
    if os.path.exists(out) and not args.force:
        sys.exit("%s esiste gia': scegli un NN superiore o usa --force" % out)
    if not args.no_master:
        print("> build_quaderno.py ...", flush=True)
        r = subprocess.run(["python3", "build_quaderno.py"], cwd=BASE,
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("build_quaderno.py FALLITO:\n" + (r.stdout[-2000:] + r.stderr[-2000:]))
    print("> weasyprint -> %s ..." % os.path.basename(out), flush=True)
    from weasyprint import HTML
    HTML(filename=os.path.join(BASE, "master-unico.html"), base_url=BASE).write_pdf(out)
    qa(out, BASE, args.nn)
    print("OK quaderno-unico-v%s.pdf" % args.nn)


def qa(out, base, nn):
    import pymupdf
    d = pymupdf.open(out)
    md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
    print("pagine: %d" % len(d))
    print("md5: %s" % md5)
    print("bytes: %d" % os.path.getsize(out))
    prev = None
    for f in sorted(os.listdir(base)):
        m = re.fullmatch(r"quaderno-unico-v(\d+)\.pdf", f)
        if m and int(m.group(1)) < int(nn):
            if prev is None or int(m.group(1)) > prev[0]:
                prev = (int(m.group(1)), f)
    if prev:
        dp = pymupdf.open(os.path.join(base, prev[1]))
        diff = [p + 1 for p in range(min(len(d), len(dp))) if d[p].get_text() != dp[p].get_text()]
        print("diff testo vs v%d: pagine %s" % (prev[0], diff if diff else "[] (nessuna)"))
    imgs = d[0].get_images(full=True)
    rects = [r for img in imgs for r in d[0].get_image_rects(img[0])]
    if rects:
        r = rects[0]
        print("immagine copertina: rect=(%.0f,%.0f)-(%.0f,%.0f) w=%d" %
              (r.x0, r.y0, r.x1, r.y1, imgs[0][2]))


if __name__ == "__main__":
    main()
