---
name: math-input-panel
description: "Manutenzione e personalizzazione dell'app Operazioni con le Frazioni (Vite + React + TypeScript + Tailwind, scaffold web-static). Usare per: modificare la UI, personalizzare i passi guidati, modificare la generazione PDF, gestire/aggiornare la cornice dinamica per Blogger (protocollo labvisivo:height, token v3, anti-loop), modificare i margini e il layout della prima pagina (WelcomePage, classi lf-welcome-top/lf-embedded, heightSync.ts), deploy preview/produzione, modificare stili e font, arrotondamento decimali, aggiornare la documentazione (ACCESSIBILITA.md, DEPLOY-RENDER.md, GUIDA-IA.md, render.yaml, README.md) e rigenerare il pacchetto ZIP esportabile per ricostruzione via GitHub/Render. L'app guida lo studente passo-passo in addizione/sottrazione e moltiplicazione/divisione tra frazioni con input a scrittura a mano (ONNX) e quaderno PDF scaricabile."
---

# Math Input Panel — Operazioni con le Frazioni

App didattica interattiva per esercizi di frazioni (addizione, sottrazione, moltiplicazione, divisione). Lo studente scrive le frazioni a mano libera, segue passi guidati con feedback immediato, e scarica il quaderno in PDF.

- **Preview**: `https://3000-ioyi3yqr545m02kt02dpl.sandbox.easy-peasy.ai/`
- **Produzione**: `https://math-input-panel.easy-peasy.site`
- **Project root**: `/home/user/math-input-panel`
- **Scaffold**: `web-static` (no DB, no auth, solo client React + server Express minimale)
- **Repo di riferimento (benchmark layout/documentazione)**: `/home/user/ref-latino-facile` (LATINO FACILE) e `/home/user/ref-biquadratiche`

## Principio fondamentale (INCLUSIVITÀ)

**L'app NON deve essere modificata togliendo qualcosa.** Ogni modifica deve AGGIUNGERE gli elementi che la rendono più inclusiva (font OpenDyslexic, TTS, contrasto alto, righello di lettura, riduzione movimento, ecc.). Non rimuovere mai funzionalità o misure di accessibilità esistenti.

## File chiave

| File | Ruolo |
|---|---|
| `client/src/pages/FractionExercises.tsx` | **Componente principale** (~2178 righe). Tutta la logica: state, computed values, render, NotebookGuide, PDF, RICOPIA SUL QUADERNO. |
| `client/src/pages/WelcomePage.tsx` | **Prima pagina** (card di ingresso: nome/cognome, modalità). Layout compatto, classe `lf-welcome-top`. |
| `client/src/components/FractionDisplay.tsx` | Renderizza una frazione (numeratore, barra, denominatore) con taglie xs/sm/md/lg. Quando `den === 1` mostra il solo numero intero: DEVE avere `justify-center` per centrarlo (vedi "Fix frequenti"). |
| `client/src/components/NumberInputCanvas.tsx` | Canvas per scrittura a mano, riconoscimento ONNX (modelli in `client/public/models/comer/`) |
| `client/src/components/MathDrawCanvas.tsx` | Canvas alternativo per input matematico |
| `client/src/lib/heightSync.ts` | **Sincronizzazione altezza iframe** (protocollo `labvisivo:height`). Inizializzato da `main.tsx`. |
| `client/src/main.tsx` | Chiama `initHeightSync()` prima del render (riga 10). |
| `client/src/index.css` | Tema globale, colori, font, regole `lf-embedded`/`lf-welcome-top`. |
| `cornice-dinamica/` | **4 versioni embed per Blogger** + test + font OpenDyslexic (vedi sezione dedicata). |
| `server/index.ts` | Server Express di produzione |
| `ACCESSIBILITA.md` / `DEPLOY-RENDER.md` / `GUIDA-IA.md` / `README.md` / `render.yaml` / `ISTRUZIONI-GITHUB.txt` | Documentazione per IA, accessibilità e deploy su Render (vedi sezione "Pacchetto ZIP"). |

## Funzioni matematiche (in FractionExercises.tsx, righe ~7-70)

- `gcd(a, b)` — massimo comune divisore (Euclide ricorsivo)
- `lcm(a, b)` — minimo comune multiplo, output già arrotondato via `round2()`
- `semplificaFrazione(num, den)` — restituisce `{ num, den }` semplificati
- `fattorizzazionePrimi(n)` — restituisce `Record<numero, esponente>` per la scomposizione
- `formatFattori(n, fattori)` — formatta la scomposizione come stringa leggibile
- `round2(n)` — arrotonda a 2 decimali: `Math.round(n * 100) / 100`

## Computed values (useMemo)

### `addSubComputed` (~riga 115): Addizione/Sottrazione
Campi: `mcmCorretto`, `fattori1`, `fattori2`, `mcmFormula`, `val1Corretto`, `val2Corretto`, `numFinaleRaw`, `denFinaleRaw`, `numFinaleCorretto`, `denFinaleCorretto`

### `mulDivComputed` (~riga 200): Moltiplicazione/Divisione
Campi: `actualNum2`, `actualDen2`, `displayNum2`, `displayDen2`, `dNum2S`, `dDen2S`, `divCom1`, `divCom2`, `numFinaleRaw`, `denFinaleRaw`, `numFinaleCorretto`, `denFinaleCorretto`, `fattori1-4`, `mcd1-6`, `nd1-4`.

**Regola divisione**: nella divisione si invertono TUTTE le frazioni eccetto la prima (non solo la seconda).

Tutti i valori sono già arrotondati a 2 decimali via `round2()`.

## State principale

- `mode`: `"addsub"` | `"muldiv"`
- Input frazioni: `num1`, `den1`, `num2`, `den2` (number | null)
- Risposte studente: `mcmUtente`, `risultato1Utente`, `risultato2Utente`, `risultatoFinaleUtente`, `numeratoreFinaleUtente`, `denominatoreFinaleUtente`
- Semplificazione incrociata: `num1Semplificato`, `den2Semplificato`, `den1Semplificato`, `num2Semplificato`
- `generatingPdf`: boolean per forzare l'apertura di tutti i NotebookGuide durante la generazione PDF

## Struttura NotebookGuide

Sezioni con `forceOpen={generatingPdf}` per il PDF. Ogni NotebookGuide ha `className="notebook-content"` — la funzione `handleScaricaPdf` raccoglie tutti i `.notebook-content` dal DOM.

### Sezione MOLTIPLICAZIONE/DIVISIONE

Contenitore: `<div className="space-y-5 max-w-2xl mx-auto">`

1. **Card "1. Moltiplicazione e inversione"** — `<div className="p-4 rounded-xl bg-card/40 border border-border space-y-6 leading-loose">` — **SENZA `max-w-md`** (allargata per combaciare con le altre card)
2. **Card "2. SEMPLIFICAZIONE TRA FRAZIONI"** — stessa struttura, senza vincolo di larghezza
3. **Prima RICOPIA SUL QUADERNO**: mostra TUTTE le frazioni (incluse 3ª e 4ª) nel passaggio di inversione
4. **Seconda RICOPIA SUL QUADERNO**: semplificazione incrociata in stile penna su carta

## RICOPIA SUL QUADERNO — stile penna su carta

La seconda RICOPIA (semplificazione incrociata) segue queste regole di design.

### Allineamento (CRITICO: barre tutte sulla stessa riga)
- Contenitore flex: `flex justify-center items-center gap-3 sm:gap-4 my-2 flex-wrap font-serif text-center` (NON `items-end`).
- Ogni frazione è `<div className="flex flex-col items-center py-4">`: il `py-4` (padding verticale simmetrico) riserva spazio alle annotazioni SENZA spostare la barra.
- I segni `×` sono `<span className="text-[22px] font-bold">×</span>` semplici, senza offset: con `items-center` si allineano naturalmente alla linea di frazione.
- **NON** usare `mb-[Xpx]`/`-mb-1` sui segni ×.

### Annotazioni semplificate (valori grigi sopra/sotto) — REGOLA FONDAMENTALE
I valori semplificati DEVONO essere posizionati **in modo assoluto**, NON in-flow. In-flow (sibling nel flex-col) → la frazione si allunga e la barra si disallinea rispetto alle altre.
- Numeratore: annotazione INSERITA dentro lo `relative inline-block`, con classe `absolute -top-4 left-1/2 -translate-x-1/2 text-[12px] leading-none text-muted-foreground`.
- Denominatore: stessa cosa con `-bottom-4` (al posto di `-top-4`).
- Numeri: `text-[22px] leading-none` (il `leading-none` evita lo scarto di line-height e rende l'altezza esatta).
- Distanza: `-top-4`/`-bottom-4` (16px) dà ~4px di distacco dal numero colorato. NON usare `-top-3`/`-bottom-3` (attaccati).

### Barrature
- SVG `<svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 100 100" preserveAspectRatio="none">` con `<line x1="4" y1="94" x2="96" y2="6" stroke="#dc2626" strokeWidth="3" strokeLinecap="round" opacity="0.8"/>` (diagonale rossa bottom-left → top-right).
- La barra copre solo il numero (`inset-0` sull'inline-block), NON l'annotazione.

### Frazioni nella RICOPIA
- Struttura numeratore/denominatore: `<span className="relative inline-flex flex-col items-center"><span className="relative inline-block">…</span></span>`.
- Numeratore/denominatore: `text-[22px] leading-none font-bold font-serif` con colori per frazione:
  - Frazione 1: num `text-orange-600`, den `text-sky-600`
  - Frazione 2: num `text-red-500`, den `text-blue-500`
  - Frazione 3: num `text-green-600`, den `text-teal-600`
  - Frazione 4: num `text-purple-600`, den `text-pink-600`
- Linea frazione: `<div className="w-10 h-[2px] bg-black my-0.5" />`.
- **NON** mostrare `=` e risultato finale — solo le frazioni con i × tra loro.

## PDF (`handleScaricaPdf`, ~riga 455)

**⚠️ IMPORTANTE**: il PDF NON mantiene più un CSS manuale. Ora copia automaticamente TUTTI i fogli di stile dalla pagina corrente:

```typescript
// Copia TUTTI i fogli di stile dalla pagina corrente
let stylesHtml = '';
document.querySelectorAll('link[rel="stylesheet"]').forEach((link) => {
  stylesHtml += link.outerHTML;
});
document.querySelectorAll('style').forEach((style) => {
  const text = style.textContent || '';
  // Salta gli style di Vite HMR e quelli troppo grandi
  if (text.includes('__vite') || text.length > 200000) return;
  stylesHtml += `<style>${text}</style>`;
});
```

Questo risolve il problema storico del PDF illeggibile: tutte le classi Tailwind (colori, flex, grid, dimensioni arbitrarie, SVG) funzionano automaticamente.

### Regole CSS di stampa obbligatorie

Il CSS inline nel `printHtml` DEVE contenere queste regole:
- `*,*::before,*::after{font-family:'Cambria Math',Cambria,serif!important}` — forza il font matematico
- `body,body *,p,span,div,h1-h6,...{font-size:12pt!important;line-height:1.55!important}` — tutto a 12pt
- `@media print{body{padding:0!important;-webkit-print-color-adjust:exact!important;...}@page{size:A4;margin:2.5cm 2cm 2cm 2cm}}` — layout A4

Se il PDF appare illeggibile → verificare che `stylesHtml` catturi effettivamente i fogli di stile (in Vite dev, Tailwind è iniettato via `<style>`).

## Cornice dinamica (embed per Blogger)

La cartella `cornice-dinamica/` contiene l'embed **aggiornato** per Blogger. Il vecchio `embed.html`/`post-blog.html` in root sono superati: usa sempre la versione dedicata qui sotto.

| File | Uso |
|---|---|
| `cornice-dinamica/embed-frazioni-dedicata.html` | ⭐ **Consigliata** (~19 KB, v3 impermeabile + anti-loop). Serve SOLO questa app (URL fisso). Da incollare nella vista HTML del post. |
| `cornice-dinamica/embed-frazioni-lite.html` | Versione leggera (~5 KB), riutilizzabile (basta cambiare `APP_URL`, oppure `?app=URL` nella pagina). |
| `cornice-dinamica/embed-universale.html` | Template universale per altre app (URL segnaposto). |
| `cornice-dinamica/embed-frazioni.html` | Autosufficiente (~110 KB), font incorporati in base64 (funziona anche offline). |
| `cornice-dinamica/test-dedicata.html` / `test-impermeabile.html` | Pagine di test locale (simulano il blog, anche con 2 cornici + una "estranea"). |
| `cornice-dinamica/generate_embed.py` / `generate_test_impermeabile.py` | Script che rigenerano la versione base64 e il test impermeabile. |
| `cornice-dinamica/fonts/` | OpenDyslexic Regular/Bold `.woff2` serviti dall'app via CORS. |

### Protocollo di sincronizzazione altezza (`labvisivo:height`)

- `heightSync.ts` (inizializzato in `main.tsx` via `initHeightSync()`) aggiunge la classe `lf-embedded` su `<html>` quando `window.self !== window.top`.
- L'app misura la propria altezza e invia al genitore: `{ type: "labvisivo:height", height, cornice?: token }`.
- La cornice risponde al `ping` con `{ type: "labvisivo:ping", cornice: token }`.
- Il token `?cornice=<token>` viene passato dalla cornice nell'URL dell'iframe e rispecchiato nei messaggi → ogni istanza è un'isola (filtro `e.source === iframe.contentWindow` + filtro token).

### Impermeabilità + anti-loop (v3)

La cornice dedicata è "impermeabile" (id univoci con token, scoping DOM via `document.currentScript`, filtro `e.source`) e "anti-loop su mobile" (nessuna transizione CSS sull'altezza, debounce ~200 ms, clamp 100–15000 px, conferma dei salti sospetti > 2×, congelamento 5 s dopo 3 crescite consecutive). **NON** reintrodurre transizioni CSS su `.lf-iframe` e non rimuovere il debounce: causano il bug "l'app si allunga a dismisura".

## Prima pagina (WelcomePage) e margini

La prima pagina usa il **layout compatto di LATINO FACILE** (benchmark `/home/user/ref-latino-facile`). Struttura:

```jsx
<main className="lf-welcome flex flex-col items-center bg-background px-4 pb-8 sm:pb-12">
  <div className="flex w-full flex-col items-center pt-4 sm:pt-8">   {/* inner wrapper */}
    <div className="bg-[#FAF8F5] border ... rounded-[20px] p-5 md:p-6 w-full max-w-[400px] ...">
      {/* card */}
    </div>
  </div>
</main>
```

**NON** usare `min-h-[calc(100dvh-…)]` + `items-center justify-center` (causa il grande vuoto sopra la card).

### Regole CSS in `index.css`

1. **Dentro l'iframe** (`lf-embedded`): margini simmetrici 24px sopra/sotto.
   ```css
   html.lf-embedded .lf-welcome {
     min-height: 0 !important;
     justify-content: flex-start;
     padding-top: 20px;      /* + 4px (mb-1 barra) = 24px sopra */
     padding-bottom: 24px;
   }
   html.lf-embedded .lf-welcome > div:first-child {
     padding-top: 0 !important;   /* azzera pt-4 sm:pt-8 dell'inner wrapper */
   }
   ```
2. **Vista autonoma** (`lf-welcome-top`, messa su `<html>` da WelcomePage quando `window.self === window.top`): body bianco + dissolvenza crema→bianco sotto la card.
   ```css
   html.lf-welcome-top body { background-color: #ffffff; }
   html.lf-welcome-top .lf-welcome { position: relative; }
   html.lf-welcome-top .lf-welcome::after {
     content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 48px;
     background: linear-gradient(to bottom, rgba(248, 241, 228, 0), #ffffff);
     pointer-events: none;
   }
   ```

### Fix critico di `heightSync.ts` (`currentHeight`)

**NON** usare `documentElement.scrollHeight` come riferimento assoluto: quando il contenuto è più corto dell'iframe, resta gonfiato all'altezza del viewport e la cornice non si restringe MAI. Usare invece l'altezza reale del contenuto e aggiungere lo scrollHeight solo se supera il viewport:

```typescript
function currentHeight(): number {
  const docEl = document.documentElement;
  const body = document.body;
  const viewportH = window.innerHeight || (docEl ? docEl.clientHeight : 0);
  let h = Math.max(
    body ? body.scrollHeight : 0,
    body ? body.offsetHeight : 0,
    docEl ? docEl.offsetHeight : 0
  );
  if (docEl && docEl.scrollHeight > viewportH) {
    h = Math.max(h, docEl.scrollHeight);
  }
  return h;
}
```

La WelcomePage **non** ha più un `useEffect` di auto-resize `postMessage` proprio (era ridondante): l'altezza è gestita centralmente da `heightSync.ts`.

## Pacchetto ZIP esportabile e documentazione

L'app è esportabile in un pacchetto ZIP per **ricostruzione da GitHub** e **deploy su Render**:

- **ZIP**: `/home/user/app-math-input-panel.zip` (rigenerare dopo ogni modifica al codice o alla documentazione con `zip -r`).
- **`AGENTS.md`** — istruzioni rapide per agenti IA (Copilot/Claude/MARKY), lette automaticamente quando l'IA apre il repository: comandi, file critici, regole anti-regressione.
- **`README.md`** — guida al progetto e istruzioni di build/deploy.
- **`ACCESSIBILITA.md`** — sezione ACCESSIBILITÀ in evidenza: OpenDyslexic, barra accessibilità, contrasto alto (`lf-hc`), righello di lettura, TTS (`useReadAloud`), riduzione movimento. Da riusare su altre app della famiglia.
- **`DEPLOY-RENDER.md`** — trasferimento da Easy-Peasy AI a Render via GitHub (build/deploy).
- **`GUIDA-IA.md`** — istruzioni per un agente IA per ricostruire l'app identica dal repository e creare varianti.
- **`render.yaml`** — configurazione Render (blueprint).
- **`ISTRUZIONI-GITHUB.txt`** — istruzioni rapide per il trasferimento.

### Rigenerare il pacchetto ZIP
```bash
cd /home/user && rm -f app-math-input-panel.zip && \
zip -r app-math-input-panel.zip math-input-panel \
  -x "math-input-panel/node_modules/*" "math-input-panel/.git/*" "math-input-panel/dist/*" "math-input-panel/dev-server.log"
```

## Convenzioni di stile

- **Tema chiaro**: sfondo `bg-background` con `paper-grain`, header centrato
- **Font**: Cambria Math per PDF e RICOPIA, Georgia/serif per frazioni a schermo, sistema per UI
- **Proporzioni compatte**: main `max-w-2xl` (672px) per la sezione MOLTIPLICAZIONE/DIVISIONE, canvas bassi, spaziature ridotte
- **Pulsanti modalità**: simboli in alto (`flex-col`), testo sotto — "+ / −" sopra "ADDIZIONE E SOTTRAZIONE", "× / ÷" sopra "MOLTIPLICAZIONE E DIVISIONE"
- **Footer**: `border-t border-border/60 py-4 text-center text-xs text-muted-foreground` — "Realizzato da Andrea Centinaro"
- **PDF**: tutto Cambria Math 12pt forzato via `!important`, fogli di stile copiati automaticamente dalla pagina, colori preservati via `-webkit-print-color-adjust:exact`
- **Bottoni**: `SCARICA PDF` in fondo alla pagina
- **NESSUNA SEMPLIFICAZIONE**: testo `text-primary` non in grassetto

### Regola colori label

**REGOLA FONDAMENTALE**: Label NUMERATORE/DENOMINATORE sono marroni (`text-amber-900`) senza grassetto in tutta l'app, **ECCETTO** nella sezione Moltiplicazione e Divisione dove mantengono colore e grassetto.

Il `NumberInputCanvas` ha classe base `text-base tracking-widest text-amber-900` (marrone, no grassetto). Le label nella sezione MulDiv sovrascrivono con `colorClass` specifici.

| Label | Sezione | `colorClass` |
|---|---|---|
| **NUMERATORE** / **DENOMINATORE** | AddSub | (nessuno — eredita `text-amber-900`) |
| **NUMERATORE** / **DENOMINATORE** | MulDiv finale | `text-orange-400 font-bold` / `text-blue-400 font-bold` |
| **Numeratore arancione** | MulDiv sempl. 1 | `text-orange-400 font-bold` |
| **Denominatore blu** | MulDiv sempl. 1 | `text-blue-400 font-bold` |
| **Denominatore azzurro** | MulDiv sempl. 2 | `text-sky-400 font-bold` |
| **Numeratore rosso** | MulDiv sempl. 2 | `text-red-400 font-bold` |
| Inline span `NUMERATORE (x)` | MulDiv sempl. 1 | `text-orange-400 font-bold` |
| Inline span `DENOMINATORE (y)` | MulDiv sempl. 1 | `text-blue-400 font-bold` |
| Inline span `DENOMINATORE (x)` | MulDiv sempl. 2 | `text-sky-400 font-bold` |
| Inline span `NUMERATORE (y)` | MulDiv sempl. 2 | `text-red-400 font-bold` |
| **DENOMINATORE 1ª/2ª FRAZIONE:** | AddSub m.c.m. | `text-amber-900` (inline, non canvas) |

## Task comuni

### Modificare testo o placeholder
Cercare in `FractionExercises.tsx` le stringhe italiane. I placeholder degli input canvas sono nel JSX.

### Cambiare stili PDF
Modificare il CSS inline dentro `printHtml` in `handleScaricaPdf` (~riga 275-345).

### Aggiungere classi Tailwind al PDF
Aggiungerle nel CSS inline di `printHtml`. Le classi con caratteri speciali vanno escape: `h-[2px]` → `.h-\\[2px\\]`.

### Deploy
```bash
webdev_deploy mode="preview"  # test
webdev_deploy mode="production"  # produzione
```

Prima del deploy in produzione, fare sempre un checkpoint con `webdev_save_checkpoint`.

### Aggiornare la cornice dinamica
La cornice consigliata è `cornice-dinamica/embed-frazioni-dedicata.html`. Se cambia il dominio di produzione, cambiare `APP_URL` nella sezione `⚙️ CONFIGURAZIONE`. Per una cornice riutilizzabile per un'altra app, partire da `embed-frazioni-lite.html` o `embed-universale.html`.

### Modificare i margini della prima pagina
Intervenire su `WelcomePage.tsx` (struttura/layout) e sulle regole `lf-embedded`/`lf-welcome-top` in `index.css`. NON toccare la logica di misura in `heightSync.ts` senza necessità: il `currentHeight` corretto è quello che evita lo scrollHeight del documento come riferimento assoluto.

## Script e template

- `cornice-dinamica/embed-frazioni-dedicata.html` — ⭐ embed consigliato per Blogger (vista HTML del post)
- `cornice-dinamica/embed-frazioni-lite.html` / `embed-universale.html` / `embed-frazioni.html` — varianti embed
- `cornice-dinamica/generate_embed.py` / `generate_test_impermeabile.py` — script di rigenerazione
- `embed.html` / `post-blog.html` (root) — embed storici, SUPERSEDUTI dalla cornice dinamica
- `templates/embed.html` — copia dell'embed nella skill

## Fix frequenti e note

### Segni × non allineati
Verificare che il contenitore flex usi `items-center` e NON `items-end` + `mb-[Xpx]`. I segni × devono essere `<span>` semplici senza offset di margine.

### Linee di frazione non allineate nella RICOPIA (barre su livelli diversi)
Causa: le annotazioni semplificate sono renderizzate IN-FLOW (sibling nel flex-col) → la frazione con annotazione diventa più alta e la sua barra si sposta rispetto alle altre. Fix: annotazioni `absolute` dentro lo `relative inline-block` (`-top-4` numeratore / `-bottom-4` denominatore) + `leading-none` sui numeri + `py-4` sulla colonna frazione (vedi "RICOPIA SUL QUADERNO").

### Numeri grigi semplificati troppo attaccati ai numeri colorati
Aumentare l'offset delle annotazioni a `-top-4`/`-bottom-4` (16px) con `py-4` sul contenitore. NON usare `-top-3`/`-bottom-3` (distanza quasi nulla).

### Risultato intero non centrato (es. "2" nella casella grigia di Moltiplicazione finale)
Nel caso `den === 1` di `FractionDisplay.tsx` il numero intero resta a SINISTRA dentro `min-w-[72px]` perché `inline-flex items-center` (riga) centra solo in verticale. Fix: aggiungere `justify-center` → `inline-flex items-center justify-center align-middle mx-1`.

### PDF illeggibile
Verificare che `stylesHtml` copi correttamente i fogli di stile. In produzione, il CSS compilato è in un `<link>`; in dev Vite, è in `<style>`.

### Frazioni mancanti nella prima RICOPIA
Verificare che il blocco di inversione iteri su TUTTE le frazioni (non solo le prime due). La regola è: prima frazione invariata, tutte le altre invertite.

### `dDen2S` non mostra il valore corretto
`dDen2S` deve includere `den2IntS` (il denominatore invertito), non solo `num2IntS`.

### Card "1. Moltiplicazione e inversione" troppo stretta
La card NON deve avere `max-w-md mx-auto`. Deve usare la stessa struttura senza vincolo della card 2 (`p-4 rounded-xl bg-card/40 border border-border space-y-6 leading-loose`).

### Grande vuoto sopra/sotto la card della prima pagina (margini non pareggiati)
Causa tipica: `min-h-[calc(100dvh-…)]` + `items-center justify-center` nel `<main>` della WelcomePage, oppure `currentHeight()` che usa `documentElement.scrollHeight` come riferimento assoluto (gonfia l'altezza). Ripristinare il layout compatto (inner wrapper + `pt-4 sm:pt-8`) e il `currentHeight` con `viewportH` (vedi sezione "Prima pagina").
