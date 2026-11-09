"""Regressioni: niente raggruppamenti forzati, selettori personalizzabili."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('flow_blog',ROOT/'scripts/verifica_flusso_fonti_blog.py')
flow=importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)

STYLE='''<style>@page{size:210mm 240mm;margin:20mm}body{margin:0;font:14px sans-serif}
.sec{break-before:page}.blk,.lf-summary,.text-chunk{break-inside:avoid;background:#eee;margin:0 0 2mm}
.one{height:105mm}.two{height:45mm}.three{height:55mm}.summary-group{break-inside:avoid}
</style>'''

class FlowTests(unittest.TestCase):
 def create(self,root,grouped=False,old_class=False):
  cls='text-chunk' if old_class else 'blk'
  first=f'<div class="{cls} one">PRIMO</div>'
  nexts=f'<div class="{cls} two">SECONDO</div><div class="{cls} three">TERZO</div>'
  if grouped:nexts='<div class="summary-group">'+nexts+'</div>'
  f=root/'sample.html';f.write_text('<!doctype html><meta charset="utf-8">'+STYLE+'<section id="sec1" class="sec">'+first+nexts+'</section>',encoding='utf8');return f
 def test_precedente_gruppo_forzato_segnalato(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=self.create(Path(tmp),grouped=True)
   r=flow.check(f,units=['sec1'],without_sources=True,card_selector='.blk')
   self.assertFalse(r['passed'])
   self.assertTrue(any('anticipato' in e for e in r['errors']),r)
 def test_flusso_naturale_supera(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=self.create(Path(tmp))
   r=flow.check(f,units=['sec1'],without_sources=True,card_selector='.blk')
   self.assertTrue(r['passed'],r['errors'])
   self.assertEqual(r['units'][0]['boxes_by_page'],{'1':2,'2':1})
 def test_selettore_storico_funzionante(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=self.create(Path(tmp),old_class=True)
   r=flow.check(f,units=['sec1'],without_sources=True)
   self.assertTrue(r['passed'],r['errors'])
   self.assertEqual(r['units'][0]['boxes_by_page'],{'1':2,'2':1})

if __name__=='__main__':unittest.main()

