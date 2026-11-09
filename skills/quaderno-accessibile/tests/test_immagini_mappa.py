from pathlib import Path
import base64
import hashlib
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from verifica_immagini_mappa import check


class MapImageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'a.png').write_bytes(b'asset-one')
        (self.root / 'b.png').write_bytes(b'asset-two')
        (self.root / 'a-copy.png').write_bytes(b'asset-one')

    def tearDown(self):
        self.temp.cleanup()

    def card(self, cid, src, alt='Descrizione utile', title='IDEA'):
        return f'<div id="{cid}" class="lf-map-card"><h4>{title}</h4><img src="{src}" alt="{alt}"></div>'

    def document(self, cards, map_id='mappa'):
        p = self.root / 'test.html'
        p.write_text(f'<html><body><section class="lf-simple-map" id="{map_id}">{cards}</section></body></html>', encoding='utf-8')
        return p

    def test_scene_distinte_senza_avviso(self):
        h = self.document(self.card('a', 'a.png') + self.card('b', 'b.png'))
        result = check(h, require_distinct=True)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['unique_local_or_data_images'], 2)
        self.assertEqual(result['duplicates'], [])

    def test_duplicato_in_file_diverso_segnalato_non_bloccato(self):
        h = self.document(self.card('a', 'a.png', title='STORIA') + self.card('b', 'a-copy.png', title='TEATRO'))
        result = check(h)
        self.assertTrue(result['passed'])
        self.assertEqual(result['duplicates'][0]['nodes'], ['a', 'b'])
        self.assertEqual(result['warnings'][0]['issue'], 'immagine_ripetuta_valutare_pertinenza')

    def test_unicita_stretta_solo_se_richiesta(self):
        h = self.document(self.card('a', 'a.png') + self.card('b', 'a.png'))
        result = check(h, require_distinct=True)
        self.assertFalse(result['passed'])
        self.assertEqual(result['errors'][0]['issue'], 'immagine_ripetuta_valutare_pertinenza')

    def test_stessa_scena_in_due_mappe_non_e_duplicato_interno(self):
        p = self.root / 'due-mappe.html'
        p.write_text('<section id="m1" class="lf-simple-map">' + self.card('a', 'a.png') + '</section>'
                     '<section id="m2" class="lf-simple-map">' + self.card('b', 'a.png') + '</section>')
        result = check(p, require_distinct=True)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['maps'], 2)
        self.assertEqual(result['duplicates'], [])

    def test_alt_e_file_mancanti_rilevati(self):
        h = self.document(self.card('a', 'inesistente.png', alt=''))
        result = check(h)
        self.assertFalse(result['passed'])
        self.assertEqual({e['issue'] for e in result['errors']}, {'alt_mancante', 'file_immagine_mancante'})

    def test_immagini_remote_non_scaricate_ne_certificabili(self):
        h = self.document(self.card('a', 'https://example.invalid/test.png'))
        result = check(h)
        self.assertTrue(result['passed'])
        self.assertEqual(result['warnings'][0]['issue'], 'immagine_remota_non_scaricata')
        self.assertFalse(check(h, require_distinct=True)['passed'])

    def test_data_uri_senza_rete(self):
        encoded = base64.b64encode(b'hello').decode()
        h = self.document(self.card('a', f'data:image/png;base64,{encoded}'))
        result = check(h)
        self.assertTrue(result['passed'])
        self.assertEqual(result['nodes'][0]['sha256'], hashlib.sha256(b'hello').hexdigest())

    def test_mappa_errata_o_mancante(self):
        h = self.document(self.card('a', 'a.png'))
        self.assertFalse(check(h, map_id='inesistente')['passed'])
        self.assertTrue(check(h, map_id='mappa')['passed'])

    def test_sei_asset_shakespeare_portabili_e_hash_coerenti(self):
        template = ROOT / 'templates/shakespeare-romeo-juliet'
        manifest = json.loads((template / 'manifest.json').read_text())
        data = json.loads((template / manifest['configuration']).read_text())
        self.assertEqual(len(manifest['assets']), 6)
        self.assertEqual(len({a['sha256'] for a in manifest['assets']}), 6)
        for asset in manifest['assets']:
            self.assertEqual(hashlib.sha256((template / asset['file']).read_bytes()).hexdigest(), asset['sha256'])
        cards = ''
        for group in data['groups']:
            for node in group['nodes']:
                image = node['image']
                title = node['title'] if isinstance(node['title'], str) else ' '.join(node['title'])
                cards += self.card(str(len(cards)), (template / image['src']).as_uri(), image['alt'], title)
        result = check(self.document(cards), require_distinct=True)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['nodes_with_images'], 6)
        self.assertEqual(result['unique_local_or_data_images'], 6)


if __name__ == '__main__':
    unittest.main()

