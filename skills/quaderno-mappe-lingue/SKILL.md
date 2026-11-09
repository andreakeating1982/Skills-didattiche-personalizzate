---
name: quaderno-mappe-lingue
description: "Creare e aggiornare quaderni inclusivi di grammatica per lingue straniere, anche il quaderno inglese esistente. Standard attuale: collana INGLESE FACILE, FRANCESE FACILE e SPAGNOLO FACILE sul modello di LATINO FACILE (copertine terracotta con clay adulto, guide iniziali, percorso quinquennale adattabile, indice cliccabile). Usare per: rigenerare i tre quaderni, aggiungere mappe, conservare tutte le mappe senza modificarle, nuove lingue e copertine coordinate. Include script di costruzione e confronto byte/testo/pixel con gli originali. Sorgenti: /home/user/inglese_build, /home/user/mappe-fr, /home/user/mappe-es; edizione attuale in /home/user/facile_edizione. NON per app web, presentazioni blog o quaderni narrativi (quaderno-accessibile)."
---

# Quaderni di grammatica delle lingue — collana FACILE

## Scegliere il flusso

- **Rigenerare o mantenere INGLESE FACILE, FRANCESE FACILE, SPAGNOLO FACILE; creare copertine come Latino Facile; conservare le mappe:** leggere prima `references/collana-facile.md`. Usare gli script e le copertine inclusi, non il vecchio modello viola.
- **Aggiungere o correggere una mappa:** lavorare nel build della lingua; modificare soltanto quanto richiesto, rigenerare il PDF sorgente corrispondente, poi aggiornare inventario e collana. Non rimpaginare le mappe estranee alla richiesta.
- **Creare un nuovo quaderno/una nuova lingua:** seguire il flusso contenuti sottostante; applicare la veste editoriale FACILE dopo aver verificato le mappe.
- **Quaderni narrativi, Shakespeare, metodologie, 6 passi:** usare `quaderno-accessibile`.

## Standard e riferimenti attuali

Modello editoriale: `/home/user/uploads/Latino_Facile_colori_app.pdf`.
Cartella della collana approvata il 28 ottobre 2026: `/home/user/facile_edizione/`.

| Quaderno attuale | Mappe | Pagine totali | Pagine delle mappe |
|---|---:|---:|---:|
| `Inglese_Facile.pdf` | 96 | 60 | 51 |
| `Francese_Facile.pdf` | 79 | 49 | 40 |
| `Spagnolo_Facile.pdf` | 72 | 44 | 36 |

Considerare i conteggi una baseline, non un limite per aggiunte future. Leggere il riferimento per i percorsi esatti dei sorgenti e gli aggiornamenti inglesi già inclusi.

### Vincolo prioritario: mappe immutate

Quando richiesto «senza cambiarle in alcun modo», conservare **testi, esempi, tabelle, immagini, colori, numerazione delle mappe, ordine, coppie di argomenti e impaginazione interna**. Non correggere silenziosamente neppure eventuali errori: segnalarli a parte. Aggiungere solo la veste editoriale richiesta, aggiornare paginazione e navigazione. Verificare HTML byte-identico e tutte le pagine delle mappe per testo e pixel, escluso il footer. Non dichiarare equivalenza visiva sulla sola base del testo estratto.

## Veste FACILE (precede le vecchie regole della copertina)

1. Copertina autonoma: titolo esatto italiano, banner terracotta, illustrazione clay adulta, tre righe di sottotitolo, spazio nome/classe/anno; nessun numero visibile.
2. Quattro pagine guida: «Una scheda alla volta», «Cinque anni: come orientarsi», «Per chi accompagna lo studio», «Colori e parole-guida».
3. Indice a una colonna su pagine separate: titoli **e** numeri cliccabili, numeri automatici con `target-counter`.
4. Mappe originali in ordine, con numero di pagina e «Torna all’indice ↑» nel footer.
5. Mantenere OpenDyslexic 14pt nelle mappe. Per il frontespizio seguire il modello latino: titolo 30pt, sottotitoli 15pt, intestazioni guide 18pt, corpo 14pt e dimensioni ausiliarie documentate nel CSS. La vecchia uniformità 14pt NON prevale su questa veste richiesta.
6. Non presentare la guida quinquennale come programma ministeriale completo o elenco di obiettivi minimi; distinguerla dalle decisioni PEI/PDP. Non inventare esercizi, soluzioni o un atlante che il quaderno non contiene.

## Flusso contenuti — nuova lingua o nuove mappe

1. Leggere `references/semplificazione.md` per il contenuto delle mappe; per la copertina usare invece `references/collana-facile.md`.
2. Solo per una NUOVA lingua, inizializzare:
   ```bash
   python3.11 /home/user/skills/quaderno-mappe-lingue/scripts/nuovo_quaderno.py de --titolo "MAPPE CONCETTUALI DI GRAMMATICA TEDESCA"
   ```
   Non eseguire lo scaffold su cartelle esistenti.
3. Compilare il build con `B_(titolo, colore, icona, caption, contenuto)` e `PAGE()`. Tipi: `F` formula, `X` esempio, `P` coppie, `T` tabella, `R` regole, `N` nota. Mantenere spiegazioni italiane brevi e concrete, esempi nella lingua studiata.
4. Scegliere icone dal catalogo `references/catalogo-icone.md`: clay adulto, coerenti con il significato; riutilizzare quelle disponibili. Non rigenerare media già approvati né correggere immagini a pagamento senza richiesta/consenso.
5. Accoppiare le mappe nuove per affinità quando entrano leggibili; non cambiare gli accoppiamenti preesistenti per un semplice restyling.
6. Renderizzare il PDF base con `scripts/render_quaderno.py`, verificare con `scripts/verify_quaderno.py` e controllare visivamente le pagine cambiate.
7. Aggiornare la collana con il workflow dettagliato nel riferimento; mantenere sincronizzati HTML e PDF sorgenti usati come baseline.
8. Consegnare con `send_attachment` tutti i PDF richiesti. Non consegnare solo copertine o appunti al posto dei quaderni completi.

## Risorse specifiche della collana

- `references/collana-facile.md`: geometrie, percorsi, baseline, comandi e insidie verificate.
- `scripts/prepara_collana_facile.py`: copiare asset mancanti e costruire inventario dai sorgenti effettivi; non sovrascrivere immagini approvate.
- `scripts/build_collana_facile.py`: conservare HTML/CSS delle mappe e costruire frontespizio, guide e indice; variabile `LF_WORKDIR` per la cartella di lavoro.
- `scripts/verifica_collana_facile.py`: controllare testi/pixel di OGNI pagina, link e numeri dell’indice; terminare con errore in caso di differenze non autorizzate.
- `templates/collana-facile/`: tre illustrazioni approvate e anteprima delle copertine. Non generarle di nuovo per ricostruire la stessa edizione.

PDF: usare il profilo WeasyPrint `pdf/ua-1`, lingua generale italiana (guide/spiegazioni italiane), alt descrittivi e segnalibri. `Marked: True` e profilo richiesto non costituiscono da soli una certificazione completa di conformità: non dichiarare una validazione specialistica non svolta.

