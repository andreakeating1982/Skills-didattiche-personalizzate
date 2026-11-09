#!/usr/bin/env python3
"""Genera il piano delle scene per un video claymation didattico.

La durata di ogni scena è proporzionale al numero di caratteri del testo
narrato (velocità di lettura costante) e viene riscalata esattamente sulla
durata dell'audio; l'ultimo clip assorbe il resto dell'arrotondamento.

Uso:
  python3 plan_scene.py --audio 318.483 --scenes scene.tsv --out clips_plan.json

Formato scene.tsv (TAB come separatore; opzionali le ultime due colonne):
  caption<TAB>testo narrato
  oppure
  caption<TAB>testo narrato<TAB>descrizione visiva (senza suffisso stile)
  oppure
  caption<TAB>testo narrato<TAB>descrizione visiva<TAB>chiave_ref1,chiave_ref2

Le chiavi ref vengono risolte nel dizionario REF qui sotto; se una chiave
contiene "http" viene usata come URL diretto.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# Suffisso di stile standard del progetto claymation (tenerlo identico in
# tutte le scene dello stesso video per garantire coerenza visiva).
CLAY = ("Claymation stop-motion diorama, plasticine clay texture with visible fingerprints, "
        "miniature figures and sets, warm cinematic lighting, dramatic sky, epic documentary "
        "style, 16:9 widescreen.")

# Immagini di riferimento del progetto "Marco histórico del Romanticismo en
# España". Per altri argomenti sostituire con i propri riferimenti: 5-8
# immagini (personaggi/ambienti ricorrenti) generate nello stesso stile.
REF = {
    "palace": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/47093cef-b6eb-4559-9b28-94625339e230.png",
    "fernando": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/46176de8-758f-45f5-8ab9-b325d68623b5.png",
    "isabel": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/5ed4c27b-4a33-4c73-a7d3-e6ea9848ced4.png",
    "mariacristina": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/7f52c3c8-c730-468c-9293-ffc73e48cecf.png",
    "carlista": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/2cf7fadd-807e-4fca-910b-80f610b29bfe.png",
    "napoleon": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/570cabf3-f9d0-4bb7-b52a-3d43d97c45c0.png",
    "imperio": "https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/076374dc-657d-4804-9547-3bccc1acb38d.png",
}


def resolve_ref(token: str) -> str:
    token = token.strip()
    if token.startswith("http"):
        return token
    if token in REF:
        return REF[token]
    raise KeyError(f"Chiave ref sconosciuta: {token!r} (aggiungila a REF o usa un URL diretto)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Piano scene claymation da narrazione")
    ap.add_argument("--audio", type=float, required=True, help="Durata della narrazione in secondi")
    ap.add_argument("--scenes", required=True, help="File TSV: caption<TAB>testo[<TAB>visual[<TAB>ref1,ref2]]")
    ap.add_argument("--out", default="clips_plan.json", help="File JSON di output")
    ap.add_argument("--style", default=CLAY, help="Suffisso di stile (default: CLAY standard)")
    args = ap.parse_args()

    rows = []
    with open(args.scenes, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            caption, text = parts[0], parts[1]
            visual = parts[2] if len(parts) > 2 else ""
            refs = [r for r in parts[3].split(",") if r.strip()] if len(parts) > 3 else []
            rows.append((caption, text, visual, refs))

    if not rows:
        raise SystemExit("Nessuna scena trovata in " + args.scenes)

    total_chars = sum(len(r[1]) for r in rows)
    clips = []
    for i, (caption, text, visual, refs) in enumerate(rows, 1):
        dur = args.audio * len(text) / total_chars
        clip = {
            "id": f"clip{i:02d}",
            "caption": caption,
            "text": text,
            "dur": round(dur, 3),
            "visual": f"{visual} {args.style}".strip() if visual else args.style,
            "refs": [resolve_ref(r) for r in refs],
        }
        clips.append(clip)

    # riscalatura esatta sulla durata dell'audio
    factor = args.audio / sum(c["dur"] for c in clips)
    for c in clips:
        c["dur"] = round(c["dur"] * factor, 3)
    diff = args.audio - sum(c["dur"] for c in clips)
    clips[-1]["dur"] = round(clips[-1]["dur"] + diff, 3)

    out = Path(args.out)
    out.write_text(json.dumps(clips, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TOTAL {len(clips)} clip  sum={sum(c['dur'] for c in clips):.3f}s (audio {args.audio}s)")
    for c in clips:
        print(f"{c['id']} {c['dur']:7.3f}s | {c['caption'][:46]:46s} | refs={len(c['refs'])}")


if __name__ == "__main__":
    main()
