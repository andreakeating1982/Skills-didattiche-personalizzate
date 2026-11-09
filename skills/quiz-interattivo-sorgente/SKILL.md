---
name: quiz-interattivo-sorgente
description: "Clona l'app QUIZ INTERATTIVO SORGENTE (l'app Shakespeare Quiz in /home/user/shakespeare-quiz) in una NUOVA app identica con un set di domande diverso. Usare quando l'utente chiede una nuova app simile/uguale al quiz sorgente cambiando solo le domande (stesso aspetto, codici classe, sessioni, contatore studenti, report PDF, voto su 10). NON usare per modificare le domande dell'app sorgente stessa (usare quiz-adapter) né per manutenere l'app sorgente (usare shakespeare-quiz)."
---

# Quiz Interattivo Sorgente — Skill di Clonazione

## Overview

Il **QUIZ INTERATTIVO SORGENTE** è l'app full-stack per quiz in classe (docente + studenti in tempo reale, codice classe, report PDF). Vive in `/home/user/shakespeare-quiz` (produzione: `https://shakespeare-quiz.easy-peasy.site`). Stack: Vite + React + TypeScript + Tailwind + tRPC + Drizzle + SQLite + jsPDF (scaffold web-db-user).

Questa skill serve a **generare una copia identica** dell'app in una cartella nuova, cambiando **solo il set di domande** (e opzionalmente il titolo della scheda browser). Tutto il resto — UI, header "QUIZ INTERATTIVO", codici classe, logica sessioni, contatore studenti, PDF, stili (inclusi centratura data e tooltip touch) — rimane **identico al sorgente**.

## Architettura — MIRROR FILE SYSTEM (CRITICO)

Il sorgente ha **quattro coppie di file mirror** che devono restare **sempre identici**. Ogni modifica va fatta su ENTRAMBE le copie:

| Ruolo | Copia radice | Copia client/server |
|-------|-------------|---------------------|
| UI docente | `TeacherPage.tsx` | `client/src/pages/TeacherPage.tsx` |
| UI studente | `StudentQuiz.tsx` | `client/src/pages/StudentQuiz.tsx` |
| Domande | `questions.ts` | `server/questions.ts` |
| Report PDF | `reportPdf.ts` | `client/src/lib/reportPdf.ts` |

Verifica sempre con `diff` dopo ogni clonazione o modifica. Lo script di clonazione aggiorna **entrambe** le copie automaticamente.

## Flusso di clonazione (in 3 passi)

### Passo 1 — Prepara il JSON delle domande

Usa come modello: `/home/user/skills/quiz-interattivo-sorgente/templates/questions_example.json`

```json
{
  "title": "QUESTIONARIO SULL'ANTICA ROMA",
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
```

- `title` (obbligatorio): intestazione stampata sui PDF.
- `questions` (obbligatorio): numero di domande **qualsiasi**, opzioni **da 2 in su**.
- `report_pdf_filename` / `blank_pdf_filename` (opzionali): prefissi dei file PDF.
- Il voto finale dello studente resta **sempre su base 10**, qualunque sia il numero di domande.

### Passo 2 — Lancia lo script di clonazione

```bash
python /home/user/skills/quiz-interattivo-sorgente/scripts/clone_quiz_app.py \
  --name quiz-roma-antica \
  --questions /percorso/domande.json \
  --title "Quiz Antica Roma"
```

Lo script:
1. Copia il progetto in `/home/user/quiz-roma-antica` (esclude `node_modules`, `.git`, `dist`, `.quiz-backups`, zip e le guide `GUIDA-*.html`).
2. Rinomina `package.json` (name) e il `<title>` di `client/index.html`.
3. Inizializza git e crea il primo commit (necessario per i checkpoint webdev).
4. Lancia `change_quiz_theme.py` sulla **copia** (non sul sorgente): domande, validatori `.min(1).max(N)`, riferimenti `/N` in TeacherPage/StudentQuiz, titoli e griglia opzioni nei PDF — **su tutte le copie mirror**.
5. Esegue `pnpm install` e `pnpm check` e verifica che le coppie mirror siano identiche.

Flag utili: `--force` (sovrascrivi), `--no-install` (salta install/check), `--source` (sorgente diverso), `--adapter` (percorso change_quiz_theme.py alternativo).

**Usare la repository GitHub come sorgente** — se l'utente ha caricato il pacchetto su GitHub, basta passare l'URL della repository: lo script la clona da solo in `/home/user/_repo_<nome>` e ci lavora sopra (così la nuova app nasce direttamente dalla versione pubblicata):

```bash
python /home/user/skills/quiz-interattivo-sorgente/scripts/clone_quiz_app.py \
  --name quiz-roma-antica \
  --questions /percorso/domande.json \
  --title "Quiz Antica Roma" \
  --source https://github.com/andreakeating1982/Quiz-interattivo-sorgente
```

**Nota sulla versione da GitHub:** il pacchetto ZIP che l'utente carica su GitHub contiene anche la cartella `skills/` con queste stesse skill: se la repository è aggiornata, il flusso è identico a quello locale.

### Passo 3 — Verifica e deploy

1. **Verifica mirror** (lo script lo fa già, ma ricontrolla):
   ```bash
   diff /home/user/quiz-roma-antica/TeacherPage.tsx /home/user/quiz-roma-antica/client/src/pages/TeacherPage.tsx
   diff /home/user/quiz-roma-antica/StudentQuiz.tsx /home/user/quiz-roma-antica/client/src/pages/StudentQuiz.tsx
   diff /home/user/quiz-roma-antica/questions.ts /home/user/quiz-roma-antica/server/questions.ts
   diff /home/user/quiz-roma-antica/reportPdf.ts /home/user/quiz-roma-antica/client/src/lib/reportPdf.ts
   ```
2. **pnpm check** nella nuova cartella (fatto dallo script; se fallisce, correggi prima di proseguire).
3. **Deploy PREVIEW** (`webdev_deploy` mode=preview, project_dir = nuova cartella) e **test visivo**: apri una classe come docente, entra con uno studente, verifica che domande/opzioni/PDF mostrino il nuovo tema e che l'app sia identica al sorgente nel resto.
4. **Checkpoint** (`webdev_save_checkpoint`) e chiedi **conferma esplicita** all'utente.
5. **Deploy PRODUZIONE** (`webdev_deploy` mode=production) solo dopo la conferma.

## Cosa cambia vs cosa resta identico

**Cambia:** array domande, validatori `.max(N)`, riferimenti `/N` in UI (es. "DOMANDA X/5"), titoli e nomi file dei PDF, `package.json` name, `<title>` del browser.

**Resta identico:** header "QUIZ INTERATTIVO", layout docente/studente, codici classe e password, logica sessioni e contatore studenti, report PDF (struttura), voto su 10, stili CSS (inclusa la centratura del campo data in "APRI UNA NUOVA CLASSE" e il tooltip touch sul nome studente), script iframe per embed Blogger.

## Pacchetto GitHub e sincronizzazione

Il progetto sorgente include una cartella `skills/` interna con **copie identiche** delle 3 skill (quiz-interattivo-sorgente, quiz-adapter, shakespeare-quiz): quando l'utente esporta lo ZIP per GitHub, le skill viaggiano insieme al codice. Se una skill viene aggiornata in `/home/user/skills/`, sincronizzare anche la copia interna del progetto (`/home/user/shakespeare-quiz/skills/`) così la repository pubblicata resta allineata.

## Backup e rollback

`change_quiz_theme.py` salva i backup in `<progetto>/.quiz-backups/` prima di ogni modifica. Per ripristinare: copia il `.bak.<timestamp>` sul file originale e rilancia `pnpm check`. La clonazione NON tocca mai il sorgente (`/home/user/shakespeare-quiz`).

## Pitfall noti

- **Mirror fuori sync**: se qualcuno modifica solo una copia, la clonazione copia lo stato incoerente. Prima di clonare verifica che il sorgente abbia i mirror identici.
- **`--name`**: solo minuscole/numeri/trattini (es. `quiz-roma-antica`). Il nome diventa anche la cartella in `/home/user/`.
- **Stringhe sostituite testualmente**: se il codice del sorgente cambia formato (es. "Domanda X/10" → altro), lo script avvisa con ⚠️ ma non abortisce: controlla sempre l'output e `pnpm check`.
- **Deploy**: mai in produzione nella stessa risposta in cui hai scritto codice o creato la preview — prima checkpoint, poi conferma esplicita dell'utente.
- **Non clonare dentro il sorgente**: la destinazione è sempre `/home/user/<nome>`.
