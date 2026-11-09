---
name: romanticismo-interattivo
description: "Manutenzione completa dell'app Romanticismo Interattivo (Vite + React + TypeScript + Tailwind + tRPC + Drizzle). Usare per modificare UI, deploy, hotspot, PDF report, stili. Esplorazione interattiva del Romanticismo spagnolo con hotspot e audio."
---

# Romanticismo Interattivo

App interattiva per l'esplorazione del Romanticismo spagnolo tramite hotspot su un'immagine, sincronizzata con segmenti audio. Scaffold: `web-db-user`.

## Riferimenti

| Risorsa | Valore |
|---------|--------|
| Progetto | `/home/user/romanticismo-interattivo` |
| Preview | `https://3000-i33ayvau357uvrfkpnch7.sandbox.easy-peasy.ai/` |
| Produzione | `https://romanticismo-interattivo.easy-peasy.site` |
| Immagine | `client/public/romanticismo-sintesi.png` (2752×1536) |
| Audio | `client/public/audio/explicacion.m4a` |
| Embed | `client/public/embed.html` |

## File chiave

| File | Ruolo |
|------|-------|
| `shared/exploraData.ts` | Hotspot, segmenti audio, temi sezioni, testo explicativo |
| `client/src/pages/Home.tsx` | Schermata studente: login "TROVA LA TUA CLASSE" |
| `client/src/pages/StudentExplora.tsx` | Schermata esplorazione: immagine, hotspot, audio, invio risposte |
| `client/src/pages/TeacherPage.tsx` | Dashboard docente: creazione classi, gestione sessione, report, audio |
| `client/src/lib/reportPdf.ts` | Generazione PDF report studente |
| `client/src/lib/hotspotImage.ts` | Generazione immagine con cerchi hotspot vuoti (Canvas) |
| `client/src/hooks/useIframeResize.ts` | Auto-resize iframe via postMessage |
| `server/db.ts` | Query database (classi, studenti, submissions, re-entry) |
| `server/routers.ts` | API tRPC per classi, submissions, report |

## Struttura dati

### Hotspot

Definiti in `HOTSPOTS[]` in `shared/exploraData.ts`. Ogni hotspot:
- `id`: stringa univoca (es. `"libro-central"`)
- `section`: `centro` | `huida` | `poesia` | `prosa` | `teatro`
- `x`, `y`: percentuali (0-100) sull'immagine
- `size`: `sm` | `md` | `lg` (raggio cerchio)
- `label`: etichetta con numero (es. `"1. El Romanticismo"`)
- `info`: testo informativo mostrato al tocco

### Segmenti audio

Definiti in `AUDIO_SEGMENTS[]`. Ogni segmento:
- `id`: 0-4
- `startTime`, `endTime`: secondi nell'audio
- `hotspotIds`: array di id hotspot attivi in quel segmento
- `prompt`: testo mostrato allo studente

### Temi sezioni

`SECTION_THEMES` mappa sezione → colori Tailwind per ring, dot, glow, badge.

## Convenzioni di design

### Footer

TUTTI i footer usano lo stesso markup ovunque (Home, Teacher, StudentExplora — TRANNE la schermata login studente dove è stato rimosso):
```tsx
<footer className="shrink-0 border-t border-border/60 py-4 text-center text-xs text-muted-foreground uppercase tracking-wide">REALIZZATO DA ANDREA CENTINARO</footer>
```
NON usare `<span>` interno. NON inserire il footer nella schermata in cui lo studente inserisce nome e cognome (StudentExplora, prima schermata).

### Pulsanti AREA DOCENTE / AREA STUDENTI

```tsx
className="inline-flex items-center gap-2 px-5 py-2 rounded-full border border-border bg-card text-foreground hover:text-primary hover:border-primary transition-colors text-sm font-medium tracking-[0.06em]"
```

### Pulsante TESTO (StudentExplora)

Il pulsante "TESTO" che mostra il testo completo NON deve avere testo in uppercase. L'header della modale deve essere dello stesso colore dello sfondo (blendato).

### Pulsante HOME (schermata studente)

Nella pagina StudentExplora (dove lo studente inserisce nome e cognome):
```tsx
<a href="/"
  className="mt-4 mb-14 inline-flex items-center gap-4 px-5 py-2 rounded-full border border-border bg-card text-foreground hover:text-primary hover:border-primary transition-colors text-sm tracking-[0.12em]">
  <Home className="size-4" />
  HOME
</a>
```
Usare `text-sm` (14px), NON `text-[12px]`.

### Layout Home (studente)

Struttura identica a Shakespeare Quiz e Bécquer Schema:
```tsx
<div className="flex flex-col min-h-screen bg-background paper-grain">
  <div className="flex flex-col items-center pt-12 pb-4 gap-3">
    <h1 className="text-2xl sm:text-3xl font-bold">IMMAGINE INTERATTIVA</h1>
    <a ...>AREA DOCENTE</a>
  </div>
  <main className="flex-1 flex items-start justify-center px-4 w-full pt-4 sm:pt-6">
    {/* Card TROVA LA TUA CLASSE */}
  </main>
  <footer ...>REALIZZATO DA ANDREA CENTINARO</footer>
</div>
```
NON usare `justify-between` sul contenitore esterno.

### Layout Teacher dashboard

L'intera pagina docente è racchiusa in un unico card:
```tsx
<div className="min-h-screen bg-background paper-grain flex items-start justify-center p-3 sm:p-4 overflow-x-hidden">
  <div className="w-full max-w-6xl min-h-[92vh] bg-card rounded-2xl border border-border/60 shadow-xl flex flex-col overflow-hidden">
    {/* ── HEADER ── */}
    <div className="flex items-center justify-between px-6 py-4 border-b border-border/60 shrink-0">
      <h1>IMMAGINE INTERATTIVA</h1>
      <a href="/">AREA STUDENTI</a>
    </div>
    {/* ── BODY: sidebar + main ── */}
    <div className="flex-1 flex flex-col sm:flex-row overflow-y-auto sm:overflow-hidden">
      <aside className="sm:w-[38%] sm:min-w-[320px] w-full sm:border-r sm:border-b-0 border-b border-border/60 bg-card sm:overflow-y-auto shrink-0">
        ...
      </aside>
      <main className="flex-1 sm:overflow-y-auto">
        <div className="w-full p-4 sm:p-5 space-y-6">
          {/* Card info classe — full-width */}
          {/* Card STUDENTI ATTIVI — full-width, mt-6 */}
          {/* Card SESSIONE */}
        </div>
      </main>
    </div>
    {/* ── FOOTER ── */}
    <footer className="shrink-0 border-t border-border/60 py-4 text-center text-xs text-muted-foreground uppercase tracking-wide">REALIZZATO DA ANDREA CENTINARO</footer>
  </div>
</div>
```

Regole CRITICHE:
- Usare `sm:flex-row` (640px), NON `md:flex-row` né `lg:flex-row`
- Card: `max-w-6xl min-h-[92vh]`, MAI usare `style={{ minHeight: "calc(100vh - 2rem)" }}` (forza altezza eccessiva)
- Bordi: sempre `border-border/60`, NON `border-border`
- Sidebar: `sm:w-[38%] sm:min-w-[320px]`
- **Input centrati**: tutti gli `<Input>` nella sidebar (Nome classe, Data, Password, Codice, Password riapertura) devono avere `text-center` per centrare placeholder e testo digitato. Per il campo **Data** (`type="date"`) servono anche le regole CSS in `client/src/index.css` (`input[type="date"]::-webkit-date-and-time-value`, `::-webkit-datetime-edit`, `::-webkit-datetime-edit-fields-wrapper`, `::-webkit-calendar-picker-indicator`) — senza, la data nativa resta allineata a sinistra.
- Main padding: `w-full p-4 sm:p-5` (non `p-6`)
- **Layout main**: `space-y-6` tra le card. Le card sono full-width, NON in griglia 2-colonne.
- Footer: usa `<footer>` (non `<div>`), senza `<span>` interno, con `shrink-0 py-4 text-xs uppercase tracking-wide`

### Colori (sezione CLASSI e icone)

NON usare `emerald` da nessuna parte. Usare sempre `green`:
- Pallino classe attiva: `bg-green-500 shadow-[0_0_6px_rgba(34,197,94,.4)]`
- Score nel report: `text-green-600`
- Badge sessione attiva: `text-green-700 bg-green-100`
- Badge sessione in attesa: `text-amber-700 bg-amber-100`

**Icone sidebar docente** (Plus, KeyRound, BookOpen): usare `text-primary` (marrone/plum dell'app, MAI `text-[#4A3B32]`).
**Icona cestino eliminazione classe** (Trash2): `text-red-400 hover:text-red-600`.

### Pulsante ELIMINA CLASSE

Il pulsante ELIMINA CLASSE si trova nella dashboard docente (NON nella sidebar LE TUE CLASSI). Appare accanto al pulsante CHIUDI quando una classe è selezionata. Al click:
1. Mostra un `confirm()` per chiedere conferma
2. Imposta `activeClassId` a `null` (chiude immediatamente la dashboard)
3. Chiama `deleteClassMutation.mutate({ id })` per eliminare la classe dal database

```tsx
<Button onClick={() => {
  if (confirm(`Eliminare definitivamente la classe "${activeClassInfo.name}"?`)) {
    const id = activeClassId!;
    setActiveClassId(null);
    setActiveClassInfo(null);
    setExpandedStudent(null);
    deleteClassMutation.mutate({ id });
  }
}} variant="outline"
  className="border-red-400 text-red-700 hover:bg-red-50 hover:border-red-500 rounded-full h-9 px-3 text-xs font-bold">
  {deleteClassMutation.isPending ? <Loader2 className="size-3.5 animate-spin" /> : <Trash2 className="size-3.5" />} ELIMINA CLASSE
</Button>
```

NON inserire il pulsante Trash2 nella lista LE TUE CLASSI della sidebar.

### Lista studenti (stile Gustavo Adolfo Bécquer Schema)

Riferimento: `https://github.com/andreakeating1982/gustavoadolfobecquer-schemainterattivo`

Nella sezione STUDENTI ATTIVI NELLA SESSIONE:
- Indicatore: **pallino grigio** `size-2.5 rounded-full shrink-0 bg-gray-300`. Tutti gli studenti hanno lo stesso pallino grigio, indipendentemente dallo stato.
- **Nessuna etichetta testuale** (niente "COMPLETATO", "IN CORSO", "IN ATTESA")
- **Tooltip nero (hover + touch)**: il nome usa un tooltip CSS custom (NON Radix) che mostra nome e cognome completi. Funziona su PC (hover) E su cellulare (tap). Stato `tooltipStudent` (useState<string|null>) + `useEffect` che aggiunge un listener `document.addEventListener("click", close)` per chiudere al click fuori. Struttura: `<span className="group relative block min-w-0 cursor-pointer" onClick={...}>` con `onClick` che usa `window.matchMedia('(hover: none)').matches` per il toggle su touch; il tooltip è un `<span>` figlio `absolute left-1/2 top-full z-[100] mt-2 -translate-x-1/2 max-w-[85vw] rounded-md bg-black px-3 py-1.5 text-xs font-bold uppercase text-white shadow-lg` con visibilità `opacity-0 group-hover:opacity-100 group-active:opacity-100 group-focus:opacity-100` (+ `opacity-100` quando `tooltipStudent === student.id`).
- Nome: `font-semibold text-sm text-foreground truncate uppercase` (centrato e MAIUSCOLO)
- Punteggio/segnaposto: se lo studente ha inviato risposte → `${score}/10` con `text-sm font-bold` e colore dinamico; altrimenti → `<span className="text-[10px] uppercase tracking-wider font-semibold">IN ATTESA DI INVIO</span>` in `text-amber-600`. Il contenitore del punteggio DEVE avere `whitespace-nowrap` (evita l'overflow orizzontale di "IN ATTESA DI INVIO").
- **Pallini segmento**: 5 cerchi colorati (`size-2.5 rounded-full`) per i 5 segmenti audio (ambra #d4a853, blu #3b82f6, verde #10b981, viola #8b5cf6, rosa #f43f5e). Pieni se inviati, bordati (solo outline) se in attesa. Ogni pallino ha un tooltip con lo stato del segmento.
- Pulsante rimuovi: `<Button variant="ghost" size="sm">` con `<XCircle className="size-4" />`, classi `text-red-500 hover:text-red-700 hover:bg-red-100 px-1.5 h-7 rounded-full`
- **Nessun chevron**: NON ci sono freccette expand/collapse. Il menu a tendina è stato rimosso.
- Row wrapper: `rounded-xl border border-border/50 bg-muted/10` (SENZA `overflow-hidden`, altrimenti il tooltip viene tagliato), inner div: `w-full flex items-center gap-3 px-4 py-2.5 hover:bg-muted/30 transition-colors text-center cursor-default rounded-xl`
- Tra il sottotitolo e la lista studenti: linea separatrice `<div className="border-t border-border/40 my-6" />`
- Sotto la lista studenti: contatore `<span className="...">{studentList.length} attivi</span>` con icona Users
- **STUDENTI ATTIVI card**: full-width sotto la card info classe, `mt-6`, NON in griglia 2-colonne

### Card interne (dashboard)

Card info classe: `bg-primary/5 border-2 border-primary/30 shadow-md`, CardContent `p-5 sm:p-6 space-y-4 sm:space-y-5`.
- **Riga codice + pulsanti** (CHIUDI / ELIMINA CLASSE): `<div className="flex flex-wrap items-center justify-center gap-2">` — il `flex-wrap` evita la sovrapposizione quando lo spazio è stretto. Il box codice: `flex items-center gap-1.5 rounded-lg bg-card border border-border/50 px-3 py-1.5 shrink-0`.
Card studenti: `bg-card border border-border/60 shadow-sm mt-6`, CardContent `p-6 sm:p-8`. **Full-width** sotto la card info classe (NON in griglia 2-colonne).
Card sessione: `bg-card border border-border/60 shadow-sm`, CardContent `p-6 sm:p-8`.
Row studente: `rounded-xl border border-border/50 bg-muted/10` (SENZA `overflow-hidden`), inner div (NON `<button>` — il menu a tendina è stato rimosso): `w-full flex items-center gap-3 px-4 py-2.5 hover:bg-muted/30 transition-colors text-center cursor-default rounded-xl`.
**IMPORTANTE**: NON implementare expand/collapse, NON usare AnswerDetails, NON mostrare menu a tendina con risposte. Le righe studente sono statiche.

**Linea separatrice**: tra il sottotitolo "TUTTI GLI STUDENTI ISCRITTI..." e la lista studenti, inserire `<div className="border-t border-border/40 my-6" />` per dare spazio sopra e sotto.

### Empty state docente

```tsx
<div className="flex flex-col items-center justify-center py-24 text-center">
  <div className="size-20 rounded-2xl bg-muted/50 flex items-center justify-center mb-2">
    <BookOpen className="size-10 text-muted-foreground/30" />
  </div>
  <h2 className="text-2xl font-bold text-foreground mb-2">NESSUNA CLASSE SELEZIONATA</h2>
  <p className="text-sm text-muted-foreground max-w-sm text-center leading-relaxed">
    CREA UNA NUOVA CLASSE DALLA BARRA LATERALE OPPURE RIAPRINE UNA GIÀ ESISTENTE
  </p>
</div>
```

### JSX ternary syntax (CRITICO)

NON usare ternary inline con `}</>` su una sola riga — causa TS1381:
```tsx
// ❌ ERRATO — causa TS1381 "Unexpected token. Did you mean {'}'}?"
{condition ? <Loader2 /> : <><Icon /> TESTO}</>}

// ✅ CORRETTO
{condition ? (
  <Loader2 />
) : (
  <>
    <Icon />
    TESTO
  </>
)}
```

### Pulsanti docente

- **TERMINA SESSIONE**: `h-8 px-3 text-xs font-semibold bg-red-600 hover:bg-red-700 text-white rounded-xl shadow-sm`
- **RIAVVIA CLASSE**: `h-9 px-5 text-sm font-semibold bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl`
- **AVVIA SESSIONE**: `h-8 px-3 text-xs font-semibold bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl`
- Icone nei pulsanti: `size-4 mr-1.5` per RIAVVIA, `size-3.5 mr-1` per AVVIA e TERMINA

### Contatore studenti (card sessione)

Dopo i controlli sessione, aggiungere:
```tsx
{studentList.length > 0 && (
  <div className="flex flex-wrap items-center justify-center gap-4 text-xs pt-6 mt-6 border-t border-border/40">
    <span className="inline-flex items-center gap-1.5 font-normal lowercase text-muted-foreground">
      <Users className="size-3.5 text-plum" /> {studentList.length} attivi
    </span>
  </div>
)}
```
Nota: `pt-6 mt-6` per ampio spazio sopra la linea, `font-normal lowercase text-muted-foreground` per "attivi" minuscolo.

### Pulsante IMMAGINE CON HOTSPOT

Nella TeacherPage, vicino a REPORT PDF (solo quando classe selezionata):
```tsx
<Button onClick={() => downloadHotspotImage().catch(() => toast.error("..."))}
  variant="outline"
  className="border-amber-400 text-amber-700 hover:bg-amber-50 hover:border-amber-500 rounded-full h-9 px-3 text-xs">
  <ImageIcon className="size-3.5" /> IMMAGINE CON HOTSPOT
</Button>
```

### Embed

L'iframe wrapper è in `client/public/embed.html`. Header beige: `linear-gradient(135deg, #E6CDAB 0%, #F0DBC3 100%)`, testo `#4A3728`. L'app invia `postMessage` con `{type: "labvisivo:height", height: N}` per l'auto-resize.

## Comportamenti speciali

### Rientro studente

Quando uno studente rientra in una classe con stesso nome, il sistema riusa il record esistente preservando i punteggi. Implementato in `server/db.ts` (`addStudent`).

### Audio docente

In TeacherPage, l'audio si ferma automaticamente al `endTime` del segmento corrente tramite `timeupdate` event listener. Il pulsante Play riparte dal `startTime`. Quando il docente clicca TERMINA SESSIONE, l'audio in riproduzione si ferma automaticamente.

**Trascrizione testuale rimossa**: la riga `<p>{seg.subtitle}</p>` è stata eliminata dalla sezione sessione. Mostrare solo `seg.label`, `seg.prompt`, la barra di progresso, e il badge "X HOTSPOT DA SELEZIONARE".

**Badge segmento**: il testo "X HOTSPOT DA SELEZIONARE" usa `text-[10pt] font-semibold text-primary` dentro un contenitore `rounded-full bg-primary/10 border border-primary/20`.

### Hotspot image download

`downloadHotspotImage()` in `client/src/lib/hotspotImage.ts` disegna cerchi VUOTI (senza numeri) sull'immagine 2752×1536 usando Canvas. Colori per sezione: ambra (centro), blu (huida), smeraldo (poesia), viola (prosa), rosa (teatro).

### Hotspot click (handleTap)

In `StudentExplora.tsx`, la logica `handleTap`:
- Se `selected.size < seg.hotspotIds.length` → lo studente può aggiungere e togliere hotspot liberamente
- Se `selected.size === seg.hotspotIds.length` → NON può aggiungere altri hotspot, ma può DESELEZIONARNE uno e riselezionarne un altro per cambiare risposta prima dell'invio
- Dopo l'invio (`segmentVerified === true`) → tutti gli hotspot sono bloccati fino al segmento successivo
- Il reset di `segmentVerified` avviene a ogni `startSelectionPhase`, permettendo di cliccare hotspot in ogni segmento anche se si è sbagliato nei segmenti precedenti

### Sezione "In attesa di risposta"

RIMOSSA. Non mostrare più questa sezione nella TeacherPage.

### Menu a tendina risposte (AnswerDetails)

RIMOSSO completamente. Le righe studente NON sono espandibili. Niente freccette ChevronUp/ChevronDown. La funzione `AnswerDetails` è stata eliminata dal file. Ogni studente ha il proprio stato visibile direttamente nella riga (punteggio o "IN ATTESA DI INVIO").

### PDF Report

Generato da `client/src/lib/reportPdf.ts` con **jsPDF + jspdf-autotable** (download immediato via `doc.save()`, NON finestra di stampa).
- **Font**: Cambria (regular + bold), incorporato a runtime da `client/public/fonts/cambria-regular.ttf` e `cambria-bold.ttf` con cache in memoria.
- **Layout**: A4 verticale, `unit: "mm"`, margini normali (top 2.5cm = 25, laterali/inferiore 2cm = 20). **Ogni studente occupa UNA pagina** (`if (si > 0) doc.addPage()` all'inizio del `forEach`) — report + griglia PUNTEGGIO sempre sulla stessa pagina.
- Per ogni studente: intestazione (titolo + "REPORT DI VERIFICA"), nome, classe · data, punteggio colorato, legenda (verde=corretta, rosso=errata), tabella **Segmento | Punteggio | Corrette | Errate** (colonna Corrette verde, colonna Errate rossa).
- La tabella elenca SEMPRE tutte le 5 domande (itera `AUDIO_SEGMENTS`). Le domande a cui lo studente NON ha risposto appaiono con punteggio `0/X` in grigio `[156,163,175]` e `—` nelle colonne Corrette/Errate (SENZA verde/rosso). Niente scritta "Nessuna risposta inviata".
- **Griglia PUNTEGGIO** (`drawScoreBox`, ~112mm, bordo marrone 146,64,14) in fondo a ogni pagina con: `Punteggio ottenuto: X/10`, `Punti per domanda: D1=1 · D2=2 · D3=3 · D4=2 · D5=2` (da `AUDIO_SEGMENTS[].hotspotIds.length`), `Punteggio massimo = 10/10`.
- I caratteri `✓`/`✗` NON funzionano in jsPDF standard font → usare colonne colorate (verde/rosso), non simboli.
- **NON esiste un "PDF in bianco"** — solo REPORT PDF.

## Deploy

```bash
# Preview (dev server)
webdev_deploy mode="preview"

# Produzione
webdev_save_checkpoint  # OBBLIGATORIO prima
webdev_deploy mode="production"
```

## Modifica contenuti

Per cambiare hotspot, segmenti audio o testo explicativo: modificare `shared/exploraData.ts`. I dati sono condivisi tra server e client. Dopo la modifica: `webdev_deploy mode="preview"` per testare.

### Coordinate attuali hotspot

| Hotspot | x | y |
|---------|---|---|
| libro-central (El Romanticismo) | 48 | 22 |
| poeta-espejo (Individualismo) | 20 | 16 |
| costumbrismo | 37 | 27 |
| castillo-ermita (Huida) | 35 | 27 |
| cementerio | 86 | 42 |
| poesia-lirica | 55 | 58 |
| prosa-articulos | 28 | 75 |
| prosa-leyendas | 72 | 73 |
| teatro-donjuan | 38 | 88 |
| teatro-donalvaro | 62 | 90 |

Per cambiare l'immagine di sfondo: sostituire `client/public/romanticismo-sintesi.png` e aggiornare le coordinate `x`/`y` in `HOTSPOTS[]` (valori in percentuale 0-100).

Per cambiare l'audio: sostituire `client/public/audio/explicacion.m4a` e aggiornare `startTime`/`endTime` in `AUDIO_SEGMENTS[]`.

I sottotitoli dei segmenti audio in `AUDIO_SEGMENTS[].subtitle` devono corrispondere esattamente al testo del DOCX (`/home/user/uploads/Spagnolo_-_Letteratura_-_Romanticismo_-_Spiegazione_dell_immagine.docx`).
