from pathlib import Path
import sys,tempfile,unittest,json
from bs4 import BeautifulSoup
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
if not SCRIPTS.exists():SCRIPTS=Path(__file__).resolve().parent
sys.path.insert(0,str(SCRIPTS))
from integra_sintesi_mappe import apply
from verifica_specchietti_box import check
class SpecchiettiTests(unittest.TestCase):
 def fixture(self):
  html='<html><head><style>body{font-size:13pt;line-height:1.85}section{break-before:page}</style></head><body><section id="u"><h2>UNITÀ</h2><p>Testo originale <strong>con enfasi</strong> da conservare.</p></section><section id="fonti"><h2>FONTI</h2><p>Riferimenti originali da conservare.</p></section></body></html>'
  cfg={'unit_ids':['u'],'final_map_ids':['mappa'],'body_font_size_px':17.333333333333332,'body_line_height':1.85,'summaries':[{'id':'u','color':'#257041','rows':[[f'IDEA {i}','Una spiegazione esplicita della relativa idea, non limitata a una singola frase generica.'] for i in range(7)]}],'maps':[{'id':'mappa','root':'TEMA','groups':[{'title':'UN GRUPPO','nodes':[['PRIMO BOX',['ORGANIZZAZIONE','MATERIALI']],['SECONDO BOX',['CONTROLLO','RIPASSO']]]}]}]}
  asset=SCRIPTS.parent/'templates/clay-adulto/pianificazione.png'
  if not asset.exists():asset=Path('/home/user/skills/quaderno-accessibile/templates/clay-adulto/pianificazione.png')
  for g in cfg['maps'][0]['groups']:g['images']=[{'src':asset.as_uri(),'alt':'Insegnante adulta prepara una lezione in stile clay.'} for n in g['nodes']]
  return html,cfg
 def validate(self,html,cfg):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'doc.html';p.write_text(html);return check(p,cfg)
 def test_schema_sette_righe_non_limitate(self):
  h,c=self.fixture();x,r=apply(h,c);v=self.validate(x,c);self.assertTrue(v['passed'],v['errors']);self.assertEqual(v['summary_rows'],7);self.assertIn('MAPPA CONCETTUALE FINALE',x)
 def test_interlinea_ridotta_rifiutata(self):
  h,c=self.fixture();x,r=apply(h,c);x=x.replace('line-height:var(--body-leading)!important','line-height:1.4!important');v=self.validate(x,c);self.assertFalse(v['passed']);self.assertIn('support_line_height_not_body',[x['issue'] for x in v['errors']])
 def test_titolo_mappa_non_standard_rifiutato(self):
  h,c=self.fixture();x,r=apply(h,c);x=x.replace('MAPPA CONCETTUALE FINALE','LA MAPPA IN BREVE');v=self.validate(x,c);self.assertFalse(v['passed']);self.assertIn('map_title_not_standard',[x['issue'] for x in v['errors']])
 def test_contenuto_originale_e_idempotenza(self):
  h,c=self.fixture();x,r=apply(h,c);again,r=apply(x,c);self.assertEqual(x,again);s=BeautifulSoup(x,'html.parser');s.select_one('.lf-summary').decompose();s.select_one('.lf-simple-map').decompose();o=BeautifulSoup(h,'html.parser');self.assertEqual(s.body.get_text(),o.body.get_text());self.assertEqual([str(x) for x in s.select('strong')],[str(x) for x in o.select('strong')])
 def test_paragrafo_non_accettato_al_posto_della_tabella(self):
  h,c=self.fixture();x,r=apply(h,c);s=BeautifulSoup(x,'html.parser');s.select_one('.lf-summary-table').decompose();v=self.validate(str(s),c);self.assertFalse(v['passed']);self.assertIn('summary_not_two_column_table',[x['issue'] for x in v['errors']])
 def test_frecce_grafiche_rifiutate(self):
  h,c=self.fixture();x,r=apply(h,c);x=x.replace('PRIMO BOX','↓ PRIMO BOX');v=self.validate(x,c);self.assertFalse(v['passed']);self.assertIn('graphical_connector_in_map',[x['issue'] for x in v['errors']])
 def test_righe_esplicite_obbligatorie(self):
  h,c=self.fixture();c['summaries'][0]={'id':'u','color':'#257041','text':'Paragrafo compresso.'}
  with self.assertRaises(ValueError):apply(h,c)
 def test_immagine_mancante_rifiutata(self):
  h,c=self.fixture();x,r=apply(h,c);s=BeautifulSoup(x,'html.parser');s.select_one('.lf-map-image').decompose();v=self.validate(str(s),c);self.assertFalse(v['passed']);self.assertIn('map_box_image_missing_or_no_alt',[x['issue'] for x in v['errors']])
 def test_sintesi_tutte_regular_compresi_titoli_e_chiavi(self):
  h,c=self.fixture();x,_=apply(h,c);v=self.validate(x,c);self.assertTrue(v['passed'],v['errors']);self.assertEqual(v['summary_font_weights'],[400])
 def test_markup_bold_nella_sintesi_rimosso_non_nel_corpo(self):
  h,c=self.fixture();c['summaries'][0]['rows'][0][1]='Testo <strong>chiave</strong> e <b>nota</b>.';x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');self.assertFalse(s.select('.lf-summary strong,.lf-summary b'));self.assertEqual(s.select_one('section#u > p strong').text,'con enfasi');v=self.validate(x,c);self.assertTrue(v['passed'],v['errors'])
 def test_css_bold_ereditato_da_th_rifiutato(self):
  h,c=self.fixture();x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');s.select_one('.lf-summary tbody th')['style']='font-weight:700!important';v=self.validate(str(s),c);self.assertIn('summary_font_not_regular_400',[e['issue'] for e in v['errors']])
 def test_titolo_sintesi_bold_rifiutato(self):
  h,c=self.fixture();x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');s.select_one('.lf-summary h4')['style']='font-weight:700!important';v=self.validate(str(s),c);self.assertIn('summary_font_not_regular_400',[e['issue'] for e in v['errors']])
 def test_cella_sintesi_bold_inline_rifiutata(self):
  h,c=self.fixture();x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');cell=s.select_one('.lf-summary tbody td');cell['style']='font-weight:700!important';v=self.validate(str(s),c);self.assertIn('summary_font_not_regular_400',[e['issue'] for e in v['errors']])
 def test_bold_markup_reintrodotto_rifiutato(self):
  h,c=self.fixture();x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');cell=s.select_one('.lf-summary tbody td');strong=s.new_tag('strong');strong.string='Errore';cell.append(strong);v=self.validate(str(s),c);self.assertIn('summary_bold_markup',[e['issue'] for e in v['errors']])
 def test_nodi_dispari_sempre_stessa_misura(self):
  h,c=self.fixture();g=c['maps'][0]['groups'][0];g['nodes'].append(['TERZO BOX',['AIUTO','STRATEGIE']]);g['images'].append(g['images'][0].copy());x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');self.assertFalse(s.select('#mappa [colspan]'));self.assertEqual(len(s.select('.lf-map-row:last-child .lf-map-card')),1);v=self.validate(x,c);self.assertTrue(v['passed'],v['errors']);self.assertEqual(len(v['map_geometry']),3)
  for d in v['map_geometry'].values():self.assertAlmostEqual(d['width_mm'],78,places=3);self.assertAlmostEqual(d['height_mm'],78,places=3)
 def test_box_troppo_largo_rifiutato(self):
  h,c=self.fixture();x,_=apply(h,c);x=x.replace('78mm','160mm');v=self.validate(x,c);self.assertIn('map_box_not_standard_78mm_square',[e['issue'] for e in v['errors']])
 def test_immagini_piccole_rifiutate(self):
  h,c=self.fixture();x,_=apply(h,c);x=x.replace('width:52mm','width:37mm');v=self.validate(x,c);self.assertIn('map_image_not_standard_52mm',[e['issue'] for e in v['errors']])
 def test_frasi_al_posto_di_parole_chiave_rifiutate(self):
  h,c=self.fixture();c['maps'][0]['groups'][0]['nodes'][0][1]='Capisco che cosa devo imparare e preparo il necessario.'
  with self.assertRaisesRegex(ValueError,'PAROLE CHIAVE'):apply(h,c)
 def test_descrizione_discorsiva_reintrodotta_rifiutata(self):
  h,c=self.fixture();x,_=apply(h,c);s=BeautifulSoup(x,'html.parser');s.select_one('.lf-map-keywords span').string='Questa frase descrive tutto il concetto.';v=self.validate(str(s),c);self.assertIn('map_sentence_or_too_many_words',[e['issue'] for e in v['errors']])
 def test_tre_opere_con_titolo_integrale_ammessi_e_leggibili(self):
  h,c=self.fixture();c['body_font_size_px']=18.666666666666668;c['maps'][0]['groups'][0]['nodes'][0]=['OBRAS',['CANTARES GALLEGOS','FOLLAS NOVAS','EN LAS ORILLAS DEL SAR']];font=SCRIPTS.parent/'templates/rosalia-completa-approvata-2026-11-04/media/OpenDyslexic-Regular.otf';h=h.replace('<style>',f'<style>@font-face{{font-family:OpenDyslexic;src:url("{font.as_uri()}")}}');x,_=apply(h,c);v=self.validate(x,c);self.assertTrue(v['passed'],v['errors']);self.assertIn('EN LAS ORILLAS DEL SAR',x)
 def test_troppe_espressioni_non_tagliate_ma_segnalate(self):
  h,c=self.fixture();c['maps'][0]['groups'][0]['nodes'][0]=['OBRAS',['UNO','DUE','TRE','QUATTRO','CINQUE']];x,_=apply(h,c);v=self.validate(x,c);self.assertIn('map_content_outside_box',[e['issue'] for e in v['errors']]);self.assertIn('CINQUE',x)
 def test_nodo_pieno_di_testo_non_allarga_il_box(self):
  h,c=self.fixture();c['maps'][0]['groups'][0]['nodes'][0][1]=['PAROLACH IAVEMOLTOLUNGA SENZASPAZIO','RIPASSO'];x,_=apply(h,c);v=self.validate(x,c);self.assertIn('map_content_outside_box',[e['issue'] for e in v['errors']])
if __name__=='__main__':unittest.main()

