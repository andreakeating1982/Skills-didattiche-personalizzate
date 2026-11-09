# Archivio di dettaglio — becquer-quiz

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/quiz.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Panoramica
- Struttura del Progetto
- Database (Drizzle ORM + SQLite/Postgres)
- Schema: `drizzle/schema.ts`
- Endpoint tRPC (`server/routers.ts`)
- Classi
- Studenti
- Risposte
- Pagine Client
- StudentQuiz.tsx (Interfaccia Studente)
- TeacherPage.tsx (Dashboard Docente)
- Segmenti Audio e Mappatura Domande
- I 5 Segmenti Audio
- Mappatura Domande
- Regolazione Tempi Audio
- Pattern di UI Recenti (Sessioni Domande & Studenti Attivi)
- IN ATTESA DI INVIO (Per Domanda Corrente)
- Nome Studente (Non Troncato)
- Icone Risposte Corrette/Errate (Dropdown Studente)
- Card LETTURA INIZIALE / PAUSA DI LETTURA (Colori Uniformati)
- Schermata Studente: PREGUNTA X (niente testo domanda)
- PAUSA DI LETTURA (Schermata Studente): "Ascolta" non "Leggi"
- Tema Visivo (PLUM THEME)
- Palette Colori (`client/src/index.css`)
- Regole Globali CSS
- Override per le Pause di Lettura
- Pattern di Modifica Comuni
- Modificare le Domande del Quiz

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Bécquer Quiz

## Panoramica

L'app Bécquer Quiz è un'applicazione interattiva per quiz in classe basata su Vite + React + TypeScript + Tailwind CSS v4 + tRPC + Drizzle + SQLite. È un fork/adattamento dell'app Shakespeare Quiz, progettata per quiz letterari su Gustavo Adolfo Bécquer.

**Cartella progetto:** `/home/user/becquer-quiz`
**Deploy produzione:** `https://becquer-quiz.easy-peasy.site`

## Struttura del Progetto

```
becquer-quiz/
├── client/src/
│   ├── App.tsx                    # Router principale (wouter)
│   ├── const.ts                   # Costanti, domande del quiz
│   ├── index.css                  # Stili globali + PLUM THEME
│   ├── lib/
│   │   ├── reportPdf.ts           # Generazione PDF report (jsPDF)
│   │   └── trpc.ts                # Client tRPC
│   ├── pages/
│   │   ├── StudentQuiz.tsx        # Interfaccia studente
│   │   ├── TeacherPage.tsx        # Dashboard docente
│   │   └── LandingPage.tsx        # Pagina iniziale
│   ├── components/                # Componenti UI (shadcn)
│   └── public/audio/              # Segmenti audio .m4a
├── server/
│   ├── db.ts                      # DB queries (Drizzle ORM)
│   ├── routers.ts                 # Endpoint tRPC
│   ├── questions.ts               # Definizione domande
│   └── storage.ts                 # Storage backend
├── drizzle/                       # Migrazioni DB
├── deploy/                        # Dockerfile per produzione
└── shared/
    ├── const.ts                   # Costanti condivise
    └── types.ts                   # Tipi TypeScript
```

## Database (Drizzle ORM + SQLite/Postgres)

### Schema: `drizzle/schema.ts`

- **classi** — id, name, password, codice (codice classe), isActive, currentQuestion, startedAt, endedAt, phase, readingPauseStage, createdAt
- **studenti** — id, classId, name, score, completed, completedAt
- **risposte** — id, studentId, classId, questionNumber, selectedAnswer, isCorrect, submittedAt
- **classi_abilitate** — id, classId (tabella di lookup)

## Endpoint tRPC (`server/routers.ts`)

### Classi
- `classes.listAll` — elenca tutte le classi
- `classes.getById` — dettagli classe + codice
- `classes.create` — crea nuova classe (nome + password)
- `classes.enable` — abilita classe per accesso
- `classes.startSession` — avvia sessione (imposta phase="reading", readingPauseStage=1)
- `classes.nextQuestion` — passa alla domanda successiva
- `classes.startReadingPause` — avvia una pausa di lettura (incrementa readingPauseStage)
- `classes.revealAnswer` — mostra risposta corretta (setta currentQuestion come negativo)
- `classes.endSession` — termina sessione (setta endedAt)
- `classes.reset` — riavvia classe (elimina studenti + risposte)
- `classes.stats` — statistiche in tempo reale (studenti, risposte, punteggi)
- `classes.removeStudent` — rimuove studente dalla sessione

### Studenti
- `students.join` — registra studente (restituisce studentId)
- `students.getMyAnswers` — restituisce risposte già inviate dallo studente

### Risposte
- `answers.submit` — invia risposta (controlla se già risposta: errore se duplicata)
- `answers.submitAll` — invia tutte le risposte in blocco

## Pagine Client

### StudentQuiz.tsx (Interfaccia Studente)
1. **Schermata Join** — inserimento nome/cognome + codice classe. Bottone **HOME** con icona `House`.
2. **Schermata Attesa** — "In attesa che il docente avvii la sessione" se phase="reading"
3. **Schermata Quiz** — mostra **PREGUNTA {currentQNum}** (PREGUNTA 1, PREGUNTA 2, ...) al posto del testo della domanda, con opzioni A/B/C/D. Il testo reale della domanda NON è visibile allo studente. Al submit: feedback visivo (verde = corretto, rosso = errato). Pulsante "CONTINUA" marrone per proseguire.
4. **Re-entry** — se lo studente rientra, carica `getMyAnswers` e mostra le domande già risposte come bloccate ("Hai già risposto a questa domanda.")

### TeacherPage.tsx (Dashboard Docente)
1. **Seleziona/Riapri Classe** — scegli classe dalla lista o riapri con codice + password
2. **Pannello Controllo Sessione** — pulsanti: Avvia Sessione, Domanda Successiva, Rivela Risposta, Termina Sessione, Riavvia Classe
3. **Pausa Lettura** — schermata intermedia con titolo segmento, testo in case normale e giustificato, audio player, pulsante "CONTINUA"
4. **Studenti Attivi** — lista studenti con badge verde, punteggio in tempo reale, espansione risposte, pulsante rimozione
5. **Statistiche Classe** — grafici, medie percentuali, report PDF
6. **Report PDF** — genera PDF con dettagli studenti, risposte corrette/errate

## Segmenti Audio e Mappatura Domande

### I 5 Segmenti Audio
I file audio sono in `client/public/audio/segment_1.m4a` ... `segment_5.m4a`.

| # | Segmento | Durata | Audio termina con |
|---|---|---|---|
| 🎵1 | El autor | 0-105s | "...reconocimiento" |
| 🎵2 | Quintaesencia | 105-164s | "...lúgubre" |
| 🎵3 | Rimas | 164-207s | "...Romanticismo español" |
| 🎵4 | Estructura | 207-279.5s | "...sueños" (NON include il titolo del segmento successivo) |
| 🎵5 | Lenguaje | 279.5-384s | inizia con "3.2, lenguaje y estilo..." |

### Mappatura Domande
Le domande Q1-Q10 sono distribuite dopo ogni pausa di lettura:

| Pausa | Dopo lettura | Domande successive |
|---|---|---|
| PAUSA 1 (El autor) | Q1, Q2 | Q3 |
| PAUSA 2 (Quintaesencia) | Q3, Q4 | Q5 |
| PAUSA 3 (Rimas) | Q5 | Q6 |
| PAUSA 4 (Estructura) | Q6, Q7 | Q8 |
| PAUSA 5 (Lenguaje) | Q8, Q9, Q10 | Fine quiz |

Nel trigger del DB si attiva `readingPauseStage`: dopo Q2 → stage 2, dopo Q4 → stage 3, dopo Q5 → stage 4, dopo Q7 → stage 5.

### Regolazione Tempi Audio
I tagli audio vanno fatti con ffmpeg. Comando base:
```bash
ffmpeg -i audio_becquer.m4a -ss 0 -t 105 -c copy segment_1.m4a
```
`-ss` = start time, `-t` = durata. Per i tagli intermedi, calcolare posizioni precise con lo strumento di ascolto.

## Pattern di UI Recenti (Sessioni Domande & Studenti Attivi)

### IN ATTESA DI INVIO (Per Domanda Corrente)

La scritta **IN ATTESA DI INVIO** appare nella riga di ogni studente che **non ha ancora risposto alla domanda corrente** (non più in base al totale delle risposte).

**Logica in TeacherPage.tsx:**
```tsx
// Nuova variabile: controlla la domanda corrente, non il totale
const hasAnsweredCurrent = classDetail?.currentQuestion
  ? studentAnswers.some((a: any) => a.questionNumber === classDetail.currentQuestion)
  : false;

// Condizione per mostrare IN ATTESA
{!hasAnsweredCurrent && classDetail?.currentQuestion ? (
  <span className="text-sm font-bold text-amber-500 whitespace-nowrap">IN ATTESA DI INVIO</span>
) : (
  <span>...punteggio...</span>
)}
```

**Stile:** `text-sm font-bold text-amber-500 whitespace-nowrap` — arancione vivo, grassetto, **senza cornice/bordo**. Conservare anche la variabile originale `hasAnswers` (per controllare visibilità chevron espansione e contenuto espandibile).

### Nome Studente (Non Troncato)

Il nome dello studente nella sezione STUDENTI ATTIVI **non deve essere troncato**. Evitare `max-w-[130px]` e `truncate`:
```tsx
{/* ✅ Corretto */}
<span className="font-bold text-sm text-foreground cursor-default">{student.name}</span>

{/* ❌ Sbagliato: tronca i nomi lunghi */}
<span className="font-bold text-sm text-foreground truncate max-w-[130px] inline-block cursor-default">
```

### Icone Risposte Corrette/Errate (Dropdown Studente)

Nel menu espanso (`AnswerDetails`) della sezione studenti attivi, usare icone vuote invece di pallini pieni:
```tsx
{/* ✅ Corretto */}
<CheckCircle2 className="size-3.5 text-green-600 shrink-0" />  {/* corretto */}
<XCircle className="size-3.5 text-red-500 shrink-0" />          {/* errato */}

{/* ❌ Vecchio stile */}
<div className="size-3.5 rounded-full bg-green-600 ..."><Check className="..." /></div>
```

### Card LETTURA INIZIALE / PAUSA DI LETTURA (Colori Uniformati)

Le card di lettura **devono usare gli stessi colori del resto dell'app** (non stone/ambra):

| Proprietà | ❌ Vecchio | ✅ Nuovo |
|---|---|---|
| **Sfondo card** | `bg-stone-100` | `bg-muted/30` |
| **Bordo card** | `border-2 border-amber-300` | `border border-border/50` |
| **Icona Volume2** | `size-6 text-amber-700` | `size-5 text-plum` |
| **Titolo lettura** | `text-amber-800` | `text-foreground` |
| **Badge sezione** | `text-amber-700 bg-amber-200/80` | `text-plum/70 bg-plum/10` |
| **Card audio player** | `border-amber-200/60` | `border-border/40` |
| **Barra progresso** | `bg-amber-100` / `bg-amber-500` | `bg-muted` / `bg-plum` |
| **Pulsante Play/Pausa** | `border-amber-300 text-amber-700` | `border-border/60 text-plum` |
| **Hover riga studente** | `hover:bg-amber-50/40` | rimosso (solo `hover:bg-muted/60`) |

**Regola generale:** La palette dell'app è **plum** (viola caldo) + **grigio/muted**. Evitare toni stone/ambra/marrone che stonano con il resto dell'interfaccia.

### Schermata Studente: PREGUNTA X (niente testo domanda)

In `StudentQuiz.tsx` la schermata quiz **NON mostra più il testo della domanda** (es. "¿DÓNDE NACIÓ GUSTAVO ADOLFO BÉCQUER?"). Al suo posto viene mostrata l'etichetta **PREGUNTA {currentQNum}** (PREGUNTA 1, PREGUNTA 2, ... PREGUNTA 10).

```tsx
{/* ✅ Corretto — solo sezione + PREGUNTA X */}
<div className="text-center">
  {currentQ.sectionTitle && (
    <div className="text-xs font-bold text-plum/70 tracking-wider uppercase mb-2">{currentQ.sectionTitle}</div>
  )}
  <h2 className="text-xl sm:text-2xl font-bold text-foreground leading-snug">
    PREGUNTA {currentQNum}
  </h2>
</div>

{/* ❌ Vecchio — mostrava il testo della domanda + etichetta "DOMANDA X" ridondante */}
<p className="text-xs text-muted-foreground tracking-widest mb-2">DOMANDA {currentQNum}</p>
<h2 ...>{currentQ.question}</h2>
```

**Note:** il testo reale della domanda non è visibile allo studente (lo legge/pronuncia il docente). NON modificare la schermata docente (`TeacherPage.tsx`), che continua a mostrare il testo della domanda. `currentQNum` è il numero della domanda corrente nella sessione.

### PAUSA DI LETTURA (Schermata Studente): "Ascolta" non "Leggi"

Il testo di istruzione della pausa di lettura nella schermata studente è:

> **PAUSA DI LETTURA**
> *Ascolta tutto il prossimo paragrafo prima di procedere con le domande successive*

**Attenzione:** non ripristinare "Leggi" — il docente ha scelto "Ascolta" perché gli studenti ascoltano l'audio del paragrafo. Il testo si trova in `StudentQuiz.tsx` (vicino a `<h2>PAUSA DI LETTURA</h2>`); il titolo "PAUSA DI LETTURA" in `TeacherPage.tsx` è una card diversa e non va toccata.

## Tema Visivo (PLUM THEME)

### Palette Colori (`client/src/index.css`)
L'app usa un tema personalizzato "PLUM" (viola caldo + oro). Le variabili sono definite in `:root:root` (il doppio `:root` serve per aumentare la specificità e sovrascrivere i default generati da Tailwind v4):

```css
:root:root {
  --plum: oklch(55% .115 42);
  --gold: oklch(68% .1 72);
  --success: oklch(55% .12 145);
  --background: oklch(95.5% .015 85);    /* beige caldo */
  --foreground: oklch(26% .025 55);       /* marrone scuro */
  --primary: oklch(55% .115 42);          /* plum/viola */
  --accent: oklch(82% .055 42);           /* oro/ambra chiaro */
  --radius: 1.1rem;
  ...
}
```

**IMPORTANTE:** Usare sempre `:root:root` (doppio selettore) per le variabili CSS. Tailwind v4 genera il proprio `:root` inline con valori di default che sovrascriverebbero quelli custom.

### Regole Globali CSS
`client/src/index.css` applica queste regole con `!important` su TUTTI gli elementi:
```css
html, body, #root {
  text-align: center !important;
  text-transform: uppercase !important;
}
body *:not(input):not(textarea):not(select) {
  text-align: center !important;
  text-transform: uppercase !important;
}
```
**NON rimuovere queste regole globali** — sono intenzionali e danno coerenza visiva all'app.

### Override per le Pause di Lettura
Solo il testo delle pause di lettura deve essere giustificato e in case normale. Usare la classe dedicata:

```css
.reading-pause-text {
  text-align: justify !important;
  text-transform: none !important;
}
```
Applicata come `className="... reading-pause-text"` sul `<p>` della pausa lettura in TeacherPage.tsx. Non cambiare altri elementi.

## Pattern di Modifica Comuni

### Modificare le Domande del Quiz
**NON modificare a mano.** Usare la skill **quiz-adapter** che ha uno script Python per cambiare le domande automaticamente.

### Modificare la UI
- Tema visivo: palette marrone/plum (classi Tailwind `plum`, `plum/30`, `plum/40`)
- Componenti: shadcn/ui con Tailwind v4
- Icone: lucide-react
- Stili principali in `client/src/index.css` (Tailwind + CSS custom)
- **Non rimuovere le regole globali di uppercase/centrato** — aggiungere overrides mirati con classi dedicate

### Modificare i Testi delle Pause di Lettura
I testi sono in `TeacherPage.tsx` nell'array `READING_SECTIONS`. Ogni sezione ha:
```ts
{
  title: "1 · El autor",
  audio: "/audio/segment_1.m4a",
  text: "..."  // Testo in case normale (non uppercase)
}
```
Il testo deve essere in case normale (solo maiuscole dove necessario). Il box di lettura ha scorrimento (`max-h-48 overflow-y-auto`).

### Modificare il PDF Report
File: `client/src/lib/reportPdf.ts`
- Usa jsPDF con font Helvetica
- Margini: Top 2.5cm, Bottom/Left/Right 2.0cm
- Risposte corrette in verde corsivo (non grassetto)
- Usare `doc.splitTextToSize()` per text wrapping su testo lungo
- Controllare overflow pagina prima di sezioni summary
- Filtrare studenti rimossi dal report

### Modificare la Logica degli Studenti
- **Re-entry**: server controlla in `answers.submit` se lo studente ha già risposto (query su tabella `risposte`). Client carica risposte via `getMyAnswers` al mount.
- **Rimozione**: `removeStudent` elimina record studente + tutte le sue risposte dal DB

### Modificare il Contatore Studenti
- Il polling stats è a `refetchInterval: 2000` (2 secondi)
- Invalidate esplicito: `utils.classes.stats.invalidate()` in ogni mutation (startSession, nextQuestion, revealAnswer, resetClass, endSession, removeStudent)

## Comandi

```bash
# Development
cd /home/user/becquer-quiz
pnpm dev                    # Avvia server di sviluppo

# TypeScript
pnpm check                  # Controllo tipi (usare PRIMA di deploy)

# Database
pnpm db:push                # Genera migrazioni e applica
pnpm db:reset               # Cancella DB e ricrea
pnpm db:studio              # Apre Drizzle Studio

# ZIP del progetto (escludere node_modules, .git, dist)
cd /home/user && zip -r becquer-quiz.zip becquer-quiz/ \
  -x "becquer-quiz/node_modules/*" \
  -x "becquer-quiz/.git/*" \
  -x "becquer-quiz/dist/*" \
  -x "becquer-quiz/dev-server.log"

# Salva checkpoint (SEMPRE prima di deploy produzione)
webdev_save_checkpoint(...)
```

## Deploy

### Preview
```bash
webdev_deploy(mode="preview")
```
URL temporaneo: `https://3000-{sandbox-id}.sandbox.easy-peasy.ai/`

### Produzione
```bash
webdev_save_checkpoint()    # Prima: salva checkpoint
webdev_deploy(mode="production")
```
URL permanente: `https://becquer-quiz.easy-peasy.site`

**Regola:** MAI deployare produzione nella stessa risposta in cui si è scritto codice. Sequenza: checkpoint → preview → chiedere conferma → produzione.

## Risorse

### scripts/
Usare `quiz-adapter` per modificare le domande.

### references/
Vuoto. Documentazione su API tRPC e schema DB nella sezione "Database" e "Endpoint tRPC" sopra.

### templates/
Vuoto. Può contenere template JSON per domande o asset per il PDF.
