# Archivio di dettaglio — mappa-3passi

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/mappe-interattive.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- File chiave
- Deploy
- Passi dell'app (3 passi + welcome)
- Mappa completata (ConceptMapCanvas)
- Drag & Drop — architettura basata su ref (nessun setState durante il drag)
- Layout e dimensioni contenitori
- Sfondo mappa
- Bottoni download
- Immagini
- Drag su canvas
- Inizializzazione posizioni
- Limite 10 immagini
- Legenda immagini
- Rimozione immagini
- Dettagli UI
- Limiti di caratteri negli input
- Layout SVG (buildDefaultLayout)
- Step indicator
- Color picker
- Embed Blogger
- Esportazione ZIP
- Note

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Mappa Concettuale 3 Passi — Manutenzione

L'app si trova in `/home/user/mappa-3passi-preview`. È un'app `web-db-user` standalone.

## File chiave

| File | Contenuto |
|------|-----------|
| `client/src/pages/Home.tsx` | **Tutta l'app**: welcome, 3 passi, mappa completata, pulsanti download, footer, postMessage |
| `client/src/lib/tipi-mappa.ts` | Tipi TypeScript (`MappaConcettuale`, `Ramo`, `ImmagineMappa`), `COLORI_RAMI`, `darkenColor()` |
| `client/src/components/ConceptMapCanvas.tsx` | Canvas SVG con drag & drop, riquadri rettangolari arrotondati, layout radiale, posizioni in ref |
| `client/src/index.css` | Palette terracotta, variabili CSS |

## Deploy

- **Preview**: `webdev_deploy` con `mode="preview"` sul project_dir `/home/user/mappa-3passi-preview`
- **Produzione**: `webdev_deploy` con `mode="production"` — URL permanente: `https://mappa-3passi-preview.easy-peasy.site`
- **Prima della produzione**: eseguire `webdev_save_checkpoint` con descrizione significativa
- **TypeScript check**: `pnpm check` nella directory del progetto

## Passi dell'app (3 passi + welcome)

| Step | Nome | `currentStep` | Descrizione |
|------|------|---------------|-------------|
| 0 | BENVENUTO | 0 | Form nome/cognome/data/classe, bottone ENTRA |
| 1 | IL TRONCO | 1 | Titolo centrale + color picker (default `#E05D2E`) |
| 2 | I RAMI | 2 | Sottotitoli con colori personalizzabili (default da `COLORI_RAMI`) |
| 3 | LE FOGLIE | 3 | Parole chiave con colori personalizzabili + immagini trascinabili |

`STEP_TITLES = ["BENVENUTO", "PASSO 1 – IL TRONCO", "PASSO 2 – I RAMI", "PASSO 3 – LE FOGLIE"]`

## Mappa completata (ConceptMapCanvas)

Quando `mappa.completata === true`, il canvas SVG mostra:
- Nodo centrale colorato (`coloreTitolo`) con testo bianco, font Cambria/Georgia
- Rami (rettangoli colorati) connessi al centro da linee continue
- Parole chiave (rettangoli bianchi con bordo colorato) connesse al ramo da linee tratteggiate
- Immagini posizionabili con drag direttamente sul canvas SVG (nessun pad/popup separato)

### Drag & Drop — architettura basata su ref (nessun setState durante il drag)

Il drag usa **esclusivamente `useRef`** per posizioni e stato durante il trascinamento. L'unico state è un contatore `tick` incrementato via `requestAnimationFrame` per forzare il refresh visivo (1 solo re-render per frame).

**Struttura dati:**
- `posRami` (ref): `Record<string, {x, y}>` — posizioni committed dei rami
- `posParole` (ref): `Record<string, {x, y}>` — posizioni committed delle parole
- `posImmagini` (ref): `{ x: number; y: number }[]` — posizioni committed delle immagini (array indicizzato)
- `onImmaginiPosizioniRef` (ref): punta sempre all'ultima `onImmaginiPosizioni` callback — **fondamentale per evitare stale closure**
- `drag` (ref): `{on, type, id, ramoId, sx, sy, ox, oy, dx, dy, paroleOff, raf}` — stato drag corrente; `type` può essere `'ramo'`, `'parola'` o `'immagine'`
- `[tick, setTick]` (state): contatore per forzare re-render durante il drag

**Flusso drag:**
1. `onPointerDown` → `svg.setPointerCapture()`, inizializza `drag.current` con posizione originale
2. `onPointerMove` → aggiorna `drag.current.dx/dy`, chiama `requestAnimationFrame` → `setTick(t+1)`
3. `endDrag` → committa posizione finale in `posRami`/`posParole`, resetta `drag.current.dx=0`
4. Durante il render: `displayX = posRami[id].x + (drag.current.on && typeMatch ? drag.current.dx : 0)`

**⚠️ IMPORTANTE:** Non introdurre `setState` durante `onPointerMove` — causa la perdita del pointer capture su touch e il ritorno a scatto. Se serve modificare il comportamento del drag, intervenire SOLO sui ref o sul contatore `tick`.

**⚠️ STALE CLOSURE:** `endDrag` ha dipendenze `[]`. Usare SEMPRE un ref (`onImmaginiPosizioniRef`) per le callback che devono accedere allo stato più recente del parent. Non aggiungere la callback alle dipendenze di `endDrag` — causerebbe la cattura di funzioni vecchie in `onPointerUp`.

**Clamp:** `clampX`/`clampY` limitano le posizioni tra -10 e 110 per evitare che gli elementi escano dal viewBox.

### Layout e dimensioni contenitori

**Stima larghezza testo:** `tw(testo, fontSize) = testo.length * fontSize * 0.72`. Il fattore `0.72` è calibrato su Cambria/Georgia. Non ridurlo: testo più stretto trabocca dai contenitori.

**Padding dichiarato per lato** — la formula larghezza è sempre `tw + 2 * padH`. Non cambiare la semantica.

| Parametro | Valore | Uso |
|-----------|--------|-----|
| `padCentroH = 10` | Per lato | Larghezza centrale = `tw(titolo, fCentro) + 20` |
| `padCentroV = fCentro * 1.6` | Per lato | Altezza centrale = `fCentro + 2 * padCentroV` |
| `padRamoH = 8` | Per lato | Larghezza ramo = `tw(ramo.titolo, fRamo) + 16` |
| `padRamoV = fRamo * 1.4` | Per lato | Altezza ramo = `fRamo + 2 * padRamoV` |
| `padKwH = 7` | Per lato | Larghezza keyword = `tw(parola.testo, fFoglia) + 14` |
| `padKwV = fFoglia * 1.6` | Per lato | Altezza keyword = `fFoglia + 2 * padKwV` |
| `kwMinW` | mini:12, normal:13, fullSize:14 | Larghezza minima contenitore keyword |

**Font size:**
- `fCentro`: mini 3.0, normal 3.0, fullSize 3.4
- `fRamo`: mini 2.5, normal 2.6, fullSize 2.9
- `fFoglia`: mini 2.0, normal 2.1, fullSize 2.4

**Raggio rami:** mini 21, normal 26, fullSize 30. Aumentare se i contenitori dei rami diventano troppo larghi e si sovrappongono al nodo centrale.

### Sfondo mappa

Il contenitore `#mappa-da-stampare` ha `bg-white` (sfondo bianco puro). L'SVG interno è trasparente. Non cambiarlo con `bg-card` (crema): i riquadri bianchi delle keyword perdono definizione.

### Bottoni download

Tutti e tre i pulsanti usano lo stesso stile `bg-secondary hover:bg-secondary/80 text-secondary-foreground`. Ordine: SCARICA PDF → SCARICA IMMAGINE → CREA UN'ALTRA MAPPA.

| Pulsante | Funzione | Tecnologia | Scala |
|----------|----------|------------|-------|
| SCARICA PDF | `scaricaPDF()` | `html2canvas` + `jsPDF` | 2× |
| SCARICA IMMAGINE | `scaricaImmagine()` | `html2canvas` + `canvas.toBlob("image/png")` | 3× |
| CREA UN'ALTRA MAPPA | `ricomincia()` | Reset stato | — |

La funzione `scaricaImmagine` cattura `#mappa-da-stampare` a scala 3×, converte in PNG blob, crea un `<a>` temporaneo e avvia il download di `mappa-concettuale.png`.

## Immagini

### Drag su canvas

Le immagini si posizionano **direttamente sul canvas SVG** con lo stesso sistema drag dei rami e delle keyword. **Non esiste più il pad/popup laterale** per il posizionamento — è stato rimosso. L'utente:
1. Carica le immagini col pulsante `SCEGLI IMMAGINI`
2. Le trascina dove vuole sul canvas (cursore ✋ grab)
3. Regola le dimensioni con i controlli sotto la mappa

Il drag delle immagini usa `type: 'immagine'` e l'indice come `id` (`String(i)`). `endDrag` committa in `posImmagini.current[idx]` e chiama `onImmaginiPosizioniRef.current()` per sincronizzare col parent.

**⚠️ Critico:** `onImmaginiPosizioniRef` è un ref che punta sempre all'ultima callback — SENZA di esso, `endDrag` (con `[]` dipendenze) chiamerebbe la callback iniziale, che legge `mappa.immagini` vecchio, **ripristinando immagini eliminate e posizioni iniziali**.

### Inizializzazione posizioni

`posImmagini` viene inizializzato dal prop `immagini` quando cambia `imgKey` (basata sui `dataUrl`). Il check evita re-init durante i drag (le posizioni restano nei ref).

```ts
const imgKey = immagini?.map(img => img.dataUrl.substring(0, 50)).join('|') || '';
if (imgKey !== prevImgKey.current) {
  prevImgKey.current = imgKey;
  if (immagini) posImmagini.current = immagini.map(img => ({ x: img.x, y: img.y }));
}
```

### Limite 10 immagini

`handleImageUpload` blocca l'upload oltre le 10 immagini. Se l'utente seleziona più file di quanti posti liberi, vengono caricate solo le prime N necessarie per arrivare a 10.

### Legenda immagini

Dopo il caricamento, sotto la mappa appare la legenda con:
- Thumbnail (`w-14 h-14`), titolo **marrone** (`text-amber-900`) **non grassetto** (`font-normal`)
- Controlli **LARGHEZZA** e **ALTEZZA** (scritti per intero, MAI in forma abbreviata)
- Layout arioso: `p-4`, `gap-4`, `space-y-4`, input con `ml-1.5 px-1.5 py-1`
- Pulsante X per rimuovere l'immagine

### Rimozione immagini

`rimuoviImmagine(i)` filtra l'array con `filter((_, j) => j !== i)`. Quando il prop `immagini` cambia, `imgKey` cambia e `posImmagini` viene re-inizializzato correttamente con le sole immagini rimanenti.

## Dettagli UI

- **MAPPA COMPLETATA**: scritto senza punto esclamativo
- **REALIZZATO DA [studente]**: ha `mt-4 mb-2 py-1.5` per dare respiro sopra e sotto
- **Sfondo mappa**: `bg-white` puro nel contenitore `#mappa-da-stampare`

## Limiti di caratteri negli input

I campi di input hanno `maxLength` e validazione con contatore `x/N caratteri` (diventa rosso al raggiungimento del limite):

| Campo | Passo | Limite | Note |
|-------|-------|--------|------|
| Titolo centrale | 1 (IL TRONCO) | **40** | `slice(0, 40)`, `maxLength={40}`, `>= 40` |
| Sottotitolo / Ramo | 2 (I RAMI) | **28** | `slice(0, 28)`, `maxLength={28}`, `>= 28` |
| Parola chiave / Foglia | 3 (LE FOGLIE) | **32** | `slice(0, 32)`, `maxLength={32}`, `>= 32` |

I campi del benvenuto (Cognome, Nome, Data, Classe) NON hanno limiti. Se un testo è molto lungo, il riquadro sulla mappa si allarga automaticamente (larghezza = `tw(testo) + 2 * padH`), quindi il layout resta adattivo.

## Layout SVG (buildDefaultLayout)

La funzione `buildDefaultLayout` calcola il layout radiale di default nel viewBox SVG (0-100). È usata solo come posizione iniziale: dopo il primo drag, le posizioni sono nei ref e il layout default non viene più applicato.

**Attenzione:** La funzione riceve `padKwH` come parametro e lo usa come `2 * padKwH` internamente (perché il chiamante passa il valore per-lato). Non modificare la chiamata senza aggiornare anche il corpo.

Parametri passati: `ramiAttivi, totale, raggioRami, distFoglie, gapTraKw, spreadCap, fFoglia, kwMinW, padKwH`.

## Step indicator

Barra di avanzamento: INIZIO (step 0), 1, 2, 3, FINE. Il passo corrente è evidenziato con `bg-primary text-primary-foreground`. Quando `mappa.completata` è true, tutti i 3 passi diventano verdi (`bg-green-400`) con spunta ✓.

## Color picker

L'utente può personalizzare:
- **Titolo centrale** (Passo 1): `<input type="color">` con default `#E05D2E`, salva in `coloreTitolo`
- **Rami** (Passo 2): Per ogni ramo, color picker con default ciclato da `COLORI_RAMI`
- **Parole chiave** (Passo 3): Per ogni keyword, color picker che eredita il colore del ramo selezionato

Il colore titolo viene scurito per il bordo tramite `darkenColor()` esportata da `tipi-mappa.ts`.

## Embed Blogger

L'app usa `ResizeObserver` + `postMessage` (`{ type: 'mappaconcettuale:height', height }`) per altezza dinamica. Codice embed in `embed-blogger.html`. La cornice ha gradiente `rgb(230, 205, 171)`.

## Esportazione ZIP

```bash
cd /home/user/mappa-3passi-preview && zip -r /home/user/mappa-3passi.zip . \
  -x "node_modules/*" "client/node_modules/*" "server/node_modules/*" \
  -x ".git/*" "dist/*" "dev-server.log"
```

## Note

- Dati salvati in `localStorage` con chiave `"mappa-concettuale-3passi"`
- Type `MappaConcettuale`: `studente`, `titoloCentrale`, `rami`, `immagini`, `stepCorrente`, `completata`, `coloreTitolo`
- PDF generato con `jsPDF` + `html2canvas`; PNG generato con `html2canvas` + `canvas.toBlob()`
- Il colore di ogni keyword è salvato in `parola.colore` e usato come `stroke` del riquadro
- Rispetto alla versione 6 passi (skill `mappa-concettuale`), NON ci sono `riassunto`, `appunti`, `hashtags`
- **Drag system critico**: tutto in ref, zero setState durante `onPointerMove`. Modificare solo `drag.current` e `posRami`/`posParole` ref.
