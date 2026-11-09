#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae l'HTML di un codice dal DOCX CODICI-EMBED-CORNICI.

Uso:
  python estrai_codice.py --src file.docx --codice 3 [--out codice3-attuale.html]

Stampa la mappa di ciò che va adattato per una nuova app: titolo del blocco,
APP_URL, domini usati, font woff2, titolo della testata, prefissi CSS.
"""
import argparse
import re
from collections import Counter

from docx import Document


def corpo(doc):
    """Ritorna [(tipo, oggetto)] con paragrafi e tabelle in ordine reale."""
    seq, pi, ti = [], 0, 0
    for child in doc.element.body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            seq.append(("p", doc.paragraphs[pi]))
            pi += 1
        elif tag == "tbl":
            seq.append(("tbl", doc.tables[ti]))
            ti += 1
    return seq


def trova(doc, n):
    """Ritorna (paragrafo_titolo, tabella_codice) per il Codice n."""
    seq = corpo(doc)
    for i, (tipo, obj) in enumerate(seq):
        if tipo == "p" and obj.text.strip().startswith(f"Codice {n} — "):
            for tipo2, obj2 in seq[i + 1:]:
                if tipo2 == "tbl":
                    return obj, obj2
            raise SystemExit(f"Nessuna tabella dopo il titolo del Codice {n}")
    raise SystemExit(f"Titolo «Codice {n} — …» non trovato")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--codice", type=int, required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    doc = Document(a.src)
    heading, table = trova(doc, a.codice)
    cell = table.rows[0].cells[0]
    lines = [p.text for p in cell.paragraphs]
    full = "\n".join(lines)

    out = a.out or f"codice{a.codice}-attuale.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)

    print(f"titolo: {heading.text.strip()}")
    print(f"righe estratte: {len(lines)} -> {out}")

    print("\nAPP_URL / URL di configurazione:")
    for m in sorted(set(re.findall(r"APP_URL\s*=\s*'[^']*'", full))):
        print("  " + m)

    print("\nDomini usati (da sostituire per la nuova app):")
    for dom, cnt in Counter(re.findall("https://([^/\\s'\\\"<)]+)", full)).most_common():
        print(f"  {dom}  x{cnt}")

    print("\nFont woff2:")
    for m in sorted(set(re.findall("https://[^\\s']+\\.woff2", full))):
        print("  " + m)

    print("\nTitolo testata (lf-titolo):")
    for m in re.findall(r'class="[a-z0-9]+-titolo">([^<]+)<', full):
        print("  " + m)

    pref = re.findall(r'class="([a-z0-9]+)-', full) + re.findall(r"\.([a-z0-9]+)-[a-z]+", full)
    print(f"\nPrefissi CSS: {Counter(pref).most_common(5)}")


if __name__ == "__main__":
    main()
