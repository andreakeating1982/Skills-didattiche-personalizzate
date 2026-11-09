# Archivio di dettaglio — math-input-panel

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/frazioni.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- File chiave
- Funzioni matematiche (in FractionExercises.tsx, righe ~7-70)
- Computed values (useMemo)
- `addSubComputed` (~riga 115): Addizione/Sottrazione
- `mulDivComputed` (~riga 200): Moltiplicazione/Divisione
- State principale
- Struttura NotebookGuide
- Sezione MOLTIPLICAZIONE/DIVISIONE
- RICOPIA SUL QUADERNO — stile penna su carta
- Allineamento
- Barrature
- Frazioni nella RICOPIA
- PDF (`handleScaricaPdf`, ~riga 455)
- Regole CSS di stampa obbligatorie
- Embed Blogger
- Convenzioni di stile
- Regola colori label
- Task comuni
- Modificare testo o placeholder
- Cambiare stili PDF
- Aggiungere classi Tailwind al PDF
- Deploy
- Modificare l'embed
- Script e template
- Fix frequenti e note
- Segni × non allineati
- PDF illeggibile
- Frazioni mancanti nella prima RICOPIA

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Math Input Panel — Operazioni con le Frazioni

App didattica interattiva per esercizi di frazioni (addizione, sottrazione, moltiplicazione, divisione). Lo studente scrive le frazioni a mano libera, segue passi guidati con feedback immediato, e scarica il quaderno in PDF.

- **Preview**: `https://3000-ioyi3yqr545m02kt02dpl.sandbox.easy-peasy.ai/`
- **Produzione**: `https://math-input-panel.easy-peasy.site`
- **Project root**: `/home/user/math-input-panel`
- **Scaffold**: `web-static` (no DB, no auth, solo client React + server Express minimale)

## File chiave

| File | Ruolo |
|---|---|
| `client/src/pages/FractionExercises.tsx` | **Componente principale** (~2178 righe). Tutta la logica: state, computed values, render, NotebookGuide, PDF, RICOPIA SUL QUADERNO. |
| `client/src/components/FractionDisplay.tsx` | Renderizza una frazione (numeratore, barra, denominatore) con taglie xs/sm/md/lg |
| `client/src/components/NumberInputCanvas.tsx` | Canvas per scrittura a mano, riconoscimento ONNX (modelli in `client/public/models/comer/`) |
| `client/src/components/MathDrawCanvas.tsx` | Canvas alternativo per input matematico |
| `client/src/index.css` | Tema globale, colori, font |
| `embed.html` | Codice embed per Blogger con iframe auto-ridimensionante |
| `server/index.ts` | Server Express di produzione |

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

La seconda RICOPIA (semplificazione incrociata) segue queste regole di design:

### Allineamento
- Contenitore flex: `items-center gap-3 sm:gap-4` (NON `items-end`)
- I segni `×` sono semplici `<span>` senza offset — con `items-center` si allineano naturalmente alla linea di frazione
- **NON** usare `mb-[Xpx]` o `-mb-1` sui segni × — sono fragili e si rompono con frazioni di diversa altezza

### Barrature
- SVG `<svg className="absolute inset-0 pointer-events-none">` con linee diagonali `stroke="#000" strokeWidth="2.5"`
- Una linea da top-left a bottom-right dell'area del numero
- I nuovi valori (semplificati) sono in `text-[12px]` posizionati SOPRA (numeratore) e SOTTO (denominatore) i valori originali barrati
- Stile monocromatico: `#000000` su sfondo bianco, SENZA box colorati

### Frazioni nella RICOPIA
- Ogni frazione usa struttura: `<span className="relative inline-flex flex-col items-center">`
- Numeratore/denominatore: `text-[22px] font-bold font-serif text-black`
- Linea frazione: `<div className="w-10 h-[2px] bg-black my-0.5" />`
- Le annotazioni (valori semplificati sopra/sotto) usano `text-[12px] leading-none text-muted-foreground`
- **NON** mostrare `=` e risultato finale — solo le frazioni con i × tra loro

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

## Embed Blogger

Il file `embed.html` (nella root) contiene il wrapper pronto. L'iframe si auto-ridimensiona via `postMessage`:
- L'app invia `{ type: 'labvisivo:height', height }` al genitore
- `ResizeObserver` + `MutationObserver` su `document.body` monitorano i cambi di altezza
- Per aggiornare l'URL nell'embed, cambiare `src` nell'iframe

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

### Modificare l'embed
Il template è in `/home/user/skills/didattica-app-matematica/templates/math-input-panel/embed.html`. Cambiare l'URL dell'iframe se il dominio produzione cambia.

## Script e template

- `embed.html` — Codice embed per Blogger nella root, da incollare in modalità HTML
- `post-blog.html` — Versione alternativa dell'embed
- `scripts/` e `references/` — non utilizzati; mantenuti vuoti per espansioni future

## Fix frequenti e note

### Segni × non allineati
Verificare che il contenitore flex usi `items-center` e NON `items-end` + `mb-[Xpx]`. I segni × devono essere `<span>` semplici senza offset di margine.

### PDF illeggibile
Verificare che `stylesHtml` copi correttamente i fogli di stile. In produzione, il CSS compilato è in un `<link>`; in dev Vite, è in `<style>`.

### Frazioni mancanti nella prima RICOPIA
Verificare che il blocco di inversione iteri su TUTTE le frazioni (non solo le prime due). La regola è: prima frazione invariata, tutte le altre invertite.

### `dDen2S` non mostra il valore corretto
`dDen2S` deve includere `den2IntS` (il denominatore invertito), non solo `num2IntS`.

### Card "1. Moltiplicazione e inversione" troppo stretta
La card NON deve avere `max-w-md mx-auto`. Deve usare la stessa struttura senza vincolo della card 2 (`p-4 rounded-xl bg-card/40 border border-border space-y-6 leading-loose`).
