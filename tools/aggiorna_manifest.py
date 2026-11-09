#!/usr/bin/env python3
"""Rigenerare gli hash solo dopo modifiche intenzionali e review. Non firma il contenuto."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 files=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or p.name=='MANIFEST.json' or any(x in ('.git','__pycache__','.venv','node_modules') for x in p.parts):continue
  files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (ROOT/'MANIFEST.json').write_text(json.dumps({'format_version':1,'snapshot_date':'2026-11-05','skills':len(list((ROOT/'skills').glob('*/SKILL.md'))),'files':files},ensure_ascii=False,indent=2));print(f'Manifest aggiornato: {len(files)} file. Rieseguire verifica e test; non implica una firma autenticata.')
if __name__=='__main__':main()

