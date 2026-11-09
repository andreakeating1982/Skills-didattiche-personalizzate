#!/usr/bin/env bash
# Normalizzazione loudness EBU R128 per i file MP3 delle circolari (skill circolari-audio).
# Uso: normalizza_audio.sh file1.mp3 [file2.mp3 ...]
#
# Target FISSO, identico per ogni file prodotti dalla skill, così che TUTTI gli
# MP3 consegnati abbiano lo stesso volume percepito:
#   Integrated loudness (I)  = -16 LUFS
#   True Peak (TP)           = -1.5 dBTP
#   Loudness Range (LRA)     = 11 LU
#
# Uso la normalizzazione in DUE PASSATE (misura + applicazione lineare), che
# preserva la dinamica naturale della voce meglio della modalità dinamica.
# In coda: ricodifica MP3 44100 Hz stereo qualità alta.
set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ERRORE: ffmpeg non installato (sudo apt-get install -y ffmpeg)" >&2
  exit 1
fi

TARGET_I="-16"; TARGET_TP="-1.5"; TARGET_LRA="11"

for f in "$@"; do
  if [ ! -f "$f" ]; then echo "File non trovato: $f" >&2; exit 1; fi

  # Passata 1: misura loudness
  analysis=$(ffmpeg -hide_banner -nostats -i "$f" \
    -af "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=${TARGET_LRA}:print_format=json" \
    -f null - 2>&1 | sed -n '/^{/,/^}/p')

  measured_I=$(echo "$analysis"  | grep '"input_i"'      | head -1 | cut -d: -f2 | tr -d ' ",')
  measured_TP=$(echo "$analysis" | grep '"input_tp"'     | head -1 | cut -d: -f2 | tr -d ' ",')
  measured_LRA=$(echo "$analysis"| grep '"input_lra"'    | head -1 | cut -d: -f2 | tr -d ' ",')
  measured_th=$(echo "$analysis" | grep '"input_thresh"' | head -1 | cut -d: -f2 | tr -d ' ",')
  offset=$(echo "$analysis"      | grep '"target_offset"'| head -1 | cut -d: -f2 | tr -d ' ",')
  [ -n "$offset" ] || offset="0"

  tmp="${f%.mp3}.__norm_tmp__.mp3"
  # Passata 2: applicazione con valori misurati (linear=true)
  ffmpeg -y -hide_banner -loglevel error -i "$f" \
    -af "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=${TARGET_LRA}:measured_I=${measured_I}:measured_TP=${measured_TP}:measured_LRA=${measured_LRA}:measured_thresh=${measured_th}:offset=${offset}:linear=true" \
    -ar 44100 -ac 2 -c:a libmp3lame -q:a 2 "$tmp"
  mv "$tmp" "$f"

  echo "OK normalizzato (I=${TARGET_I} LUFS, TP=${TARGET_TP} dBTP): $f"
done
