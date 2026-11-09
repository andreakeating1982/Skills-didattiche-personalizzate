# ROMANTICISMO — MAPPA SENZA ATTIVITÀ (6 NOVEMBRE 2026)

## Regola generale, priorità e confini

Per **tutte le mappe concettuali finali dei documenti didattici dell'utente** rappresentare i contenuti disciplinari del PDF, **mai attività, esercizi, istruzioni operative o rimandi alle attività del PDF**. Nella copertura «un box per ogni capitolo», considerare i capitoli di contenuto, non le sezioni dedicate alle attività. Questa istruzione esplicita successiva corregge la precedente eccezione che erroneamente prevedeva un box per `ACTIVIDAD 3D` nel Romanticismo.

Distinguere sempre il **tema disciplinare** da una consegna: se, per esempio, la realtà virtuale o l'audio sono argomento sostanziale del documento possono far parte della mappa; non includere invece «attività 3D», «ascolta», istruzioni o un nodo che riassume un esercizio. Non eliminare meccanicamente tutte le parole `audio`, `3D` o `linea del tempo` dalle mappe: conta il significato. Nel Romanticismo i termini di quella particolare scheda fotografata erano riferimenti all'attività e sono stati eliminati soltanto dalla mappa finale. Non cancellare le attività nel corpo del documento, le loro immagini, istruzioni, riferimenti nell'indice o mappe specificamente interne agli esercizi, salvo richiesta.

## Baseline attuale del quaderno

[MARCO_HISTORICO_ROMANTICISMO_MAPPA_CORRETTA.pdf](../templates/romanticismo-marco-mappa-senza-attivita-2026-11-06/MARCO_HISTORICO_ROMANTICISMO_MAPPA_CORRETTA.pdf), **20 pagine**, SHA-256 `f2ff1e94f785e719648bd475bda7fe04ab93233cec291f849213aa6fa52e1ec4`. È la nuova versione da consegnare e usare per futuri interventi; al momento della realizzazione non era attestata un'ulteriore approvazione dell'utente. La precedente versione completa da 21 pagine è storica: [riferimento e provenienza](romanticismo-marco-completo-2026-11-06.md), SHA-256 `36e8ac0e2d01bf497c5f38ed7348b3266f1788a4b7527c0b0560673489ff1703`. Non riprendere l'eccezione sull'attività né l'indice della versione storica.

Le due immagini dell'utente, conservate in `qa/da-eliminare-riquadro.png` e `qa/da-eliminare-testo.png`, mostravano rispettivamente l'intero nodo **ACTIVIDAD 3D / LÍNEA DEL TIEMPO / AUDIO / FECHAS Y HECHOS** e la scritta **Y ACTIVIDAD** nel titolo. Sono stati rimossi dalla mappa finale; l'attività vera e propria rimane intatta nella sezione 6 del quaderno.

## Mappa corretta e invarianti

La mappa è ora in **tre pagine ordinate** (17–19), senza connettori, con **11 nodi** preservati: cinque dedicati ai capitoli storici 1–5 e sei nodi già realizzati su idee e protagonisti. Griglia **4 + 4 + 3**, due colonne con l'ultimo nodo dispari centrato; box 78×78 mm, immagini 52×29,373 mm, parole chiave in spagnolo. Gruppi: `ETAPAS HISTÓRICAS · 1808–1868`, `RESTAURACIÓN E IDEAS DE ESPAÑA`, `LOS PROTAGONISTAS DEL SIGLO`. L'uso di immagini identiche tra capitolo e nodo collegato è ereditato dal documento già consegnato, non un invito a sostituire o generare immagini automaticamente.

Conservare contenuti delle sei sezioni, attività 3D nel corpo, schemi dell'unità 3 e cronologia/schema dell'unità 5 prima di `EN RESUMEN`, le **10 domande con 4 opzioni**, le **5 fonti** finali e **13 richiami cliccabili**. Nella mappa non ripristinare la scritta `EL SIGLO XIX EN UNA LÍNEA · SÍNTESIS FINAL` rimossa in precedenza; rimane il titolo distinto della cronologia dentro l'unità 5. L'indice aggiornato della presente versione mostra sezioni 1–6 a 2, 4, 6, 8, 10, 13; verifica 15, mappa 17, bibliografia 20. Ricalcolare sempre i numeri dopo ogni nuova modifica.

## Modello portabile e controlli

`templates/romanticismo-marco-mappa-senza-attivita-2026-11-06/` contiene il PDF, l'HTML corrispondente, i font e le illustrazioni locali; `sorgenti/impagina.py`, `CONTENUTI_ORIGINALI.json` e `NUEVOS_CONTENIDOS.json` generano la revisione. La chiave del quiz è nel JSON interno, non nel PDF. `qa/BASELINE_COMPLETA_PRECEDENTE.html` è necessaria per il controllo differenziale e `sorgenti/verifica_completo.py` controlla preservazione di intere sezioni/quiz/fonti, gli 11 nodi mantenuti, geometria, assenza dell'attività dalla mappa, riga e numero di indice, 13 destinazioni bibliografiche precise e link esterni. Generatore e verifica scrivono nella stessa cartella: **copiare tutto il modello in un nuovo spazio di lavoro e non modificarlo direttamente**. Usare WeasyPrint, BeautifulSoup4 e PyMuPDF.

In questa revisione, il confronto testuale PDF pagine 2–16 è risultato identico alla versione precedente; sono stati verificati la misura dei box, l'ordine delle mappe, l'indice e le note. `qa/box_corretto.json`, `flusso_corretto.json`, `fonti_corretto.json` mostrano i controlli strutturali; l'unico avviso bibliografico riguarda la frase introduttiva non classificata come voce. Le pagine delle mappe, copertina e fonti sono state ispezionate visivamente. Il PDF è taggato; **non affermare conformità PDF/UA senza validazione indipendente**.

Per ogni modifica futura rileggere semanticamente i nodi: il test che cerca parole vietate è una difesa per questo caso, non sostituisce il giudizio su altri documenti. Verificare che tutti i capitoli di contenuto siano rappresentati, che i nodi sopravvissuti siano intatti e le attività restino nel corpo. Verificare indice e destinazione esatta delle note, senza confondere funzionamento dei link e attendibilità delle fonti. Non aggiornare automaticamente altri PDF, podcast o ZIP per questa regola.

