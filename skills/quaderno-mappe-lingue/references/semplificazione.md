# Regole di contenuto ed edizione semplificata

> Aggiornamento 28 ottobre 2026: applicare queste regole al CONTENUTO delle mappe nuove. Per copertina, frontespizio, guide, dimensioni editoriali e indice seguire `collana-facile.md`, che sostituisce il precedente modello viola. Non applicare queste regole per riscrivere mappe esistenti se richieste immutate.

## Obiettivo
Quaderno per studenti con disabilità intellettiva grave: mappe di grammatica
della lingua straniera spiegate con frasi italiane brevissime e concrete,
struttura visiva costante, due argomenti per pagina dove possibile.

## Struttura fissa (NON variare)
- A4, OpenDyslexic 14pt uniforme all’interno delle mappe. Nelle pagine editoriali FACILE usare la gerarchia tipografica del modello latino (vedi `collana-facile.md`).
- Ogni mappa: `banner colorato` (icona clay a tema + numero + titolo MAIUSCOLO)
  → `scheda` (bordo del colore della famiglia) → `box IN PRATICA` (crema,
  didascalia di 1-2 frasi).
- 1 o 2 mappe per pagina logica (`B_` + `PAGE()` nel build script): 2 mappe
  separate da spazio bianco di 20pt, senza linee di separazione.
- Copertina: titolo su banner viola + immagine clay centrata (42% larghezza) +
  indice a UNA colonna cliccabile (link → ancora `#mNN`, numero pagina via
  `target-counter`). Nessuna dicitura aggiuntiva tipo "Edizione inclusiva".
- Numeri di pagina in fondo (esclusa copertina).
- PDF/UA-1: render con render_quaderno.py (già impostato, legge lang e alt).

## Semplificazione per disabilità intellettiva grave
- Spiegazioni in italiano: 1 frase corta, parole concrete ("le cose che faccio
  sempre" invece di "azioni abituali").
- Coniugazioni: tabelle di massimo 4 righe con soggetto raggruppato
  (I / You / He-She-It / We-You-They) + colonne "forma piena / forma contratta
  (+ traduzione)".
- Interrogative: tabelle "question / YES / NO" a 4 righe con "..." al posto del
  soggetto ripetuto.
- Esempi: 1-2 per mappa, sempre in blu, frasi brevi.
- Titoli MAIUSCOLI semplici ("VERB 'BE' – QUESTIONS", non "interrogative form
  and short answers").
- Box IN PRATICA: 1-2 frasi, struttura "regola in una riga + risposta tipica".
- Nota finale (N): solo se aggiunge un'informazione concreta.

## Accoppiamento argomenti sulla stessa pagina
Accoppiare per affinità tematica (affermativa+negativa, mappa piccola+mappa
piccola). Vincolo: le DUE mappe devono stare in ~745pt di altezza. Il blocco
`.blk` ha `page-break-inside:avoid`: se una coppia non ci sta, la seconda mappa
va da sola a pagina intera (accettabile per le mappe più piene, es. interrogative
con risposte brevi). Riferimento: il quaderno inglese ha 95 mappe in 50 pagine
logiche (40 accoppiate, 10 singole) = 54 pagine totali con indice di 4 pagine.

## Palette per famiglia grammaticale
ROSSO=be/have/obbligo, ARANCIO=articoli/imperativo/condizionali,
AMBRA=preposizioni/consigli, VERDE=have/can/quantità/comparativi,
LIME=some/any/quantità, TEAL=nomi/present perfect, PETROLIO=there is/preposizioni/
how much, BLU=pronomi/present simple/futuro, INDACO=dimostrativi/past simple/
one-ones, VIOLA=possessivi/past continuous/question words, MAGENTA=question words/
present continuous, MARRONE=espressioni di tempo/possessivo sassone.
Una famiglia = un colore, coerente in tutto il quaderno.

## Copertina
Generare con media_generate_image, orientamento "square", stile coerente:
"Claymation style 3D illustration: an open grammar book on a school desk with
letter cubes spelling [LINGUA], red apple, colored pencils and question marks,
handmade plasticine clay look, warm studio lighting". Salvarla in
`<build>/media/cover.png`. Verificare l'ortografia della parola sulla copertina
(se sbagliata, mostrare il risultato, indicare l’errore e chiedere se correggere; non rigenerare autonomamente). Questa è la ricetta STORICA: per la collana FACILE riutilizzare gli asset clay adulti approvati; non introdurre cubetti con lettere o altri soggetti infantili.

## Trascrizione dal PDF sorgente
1. `pdftotext` per il testo; per le mappe disegnate usare file_view sulle
   immagini estratte (`pdftoppm` o `pdfimages`).
2. Una mappa del sorgente = una mappa del quaderno (stesso ordine di studio,
   salvo accorpamenti tematici per l'accoppiamento a pagina).
3. Verificare SEMPRE tabelle interrogative complete (spesso risultano
   troncate nell'estrazione).

## Render e verifica (obbligatori)
```
python build_<codice>.py
python <skill>/scripts/render_quaderno.py mappe_<codice>.html Quaderno_<codice>.pdf --base <build>
python <skill>/scripts/verify_quaderno.py Quaderno_<codice>.pdf
```
Esito atteso: nessuna pagina quasi vuota; numero pagine stabile dopo ogni
modifica (crescite inattese = coppie spezzate); segnalibri presenti; Lang =
lingua prevalente effettiva (nella collana FACILE `it`, con spiegazioni italiane); Marked = True. Non equiparare questi controlli a una certificazione completa PDF/UA.
Verifica visiva: `pdftoppm -png -r 55 -f N -l N <pdf> /tmp/pg` + file_view di
2-3 pagine accoppiate prima della consegna.
