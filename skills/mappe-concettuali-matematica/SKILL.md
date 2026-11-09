---
name: mappe-concettuali-matematica
description: "Produzione di PDF «Mappe concettuali» per esercizi di matematica partendo da foto o testo (qualsiasi anno scolastico). Usare SEMPRE quando l'utente carica una foto (o incolla testo) di esercizi di matematica e vuole le mappe concettuali, o chiede «le stesse mappe». Layout FISSO richiesto dall'utente — solo titolo «Mappe concettuali»; per ogni esercizio una card con COSA CHIEDE e STRUMENTO affiancati e ESATTAMENTE 3 passi numerati; NIENTE box giallo «Occhio a», NIENTE nota finale, NIENTE soluzioni. Font OpenDyslexic auto-ospitato, generazione WeasyPrint."
---

# Mappe concettuali di matematica

Trasforma foto/testi di esercizi di matematica in un PDF di "mappe concettuali" con formato invariabile, definito dall'utente (versione finale: 12 esercizi, 5 pagine, senza box giallo e senza nota finale).

## Flusso di lavoro

1. **Leggi la foto** con `file_view`: trascrivi TUTTI gli esercizi (numeri, testi, dati, opzioni A-D, punteggi). Se una parte non è leggibile o gli esercizi continuano in un'altra pagina, dillo nella risposta finale. Più foto → più esercizi nello stesso PDF, in ordine.
2. **Prepara la cartella di lavoro**: copia `templates/mappe-template.html` e `templates/fonts/` (OpenDyslexic-Regular.otf, OpenDyslexic-Bold.otf) preservando il percorso relativo `fonts/` usato dall'`@font-face`.
3. **Costruisci il PDF dal template** (le regole complete sono anche commentate nel file): una `<section class="card alg|geo">` per esercizio, in ordine.
   - `alg` (blu) per algebra/aritmetica/analisi/equazioni/disequazioni; `geo` (verde) per geometria e geometria analitica.
   - `card-head`: numero cerchiato, titolo BREVE, badge facoltativi (`b-punti` = "VALE 2 PUNTI" se il test lo indica, `b-aperta` = "RISPOSTA APERTA" se non ci sono opzioni, più `b-alg`/`b-geo`).
   - `.due`: box affiancati `.chiede` (COSA CHIEDE: riscrive l'esercizio con i dati completi) e `.strumenti` (STRUMENTO: formule/regole generali).
   - `.steps`: ESATTAMENTE 3 `<div class="step">` separati da `<div class="arr"></div>`. Passi imperativi, brevi, che dicono COSA fare in sequenza.
   - Per le radici nell'HTML usa `√<span style="text-decoration:overline">radicando</span>`.
4. **Vietato**: box giallo "Occhio a", checkbox, nota finale/fonte, intestazioni oltre al titolo, emoji nel PDF, e QUALSIASI soluzione (formule standard nel box Strumento sono ammesse; valori finali o passaggi risolti no).
5. **Genera**: `python3.11 -m weasyprint mappe.html "Mappe-concettuali.pdf"` e controlla le pagine con `pdfinfo`. Tipicamente 3-6 pagine (3-4 card per pagina).
6. **QA**: `pdftoppm -png -r 70` su prima e ultima pagina, poi `file_view`: solo il titolo "Mappe concettuali" in alto, nessun card tagliato, nessun carattere mancante (tofu), footer "Mappe concettuali — pagina X di Y".
7. **Consegna** il PDF con `send_attachment` (solo il PDF; la versione .md solo se richiesta).

## Limiti e casi particolari

- Esercizi con figure (triangoli, rette, grafici): non riprodurre il disegno; riporta i dati nel box COSA CHIEDE e inserisci tra i passi "disegna/rappresenta".
- Se un esercizio richiede più di 3 passi per essere spiegato, condensa: i passi devono restare ESATTAMENTE 3.
- Se l'utente chiede varianti (versione completa con Occhio a, versione B/N, versione con passi diversi), produci un nuovo PDF senza cambiare il formato base.
