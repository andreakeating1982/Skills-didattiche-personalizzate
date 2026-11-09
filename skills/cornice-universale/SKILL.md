---
name: cornice-universale
description: "Manutenzione completa dell'app Cornice Universale (Vite + React + TS + Tailwind + server Express) che embedda un PDF Google Drive in una cornice protetta da password con stato nascosto/visibile sincronizzato su TUTTI i dispositivi via /api/state, testo ad alta voce (TTS) e ricerca parole. Usare per: modificare UI (password, Nascondi/Mostra, viste Documento/Lettura testo, Cerca, pannello Accessibilità 6 gruppi su 2 colonne centrate, screen reader/ARIA: aria-label/aria-pressed/aria-expanded/aria-controls/role=group/role=status/regione aria-live, focus gestito), cambiare password (in DUE file: Home.tsx e server/index.ts), colori/font (OpenDyslexic ovunque, auto-ospitato in client/public/fonts), messaggio nascosto (MAIUSCOLO esatto, no sottotesto), sincronizzazione (POLL_INTERVAL), TTS e ricerca, deploy preview/produzione, esportare ZIP ricostruibile per GitHub/Render con README.md + ACCESSIBILITA.md. NIENTE cornice dinamica (postMessage labvisivo:height/embed.html): rimossa su richiesta, embed iframe fisso."
---

# Cornice Universale — Skill di Manutenzione

## Overview

App in `/home/user/cornice-universale`. Scaffold `web-static` + server Express aggiunto per sincronizzazione, estrazione testo e sintesi vocale. Stack: Vite + React + TypeScript + TailwindCSS + Express + pdfjs-dist.

Scopo: cornice interattiva con protezione password che embedda un PDF Google Drive, con vista testo leggibile ad alta voce (TTS), ricerca parole e pannello Accessibilità per ipovedenti e dislessici. Lo stato "nascosto/visibile" è **condiviso su tutti i dispositivi** tramite API server (`/api/state`), NON solo in localStorage.

**URL produzione**: `https://cornice-universale.easy-peasy.site`

**Embed su Blogger (iframer fisso — NIENTE cornice dinamica)**:
```html
<iframe src="https://cornice-universale.easy-peasy.site/?doc=1pASV4GUKQqKD_cZtNv7SfiRJg0WsDWUi" width="100%" height="640" style="border:none;max-width:900px;display:block;margin:0 auto;" title="Cornice Documento" loading="lazy"></iframe>
```
L'altezza dell'iframe è fissa (640 px) e la cornice gestisce internamente lo scorrimento. **Decisione utente esplicita**: la cornice dinamica (auto-altezza via `postMessage` `labvisivo:height`, hook `useDynamicFrame`, pagina `client/public/embed.html`) NON serve ed è stata rimossa completamente — non riproporla né riaggiungerla in futuro.

## File Critici

| File | Ruolo |
|------|-------|
| `client/src/pages/Home.tsx` | ⭐ Componente principale (tutta la UI, ricerca, lettura TTS, pannello accessibilità, ARIA) — ~1000 righe |
| `server/index.ts` | 🔧 Server Express — `/api/state`, `/api/document-text` (estrazione PDF), `/api/tts` (sintesi vocale) |
| `client/src/index.css` | Font OpenDyslexic `@font-face`, tema, `--font-sans` |
| `render.yaml` | Render Blueprint (Web Service Node.js, MAI static) |
| `vite.config.ts` | Config Vite (root `client/`, outDir `dist/public`) |
| `README.md` | Docs: ricostruzione IA, deploy Render, embed. Aggiornare quando cambia il comportamento |
| `ACCESSIBILITA.md` | ⭐ Sezione ACCESSIBILITÀ ben segnalata: 21 misure con "dove nel codice" e guida al riuso su altre app. Aggiornare a ogni modifica di accessibilità |

## Password (⚠️ IN DUE FILE)

La password `INSERIRE_PASSWORD_LOCALE` è definita **in entrambi** i file — cambiarne uno solo rompe la sincronizzazione:

1. `client/src/pages/Home.tsx` → `const PASSWORD = "INSERIRE_PASSWORD_LOCALE";`
2. `server/index.ts` → `const PASSWORD = "INSERIRE_PASSWORD_LOCALE";`

Quando si cambia password, modificare SEMPRE entrambi i file.

## Meccanismo di Sincronizzazione Cross-Device

- Il server mantiene `hiddenState` (boolean) **in memoria** (variabile a livello di modulo in `server/index.ts`).
- `GET /api/state` → `{ hidden: boolean }` — lettura stato.
- `POST /api/state` → body `{ password, hidden }` — verifica password, aggiorna stato. Risponde `401` se password errata.
- Il client:
  - Al mount: legge localStorage (`cd_hidden`, `STORAGE_KEY`) per render immediato, poi fetch `GET /api/state` per lo stato reale.
  - **Polling ogni 2500 ms** (`const POLL_INTERVAL = 2500`) su `GET /api/state`.
  - Su hide/show: aggiorna subito locale, poi `POST /api/state`; se fallisce → rollback locale + toast errore.
- **NOTA**: lo stato in-memory si resetta al riavvio del server. Per un uso classe è accettabile.

### ⚠️ IMPORTANTE per il deploy

Questa app **NON è un sito statico**: ha bisogno del server Express per `/api/state`, `/api/document-text`, `/api/tts`. Su Render usare `runtime: node` (Web Service), MAI `runtime: static`.

`render.yaml` corrente:
```yaml
services:
  - type: web
    name: cornice-universale
    runtime: node
    plan: free
    buildCommand: corepack enable && pnpm install --frozen-lockfile && pnpm build
    startCommand: pnpm start
    envVars:
      - key: NODE_VERSION
        value: "22"
    healthCheckPath: /api/state
    autoDeploy: true
```

Build: `pnpm build` = `vite build && esbuild server/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist`
Start: `pnpm start` = `NODE_ENV=production node dist/index.js`

## API Server

| Endpoint | Descrizione |
|---|---|
| `GET /api/state` | Stato nascosto/visibile `{ hidden }` |
| `POST /api/state` | `{ password, hidden }` → aggiorna stato (401 se password errata) |
| `GET /api/document-text?doc=ID` | Estrae il testo del PDF (parole unite, annunci "Page N …", indice pulito) + lingua rilevata `{ text, language, length }` |
| `GET /api/tts?text=...&lang=...` | Audio MP3 (proxy Google Translate TTS), max 200 caratteri |

## Lettura Automatica (TTS) — comportamenti attuali

- Pulsante **LETTURA TESTO** (vista testo): se la lettura non è attiva avvia da capo, altrimenti ferma (`startReadingFrom(0)`); durante la lettura il pulsante diventa "FERMA LETTURA" e ha `aria-pressed`.
- **Lingua automatica**: rilevata dal testo (`it/en/es/fr`) dal server — nessun selettore manuale.
- **Chunking**: il client spezza il testo in frasi (`splitSentences`), le raggruppa in blocchi ≤ 180 caratteri (`buildChunksFrom`, `hardSplit`), li invia a `/api/tts` uno alla volta con pre-caricamento del successivo.
- **Marcatore di pausa `…`**: le frasi che terminano con `…` chiudono il blocco e il client inserisce una **pausa di 850 ms** (`PAUSE_AFTER_MARK`) prima del blocco successivo; prima di inviare a TTS il marcatore viene rimosso (`stripPauseMark`).
- **Evidenziazione frase letta**: la frase corrente è evidenziata con i colori del tema (`theme.hl` / `theme.hlText`); `isCurrent(idx)` usa `currentRange`.
- **Numeri di pagina**: la lettura annuncia "Page N …" / "Pagina N …" / "Página N …" (in base alla lingua) — vedi estrazione.
- **Parole spezzate**: le lettere separate dal PDF (es. "W ILLIAM S HAKESPEARE") vengono riunite — vedi estrazione.

## Estrazione Testo PDF (server) — comportamenti attuali

In `server/index.ts`:

- `extractLinesFromPdf(buffer)`: estrae le righe **dall'alto verso il basso** usando le coordinate y, poi **da sinistra a destra** (x). **Ricostruisce le parole**: due item con gap orizzontale ≤ `WORD_GAP_PT` (1.5 pt) vengono uniti SENZA spazio; oltre quella soglia si mette uno spazio. Così "W ILLIAM S HAKESPEARE" → "WILLIAM SHAKESPEARE".
- **Virgolette delimitatrici**: item composti solo da virgolette/apostrofi (`QUOTE_CHARS`) scartati se NON attaccati a entrambi i lati; apostrofi interni ("teacher's") conservati.
- `pagePhrase(lang)`: "Page"/"Pagina"/"Página" per la lingua rilevata.
- `extractFooterNumber(text)`: estrae il numero da una riga di footer ("1", "pag. 3", "3 / 10").
- `buildReadingText(buffer)`: per ogni pagina, le righe in fondo (top > 90%): numeriche → `${pagePhrase} ${num} …`; testi ricorrenti su 2+ pagine → `${testo} …`; poi `cleanDotLeaders`. Restituisce `{ text, language }`.
- **Niente filtri**: header, footer e indice vengono letti tutti (decisione utente).

## Accessibilità (ipovedenti e dislessici) — stato ATTUALE

### Font: OpenDyslexic OVUNQUE

Decisione utente: **tutta l'app usa OpenDyslexic**, auto-ospitato in `client/public/fonts/OpenDyslexic-Regular.woff2` e `OpenDyslexic-Bold.woff2`.

- `client/src/index.css`: due blocchi `@font-face` (Regular + Bold), `--font-sans: 'OpenDyslexic', 'Comic Sans MS', 'Trebuchet MS', sans-serif` e `body { font-family: 'OpenDyslexic', ... }`.
- `Home.tsx`: `const FONT_STACK = "'OpenDyslexic', 'Comic Sans MS', 'Trebuchet MS', sans-serif";` applicata alla card, alla barra e al testo (`a11yTextStyle`); i controlli ereditano con `style={{ fontFamily: "inherit" }}`.
- **NON ripristinare Cambria o Century Gothic** come font standard: il campo `font` del modello a11y è `"std" | "high"` dove **std = OpenDyslexic** e **high = OpenDyslexic con spaziatura extra** (`letterSpacing: "0.04em"`, `wordSpacing: "0.25em"`).

### Modello e persistenza

```ts
type A11y = { font: "std" | "high"; textSize: number /* 75–200 */; lineHeight: "compact"|"normal"|"wide";
  theme: "white"|"ivory"|"dark"; ruler: boolean; on: boolean };
const A11Y_KEY = "cd_a11y"; // localStorage
const DEFAULT_A11Y = { font:"std", textSize:100, lineHeight:"normal", theme:"white", ruler:false, on:false };
const A11Y_PRESET  = { font:"high", textSize:130, lineHeight:"wide", theme:"ivory", ruler:true, on:true }; // modalità Attiva
const A11Y_THEMES = {
  white:{ bg:"#fdfcfb", text:"#3d2f24", hl:"#f3e0c0", hlText:"#4a3628" },
  ivory:{ bg:"#fdf6e3", text:"#2e2a24", hl:"#ecd9a8", hlText:"#3a2f1e" },
  dark: { bg:"#171717", text:"#f2ead8", hl:"#7a5c3e", hlText:"#ffffff" },
};
```
- Persistenza: `useEffect` salva `A11Y_KEY` a ogni modifica; `useState` inizializzato dal valore salvato (lettura in `try/catch`).
- `a11yTextStyle` applicato al contenitore del testo: `fontFamily: FONT_STACK`, `fontSize: ${textFontSize}px` dove `textFontSize = Math.max(14, Math.round(17 * textSize/100))`, `lineHeight` 2/1.4/1.7 (wide/compact/normal), spaziature per "high", `color: theme.text`, `background: theme.bg`.
- `toggleA11yMode()`: se `on` → `DEFAULT_A11Y`, altrimenti → `A11Y_PRESET`.

### Pannello Accessibilità — 6 gruppi su 2 colonne, sempre centrati

Richiesta utente: **layout a 2 gruppi per riga (3 righe totali), tutto centrato**. NON usare colonna unica.

- Pulsante **ACCESSIBILITÀ** in Riga 2 (aria-expanded + `aria-controls="pannello-accessibilita"`); `toggleA11y()` all'apertura passa alla **vista testo** (così i controlli hanno effetto visibile subito) e sposta il **focus sul primo controllo** del pannello dopo ~80 ms (`a11yFirstRef`). `id="pannello-accessibilita"`.
- Contenitore griglia (i 6 gruppi si dispongono 2 per riga): `grid grid-cols-2 gap-x-2 sm:gap-x-6 gap-y-2.5 sm:gap-y-3 w-full sm:max-w-2xl sm:mx-auto items-start`.
- Ogni gruppo: `<div role="group" aria-label="…" className="flex flex-col items-center gap-1 min-w-0">` con **etichetta (TITOLO) sopra** (span `text-[11px] uppercase text-[#8b7355]`) e **pulsanti sotto** (`flex flex-wrap items-center justify-center gap-1 sm:gap-1.5`).
- Ordine dei 6 gruppi nella griglia (2 per riga, da sinistra a destra): **MODALITÀ | RIGHELLO** (riga 1), **FONT | TESTO** (riga 2), **INTERLINEA | SFONDO** (riga 3) — RIGHELLO è volutamente PRIMA di FONT (richiesta utente). I pulsanti opzione hanno `aria-pressed`; stili `btnA11yActive` = pieno `#967153`, `btnA11yInactive` = `#967153/30` (il marrone del pannello è leggermente più scuro del resto dell'UI `#a98364`):
  1. **Modalità**: "Attiva"/"Disattiva" (`aria-pressed={a11y.on}`, `ref={a11yFirstRef}`).
  2. **Righello**: "Sì"/"No" (`a11y.ruler`).
  3. **Font**: "Standard" / "Alta leggibilità" (`a11y.font === "std"|"high"`).
  4. **Testo**: `A−` (`aria-label="Riduci dimensione testo"`, −15, min 75) / valore `{a11y.textSize}%` / `A+` (`aria-label="Aumenta dimensione testo"`, +15, max 200).
  5. **Interlinea**: "Compatta"/"Normale"/"Ampia".
  6. **Sfondo**: "Bianco"/"Avorio"/"Scuro".
- Stile pulsanti pannello: `btnA11yActive` = `px-2.5 sm:px-3 py-1.5 rounded-lg text-[11px] sm:text-xs font-semibold uppercase tracking-wide transition bg-[#967153] hover:bg-[#826143] text-white`; `btnA11yInactive` = stessa cosa con `bg-[#967153]/30 hover:bg-[#967153]/50`.

### Righello di lettura

- Vista testo: `onMouseMove` su `textContentRef` → `rulerY`; div assoluto `pointer-events-none` con `top: rulerY - textFontSize*0.85`, `height: textFontSize*1.7`, bordo 2px alto/basso; colore: tema dark → `rgba(242,234,216,…)`, altrimenti marrone `rgba(169,131,100,…)`.

## Screen Reader e ARIA — stato ATTUALE (richiesta utente)

Ogni controllo ha **nome accessibile e stato corretto**; i cambiamenti importanti sono annunciati. Da mantenere e da replicare su ogni nuovo controllo:

- **Regione live nascosta** in cima al render: `<span role="status" aria-live="polite" aria-atomic="true" className="sr-only">{liveMsg}</span>`. `liveMsg` aggiornata con `setLiveMsg`:
  - Nascondi/mostra: "Documento nascosto a tutti gli utenti." / "Documento di nuovo visibile a tutti."
  - Lettura: "Lettura del testo avviata." / "Lettura del testo fermata."
  - Pannello accessibilità: "Pannello accessibilità aperto." / "Pannello accessibilità chiuso."
  - Errori TTS/audio: "Errore nella sintesi vocale." / "Errore durante la riproduzione audio." / "Riproduzione audio non riuscita."
- **Input password**: `aria-label="Password per i comandi"`, `placeholder="Inserisci password..."`, `autoComplete="off"`. Invio nel campo = toggle Nascondi/Mostra (`handleKeyDown`).
- **Pulsante Nascondi/Mostra**: `aria-label={hidden ? "Mostra documento" : "Nascondi documento"}` + `title` corrispondente; testo visibile "Mostra"/"Nascondi".
- **Tab viste** (Documento, Lettura testo): `aria-pressed={view === "pdf"}` / `aria-pressed={reading || loadingText}`.
- **Pulsanti che aprono pannelli** (Cerca, Accessibilità): `aria-expanded` + `aria-controls` verso `pannello-ricerca` / `pannello-accessibilita`.
- **Pannello ricerca**: input `aria-label="Cerca nel documento"`; contatore risultati in `<span role="status" aria-live="polite" aria-atomic="true">` ("X / Y", "Nessun risultato", "0 risultati"); pulsanti frecce `aria-label="Risultato precedente"` / `"Risultato successivo"` + `title`, `disabled` se 0 risultati; pulsante "Chiudi".
- **Gruppi di opzioni**: `role="group"` + `aria-label` su ogni gruppo del pannello a11y; ogni opzione con `aria-pressed`.
- **Pulsanti icona senza testo visibile**: sempre `aria-label` (es. A−/A+ e frecce ricerca).
- **Focus gestito**: all'apertura di Cerca il focus va nel campo (`searchInputRef`, ~80 ms); all'apertura di Accessibilità va al primo controllo (`a11yFirstRef`).
- **Nessun badge VISIBILE/NASCOSTO** nella barra (rimosso su richiesta: UI pulita). Lo stato è comunicato dal testo del pulsante, dal toast e dall'annuncio live.

## Ricerca parole — comportamento ATTUALE

- Pulsante **CERCA** (Riga 2) → pannello `pannello-ricerca` con input; all'apertura azzera tutto e passa alla vista testo, focus nell'input.
- `runSearch(raw)`: confronto **senza distinzione maiuscole/minuscole** su tutte le frasi estratte (`sentences`), trova TUTTE le occorrenze (`SearchMatch { sentIdx, start, end }`); se ce ne sono: ferma la lettura, `setView("text")` e scorre alla prima occorrenza dopo ~100 ms (`scrollToSentence`).
- `goSearch(delta)`: naviga i risultati **in modo ciclico** (modulo); contatore `searchIndex+1 / searchMatches.length` mostrato e annunciato.
- Evidenziazione nel testo: `renderSentenceText(s)` spezza la frase in segmenti e usa `<mark>` — occorrenza corrente `bg-[#f4b942]`, altre `bg-[#f3d78e]`, testo `#1f1a12`.
- Invio nel campo → risultato successivo. "Chiudi" azzera tutto. Nessun risultato → stato "Nessun risultato" (bordo rosso tenue).

## Layout Barra Controlli

Barra centrata (header), **nessuna emoji**, tutti i pulsanti **marrone chiaro `#a98364`** (hover `#967153`, testo bianco). Card `max-w-[900px]` centrata, `rounded-xl`, bordo `#d9cec3`, ombra `rgba(92,67,50,0.1)`.

```
Riga 1 (sempre): [ input password ] [ Nascondi / Mostra ]
Riga 2 (solo se !hidden): [ Documento ] [ Lettura testo ] [ Cerca ] [ Accessibilità ]
```

- Riga 1: input password (`w-[140px] sm:w-[170px]`) + pulsante toggle Nascondi/Mostra.
- Riga 2 nascosta quando `hidden === true` (insieme a pannelli e contenuto).
- Tab viste: attivo = pieno `#a98364`; inattivo = `#a98364/30` (hover `/50`).
- **NON esiste più** il badge di stato "Visibile/Nascosto" né i pulsanti zoom −/%/+ in barra (rimossi). La dimensione del testo si regola nel pannello Accessibilità (gruppo Testo).

### Messaggio Documento Nascosto

Quando `hidden === true`, al posto dell'iframe compare:

- Solo il titolo: **`DOCUMENTO MOMENTANEAMENTE NON DISPONIBILE`** — MAIUSCOLO, `text-xl font-bold text-[#5c4332]`.
- **NESSUN sottotesto**, **NESSUN emoji** (sopra c'è solo un div decorativo vuoto con `&nbsp;` per il ritmo verticale). Centrato (`minHeight: 480px`).

### Vista Testo

- `view === "text"`: testo estratto in frasi cliccabili (click = `startReadingFrom(idx)`), evidenziazione frase in lettura con `theme.hl`, `<mark>` per i risultati di ricerca.
- Scroll verticale (`height: 480px`, `maxHeight: 70vh`), sfondo `theme.bg`.

### Iframe Documento

- URL: `https://drive.google.com/file/d/${docId}/preview` (`docId` da `?doc=`), `allow="autoplay"`, `loading="lazy"`, `title="Documento"`.
- Se `docId` manca → card "Nessun documento specificato" con hint `?doc=ID_FILE`.

### Toast (sonner) — nessuno con emoji

- `toast.error("Password errata. Riprova.")` · `toast.info("Già nascosto.")` · `toast.success("Documento nascosto a tutti!")` · `toast.error("Errore di sincronizzazione. Riprova.")` · `toast.info("Già visibile.")` · `toast.success("Documento visibile a tutti!")`
- `toast.error("Testo non ancora disponibile. Attendi un momento.")` · `toast.error("Nessun testo da leggere.")`
- Errori TTS: "Errore nella sintesi vocale.", "Errore durante la riproduzione.", "Riproduzione audio non avviata." (a volte con `err.message`).

## Palette Colori

| Ruolo | Colore |
|---|---|
| Sfondo pagina | `#f5f0eb` |
| Card cornice | `#ffffff` (max-w 900px) |
| Bordo cornice / input | `#d9cec3` |
| Header controlli | `#faf7f3` |
| Testo scuro | `#5c4332` |
| Testo chiaro | `#8b7355` |
| Pulsanti interfaccia | `#a98364` (hover `#967153`, testo bianco; inattivo `#a98364/30` hover `/50`) |
| Pulsanti pannello Accessibilità | `#967153` (hover `#826143`, testo bianco; inattivo `#967153/30` hover `/50`) — leggermente più scuro del resto dell'UI |
| Sfondo avorio (a11y) | `#fdf6e3` |
| Sfondo scuro (a11y) | `#171717` con testo `#f2ead8` |
| Evidenziazione ricerca | corrente `#f4b942`, altre `#f3d78e`, testo `#1f1a12` |
| Evidenziazione frase letta | dal tema: `hl`/`hlText` (white `#f3e0c0`, ivory `#ecd9a8`, dark `#7a5c3e`) |

## Font

**OpenDyslexic è usato ovunque** (`FONT_STACK` in `Home.tsx`, `@font-face` + `--font-sans` + `body` in `index.css`). File auto-ospitati: `client/public/fonts/OpenDyslexic-Regular.woff2`, `OpenDyslexic-Bold.woff2`. Fallback: `'Comic Sans MS', 'Trebuchet MS', sans-serif`. "Alta leggibilità" = OpenDyslexic + `letterSpacing 0.04em` + `wordSpacing 0.25em`. NON reintrodurre Cambria/Century Gothic.

## Personalizzazioni Frequenti

- **Cambiare password**: `const PASSWORD` in **entrambi** `client/src/pages/Home.tsx` e `server/index.ts`.
- **Cambiare intervallo sync**: `Home.tsx` → `const POLL_INTERVAL = 2500;` (ms).
- **Cambiare pausa dopo i marcatori di lettura**: `Home.tsx` → `const PAUSE_AFTER_MARK = 850;` (ms).
- **Cambiare soglia unione lettere (parole spezzate)**: `server/index.ts` → `const WORD_GAP_PT = 1.5;`.
- **Cambiare preset/modalità accessibile**: `A11Y_PRESET` e `DEFAULT_A11Y` in `Home.tsx` (allineare con ACCESSIBILITA.md).
- **Cambiare documento**: NON nel codice — `?doc=ID_FILE` nell'URL embed (iframe su Blogger).
- **Cambiare altezza contenuto**: in `Home.tsx` l'altezza è `480px` in più punti (contenitore contenuto `minHeight`, vista PDF, iframe, vista testo, placeholder — cercare `480px` con grep). L'iframe del BLOG è invece `height="640"` (fisso) e non dipende da Home.tsx.
- **Aggiungere un gruppo al pannello accessibilità**: copiare la struttura `role="group"` (etichetta sopra + pulsanti con `aria-pressed` sotto) dentro la griglia `grid-cols-2`, e aggiungere il campo al tipo `A11y` + `DEFAULT_A11Y`/`A11Y_PRESET` + `a11yTextStyle` se serve.
- **Aggiungere un pulsante alla barra**: stesso marrone `#a98364`, testo MAIUSCOLO, `aria-label`/`aria-pressed`/`aria-expanded`+`aria-controls` a seconda del caso, `style={{ fontFamily: "inherit" }}`, mai emoji.

## Verifica Accessibilità dopo una modifica

Quando si tocca la UI, verificare su preview/produzione (browser):
1. Pannello Accessibilità: **6 gruppi, 2 per riga, centrati**, ordine `Modalità / Righello / Font / Testo / Interlinea / Sfondo` (prima riga: Modalità | Righello; controllo: `#pannello-accessibilita [role="group"]`).
2. Input password e pulsanti hanno nomi accessibili (`aria-label`) e stati (`aria-pressed`, `aria-expanded`).
3. La regione `sr-only` annuncia le azioni (nascondi/mostra, lettura, pannelli).
4. Focus all'apertura di Cerca (input) e Accessibilità (primo controllo).
5. Nessun badge "Visibile/Nascosto", nessuna emoji, nessuna scritta "VISIBILE"/"NASCOSTO".
6. La `ACCESSIBILITA.md` rispecchia le misure correnti (è la "sezione ben segnalata" richiesta per il riuso su altre app).

## Deploy

```bash
cd /home/user/cornice-universale
pnpm check    # verifica TypeScript (tsc --noEmit)
pnpm build    # build frontend (dist/public) + bundle server (dist/index.js)
```

Poi:
- `webdev_deploy` mode=`preview` per test.
- `webdev_deploy` mode=`production` per produzione (URL: `https://cornice-universale.easy-peasy.site`).
- **Prima del deploy produzione**: sempre `webdev_save_checkpoint`.
- Produzione attuale (sett. 2026): commit `5b90b37` — pannello Accessibilità con marrone `#967153` e RIGHELLO prima di FONT (deploy 6572).
- Il codice di produzione corrisponde a `pnpm build` locale: se l'asset JS prodotto ha lo **stesso hash** di quello già in produzione (asset corrente a sett. 2026: `dist/public/assets/index-B5aR3Vl8.js`), il codice è identico e un nuovo deploy non è necessario.

## Esportare ZIP per GitHub/Render

Il pacchetto deve essere **autocontenuto e ricostruibile**: chiunque (o un'IA) deve poter fare `corepack enable && pnpm install --frozen-lockfile && pnpm build && pnpm start` e ottenere la stessa app. Requisiti:

- **NON eliminare `pnpm-lock.yaml`** (install riproducibile con `--frozen-lockfile`).
- **Includere `patches/`** (la patch di wouter è richiesta da `patchedDependencies`).
- Includere le guide IA del pacchetto: **README.md** (panoramica + indice guide), **REBUILD.md** (ricostruzione identica dal repository), **ADATTARE.md** (varianti: documento/lingua/aspetto + catalogo variazioni del pattern ZIP), **RENDER.md** (trasferimento Easy-Peasy → GitHub → Render), **AGENTS.md** (regole per agenti IA) e **ACCESSIBILITA.md** (sezione ACCESSIBILITÀ ben segnalata con "dove nel codice" e guida al riuso).
- Includere **`render.yaml`** (Web Service Node, build `corepack enable && pnpm install --frozen-lockfile && pnpm build`, start `pnpm start`, `NODE_VERSION=22`, health `/api/state`).
- `package.json` deve avere `pnpm.onlyBuiltDependencies: ["esbuild", "@tailwindcss/oxide"]` (pnpm 10 blocca gli script di build altrimenti).
- **NON includere** `node_modules/`, `dist/`, `.git/`, `data/`, file diagnostici (`diag_*.mjs`, `template.json`), `.DS_Store`.
- Nel pacchetto **non deve esserci nulla** di cornice dinamica (niente `embed.html`, niente riferimenti `labvisivo`/`useDynamicFrame` nei doc).

Comandi (già collaudati in questa chat):
```bash
cd /home/user && STAGE=/home/user/package-export && rm -rf "$STAGE" && mkdir -p "$STAGE/cornice-universale"
cd /home/user/cornice-universale
tar cf - --exclude='./node_modules' --exclude='./dist' --exclude='./.git' --exclude='./.DS_Store' \
  --exclude='./diag_items.mjs' --exclude='./diag_pdf.mjs' --exclude='./template.json' --exclude='./data' . \
  | (cd "$STAGE/cornice-universale" && tar xf -)
cd "$STAGE" && rm -f /home/user/cornice-universale.zip \
  && zip -rq /home/user/cornice-universale.zip cornice-universale \
     -x "cornice-universale/node_modules/*" -x "cornice-universale/dist/*" -x "cornice-universale/data/*"
```

**Sempre testare la ricostruzione da zero prima di consegnare**: estrarre lo ZIP in una cartella vuota (`unzip`, poi `corepack enable && pnpm install --frozen-lockfile && pnpm check && pnpm build`). Verifica di successo: il build produce asset con lo **stesso hash** del progetto sorgente (se l'hash JS coincide con quello di produzione, codice identico). Consegnare lo ZIP con `send_attachment` (`/home/user/cornice-universale.zip`).

## Regole d'Oro

1. **Password in DUE file** — `Home.tsx` e `server/index.ts` sempre insieme.
2. **Mai emoji** — nessuna icona in toast, placeholder, pulsanti, docs.
3. **Messaggio nascosto MAIUSCOLO esatto** — "DOCUMENTO MOMENTANEAMENTE NON DISPONIBILE", senza sottotesto.
4. **Tutti i pulsanti dello stesso marrone** — interfaccia `#a98364`; i pulsanti del pannello Accessibilità usano il marrone leggermente più scuro `#967153` (hover `#826143`). Nessun rosso/verde/blu di stato.
5. **NIENTE cornice dinamica** — embed iframe ad altezza fissa (640). `labvisivo:height`, `useDynamicFrame`, `embed.html`: rimossi su richiesta, non riaggiungerli.
6. **Font OpenDyslexic ovunque** — non tornare a Cambria/Century Gothic; file in `client/public/fonts/`.
7. **NIENTE badge stato** Visibile/Nascosto nella barra (rimosso).
8. **Pannello Accessibilità a 2 colonne** (6 gruppi centrati), non colonna unica.
9. **Screen reader su ogni controllo** — nomi accessibili, `aria-pressed`, `aria-expanded`+`aria-controls`, `role="group"`, `role="status"`, regione `aria-live` sr-only, focus gestito all'apertura dei pannelli.
10. **render.yaml = `runtime: node`** — MAI `runtime: static`; build con `--frozen-lockfile` + `corepack enable`.
11. **Polling 2500 ms** — non rimuovere: è ciò che sincronizza i dispositivi.
12. **Documento via `?doc=ID`**, mai hardcoded.
13. **Lettura completa**: header, footer e indice letti TUTTI; numeri di pagina annunciati ("Page N …").
14. **Parole mai spezzate** — non tornare al semplice join con spazio degli item PDF.
15. **Aggiornare README.md e ACCESSIBILITA.md** quando cambia il comportamento (ricostruzione IA + sezione accessibilità ben segnalata).
