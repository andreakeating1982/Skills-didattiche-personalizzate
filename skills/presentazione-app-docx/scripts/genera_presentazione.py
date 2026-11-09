#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la presentazione DOCX BREVE (max 15 righe) di un'app per il blog.

Uso:
  python genera_presentazione.py --titolo "INGLESE FACILE" \
      --testo paragrafo.txt --link https://app.easy-peasy.site \
      --out Presentazione.docx \
      [--colore-titolo 7B2D26] [--colore-accento 8A6400] [--dimensione-titolo 22]

Il file --testo contiene il paragrafo completo (UTF-8). Il token {LINK}
viene sostituito con l'hyperlink cliccabile verso --link. Lo script stampa
parole e righe stimate e avvisa oltre il limite di 15 righe (~220 parole).
"""
import argparse

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


def hyperlink(paragraph, url, text, colore):
    """Aggiunge un hyperlink cliccabile al paragrafo."""
    r_id = paragraph.part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hl = OxmlElement("w:hyperlink")
    hl.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    col = OxmlElement("w:color")
    col.set(qn("w:val"), colore)
    rPr.append(col)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    b = OxmlElement("w:b")
    rPr.append(b)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    hl.append(run)
    paragraph._p.append(hl)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--titolo", required=True)
    ap.add_argument("--testo", required=True, help="file UTF-8 con il paragrafo; token {LINK}")
    ap.add_argument("--link", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--colore-titolo", default="7B2D26")
    ap.add_argument("--colore-accento", default="8A6400")
    ap.add_argument("--dimensione-titolo", type=float, default=22)
    a = ap.parse_args()

    with open(a.testo, encoding="utf-8") as f:
        testo = f.read().strip()

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.2)
    sec.left_margin = sec.right_margin = Cm(2.4)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11.5)
    normal.paragraph_format.line_spacing = 1.2

    # titolo centrato
    tp = doc.add_paragraph()
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = tp.add_run(a.titolo)
    tr.bold = True
    tr.font.size = Pt(a.dimensione_titolo)
    tr.font.color.rgb = RGBColor.from_string(a.colore_titolo)
    tp.paragraph_format.space_after = Pt(10)

    # paragrafo unico con hyperlink al posto di {LINK}
    p = doc.add_paragraph()
    parti = testo.split("{LINK}")
    label = a.link.replace("https://", "")
    if len(parti) == 1:
        p.add_run(testo)
    else:
        p.add_run(parti[0])
        hyperlink(p, a.link, label, a.colore_titolo)
        p.add_run("{LINK}".join(parti[1:]) if len(parti) > 2 else parti[1])

    doc.save(a.out)

    # ---- verifica ----
    d2 = Document(a.out)
    parole = sum(len(par.text.split()) for par in d2.paragraphs)
    print(f"salvato: {a.out}")
    print(f"parole: {parole}  (~{round(parole / 15)} righe — limite 15 righe ≈ 220 parole)")
    if parole > 220:
        print("⚠️ TROPPO LUNGO: l'utente vuole al massimo 15 righe — accorciare il paragrafo.")
    ok_link = any(
        r.reltype == RELATIONSHIP_TYPE.HYPERLINK and r.target_ref == a.link
        for r in d2.part.rels.values()
    )
    print(f"hyperlink {a.link}: {'OK' if ok_link else 'MANCANTE'}")
    print(f"immagini: {len(d2.inline_shapes)} (attese 0 nella versione breve)")


if __name__ == "__main__":
    main()
