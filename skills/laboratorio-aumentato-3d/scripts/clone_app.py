#!/usr/bin/env python3
"""
clone_app.py — Clona l'app LABORATORIO AUMENTATO 3D SORGENTE in una nuova app
identica, cambiando SOLO il contenuto dell'attività (tema, istruzioni, rubrica).

Supporta il clone da una cartella locale OPPURE da una repository GitHub.

Usage:
    # Da cartella locale (default: /home/user/laboratorio-visivo)
    python clone_app.py --dest /home/user/nuova-app --title "NUOVO TITOLO"

    # Da una repository GitHub (l'utente l'ha caricata su GitHub)
    python clone_app.py --source https://github.com/USER/REPO.git \
        --dest /home/user/nuova-app --title "NUOVO TITOLO"

    # Con personalizzazione completa dei contenuti (istruzioni + rubrica)
    python clone_app.py --dest /home/user/nuova-app --title "NUOVO TITOLO" \
        --config config.json

Vedi templates/config_esempio.json per il formato del config.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

# ── Sorgente di default ────────────────────────────────────────────────────
DEFAULT_SOURCE = "/home/user/laboratorio-visivo"

# Titolo attuale (due varianti di maiuscole presenti nel codice)
TITLE_UPPER = "LABORATORIO AUMENTATO 3D"
TITLE_CASE = "Laboratorio Aumentato 3D"

# Chiave localStorage attuale della lista classi docente
OLD_STORAGE_KEY = "laboratorio_audiovisivo_classes"

# Parole-tema sparse nel codice (sostituite globalmente in ogni clone).
# "spagnolo" → "lingua straniera" è il default corretto per qualsiasi nuovo tema
# (l'app sorgente aveva già uniformato StudentSubmit a "lingua straniera").
THEME_WORDS_DEFAULT = {
    "spagnolo": "lingua straniera",
}

# ── Mappa delle stringhe di contenuto VARIABILE ─────
# Le stringhe OLD sono quelle presenti nell'app sorgente. Il config fornisce
# solo i valori NUOVI; qui c'è il mapping old→new basato sulle chiavi.

STEPS = {
    "step3_desc": (
        "Caricate lo screenshot (o gli screenshot, fino a 3) della poesia in "
        "realtà aumentata posizionata nel luogo che avete scelto. L'immagine "
        "deve rappresentare il vostro lavoro creativo di collocazione della "
        "poesia nello spazio."
    ),
    "step4_desc": (
        "Scrivete una breve spiegazione (3-5 frasi) in cui descrivete: "
        "<strong>1)</strong> perché avete scelto proprio quel luogo per "
        "collocare la poesia, <strong>2)</strong> quale legame c'è tra lo "
        "spazio scelto e il significato della poesia, <strong>3)</strong> "
        "che effetto volevate ottenere con il vostro elaborato visivo."
    ),
    "step5_heading": "Lettura in lingua straniera",
    "step5_desc": (
        "Registrate e caricate un file audio (MP3) con la lettura espressiva "
        "della poesia in lingua straniera. Tutti i componenti del gruppo "
        "devono partecipare alla lettura, dividendosi le strofe. Curate la "
        "pronuncia e l'intonazione."
    ),
    "step5_label": "CARICA AUDIO LETTURA (MP3)",
    "step5_subtext": "Lettura espressiva della poesia in lingua straniera (tutti i componenti)",
    "step6_heading": "Spiegazione audio delle ragioni della foto",
    "step6_desc": (
        "Registrate e caricate un file audio (MP3) in cui spiegate a voce le "
        "ragioni della vostra scelta: perché avete collocato la poesia in "
        "quel luogo e cosa rappresenta per voi. Tutti i componenti del gruppo "
        "devono leggere almeno una frase della spiegazione."
    ),
    "step6_label": "CARICA AUDIO SPIEGAZIONE (MP3)",
    "step6_subtext": "Spiegazione orale: luogo e significato della scelta",
}

RUBRIC = {
    "pertinenzaTema": {
        "label": "1. Pertinenza al tema",
        "desc": "L'immagine scelta riflette adeguatamente il contenuto e le emozioni del poema?",
    },
    "originalita": {
        "label": "2. Originalità e creatività",
        "desc": "La composizione è originale? Dimostra un approccio creativo nella scelta del luogo e dell'inquadratura?",
    },
    "qualitaTecnica": {
        "label": "3. Qualità tecnica dell'elaborato audiovisivo",
        "desc": "Le catture sono nitide? La composizione visiva è curata?",
    },
    "qualitaLettura": {
        "label": "4. Qualità della lettura in spagnolo",
        "desc": "La pronuncia è corretta? L'intonazione è espressiva? Partecipano tutti i membri del gruppo?",
    },
    "rispettoTempi": {
        "label": "5. Rispetto dei tempi",
        "desc": "Il lavoro è stato consegnato entro il termine stabilito?",
    },
}


def bail(msg: str) -> None:
    print(f"❌ ERROR: {msg}")
    sys.exit(1)


def slugify(text: str) -> str:
    """Trasforma una stringa in uno slug ASCII minuscolo con underscore."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text or "nuova_app"


def is_github_url(source: str) -> bool:
    s = source.strip().lower()
    return s.startswith(("http://", "https://", "git@", "ssh://")) or "github.com" in s


def clone_source(source: str, dest: Path) -> None:
    """Clona la sorgente (cartella locale o repo GitHub) in dest."""
    if is_github_url(source):
        print(f"🌐 Clonazione da repository GitHub:\n   {source}\n")
        cmd = ["git", "clone", "--depth", "1", source, str(dest)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            bail(f"git clone fallito:\n{res.stderr.strip()}")
        # Rimuovi il .git per una copia pulita
        git_dir = dest / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)
        print("   ✔ Repository clonata e .git rimosso")
    else:
        src = Path(source).expanduser()
        if not src.exists() or not (src / "package.json").exists():
            bail(f"Sorgente locale non valida (manca package.json): {src}")
        print(f"📁 Copia da cartella locale:\n   {src}\n")
        dest.mkdir(parents=True, exist_ok=True)
        excludes = ["node_modules", ".git", "dist", ".vite", "dev-server.log"]
        # Uso tar per copiare preservando i permessi e saltando gli esclusi
        tar_cmd = ["tar", "cf", "-"]
        for e in excludes:
            tar_cmd += ["--exclude", e]
        tar_cmd += ["-C", str(src), "."]
        p1 = subprocess.Popen(tar_cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(
            ["tar", "xf", "-", "-C", str(dest)],
            stdin=p1.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        p1.stdout.close()
        _, err = p2.communicate()
        if p2.returncode != 0:
            bail(f"copia fallita:\n{err.decode()}")
        print("   ✔ Cartella copiata")


def replace_all(path: Path, replacements: list[tuple[str, str]]) -> int:
    """Applica una lista di (old, new) su un file; ritorna il numero di file modificati."""
    if not path.exists():
        print(f"   ⚠ file non trovato (saltato): {path.name}")
        return 0
    content = path.read_text(encoding="utf-8")
    original = content
    for old, new in replacements:
        if old and old in content:
            content = content.replace(old, new)
    if content != original:
        path.write_text(content, encoding="utf-8")
        return 1
    return 0


def apply_title(dest: Path, title: str) -> None:
    """Sostituisce il titolo (2 varianti di maiuscole) in tutti i file."""
    print("[2/5] Sostituzione del titolo …")
    targets = [
        dest / "client" / "index.html",
        dest / "client" / "src" / "pages" / "Home.tsx",
        dest / "client" / "src" / "pages" / "StudentSubmit.tsx",
        dest / "client" / "src" / "pages" / "TeacherDashboard.tsx",
    ]
    changed = 0
    for f in targets:
        changed += replace_all(f, [(TITLE_UPPER, title), (TITLE_CASE, title)])
    print(f"   ✔ Titolo aggiornato in {changed} file")


def apply_storage_key(dest: Path, slug: str) -> None:
    """Sostituisce la chiave localStorage con un prefisso univoco."""
    print("[3/5] Aggiornamento chiave localStorage …")
    path = dest / "client" / "src" / "pages" / "TeacherDashboard.tsx"
    new_key = f"{slug}_classes"
    n = replace_all(path, [(OLD_STORAGE_KEY, new_key)])
    if n:
        print(f"   ✔ Chiave → {new_key}")
    else:
        print(f"   ⚠ chiave '{OLD_STORAGE_KEY}' non trovata (verifica manuale)")


def apply_theme_words(dest: Path, theme_words: dict) -> None:
    """Sostituisce globalmente le parole-tema (es. spagnolo→lingua straniera).
    Gestisce le varianti di maiuscole: minuscola, Maiuscola, MAIUSCOLA."""
    print("[5/5] Sostituzione parole-tema (spagnolo→lingua straniera, …) …")
    scan_dirs = [dest / "client" / "src", dest / "server"]
    ext = {".ts", ".tsx", ".html"}
    for word, repl in theme_words.items():
        variants = [
            (word, repl),
            (word.capitalize(), repl.capitalize()),
            (word.upper(), repl.upper()),
        ]
        hit = 0
        for d in scan_dirs:
            if not d.exists():
                continue
            for f in d.rglob("*"):
                if f.suffix not in ext:
                    continue
                hit += replace_all(f, variants)
        print(f"   ✔ '{word}' → '{repl}' ({hit} file)")


def apply_content(dest: Path, config: dict) -> None:
    """Applica le modifiche di contenuto (istruzioni + rubrica) dal config."""
    print("[4/5] Personalizzazione contenuto (istruzioni + rubrica) …")
    student = dest / "client" / "src" / "pages" / "StudentSubmit.tsx"
    teacher = dest / "client" / "src" / "pages" / "TeacherDashboard.tsx"

    # ── Istruzioni dei passi ──
    steps_cfg = config.get("steps", {})
    for key, old in STEPS.items():
        if key in steps_cfg and steps_cfg[key]:
            replace_all(student, [(old, steps_cfg[key])])
            print(f"   ✔ step {key} aggiornato")

    # ── Rubrica (label mixed + uppercase + desc) ──
    rubric_cfg = config.get("rubric", [])
    by_key = {item.get("key"): item for item in rubric_cfg if isinstance(item, dict)}
    for key, old_map in RUBRIC.items():
        item = by_key.get(key)
        if not item:
            continue
        new_label = item.get("label")
        new_desc = item.get("desc")
        if new_label:
            # label mixed (UI) e label uppercase (PDF report + rubrica bianca)
            replace_all(teacher, [
                (old_map["label"], new_label),
                (old_map["label"].upper(), new_label.upper()),
            ])
            print(f"   ✔ rubrica {key} label aggiornata")
        if new_desc:
            replace_all(teacher, [(old_map["desc"], new_desc)])
            print(f"   ✔ rubrica {key} desc aggiornata")

    # ── Meta description (opzionale) ──
    if config.get("meta_description"):
        index = dest / "client" / "index.html"
        if index.exists():
            html = index.read_text(encoding="utf-8")
            html = re.sub(
                r'<meta name="description" content="[^"]*"\s*/>',
                f'<meta name="description" content="{config["meta_description"]}" />',
                html,
            )
            index.write_text(html, encoding="utf-8")
            print("   ✔ meta description aggiornata")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clona LABORATORIO AUMENTATO 3D SORGENTE")
    parser.add_argument("--source", default=DEFAULT_SOURCE,
                        help="Cartella locale o URL GitHub (default: %(default)s)")
    parser.add_argument("--dest", required=True,
                        help="Directory della nuova app (es. /home/user/nuova-app)")
    parser.add_argument("--title", required=True,
                        help="Nuovo titolo visualizzato (es. LABORATORIO DI STORIA)")
    parser.add_argument("--slug", default=None,
                        help="Prefisso chiave localStorage (default: derivato da --dest)")
    parser.add_argument("--config", default=None,
                        help="JSON opzionale con istruzioni e rubrica (vedi templates/)")
    args = parser.parse_args()

    dest = Path(args.dest).expanduser()
    if dest.exists() and any(dest.iterdir()):
        bail(f"La directory di destinazione non è vuota: {dest}")

    config = {}
    if args.config:
        cfg_path = Path(args.config)
        if not cfg_path.exists():
            bail(f"Config non trovato: {cfg_path}")
        config = json.loads(cfg_path.read_text(encoding="utf-8"))

    slug = args.slug or slugify(dest.name)

    print(f"\n🚀 Clonazione di LABORATORIO AUMENTATO 3D SORGENTE")
    print(f"   Destinazione: {dest}")
    print(f"   Nuovo titolo: {args.title}\n")

    # 1. Clone
    print("[1/5] Copia della sorgente …")
    clone_source(args.source, dest)

    # 2. Titolo
    apply_title(dest, args.title)

    # 3. Chiave localStorage
    apply_storage_key(dest, slug)

    # 4. Contenuto (opzionale) — PRIMA delle parole-tema: così la rubrica
    #    "…in spagnolo" viene sostituita dal config PRIMA della conversione
    #    globale spagnolo→lingua straniera (altrimenti il match fallirebbe).
    if config:
        apply_content(dest, config)

    # 5. Parole-tema (sempre)
    theme_words = dict(THEME_WORDS_DEFAULT)
    theme_words.update(config.get("theme_words", {}))
    apply_theme_words(dest, theme_words)

    print("\n✅ Clone completato!\n")
    print("Prossimi passi:")
    print(f"  1. cd {dest}")
    print("  2. pnpm install")
    print("  3. pnpm check       (verifica TypeScript)")
    print("  4. pnpm build       (build produzione)")
    print("  5. Controlla che non restino stringhe del tema vecchio:")
    print('     grep -rn "poesia\\|spagnolo\\|realtà aumentata" client/src server/')
    print("\n   Poi deploy preview/produzione con gli strumenti webdev_*.\n")


if __name__ == "__main__":
    main()
