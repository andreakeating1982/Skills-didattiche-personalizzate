# LÁZARO CARRETER — CONTENUTI APPROVATI E FLUSSO CORRETTO (5 NOVEMBRE 2026)

## ULTIMA VERSIONE CONSEGNATA — MAPPA E INDICE CORRETTI

Per ogni successiva modifica di Lázaro partire dal PDF `templates/lazaro-carreter-indice-2026-11-05/LAZARO_CARRETER_INDICE_CORRETTO.pdf` (32 pagine; SHA-256 `bc2e603157991cc978b86a28b60c4eaee8ffb1acce2d47b933e47b8416a776ec`) e dal sorgente portabile `LAZARO_INDICE_ARIOso.html` con `media/` nella stessa cartella. È la versione più recente consegnata; non risulta un'approvazione esplicita successiva alla correzione dell'indice.

- Indice in prima pagina, arioso e cliccabile: la voce della traduzione è **solo `TRADUCCIÓN AL ITALIANO`**. Non ripristinare il titolo italiano nell'indice; conservare invece la traduzione completa nel corpo. Le altre voci e i link restano. Il minimo di 10,2 mm per riga è una misura di questo esempio, non un valore obbligatorio per altri indici. Non ridurre caratteri/immagini o alterare il resto per creare più spazio.
- Conservare il testo spagnolo, la traduzione italiana e i 14 specchietti (sette per lingua), la mappa originale del Lazarillo, le fonti e le note. Non reinserire la verifica di 10 domande **in italiano** né la mappa **in italiano**, eliminate su esplicita richiesta. Mantenerne invece la versione spagnola: 10 domande e una mappa con sette box.
- Nella mappa spagnola possono figurare **più di due parole chiave** per box: la versione consegnata ne contiene tre in ogni nodo, ma non è una quota da estendere ad altre mappe. Conservare la correttezza, la pertinenza e la leggibilità dei termini, i box 78×78 mm e le immagini clay adulte 52×29,373 mm, evitando tagli e sovrapposizioni.
- I rapporti nella cartella del modello sono `QA_FINALE.json`, `QA_REVISIONI_LAZARO_BECQUER.json` e `QA_SUPPORTI_ES.json`. Le ultime modifiche dell'indice hanno lasciato invariate al pixel le pagine 2–32 e le destinazioni dei link; il controllo non certifica PDF/UA. Per modifiche future verificare testo, enfasi, immagini, tutte le destinazioni con area positiva, numeri e corrispondenza delle voci d'indice, resa visiva e flusso prima-faccia.
- Le esclusioni della mappa e del quiz italiani valgono **per questo quaderno**, non per tutti i bilingui. Nei futuri progetti seguire le richieste esplicite e non aggiungere o togliere supporti nel solo restyling.

## STATO DELLA VERSIONE PRECEDENTE — STORICO

L'utente ha giudicato molto buoni contenuti e aspetto del quaderno completo, ma ha chiesto di correggere la distribuzione delle pagine. La versione **a flusso corretto** è stata preparata e verificata; al momento della consegna la nuova impaginazione è **in attesa del riscontro dell'utente**. Non attribuirle una successiva approvazione non ancora ricevuta.

- Versione completa, contenuti approvati salvo impaginazione: SHA-256 `5bf62376df7381101db819ef50d74b3891a926c4d69364ecd7c288d9950effbb`.
- Versione con flusso corretto: `templates/lazaro-carreter-flusso-2026-11-05/LAZARO_CARRETER_FLUSSO_CORRETTO.pdf`, SHA-256 `883c9b2fa1d8dc1ecb9f9ccc40341e8aa8c4ef6fbf8a07543d970511be2ed79d`. Sorgente portabile `LAZARO_FLUSSO_CORRETTO.html` e `media/` nella stessa cartella; report `QA_FINALE.json` e `QA_FLUSSO.json`.
- È la revisione del quaderno già consegnato, non un restyling a partire dall'allegato originario di 12 pagine. Preservare l'ultima edizione e non ricostruire il quiz originale più facile né cancellare le aggiunte concordate.

## REGOLA PER I PROSSIMI QUADERNI

Ogni capitolo, se previsto dal modello, inizia su pagina propria. **All'interno del capitolo riempire la prima facciata con il massimo possibile di blocchi integri, in ordine; collocare nelle successive solo il testo o i supporti rimanenti.** Applicare lo stesso principio alle transizioni successive. Non bilanciare le pagine e non trascinare blocchi avanti perché la pagina di coda sembri più piena.

- Rimuovere `break-before` superflui e contenitori `break-inside:avoid` che raggruppano forzatamente testo e sintesi; far fluire i blocchi individualmente. Conservare i reali vincoli `break-inside:avoid` dei singoli box, tabelle e domande e la sequenza banner → immagine → testo.
- Se il prossimo box integro non entra nello spazio rimanente, lasciarlo all'inizio della pagina successiva. Non saltarlo per far entrare un altro box né spostare il testo della pagina precedente; è corretta anche una pagina di coda con la sola sintesi se la tabella non entra intera prima.
- Non ridurre corpo, font OpenDyslexic, interlinea 1,85, immagini o margini; non spezzare un nucleo già coerente per riempire un vuoto. Rispettare i max 5 righi reali per box ordinario e non frammentare eccessivamente. Le sintesi restano intere, a due colonne e sempre Regular, anche nel titolo.
- Mantenere pagina autonoma delle unità, mappe e bibliografia ove già stabilito. Non spostare fra capitoli per riempire uno spazio. Conservare testi, enfasi, lingue, immagini, mappe, quiz, fonti, note e collegamenti; ricalcolare le pagine dell'indice sul PDF finale.
- Misurare ogni transizione, non solo la prima: spazio effettivo tra fine dell'ultimo box e fondo stampabile vs ingombro del successivo, con margini reali e titoli eventualmente associati. Ispezionare anche il PDF. Verificare `scripts/verifica_flusso_fonti_blog.py` con selettori compatibili; per l'ultima versione Lázaro:

```sh
python3 scripts/verifica_flusso_fonti_blog.py templates/lazaro-carreter-indice-2026-11-05/LAZARO_INDICE_ARIOso.html \
  --pdf templates/lazaro-carreter-indice-2026-11-05/LAZARO_CARRETER_INDICE_CORRETTO.pdf \
  --unita es1,es2,es3,es4,es5,es6,es7,it1,it2,it3,it4,it5,it6,it7 \
  --selettore-box '.blk, .lf-summary' --selettore-fonti '#bibliografia' --strict
```

Il controllo geometrico segnala candidati, non certifica contenuti, accessibilità o compatibilità di griglie/floating complessi: verificare il renderer e la coerenza semantica. Usare anche `verifica_box_semantici.py`, `verifica_box_fonti.py`, `verifica_specchietti_box.py`, controllo immagini mappa e link.

## ELEMENTI DELLA REVISIONE A FLUSSO CORRETTO — STORICO, SUPERATO

Prima delle successive eliminazioni richieste, la revisione a flusso corretto aveva pagina 2 non vuota, testo originale e traduzione, sette sintesi per lingua, dieci domande per lingua e due mappe, oltre a Lazarillo, cinque fonti e richiami cliccabili. **I conteggi storici di domande e mappe italiane non descrivono il modello corrente**: applicare le istruzioni dell'ultima versione all'inizio del riferimento.

Nel confronto delle 37 pagine prima/dopo si sono riportati **9 blocchi testuali** alla pagina precedente, senza alterare il DOM sostanziale, 20.312 caratteri PDF normalizzati, enfasi, 10 immagini o destinazioni. I cinque gruppi forzati `es4,it2,it3,it4,it7` non vanno reintrodotti. Il numero di pagine e di blocchi spostati è un risultato del caso, non un obiettivo generale. QA: 13 controlli superati; 14 sintesi, 20 domande, due mappe, 5 fonti e 15 voci d'indice preservate. PDF taggato non significa PDF/UA certificato.

