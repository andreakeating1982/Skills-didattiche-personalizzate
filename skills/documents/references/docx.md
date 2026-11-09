# Word documents with python-docx

python-docx is installed (in an older sandbox: `pip install -q python-docx`).

## A clean, well-structured document

```python
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Cm

doc = Document()

# Base style: one readable font for the whole document.
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
for section in doc.sections:
    section.left_margin = section.right_margin = Cm(2.2)
    section.top_margin = section.bottom_margin = Cm(2)

doc.add_heading("Quarterly Operations Review", level=0)
p = doc.add_paragraph("Prepared for the leadership team · October 2026")
p.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)

doc.add_heading("1. Summary", level=1)
doc.add_paragraph(
    "Delivery times fell by 18% after the new routing system went live, while costs stayed flat."
)
for item in ["Average delivery: 2.3 days (from 2.8)", "Complaints: down 31%", "Cost per order: $4.12"]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("2. Results by region", level=1)
rows = [("Region", "Orders", "Avg. days"), ("North", "12,410", "2.1"), ("South", "9,870", "2.6")]
table = doc.add_table(rows=len(rows), cols=3)
table.style = "Light Grid Accent 1"
table.alignment = WD_TABLE_ALIGNMENT.CENTER
for r, row in enumerate(rows):
    for c, value in enumerate(row):
        cell = table.cell(r, c)
        cell.text = value
        if r == 0:
            cell.paragraphs[0].runs[0].font.bold = True
        if c > 0:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

doc.add_picture("/home/user/analysis/chart.png", width=Cm(15))
doc.add_page_break()
doc.save("/home/user/docs/operations-review.docx")
```

## Useful pieces

- **Headings.** Use `add_heading(level=1..3)` so Word's navigation pane and table of contents work. Don't fake headings with bold paragraphs.
- **Numbered lists:** `style="List Number"`. Nested lists: `"List Bullet 2"`, `"List Number 2"`.
- **Bold, italic and colour inside a sentence:** add several runs to one paragraph.
  ```python
  p = doc.add_paragraph()
  p.add_run("Due date: ").bold = True
  p.add_run("15 November 2026")
  ```
- **Page numbers and headers.** `section.header.paragraphs[0].text = "Acme Ltd · Confidential"`. A page number field needs raw XML (`w:fldSimple` with `PAGE`). Add it only when asked.
- **Letters, CVs and contracts.** Keep the layout simple: one column, clear headings, consistent spacing (`paragraph_format.space_after = Pt(6)`). Fancy multi-column CVs break in many readers.
- **Templates.** When the user supplies a .docx to fill in, open it with `Document(path)` and replace text run by run, so the formatting survives. Placeholders split across runs need joining first.

## Long text: Markdown through pandoc

For a long report already written in Markdown, pandoc gives proper headings, lists, tables and footnotes:

```bash
pandoc report.md -o report.docx --toc
```

To match a house style, generate a reference document once (`pandoc -o ref.docx --print-default-data-file reference.docx`), adjust its styles with python-docx, then pass `--reference-doc=ref.docx`.
