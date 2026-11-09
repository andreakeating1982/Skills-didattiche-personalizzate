#!/usr/bin/env python3.11
"""Scaffold: crea la cartella di build di un nuovo quaderno di mappe per una lingua.

Uso:
    python nuovo_quaderno.py <codice-lingua> --titolo "MAPPE CONCETTUALI DI GRAMMATICA FRANCESE" [--dest DIR]

- codice-lingua: codice ISO breve (fr, es, en, de, ...)
- copia icons/ (85 icone clay) e fonts/ nella cartella di destinazione
- installa OpenDyslexic in ~/.fonts (necessario a WeasyPrint)
- genera build_<codice>.py dal template con titolo e codice sostituiti
- crea media/ (dove salvare la copertina cover.png)

Esempio:
    python nuovo_quaderno.py fr --titolo "MAPPE CONCETTUALI DI GRAMMATICA FRANCESE"
"""
import argparse, os, shutil, subprocess, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("codice", help="codice ISO della lingua (fr, es, en, de...)")
    ap.add_argument("--titolo", required=True, help="titolo del quaderno, es. MAPPE CONCETTUALI DI GRAMMATICA FRANCESE")
    ap.add_argument("--dest", default=None, help="cartella di build (default: /home/user/mappe-<codice>)")
    a = ap.parse_args()
    cod = a.codice.lower()
    dest = os.path.abspath(a.dest or f"/home/user/mappe-{cod}")

    os.makedirs(dest, exist_ok=True)
    for d in ("icons", "fonts"):
        tgt = os.path.join(dest, d)
        if os.path.exists(tgt):
            shutil.rmtree(tgt)
        shutil.copytree(os.path.join(SKILL, "templates", d), tgt)
    os.makedirs(os.path.join(dest, "media"), exist_ok=True)

    # installa i font per WeasyPrint
    fonts_dst = os.path.expanduser("~/.fonts")
    os.makedirs(fonts_dst, exist_ok=True)
    for f in os.listdir(os.path.join(dest, "fonts")):
        shutil.copy(os.path.join(dest, "fonts", f), fonts_dst)
    subprocess.run(["fc-cache", "-f"], capture_output=True)

    nome_file = f"mappe_{cod}.html"
    with open(os.path.join(SKILL, "templates", "build_template.py"), encoding="utf-8") as f:
        tpl = f.read()
    build = (tpl.replace("{{TITOLO}}", a.titolo)
                .replace("{{CODICE}}", cod)
                .replace("{{NOME_FILE}}", nome_file))
    build_path = os.path.join(dest, f"build_{cod}.py")
    with open(build_path, "w", encoding="utf-8") as f:
        f.write(build)

    print(f"Cartella di build pronta: {dest}")
    print(f"  - build script: {build_path}  (sostituisci il contenuto tra i marcatori INIZIO/FINE CONTENUTO)")
    print(f"  - copertina:    {dest}/media/cover.png  (da generare, vedi references/semplificazione.md)")
    print("Prossimi passi:")
    print(f"  1. compila il contenuto in {os.path.basename(build_path)}")
    print(f"  2. python {os.path.basename(build_path)}")
    print(f"  3. python {SKILL}/scripts/render_quaderno.py {nome_file} Quaderno_{cod}.pdf --base {dest}")
    print(f"  4. python {SKILL}/scripts/verify_quaderno.py Quaderno_{cod}.pdf")

if __name__ == "__main__":
    sys.exit(main())
