#!/usr/bin/env python3.11
"""Rende un quaderno accessibile PDF/UA-1 da HTML con WeasyPrint.

Uso:
    python render_quaderno.py <input.html> <output.pdf> [--base DIR]

--base: cartella base per le risorse relative (immagini, font). Se omessa,
usa la cartella del file HTML di input.

Produce un PDF conforme a PDF/UA-1 (pdf_variant='pdf/ua-1'): i segnalibri
derivano dai titoli h1/h2/h3 dell'HTML, il tag <html lang> imposta la lingua
del documento, gli attributi alt delle immagini vengono inclusi.
"""
import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html', help='file HTML di input')
    ap.add_argument('pdf', help='file PDF di output')
    ap.add_argument('--base', default=None,
                    help='cartella base per le risorse relative (default: cartella dell\'HTML)')
    args = ap.parse_args()

    try:
        from weasyprint import HTML
    except ImportError as e:
        print('Errore: serve WeasyPrint (pip install weasyprint).', file=sys.stderr)
        return 2

    src = Path(args.html).resolve()
    if not src.exists():
        print(f'Errore: HTML non trovato: {src}', file=sys.stderr)
        return 2
    base = args.base or str(src.parent)
    out = Path(args.pdf).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    HTML(str(src), base_url=base).write_pdf(str(out), pdf_variant='pdf/ua-1')
    print('OK ->', out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
