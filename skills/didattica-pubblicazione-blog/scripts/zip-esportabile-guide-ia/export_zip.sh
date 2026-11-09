#!/usr/bin/env bash
# export_zip.sh — genera il pacchetto ZIP esportabile «repository GitHub pronta
# per agenti AI» dal commit HEAD di una qualsiasi app (Easy-Peasy AI).
#
# Uso:
#   ./export_zip.sh [cartella-repo] [file-output]
#
# Default:
#   repo  = argomento 1 (obbligatorio, es. /home/user/mia-app)
#   output= argomento 2 (opzionale; default: /home/user/<nome-cartella>-export-<DATA>.zip)
#
# Pre-requisiti:
#   - working tree COMMITTATO (lo ZIP nasce da HEAD: `git archive`)
#   - repository ripulita: niente .env, node_modules, dist/, .git, log,
#     script di sviluppo temporanei (test-*.ts in radice, scripts/ usa-e-getta)
#     — REBUILD.md §8 dichiara che la repo NON li contiene
set -euo pipefail

REPO="${1:?Uso: export_zip.sh <cartella-repo> [file-output]}"
BASE="$(basename "$REPO")"
OUT="${2:-/home/user/${BASE}-export-$(date +%F).zip}"

cd "$REPO"

echo "==> Stato git:"
git status --short
if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
  echo "ERRORE: working tree/staging non puliti. Esaminare le modifiche e salvare il checkpoint prima dell'export." >&2
  exit 2
fi
for required in README.md AGENTS.md REBUILD.md ADATTARE.md RENDER.md ACCESSIBILITA.md manifest.json package.json pnpm-lock.yaml .env.example render.yaml; do
  git cat-file -e "HEAD:$required" || { echo "ERRORE: manca $required nel commit." >&2; exit 3; }
done

echo "==> Export da HEAD con prefisso ${BASE}/"
OUT="$(realpath -m "$OUT")"
TMP="$(mktemp "${OUT}.tmp.XXXXXX")"
trap 'rm -f "$TMP"' EXIT
git archive --format=zip --prefix="${BASE}/" HEAD -o "$TMP"
unzip -t "$TMP" >/dev/null
mv "$TMP" "$OUT"

echo "==> ZIP creato: $OUT"
ls -la "$OUT"
unzip -t "$OUT" | tail -1
unzip -l "$OUT" | tail -2

echo "==> Controllo assenza file indesiderati:"
if unzip -l "$OUT" | grep -E "node_modules|/dist/|\.env$|\.git/|\.log$"; then
  echo "⚠️  Trovati file indesiderati — pulisci il tracking (git rm) prima di consegnare."
  exit 1
else
  echo "OK: nessun file indesiderato."
fi

echo "==> Guide IA e cornice dinamica presenti:"
unzip -l "$OUT" | grep -E "ACCESSIBILITA|ADATTARE|REBUILD|RENDER|AGENTS|README|manifest|cornice-dinamica/|render.yaml" | sed -n '1,25p'
echo "Dimensione reale in byte: $(stat -c '%s' "$OUT")"
sha256sum "$OUT"
echo "Fatto."
