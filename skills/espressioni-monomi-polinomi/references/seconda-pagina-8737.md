# Cronologia seconda pagina — produzioni8737/8742/8744

**Superata per il layout corrente:** la produzione8756 usa pagina2 a640px
più pagina3 adattiva fino a640px. Leggere prima
[layout-compatto-8756.md](layout-compatto-8756.md). Conservare le sezioni
sotto per la storia di cropper, header e overflow; non riportare il runtime
ai limiti820/720 né dichiarare ancora «terza pagina invariata».


## Stato storico verificato e perimetro

- App corrente: `/home/user/espressioni-monomi-polinomi`, WIDGET METACOGNITIVO.
- Produzione autorizzata e verificata: **8744**, 28/10/2026 (overflow pezzi
  e didascalia finale; 8742 resta valido per header e 8737 per scrollbar).
- Commit funzionale pubblicato: `a90d5972c9f46adbfbc24f994f30ab4e976f7957`.
- Client JS: `index-BnuQEBUp.js`, SHA-256
  `c68d11243554e58fb2c21bff0e3d7dd50f8948c7aba9f4e53be448636e2262db`.
- CSS: `index-D1FTbNg8.css`, SHA-256
  `7699ceeb6be69e7f4524154b148e17564845da855e682538beabd96be09ebe43`.

**Nota propagazione:** subito dopo il deploy 8744 il sito serviva ancora
gli asset vecchi; ricontrollare dopo attesa prima di dichiarare riuscita la
verifica online.
- Pubblico: https://espressioni-monomi-polinomi.easy-peasy.site

Usare questo riferimento PRIMA delle note 8736 per layout, heightSync,
collaudo e ZIP. Il nucleo del cropper 8731 resta invariato: leggere anche
`photo-crop-8736.md`. Non ridistribuire per aggiornare soltanto ZIP/skill.

## Richiesta e implementazione da preservare

L'utente chiama «sidebar» la **scrollbar nativa** sottile di Latino Facile,
NON un menu. Riferimento repository Applicazione-Latino-Facile `39f503c`:
4px, marrone rgba(139,92,62,.2), hover .35. Il limite generale della pagina
è un'aggiunta del widget richiesta dall'utente, non presente in quel clone.

- SOLO `/espressione` (pagina 2): `App.tsx` applica `expr-input-frame`;
  toolbar esterna allo scroll, contenuto in `.expr-input-page`.
- Autonoma: max 820px desktop /720px larghezza <640px, mai oltre il viewport
  visibile. `--expr-visible-height` segue `visualViewport`/resize SOLO fuori
  dall'iframe e viene rimossa uscendo dalla pagina.
- Iframe: altezza 820/720px indipendente dall'altezza del child; NON usare
  100vh/innerHeight per determinare un'altezza che il parent ricalcola dal child.
- Area flex: `min-height:0`, `overflow-y:auto`, `scrollbar-gutter:stable`,
  regione ARIA con nome e `tabIndex=0`, focus visibile. Nessun limite ai pezzi,
  nessuna riduzione di font e nessun contenuto rimosso.
- **position:relative SU FRAME E AREA SCROLL**: obbligatorio per contenere
  il MathML assoluto invisibile di KaTeX; altrimenti il body sembra basso
  ma documentElement.scrollHeight cresce e la pagina intera si sposta.
- Congelare scroll interno con `html[data-lf-crop-open] .expr-input-page`;
  nascondere `.toaster` SOLO durante il crop, perché non copra i 4 comandi.
  Non cancellare notifiche e non cambiare CropDialog per questo.
- Rimosso vecchio ResizeObserver/MutationObserver locale da pagina 2:
  inviava messaggi senza token e senza guardia crop. Unica fonte =
  `initHeightSync()` in main.tsx. NON reintrodurre il doppio observer.
- Non modificare pagina 1/3, PDF, OCR, motore, backend o dati per il layout.

## Collaudo e falsi negativi già risolti

- 738 unitari passati, 28 saltati; check/build riusciti.
- `tests/input-scroll.e2e.mjs`: 7 scenari /151 controlli, inclusi dieci pezzi
  veri, touch/rotella/tastiera, font 160%, iframe e hit test dei 4 comandi.
- `tests/crop-mobile.e2e.mjs`: 9 scenari /223 controlli, compresa rotazione.
- Eseguire le due suite **in sequenza**, attendere commit e smooth-scroll
  tra aggiunte: niente force-click né PointerEvent simulati nel DOM.
- Dopo rotazione `--expr-visible-height` DEVE cambiare. Confrontare gli
  stili del lock escludendo SOLO quella variabile e verificare separatamente
  che rifletta il viewport nuovo; non ripristinare una vecchia altezza.
- Dopo drag la maniglia può uscire dalla porzione visibile; per leggerne
  il valore usare locator DOM per aria-label, non richiedere un nodo accessibile
  ancora esposto. Prima del gesto controllare l'hit test della maniglia.
- Touch/viewport emulati Chromium, blog cross-origin simulato, OCR mock.
  Non dichiarare certificazione su telefoni fisici o blog pubblico.

## ZIP e riuso

Includere `SECONDA-PAGINA-SCROLL.md`, `tests/INPUT-SCROLL.md`, i due E2E e
`tests/input-scroll-results.json`, oltre alle guide già obbligatorie.
Per clonare il layout copiare insieme wrapper/effetto App, classi pagina,
CSS e contratto heightSync unico. Non applicare a tutte le route.
Per il pacchetto completo usare lo script verificato della skill ZIP:
escludere chiavi/runtime ma conservare font, ONNX, WASM, fixture e lockfile.
Confrontare il client ricostruito con gli hash 8744, NON con 8742/8737/8736.

**Header 8742 (da foto utente):** nella seconda pagina sono RIMOSSI il
titolo «WIDGET METACOGNITIVO…» e la riga dati studente (restano in prima
pagina e nel PDF); il link home è sostituito dal piccolo pulsante marrone
**INDIETRO** (token primary, text-xs px-3 py-1.5, aria-label «Torna alla
pagina iniziale», sempre visibile). NON reintrodurre il titolo né la riga
dati in pagina 2.

**8744 (da foto mobile):** didascalia SOLO «SCRIVI QUI L'ESPRESSIONE» in
grassetto scuro; pezzi lunghi contenuti con scorrimento DENTRO il box
(span KaTeX con classe `piece-display` + `flex-1 min-w-0`, regola CSS su
`.katex-display` con `width max-content` e `min-width 100%` per tenere
centrati i pezzi corti). Applicare `piece-display` a OGNI nuovo box con
resa KaTeX (es. trascrizione, conferma): senza di essa le espressioni
lunghe escono dai bordi (avviso con scrollWidth pagina verificato con
pezzo lunghissimo di prova; il clone MathML di KaTeX è invisibile e va
ignorato nei controlli di contenimento).

Verifica ZIP 8737 completata: nuova estrazione senza chiavi/DB, install da
lockfile, check, 738 test superati/28 saltati e build riusciti; **tutti i 37
file client identici** alla build pubblicata. Express locale: root/font
HTTP 200, IA senza chiave 503 atteso. `VERIFICA-PACCHETTO-8737.md` incluso.
Dopo il test aggiungere soltanto rapporto/checklist; confrontare il manifest
finale con quello ricostruito e verificare CRC/hash di ciascun payload.

