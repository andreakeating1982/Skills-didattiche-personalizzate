from pathlib import Path
import importlib.util,json,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('gestisci',ROOT/'tools/gestisci_skill.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
class RepositoryTests(unittest.TestCase):
 def test_catalogo_completo(self):
  rows=mod.catalogo();self.assertEqual(len(rows),55);self.assertEqual(len({r['name'] for r in rows}),55)
  self.assertTrue(all((ROOT/r['entrypoint']).is_file() for r in rows))
 def test_ricerca_in_italiano(self):
  rows=mod.cerca('quaderno accessibile');self.assertIn('quaderno-accessibile',[r['name'] for r in rows[:5]])
 def test_verifica_statica(self):
  r=mod.validate();self.assertTrue(r['passed'],r['errors'])
 def test_preparazione_senza_esecuzione(self):
  with tempfile.TemporaryDirectory() as t:
   t=Path(t);dest=t/'copia';work=t/'lavoro';m=t/'mappa.json';project=t/'progetto-quiz';m.write_text(json.dumps({'/home/user/shakespeare-quiz':str(project)}));r=mod.prepara(dest,work,m)
   self.assertEqual(r['skills'],55);self.assertTrue((dest/'PREPARAZIONE.json').is_file());self.assertFalse(work.exists());self.assertFalse(project.exists())
   skill=(dest/'skills/quaderno-accessibile/SKILL.md').read_text();self.assertNotIn('/home/user/skills',skill);self.assertIn(str(work),skill)
   validator=(dest/'skills/skill-creator/scripts/quick_validate.py').read_text();self.assertIn(str(dest/'skills'),validator);self.assertNotIn('/home/user/skills',validator)
   quiz=(dest/'skills/shakespeare-quiz/SKILL.md').read_text();self.assertIn(str(project),quiz)
   for p in (dest/'skills').glob('*/SKILL.md'):
    self.assertNotIn('/home/user/',p.read_text())
   with self.assertRaises(ValueError):mod.prepara(dest,work)
 def test_nessuna_sovrascrittura_repository(self):
  with self.assertRaises(ValueError):mod.prepara(ROOT/'runtime-non-creare',ROOT/'work-non-creare')
  self.assertFalse((ROOT/'runtime-non-creare').exists())
 def test_asset_binari_invariati_nella_preparazione(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t)/'copia';mod.prepara(d,Path(t)/'work')
   for original in (ROOT/'skills/quaderno-accessibile/templates/clay-adulto').glob('*.png'):
    self.assertEqual(mod.sha(original),mod.sha(d/original.relative_to(ROOT)))
if __name__=='__main__':unittest.main()

