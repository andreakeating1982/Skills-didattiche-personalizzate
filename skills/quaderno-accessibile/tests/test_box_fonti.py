from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from verifica_box_fonti import check


class BibliographyBoxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'fonti.html'

    def tearDown(self):
        self.temp.cleanup()

    def html(self, entries=None, extra_css='', intro=''):
        if entries is None:
            entries = '''<div id="r1" class="ref-entry"><div class="blk" id="b1">
              <p>Autore. Titolo. <a href="https://example.org">Fonte</a></p></div></div>
              <div class="scene-entry"><div class="blk" id="b2"><p>Atto 1, scena 1.</p></div>
              <div class="blk" id="b3"><p>Atto 2, scena 2.</p></div></div>'''
        return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
        @page {{size:A4; margin:18mm}} .blk {{background:#fffaf0; padding:6px;
        border:1px solid #ddd; break-inside:avoid}} {extra_css}
        </style></head><body><section id="bibliografia"><h2>RIFERIMENTI BIBLIOGRAFICI</h2>
        {intro} {entries}</section></body></html>'''

    def run_check(self, html=None, **kwargs):
        before = html if html is not None else self.html()
        self.path.write_text(before, encoding='utf-8')
        result = check(self.path, **kwargs)
        self.assertEqual(self.path.read_text(encoding='utf-8'), before,
                         'Il controllo non deve modificare il sorgente')
        return result

    def test_fonti_in_box_crema_e_scene_suddivise(self):
        result = self.run_check()
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['entries'], 2)
        self.assertEqual(len(result['cards']), 3)
        self.assertEqual(result['max_lines_observed'], 1)
        self.assertTrue(all(p['cream'] for c in result['cards'] for p in c['fragments']))

    def test_testo_o_link_fuori_box_rifiutato(self):
        entries = '''<div class="ref-entry"><div class="blk"><p>Autore.</p></div>
          <a href="https://example.org">URL fuori dal riquadro</a></div>'''
        result = self.run_check(self.html(entries))
        self.assertFalse(result['passed'])
        self.assertIn('contenuto_fuori_box', [e['issue'] for e in result['errors']])

    def test_sfondo_bianco_rifiutato(self):
        result = self.run_check(self.html(extra_css='.blk { background: white }'))
        self.assertFalse(result['passed'])
        self.assertIn('sfondo_non_conforme', [e['issue'] for e in result['errors']])

    def test_sfondo_trasparente_rifiutato(self):
        result = self.run_check(self.html(extra_css='.blk { background: transparent }'))
        self.assertFalse(result['passed'])
        self.assertIn('sfondo_non_conforme', [e['issue'] for e in result['errors']])

    def test_oltre_cinque_righe_rifiutato(self):
        entries = '<div class="ref-entry"><div class="blk"><p>1<br>2<br>3<br>4<br>5<br>6</p></div></div>'
        result = self.run_check(self.html(entries))
        self.assertFalse(result['passed'])
        self.assertIn('oltre_limite_righe', [e['issue'] for e in result['errors']])

    def test_box_nascosto_rifiutato(self):
        result = self.run_check(self.html(extra_css='#b1 {display:none}'))
        self.assertFalse(result['passed'])
        self.assertIn('box_non_renderizzato', [e['issue'] for e in result['errors']])

    def test_senza_sezione_bibliografia_rifiutato(self):
        result = self.run_check('<html><body>Solo testo</body></html>')
        self.assertFalse(result['passed'])
        self.assertEqual(result['errors'][0]['issue'], 'bibliografia_non_trovata')

    def test_senza_voci_marcate_rifiutato(self):
        result = self.run_check(self.html('<p>Un testo non classificato.</p>'))
        self.assertFalse(result['passed'])
        self.assertIn('voci_bibliografiche_non_identificate', [e['issue'] for e in result['errors']])

    def test_paragrafo_non_classificato_segnalato(self):
        result = self.run_check(self.html(intro='<p>Nota da controllare manualmente.</p>'))
        self.assertTrue(result['passed'])
        self.assertIn('paragrafo_non_classificato', [w['issue'] for w in result['warnings']])

    def test_dati_e_selettori_personalizzati(self):
        entries = '<article class="voce"><div class="riquadro"><p>Autore e titolo.</p></div></article>'
        html = self.html(entries, extra_css='.riquadro {background:#fffaf0;padding:5px}')
        result = self.run_check(html, entry_selector='.voce', card_selector='.riquadro')
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(len(result['cards']), 1)

    def test_colore_alternativo_esplicito(self):
        result = self.run_check(self.html(extra_css='.blk {background:#fff3cc}'), color='#fff3cc')
        self.assertTrue(result['passed'], result['errors'])

    def test_limiti_e_colore_non_validi(self):
        self.path.write_text(self.html(), encoding='utf-8')
        with self.assertRaises(ValueError):
            check(self.path, color='yellowish')
        with self.assertRaises(ValueError):
            check(self.path, max_lines=0)


if __name__ == '__main__':
    unittest.main()

