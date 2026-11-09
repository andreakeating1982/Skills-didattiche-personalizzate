#!/usr/bin/env python3
"""Estrae fotogrammi di controllo (QA) a timestamp precisi e crea un foglio
di verifica unico (contact sheet) con i timestamp gialli, come nel progetto
claymation di riferimento (qa_finale.jpg, verify_const_final.jpg, ...).

Uso:
  python3 qa_frames.py video.mp4 --times 78.5,80,82,84,86,87 --out verify.jpg

Ogni fotogramma è un frame chiave dove l'IA potrebbe aver inserito testi
(documenti, giornali, bandiere, insegne) o dove serve controllare la scena.
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    ap = argparse.ArgumentParser(description="Foglio QA con frame estratti a timestamp")
    ap.add_argument("video", help="File video da ispezionare")
    ap.add_argument("--times", required=True, help="Timestamp separati da virgola, es. 78.5,80,82,84,86,87")
    ap.add_argument("--out", default="qa_foglio.jpg", help="Immagine di output")
    ap.add_argument("--cols", type=int, default=3, help="Colonne della griglia")
    args = ap.parse_args()

    times = [float(t) for t in args.times.split(",") if t.strip()]
    video = Path(args.video)

    tmp = Path(tempfile.mkdtemp(prefix="qa_frames_"))
    frames: list[Image.Image] = []
    for t in times:
        out = tmp / f"f_{t}.jpg"
        subprocess.check_call(
            ["ffmpeg", "-y", "-ss", str(t), "-i", str(video),
             "-frames:v", "1", "-q:v", "2", str(out)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        frames.append(Image.open(out).convert("RGB"))

    w, h = frames[0].size
    cols = args.cols
    rows = (len(frames) + cols - 1) // cols
    pad, tag_h = 8, 26
    sheet = Image.new("RGB", (cols * w + (cols + 1) * pad, rows * (h + tag_h) + (rows + 1) * pad), "#202020")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception:
        font = ImageFont.load_default()

    for k, (t, img) in enumerate(zip(times, frames)):
        r, c = divmod(k, cols)
        x = pad + c * (w + pad)
        y = pad + r * (h + tag_h + pad)
        sheet.paste(img, (x, y))
        draw.text((x + 4, y + h + 4), f"t={t}s", fill="#FFD700", font=font)

    sheet.save(args.out, quality=92)
    print("QA sheet:", args.out, sheet.size, f"({len(frames)} frame)")


if __name__ == "__main__":
    main()
