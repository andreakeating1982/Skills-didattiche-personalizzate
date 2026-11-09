# VERSIONI, APPENDICI E PRIVACY — CONSOLIDAMENTO 1 NOVEMBRE 2026

Leggere prima di modificare un PDF già consegnato, aggiungere un’appendice o scegliere il PDF da leggere. Le istruzioni recenti dell’utente e il nuovo allegato destinato al lavoro prevalgono sui percorsi storici. Il numero di versione più alto non prova da solo che la base sia corretta.

## PRIORITÀ CORRENTE — SPECCHIETTI E BOX ILLUSTRATI

**Ultima correzione dell’utente:** sintesi come vere tabelle a due colonne con tutte le righe necessarie; **MAPPA CONCETTUALE FINALE** a box semplici senza connettori, con piccole immagini clay esplicative interne. Interlinea e dimensione uguali al corpo per entrambi. Nessun limite di cinque righe per questi supporti. Registro storico dei PDF ancora nel perimetro: BES v23, studio v9, metodologie v14, classe serena v8 e regole/bilingue/VR/mappa6passi v5. Per la raccolta corrente prevale il registro scientifico del 2 novembre, con otto articoli e il ritiro vincolante del codice 05. Registro corrente [raccolta-specchietti-box-2026-11.json](raccolta-specchietti-box-2026-11.json); standard [sintesi-e-mappa-finale.md](sintesi-e-mappa-finale.md); sorgenti metodologie correnti in `../templates/metodologie-v14/`. **Le prescrizioni successive di questo file su v13 invariata o massimo cinque righe in mappe/sintesi sono STORICHE, non applicabili all’ultima edizione.** Restano gli invarianti del corpo, privacy, fonti e aperture. Gli audio non si rigenerano automaticamente.

## AGGIORNAMENTO STORICO PRECEDENTE — IN SINTESI E MAPPA FINALE

La richiesta successiva aggiunge gli elementi riepilogativi mancanti: **IN SINTESI a fine di ogni unità e MAPPA CONCETTUALE finale**. Le nuove edizioni sono BES v22, studio v8, classe serena v7, regole v4 e bilingue v4; metodologie v13, realtà virtuale v4 e mappa6passi v4 restano identiche. Nel bilingue sintesi e mappe sono in entrambe le lingue e indicate come supporti editoriali aggiunti. Registro completo con SHA-256 e pagine: [raccolta-sintesi-mappe-2026-11.json](raccolta-sintesi-mappe-2026-11.json); metodo: [sintesi-e-mappa-finale.md](sintesi-e-mappa-finale.md). Questo aggiornamento non riapre privacy, sezioni rimosse, fonti o contenuti originari. Gli audio precedenti non sono automaticamente aggiornati alle nuove sintesi/mappe; nessuna nuova generazione audio senza richiesta.

## AGGIORNAMENTO SUCCESSIVO — V13 IMMAGINE OGNI UNITÀ

Baseline storica delle aperture, poi mantenute nella v14: **v13 IMMAGINE OGNI UNITÀ (29 pagine)**: una sola immagine immediatamente dopo OGNI banner delle dieci unità, prima di sottotitolo e testo. Eliminare solo le seconde illustrazioni nella stessa unità; la selezione di cinque sole unità della v12 era errata. Conservare gli inizi pagina della v12, i titoli/colori della v11 e la radice v8 riparata. La v11 è stata rifiutata per gli inizi pagina: ciascuna delle dieci unità, mappe finali, fonti e appendice deve iniziare su una nuova pagina. Compattare solo entro l’unità, mai fra unità distinte. Leggere `titoli-centrati-reflow-metodologie-v11.md` e il registro `baseline-metodologie-v13.json`: titoli centrati/coordinati ai banner, copertina + 10 immagini di apertura, nessuna seconda immagine, bibliografia conservata senza etichette ripetute. Sorgenti completi inclusi in `../templates/metodologie-v13/`. Non tornare a v8 per una correzione successiva; la v8 sotto documenta la radice corretta e la regressione risolta.

Audio corrente **v9 senza lettura delle fonti, 20:30**, con Peer tutoring approvato; non il vecchio integrale da 26:24. Leggere `didattica-media-audio-3d/references/montaggio-approvato-senza-fonti.md`. Rimpaginazione e centratura non richiedono una nuova registrazione.

## SCEGLIERE LA BASE PRIMA DI SCRIVERE CODICE

1. Identificare il documento e lo scopo: restyling, rimozione, appendice, modifica al testo o sola lettura. Usare direttamente il PDF appena allegato se l’utente chiede l’audio di quel file. Se l’allegato manca, cercarlo nei file disponibili, poi chiedere di ricaricarlo; non riprendere una vecchia edizione in silenzio.
2. Registrare nome, percorso, SHA-256, numero di pagine, titolo e modifiche/rimozioni già approvate. Leggere l’intero documento e identificare il sorgente HTML/CSS/font/media corrispondente. Non assumere che l’HTML più recente nel nome appartenga al PDF scelto.
3. Controllare le dipendenze degli script: una riga `OLD=.../metodologie_build` o un template storico può reintrodurre tic, titoli, diagnosi o box rimossi anche se il nuovo output si chiama v7. Non eseguire uno script vecchio senza leggerne input, CSS copiati e sostituzioni.
4. Lavorare in nuova cartella versionata. Non sovrascrivere la base approvata. Nel rapporto distinguere **base scelta**, **modifiche autorizzate**, **parti da preservare**, **controlli svolti**.
5. Confrontare contro la base effettivamente approvata, non contro l’input sbagliato dello script. Un test «identico al pixel» contro una bozza regressiva non dimostra conservazione del lavoro approvato.

## REGRESSIONE DELLE METODOLOGIE: LEZIONE DA NON RIPETERE

- La base grafica approvata è **BOX RIVISTI v5**: nuclei coerenti, niente freccette/spunte ornamentali e massimo cinque righe effettive compreso il sottotitolo.
- L’appendice delle edizioni v4–v7 della cartella `metodologie_appendice` era stata agganciata per errore alla **rimpaginazione v2**, non alla v5. Quelle edizioni non sono una base grafica da riutilizzare.
- Edizione riparata: **v8 BASE CORRETTA**, titolo esatto **10 METODOLOGIE DIDATTICHE INCLUSIVE**. Base v5 conservata; copertina/indice aggiornati; appendice con fonti alle pagine 33–35. Pagine 2–32 identiche al pixel alla v5 nella verifica eseguita. Totale 35 pagine, 113 contenitori e 68 unità strutturate misurati, massimo cinque righe: dati di questa edizione, non quote universali.
- Impronte degli artefatti verificati e relazione v5/v8 nel registro portabile **`baseline-metodologie-v8.json`**. Il registro non include i PDF completi e non sostituisce la verifica del file disponibile.
- Percorsi locali: `/home/user/metodologie_v8_BASE_CORRETTA/10_METODOLOGIE_DIDATTICHE_INCLUSIVE_v8_BASE_CORRETTA.html` e `.pdf`; rapporto `verifica/PROVENIENZA_E_CONFRONTO.json`; sorgenti `10_METODOLOGIE_v8_BASE_CORRETTA_SORGENTI.zip`.
- Per ricostruire proprio la v8, se manca usare lo ZIP di quella edizione o richiederla; per una nuova modifica usare invece i sorgenti correnti v13 inclusi. La v5 è il riferimento del corpo, non contiene da sola l’appendice. Non rieseguire `metodologie_appendice/aggiungi_appendice.py`: il suo input v2 è superato. La v8 è una baseline editoriale, non una certificazione giuridica delle sue frasi.

## APPENDICE SENZA ALTERARE IL QUADERNO

1. Preservare esattamente le sezioni approvate: raggruppamenti dei box, paragrafi, enfasi, titoli, immagini, font, palette e ordine. Non ricostruire il corpo da testo estratto né raggrupparlo di nuovo con un algoritmo di lunghezza.
2. Aggiungere l’appendice come **sezione sorella** dopo il corpo e le fonti originarie, non annidata dentro la bibliografia. Usare id univoci, titoli realmente maiuscoli, box sobri e fonti proprie dell’appendice. Per modifiche minime non riorganizzare tutte le fonti del quaderno.
3. **Conservare le voci originali dell’indice della prima pagina**: testo, ordine, link e stile. Quando richiesto, aggiungere soltanto la voce APPENDICE, con destinazione e pagina automatiche; ciò non autorizza a riscrivere o compattare l’intero indice. Se non entra, segnalare il vincolo invece di cancellare voci o ridurre caratteri/immagini.
4. Verificare DOM delle sezioni preesistenti e hash di immagini/font; confrontare testo ed enfasi. Ispezionare copertina, passaggio alle nuove pagine, appendice e fonti. Solo se geometria e renderer restano uguali, confrontare anche le pagine non toccate al pixel; altrimenti dichiarare il reflow e verificarne gli invarianti, senza pretendere uguaglianze impossibili.
Per il confronto pixel portabile usare `scripts/confronta_baseline_pdf.py base.pdf nuovo.pdf --baseline-sha256 HASH_APPROVATO --pages 2-32 --report confronto.json`, dopo aver stabilito quali pagine devono restare identiche. L’hash va calcolato sulla baseline realmente approvata, non copiato da un file scelto per comodità.

5. Controllare tutte le LineBox, incluse intestazioni, celle e nodi. Il limite di cinque righe è un tetto, non un criterio di accorpamento. Nessun box spezzato, overflow nascosto o ritorno di marcatori tramite `::before`/CSS esterno. Conservare le frecce semantiche negli esempi e i segni matematici.

## CONTENUTO DELL’APPENDICE SUI PERCORSI SCOLASTICI

Quando è richiesta una nuova stesura o revisione di merito, collegare esplicitamente l’appendice alle dieci metodologie: strumenti inclusivi applicabili a tutti; cambiano obiettivi e percorso individualizzato, non l’appartenenza di una metodologia a una categoria di alunni. Distinguere percorso ordinario/personalizzato con prove equipollenti e percorso differenziato secondo il PEI nella secondaria di secondo grado. Chiarire che l’equipollenza riguarda il valore e gli effetti legali delle prove, non l’identità materiale delle prove né un automatismo diagnostico. Non assegnare un percorso solo dalla «gravità» o dalla diagnosi, né confondere PEI e PDP. Spiegare a chi si applica ciascun documento, l’esito diploma/attestato e il ruolo degli organi competenti verificando la normativa vigente.

Non usare la bibliografia già stampata come prova della sua esattezza: verificare articoli, titoli e atti su fonti primarie quando si interviene sul contenuto. Una lettura fedele o una correzione grafica non autorizzano correzioni legali silenziose. «DVA» va spiegato, se presente nella fonte, come «diversamente abili»; preferire nel nuovo testo «studenti con disabilità».

## GUIDA BES: RIMOZIONI E RISERVATEZZA

- Non trascrivere diagnosi specifiche, codici clinici o dati identificativi dello studente. Parlare di bisogni educativi e disturbi in termini generali, senza conclusioni cliniche.
- Separare chiaramente **criteri generali BES/DSA** e **applicazione al profilo descritto**. Presentare bisogni e supporti come ipotesi didattiche da verificare con lo studente, le osservazioni e il PEI/PDP pertinente.
- Non inserire riferimenti a **Lingue Facili** nella guida BES o nel suo audio. Una revisione grafica non deve recuperarli da bozze precedenti.
- Nella revisione v20 è stata rimossa integralmente **8. VERIFICA, SCHEDA RAPIDA E REVISIONE**, con il relativo rimando. Conservare la rimozione; non eliminare altro. Riferimento locale: `/home/user/guida_bes_senza_sezione8_v20/ADATTARE_GLI_ESERCIZI_v20.pdf`.
- Conservare questa guida generale/applicata, distinta dal documento ritirato. Un nuovo allegato senza numero di versione è comunque la fonte dell’audio quando esplicitamente richiesto.
- Conservare l’eliminazione del box **Limiti** in «Una classe serena». Non reintrodurlo usando vecchi template.

## REVISIONI IMMAGINI — CLAY ADULTO A OGNI UNITÀ, FONTI ESCLUSE

Per nuove guide leggere `immagini-clay-adulto-unita.md`; per le metodologie applicare la v13: UNA immagine subito dopo OGNI banner, non una selezione di unità, togliendo soltanto le seconde immagini come descritto in `titoli-centrati-reflow-metodologie-v11.md`. La richiesta successiva dell’utente rende obbligatorie illustrazioni clay adulte in copertina e all’inizio di ogni unità tematica, non nelle fonti. Non conservare asset flat per il solo fatto che erano nell’allegato. Nei bilingui coprire entrambe le lingue con scene corrispondenti; mantenere testo/enfasi e usare immagini uniformi già approvate quando pertinenti. Baseline corrette: **Regole di classe CLAY ADULTO v2** (5pagine) e **Gestione della classe — originale/traduzione CLAY ADULTO v2** (43pagine). I numeri di pagine non sono vincoli futuri. Risorse riusabili nella skill, `templates/clay-adulto/manifest.json`; controllo di copertura in `scripts/verifica_copertura_immagini_unita.py`. Non ripartire dalle edizioni con JPEG flat o con la sola copertina illustrata.

## QUANDO L’AUDIO RESTA VALIDO

Una modifica di soli colori, box, maiuscole tipografiche o spazi non autorizza a rifare l’audio. Verificare prima se testo e ordine letti sono invariati. Storicamente v8 era compatibile con l’audio integrale v7. Dopo la correzione approvata di Peer tutoring e l’esclusione delle fonti, usare l’MP3 v9 senza fonti: resta compatibile con le revisioni grafiche v10/v11/v12/v13. Se cambia una frase, una sezione, una fonte o il loro ordine, rivalutare la corrispondenza e generare un nuovo audio solo quando richiesto. Per la costruzione leggere `didattica-media-audio-3d/references/audio-pdf-due-voci.md` e la skill generale `audio-generation`.

