# Archivio di dettaglio — immagine-interattivo-sorgente

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/immagini-interattive.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Cosa compone il "contenuto" (set di domande)
- Workflow di clonazione
- 1. Estrai il contenuto corrente (punto di partenza)
- 2. Costruisci il nuovo contenuto
- 3. Clona
- 4. Configura e avvia
- 5. Deploy
- 6. Export ZIP (per GitHub/Render)
- Verifica automatica (obbligatoria dopo ogni clone)
- Regole da rispettare SEMPRE
- Riferimenti

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# IMMAGINE INTERATTIVA SORGENTE — Clonazione

Questa skill clona l'app **IMMAGINE INTERATTIVA SORGENTE** (cartella `/home/user/romanticismo-mappa-concettuale`, scaffold `web-db-user`: Vite + React 19 + TypeScript + Tailwind + tRPC + Drizzle) in una nuova app **identica**, cambiando **solo il contenuto** (il "set di domande": i paragrafi, le parole chiave, i segmenti audio, l'immagine di sfondo e i titoli).

Tutto il resto resta esattamente uguale: dashboard docente, codice classe a 4 cifre, sessioni, contatore studenti attivi, PDF (Report / Mappa Completa / Mappa in Bianco), palette plum/gold, embed iframe `labvisivo:height`.

## Cosa compone il "contenuto" (set di domande)

L'app è una **mappa concettuale interattiva**: una immagine di sfondo con 4 rami (paragrafi), 10 slot in cui lo studente trascina le parole chiave, guidato dall'audio del docente. Il contenuto è definito in questi punti:

| File | Cosa contiene (contenuto) |
|---|---|
| `server/schema-data.ts` | `ALL_KEYWORDS`, `PARAGRAPH_ROWS` (id, label, subtitle, color, slots, audioStopAt), `TOTAL_SLOTS` |
| `client/src/lib/audioData.ts` | `SEGMENTS` (titoli + timestamp), `AUDIO_TRACKS` (id, titolo, src) |
| `client/src/lib/conceptMapPositions.ts` | `HUB_TITLE`, `CONCEPT_MAP_SLOTS[].keyword`, `PARA_BOXES[].label/color` |
| `client/src/lib/reportPdf.ts` | Titoli PDF e prefissi dei nomi file (`Report_Mappa_…`, ecc.) |
| `client/index.html` | `<title>` |
| `client/src/pages/Home.tsx` | titolo `<h1>` |
| `client/public/mappa-vuota.png` | immagine di sfondo |
| `client/public/audio.m4a` | traccia audio |

Lo script di clonazione (`/home/user/skills/didattica-app-classe/scripts/immagine-interattivo-sorgente/clone_app.py`) rigenera i 3 file di dati e applica sostituzioni mirate agli altri. **NON modificare a mano questi file nella nuova app** — lavora sempre sul JSON contenuto.

## Workflow di clonazione

### 1. Estrai il contenuto corrente (punto di partenza)

```bash
python3 /home/user/skills/didattica-app-classe/scripts/immagine-interattivo-sorgente/clone_app.py \
  --dump -o contenuto.json
```

Produce un `contenuto.json` con TUTTO il contenuto corrente (paragrafi, keyword, coordinate slot, hub, ecc.). Le coordinate `map.slots`, `map.paraBoxes`, `map.hub`, `map.imgW/imgH` vanno **lasciate invariate** (rappresentano la geometria dell'immagine di sfondo).

### 2. Costruisci il nuovo contenuto

Parti dal JSON estratto (o scrivilo da zero se hai testo libero). Modifica **solo i campi di testo**:

- `app.name`, `app.title`, `app.hubTitle`, `app.pdfTitle`, `app.pdfBlankTitle`, `app.pdfSlug`
- `audio.trackId`, `audio.trackTitle`
- `paragraphs[].label` (con numero, es. "2. POESÍA"), `paragraphs[].subtitle`, `paragraphs[].color`, `paragraphs[].slots` (keyword in ordine), `paragraphs[].audioStopAt`
- `segments[].title` (SENZA numero), `segments[].text`, `segments[].startTime/endTime`
- `map.paraBoxes[].label` (con `\n` per il capo riga)

Lo schema completo è in `/home/user/skills/didattica-app-classe/references/immagine-interattivo-sorgente/contenuto-json.md`.

**Vincoli di struttura** (l'app resta identica):
- Stesso numero di paragrafi (4) e stesso numero di slot per paragrafo (2-3-2-3 = 10 slot). Lo script valida che `paragraphs[].slots` e `map.slots` siano allineati.
- Stesso numero di segmenti audio dei paragrafi (`segments.length == paragraphs.length`).
- `segments[i].endTime` deve combaciare con `paragraphs[i].audioStopAt` (il segmento N finisce PRIMA che il narratore pronunci il numero del paragrafo successivo).

### 3. Clona

```bash
python3 /home/user/skills/didattica-app-classe/scripts/immagine-interattivo-sorgente/clone_app.py \
  --json contenuto.json --name nome-nuova-app
```

Flag utili:
- `--source <path|git-url>` — sorgente diversa dalla cartella locale (es. `https://github.com/user/repo.git`). Default: `/home/user/romanticismo-mappa-concettuale`.
- `--name <slug>` — nome della nuova cartella (default: `app.name` del JSON).
- Nuovo audio: metti il path assoluto del file in `audio.file` (es. `/home/user/uploads/nuovo.m4a`) → viene copiato in `client/public/audio.m4a`.
- Nuova immagine di sfondo: path in `image.file` (es. `/home/user/uploads/nuova-mappa.png`) → copiata in `client/public/mappa-vuota.png`. Se cambi l'immagine, ricalcola le coordinate con lo script flood-fill (vedi skill `immagine-interattivo`).

La nuova app viene creata in `/home/user/<name>`.

### 4. Configura e avvia

```bash
cd /home/user/<name>
cp .env.example .env   # imposta DATABASE_URL
pnpm install
pnpm db:push
pnpm check            # validazione TypeScript (deve dare 0 errori)
pnpm dev
```

### 5. Deploy

```bash
webdev_deploy mode=preview    # test
webdev_save_checkpoint        # obbligatorio prima della produzione
webdev_deploy mode=production # URL permanente *.easy-peasy.site
```

### 6. Export ZIP (per GitHub/Render)

```bash
cd /home/user && zip -r <name>-export.zip <name>/ \
  -x "*/node_modules/*" -x "*/.git/*" -x "*/dist/*" -x "*/dev-server.log" -x "*/.env" -x "*/.db/*"
```

## Verifica automatica (obbligatoria dopo ogni clone)

1. `pnpm check` deve terminare con 0 errori.
2. Controlla che `server/schema-data.ts` contenga le nuove keyword e i nuovi titoli.
3. Controlla che `client/src/lib/conceptMapPositions.ts` abbia `HUB_TITLE` e `keyword` aggiornati.
4. Controlla che `reportPdf.ts` abbia i nuovi titoli PDF e prefissi file.
5. Apri la preview e prova: crea classe → entra studente → avanza paragrafi → scarica i 3 PDF.

## Regole da rispettare SEMPRE

- **Cambiare SOLO il contenuto.** Non toccare logica di sessione, dashboard, PDF, palette, embed, re-entry studente.
- **Non modificare la sorgente** `/home/user/romanticismo-mappa-concettuale` durante la clonazione (è il riferimento).
- **Mai rimuovere accenti/spagnolismi** dalle keyword (es. "POESÍA", "BÉCQUER").
- **`audioStopAt` e `endTime` vanno sincronizzati**: un segmento audio finisce PRIMA che il narratore dica il numero del paragrafo successivo.
- Se il nuovo contenuto ha un numero diverso di paragrafi/slot, la geometria dell'immagine non corrisponde più: in quel caso ricalcola le coordinate con lo script flood-fill (vedi `immagine-interattivo`) e aggiorna `map.slots`/`map.paraBoxes` di conseguenza.

## Riferimenti

- `/home/user/skills/didattica-app-classe/references/immagine-interattivo-sorgente/contenuto-json.md` — schema completo del JSON contenuto con esempio annotato.
- `/home/user/skills/didattica-app-classe/scripts/immagine-interattivo-sorgente/clone_app.py` — script di clonazione (usa `python3 clone_app.py --help`).
- Skill `immagine-interattivo` — manutenzione dell'app sorgente (UI, PDF, audio, coordinate, deploy).
