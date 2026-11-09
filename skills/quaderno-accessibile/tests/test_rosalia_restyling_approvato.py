"""Regression checks for the user-approved Rosalía layout; no PDFs are written.

This is a *case-specific* check, not certification of arbitrary documents. The
visual/semantic review and independent PDF/UA validation remain necessary.
Run: python3 -m unittest discover -s tests -p 'test_rosalia_restyling_approvato.py'
"""
from pathlib import Path
import collections
import hashlib
import json
import re
import sys
import unicodedata
import unittest

import pymupdf as fitz
from bs4 import BeautifulSoup
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'templates' / 'rosalia-revisione-approvata-2026-11-04'
sys.path.insert(0, str(ROOT / 'scripts'))
from verifica_box_semantici import check


def compact(s):
    return ''.join(ch for ch in unicodedata.normalize('NFKC', s)
                   if not ch.isspace() and ch != '\u00ad')


def tokens(lines):
    text = unicodedata.normalize('NFKC', ' '.join(lines)).replace('\u00ad', '')
    return re.findall(r"[^\W_]+(?:[’'\-][^\W_]+)*|[➜☐—]", text, re.U)


def pdf_lines(doc):
    lines = []
    for page in list(doc)[1:]:  # skip first-page index and variable page numbers
        for block in page.get_text('dict', sort=True)['blocks']:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                if line['bbox'][1] <= 790:
                    lines.append(''.join(s['text'] for s in line['spans']))
    return lines


class RosalíaApprovedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = fitz.open(T / 'ROSALIA_ORIGINALE.pdf')
        cls.final = fitz.open(T / 'ROSALIA_DE_CASTRO_APPROVATO.pdf')
        cls.soup = BeautifulSoup((T / 'modello.html').read_text(encoding='utf-8'), 'html.parser')
        cls.report = json.loads((T / 'qa' / 'VERIFICA_FINALE.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.source.close()
        cls.final.close()

    def test_hash_e_baseline(self):
        files = {
            'ROSALIA_ORIGINALE.pdf': '13de20e7fb47de98afb5e67b0d25b1d252222431e24a6b4ccc61a75bdeeb8aba',
            'ROSALIA_DE_CASTRO_APPROVATO.pdf': '8c15697a1dca573b580f6de00d6cadb910ea68410d415be8b193a98cdaec54ec',
        }
        for name, expected in files.items():
            self.assertEqual(hashlib.sha256((T / name).read_bytes()).hexdigest(), expected)
        self.assertEqual((len(self.source), len(self.final)), (15, 21))
        self.assertTrue(self.report['passed'])

    def test_media_portabili(self):
        for node in self.soup.select('img[src]'):
            path = (T / node['src']).resolve()
            self.assertTrue(path.is_file(), node['src'])
            self.assertTrue(path.is_relative_to(T), node['src'])
        for name in ('OpenDyslexic-Regular.otf', 'OpenDyslexic-Bold.otf'):
            self.assertTrue((T / 'media' / name).exists())

    def test_confronto_testo_con_etichetta_ammessa_esplicita(self):
        old = collections.Counter(tokens(pdf_lines(self.source)))
        new = collections.Counter(tokens(pdf_lines(self.final)))
        labels = [e.get_text(' ', strip=True) for e in self.soup.select('[data-repeated-label]')]
        repeated = collections.Counter(tokens(labels))
        self.assertEqual(sum(repeated.values()), 40)
        self.assertEqual(old - (new - repeated), collections.Counter())
        self.assertEqual((new - repeated) - old, collections.Counter())
        self.assertEqual(sum((new - old).values()), 40)

    def test_sequenza_e_neretti_corpuscoperti(self):
        sections = {
            1:[(2,range(2,15))], 2:[(3,range(2,18))],
            3:[(4,range(10,20)),(5,range(0,5))], 4:[(5,range(13,17)),(6,range(0,7))],
            5:[(6,range(9,20)),(7,range(0,12)),(7,[21])],
            6:[(8,range(3,6)),(8,range(7,22)),(9,range(0,9)),(9,range(10,13)),
               (9,range(13,24)),(9,range(25,29)),(10,range(0,14)),(10,[14])],
            7:[(11,range(1,21))], 8:[(13,range(2,12)),(13,range(13,19)),
               (14,range(0,27)),(15,range(0,5))], 9:[(15,range(7,12))],
        }
        for n, parts in sections.items():
            expected = []
            for page_number, ids in parts:
                blocks = self.source[page_number-1].get_text('dict', sort=True)['blocks']
                for i in ids:
                    for line in blocks[i]['lines']:
                        for span in line['spans']:
                            bold = 'Bold' in span['font'] and 'DejaVu' not in span['font']
                            expected.extend((ch, bold) for ch in compact(span['text']))
            actual = []
            for p in self.soup.select(f'#sec{n} .blk p'):
                for node in p.find_all(string=True):
                    actual.extend((ch, bool(node.find_parent('strong'))) for ch in compact(str(node)))
            self.assertEqual(actual, expected, f'testo/neretto sezione {n}')

    def test_informazioni_tabelle_non_slittano(self):
        tables = self.soup.select('.summary-table')
        expected = [
            [('Cantares gallegos',['1863','gallego','poemario','la voz del pueblo gallego']),
             ('Follas novas',['1880','gallego','poemario','sufrimiento y soledad']),
             ('En las orillas del Sar',['1884','castellano','poemario','intimismo y muerte']),
             ('Lieders',['1858','castellano','prosa','la condición femenina']),
             ('La hija del mar · Flavio · El caballero de las botas azules · El primer loco',
              ['—','castellano','novelas','narrativa'])],
            [('Anáfora',['repetir una palabra al principio de versos o frases','“Libre es mi corazón, libre mi alma, y libre mi pensamiento”']),
             ('Paralelismo',['repetir la misma estructura sintáctica','“como los pájaros, como las brisas; como los árboles…”']),
             ('Pregunta retórica',['una pregunta que no espera respuesta','“¿Por qué siendo tan pura…?”'])],
        ]
        for table, rows in zip((tables[0],tables[2]), expected):
            trs = table.select('tbody tr')
            self.assertEqual(len(trs), len(rows))
            for tr, (name, values) in zip(trs, rows):
                cells = tr.find_all('td', recursive=False)
                self.assertEqual(compact(cells[0].get_text()), compact(name))
                fields = cells[1].select('.data-field')
                self.assertEqual(len(fields), len(values))
                for node, value in zip(fields, values):
                    label = node.select_one('.data-label').get_text()
                    self.assertEqual(compact(node.get_text().replace(label, '', 1)), compact(value))
        self.assertEqual(len(self.soup.select('#sec9 .checklist-line')), 5)

    def test_qr_e_mappe_presenti_come_immagini_originali(self):
        digests = {x['digest'].hex() for p in self.final
                   for x in p.get_image_info(hashes=True, xrefs=True)}
        for page_no, block_no in [(12,1),(12,3),(13,12)]:
            page = self.source[page_no-1]
            block = page.get_text('dict',sort=True)['blocks'][block_no]
            media = T / 'media' / f'p{page_no:02d}-b{block_no:02d}.{block["ext"]}'
            self.assertEqual(media.read_bytes(), block['image'])
            matches = [i for i in page.get_image_info(hashes=True,xrefs=True)
                       if fitz.Rect(i['bbox']).intersects(fitz.Rect(block['bbox']))
                       and i['width']==block['width'] and i['height']==block['height']]
            self.assertEqual(len(matches),1)
            self.assertIn(matches[0]['digest'].hex(),digests)
        qr = json.loads((T / 'qa' / 'QA_QR.json').read_text())
        self.assertTrue(qr['matches_original'])

    def test_indice_link_e_numero_pagina(self):
        # Do not confuse an anchor's final continuation page with its first page.
        doc = HTML(filename=str(T / 'modello.html')).render()
        anchors = {}
        for page_no,page in enumerate(doc.pages,1):
            for name in page.anchors:
                anchors.setdefault(name,page_no)
        links = self.final[0].get_links()
        for n in range(1,10):
            a = self.soup.select_one(f'#indice a.c{n}')
            page = anchors[f'sec{n}']
            self.assertEqual(int(a.select_one('.index-pg').get_text(strip=True)),page)
            text = a.select_one('.index-label').get_text(' ',strip=True)
            hits = self.final[0].search_for(text)
            self.assertTrue(any(z.get('page') == page-1 and any(z['from'].intersects(r) for r in hits)
                                for z in links), n)

    def test_limite_reale_box(self):
        result = check(T / 'modello.html')
        self.assertTrue(result['passed'], result['errors'])
        self.assertLessEqual(result['max_lines'],5)
        self.assertEqual(result['cards'],66)


if __name__ == '__main__':
    unittest.main()

