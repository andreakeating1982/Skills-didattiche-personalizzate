# TITOLI, IMMAGINI DI APERTURA E INIZI PAGINA — METODOLOGIE V13

## REGOLA PRIORITARIA — UNA IMMAGINE DOPO OGNI BANNER

In ciascuna delle dieci unità rispettare **titolo nel banner → UNA immagine clay adulta → sottotitolo e testo**. Non interporre paragrafi o sottotitoli prima dell’immagine. È superflua la SECONDA illustrazione nella stessa unità, non l’immagine di apertura. La precedente selezione di cinque unità illustrate e la collocazione dopo il primo nucleo erano errate: la v13 le corregge ripristinando le dieci prime immagini originali della v8, senza recuperare il suo vecchio layout o contenuto regressivo. Copertina conservata: **11 immagini totali**, nessuna nelle sezioni finali del modello corrente. Grafici/diagrammi funzionali di altri documenti non sono figure decorative da togliere automaticamente.

Verificare `scripts/verifica_aperture_unita.py HTML --manifest templates/metodologie-v13/aspettative-aperture.json --report REPORT --strict`: numero esatto per unità, sibling immediato del banner e stessa pagina nel renderer. Eseguire anche il controllo di copertura; non disattivarlo con un manifest selettivo. Affiancare misure delle immagini nel PDF e ispezione delle dieci aperture.

## REGOLA CUMULATIVA — NUOVA PAGINA PER OGNI UNITÀ E SEZIONE FINALE

**Ogni unità 1–10 deve SEMPRE iniziare su una NUOVA pagina.** Anche la sezione delle mappe finali, FONTI E RIFERIMENTI e l’APPENDICE iniziano ciascuna su una nuova pagina. La compattazione è solo INTERNA alla stessa unità/sezione: non accodare la nuova unità nello spazio lasciato dalla precedente. Un margine residuo imposto da questo confine è accettabile e non si corregge annullando l’interruzione. Non imporre un numero fisso di pagine né comprimere il font. La v11 con flusso continuo fra unità è stata rifiutata: conservarne titoli/colori/testi ma non la paginazione. Per questo PDF i 13 confini principali sono `sec1`…`sec10`, `mappa`, `fonti`, `appendice`. I nodi, i sottotitoli e le sintesi interne non sono nuove unità.

CSS corrente: `body > section.sec, body > section#fonti {break-before:page;page-break-before:always;break-inside:auto}`; azzerare il margine superiore dell’h2 di apertura. Conservare i box indivisibili, non rendere indivisibile tutta un’unità multipagina. Verificare il PRIMO frammento della sezione, posizione in cima al foglio e assenza di contenuto estraneo sulla pagina di apertura con `scripts/verifica_inizi_pagina.py HTML --manifest templates/metodologie-v13/aspettative-inizi-pagina.json --report REPORT --strict`. Il test degli inizi sulla v11 deve fallire e sulla v13 deve passare; la v12 passa gli inizi ma NON il nuovo controllo delle aperture: la presenza della sola regola CSS non è una verifica sufficiente.

La base corrente è **v13 IMMAGINE OGNI UNITÀ**, 29 pagine. I percorsi con v11 nel nome di questo riferimento sono storici; il contenuto aggiornato e il registro v13 prevalgono.

Leggere per correggere centratura/colori dei titoli, ridurre spazi bianchi o scegliere l’ultima edizione delle metodologie. Applicare le richieste esplicite più recenti prima dei modelli storici. Non estendere le eccezioni di questo PDF a tutte le altre collane.

## TITOLI CENTRATI E COLORATI

- Mantenere tutti i titoli e sottotitoli editoriali in MAIUSCOLO reale e **centrarli orizzontalmente nel proprio contenitore**: titolo principale, banner di capitolo, sottosezioni, sintesi, mappe/nodi, fonti e appendice. Centrare le etichette/intestazioni delle tabelle nella propria cella, non rispetto all’intero foglio.
- Assegnare ai titoli prima neri su sfondo chiaro il colore effettivo del banner dell’unità. Riusare la palette esistente: non inventare una tinta simile. Conservare bianchi i titoli già bianchi sui banner colorati, per non renderli invisibili.
- Coordinare anche i richiami alle singole unità nella mappa e nella bibliografia. Per l’appendice usare il suo colore; per le sezioni comuni usare quello del loro banner.
- Conservare corpo, citazioni e parole chiave in neretto neri e allineati a sinistra. Non trattare ogni `<strong>` come titolo. Non centrare automaticamente le voci dell’indice: conservarne testo, rientri sospesi, struttura, palette e allineamento approvati.
- Non imporre una geometria nuova alle mappe/esercizi specialistici; conservare il centro dei rispettivi nodi e il modello richiesto. Una correzione dei titoli non autorizza nuove immagini, reflow generale, riscrittura o rigenerazione audio.

### CSS E VERIFICA EFFETTIVA

Controllare inline style, selettori con id, variabili e `!important`: una regola `color:var(--section-color)!important` può vincere sul nuovo `color` inline se la variabile resta quella vecchia. Aggiornare coerentemente la variabile locale quando serve. Non applicare una regola indiscriminata che colori di nuovo il corpo o i titoli bianchi.

Usare `scripts/verifica_titoli_centrati.py HTML --expectations MANIFEST --report RAPPORTO --strict`. Se il manifest è assente, il controllo misura centratura ma non certifica l’abbinamento cromatico. Il manifest deve avere `titles: [{id, expected_color}]`; esempio completo incluso in `templates/metodologie-v13/aspettative-titoli.json`.

Misurare ogni `LineBox` rispetto al centro del contenitore, oltre a verificare lo stile calcolato: `text_align_all` nelle versioni recenti di WeasyPrint, con fallback `text_align`. In una cella stretta l’etichetta sembra spostata rispetto al testo della colonna destra anche quando è correttamente centrata. Risolvere dubbi visivi con coordinate reali; non ignorare un difetto effettivo né rigenerare a tentativi. Il report non certifica contrasto, semantica o PDF/UA.

## RIDUZIONE DEGLI SPAZI VUOTI SU RICHIESTA

1. Partire dall’ultima versione corretta e preservare paragrafi, enfasi, ordine, titoli, voci dell’indice e bibliografia. Non recuperare una base vecchia solo perché lo script è già pronto.
2. Rimuovere SOLO interruzioni interne premature e wrapper indivisibili troppo grandi. Non togliere MAI gli inizi pagina delle dieci unità, delle mappe finali, delle fonti e dell’appendice per riempire il foglio precedente. Mantenere insieme titolo e primo testo, box e righe di tabella; consentire a una lunga sintesi di proseguire per righe complete senza spezzare celle. Non modificare i nuclei di significato per riempire carta.
3. Se l’utente chiede meno immagini, eliminare le SECONDE illustrazioni nella stessa unità, conservando l’immagine subito dopo il banner di OGNI unità e tutti i sottotitoli/testi. Non selezionare alcune unità a scapito di altre e non escludere controlli di copertura.
4. Non collocare l’immagine dopo il primo nucleo di testo per risparmiare spazio. Tenere banner e unica immagine sulla pagina di apertura, con sottotitolo e primo testo a seguire; mantenere dimensioni comuni e stile clay adulto. Non ridurre immagine o font per conservare un vecchio totale di pagine.
5. Ridurre padding/margini decorativi, non font, interlinea o margini della pagina. Nessun contenuto tagliato, overflow nascosto o pagina compressa artificialmente. Il totale delle pagine è un risultato, non una quota.
6. Confrontare DOM e `<strong>` prima/dopo, immagini rimaste per hash, LineBox di tutti i box/celle (max cinque), indice automatico e link. Controllare tutte le pagine renderizzate. Nel verificare le destinazioni usare la **prima** pagina che contiene l’ancora, non sovrascriverla con le continuazioni della sezione; PyMuPDF può riportare `LINK_NAMED` oltre a `LINK_GOTO`.

## FONTI: TRE OPERAZIONI DISTINTE

- **PDF:** eliminare soltanto l’etichetta ripetuta «Fonti:» prima delle citazioni e l’etichetta equivalente «Fonti normative:» nell’appendice. Conservare i titoli **FONTI E RIFERIMENTI / FONTI DELL’APPENDICE**, tutte le citazioni, URL e norme. Non fare sostituzione globale della parola FONTI.
- **Audio:** escludere gli elenchi bibliografici soltanto quando richiesto; per le metodologie è stato richiesto esplicitamente, comprese le fonti dell’appendice. Non cancellare autori o riferimenti normativi utili dentro le spiegazioni. Leggere `didattica-media-audio-3d/references/montaggio-approvato-senza-fonti.md`.
- **Contenuto:** una modifica grafica non è una revisione normativa. Verificare fonti primarie se si aggiorna il merito; non introdurre correzioni legali silenziose.

## ULTIMA VERSIONE DA RIUTILIZZARE

- **PDF v13 IMMAGINE OGNI UNITÀ:** `/home/user/metodologie_immagine_ogni_unita_v13/10_METODOLOGIE_DIDATTICHE_INCLUSIVE_IMMAGINE_OGNI_UNITA_v13.pdf`.
- SHA-256: `5454c1aa4f29a8d4bb8abd3a5e5d4b4364d39c866175ea290ce072db6a595f7c`.
- **29 pagine**, **11 immagini** (copertina + UNA subito dopo il banner in ciascuna delle dieci unità); 111 titoli/intestazioni controllati, 127 righe centrate nel renderer. Queste quantità descrivono il caso, non sono standard per altri PDF.
- Derivazione: v5 BOX RIVISTI → v8 BASE CORRETTA (35 pagine, 21 immagini) → v10 RIMPAGINATO (23 pagine, 6 immagini, senza etichette ripetitive nelle fonti) → v11 (centratura e colori, ma inizi pagina non conformi) → v12 (inizi pagina corretti ma immagini di apertura insufficienti/mal collocate) → **v13 (inizi pagina preservati e UNA immagine subito dopo OGNI banner)**. Non riutilizzare il flusso continuo v10/v11. Non tornare a v8 per una successiva correzione grafica e non usare le v4–v7 con appendice regressiva.
- **Sorgenti portabili inclusi** in `templates/metodologie-v13/`: HTML, CSS, font, le 11 immagini effettivamente usate, script di render, aspettative dei titoli e manifest dei 13 inizi pagina e delle 10 aperture illustrate. Copiare la directory in una nuova cartella di lavoro prima di modificarla. `python3 render_pdf.py` ricrea il documento con WeasyPrint; hash binario e a volte paginazione dipendono dall’ambiente, perciò ricontrollare gli invarianti e non promettere un hash identico dopo rigenerazione.
- Leggere `references/baseline-metodologie-v13.json` per percorsi, impronte dei file e dettagli della compatibilità con l’audio corrente. Il PDF completo e l’MP3 non sono allegati alla skill: se mancano, ricreare il PDF dai sorgenti inclusi; recuperare/chiedere l’MP3, non rigenerarlo automaticamente.

### INIZI DELLA VERSIONE CORRENTE (ESITO, NON QUOTA UNIVERSALE)

Unità 1–10: pagine **2, 4, 6, 8, 10, 12, 14, 16, 18, 20**. Mappe di sintesi: **22**; fonti: **24**; appendice: **27**. Le sezioni possono proseguire su più pagine senza che le unità successive si accodino. Indice originale conservato e numeri automatici aggiornati. Audio v9 senza fonti invariato: testo e ordine del PDF non sono cambiati.

## IMMAGINE SEPARATA PER IL POST

Riutilizzare `templates/post-blog/metodologie-inclusive.png` per questo post: titolo esatto **10 METODOLOGIE DIDATTICHE INCLUSIVE**, lavagna verde scuro e legno, plastilina adulta opaca, docente e adolescenti al tavolo ovale, palette salvia/terracotta/crema e luce calda. Nessuna scritta AUDIO, AUDIO INTEGRALE o PDF. È un asset per il post, non una sostituzione automatica della copertina interna del PDF.

Per nuove immagini del blog osservare la pagina pubblica con il browser e usare un asset approvato come riferimento con gli strumenti media. Non usare Python per ritocchi. Una sola generazione per la richiesta; errori da mostrare e correggere solo con consenso. Non produrre media per collaudare una skill.

