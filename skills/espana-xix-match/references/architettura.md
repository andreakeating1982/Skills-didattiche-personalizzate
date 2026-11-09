# Riferimento — Architettura dell'app «Marco histórico del Romanticismo en España» (espana-xix-match)

Riferimento completo del progetto reale `/home/user/espana-xix-match/`. Leggere
questo file quando serve la massima fedeltà all'app originale o un esempio
dettagliato per costruirne una simile.

## Scheda tecnica

| Proprietà | Valore |
|---|---|
| Progetto | `/home/user/espana-xix-match` (scaffold web-static) |
| Stack | Vite 7 + React 19 + TypeScript 5.6 + Tailwind CSS 4 + shadcn/ui + wouter 3.7 (routing) |
| Server | Express minimale (`server/index.ts`): static + `/healthz`, SPA fallback — solo per il deploy Cloud Run |
| Attività | Ascolto-abbinamento: audio di un avvenimento → tocca il puntino giusto sulla linea del tempo |
| Dati | `client/src/data/events.ts` — 7 eventi (id, anno, titolo, audio, x%, y%) + SFX (intro/ok/ko/fin) |
| Immagine | `client/public/timeline.png`, dimensione naturale 1376×821 (`MAP_W`/`MAP_H` in Home.tsx) |
| Audio | `client/public/audio/` — e1808.mp3…e1898.mp3 + intro/ok/ko/fin.mp3 |
| Font | **OpenDyslexic** (UI + PDF; TTF/OTF + base64 in `lib/opendyslexicBase64.ts`) con Cambria/Caladea come fallback |
| Accessibilità | Barra IN ITALIANO (Font, Interlinea, Righello, Modalità, Ascolto, PDF) + TTS auto-lingua + alto contrasto + righello + PDF accessibile; contenuto attività in spagnolo |
| Tema | Dark (`ThemeProvider defaultTheme="dark"`); palette in `client/src/index.css` |
| Embed | postMessage `labvisivo:height`/`romanticismo:height` (rispecchiando il token `cornice` se presente) + risposta al ping `labvisivo:ping` |
| Cornice dinamica | Cartella `cornice-dinamica/` (embed-espana-xix-dedicata.html v3 impermeabile + anti-loop, embed-universale.html, test-impermeabile-espana.html, README.md) |
| Deploy | Preview sandbox + produzione Cloud Run (`pnpm build` → `pnpm start`) |
| Blog | cornice dinamica v3 dedicata nel post Blogger del docente |

## Struttura dei file (rilevante)

```
client/src/
├── App.tsx            → routing wouter: "/" = Home, fallback NotFound; ErrorBoundary + ThemeProvider(dark) + Toaster + TooltipProvider
├── data/events.ts     → EVENTS (dati attività) + SFX + shuffleIds()
├── pages/Home.tsx     → TUTTA l'attività (432 righe, unico componente); prompt iniziale con classe .prompt.start (centrato)
├── components/AccessibilityToolbar.tsx → barra accessibilità IN ITALIANO (Font, Interlinea, Righello, Modalità, Ascolto, PDF); il bottone PDF (senza etichetta «PDF» ripetuta) mostra solo «LINEA DEL TEMPO IN PDF»
├── contexts/AccessibilityContext.tsx  → stato accessibilità (fontScale, lineHeight, ruler, mode) salvato in localStorage exm_access
├── contexts/ThemeContext.tsx, hooks/useReadAloud.ts (TTS auto-lingua es/it), hooks/useComposition.ts, hooks/useMobile.tsx, hooks/usePersistFn.ts, lib/utils.ts
├── lib/timelinePdf.ts → PDF accessibile della linea del tempo (OpenDyslexic incastonato, load dinamico via import())
├── lib/opendyslexicBase64.ts → font OpenDyslexic in base64 per jsPDF
├── components/Map.tsx (Google Maps, non usato dall'attività) + ui/* (shadcn)
├── index.css          → token + classi attività + blocco ACCESIBILIDAD (.accbar, .accgroup, .acclabel, .accbtn, .accbtn-on, .accbtn-pdf, .lf-ruler-band, html.lf-hc, :focus-visible, prefers-reduced-motion)
server/index.ts        → express: /healthz, static dist/public, SPA fallback, porta PORT||3000
shared/const.ts        → COOKIE_NAME, ONE_YEAR_MS (compatibilità scaffold)
client/index.html      → lang="es", title, theme-color #3B1849, viewport mobile
```

## Meccanica di gioco (macchina a stati in Home.tsx)

- **Fasi**: `playing` → `done`. `needsTap` (schermata iniziale), `order` (id eventi mescolati con `shuffleIds`), `step` (indice corrente), `matched` (Set di id azzeccati), `flash` (pulsazione ok/ko sul puntino), `heard` (audio dell'evento ascoltato almeno una volta — lo imposta SOLO il pulsante).
- **Flusso**: tap ovunque → `begin()` → intro → per ogni step: pulsante «Escuchar el audio» → `listen()` (solo se non sta parlando) → l'alunno tocca il puntino → corretto: suono ok, pin ✓, step++ (l'audio dell'evento successivo NON parte da solo); sbagliato: suono ko + flash rosso 1300 ms, nessuna penalità. Finiti tutti → `fin.mp3` → overlay «Actividad completada».
- **Canale audio unico**: UN solo `<audio>` (audioRef) + copie silenziose con `preload="auto"` per ogni clip. Ogni `play()` mette in pausa ciò che suona: le sovrapposizioni non possono esistere. `cue` = "intro" | "event" | "ok" | "ko" | "fin"; `settle(id)` chiude la coda solo se l'id è ancora corrente; `ended`/`error` → settle (un file mancante non blocca il gioco).
- **Puntini ancorati all'area DIPINTA**: l'immagine usa `object-fit: contain`, quindi il box può essere più grande dell'immagine (letterboxing). `syncOverlay()` calcola con `getBoundingClientRect` e `naturalWidth/naturalHeight` l'area dipinta (scala = min(rw/nw, rh/nh)) e posiziona il layer dei pin su quell'area. Le posizioni dei pin sono percentuali di X/Y nell'immagine (`event.x/event.y`).
- **Resize**: ResizeObserver su map/img/root + listener resize/orientationchange/visualViewport + rAF + timeout 250/1200 ms.

## Embed iframe (Blogger) — cornice dinamica v3 impermeabile

- `IS_EMBEDDED = window.parent !== window`; in embed la radice ha classe `embedded`.
- `postHeight()` misura board (con padding), calcola `mapH = availW × MAP_H / MAP_W`,
  somma topbar + dock + barra accessibilità, e invia al parent
  `postMessage({type:"labvisivo:height", height})` E
  `postMessage({type:"romanticismo:height", height})` (legacy) — entrambi i
  tipi NON si cambiano mai. Rinvio quando cambiano phase/needsTap/heard/cue,
  dimensioni del testo, interlinea o modalità.
- **Token `cornice`**: la cornice v3 carica l'app con `?cornice=<token>`;
  `client/src/lib/corniceToken.ts` legge il token e `postHeight()` lo
  rispecchia nei messaggi. La cornice accetta SOLO messaggi con
  `e.source === iframe.contentWindow` e (se presente) token proprio → più
  cornici nella stessa pagina restano isolate (impermeabilità).
- **Ping**: la cornice invia `{type:"labvisivo:ping", cornice:token}` subito,
  ogni 3 s e al resize; Home.tsx ha un listener che risponde con `postHeight()`.
- **Anti-loop**: la cornice NON ha transizioni CSS sull'altezza, applica con
  debounce ~300 ms e clamp 100–15000 px; dentro l'iframe l'altezza è calcolata
  dall'aspect ratio (non dipende dall'altezza dell'iframe).
- **File**: `cornice-dinamica/embed-espana-xix-dedicata.html` (⭐ consigliata,
  da incollare nel post), `embed-universale.html` (template per altre app),
  `test-impermeabile-espana.html` (prova con 2 cornici + intruso). Copia
  pronta anche in `/home/user/embed-blogger-romanticismo.html`.
- **Font/CORS**: la cornice carica OpenDyslexic da
  `/fonts/OpenDyslexic-{Regular,Bold}-v2.woff2` (WOFF2 generati dai TTF con
  `scripts/gen_woff2_cornice.py` della skill — suffisso `-v2` = cache-buster);
  `server/index.ts` risponde a `/fonts/*` con `Access-Control-Allow-Origin: *`
  (obbligatorio per il @font-face cross-origin da Blogger). Verifica rapida su
  produzione: `curl -sI https://espana-xix-match.easy-peasy.site/fonts/OpenDyslexic-Regular-v2.woff2`
  deve dare `200` + `content-type: font/woff2` + `access-control-allow-origin: *`.
- **Verifica end-to-end (fatta in questa chat)**: (1) test locale di
  impermeabilità — 2 istanze della cornice + intruso, con l'app su URL preview:
  ogni cornice applica la PROPRIA altezza (mai 9999) e mostra «App online»;
  (2) test su produzione — iframe cross-origin che carica l'app con
  `?cornice=<token>`: l'app risponde con `{type:"labvisivo:height", height,
  cornice:<token>}` e l'iframe non ha scrollbar.

## Stile (token verificati in index.css)

- Palette :root: `--primary #7a1f2b` (bordeaux), `--chart-1 #c9a227` (oro), `--chart-3 #2c1810`, `--chart-5 #3b1849` (viola scuro), `--background #1a0f12`, `--foreground #f6ead2`, `--radius 0.65rem`.
- Font: OpenDyslexic con priorità (`body`, `.game-root`, `.brand h1`, `.panel h2`, `.listen-btn`, `.cta`, `.prompt`, `.eyebrow`, `.kicker`, `.meta`, `.step`) e Cambria/Caladea come fallback; OpenDyslexic TTF/OTF in `client/public/fonts/` + `@font-face` in coda a index.css.
- Classi accessibilità: `.accbar` (prima riga di .game-root), `.accgroup` (capsula role=group), `.acclabel`/`.accval`/`.accbtn`/`.accbtn-on`/`.accbtn-pdf` (bottone PDF lungo), `html.lf-hc` (alto contrasto), `html.lf-ruler .lf-ruler-band` (banda di lettura), `.dock .prompt.start` (centratura schermata iniziale).
- Classi custom chiave: `.pin` (puntino cliccabile), `.pin-core` (✓ se matched), `.flash-ok`/`.flash-ko` (pulsazioni), `.matched`, `.listen-btn` (pulsante ascolto), `.dock` (footer), `.topbar` (header con h1), `.board`/`.frame`/`.map`/`.pins-layer` (area immagine), `.overlay`/`.panel` (schermata finale «Actividad completada»), `.prompt` (testo guida), `.meta`/`.step` (contatore Audio n/7).
- Schermata finale: `.overlay` è un flex con `overflow-y:auto` + `overscroll-behavior:contain` e `.panel` usa `margin:auto` (centratura sicura: se il pannello supera l'altezza del viewport si scorre invece di clippare il titolo — succedeva su cellulare con font/righe ingranditi). `.overlay` ha `z-index:120`: sta SOPRA la barra accessibilità (`.accbar` z 30) e il righello (z 110), così la schermata finale copre tutto e il titolo non viene più tagliato dalla barra scura sul cellulare (bug segnalato con foto). `.panel h2` ha `line-height` fisso 1.2 (come `.brand h1`, non eredita --lf-lh), `overflow-wrap:anywhere` e `text-wrap:balance`; su schermi stretti il media query riduce padding e scala il titolo (`clamp(1.3rem,6.5vw,2rem)`, centrato). L'overlay finale NON contiene più il pulsante di download del PDF (rimosso su richiesta): il PDF si scarica solo dal modulo della barra.
- Testi guida (promptText): "Pulsa en cualquier parte para empezar." → "Escucha las instrucciones…" → "¡Correcto!" → "No es ese punto. Vuelve a escucharlo cuando quieras." → "Escucha… luego pulsa el acontecimiento correspondiente." → "Pulsa el botón para escuchar el audio." → "Pulsa en el mapa el acontecimiento histórico correspondiente."

## Accessibilità — dettagli (stato settembre 2026)

- **Barra in italiano**: etichette visibili, aria-label, tooltip, testo sr-only e live region sono in italiano (`lang="it"`); il contenuto dell'attività resta spagnolo (`lang="es"` su `<html>`). La barra è la PRIMA riga di `.game-root`: `postHeight()` misura `.accbar` e lo somma al chrome. Il modulo PDF non mostra l'etichetta «PDF» (evita il doppio «PDF» con il testo del bottone): il bottone mostra solo «LINEA DEL TEMPO IN PDF» (una sola riga, va a capo da sé su schermi stretti).
- **Maiuscole uniformi (stile comune)**: `.brand h1`, `.panel h2`, `.cta` e `.meta` sono in MAIUSCOLO via `text-transform: uppercase` (letter-spacing dedicato); il testo nel DOM resta in minuscolo per una corretta lettura da screen reader/TTS.
- **TTS auto-lingua** (`useReadAloud.ts`): lettura ELEMENTO per ELEMENTO
  (vedi `getReadableItems()`): titolo, contatore «Audio {n} de 7», ogni
  pulsante-punto della linea del tempo (dal suo aria-label «anno titolo»),
  messaggi e pulsanti del dock. Tra un elemento e l'altro pausa minima
  `ITEM_PAUSE_MS = 350` ms; tra frasi dello stesso elemento `CHUNK_PAUSE_MS =
  90` ms; frasi spezzate a max 220 caratteri (`splitSentences`).
  `detectLang()` conta marcatori spagnoli/italiani per frase (liste
  ES_MARKERS/IT_MARKERS); `pickBestVoice(lang)` sceglie la voce migliore per
  la lingua (cache es/it/xx, punteggio per provider natural/neural), rate
  0.95. `toNaturalCase()` converte in minuscole le parole in MAIUSCOLO
  (text-transform) e «Y» → «y». `normalizeNumbers()` espande numeri e romani
  nella lingua rilevata; `expandOrdinalsEs()` trasforma i romani ORDINALI
  davanti a nomi propri («I Guerra Carlista» → «Primera Guerra Carlista»)
  deducendo il genere dalla desinenza/parola seguente (lista: república,
  guerra, constitución, restauración, revolución…). Esclusi dalla lettura:
  role=toolbar (la barra italiana), role=status, `.sr-only`, `.lf-ruler-band`,
  `.lf-ruler`; i tag SCRIPT/STYLE/CANVAS/SVG/IFRAME/AUDIO/IMG non vengono
  letti; blocchi separati da DIV/P/H*/LI/SECTION/HEADER/FOOTER/… (BLOCK_TAGS).
- **PDF** (`timelinePdf.ts`): in A4 orizzontale (297×210), SENZA hotspot ma CON le 7 ILLUSTRAZIONI sopra l'asse, anni e titoli sotto; OpenDyslexic Regular+Bold incastonati via base64 (fallback times se fallisce); contenuto ≥14 pt.
  - **Ritaglio icone DINAMICO nel browser** (`loadIconData()`): legge la `<img>` timeline della pagina (stessa origin → canvas pulito, niente CORS), franja verticale icone `ICON_Y0_FR = 246/821` … `ICON_H_FR = 200/821` (fondo 446/821, prima che nella cella 1898 compaia l'eje a ~457), celle verticali tra i punti medi delle colonne (x% di EVENTS), larghezza finestra uniforme `ICON_W_FR = 176/1376`. Per ogni cella misura il bounding box REALE del contenuto (pixel non-bianchi, passo 2 px) e centra la finestra su quel centro (fallback: colonna dell'evento); larghezza ritaglio `min(cw, max(60, cellR-cellL))` dentro la cella. Ritorna dataURL PNG per evento.
  - **Margini di ~3 cm sui 4 lati** (`M = 30` mm): composizione (titolo, figure, eje, anni, titoli) dentro [30..267]×[30..180]; `EDGE = M+3` (33 mm) = incasso del bordo esterno delle figure; geometria: `iconW ≈ 32` (risolta iterando `min(32, max(12, span-1))`, con `span = (PAGE_W-2·EDGE-iconW)/(n-1)`), `iconH = iconW*(ICON_H_FR/ICON_W_FR) = iconW*200/176 ≈ 36.4`, `first = EDGE+iconW/2 ≈ 49`, `iconTop = 66`, `axisY = iconTop+iconH+16`, eje da `M+7 ≈ 37` a `PAGE_W-M-7 ≈ 260` (punta +2 ≈ 262), titolo a y 46 (baseline top, 21 pt), sottotitolo 56 (12 pt), regola oro a y 61 (da M a PAGE_W-M), `yearSize = 16` bold viola (anno sotto l'eje, `yearTop = axisH+7`), `titleSize = 15` tinta con wrap max 3 righe (`titleY0 = yearTop + mmLineHeight(16,1.25) + 5`).
  - La QA del layout PDF (margini e centratura) si fa fuori dal browser replicando la geometria con lo script `scripts/qa_pdf_layout.mjs` (jsPDF in Node: disegna gli stessi rettangoli senza icone vere) e ispezionando il PNG a 120 dpi (pdftoppm): margini ≥ ~30 mm sui 4 lati.
  - Accessibile SOLO da `AccessibilityToolbar` (modulo PDF, `import()` dinamico, chunk separato ~767 kB): l'overlay «Actividad completada» non ha più il pulsante di download.
- **Immagine**: `timeline.png` (1376×821) rigenerata con testi OpenDyslexic (istruzione in alto, anni Bold viola, titoli Regular) tramite `scripts/riscrivi_testi_immagine_opendyslexic.py`; geometria identica → pin (y 20.1%) ed embed invariati. Backup vecchia immagine: `/home/user/timeline_v11_serif_backup.png`.
- **Alto contrasto**: `html.lf-hc { filter: contrast(1.35) saturate(1.15); }` + sfondo nero su body/.game-root, testo bianco su prompt/brand/meta, pannello finale bianco. **Righello**: `.lf-ruler-band` segue il puntatore (banda gialla semitrasparente, pointer-events:none).
- **Stato persistente**: `localStorage` chiave `exm_access` con `{fontScale, lineHeight, ruler, mode}`; applicato su `<html>` (`root.style.fontSize = 16*fontScale px`, CSS vars `--lf-scale`/`--lf-lh`, classi `lf-ruler`/`lf-hc`). Range fontScale 0.8–1.6 (step 0.1), lineHeight tra 1.5 e 2.6.
- **Prompt iniziale**: «Pulsa en cualquier parte para empezar.» con classe `.prompt.start` (flex:1 + text-align:center) — centrato nella dock.
- **Contatore passo**: nel dock, testo `Audio {Math.min(step+1, total)} de {total}` (es. «Audio 3 de 7»), MAIUSCOLO via CSS `.step`.
- **MAIUSCOLO via CSS**: `.brand h1`, `.panel h2`, `.cta`, `.meta`/`.step` hanno `text-transform: uppercase` (mai maiuscole nel DOM: il TTS pronuncia la forma corretta).

## Deploy

```bash
pnpm check          # tsc --noEmit
pnpm build          # vite build && esbuild server/index.ts → dist/
pnpm start          # NODE_ENV=production node dist/index.js (Cloud Run, PORT)
```
- Preview: `webdev_deploy` mode="preview"; Produzione: mode="production" (dopo checkpoint + conferma esplicita dell'utente).
- Il server Express serve `dist/public` (in produzione) con fallback SPA su tutte le route + `/healthz` per il load balancer.

## Checklist per una NUOVA app simile (8 passi)

1. **Base**: usare lo stesso scaffold web-static (o copiare espana-xix-match) — stessi file, stessa logica.
2. **Immagine**: creare la nuova `timeline.png` con lo STESSO aspect ratio (map_w:map_h dichiarati in Home.tsx) e segnare la posizione % di ogni punto (x/y) sulla nuova immagine. Poi ridisegnare i suoi testi in OpenDyslexic con `scripts/riscrivi_testi_immagine_opendyslexic.py` (adattando CX/YEARS/TITLES/INSTR) e verificare numericamente i bounding box delle etichette (nessuna cancellazione incrociata tra colonne vicine: le etichette devono restare complete e separate da spazio bianco).
3. **Audio**: generare con TTS la narrazione di ogni evento + intro/ok/ko/fin (spagnolo/altra lingua), ~1 clip per evento, in `client/public/audio/`.
4. **Dati**: compilare `templates/app-config.json` (titolo, eventi, sfx, dimensioni) ed eseguire `scripts/adatta_app.py --config … --root …`.
5. **Verifica**: `pnpm check` senza errori; provare in locale l'intero flusso (intro → ascolto → corretto/sbagliato → fine).
6. **Cache busting**: incrementare i `?v=N` di immagine e audio quando si sostituiscono i file.
7. **Preview e produzione**: `webdev_deploy` preview → verifica → checkpoint → produzione (con conferma utente).
8. **Embed**: cornice dinamica v3 dedicata (`cornice-dinamica/embed-espana-xix-dedicata.html`) nel post Blogger; per una nuova app aggiornare APP_URL/titolo/colori/URL font (o partire da `embed-universale.html`). L'altezza si adatta da sola (token + ping).

## Errori comuni

| Errore | Soluzione |
|---|---|
| Pin non allineati all'immagine | Controllare che MAP_W/MAP_H corrispondano alla naturale e le % alla nuova immagine |
| Audio sovrapposti | MAI due elementi audio attivi: un solo canale + copie preload |
| Embed con scrollbar | postHeight() deve ricalcolare a ogni cambio di fase; rilanciare ?v= |
| Più cornici nella stessa pagina si «rubano» l'app | Usare SOLO la cornice v3 dedicata (id con token, filtro e.source, token `cornice` rispecchiato dall'app); la vecchia cornice v1 a id fissi non è impermeabile |
| Cornice v3 resta in «Caricamento…/ERRORE» o altezza sbagliata | L'app deve rispondere al ping `labvisivo:ping` e rispecchiare il token `cornice` (corniceToken.ts + Home.tsx); ridistribuire la produzione dopo le modifiche e ripetere il test end-to-end sull'URL live |
| Font della cornice non si caricano (compare Cambria) | Verificare che i WOFF2 `-v2` esistano in client/public/fonts/ e che /fonts/* risponda con `Access-Control-Allow-Origin: *` (curl -sI sull'URL di produzione) |
| PDF: figura tagliata o con la freccia dell'eje in coda | Il crop è dinamico (bbox reale per cella, finestra uniforme centrata) e la franja termina a 446/821 prima dell'eje della cella 1898: se si cambia la timeline.png verificare ICON_Y0_FR/ICON_H_FR/ICON_W_FR e le x% di EVENTS |
| PDF: contenuti fuori dai margini richiesti (~3 cm) | Rifare con `M = 30` mm e la geometria incassata `EDGE = M+3`; verificare con `scripts/qa_pdf_layout.mjs` + pdftoppm 120 dpi |
| Titolo «Actividad completada» tagliato sul cellulare | `.overlay` deve stare SOPRA la barra (z-index 120 > `.accbar` z 30 e righello z 110) ed essere scroll-safe (overflow-y:auto + .panel margin:auto): la barra non deve mai coprire il titolo |
| TTS legge «uno Guerra Carlista» invece di «Primera Guerra Carlista» | `expandOrdinalsEs()` in useReadAloud.ts: romano + parola con iniziale maiuscola → ordinale; estendere ES_ORD_FEM/ES_ORD_MASC e la lista dei femminili se cambiano i titoli |
| Testi scritti già in MAIUSCOLO nel DOM (per «uniformità») | NO: usare `text-transform: uppercase` via CSS così screen reader/TTS pronunciano la forma corretta |
| Bottone PDF con doppio «PDF» o con «SCARICA» | Il modulo PDF non ha etichetta visibile e il bottone è a UNA riga: solo «LINEA DEL TEMPO IN PDF» |
| File audio mancante che blocca il gioco | `error` → `settle(id)`: il gioco continua comunque |
| Immagine/audio vecchi in cache | Incrementare `?v=` su src (es. `?v=12` → `?v=13`) |
| Testi dell'immagine con vecchio serif | Rigenerare con `scripts/riscrivi_testi_immagine_opendyslexic.py`; attenzione ai rettangoli di cancellazione che non devono sconfinare sulle colonne vicine |
| Barra in spagnolo | La barra (AccessibilityToolbar.tsx) è in italiano per scelta: etichette, aria, sr-only e live region; il TTS resta automatico sulla lingua |
| Voce TTS lingua sbagliata | `detectLang()` in useReadAloud.ts bilancia marcatori es/it; estendere i marker per altre lingue |
| h1/title disallineati | Cambiare in 3 punti: Home.tsx h1, Home.tsx alt, index.html title |
