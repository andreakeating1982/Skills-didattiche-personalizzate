# heightSync — anti-tremolio (sincronizzazione altezza in embed)

Perché esiste: su mobile e nel blog l'app «tremava» cambiando altezza di continuo (durante l'elaborazione della foto, l'apertura della sezione PDF…). La causa era un **anello di feedback**: l'app inviava un messaggio di altezza a ogni evento di layout (ResizeObserver + resize) e misurava anche valori derivati dal **viewport** dell'iframe; su mobile il viewport è frazionario (barra degli indirizzi, DPR) → il valore oscillava tra «contenuto» e «viewport» → la cornice ridimensionava → il resize dell'iframe generava un altro evento → ciclo infinito.

## Il protocollo

- App → parent: `{ type: "labvisivo:height", height: <px>, cornice?: <token> }`
- Parent → app (ping di recovery): `{ type: "labvisivo:ping", cornice? }` — la cornice la usa per chiedere l'altezza in ogni momento
- Token: query param `?cornice=...` nell'URL dell'iframe, rispedito nei messaggi
- Attivo solo se `window.self !== window.top`; altrimenti `initHeightSync()` non invia nulla

## Le 5 regole in `client/src/lib/heightSync.ts` (NON violarle)

1. **Misura solo il contenuto** — `measureContentHeight()` usa `#root` (mount di React) e `body` (`scrollHeight`/`offsetHeight`). MAI `documentElement.scrollHeight/offsetHeight` (restano «gonfiati» all'altezza del viewport quando il contenuto è corto) e MAI `innerHeight` (frazionario su mobile). Sotto `MIN_HEIGHT = 100` non si invia (pagina non renderizzata).
2. **Deduplica** — se il valore quantizzato è uguale a `lastSent`, ZERO invii. È la regola che spezza il feedback cornice→resize→invio: quando la cornice ridimensiona l'iframe, il `resize` dell'app non produce nulla.
3. **Quantizzazione 2 px per eccesso** — `Math.ceil(raw / 2) * 2` (`QUANTUM_STEP`): assorbe il jitter ±1 px da DPR/sottopixel senza tagliare contenuto.
4. **Throttle 150 ms** (`MIN_SEND_INTERVAL`) con **trailing send** a fine raffica (spinner OCR, miniature, apertura PDF = raffiche di eventi → un solo invio con l'ultimo valore). Il trailing NON usa `force` (la deduplica scarta i valori invariati).
5. **Isteresi in riduzione 250 ms** (`SHRINK_STABILITY_MS`): una crescita parte subito; una riduzione solo se il valore più piccolo resta stabile ≥250 ms (niente effetto elastico con elementi che appaiono/scompaiono). Un timer di retry ritenta da solo se nessun altro evento arriverà.

## Chi forza l'invio (force = true) e chi no

- **force = true**: il primissimo handshake all'avvio e le risposte ai `labvisivo:ping` (sono la rete di recovery: il parent paragona il valore con LA SUA altezza applicata, quindi un valore «già inviato» può servirgli). I valori identici non producono comunque movimento (filtro ±2 px lato cornice).
- **NON forzati**: `load`, i retry a 500/1500/3000 ms, gli eventi `resize` e `ResizeObserver`. Usare force sui retry crea messaggi identici ripetuti (bug corretto nel checkpoint `1f929f6`).

## ResizeObserver e listener

- Osservare **solo `#root`** (fallback `body`): osservare `<html>`/`<body>` farebbe scattare l'observer anche quando è la CORNICE a ridimensionare l'iframe (feedback diretto).
- `window.addEventListener("resize", …)` serve per i cambi di LARGHEZZA (rotazione, resize della cornice): è innocuo perché passa per throttle+deduplica.
- `initHeightSync()` (in `main.tsx`, prima di `createRoot`) aggiunge la classe `lf-embedded` a `<html>` quando siamo in iframe.

## Lato cornice (non modificare per i problemi di tremolio)

`cornice-dinamica/embed-mappe-lingue-dedicata.html` ha già: `.lf-iframe { transition: none }`, debounce 200 ms, **filtro ±2 px** (niente movimento per variazioni minime), **finestra di silenzio** 300 ms per cambi <30 px dopo un'applicazione, **anti-loop graduale** (3 crescite consecutive → congela 5 s), conferma per salti sospetti, ping ogni 3 s. Con un'app «silenziosa» (le 5 regole sopra) questi filtri non vengono mai sfidati.

## Sintomi → cause (storico di questa app)

| Sintomo | Causa | Fix |
|---|---|---|
| Tremolio continuo su mobile/blog | invii a ogni evento + misure da viewport + feedback resize | 5 regole heightSync (`1f929f6`) |
| Cornice che si allarga a dismisura quando si genera il PDF | anteprima PDF `h-[75vh]` dipende dal viewport della cornice | `.lf-pdf-preview { height: 520px !important }` in `html.lf-embedded` (`8ef78a9`) |
| Grande vuoto sotto la prima pagina | `min-h-dvh` nel calcolo dell'altezza in embed | `min-height: 0 !important` su `html.lf-embedded` |
| Pagina autonoma termina male | body crema riempiva il viewport | `html.lf-welcome-top body { background:#fff }` |
| Manca la freccia tra gli ultimi due passi | off-by-one nell'array `connectors` di pdf.ts | freccia prima di OGNI passo (`910225e`) |

## Test anti-tremolio

Pagina `client/public/test-oscillazione.html` (servita dal dev server a `/test-oscillazione.html`): iframe 390 px con **viewport frazionario 703.37 px** (come mobile), registra TUTTI i messaggi `labvisivo:height`, replica l'applicazione con debounce 200 ms, espone `window.__log` e `window.__analizza()` (conteggio oscillazioni = 3 messaggi consecutivi che alternano su/giù di ≥2 px entro 1,5 s).

Esito atteso sull'intero flusso (entra → estrai 3 esercizi → genera PDF): **3 messaggi in totale** (avvio → schede → sezione PDF), **0 oscillazioni**, **0 valori identici ripetuti**, tutti pari. Al termine, impostare `iframe.style.height = (ultimaAltezza + 0.37) + 'px'` e verificare che **arrivi alcun nuovo messaggio** (il vecchio codice reagiva al viewport frazionario).

Procedura di collaudo completa: `references/collaudo-browser.md`.
