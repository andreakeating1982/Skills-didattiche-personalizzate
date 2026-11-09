---
name: laboratorio-aumentato-3d
description: "Manutenzione, personalizzazione e clonazione dell'app LABORATORIO AUMENTATO 3D SORGENTE (Vite + React + TypeScript + Tailwind + tRPC + Drizzle + PostgreSQL, scaffold web-db-user). Usare per MANUTENZIONE: modificare UI studente/docente, allineare stili a Shakespeare Quiz, deploy preview/produzione, personalizzare report PDF (una pagina per gruppo, foto non ritagliate), rinominare l'app, modificare testi/consegna, gestire stato classe (chiudi/riavvia/elimina), eliminare gruppi (trash bin nelle card + endpoint submissions.delete), cornice dinamica (embed Blogger), margini della prima pagina (WelcomePage), footer. Usare per CLONAZIONE: creare una NUOVA app identica con contenuto diverso (contenuto dell'attività: tema, istruzioni dei 6 passi studente, criteri della rubrica) tramite scripts/clone_app.py (anche da repository GitHub con --source), lasciando invariati struttura a 6 passi, dashboard docente (crea/riapri/chiudi/elimina classe), codici a 4 cifre, contatore, report PDF, palette plum/gold ed embed iframe."
---

# Laboratorio Aumentato 3D (Sorgente) — manutenzione + clonazione

App interattiva per laboratori scolastici multimediali (AR, audiovisivo), chiamata **LABORATORIO AUMENTATO 3D SORGENTE**. Questa skill unica copre DUE modalità d'uso:

- **PARTE 1 — Manutenzione**: modificare/personalizzare l'app sorgente stessa.
- **PARTE 2 — Clonazione**: creare una nuova app identica con contenuto diverso.

L'app di riferimento per lo stile è **Shakespeare Quiz** (`/tmp/shakespeare-quiz`). Basata su scaffold `web-db-user`.

## Percorsi

- **Progetto / app sorgente locale**: `/home/user/laboratorio-visivo`
- **Preview sorgente**: https://3000-iycc2cajgdo49lj9lv8lq.sandbox.easy-peasy.ai/
- **Production sorgente**: https://laboratorio-visivo-2.easy-peasy.site
- **Script di clonazione**: `/home/user/skills/laboratorio-aumentato-3d/scripts/clone_app.py`
- **Template config**: `/home/user/skills/laboratorio-aumentato-3d/templates/config_esempio.json`

> Se l'utente ha caricato l'app sorgente su GitHub, chiedigli l'URL del repository e usalo come `--source` per la clonazione (vedi Parte 2). Non serve che l'app sia presente in locale.

## Cos'è l'app (struttura FISSA, non cambia mai)

L'app è un **laboratorio di consegna elaborati a gruppi** con 6 passi per lo studente:

1. **PASSO 1** — scelta del gruppo (griglia di numeri cliccabili)
2. **PASSO 2** — componenti del gruppo (cognome + nome, fino a 3)
3. **PASSO 3** — elaborato visivo (upload foto/screenshot, max 3)
4. **PASSO 4** — spiegazione scritta (textarea)
5. **PASSO 5** — audio lettura (MP3)
6. **PASSO 6** — audio spiegazione (MP3)

Più la **dashboard docente** (crea/riapri/chiudi/elimina classe, rubrica di valutazione 1-4, report PDF stampabile, contatore lavori consegnati) e l'**embed iframe** con postMessage `labvisivo:height`.

Stack: Vite + React + TypeScript + Tailwind + tRPC + Drizzle + PostgreSQL (scaffold `web-db-user`). Schema DB: `classes`, `submissions`, `evaluations` in `drizzle/schema.ts`.

---

# PARTE 1 — MANUTENZIONE dell'app sorgente

## Palette e tipografia

L'app ha un tema caldo/terroso (carta vintage). I colori personalizzati in `client/src/index.css`:

| Variabile | Valore |
|-----------|--------|
| `--plum` | `oklch(55% .115 42)` — primario per icone e accenti |
| `--gold` | `oklch(68% .1 72)` — accenti secondari |
| `--success` | `oklch(55% .12 145)` — stati positivi |
| `--primary` | `oklch(55% 0.115 42)` — sfondo bottoni (stesso di plum) |

Font: `Cambria, Georgia, "Times New Roman", serif` con `text-transform: uppercase` globale.

Tutti gli input hanno `text-align: left` e `text-transform: none` (override globale). **Nella sidebar docente** gli input vanno centrati con `!text-center` (cursore e testo partono dal centro). Fuori dalla sidebar (es. dashboard) resta `!text-left`.

## Regole di stile per l'allineamento a Shakespeare Quiz

### Bottoni

Usare **sempre** il componente shadcn `<Button>` (mai `<button>` raw) per i pulsanti primari:

```tsx
import { Button } from "@/components/ui/button";

<Button onClick={handler} disabled={condition} className="w-full h-9 text-sm font-semibold" size="sm">
  {loading ? <Loader2 className="size-4 animate-spin" /> : "TESTO"}
</Button>
```

### Regola RIAPRI: mai disabilitare per campi vuoti

Il pulsante RIAPRI **NON deve mai avere `disabled` legato alla validazione dei campi** (codice/password). La validazione avviene SOLO al click con toast di errore, come in Shakespeare Quiz:

```tsx
// ✅ CORRETTO — solo loading come condizione di disable
<Button onClick={handleReopen} disabled={reopening} className="w-full h-9 text-sm font-semibold" size="sm">
  {reopening ? <Loader2 className="size-4 animate-spin" /> : "RIAPRI"}
</Button>

// ❌ SBAGLIATO — NON condizionare il disabled ai campi vuoti
<Button onClick={handleReopen} disabled={reopening || code.length !== 4 || !password.trim()} ...>
```

Validazione al click (con toast, non silenziosa):
```tsx
const handleReopen = async () => {
  if (reopenCode.length !== 4) { toast.error("Inserisci un codice valido di 4 cifre"); return; }
  if (!reopenPassword.trim()) { toast.error("Inserisci la password della classe."); return; }
  // ... api call
};
```

Così il pulsante ha sempre hover (`hover:bg-primary/90`), colore pieno e cursore pointer — identico a CREA CLASSE.

### Input

Usare `rounded-md border bg-transparent` (NON `rounded-lg border-input bg-white font-sans`):

```tsx
// Input nella dashboard (allineati a sinistra)
<input className="w-full h-9 px-3 rounded-md border bg-transparent text-sm !text-left" />

// Input nella sidebar (centrati, cursore al centro)
<input className="w-full h-9 px-3 rounded-md border bg-transparent text-sm !text-center" />
```

Se l'input ha un'icona a sinistra: `pl-8` con icona `left-2.5`.

### Icone

- Icona principale (edificio scuola): `School` da `lucide-react`, contenitore `bg-plum/10` con `text-plum`
- Icona sezione "APRI UNA NUOVA CLASSE": `Plus` con `text-plum`
- Icona sezione "RIAPRI UNA CLASSE": `KeyRound` con `text-plum`
- Icona codice: `Hash` posizionato `left-2.5`

### Link di navigazione

I link "Area docente" / "Area studenti" usano `<a>` (NON `<button>`) con stile:

```tsx
<a href="/docente" className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3.5 py-2 text-sm font-medium text-foreground shadow-sm transition hover:border-plum/40 hover:text-plum">
  <School className="size-4" />
  Area docente
</a>
```

### Spaziatura sidebar

Usare `space-y-2` (non `space-y-2.5`) tra gli elementi della sidebar.

### Link AREA DOCENTI (Home.tsx)

Il link "Area docente" nella schermata studente deve avere `mb-4` per distanziarlo dalla card sottostante:

```tsx
<a href="/docente" className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3.5 py-2 text-sm font-medium text-foreground shadow-sm transition hover:border-plum/40 hover:text-plum mb-4">
```

### Placeholder dashboard (nessuna classe selezionata)

Il testo mostrato quando nessuna classe è selezionata:
> "Crea una nuova classe dalla barra laterale oppure riaprine una già esistente."

## Pagine chiave

### `client/src/pages/Home.tsx`
Schermata studente (prima pagina) con **margini pareggiati** (vedi sezione "Margini prima pagina"). Contiene `<h1>` titolo, link "Area docente", card con codice classe. NON ha più `min-h-screen` né footer. Usa `School` da lucide-react.

### `client/src/pages/TeacherDashboard.tsx`
Dashboard docente completa con sidebar (crea/riapri classe, lista classi) e pannello principale (gestione sessione, rubric, report). È il file più grande (oltre 1200 righe). Importa `Button` da shadcn, `Loader2`, `KeyRound` e `Trash2` da lucide-react.

### `client/src/pages/StudentSubmit.tsx`
Invio elaborati studente per gruppo.

## Dashboard docente: centratura e valutazioni (rev. 2026-09)

Nella dashboard docente TUTTO è centrato (niente più `text-left` nelle card/dettaglio/valutazione):

- **Card gruppo** (`LAVORI CONSEGNATI`): `text-center`; header titolo+stella e data su due righe (`flex flex-col items-center gap-1`); badge componenti, indicatori (foto/spiegazione/lettura/audio) e badge voto con `justify-center`.
- **Dettaglio gruppo**: header "Gruppo N — N componenti" centrato; titoli sezione (`Componenti`, `Elaborato visivo`, `Spiegazione`, `Lettura in spagnolo`, `Spiegazione audio`) con `text-center`; badge componenti con `justify-center`; foto `flex flex-wrap justify-center`.
- **Sezione valutazione**: `Rubrica di valutazione` con `justify-center`; `Valutazione di gruppo` con `text-center`; etichette e descrizioni dei criteri con `text-center`.

**Campo "Note (facoltative)" RIMOSSO**: il textarea `Note (facoltative)` non esiste più, insieme al campo `notes` del tipo `ScoreState`, al salvataggio e al caricamento della valutazione. NON riaggiungerlo (non è più né scritto né letto).

**Pulsanti "Modifica" e trash nella lista valutazioni RIMOSSI**: le righe delle valutazioni esistenti mostrano SOLO stella + "Valutazione di gruppo" + punteggio (centrate). Rimossi i pulsanti "Modifica" e il trash (elimina singola valutazione) e le relative funzioni `loadEvalScores`, `handleDeleteEval` e la mutation `deleteEvalMutation`. L'endpoint server `evaluations.delete` resta ma non è più usato dal client.

## Eliminazione gruppo (trash bin nelle card)

Ogni card gruppo ha un trash bin "Elimina" (icona `Trash2` + testo) centrato accanto ad "Audio" nella riga indicatori. Alla conferma elimina gruppo + valutazioni + file (foto/audio).

```tsx
<button
  type="button"
  onClick={(e) => { e.stopPropagation(); handleDeleteGroup(sub); }}
  aria-label={`Elimina il gruppo ${sub.groupNumber}`}
  className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-destructive transition-colors"
>
  <Trash2 className="w-3 h-3" /> Elimina
</button>
```

```tsx
// dichiarare accanto alle altre mutation:
const deleteSubmissionMutation = trpc.submissions.delete.useMutation();

const handleDeleteGroup = async (sub: any) => {
  if (!confirm(`Eliminare definitivamente il Gruppo ${sub.groupNumber}? L'azione non è reversibile.`)) return;
  try {
    await deleteSubmissionMutation.mutateAsync({ submissionId: sub.id });
    toast.success(`Gruppo ${sub.groupNumber} eliminato.`);
    if (selectedSubmission?.id === sub.id) { setSelectedSubmission(null); setScores({}); }
    await submissionsQueryByClass.refetch();
    await evaluationsQueryByClass.refetch();
  } catch (e: any) {
    toast.error(e?.message || "Errore durante l'eliminazione.");
  }
};
```

Endpoint server `submissions.delete` in `server/routers.ts` (con `import { deleteFile } from "./storage";` in cima):

```ts
delete: publicProcedure
  .input(z.object({ submissionId: z.string() }))
  .mutation(async ({ input }) => {
    const d = requireDb();
    const [sub] = await d.select().from(schema.submissions).where(eq(schema.submissions.id, input.submissionId));
    if (!sub) return { success: true };
    await d.delete(schema.evaluations).where(eq(schema.evaluations.submissionId, input.submissionId));
    await d.delete(schema.submissions).where(eq(schema.submissions.id, input.submissionId));
    const keys: string[] = [];
    if (Array.isArray(sub.photos)) for (const p of sub.photos as any[]) { if (p?.fileKey) keys.push(p.fileKey); }
    if (sub.audioReadingKey) keys.push(sub.audioReadingKey);
    if (sub.audioExplanationKey) keys.push(sub.audioExplanationKey);
    for (const k of keys) { try { await deleteFile(k); } catch {} }
    return { success: true };
  }),
```

**Card gruppo = `<div role="button">`** (NON `<button>`): così può contenere il trash bin (i bottoni annidati non sono validi). Aggiungere `role="button" tabIndex={0} aria-pressed={isSelected} cursor-pointer focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary` e gestire Enter/Space con `onKeyDown` (stesso toggle dell'`onClick`).

## Report PDF e layout foto/mobile (rev. 2026-09)

- **PDF una pagina per gruppo**: ogni gruppo inizia su una nuova pagina — `<div class="section"${idx > 0 ? ' style="page-break-before:always"' : ''}>` nel `sortedSubs.forEach((sub, idx) => ...)`.
- **Foto nel PDF NON ritagliate**: `.photo-grid { display:flex; flex-wrap:wrap; justify-content:center; gap:8px }` e `img { width:150px; height:112px; object-fit:contain; background:#f3efe8; border-radius:5px; border:1px solid #e5ded2 }` (NON grid, e MAI `object-fit:cover` che ritaglia le foto consegnate dagli studenti).
- **Layout mobile docente**: radice `lf-docente min-h-dvh` (NON `min-h-screen`/100vh, che su mobile fa tremare la pagina quando la barra del browser si nasconde), card `lf-docente-card`, body `lf-docente-body`; i vincoli `sm:min-h-[580px]`, `sm:max-h-[92vh]` e `sm:overflow-hidden` sono SOLO su `sm:` (su mobile niente taglio/overflow).
- **Anti-tremolio (heightSync)**: in `client/src/lib/heightSync.ts` l'invio altezza è debounced via `requestAnimationFrame` e scatta solo se l'altezza cambia di `>= 2px` (funzione `scheduleSend()` con `lastHeight`/`rafPending`). Evita il loop di resize che fa tremare l'app dentro l'iframe. NON tornare a chiamare `sendHeight()` direttamente nel ResizeObserver.
- **Bottoni voto (1-4)**: usare `transition-colors` (NON `transition-all`) e NIENTE `scale-105` sullo stato selezionato (scale + transition-all = scatti sul touch). Lo stato selezionato resta evidente con `level.color + " border-current shadow-sm"`.
- **Foto studente**: `flex flex-wrap justify-center gap-3`, foto `w-28 sm:w-40 aspect-square shrink-0`, max 3 foto (`photos.length < 3`). Nel dettaglio docente stesse dimensioni con `flex flex-wrap justify-center`.
- **Icone che straripano**: aggiungere `shrink-0` a Star/Trash2 ecc.; contenuto riga valutazione con `min-w-0 flex-1`.

## Deploy

```bash
# Preview (sviluppo)
webdev_deploy project_dir="/home/user/laboratorio-visivo" mode="preview"

# Checkpoint (obbligatorio prima di production)
webdev_save_checkpoint project_dir="/home/user/laboratorio-visivo" description="..."

# Production (solo dopo conferma utente)
webdev_deploy project_dir="/home/user/laboratorio-visivo" mode="production"
```

## Rinominare l'app

Modificare in 4 file:
1. `client/index.html` — `<title>` e `<meta name="description">`
2. `client/src/pages/Home.tsx` — `<h1>`
3. `client/src/pages/TeacherDashboard.tsx` — titolo header + chiave localStorage (`lv2_active_class_id`)
4. `client/src/pages/StudentSubmit.tsx` — eventuali riferimenti

## Cornice dinamica (embed per Blogger)

La cornice dinamica è in `cornice-dinamica/` (cartella a livello di progetto, NON servita dall'app). File:

| File | Uso |
|---|---|
| `embed-laboratorio-aumentato-3d-dedicata.html` | ⭐ embed dedicato da incollare nel post (v3 impermeabile + anti-loop v4: titolo+pulsanti sulla stessa riga centrati, Schermo intero, Ricarica, stato online/errore, ping) |
| `embed-laboratorio-aumentato-3d-lite.html` | versione leggera (~5 KB), font OpenDyslexic via CORS |
| `embed-laboratorio-aumentato-3d.html` | autosufficiente (~110 KB), font in base64 |
| `embed-universale.html` | template per ALTRE app (cambiare solo `APP_URL`/`APP_TITLE`) |
| `test-dedicata.html`, `test-impermeabile.html` | pagine di test |
| `README.md` | documentazione |
| `fonts/` | i WOFF2 serviti via CORS |

**Protocollo altezza** `labvisivo:height` + ping `labvisivo:ping`, con token `?cornice=<token>` rispecchiato dall'app nei messaggi. La sincronizzazione NON è in `App.tsx`: è in `client/src/lib/heightSync.ts`, esportata come `initHeightSync()` e chiamata in `main.tsx`. `heightSync.ts`:
- aggiunge `lf-embedded` a `<html>` quando `window.self !== window.top`;
- invia l'altezza solo se dentro iframe e solo se `height > 100`;
- risponde ai ping (ResizeObserver su `documentElement`/`body` + timer); l'invio è debounced via `requestAnimationFrame` e scatta solo se l'altezza cambia di `>= 2px` (`scheduleSend()` con `lastHeight`/`rafPending`).

**CORS font**: `server/_core/index.ts` ha `app.use("/fonts", ...)` con `Access-Control-Allow-Origin: *` (la cornice carica OpenDyslexic cross-origin). Font serviti: `OpenDyslexic-Regular-v2.woff2` e `OpenDyslexic-Bold-v2.woff2` in `client/public/fonts/`.

**Rigenerare la cornice**: se cambia l'URL di produzione, aggiornare `APP_URL` (e il `@font-face` `src`) in tutti gli `embed-*.html`. La cornice NON richiede deploy: è HTML autonomo da incollare nella vista HTML di Blogger.

## Margini prima pagina (WelcomePage)

La prima pagina NON usa `min-h-screen`: il contenuto sta subito sotto la barra di accessibilità e la pagina termina subito dopo la card (niente vuoto sopra/sotto; 24px simmetrici sopra/sotto nella cornice).

In `client/src/pages/Home.tsx`:
- radice: `lf-welcome flex flex-col items-center bg-background paper-grain px-4 pb-8 sm:pb-12` (NON `min-h-screen`)
- primo figlio (wrapper): `<div className="flex w-full flex-col items-center pt-4 sm:pt-8">` — DEVE essere il `> div:first-child` di `.lf-welcome`
- `useEffect` che aggiunge `lf-welcome-top` a `<html>` solo quando `window.self === window.top` (pagina autonoma)
- header `mb-4 sm:mb-5`, main `w-full flex justify-center` (niente `flex-1`/`items-start`/`pb-16`)

Regole CSS in `client/src/index.css`:
- `html.lf-embedded .lf-welcome` → `min-height:0`, `padding-top:20px`, `padding-bottom:24px`
- `html.lf-embedded .lf-welcome > div:first-child` → `padding-top:0`
- `html.lf-welcome-top .lf-welcome::after` → dissolvenza bianca 48px in fondo al blocco crema (pagina autonoma)

## Footer (assente)

NON esiste alcun footer "REALIZZATO DA ANDREA CENTINARO": è stato rimosso da tutte le pagine e dai PDF. Non riaggiungerlo. Punti dove NON c'è più: `Home.tsx`, `StudentSubmit.tsx` (2 viste), `TeacherDashboard.tsx` (JSX "DOWNBAR" + 2 report PDF); anche le regole CSS `.footer` sono state eliminate.

## Testi personalizzabili

In `client/src/pages/StudentSubmit.tsx` le istruzioni per gli studenti sono scritte in italiano generico (senza riferimenti ad autori specifici):
- Spiegazione: NON contiene riferimenti ad autori (es. Rosalía de Castro)
- Lettura audio: "in lingua straniera" (NON "in spagnolo")

## ELIMINA CLASSE

Il pulsante ELIMINA CLASSE è nella dashboard (NON nella sidebar). Comportamento:

1. Pulsante rosso con icona `Trash2`, visibile solo quando una classe è selezionata
2. Click → `confirm()` di conferma
3. Chiama l'endpoint `classes.delete` (verifica password insegnante)
4. Cancella dal DB: classe, submission, valutazioni
5. Rimuove dalla lista sidebar e chiude immediatamente la dashboard

```tsx
// Pulsante (nella dashboard, sotto il titolo classe)
<button
  onClick={handleDeleteClass}
  disabled={deleteClassMutation.isPending}
  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-red-300 bg-red-50 text-red-600 text-xs font-medium hover:bg-red-100 hover:border-red-400 transition-colors disabled:opacity-50"
>
  <Trash2 className="size-3.5" />
  ELIMINA CLASSE
</button>
```

```tsx
// Handler
const handleDeleteClass = async () => {
  if (!selectedClass) return;
  if (!confirm(`Eliminare definitivamente "${selectedClass.name}"? L'azione non è reversibile.`)) return;
  try {
    await deleteClassMutation.mutateAsync({
      classId: selectedClass.id,
      teacherPassword: selectedClass.teacherPassword,
    });
    setClasses((prev) => prev.filter((c) => c.id !== selectedClass.id));
    setSelectedClassId(null);
    setSelectedSubmission(null);
    setSubmissions([]);
    setEvaluations([]);
    toast.success("Classe eliminata definitivamente");
  } catch (e: any) {
    toast.error(e?.message || "Errore durante l'eliminazione.");
  }
};
```

Endpoint server in `server/routers.ts`:
```tsx
delete: publicProcedure
  .input(z.object({ classId: z.string(), teacherPassword: z.string() }))
  .mutation(async ({ input }) => {
    const d = requireDb();
    const [cls] = await d.select().from(schema.classes).where(eq(schema.classes.id, input.classId));
    if (!cls) throw new Error("Classe non trovata.");
    if (cls.teacherPassword !== input.teacherPassword) throw new Error("Password insegnante errata.");
    await d.delete(schema.classes).where(eq(schema.classes.id, input.classId));
    // submissions + evaluations vengono eliminate via ON DELETE CASCADE
    return { success: true };
  }),
```

**NB**: La sidebar NON ha più l'icona trash — la lista classi mostra solo nome e codice, con pallino verde (attiva) / grigio (chiusa).

## CHIUDI / RIAVVIA CLASSE

Il pulsante **CHIUDI** (nella dashboard, accanto al codice) disattiva la classe impostando `isActive = false`. Comportamento:

1. Click → chiama `classes.close` (verifica password insegnante) → toast "Classe chiusa!"
2. Nella dashboard compare la card "Questa classe è chiusa. Riavvia per iniziare una nuova sessione." con il pulsante **RIAVVIA CLASSE** (chiama `classes.reset`, riporta `isActive = true`)
3. Il pulsante CHIUDI scompare (sostituito dal RIAVVIA nella card) finché la classe è chiusa
4. Lo studente che accede a una classe chiusa vede la schermata **"IL DOCENTE HA CHIUSO LA CLASSE"** ("La sessione è terminata. Grazie per aver partecipato!") con pulsante HOME
5. Lo studente ricontrolla lo stato ogni 3s (`refetchInterval`), quindi vede la chiusura anche a schermo aperto

Il campo `is_active` è nel DB (`ALTER TABLE classes ADD COLUMN IF NOT EXISTS is_active boolean NOT NULL DEFAULT true;`) e le procedure server sono `classes.close` e `classes.reset`. Il campo non si rimuove.

## Differenze rispetto a Shakespeare Quiz

- Nome app: "LABORATORIO AUMENTATO 3D" vs "SHAKESPEARE QUIZ"
- Shakespeare Quiz è in `/tmp/shakespeare-quiz` (sola lettura, riferimento)
- Laboratorio Aumentato 3D ha campi extra nella creazione classe: N. gruppi, Data, Titolo del progetto
- Shakespeare Quiz NON ha `KeyRound` (usa `Key` in alcune versioni)
- Entrambi condividono la stessa palette (`--plum`, `--primary`, `--gold`)
- **RIAPRI**: in SQ il pulsante non è mai disabilitato per campi vuoti — la validazione avviene al click con toast
- **Embed**: Laboratorio Aumentato 3D supporta embedding iframe con postMessage auto-resize; SQ no
- **Testi**: Laboratorio Aumentato 3D ha istruzioni generiche (no autore specifico, "lingua straniera"); SQ ha testi fissi su Shakespeare

---

# PARTE 2 — CLONAZIONE (nuova app con contenuto diverso)

Clona l'app sorgente in una nuova app identica cambiando SOLO il contenuto dell'attività. Supporta il clone da **cartella locale** o da **repository GitHub**.

## Il contenuto VARIABILE dell'attività

Per questa app il **contenuto VARIABILE** è: il tema trattato, i testi delle istruzioni dei 6 passi e i criteri della rubrica. Cambiare "solo il contenuto dell'attività" = cambiare questi testi, lasciando intatta tutta la logica (flusso, DB, API, UI, colori, report).

## Procedura di clonazione (script — consigliata)

### 1. Prepara il config JSON (opzionale ma consigliato)

Usa `templates/config_esempio.json` come modello. Contiene:
- `theme_words` — parole-tema da sostituire globalmente (default: `"spagnolo" → "lingua straniera"`)
- `meta_description` — nuovo testo del `<meta name="description">`
- `steps` — i 10 testi delle istruzioni (step3_desc … step6_subtext)
- `rubric` — array di 5 criteri con `key`, `label`, `desc`

Le chiavi `key` della rubrica sono FISSE (legate alle colonne DB): `pertinenzaTema`, `originalita`, `qualitaTecnica`, `qualitaLettura`, `rispettoTempi`.

### 2. Esegui lo script

```bash
# Da cartella locale (default)
python3 /home/user/skills/laboratorio-aumentato-3d/scripts/clone_app.py \
  --dest /home/user/<nuova-app> \
  --title "NUOVO TITOLO" \
  --config config.json

# Da repository GitHub (l'utente l'ha caricata su GitHub)
python3 /home/user/skills/laboratorio-aumentato-3d/scripts/clone_app.py \
  --source https://github.com/USER/REPO.git \
  --dest /home/user/<nuova-app> \
  --title "NUOVO TITOLO" \
  --config config.json
```

Lo script esegue 5 passi:
1. **Clone** della sorgente (git clone per URL GitHub, copia `tar` per cartella locale, escludendo `node_modules`/`.git`/`dist`/`.vite`)
2. **Titolo** — sostituisce `LABORATORIO AUMENTATO 3D` e `Laboratorio Aumentato 3D` in `index.html`, `Home.tsx`, `StudentSubmit.tsx` (3×), `TeacherDashboard.tsx`
3. **Chiave localStorage** — `laboratorio_audiovisivo_classes` → `<slug>_classes` (slug derivato dal nome di `--dest`)
4. **Contenuto** (solo se `--config`) — istruzioni dei passi + rubrica (label mixed/uppercase + desc) + meta description. Eseguito PRIMA delle parole-tema: così la rubrica "…in spagnolo" viene sostituita dal config prima della conversione globale spagnolo→lingua straniera.
5. **Parole-tema** — sostituisce globalmente `spagnolo`→`lingua straniera` (e varianti di maiuscole) in `client/src` e `server`

### 3. Verifica

```bash
cd /home/user/<nuova-app>
pnpm install
pnpm check     # nessun errore TypeScript
pnpm build     # build produzione ok
# controlla che non restino stringhe del tema vecchio:
grep -rn "poesia\|spagnolo\|realtà aumentata\|Laboratorio Aumentato" client/src server/
```

## Procedura di clonazione (manuale — fallback)

Se lo script non è disponibile o serve un controllo fine, i punti da modificare sono:

| File | Cosa cambiare |
|------|---------------|
| `client/index.html` | `<title>` e `<meta name="description">` |
| `client/src/pages/Home.tsx` (~32) | `<h1>` |
| `client/src/pages/StudentSubmit.tsx` (~189, ~262) | `<h1>` (2×) + 4 blocchi istruzioni (PASSO 3-6) |
| `client/src/pages/TeacherDashboard.tsx` (~16-21, ~394-398, ~495-499) | rubrica in 3 punti (UI + 2 nel report PDF) + riga ~55 chiave localStorage + righe ~383 e ~951 "spagnolo" |
| `client/src/pages/TeacherClass.tsx` | file LEGACY non instradato (non usato) — contiene altri "spagnolo"; ignorabile |

Attenzione: i `key` della rubrica e le colonne dello schema (`coerenza`, `contributo`, `autonomia`, `riflessione`, ecc.) NON si rinominano.

## Cosa NON toccare (struttura FISSA)

- `drizzle/schema.ts` — tabelle `classes`, `submissions`, `evaluations` (NON rinominare le colonne dei criteri; il campo `is_active`/`isActive` di `classes` è parte della struttura fissa)
- `server/routers.ts` — endpoint tRPC e validatori (le chiavi dei criteri restano identiche; le procedure `close` e `reset` che gestiscono `isActive` sono parte della struttura fissa)
- Logica dashboard: crea/riapri/chiudi/elimina classe, `RIAPRI` mai disabilitato (validazione al click con toast), `ELIMINA CLASSE` con `confirm()`, `CHIUDI` (isActive=false) + `RIAVVIA CLASSE` (isActive=true)
- Schermata studente: `IL DOCENTE HA CHIUSO LA CLASSE` (quando isActive=false) e `CLASSE NON TROVATA` (quando eliminata) — fanno parte della struttura fissa
- Componenti UI shadcn (`Button`, `Input`), palette `--plum`/`--gold`/`--success`, font Cambria/Georgia con uppercase globale
- Input sidebar centrati (`!text-center`), data con overlay `gg/mm/aaaa` e icona calendario nascosta
- Cornice dinamica (`cornice-dinamica/`) e postMessage `labvisivo:height` in `client/src/lib/heightSync.ts` (chiamato da `main.tsx` via `initHeightSync()`); la prima pagina NON ha footer e usa i margini pareggiati (classi `lf-welcome`/`lf-embedded`)
- Il routing: `/` Home, `/studente/:classCode/:groupNumber`, `/docente` (NON aggiungere `TeacherClass.tsx`)

## Deploy, ZIP, embed (per la nuova app)

- **Preview**: `webdev_deploy project_dir="/home/user/<nuova-app>" mode="preview"`
- **Checkpoint** (obbligatorio prima di production): `webdev_save_checkpoint project_dir="/home/user/<nuova-app>" description="..."`
- **Production** (solo dopo conferma esplicita dell'utente): `webdev_deploy project_dir="/home/user/<nuova-app>" mode="production"`
- **ZIP**: `cd /home/user/<nuova-app> && zip -r /home/user/<nuova-app>.zip . -x "node_modules/*" ".git/*" "dist/*" ".vite/*" "*.log" ".env"` (includi `cornice-dinamica/` se presente)
- **Embed**: la cornice dinamica è in `cornice-dinamica/` (`embed-laboratorio-aumentato-3d-dedicata.html` è il file ⭐ da incollare in Blogger). Dopo il clone aggiorna `APP_URL` (e il `@font-face` `src`) in tutti gli `embed-*.html` con la production della NUOVA app.

## Flusso GitHub

Quando l'utente dice di avere la sorgente su GitHub (o vuole caricarla), chiedigli l'URL del repository. Poi:
1. Usa `--source <url-github>` nello script (clona con `git clone --depth 1`).
2. Se il repo è privato, chiedi all'utente di renderlo accessibile o di passare le credenziali (non chiedere mai password in chat).
3. Dopo il clone, lo script rimuove la cartella `.git` per una copia pulita.

**Pacchetto ZIP / repo self-contained**: il pacchetto esportabile (ZIP) include l'app sorgente + la cartella `skills/` (questa skill con `clone_app.py` e il template config) + un README dettagliato. Quindi il repository GitHub creato dal pacchetto contiene già tutto il necessario: lo script è in `skills/laboratorio-aumentato-3d/scripts/clone_app.py` e può essere eseguito direttamente dal repo (`python3 skills/laboratorio-aumentato-3d/scripts/clone_app.py --source <url-github> …`). Se questa skill è disponibile in locale usa `/home/user/skills/laboratorio-aumentato-3d/scripts/clone_app.py`, altrimenti usa lo script incluso nel repo clonato.

## Attenzione

- Il tema dell'app sorgente è "poesia in realtà aumentata": quando l'utente fornisce il nuovo tema, deriva i testi dei 6 passi e i criteri della rubrica PRIMA di scrivere il config, per non lasciare residui del tema precedente.
- Dopo la clonazione controlla sempre con `grep` che non restino "poesia", "spagnolo" o "realtà aumentata".
- `TeacherClass.tsx` è un file legacy NON instradato (non appare nel routing); non è necessario aggiornarlo, ma se serve pulizia puoi ignorarlo.
