import json, re, sys, time, requests
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/home/user/qa")
from corpus import CORPUS

URL = sys.argv[1] if len(sys.argv) > 1 else "https://3000-i4nq7yqdswtyddr7hb8sj.sandbox.easy-peasy.ai/api/trpc/latino.translate"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/user/qa/results.json"
CASE = {"nominativo":"N","genitivo":"G","dativo":"D","accusativo":"A","vocativo":"V","ablativo":"Ab"}
MOOD = {"indicativo":"ind","congiuntivo":"cong","imperativo":"imp","infinito":"inf","participio":"part","gerundivo":"part","gerundio":"part","supino":"part"}

def tag(a):
    o = a["options"][a["selected"]] if a["options"] else {}
    cat = a["category"]
    if cat == "verbo" or o.get("pos") == "participio":
        return MOOD.get(o.get("mood"), "verbo?")
    if cat in ("nome", "aggettivo", "pronome", "numerale", "participio"):
        return CASE.get(o.get("case"), cat + "?")
    if cat == "preposizione": return "PREP"
    if cat == "congiunzione": return "CONJ"
    if cat in ("avverbio", "particella"): return "ADV"
    return cat

# raggruppa in batch da max 40 parole, frasi intere
batches, cur, n = [], [], 0
for i, (lat, gold) in enumerate(CORPUS):
    w = len(lat.split())
    if cur and n + w > 40:
        batches.append(cur); cur, n = [], 0
    cur.append(i); n += w
if cur: batches.append(cur)

def run(b):
    text = " ".join(CORPUS[i][0] for i in b)
    t0 = time.time()
    for attempt in range(3):
        try:
            r = requests.post(URL, json={"json": {"text": text}}, timeout=170)
            d = r.json()["result"]["data"]["json"]
            break
        except Exception as e:
            d = None; err = str(e)
    el = time.time() - t0
    if d is None: return {"batch": b, "error": err, "secs": el}
    toks = []
    for s in d["coloredSentences"]:
        for t in s["tokens"]:
            if not t["isPunct"] and t["analysis"]:
                toks.append((t["word"], tag(t["analysis"]), t["analysis"]["color"]))
    return {"batch": b, "secs": el, "source": d["source"], "color": d["colorSource"],
            "lines": d["lines"], "toks": toks, "nsent": len(d["coloredSentences"])}

t0 = time.time()
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(run, batches))
json.dump(res, open(OUT, "w"), ensure_ascii=False)
print("batches", len(batches), "tempo totale %.0fs" % (time.time() - t0))
