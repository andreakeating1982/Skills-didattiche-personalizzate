#!/usr/bin/env python3.11
"""Verifica che in una mappa non restino frazioni scritte IN LINEA con la barra (a/b).
Le frazioni devono essere ESCLUSIVAMENTE impilate (classe .frz).

Uso:
    python verifica_frazioni.py file1.html [file2.html ...]
    python verifica_frazioni.py --pdf file1.pdf [file2.pdf ...]

Restituisce exit code 0 se tutto ok, 1 se trova frazioni in linea.
Permesse: l'icona "+/−" (simbolo di segno) e i percorsi/URL.
"""
import re, sys, html, subprocess

PAT_HTML = re.compile(r'[^<>\n]{1,14}/[^<>\n]{1,14}')
PAT_PDF = re.compile(r'[a-zA-Z0-9)&][ ]?/[ ]?[a-zA-Z(0-9]')

def pulisci_html(txt):
    txt = re.sub(r'<style.*?</style>', '', txt, flags=re.S)
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)
    txt = re.sub(r'<svg.*?</svg>', '', txt, flags=re.S)
    # rimuovi le frazioni gia impilate
    txt = re.sub(r'<span class="frz".*?</span></span>', ' FRZ ', txt, flags=re.S)
    txt = re.sub(r'<[^>]*>', ' ', txt)
    return txt

def ok(hit):
    """True = caso permesso, non e' una frazione matematica."""
    h = html.unescape(hit).strip()
    raw = hit.strip()
    if h.startswith('/') or h.endswith('/'):   # frammenti/URL, non frazioni
        return True
    if 'http' in raw or '&#' in raw:           # URL ed entita' HTML spezzate
        return True
    if h in {'+/−', '+/-' }:                   # icona del segno piu'/meno
        return True
    return False

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    if args[0] == '--pdf':
        targets = [('pdf', f) for f in args[1:]]
    else:
        targets = [('html', f) for f in args]
    problemi = 0
    for kind, f in targets:
        if kind == 'html':
            txt = pulisci_html(open(f, errors='ignore').read())
            hits = [m.group(0) for m in PAT_HTML.finditer(txt)]
        else:
            # estrai il TESTO del pdf con pdftotext, mai il binario!
            txt = subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout
            hits = [m.group(0) for m in PAT_PDF.finditer(txt)]
        for h in hits:
            if not ok(h):
                print(f'{f}: possibile frazione in linea -> "{h.strip()}"')
                problemi += 1
    if problemi:
        print(f'TROVATE {problemi} frazioni in linea: convertirle in <span class="frz">...')
        sys.exit(1)
    print('OK: nessuna frazione in linea trovata.')

if __name__ == '__main__':
    main()
