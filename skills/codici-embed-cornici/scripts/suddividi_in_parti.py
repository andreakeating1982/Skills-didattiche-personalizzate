#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Suddivide il DOCX CODICI-EMBED-CORNICI v4 in 3 documenti per materia.

Metodo: parte dal documento COMPLETO e rimuove i blocchi fuori dalla parte,
preservando stili, formattazione (Consolas 7pt), indice e impaginazione.
La numerazione dei codici resta invariata (coerenza con i post del blog).
"""
import re

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

SRC = "/home/user/CODICI-EMBED-CORNICI-v4-aggiornato-espressioni-monomi-polinomi.docx"

PARTI = [
    {
        "file": "CODICI-EMBED-CORNICI-v4-PARTE-1-matematica-e-fisica.docx",
        "titolo": "Cornici dinamiche v4 — Parte 1 · MATEMATICA E FISICA",
        "sottotitolo": ("Documento 1 di 3 — contiene i Codici 2, 4, 14 e 16. "
                        "La numerazione dei codici resta quella del documento "
                        "completo, per non cambiare i post già pubblicati."),
        "codici": {2, 4, 14, 16},
    },
    {
        "file": "CODICI-EMBED-CORNICI-v4-PARTE-2-lingue-e-strategie-di-studio.docx",
        "titolo": "Cornici dinamiche v4 — Parte 2 · LINGUE E STRATEGIE DI STUDIO",
        "sottotitolo": ("Documento 2 di 3 — contiene i Codici 1, 3, 5 e 15. "
                        "La numerazione dei codici resta quella del documento "
                        "completo, per non cambiare i post già pubblicati."),
        "codici": {1, 3, 5, 15},
    },
    {
        "file": "CODICI-EMBED-CORNICI-v4-PARTE-3-letteratura-inglese-e-spagnola.docx",
        "titolo": "Cornici dinamiche v4 — Parte 3 · LETTERATURA INGLESE E SPAGNOLA",
        "sottotitolo": ("Documento 3 di 3 — contiene i Codici 6, 7, 8, 9, 10, "
                        "11, 12 e 13. La numerazione dei codici resta quella "
                        "del documento completo, per non cambiare i post già "
                        "pubblicati."),
        "codici": {6, 7, 8, 9, 10, 11, 12, 13},
    },
]

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def codice_da_titolo(testo):
    m = re.match(r"\s*Codice (\d+) —", testo)
    return int(m.group(1)) if m else None


def codici_della_riga(testo_dx):
    return {int(n) for n in re.findall(r"\d+", testo_dx)}


def set_testo(paragrafo, testo):
    if paragrafo.runs:
        paragrafo.runs[0].text = testo
        for r in paragrafo.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        paragrafo.add_run(testo)


origine = Document(SRC)
celle_completa = {
    n: "\n".join(p.text for p in origine.tables[n].rows[0].cells[0].paragraphs)
    for n in range(1, 17)
}

for parte in PARTI:
    doc = Document(SRC)
    body = doc.element.body

    # --- mappa i figli del body in ordine reale ---
    seq = []
    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            seq.append(("p", Paragraph(child, doc)))
        elif tag == "tbl":
            seq.append(("tbl", Table(child, doc)))

    # --- decide cosa tenere: titolo, indice, blocchi della parte ---
    da_rimuovere = []
    corrente = None
    for tipo, obj in seq:
        if tipo == "p" and obj is not None:
            cod = codice_da_titolo(obj.text)
            if cod is not None:
                corrente = cod
                if cod not in parte["codici"]:
                    da_rimuovere.append(obj._p)
                continue
            testo = obj.text.strip()
            if testo.startswith("Cornici dinamiche"):
                set_testo(obj, parte["titolo"])
                continue
            if not testo:
                # paragrafi vuoti: il primo (sotto il titolo) si riempie con
                # il sottotitolo; gli altri seguono il loro blocco
                if corrente is None:
                    if parte["sottotitolo"]:
                        set_testo(obj, parte["sottotitolo"])
                        parte["sottotitolo"] = None
                    continue
                if corrente not in parte["codici"]:
                    da_rimuovere.append(obj._p)
                continue
            # paragrafo non vuoto non-titolo fuori dai blocchi: rimuovi
            if corrente is None or corrente not in parte["codici"]:
                da_rimuovere.append(obj._p)
            continue
        if tipo == "tbl":
            prima_cella = obj.rows[0].cells[0].text.strip() if obj.rows else ""
            if prima_cella.startswith("Post del blog"):
                # tabella indice: filtra le righe
                t0 = obj
                righe_da_togliere = []
                for row in t0.rows[1:]:
                    numeri = codici_della_riga(row.cells[1].text)
                    if not (numeri & parte["codici"]):
                        righe_da_togliere.append(row)
                for row in righe_da_togliere:
                    row._tr.getparent().remove(row._tr)
                continue
            if corrente is not None and corrente not in parte["codici"]:
                da_rimuovere.append(obj._tbl)
            continue

    for el in da_rimuovere:
        el.getparent().remove(el)

    doc.save("/home/user/" + parte["file"])
    print("salvato:", parte["file"])

# --- VERIFICHE ---
print("\n=== VERIFICHE ===")
ok = True
for parte in PARTI:
    d = Document("/home/user/" + parte["file"])
    # titoli dei blocchi presenti, in ordine
    titoli = []
    for p in d.paragraphs:
        cod = codice_da_titolo(p.text)
        if cod is not None:
            titoli.append(cod)
    attesi = [n for n in range(1, 17) if n in parte["codici"]]
    assert titoli == attesi, f"{parte['file']}: titoli {titoli} != {attesi}"
    # tabelle = indice + blocchi
    assert len(d.tables) == 1 + len(attesi), f"{parte['file']}: tabelle {len(d.tables)}"
    # celle identiche al documento completo
    for i, n in enumerate(attesi, start=1):
        cella = "\n".join(p.text for p in d.tables[i].rows[0].cells[0].paragraphs)
        assert cella == celle_completa[n], f"{parte['file']}: cella {n} alterata"
    # indice: righe corrette, ogni codice della parte citato esattamente una volta?
    righe = [(r.cells[0].text.strip(), r.cells[1].text.strip())
             for r in d.tables[0].rows[1:]]
    citati = set()
    for _, dx in righe:
        citati |= codici_della_riga(dx)
    assert citati == parte["codici"], f"{parte['file']}: indice copre {citati}"
    print(f"OK {parte['file']}: codici {titoli}, {len(righe)} righe indice")
    for sx, dx in righe:
        print(f"   {sx[:55]} → {dx}")
print("\nTUTTE LE VERIFICHE OK")
