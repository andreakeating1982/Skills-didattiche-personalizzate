#!/usr/bin/env python3
"""
clone_app.py — Clona l'app IMMAGINE INTERATTIVA SORGENTE in una NUOVA app
identica, cambiando SOLO il contenuto (paragrafi, parole chiave, audio,
immagine di sfondo e titoli) e lasciando invariato tutto il resto:
dashboard docente, codici classe a 4 cifre, sessioni, contatore studenti,
report PDF (una pagina per studente + box PUNTEGGIO), palette plum/gold e
embed iframe.

Due modalità:

  1) --dump    Estrae il contenuto corrente dell'app sorgente e scrive un
                file JSON (contenuto.json) pronto da modificare.

  2) (default) Clona l'app sorgente in una nuova cartella applicando il
                contenuto del JSON.

Esempi:

  # 1. Estrai il contenuto corrente come punto di partenza
  python3 clone_app.py --dump -o contenuto.json

  # 2. Clona con il nuovo contenuto
  python3 clone_app.py --json contenuto.json --name mio-nuovo-argomento

  # 3. Clona da un repository GitHub
  python3 clone_app.py --json contenuto.json \
      --source https://github.com/user/repo.git --name mio-nuovo-argomento
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_SOURCE = "/home/user/romanticismo-mappa-concettuale"

# Directory/files da NON copiare nella nuova app.
EXCLUDE_DIRS = {"node_modules", ".git", "dist", ".db", ".cache", ".DS_Store"}
EXCLUDE_FILES = {".env", "dev-server.log"}


# =============================================================================
# Helpers generici
# =============================================================================

def die(msg: str) -> None:
    print(f"\n[ERRORE] {msg}\n", file=sys.stderr)
    sys.exit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def from_ts_unescaped(s: str) -> str:
    """Converte escape letterali \\n del sorgente TS in newline reali."""
    return s.replace("\\n", "\n")


def js_string_literal(value: str) -> str:
    """Ritorna value come stringa TS tra doppi apici (JSON-like)."""
    return json.dumps(value, ensure_ascii=False)


def slugify(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower() or "app"


def resolve_source(source: str) -> Path:
    """Ritorna un Path locale della sorgente; clona da git se serve."""
    if source.startswith(("http://", "https://", "git@", "ssh://")):
        tmp = tempfile.mkdtemp(prefix="clone_src_")
        print(f"[git] clonando {source} ...")
        r = subprocess.run(["git", "clone", "--depth", "1", source, tmp],
                           capture_output=True, text=True)
        if r.returncode != 0:
            die(f"git clone fallito: {r.stderr.strip()}")
        return Path(tmp)
    p = Path(source).expanduser().resolve()
    if not p.exists():
        die(f"Sorgente non trovata: {p}")
    return p


def copy_project(src: Path, dst: Path) -> None:
    """Copia la cartella del progetto escludendo node_modules/.git/dist/ecc."""
    def ignore(dirpath, names):
        base = os.path.basename(dirpath)
        ignored = set()
        for n in names:
            full = os.path.join(dirpath, n)
            if os.path.isdir(full):
                if n in EXCLUDE_DIRS:
                    ignored.add(n)
            else:
                if n in EXCLUDE_FILES:
                    ignored.add(n)
                elif n.endswith(".zip"):
                    ignored.add(n)
        return ignored

    print(f"[copia] {src} -> {dst}")
    shutil.copytree(src, dst, ignore=ignore)


# =============================================================================
# Generazione dei 3 file di DATI a partire dal JSON contenuto
# =============================================================================

def _gen_schema_data(c: dict) -> str:
    app = c["app"]
    paras = c["paragraphs"]
    all_kw = [kw for p in paras for kw in p["slots"]]
    total = len(all_kw)

    L = []
    L.append("/**")
    L.append(" * Schema data for the interactive concept map.")
    L.append(" * Used by both db.ts (for reports) and routers.ts (for the API).")
    L.append(" *")
    L.append(f" * {len(paras)} paragraphs from the audio/text:")
    for p in paras:
        L.append(f" *   {p['label']}")
    L.append(" *")
    L.append(f" * {total} keywords total, distributed across the {len(paras)} paragraphs.")
    L.append(" */")
    L.append("")
    L.append("export interface ParagraphRow {")
    L.append("  id: string;")
    L.append("  paragraphLabel: string;")
    L.append("  paragraphSubtitle: string;")
    L.append("  color: string;")
    L.append("  slots: string[];")
    L.append("  /** Audio timestamp where this paragraph ends (seconds). Audio auto-stops here. */")
    L.append("  audioStopAt: number;")
    L.append("}")
    L.append("")
    L.append("export interface MapSlot {")
    L.append("  id: string;")
    L.append("  rowId: string;")
    L.append("  paragraphLabel: string;")
    L.append("  paragraphSubtitle: string;")
    L.append("  paragraphColor: string;")
    L.append("  correctAnswer: string;")
    L.append("  options: string[];")
    L.append("}")
    L.append("")
    L.append(f"export const TOTAL_SLOTS = {total};")
    L.append("")
    L.append(f"/**\n * All {total} correct keywords — one pool for all {len(paras)} paragraphs.\n */")
    L.append("export const ALL_KEYWORDS: string[] = [")
    for kw in all_kw:
        L.append(f"  {js_string_literal(kw)},")
    L.append("];")
    L.append("")
    L.append("/**\n * The paragraph rows of the concept map.\n * audioStopAt values come from the transcription timestamps.\n */")
    L.append("export const PARAGRAPH_ROWS: ParagraphRow[] = [")
    for p in paras:
        L.append("  {")
        L.append(f"    id: {js_string_literal(p['id'])},")
        L.append(f"    paragraphLabel: {js_string_literal(p['label'])},")
        L.append(f"    paragraphSubtitle: {js_string_literal(p['subtitle'])},")
        L.append(f"    color: {js_string_literal(p['color'])},")
        slots = ", ".join(js_string_literal(s) for s in p["slots"])
        L.append(f"    slots: [{slots}],")
        L.append(f"    audioStopAt: {p['audioStopAt']},")
        L.append("  },")
    L.append("];")
    L.append("")
    # Funzioni costanti (copiate verbatim dalla sorgente)
    L.append("""/**
 * Fisher-Yates shuffle.
 */
export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Order-free validation: given a list of slot entries for one paragraph
 * and the paragraph's expected keywords, returns the set of slotIds considered correct.
 * Each expected keyword is matched at most once — first available slot wins.
 */
export function computeCorrectSlotIds(
  slotEntries: { slotId: string; selectedKeyword: string | null }[],
  expectedKeywords: string[]
): Set<string> {
  const remaining = new Set(expectedKeywords);
  const correctIds = new Set<string>();
  for (const { slotId, selectedKeyword } of slotEntries) {
    if (selectedKeyword && remaining.has(selectedKeyword)) {
      correctIds.add(slotId);
      remaining.delete(selectedKeyword);
    }
  }
  return correctIds;
}

/**
 * Build the flattened list of interactive map slots.
 * Each student gets a shuffled keyword pool.
 */
export function buildMapSlots(): MapSlot[] {
  const keywordsForAllSlots = shuffle(ALL_KEYWORDS);
  return PARAGRAPH_ROWS.flatMap((row) =>
    row.slots.map((keyword, idx) => ({
      id: `${row.id}-slot-${idx}`,
      rowId: row.id,
      paragraphLabel: row.paragraphLabel,
      paragraphSubtitle: row.paragraphSubtitle,
      paragraphColor: row.color,
      correctAnswer: keyword,
      options: keywordsForAllSlots,
    }))
  );
}
""")
    return "\n".join(L)


def _gen_audio_data(c: dict) -> str:
    app = c["app"]
    audio = c["audio"]
    segs = c["segments"]
    L = []
    L.append("// =============================================================================")
    L.append(f"// DATI AUDIO SEGMENTATI — {app['title']}")
    L.append("// I segmenti corrispondono ai paragrafi della mappa concettuale.")
    L.append("// L'audio si stoppa automaticamente alla fine di ogni segmento.")
    L.append("// =============================================================================")
    L.append("")
    L.append("export interface AudioSegment {")
    L.append("  id: number;")
    L.append("  title: string;")
    L.append("  text: string;")
    L.append("  startTime: number; // secondi")
    L.append("  endTime: number;   // secondi")
    L.append("}")
    L.append("")
    L.append("export interface AudioTrack {")
    L.append("  id: string;")
    L.append("  title: string;")
    L.append("  src: string;")
    L.append("  segments: AudioSegment[];")
    L.append("}")
    L.append("")
    L.append("const SEGMENTS: AudioSegment[] = [")
    for i, s in enumerate(segs):
        L.append(f"  {{ id: {i}, title: {js_string_literal(s['title'])}, text: {js_string_literal(s['text'])}, startTime: {s['startTime']}, endTime: {s['endTime']} }},")
    L.append("];")
    L.append("")
    L.append("export const AUDIO_TRACKS: Record<string, AudioTrack> = {")
    L.append(f"  {js_string_literal(audio['trackId'])}: {{")
    L.append(f"    id: {js_string_literal(audio['trackId'])},")
    L.append(f"    title: {js_string_literal(audio['trackTitle'])},")
    L.append(f"    src: {js_string_literal(audio['src'])},")
    L.append("    segments: SEGMENTS,")
    L.append("  },")
    L.append("};")
    L.append("")
    return "\n".join(L)


def _gen_concept_map_positions(c: dict) -> str:
    app = c["app"]
    paras = c["paragraphs"]
    m = c["map"]

    # Appiattisce (keyword, rowId) in ordine per associarli alle posizioni.
    flat = [(p["id"], kw) for p in paras for kw in p["slots"]]
    slots = m["slots"]
    boxes = m["paraBoxes"]
    if len(flat) != len(slots):
        die(f"Mismatch slot: {len(flat)} parole chiave ma {len(slots)} posizioni in map.slots.")
    if len(paras) != len(boxes):
        die(f"Mismatch paragrafi: {len(paras)} paragrafi ma {len(boxes)} posizioni in map.paraBoxes.")

    L = []
    L.append("/**")
    L.append(f" * Pixel positions of concept map slots within the {m['imgW']}×{m['imgH']} template image.")
    L.append(" * Used by PDF generators and the student-page concept map overlay.")
    L.append(" */")
    L.append(f"export const IMG_W = {m['imgW']};")
    L.append(f"export const IMG_H = {m['imgH']};")
    L.append("")
    L.append("export interface SlotPos {")
    L.append("  slotId: string;")
    L.append("  rowId: string;")
    L.append("  keyword: string;       // correct keyword for this slot")
    L.append("  cx: number;            // center X in image pixels")
    L.append("  cy: number;            // center Y in image pixels")
    L.append("  w: number;             // box width")
    L.append("  h: number;             // box height")
    L.append("}")
    L.append("")
    L.append(f"/** All {len(flat)} keyword-slot positions (detected from the template image). */")
    L.append("export const CONCEPT_MAP_SLOTS: SlotPos[] = [")
    para_idx = {}
    for i, (row_id, kw) in enumerate(flat):
        idx = para_idx.get(row_id, 0)
        para_idx[row_id] = idx + 1
        s = slots[i]
        L.append(f"  {{ slotId: {js_string_literal(f'{row_id}-slot-{idx}')}, rowId: {js_string_literal(row_id)}, keyword: {js_string_literal(kw)}, cx: {s['cx']}, cy: {s['cy']}, w: {s['w']}, h: {s['h']} }},")
    L.append("];")
    L.append("")
    L.append("/** Paragraph branch-box centres (where the paragraph title is shown). */")
    L.append("export interface ParaBox { rowId: string; label: string; cx: number; cy: number; w: number; h: number; color: string; }")
    L.append("export const PARA_BOXES: ParaBox[] = [")
    for i, p in enumerate(paras):
        b = boxes[i]
        L.append(f"  {{ rowId: {js_string_literal(p['id'])}, label: {js_string_literal(b['label'])}, cx: {b['cx']}, cy: {b['cy']}, w: {b['w']}, h: {b['h']}, color: {js_string_literal(p['color'])} }},")
    L.append("];")
    L.append("")
    hub = m["hub"]
    L.append(f"/** Central hub */")
    L.append(f"export const HUB = {{ cx: {hub['cx']}, cy: {hub['cy']}, w: {hub['w']}, h: {hub['h']} }};")
    L.append(f"export const HUB_TITLE = {js_string_literal(app['hubTitle'])};")
    L.append("")
    L.append("""/**
 * Given a placement of the template image in PDF millimetres (imgX, imgY, imgW, imgH),
 * returns the PDF (x, y) centre for a slot in image-pixel coordinates.
 */
export function toPdfCoords(
  px: number, py: number,
  imgX: number, imgY: number, imgW: number, imgH: number,
): [number, number] {
  const sx = imgW / IMG_W;
  const sy = imgH / IMG_H;
  return [imgX + px * sx, imgY + py * sy];
}
""")
    return "\n".join(L)


# =============================================================================
# Sostituzioni mirate sui file non-dati
# =============================================================================

def _apply_pdf_replacements(pdf_path: Path, c: dict) -> None:
    txt = read_text(pdf_path)
    app = c["app"]
    slug = app["pdfSlug"]
    # Titoli in testa ai PDF Mappa Completa e Mappa in Bianco
    txt = re.sub(
        r'doc\.text\("MAPPA CONCETTUALE — [^"]*", PW / 2',
        lambda m: f'doc.text("{app["pdfTitle"]}", PW / 2',
        txt,
    )
    txt = re.sub(
        r'doc\.text\("MAPPA CONCETTUALE IN BIANCO — [^"]*", PW / 2',
        lambda m: f'doc.text("{app["pdfBlankTitle"]}", PW / 2',
        txt,
    )
    # Prefissi dei nomi file
    txt = txt.replace("Report_Mappa_Romanticismo_", f"Report_Mappa_{slug}_")
    txt = txt.replace("Mappa_Completa_Romanticismo_", f"Mappa_Completa_{slug}_")
    txt = txt.replace("Mappa_Bianco_Romanticismo_", f"Mappa_Bianco_{slug}_")
    write_text(pdf_path, txt)


def _apply_index_html_title(index_path: Path, c: dict) -> None:
    txt = read_text(index_path)
    txt = re.sub(r"<title>[^<]*</title>", f"<title>{c['app']['title']}</title>", txt, count=1)
    write_text(index_path, txt)


def _apply_home_title(home_path: Path, c: dict) -> None:
    txt = read_text(home_path)
    # Il titolo principale in Home.tsx è dentro <h1 ...> ... </h1>
    txt = re.sub(
        r"(<h1[^>]*>\s*)[^<\n]+(\s*</h1>)",
        lambda mm: mm.group(1) + c["app"]["title"].upper() + mm.group(2),
        txt,
        count=1,
    )
    write_text(home_path, txt)


def _apply_audio_track_ref(teacher_path: Path, c: dict) -> None:
    txt = read_text(teacher_path)
    txt = txt.replace("AUDIO_TRACKS.romanticismo", f"AUDIO_TRACKS.{c['audio']['trackId']}")
    write_text(teacher_path, txt)


def _apply_paragraph_count_robustness(root: Path) -> None:
    """Sostituisce gli hardcode `4` (numero paragrafi) con PARAGRAPH_ROWS.length."""
    teacher = root / "client/src/pages/TeacherPage.tsx"
    student = root / "client/src/pages/StudentMapPage.tsx"
    db = root / "server/db.ts"

    t = read_text(teacher)
    t = t.replace("currentParagraph <= 4", "currentParagraph <= PARAGRAPH_ROWS.length")
    t = t.replace("currentParagraph >= 4", "currentParagraph >= PARAGRAPH_ROWS.length")
    t = t.replace("PARAGRAFO {currentParagraph}/4", "PARAGRAFO {currentParagraph}/{PARAGRAPH_ROWS.length}")
    write_text(teacher, t)

    s = read_text(student)
    s = s.replace("currentParagraph <= 4", "currentParagraph <= PARAGRAPH_ROWS.length")
    write_text(student, s)

    d = read_text(db)
    d = d.replace("if (next > 4) throw", "if (next > PARAGRAPH_ROWS.length) throw")
    write_text(db, d)


def _apply_package_name(root: Path, c: dict) -> None:
    pkg = root / "package.json"
    txt = read_text(pkg)
    data = json.loads(txt)
    data["name"] = c["app"]["name"]
    write_text(pkg, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def _copy_media(root: Path, c: dict) -> None:
    pub = root / "client/public"
    audio_file = c["audio"].get("file") or ""
    if audio_file:
        src = Path(audio_file).expanduser()
        if not src.exists():
            die(f"File audio non trovato: {src}")
        shutil.copy2(src, pub / "audio.m4a")
        print(f"[media] audio copiato -> client/public/audio.m4a")

    image_file = (c.get("image") or {}).get("file") or ""
    if image_file:
        src = Path(image_file).expanduser()
        if not src.exists():
            die(f"Immagine non trovata: {src}")
        shutil.copy2(src, pub / "mappa-vuota.png")
        print(f"[media] immagine copiata -> client/public/mappa-vuota.png")


# =============================================================================
# DUMP — estrazione del contenuto corrente dalla sorgente
# =============================================================================

def dump_content(src: Path) -> dict:
    schema = read_text(src / "server/schema-data.ts")
    audio = read_text(src / "client/src/lib/audioData.ts")
    positions = read_text(src / "client/src/lib/conceptMapPositions.ts")
    pdf = read_text(src / "client/src/lib/reportPdf.ts")
    index = read_text(src / "client/index.html")
    home = read_text(src / "client/src/pages/Home.tsx")

    c = {}

    # --- app ---
    m_title = re.search(r"<title>([^<]*)</title>", index)
    m_h1 = re.search(r"<h1[^>]*>\s*([^<\n]+)\s*</h1>", home)
    m_hub = re.search(r'export const HUB_TITLE = "([^"]*)"', positions, re.DOTALL)
    m_pdftitle = re.search(r'doc\.text\("MAPPA CONCETTUALE — ([^"]*)", PW / 2', pdf)
    m_pdfblank = re.search(r'doc\.text\("MAPPA CONCETTUALE IN BIANCO — ([^"]*)", PW / 2', pdf)
    m_slug = re.search(r"Report_Mappa_([A-Za-z0-9_]+)_", pdf)

    if not (m_title and m_h1 and m_hub and m_pdftitle and m_pdfblank and m_slug):
        die("DUMP: impossibile estrarre i titoli app (schema sorgente non riconosciuto).")

    c["app"] = {
        "name": slugify(m_h1.group(1)),
        "title": m_title.group(1),
        "hubTitle": from_ts_unescaped(m_hub.group(1)),
        "pdfTitle": "MAPPA CONCETTUALE — " + m_pdftitle.group(1),
        "pdfBlankTitle": "MAPPA CONCETTUALE IN BIANCO — " + m_pdfblank.group(1),
        "pdfSlug": m_slug.group(1),
    }

    # --- audio ---
    m_track = re.search(
        r'(\w+):\s*\{\s*id:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*src:\s*"([^"]+)"',
        audio,
    )
    if not m_track:
        die("DUMP: impossibile estrarre AUDIO_TRACKS.")
    segs = re.findall(
        r'id:\s*(\d+),\s*title:\s*"([^"]+)",\s*text:\s*"([^"]*)",\s*startTime:\s*(\d+),\s*endTime:\s*(\d+)',
        audio,
    )
    c["audio"] = {
        "trackId": m_track.group(2),
        "trackTitle": m_track.group(3),
        "src": m_track.group(4),
        "file": "",
    }
    c["segments"] = [
        {"title": t, "text": tx, "startTime": int(st), "endTime": int(en)}
        for (_id, t, tx, st, en) in segs
    ]

    # --- paragraphs ---
    m_total = re.search(r"export const TOTAL_SLOTS = (\d+);", schema)
    rows = re.findall(
        r'\{\s*id:\s*"([^"]+)",\s*paragraphLabel:\s*"([^"]+)",\s*paragraphSubtitle:\s*"([^"]+)",\s*color:\s*"([^"]+)",\s*slots:\s*\[([^\]]*)\],\s*audioStopAt:\s*(\d+),',
        schema,
        re.DOTALL,
    )
    if not rows:
        die("DUMP: impossibile estrarre PARAGRAPH_ROWS.")
    paras = []
    for (pid, label, subtitle, color, slots_raw, stop_at) in rows:
        slots = re.findall(r'"([^"]+)"', slots_raw)
        paras.append({
            "id": pid,
            "label": label,
            "subtitle": subtitle,
            "color": color,
            "slots": slots,
            "audioStopAt": int(stop_at),
        })
    c["paragraphs"] = paras

    # --- map ---
    m_imgw = re.search(r"export const IMG_W = (\d+);", positions)
    m_imgh = re.search(r"export const IMG_H = (\d+);", positions)
    m_hub = re.search(r"export const HUB = \{\s*cx:\s*(\d+),\s*cy:\s*(\d+),\s*w:\s*(\d+),\s*h:\s*(\d+)\s*\};", positions)
    slot_positions = re.findall(
        r'\{ slotId:\s*"([^"]+)",\s*rowId:\s*"([^"]+)",\s*keyword:\s*"([^"]*)",\s*cx:\s*(\d+),\s*cy:\s*(\d+),\s*w:\s*(\d+),\s*h:\s*(\d+)\s*\}',
        positions,
    )
    boxes = re.findall(
        r'\{ rowId:\s*"([^"]+)",\s*label:\s*"([^"]*)",\s*cx:\s*(\d+),\s*cy:\s*(\d+),\s*w:\s*(\d+),\s*h:\s*(\d+),\s*color:\s*"([^"]*)"\s*\}',
        positions,
    )
    if not (m_imgw and m_imgh and m_hub and slot_positions and boxes):
        die("DUMP: impossibile estrarre le posizioni mappa.")

    c["map"] = {
        "imgW": int(m_imgw.group(1)),
        "imgH": int(m_imgh.group(1)),
        "hub": {"cx": int(m_hub.group(1)), "cy": int(m_hub.group(2)), "w": int(m_hub.group(3)), "h": int(m_hub.group(4))},
        # per i 3 campi slotId/rowId/keyword il clone usa le posizioni ma deriva
        # slotId/rowId/keyword dai paragrafi: qui conserviamo solo le coordinate.
        "slots": [{"cx": int(cx), "cy": int(cy), "w": int(w), "h": int(h)}
                  for (_sid, _rid, _kw, cx, cy, w, h) in slot_positions],
        # per paraBoxes deriviamo rowId e color dai paragrafi; conserviamo label+coords.
        "paraBoxes": [{"label": from_ts_unescaped(label), "cx": int(cx), "cy": int(cy), "w": int(w), "h": int(h)}
                      for (_rid, label, cx, cy, w, h, _color) in boxes],
    }

    c["image"] = {"file": ""}
    return c


# =============================================================================
# CLONE — applica il contenuto alla nuova app
# =============================================================================

def apply_content(root: Path, c: dict) -> None:
    _apply_pdf_replacements(root / "client/src/lib/reportPdf.ts", c)
    _apply_index_html_title(root / "client/index.html", c)
    _apply_home_title(root / "client/src/pages/Home.tsx", c)
    _apply_audio_track_ref(root / "client/src/pages/TeacherPage.tsx", c)
    _apply_paragraph_count_robustness(root)
    _apply_package_name(root, c)
    _copy_media(root, c)

    write_text(root / "server/schema-data.ts", _gen_schema_data(c))
    write_text(root / "client/src/lib/audioData.ts", _gen_audio_data(c))
    write_text(root / "client/src/lib/conceptMapPositions.ts", _gen_concept_map_positions(c))


def validate_content(c: dict) -> None:
    for key in ("app", "audio", "paragraphs", "segments", "map"):
        if key not in c:
            die(f"JSON mancante della sezione '{key}'.")
    app = c["app"]
    for k in ("name", "title", "hubTitle", "pdfTitle", "pdfBlankTitle", "pdfSlug"):
        if k not in app:
            die(f"app.{k} mancante nel JSON.")
    if not c["paragraphs"]:
        die("paragraphs vuoto.")
    if len(c["segments"]) != len(c["paragraphs"]):
        die(f"Mismatch: {len(c['paragraphs'])} paragrafi ma {len(c['segments'])} segmenti audio.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Clona IMMAGINE INTERATTIVA SORGENTE con un nuovo contenuto.")
    ap.add_argument("--json", help="Percorso del JSON contenuto (obbligatorio in modalità clone).")
    ap.add_argument("--dump", action="store_true", help="Estrae il contenuto corrente in un JSON e termina.")
    ap.add_argument("-o", "--out", help="File JSON di output per --dump (default: contenuto.json).")
    ap.add_argument("--source", default=DEFAULT_SOURCE, help="Cartella o URL git della sorgente.")
    ap.add_argument("--name", help="Nome della nuova cartella app (default: app.name del JSON).")
    args = ap.parse_args()

    src = resolve_source(args.source)

    if args.dump:
        c = dump_content(src)
        out = Path(args.out or "contenuto.json")
        write_text(out, json.dumps(c, ensure_ascii=False, indent=2) + "\n")
        print(f"\n[OK] Contenuto estratto in: {out}")
        print("     Modifica solo i campi testo (label, subtitle, slots, title, hubTitle, ecc.)")
        print("     e lascia invariate le coordinate (map.slots, map.paraBoxes, map.hub).")
        return

    if not args.json:
        die("Specifica --json (oppure --dump per estrarre il contenuto).")
    json_path = Path(args.json)
    if not json_path.exists():
        die(f"JSON non trovato: {json_path}")
    c = json.loads(read_text(json_path))
    validate_content(c)

    name = args.name or c["app"]["name"]
    c["app"]["name"] = name
    dst = Path("/home/user") / name
    if dst.exists():
        die(f"La cartella di destinazione esiste già: {dst}")

    copy_project(src, dst)
    apply_content(dst, c)

    print("\n[OK] App clonata in:", dst)
    print("\nProssimi passi:")
    print(f"  1. cd {dst}")
    print("  2. Crea il file .env (copia da .env.example e imposta DATABASE_URL)")
    print("  3. pnpm install")
    print("  4. pnpm db:push")
    print("  5. pnpm check   (validazione TypeScript)")
    print("  6. pnpm dev     (anteprima locale)")


if __name__ == "__main__":
    main()
