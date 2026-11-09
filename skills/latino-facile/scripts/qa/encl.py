import requests, json, sys
U="https://3000-i4nq7yqdswtyddr7hb8sj.sandbox.easy-peasy.ai/api/trpc/latino.translate"
TS=[
 "Marcusque Iuliaque rosas amant. Senatus populusque Romanus bellum gerit.",
 "Venitque et videt hostesque fugiunt. Veniuntque amici liberique.",
 "Tecum ambulo et nobiscum manet. Mecum venit, vobiscum loquitur.",
 "Amasne me? Venitne pater? Rexne aderat?",
 "Duo tresve milites venerunt. Pace bellove vivemus.",
 "Atque ita, neque ille neque iste, itaque denique quoque aeque venit.",
 "Armaque virumque cano. Terrasque tractusque maris caelumque profundum.",
 "Quisque suum amat. Uterque venit. Quinque pueri adsunt. Usque ad finem.",
 "Pueri puellaeque in horto ludunt, et liberos liberasque laudant.",
]
for T in TS:
    d=requests.post(U,json={"json":{"text":T}},timeout=170).json()["result"]["data"]["json"]
    print("\n"+T, "| src",d["source"],d["colorSource"])
    for s in d["coloredSentences"]:
        out=[]
        for t in s["tokens"]:
            if t["isPunct"]: continue
            a=t["analysis"]; su=a.get("suffisso")
            if su: out.append(f"{t['word']}[{su['testo']}:{su['colore']} base:{a['category']} {a['color']}]")
        print("  ", " ".join(out) if out else "(nessuna enclitica rilevata)")
