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
| Font | Cambria → fallback Caladea (TTF in `client/public/fonts/`) |
| Tema | Dark (`ThemeProvider defaultTheme="dark"`); palette in `client/src/index.css` |
| Embed | postMessage `labvisivo:height` e `romanticismo:height` per il resize in iframe |
| Deploy | Preview sandbox + produzione Cloud Run (`pnpm build` → `pnpm start`) |
| Blog | iframe nel post Blogger del docente |

## Struttura dei file (rilevante)

```
client/src/
├── App.tsx            → routing wouter: "/" = Home, fallback NotFound; ErrorBoundary + ThemeProvider(dark) + Toaster + TooltipProvider
├── data/events.ts     → EVENTS (dati attività) + SFX + shuffleIds()
├── pages/Home.tsx     → TUTTA l'attività (401 righe, unico componente)
├── index.css          → token di tema + classi custom (.game-root, .board, .map, .pins-layer, .pin, .pin-core, .flash-ok, .flash-ko, .matched, .dock, .listen-btn, .prompt, .topbar, .brand, .meta, .step, .overlay, .panel)
├── contexts/ThemeContext.tsx, hooks/useComposition.ts, hooks/useMobile.tsx, hooks/usePersistFn.ts, lib/utils.ts
├── components/Map.tsx (Google Maps, non usato dall'attività) + ui/* (shadcn)
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

## Embed iframe (Blogger)

- `IS_EMBEDDED = window.parent !== window`; in embed la radice ha classe `embedded`.
- `postHeight()` misura board (con padding), calcola `mapH = availW × MAP_H / MAP_W`, somma topbar + dock, e invia al parent: `postMessage({type:"labvisivo:height", height}, "*")` E `postMessage({type:"romanticismo:height", height}, "*")` — entrambi i tipi sono usati dal sistema di embedding. Rinvio quando cambiano phase/needsTap/heard/cue (il footer cambia altezza).
- NON cambiare mai i tipi di messaggio.

## Stile (token verificati in index.css)

- Palette :root: `--primary #7a1f2b` (bordeaux), `--chart-1 #c9a227` (oro), `--chart-3 #2c1810`, `--chart-5 #3b1849` (viola scuro), `--background #1a0f12`, `--foreground #f6ead2`, `--radius 0.65rem`.
- Font: `Cambria, "Caladea", "Liberation Serif", Georgia, serif` ovunque; Caladea embeddata in `client/public/fonts/`.
- Classi custom chiave: `.pin` (puntino cliccabile), `.pin-core` (✓ se matched), `.flash-ok`/`.flash-ko` (pulsazioni), `.matched`, `.listen-btn` (pulsante ascolto), `.dock` (footer), `.topbar` (header con h1), `.board`/`.frame`/`.map`/`.pins-layer` (area immagine), `.overlay`/`.panel` (schermata finale), `.prompt` (testo guida), `.meta`/`.step` (contatore Audio n/7).
- Testi guida (promptText): "Pulsa en cualquier parte para empezar." → "Escucha las instrucciones…" → "¡Correcto!" → "No es ese punto. Vuelve a escucharlo cuando quieras." → "Escucha… luego pulsa el acontecimiento correspondiente." → "Pulsa el botón para escuchar el audio." → "Pulsa en el mapa el acontecimiento histórico correspondiente."

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
2. **Immagine**: creare la nuova `timeline.png` con lo STESSO aspect ratio (map_w:map_h dichiarati in Home.tsx) e segnare la posizione % di ogni punto (x/y) sulla nuova immagine.
3. **Audio**: generare con TTS la narrazione di ogni evento + intro/ok/ko/fin (spagnolo/altra lingua), ~1 clip per evento, in `client/public/audio/`.
4. **Dati**: compilare `templates/app-config.json` (titolo, eventi, sfx, dimensioni) ed eseguire `scripts/adatta_app.py --config … --root …`.
5. **Verifica**: `pnpm check` senza errori; provare in locale l'intero flusso (intro → ascolto → corretto/sbagliato → fine).
6. **Cache busting**: incrementare i `?v=N` di immagine e audio quando si sostituiscono i file.
7. **Preview e produzione**: `webdev_deploy` preview → verifica → checkpoint → produzione (con conferma utente).
8. **Embed**: iframe nel post Blogger; il resize automatico funziona via postMessage.

## Errori comuni

| Errore | Soluzione |
|---|---|
| Pin non allineati all'immagine | Controllare che MAP_W/MAP_H corrispondano alla naturale e le % alla nuova immagine |
| Audio sovrapposti | MAI due elementi audio attivi: un solo canale + copie preload |
| Embed con scrollbar | postHeight() deve ricalcolare a ogni cambio di fase; rilanciare ?v= |
| File audio mancante che blocca il gioco | `error` → `settle(id)`: il gioco continua comunque |
| Immagine/audio vecchi in cache | Incrementare `?v=` su src (es. `?v=12` → `?v=13`) |
| h1/title disallineati | Cambiare in 3 punti: Home.tsx h1, Home.tsx alt, index.html title |
