---
name: equazioni-secondo-grado
description: "Manutenzione dell'app EQUAZIONI DI SECONDO GRADO (/home/user/equazioni-secondo-grado, Vite + React 19 + TS + Tailwind 4 + shadcn/ui + KaTeX + ONNX/ink-on, web-static con mini server Express). Variante grado 2 (k=1) del Widget Matematico: a·x²+b·x+c=0 in 5 passi con scrittura manuale e PDF. Usare per: prima pagina (WelcomePage, lf-welcome-top/lf-embedded, heightSync), barra accessibilità, cornice dinamica Blogger (anti-loop), verifica embed (COEP: solo same-origin), PDF, trascrizione soluzioni (incomplete SENZA zeri visibili, semplificazione massima radici esatte), patch ink-on numThreads=1 (blocco caricamento modello AI), deploy con verifica URL (lezione 403/404), doc bundle. NON per clonare in altro grado (widget-matematico-sorgente) né per la sorgente biquadratica (equazioni-biquadratiche)."
---

# Equazioni di Secondo Grado — Skill di Manutenzione

## Overview

App in `/home/user/equazioni-secondo-grado`. Variante **grado 2 (k = 1)** del Widget Matematico, clonata dalla sorgente biquadratica (k = 2) in `/home/user/equazioni-biquadratiche`. Scaffold **`web-static`** con un **mini server Express** (`server/index.ts`) che serve i file statici e imposta header COOP/COEP (richiesti da ONNX Runtime Web). Stack: Vite + React 19 + TypeScript + TailwindCSS 4 + shadcn/ui + KaTeX + `ink-on`/ONNX per il riconoscimento della scrittura.

**URL produzione**: `https://equazioni-secondo-grado.easy-peasy.site` (Cloud Run, attivo dalla chat del 04/10/2026, deploymentId 7445). **Il sottodominio `friendlyUrl` è assegnato dalla piattaforma e PUÒ CAMBIARE tra un deploy e l'altro** (storicamente: `app-2.easy-peasy.site`, prima ancora `deploy-hook-eq2grado.easy-peasy.site`): dopo OGNI deploy verificare con `curl` quale dominio risponde e aggiornare `APP_URL` nelle cornici se cambia. **Repo sorgente famiglia**: `https://github.com/andreakeating1982/EQUAZIONI-DI-QUARTO-GRADO-TRINOMIE-BIQUADRATICHE`. Modello di riferimento per layout/accessibilità: LATINO FACILE.

L'app guida lo studente nella risoluzione di una quadratica `a·x² + b·x + c = 0` in **5 passi** (niente sostituzione `t = x^k`, niente estrazione di radice: k = 1): forma canonica/coefficienti → Δ → `x₁ = (−b+√Δ)/(2a)` → `x₂ = (−b−√Δ)/(2a)` → verifica finale. Ogni calcolo è inserito a mano su canvas (ONNX), con box **RICOPIA SUL QUADERNO** e PDF finale in OpenDyslexic.

## Routing (App.tsx)

| Route | Componente | Ruolo |
|---|---|---|
| `/` | `WelcomePage` | Prima pagina: card Cognome/Nome/Data/Classe + ENTRA |
| `/esercizio` | `QuadraticExercises` | L'esercizio vero (5 passi, ~1435 righe) |
| `/404` | `NotFound` | Fallback |

`WelcomePage` naviga a `/esercizio?cognome=…&nome=…&data=…&classe=…` (parametri in query).

## File Critici

| File | Ruolo | Righe |
|---|---|---|
| `client/src/main.tsx` | **`initHeightSync`**: sincronizzazione altezza con la cornice embed (protocollo `labvisivo:height` + ping) | 130 |
| `client/src/pages/WelcomePage.tsx` | Prima pagina compatta (card sotto la barra), classe `lf-welcome-top` in vista autonoma | ~157 |
| `client/src/pages/QuadraticExercises.tsx` | Tutto l'esercizio: generazione, 5 passi, NotebookGuide, PDF, verifica | ~1435 |
| `client/src/components/AccessibilityToolbar.tsx` | Barra accessibilità 5 moduli (FONT, INTERLINEA, RIGHELLO, MODALITÀ, ASCOLTO), fix screen reader | ~206 |
| `client/src/components/NumberInputCanvas.tsx` | Canvas input con riconoscimento ONNX (condiviso con la famiglia) | ~797 |
| `client/src/components/MathDrawCanvas.tsx` | Canvas disegno puro | 349 |
| `client/src/hooks/useReadAloud.ts` | Lettura ad alta voce (TTS italiano) | — |
| `client/src/contexts/AccessibilityContext.tsx` | Preferenze accessibilità (persistite in `localStorage` → `wms_access`) | — |
| `client/src/index.css` | Tema + **tutte le regole `lf-*`** (welcome-top, embedded, ruler, hc, scale) | ~471 |
| `server/index.ts` | Express statico + header COOP/COEP **solo su HTML** + CORS `/fonts` + MIME wasm | — |
| `cornice-dinamica/embed-equazioni-secondo-grado-dedicata.html` | **Cornice dedicata v3** per Blogger (quella da incollare) | 478 |

## PRIMA PAGINA — margini pareggiati (lavoro principale di questa chat)

Obiettivo (foto di verifica "Prima/Ora"): la prima pagina deve replicare il layout compatto di LATINO FACILE — card **subito sotto la barra di accessibilità**, pagina che **termina subito dopo la card**, niente "grande vuoto crema". Valori di riferimento misurati:

- **Dentro la cornice (embed)**: 24px sopra la card (20px padding-top di `.lf-welcome` + 4px `mb-1` della barra) e **24px sotto** → simmetrici. L'iframe si restringe a **≈486px** (non 640px fissi).
- **Vista autonoma** (fuori dal blog): body **bianco** sotto la card, pagina termina subito dopo (misurato: card 58→402, body 442px).

### Regole in `client/src/index.css` (leggere PRIMA di toccare la prima pagina)

```css
/* Vista AUTONOMA: WelcomePage aggiunge html.lf-welcome-top su <html>
   quando window.self === window.top (useEffect in WelcomePage) */
html.lf-welcome-top body { background-color: #ffffff; }
html.lf-welcome-top .lf-welcome { position: relative; }
/* Dissolvenza morbida in fondo al blocco crema */
html.lf-welcome-top .lf-welcome::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 0;
  height: 48px;
  background: linear-gradient(to bottom, rgba(248,241,228,0), #ffffff);
  pointer-events: none;
}

/* Vista EMBED: heightSync aggiunge html.lf-embedded su <html> quando
   l'app è in un iframe — azzera i min-height 100vh (causa del loop) */
html.lf-embedded .min-h-screen,
html.lf-embedded .min-h-dvh { min-height: 0 !important; }
html.lf-embedded body { min-height: 0 !important; }
html.lf-embedded .lf-welcome {
  min-height: 0 !important;
  justify-content: flex-start;
  padding-top: 20px;      /* + mb-1 della barra (4px) = 24px sopra */
  padding-bottom: 24px;   /* 24px sotto: simmetrico */
}
/* Neutralizza pt-4 sm:pt-8 del primo contenitore interno (16/32px): lo
   spazio sopra la card è già dato dal padding-top di .lf-welcome */
html.lf-embedded .lf-welcome > div:first-child { padding-top: 0 !important; }
```

**NON** aggiungere `lf-welcome-top` in modalità embed (è heightSync a gestire l'altezza reale). La classe va messa/rimossa solo in vista autonoma, con cleanup nel `useEffect` (`return () => …remove`).

## heightSync in `client/src/main.tsx` (NON esiste file separato)

IIFE `initHeightSync` eseguita prima del `createRoot`. Da NON rimuovere né duplicare altrove.

- **Modalità embed**: se `window.self !== window.top` (con try/catch: cross-origin → `true`) aggiunge `lf-embedded` su `<html>`.
- **Misura che SA RESTRINGERSI** (fix chiave della chat): NON usare `documentElement.scrollHeight` come riferimento assoluto — dentro un iframe più alto del contenuto lo scrollHeight resta "gonfiato" all'altezza del viewport e la cornice non potrebbe mai restringersi. Si usa:
  ```ts
  let h = Math.max(body.scrollHeight, body.offsetHeight, docEl.offsetHeight);
  if (docEl.scrollHeight > viewportH) h = Math.max(h, docEl.scrollHeight);
  ```
  → la cornice segue la card (~486px) invece di restare a 640px.
- **`corniceToken()`**: legge `?cornice=…` dalla query e lo rispecchia nei messaggi → la cornice accetta solo i messaggi del proprio iframe.
- **`sendHeight`**: attivo solo in iframe; ignora `height < 100`; soglia anti-rimbalzo `< 2px`; posta `{ type: "labvisivo:height", height, cornice? }` a `window.parent` con `"*"`.
- **Ping**: ascolta `{ type: "labvisivo:ping", cornice }` e risponde subito con `sendHeight` (la cornice v3 pinga ogni 3s e al resize della finestra).
- Trigger di rinvio: `load`, `resize`, `ResizeObserver` su `html` e `body`, `setTimeout` a 250/500/1500ms, `document.fonts.ready`.

## Barra di accessibilità (AccessibilityToolbar)

5 moduli: **FONT** (Riduci/Aumenta 80–160%), **INTERLINEA** (1.65–2.6), **RIGHELLO**, **MODALITÀ** (contrasto alto), **ASCOLTO** (TTS). Colori fissi stile Cornice Universale (rilevati da foto): barra `#fdfbf8` bordo `#dedbd6`, capsule `#f5f0e6` senza bordo, testo `#2e2118`, anello focus `#b71c1c` (solo da tastiera). Fix screen reader già applicati: icone lucide `aria-hidden`, capsule `role="group"` + `aria-label`, testo introduttivo `sr-only`, live region `role="status"` all'avvio (annuncio a 800ms), nome accessibile del pulsante ASCOLTO contiene la parola "Ascolto". La barra ha `mb-1 mt-2` (il 4px che contribuisce ai 24px sopra la card in embed).

## Cornice dinamica per Blogger (`cornice-dinamica/`)

| File | Uso |
|---|---|
| `embed-equazioni-secondo-grado-dedicata.html` | ⭐ **DA INCOLLARE NEL BLOG** (v3 impermeabile, ~15 KB). URL fisso dell'app. |
| `verifica-embed-produzione.html` | Copia identica + pannello di debug (consegnata all'utente per verifiche locali) |
| `test-impermeabile.html` / `test-dedicata.html` | Pagine di test multi-cornice / cornice singola |
| `embed-equazioni-secondo-grado-lite.html` | Versione leggera (~5 KB), riusabile cambiando `APP_URL` |
| `embed-equazioni-secondo-grado.html` | Autosufficiente (~124 KB, font in base64) |
| `embed-universale.html` | Template per altre app (segnaposto `APP_URL`/`APP_TITLE`) |
| `generate_embed.py`, `generate_test_impermeabile.py` | Rigeneratori |
| `README.md` | Documentazione completa della cartella |

Copie della versione dedicata esistono anche alla **root** del progetto (`embed.html`, `embed-blogger.html`).

### Caratteristiche v3 (mantenerle nei refactor)

- **Impermeabile**: ogni cornice è un'isola — trova i propri elementi via `document.currentScript`, rinomina gli id con un **token univoco** (`lf` + random, es. `lfIframe-xyz123`), accetta **solo** messaggi dal proprio iframe (`e.source`) e col proprio token. Il ping usa `"*"` come target ma il token filtra le risposte.
- **Header**: titolo e pulsanti **sulla stessa riga**, centrati (layout aggiornato rispetto al README che mostrava i pulsanti sotto).
- **Pulsanti**: Schermo intero (nascosto se non supportato) e Ricarica; **spinner** rispettoso di `prefers-reduced-motion`.
- **Stato**: `Caricamento…` → `App online — buon lavoro!` oppure errore `L'app non è raggiungibile. Controlla la connessione e riprova.` con pulsante **Riprova**; timeout errore **15s**; la scritta online sparisce dopo 3s.
- **Configurazione**: `var APP_URL = 'https://equazioni-secondo-grado.easy-peasy.site/';` (URL già verificato attivo con HTTP 200) — per riusare su un'altra app cambiare solo `APP_URL`/`APP_TITLE`.
- **Altezza**: iframe `src = APP_URL + '?cornice=' + token`; CSS iniziale 640px, **nessuna transizione CSS sull'altezza** (durante l'animazione l'app misurerebbe altezze intermedie → loop).
- **Anti-loop a 3 livelli**: (1) nessuna transizione CSS; (2) **debounce ~200ms** (applica solo a layout stabilizzato); (3) **clamp di sanità** (<100 o >15000 px ignorati) + crescita sospetta > 2× confermata dall'app entro 2s prima di essere applicata (una crescita divergente non viene mai confermata → iframe fermo).

### Come incollare su Blogger
1. Post → vista HTML → incollare tutto il contenuto di `embed-equazioni-secondo-grado-dedicata.html`.
2. Pubblicare. L'iframe si adatta da solo (desktop, tablet, mobile).

## VERIFICA EMBED e LIMITE COEP (lezione chiave della chat)

**Sintomo**: il test della cornice (pagina host su preview Easy-Peasy che incornicia la produzione `deploy-hook-eq2grado.easy-peasy.site`) mostrava l'icona "documento rotto" nell'iframe, nessun messaggio `labvisivo:height`, stato che passava a errore dopo 15s.

**Causa**: l'ambiente Easy-Peasy (sia preview sandbox sia produzione servita via proxy) invia l'header `Cross-Origin-Embedder-Policy: require-corp` su TUTTE le pagine. Un documento con COEP `require-corp` **blocca qualsiasi iframe cross-origine** la cui risposta non abbia `Cross-Origin-Resource-Policy: cross-origin`. Verificato con iframe di controllo: persino `example.com` non si carica dentro una pagina sandbox. **Non è un difetto della cornice né dell'app.**

**Conseguenza operativa**: DENTRO la sandbox si può verificare l'embed **solo same-origin** (pagina host e app sullo stesso dominio, es. `client/public/test-embed-sameorigin.html` che punta alla preview, oppure una pagina servita dalla produzione stessa). Su un blog vero (Blogger) il genitore NON ha COEP → l'iframe cross-origine carica normalmente. La produzione non invia `X-Frame-Options` né CSP `frame-ancestors` (verificato con `curl -sI`): è embeddabile.

- Per verificare "come su Blogger" **in locale**: consegnare/leggere `cornice-dinamica/verifica-embed-produzione.html` (cornice dedicata → produzione + pannello di debug con riga per riga: `msg height=…px`, `altezza IFRAME applicata = …px`, stato). L'utente la apre nel suo browser (niente COEP).
- Esito atteso same-origin (misurato): messaggi 452→487px, altezza applicata **487px**, stato "App online — buon lavoro!", margini simmetrici e compatti.
- Per il debug rapido: `client/public/test-embed-finale.html` (→ produzione) e `test-embed-sameorigin.html` (→ preview) serviti da Vite in `client/public/`.

## Server Express (`server/index.ts`) — regole header

- Serve i file statici da `dist/public` (produzione). In dev Vite non usa il server.
- **COOP/COEP `same-origin`/`require-corp` SOLO sui documenti `.html`** (servono a ONNX Runtime Web per `SharedArrayBuffer`). **MAI su font/asset**: altrimenti OpenDyslexic non si carica cross-origin dalle cornici embed su Blogger (ricadrebbe su un font serif).
- **CORS** `Access-Control-Allow-Origin: *` sulla route `/fonts` (per il font OpenDyslexic usato dalle cornici).
- MIME corretto per i `.wasm` (`application/wasm`).
- Fallback SPA: `app.get("*")` serve `index.html` (con COOP/COEP).
- Porta: `process.env.PORT || 3000`.

## PDF (QuadraticExercises)

`handleScaricaPdf` (~riga 681): forza `generatingPdf=true` (apre i NotebookGuide), dopo ~100ms apre `window.open('', '_blank')`, scrive HTML con CSS inline compatto (font OpenDyslexic + fallback Cambria Math per KaTeX), `print()`, poi resetta. Ogni sezione ha `page-break-inside:avoid`. Pulsante 📄 SCARICA PDF a ~riga 1030.

## Deploy

```bash
cd /home/user/equazioni-secondo-grado
pnpm check    # MAI saltare: gli errori TypeScript bloccano la build
webdev_deploy mode="preview" project_dir="/home/user/equazioni-secondo-grado"
# Produzione SOLO dopo conferma esplicita dell'utente in un nuovo messaggio:
webdev_save_checkpoint description="..." project_dir="/home/user/equazioni-secondo-grado"
webdev_deploy mode="production" project_dir="/home/user/equazioni-secondo-grado"
```

Produzione: `https://equazioni-secondo-grado.easy-peasy.site` (aggiorna `APP_URL` nelle cornici e `embed.html`/`embed-blogger.html` se cambia).

### VERIFICA POST-DEPLOY OBBLIGATORIA (lezione chiave della chat del 04/10/2026)

Dopo OGNI deploy in produzione, verificare SUBITO con `curl` (non fidarsi del messaggio "Successfully deployed", che può essere true anche quando l'app resta irraggiungibile):

```bash
for u in https://equazioni-secondo-grado.easy-peasy.site https://deploy-<id>.a.run.app; do
  curl -s -o /tmp/chk.html -w "HTTP %{http_code}\n" --max-time 15 "$u" && grep -io "<title>[^<]*</title>" /tmp/chk.html | head -1
done
```

Esiti osservati e loro significato:
- **HTTP 200 + titolo corretto** → deploy davvero pubblicato ✅ (atteso: dopo ~2 min dal deploy, verificare anche dopo 60s).
- **HTTP 404** sul dominio dedicato → dominio non configurato: il deploy è partito ma la piattaforma non ha associato il sottodominio.
- **HTTP 403** sull'URL `*.easy-peasy.site` e/o su Cloud Run → accesso pubblico bloccato dalla piattaforma.
- **403/404 PERSISTENTI non si risolvono con redeploy**: nella chat 4 deploy consecutivi (7433, 7434, …) sono andati a buon fine lato piattaforma restando irraggiungibili. È un problema lato piattaforma (accesso/dominio), l'unica strada è scrivere al supporto https://easy-peasy.ai/support citando il deploymentId — poi ritentare e riverificare con curl. NON continuare a fare deploy a ciclo infinito.
- Il `friendlyUrl` restituito dal deploy è la fonte di verità: al deploy 7445 la piattaforma ha assegnato `equazioni-secondo-grado.easy-peasy.site` (il dominio già incorporato nella cornice) e subito dopo è diventato raggiungibile senza modifiche alla cornice.

## Documentazione bundle (root del progetto)

`ACCESSIBILITA.md` (tutte le misure, portabili), `DEPLOY-RENDER.md` + `render.yaml` (trasferimento su Render via GitHub Blueprint), `GUIDA-IA.md` (ricostruzione/varianti: grado, disequazioni, fratte), `ISTRUZIONI-GITHUB.txt`, `docs/` (`grado.md`, `disequazioni.md`, `fratte.md`), `scripts/clone_app.py` + `remove_step6.py`, `template.json`, `GUIDA-UNICA.html`. Prima di rigenerare il pacchetto ZIP esportabile, leggere la skill `zip-esportabile-guide-ia` (pattern REBUILD/ADATTARE/RENDER/ACCESSIBILITA). Per il riconoscimento ONNX/ink-on e i canvas, l'architettura è condivisa con la sorgente: leggere la skill `equazioni-biquadratiche` (pipeline, `DIGIT_FIXES`, `renderKatex`, regole LaTeX) — le stesse regole valgono qui.

## BLOCCO CARICAMENTO MODELLO AI — patch ink-on numThreads=1 (lezione chiave della chat del 12/10/2026)

**Sintomo**: il pulsante resta per sempre su «CARICAMENTO…» disabilitato → l'utente non può MAI premere RICONOSCI dopo la scrittura a mano. La diagnosi iniziale («i modelli ONNX si caricano lentamente») è una PISTOLA FUMANTE da evitare: le risorse arrivano in ~1s; è la creazione della sessione a bloccarsi.

**Causa radicale (verificata con test diretti in console del browser)**: `ort.env.wasm.numThreads = navigator.hardwareConcurrency || 4` (top-level di `node_modules/ink-on/dist-lib/chunks/inference-4T2UM6yg.js`) fa usare i worker WebAssembly multi-thread; `ort.InferenceSession.create` NON SI RISOLVE MAI con i worker, in nessun ambiente. Con `numThreads=1` l'init riesce in **~2,2 s**.

**Metodo diagnostico riutilizzabile** (confermare PRIMA di patchare):
1. Verificare che le risorse arrivino: `performance.getEntriesByType('resource')` filtrate per onnx/wasm/vocab → tutte 200 e veloci = non è la rete.
2. Importare il chunk compilato e creare un'istanza con timeout:
   ```js
   const mod = await import('/assets/core-<HASH>.js');
   const eng = new mod.InferenceEngine({encoderUrl:'/models/comer/encoder_int8.onnx', decoderUrl:'/models/comer/decoder_int8.onnx', beamWidth:5, executionProvider:'wasm'});
   await Promise.race([eng.init(), new Promise((_,r)=>setTimeout(()=>r(new Error('TIMEOUT 20s')),20000))]);
   ```
   → TIMEOUT = sessione bloccata.
3. Ripetere con `Object.defineProperty(navigator,'hardwareConcurrency',{value:1,configurable:true})` + import con query-busting (`?v=1thread`) per rieseguire il top-level del modulo → INIT OK = conferma multi-thread.

**Fix applicato**:
1. **Patch pnpm permanente**: `pnpm patch ink-on` → in `dist-lib/chunks/inference-4T2UM6yg.js` sostituire l'assegnazione con `ort.env.wasm.numThreads = 1;` → `pnpm patch-commit`. Risultato: `patches/ink-on.patch` + `patchedDependencies: { "ink-on": "patches/ink-on.patch" }` in package.json. La patch DEVE essere presente in ogni pacchetto ZIP e committata su GitHub (senza di essa l'app ricostruita si blocca di nuovo).
2. **Rete di sicurezza in `client/src/hooks/useMathRecognition.ts`**: `await engine.init()` racchiuso in `Promise.race` con un rifiuto a **30s** → il catch esistente imposta `loadError` invece del «CARICAMENTO…» infinito.
3. **Messaggio fallback in `NumberInputCanvas.tsx`** (in `{!isLoading && loadError && …}`): «⚠️ Riconoscimento non disponibile — usa ✎ digita il valore / DIGITA L'EQUAZIONE» → l'utente non resta mai in stallo; usa `loadError` destrutturato da `useMathRecognition()`.

**Verifica** (fatta in preview E produzione, URL esercizio con query `?cognome=…&nome=…&data=…&classe=…`): il pulsante mostra RICONOSCI entro ~2–5 s invece di CARICAMENTO…; cliccando RICONOSCI dopo un tratto (anche un puntino) la pipeline parte e arriva alla fine (es. «NESSUNA ESPRESSIONE RICONOSCIUTA» per un tratto privo di significato = inferenza riuscita).

**Nota diagnostica UI per test sintetici**: il canvas MathDrawCanvas NON reagisce ai MouseEvent sintetici dispatchati sul DOM (React non li processa sempre). Chiamare DIRETTAMENTE gli handler React: `const p = canvas[Object.keys(canvas).find(k=>k.startsWith('__reactProps'))]` → `p.onMouseDown/onMouseMove/onMouseUp` con `{clientX, clientY, preventDefault(){}, button:0}` in coordinate client. RICONOSCI è `disabled = !hasContent || !isModelReady || isRecognizing`.

## TRASCRIZIONE SOLUZIONI — incomplete senza zero e semplificazione massima (in QuadraticExercises.tsx)

**Regola fissa dell'utente**: nelle equazioni INCOMPLETE PURE (b = 0) la trascrizione delle soluzioni NON deve mai mostrare zeri visibili (`−0 − √24`, `0 − √24` sono vietati: il numeratore è semplicemente `±√Δ`), e le soluzioni esatte fornite dall'utente vanno trascritte SEMPRE nella forma più semplificata possibile (es. `√24/6` → `2√6/6` → `√6/3`), perché è la forma che lo studente scrive a mano e l'app riconosce come CORRETTO.

Helper a livello modulo (in QuadraticExercises.tsx, dopo `formatDenomCoeff`):

| Funzione/Componente | Ruolo |
|---|---|
| `numeratoreRadiceQuadr(b, deltaLatex, op)` | Numeratore di `−b ± √Δ`: con b=0 restituisce solo `±\sqrt{Δ}` (niente `0`) |
| `estraiRadice(n)` | `Δ → {k, m}` con `√Δ = k√m` e m senza fattori quadrati (es. 24 → 2√6) |
| `radiceLatex(k, m)` | LaTeX di `k√m` (`2\sqrt{6}`, `\sqrt{6}`) |
| `frazioneRadiceLatex(raz, k, m, den)` | `(raz ± k√m)/den` con den>0; den=1 → senza frazione; raz=0 → segno FUORI dalla frazione (`-\dfrac{\sqrt{6}}{3}`) |
| `frazioneRadiceSemplice(b, a, deltaLatex, segno)` | Fallback quando `√Δ` è già irriducibile: `(−b ± √Δ)/(2a)` con denominatore reso positivo (flip dei segni se a<0) |
| `semplificaRadiceEsatta(b, a, delta, segno)` | Semplificazione massima di `(−b ± √Δ)/(2a)` con coefficienti interi: estrae i fattori quadrati da Δ e riduce la frazione per gcd. Ritorna `{latex, intermedio}` o `null` se nulla da semplificare (o coefficienti non interi) |
| `CatenaRadice(name, b, a, delta, segno, classe)` | Componente JSX per il ramo Δ non quadrato perfetto: riga sostituita (senza zero) → eventuale riga intermedia (`-\dfrac{2\sqrt{6}}{6}`) → riga finale in grassetto semplificata (`-\dfrac{\sqrt{6}}{3}`) |

Punti collegati da NON regredire:
- `x1ExactLatex`/`x2ExactLatex` nel `useMemo` di `computed`: ramo non quadrato perfetto = `semplificaRadiceEsatta(...)?.latex ?? frazioneRadiceSemplice(...)`. Sono le formule usate nelle soluzioni finali, nella verifica e nel PDF (`buildSolutionLine` legge `entry.radicalLatex`, che contiene ancora `sqrt` → il decimale `≈` resta). 
- **Δ = 0 con b = 0** (equazione `ax² = 0`): mostrare direttamente `x_{1} = x_{2} = 0` (header con `opacity-80` e NotebookGuide), niente `\frac{-0}{2·3}` né `\frac{0}{6}`.
- Passi x₁/x₂: formula sostituita via `numeratoreRadiceQuadr` (sia header `opacity-80` sia NotebookGuide); ramo quadrato perfetto: con b=0 il numeratore è solo `±numberToLatexAbs(√Δ)` senza `0 ±`.
- Test rapido della logica di semplificazione: `/home/user/test-semplifica.mjs` (replica JS pura di `estraiRadice`/`semplificaRadiceEsatta`, 8 casi con esiti attesi: `b=0 a=3 Δ=24 segno=-1 → -\dfrac{\sqrt{6}}{3}` con intermedio `-\dfrac{2\sqrt{6}}{6}`).

**Gotcha file_edit**: in QuadraticExercises.tsx alcune righe usano `\frac` e altre `\dfrac` nei template literal — se un find non trova corrispondenza, ispezionare i byte reali con `sed -n '<N>p' client/src/pages/QuadraticExercises.tsx | cat -A` prima di riprovare (le catene finali di CatenaRadice hanno sostituito le vecchie righe `\dfrac` del ramo non perfetto).

## Regole d'Oro

1. **MAI saltare `pnpm check`** prima del deploy.
2. **Dentro un iframe MAI `min-h-screen`/`100vh`**: l'altezza misurata dipenderebbe dall'altezza dell'iframe → loop di crescita infinita (visibile su mobile). Le classi `lf-embedded`/`lf-welcome-top` in index.css e heightSync in main.tsx gestiscono già tutto: NON introdurre centrature verticali o min-height sulla prima pagina.
3. **La misura dell'altezza deve saper RESTRINGERSI**: non usare `documentElement.scrollHeight` come valore assoluto (resta gonfiato al viewport dentro l'iframe). Usare la logica `misuraAltezza()` di main.tsx (max di body/offsetHeight + scrollHeight solo se > viewport).
4. **`lf-welcome-top` solo in vista autonoma** (WelcomePage, useEffect con cleanup); in embed NO (heightSync invia l'altezza reale).
5. **Margini embed prima pagina = 24px sopra / 24px sotto** (20px padding + 4px `mb-1` barra; `> div:first-child { padding-top: 0 }`).
6. **Canale postMessage condiviso**: `labvisivo:height` e `labvisivo:ping` — non cambiarli. Il token `?cornice=` deve essere rispecchiato.
7. **Nella cornice**: nessuna transizione CSS sull'altezza, debounce ~200ms, clamp 100–15000px, crescita > 2× richiede conferma entro 2s, filtra `e.source` + token.
8. **COOP/COEP solo sui `.html`** (server/index.ts), CORS su `/fonts`, mai COEP su font/asset.
9. **Test embed nella sandbox solo same-origin** (COEP del proxy blocca ogni iframe cross-origine senza CORP — non è un bug dell'app). Per il comportamento "Blogger reale": pagina di test locale (`verifica-embed-produzione.html`) o `curl -sI` per confermare assenza di X-Frame-Options/frame-ancestors.
10. Non toccare `QuadraticExercises.tsx` senza leggere prima la skill `equazioni-biquadratiche` (convenzioni condivise: `renderKatex`, NotebookGuide, PDF, formattazione numeri).
11. L'app è **grado 2 (k=1)**: niente sostituzione `t`, niente estrazione di radice. Per un altro grado usare `widget-matematico-sorgente`; per la sorgente biquadratica `equazioni-biquadratiche`.
12. **Dopo ogni deploy in produzione verificare con curl** (HTTP 200 + titolo): 404/403 persistenti = problema piattaforma, si risolve col supporto citando il deploymentId, NON con redeploy a ciclo infinito. Il `friendlyUrl` può cambiare tra i deploy: se cambia, aggiornare `APP_URL` in `cornice-dinamica/embed-equazioni-secondo-grado-dedicata.html`, `embed.html`, `embed-blogger.html` e nel DOCX dei codici embed.
13. **Equazioni incomplete (b=0): MAI zeri visibili nelle soluzioni** e sempre la forma esatta più semplificata (`semplificaRadiceEsatta` → catena `CatenaRadice`). La forma semplificata deve coincidere con quella che lo studente scrive a mano e l'app accetta come CORRETTO.
