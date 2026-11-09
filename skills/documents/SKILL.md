---
name: documents
description: 'Create, edit and convert Word (.docx), Excel (.xlsx, .csv) and PDF files: reports, letters, contracts, CVs, invoices, budgets, trackers, printable handouts. Use whenever the user wants a document file. Presentations use the slides tools.'
---

# Documents

Build documents in the sandbox with Python, check the result, and deliver the file with `send_attachment`. Presentations and slide decks are not this skill: use `slides_generate` and the slides tools, even when the user wants a .pptx.

## Pick the format and the tool

| Deliverable                                                                           | Build with                                                                                            | Read                 |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------- |
| Word document (.docx): reports, letters, contracts, CVs, templates the user will edit | `python-docx` (installed), or pandoc from Markdown for long text                                      | `references/docx.md` |
| Spreadsheet (.xlsx): budgets, trackers, models, data exports, invoices with totals    | `openpyxl` (installed)                                                                                | `references/xlsx.md` |
| PDF: polished reports, invoices, certificates, printable one-pagers                   | HTML + CSS rendered with WeasyPrint (installed)                                                       | `references/pdf.md`  |
| CSV                                                                                   | pandas `to_csv(index=False)`, UTF-8 with BOM (`encoding="utf-8-sig"`) when it will be opened in Excel | -                    |
| Markdown                                                                              | Write it directly. Keep it the default for research reports unless the user asks for another format   | -                    |

When the user names no format: an editable document means .docx, numbers or a list to work with means .xlsx, and something final to print or send means PDF.

## Editing an existing file

1. Read it first. `file_read` extracts the text from DOCX, XLSX, PPTX and PDF. Inspect the structure with the library (styles, sheets, tables) before changing anything.
2. Change only what was asked and keep the existing styles, fonts and layout. With python-docx and openpyxl, edit the loaded document and save it under a new name (`*_edited.docx`), so the original survives.
3. PDFs cannot be edited reliably in place. Rebuild them (extract the content, then regenerate), or for small changes add an overlay with `pypdf` + `reportlab` (both installed).

## Conversions

| From             | To   | How                                                                                |
| ---------------- | ---- | ---------------------------------------------------------------------------------- |
| Markdown         | DOCX | `pandoc in.md -o out.docx` (add `--reference-doc=style.docx` for custom styles)    |
| Markdown or HTML | PDF  | Markdown to HTML (`python -m markdown`) with a stylesheet, then WeasyPrint         |
| PPTX             | PDF  | `soffice --headless --convert-to pdf deck.pptx` (LibreOffice Impress is installed) |
| DOCX             | PDF  | `soffice --headless --convert-to pdf file.docx` (LibreOffice Writer is installed)  |
| XLSX             | PDF  | `soffice --headless --convert-to pdf file.xlsx` (LibreOffice Calc is installed)    |
| PDF              | Text | `file_read`, or `pdftotext -layout`                                                |
| PDF pages        | PNG  | `pdftoppm -png -r 110 file.pdf page`                                               |

An older sandbox may lack some of these tools. Install what is missing: `pip install -q python-docx`, or `sudo apt-get update -qq && sudo apt-get install -y -qq pandoc libreoffice-writer libreoffice-calc`.

## Check before delivering

- **PDF:** render the first pages to PNG (`pdftoppm -png -r 80 -f 1 -l 3 out.pdf check`) and look at them with `file_view`. Check page breaks, overflowing tables, fonts and margins.
- **DOCX:** read it back with `file_read` and confirm the headings, tables and text are all present. When the layout matters, convert a copy to PDF and look at it.
- **XLSX:** reopen it with openpyxl and check the formulas, sheet names, column widths and number formats. Recompute the key totals with pandas to confirm the formulas are right.

## Deliver

Send the file with `send_attachment` (with the source data or charts as extra files when useful). In the chat, describe what is in it in a sentence or two. Don't paste the document's content into the reply.
