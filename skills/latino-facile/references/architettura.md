# Latino Facile — Scheda tecnica (architettura)

Riferimento per interventi profondi sull'app. Leggere SKILL.md prima; questo file
entra nel dettaglio di file, flussi e comandi. La repo contiene guide aggiornate
(`README.md`, `AGENTS.md`, `REBUILD.md`, `ADATTARE.md`, `RENDER.md`,
`ACCESSIBILITA.md`, `manifest.json`): **sono la fonte di verità** e vanno lette
prima di modifiche strutturali.

## Struttura del progetto

```
latino-facile-app/
├── client/                    # Frontend Vite + React 19 + TS + Tailwind 4
│   ├── index.html             # <html lang="it">, title LATINO FACILE
│   └── public/
│       ├── fonts/             # OpenDyslexic (ttf/otf/woff2) — font UI + PDF
│       ├── tessdata/lat.traineddata.gz   # OCR tesseract.js (latino)
│       ├── quaderno-unico-v16.pdf        # quaderno scaricabile (storici v6, v9, v10-v15)
│       └── cornice-test/      # copia cornice embed servita dall'app
├── shared/types.ts            # Tipi condivisi + COLORI/etichette (CASE/MOOD/POS)
├── server/
│   ├── _core/index.ts         # Express root: CORS /fonts, /_health, mount API
│   ├── routers.ts             # Endpoint tRPC (analisi, OCR, PDF, traduzione…)
│   ├── db.ts / storage.ts     # Drizzle (PostgreSQL opzionale)
│   └── analyzer/              # Whitaker + glossario + traduzione + colori
│       ├── whitaker.ts        # motore Whitaker's Words
│       ├── itGloss*.ts        # glossario italiano personalizzato
│       ├── itTranslate.ts     # traduzione IT
│       ├── translationColors.ts / mapper.ts / normalize.ts / mt.ts
│       └── collatinus.ts, deepl.ts (opzionali)
├── cornice-dinamica/          # Embed per Blogger (dedicata/lite/universale/autosuf.)
├── render.yaml                # Blueprint Render
├── .github/workflows/ci.yml   # CI (check+test+build)
├── .env.example               # variabili d'ambiente di riferimento
├── manifest.json              # metadati macchina dello stack
└── REBUILD.md ADATTARE.md RENDER.md ACCESSIBILITA.md AGENTS.md README.md
```

## Rotta e pagine (wouter)

- `/` → `WelcomePage` (card ingresso: cognome, nome, data gg/mm/aaaa, classe →
  salva in `localStorage["latino-facile-studente"]` → navigate `/app?<query>`).
- `/app` → `Home` (analisi frasi: textarea, OCR foto/PDF via CropDialog →
  tesseract, legenda colori, token cliccabili, PDF colorato, traduzione toggle).
- `/login` → `Login`, `/404` → `NotFound`.
- Il PDF legge i dati studente dalla query string e/o dal `localStorage`.

## Flusso di analisi

1. L'utente inserisce testo o carica foto/PDF → OCR (`client/src/lib/ocr.ts`,
   `cleanOcrText`, worker tesseract.js con `lat.traineddata.gz`).
2. `trpc.analyze` (server) → normalizza → `whitaker.ts` (Whitaker's Words)
   arricchito da glossario italiano (`itGloss*.ts`) → opzioni di analisi per
   ogni parola (caso, modo, POS).
3. `mapper.ts`/`translationColors.ts` assegnano i colori → `TokenData` con
   `CASE_COLORS`, `MOOD_COLORS`, `POS_COLORS` in `shared/types.ts`.
4. `Home.tsx` colora le parole; click su una parola → elenco analisi possibili e
   cambio colore; legenda `LEGEND_ITEMS` (fonte unica APP+PDF: 11 voci
   `label`/`compl`/`sub` con complementi nel colore chiaro via `lightenColor`,
   INDICATIVO arancione, ALTRI MODI VERBALI → PREDICATO VERBALE, niente
   SCONOSCIUTO) + nota voce `LEGEND_VOICE_NOTE` (passivi SOTTOLINEATI:
   `TokenAnalysis.voice` → chip sottolineato in app).
5. Traduzione: `itTranslate.ts` (più Deepl/Collatinus opzionali) con pulsante
   mostra/nascondi.

## PDF (`client/src/lib/export.ts`)

- `buildPdfBlob(tokens, studente, …)` con **pdf-lib + fontkit**.
- Carica `/fonts/OpenDyslexic-Regular.ttf` e `/fonts/OpenDyslexic-Bold.ttf`
  (fetch + arrayBuffer + `embedFont`). **Niente Caladea.**
- Disegna parole colorate con wrapping (`widthOfTextAtSize`), legenda a 3 righe
  per voce (`label` / `compl` nel colore chiaro via `lightenColor` / `sub`,
  righe 38 pt), etichette di analisi (11px), intestazione studente. Download
  con `downloadBlob`.

## Accessibilità — file e meccanica

| Misura | File/meccanica |
|---|---|
| Font OpenDyslexic | `@font-face` in `index.css` (righe ~8–35), file in `client/public/fonts/`, CORS `/fonts` nel server |
| Dimensione testo 80–160% | `--lf-scale` su `:root` (`html[data-lf-…]`), applicato con `calc(18px * var(--lf-scale,1))` |
| Interlinea 1.65–2.6 | `--lf-lh`, usata come `line-height: var(--lf-lh, 1.65)` |
| Righello di lettura | classi `lf-ruler`/`.lf-ruler-band` in `index.css` |
| Alto contrasto | `html.lf-hc` + override body/`.paper-bg`/`.card-paper` |
| Lettura ad alta voce | `hooks/useReadAloud.ts` (barra: Ascolto → Leggi), voce italiana |
| Persistenza | `AccessibilityContext.tsx` salva in `localStorage` |

La barra (`AccessibilityToolbar.tsx`) è montata a livello app e appare su ogni
pagina; pulsanti con `aria-label` (Riduci/Aumenta testo, Interlinea, Righello,
Modalità, Ascolto). Il toggle «Aumenta/Ascolto» ecc. NON altera i dati.

## Embed e cornice (riassunto tecnico)

- `heightSync.ts`: aggiunge `lf-embedded` a `<html>` quando dentro iframe,
  calcola l'altezza reale (regola: mai `documentElement.scrollHeight` assoluto),
  invia `{type:"labvisivo:height", height, cornice:token}`; gestisce token
  `?cornice=` e `ResizeObserver`.
- Cornice dedicata `cornice-dinamica/embed-latino-facile-dedicata.html`: iframe
  → `https://latino-facile-app-2.easy-peasy.site/?cornice=<token>`; ascolta solo
  `e.source` del proprio iframe; clamp 100–15000 px; debounce 200 ms;
  congelamento dopo 3 crescite; font OpenDyslexic via CORS.
- `test-impermeabile.html`: verifica multi-cornice (2 cornici + 1 estranea).

## CropDialog free-box — produzione 8731 (28/10/2026)

Leggere `ritaglio-mobile.md` prima di cambiare layout/scroll. Contratto:
**app dietro FERMA, corpo interno scorrevole col dito**, anche nel blog.
`modal={true}` SOLO per CropDialog, senza cambiare ColorDialog.

- `MIN_BOX = 8%`, `HANDLE_SIZE = 44px`, frecce 2% / Maiusc 10%, 8 maniglie.
- `MIN_IMG_W = 560`: ingrandimento solo visivo e sempre limitato alla larghezza
  utile (meno 4px di bordo), ricalcolato con viewport visibile e rotazione.
- `useCropDialogViewport.ts`: lock body fixed con priorità important (Radix
  altrimenti applica relative important), ripristino stili/scroll; misura con
  visualViewport oppure IntersectionObserver.intersectionRect cross-origin.
- Solo titolo RITAGLIA LA FOTO e foto in corpo overflow-y-auto; nessuna
  istruzione sotto. RUOTA SINISTRA/DESTRA, CHIUDI, RITAGLIA in UN riquadro
  centrato; tutte pillole marroni, touch 44px, senza AZZERA.
- Intera selezione e maniglie: touch-none, senza icona centrale; pan nei
  margini e zone esterne. Capture sul wrapper stabile, pointerId unico e
  delta incrementali per evitare zona morta invertendo ai limiti.
- Test aggiuntivo `tests/crop-drag.e2e.mjs`, 4 scenari; crop-mobile ne ha 9.
  `100dvh` dell'iframe non basta.
- `heightSync.ts`: sospendere invii con `data-lf-crop-open`; rimisurare dopo
  `lf:crop-closed`. Nessun nuovo codice embed richiesto.
- Rotazioni e conferma in PNG lossless (ritaglio lato max 2200). L'invio IA
  successivo scala in JPEG max 1800: sono fasi diverse.
- `confirm()` e `cropBox.ts` invariati nella correzione di layout/scroll.
- `tests/crop-mobile.e2e.mjs`: 9 scenari anche sul pubblico; OCR simulato,
  canvas reale, touch Chromium emulato, nessun telefono fisico.

## Comandi utili

```bash
cd /home/user/latino-facile-app
pnpm check                 # tsc --noEmit
pnpm build                 # vite build + esbuild server
pnpm start                 # produzione locale (dist/index.js)
pnpm exec vitest run       # test (server/**/*.test.ts)
pnpm format                # prettier
pnpm db:push / db:studio   # solo se si usa il DB
```

## Deploy

- Preview: `webdev_deploy mode="preview"` (project dir `/home/user/latino-facile-app`).
- Produzione: checkpoint → preview → condivisione URL → attendere conferma
  esplicita in un NUOVO messaggio → checkpoint → deploy produzione.
  URL stabile: `https://latino-facile-app-2.easy-peasy.site`.
  Stato del rilascio 28/10: deploy 8728, codice `201a6ac`.
- Esportazioni e modifiche alle guide non richiedono né autorizzano un nuovo deploy.
- Render (da GitHub): seguire `RENDER.md`; Blueprint `render.yaml` con
  `pnpm install --frozen-lockfile && pnpm build` e `pnpm start`, health `/_health`.

## Errori/lezione storica (non ripetere)

1. Il vuoto sotto/sopra la card nel post del blog era causato da
   `heightSync` che usava `documentElement.scrollHeight` come altezza assoluta:
   dentro l'iframe resta mai-minore-del-viewport → cornice mai ristretta.
2. Tentativo intermedio fallito: ancorare la card in basso (min-height +
   `justify-content: flex-end` + variabile `--lf-welcome-top`) → spostava il
   vuoto sopra. Rimosso in favore di: card compatta + altezza reale.
3. Font PDF: la documentazione citava Caladea ma il codice carica OpenDyslexic;
   allineare sempre doc (`README.md`, `REBUILD.md`, `ADATTARE.md`, `manifest.json`)
   al codice reale.
4. Script di sviluppo temporanei (test-*.ts in radice, cartella `scripts/`)
   NON devono entrare nel pacchetto esportato (REBUILD.md §8).
