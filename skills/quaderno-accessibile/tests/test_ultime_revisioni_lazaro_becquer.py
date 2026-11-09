"""Regressioni delle ultime revisioni consegnate; non rigenera PDF.

Non certifica PDF/UA, qualità delle fonti, approvazione dell'utente o contenuto
semantico delle immagini. Eseguire con unittest discover dalla cartella skill.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from bs4 import BeautifulSoup
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
L = ROOT/'templates'/'lazaro-carreter-indice-2026-11-05'
B = ROOT/'templates'/'becquer-completo-approvato-2026-11-05'
L_SHA = 'bc2e603157991cc978b86a28b60c4eaee8ffb1acce2d47b933e47b8416a776ec'
B_SHA = '75598bca9b5226caf7d2804e2180c86aaba2ab7299f02c61e0eddd618971cb50'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def soup(path):
    return BeautifulSoup(path.read_text(encoding='utf8'), 'html.parser')

def check_index(test, dom, pdf, number):
    rows = dom.select('#indice .index-row')
    test.assertEqual(len(rows), number)
    links = pdf[0].get_links()
    for row in rows:
        dest = row['href'][1:]
        page = int(row.select_one('.index-pg').get_text(strip=True)) - 1
        test.assertTrue(any(x.get('nameddest') == dest and x.get('page') == page
                            and x['from'].get_area() > 0 for x in links), dest)

def check_assets(test, dom, root):
    for img in dom.select('img[src]'):
        src = img['src']
        if src.startswith(('data:', 'http:', 'https:')):
            continue
        p = (root/src).resolve()
        test.assertTrue(p.is_relative_to(root.resolve()) and p.is_file(), src)

class LazaroRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dom = soup(L/'LAZARO_INDICE_ARIOso.html')
        cls.pdf = fitz.open(L/'LAZARO_CARRETER_INDICE_CORRETTO.pdf')

    @classmethod
    def tearDownClass(cls):
        cls.pdf.close()

    def test_baseline_e_rapporti(self):
        self.assertEqual(len(self.pdf), 32)
        self.assertEqual(sha(L/'LAZARO_CARRETER_INDICE_CORRETTO.pdf'), L_SHA)
        for file in ('QA_FINALE.json', 'QA_REVISIONI_LAZARO_BECQUER.json', 'QA_SUPPORTI_ES.json'):
            result = json.loads((L/file).read_text(encoding='utf8'))
            self.assertTrue(result['passed'], result.get('errors'))

    def test_indice_con_traduzione_abbreviata(self):
        check_index(self, self.dom, self.pdf, 13)
        self.assertEqual(self.dom.select_one('#indice a[href="#it1"] .index-label').get_text(strip=True),
                         'TRADUCCIÓN AL ITALIANO')
        self.assertIn('.index-row{min-height:10.2mm}', str(self.dom.select('style')))
        measures = json.loads((L/'misure_indice.json').read_text(encoding='utf8'))['choice']
        self.assertEqual(measures['row_min_mm'], 10.2)
        self.assertGreaterEqual(measures['remaining_mm'], 5)

    def test_italiano_solo_cio_che_e_richiesto(self):
        self.assertIsNotNone(self.dom.select_one('#it1'))
        self.assertEqual(len(self.dom.select('.lf-summary')), 14)
        self.assertIsNone(self.dom.select_one('#quiz-it'))
        self.assertIsNone(self.dom.select_one('#mappa-it'))
        self.assertEqual(len(self.dom.select('#quiz-es .quiz-card')), 10)
        self.assertEqual(len(self.dom.select('#bibliografia [data-bibliography-entry]')), 5)

    def test_mappa_e_risorse_portabili(self):
        nodes = self.dom.select('#mappa-es .lf-map-card')
        self.assertEqual(len(nodes), 7)
        for node in nodes:
            self.assertEqual(len(node.select('.lf-map-keywords span')), 3)
            self.assertTrue(node.select_one('img[alt][src]'))
        check_assets(self, self.dom, L)

class BecquerRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = soup(B/'modello-mappa-illustrata.html')
        cls.dom = soup(B/'BECQUER_TITOLI_CORRETTI.html')
        cls.before = fitz.open(B/'BECQUER_MAPPA_ILLUSTRATA_APPROVATA.pdf')
        cls.pdf = fitz.open(B/'BECQUER_MAPPA_CORRETTA.pdf')

    @classmethod
    def tearDownClass(cls):
        cls.before.close()
        cls.pdf.close()

    def test_baseline_e_rapporto(self):
        self.assertEqual(len(self.pdf), 31)
        self.assertEqual(sha(B/'BECQUER_MAPPA_CORRETTA.pdf'), B_SHA)
        report = json.loads((B/'QA_MAPPA_CORRETTA.json').read_text(encoding='utf8'))
        self.assertTrue(report['passed'], report.get('errors'))
        self.assertEqual(report['becquer_sha256'], B_SHA)

    def test_sette_titoli_e_modifica_esclusiva(self):
        previous = ['1 RIMAS', '4 BLOQUES', '2 LEYENDAS', '3 CARTAS Y ARTÍCULOS',
                    'A MÉTRICA', 'B FIGURAS', 'C LENGUAJE']
        corrected = ['RIMAS', 'BLOQUES', 'LEYENDAS', 'CARTAS Y ARTÍCULOS',
                     'MÉTRICA', 'FIGURAS', 'LENGUAJE']
        old = self.old.select('#mappa .map-node .node-title')
        after = deepcopy(self.dom)
        new = after.select('#mappa .map-node .node-title')
        self.assertEqual(len(old), 12)
        self.assertEqual(len(new), 12)
        changes = [(x.get_text(strip=True), y.get_text(strip=True)) for x,y in zip(old,new)
                   if x.get_text(strip=True) != y.get_text(strip=True)]
        self.assertEqual(changes, list(zip(previous, corrected)))
        for x,y in zip(old,new):
            y.string = x.get_text(strip=True)
        self.assertEqual(str(self.old), str(after))
        text = ' '.join(p.get_text() for p in self.pdf[27:30])
        for datum in ('79 POESÍAS', '1871', '18 RELATOS'):
            self.assertIn(datum, text)

    def test_pagine_esterne_mappa_invariate(self):
        for i in list(range(27)) + [30]:
            x = self.before[i].get_pixmap(matrix=fitz.Matrix(.75,.75), alpha=False)
            y = self.pdf[i].get_pixmap(matrix=fitz.Matrix(.75,.75), alpha=False)
            self.assertEqual((x.width,x.height), (y.width,y.height), f'pagina {i+1}')
            self.assertEqual(hashlib.sha256(x.samples).digest(), hashlib.sha256(y.samples).digest(),
                             f'pagina {i+1}')

    def test_indice_immagini_e_collegamenti(self):
        check_index(self, self.dom, self.pdf, 11)
        check_assets(self, self.dom, B)
        nodes = self.dom.select('#mappa [data-map-node]')
        self.assertEqual(len(nodes), 12)
        imgs = [(B/n.select_one('img')['src']).resolve() for n in nodes]
        self.assertEqual(len({sha(p) for p in imgs}), 12)
        # Compare counters by representation because internal and external links have different fields.
        def links(pdf):
            return sorted(repr(x) for x in [(l.get('nameddest'),l.get('page'),l.get('uri'))
                         for p in pdf for l in p.get_links() if l.get('nameddest') or l.get('uri')])
        self.assertEqual(links(self.before), links(self.pdf))

if __name__ == '__main__':
    unittest.main()

