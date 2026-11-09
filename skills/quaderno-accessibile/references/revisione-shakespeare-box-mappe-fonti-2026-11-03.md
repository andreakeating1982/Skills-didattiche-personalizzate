# BOX, IMMAGINI DELLA MAPPA E FONTI — REVISIONE DEL 3 NOVEMBRE 2026

## QUANDO APPLICARE

Usare per guide e quaderni discorsivi del blog quando si rimpaginano testi, si illustrano mappe concettuali finali o si aggiungono riferimenti bibliografici. Integrare i profili `box-per-nuclei-di-significato.md` e `sintesi-e-mappa-finale.md`; non alterare automaticamente mappe/esercizi con modelli specialistici o revisioni che l’utente ha limitato a un singolo elemento.

## BOX: MENO FRAMMENTAZIONE, SENZA FUSIONI MECCANICHE

1. Leggere tutta l’unità e individuare i nuclei di significato. Riconoscere frasi collegate, soggetto e continuazione, causa ed effetto, personaggio e azione, spiegazione e relativo completamento.
2. Raggruppare **i box adiacenti che completano lo stesso nucleo**, se coerenti e se entrano nel limite. Non produrre un riquadro per frase né lasciare in un box separato un pronome, una conseguenza o la conclusione necessaria. Uno o due righi restano corretti per un concetto autonomo.
3. Misurare nel renderer definitivo **massimo cinque righe reali complessive**, inclusi titolo, enfasi e riferimenti inline; non stimare dai caratteri. Se supera il limite, separare tra sottoidee o frasi complete; non ridurre font, interlinea o margini, né tagliare, riscrivere o riordinare il testo per farlo entrare.
4. Conservare testi, lingua, ordine, titoli e neretti; preservare test/quiz e opzioni se non richiesto altrimenti. L’accorpamento va motivato editorialmente, non deciso da un algoritmo greedy. `scripts/verifica_box_semantici.py` controlla l’ingombro, non la coerenza semantica: rileggere i nuclei e ispezionare il PDF.

## MAPPA: UNA SCENA PERTINENTE PER CIASCUN CONCETTO

- Nei box standard **78×78 mm**, parole chiave e immagini clay adulte **52×29,373 mm**: scegliere scene diverse e significative per concetti diversi, capaci di aiutare a capire, non la stessa immagine generica ripetuta ovunque.
- Le immagini devono corrispondere al nodo per soggetti e azione, avere proporzioni adulte, stile coerente e `alt` veritiero nella lingua del documento. Non inventare scritte, fare fotografie passare per documenti storici o trasformare dati/grafici in finzione.
- Riusare immagini pertinenti già disponibili; la stessa scena può essere riusata per lo **stesso concetto**, ad esempio nelle due lingue, quando effettivamente utile. Non imporre una quota universale o vietare ogni ripetizione indipendentemente dal significato.
- Per l’esempio Shakespeare, sei scene coerenti e distinte sono riutilizzabili in `templates/shakespeare-romeo-juliet/media/` e descritte nel relativo `manifest.json`: Stratford e studi, Globe, scrittore ed eredità, famiglie rivali, matrimonio, pozione e lettera. Rispettare i diritti e la provenienza annotata, soprattutto dell’immagine estratta dall’allegato originale.
- Se manca un’immagine adatta, usare i tool media con un riferimento clay pertinente. Non rigenerare automaticamente un risultato errato: mostrarlo, spiegare il difetto e chiedere se correggerlo. Un aggiornamento delle sole skill non richiede nuove generazioni.
- Usare `scripts/verifica_immagini_mappa.py` per individuare immagini identiche e alt assenti; l’hash rivela uguaglianza di file, **non** pertinenza concettuale né somiglianza visiva. Ispezionare le immagini e la mappa stampata per dimensioni, tagli e comprensibilità.

## RIFERIMENTI BIBLIOGRAFICI PUNTUALI

- Quando la bibliografia è richiesta o prevista dal profilo scientifico, includerla dopo la mappa con titolo **RIFERIMENTI BIBLIOGRAFICI**, indice e numeri aggiornati, senza immagini nella sezione. Per un restyling espressamente limitato alla sola grafica conservare le fonti e non aggiungere contenuti non autorizzati.
- Verificare realmente ogni fonte e selezionare opere attendibili e pertinenti. Riportare autori o istituzione, titolo, edizione/ente, anno se disponibile, URL funzionante e data di consultazione; per opere letterarie indicare anche atto/scena, per studi pagina o sezione quando verificabili. Non inventare dati mancanti o bibliografie.
- Distinguere le fonti consultate per la revisione da quelle dell’originale, senza retroattribuirle; conservare la provenienza nel registro di lavoro e non aggiungere frasi esplicitamente eliminate dall’utente. Non usare un rinvio come se confermasse una frase che la fonte contraddice; rispettare i limiti della richiesta prima di cambiare il testo originale.
- **Aggiornamento successivo:** suddividere anche la bibliografia in box crema per nuclei coerenti, massimo cinque righe renderizzate, senza perdere dati, ordine o link. Leggere `fonti-in-box-2026-11-03.md` e controllare con `scripts/verifica_box_fonti.py`, oltre al QA dei link e al PDF visivo.
- Se si usano richiami interni `[n]`, devono rinviare alla fonte corretta nel PDF, restare leggibili e avere una **superficie cliccabile non nulla**: evitare `line-height:0` sul link. Verificare anche link esterni, numerazione, destinazioni, margini e presenza delle fonti nel PDF effettivo. `scripts/verifica_fonti_bibliografia.py` controlla struttura, destinazioni e superfici dei rimandi; non certifica attendibilità o verifica fattuale.

## ESEMPIO CONSEGNATO — SHAKESPEARE E ROMEO AND JULIET

La versione più recente, verificata il 3 novembre 2026, è `WILLIAM_SHAKESPEARE_ROMEO_AND_JULIET_FONTI_IN_BOX.pdf`, SHA-256 `f67207768a8dfc7bccacdcdf165c815bb63cf1e61c09e379b34c418f18d59d8a`. Usarla per ulteriori interventi sul quaderno, salvo nuovo allegato. Non reintrodurre l’introduzione e le quattro note storiche rimosse dopo la versione `fc74f709…`; mantenere le cinque fonti e gli otto collegamenti alle scene nei box crema. I sorgenti locali e il QA sono registrati in `shakespeare-revisione-corrente-2026-11-03.json`: verificarne esistenza e hash, senza presumere che siano inclusi nello ZIP portabile. Nessuna approvazione esplicita della nuova edizione è registrata.

Nel caso specifico i box narrativi sono passati da 31 a 20 con 11 accorpamenti semantici; questi numeri **non sono quote generali**. Sei immagini diverse, cinque riferimenti, otto link a scene; testo ed enfasi originali e le 10 domande con 40 alternative sono stati mantenuti. Le note sulle incertezze sono state eliminate per la richiesta successiva, solo nel caso Shakespeare. La bibliografia è frutto della revisione, non dell’allegato originario. Non ripartire dalla v4 o dal PDF privo di fonti per una modifica successiva, né rigenerare l’audio annullato.

## COLLAUDO MINIMO

```sh
python3 scripts/verifica_box_semantici.py documento.html --report box.json --strict
python3 scripts/verifica_specchietti_box.py documento.html manifest-supporti.json --report supporti.json
python3 scripts/verifica_immagini_mappa.py documento.html --report immagini-mappa.json
python3 scripts/verifica_box_fonti.py documento.html --report box-fonti.json
python3 scripts/verifica_fonti_bibliografia.py documento.html --pdf documento.pdf --report riferimenti.json
```

Controllare manualmente pertinenza delle scene, fonti e corrispondenza fra affermazione e citazione; confrontare testo/enfasi/quiz con la base. Misurare in PDF le aree cliccabili (larghezza e altezza positive), destinazioni interne, URL, indice e tutte le pagine. Nessun controllo automatico è una certificazione PDF/UA o una prova di attendibilità delle fonti.

