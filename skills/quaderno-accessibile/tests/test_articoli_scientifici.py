from pathlib import Path
from copy import deepcopy
import sys,json,unittest
from bs4 import BeautifulSoup
Q=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Q/'scripts'))
from verifica_articolo_scientifico import check
class ScientificArticleTests(unittest.TestCase):
 def fixture(self):return json.loads((Q/'templates/articolo-scientifico-quiz/esempio-realta-virtuale.json').read_text())
 def issues(self,d,h=None):return [e['issue'] for e in check(d,h)['errors']]
 def html(self,d):
  s=BeautifulSoup('<html><head><meta name="author" content="ANDREA CENTINARO"/></head><body><section id="verifica"></section><section class="lf-simple-map"></section><section id="bibliografia"><h2>RIFERIMENTI BIBLIOGRAFICI</h2><p>Articolo scritto da ANDREA CENTINARO.</p></section></body></html>','html.parser')
  for q in d['quiz']['questions']:
   a=s.new_tag('article',id=q['id'],attrs={'class':'quiz-card'});t=s.new_tag('table',attrs={'class':'quiz-options'})
   for letter,text in zip('ABCD',q['options']):
    td=s.new_tag('td');b=s.new_tag('span',attrs={'class':'option-letter'});b.string=letter+')';td.append(b);td.append(s.new_string(text));t.append(td)
   a.append(t);s.select_one('#verifica').append(a)
  return str(s)
 def test_manifest_reale_valido(self):
  d=self.fixture();self.assertTrue(check(d)['passed'])
 def test_html_valido(self):
  d=self.fixture();self.assertTrue(check(d,self.html(d))['passed'])
 def test_minimo_5_e_massimo_10_ammessi(self):
  for n in [5,10]:
   d=self.fixture();qs=d['quiz']['questions']
   if n==5:
    d['quiz']['questions']=qs[:5];d['quiz']['questions'][-1]['section_ids'].append('sec5')
   else:
    for i in range(8,10):q=deepcopy(qs[0]);q['id']='q'+str(i+1);qs.append(q)
   self.assertTrue(check(d)['passed'],check(d))
 def test_4_o_11_domande_rifiutate(self):
  for n in [4,11]:
   d=self.fixture();qs=d['quiz']['questions']
   if n==4:d['quiz']['questions']=qs[:4]
   else:
    for i in range(8,11):q=deepcopy(qs[0]);q['id']='q'+str(i+1);qs.append(q)
   self.assertIn('quiz_count_not_5_to_10',self.issues(d))
 def test_tre_o_cinque_opzioni_rifiutate(self):
  for n in [3,5]:
   d=self.fixture();opts=d['quiz']['questions'][0]['options'];d['quiz']['questions'][0]['options']=opts[:n] if n==3 else opts+['Un’altra opzione'];self.assertIn('question_not_four_distinct_options',self.issues(d))
 def test_risposte_multiple_o_assenti_rifiutate(self):
  for answer in ['AC',None]:
   d=self.fixture();d['quiz']['questions'][0]['correct']=answer;self.assertIn('question_missing_single_answer_key',self.issues(d))
 def test_copertura_incompleta_rifiutata(self):
  d=self.fixture()
  for q in d['quiz']['questions']:q['section_ids']=['sec1']
  self.assertIn('quiz_not_covering_whole_article',self.issues(d))
 def test_rimando_video_blog_rifiutato(self):
  d=self.fixture();d['sections'][0]['blocks'].append('Come mostrato nel video di questo post.');self.assertIn('blog_video_self_reference',self.issues(d))
 def test_citazione_senza_riferimento_rifiutata(self):
  d=self.fixture();d['sections'][0]['blocks'].append('Un’affermazione [9].');self.assertIn('citation_without_reference',self.issues(d))
 def test_autore_errato_rifiutato(self):
  d=self.fixture();d['author']='Altro autore';self.assertIn('wrong_author',self.issues(d))
 def test_etichetta_fonte_rifiutata(self):
  d=self.fixture();h=self.html(d).replace('RIFERIMENTI BIBLIOGRAFICI','FONTE');self.assertIn('forbidden_fonte_label',self.issues(d,h))
 def test_ordine_quiz_mappa_invertito_rifiutato(self):
  d=self.fixture();s=BeautifulSoup(self.html(d),'html.parser');s.body.insert(0,s.select_one('.lf-simple-map').extract());self.assertIn('wrong_quiz_map_bibliography_order',self.issues(d,str(s)))
 def test_soluzioni_visibili_non_richieste_rifiutate(self):
  d=self.fixture();h=self.html(d).replace('</body>','<section id="soluzioni">1C</section></body>');self.assertIn('answer_key_visible_without_request',self.issues(d,h))
 def test_firma_finale_assente_rifiutata(self):
  d=self.fixture();h=self.html(d).replace('Articolo scritto da ANDREA CENTINARO.','');self.assertIn('missing_final_signature',self.issues(d,h))
if __name__=='__main__':unittest.main()

