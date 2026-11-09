from pathlib import Path
from weasyprint import HTML
r=Path(__file__).resolve().parent
h=r/'10_METODOLOGIE_DIDATTICHE_INCLUSIVE_SPECCHIETTI_BOX_v14.html'
HTML(filename=str(h)).write_pdf(str(h.with_suffix(".pdf")),pdf_variant="pdf/ua-1")
