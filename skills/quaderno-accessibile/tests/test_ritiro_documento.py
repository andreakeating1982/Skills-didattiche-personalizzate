from pathlib import Path
import json,re,unittest
Q=Path(__file__).resolve().parents[1]
P=Q/'references'

class WithdrawalTests(unittest.TestCase):
 def test_collezione_attiva_di_otto(self):
  d=json.loads((P/'revisione-raccolta-scientifica-2026-11-02.json').read_text())
  self.assertEqual(d['active_article_codes'],['01','02','03','04','06','07','08','09'])
  self.assertEqual(d['totals']['pdfs'],8)
  self.assertNotIn('05',d['scientific_rewrites'])
  self.assertEqual(len(d['scientific_rewrites']),5)
  self.assertEqual(d['totals']['pages'],sum(r['pages'] for r in d['documents'])+d['approved_vr']['pages'])
 def test_guida_generale_non_ritirata(self):
  d=json.loads((P/'revisione-raccolta-scientifica-2026-11-02.json').read_text())
  self.assertIn('01',[r['code'] for r in d['documents']])
 def test_registri_senza_documento_ritirato(self):
  pat=re.compile(r'materia[ _-]+per[ _-]+materia',re.I)
  for name in ['raccolta-sintesi-mappe-2026-11.json','raccolta-specchietti-box-2026-11.json','revisione-raccolta-scientifica-2026-11-02.json']:
   d=json.loads((P/name).read_text());rows=d.get('records',d.get('documents',[]))
   self.assertFalse(any(pat.search(json.dumps(r,ensure_ascii=False)) for r in rows),name)
   self.assertFalse(any(r.get('code')=='05' or str(r.get('name','')).startswith('05_') for r in rows),name)
 def test_istruzione_di_esclusione_presente(self):
  policy=P/'documento-ritirato-2026-11-02.md'
  self.assertTrue(policy.is_file())
  self.assertIn('Non recuperarlo',policy.read_text())
  self.assertIn('documento-ritirato-2026-11-02.md',(Q/'SKILL.md').read_text())
 def test_nessun_documento_binario_ritirato(self):
  pat=re.compile(r'materia[ _-]+per[ _-]+materia',re.I)
  bad=[str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file() and pat.search(p.name)]
  self.assertEqual(bad,[])

if __name__=='__main__':unittest.main()

