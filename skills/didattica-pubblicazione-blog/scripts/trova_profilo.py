#!/usr/bin/env python3
"""Trova una scheda operativa locale per nome/alias, senza rete o modifiche."""
import argparse,json,re,unicodedata
from pathlib import Path

def normalize(value):
 value=unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode().lower()
 return re.sub(r'[^a-z0-9]+',' ',value).strip()

def select(records,query):
 norm=normalize(query);tokens=set(norm.split());out=[]
 for record in records:
  aliases=[record['original_name'],*record.get('aliases',[])]
  best=0
  for alias in aliases:
   a=normalize(alias);a_tokens=set(a.split());shared=tokens&a_tokens
   if not shared:continue
   score=100*len(shared)/max(len(tokens),len(a_tokens))
   if norm==a:score+=1000
   elif norm in a or a in norm:score+=150
   best=max(best,score)
  if best>0:out.append((best,record))
 return sorted(out,key=lambda pair:(-pair[0],pair[1]['original_name']))

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('query',nargs='?',help='Nome app, task o alias')
 parser.add_argument('--list',action='store_true',help='Elenca tutti i profili del pacchetto')
 parser.add_argument('--json',action='store_true',help='Output JSON')
 parser.add_argument('--limit',type=int,default=5)
 args=parser.parse_args();root=Path(__file__).resolve().parent.parent
 data=json.loads((root/'references/alias.json').read_text())
 if not args.query and not args.list:parser.error('Specificare query o --list')
 ranked=[(None,r)for r in data] if args.list else select(data,args.query)[:max(1,args.limit)]
 result=[]
 for score,r in ranked:
  path=root/r['guide']
  if not path.is_file():raise SystemExit('Scheda mancante: '+str(path))
  result.append({'original_name':r['original_name'],'skill':r['new_skill'],
   'guide':str(path),'status':r['status'],'score':None if score is None else round(score,2),
   'missing_original_resources':r['missing_original_resources']})
 if args.json:print(json.dumps(result,ensure_ascii=False,indent=2))
 else:
  for r in result:
   print(f"{r['original_name']} → {r['guide']} [{r['status']}]")
   if r['missing_original_resources']:print('  Originale da recuperare: '+', '.join(r['missing_original_resources']))
 if not result:raise SystemExit(2)

if __name__=='__main__':main()

