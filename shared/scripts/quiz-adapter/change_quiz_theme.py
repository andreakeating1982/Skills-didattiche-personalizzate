#!/usr/bin/env python3
"""
change_quiz_theme.py — DEPRECATED (non usare).

SUPERSEDED da scripts/rebuild_app.py nella skill `parole-chiave-sorgente`:
    python /home/user/skills/didattica-app-classe/scripts/parole-chiave-sorgente/rebuild_app.py \
        --name <slug> --questions <questions.json>

Questo script modificava l'app Shakespeare Quiz in-place e cerca token
ormai inesistenti (QUESTIONARIO SU WILLIAM SHAKESPEARE, .max(10), /10).
Mantenuto solo come riferimento storico.

Automates replacing the question set, PDF titles, and hardcoded question
count in the Shakespeare Quiz app.

Usage:
    python change_quiz_theme.py questions.json

Input JSON format (questions.json):
{
  "title": "QUESTIONARIO SULL'ANTICA ROMA",
  "pdf_topic": "Antica_Roma",
  "report_pdf_filename": "Report_Quiz",
  "blank_pdf_filename": "Questionario",
  "questions": [
    {
      "number": 1,
      "question": "In che anno è stata fondata Roma?",
      "options": ["753 a.C.", "476 a.C.", "27 a.C.", "313 d.C."],
      "correctAnswer": "753 a.C."
    }
  ]
}

Note: questions can have any count and options can have any length.
"""

import json
import sys
import os
import shutil
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT = Path("/home/user/shakespeare-quiz")

FILES = {
    "questions":    PROJECT / "server" / "questions.ts",
    "routers":      PROJECT / "server" / "routers.ts",
    "teacher_page": PROJECT / "client" / "src" / "pages" / "TeacherPage.tsx",
    "student_page": PROJECT / "client" / "src" / "pages" / "StudentQuiz.tsx",
    "report_pdf":   PROJECT / "client" / "src" / "lib" / "reportPdf.ts",
}

BACKUP_DIR = PROJECT / ".quiz-backups"


# ── Helpers ────────────────────────────────────────────────────────────────

def backup(file: Path) -> None:
    """Create a timestamped backup of *file* inside BACKUP_DIR."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = os.path.getmtime(file) if file.exists() else "0"
    dest = BACKUP_DIR / f"{file.name}.bak.{int(ts)}"
    shutil.copy2(file, dest)
    print(f"  ✔ Backup saved: {dest.name}")


def bail(msg: str) -> None:
    print(f"❌ ERROR: {msg}")
    sys.exit(1)


# ── File-modification functions ────────────────────────────────────────────

def replace_questions_ts(data: list[dict]) -> None:
    """Replace the entire SHAKESPEARE_QUESTIONS array."""
    path = FILES["questions"]
    backup(path)

    lines = []
    for q in data:
        opts = json.dumps(q["options"])
        answer = json.dumps(q["correctAnswer"])
        lines.append("  {")
        lines.append(f'    number: {q["number"]},')
        lines.append(f'    question: {json.dumps(q["question"])},')
        lines.append(f"    options: {opts},")
        lines.append(f"    correctAnswer: {answer},")
        lines.append("  },")

    content = path.read_text(encoding="utf-8")

    # Replace everything between 'export const SHAKESPEARE_QUESTIONS = [' and the
    # matching '];' (end of file).
    marker = "export const SHAKESPEARE_QUESTIONS = ["
    start = content.index(marker)
    bracket = start + len(marker)
    # Find the matching '];' — it's the last one in the file
    end_bracket = content.rindex("];") + 2

    new = (
        content[:bracket]
        + "\n"
        + "\n".join(lines)
        + "\n"
        + "];"
        + content[end_bracket:]
    )
    path.write_text(new, encoding="utf-8")
    print(f"  ✔ {path.name} — {len(data)} questions written")


def replace_max10_in_routers(count: int) -> None:
    """Update all `.max(10)` to `.max(count)` in routers.ts."""
    path = FILES["routers"]
    backup(path)
    content = path.read_text(encoding="utf-8")
    # Only replace .max(10) that immediately follow .min(1) — these are the
    # question-number validators.
    new = re.sub(r"\.min\(1\)\.max\(10\)", f".min(1).max({count})", content)
    if new == content:
        bail("Could not find any '.min(1).max(10)' in routers.ts")
    path.write_text(new, encoding="utf-8")
    print(f"  ✔ {path.name} — .max({count}) applied")


def replace_in_teacher_page(count: int) -> None:
    """Update hardcoded /10 and >=10 in TeacherPage.tsx."""
    path = FILES["teacher_page"]
    backup(path)
    content = path.read_text(encoding="utf-8")

    # Domanda X/10  →  Domanda X/{count}
    content = content.replace("Domanda {classDetail.currentQuestion}/10",
                              f"Domanda {{classDetail.currentQuestion}}/{count}")
    content = content.replace("Domanda {classDetail?.currentQuestion || 1}/10",
                              f"Domanda {{classDetail?.currentQuestion || 1}}/{count}")

    # (classDetail?.currentQuestion || 0) >= 10
    content = content.replace(
        "(classDetail?.currentQuestion || 0) >= 10",
        f"(classDetail?.currentQuestion || 0) >= {count}",
    )

    # studentAnswers.length + '/10 risposte'
    # WARNING: this could match student.score + '/10' too if we're not careful,
    # but the latter is always grade-out-of-10 which is correct.
    # Let's use a precise match.
    content = content.replace(
        "studentAnswers.length + '/10 risposte'",
        f"studentAnswers.length + '/{count} risposte'",
    )

    path.write_text(content, encoding="utf-8")
    print(f"  ✔ {path.name} — /{count} and >={count} applied")


def replace_in_student_page(count: int) -> None:
    """Update hardcoded /10 in StudentQuiz.tsx progress bar."""
    path = FILES["student_page"]
    backup(path)
    content = path.read_text(encoding="utf-8")

    # DOMANDA {currentQNum}/10
    content = content.replace(
        "DOMANDA {currentQNum}/10",
        f"DOMANDA {{currentQNum}}/{count}",
    )

    # width: `${(currentQNum / 10) * 100}%`
    content = content.replace(
        "(currentQNum / 10) * 100",
        f"(currentQNum / {count}) * 100",
    )

    path.write_text(content, encoding="utf-8")
    print(f"  ✔ {path.name} — /{count} applied")


def replace_in_report_pdf(
    new_title: str,
    report_filename: str,
    blank_filename: str,
) -> None:
    """Replace PDF titles, filenames, and the 2×2 option grid."""
    path = FILES["report_pdf"]
    backup(path)
    content = path.read_text(encoding="utf-8")

    # ── Title (report) ──
    content = content.replace(
        'doc.text("QUESTIONARIO SU WILLIAM SHAKESPEARE", PAGE_W / 2, M + 6, { align: "center" });',
        f'doc.text("{new_title}", PAGE_W / 2, M + 6, {{ align: "center" }});',
    )

    # ── Title (blank questionnaire) ──
    content = content.replace(
        'doc.text("QUESTIONARIO SU WILLIAM SHAKESPEARE", PAGE_W / 2, y, { align: "center" });',
        f'doc.text("{new_title}", PAGE_W / 2, y, {{ align: "center" }});',
    )

    # ── Report filename ──
    content = content.replace(
        "doc.save(`Report_Quiz_",
        f"doc.save(`{report_filename}_",
    )

    # ── Blank PDF filename ──
    content = content.replace(
        "doc.save(`Questionario_Shakespeare_",
        f"doc.save(`{blank_filename}_",
    )

    # ── Option grid — REPORT block (uses M + 4) ──
    old_grid_report = """    const halfW = CW / 2 - 4;
    const optLabels = q.options.map((opt, idx) => `${String.fromCharCode(65 + idx)}) ${opt}`);

    // Row 1 (options 0-1)
    doc.text(optLabels[0], M + 4, y);
    doc.text(optLabels[1], M + 4 + halfW, y);
    y += 3.8;

    // Row 2 (options 2-3)
    doc.text(optLabels[2], M + 4, y);
    doc.text(optLabels[3], M + 4 + halfW, y);
    y += 4.1;"""

    new_grid_report = """    const halfW = CW / 2 - 4;
    const optLabels = q.options.map((opt, idx) => `${String.fromCharCode(65 + idx)}) ${opt}`);

    // Dynamic grid (any number of options)
    q.options.forEach((_, idx) => {
      const col = idx % 2;
      const row = Math.floor(idx / 2);
      doc.text(optLabels[idx], M + 4 + col * halfW, y + row * 3.8);
    });
    y += Math.ceil(q.options.length / 2) * 3.8 + 0.3;"""

    content = content.replace(old_grid_report, new_grid_report)

    # ── Option grid — BLANK PDF block (uses M + 2) ──
    old_grid_blank = """    const halfW = CW / 2 - 4;
    const optLabels = q.options.map((opt, idx) => `${String.fromCharCode(65 + idx)}) ${opt}`);

    doc.text(optLabels[0], M + 2, y);
    doc.text(optLabels[1], M + 2 + halfW, y);
    y += 3.8;

    doc.text(optLabels[2], M + 2, y);
    doc.text(optLabels[3], M + 2 + halfW, y);
    y += 4.5;"""

    new_grid_blank = """    const halfW = CW / 2 - 4;
    const optLabels = q.options.map((opt, idx) => `${String.fromCharCode(65 + idx)}) ${opt}`);

    // Dynamic grid (any number of options)
    q.options.forEach((_, idx) => {
      const col = idx % 2;
      const row = Math.floor(idx / 2);
      doc.text(optLabels[idx], M + 2 + col * halfW, y + row * 3.8);
    });
    y += Math.ceil(q.options.length / 2) * 3.8 + 0.7;"""

    content = content.replace(old_grid_blank, new_grid_blank)

    path.write_text(content, encoding="utf-8")
    print(f"  ✔ {path.name} — titles, filenames, dynamic grid applied")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        bail("Usage: python change_quiz_theme.py <questions.json>")

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        bail(f"File not found: {json_path}")

    payload = json.loads(json_path.read_text(encoding="utf-8"))

    # Validate
    if "questions" not in payload or not isinstance(payload["questions"], list):
        bail("JSON must contain a 'questions' array")
    if not payload["questions"]:
        bail("questions array is empty")
    if "title" not in payload:
        bail("JSON must contain a 'title' string")

    title = payload["title"]
    questions = payload["questions"]
    count = len(questions)

    # Validate question structure
    for q in questions:
        if not all(k in q for k in ("number", "question", "options", "correctAnswer")):
            bail(f"Question #{q.get('number', '?')} is missing one of: number, question, options, correctAnswer")
        if not isinstance(q["options"], list) or len(q["options"]) < 2:
            bail(f"Question #{q['number']} must have at least 2 options")

    report_fn = payload.get("report_pdf_filename", "Report_Quiz")
    blank_fn = payload.get("blank_pdf_filename", "Questionario")

    print(f"\n🚀 Changing quiz theme to: {title}")
    print(f"   Questions: {count}\n")

    # 1. Questions
    print("[1/6] Replacing questions array …")
    replace_questions_ts(questions)

    # 2. Routers
    print("[2/6] Updating question-number validators …")
    replace_max10_in_routers(count)

    # 3. Teacher page
    print("[3/6] Updating TeacherPage.tsx …")
    replace_in_teacher_page(count)

    # 4. Student page
    print("[4/6] Updating StudentQuiz.tsx …")
    replace_in_student_page(count)

    # 5. Report PDF
    print("[5/6] Updating reportPdf.ts …")
    replace_in_report_pdf(title, report_fn, blank_fn)

    # 6. Summary
    print(f"\n✅ All done! {count} questions written.\n")
    print("Next steps:")
    print("  1. cd /home/user/shakespeare-quiz")
    print("  2. pnpm check         (verify no TypeScript errors)")
    print("  3. pnpm build         (compile for production)")
    print("  4. Deploy on the dashboard\n")
    print(f"📁 Backups saved in: {BACKUP_DIR}\n")


if __name__ == "__main__":
    main()
