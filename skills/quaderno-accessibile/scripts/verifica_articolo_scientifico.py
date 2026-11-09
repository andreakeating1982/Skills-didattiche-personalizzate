#!/usr/bin/env python3
"""Controlli offline per articoli scientifici inclusivi e quiz5-10/4opzioni.
Non prova correttezza scientifica o difficoltà: leggere articolo, opere e quesiti.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,json,re
SELF_REFERENCES=re.compile(r'video\s+di\s+questo|video\s+nel\s+mio\s+blog|mio\s+blog|questo\s+post|come\s+mostrato\s+nel\s+video',re.I)
def plain(t):return BeautifulSoup(t,'html.parser').get_text(' ',strip=True)
def norm(t):return re.sub(r'\s+','',t)
def check(data,html=None):
 errors=[]
 def fail(issue,**details):errors.append({'issue':issue,**details})
 sections=data.get('sections',[]);unit_ids=[u.get('id') for u in sections];ids=set(unit_ids);quiz=data.get('quiz',{});questions=quiz.get('questions',[]);coverage=set();refs=data.get('references',[]);refids={r.get('number') for r in refs}
 if not sections or len(ids)!=len(unit_ids):fail('units_missing_or_duplicate')
 if not 5<=len(questions)<=10:fail('quiz_count_not_5_to_10',actual=len(questions))
 if quiz.get('difficulty')!='media':fail('quiz_difficulty_not_medium')
 seen=set()
 for q in questions:
  qid=q.get('id');opts=q.get('options',[])
  if not qid or qid in seen:fail('question_id_missing_or_duplicate',id=qid)
  seen.add(qid)
  if len(opts)!=4 or any(not isinstance(v,str) or not v.strip() for v in opts) or len(set(opts))!=len(opts):fail('question_not_four_distinct_options',id=qid)
  if q.get('correct') not in ['A','B','C','D']:fail('question_missing_single_answer_key',id=qid)
  if not q.get('stem') or not q.get('rationale'):fail('question_missing_stem_or_internal_rationale',id=qid)
  topics=set(q.get('section_ids',[]));coverage|=topics
  if not topics or not topics<=ids:fail('question_topic_not_in_article',id=qid)
 if coverage!=ids:fail('quiz_not_covering_whole_article',uncovered=sorted(ids-coverage))
 if data.get('author')!='ANDREA CENTINARO':fail('wrong_author')
 body=' '.join(plain(p) for u in sections for p in u.get('blocks',[]))
 if SELF_REFERENCES.search(body):fail('blog_video_self_reference')
 cited=set()
 for group in re.findall(r'\[([0-9, ]+)\]',body):cited|={int(i.strip()) for i in group.split(',')}
 if not refs or len(refids)!=len(refs):fail('references_missing_or_duplicate')
 if cited-refids:fail('citation_without_reference',citations=sorted(cited-refids))
 if refids-cited:fail('unused_reference',references=sorted(refids-cited))
 for r in refs:
  if any(not r.get(f) for f in ['authors','year','title','publication','url']):fail('reference_incomplete',number=r.get('number'))
  if not r.get('url','').startswith('https://'):fail('reference_without_https',number=r.get('number'))
 if html is not None:
  s=BeautifulSoup(html,'html.parser');qs=s.select('.quiz-card');qsec=s.find(id=quiz.get('id','verifica'));msec=s.select_one('.lf-simple-map');bsec=s.find(id='bibliografia')
  nodes=s.find_all(True);positions={id(x):i for i,x in enumerate(nodes)}
  if any(x is None for x in [qsec,msec,bsec]):fail('quiz_map_bibliography_missing')
  elif not positions[id(qsec)]<positions[id(msec)]<positions[id(bsec)]:fail('wrong_quiz_map_bibliography_order')
  if len(qs)!=len(questions):fail('html_question_count_mismatch')
  for q in questions:
   el=s.find(id=q.get('id'));cells=el.select('.quiz-options td') if el else []
   if len(cells)!=4:fail('html_not_four_options',id=q.get('id'));continue
   if [c.select_one('.option-letter').get_text().strip() if c.select_one('.option-letter') else '' for c in cells]!=['A)','B)','C)','D)']:fail('html_option_order_not_abcd',id=q['id'])
   for t,c in zip(q['options'],cells):
    if norm(t) not in norm(c.get_text()):fail('html_option_text_mismatch',id=q['id'])
  if s.select('[data-correct],.correct-answer,#soluzioni') and not data.get('include_answer_key',False):fail('answer_key_visible_without_request')
  if bsec:
   if not bsec.find(['h1','h2']) or bsec.find(['h1','h2']).get_text().strip()!='RIFERIMENTI BIBLIOGRAFICI':fail('wrong_bibliography_heading')
   if re.search(r'\bFONT[EI]\b',bsec.get_text(' ',strip=True),re.I):fail('forbidden_fonte_label')
   if not bsec.get_text().strip().endswith('Articolo scritto da ANDREA CENTINARO.'):fail('missing_final_signature')
   if bsec.select('img'):fail('image_in_bibliography')
  author=s.find('meta',attrs={'name':'author'})
  if not author or author.get('content')!='ANDREA CENTINARO':fail('pdf_author_metadata_missing')
  if SELF_REFERENCES.search(s.get_text(' ',strip=True)):fail('blog_video_reference_in_html')
 return {'passed':not errors,'units':len(sections),'questions':len(questions),'references':len(refs),'quiz_coverage':sorted(coverage),'errors':errors,'limits':'Controllo strutturale offline, non certifica livello di difficoltà, correttezza scientifica, veridicità bibliografica né PDF/UA. Integrare QA tipografico/visivo e revisione umana.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--html');p.add_argument('--report');a=p.parse_args();r=check(json.loads(Path(a.manifest).read_text()),Path(a.html).read_text() if a.html else None)
 if a.report:Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

