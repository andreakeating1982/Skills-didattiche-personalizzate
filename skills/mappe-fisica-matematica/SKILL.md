---
name: mappe-fisica-matematica
description: >-
  Creare mappe concettuali PDF di FISICA e MATEMATICA accessibili per uno
  studente con disabilita' intellettiva grave, nello stile «v8» consolidato
  (OpenDyslexic, box colorati con icone e pallini numerati, titolo nel nodo
  centrale, 2 cm di margini, frazioni SEMPRE impilate). Usare quando l'utente
  chiede una mappa concettuale di matematica o fisica, un problema risolto
  passo passo, l'inserimento di una mappa nei raccoglitori
  (PRIMO/TERZO superiore/FISICA) o nella RACCOLTA COMPLETA, o la conversione
  di frazioni in linea in frazioni impilate. NON usare per quaderni PDF,
  presentazioni o app web.
---

# Mappe concettuali fisica/matematica — stile accessibile «v8»

Una mappa = UNA pagina A4 PDF generata da HTML con WeasyPrint. Tutto lo stile
base e' gia' nel template, NON riscriverlo.

## Risorse della skill

- `templates/mappa_base.html` — CSS completo (@font-face OpenDyslexic,
  `@page` con margini 2 cm, classi `.page`, `.rami`, `.ramo blu|arancio|viola|verde|giallo largo`,
  `.testa-ramo`, `.icona`, `.nome`, `.regoletta`, `.pallino-regola`, `.testo`,
  `.esempio`, `.centro`, `.nodo-centrale rosso`, `.palla`, `.nodo-titolo`,
  `.nodo-sotto`, `.densa`, `.frz` per le frazioni impilate) + scheletro commentato.
  I font OpenDyslexic sono in `templates/fonts/` e vanno copiati accanto all'HTML.
- `scripts/verifica_frazioni.py` — controlla che non restino frazioni in linea.
  Modalita' HTML (sorgenti) e `--pdf` (usa pdftotext, mai il binario).
  Exit code 0 = OK, 1 = trovate frazioni in linea.

## Workflow

1. Copia il template nella cartella di lavoro della chat (di solito
   `/home/user/mappe-N-Z/`): `cp <skill>/templates/mappa_base.html mappa-nome.html`
   e `mkdir -p fonts && cp <skill>/templates/fonts/*.otf fonts/`.
2. Compila il contenuto mantenendo la struttura fissa:
   - **Riga alta**: `.ramo blu` (il problema e i dati) + `.ramo arancio` (passo 1);
   - **Nodo centrale**: titolo della mappa in `.nodo-titolo` (MAI una
     intestazione «MAPPE CONCETTUALI» in alto alla pagina);
   - **Riga bassa**: `.ramo viola` (passo 2) + `.ramo verde` (passo 3) +
     `.ramo giallo largo` (riepilogo, es. intervallo di indeterminazione);
   - Adatta il numero di box all'argomento ma conserva la gerarchia e il nodo centrale.
3. Regole di contenuto (obbligatorie):
   - Studente con disabilita' intellettiva grave: frasi brevissime, parole note,
     parola chiave in `<b>grassetto</b>`, mai paragrafi densi;
   - **Frazioni SEMPRE impilate**, mai con la barra obliqua:
     `<span class="frz"><span class="num">numeratore</span><span class="den">denominatore</span></span>`;
     in intestazioni `.nome` usa `style="font-size:0.72em"`, nelle `.icona`
     `style="font-size:0.6em"`, altrove 0.8em o il default. Le unita' composte
     (kg/m³) sono anch'esse frazioni impilate. Le operazioni con simbolo
     (`÷`, `:`, `·`) restano scritte normalmente;
   - I passi guidati usano `.regoletta` con `.pallino-regola` numerato
     (colori: blu `#1976D2`, verde `#2E7D32`, arancio `#EF6C00`);
   - Esempi numerici con valori semplici e risultato seguito da `&#10004;`;
   - Disegnini: SVG inline per strumenti e schemi (es. quadrante di un
     amperometro, zoom sulle suddivisioni, grafici retta/iperbole/parabola);
     larghezza tipica 0.20–0.28 × viewBox in mm. Icone dei box: caratteri
     supportati dal font (es. `&#9889;` ⚡, `&#9654;`, `&#9998;`, `&#8596;`,
     `&#9662;`, `&plusmn;`); evitare emoji (👀 ecc. → warning `.notdef`);
   - Problemi di MISURA (fisica): aggiungere la scrittura corretta
     `I = (valore ± errore) unita'` e il box largo con l'**intervallo di
     indeterminazione** (SOMMO e SOTTRAGGO l'errore al valore).
4. Genera il PDF e controlla:
   ```bash
   python3.11 -m weasyprint mappa-nome.html Mappe-concettuali-Nome.pdf
   pdfinfo Mappe-concettuali-Nome.pdf | grep Pages     # deve essere 1 pagina
   python3.11 <skill>/scripts/verifica_frazioni.py mappa-nome.html
   pdftoppm -png -r 100 Mappe-concettuali-Nome.pdf qa && (controlla con file_view)
   ```
5. QA visivo: tutto dentro i box, nessun taglio a fondo pagina, frazioni
   leggibili, titolo centrato. Se esce su 2 pagine:
   - WeasyPrint NON spezza i contenitori flex: separa i box bassi in piu'
     `<div class="rami">` consecutivi (uno per viola+verde, uno per giallo largo);
   - riduci gli SVG e accorcia le `.regoletta`.
   Verifica al pixel con crop + ingrandimento quando il QA a 100 dpi e'
   dubbioso (le frazioni piccole spesso vengono lette male dal modello di visione;
   conferma con `pdftotext` che num/den siano su righe separate).
6. Consegna con `send_attachment` il PDF singolo (es.
   `Mappe-concettuali-Amperometro.pdf`).

## Inserimento nei raccoglitori (su richiesta)

I raccoglitori si costruiscono con `pdfunite`/`pdfseparate` nella cartella
`/home/user/mappe-N-Z/` (verifica l'ordine attuale con `pdftotext -f N -l N`):

- **FISICA-TERZO-SUPERIORE** = Unità di misura della massa + Conversione +
  Fisica (potenze del dieci, densità, strumenti, errori, **amperometro dopo
  gli errori**, relazioni) → 8 pagine. Attenzione: rigenerando `fisica.html`
  l'ordine interni torna a relazioni-prima-di-errori, quindi reinsertire
  l'amperometro con `pdfseparate` e unire `f1 f2 f3 f5 AMP f4`;
- **MATEMATICA-PRIMO-SUPERIORE** = FACILI (2 pg) + N-e-Z (8 pg) + Potenze delle frazioni (1 pg) = 11 pagine;
- **MATEMATICA-TERZO-SUPERIORE** = 4 pagine (invariate a meno di modifica esplicita);
- **RACCOLTA-COMPLETA** = FACILI + N-e-Z + Le-potenze + Pot-frazioni + massa +
  conversione + equazioni + fisica + densita' = 24 pagine.

Usare nomi di versione progressivi (es. `-v9`) quando si sostituisce un PDF
precedente, e verificare l'ordine pagina per pagina con `pdftotext` prima di
consegnare. Consegnare tutti i raccoglitori toccati + la raccolta aggiornata.

