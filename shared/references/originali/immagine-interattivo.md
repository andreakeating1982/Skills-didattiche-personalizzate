# Archivio di dettaglio — immagine-interattivo

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/immagini-interattive.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Panoramica tecnica
- File chiave
- I 10 keyword (4 paragrafi)
- Flusso docente-studente
- Layout dashboard docente (3 card)
- Layout pagina studente
- Convenzioni di stile
- Sistema PDF
- Meccanismi di testo interni
- `generateReportPdf(data)` — async
- `generateCompletedMapPdf(data)` — async
- `generateBlankMapPdf(data)` — async
- Audio
- Embed in siti esterni (iframe dinamico)
- Export ZIP
- Deploy
- Modifiche comuni
- Cambiare le parole chiave (solo piccoli ritocchi in-place)
- Risincronizzare i confini dei segmenti audio
- Cambiare i titoli dei segmenti audio
- Aggiungere/togliere paragrafi
- Cambiare l'immagine template della mappa
- Cambiare colori dei paragrafi
- Gestire il re-entry di uno studente
- Modificare l'ordine delle card nella dashboard
- Riferimenti

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# IMMAGINE INTERATTIVA SORGENTE — Mappa Concettuale

App interattiva per l'insegnamento del Romanticismo spagnolo. Gli studenti trascinano 10 parole chiave nei 4 paragrafi della mappa concettuale, guidati dall'audio del docente che avanza un paragrafo alla volta.

> **Questa è la skill di MANUTENZIONE** (modifiche a UI, PDF, audio, stili della sorgente). Per creare una NUOVA app identica con un diverso set di domande/contenuto, usa la skill **`immagine-interattivo-sorgente`** (script `clone_app.py`), NON questa.

## Panoramica tecnica

| Elemento | Valore |
|---|---|
| **Scaffold** | web-db-user (Vite + React 19 + TypeScript 5.9 + Tailwind 4 + shadcn/ui) |
| **Backend** | Express + tRPC 11 + Drizzle ORM + PostgreSQL |
| **PDF** | jsPDF 4 (portrait A4, font Times) |
| **Progetto** | `/home/user/romanticismo-mappa-concettuale` |
| **Preview** | `https://3000-id4xjbjv6s9t8oelcj8mg.sandbox.easy-peasy.ai/` |
| **Produzione** | `https://romanticismo-mappa-concettuale.easy-peasy.site` |
| **Audio** | `/home/user/uploads/EL_ROMANTICISMO_EN_ESPANA.m4a` → `client/public/audio.m4a` |
| **App originale Bécquer** | `https://github.com/andreakeating1982/gustavoadolfobecquer-schemainterattivo` |
| **App Rosalía riferimento** | `https://github.com/andreakeating1982/rosaliadecastro-parolechiave` |

## File chiave

| File | Scopo |
|---|---|
| `server/schema-data.ts` | Definizione dei 4 paragrafi e 10 keyword + `audioStopAt`. Modificare qui per cambiare contenuti. |
| `client/src/lib/audioData.ts` | Segmenti audio (4 segmenti, titoli SENZA numero, timestamp 0-58/58-109/109-175/175-999). |
| `client/src/lib/reportPdf.ts` | 3 PDF async: Report, Mappa Completa, Mappa in Bianco. Funzioni `fitFontSize()` (ricerca binaria) e `textInSlot()` per centrare il testo nei riquadri. `overlayTitles()` per i titoli sovrapposti. |
| `client/src/lib/conceptMapPositions.ts` | Coordinate pixel di slot, rami, hub, `HUB_TITLE`, `PARA_BOXES[].label` con numerazione. Funzione `toPdfCoords()` e `hexToRgb()`. Usato da PDF e ConceptMapDrawing. |
| `client/src/pages/TeacherPage.tsx` | Dashboard docente con 3 card separate. |
| `client/src/pages/StudentMapPage.tsx` | Pagina studente con drag-and-drop, disegno mappa in fondo. |
| `server/routers.ts` | API tRPC per classi, sessioni, risposte, report. |
| `server/db.ts` | Query SQL per report e statistiche. |
| `client/src/components/AudioPlayer.tsx` | Player audio con segmenti e auto-stop. |
| `client/public/audio.m4a` | File audio (copia da `/home/user/uploads/EL_ROMANTICISMO_EN_ESPANA.m4a`). |

## I 10 keyword (4 paragrafi)

Ogni paragrafo ha un colore distintivo usato in titoli, slot e PDF.

| Par. | Titolo | Colore | Keyword |
|---|---|---|---|
| 1 | HUIDA HACIA LO IRRACIONAL | `#8B1A1A` (rosso scuro) | COSTUMBRISMO, INDIVIDUALISMO |
| 2 | POESÍA | `#B8860B` (oro) | JOSÉ DE ESPRONCEDA, GUSTAVO ADOLFO BÉCQUER, ROSALÍA DE CASTRO |
| 3 | PROSA | `#2E5E2E` (verde) | ARTÍCULOS DE COSTUMBRES, MARIANO JOSÉ DE LARRA |
| 4 | TEATRO | `#4A6FA5` (blu) | AMOR IMPOSIBLE, DUQUE DE RIVAS, JOSÉ ZORRILLA |

Tutti i 10 keyword in `ALL_KEYWORDS` in `server/schema-data.ts`.

## Flusso docente-studente

1. **Docente** crea classe (nome, data, password opzionale) → ottiene codice 4 cifre.
2. **Studente** entra con codice + cognome/nome.
3. **Docente** avvia sessione → l'audio player appare nella card SESSIONE.
4. **Docente** preme play sull'audio. L'audio si stoppa automaticamente a fine paragrafo.
5. **Studente** vede il paragrafo corrente, trascina le keyword dagli slot, invia.
6. **Studente** vede "IN ATTESA DI INVIO" per i paragrafi non ancora fatti.
7. **Docente** avanza al paragrafo successivo con le frecce ◀ ▶.
8. Quando tutti e 4 i paragrafi sono inviati, lo studente vede il voto.
9. **Docente** può mostrare/nascondere la soluzione, scaricare PDF.

⚠️ **Re-entry studente**: se uno studente rientra nella stessa classe con lo stesso nome e cognome, `addStudent` in `db.ts` restituisce lo studente esistente. `StudentMapPage.tsx` carica le risposte precedenti via `trpc.answers.list`, ripristina slot, `submittedParagraphs` e `usedKeywords`, e blocca i paragrafi già inviati (non più modificabili).

## Layout dashboard docente (3 card)

Nell'ordine dall'alto:

1. **INFO CLASSE** — nome, data, codice, CHIUDI, ELIMINA CLASSE, NUMERO STUDENTI ATTIVI NELLA SESSIONE, REPORT PDF, MAPPA COMPLETA PDF, MAPPA CONCETTUALE IN BIANCO.
2. **STUDENTI ATTIVI NELLA SESSIONE** — lista studenti con punteggio (IN ATTESA DI INVIO arancione se 0 risposte). Pallini colorati per paragrafo: pieni = inviati, vuoti = IN ATTESA DI INVIO (tooltip al passaggio mouse). Espandi per dettagli, rimuovi studente.
3. **SESSIONE** — AVVIA/TERMINA SESSIONE, MOSTRA/NASCONDI RISPOSTA ESATTA, AudioPlayer coi 4 segmenti, frecce PARAGRAFO X/4, parole chiave del paragrafo corrente centrate.

La sidebar sinistra ha: APRI UNA NUOVA CLASSE, RIAPRI UNA CLASSE, LE TUE CLASSI (non cliccabili — sola visualizzazione).

## Layout pagina studente

- **Header**: senza `bg-card`, eredita `bg-background` della pagina per amalgamarsi allo sfondo.
- Barra superiore: titolo + contatore keyword piazzate.
- Chip di stato: IN CORSO (arancione) per il paragrafo attivo, ✓ verde per quelli inviati, grigio IN ATTESA.
- Barra progresso PARAGRAFO X DI 4.
- Pool keyword: flex-wrap centrato (`justify-center`), drag-and-drop.
- Card paragrafo corrente con slot colorati e pulsante INVIA.
- **Disegno mappa concettuale** in fondo: immagine `mappa-vuota.png` (template radiale 1376×768) con **titolo centrale** «LA LITERATURA DEL ROMANTICISMO EN ESPAÑA» e **4 titoli numerati** sui rami (1. HUIDA HACIA LO IRRACIONAL, 2. POESÍA, 3. PROSA, 4. TEATRO) sovrapposti via CSS. Font adattivo: clamp(6px,0.9vw,10px) centro, clamp(5px,0.7vw,8px) rami. Badge ✓INV / ATTESA su ogni ramo. Verde=corretta, Rosso=errata, Blu=in attesa, Grigio=vuota.
- **Barra progresso footer**: `h-px bg-border/40` (1px, molto sottile, come le altre linee dell'app).
- Footer: REALIZZATO DA ANDREA CENTINARO.

## Convenzioni di stile

- **Font**: Cambria (`font-family: 'Cambria', ...`) ovunque — dichiarato in `index.css`.
- **Input**: sempre `text-center` + classe `center-placeholder`.
- **Testo**: MAIUSCOLO per etichette, titoli sezioni, stati.
- **Colore primario**: plum/viola (ereditato dal tema shadcn).
- **Badge stato**: `bg-amber-100 text-amber-700` per "IN ATTESA DI INVIO", `bg-green-100 text-green-700` per completato.
- **Card**: `bg-card border border-border/60 shadow-sm` per layout pulito.
- **Session controls**: `h-8 px-3 text-xs` per pulsanti compatti.

## Sistema PDF

Tutti i PDF usano jsPDF portrait A4, font Times. **Il template visivo è l'immagine `mappa-vuota.png`** (layout radiale con centro + 4 rami). Le funzioni sono **async**: embeddano l'immagine via `fetch("/mappa-vuota.png")` e sovrappongono il testo negli slot usando `toPdfCoords()`.

### Meccanismi di testo interni

- **`fitFontSize(doc, text, maxWidth, minSize, maxSize)`**: ricerca binaria per trovare la dimensione esatta che fa entrare il testo nell'82% della larghezza del riquadro. Usata per keyword, titoli rami e titolo centrale.
- **`textInSlot(doc, text, sx, sy, boxW, boxH, color)`**: auto-fitting: se il testo sta su una riga (≥4.8pt) lo centra; altrimenti va su 2 righe con `splitTextToSize()`; per testi molto lunghi riduce a 4.2pt.
- **`overlayTitles(doc, map)`**: sovrappone il titolo centrale HUB ("LA LITERATURA DEL ROMANTICISMO EN ESPAÑA") e i 4 titoli dei rami numerati ("1. HUIDA HACIA LO IRRACIONAL", ecc.) con `fitFontSize` e `splitTextToSize` per vincolare il testo entro i bordi dei riquadri.

### `generateReportPdf(data)` — async
**Una pagina per studente**. Intestazione con Nome, Classe, Data, Codice + badge Voto /10. Immagine template con titoli + **solo le risposte di quel singolo studente**: verde (`[0,128,0]`) per corrette, rosso (`[200,30,30]`) per errate. In fondo, riepilogo delle risposte corrette in verde. Dati da `getReportData` (tRPC `classes.report`).

### `generateCompletedMapPdf(data)` — async
Mappa completa: template con titoli + tutte e 10 le keyword corrette sovrapposte in nero con `textInSlot()`. Intestazione con classe/codice/data.

### `generateBlankMapPdf(data)` — async
Mappa vuota: template con titoli + placeholder `………` grigio in ogni slot. In alto: box beige «PAROLE DA INSERIRE» con keyword centrate per riga. **Altezza del box calcolata dinamicamente**: `bankH = firstRowY + (rows.length - 1) * rowGap + tagH/2 + bottomPad`. I tag delle keyword hanno `tagH=7`, `rowGap=9`, `bottomPad=5`. Campi COGNOME/NOME/Classe/Data.

**⚠️ Le tre funzioni PDF sono async** — vanno chiamate con `await` nei callback (TeacherPage lo fa già).

**⚠️ Quando modifichi keyword o paragrafi, aggiorna ANCHE `conceptMapPositions.ts`** (campo `keyword` in ogni `SlotPos`). `reportPdf.ts` deriva già le keyword da `CONCEPT_MAP_SLOTS`, quindi non richiede un aggiornamento separato.

## Audio

File: `client/public/audio.m4a` (copia da `/home/user/uploads/EL_ROMANTICISMO_EN_ESPANA.m4a`).

L'`AudioPlayer` gestisce 4 segmenti con auto-stop. I titoli NON hanno numero davanti (es. "Huida hacia lo irracional", non "1. Huida...").

**Timestamp sincronizzati** (aggiornati per evitare che il numero del paragrafo successivo venga pronunciato nel segmento sbagliato):

| Segmento | Titolo | Inizio | Fine | Note |
|---|---|---|---|---|
| 0 | Huida hacia lo irracional | 0s | 58s | Si ferma PRIMA di "2. Poesía" (58.3s) |
| 1 | Poesía | 58s | 109s | Include "2. Poesía" completo |
| 2 | Prosa | 109s | 175s | Si ferma PRIMA di "4. Teatro" (175.4s) |
| 3 | Teatro | 175s | 999s | Include "4. Teatro" completo |

⚠️ **Regola**: ogni segmento deve finire PRIMA che il narratore pronunci il numero del paragrafo successivo. Il segmento successivo inizia esattamente lì, includendo il titolo completo (numero + nome). `schema-data.ts` ha `audioStopAt` allineato: par.1=58, par.2=109, par.3=175, par.4=999.

Se l'audio non funziona:
1. Verifica che `client/public/audio.m4a` esista.
2. I timestamp devono combaciare tra `schema-data.ts` (`audioStopAt`) e `audioData.ts` (`startTime`/`endTime`).
3. Per risincronizzare, trascrivi l'audio con `file_view` e individua i punti esatti in cui il narratore dice il titolo del paragrafo successivo.

## Embed in siti esterni (iframe dinamico)

L'`App.tsx` ha un `ResizeObserver` che invia `postMessage({ type: "labvisivo:height", height })` al parent. Codice embed:

```html
<div style="background:rgb(250,248,245);border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,0.08);margin:0 auto;max-width:800px;overflow:hidden;">
  <div style="background:linear-gradient(135deg,rgb(232,210,180) 0%,rgb(242,225,200) 100%);padding:16px 20px;text-align:center;">
    <span style="color:#3d2b1f;font-family:Cambria,serif;font-size:15px;font-weight:600;letter-spacing:1px;">MAPA CONCEPTUAL — ROMANTICISMO ESPAÑOL</span>
  </div>
  <iframe id="romanticismoIframe" loading="lazy" src="https://romanticismo-mappa-concettuale.easy-peasy.site/" style="border:none;display:block;height:600px;min-width:100%;transition:height 0.2s ease;width:1px;"></iframe>
</div>
<script>
(function(){var f=document.getElementById('romanticismoIframe');if(!f)return;window.addEventListener('message',function(e){if(e.data&&e.data.type==='labvisivo:height'&&typeof e.data.height==='number'&&e.data.height>100)f.style.height=e.data.height+'px';});})();
</script>
```

⚠️ Per cambiare il colore dell'header: modifica il `linear-gradient` nel div interno. Il gradiente deve restare sui toni del marrone/beige chiaro.

## Export ZIP

Per creare un pacchetto esportabile (come il repo `romanticismo-immagineinterattiva`):

```bash
cd /home/user && zip -r romanticismo-mappa-concettuale-export.zip romanticismo-mappa-concettuale/ \
  -x "*/node_modules/*" -x "*/.git/*" -x "*/dist/*" -x "*/dev-server.log" -x "*/.env" -x "*/.db/*"
```

Il pacchetto contiene 156 file (~5 MB): audio, template PNG, schema Drizzle, README con istruzioni. Basta `pnpm install && pnpm db:push && pnpm dev` per avviarlo.

## Deploy

```bash
# Development
cd /home/user/romanticismo-mappa-concettuale && pnpm dev

# TypeScript check
pnpm check

# Preview (sandbox temporaneo)
webdev_deploy mode=preview

# Produzione (URL permanente *.easy-peasy.site)
webdev_save_checkpoint → webdev_deploy mode=production
```

**Prima del deploy in produzione**: sempre `pnpm check` e checkpoint.

## Modifiche comuni

### Cambiare le parole chiave (solo piccoli ritocchi in-place)

⚠️ Per cambiare INTERAMENTE il set di domande (nuovo argomento/tema), NON farlo qui: usa la skill **`immagine-interattivo-sorgente`** (clone). Qui sotto solo i ritocchi puntuali alla sorgente:

Modifica `server/schema-data.ts`:
- `ALL_KEYWORDS` — l'array completo.
- `PARAGRAPH_ROWS` — `slots` per ogni paragrafo.
- Poi aggiorna `conceptMapPositions.ts`: campo `keyword` in ogni `CONCEPT_MAP_SLOTS`.
- `reportPdf.ts` deriva già le keyword da `CONCEPT_MAP_SLOTS` (niente `ALL_KW` separato).
- Verifica che `TOTAL_SLOTS` sia corretto.
- `pnpm check` prima di deployare.

### Risincronizzare i confini dei segmenti audio

Se l'audio "mangia" il numero del paragrafo successivo:
1. Trascrivi l'audio con `file_view` per trovare i timestamp esatti in cui il narratore dice "2. Poesía", "3. Prosa", "4. Teatro".
2. In `audioData.ts`: sposta `endTime` del segmento N a **prima** del punto in cui il narratore dice il numero successivo; sposta `startTime` del segmento N+1 allo stesso punto.
3. In `schema-data.ts`: allinea `audioStopAt` del paragrafo corrispondente.
4. Regola: ogni segmento deve finire PRIMA che il narratore pronunci il numero del paragrafo successivo. Il segmento successivo include il titolo completo (numero + nome).

### Cambiare i titoli dei segmenti audio

Modifica `client/src/lib/audioData.ts` — array `ROMANTICISMO_SEGMENTS`. I titoli devono essere SENZA numero.

### Aggiungere/togliere paragrafi

1. `server/schema-data.ts`: modifica `PARAGRAPH_ROWS`.
2. `server/routers.ts`: adatta `nextParagraph`/`prevParagraph` ai nuovi limiti.
3. `client/src/lib/audioData.ts`: aggiungi/rimuovi segmenti.
4. `client/src/lib/reportPdf.ts`: aggiorna i `PARAGRAPHS` in entrambe le funzioni PDF.
5. `TeacherPage.tsx`: aggiorna `currentParagraph >= 4` e simili.
6. `StudentMapPage.tsx`: aggiorna riferimenti a `PARAGRAPH_ROWS.length`.

### Cambiare l'immagine template della mappa

Se viene caricata una nuova `Mappa_concettuale_vuota.png`:
1. Copiala in `client/public/mappa-vuota.png`.
2. Rileva le posizioni delle caselle con lo script Python di flood-fill (cerca pixel bianchi R>240,G>240,B>240, filtra per area 50-600×30-200).
3. Aggiorna `conceptMapPositions.ts`: `IMG_W`, `IMG_H`, `CONCEPT_MAP_SLOTS`, `PARA_BOXES`, `HUB`.
4. Verifica che slotId combacino con `PARAGRAPH_ROWS` in `schema-data.ts`.

### Cambiare colori dei paragrafi

1. `server/schema-data.ts`: campo `color` in ogni `PARAGRAPH_ROWS`.
2. `conceptMapPositions.ts`: campo `color` nei `PARA_BOXES`.
3. `StudentMapPage.tsx`: i badge `✓INV`/`ATTESA` e card paragrafo usano `row.color`.

### Gestire il re-entry di uno studente

Quando uno studente rientra nella classe:
1. `addStudent` in `db.ts` restituisce già lo studente esistente (match per `classId` + `name`).
2. `StudentMapPage.tsx` chiama `trpc.answers.list` con `studentId` dopo il join.
3. L'`useEffect` su `existingAnswers` ripristina slot, `submittedParagraphs`, `usedKeywords`, e `score`.
4. I paragrafi già inviati sono bloccati (`pointer-events-none`, pulsante INVIA nascosto).
5. `handleSubmitParagraph` rifiuta il reinvio con toast "Paragrafo già inviato".

### Modificare l'ordine delle card nella dashboard

Le 3 card sono in `TeacherPage.tsx` dentro il `<main>` con classe `space-y-6`. L'ordine è: INFO CLASSE → STUDENTI ATTIVI → SESSIONE.

## Riferimenti

Per dettagli sul database e le API, consulta `server/db.ts` e `server/routers.ts`.
Per i tipi condivisi, vedi `shared/types.ts` e `server/schema-data.ts`.
Per le posizioni degli slot nell'immagine template, vedi `client/src/lib/conceptMapPositions.ts`.
