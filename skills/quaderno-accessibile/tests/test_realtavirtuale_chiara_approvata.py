#!/usr/bin/env python3
"""Verifiche offline della specifica baseline VR approvata; nessuna generazione."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re,unicodedata,unittest
import fitz

SKILL=Path(__file__).resolve().parents[1]
BASE=SKILL/'templates/realta-virtuale-chiara-approvata-2026-11-05'
PDF=BASE/'REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.pdf'
HTML=BASE/'REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.html'
DATA=BASE/'articolo_chiaro.json'
EXPECTED='5dcc0e4b22acb02941ae3fae3a9cb6f7ad1e672fb829907a5c04d435e2720e76'

def norm(s):
    s=unicodedata.normalize('NFKC',s).casefold().replace('’',"'").replace('–','-')
    return re.sub(r'\s+',' ',s).strip()

class TestBaselineRealtaVirtualeApprovata(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_text(encoding='utf-8'))
        cls.html=BeautifulSoup(HTML.read_text(encoding='utf-8'),'html.parser')
        cls.doc=fitz.open(PDF)

    @classmethod
    def tearDownClass(cls): cls.doc.close()

    def test_pdf_originale_identico_e_metadata(self):
        self.assertEqual(hashlib.sha256(PDF.read_bytes()).hexdigest(),EXPECTED)
        self.assertEqual(len(self.doc),17)
        self.assertEqual(self.doc.metadata['title'],'REALTÀ VIRTUALE A SCUOLA')
        self.assertEqual(self.doc.metadata['author'],'ANDREA CENTINARO')

    def test_tutte_domande_e_opzioni_in_pdf(self):
        qs=self.data['quiz']['questions']; self.assertEqual(len(qs),10)
        text=norm(' '.join(self.doc[n-1].get_text(sort=False) for n in (13,14)))
        covered=set()
        for q in qs:
            self.assertEqual(len(q['options']),4,q['id'])
            self.assertIn(q['correct'],'ABCD'); self.assertTrue(q['rationale'])
            self.assertIn(norm(q['stem']),text,q['id'])
            for option in q['options']:self.assertIn(norm(option),text,(q['id'],option))
            covered.update(q['section_ids'])
        self.assertEqual(covered,{s['id'] for s in self.data['sections']})
        self.assertNotIn('SOLUZIONI DELLA VERIFICA',text.upper())

    def test_riassunti_immagini_e_mappa(self):
        self.assertEqual(len(self.data['sections']),5)
        self.assertEqual(sum(len(s['summary']) for s in self.data['sections']),25)
        for u in self.data['sections']:
            section=self.html.select_one('#'+u['id']);self.assertIsNotNone(section)
            self.assertEqual(len(section.select('.lf-summary')),1)
            self.assertEqual(len(section.select('.unit-opening img')),1)
        cards=self.html.select('#mappa .standard-map-card')
        self.assertEqual(len(cards),7)
        map_text=norm(' '.join(self.doc[n-1].get_text(sort=False) for n in (15,16)))
        for card in cards:self.assertEqual(len(card.select('img')),1)
        for item in self.data['map_updates'].values():
            for word in item['keywords']:self.assertIn(norm(word),map_text)
        self.assertFalse(self.html.select('#bibliografia img'))

    def test_riferimenti_e_indice_nel_pdf(self):
        uris={l.get('uri') for p in self.doc for l in p.get_links() if l.get('uri')}
        self.assertEqual(len(self.data['references']),4)
        for ref in self.data['references']:self.assertIn(ref['url'],uris)
        self.assertGreaterEqual(len([x for x in self.doc[0].get_links() if x.get('page') is not None]),8)
        self.assertIn('Articolo scritto da',self.doc[-1].get_text())

    def test_sorgente_e_media_portabili(self):
        for node,attr in [('link','href'),('img','src')]:
            for el in self.html.select(f'{node}[{attr}]'):
                ref=el[attr]
                if not ref.startswith(('http:','https:','data:','#')):
                    self.assertTrue((BASE/ref).is_file(),ref)
        self.assertTrue((BASE/'fonts/OpenDyslexic-Regular.otf').is_file())
        self.assertTrue((BASE/'fonts/OpenDyslexic-Bold.otf').is_file())
        for n in ('QA_ARTICOLO.json','QA_SUPPORTI.json','QA_BOX.json','QA_FONTI.json','QA_FLUSSO.json','QA_FINALE.pdf.json'):
            self.assertTrue(json.loads((BASE/n).read_text(encoding='utf-8'))['passed'],n)

if __name__=='__main__':unittest.main()

