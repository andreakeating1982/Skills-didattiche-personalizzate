# Guida al layout del quaderno accessibile

Riferimento operativo della skill **quaderno-accessibile**. Leggere questa guida quando si costruisce o si calibra un quaderno. I valori numerici derivano dai quaderni reali già consegnati (10 metodologie, mappa concettuale, Shakespeare v4 — quest'ultimo è il lavoro più recente, 2026-09-06) e dal CSS validato in `templates/quaderno_template.html`.

## 1. Il formato in breve

- Pagina A4 (595 × 842 pt), margini del template: 1.8 cm laterali (~51 pt), 1.9 cm in basso, 1.8 cm in alto (la prima pagina usa 1.2/1.7 cm). Con questi margini la **zona utile** di una pagina normale va circa da y=51 a y=788 (~737 pt di altezza) e larga ~493 pt.
- **Numeri di pagina**: numero semplice (`counter(page)`) in basso al centro su ogni pagina tranne la prima. Nel CSS: `@page { @bottom-center { content: counter(page); font-size: 12pt; font-weight: 700; color: #26211b; } }` e `@page :first { @bottom-center { content: none; } }` (la copertina NON mostra il numero). Niente testo lungo nel footer: il numero da solo è più pulito e non va tradotto.
- Una pagina "piena" nei quaderni reali finisce tra y≈730 e y≈778. Una pagina con contenuto che termina sotto ~200 pt è da considerare **quasi vuota** e va corretta.
- Piano tipico: **pagina 1 = copertina** (titolo + indice colorato) in una delle due varianti del §8 — densa (la sezione 1 inizia subito sotto l'indice, modello di default del template) o dedicata (titolo + immagine + indice, sezione 1 a pagina 2: «10 metodologie» e quaderno Shakespeare nella versione finale v4, 8 pagine con sezioni alle pagine 2/4/6/8) — poi 2-4 sezioni da 1-2 pagine, sezione quiz eventuale (domande compatte, più di 2 per pagina), eventuale glossario DIFFICULT WORDS in uno spazio residuo, mappa di revisione finale come ultima pagina piena → totale tipico 8-13 pagine.

## 2. Fase 1 — estrazione di testo e immagini dal PDF sorgente

Snippet PyMuPDF (testato su python3.11):

```python
import pymupdf
doc = pymupdf.open('percorso.pdf')
print('Pagine:', len(doc))
for i, page in enumerate(doc):
    print(f'--- Pagina {i+1} ({page.rect.width:.0f}x{page.rect.height:.0f}pt)')
    for k, im in enumerate(page.get_images(full=True)):
        pix = pymupdf.Pixmap(doc, im[0])          # estrai immagine originale
        if pix.n > 4:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        pix.save(f'orig-p{i+1}-{k}.png')
        print('  immagine', pix.width, 'x', pix.height)
full = '\n===PAGINA===\n'.join(p.get_text() for p in doc)
open('testo.txt', 'w').write(full)                # poi leggere con file_read
```

Regole:
- Leggere **tutto** il testo prima di progettare: suddivisione in sezioni, tono, lingua.
- Salvare l'immagine originale della prima pagina: sarà la copertina se adatta (controllarla con `file_view`).
- Annotare dal testo originale gli accenti di colore usati (es. parole chiave in viola) per replicarli nella palette del quaderno.

## 3. Economia di pagina: pagine quasi vuote e blocchi orfani

Sintomo: la verifica segnala una pagina quasi vuota perché un **blocco non spezzabile** (`.sintesi`, `.qcard`, `.m-node`, immagine) è "scappato" da solo in cima alla pagina successiva, lasciando la precedente molto corta.

Due rimedi aggiuntivi (usati sul quaderno Shakespeare) quando un box "di chiusura" non entra:
- **Ricollocare il blocco in uno spazio residuo precedente**: se una pagina (es. l'ultima del quiz) ha molto spazio libero in fondo e il blocco non spezzabile (es. glossario DIFFICULT WORDS) verrebbe da solo in una pagina nuova quasi vuota, sposta il blocco nel flusso PRIMA dell'ultima sezione, in coda alla pagina che ha spazio. L'ultima pagina resta così la mappa di revisione piena.
- **Riempire la pagina 1**: se dopo l'indice resta spazio, la sezione 1 inizia subito in pagina 1 (banner + primo box) invece di lasciare la copertina semi-vuota con la sola nota "Fai clic…".

Regola generale: non forzare mai interruzioni manuali; si recupera spazio a monte riducendo gli spazi, in **quest'ordine** (ogni passo vale ~10-40 pt, ri-rendere e riverificare dopo ogni passo):

1. Ridurre i margini dei box `.sintesi` (es. `margin: 16px 0 12px` → `9px 0 8px`) e i padding interni (`.sintesi td` 6px → 4-5px; `.s-head` 6px → 4-5px).
2. Ridurre il margine dei sottotitoli `h3.st` (`margin: 20px 0 6px` → `11px 0 4px`).
3. Ridurre il margine dei paragrafi `p` (`9px 0` → `7px 0`).
4. Restringere l'immagine della sezione sovraccarica con una regola dedicata, es. `#sec3 img.ilust { width: 54%; margin: 14px auto 10px; }` (default 62%; non scendere sotto il ~50% per non rompere l'uniformità).
5. Compattare le schede `.qcard` (margini 8px → 5px, padding, margine del titolo domanda `.qq`).

Quando il box rientra nella pagina precedente, il documento si riallinea da solo (es. si passa da 10 a 8 pagine senza interventi sui salti pagina).

Misure di riferimento dei blocchi: box `.sintesi` a 3 righe ≈ 150-200 pt; scheda `.qcard` ≈ 90-110 pt; immagine al 62% ≈ 170-180 pt di altezza (landscape 16:9: altezza = larghezza / 1.78).

## 4. Griglia quiz 2×2: opzioni A-D incolonnate

**Lezione appresa sul campo**: opzioni rese con `inline-block` al 47-49% di larghezza in un contenitore che eredita `text-align: justify` dal body producono colonne sfalsate (righe irregolari, testi che vanno a capo, spazi disuguali). La soluzione validata è una **tabella CSS rigida**:

```html
<div class="opts">
  <div class="optrow">
    <div class="opt"><span class="ol">A</span>Testo opzione</div>
    <div class="opt"><span class="ol">B</span>Testo opzione</div>
  </div>
  <div class="optrow">
    <div class="opt"><span class="ol">C</span>Testo opzione</div>
    <div class="opt"><span class="ol">D</span>Testo opzione</div>
  </div>
</div>
```

```css
.qcard { ... text-align: left; }          /* blocca la giustificazione ereditata */
.opts  { display: table; width: 100%; table-layout: fixed;
         border-collapse: collapse; margin: 2px 0 1px; text-align: left; }
.optrow{ display: table-row; }
.opt   { display: table-cell; width: 50%; vertical-align: top;
         font-size: 10pt; line-height: 1.55; padding: 1px 0; text-align: left; }
.opt + .opt { padding-left: 12px; }       /* spazio tra colonna 1 e 2 */
.ol    { display: inline-block; width: 16px; height: 16px; border-radius: 50%;
         background: #37474a; color: #fff; font-weight: 800; font-size: 9pt;
         line-height: 16px; text-align: center; margin-right: 6px;
         vertical-align: middle; }
```

Regole:
- Ogni opzione deve stare su **una sola riga**: a 10-10.5 pt con OpenDyslexic in una cella da ~50% della scheda (~218 pt di testo) entrano ~33-37 caratteri. Se un'opzione va a capo, ridurre il font a 9.5-10 pt o alleggerire margini/padding della scheda.
- Verificare sempre con un'anteprima ad alta risoluzione (150 dpi) che A+B siano sulla stessa riga e C+D sulla riga sotto, con colonna sinistra e destra allineate alla stessa x.
- Mantenere `page-break-inside: avoid` sulle `.qcard` (o su coppie `.qpair` di 2 schede); le domande scorrono liberamente e vanno compattate per ottenere **più di 2 domande per pagina** (gold standard Shakespeare: 10 domande su ~2 pagine piene, le ultime 2 in fondo alla pagina insieme al glossario).
- Quiz guidato dall'insegnante o con audio: nelle istruzioni (box HOW TO PLAY) usare la formula validata, es. EN "Listen to the teacher reading each question and Tap the correct answer. You cannot change it afterwards"; IT "Ascolta l'insegnante che legge ogni domanda e tocca la risposta giusta. Non puoi cambiarla in seguito"; ES "Escucha al profesor…". Adattare la lingua al documento.

## 5. Immagini uniformi e copertina

- Generare le immagini delle sezioni con `media_generate_from_images` passando l'immagine originale del documento come riferimento (`image_urls`) e descrivendo "stesso stile dell'immagine di riferimento…", orientamento **landscape** (i generatori restituiscono ~1376×768).
- Controllo qualità: comporre un foglio contatto (originale + nuove) con Pillow e ispezionarlo con `file_view` prima di inserirle.
- **Uniformità obbligatoria**: tutte le immagini dentro i box devono avere la STESSA larghezza (~50% del contenuto). Sul quaderno Shakespeare tutte le `.blk img.ilust { width: 50% }` (52% nella sezione quiz). **Mai** ridurre una sola immagine (es. al 33%) per far stare il layout: si recupera spazio da margini/padding. Vale anche per l'eventuale immagine del box introduttivo in pagina 1 (es. `.whocover img.ilust { width: 50% }`, non 33%).
- Dimensioni di riferimento: `img.ilust { width: 50-54% }` dentro i box; immagine di copertina grande solo nel modello a copertina dedicata (§8). Override per sezione con molto testo (es. quiz) ~50-52%.
- Ogni `<img>` richiede `alt` descrittivo nella lingua del documento (serve anche per la marcatura PDF/UA-1).

## 6. PDF/UA-1, indice e accessibilità

- Render sempre con `pdf_variant='pdf/ua-1'` (WeasyPrint). I segnalibri derivano automaticamente dai titoli: conteggio atteso = h1 + h2 + h3 (es. 20 segnalibri nel quaderno Shakespeare v4 finale, 8 pagine).
- La lingua viene da `<html lang="…">`: un documento in inglese deve avere `lang="en"` (gli screen reader pronuncerebbero l'inglese con la fonetica italiana con `lang="it"`).
- Indice: i numeri di pagina NON si scrivono a mano: `a::after { content: target-counter(attr(href), page); }` e ogni riga ha un link `href="#secN"`. Verificare che i numeri mostrati coincidano con gli inizi sezione rilevati dalla verifica.
- Contrasto: nero su bianco; colori per le evidenziazioni sempre accompagnati da grassetto (mai solo colore). Palette: rosso `#b3261e`, blu `#1a5fb4`, verde `#2e7d32`, arancione `#a35400`, viola `#5e35b1`, acquamarina `#0e7c66`, navy `#1f3864`.
- Font OpenDyslexic: verificare con `fc-list | grep -i dyslexic`; se manca, `cp templates/fonts/*.otf ~/.fonts/ && fc-cache -f`. I quaderni usano corpi 13-14 pt testo, 11-12 pt schede/box; il numero di pagina è 12-13 pt bold scuro, niente testo nel footer.
- Numeri di pagina: `@bottom-center { content: counter(page); }` su `@page`, e `@page :first { @bottom-center { content: none; } }` per non numerare la copertina.

## 7. Verifica e QA

- Struttura: `python scripts/verify_quaderno.py out.pdf --secs "…|…"` (lo script ignora da solo i numeri di pagina puri in fondo al foglio; `--footer-prefix` serve solo per footer testuali).
- Esito atteso: nessuna pagina quasi vuota; sezioni alle pagine previste; numeri di pagina dalla 2 in poi e assenti in copertina; segnalibri > 0; `Lang` giusto; `Marked: True`.
- Numeri indice: controllare sul testo della pagina 1 che i valori di destra corrispondano agli inizi sezione.
- Anteprime: `pdftoppm -png -r 80 file.pdf sv` e ispezione `file_view` di copertina, una pagina per sezione, pagine quiz (griglia allineata), mappa finale.
- Consegna: `send_attachment` con il PDF finale; anteprima opzionale in markdown col percorso sandbox (es. `![…](/home/user/<slug>_build/sv-1.png)`).

## 8. Modello a copertina dedicata e indice raffinato (gold standard «Le 10 metodologie didattiche inclusive»)

**Quando usarlo**: il quaderno ha MOLTE sezioni/macro-blocchi (es. 10 metodologie) e l'utente chiede che ogni sezione inizi su una nuova pagina. In questo modello la pagina 1 è DEDICATA a copertina + indice (la sezione 1 inizia a pagina 2), a differenza del modello «pagina 1 densa» dove la sezione 1 inizia subito sotto l'indice (template di default; il quaderno Shakespeare è passato al modello dedicato nella versione finale v4 — vedi `restyling_compatto.md` §Shakespeare v4). Chiedi all'utente o inferisci dalla struttura del sorgente (pagine per capitolo/metodologia → modello dedicato).

### Struttura HTML (validata)

```html
<section class="sec" id="indice">                <!-- page-break-before: auto -->
  <h1 class="cover-title">Titolo del quaderno</h1>
  <div class="cover-img"><img class="ilust" src="media/cover.png" alt="…"></div>
  <h2 class="banner navy">Indice</h2>
  <div class="indwrap">
    <table class="indice">
      <!-- NIENTE riga di intestazione <tr><th>Metodologia</th><th>Pagina</th></tr>:
           rimossa su richiesta (niente didascalie sopra l'elenco; le colonne
           restano chiare grazie al rientro sospeso). -->
      <tr><td><span class="ind-num ind1">1</span><a class="ind-title" href="#sec1">Titolo sezione</a></td>
          <td class="ind-pag"><a href="#sec1"></a></td></tr>
      <!-- … altre voci (ind2…indN), ultima riga con stella (★) verso #mappa -->
    </table>
  </div>
</section>

<section class="sec-flow" id="sec1">            <!-- page-break-before: always -->
  <h2 class="banner red">1 · Titolo sezione</h2>
  <div class="blk">…card…</div>                   <!-- card NON spezzabili -->
  <div class="sintesi" style="border-color:#b3261e;">…</div>
</section>
<!-- … altre section.sec-flow (colori in ordine), chiusura con #mappa -->
```

Ogni sezione è `section.sec-flow` (nuova pagina); la mappa finale resta l'ultima `section.sec` con `#mappa`. Le card `.blk` hanno `page-break-inside: avoid` e `h2.banner { page-break-after: avoid; }`.

### CSS indice arioso con rientro sospeso (valori validati su 22 pagine)

```css
/* copertina */
.cover-title { background:#5e35b1; color:#fff; border-radius:14px; padding:10px 18px;
  font-size:20pt; line-height:1.3; font-weight:700; margin:0 0 8px;
  text-align:center; text-transform:uppercase; }
.cover-img img.ilust { width:70%; margin:0 auto 6px; }      /* landscape, bilancia la pagina 1 */
.banner.navy { background:#1f3864; margin:6px 0 12px; }
/* box crema dell'indice */
.indwrap { background:#fffaf0; border:2px solid #e6d5ae; border-radius:14px;
  padding:5px 10px 8px; margin:0 0 12px; page-break-inside:avoid; }
table.indice { width:100%; border-collapse:collapse; }
.indice td { padding:8px 12px; text-align:left; font-size:13.5pt; vertical-align:middle; } /* aria: 8px verticali */
.ind-pag { text-align:right; width:13%; white-space:nowrap; }
.ind-pag a { text-decoration:none; color:#26211b; font-weight:700; }
.ind-pag a::after { content:target-counter(attr(href),page); }
/* RIENTRO SOSPESO: numero flottante + titolo a blocco. Le righe che vanno a
   capo si allineano all'INIZIO DEL TESTO (offset 37px), mai sotto il numero. */
.ind-num { display:block; float:left; width:27px; height:27px; border-radius:50%;
  color:#fff; font-weight:700; text-align:center; line-height:27px;
  font-size:13.5pt; margin:0 10px 0 0; }
.ind-title { display:block; margin:3px 0 0 37px; font-size:13.5pt; font-weight:700;
  line-height:1.45; color:#26211b; text-decoration:none; text-transform:uppercase; }
/* colori cerchi ind1…indN: 1 rosso #b3261e, 2 blu #1a5fb4, 3 verde #2e7d32,
   4 arancio #a35400, 5 grigio #4a4a4a, 6 viola #5e35b1, 7 acquamarina #0e7c66,
   … navy #1f3864 per l'ultima stella */
```

Calibrazione del rientro sospeso (se cambi font o diametro dei cerchi):
- `offsetX` (margin-left del titolo) = diametro cerchio + margine destro: 27 + 10 = 37px.
- `offsetY` (margin-top del titolo) ≈ (diametro cerchio − altezza riga testo)/2: con 13.5pt e line-height 1.45 la riga è ~19.6pt → (27−19.6)/2 ≈ 3px. Il numero deve essere `display:block; float:left` (NON inline-block), altrimenti le righe successive tornano sotto il numero.

### Bilanciamento pagina 1 (copertina dedicata)
- Obiettivo: pagina 1 piena ma NON traboccante — ultimo contenuto con ~35–70 pt (1.2–2.5 cm) di spazio bianco sopra il margine inferiore (valore verificato: ~47 pt ≈ 1.7 cm con immagine al 70%). Misura con Pillow sulle anteprime: `content_end = H − (margine_basso_pag1/72*dpi)`; differenza con l'ultima riga di contenuto.
- Se la pagina trabocca, la sezione 1 slitta a pagina 3: riduci l'immagine cover (68–70%) o i padding, prima di toccare i contenuti.
- Nessun sottotitolo didascalico sotto il titolo di copertina, salvo richiesta contraria.

### Regola di riempimento delle sezioni (modello a card)
La prima pagina di ogni sezione va riempita il più possibile con le card nell'ordine del flusso; lo spazio vuoto è ammesso SOLO in coda alla fine della metodologia/sezione, mai come buco all'inizio o in mezzo (nessun orfano). Manopole nell'ordine: ridurre `margin-bottom` e `padding` delle `.blk`, margini delle liste, e in ultima istanza override per-sezione sulle immagini `#secN .blk img.ilust { width: …% }` (es. 34%, 31–41% nei quaderni reali). Nel modello a card l'uniformità delle immagini vale DENTRO la card; tra sezioni gli override sono ammessi per l'impaginazione (a differenza del modello Shakespeare §5).

### Verifica aggiuntiva del modello dedicato
- `verify_quaderno.py --secs "…|…"`: la sezione 1 DEVE iniziare a pagina 2 (mai 3+); nessuna pagina quasi vuota dentro le sezioni; ultima pagina = mappa piena.
- Controllo visivo a 150 dpi: i cerchi numerati restano centrati rispetto alla PRIMA riga del titolo e le righe a capo hanno la stessa x dell'inizio del testo.

Riferimenti reali: `/home/user/metodologie_shake_build/metodologie_alta.html` (v11) e il PDF `Metodologie_Didattiche_Inclusive_quaderno_alta_leggibilita.pdf` (22 pagine): la pagina 1 del PDF è l'implementazione di riferimento di questo modello.
