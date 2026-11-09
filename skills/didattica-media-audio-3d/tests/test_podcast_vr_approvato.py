#!/usr/bin/env python3
"""Controllo dei file podcast approvati senza generazioni né ricodifica."""
from pathlib import Path
import hashlib,importlib.util,json,re,shutil,subprocess,unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'templates/realta-virtuale-podcast-approvato-2026-11-05'
PDF=BASE/'REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.pdf'
VIDEO=BASE/'PODCAST_REALTA_VIRTUALE_A_SCUOLA.mp4'
MANIFEST=BASE/'manifest.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

class TestPodcastVRApprovato(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=json.loads(MANIFEST.read_text(encoding='utf-8'))

    def test_pdf_e_video_identici(self):
        self.assertEqual(sha(PDF),'5dcc0e4b22acb02941ae3fae3a9cb6f7ad1e672fb829907a5c04d435e2720e76')
        self.assertEqual(sha(VIDEO),'9287cc59bd0e6dab9bf49fcf627d2f1a1408ac7a6753ea61efcea4d7357ea5e7')
        self.assertEqual(self.m['source_sha256'],sha(PDF));self.assertEqual(self.m['approved_video_sha256'],sha(VIDEO))
        self.assertTrue(self.m['approved']);self.assertEqual(self.m['approved_date'],'2026-11-05')

    def test_manifest_nove_clip_alternate_e_impronte(self):
        parts=self.m['parts'];self.assertEqual(len(parts),9)
        self.assertEqual([p['gender'] for p in parts],['female','male','female','male','female','male','female','male','female'])
        self.assertEqual(self.m['speed'],1.12)
        for p in parts:
            self.assertEqual(p['speed'],1.12)
            self.assertEqual(sha(BASE/p['clip_path']),p['expected_clip_sha256'])
            self.assertNotIn('source_url',p);self.assertNotIn('normalized_path',p)
        pages={j for p in parts for j in range(p['pages'][0],p['pages'][1]+1)}
        self.assertEqual(pages,set(range(1,18)))
        spec=importlib.util.spec_from_file_location('assemblatore',ROOT/'scripts/assembla_audio_pdf.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.assertEqual(module.validate(self.m,BASE),PDF.resolve())

    def test_quiz_mappa_fonti_e_testo_indice(self):
        text=self.m['parts'][6]['text_fedele']
        self.assertEqual(len(re.findall(r'(?i)\bDomanda\s+\d+\.',text)),10)
        for letter in 'ABCD':self.assertEqual(len(re.findall(r'(?i)\bOpzione\s+'+letter+r'\.',text)),10)
        self.assertIn('MAPPA CONCETTUALE FINALE',self.m['parts'][7]['text_fedele'])
        self.assertIn('RIFERIMENTI BIBLIOGRAFICI',self.m['parts'][8]['text_fedele'])
        self.assertIn('ANDREA CENTINARO',self.m['parts'][8]['text_fedele'])
        index=(BASE/'PODCAST_TESTO_E_INDICE.md').read_text(encoding='utf-8')
        self.assertIn('16:44',index);self.assertIn('00:00',index);self.assertIn('10.',index)
        self.assertTrue((BASE/'COPERTINA_PODCAST_ORIGINALE.png').is_file())

    @unittest.skipUnless(shutil.which('ffprobe'),'ffprobe non installato')
    def test_mp4_codec_e_durata(self):
        proc=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(VIDEO)],capture_output=True,text=True,check=True)
        info=json.loads(proc.stdout);streams=info['streams']
        video=[s for s in streams if s['codec_type']=='video'];audio=[s for s in streams if s['codec_type']=='audio']
        self.assertEqual(len(video),1);self.assertEqual(len(audio),1)
        self.assertEqual(video[0]['codec_name'],'h264');self.assertEqual(audio[0]['codec_name'],'aac')
        self.assertEqual((video[0]['width'],video[0]['height']),(1280,720))
        self.assertAlmostEqual(float(info['format']['duration']),1004.385,delta=0.5)
        self.assertEqual(len(info.get('chapters',[])),9)

if __name__=='__main__':unittest.main()

