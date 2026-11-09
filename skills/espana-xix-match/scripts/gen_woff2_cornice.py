#!/usr/bin/env python3
"""Genera i WOFF2 OpenDyslexic per la CORNICE DINAMICA (embed Blogger).

La cornice dinamica v3 (cartella cornice-dinamica/) carica i font dal
dominio dell'app con suffisso -v2 (cache-buster), es.:
  https://<APP>/fonts/OpenDyslexic-Regular-v2.woff2
  https://<APP>/fonts/OpenDyslexic-Bold-v2.woff2

Il server dell'app deve servire /fonts/* con l'header
"Access-Control-Allow-Origin: *" (CORS per il @font-face cross-origin
da Blogger) — in espana-xix-match è in server/index.ts.

Uso:
  python3 gen_woff2_cornice.py                     # default: root app espana
  python3 gen_woff2_cornice.py --root /percorso/nuova-app

Dipendenze: fonttools + brotli (pip install fonttools brotli).
"""
import argparse
import os
from fontTools.ttLib import TTFont

# (TTF sorgente, woff2 di destinazione con suffisso -v2)
PAIRS = [
    ("OpenDyslexic-Regular.ttf", "OpenDyslexic-Regular-v2.woff2"),
    ("OpenDyslexic-Bold.ttf", "OpenDyslexic-Bold-v2.woff2"),
]


def main() -> None:
    ap = argparse.ArgumentParser(description="Genera i WOFF2 -v2 per la cornice dinamica")
    ap.add_argument("--root", default="/home/user/espana-xix-match",
                    help="root del progetto (default: espana-xix-match)")
    args = ap.parse_args()

    fonts_dir = os.path.join(args.root, "client", "public", "fonts")
    if not os.path.isdir(fonts_dir):
        raise SystemExit(f"cartella font non trovata: {fonts_dir}")

    for src, dst in PAIRS:
        src_path = os.path.join(fonts_dir, src)
        dst_path = os.path.join(fonts_dir, dst)
        if not os.path.isfile(src_path):
            print(f"!! sorgente mancante, salto {src}")
            continue
        f = TTFont(src_path)
        f.flavor = "woff2"
        f.save(dst_path)
        print(f"OK {dst_path} ({os.path.getsize(dst_path)} bytes)")


if __name__ == "__main__":
    main()
