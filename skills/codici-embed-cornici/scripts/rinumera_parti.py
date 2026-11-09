#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigenera i 3 documenti DOCX della raccolta con la numerazione delle
cornici RIPARTENTE DA 1 in ogni file.

- Titolo dei blocchi: «Cornice k — NOME APP» (k = 1..n nel singolo file)
- Indice: colonna destra «Cornici a, b (Codici N, M)» con il numero
  originale tra parentesi, per i post del blog già pubblicati
- Le celle HTML restano byte-per-byte identiche al documento completo
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
        "codici": [2, 4, 14, 16],
    },
    {
        "file": "CODICI-EMBED-CORNICI-v4-PARTE-2-lingue-e-strategie-di-studio.docx",
        "titolo": "Cornici dinamiche v4 — Parte 2 · LINGUE E STRATEGIE DI STUDIO",
        "codici": [1, 3, 5, 15],
    },
    {
        "file": "CODICI-EMBED-CORNICI-v4-PARTE-3-letteratura-inglese-e-spagnola.docx",
        "titolo": "Cornici dinamiche v4 — Parte 3 · LETTERATURA INGLESE E SPAGNOLA",
        "codici": [6, 7, 8, 9, 10, 11, 12, 13],
    },
]

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def codice_da_titolo(testo):
    m = re.match(r"\s*Codice (\d+) —", testo)
    return int(m.group(1)) if m else None


def codici_della_riga(testo_dx):
    return [int(n) for n in re.findall(r"\d+", testo_dx)]


def elenca(numeri, parola):
    """[2,3] -> 'Cornici 2 e 3'; [3,4,5] -> 'Cornici 3, 4 e 5'; [1] -> 'Cornice 1'"""
    nums = [str(n) for n in numeri]
    if len(nums) == 1:
        return f"{parola} {nums[0]}"
    if len(nums) == 2:
        return f"{parola} {nums[0]} e {nums[1]}"
    return f"{parola} " + ", ".join(nums[:-1]) + f" e {nums[-1]}"


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
    mappa = {orig: k for k, orig in enumerate(parte["codici"], start=1)}
    n = len(parte["codici"])
    sottotitolo = (
        f"Documento {list(p['file'] for p in PARTI).index(parte['file']) + 1} di 3 — "
        f"contiene le Cornici 1–{n}, corrispondenti ai Codici "
        f"{', '.join(str(c) for c in parte['codici'])} del documento completo. "
        "La numerazione riparte da 1 in ogni parte: nell'indice, tra parentesi, "
        "trovi il numero originale («Codice») da citare nei post del blog."
    )

    doc = Document(SRC)
    body = doc.element.body

    seq = []
    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            seq.append(("p", Paragraph(child, doc)))
        elif tag == "tbl":
            seq.append(("tbl", Table(child, doc)))

    da_rimuovere = []
    corrente = None
    for tipo, obj in seq:
        if tipo == "p" and obj is not None:
            cod = codice_da_titolo(obj.text)
            if cod is not None:
                corrente = cod
                if cod in mappa:
                    resto = obj.text.split(" — ", 1)[1]
                    set_testo(obj, f"Cornice {mappa[cod]} — {resto}")
                else:
                    da_rimuovere.append(obj._p)
                continue
            testo = obj.text.strip()
            if testo.startswith("Cornici dinamiche"):
                set_testo(obj, parte["titolo"])
                continue
            if not testo:
                if corrente is None:
                    set_testo(obj, sottotitolo)
                    continue
                if corrente not in mappa:
                    da_rimuovere.append(obj._p)
                continue
            if corrente is None or corrente not in mappa:
                da_rimuovere.append(obj._p)
            continue
        if tipo == "tbl":
            prima_cella = obj.rows[0].cells[0].text.strip() if obj.rows else ""
            if prima_cella.startswith("Post del blog"):
                # intestazione della colonna destra
                set_testo(obj.rows[0].cells[1].paragraphs[0], "Cornici da usare")
                for row in obj.rows[1:]:
                    orig_testo = row.cells[1].text.strip()
                    orig_nums = codici_della_riga(orig_testo)
                    if not orig_nums or not set(orig_nums) & set(mappa):
                        row._tr.getparent().remove(row._tr)
                        continue
                    nuovi = sorted(mappa[x] for x in orig_nums)
                    parola = "Cornice" if len(nuovi) == 1 else "Cornici"
                    parola_orig = "Codice" if len(orig_nums) == 1 else "Codici"
                    set_testo(row.cells[1].paragraphs[0],
                              f"{elenca(nuovi, parola)} "
                              f"({elenca(orig_nums, parola_orig)})")
                continue
            if corrente is not None and corrente not in mappa:
                da_rimuovere.append(obj._tbl)
            continue

    for el in da_rimuovere:
        el.getparent().remove(el)

    doc.save("/home/user/" + parte["file"])
    print("salvato:", parte["file"], "| mappa:", mappa)

# ---------------- VERIFICHE ----------------
print("\n=== VERIFICHE ===")
for parte in PARTI:
    mappa = {orig: k for k, orig in enumerate(parte["codici"], start=1)}
    d = Document("/home/user/" + parte["file"])

    # titoli rinumerati, in ordine
    titoli = []
    for p in d.paragraphs:
        m = re.match(r"\s*Cornice (\d+) —", p.text)
        if m:
            titoli.append((int(m.group(1)), p.text))
    attesi = list(range(1, len(parte["codici"]) + 1))
    assert [k for k, _ in titoli] == attesi, f"{parte['file']}: titoli {titoli}"
    # il nome dell'app è rimasto identico
    for k, t in titoli:
        orig_n = parte["codici"][k - 1]
        completo = [p.text for p in origine.paragraphs
                    if p.text.strip().startswith(f"Codice {orig_n} —")][0]
        assert t.split(" — ", 1)[1] == completo.split(" — ", 1)[1]

    # celle invariate
    assert len(d.tables) == 1 + len(parte["codici"])
    for i, orig_n in enumerate(parte["codici"], start=1):
        cella = "\n".join(p.text for p in d.tables[i].rows[0].cells[0].paragraphs)
        assert cella == celle_completa[orig_n], f"{parte['file']}: cella {orig_n} alterata"

    # indice: ogni cornice citata, con l'originale tra parentesi
    righe = [(r.cells[0].text.strip(), r.cells[1].text.strip())
             for r in d.tables[0].rows[1:]]
    citati, originali = set(), set()
    for _, dx in righe:
        m = re.match(r"Cornic[ei] [^()]*\(([^()]*)\)$", dx)
        assert m, f"riga indice non conforme: {dx!r}"
        citati |= {int(x) for x in re.findall(r"\d+", dx.split("(")[0])}
        originali |= {int(x) for x in re.findall(r"\d+", m.group(1))}
    assert originali == set(parte["codici"]), \
        f"{parte['file']}: originali {originali}"
    print(f"OK {parte['file']}")
    print("   titoli:", [t for _, t in titoli])
    for sx, dx in righe:
        print(f"   {sx[:52]} → {dx}")
print("\nTUTTE LE VERIFICHE OK")
