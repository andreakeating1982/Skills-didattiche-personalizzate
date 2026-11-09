#!/usr/bin/env python3
"""
clone_app.py — Clona l'app IMMAGINE INTERATTIVA SORGENTE in una NUOVA app identica
cambiando SOLO il set di domande (immagine, audio, hotspot, segmenti, testo).

Utilizzo:
  python3 clone_app.py --name <nuova-cartella> \
      [--source <cartella|url-github>] \
      [--json <contenuto.json>] \
      [--image <immagine.png>] \
      [--audio <audio.m4a>] \
      [--title <titolo>]

Opzioni:
  --name    (obbligatorio) nome della NUOVA cartella app (es. "mio-argomento")
  --source  sorgente da clonare: cartella locale O URL repo GitHub
            (default: /home/user/romanticismo-interattivo)
  --json    JSON col nuovo contenuto (hotspots, audioSegments, sections, textoExplicativo)
  --image   nuova immagine di sfondo -> client/public/romanticismo-sintesi.png
  --audio   nuovo audio -> client/public/audio/explicacion.m4a
  --title   titolo mostrato nell'app (default: IMMAGINE INTERATTIVA)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

DEFAULT_SOURCE = "/home/user/romanticismo-interattivo"
DEFAULT_TITLE = "IMMAGINE INTERATTIVA"

IGNORE = shutil.ignore_patterns(
    "node_modules", ".git", "dist", "*.zip", "*.skill", ".DS_Store"
)


def js_str(value):
    """Serializza una stringa Python in una stringa JS valida (doppi apici + escape)."""
    return json.dumps(value, ensure_ascii=False)


def ts_literal(text):
    """Costruisce un template literal TS sicuro (escape backtick, backslash, ${)."""
    t = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    return "`" + t + "`"


def num(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("valore numerico non valido: %r" % value)
    return json.dumps(value)


def build_explora_data(content, title):
    """Genera il contenuto di shared/exploraData.ts a partire dal JSON."""
    L = []
    L.append("/**")
    L.append(" * Dati condivisi per l'attività \"Explora la imagen\" — %s." % title)
    L.append(" * Generato da clone_app.py. Usato sia dal server che dal client.")
    L.append(" */")
    L.append("")
    L.append("export interface HotspotData {")
    L.append("  id: string;")
    L.append("  section: string;")
    L.append("  x: number;")
    L.append("  y: number;")
    L.append('  size: "sm" | "md" | "lg";')
    L.append("  label: string;")
    L.append("  info: string;")
    L.append("}")
    L.append("")
    L.append("export interface AudioSegmentData {")
    L.append("  id: number;")
    L.append("  startTime: number;")
    L.append("  endTime: number;")
    L.append("  label: string;")
    L.append("  subtitle: string;")
    L.append("  hotspotIds: string[];")
    L.append("  prompt: string;")
    L.append("}")
    L.append("")
    L.append("export const HOTSPOTS: HotspotData[] = [")
    for h in content["hotspots"]:
        L.append(
            "  { id: %s, section: %s, x: %s, y: %s, size: %s, label: %s, info: %s },"
            % (js_str(h["id"]), js_str(h["section"]), num(h["x"]), num(h["y"]),
               js_str(h["size"]), js_str(h["label"]), js_str(h["info"]))
        )
    L.append("];")
    L.append("")
    L.append("export const AUDIO_SEGMENTS: AudioSegmentData[] = [")
    for seg in content["audioSegments"]:
        ids = ", ".join(js_str(i) for i in seg["hotspotIds"])
        L.append(
            "  { id: %s, startTime: %s, endTime: %s, label: %s, subtitle: %s, hotspotIds: [%s], prompt: %s },"
            % (num(seg["id"]), num(seg["startTime"]), num(seg["endTime"]),
               js_str(seg["label"]), js_str(seg["subtitle"]), ids, js_str(seg["prompt"]))
        )
    L.append("];")
    L.append("")
    L.append("export const SECTION_THEMES: Record<string, { name: string; ring: string; dot: string; glow: string; badge: string }> = {")
    for key, th in content["sections"].items():
        L.append(
            "  %s:  { name: %s,  ring: %s,  dot: %s,  glow: %s,  badge: %s },"
            % (js_str(key), js_str(th["name"]), js_str(th["ring"]), js_str(th["dot"]),
               js_str(th["glow"]), js_str(th["badge"]))
        )
    L.append("};")
    L.append("")
    L.append("export const TEXTO_EXPLICATIVO = " + ts_literal(content.get("textoExplicativo", "")) + ";")
    L.append("")
    return "\n".join(L)


def clone_from_git(url, dest):
    subprocess.run(["git", "clone", "--depth", "1", url, dest], check=True)
    shutil.rmtree(os.path.join(dest, ".git"), ignore_errors=True)


def verify(content):
    """Verifica di base: id hotspot esistenti, sezioni valide, punti per segmento."""
    hs = {h["id"] for h in content["hotspots"]}
    sections = set(content["sections"].keys())
    errors = []
    for h in content["hotspots"]:
        if h["section"] not in sections:
            errors.append("hotspot %s -> sezione sconosciuta %r" % (h["id"], h["section"]))
    for seg in content["audioSegments"]:
        for hid in seg["hotspotIds"]:
            if hid not in hs:
                errors.append("segmento %s -> hotspot inesistente %r" % (seg["id"], hid))
    if len(content["audioSegments"]) != 5:
        errors.append("servono ESATTAMENTE 5 segmenti audio (id 0-4), trovati %d" % len(content["audioSegments"]))
    pts = [len(seg["hotspotIds"]) for seg in content["audioSegments"]]
    if sum(pts) != 10:
        errors.append("il punteggio totale deve essere 10 (somma hotspot per segmento), trovato %d" % sum(pts))
    if errors:
        for e in errors:
            print("  [ERRORE] " + e, file=sys.stderr)
        sys.exit(1)
    print("  [OK] %d hotspot, %d segmenti audio" % (len(hs), len(content["audioSegments"])))
    print("  [OK] punti per domanda: " + " · ".join("D%d=%d" % (i + 1, p) for i, p in enumerate(pts)))
    print("  [OK] punteggio totale: %d/10" % sum(pts))


def replace_title(root, old, new):
    exts = (".tsx", ".ts", ".html")
    count = 0
    for dirpath, _, filenames in os.walk(root):
        if "node_modules" in dirpath or ".git" in dirpath:
            continue
        for fn in filenames:
            if not fn.endswith(exts):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8") as f:
                txt = f.read()
            if old in txt:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(txt.replace(old, new))
                count += 1
    if count:
        print(">> Titolo aggiornato in %d file" % count)


def rename_package(root, name):
    p = os.path.join(root, "package.json")
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        data["name"] = name
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")


def main():
    ap = argparse.ArgumentParser(description="Clona IMMAGINE INTERATTIVA SORGENTE in una nuova app")
    ap.add_argument("--name", required=True, help="nome nuova cartella app")
    ap.add_argument("--source", default=DEFAULT_SOURCE, help="sorgente (cartella o URL git)")
    ap.add_argument("--json", default=None, help="JSON contenuto")
    ap.add_argument("--image", default=None, help="nuova immagine sfondo")
    ap.add_argument("--audio", default=None, help="nuovo audio")
    ap.add_argument("--title", default=None, help="titolo app (default: dal JSON o IMMAGINE INTERATTIVA)")
    args = ap.parse_args()

    target = os.path.join("/home/user", args.name)
    if os.path.exists(target):
        print("[ERRORE] la cartella %s esiste già" % target, file=sys.stderr)
        sys.exit(1)

    # 1. Copia sorgente
    print(">> Copio la sorgente in %s ..." % target)
    if args.source.startswith("http://") or args.source.startswith("https://"):
        clone_from_git(args.source, target)
    else:
        if not os.path.isdir(args.source):
            print("[ERRORE] sorgente non trovata: %s" % args.source, file=sys.stderr)
            sys.exit(1)
        shutil.copytree(args.source, target, ignore=IGNORE)

    # 2. Contenuto
    content = None
    if args.json:
        with open(args.json, encoding="utf-8") as f:
            content = json.load(f)
        verify(content)
        out = os.path.join(target, "shared", "exploraData.ts")
        title = args.title or content.get("titolo") or DEFAULT_TITLE
        with open(out, "w", encoding="utf-8") as f:
            f.write(build_explora_data(content, title))
        print(">> Generato %s" % out)

    # 3. Immagine
    if args.image:
        if not os.path.isfile(args.image):
            print("[ERRORE] immagine non trovata: %s" % args.image, file=sys.stderr)
            sys.exit(1)
        shutil.copyfile(args.image, os.path.join(target, "client", "public", "romanticismo-sintesi.png"))
        print(">> Immagine copiata in client/public/romanticismo-sintesi.png")

    # 4. Audio
    if args.audio:
        if not os.path.isfile(args.audio):
            print("[ERRORE] audio non trovato: %s" % args.audio, file=sys.stderr)
            sys.exit(1)
        shutil.copyfile(args.audio, os.path.join(target, "client", "public", "audio", "explicacion.m4a"))
        print(">> Audio copiato in client/public/audio/explicacion.m4a")

    # 5. Titolo
    title = args.title or (content.get("titolo") if content else None) or DEFAULT_TITLE
    if title != DEFAULT_TITLE:
        replace_title(target, DEFAULT_TITLE, title)

    # 6. package.json name
    rename_package(target, args.name)

    print("")
    print("FATTO. App clonata in %s" % target)
    print("Passi successivi:")
    print("  1) cd %s && pnpm install" % target)
    print("  2) pnpm check")
    print("  3) webdev_deploy mode='preview' (verifica) -> poi 'production'")


if __name__ == "__main__":
    main()
