# PDFs from HTML and CSS with WeasyPrint

Design the document as HTML with a print stylesheet and render it with WeasyPrint, which is installed. It handles page sizes, margins, headers and footers, page numbers, page breaks, tables, images and web fonts, and the HTML stays editable.

## Template

```python
from weasyprint import HTML

html = """<!doctype html><html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  @page { size: A4; margin: 22mm 18mm 20mm;
          @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 9pt Inter; color: #6b7280; }
          @bottom-left { content: "Acme Ltd · Invoice INV-2026-014"; font: 9pt Inter; color: #6b7280; } }
  body { font: 10.5pt/1.5 Inter, sans-serif; color: #111827; }
  h1 { font-size: 22pt; margin: 0 0 4mm; }
  h2 { font-size: 13pt; margin: 8mm 0 3mm; break-after: avoid; }
  table { width: 100%; border-collapse: collapse; margin: 4mm 0; }
  th { text-align: left; background: #f3f4f6; font-weight: 600; }
  th, td { padding: 2.2mm 3mm; border-bottom: 1px solid #e5e7eb; }
  td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
  tr { break-inside: avoid; }
  .total td { font-weight: 700; border-top: 2px solid #111827; }
  img { max-width: 100%; }
</style></head><body>
  <h1>Invoice</h1>
  <p>Billed to: Northwind Traders · Due 15 November 2026</p>
  <table>
    <tr><th>Item</th><th class="num">Qty</th><th class="num">Price</th><th class="num">Amount</th></tr>
    <tr><td>Design sprint</td><td class="num">1</td><td class="num">$4,800</td><td class="num">$4,800</td></tr>
    <tr class="total"><td colspan="3">Total</td><td class="num">$4,800</td></tr>
  </table>
</body></html>"""

HTML(string=html, base_url="/home/user/docs/").write_pdf("/home/user/docs/invoice.pdf")
```

## Tips

- **Page sizes:** `size: A4` or `size: Letter` (US); `size: A4 landscape` for wide tables.
- **Page breaks:**
  - `break-before: page` on a section that must start a new page;
  - `break-inside: avoid` on table rows, figures and cards;
  - `break-after: avoid` on headings so they never end a page.
- **Images:** images, logos and charts load from file paths relative to `base_url`, or from absolute paths. Use PNG at 2x the displayed size, or SVG.
- **Fonts:** load web fonts with `@import` (the sandbox has internet access), or use `@font-face` with a local file. For Chinese, Japanese, Korean, Arabic or Hindi, use a Noto font for that script, or the text renders as boxes.
- **Markdown source:** convert it to HTML first (`import markdown; body = markdown.markdown(text, extensions=["tables", "fenced_code"])`), then wrap the result in the template above.
- **Layout support:** WeasyPrint supports flexbox and simple grids. Prefer normal flow and tables for print layouts.
- **Forms, fillable fields and digital signatures** need a dedicated library (for example `reportlab` for AcroForm fields). Ask what the user needs first.

## Check

```bash
pdftoppm -png -r 80 -f 1 -l 3 /home/user/docs/invoice.pdf /home/user/docs/check
```

Look at the page images with `file_view`. Check that nothing overflows the margins, tables don't split mid-row, the headers and footers are right, and the fonts loaded (no fallback serif or boxes).
