"""Test portabile della baseline Bécquer approvata. Non genera né modifica il PDF.

La struttura non certifica PDF/UA, la qualità didattica o l'attendibilità delle fonti.
Eseguire: python3 -m unittest discover -s tests -p 'test_becquer_completo_approvato.py' -v
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

import pymupdf as fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'templates' / 'becquer-completo-approvato-2026-11-05'
EXPECTED = '2e2ee895bd94d261ed77a45e6c712f76ee6b8b17df216fa6cb77283f00b6e515'


def norm(element):
    return ' '.join(element.get_text(' ', strip=True).split())


class BecquerCompletoApprovatoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = BeautifulSoup((T / 'modello.html').read_text(encoding='utf8'), 'html.parser')
        cls.before = BeautifulSoup((T / 'versione_precedente.html').read_text(encoding='utf8'), 'html.parser')
        cls.pdf = fitz.open(T / 'BECQUER_COMPLETO_APPROVATO.pdf')
        cls.qa = json.loads((T / 'qa' / 'QA_FINALE.json').read_text(encoding='utf8'))

    @classmethod
    def tearDownClass(cls):
        cls.pdf.close()

    def test_hash_pagine_e_report(self):
        self.assertEqual(hashlib.sha256((T/'BECQUER_COMPLETO_APPROVATO.pdf').read_bytes()).hexdigest(), EXPECTED)
        self.assertEqual(len(self.pdf), 31)
        self.assertTrue(self.qa['passed'], self.qa['errors'])
        self.assertEqual(self.qa['finale_sha256'], EXPECTED)
        self.assertEqual(self.soup.html['lang'], 'es')
        for name in ('QA_BOX.json', 'QA_FONTI.json'):
            report = json.loads((T/'qa'/name).read_text(encoding='utf8'))
            self.assertTrue(report['passed'], report['errors'])

    def test_risorse_relative(self):
        for image in self.soup.select('img[src]'):
            resource = (T/image['src']).resolve()
            self.assertTrue(resource.is_relative_to(T), image['src'])
            self.assertTrue(resource.is_file(), image['src'])
        for font in ('OpenDyslexic-Regular.otf', 'OpenDyslexic-Bold.otf'):
            self.assertTrue((T/'media'/font).is_file())

    def test_indice_11_voci_in_prima_pagina(self):
        rows = self.soup.select('#indice .index-row')
        self.assertEqual(len(rows), 11)
        links = self.pdf[0].get_links()
        for row in rows:
            dest = row['href'][1:]
            page = int(row.select_one('.index-pg').get_text(strip=True))-1
            self.assertTrue(any(l.get('nameddest') == dest and l.get('page') == page
                                and l['from'].get_area() > 0 for l in links), dest)
        self.assertEqual(norm(self.soup.select_one('.index-row[href="#mappa"] .index-label')), 'MAPA CONCEPTUAL FINAL')
        self.assertEqual(norm(self.soup.select_one('.index-row[href="#bibliografia"] .index-label')), 'REFERENCIAS BIBLIOGRÁFICAS')

    def test_specchietti_conservati_senza_grassetto(self):
        summaries = self.soup.select('[data-support-profile="summary"]')
        self.assertEqual(len(summaries), 6)
        for table in summaries:
            self.assertEqual(norm(table.select_one('.summary-title')), 'EN RESUMEN')
            self.assertFalse(table.select('strong,b'))
        for section in range(1, 10):
            self.assertEqual(len(self.soup.select(f'#sec{section} [data-support-profile="summary"]')),
                             1 if section in (1, 2, 3, 4, 5, 7) else 0)

    def test_testo_salvo_cambi_approvati(self):
        for section in range(1, 10):
            a = deepcopy(self.before.select_one(f'#sec{section}'))
            b = deepcopy(self.soup.select_one(f'#sec{section}'))
            for x in a.select('.summary-title') + b.select('.summary-title'):
                x.string = 'EN RESUMEN'
            for x in b.select('.refnote'):
                x.decompose()
            if section == 5:
                a.select_one('[data-bibliography-box]').decompose()
            if section == 8:
                headers = [h for h in a.select('h3') if norm(h) == 'ESCANEAD EL CÓDIGO QR']
                self.assertEqual(len(headers), 1)
                headers[0].decompose()
                duplicate = a.select_one('[data-id="s8a-3"] strong:nth-of-type(2)')
                self.assertEqual(norm(duplicate), 'ESCANEAD EL CÓDIGO QR.')
                duplicate.decompose()
            self.assertEqual(str(a), str(b), f'sezione {section}')
        self.assertEqual(len(self.soup.select('#sec6 .question')), 10)
        self.assertTrue(all(len(q.select('td')) == 4 for q in self.soup.select('#sec6 .question')))

    def test_mappa_e_cronologia_specifiche(self):
        a = deepcopy(self.before.select_one('#mappa'))
        b = deepcopy(self.soup.select_one('#mappa'))
        for header in list(a.select('h3')):
            if norm(header) == 'BÉCQUER EN UN MAPA · SÍNTESIS FINAL':
                header.decompose()
            elif norm(header) == 'SU VIDA · LOS AÑOS CLAVE':
                header.find_next_sibling('div', class_='timeline').decompose()
                header.decompose()
        for row in b.select('.map-row'):
            row.attrs.pop('style', None)
        self.assertEqual(str(a), str(b))
        self.assertEqual(len(self.soup.select('#sec1 .timeline .year')), 8)
        self.assertEqual(len(self.soup.select('#mappa .timeline')), 0)
        self.assertEqual(len(self.soup.select('#mappa [data-map-node]')), 12)
        self.assertEqual(norm(self.soup.select_one('#mappa h2')), 'MAPA CONCEPTUAL FINAL')
        self.assertIn('width:78mm;height:78mm', self.soup.style.string)

    def test_riferimento_originale_spostato(self):
        old = norm(self.before.select_one('#sec5 [data-bibliography-box]')).replace('FUENTE · ', '')
        new = norm(self.soup.select_one('#rif-2')).replace('[2] ', '').replace('hispano ,', 'hispano,')
        self.assertEqual(old, new)
        self.assertFalse(self.soup.select('#sec5 [data-bibliography-box]'))
        self.assertEqual(len(self.soup.select('#bibliografia [data-bibliography-entry]')), 2)
        self.assertFalse(self.soup.select('#bibliografia img'))

    def test_quattro_note_cliccabili(self):
        refs = [l for page in self.pdf for l in page.get_links()
                if l.get('nameddest') in ('rif-1', 'rif-2')]
        self.assertEqual(len(refs), 4)
        self.assertEqual(sum(l['nameddest'] == 'rif-1' for l in refs), 2)
        self.assertEqual(sum(l['nameddest'] == 'rif-2' for l in refs), 2)
        self.assertTrue(all(l['page'] == 30 and l['from'].get_area() > 0 for l in refs))
        self.assertEqual(len(self.soup.select('sup.refnote a')), 4)
        self.assertTrue(any(l.get('uri') == 'https://www.cervantesvirtual.com/portales/gustavo_adolfo_becquer/autor_biografia/'
                            for l in self.pdf[-1].get_links()))

    def test_qr_e_consegna_conservati(self):
        self.assertEqual(len(self.soup.select('#sec8 img.qr')), 1)
        self.assertIn('escanear el código QR', norm(self.soup.select_one('[data-id="s8a-3"]')))
        source = fitz.Pixmap(str(T/'media'/'immagine-008.png'))
        expected = hashlib.sha256(source.samples).hexdigest()
        occurrences = []
        for page in self.pdf:
            for image in page.get_images(full=True):
                if image[2:4] == (194, 194) and page.get_image_rects(image[0]):
                    occurrences.append(hashlib.sha256(fitz.Pixmap(self.pdf, image[0]).samples).hexdigest())
        self.assertEqual(occurrences, [expected])


if __name__ == '__main__':
    unittest.main()

