# ROMANTICISMO IN SPAGNA — SCHEMI NELLE UNITÀ (6 NOVEMBRE 2026)

> **VERSIONE STORICA SUPERATA:** il documento descritto qui conta 16 pagine. Per ogni intervento attuale partire invece dalla [versione completa di 21 pagine con mappa ampliata, domande e riferimenti](romanticismo-marco-completo-2026-11-06.md). Numeri di pagina, quantità di schede e istruzioni di baseline che seguono si riferiscono esclusivamente alla revisione storica e non a quella attuale.

## Quando usare questo riferimento

Leggere per successive modifiche al quaderno **MARCO HISTÓRICO DEL ROMANTICISMO EN ESPAÑA** o per rimpaginazioni analoghe in cui il docente chiede esplicitamente di collocare schemi e cronologie nelle unità corrispondenti. Non confondere questo documento con i quaderni su Rosalía, Bécquer o Lázaro, né con le app sul Romanticismo.

Il docente ha giudicato molto buona la prima rimpaginazione e ha poi chiesto di spostare **gli schemi e la linea del tempo mostrati nelle sue due foto** dalla fine del PDF alle unità pertinenti, prima di `EN RESUMEN`. La versione successiva è stata consegnata; **non è attestata un'ulteriore approvazione esplicita di questa versione**. L'ultima richiesta «Aggiorna le skills» riguarda le skill, non autorizza a modificare nuovamente PDF, immagini o audio.

## Baseline storica e provenienza

Nella revisione storica era stato consegnato [MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.pdf](../templates/romanticismo-marco-schemi-nelle-unita-2026-11-06/MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.pdf), **16 pagine**, SHA-256 `4ec51501219766e65de933886fd9b786c14c1190f95a872d3999e4d67cfe6b0e`. Non tornare al precedente PDF che mette gli schemi fotografati in fondo: aveva SHA-256 `e45d9dd11d07247c8ba7325dd8d70c039ab37ebf275b371aa39f06e4e03bd57d`.

L'allegato iniziale era un PDF spagnolo di 10 pagine, SHA-256 `7ebb3eddbdf28d4bd718aa50dca3c0e2905f047aa5f0fd3cd1e88a3f98fb6293`. L'allegato non è incluso nel template: non fingere di averlo a disposizione né ricostruirne eventuali collegamenti o altre caratteristiche non documentate. Il testo ricostruito, le immagini usate e la versione consegnata sono nel template. L'eventuale pacchetto sorgente consegnato con la **prima** rimpaginazione non contiene lo spostamento successivo: non usarlo come sorgente corrente.

## Collocazione esatta degli elementi

- **Unità 3 · 1833 / Isabel II e Prima guerra carlista:** dopo tutto il testo, lo schema a due colonne `DOS IDEAS DE ESPAÑA EN LUCHA`, con le righe `TRADICIÓN`, `LIBERALES`, `EL PÉNDULO`; segue `EN RESUMEN`. Nella versione consegnata lo schema è a pagina **7**.
- **Unità 5 · 1875 / Restauración y desastre del 98:** dopo tutto il testo, la cronologia `EL SIGLO XIX EN UNA LÍNEA` (sette date e relativi eventi dal 1808 al 1898), quindi lo schema `LOS PROTAGONISTAS DEL SIGLO` con `FERNANDO VII`, `ISABEL II`, `ALFONSO XII`; segue `EN RESUMEN`. Nella versione consegnata cronologia e schema sono a pagina **11**, la sintesi prosegue dopo questi supporti.
- **Mappa finale:** rimangono i sei riquadri illustrati a parole chiave, alle pagine **15–16**. I due schemi descrittivi e la cronologia, oggetto della richiesta, **non** sono duplicati nella mappa finale. Conservare i gruppi e le parole chiave: `TRADICIÓN`, `LIBERALES`, `EL PÉNDULO`, `FERNANDO VII`, `ISABEL II`, `ALFONSO XII`.
- Indice della versione storica di 16 pagine: capitoli e attività da pagina **2, 4, 6, 8, 10, 13**, mappa da **15**; ricalcolarlo se l'impaginazione cambia. Le pagine sono risultati, non vincoli rigidi per revisioni future.

Non imporre la stessa suddivisione 3/5 ad altri quaderni. In richieste analoghe identificare i supporti mostrati e attribuirli all'unità per contenuto; se la scelta è ambigua, chiedere prima. Mettere **testo → supporto tematico → sintesi**, senza duplicare o eliminare dati e senza eliminare la mappa finale non interessata dalla richiesta. Non spostare automaticamente tutti gli schemi di qualsiasi documento.

## Invarianti del quaderno

- Conservare le sei unità, il testo in spagnolo, i neretti del corpo, le **cinque** sintesi delle unità teoriche, le istruzioni dell'attività 3D e le immagini. Non aggiungere quiz, bibliografia o nuove riscritture a un incarico di sola rimpaginazione.
- Aspetto basato sugli ultimi modelli Rosalía/Bécquer: titolo/indice coordinati e navigabili, OpenDyslexic, sfondo bianco e box crema, una scena dopo ogni banner e ritmo leggibile. Gli specchietti `EN RESUMEN` sono in peso regolare 400, interlinea 1,85; rispettare i neretti del corpo.
- Mappa finale storica: sei schede **78×78 mm**, immagini **52×29,373 mm**, parole chiave in spagnolo, scene differenziate; non ridurre il carattere per farle stare nella stessa pagina. I tre riquadri per gruppo e le loro etichette restano quelli consegnati.
- Le immagini storiche del modello sono state riutilizzate dall'allegato; l'apertura dell'attività usa una scena già approvata sulla realtà virtuale. Non sostituire né rigenerare immagini senza richiesta.

## Risorse e modalità d'uso

Directory portabile storica: `templates/romanticismo-marco-schemi-nelle-unita-2026-11-06/`. Non usarla come baseline delle revisioni correnti.

- `MARCO_HISTORICO_ROMANTICISMO_SCHEMI_NELLE_UNITA.pdf`: copia integrale del PDF consegnato.
- File `.html` omonimo e `media/`: impaginazione modificabile e risorse locali.
- `sorgenti/CONTENUTI_ORIGINALI.json`: contenuti, titoli, sintesi, cronologia e nodi; `sorgenti/impagina.py`: generatore che legge il JSON e riscrive **sia** HTML sia PDF nell'albero del template.
- `qa/PRECEDENTE.html`, `qa/QA_REVISIONE.json`, `qa/BOX.json`, `qa/FLUSSO.json`: riferimento e controlli della revisione. `sorgenti/verifica_revisione.py` confronta versioni HTML e misura il PDF corrente; non certifica accessibilità né correttezza storica.

**Mai eseguire `impagina.py` dentro il template originale**, perché sovrascriverebbe la baseline. Copiare l'intera directory in un nuovo spazio di lavoro, applicare lì le modifiche e avviare `python3 sorgenti/impagina.py` dalla copia. Le versioni di WeasyPrint possono cambiare la paginazione; ricontrollare sempre il PDF effettivo. Non sostenere che il documento sia certificato PDF/UA soltanto perché è taggato.

## QA per revisioni future

1. Confrontare integralmente testo e neretti, celle, date/eventi, supporti e ordine con l'ultima baseline; non far derivare PDF nuovi dal vecchio ZIP. Il verificatore di regressione incluso funziona per questa revisione e può richiedere adattamenti per modifiche future autorizzate.
2. Verificare una sola occorrenza degli schemi e della cronologia, posizione dopo il testo e prima della sintesi, e sei riquadri finali senza tagli. Le tabelle devono rimanere leggibili e non spezzate in celle.
3. Eseguire i controlli box e flusso `scripts/verifica_box_semantici.py` e `scripts/verifica_flusso_fonti_blog.py` della skill; controllare peso 400 nelle sintesi, geometria dei nodi, numeri e destinazioni cliccabili dell'indice, lingua e numerazione delle pagine.
4. Controllare visivamente le pagine modificate, la mappa e l'indice. La precedente revisione è stata controllata anche visivamente; il QA automatico memorizzato passa, con 32 box narrativi e 21 aree di collegamento all'indice. Non considerare i soli test automatici prova di correttezza semantica o certificazione PDF/UA.
5. Per il solo aggiornamento delle skill non rigenerare PDF/audio/immagini né modificare gli archivi precedenti. Creare un nuovo ZIP completo soltanto se esplicitamente richiesto.

