---
name: shakespeare-quiz
description: "Manutenzione completa e personalizzazione dell'app Shakespeare Quiz (Vite + React + TypeScript + Tailwind + tRPC + Drizzle + SQLite). Usare per: modificare UI studente/docente, correggere logica di sessione, deploy preview/produzione, personalizzare report PDF, modificare il contatore studenti attivi, gestire ZIP e checkpoint. NON usare per cambiare le domande del quiz — usare quiz-adapter."
---

# Shakespeare Quiz — Skill di Manutenzione

## Overview

App Shakespeare Quiz in `/home/user/shakespeare-quiz`. Scaffold `web-db-user`. Stack: Vite + React 18 + TypeScript + TailwindCSS 3 + shadcn/ui + tRPC + Drizzle ORM + SQLite (libsql).

**URL produzione**: `https://shakespeare-quiz-2.easy-peasy.site`

## File Critici

| File | Ruolo |
|------|-------|
| `client/src/pages/Home.tsx` | Home page root `/` — embeddata nel blog (titolo + TROVA LA TUA CLASSE) |
| `client/src/pages/TeacherPage.tsx` | Dashboard docente (sidebar classi + area principale) |
| `client/src/pages/StudentQuiz.tsx` | Quiz studente (JOIN screen + MAPA 1/2 quiz) |
| `client/src/index.css` | Tema Tailwind, `--font-sans/--font-serif`, `:not(.preserve-case)`, animazioni |
| `client/index.html` | `<html lang="it">`, `<body class="antialiased">`, titolo pagina |
| `client/src/lib/reportPdf.ts` | Generazione PDF (report studente + questionario bianco) |
| `server/routers.ts` | Endpoint tRPC (classes, answers, questions, stats, report) |
| `server/db.ts` | Funzioni query Drizzle (getStudentsByClass, deleteStudent, etc.) |
| `server/questions.ts` | Array SHAKESPEARE_QUESTIONS |

## Comportamenti Attuali (2026-08-04)

### Dashboard Docente — Layout

**Sidebar "LE TUE CLASSI"**:
- Le card NON sono cliccabili, sono informative
- **Nessuna evidenziazione colore** — tutte le card hanno lo stesso sfondo (rimosso `bg-muted/40`)
- **Hotspot grigio fisso** `size-2 rounded-full bg-gray-300` per ogni classe (mai verde)
- **Nessun pulsante cestino** nella sidebar — l'eliminazione classe è nella dashboard

**Area principale (classe selezionata)**:
- Card info: nome classe/data, codice sessione, studenti attivi
- Pulsante "CHIUDI": **nessuna conferma**, chiude direttamente la sessione
- Pulsante "ELIMINA CLASSE": accanto a CHIUDI. Chiama `hDel(selId!)`, conferma con `confirm()`, elimina la classe e resetta `selId` chiudendo la dashboard
- Pulsante "AREA STUDENTI" in alto a destra
- Card "STUDENTI ATTIVI NELLA SESSIONE": lista espandibile, ogni studente mostra risposte
- Rimosso il box "NUMERO COMPLESSIVO DI STUDENTI FINORA PARTECIPANTI"

### Studenti — Hotspot e Status

- **Hotspot studente**: `size-2 rounded-full shrink-0 bg-gray-300` — **sempre e solo grigio**, mai verde (rimosso il condizionale `completed ? 'bg-green-500' : 'bg-gray-300'`)
- **Rimossi TUTTI i testi di stato**: "In attesa", "In corso", "Completato", "X/10 risposte"
- Il nome dello studente è centrato tra l'hotspot a sinistra e il punteggio a destra

### Input Sidebar

- **Tutti gli input** nella sidebar docente usano `!text-center` con `!important` per forzare il centramento
- Questo include: Nome classe, Data, Password, Codice riapertura, Password riapertura
- Il placeholder `text-center` da solo NON basta — shadcn/ui Input può resettare l'allineamento; serve `!text-center`

### Schermata Home (root `/`)

`Home.tsx`. La Home page è la pagina embeddata nel blog (NON la schermata studente). Struttura **identica** a `laboratorioaumentato` Home.tsx.

```jsx
<div className="min-h-screen bg-background paper-grain flex flex-col">
  <header className="mx-auto w-full max-w-5xl px-4 py-6 sm:px-6 sm:py-9">
    <div className="flex flex-col items-center gap-3">
      <h1 className="text-2xl sm:text-3xl font-bold leading-tight text-foreground text-center">
        PAROLE CHIAVE INTERATTIVE
      </h1>
      <a href="/docente"
        className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3.5 py-2 text-sm font-medium text-foreground shadow-sm transition hover:border-plum/40 hover:text-plum mb-4">
        <School className="size-4" /> AREA DOCENTE
      </a>
    </div>
  </header>
  <main className="flex-1 flex items-start justify-center px-4 pb-16">
    <div className="w-full max-w-md animate-pop-in">
      <div className="bg-card border border-border/60 rounded-xl shadow-sm hover:shadow-lg transition-shadow animate-pop-in">
        <div className="p-6 sm:p-8 flex flex-col items-center gap-5">
          <div className="size-14 rounded-2xl bg-plum/10 flex items-center justify-center">
            <School className="size-7 text-plum" />
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-foreground">TROVA LA TUA CLASSE</h2>
          <p className="text-sm text-muted-foreground leading-relaxed max-w-sm text-center">
            Inserisci il codice fornito dal docente per iniziare l'attività.
          </p>
          <div className="w-full space-y-3 mt-2">
            <div className="relative">
              <Hash className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
              <Input ... className="pl-10 text-center uppercase tracking-widest" maxLength={4} />
            </div>
            <Button ... className="w-full h-12 rounded-xl bg-plum hover:bg-plum/90 text-white font-bold tracking-wider">
              ENTRA COL CODICE
            </Button>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
```

**Dettagli tecnici Home**:
- Titolo: `text-2xl sm:text-3xl font-bold leading-tight text-foreground text-center` — **identico a laboratorioaumentato**
- **NON** usa più `text-4xl font-semibold tracking-wide` — il titolo da 36px era la causa della differenza visiva nel blog
- **NON** usa `<Card>` + `<CardContent>` shadcn — usa `<div>` raw come laboratorioaumentato
- Bottone: `bg-plum hover:bg-plum/90 text-white font-bold tracking-wider` (NON `bg-primary`)
- Input: `pl-10` (NON `pl-9`), senza `h-12` esplicito
- Header: `<header>` + `<main>` semantici (non `<div>` generici)
- Descrizione: senza `normal-case` / `style={{textTransform:"none"}}` — usa il text-transform globale
- Animazione: `animate-pop-in` 0.35s ease-out forwards

### Schermata Studente — JOIN

`StudentQuiz.tsx`, blocco `if (!joined)`. Schema esatto:

```
┌─ Sfondo bg-background paper-grain ─────────────┐
│  PAROLE CHIAVE INTERATTIVE  [🏠 HOME]            │  ← h1 text-2xl sm:text-3xl + Button
│                                                  │
│  ┌─ Card bg-card border-border/60 ──────────┐  │
│  │      [📖]  ← size-14 rounded-2xl          │  │
│  │            bg-plum/10, icon text-plum     │  │
│  │                                           │  │
│  │    ENTRA NELLA CLASSE                     │  │
│  │    CODICE CLASSE: XXXX                    │  │
│  │                                           │  │
│  │  [ Cognome ]  [  Nome   ]  ← text-center  │  │
│  │                                           │  │
│  │  [         ENTRA         ]  ← bg-plum     │  │
│  └───────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

**Dettagli tecnici JOIN**:
- Titolo generale app: **"PAROLE CHIAVE INTERATTIVE"** (non più "PAROLE CHIAVE DI ROSALÍA DE CASTRO")
- Struttura: `<header>` + `<main>` semantici, **identica** a `laboratorioaumentato` Home.tsx
- Titolo JOIN "PAROLE CHIAVE INTERATTIVE": `text-2xl sm:text-3xl font-bold leading-tight text-foreground text-center`
- Titolo quiz header "PAROLE CHIAVE INTERATTIVE": `text-lg sm:text-xl font-bold leading-tight text-foreground` — allineato a `williamshakespeare-quizinterattivo`
- Titolo docente header: `text-lg sm:text-xl font-bold leading-tight text-foreground`
- Titolo "ENTRA NELLA CLASSE": `text-xl sm:text-2xl font-bold text-foreground`
- Titolo "IN ATTESA DEL DOCENTE" / "IL DOCENTE HA CHIUSO LA CLASSE": `text-xl sm:text-2xl font-bold text-foreground text-center`
- Icona Home button: `House` da lucide-react (NON BookOpen)
- Pulsante HOME: `inline-flex items-center gap-2 rounded-md border border-border bg-card px-3.5 py-2 text-sm font-medium text-foreground shadow-sm transition hover:border-plum/40 hover:text-plum mb-4`
- Pulsante ENTRA: `w-full h-12 rounded-xl bg-plum hover:bg-plum/90 text-white font-bold tracking-wider`
- Icona libro: `size-14 rounded-2xl bg-plum/10`, icona `size-7 text-plum`
- Input Cognome/Nome: `h-12 text-base text-center border-gray-300 focus-visible:ring-plum focus-visible:border-plum`

### Testo Risposta Esatta

Nel GroupPanel (TeacherPage.tsx), blocco `isRev && curRev`:
- **Tutto in maiuscolo**: `uppercase`
- **10pt**: `text-[10px]`
- **Stesso font**: `font-normal` (no bold/medium)
- **Formato**: `✅ RISPOSTA ESATTA: <answer> (X RISPOSTE ESATTE)`
- Il conteggio studenti è incluso NEL paragrafo stesso (non in un `<p>` separato)

### Eliminazione Classe

- **Niente cestino nella sidebar** — rimosso `Trash2` e `onClick` da ogni card classe
- **Pulsante "ELIMINA CLASSE" nella dashboard** (accanto a CHIUDI):
  ```
  <Button onClick={()=>hDel(selId!)} disabled={del.isPending} variant="outline"
    className="border-red-400 text-red-700 hover:bg-red-50 hover:border-red-500 rounded-xl h-9 px-3 text-xs sm:text-sm">
    <Trash2 className="size-4" /> <span>ELIMINA CLASSE</span>
  </Button>
  ```
- `hDel` usa `confirm("Eliminare questa classe?")` prima di chiamare `del.mutate({id})`
- Se `selId === id`, setta `selId` a null → chiude immediatamente la dashboard

### Placeholder Empty State

Testo quando nessuna classe è selezionata:
> "Crea una nuova classe dalla barra laterale oppure riaprine una già esistente"

**Attenzione**: NON "selezionane una esistente per gestire la sessione" ma "**riaprine una già esistente**"

### Persistenza Studenti

- **Nessun cleanup automatico** — la chiamata `cleanupInactiveStudents` è stata rimossa da `getStudents` e da tutte le altre query
- Il testo descrittivo dice: "Tutti gli studenti iscritti restano visibili. Il contatore non si azzera se lo studente salta una domanda."
- `getStudents` usa `getStudentsByClass` (filtra `removed: true`) — gli studenti rimossi manualmente spariscono
- Stats e report usano `getAllStudentsByClassIncludingRemoved` (include tutti) tranne il report che usa `getStudentsByClass`

### Rimozione Manuale Studenti

- `deleteStudent` fa soft-delete (`removed: true`) — preserva le risposte per eventuali report futuri
- `getStudents` usa `getStudentsByClass` → rimossi manualmente spariscono dalla dashboard
- `report` usa `getStudentsByClass` → rimossi manualmente NON compaiono nel PDF
- `stats` usa `getAllStudentsByClassIncludingRemoved` → include tutti per statistiche complete

### Sezione "Studenti in attesa di risposta" — RIMOSSA

Il box giallo ambra "STUDENTI IN ATTESA DI RISPOSTA" è stato **eliminato**. Al suo posto, nella riga principale STUDENTI ATTIVI, appare il testo arancione **`IN ATTESA`** (`text-[10px] font-bold text-orange-600`) a sinistra del nome per ogni studente che non ha ancora risposto alla domanda corrente.

`pendingStudents` si calcola ancora con `useMemo` ma il suo unico utilizzo è la verifica `(pendingStudents as any[]).some((p:any) => p.id === s.id)` dentro la riga studente.

### Contatori e Testi (aggiornato 2026-07-29)

- **Rimosso** "Completato" dalla riga studente (mostra stringa vuota)
- **Rimosso** contatore "X completati" dalla barra riassuntiva
- **Rimosso** contatore "X in corso" dalla barra riassuntiva
- Resta solo: "👥 X attivi"
- "Domande completate" (linea 135) NON è stato toccato
- **IN ATTESA DI INVIO** arancione (`text-orange-500`) nella riga studente quando `hasAnswers` è false — nessun box separato
- **IN ATTESA** arancione (`text-[10px] font-bold text-orange-600`) a sinistra del nome per studenti pending
- **Freccia espansione sempre visibile** — anche senza risposte (rimosso condizionale `hasAnswers &&`)
- **Pallini MAPA sempre colorati**: 🟢 `bg-emerald-500` (MAPA 1) e 🔵 `bg-blue-500` (MAPA 2) — mai grigi

### Contatore Real-Time

Ogni studente nella lista mostra il punteggio in tempo reale (es. `2/10`), aggiornato via polling/stats. Se uno studente salta una domanda il contatore non si azzera.

### Report PDF

`client/src/lib/reportPdf.ts`:
- Testo verde: **italic**, mai bold (`fontStyle: 'italic'`)
- Margini: top 25mm, bottom/left/right 20mm
- Layout adattivo per opzioni (griglia 2 colonne di default)
- Costruito con `pdf-lib`, mai html2pdf
- Report esclude studenti rimossi manualmente

### MAPA 1 / MAPA 2

- MAPA 1: domande 1-5
- MAPA 2: domande 6-8
- Navigazione indipendente per ogni MAPA
- Multi-select su domande 4 e 5 (checkbox, risposte unite con `||`)
- **Audio rimosso** — `AudioPlayer` e import `AUDIO_TRACKS`/`getTrackForGroup` eliminati da StudentQuiz.tsx
- **Box ATTENZIONE rimosso** — il box ambra "ATTENZIONE: questa domanda richiede 2 risposte corrette" è stato eliminato; resta solo il testo guida in basso "Selezionate X di 2 risposte richieste"
- **Sezione espansa**: mostra solo le domande con risposte (`mapa1Answers.length > 0 && ...`); nessuna riga "IN ATTESA DI INVIO" nel dropdown

## Endpoint Backend

| Router | Endpoint | Nota |
|--------|----------|------|
| classes | `getStudents` | `getStudentsByClass` — esclude rimossi |
| classes | `stats` | `getAllStudentsByClassIncludingRemoved` — include tutti |
| classes | `revealAnswer` | `getAllStudentsByClassIncludingRemoved` |
| classes | `removeStudent` | Soft-delete (`removed: true`) |
| classes | `closeClass` | Imposta `isActive: false`, `sessionStarted: false` |
| answers | `submitAnswer` | Blocca duplicati: "Hai già risposto a questa domanda." |
| report | `getReport` | `getStudentsByClass` — esclude rimossi |

## Deploy

```bash
cd /home/user/shakespeare-quiz
pnpm check    # verifica TypeScript
# Poi webdev_deploy mode="preview" per test
# Poi webdev_deploy mode="production" per produzione
```

**Prima del deploy produzione**: sempre `webdev_save_checkpoint` con descrizione significativa.

## File di Configurazione

### `client/index.html`

- `<html lang="it">` — **NON** `lang="en"` (differenza con laboratorioaumentato)
- `<body class="antialiased">` — **NON** `<body>` senza classe
- `<title>PAROLE CHIAVE INTERATTIVE</title>`

### `client/src/index.css`

Nel blocco `@theme inline`:
```css
--font-sans: Cambria, Georgia, "Times New Roman", serif;
--font-serif: Cambria, Georgia, "Times New Roman", serif;
```

Nel blocco `@layer base`:
```css
body *:not(input):not(textarea):not(select):not(.preserve-case) {
  text-align: center !important;
  text-transform: uppercase !important;
  font-family: Cambria, Georgia, "Times New Roman", serif !important;
}
```
**Attenzione**: `:not(.preserve-case)` è ESSENZIALE — **NON** usare `body *:not(input):not(textarea):not(select)` senza l'esclusione.

Animazione pop-in:
```css
.animate-pop-in {
  animation: pop-in 0.35s ease-out forwards;
}
```
**NON** usare `.25s ease-out both`.

## Regole d'Oro

1. **Mai cambiare dimensione icone lucide-react** — le classi `size-*` sono calibrate
2. **`style` in React è oggetto**, non stringa
3. **Sempre `.map()`**, mai `for...of` nel JSX
4. **Placeholder in italiano** per UI italiana
5. **`disabled={mutation.isPending}`** sui pulsanti che chiamano mutation
6. **`e.stopPropagation()`** su bottoni dentro righe cliccabili
7. **Mai cleanup automatico studenti** — la persistenza è sacra
8. **Sidebar classi MAI cliccabile** — niente `onClick`, niente `cursor-pointer`
9. **Testo verde nei PDF sempre italic, mai bold**
10. **`pdf-lib` per PDF, mai html2pdf**
11. **Input sidebar usano `!text-center`** (non `text-center` semplice) — lo shadcn/ui Input può sovrascrivere l'allineamento
12. **Hotspot studenti sempre grigio fisso** `bg-gray-300` — niente condizionale verde
13. **Schermata JOIN e Home usano la stessa struttura di laboratorioaumentato** — `<header>` + `<main>` semantici, `max-w-5xl`, `text-2xl sm:text-3xl`, `animate-pop-in 0.35s`
14. **Home page NON usa `<Card>` shadcn** — usa `<div>` raw con `bg-card border border-border/60 rounded-xl`
15. **Testo risposta esatta tutto maiuscolo 10pt font-normal** — conteggio studenti integrato nello stesso `<span>`
16. **Eliminazione classe SOLO dal pulsante ELIMINA CLASSE nella dashboard** — MAI cestino nella sidebar
17. **`<html lang="it">` e `<body class="antialiased">` in index.html** — MAI `lang="en"` o body senza classe
18. **`--font-sans` e `--font-serif` in `@theme inline`** — devono puntare a `Cambria, Georgia, "Times New Roman", serif`
19. **`body *` rule DEVE includere `:not(.preserve-case)`** — copiato da laboratorioaumentato
20. **La pagina embeddata nel blog è la Home (root `/`), NON il JOIN** — se il titolo sembra diverso da laboratorioaumentato, controllare Home.tsx, non StudentQuiz.tsx
