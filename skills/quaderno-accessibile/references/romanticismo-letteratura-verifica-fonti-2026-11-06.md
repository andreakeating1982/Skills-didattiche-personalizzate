# ROMANTICISMO LETTERARIO — VERIFICA E FONTI, 6 NOVEMBRE 2026

## Regola generale successiva

L'utente ha segnalato come grave l'omissione della verifica e dei riferimenti nella rimpaginazione e ha esplicitato che **devono essere sempre presenti nel PDF rimpaginato**. Nei successivi nuovi PDF didattici rimpaginati inserire esattamente dieci domande e una bibliografia finale anche se assenti dall'allegato; una specifica richiesta esplicita successiva può disporre diversamente. Non rigenerare in automatico i documenti precedenti, né annullare le eliminazioni puntuali già richieste.

## Revisione del caso

**Aggiornamento successivo:** la versione di 21 pagine sotto documentata è storica. Per la versione richiesta con consegna esatta della foto, domande più semplici e mappa ridotta leggere [Romanticismo letterario semplificato](romanticismo-letteratura-semplificata-2026-11-06.md). Non presentare la vecchia revisione come corrente.

- Fonte originale dell'utente: `2026-09-08T07-11-35-265Z_Romanticismo_Espanol_Literatura_quaderno_accessibile_v1.pdf`, SHA-256 `8546585c675b4d47bc93f5916bb382f0992ef173a51c28756e4593914c5f477e`.
- Prima rimpaginazione: `LITERATURA_DEL_ROMANTICISMO_RIMPAGINATO.pdf`, 17 pagine, SHA-256 `0adbeb0e9981f9ef903ce698e9720886478900cbe7e926028c839b8171c88082`; incompleta, non usare come versione finale.
- Revisione completa: `/home/user/romanticismo_letteratura_completa_2026_11_06/LITERATURA_ROMANTICISMO_VERIFICA_E_FONTI.pdf`, 21 pagine, SHA-256 `bd0859302a96e7b09c4aa454825466b9f3278bb87dde4e232d53983e53151923`. È la revisione completa preparata in seguito alla correzione, **senza attestare approvazione ulteriore non dichiarata**. `impagina.py`, `contenuti_estratti.json`, `dati_editoriali.json`, `quiz_referencias.json`, HTML e report QA nella stessa cartella; `media` fa riferimento alle immagini della rimpaginazione precedente. Per il recupero portabile procurarsi anche `media` e il CSS nel sorgente storico di Marco histórico. La chiave di risposta in JSON è materiale interno, non nel PDF.
- Verifica 10 domande/40 alternative in spagnolo, pp. 14–16; argomenti riferiti a quattro unità, non ad attività. Mappa disciplinare invariata, pp. 17–20. `REFERENCIAS BIBLIOGRÁFICAS` p. 21: 4 voci, 12 richiami nel testo. Indice aggiornato in p. 1.
- Il riferimento originale a *Horizontes* p. 210 è stato riportato in bibliografia, non asserire consultazione indipendente del libro. Ulteriori riferimenti consultati: Britannica, «Spanish (Castilian) Romantic literature»; Antonio García Jiménez, «Bécquer y los cimientos de la Biblioteca Nacional», BNE; Britannica, «Serafín Estébanez Calderón». Attribuire le nuove risorse alla revisione, non inventare che fossero fonti dell'autore originale.

## Gate e suoi limiti

Eseguire `python3 /home/user/skills/quaderno-accessibile/scripts/verifica_quiz_fonti_obbligatori.py documento.html --pdf documento.pdf` prima della consegna. Controlla numero di quesiti, quattro alternative A–D, bibliografia, richiami, ordine verifica → mappa → fonti, link nell'indice e alcune destinazioni PDF. Adattare i selettori da CLI se un altro modello usa classi diverse. Fallire/bloccare la consegna quando mancano quiz o bibliografia. Eseguire `python3 -m unittest discover -s tests -p test_verifica_quiz_fonti_obbligatori.py -v` nella skill. Completare sempre la verifica editoriale: il gate non dimostra unicità delle risposte, affidabilità/pertinenza dei riferimenti, puntuale destinazione semantica delle note o conformità PDF/UA.

