# Restyling compatto e rifiniture — riferimento storico «Rosalía de Castro» v5

> **AGGIORNAMENTO PRIORITARIO 4 NOVEMBRE 2026:** la versione corrente approvata è `templates/rosalia-revisione-approvata-2026-11-04/ROSALIA_DE_CASTRO_APPROVATO.pdf`, non v5; leggere [metodo, differenze e QA](restyling-conservativo-rosalia-approvato-2026-11-04.md). Le prescrizioni di questo file sono storiche e si applicano solo se l'utente richiede esplicitamente il vecchio stile specialistico; non usare le vecchie frecce, compattazioni e disposizione delle immagini per sovrascrivere la versione approvata o una richiesta di conservazione integrale.

> **Precedenza per documenti discorsivi lunghi simili alla guida BES (30/10/2026):** leggere `documenti-lunghi-blog.md`. La baseline finale v8 impone bianco FUORI dai box, crema solo DENTRO, massimo 5 righe reali per piccolo blocco e nessun titolo sotto le immagini. Per questi documenti il nuovo profilo prevale sulle vecchie regole generiche; non sovrascrivere invece le collane con modello proprio.

Regole storiche apprese sul restyle del quaderno Rosalía — versione allora di riferimento = **v5**
(`/home/user/rosalia_v2_build/rosalia_v5.html`, PDF `Rosalia_de_Castro_Facile_quaderno_accessibile_v5.pdf`):
15 pagine, con testo spagnolo conservato salvo eliminazioni allora richieste. Questo trattamento
è storico: replicarlo soltanto se l'utente richiede espressamente la v5, non quando chiede
l'ultima Rosalía approvata. Il tag PDF non equivale a una certificazione PDF/UA indipendente.
Si applicano quando l'utente chiede su un quaderno già fatto: «elimina la scritta X»,
«più immagini, in testa alle card e più grandi», «mappe/QR senza card crema e centrati»,
«testi lunghi spezzali ogni ~5 righe senza cambiarli», «compatta le card per pagina»,
«aggiungi simboli/icone tipo ✔ ➜ per segnare passaggi/azioni».

## Workflow
1. Lavora sull'HTML attuale del quaderno (mai sul testo: parole invariate).
2. Usa uno script Python con BeautifulSoup (modello: `/home/user/rosalia_v2_build/build_v3.py`)
   che trasforma l'HTML e poi rende con WeasyPrint `pdf_variant='pdf/ua-1'`.
3. Verifica automatica: confronta il testo delle sezioni (prima/dopo) normalizzato —
   unica differenza ammessa sono i titoli delle mappe spostati fuori dalle card.
4. Controllo visivo: `pdftoppm -png -r 110` e `file_view` su TUTTE le pagine.

## Regole
- **Scritta dell'indice**: se l'indice non è un PDF cliccabile, rimuovi frasi tipo
  «Pulsa sobre cada apartado para ir directamente a la página correspondiente».
- **Immagini in testa alle card**: ogni sezione ha UN'immagine grande (larghezza ~62–64%
  della card) inserita DENTRO la prima card di testo, subito sotto l'eventuale h3.
  Cattura la card-immagine della sezione con una pre-scansione a due passate (anche se
  nel DOM viene DOPO la card di testo) e spostala in testa alla prima card.
  Per le sezioni senza immagine: `media_generate_from_images` con una delle immagini
  esistenti come riferimento (stile coerente), orientamento landscape, poi copia in `media/`.
- **Mappe concettuali e QR fuori dalle card**: wrapper `<div class="media-out">`
  centrato su fondo BIANCO, niente sfondo/bordo crema attorno all'immagine; titolo
  centrato sopra (solo testo, senza box). Mappe a larghezza ~96–100%, QR ~150px.
  `page-break-inside: avoid` sul wrapper.
- **QR subito dopo la card che lo cita**: se un passo dice «escanear el código QR que
  tenéis aquí abajo», il QR va subito DOPO quella card (mai in coda alla sezione, dove
  rischia di restare orfano in cima alla pagina successiva).
- **Testi lunghi spezzati ogni ~5 righe senza cambiarli**: taglio solo a fine frase
  (`(?<=[.!?;])\s+(?=[A-ZÁÉÍÓÚÜÑ¿¡«“"\[])`), chunk ≤ ~295 caratteri; card successive
  senza titolo né immagine. I tag inline (span, b, img circolari) vanno preservati
  rasoio: appiattisci il `<p>` in run (testo + catena di tag) e ricostruisci i chunk.
- **Compattazione**: niente `page-break-before: always` per ogni sezione → flusso
  continuo (`auto`) così le card riempiono le pagine. Sezioni ~1–2 pagine dense;
  i banner numerati possono iniziare anche a metà pagina.
- **Calibrazione fine**: se un blocco non entra per pochi mm, prima riduci le manopole
  locali (padding/margini della sola sezione via `#secN .blk {…}`, larghezza immagine,
  QR) e ri-rendi; misura gli spazi residui reali sulle anteprime a 110 dpi (1 cm ≈
  43,3 px) cercando le righe non bianche, non fidarti delle stime a occhio.
- **PDF/UA**: mantenere `Tagged: yes`, alt in lingua del documento, `lang` corretto.

## v4 — immagini più piccole solo in alcune sezioni: regola CSS residua

**Sintomo**: dopo il restyling quasi tutte le immagini sono uniformi (~10,6×5,9 cm,
larghezza 64% della card) ma UNA O DUE sezioni hanno l'immagine molto più piccola
(es. 5,6×3,1 cm), anche se nel DOM l'immagine è identica alle altre (stessa classe
`ilust` dentro `.blk-head`).

**Causa tipica**: nel CSS del template/sorgente restano regole con id di sezione che
sovrascrivono la larghezza globale, es. `#sec1 .blk img.ilust, #sec2 .blk img.ilust { width: 34%; }`.
La specificità (id + classi) batte `.blk-head img.ilust { width: 64%; }`.

**Diagnosi oggettiva** (mai a occhio): misura i rettangoli reali delle immagini nel PDF
con PyMuPDF (`pip3 install pymupdf`) e confrontali fra le pagine:

```python
import pymupdf
doc = pymupdf.open('quaderno.pdf'); cm = 72/2.54
for pno in range(len(doc)):
    for im in doc[pno].get_image_info():
        bb = im['bbox']; w = (bb[2]-bb[0])/cm; h = (bb[3]-bb[1])/cm
        if w > 1.5 and h > 1.0:
            print(pno+1, f'{w:.1f} x {h:.1f} cm')
```

**Fix**: rimuovi la regola residua nel CSS dello script. ATTENZIONE: nel sorgente la
regola può essere spezzata su più righe (`#sec1 .blk img.ilust,⏎#sec2 … { width: 34%; }`)
quindi `str.replace()` con la stringa su una riga fallisce IN SILENZIO → usa una regex
che tollera gli a-capo e poi VERIFICA grepando l'HTML finale (`css.count('width: 34%')`
== 0):

```python
CSS = re.sub(r'(?ms)#sec1 \.blk img\.ilust,\s*#sec2 \.blk img\.ilust \{ width: 34%; \}',
             '/* immagini sez.1-2 uniformate al 64% */', CSS)
```

Ri-rendi e rimisura: le immagini devono tornare identiche alle altre (10,6×5,9 cm) e
l'impaginazione non deve cambiare (stesso numero di pagine).

## v4 — linea del tempo a blocchi colorati → freccia orizzontale verso destra

**Quando**: l'utente chiede che la «línea del tiempo»/timeline «assomigli di più a una
freccia verso destra». Markup sorgente tipico: `<table class="timeline">` con celle
`<td class="tl-cell tl1…tl7">` contenenti `<span class="yr">anno</span>` e
`<span class="ev">evento</span>`. I colori degli anni vivono nelle classi CSS `tl1…tl7`
(es. verde #2e7d32, petrolio #0e7c66, arancio #a35400, blu #1a5fb4, viola #5e35b1,
rosso #b3261e): RECUPERALI grep-pando le regole `.tlN` nel CSS e riusali sui cerchi.

**Trasformazione** (BeautifulSoup, dentro lo script di restyling — testo invariato):

```python
tl = sec1el.find('table', class_='timeline')   # sezione che contiene la timeline
cells = []
for td in tl.find_all('td'):
    yr, ev = td.find(class_='yr'), td.find(class_='ev')
    if yr is None or ev is None:
        continue
    cls = ' '.join(td.get('class') or [])
    num = next((c for c in cls.split() if re.fullmatch(r'tl\d+', c)), 'tl1')
    cells.append((num, yr.get_text(' ', strip=True), ev.get_text(' ', strip=True)))
inner = ''.join(
    '<td><div class="tl-dot %s"><span>%s</span></div><div class="tl-ev">%s</div></td>'
    % (num, yr, ev) for num, yr, ev in cells)
new_tl = ('<div class="tl"><div class="tl-bar"></div><div class="tl-arrow"></div>'
          '<table class="tl-grid"><tr>' + inner + '</tr></table></div>')
tl.replace_with(BeautifulSoup(new_tl, 'html.parser'))
```

**CSS** da accodare allo stile (geometria validata su A4: cerchi 40px, linea che li
attraversa al centro, testo evento sotto):

```css
.tl { position: relative; margin: 2px 0 0; page-break-inside: avoid; }
.tl-bar { position: absolute; top: 16px; left: 12px; right: 30px; height: 6px;
          border-radius: 3px; background: #6b6255; z-index: 0; }
.tl-arrow { position: absolute; top: 5px; right: 2px; width: 0; height: 0; z-index: 0;
            border-top: 14px solid transparent; border-bottom: 14px solid transparent;
            border-left: 18px solid #6b6255; }
.tl-grid { width: 100%; border-collapse: collapse; table-layout: fixed; margin: 0; }
.tl-grid td { padding: 0 1px; text-align: center; vertical-align: top; }
.tl-dot { position: relative; z-index: 1; box-sizing: border-box; width: 40px; height: 40px;
          border-radius: 50%; margin: 0 auto; line-height: 36px; color: #fff;
          font-size: 9.5pt; font-weight: 800; text-align: center; border: 2px solid #fff; }
.tl-ev { margin: 7px auto 0; color: #3f382e; font-size: 8pt; line-height: 1.3;
         font-weight: 600; }
```

Note chiave: le classi `tl1…tl7` (lasciate su ogni cerchio) forniscono ancora il COLORE
dell'anno; `width/height` 40px e `border-radius: 50%` di `.tl-dot` vincono sui valori
originali delle celle perché il nuovo stile è accodato dopo (stessa specificità di
classe, vince l'ultimo). La punta della freccia è un triangolo CSS fatto di bordi
trasparenti (`border-left` colorato) che WeasyPrint rende correttamente. La barra
assoluta non deve coprire i cerchi: `.tl-dot` ha `z-index: 1` sopra `z-index: 0` della
barra. Geometria: bar `top:16px` + altezza 6px ⇒ centro a 19px = centro dei cerchi 40px;
freccia `top:5px` + altezza 28px ⇒ centro a 19px. Controllo finale con `file_view`:
linea dietro i cerchi, punta visibile a destra, eventi sotto senza sovrapposizioni,
stesso numero di pagine.

## v5 — marcatori testuali ➜/✔ per passaggi e azioni (Rosalía v5, richiesta tipica)

**Richiesta tipo**: «se necessario aggiungi piccole icone o simboli testuali (es. ✔, ➜)
per segnare passaggi/azioni» (applicata anche a Lázaro v3 e ora standard della v5).

**Principio: NON raddoppiare marcatori già presenti.** Prima di aggiungere ➜ controlla se
il blocco ha già un simbolo/etichetta che marca il passaggio:
- card con chip numerate tipo `<span class="chip">PASO 1</span>…PASO 8` → lascia le chip,
  NIENTE freccia;
- liste di controllo con caselle già generate dal CSS (`.check li::before { content:"\2610…"; }` →
  ☐ verde) → lascia le caselle, NIENTE freccia;
- card di istruzioni/azioni SENZA alcun marcatore (es. «Abre la aplicación…», «Escucha el
texto…», «Vuelve a leer el poema… y, a continuación, escribe…») → freccia ➜ colorata.
Nel quaderno v5 sono marcate 5 card: 4 nella sezione attività 1 (acquamarina `#0e7c66`) e
1 nella consegna finale di analisi testuale (blu `#14508f`). Le sezioni puramente
informative (biografia, opere, poemi) NON ricevono frecce.

**CSS da accodare** (codice identico al sistema usato per Lázaro, validato):

```css
/* marcatori: ➜ azione/passaggio */
.blk.paso > p:first-of-type::before {
  content: "\279C\00a0\00a0";
  font-family: "DejaVu Sans", sans-serif;
  font-weight: 700;
  font-size: 12pt;
  color: #26211b;               /* default scuro */
}
.blk.paso.c-0e7c66 > p:first-of-type::before { color: #0e7c66; }  /* sezione acquamarina */
.blk.paso.c-14508f > p:first-of-type::before { color: #14508f; }  /* sezione blu scuro */
```

**Applicazione in BeautifulSoup** (modello: `/home/user/rosalia_v2_build/build_rosalia_v5.py`):
per ogni sezione da marcare aggiungi alla card le classi `paso` e `c-<hex>` (hex senza `#`,
colore del banner della sezione); il `::before` si aggancia al primo `<p>` della card:

```python
for blk in sezione.find_all('div', class_='blk'):
    cls = blk.get('class') or []
    for extra in ('paso', 'c-' + hex_colore):
        if extra not in cls: cls.append(extra)
    blk['class'] = cls
```

Nota: `.blk.paso > p:first-of-type` aggancia la freccia al primo paragrafo anche quando la
card ha un'immagine in testa (`.blk-head`): la freccia compare quindi in testa al testo,
sotto l'immagine. Se una card ha più `<p>` e la consegna sta nel primo, va bene comunque
(la freccia marca l'inizio dell'azione). Se serve marcare un paragrafo NON primo (raro),
usa una classe sul `<p>` (es. `p.paso::before`). Colore della freccia = colore del banner
della sezione per coerenza cromatica.

## v5 — eliminazione di una card/scritta con rimandi coerenti (Rosalía v5, richiesta tipica)

**Richiesta tipo**: «elimina la parte che vedi nella foto / elimina la scritta X».
Regola appresa: elimina l'elemento richiesto E i rimandi che resterebbero incoerenti.

Caso reale (v5): eliminata la card con «Antes de escribir tu texto, vuelve a leer el
análisis textual que está en la lección sobre Gustavo Adolfo Bécquer» → eliminata ANCHE
la voce di checklist «He releído el análisis sobre Bécquer antes de empezar» che senza
la card non avrebbe più senso (la voce è nel `ul.check` della stessa sezione). Informa
sempre l'utente dell'eliminazione aggiuntiva così può chiedere di ripristinarla.

Identificazione oggettiva del bersaglio: trova la card dal testo esatto (normalizzato,
spazi → uno solo) con BeautifulSoup e fai `decompose()` sul `div.blk` contenitore; per la
voce di lista fai `decompose()` sul `<li>`.

Verifica automatica dopo l'eliminazione: confronta il testo normalizzato prima/dopo —
l'unica differenza ammessa sono le frasi eliminate (vedi lo script modello: rimozione
mirata + `assert` + diff). Poi ri-rendi, verifica struttura (`verify_quaderno.py`) e
controlla visivamente la pagina interessata con `file_view`.

Script modello completo v4→v5: `/home/user/rosalia_v2_build/build_rosalia_v5.py`
(include: eliminazione card + voce checklist, aggiunta classi `paso`, CSS marcatori,
verifica testi prima/dopo).

## Shakespeare v4 — rifiniture successive su un quaderno già consegnato (2026-09-06, modello operativo)

Quando l'utente torna su un quaderno già consegnato con richieste puntuali successive —
«elimina la scritta X», «l'indice in prima pagina è troppo arioso», «riscrivi le istruzioni
del quiz come nella foto» — il modello operativo è il quaderno **Shakespeare Romeo & Juliet v4**
(accettato: 8 pagine PDF/UA; cartella `/home/user/shake_v2_build/`; HTML base
`shake_accessibile_v1_originale.html` → script `build_shake_v4.py` → `shake_v4.html` →
`Shakespeare_Romeo_Juliet_quaderno_accessibile_v4.pdf`). Lo script è IDEMPOTENTE: riparte
sempre dall'HTML base v1 e riapplica tutte le trasformazioni in sequenza (restyling v3 +
rifiniture v4): rifacimento delle sezioni di contenuto e del quiz (funzioni
`rebuild_content_section`, `rebuild_quiz_section`), incapsulamento della tabella indice in
`div.indwrap`, CSS calibrato accodato in blocchi (`v4b_css`, `v4c_css`), modifiche di
contenuto, verifica testi finale. Non modificare mai a mano l'HTML già reso: ogni nuova
richiesta = una nuova trasformazione nello script (commento numerato `# N) …`), rebuild,
render, verify, anteprima, consegna.

**Verifica testi incorporata** (regola per ogni intervento): normalizza SRC e OUT
(BeautifulSoup, elimina style/script, `get_text` con spazi singoli), confronta con
`difflib.unified_diff` a livello di parola e asserisci esplicitamente le frasi rimosse
(lista `removed`) e aggiunte (lista `added`): le uniche differenze ammesse sono quelle
dichiarate; altrimenti il testo deve restare byte-identico.

### Richiesta tipo «elimina la scritta X»
Casi reali (tutti con `decompose()` su elementi mirati): scritta sotto l'indice
(`p.nota` dopo la tabella CONTENTS); riga 💡 in fondo alla mappa (`p.map-legend`);
testo introduttivo della mappa (`p.m-intro`: «Everything you need to remember: …»).
Dopo ogni rimozione ri-rendi, riverifica (frasi in lista `removed` = assenti) e controlla
che la pagina non sia diventata semivuota. Sulla MAPPA finale le rimozioni si compensano
con spaziature più ampie (valori finali validati, accodali al CSS):
```css
.map-root  { margin: 0 0 34px; padding: 14px 14px; }
.map-group { padding: 13px 12px 16px; margin: 0 0 42px; }
.map-ghead { margin-bottom: 16px; }
.map-row   { margin-top: 14px; }
.m-node    { padding: 12px 10px 15px; }
```
→ la mappa finale torna a terminare a y≈684/790 (pagina piena).

### Richiesta tipo «l'indice in prima pagina è troppo arioso»
Sintomo: voci dell'indice molto distanziate (pitch misurato ~36–38 pt) e padding interni
del box grandi. Misura oggettivamente con PyMuPDF (mai a occhio) il pitch fra i blocchi
di testo delle righe (`1`, `2`… o i titoli delle voci):
```python
import pymupdf
d = pymupdf.open('out.pdf')
rows = sorted(b[1] for b in d[0].get_text('blocks')
              if b[4].strip()[:1].isdigit() and 'WILLIAM' not in b[4])
print('pitch voci:', [round(rows[i+1]-rows[i], 1) for i in range(len(rows)-1)])
```
La distanza tra le voci è governata da `border-spacing` + `padding` delle `td` del
`table.indice` (NON dai margini del banner). Valori finali accettati per voci compatte e
copertina ordinata:
```css
.title-banner    { margin: 0 0 30px; }
img.ilust.cover  { margin: 12px auto 38px; }
h2.banner.navy   { margin: 30px 0 16px; }
.indwrap         { padding: 12px 18px 18px; margin: 0; }
table.indice     { border-collapse: separate; border-spacing: 0 4px; }
.indice td       { padding: 3px 12px; font-size: 13.5pt; }
```
Risultato misurato: pitch voci ≈ 30.1 pt (riferimento Rosalía v5: 33.8 pt uniformi);
gap naturale immagine→CONTENTS (~30 pt); il box termina a ~y463/790. ATTENZIONE (errore
già commesso e corretto): NON compensare una copertina «corta» allargando il margine sotto
l'immagine (es. `margin-bottom: 116px`): si crea un buco visivo tra immagine e indice che
il controllo visivo boccia. Con poche voci (4 righe) la copertina dedicata resta con ~40%
di aria in fondo ed è stata accettata così; con molte voci (9, Rosalía) si riempie da sola.
La riga con la ★ può avere pitch leggermente maggiore (glifo) senza essere un problema.

### Richiesta tipo «riscrivi le istruzioni del quiz come nella foto»
Modifica di CONTENUTO esplicitamente richiesta dall'utente (unica eccezione al testo
invariato) per allineare il quaderno all'app reale fotografata. Nel quiz Shakespeare:
individua la card HOW TO PLAY (`h3.blk-t` contenente «HOW TO PLAY»), `decompose()` sugli
`<ol>`, poi accoda passi `<p class="howstep"><span class="stn">1</span><span class="howtxt">…</span></p>`
(numero in cerchio verde) e una riga finale `<p class="howok"><span class="stok">✔</span>…</p>`.
Formula inglese validata: «Open Shakespeare's page on the teacher's blog» → «The teacher
gives you a 4-digit code: write your name and the code, then tap “Join the class”» → «The
questions appear, each with 4 answers: A, B, C, D» → «Listen to the teacher reading each
question and tap the correct answer. You cannot change it afterwards» → «After each
question, the teacher shows the results» → «✔ There is only 1 correct answer for every
question». Aggiungi le stringhe nuove alla lista `added` della verifica.

### Keyword colorate → nero grassetto (richiesta frequente, regola finale pulita)
Se le parole chiave colorate (`.k`, `.f`, `.v`…) vanno rese **nere in grassetto**, accoda
PER ULTIMO un blocco pulito con `!important`: selettori residui invalidi o commenti non
chiusi nel CSS possono annullare la regola precedente:
```css
.k, .f, .v { color: #000000 !important; font-weight: 700 !important; }
```

## Lázaro v4 — pulizia della nota FUENTE (citazione con attribuzione ridondante)

Richiesta tipo (quaderno in spagnolo/altra lingua): nel box di chiusura FUENTE eliminare la
frase introduttiva di attribuzione ridondante — «Testo principalmente rielaborato da: El
presente texto es tomado de » — lasciando l'etichetta FUENTE in neretto e la citazione
bibliografica completa (es. «CARRETER LÁZARO, Fernando - CALDERÓN CORREA, Evaristo.
*Cómo se comenta un texto literario*, Madrid: Cátedra, 2013 (1974), pág. 109-112. -
Traduzione di Andrea Centinaro.»). Script modello (patch piccola su HTML già reso):
`/home/user/lazaro_v2_build/build_lazaro_v4.py` (lazaro_v3.html → lazaro_v4.html, PDF
`Lazaro_Carreter_Metodo_Analisis_quaderno_accessibile_v4.pdf` + ZIP sorgente in `/home/user/`).

Tecnica: individua la nota dal testo normalizzato (es. `div.note-box` il cui testo inizia
con «FUENTE»), lavora sul testo piatto del `<p>`: `s.replace(FRASE, '')`, rimuovi gli
spazi fantasma prima della punteggiatura con `re.sub(r'\s+([,.;:!?])', r'\1', s)`,
normalizza gli spazi, separa l'etichetta dal resto, ripristina il corsivo `<em>` sul
titolo dell'opera (spesso perso nelle ricostruzioni) e ricostruisci il paragrafo come
`<strong>FUENTE</strong>` + citazione. Verifica automatica a fine script: testo normalizzato
prima/dopo, nessuna parola aggiunta o cambiata salvo la frase eliminata; poi render,
`verify_quaderno.py` e controllo visivo della pagina interessata.
