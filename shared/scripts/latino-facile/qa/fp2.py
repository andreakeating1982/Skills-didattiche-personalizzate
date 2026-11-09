import requests
U="https://3000-i4nq7yqdswtyddr7hb8sj.sandbox.easy-peasy.ai/api/trpc/latino.translate"
NON = ["nomine","homine","virgine","ratione","legione","regione","nave","neve","breve","bene","omne","sine","Cicerone","Platone","Nerone","carne","mane","ordine","pane","atque","neque","itaque","denique","quoque","usque","uterque","quisque","ubique","undique","quinque","aeque","nonne","namque","quicumque","umquam","passione"]
SI = ["Marcusque","Iuliaque","venitque","hostesque","populusque","amicosque","liberique","Romanorumque","puellisque","terrasque","tractusque","caelumque","Amasne","Rexne","Venitne","Habetne","tresve","bellove","pacive","tecum","mecum","secum","nobiscum","vobiscum","quocum","quibuscum"]
def run(words, tmpl):
    text=" ".join(tmpl.format(w=w) for w in words)
    d=requests.post(U,json={"json":{"text":text}},timeout=170).json()["result"]["data"]["json"]
    out={}
    for s in d["coloredSentences"]:
        for t in s["tokens"]:
            if t["isPunct"]: continue
            out[t["word"].lower()]=t["analysis"].get("suffisso")
    return d,out
fp=[];srcs=set()
for i in range(0,len(NON),9):
    ws=NON[i:i+9]; d,o=run(ws,"Vidi {w}.")
    srcs.add((d["source"],d["colorSource"]))
    fp+=[(w,o[w.lower()]["testo"]) for w in ws if o.get(w.lower())]
print("sorgenti",srcs,"| FALSI POSITIVI:",fp)
miss=[]
for i in range(0,len(SI),9):
    ws=SI[i:i+9]; d,o=run(ws,"Audio {w}.")
    srcs.add((d["source"],d["colorSource"]))
    miss+=[w for w in ws if not o.get(w.lower())]
print("sorgenti",srcs,"| NON riconosciute:",miss)
