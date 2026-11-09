#!/usr/bin/env python3
"""Catalogo, preparazione portabile e validazione OFFLINE. Nessuna rete, API o deploy."""
from pathlib import Path
import argparse,ast,collections,hashlib,json,re,shutil,sys,unicodedata

ROOT=Path(__file__).resolve().parents[1]
TEXT={'.md','.py','.sh','.json','.html','.css','.txt','.ts','.tsx','.js','.mjs','.yml','.yaml','.toml'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(x):print(json.dumps(x,ensure_ascii=False,indent=2))
def catalogo():return json.loads((ROOT/'catalogo/skills.json').read_text(encoding='utf-8'))
def normalize(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
def cerca(query):
 words=normalize(query).split();rows=[]
 for row in catalogo():
  name=normalize(row['name']);text=normalize(row['description']+' '+row['category']);score=sum((5 if w in name else 1 if w in text else 0) for w in words)
  if not words or score:rows.append({'name':row['name'],'score':score,'category':row['category'],'file':row['entrypoint'],'description':row['description']})
 return sorted(rows,key=lambda x:(-x['score'],x['name']))

def prepara(dest,workspace,mapping_file=None):
 dest=Path(dest).expanduser().resolve();workspace=Path(workspace).expanduser().resolve()
 if dest.exists():raise ValueError('Destinazione già esistente: sceglierne una NUOVA; nessun file viene sovrascritto.')
 if dest==ROOT or ROOT in dest.parents or dest in ROOT.parents:raise ValueError('Destinazione dentro/sopra il repository: usare una cartella esterna separata.')
 maps={'/home/user/skills':(dest/'skills').as_posix(),'/home/user':workspace.as_posix(),'/home/ubuntu':workspace.as_posix()}
 if mapping_file:
  custom=json.loads(Path(mapping_file).read_text(encoding='utf-8'))
  if not isinstance(custom,dict):raise ValueError('Mappa progetti: oggetto JSON old_path→new_path richiesto.')
  for old,new in custom.items():
   if not isinstance(old,str) or not old.startswith('/home/'):raise ValueError('Prefisso storico non valido nella mappa.')
   if not isinstance(new,str) or 'PERCORSO_ASSOLUTO' in new or '<' in new:raise ValueError('Compilare i segnaposto della mappa con percorsi reali.')
   new=Path(new).expanduser()
   if not new.is_absolute():raise ValueError('Le destinazioni della mappa devono essere percorsi assoluti.')
   if old=='/home/user/skills':raise ValueError('Il prefisso skills è riservato alla copia portabile.')
   maps[old]=new.resolve().as_posix()
 # Una sola passata evita di risostituire i nuovi percorsi che vivono sotto /home/user.
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(maps,key=len,reverse=True)))
 dest.mkdir(parents=True)
 changed=[];count=0
 for sub in ('skills','shared'):
  shutil.copytree(ROOT/sub,dest/sub)
  for p in sorted((dest/sub).rglob('*')):
   if not p.is_file():continue
   count+=1
   if p.suffix not in TEXT:continue
   text=p.read_text(encoding='utf-8');new=pattern.sub(lambda m:maps[m.group(0)],text)
   if new!=text:p.write_text(new,encoding='utf-8');changed.append(p.relative_to(dest).as_posix())
 report={'destination':str(dest),'workspace':str(workspace),'skills':len(catalogo()),'files':count,'rewritten_text_files':len(changed),'rewritten_paths':changed,'mapping':maps,'note':'Copia preparata, non eseguita. Nessuna app esterna installata; input/progetti ancora da fornire. Nessuna credenziale copiata.'}
 (dest/'PREPARAZIONE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 (dest/'AGENTS.md').write_text('# COPIA PORTABILE\n\nLe 55 skill sono in `skills/`. Leggere la skill adatta, poi solo i riferimenti pertinenti. `shared/INGRESSO_STORICO.md` non è una skill attiva. I percorsi sono stati adattati alla cartella workspace dichiarata in PREPARAZIONE.json; i progetti/input non sono stati copiati. Rivedere lo script prima di eseguirlo. Non eseguire deploy, chiamate a pagamento o operazioni sui dati reali senza richiesta e autorizzazione.\n')
 return report

def validate(root=ROOT):
 root=Path(root);errors=[];warnings=[];count=0;py=0;links=0
 for p in sorted((root/'skills').glob('*/SKILL.md')):
  count+=1;t=p.read_text();m=re.match(r'\A---\s*\n(.*?)\n---(?:\n|$)',t,re.S)
  if not m:errors.append({'file':str(p.relative_to(root)),'issue':'frontmatter mancante'});continue
  if not re.search(r'(?m)^name:\s*'+re.escape(p.parent.name)+r'\s*$',m.group(1)):errors.append({'file':str(p.relative_to(root)),'issue':'name non coincide con cartella'})
  if not re.search(r'(?m)^description:\s*\S',m.group(1)):errors.append({'file':str(p.relative_to(root)),'issue':'description mancante'})
  prose=re.sub(r'```.*?```','',t,flags=re.S)
  for link in re.findall(r'\]\(([^)]+)\)',prose):
   if re.match(r'^(?:https?://|mailto:|data:|#|/)',link) or link in ('url',):continue
   target=link.split('#')[0]
   if target:links+=1
   if target and not (p.parent/target).exists():errors.append({'file':str(p.relative_to(root)),'issue':'link locale mancante','target':target})
 for p in sorted(root.rglob('*')):
  if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:continue
  rel=p.relative_to(root).as_posix()
  if p.is_symlink():errors.append({'file':rel,'issue':'link simbolico non portabile'})
  if p.stat().st_size>=100_000_000:errors.append({'file':rel,'issue':'dimensione incompatibile con GitHub ordinario'})
  if p.name.startswith('.env') and p.name!='.env.example':errors.append({'file':rel,'issue':'file ambiente privato'})
  if p.suffix=='.py':
   py+=1
   try:ast.parse(p.read_text())
   except SyntaxError as e:errors.append({'file':rel,'issue':'Python non compilabile','line':e.lineno})
  if p.suffix=='.json':
   try:json.loads(p.read_text())
   except ValueError:errors.append({'file':rel,'issue':'JSON non valido'})
  if p.suffix in TEXT:
   text=p.read_text()
   for n,line in enumerate(text.splitlines(),1):
    # Riconoscimento per valori, non nomi di variabili o esempi di scansione.
    if re.search(r'\b(?:sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_-]{30,}|gh[pousr]_[A-Za-z0-9_]{25,}|github_pat_[A-Za-z0-9_]{25,}|AKIA[A-Z0-9]{16})\b',line):errors.append({'file':rel,'issue':'possibile chiave riservata','line':n})
    if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',line):errors.append({'file':rel,'issue':'chiave privata','line':n})
 manifest=root/'MANIFEST.json';checked=0
 if manifest.exists():
  data=json.loads(manifest.read_text());expected=set()
  for row in data['files']:
   rel=Path(row['path']);expected.add(rel.as_posix())
   if rel.is_absolute() or '..' in rel.parts:errors.append({'file':str(rel),'issue':'percorso manifest non sicuro'});continue
   p=root/rel;checked+=1
   if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append({'file':str(rel),'issue':'hash o dimensione diversi dal manifest'})
  actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and not any(x in ('.git','__pycache__') for x in p.parts)}
  for rel in sorted(actual-expected):errors.append({'file':rel,'issue':'file non presente nel manifest'})
 if count!=55:errors.append({'issue':'numero skill inatteso','actual':count,'expected':55})
 return {'passed':not errors,'skills':count,'python_files_syntax_checked':py,'active_skill_links_checked':links,'manifest_files_checked':checked,'errors':errors,'warnings':warnings,'scope':'Controlli offline statici. Nessun test integrale delle app, generazione a pagamento, API o deploy.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
 sub.add_parser('catalogo');s=sub.add_parser('trova');s.add_argument('query',nargs='*');s=sub.add_parser('prepara');s.add_argument('--dest',required=True);s.add_argument('--workspace',required=True);s.add_argument('--map',dest='mapping_file');sub.add_parser('verifica')
 args=p.parse_args()
 try:
  if args.action=='catalogo':dump(catalogo())
  elif args.action=='trova':dump(cerca(' '.join(args.query)))
  elif args.action=='prepara':dump(prepara(args.dest,args.workspace,args.mapping_file))
  else:
   r=validate();dump(r);return 0 if r['passed'] else 1
 except (ValueError,OSError) as e:print('ERRORE: '+str(e),file=sys.stderr);return 2
 return 0
if __name__=='__main__':raise SystemExit(main())

