#!/usr/bin/env python3
"""Gate per i nuovi quaderni didattici rimpaginati dell'utente.
Non sostituisce la verifica semantica delle risposte o delle fonti.
Esempio: python3 verifica_quiz_fonti_obbligatori.py quaderno.html --pdf quaderno.pdf
I selettori possono essere adattati con gli argomenti da riga di comando.
"""
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
import argparse, json, re, sys


def verify(html_path, pdf_path=None, quiz_selector='#verifica', card_selector='.quiz-card, [data-question]',
           refs_selector='#referencias, #bibliografia, #riferimenti',
           entry_selector='[data-bibliography-entry], .ref-entry[id]',
           notes_selector='sup a[href^="#"], a[data-bibliographic-note][href^="#"]', expected_instruction=None):
    errors=[]
    def check(condition, message):
        if not condition: errors.append(message)
    html_path=Path(html_path)
    soup=BeautifulSoup(html_path.read_text(encoding='utf8'), 'html.parser')
    quiz=soup.select_one(quiz_selector)
    refs=soup.select_one(refs_selector)
    mapa=soup.select_one('#mapa, #mappa, [data-support-profile="map"]')
    check(quiz is not None,'Manca la sezione della verifica')
    check(refs is not None,'Manca la sezione dei riferimenti bibliografici')
    check(mapa is not None,'Manca la mappa finale prevista dal modello')
    if expected_instruction is not None:
        intro=quiz.select_one('.quiz-intro') if quiz else None
        check(intro is not None and intro.get_text(' ',strip=True)==expected_instruction,
              'Consegna assente o diversa dal testo atteso')
    cards=quiz.select(card_selector) if quiz else []
    check(len(cards)==10, f'Domande trovate {len(cards)}, attese esattamente 10')
    for i,card in enumerate(cards,1):
        options=card.select('td') or card.select('li') or card.select('[data-option]')
        check(len(options)==4,f'Domanda {i}: trovate {len(options)} opzioni, attese 4')
        if len(options)==4:
            labels=[re.match(r'^\s*([A-D])[.)]\s*',opt.get_text(' ',strip=True)) for opt in options]
            check(all(labels) and [m.group(1) for m in labels if m]==list('ABCD'),
                  f'Domanda {i}: le opzioni devono essere in ordine A–D')
            check(len({opt.get_text(' ',strip=True) for opt in options})==4,
                  f'Domanda {i}: opzioni duplicate')
    entries=refs.select(entry_selector) if refs else []
    check(bool(entries),'Nessuna voce bibliografica identificabile')
    ids=[x.get('id') for x in entries]
    check(all(ids) and len(set(ids))==len(ids),'Le fonti devono avere id univoci')
    notes=[]
    for a in soup.select(notes_selector):
        if a.find_parent(id=refs.get('id')) if refs and refs.get('id') else False:
            continue
        target=a.get('href','')[1:]
        if target in ids: notes.append((a,target))
    for rid in ids:
        if rid: check(any(target==rid for _,target in notes),f'Nessun richiamo numerico alla fonte {rid}')
    check(bool(notes),'Nessun richiamo bibliografico cliccabile nel corpo')
    check(not (refs and refs.select('img')),'La bibliografia non deve contenere immagini')
    all_nodes=list(soup.descendants)
    if quiz and refs and mapa:
        check(all_nodes.index(quiz)<all_nodes.index(mapa)<all_nodes.index(refs),
              'Ordine richiesto: verifica, mappa, bibliografia finale')
        if refs.parent:
            later=[x for x in refs.find_all_next('section') if x not in refs.descendants]
            check(not later,'Una sezione segue la bibliografia finale')
    def indexlink(element):
        if not element or not element.get('id'):return False
        target='#'+element['id']
        candidates=soup.select('nav a[href], .index-box a[href], #indice a[href], [role="navigation"] a[href]')
        return any(x.get('href')==target for x in candidates)
    for el,label in [(quiz,'verifica'),(mapa,'mappa'),(refs,'bibliografia')]:
        if el: check(indexlink(el),'Manca il link indice alla '+label)
    pdfchecks={}
    if pdf_path:
        import pymupdf
        from weasyprint import HTML
        document=HTML(filename=str(html_path)).render()
        pdf=pymupdf.open(str(pdf_path))
        anchors={}
        for n,p in enumerate(document.pages):
            for key,pos in p.anchors.items():
                anchors.setdefault(key,(n,pos))
        for el,label in [(quiz,'verifica'),(mapa,'mappa'),(refs,'bibliografia')]:
            if el and el.get('id'):
                aid=el['id'];check(aid in anchors,'Ancora PDF mancante per '+label)
                if aid in anchors:
                    target_page=anchors[aid][0]
                    index_links=pdf[0].get_links()
                    check(any(l.get('page')==target_page and l['from'].width>0 and l['from'].height>0 for l in index_links),
                          'Indice PDF non raggiunge la prima pagina di '+label)
                    pdfchecks[label+'_page']=target_page+1
        links=[(n,link) for n,p in enumerate(pdf) for link in p.get_links()]
        for a,rid in notes:
            if rid not in anchors:
                errors.append('Ancora fonte assente nel PDF: '+rid);continue
            target_page=anchors[rid][0]
            # Area positiva e corretto foglio di destinazione sono verificati;
            # l'esatta corrispondenza numeretto/voce resta un controllo umano.
            check(any(link.get('page')==target_page and link['from'].width>0 and link['from'].height>0
                      for _,link in links),'Nessun link PDF attivo alla pagina di '+rid)
        urls=[a.get('href') for a in (refs.select('a[href^="http"]') if refs else [])]
        external=[l.get('uri') for _,l in links if l.get('uri')]
        for url in urls:
            check(any(unquote(x)==unquote(url) for x in external),'Link web assente nel PDF: '+url)
        pdfchecks['external_reference_links']=len(urls)
        pdfchecks['pages']=len(pdf)
    return {'passed':not errors,'html':str(html_path),'questions':len(cards),'options_per_question':4,
            'references':len(entries),'bibliographic_notes':len(notes),'pdf':pdfchecks,'errors':errors}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('html');p.add_argument('--pdf');p.add_argument('--report')
    p.add_argument('--quiz-selector',default='#verifica')
    p.add_argument('--cards-selector',default='.quiz-card, [data-question]')
    p.add_argument('--references-selector',default='#referencias, #bibliografia, #riferimenti')
    p.add_argument('--expected-instruction',help='Testo esatto della consegna da controllare, nella lingua del quaderno')
    args=p.parse_args()
    result=verify(args.html,args.pdf,args.quiz_selector,args.cards_selector,args.references_selector,expected_instruction=args.expected_instruction)
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.report:Path(args.report).write_text(text+'\n',encoding='utf8')
    print(text)
    return 0 if result['passed'] else 1

if __name__=='__main__':sys.exit(main())

