# PODCAST «REALTÀ VIRTUALE A SCUOLA» — APPROVATO IL 5 NOVEMBRE 2026

## Versione corretta e provenienza

L’utente ha definito «perfetto» il podcast appena consegnato, oltre al PDF sorgente. Per preservarlo, usare **il file MP4 approvato identico**, non rigenerare automaticamente voce, immagine o montaggio. I file originali della baseline sono inclusi in `../templates/realta-virtuale-podcast-approvato-2026-11-05/`:

- `PODCAST_REALTA_VIRTUALE_A_SCUOLA.mp4` — SHA-256 `9287cc59bd0e6dab9bf49fcf627d2f1a1408ac7a6753ea61efcea4d7357ea5e7`.
- `REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.pdf` — SHA-256 `5dcc0e4b22acb02941ae3fae3a9cb6f7ad1e672fb829907a5c04d435e2720e76`; 17 pagine. È la nuova revisione chiara, non il PDF v7 precedente.
- `PODCAST_TESTO_E_INDICE.md` — trascrizione fedele e inizio delle 9 parti; `COPERTINA_PODCAST_ORIGINALE.png` è la copertina fissa utilizzata.
- `manifest.json` e `clip/` — nove registrazioni TTS originali, con testo fedele, copione pronunciabile, voce, inizio e impronta. Le clip sono le sorgenti prima del montaggio; il MP4 approvato è il master finale e non è identico ai singoli MP3. Il manifest usa percorsi locali; non sono necessari URL privati scadibili.

Il file approvato dura **16:44** (1004,385 s), video H.264 1280×720 con copertina statica e audio AAC, due voci italiane alternate a **1,12×**, senza musica, sigle musicali, effetti o code. Durata e risoluzione descrivono il caso; non sono obiettivi universali.

## Regole personali per i podcast didattici

- Per i podcast personali, anche quando chiamati «file audio», il formato abituale è **MP4 leggero con copertina fissa e titolo completo più PODCAST**. Una richiesta esplicita di MP3 prevale; per le circolari usare il loro formato speciale MP3. L’MP3 di lavorazione non sostituisce il video nella consegna abituale del podcast.
- Mantenere **due voci italiane femminile e maschile alternate per sezione**; in questo caso l’introduzione è femminile e la prima unità maschile. `speed=1.12` va applicato una sola volta alla generazione TTS: non accelerare ancora nel montaggio. Aida e Lorenzo Prada sono le voci restituite in questo caso, non identificativi garantiti dal tool.
- Nessuna musica, intro, sigla musicale, sottofondo o coda, salvo nuova richiesta esplicita. Riusare la copertina appropriata e approvata: non inventare o generare nuove immagini per aggiornare questa skill.
- Leggere integralmente titolo, sommario, tutte le sezioni e sintesi, le **10 domande con tutte le 40 opzioni**, le parole della mappa e i quattro riferimenti del PDF; non aggiungere la soluzione. In altri podcast leggere le attività e i contenuti effettivamente presenti; rispettare esclusioni esplicite, documentandole.
- Nella lettura dell’indice si possono omettere i soli numeri di pagina e badge decorativi; non eliminare dati, numeri di sezioni o riferimenti. Usare un copione fedele distinto da quello fonetico, allineati al PDF effettivo. Nell’esempio gli URL sono scanditi nel parlato, mentre il testo accompagnatorio conserva gli indirizzi originali.
- Pronunciare **X = ics**, **XR = ics erre**; nel copione TTS si può usare `ìks erre`. Se compare **3D**, dire «tre dì» e fare la pausa solo dopo la D completa, prima della parola seguente. Controllare entrambe le voci nel file finale sui passaggi presenti; non basarsi unicamente sulla trascrizione automatica o sul testo del prompt.
- Allegare l’MP4 finale e, quando utile, il testo/indice temporale; indicare la durata misurata. L’uso di capitoli interni non sostituisce l’indice accessibile esterno.

## Procedura e verifiche

1. Leggere completamente il **PDF più recente effettivamente scelto**, verificarne l’impronta e ricostruire il copione in ordine, compresi riepiloghi, opzioni, mappa e fonti. Le esclusioni specifiche di un vecchio podcast non si trasferiscono ad altri.
2. Preparare il manifest e salvare subito nomi e impronte delle clip; usare `scripts/assembla_audio_pdf.py` per il montaggio offline senza nuove generazioni. Non rigenerare un risultato difettoso senza consenso e non rifare parti già approvate.
3. Normalizzare le clip senza velocizzarle, verificare volume/cambi voce, poi realizzare l’MP4 con copertina fissa, senza aggiungere musica. I parametri tecnici di questo esempio sono registrati nel manifest e in `QA_PODCAST_FINALE.json`; adattare l’encoding alle necessità senza ricodificare l’originale approvato per una semplice consegna.
4. Controllare la corrispondenza del testo e delle opzioni al PDF, decodifica, durata, indici, inizio/fine di ogni clip, passaggi fra voci e conclusione del video. Verificare la pronuncia di X/XR e di 3D in entrambe le voci **quando compaiono**. Riportare fedelmente l’estensione dell’ascolto: campioni controllati non significano ascolto integrale.
5. Verificare la copertina nei fotogrammi iniziale e finale, con titolo completo leggibile; evitare falsi allarmi e controllare nei fotogrammi reali. Se una sola sezione viene aggiornata, conservare il resto approvato e documentare esattamente eventuali ricodifiche; non sostituire registrazioni approvate senza autorizzazione.

Il report dell’esempio registra controlli di copertura e ascolti mirati su clip e video, non un’analisi completa certificata del parlato. L’approvazione dell’utente riguarda il risultato consegnato e non elimina l’obbligo di verificare i nuovi lavori.

