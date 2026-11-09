from pathlib import Path
import sys,json
PROFILI={'latino-facile': '../../latino-facile/SKILL.md', 'lingue-facili': '../../lingue-facili/SKILL.md', 'francese-facile': '../../francese-facile/SKILL.md', 'mappe-concettuali-lingue': '../../mappe-concettuali-lingue/SKILL.md'}
q=" ".join(sys.argv[1:]).casefold().split()
rows=[{"skill":n,"file":str((Path(__file__).resolve().parent/p).resolve())} for n,p in PROFILI.items() if not q or any(x in n for x in q)]
print(json.dumps(rows,ensure_ascii=False,indent=2))
