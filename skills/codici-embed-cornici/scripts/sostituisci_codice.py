#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sostituisce nel DOCX CODICI-EMBED-CORNICI il blocco HTML di un codice,
aggiorna il titolo della sezione e la riga dell'indice «Post del blog».
Mantiene la formattazione originale della cella (pPr/rPr, Consolas 7pt).

Uso:
  python sostituisci_codice.py --src orig.docx --out aggiornato.docx \
      --codice 3 --html nuovo.html \
      --titolo "Codice 3 — INGLESE FACILE" \
      --indice "INGLESE — Inglese Facile"
"""
import argparse
from copy import deepcopy

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


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


def set_testo(paragrafo, testo):
    """Sostituisce il testo mantenendo la formattazione del primo run."""
    if paragrafo.runs:
        paragrafo.runs[0].text = testo
        for r in paragrafo.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        paragrafo.add_run(testo)


def aggiorna_indice(doc, n, etichetta):
    """Aggiorna la colonna sinistra della riga «Codice n» dell'indice."""
    for tbl in doc.tables:
        if tbl.rows[0].cells[0].text.strip().startswith("Post del blog"):
            for row in tbl.rows[1:]:
                if row.cells[1].text.strip() == f"Codice {n}":
                    set_testo(row.cells[0].paragraphs[0], etichetta)
                    return True
            raise SystemExit(f"Riga «Codice {n}» non trovata nell'indice")
    raise SystemExit("Tabella indice «Post del blog» non trovata")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--codice", type=int, required=True)
    ap.add_argument("--html", required=True)
    ap.add_argument("--titolo", required=True, help='es. "Codice 3 — INGLESE FACILE"')
    ap.add_argument("--indice", default=None, help='es. "INGLESE — Inglese Facile"')
    a = ap.parse_args()

    with open(a.html, encoding="utf-8") as f:
        lines = f.read().splitlines()

    doc = Document(a.src)
    heading, tabella = trova(doc, a.codice)
    set_testo(heading, a.titolo)

    cell = tabella.rows[0].cells[0]
    tc = cell._tc
    p0 = cell.paragraphs[0]
    ppr = p0._p.find(qn("w:pPr"))
    rpr = p0.runs[0]._r.find(qn("w:rPr")) if p0.runs else None
    if ppr is None:
        raise SystemExit("Il primo paragrafo della cella non ha pPr: struttura inattesa")

    # svuota la cella e ricompila riga per riga con la stessa formattazione
    for p in tc.findall(qn("w:p")):
        tc.remove(p)
    for line in lines:
        p = OxmlElement("w:p")
        p.append(deepcopy(ppr))
        r = OxmlElement("w:r")
        if rpr is not None:
            r.append(deepcopy(rpr))
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = line
        r.append(t)
        p.append(r)
        tc.append(p)

    if a.indice is not None:
        aggiorna_indice(doc, a.codice, a.indice)

    doc.save(a.out)

    # ---- verifica ricaricando il file salvato ----
    d2 = Document(a.out)
    h2, t2 = trova(d2, a.codice)
    cell2 = t2.rows[0].cells[0]
    assert len(cell2.paragraphs) == len(lines), "conteggio paragrafi non corrisponde"
    assert cell2.paragraphs[0].text == lines[0]
    assert cell2.paragraphs[-1].text == lines[-1]
    print(f"salvato: {a.out}")
    print(f"titolo: {h2.text.strip()}")
    print(f"cella: {len(cell2.paragraphs)} paragrafi (= righe HTML)")
    if a.indice is not None:
        for tbl in d2.tables:
            if tbl.rows[0].cells[0].text.strip().startswith("Post del blog"):
                for row in tbl.rows[1:]:
                    if row.cells[1].text.strip() == f"Codice {a.codice}":
                        print(f"indice: {[c.text.strip() for c in row.cells]}")
                        break
                break
    print("VERIFICHE OK")


if __name__ == "__main__":
    main()
