from pathlib import Path
import sys
import tempfile
import unittest

from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from verifica_fonti_bibliografia import check


class BibliographyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / 'test.html'
        self.pdf = self.root / 'test.pdf'

    def tearDown(self):
        self.temp.cleanup()

    def html(self, citation='#rif-1', line_height='1', url='https://example.org/source'):
        return f'''<!doctype html><html><head><style>
        @page {{size:A4; margin:18mm}} .cite-ref {{font-size:.76em;line-height:{line_height};vertical-align:super}}
        #bibliografia {{break-before:page}}
        </style></head><body><section id="unit"><div id="body-1"><p>Una frase verificata
        <a class="cite-ref" href="{citation}">[1]</a>.</p></div></section>
        <section id="bibliografia"><h2>RIFERIMENTI BIBLIOGRAFICI</h2>
        <div id="rif-1" class="ref-entry"><p>Autore. Opera. <a href="{url}">Fonte consultata</a></p></div>
        <div id="rif-2" class="ref-entry"><p>Altro autore. Altra opera.</p></div>
        </section></body></html>'''

    def render(self, text, to=None):
        p = to or self.path
        p.write_text(text, encoding='utf-8')
        HTML(filename=str(p)).write_pdf(self.pdf)
        return p

    def test_bibliografia_e_rimando_pdf_con_area_positiva(self):
        h = self.render(self.html())
        result = check(h, self.pdf)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['entries'], 2)
        self.assertTrue(result['citations'][0]['pdf_link_ok'])
        self.assertEqual(result['pdf']['external_uris_found'], 1)
        self.assertGreater(result['citations'][0]['pdf_regions'][0]['height_pt'], 1)

    def test_bibliografia_mancante(self):
        self.path.write_text('<html><body>Testo senza bibliografia.</body></html>')
        self.assertEqual(check(self.path)['errors'][0]['issue'], 'bibliografia_non_trovata')

    def test_destinazione_html_mancante(self):
        self.path.write_text(self.html(citation='#inesistente'))
        result = check(self.path)
        self.assertFalse(result['passed'])
        self.assertIn('destinazione_non_univoca_o_assente', [e['issue'] for e in result['errors']])

    def test_destinazione_html_non_univoca(self):
        self.path.write_text(self.html().replace('id="rif-2"', 'id="rif-1"'))
        result = check(self.path)
        self.assertFalse(result['passed'])
        self.assertIn('destinazione_non_univoca_o_assente', [e['issue'] for e in result['errors']])

    def test_link_pdf_senza_altezza_e_errori(self):
        h = self.render(self.html(line_height='0'))
        result = check(h, self.pdf)
        self.assertFalse(result['passed'])
        self.assertIn('rimando_pdf_assente_o_area_nulla', [e['issue'] for e in result['errors']])

    def test_link_esterno_assente_nel_pdf(self):
        other = self.root / 'other.html'
        self.render(self.html(url='https://example.org/other'), to=other)
        self.path.write_text(self.html(url='https://example.org/source'))
        result = check(self.path, self.pdf)
        self.assertFalse(result['passed'])
        self.assertIn('link_esterno_pdf_assente_o_area_nulla', [e['issue'] for e in result['errors']])

    def test_due_rimandi_identici_nello_stesso_box_controllati_separatamente(self):
        html = self.html().replace(
            '<a class="cite-ref" href="#rif-1">[1]</a>.',
            '<a class="cite-ref" href="#rif-1">[1]</a> '
            '<a class="cite-ref" href="#rif-1" style="line-height:0">[1b]</a>.')
        h = self.render(html)
        result = check(h, self.pdf)
        self.assertFalse(result['passed'])
        self.assertTrue(result['citations'][0]['pdf_link_ok'])
        self.assertFalse(result['citations'][1]['pdf_link_ok'])
        self.assertIn('rimando_pdf_assente_o_area_nulla', [e['issue'] for e in result['errors']])

    def test_link_esterni_identici_controllati_separatamente(self):
        html = self.html().replace(
            '>Fonte consultata</a>',
            '>Fonte consultata</a> <a href="https://example.org/source" '
            'style="font-size:.76em;line-height:0;vertical-align:super">Secondo link</a>')
        h = self.render(html)
        result = check(h, self.pdf)
        self.assertFalse(result['passed'])
        self.assertTrue(result['external_links'][0]['pdf_link_ok'])
        self.assertFalse(result['external_links'][1]['pdf_link_ok'])
        self.assertIn('link_esterno_pdf_assente_o_area_nulla', [e['issue'] for e in result['errors']])

    def test_destinazione_sbagliata_anche_se_sulla_stessa_pagina(self):
        other = self.root / 'other.html'
        self.render(self.html(citation='#rif-2'), to=other)
        self.path.write_text(self.html(citation='#rif-1'))
        result = check(self.path, self.pdf)
        self.assertFalse(result['passed'])
        self.assertIn('rimando_pdf_assente_o_area_nulla', [e['issue'] for e in result['errors']])


if __name__ == '__main__':
    unittest.main()

