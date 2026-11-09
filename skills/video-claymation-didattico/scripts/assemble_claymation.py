#!/usr/bin/env python3
"""Assembla il video claymation con ffmpeg a partire dal piano delle scene.

Ogni clip viene tagliato (trim) o leggermente rallentato (setpts) per durare
esattamente quanto il segmento narrato; poi normalizzato a 1280x720@24 e
concatenato. La narrazione è l'unica traccia audio. Nessun testo sovraimpresso.

Uso:
  python3 assemble_claymation.py --plan clips_plan.json --clips clips_v2 \
      --audio narrazione.m4a --out video_finale.mp4 [--captions-dir /tmp/cap]

Con --captions-dir le didascalie del piano vengono bruciate in alto
(versione con testi); senza, nessun testo (consigliato per il montaggio finale).

Parametri di default (verificati sul progetto di riferimento):
  1280x720, 24 fps, libx264 crf 19, aac 192k 48 kHz stereo,
  fade in 0.5 s, fade out 0.7 s, +faststart, -shortest.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)], text=True).strip()
    return float(out)


def esc(t: str) -> str:
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%")


def main() -> None:
    ap = argparse.ArgumentParser(description="Assembla il video claymation con ffmpeg")
    ap.add_argument("--plan", required=True, help="clips_plan.json (output di plan_scene.py)")
    ap.add_argument("--clips", required=True, help="Cartella dei clip clipNN.mp4")
    ap.add_argument("--audio", required=True, help="File della narrazione")
    ap.add_argument("--out", required=True, help="File video di output")
    ap.add_argument("--captions-dir", default=None, help="Se impostata, brucia le didascalie")
    ap.add_argument("--fade-in", type=float, default=0.5)
    ap.add_argument("--fade-out", type=float, default=0.7)
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    clips_dir = Path(args.clips)
    audio = Path(args.audio)
    n = len(plan)

    cap_dir = Path(args.captions_dir) if args.captions_dir else None
    if cap_dir:
        cap_dir.mkdir(exist_ok=True)

    total = 0.0
    filters: list[str] = []
    labels: list[str] = []
    inputs: list[str] = []

    for i, c in enumerate(plan):
        p = clips_dir / f"{c['id']}.mp4"
        inputs += ["-i", str(p)]
        dn = probe_duration(p)
        target = c["dur"]
        total += target

        if target <= dn + 0.05:
            vf = f"[{i}:v]trim=0:{target:.3f},setpts=PTS-STARTPTS"
        else:
            vf = f"[{i}:v]setpts=PTS*({target:.3f}/{dn:.3f})"

        if cap_dir:
            tf = cap_dir / f"{c['id']}.txt"
            tf.write_text(c["caption"], encoding="utf-8")
            vf += (f",drawtext=fontfile={FONT}:textfile={tf}:fontsize=30:"
                   f"fontcolor=white:box=1:boxcolor=black@0.35:boxborderw=8:"
                   f"x=(w-text_w)/2:y=20:enable='between(t,0.25,{target:.3f}-0.2)'")

        vf += f",scale=1280:720:flags=lanczos,fps=24,format=yuv420p,setsar=1[v{i}]"
        filters.append(vf)
        labels.append(f"[v{i}]")

    fade_out_start = max(0.0, total - args.fade_out)
    filters.append(
        "".join(labels) + f"concat=n={n}:v=1:a=0,"
        f"fade=t=in:st=0:d={args.fade_in},fade=t=out:st={fade_out_start:.3f}:d={args.fade_out}[vout]"
    )
    filters.append(f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]")

    cmd = [
        "ffmpeg", "-y", *inputs, "-i", str(audio),
        "-filter_complex", ";".join(filters),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-r", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", "-shortest", str(args.out),
    ]
    print(f"clip={n} target_total={total:.3f}s audio={probe_duration(audio):.3f}s")
    print("ffmpeg assemble in corso...")
    subprocess.check_call(cmd)
    print("DONE", args.out)


if __name__ == "__main__":
    main()
