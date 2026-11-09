#!/usr/bin/env python3
"""Adatta l'app «Marco histórico del Romanticismo en España» (espana-xix-match)
a un nuovo argomento: riscrive SOLO i dati dell'attività (eventi, audio,
posizioni dei puntini), il titolo e le dimensioni dell'immagine. Non tocca
logica, UI, stili né deploy.

Uso:
  python3 adatta_app.py --config nuovo-argomento.json [--root /percorso/app]
      [--dry-run]

Config (struttura completa in templates/app-config.json della skill):
{
  "title": "Marco histórico del Romanticismo en España",
  "theme_color": "#3B1849",
  "image": "timeline.png",
  "map_w": 1376, "map_h": 821,
  "events": [
    {"id":"e1808","year":"1808","title":"Guerra de Independencia",
     "audio":"/audio/e1808.mp3?v=12","x":10.7,"y":20.1}, ...
  ],
  "sfx": {"intro":"/audio/intro.mp3?v=10","ok":"/audio/ok.mp3?v=10",
          "ko":"/audio/ko.mp3?v=10","fin":"/audio/fin.mp3?v=10"}
}

Dopo l'adattamento resta da fare (manuale, documentato nella skill):
  1) sostituire client/public/timeline.png (stesso aspect ratio e stesse
     posizioni % dei puntini);
  2) mettere i nuovi audio in client/public/audio/ e aggiornare i nomi/path;
  3) rilanciare i numeri di cache (?v=N) su immagine e audio;
  4) pnpm check && pnpm build, deploy preview/produzione.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------- frammenti TS riusati dalla versione originale -------------

SHUFFLE = """export function shuffleIds(ids: string[]): string[] {
  const copy = [...ids];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = copy[i];
    copy[i] = copy[j];
    copy[j] = tmp;
  }
  return copy;
}
"""


def render_events_ts(cfg: dict) -> str:
    lines = ["export type TimelineEvent = {",
             "  id: string;",
             "  year: string;",
             "  title: string;",
             "  audio: string;",
             "  x: number;",
             "  y: number;",
             "};", "",
             "export const EVENTS: TimelineEvent[] = ["]
    for e in cfg["events"]:
        lines.append(
            f"  {{ id: {json.dumps(e['id'])}, year: {json.dumps(e['year'])}, "
            f"title: {json.dumps(e['title'])}, audio: {json.dumps(e['audio'])}, "
            f"x: {e['x']}, y: {e['y']} }},"
        )
    lines += ["];", "", "export const SFX = {"]
    for k in ("intro", "ok", "ko", "fin"):
        lines.append(f"  {k}: {json.dumps(cfg['sfx'][k])},")
    lines += ["};", "", SHUFFLE]
    return "\n".join(lines)


def validate(cfg: dict) -> None:
    req = ("title", "events", "sfx", "map_w", "map_h")
    for k in req:
        if k not in cfg:
            sys.exit(f"ERRORE: manca '{k}' nella config")
    for e in cfg["events"]:
        for k in ("id", "year", "title", "audio", "x", "y"):
            if k not in e:
                sys.exit(f"ERRORE: manca '{k}' nell'evento {e}")
    ids = [e["id"] for e in cfg["events"]]
    if len(set(ids)) != len(ids):
        sys.exit("ERRORE: id eventi duplicati")
    for e in cfg["events"]:
        if not (0 <= e["x"] <= 100 and 0 <= e["y"] <= 100):
            sys.exit(f"ERRORE: posizione fuori scala per {e['id']} "
                     f"(x,y devono essere percentuali 0-100)")


def patch_home(src: str, cfg: dict) -> str:
    src = re.sub(r"const MAP_W = \d+;", f"const MAP_W = {cfg['map_w']};", src, count=1)
    src = re.sub(r"const MAP_H = \d+;", f"const MAP_H = {cfg['map_h']};", src, count=1)
    title = cfg["title"]
    src = re.sub(r"<h1>.*?</h1>", f"<h1>{title}</h1>", src, count=1)
    src = re.sub(r'alt="[^"]*"', f'alt="{title}"', src, count=1)
    return src


def patch_index(src: str, cfg: dict) -> str:
    src = re.sub(r"<title>.*?</title>", f"<title>{cfg['title']}</title>", src, count=1)
    tc = cfg.get("theme_color", "#3B1849")
    src = re.sub(r'<meta name="theme-color" content="[^"]*"',
                 f'<meta name="theme-color" content="{tc}"', src, count=1)
    return src


def main() -> None:
    ap = argparse.ArgumentParser(description="Adatta espana-xix-match a un nuovo argomento")
    ap.add_argument("--config", required=True, help="JSON con titolo + eventi (vedi templates/app-config.json)")
    ap.add_argument("--root", default=".", help="Radice dell'app (default: .)")
    ap.add_argument("--dry-run", action="store_true", help="Mostra le modifiche senza scrivere")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    validate(cfg)
    root = Path(args.root)

    targets = {
        "client/src/data/events.ts": None,     # riscritto per intero
        "client/src/pages/Home.tsx": patch_home,
        "client/index.html": patch_index,
    }

    print(f"=== Adattamento app per: {cfg['title']} "
          f"({len(cfg['events'])} eventi) — root: {root}")
    for rel, fn in targets.items():
        p = root / rel
        if not p.exists():
            print(f"  ! salto (non trovato): {rel}")
            continue
        if rel.endswith("events.ts"):
            out = render_events_ts(cfg)
        else:
            out = fn(p.read_text(encoding="utf-8"), cfg)
        if args.dry_run:
            print(f"  [dry-run] {rel}: {len(out)} byte pronti")
        else:
            p.write_text(out, encoding="utf-8")
            print(f"  [ok] {rel} aggiornato ({len(out)} byte)")

    print()
    print("RESTA DA FARE (manuale):")
    print(f"  1. client/public/{cfg.get('image', 'timeline.png')}: stessa "
          f"proporzione ({cfg['map_w']}x{cfg['map_h']}) e stesse posizioni %")
    print(f"  2. audio in client/public/audio/ ({len(cfg['events'])} eventi + intro/ok/ko/fin)")
    print("  3. rilanciare i ?v=N di immagine e audio (cache browser)")
    print("  4. pnpm check && pnpm build && deploy preview/produzione")


if __name__ == "__main__":
    main()
