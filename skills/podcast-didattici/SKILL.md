---
name: podcast-didattici
description: "Creare e aggiornare podcast didattici in MP4 con copertina fissa, due voci italiane a 1,12× e SENZA MUSICA. Usare per lettura integrale di PDF, documenti aggiornati, correzioni audio, fedeltà alla fonte, parti aggiunte per errore, indice parlato/temporale, pronuncia X/XR e 3D, conversioni MP3→MP4 e recupero montaggi. Il PDF corrente è l'unica fonte: eliminare contenuti delle vecchie edizioni, verificare tutte le pagine e l'intero AAC finale, riutilizzare solo letture identiche. Comprende sintesi, tutte le domande/opzioni, mappe e riferimenti, senza spiegazioni o soluzioni aggiunte. Verifica femminile e bibliografia maschile salvo diversa istruzione. X: ics; XR: ics erre; 3D: tre dì con pausa dopo la D completa. MP3 solo su richiesta esplicita. Non per circolari (circolari-audio), documentari o GLB; non sovrascrivere skill personali più ampie non disponibili."
---

# Podcast didattici personali

## PRIORITÀ — PODCAST REALTÀ VIRTUALE CHIARO APPROVATO (5 NOVEMBRE 2026)

L'utente ha giudicato **perfetti** il nuovo documento «REALTÀ VIRTUALE A SCUOLA» e il podcast corrispondente. Conservare il [caso approvato con PDF, MP4, copertina, testo e clip](references/caso-realta-virtuale-chiaro-approvato-2026-11-05.md) come baseline corrente di questo articolo: **17 pagine, 10 domande con 40 opzioni, mappa e fonti; video 16:44**, due voci a 1,12× e nessuna musica. I file approvati vanno riutilizzati identici, non rigenerati né rimontati per aggiornare la skill. La vecchia v7 da 16 pagine e 8 domande resta documentazione storica; scegliere sempre il PDF effettivamente richiesto e verificare gli hash.

Questo MP4 specifico approvato usa voce femminile per la bibliografia e dice «Domanda»/«Opzione»: sono caratteristiche **del solo file approvato**, da non correggere retroattivamente. Per i nuovi podcast continuano a valere le regole generali riportate sotto: verifica femminile, bibliografia maschile e niente etichette non presenti nella fonte, salvo nuove istruzioni esplicite. Non trasformare l'approvazione del risultato in una certificazione di ascolto integrale: i controlli documentati erano a campione; per i nuovi lavori eseguire la verifica integrale prevista.

Mantenere la scelta dell'utente del **2 novembre 2026: «Elimina per sempre la musica di sottofondo»**. I podcast sono **solo parlato a due voci, senza alcuna musica**, anche nei lavori futuri; questa regola sostituisce tutte le precedenti preferenze musicali. Mantenere la correzione del formato del 1 novembre: **MP4 con copertina fissa, non soltanto MP3**. Leggere `audio-generation` per le voci, `image-generation` per la copertina e `video-generation` per il montaggio; non modificare le skill generali.

## Impostazioni personali

- Applicare la correzione consolidata il **5 novembre 2026**: **il PDF aggiornato è l'unica fonte**. Ricostruire l'intero podcast perché corrisponda a quel documento, senza importare capitoli, esempi, righe, domande o riferimenti eliminati dalle vecchie edizioni. Un file con lo stesso nome può avere un hash e un contenuto diversi.
- Prima di una nuova edizione o di una correzione di fedeltà leggere **`references/fedelta-pdf-e-revisioni.md`**. Il riuso riguarda soltanto letture che corrispondono integralmente al nuovo testo; non è un'autorizzazione a mantenere materiale assente.
- Leggere **integralmente e soltanto ciò che è presente**: titolo, sottotitolo, indice corrente, testo, box «In sintesi», verifiche con tutte le domande e opzioni nell'ordine, mappe, fonti e attribuzione. Non aggiungere soluzioni, spiegazioni, saluti o etichette «Domanda/Risposta» non stampate. Leggere tabelle per riga e mappe nodo per nodo; non inventare descrizioni delle illustrazioni. Escludere le fonti solo su richiesta; conservare una precedente esclusione approvata soltanto se si deve montare quello stesso audio, non ricostruire una nuova lettura integrale.
- Alternare **una voce italiana femminile e una maschile**, per paragrafi o nuclei di significato. Per questa serie, salvo nuova istruzione, leggere **tutta la verifica con voce femminile** e **tutta la bibliografia con voce maschile**. Applicare ogni assegnazione richiesta anche quando la sezione è divisa in più chiamate. Usare `speed: 1.12` alla generazione; non accelerare nuovamente in montaggio.
- Pronunciare la **X «ics» /iks/** e **XR «ics erre»** in entrambe le voci. Usare la resa fonetica **`ìks` / `ìks erre` soltanto in `speech_text`**, senza alterare il testo originale. Prima di generare o correggere questi passaggi leggere `references/pronuncia-x-e-sigle.md`; non fidarsi della sola trascrizione automatica.
- Leggere **3D «tre dì»**, con una breve pausa **dopo la D completa e prima della parola successiva**, mai «tre dimostrati». Applicare la regola a tutte le occorrenze nelle due voci. Per preparazione e correzione locale senza rigenerare leggere `references/pronuncia-3d-e-pause.md`.
- **Non generare, riutilizzare o aggiungere musica**, neppure a volume basso: niente sottofondo, intro, jingle o coda strumentale. Non richiedere conferma di questa scelta nei prossimi podcast. Cambiarla solo dopo una nuova istruzione esplicita dell'utente.
- Per eliminare la musica da un vecchio montaggio, ripartire dagli **stem vocali puliti**, non limitarsi ad abbassare il mix. I vecchi esempi con musica sono soltanto storici, non modelli per nuovi lavori.
- Mantenere **titolo completo e PODCAST ben visibili**, senza sovrapposizioni o tagli, sull'immagine allegata o tratta dal documento. Salvare anche la copertina separata.
- Consegnare il podcast in **MP4 leggero con copertina fissa e audio integrale**, non soltanto in MP3: l'utente ha corretto esplicitamente il formato finale. Anche se parla di «file audio del podcast», mantenere questo formato consolidato salvo richiesta esplicita diversa. L'MP3 resta una sorgente di montaggio o un extra solo se richiesto; non generare nuove clip AI.

## Scegliere il flusso

| Richiesta | Procedura |
|---|---|
| «Ho aggiornato il documento» / «Ricostruisci in base al PDF» | Rileggere tutte le pagine, rifare inventario e manifest dalla fonte corrente e rimuovere ogni vecchia parte assente, incluse singole righe. Aggiornare indice parlato e temporale; riutilizzare solo stem esattamente corrispondenti. Leggere `references/fedelta-pdf-e-revisioni.md`. |
| «Hai aggiunto pezzi in più» | Non limitarsi ai passaggi già corretti: confrontare l'intero documento e l'intero MP4, cercando aggiunte, omissioni e ordine errato; consegnare una versione sostitutiva, non una revisione ibrida. |
| «Correggi solo queste sezioni audio, il resto va bene» | Applicare una riparazione selettiva solo entro lo scopo espresso. Non presentarla come lettura integrale dell'ultima edizione se conserva altre parti diverse; una successiva richiesta di fedeltà al PDF prevale sul vecchio criterio di conservazione. |
| «Aggiorna le skill» | Aggiornare questa skill personale e i suoi controlli, senza rigenerare media, rimontare podcast validi o modificare skill generali. Non ricostruire a memoria pacchetti personali più ampi mancanti. |
| «Crea il podcast / file audio da questo PDF» | Preparare la lettura fedele con `references/audio-e-musica.md`, poi completare **sempre l'MP4** con `references/copertina-e-video.md`, salvo esplicita richiesta di un altro formato. Non inventare un dialogo. |
| «Elimina la musica / niente sottofondo» | Usare esclusivamente le due voci e pause silenziose. La preferenza è permanente dal 2 novembre 2026; non richiamare vecchie basi né script musicali. |
| «Deve essere MP4, non MP3» | Convertire la narrazione integrale senza musica usando la copertina esistente, senza nuove generazioni. Conservare voci, velocità e finale. |
| «Usa questi due allegati per il video» | Riutilizzare audio e immagine; seguire `references/copertina-e-video.md`; non accorciare l'audio per alleggerire il file. |
| «Le voci leggono male la X» | Seguire `references/pronuncia-x-e-sigle.md`: correggere tutte le occorrenze nelle due voci, rigenerare solo i segmenti coinvolti e riconsegnare l'MP4 integrale senza musica e con copertina invariata. |
| «3D attacca la D alla parola seguente» | Seguire `references/pronuncia-3d-e-pause.md`: inserire una pausa dopo la D completa sullo stem esistente, senza spezzare sillabe né rigenerare; verificare ogni occorrenza nell'MP4 e conservare la X corretta. |
| «È fallito il montaggio» | Riprendere dai file intermedi validi; correggere solo il problema tecnico, senza nuove generazioni a pagamento. |
| «Leggi una circolare» | Usare `circolari-audio`: partire dall'Oggetto, terminare al nome del Dirigente, escludere la nota sull'omissis. Non trasferire automaticamente due voci, musica o copertina. |

## Procedura essenziale

1. **Identificare e bloccare la fonte.** Registrare nome, versione, numero di pagine e SHA-256, anche se il nome del PDF non è cambiato. Estrarre RAW e LAYOUT e controllare visivamente tutte le pagine. Ricavare l'inventario da questa fonte, incluse eliminazioni, sintesi, mappe e fonti; non usare la vecchia playlist come struttura.
2. **Preparare e confrontare il copione completo.** Separare `source_text` fedele e `speech_text` con sole espansioni orali motivate. Verificare parole e ordine per ogni pagina; non aggiungere contenuto da memoria, nemmeno nei titoli bibliografici. Aggiornare l'indice parlato alle pagine attuali. Conservare numeri, anni, citazioni, URL/DOI e nomi; applicare la pronuncia verificata di X/XR e la pausa dopo la D completa di 3D. Escludere solo elementi di servizio documentati. Usare `scripts/verifica_fedelta.py` per il controllo strutturale, senza confonderlo con l'ascolto.
3. **Preparare un nuovo manifest.** Assegnare ID univoco, sezione, pagine, voce, velocità, testo e destinazione a ogni parte prima delle chiamate TTS. Ammettere uno stem precedente solo con prova della corrispondenza al testo corrente e hash del file. Collegare ciascun risultato all'ID, non all'ordine di completamento; se l'associazione è incerta, identificarla dal contenuto effettivo. Non dedurla dal costo o dalla lunghezza della chiamata.
4. **Generare una volta.** Mantenere lingua/accento/genere coerenti; salvare URL e nome effettivo della voce restituiti. Generare soltanto parlato e l'eventuale copertina: nessuna chiamata musicale.
5. **Montare fino al formato finale.** Pareggiare le parti vocali e normalizzare il solo parlato con `scripts/normalizza_narrazione.py`, con margine per i picchi AAC. Unire con brevi pause silenziose, senza tagli o variazioni di velocità. Usare direttamente il master WAV per l'**MP4 leggero con immagine fissa**, 1280×720, H.264/AAC e avvio rapido. Nessuna traccia musicale né introduzione/coda strumentale.
6. **Controllare l'intero AAC dell'MP4.** Trascrivere, confrontare e ascoltare tutte le sezioni, incluse quelle riutilizzate, e tutti i raccordi; verificare le differenze ASR sul suono reale senza correggere dal contesto. Controllare tutte le opzioni, i nodi, le cifre dei DOI, l'ultima frase completa, voci e **assenza totale di musica**. Verificare X/XR in entrambe le voci e ogni 3D: D completa prima della pausa e parola successiva integra. Misurare durata e picchi AAC, decodificare tutto e controllare copertina a inizio/metà/fine. Legare il verbale finale agli hash di PDF, manifest e MP4; non dichiarare completato il solo successo tecnico.
7. **Consegnare.** Allegare come risultato principale l'**MP4**, insieme a copertina e testo con indice temporale. Non sostituirlo con l'MP3; quest'ultimo è facoltativo solo su richiesta. Mostrare il link esatto del video consegnato e l'immagine in Markdown; indicare durata e dimensione effettive.

**Non dichiarare il podcast finito né consegnare il solo MP3 mentre manca l'MP4.** Non chiedere nuovamente se l'utente vuole un video: il formato è già confermato per questa serie. Ridurre il peso con la codifica, mai tagliando l'audio. Consegnare solo MP3 esclusivamente se l'utente lo richiede espressamente per quella lavorazione.

## Non rigenerare i risultati riusciti

- Non generare di nuovo una voce, un'immagine o una base musicale per correggere un errore senza consenso, salvo esplicita autorizzazione a continuare fino alla correzione.
- Se il problema è tecnico (volume, metadati, codifica, giunzione, limite di picco), intervenire localmente sui file già validi, senza alterare la lettura.
- Una ripetizione **aggiunta per errore dal TTS**, non presente nella fonte, può essere rimossa con un raccordo locale verificato, conservando la frase originale una volta sola: nessuna nuova generazione. Non abbreviare il documento né rimuovere ripetizioni presenti nella fonte. Registrare intervallo e riduzione di durata, aggiornare tutti i tempi dell'indice e ricontrollare l'AAC; non dichiarare «nessun taglio» se è stato applicato questo intervento.
- Se l'utente approva espressamente un difetto di una particolare copertina, conservarla. L'accettazione non diventa una regola per nuove immagini.
- Gestire i job in background con notifica; non interrogarli ripetutamente e non avviarli una seconda volta. Attendere il risultato e poi continuare.

## Risorse del pacchetto

- **`references/fedelta-pdf-e-revisioni.md`**: leggere prima di nuove edizioni, ricostruzioni e correzioni di contenuti; unica fonte, riuso verificato, anti-aggiunte e QA integrale.
- `references/caso-mappa-6-passi-pdf-unico.md`: caso reale, versioni sostituite, righe/capitoli eliminati e criteri di regressione; i conteggi valgono solo per quel PDF.
- `scripts/verifica_fedelta.py` e `templates/SCHEMA_AUDIT_FEDELTA.json`: controllo di copertura/ordine, hash e verbale finale. Non sostituiscono l'estrazione verificata, l'ascolto o la revisione semantica.
- `scripts/test_verifica_fedelta.py`: 25 test sintetici delle protezioni anti-aggiunte, omissioni, vecchie versioni e verbali incompleti; eseguire dopo modifiche al validatore, senza generare media.
- `references/audio-e-musica.md`: nonostante il nome storico del file, contiene **solo parlato senza musica**, fedeltà, TTS, normalizzazione e QA.
- `references/pronuncia-x-e-sigle.md`: leggere prima del TTS se compare X/XR o per correzioni di pronuncia; grafia fonetica, conteggio, riuso dei segmenti e verifica nelle due voci.
- `references/pronuncia-3d-e-pause.md`: leggere se compare 3D o la D si unisce alla parola seguente; pause dopo la lettera completa, correzione locale e verifica nell'MP4.
- `references/copertina-e-video.md`: titoli, immagine sorgente, prompt, MP4 fisso leggero e controllo del finale.
- **`references/caso-realta-virtuale-chiaro-approvato-2026-11-05.md`**: ultima revisione VR approvata, impronte, copertina, MP4, clip e distinzioni rispetto alle regole generali. Il modello è autonomo nel relativo `templates/` e non richiede rigenerazioni.
- `references/caso-realta-virtuale-v7.md`: caso **storico** dell'edizione scientifica v7, precedente alla versione chiara approvata; lavorazione senza musica.
- `references/caso-realta-virtuale-v5.md`: caso **storico** per X/3D; l'eventuale musica descritta non va riprodotta nei nuovi podcast.
- `scripts/normalizza_narrazione.py`: normalizzare il solo parlato in WAV senza musica, tagli o modifiche di velocità.
- `scripts/video_statico.py`: montare un MP4 da audio e copertina già pronti, senza tagli o ritocco dell'immagine.
- `templates/COPERTINA_REALTA_VIRTUALE_v7_PODCAST.png`: copertina dell'edizione scientifica **v7 storica**, con titolo completo e PODCAST; per la nuova revisione usare la copertina del modello chiaro approvato. Non riutilizzare il titolo per argomenti diversi.
- `tests/test_podcast_vr_chiaro_approvato.py`: verifica offline di hash, manifest, clip, copertura e metadati dell'esempio approvato; non sostituisce l'ascolto integrale.
- `templates/PRONUNCIA_XR_FEMMINILE.wav` e `templates/PRONUNCIA_XR_MASCHILE.wav`: brevi esempi sintetici della pronuncia corretta, per confronto all'ascolto; non sostituiscono il controllo del nuovo audio.

- Tre estratti WAV **vocali puliti, senza musica**, di 3D nelle due voci: elencati in `references/pronuncia-3d-e-pause.md`, come riferimenti di ascolto e ritmo, non da incollare in altri podcast.

Mantenere questa skill come integrazione specifica dei podcast. Non ricostruire o sovrascrivere una skill personale più ampia se i suoi file originali non sono disponibili.

