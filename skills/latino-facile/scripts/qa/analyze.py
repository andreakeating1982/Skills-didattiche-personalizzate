import json, re, sys
sys.path.insert(0, "/home/user/qa")
from corpus import CORPUS
R = sys.argv[1] if len(sys.argv) > 1 else "/home/user/qa/results.json"
res = json.load(open(R))
tot = ok = 0
sent_ok = sent_tot = 0
errs = []
print("== batch ==")
for r in res:
    if "error" in r:
        print("ERR", r["batch"], r["error"][:100]); continue
    print(f"batch {r['batch'][0]}-{r['batch'][-1]}: {r['secs']:.1f}s source={r['source']} color={r['color']} frasi={r['nsent']} (attese {len(r['batch'])}) parole={len(r['toks'])}")
for r in res:
    if "error" in r: continue
    gold = []
    for i in r["batch"]:
        gold += [(i, g) for g in CORPUS[i][1].split()]
    if len(gold) != len(r["toks"]):
        print("DISALLINEATO batch", r["batch"], len(gold), len(r["toks"]))
        continue
    per = {}
    for (i, g), (w, p, c) in zip(gold, r["toks"]):
        tot += 1
        good = (g == p)
        ok += good
        per.setdefault(i, []).append(good)
        if not good: errs.append((CORPUS[i][0], w, g, p))
    for i, v in per.items():
        sent_tot += 1; sent_ok += all(v)
print(f"\nPAROLE corrette: {ok}/{tot} = {100*ok/tot:.1f}%")
print(f"FRASI interamente corrette: {sent_ok}/{sent_tot} = {100*sent_ok/sent_tot:.1f}%")
print("\n== ERRORI colore/ruolo ==")
for s, w, g, p in errs: print(f"{w:14} atteso={g:5} app={p:6} | {s}")
print("\n== TRADUZIONI ==")
for r in res:
    if "error" in r: continue
    for i, l in zip(r["batch"], r["lines"] + [""] * 20):
        print(f"{CORPUS[i][0]}\n   -> {l}")
