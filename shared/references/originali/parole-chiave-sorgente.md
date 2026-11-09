# Archivio di dettaglio — parole-chiave-sorgente

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/quiz.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Overview
- Architettura — File canonici e copie mirror
- Struttura fissa delle domande (8)
- Flusso di clonazione (in 3 passi)
- Passo 1 — Prepara il JSON delle domande
- Passo 2 — Lancia lo script
- Usare la repository GitHub come sorgente
- Passo 3 — Verifica e deploy
- Cosa cambia vs cosa resta identico
- Backup e rollback
- Pitfall noti

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# PAROLE CHIAVE SORGENTE — Skill di Clonazione

## Overview

Il **PAROLE CHIAVE SORGENTE** è l'app full-stack per quiz in classe (docente + studenti in tempo reale, codice classe, report PDF). Vive in `/home/user/shakespeare-quiz`. Stack: Vite + React 18 + TypeScript + Tailwind + tRPC + Drizzle + SQLite + pdf-lib (scaffold web-db-user).

Questa skill genera una **copia identica** dell'app in una cartella nuova, cambiando **solo il set di domande** (e opzionalmente i titoli). Tutto il resto — UI, struttura MAPA 1/2, codici classe, logica sessioni, contatore studenti, PDF, stili — resta **identico al sorgente**.

> **Nota sul nome**: «PAROLE CHIAVE SORGENTE» è come chiamiamo il SORGENTE in questa skill. Il titolo UI mostrato agli studenti è la stringa `PAROLE CHIAVE INTERATTIVE` (è questa che lo script sostituisce nei cloni), e il titolo sui PDF è `PAROLE CHIAVE DI ROSALÍA DE CASTRO`.

## Architettura — File canonici e copie mirror

Le **copie canoniche** (quelle che l'app usa davvero) vivono dentro `client/` e `server/`:

| Ruolo | Percorso canonico |
|-------|-------------------|
| UI docente | `client/src/pages/TeacherPage.tsx` |
| UI studente | `client/src/pages/StudentQuiz.tsx` |
| Domande | `server/questions.ts` |
| Report PDF | `client/src/lib/reportPdf.ts` |

Lo script di clonazione crea inoltre **una copia mirror alla radice** del clone (`questions.ts`, `reportPdf.ts`, `StudentQuiz.tsx`, `TeacherPage.tsx`) per comodità di consultazione. Le copie radice NON sono importate dall'app: modifica sempre i percorsi canonici qui sopra, poi lo script mantiene le copie radice allineate automaticamente. Verifica sempre con `diff`.

## Struttura fissa delle domande (8)

- **MAPA 1** = `number` 1-5, **MAPA 2** = `number` 6-8.
- **Multi-risposta** (2 risposte corrette su 4 opzioni) SOLO su domande 4 e 5: `correctAnswer` è un array `["A", "B"]`.
- Per tutte le altre domande `correctAnswer` è una stringa.
- Il numero di domande è parametrizzato in `server/routers.ts` (`TOTAL_QUESTIONS = SHAKESPEARE_QUESTIONS.length`), ma i filtri MAPA in `StudentQuiz.tsx` (righe 432-433 e 448-449) sono fissi su 1-5 / 6-8: se servono più/meno domande va modificato anche lì.

## Flusso di clonazione (in 3 passi)

### Passo 1 — Prepara il JSON delle domande

Modello: `/home/user/skills/didattica-app-classe/templates/parole-chiave-sorgente/questions_example.json`

```json
{
  "app_title": "PAROLE CHIAVE IL SISTEMA SOLARE",
  "pdf_title": "IL SISTEMA SOLARE",
  "questions": [
    { "number": 1, "question": "MAPA 1 - IL SOLE", "options": ["È una stella", "È un pianeta", "È un satellite"], "correctAnswer": "È una stella" },
    { "number": 4, "question": "MAPA 1 - I GIGANTI GASSOSI", "options": ["Giove", "Mercurio", "Saturno", "Venere"], "correctAnswer": ["Giove", "Saturno"] }
  ]
}
```

- `questions` (obbligatorio): esattamente **8** domande.
- `app_title` / `pdf_title` (opzionali): se omessi restano «PAROLE CHIAVE INTERATTIVE» / «PAROLE CHIAVE DI ROSALÍA DE CASTRO».

### Passo 2 — Lancia lo script

```bash
python /home/user/skills/didattica-app-classe/scripts/parole-chiave-sorgente/rebuild_app.py \
  --name parole-chiave-sistema-solare \
  --questions /percorso/domande.json \
  --app-title "PAROLE CHIAVE IL SISTEMA SOLARE" \
  --pdf-title "IL SISTEMA SOLARE"
```

Lo script: copia il progetto (esclude `node_modules`, `.git`, `dist`, `.env`, log), scrive le 8 domande, aggiorna i titoli PDF/UI, rinomina `package.json`, inizializza git, esegue `pnpm install` + `pnpm check`, e verifica che le coppie mirror siano identiche.

Flag utili: `--force` (sovrascrivi), `--no-install` (salta install/check), `--source` (sorgente diverso).

### Usare la repository GitHub come sorgente

Se l'utente ha caricato il pacchetto su GitHub, passa l'URL della repository: lo script la clona da solo e ci lavora sopra (così la nuova app nasce direttamente dalla versione pubblicata):

```bash
python /home/user/skills/didattica-app-classe/scripts/parole-chiave-sorgente/rebuild_app.py \
  --name parole-chiave-sistema-solare \
  --questions /percorso/domande.json \
  --app-title "PAROLE CHIAVE IL SISTEMA SOLARE" \
  --source https://github.com/UTENTE/REPO.git
```

### Passo 3 — Verifica e deploy

1. **Verifica mirror** (lo script lo fa già, ma ricontrolla con `diff`).
2. **pnpm check** nella nuova cartella.
3. **Deploy PREVIEW** (`webdev_deploy` mode=preview) e test visivo.
4. **Checkpoint** (`webdev_save_checkpoint`) e chiedi conferma esplicita.
5. **Deploy PRODUZIONE** solo dopo conferma.

## Cosa cambia vs cosa resta identico

**Cambia:** array domande, titoli PDF/UI, `package.json` name, `<title>` browser.

**Resta identico:** struttura MAPA 1/2, multi-risposta su 4-5, audio docente (topic-specifico), layout docente/studente, codici classe e password, logica sessioni e contatore studenti, report PDF con **box PUNTEGGIO** su un'unica linea centrata (cornice blu con margini stretti: `PUNTEGGIO: X/10 — ogni risposta corretta = 1 pt — massimo 10/10`) presente sia nel report che nel questionario in bianco, stili CSS.

## Backup e rollback

La clonazione NON tocca mai il sorgente (`/home/user/shakespeare-quiz`). Per ripristinare un clone, elimina la cartella `--name` e rilancia.

## Pitfall noti

- **Mirror fuori sync**: dopo la clonazione verifica che le copie radice del clone coincidano con i percorsi canonici (es. `diff questions.ts server/questions.ts`).
- **`--name`**: solo minuscole/numeri/trattini.
- **8 domande fisse**: i filtri MAPA in `StudentQuiz.tsx` sono hardcoded su 1-5 / 6-8.
- **Riquadro PUNTEGGIO su una facciata e su un'unica linea**: in `reportPdf.ts` il box PUNTEGGIO e il riassunto CORRETTE/INCORRETTE restano INSIEME su una sola pagina (logica block-height + `computeQuestionHeight`). Il riquadro è su UN'UNICA LINEA centrata, con cornice blu e margini stretti (larghezza = `scoreTextW + 3`, altezza = `scoreBoxFont * 0.352 + 2.5`, testo centrato orizzontalmente e verticalmente). NON rimuovere queste funzioni: evitano che il box venga spezzato tra due facciate o distribuito su più linee.
- **Deploy**: mai in produzione nella stessa risposta in cui hai scritto codice o creato la preview.
- **Non clonare dentro il sorgente**: la destinazione è sempre `/home/user/<nome>`.
- **Data centrata nel docente**: l'input data in «APRI UNA NUOVA CLASSE» usa un input `type="date"` con testo trasparente (`text-transparent`) + uno `<span>` overlay che mostra la data formattata centrata; il click sul wrapper apre il picker nativo via `showPicker()`. Il fix è già nel sorgente `TeacherPage.tsx`: NON rimuovere l'overlay né riabilitare l'indicatore nativo (è nascosto con `::-webkit-calendar-picker-indicator { opacity: 0 }`).
