# REALTÀ VIRTUALE A SCUOLA — VERSIONE CHIARA APPROVATA, 5 NOVEMBRE 2026

## Stato e precedenza

L’utente ha approvato esplicitamente il PDF appena ricreato: «perfetto nell’impaginazione, negli elementi presenti, nelle 10 domande». Ha approvato anche il podcast collegato. Questa è la **baseline corrente dell’articolo specifico**; l’edizione scientifica v7 da 16 pagine e 8 domande resta uno snapshot storico approvato della raccolta precedente. Non modificare retroattivamente gli archivi già consegnati e non rigenerare nulla per il solo aggiornamento delle skill. Se viene richiesto un nuovo archivio con l’ultima versione, scegliere questa baseline per il codice 08, mantenendo gli altri documenti e le rispettive eccezioni.

- PDF esatto: `../templates/realta-virtuale-chiara-approvata-2026-11-05/REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.pdf`.
- SHA-256: `5dcc0e4b22acb02941ae3fae3a9cb6f7ad1e672fb829907a5c04d435e2720e76`. Controllare l’impronta prima di lavorare; per una copia identica riusare i byte del PDF, non renderizzare di nuovo.
- Sorgente HTML/CSS, font OpenDyslexic, immagini, manifest dei supporti e dati editoriali sono nello stesso template. Il JSON contiene anche chiave e motivazioni **interne** delle risposte: non pubblicarle nel PDF o nel podcast salvo richiesta. Il JSON è un registro editoriale, non un generatore automatico; non promettere che modificarlo aggiorni l’HTML.
- Il podcast approvato, il relativo PDF e i materiali audio sono documentati in `didattica-media-audio-3d/references/podcast-vr-approvato-2026-11-05.md`. PDF e podcast appartengono alla stessa revisione: confrontare gli SHA-256, non usare il vecchio audio della v7.

## Anatomia dell’esempio approvato

I numeri seguenti descrivono questo caso concreto, non quote per tutte le guide.

| Pagine | Contenuto |
|---|---|
| 1 | Titolo e sottotitolo, immagine e SOMMARIO colorato e cliccabile con cinque unità, verifica, mappa e bibliografia. |
| 2–3 | 1 LA REALTÀ VIRTUALE (VR), con sintesi. |
| 4–5 | 2 LA REALTÀ AUMENTATA (AR), con sintesi. |
| 6–7 | 3 LA REALTÀ MISTA (MR), con sintesi. |
| 8–9 | 4 LA REALTÀ ESTESA (XR), con sintesi. |
| 10–12 | 5 LE XR A SCUOLA, con sintesi. |
| 13–14 | VERIFICA DI COMPRENSIONE: 10 domande, 5 per pagina, quattro opzioni A–D in griglia 2×2; nessuna soluzione mostrata. |
| 15–16 | MAPPA CONCETTUALE FINALE: 7 nodi, 4 e 3, raggruppati in tecnologie immersive e XR a scuola. |
| 17 | Quattro RIFERIMENTI BIBLIOGRAFICI in box crema, link cliccabili e firma «Articolo scritto da ANDREA CENTINARO.» |

## Scelte da conservare

1. Usare titoli editoriali MAIUSCOLI e centrati, indice e banner di colori coordinati, OpenDyslexic, pagina bianca e box crema, parole chiave del corpo in neretto nero selettivo. Rispettare il flusso: riempire prima la prima facciata di ciascuna unità con i box interi che entrano; non spostare forzatamente testo per bilanciare le pagine.
2. Mantenere una figura clay pertinente subito dopo il banner di ciascuna unità tematica, senza seconda figura decorativa nell’unità e senza immagini nelle fonti; l’indice ha la propria immagine. Conservare esattamente le immagini già approvate. Un restyling solo grafico non autorizza riscritture né nuovi supporti.
3. Linguaggio chiaro e concreto, definizioni spiegate alla prima occorrenza e termini tecnici comprensibili attraverso esempi; mantenere distinzioni, limiti e riferimenti effettivi. Nella VR non confondere immersione, presenza e apprendimento; non attribuire automaticamente alla tecnologia efficacia o accessibilità universale.
4. Ogni unità teorica dell’esempio termina con una tabella IN SINTESI a due colonne e **tutto Regular 400**, comprese intestazioni e parole chiave; il corpo mantiene i propri neretti. Cinque tabelle, 25 righe nell’esempio, interlinea 1,85. Sintesi nelle sole unità teoriche, salvo supporti preesistenti da conservare nel restyling.
5. Conservare integralmente le **10 domande approvate di questo documento**, le 40 opzioni, l’ordine e le risposte interne. Le domande sono chiare, con una sola risposta corretta, basate sui contenuti delle cinque unità; non introdurre risposte nel PDF. Per altri articoli 10 non diventa un obbligo universale: adattare quantità e difficoltà a pubblico, contenuto e richiesta, mantenendo la regola 5–10 salvo indicazioni diverse.
6. Mantenere nella mappa 7 box di **78×78 mm**, immagini di **52×29,373 mm**, solo parole chiave leggibili e interlinea del corpo. Possono esserci più di due parole chiave pertinenti: se non entrano, distribuirle fra nodi/pagine, non ridurre la tipografia. Non sostituire automaticamente le figure dell’esempio: alcune scene sono riutilizzate anche in nodi connessi e questa versione è stata approvata. Per altre mappe seguire la regola generale delle scene pertinenti e differenziate quando richiesta.
7. Mantenere gli specifici quattro riferimenti e i rimandi numerati dell’articolo; non attribuire consultazioni non avvenute. La nota W3C non è una norma di conformità; la rassegna Radianti riguarda l’istruzione superiore. Una fonte valida o un DOI raggiungibile non certifica da solo ogni affermazione.

## Controlli prima di modificare o consegnare

- Controllare hash, 17 pagine, titoli, tutte le domande/opzioni e parole chiave, corpo e sintesi, ordine, font, immagini e indice/link; verificare visivamente le pagine interessate.
- Usare `scripts/verifica_articolo_scientifico.py`, `verifica_specchietti_box.py`, `verifica_box_semantici.py`, `verifica_box_fonti.py` e `verifica_flusso_fonti_blog.py` sui sorgenti inclusi. Il rapporto fonti segnala come non classificata la firma finale, che non è una voce bibliografica: non eliminare la firma per far sparire l’avviso.
- Leggere semanticamente difficoltà e correttezza delle alternative: i controlli automatici non le certificano. Un PDF taggato o prodotto con l’opzione PDF/UA non equivale a certificazione indipendente di conformità.
- Dopo una modifica autorizzata creare un nome di output diverso; conservare intatti gli esemplari approvati e confrontare parole, enfasi, supporti, geometria, immagini e link non interessati. Cambi solo grafici non richiedono un nuovo podcast se testo e ordine rimangono compatibili.

