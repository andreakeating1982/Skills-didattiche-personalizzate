"""Test della baseline Bécquer con mappa illustrata approvata.

Eseguire dalla skill: python3 -m unittest discover -s tests -p
"test_becquer_mappa_illustrata_approvata.py" -v. Non rigenera né modifica i PDF.
I test non certificano la pertinenza delle immagini, le fonti o PDF/UA.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from bs4 import BeautifulSoup
import pymupdf as fitz
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'templates' / 'becquer-completo-approvato-2026-11-05'
CURRENT = 'f3fb8a98ba19fe42a5eecdb0d855aa0498be663c4c78fbdfe187afd298cdf651'
PREVIOUS = '2e2ee895bd94d261ed77a45e6c712f76ee6b8b17df216fa6cb77283f00b6e515'
EXPECTED_ASSETS = [
    'mapa-rimas.png', 'mapa-cuatro-bloques.png', 'immagine-003.png',
    'mapa-temas-leyendas.png', 'mapa-cartas-literarias.png', 'immagine-002.png',
    'mapa-metrica.png', 'mapa-verso-quebrado.png', 'mapa-figuras-retoricas.png',
    'mapa-otros-recursos.png', 'mapa-lenguaje.png', 'mapa-influencia.png',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk(box):
    yield box
    for child in getattr(box, 'children', []):
        yield from walk(child)


class MappaBecquerApprovataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = BeautifulSoup((T/'modello.html').read_text(encoding='utf8'), 'html.parser')
        cls.after = BeautifulSoup((T/'modello-mappa-illustrata.html').read_text(encoding='utf8'), 'html.parser')
        cls.oldpdf = fitz.open(T/'BECQUER_COMPLETO_APPROVATO.pdf')
        cls.pdf = fitz.open(T/'BECQUER_MAPPA_ILLUSTRATA_APPROVATA.pdf')

    @classmethod
    def tearDownClass(cls):
        cls.oldpdf.close()
        cls.pdf.close()

    def test_hash_e_rapporti(self):
        self.assertEqual(sha(T/'BECQUER_COMPLETO_APPROVATO.pdf'), PREVIOUS)
        self.assertEqual(sha(T/'BECQUER_MAPPA_ILLUSTRATA_APPROVATA.pdf'), CURRENT)
        self.assertEqual(len(self.pdf), 31)
        report = json.loads((T/'qa-mappa-illustrata'/'QA_FINALE.json').read_text(encoding='utf8'))
        self.assertTrue(report['passed'], report['errors'])
        self.assertEqual(report['baseline_sha256'], PREVIOUS)
        self.assertEqual(report['final_sha256'], CURRENT)
        self.assertTrue(all(item['pass'] for item in report['checks'].values()))
        for name in ('QA_BOX.json', 'QA_FONTI.json'):
            r = json.loads((T/'qa-mappa-illustrata'/name).read_text(encoding='utf8'))
            self.assertTrue(r['passed'], r['errors'])

    def test_modifica_circoscritta_a_src_e_alt_mappa(self):
        a, b = deepcopy(self.before), deepcopy(self.after)
        for soup in (a, b):
            for img in soup.select('#mappa [data-map-node] img'):
                img['src'], img['alt'] = 'IMAGE_UNCHANGED', 'ALT_UNCHANGED'
        self.assertEqual(str(a), str(b))

    def test_tutto_il_testo_preservato_per_pagina(self):
        self.assertEqual(len(self.oldpdf), len(self.pdf))
        for i in range(len(self.pdf)):
            self.assertEqual(self.oldpdf[i].get_text(), self.pdf[i].get_text(), f'pagina {i+1}')

    def test_pagine_esterne_alla_mappa_identiche_al_pixel(self):
        for i in list(range(27)) + [30]:
            a = self.oldpdf[i].get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
            b = self.pdf[i].get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
            self.assertEqual((a.width, a.height), (b.width, b.height), f'pagina {i+1}')
            self.assertEqual(hashlib.sha256(a.samples).digest(), hashlib.sha256(b.samples).digest(), f'pagina {i+1}')

    def test_dodici_immagini_distinte_e_alt_descritte(self):
        nodes = self.after.select('#mappa [data-map-node]')
        self.assertEqual(len(nodes), 12)
        actual = []
        for node in nodes:
            images = node.select('img')
            self.assertEqual(len(images), 1)
            img = images[0]
            path = (T / img['src']).resolve()
            self.assertTrue(path.is_relative_to(T.resolve()))
            self.assertTrue(path.is_file(), img['src'])
            self.assertTrue(img.get('alt', '').strip())
            actual.append(path)
        self.assertEqual([p.name for p in actual], EXPECTED_ASSETS)
        self.assertEqual(len({sha(p) for p in actual}), 12)
        for img in self.after.select('img[src]'):
            p = (T/img['src']).resolve()
            self.assertTrue(p.is_relative_to(T.resolve()) and p.is_file(), img['src'])

    def test_indice_e_note_cliccabili(self):
        rows = self.after.select('#indice .index-row')
        self.assertEqual(len(rows), 11)
        links = self.pdf[0].get_links()
        for row in rows:
            dest = row['href'][1:]
            page = int(row.select_one('.index-pg').get_text(strip=True))-1
            self.assertTrue(any(l.get('nameddest') == dest and l.get('page') == page and l['from'].get_area() > 0 for l in links), dest)
        refs = [l for page in self.pdf for l in page.get_links() if l.get('nameddest') in ('rif-1','rif-2')]
        self.assertEqual(len(refs), 4)
        self.assertEqual(sum(l['nameddest']=='rif-1' for l in refs), 2)
        self.assertEqual(sum(l['nameddest']=='rif-2' for l in refs), 2)
        self.assertTrue(all(l['from'].get_area() > 0 and l['page'] == 30 for l in refs))

    def test_bibliografia_esistente_non_duplicata(self):
        self.assertEqual(str(self.before.select_one('#bibliografia')), str(self.after.select_one('#bibliografia')))
        self.assertEqual(len(self.after.select('#bibliografia [data-bibliography-entry]')), 2)
        ref = ' '.join(self.after.select_one('#rif-2').get_text(' ', strip=True).split())
        for field in ('Cadelli','Salvaggio','Bruni','Caballero Sánchez','Vargas Vergara','Horizontes','Paisajes literarios y raíces culturales del mundo hispano','Milano','Europass','222-223'):
            self.assertIn(field, ref)
        self.assertEqual(self.pdf[-1].get_text().count('Cadelli'), 1)
        self.assertFalse(self.after.select('#bibliografia img'))

    def test_geometria_box_renderizzata(self):
        doc = HTML(filename=str(T/'modello-mappa-illustrata.html')).render()
        boxes = []
        for pn, page in enumerate(doc.pages, 1):
            for box in walk(page._page_box):
                el = box.element
                if el is not None and type(box).__name__ == 'BlockBox' and el.get('data-map-node') is not None:
                    boxes.append((pn, box.border_width()*25.4/96, box.border_height()*25.4/96))
        self.assertEqual(len(boxes), 12)
        for page, width, height in boxes:
            self.assertIn(page, (28,29,30))
            self.assertAlmostEqual(width, 78, places=1)
            self.assertAlmostEqual(height, 78, places=1)
        self.assertTrue(all(sum(row[0] == page for row in boxes) == 4 for page in (28,29,30)))


if __name__ == '__main__':
    unittest.main()

