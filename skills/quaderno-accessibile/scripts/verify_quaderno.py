#!/usr/bin/env python3.11
"""Verifica strutturale di un quaderno accessibile PDF/UA-1 generato dal
workflow della skill quaderno-accessibile.

Uso:
    python verify_quaderno.py <file.pdf> \
        [--secs "TITOLO SEZ 1|TITOLO SEZ 2|..."] \
        [--footer-prefix "<Testo del piè di pagina>"] \
        [--min-fill 200]

Il footer standard dei quaderni e' il numero di pagina semplice (solo cifre
in fondo al foglio): viene ignorato automaticamente nel calcolo del
riempimento. --footer-prefix serve solo per footer testuali (es. se un
quaderno piu' vecchio usa "Titolo · Page N").

Stampa:
- numero totale di pagine;
- per ogni pagina la y (pt) di fine contenuto reale (con i margini standard
  1.8/1.9 cm su A4 il contenuto utile arriva circa a y=790);
- elenco delle pagine quasi vuote (sotto la soglia --min-fill, default 200 pt);
- pagina d'inizio di ogni sezione indicata in --secs (confronto sul testo
  estratto, case-sensitive, dalla pagina 2 in poi);
- numero di segnalibri, Lang e Marked (informazioni PDF/UA-1).

Esito atteso per un quaderno ben impaginato: nessuna pagina quasi vuota,
ogni sezione inizia alla pagina prevista dall'indice, Lang = lingua del
documento, Marked = True.
"""
import argparse
import re
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf', help='file PDF da verificare')
    ap.add_argument('--secs', default='',
                    help='titoli esatti delle sezioni separati da | (es. "SEZIONE 1|SEZIONE 2")')
    ap.add_argument('--footer-prefix', default='',
                    help='prefisso del testo a piè di pagina da ignorare nel calcolo del riempimento')
    ap.add_argument('--min-fill', type=float, default=200.0,
                    help='soglia in pt sotto cui una pagina è considerata quasi vuota (default 200)')
    args = ap.parse_args()

    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print('Errore: serve PyMuPDF (pip install pymupdf).', file=sys.stderr)
            return 2
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None

    doc = pymupdf.open(args.pdf)
    print('Pagine totali:', len(doc))

    def is_footer(b):
        """True per i blocchi che sono solo il numero di pagina in fondo."""
        txt = b[4].strip()
        if not txt:
            return True
        if args.footer_prefix and txt.startswith(args.footer_prefix):
            return True
        # footer numerico semplice: solo cifre, nella fascia bassa del foglio
        if txt.isdigit() and b[1] > 700:
            return True
        return False

    for n, page in enumerate(doc, 1):
        blocks = [b for b in page.get_text('blocks') if b[4].strip()]
        blocks = [b for b in blocks if not is_footer(b)]
        y = max((b[3] for b in blocks), default=None)
        if y is None:
            print(f'  pagina {n}: VUOTA')
        else:
            flag = '  <-- quasi vuota!' if y < args.min_fill else ''
            print(f'  pagina {n}: fine contenuto y={y:.0f}/790{flag}')

    empty = []
    for n, page in enumerate(doc, 1):
        t = page.get_text()
        if args.footer_prefix:
            t = re.sub(re.escape(args.footer_prefix) + r'.*', '', t, flags=re.S)
        # rimuove i numeri di pagina semplici (righe di sole cifre)
        t = re.sub(r'^\s*\d+\s*$', '', t, flags=re.M)
        if len(re.sub(r'\s+', ' ', t).strip()) < 15:
            empty.append(n)
    print('Pagine quasi vuote:', empty if empty else 'nessuna')

    if args.secs.strip():
        starts = {}
        titles = [s.strip() for s in args.secs.split('|') if s.strip()]
        for i, page in enumerate(doc, 1):
            t = re.sub(r'\s+', ' ', page.get_text())
            if i == 1:
                continue
            for s in titles:
                if s not in starts and s in t:
                    starts[s] = i
        print('Inizio sezioni:')
        for s in titles:
            if s in starts:
                print(f'  pagina {starts[s]}: {s}')
            else:
                print(f'  NON TROVATA: {s}')

    if PdfReader is not None:
        r = PdfReader(args.pdf)
        root = r.trailer.get('/Root', {})
        outline = r.outline or []
        def count(o, n=0):
            for it in o:
                n = count(it, n) if isinstance(it, list) else n + 1
            return n
        print('Segnalibri:', count(outline),
              '| Lang:', root.get('/Lang'),
              '| Marked:', (root.get('/MarkInfo') or {}).get('/Marked'))

    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
