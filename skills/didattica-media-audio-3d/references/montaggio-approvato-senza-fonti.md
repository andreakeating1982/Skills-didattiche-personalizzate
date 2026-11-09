# CORREZIONI APPROVATE E AUDIO SENZA LETTURA DELLE FONTI

Applicare quando l’utente approva una traccia sostitutiva o richiede l’esclusione delle fonti. Non trasformare questa eccezione in un taglio automatico per tutti i PDF. Leggere anche `audio-pdf-due-voci.md` e `audio-generation` quando serve generare nuove voci; un semplice montaggio non richiede nuove chiamate di generazione.

## APPROVAZIONE PRIMA DELLA SOSTITUZIONE

1. Se la nuova lettura di una sezione è stata richiesta separatamente per l’ascolto, consegnare prima quella clip e lasciare invariato l’audio completo. Attendere il sì dell’utente prima del montaggio.
2. Una volta approvata, riutilizzare **esattamente quella registrazione**, verificandone SHA-256. Non generare un’altra lettura e non accelerarla di nuovo. Preservare le parti non toccate.
3. Preferire intermedi WAV PCM originali già verificati. Decodificare la clip approvata senza filtri aggiuntivi; confrontare i campioni nel master per controllare che il montaggio non cambi il contenuto. Una successiva esportazione MP3 non sarà byte-identica ai segmenti originali: dichiarare correttamente il livello del confronto.
4. Non applicare automaticamente nuova normalizzazione a clip già approvate: misurare loudness/true peak e controllare i raccordi, distinguendo la misura dal filtro realmente applicato. Conservare il volume e la velocità approvati salvo problema reale da discutere.

## ELIMINARE LA LETTURA DELLE FONTI, NON LE SPIEGAZIONI

- Identificare separatamente il capitolo bibliografico generale e gli eventuali blocchi delle fonti nelle appendici. Togliere tutti e soli gli elenchi richiesti.
- Conservare sintesi, mappa, spiegazioni dell’appendice e nomi/leggi integrati nel discorso. Il PDF mantiene i riferimenti: una rimozione dall’MP3 non autorizza a cancellarli dal documento.
- Se le fonti iniziano dentro la stessa clip della spiegazione, localizzare la fine dell’ultima parola completa e la pausa prima del titolo successivo con ASR temporizzato, forma d’onda/silenzio e ascolto mirato. Non tagliare soltanto su un timestamp stimato dall’ASR e non assumere che l’ultima parte del file sia tutta bibliografia.
- Tagliare nel silenzio senza residui del titolo successivo, click o parole mozzate. Non aggiungere crossfade sul parlato né una conclusione nuova non richiesta.
- Aggiornare titolo/metadati, lista dei capitoli, testo letto, esclusioni dichiarate e indice temporale. Usare «audio aggiornato senza lettura delle fonti», non «audio integrale» senza precisazioni.
- Decodificare completamente il nuovo MP3; verificare somma delle durate/pause e padding, inizio/fine della sezione sostituita, raccordo dopo la bibliografia rimossa e nuova conclusione. QA a campioni non significa audizione integrale.

## CASO CORRENTE: 10 METODOLOGIE DIDATTICHE INCLUSIVE

- La nuova metodologia 7 — Peer tutoring v2 è stata approvata esplicitamente: «sì, questa va bene, inseriscila nell’audio completo, ma eliminando anche dall’audio tutta la parte della lettura delle fonti». Non riaprire l’approvazione e non tornare alla vecchia registrazione.
- MP3 corrente: `/home/user/metodologie_audio_senza_fonti_v9/consegna/10_METODOLOGIE_DIDATTICHE_INCLUSIVE_AUDIO_PEER_TUTORING_CORRETTO_SENZA_FONTI_v9.mp3`.
- SHA-256: `1cf8b49e96177c5d8089ec8f515f7bfc1780171ae416d2115cb0d0680948ece8`. Durata **20:30**; due voci italiane, velocità originale **1,12×**, nessuna musica. Peer tutoring a **09:42**, appendice a **17:25**.
- Clip Peer tutoring approvata: `/home/user/peer_tutoring_rifatto_v2/consegna/10_METODOLOGIE_METODOLOGIA_7_PEER_TUTORING_NUOVA_LETTURA_v2.mp3`, SHA-256 `291d5244e7468e1200d68cb824e5bfa5ce9895c39fee8354f147230b0c0d6561`, circa **1:30**.
- Eliminati il capitolo **FONTI E RIFERIMENTI** e il blocco **FONTI DELL’APPENDICE**, inclusi i relativi elenchi normativi. Ultima frase conservata: «Obiettivi minimi: diploma. Curricolo differenziato: attestato.» Il taglio a 185,04 s riguarda **solo l’intermedio specifico** `14_appendice_norm.wav`, non è un parametro da riusare su un nuovo file.
- Testo/indice corrente: `/home/user/metodologie_audio_senza_fonti_v9/consegna/10_METODOLOGIE_AUDIO_SENZA_FONTI_TESTO_E_INDICE_TEMPORALE_v9.md`. Una copia portabile è inclusa in `templates/metodologie-senza-fonti/` insieme al registro delle impronte; l’MP3 non è incluso.
- La correzione non ha generato nuove voci: 11 sezioni originali preservate negli intermedi PCM, sostituzione della sola metodologia 7 e accorciamento dell’appendice alle fonti. Nessuna ulteriore accelerazione o filtro di normalizzazione; esportazione MP3 128 kbps.
- Il vecchio manifest audio v7 riporta un hash PDF storico che non coincide con il PDF ora presente a quel percorso. Non ripresentare quell’hash come verificato: il montaggio parte dall’audio storico con impronta verificata. Conservare la distinzione nel rapporto di provenienza.
- Il PDF corrente è **v13 IMMAGINE OGNI UNITÀ**, 29 pagine; provenienza v5 → v8 → v10 → v11 → v12 → v13. La v13 conserva titoli centrati/colorati e inizi pagina separati per le 10 unità, mappe finali, fonti e appendice; ripristina UNA immagine subito dopo ogni banner, nessuna seconda immagine. Le modifiche v10/v11/v12/v13 sono grafiche più la rimozione delle sole etichette bibliografiche non lette: **l’MP3 v9 resta valido**. Non riconsegnare al suo posto il vecchio MP3 di 26:24 con lettura delle fonti.

## PORTABILITÀ E LIMITI

Leggere `references/baseline-audio-metodologie-v9.json` per percorsi, impronte, esclusioni e indice. I percorsi locali sono indizi di recupero, non prova che i file esistano in un nuovo ambiente. Verificare i file se disponibili; se l’MP3 manca, recuperarlo dagli allegati o richiederlo, senza inventarlo né rigenerarlo come «lo stesso audio». Non usare link firmati scaduti come unica risorsa.

Per Cornell di «Come studiare meglio» mantenere lo stesso flusso: usare la clip separata approvata, non una nuova lettura. Non dichiarare completato un inserimento storico se non è stato verificato nel file finale.

