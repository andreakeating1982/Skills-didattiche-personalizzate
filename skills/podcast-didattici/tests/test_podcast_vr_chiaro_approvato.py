#!/usr/bin/env python3
"""Test offline del caso VR approvato. Non genera media e non ascolta il parlato."""
import hashlib
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
BASE = SKILL / 'templates' / 'realta-virtuale-chiara-approvata-2026-11-05'
EXPECTED = {
    'REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.pdf': '5dcc0e4b22acb02941ae3fae3a9cb6f7ad1e672fb829907a5c04d435e2720e76',
    'PODCAST_REALTA_VIRTUALE_A_SCUOLA.mp4': '9287cc59bd0e6dab9bf49fcf627d2f1a1408ac7a6753ea61efcea4d7357ea5e7',
    'manifest.json': '3d85160a5482c5a5bdf6a326c33c476e52f28ee8697a90d4d48aca0e7b465e2a',
    'COPERTINA_PODCAST_ORIGINALE.png': '4ef68730c29f9eed9344ffc307e2a683752266846d08136584099b2275a81762',
    'PODCAST_TESTO_E_INDICE.md': '11606537b070941f7de50702b716797e5309e0d69de02e47c6e885ac972bcafa',
    'QA_PODCAST_FINALE.json': '63211f5478702553a5182d88efe1178a43c4522b346dc378cf7df4b888df3800',
}


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


class PodcastVRApprovatoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((BASE / 'manifest.json').read_text(encoding='utf-8'))
        cls.parts = cls.manifest['parts']

    def test_originali_approvati_identici(self):
        for filename, digest in EXPECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(sha256(BASE / filename), digest)
        self.assertEqual(self.manifest['source_sha256'], EXPECTED[self.manifest['source_pdf']])
        self.assertEqual(self.manifest['approved_video_sha256'], EXPECTED[self.manifest['approved_video']])
        self.assertTrue(self.manifest['approved'])
        self.assertEqual(self.manifest['approved_date'], '2026-11-05')

    def test_nove_clip_portabili_e_pagine(self):
        self.assertEqual(len(self.parts), 9)
        self.assertEqual(self.manifest['speed'], 1.12)
        pages = set()
        previous_start = -1.0
        for part in self.parts:
            with self.subTest(part=part['name']):
                self.assertEqual(part['speed'], 1.12)
                self.assertNotIn('source_url', part)
                path = Path(part['clip_path'])
                self.assertFalse(path.is_absolute())
                self.assertNotIn('..', path.parts)
                self.assertEqual(sha256(BASE / path), part['expected_clip_sha256'])
                self.assertEqual(part['clip_sha256'], part['expected_clip_sha256'])
                self.assertGreater(part['start_seconds'], previous_start)
                previous_start = part['start_seconds']
                pages.update(range(part['pages'][0], part['pages'][1] + 1))
        self.assertEqual(pages, set(range(1, 18)))
        self.assertEqual([p['gender'] for p in self.parts],
                         ['female', 'male', 'female', 'male', 'female',
                          'male', 'female', 'male', 'female'])

    def test_verifica_approvata_e_fonti_presenti(self):
        verify = next(p for p in self.parts if p['name'] == '06_verifica')
        script = verify['text_fedele']
        self.assertEqual(verify['gender'], 'female')
        self.assertEqual(len(re.findall(r'(?i)\bDomanda\s+\d+\.', script)), 10)
        for letter in 'ABCD':
            self.assertEqual(len(re.findall(r'(?i)\bOpzione\s+' + letter + r'\.', script)), 10)
        final = next(p for p in self.parts if p['name'] == '08_fonti')
        self.assertEqual(final['gender'], 'female')  # eccezione del solo master approvato
        self.assertIn('RIFERIMENTI BIBLIOGRAFICI', final['text_fedele'])
        self.assertIn('ANDREA CENTINARO', final['text_fedele'])
        index = (BASE / 'PODCAST_TESTO_E_INDICE.md').read_text(encoding='utf-8')
        for marker in ('16:44', '00:00', '09:00', '11:52', '13:00'):
            self.assertIn(marker, index)

    def test_preferenze_originali_restano_e_limiti_dichiarati(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('tutta la verifica con voce femminile', text)
        self.assertIn('tutta la bibliografia con voce maschile', text)
        self.assertIn('etichette «Domanda/Risposta» non stampate', text)
        self.assertIn('senza alcuna musica', text)
        qa = json.loads((BASE / 'QA_PODCAST_FINALE.json').read_text(encoding='utf-8'))
        self.assertIn('non è stato ascoltato integralmente', qa['auditory_review'])
        self.assertEqual(qa['pdf_sha256'], self.manifest['source_sha256'])
        self.assertEqual(qa['video_sha256'], self.manifest['approved_video_sha256'])

    def test_risorse_originali_e_nuove_incluse(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        paths = set(re.findall(r'(?:references|scripts|templates|tests)/[A-Za-z0-9_.-]+', text))
        self.assertGreaterEqual(len(paths), 18)
        for name in paths:
            with self.subTest(path=name):
                self.assertTrue((SKILL / name).is_file(), name)
        self.assertTrue((SKILL / 'references' / 'caso-realta-virtuale-chiaro-approvato-2026-11-05.md').is_file())
        self.assertTrue((SKILL / 'references' / 'caso-realta-virtuale-v7.md').is_file())

    @unittest.skipUnless(shutil.which('pdfinfo'), 'pdfinfo non installato')
    def test_numero_pagine_pdf(self):
        pdf = BASE / self.manifest['source_pdf']
        result = subprocess.run(['pdfinfo', str(pdf)], text=True, capture_output=True, check=True)
        self.assertRegex(result.stdout, r'(?m)^Pages:\s+17\s*$')

    @unittest.skipUnless(shutil.which('ffprobe'), 'ffprobe non installato')
    def test_codec_dimensioni_durata_e_capitoli_video(self):
        mp4 = BASE / self.manifest['approved_video']
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                                 '-show_chapters', '-of', 'json', str(mp4)],
                                text=True, capture_output=True, check=True)
        media = json.loads(result.stdout)
        video = [s for s in media['streams'] if s['codec_type'] == 'video']
        audio = [s for s in media['streams'] if s['codec_type'] == 'audio']
        self.assertEqual(len(video), 1)
        self.assertEqual(len(audio), 1)
        self.assertEqual((video[0]['codec_name'], video[0]['width'], video[0]['height']),
                         ('h264', 1280, 720))
        self.assertEqual(audio[0]['codec_name'], 'aac')
        self.assertAlmostEqual(float(media['format']['duration']), 1004.385, delta=0.5)
        self.assertEqual(int(media['format']['size']), 14041111)
        self.assertEqual(len(media.get('chapters', [])), 9)


if __name__ == '__main__':
    unittest.main()

