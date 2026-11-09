# REALTÀ VIRTUALE A SCUOLA — PODCAST DELLA VERSIONE CHIARA APPROVATA

## Approvazione e precedenza

Il 5 novembre 2026 l'utente ha dichiarato perfetti sia il nuovo documento, per impaginazione, elementi e 10 domande, sia il podcast. Questa versione è la **baseline corrente di questo articolo**. L'edizione scientifica v7 da 16 pagine e 8 domande è un [caso storico](caso-realta-virtuale-v7.md), non il copione da applicare alla versione chiara. Non modificare retroattivamente archivi o lavori già consegnati. Per riproporre il podcast approvato, consegnare il file MP4 identico: non rigenerare le voci, la copertina o il montaggio.

Tutte le risorse sotto sono incluse nella skill, in `../templates/realta-virtuale-chiara-approvata-2026-11-05/`:

| Risorsa | Provenienza e verifica |
|---|---|
| `REALTA_VIRTUALE_A_SCUOLA_ARTICOLO_CHIARO.pdf` | Fonte specifica: 17 pagine; SHA-256 `5dcc0e4b22acb02941ae3fae3a9cb6f7ad1e672fb829907a5c04d435e2720e76`. |
| `PODCAST_REALTA_VIRTUALE_A_SCUOLA.mp4` | Master approvato; SHA-256 `9287cc59bd0e6dab9bf49fcf627d2f1a1408ac7a6753ea61efcea4d7357ea5e7`. |
| `COPERTINA_PODCAST_ORIGINALE.png` | Copertina fissa esistente, con titolo e PODCAST, riutilizzata nel video. |
| `PODCAST_TESTO_E_INDICE.md` | Testo di accompagnamento e indice delle 9 sezioni, con tempi misurati. |
| `manifest.json` e `clip/` | Testi per la lettura, tempi, voce, 9 clip TTS originali e loro impronte; i percorsi delle clip e del PDF sono relativi e portabili. |
| `QA_PODCAST_FINALE.json` | Controlli effettuati e limiti realmente documentati; non modificare il verbale per dichiarare controlli non eseguiti. |

Durata misurata **1004,385 s (16:44)**, 14.041.111 byte; MP4 H.264 1280×720 con immagine fissa e audio AAC. In quel montaggio: due voci italiane alternate per sezione, `speed=1.12` applicato una sola volta, nessuna musica. Nomi restituiti in quel caso: Aida e Lorenzo Prada; non garantire che siano selezionabili in un nuovo incarico.

## Inventario del caso, non quote universali

| Inizio | Contenuto | Pagine PDF | Voce nel master approvato |
|---|---|---|---|
| 00:00 | Titolo e sommario | 1 | femminile |
| 00:34 | Realtà virtuale (VR) e sintesi | 2–3 | maschile |
| 02:18 | Realtà aumentata (AR) e sintesi | 4–5 | femminile |
| 03:46 | Realtà mista (MR) e sintesi | 6–7 | maschile |
| 05:15 | Realtà estesa (XR) e sintesi | 8–9 | femminile |
| 06:26 | XR a scuola e sintesi | 10–12 | maschile |
| 09:00 | Verifica: 10 domande e 40 opzioni, senza soluzioni | 13–14 | femminile |
| 11:52 | Mappa finale: parole chiave dei 7 nodi | 15–16 | maschile |
| 13:00 | Quattro riferimenti e attribuzione | 17 | femminile |

Conservare titolo, sottotitolo, unità, tabelle di sintesi, testo delle domande e opzioni, mappa, fonti e attribuzione dell'autore. Numero di pagine, domande, opzioni, nodi, fonti e durata si riferiscono **solo a questa impronta**. Su una fonte diversa ricontarli e ricostruire il copione dal PDF effettivamente scelto.

## Distinguere il master approvato dalle regole generali

- Nel master specifico approvato la **bibliografia è letta da una voce femminile**; il copione aggiunge per chiarezza le parole «Domanda» e «Opzione» prima di numeri e lettere e non legge i numeri di pagina del sommario. Sono fatti verificabili relativi a questo video, non istruzioni nuove per tutti i podcast. La sua approvazione richiede di preservarlo così, non di correggerlo o rigenerarlo.
- Per **nuove letture**, salvo diversa richiesta, mantenere invece le istruzioni preesistenti della skill: **tutta la verifica femminile e tutta la bibliografia maschile**, numeri significativi dell'indice, e nessuna etichetta «Domanda/Risposta» non stampata. Non trasformare un'eccezione accettata in una preferenza generale. Se l'utente fornisce istruzioni nuove, applicarle allo scopo richiesto.
- Pronunciare X «ics», XR «ics erre» e 3D «tre dì» con pausa dopo la D completa, quando presenti. Usare la grafia fonetica soltanto nel copione TTS; verificare il suono nelle due voci, non solo la trascrizione automatica.
- La copertura strutturale e il controllo tecnico **non certificano la fedeltà integrale del parlato**. Per il file approvato il verbale registra ascolti mirati: inizi e finali delle nove clip, cambi di voce, ultima opzione e attribuzione; l'intero podcast non è stato ascoltato integralmente. L'utente lo ha comunque approvato. Per un nuovo lavoro restano obbligatorie le procedure complete di `fedelta-pdf-e-revisioni.md`.
- Se viene chiesta una modifica al documento, non affiancare automaticamente questo vecchio audio alla nuova versione: verificare pagina per pagina la compatibilità, conservare senza modifiche i segmenti validi e rispettare la richiesta. Una modifica solo grafica non richiede per sé una nuova registrazione; una modifica al testo sì, per i passaggi effettivamente cambiati.

## Verifica offline e conservazione

1. Calcolare SHA-256 di PDF e MP4 e confrontarli con la tabella. Rifiutare la sostituzione silenziosa di uno dei due file.
2. Leggere `manifest.json` per i 9 segmenti e controllare che le relative clip corrispondano agli hash registrati. Non utilizzare nomi di file o vecchie URL come prova di fedeltà.
3. Eseguire senza generazioni `python3 /home/user/skills/podcast-didattici/tests/test_podcast_vr_chiaro_approvato.py -v` e i 25 test originali `python3 /home/user/skills/podcast-didattici/scripts/test_verifica_fedelta.py -v`. Gli automatismi controllano i file e gli invarianti, non ascoltano il podcast né attestano conformità semantica integrale.
4. Per consegnare il risultato già approvato allegare l'MP4 originale, la copertina e il testo con indice; mantenere i nomi e indicare la durata misurata. Per una nuova edizione usare sempre la fonte corrente, la procedura integrale originale e un nuovo verbale riferito agli hash effettivi.

