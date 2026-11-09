#!/usr/bin/env bash
# export_zip.sh — genera il pacchetto ZIP esportabile di «Latino Facile»
# (repository GitHub pronta per agenti AI) dal commit HEAD della repo.
#
# Uso:
#   ./export_zip.sh [cartella-repo] [file-output]
#
# Default:
#   repo  = /home/user/latino-facile-app
#   output= /home/user/latino-facile-app-export-aggiornato-$(date +%F).zip
#
# Pre-requisiti:
#   - working tree COMMITTATO (git add -A && git commit) — lo ZIP nasce da HEAD
#   - nessun file indesiderato tracciato: .env, node_modules, dist/, .git,
#     log, script di sviluppo temporanei (test-*.ts in radice, scripts/ usa-e-getta)
#     → REBUILD.md §8 dichiara che la repo NON li contiene
set -euo pipefail

REPO="${1:-/home/user/latino-facile-app}"
OUT="${2:-/home/user/latino-facile-app-export-aggiornato-$(date +%F).zip}"

cd "$REPO"

echo "==> Stato git:"
git status --short
if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
  echo "ERRORE: working tree/staging non puliti. Verificare i cambiamenti e salvare il checkpoint prima dell'export." >&2
  exit 2
fi
for required in README.md AGENTS.md REBUILD.md ADATTARE.md RENDER.md ACCESSIBILITA.md OCR-FOTO.md SCROLLING-MOBILE.md manifest.json package.json pnpm-lock.yaml .env.example render.yaml .github/workflows/ci.yml Dockerfile client/src/components/CropDialog.tsx client/src/hooks/useCropDialogViewport.ts client/src/lib/heightSync.ts tests/crop-mobile.e2e.mjs tests/crop-drag.e2e.mjs PHOTO-CROP-CLONABILE.md; do
  git cat-file -e "HEAD:$required" || { echo "ERRORE: manca $required nel commit." >&2; exit 3; }
done

echo "==> Export da HEAD con prefisso latino-facile-app/"
OUT="$(realpath -m "$OUT")"
TMP="$(mktemp "${OUT}.tmp.XXXXXX")"
trap 'rm -f "$TMP"' EXIT
git archive --format=zip --prefix=latino-facile-app/ HEAD -o "$TMP"
unzip -t "$TMP" >/dev/null
mv "$TMP" "$OUT"

echo "==> ZIP creato: $OUT"
ls -la "$OUT"
unzip -t "$OUT" | tail -1
unzip -l "$OUT" | tail -2

echo "==> Controllo assenza file indesiderati:"
if unzip -l "$OUT" | grep -E "node_modules|/dist/|\.env$|\.git/|\.log$"; then
  echo "⚠️  Trovati file indesiderati — controlla il tracking (git rm) prima di consegnare."
  exit 1
else
  echo "OK: nessun file indesiderato."
fi

echo "==> Documenti chiave presenti:"
unzip -l "$OUT" | grep -E "ACCESSIBILITA|ADATTARE|REBUILD|RENDER|AGENTS|README|manifest|cornice-dinamica/|useCropDialogViewport|crop-mobile.e2e" | sed -n '1,25p'
echo "Dimensione reale in byte: $(stat -c '%s' "$OUT")"
sha256sum "$OUT"
echo "Verificare anche hash di sorgenti/asset con scripts/verify_export.py. Fatto."
