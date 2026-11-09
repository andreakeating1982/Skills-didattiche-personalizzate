# Architecture Reference

## 1. File Tree Funzionale

```
project-root/
├── client/src/
│   ├── App.tsx                  # Routing (3 routes) + iframe postMessage
│   ├── index.css                # Tema, utility CSS (center-placeholder, password-toggle-hide)
│   ├── pages/
│   │   ├── Home.tsx             # → STUDENT JOIN (codice 4 cifre → /schema?code=XXXX)
│   │   ├── StudentSchema.tsx     # → ATTIVITÀ INTERATTIVA (slot dropdown, fasi, submit)
│   │   └── TeacherPage.tsx      # → DASHBOARD DOCENTE (sidebar + main area)
│   ├── lib/
│   │   ├── trpc.ts              # tRPC client setup
│   │   └── reportPdf.ts         # Generazione PDF (report + blank)
│   └── components/ui/           # shadcn/ui components
├── server/
│   ├── routers.ts               # tRPC endpoints (classes, schema, answers)
│   ├── db.ts                    # Database helpers + in-memory store (showSolution)
│   ├── schema-data.ts           # → IL FILE DA MODIFICARE (dati del contenuto)
│   └── storage.ts               # R2 file storage (non usato dall'app base)
├── drizzle/
│   ├── schema.ts                # DB tables: classes, students, answers
│   └── migrations/              # Database migrations
├── shared/
│   ├── types.ts                 # Re-export dei tipi
│   └── const.ts                 # Costanti condivise
└── deploy/                      # Docker + Render config
```

## 2. Database Schema

### `classes`
| Field | Type | Notes |
|-------|------|-------|
| id | text PK | nanoid |
| name | text | Nome classe (es. "3A Liceo") |
| code | text UNIQUE | 4 cifre numeriche |
| password | text? | Per riaprire classe |
| isActive | boolean | Se la classe è visibile |
| sessionStarted | boolean | Se la sessione live è iniziata |
| date | text | Data (YYYY-MM-DD) |
| year | text | Anno scolastico |
| studentCount | integer | Numero studenti |
| createdAt | timestamp | Auto |

### `students`
| Field | Type | Notes |
|-------|------|-------|
| id | text PK | nanoid |
| classId | text FK→classes | Classe di appartenenza |
| name | text | Nome studente |
| score | integer | Punteggio (0-TOTAL_SLOTS) |
| completed | boolean | Attività completata |
| createdAt | timestamp | Auto |

### `answers`
| Field | Type | Notes |
|-------|------|-------|
| id | text PK | nanoid |
| studentId | text FK→students | Studente |
| classId | text FK→classes | Classe |
| slotId | text | Riferimento allo slot nello schema |
| selectedKeyword | text | Parola selezionata |
| isCorrect | boolean | Corretta o meno |
| createdAt | timestamp | Auto |

## 3. tRPC Endpoint Catalog

### `classes.*`
| Endpoint | Input | Output | Purpose |
|----------|-------|--------|---------|
| `create` | `{name, year?, date?, studentCount?, password?}` | Class | Nuova classe |
| `join` | `{code: 4-char, studentName}` | `{class, student}` | Studente entra |
| `getByCode` | `{code: 4-char}` | Class\|null | Verifica codice |
| `getById` | `{id}` | Class (con showSolution) | Info classe |
| `listActive` | — | Class[] | Classi attive |
| `listAll` | — | Class[] | Tutte le classi |
| `startSession` | `{id}` | Class | Avvia sessione |
| `endSession` | `{id}` | Class | Termina sessione |
| `close` | `{id}` | Class | Chiudi classe |
| `reopen` | `{code, password}` | Class | Riapri classe |
| `reset` | `{id}` | Class | Reset (cancella studenti+risposte) |
| `delete` | `{id}` | Class | Elimina classe |
| `removeStudent` | `{studentId}` | Student | Rimuovi studente |
| `setShowSolution` | `{id, show: 0\|1}` | `{id, showSolution}` | Mostra/nascondi soluzione |
| `getStudents` | `{id}` | Student[] | Studenti della classe |
| `stats` | `{id}` | Stats | Statistiche |
| `report` | `{id}` | ReportData | Dati per PDF |

### `schema.*`
| Endpoint | Input | Output | Purpose |
|----------|-------|--------|---------|
| `rows` | — | SchemaRow[] | Righe dello schema |
| `keywords` | — | string[] | Tutte le keyword |
| `totalSlots` | — | number | Numero slot totali |
| `slots` | — | SchemaSlot[] | Slot con opzioni |

### `answers.*`
| Endpoint | Input | Output | Purpose |
|----------|-------|--------|---------|
| `submit` | `{studentId, classId, slotId, selectedKeyword, isCorrect}` | Answer | Salva risposta |
| `list` | `{studentId}` | Answer[] | Risposte studente |
| `complete` | `{studentId, score}` | Student | Completa attività |

## 4. Flussi Utente

### Flusso Studente
```
Home.tsx → codice 4 cifre + ENTRA → /schema?code=XXXX
→ Inserisce nome → joined=true
→ Vede schema con slot dropdown per ogni fase
→ Seleziona keyword per ogni slot → SUBMIT
→ Risultati fase per fase
→ COMPLETA → score salvato
```

### Flusso Docente
```
/docente → sidebar: CREA CLASSE (nome + password)
→ Codice #XXXX generato → classe nella sidebar
→ Seleziona classe → card classe principale
→ AVVIA SESSIONE → studenti possono entrare
→ Vede contatore studenti attivi, tabella risposte
→ (opzionale) MOSTRA RISPOSTA ESATTA
→ TERMINA SESSIONE → genera report PDF
→ (opzionale) RIAPRI CLASSE DA CODICE
```

## 5. In-Memory State

Il flag `showSolution` (mostra risposta esatta) è gestito in memoria via `Map<string, number>` in `server/db.ts`. **Non è persistito** — si azzera al riavvio del server. Questo è intenzionale: la soluzione si resetta automaticamente per ogni nuova sessione.

## 6. PDF Generation

- **jsPDF** con font built-in "times"
- Report PDF: 1 pagina per studente con risposte raggruppate per fase
- Blank PDF: schema vuoto per pratica, **data lasciata in bianco** (lo studente scrive a mano)
- I colori delle fasi sono hardcoded in `reportPdf.ts`

## 7. Iframe Embed

In `App.tsx`, un `ResizeObserver` invia `window.parent.postMessage({ type: "labvisivo:height", height }, "*")`.
Questo fa sì che l'iframe si ridimensioni automaticamente nell'host (Blogger, sito scolastico, etc.).
