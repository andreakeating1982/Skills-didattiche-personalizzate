---
name: mappa-3passi
description: "Manutenzione completa e personalizzazione dell'app Mappa Concettuale 3 Passi (Vite + React + TypeScript + Tailwind + tRPC + Drizzle + SQLite). Usare per: modificare UI studente/docente, deploy preview/produzione, personalizzare colori titolo/rami/foglie, correggere drag & drop, modificare il layout dei contenitori, gestire i pulsanti di download (PDF e PNG), pareggiare i margini della prima pagina WelcomePage (regole lf-welcome-top/lf-embedded, heightSync, come in Latino Facile), creare embed Blogger, esportare ZIP per GitHub. L'app guida lo studente nella costruzione di una mappa concettuale in 3 passi (tronco, rami, foglie/immagini). Rispetto alla versione a 6 passi (skill mappa-concettuale), questa versione salta i passi 1-3 (leggi e ripeti, prendi appunti, crea hashtag)."
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

## Embed Blogger — cornice dinamica (v3 impermeabile)

La **cornice dinamica** è portata dall'app sorgente
`EQUAZIONI-DI-QUARTO-GRADO-TRINOMIE-BIQUADRATICHE` (stessa famiglia LabVisivo):
un blocco HTML autonomo da incollare nel post (vista HTML di Blogger).
Pacchetto in `cornice-dinamica/` alla radice del progetto:

- `embed-mappa-3passi-dedicata.html` ⭐ versione consigliata (v3 impermeabile +
  anti-loop: titolo e pulsanti su stessa riga centrati, Schermo intero, Ricarica,
  spinner, stato online/errore con Riprova, ping 3 s, altezza al resize,
  isolamento multi-embed con token e filtro `e.source`, anti-loop mobile)
- `embed-mappa-3passi-lite.html` (minima ~5 KB, riutilizzabile con `?app=`)
- `embed-universale.html` (template con URL segnaposto per altre app)
- `embed-mappa-3passi.html` (autosufficiente, font in base64 ~128 KB)
- `test-dedicata.html` / `test-impermeabile.html` (pagine di test)
- `fonts/` (OpenDyslexic Regular/Bold v2 woff2)

Anche `embed-blogger.html` (radice progetto) contiene la stessa cornice dedicata
v3: incollare l'INTERO contenuto nel post.

**Protocollo altezza dinamica `labvisivo:height`** (gestito da `heightSync.ts`):

| Pezzo | Dove | Ruolo |
|-------|------|-------|
| `client/src/lib/heightSync.ts` | lib | Invia `{ type: "labvisivo:height", height }`, risponde al ping `labvisivo:ping` rispecchiando il token `?cornice=` |
| `client/src/main.tsx` | entry | Chiama `initHeightSync()` PRIMA del render |
| `client/src/index.css` | css | Regole `html.lf-embedded` (niente 100vh in iframe → anti-loop) |
| Server `/fonts` | `server/_core/index.ts` | CORS `Access-Control-Allow-Origin: *` (per i font cross-origin) |
| `client/public/fonts/` | asset | File `OpenDyslexic-*-v2.woff2` serviti dall'app |

In `Home.tsx` resta anche il postMessage LEGACY `mappaconcettuale:height` per le
vecchie cornici già incollate nei post: NON rimuoverlo, è retrocompatibile.
Il protocollo corrente (cornice v3) è però `labvisivo:height`.

### PRIMA PAGINA (BENVENUTO, step 0) — margini pareggiati (lavoro 2026-09-03)

Obiettivo (allineamento a Latino Facile; foto di riferimento `margini_prima_pagina.png`):
la card del benvenuto segue subito la step bar invece di essere centrata verticalmente
nel vuoto, con **24px sopra e 24px sotto la card**, così la cornice dinamica si
restringe all'altezza reale del contenuto (**~486px** invece dei 640px fissi che
lasciavano un grande vuoto crema sopra la card). Tre meccanismi che lavorano insieme:

1. **`Home.tsx` — classe `lf-welcome-main` sul `<main>`** quando `currentStep === 0`:
   `className={\`container flex-1 flex flex-col ${currentStep === 0 ? "lf-welcome-main" : "py-3 md:py-5"}\`}`.
   In embed il padding verticale del main viene azzerato; a gestirlo è `.lf-welcome`.

2. **`Home.tsx` — `useEffect` che aggiunge `lf-welcome-top` su `<html>`** SOLO quando
   `currentStep === 0` E l'app è aperta autonoma (`window.self === window.top`).
   Dentro l'iframe la classe NON va aggiunta: lì lo sfondo crema resta coerente e
   l'altezza è gestita da heightSync. Cleanup alla rimozione (commento a ~riga 200).

3. **`index.css` — regole della sezione "PRIMA PAGINA BENVENUTO"**:
   - `html.lf-embedded .lf-welcome-main` → `padding-top/bottom: 0` (in embed);
   - `html.lf-embedded .lf-welcome` → `min-height: 0; justify-content: flex-start;
     padding-top: 24px; padding-bottom: 24px` (24/24 in embed);
   - `html.lf-welcome-top` (pagina autonoma) → `background: #fff` su html e body,
     disattiva i `min-h-screen`/`min-h-dvh` (100vh), `.lf-welcome` con padding-top
     24px + padding-bottom 48px e pseudo-elemento `::after` (gradiente 48px che
     sfuma nel bianco del canvas, niente taglio netto).

Regole collegate `html.lf-embedded` (già esistenti, anti-loop): azzerano il
`min-height` di `body` e dei wrapper `.min-h-screen`/`.min-h-dvh` dentro l'iframe,
altrimenti l'altezza misurata dipenderebbe dall'iframe stesso (loop di crescita).

### heightSync.ts — fix "la cornice deve poter SHRINKARE" (2026-09-03)

**Sintomo risolto**: con `documentElement.scrollHeight` come riferimento assoluto,
quando il contenuto è più corto dell'iframe lo scrollHeight del documento resta
"gonfiato" all'altezza del viewport dell'iframe (mai meno) → la cornice dinamica
NON poteva restringersi e la prima pagina mostrava un grande vuoto.

**`currentHeight()` corretto**:
1. `h = max(body.scrollHeight, body.offsetHeight, docEl.offsetHeight)` — altezza
   REALE del contenuto (body + offsetHeight del documento);
2. aggiungere `docEl.scrollHeight` SOLO se `docEl.scrollHeight > viewportH`
   (cioè quando il contenuto supera davvero il viewport dell'iframe).

**Invio**: attivo solo dentro iframe (`window.self !== window.top`), solo se
`height > 100`; i messaggi rispecchiano il token `?cornice=` (la cornice filtra
con `e.source` + token, vedi embed). Risponde anche al ping `labvisivo:ping`.

### Verifica embed (cornice Blogger) — procedura collaudata in chat

La verifica dei margini va fatta nel contesto EMBED (app dentro l'iframe della
cornice), NON in pagina standalone: lo screenshot standalone non prova il risultato.
Il riferimento era la tabella di confronto "Prima: 640px fissi + vuoto ~500px sopra
la card → Ora: ~486px dinamici + 24px/24px".

Procedura collaudata:
1. Copiare `embed-blogger.html` (o la cornice dedicata) in `client/public/_cornice-test.html`
   (prefisso `_` = pagina di test, non va in produzione);
2. Avviare la preview (`webdev_deploy mode="preview"`) e aprire nel browser
   `<preview-url>/_cornice-test.html`;
3. La cornice carica l'app (URL di produzione) nell'iframe e si ridimensiona via
   `labvisivo:height`: verificare card welcome completa, spazi sopra/sotto bilanciati
   (~24px), niente scroll interno né vuoti enormi;
4. Rimuovere il file temporaneo e committare la rimozione (la preview auto-committa
   i file presenti: `git rm --cached` + commit).

⚠️ Ambiente sandbox: `file://` è bloccato nel browser remoto e le porte locali
(`localhost:8099` ecc.) NON sono raggiungibili dal browser remoto — passare sempre
dal proxy preview (URL `*.sandbox.easy-peasy.ai`) o dal dev server esposto.

## Esportazione ZIP

Prima di esportare: rimuovere le pagine di test `client/public/_*.html` e tenere
aggiornati i documenti alla radice inclusi nel pacchetto (`GUIDA-IA.md`,
`ACCESSIBILITA.md`, `DEPLOY-RENDER.md`, `DOCUMENTAZIONE_DETTAGLIATA.md`,
`ISTRUZIONI-GITHUB.txt`, `README.md`, `cornice-dinamica/README.md`, `render.yaml`).

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
