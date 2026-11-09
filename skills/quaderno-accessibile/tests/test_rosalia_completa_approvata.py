"""Test della baseline Rosalía completa approvata; non genera né modifica PDF.

La struttura non certifica PDF/UA, attendibilità delle fonti o qualità semantica.
Esecuzione: python3 -m unittest discover -s tests -p 'test_rosalia_completa_approvata.py' -v
"""
from pathlib import Path
import hashlib
import json
import unittest

import pymupdf as fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'templates' / 'rosalia-completa-approvata-2026-11-04'
EXPECTED_HASH = '9e9262ba9c7fd1f49cbebf4639414d7afa6420324afe57139ad99f04aedf7552'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RosalíaCompletaApprovataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = BeautifulSoup((T / 'modello.html').read_text(encoding='utf-8'), 'html.parser')
        cls.before = BeautifulSoup((T / 'versione_precedente.html').read_text(encoding='utf-8'), 'html.parser')
        cls.pdf = fitz.open(T / 'ROSALIA_COMPLETA_APPROVATA.pdf')
        cls.qa = json.loads((T / 'qa' / 'QA_REVISIONE_STORICA.json').read_text(encoding='utf-8'))
        cls.qa_vita_opere = json.loads((T / 'qa' / 'QA_VERIFICA_VITA_OPERE.json').read_text(encoding='utf-8'))
        cls.qa_current = json.loads((T / 'qa' / 'QA_VERIFICA_MEDIA.json').read_text(encoding='utf-8'))

    @classmethod
    def tearDownClass(cls):
        cls.pdf.close()

    def test_hash_pagine_e_report(self):
        self.assertEqual(sha(T / 'ROSALIA_COMPLETA_APPROVATA.pdf'), EXPECTED_HASH)
        self.assertEqual(len(self.pdf), 28)
        self.assertTrue(self.qa['passed'], self.qa['errors'])
        self.assertEqual(self.qa_current['final_sha256'], EXPECTED_HASH)
        self.assertTrue(self.qa_current['passed'], self.qa_current['errors'])
        self.assertEqual(self.soup.html.get('lang'), 'es')

    def test_catena_report_edizione_definitiva(self):
        maps=json.loads((T/'qa'/'QA_MAPPE_INSIEME.json').read_text(encoding='utf-8'))
        final_map=json.loads((T/'qa'/'QA_MAPPA_FINALE.json').read_text(encoding='utf-8'))
        for report in (self.qa,maps,final_map,self.qa_vita_opere,self.qa_current):
            self.assertTrue(report['passed'])
        self.assertEqual(self.qa['new_pdf_sha256'],maps['checks']['sha256_baseline'])
        self.assertEqual(maps['checks']['sha256_risultato'],final_map['baseline_sha256'])
        self.assertEqual(final_map['final_sha256'],self.qa_vita_opere['baseline_sha256'])
        self.assertEqual(self.qa_vita_opere['final_sha256'],self.qa_current['baseline_sha256'])
        self.assertEqual(self.qa_current['final_sha256'],EXPECTED_HASH)

    def test_risorse_relative_presenti(self):
        for image in self.soup.select('img[src]'):
            resource = (T / image['src']).resolve()
            self.assertTrue(resource.is_relative_to(T), image['src'])
            self.assertTrue(resource.is_file(), image['src'])
        for font in ('OpenDyslexic-Regular.otf', 'OpenDyslexic-Bold.otf'):
            self.assertTrue((T / 'media' / font).is_file())

    def test_sintesi_solo_documentazione(self):
        for n in range(1,10):
            section = self.soup.select_one(f'#sec{n}')
            self.assertIsNotNone(section)
            summaries = section.select('.recap[data-new="summary"]')
            self.assertEqual(len(summaries), 1 if n <= 5 else 0, f'sezione {n}')
            for recap in summaries:
                self.assertEqual(recap.select_one('.summary-title').get_text(strip=True), 'EN RESUMEN')
                self.assertFalse(recap.select('b,strong'))
                self.assertEqual(len(recap.select('table')), 1)
                for row in recap.select('tr'):
                    self.assertEqual(len(row.find_all(['td','th'],recursive=False)), 2)
        self.assertIn('font-weight:400', (T / 'modello.html').read_text(encoding='utf-8'))

    def test_conservazione_corpo_meno_le_sole_eliminazioni_approvate(self):
        for n in range(1,10):
            old = BeautifulSoup(str(self.before.select_one(f'#sec{n}')), 'html.parser').select_one(f'#sec{n}')
            new = BeautifulSoup(str(self.soup.select_one(f'#sec{n}')), 'html.parser').select_one(f'#sec{n}')
            for el in new.select('sup.ref-note'):
                el.decompose()
            if n >= 6:
                for el in old.select('.recap[data-new="summary"]'):
                    el.decompose()
            if n in (5,6):
                prefix = 'Texto principalmente reelaborado a partir de:' if n == 5 else 'Texto extraído de: Rosalía de Castro.'
                found = [p for p in old.select('p') if p.get_text(' ',strip=True).startswith(prefix)]
                self.assertEqual(len(found),1)
                found[0].find_parent('div',class_='blk').decompose()
            if n == 7:
                # L'unica modifica nel corpo è l'interruzione autorizzata prima delle due mappe.
                heading = new.select_one('h3.subheading')
                self.assertEqual(heading.get('style'),'break-before:page;page-break-before:always')
                del heading['style']
            self.assertEqual(str(old),str(new),f'sezione {n}')
        self.assertEqual(len(self.soup.select('.map-original')),2)
        self.assertEqual(len(self.soup.select('.qr')),1)
        self.assertEqual(len(self.soup.select('#sec9 .checklist-line')),5)

    def test_indice_pagine_e_link(self):
        rows = self.soup.select('#indice .index-row')
        expected = self.qa['checks']['index']
        self.assertEqual(len(rows),12)
        self.assertEqual(len(expected),12)
        links = self.pdf[0].get_links()
        for row, rec in zip(rows,expected):
            label = row.select_one('.index-label').get_text(' ',strip=True)
            self.assertEqual(label,rec['title'])
            self.assertEqual(int(row.select_one('.index-pg').get_text(strip=True)),rec['page'])
            hits = self.pdf[0].search_for(label)
            self.assertTrue(hits,label)
            self.assertTrue(any(link.get('page') == rec['page']-1 and
                                any(link['from'].intersects(rect) for rect in hits)
                                for link in links),label)

    def test_domande_e_chiave(self):
        questions = self.soup.select('#verifica .question')
        self.assertEqual(len(questions),10)
        for n,question in enumerate(questions,1):
            self.assertEqual(question.get('data-question'),str(n))
            self.assertEqual(len(question.select('table.choices td')),4)
        key = json.loads((T / 'qa' / 'chiave-interna-quiz.json').read_text(encoding='utf-8'))
        self.assertEqual(key['numero_domande'],10)
        self.assertEqual(key['risposte_corrette'],['A','B','C','D','A','B','C','D','A','B'])
        self.assertEqual(len(key['domande_e_riscontri']),10)
        for i, (q, item) in enumerate(zip(questions,key['domande_e_riscontri']),1):
            text=q.select_one('.question-text').get_text(strip=True)
            self.assertEqual(text, f'{i}. {item["q"]}')
            self.assertNotRegex(text.lower(),r'actividad|ejercicio|aplicación|tableta|mapa')
            options=[td.get_text(' ',strip=True)[3:] for td in q.select('table.choices td')]
            self.assertEqual(options,item['a'])
            self.assertEqual(item['correct'],key['risposte_corrette'][i-1])
            self.assertTrue(item['source_pages'])
            self.assertTrue(all(2<=page<=12 for page in item['source_pages']))
            self.assertTrue(item['evidence'].strip())
            pdf_text=' '.join(self.pdf[24 if i<=5 else 25].get_text().split())
            self.assertIn(' '.join(f'{i}. {item["q"]}'.split()),pdf_text)
            for option in item['a']:
                self.assertIn(' '.join(option.split()),pdf_text)

    def test_riscontri_delle_risposte_nel_corpo_del_pdf(self):
        # I riscontri testuali provengono dal controllo della revisione approvata;
        # questo test non sostituisce la valutazione didattica e semantica umana.
        for n in range(1,11):
            result=self.qa_current['checks'][f'domanda_{n}_risposta_sostenuta_dal_testo']
            self.assertTrue(result['pass'])
            detail=result['detail']
            page_text=' '.join(self.pdf[detail['pagina']-1].get_text().split())
            for excerpt in detail['estratti']:
                self.assertIn(' '.join(excerpt.split()),page_text,f'domanda {n}')

    def test_mappa_e_immagini_distinte(self):
        self.assertEqual(self.soup.select_one('#mapa-final h2').get_text(strip=True),'MAPA CONCEPTUAL FINAL')
        nodes = self.soup.select('#mapa-final [data-map-node]')
        self.assertEqual(len(nodes),5)
        self.assertEqual([n.select_one('.node-title').get_text(strip=True) for n in nodes],['VIDA','OBRAS','EL SAR','LIEDERS','ESTILO'])
        self.assertEqual([n.get_text(strip=True) for n in nodes[1].select('.node-word')],['CANTARES GALLEGOS','FOLLAS NOVAS','EN LAS ORILLAS DEL SAR'])
        self.assertNotIn('ACTIVIDADES',self.pdf[26].get_text())
        self.assertIn('EN LAS ORILLAS DEL SAR',self.pdf[26].get_text())
        images = [T / node.select_one('img')['src'] for node in nodes]
        self.assertEqual(len({sha(p) for p in images}),5)
        self.assertTrue(all(node.select_one('img').get('alt') for node in nodes))
        self.assertIn('width:78mm;height:78mm',(T/'modello.html').read_text(encoding='utf-8'))

    def test_due_mappe_delle_attivita_insieme_senza_riduzione(self):
        text=self.pdf[19].get_text()
        self.assertIn('MAPA CONCEPTUAL 1 · LA VIDA DE LA ESCRITORA',text)
        self.assertIn('MAPA CONCEPTUAL 2 · EL ENSAYO LIEDERS',text)
        self.assertLess(text.index('MAPA CONCEPTUAL 1'),text.index('MAPA CONCEPTUAL 2'))
        imgs=self.pdf[19].get_image_info(hashes=True)
        m1=[i for i in imgs if (i['width'],i['height'])==(1376,768)]
        m2=[i for i in imgs if (i['width'],i['height'])==(1600,543)]
        self.assertEqual(len(m1),1);self.assertEqual(len(m2),1)
        self.assertLess(m1[0]['bbox'][3],m2[0]['bbox'][1])
        self.assertAlmostEqual((m1[0]['bbox'][2]-m1[0]['bbox'][0])*25.4/72,174,places=1)
        self.assertAlmostEqual((m2[0]['bbox'][2]-m2[0]['bbox'][0])*25.4/72,174,places=1)

    def test_note_fonti_e_link(self):
        entries = self.soup.select('#referencias .ref-entry')
        self.assertEqual([e.get('id') for e in entries],['rif-1','rif-2','rif-3','rif-4'])
        notes = self.soup.select('sup.ref-note a')
        self.assertEqual(len(notes),11)
        self.assertEqual({n['href'] for n in notes},{'#rif-1','#rif-2','#rif-3','#rif-4'})
        all_links = [link for page in self.pdf for link in page.get_links()]
        actual = [link for link in all_links if link.get('nameddest','').startswith('rif-')]
        self.assertEqual(len(actual),11)
        self.assertTrue(all(link['page']==27 and link['from'].get_area()>0 for link in actual))
        self.assertEqual(sorted(link['nameddest'] for link in actual),sorted(n['href'][1:] for n in notes))
        uri = {link['uri'] for link in all_links if link.get('uri') and link['from'].get_area()>0}
        self.assertTrue(all(a['href'] in uri for a in self.soup.select('#referencias a[href^="https:"]')))
        body = ' '.join(self.soup.select_one(f'#sec{n}').get_text(' ',strip=True) for n in range(1,10))
        for text in ('Texto principalmente reelaborado a partir de:', 'Texto extraído de: Rosalía de Castro.', 'Manual para las pruebas escritas y orales'):
            self.assertNotIn(text,body)
        self.assertIn('Mayol',entries[0].get_text(' ',strip=True))
        self.assertIn('Álbum del Miño',entries[1].get_text(' ',strip=True))

    def test_controlli_box_e_qr_gia_svolti(self):
        for report in ('qa_box.json','qa_fonti.json'):
            r = json.loads((T / 'qa' / report).read_text(encoding='utf-8'))
            self.assertTrue(r['passed'],r.get('errors'))
        qr = json.loads((T / 'qa' / 'QA_QR.json').read_text(encoding='utf-8'))
        self.assertTrue(qr['matches_original'])
        self.assertEqual(qr['pdf_codes'][0]['page'],21)


if __name__ == '__main__':
    unittest.main()

