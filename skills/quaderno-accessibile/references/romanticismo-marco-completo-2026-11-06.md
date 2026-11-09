# ROMANTICISMO IN SPAGNA — QUADERNO COMPLETO CONSEGNATO (6 NOVEMBRE 2026)

> **STORICO, NON USARE COME BASELINE CORRENTE:** l'utente ha corretto l'inclusione dell'attività nella mappa. Per nuove revisioni usare [la mappa senza attività, PDF di 20 pagine e regola permanente](romanticismo-marco-mappa-senza-attivita-2026-11-06.md). Le indicazioni successive su 12 nodi, copertura della sezione attività e indice a pagina 21 descrivono esclusivamente la versione precedente: **non sono istruzioni attive**.

## Scopo e stato

Registro storico della versione di **MARCO HISTÓRICO DEL ROMANTICISMO EN ESPAÑA** consegnata dopo la richiesta di ampliare la mappa, aggiungere una verifica e inserire fonti collegate. Per le revisioni attuali usare il riferimento più recente sopra. L'utente aveva apprezzato la precedente impaginazione; **non è attestata un'approvazione esplicita successiva della nuova versione completa**. La richiesta di aggiornare le skill non autorizza modifiche al PDF, all'audio, alle immagini o agli archivi precedenti.

Il PDF di riferimento è [MARCO_HISTORICO_ROMANTICISMO_COMPLETO.pdf](../templates/romanticismo-marco-completo-2026-11-06/MARCO_HISTORICO_ROMANTICISMO_COMPLETO.pdf), **21 pagine**, SHA-256 `36e8ac0e2d01bf497c5f38ed7348b3266f1788a4b7527c0b0560673489ff1703`. Supera come baseline il PDF da 16 pagine, SHA-256 `4ec51501219766e65de933886fd9b786c14c1190f95a872d3999e4d67cfe6b0e`, che rimane storico con [le istruzioni sulla collocazione degli schemi](romanticismo-marco-schemi-nelle-unita-2026-11-06.md). Non ripartire dalla prima rimpaginazione, dal vecchio ZIP sorgente o da un PDF precedente.

## Modifiche richieste e realizzate

1. Eliminare **solo dalla mappa finale** l'esatta dicitura fotografata `EL SIGLO XIX EN UNA LÍNEA · SÍNTESIS FINAL`. Conservare invece il titolo `EL SIGLO XIX EN UNA LÍNEA` che introduce la cronologia nell'unità 5: è una scritta diversa e il supporto non è stato eliminato. La foto di riferimento è `qa/scritta-da-rimuovere.png` nel modello.
2. Riorganizzare la mappa in modo coerente e ordinato, conservando i nuclei esistenti e inserendo almeno un riquadro per ogni capitolo presente. La versione consegnata comprende **12 schede** in quattro gruppi su quattro pagine: **sei** nodi dedicati alle sezioni 1–6 e **sei** nodi preesistenti, `TRADICIÓN`, `LIBERALES`, `EL PÉNDULO`, `FERNANDO VII`, `ISABEL II`, `ALFONSO XII`. I sei nodi nuovi coprono invasioni del 1808, Cádiz 1812, Isabel II e guerra carlista, Gloriosa, Restaurazione e 1898, e l'attività 3D. La presenza del nodo dell'attività era una interpretazione **errata e successivamente corretta**: non ripristinarlo, e non inserire riferimenti alle attività in alcuna mappa concettuale finale.
3. Inserire prima della mappa `VERIFICACIÓN DE COMPRENSIÓN`: **10 domande in spagnolo**, quattro opzioni e una risposta corretta, riferite ai cinque capitoli storici. Le risposte sono nella chiave interna `sorgenti/NUEVOS_CONTENIDOS.json`, non nel PDF. Non estendere automaticamente il numero 10 a qualsiasi altro documento o alterare le domande approvate/consegnate senza richiesta.
4. Aggiungere in chiusura `REFERENCIAS BIBLIOGRÁFICAS`: **cinque** fonti consultate per completare il quaderno, in box crema, con URL esterni cliccabili e **13 richiami numerici** collegati nel testo alle rispettive voci. Non dire che siano le fonti consultate dall'autore originale: sono risorse consultate durante l'integrazione. Verificare la pertinenza puntuale dei richiami anche se i link funzionano; non equiparare un link funzionante a una verifica di ogni singola affermazione storica.

## Struttura da conservare

- Le sei sezioni originali, il testo spagnolo con i neretti del corpo, le immagini, le cinque sintesi teoriche `EN RESUMEN` e la consegna dell'attività 3D rimangono quelli della precedente versione, con le sole note bibliografiche aggiunte nel testo. Il confronto HTML delle componenti preesistenti, escludendo le note, ha dato esito positivo.
- **Unità 3:** testo → tabella `DOS IDEAS DE ESPAÑA EN LUCHA` → `EN RESUMEN`. **Unità 5:** testo → cronologia a sette date → tabella `LOS PROTAGONISTAS DEL SIGLO` → `EN RESUMEN`. Le tabelle e la cronologia non sono duplicate nella mappa finale; restano invece le **schede illustrate** relative alle stesse tematiche.
- Nel nodo `ALFONSO XII`: `1875`, `RESTAURACIÓN`, `HIJO DE ISABEL II`. Non associare erroneamente la reggenza del 1898 al regno di Alfonso XII: nella mappa `REGENCIA · 1898` compare nel riquadro generale dell'unità 5.
- Mappe: box **78×78 mm**, immagine interna **52×29,373 mm**, parole chiave leggibili in spagnolo; titoli e gruppi coerenti, nessun restringimento per costringere la mappa in una pagina. Sono state riutilizzate le immagini già disponibili; non rigenerarle senza richiesta.
- Indice della versione consegnata: sezioni 1–6 alle pagine **2, 4, 6, 8, 10, 13**; verifica **15**, mappa **17**, bibliografia **21**. Questi numeri sono risultati dell'impaginazione, non vincoli per revisioni future: aggiornarli e testare tutti i collegamenti.

## Modello portabile e procedura

Directory: `templates/romanticismo-marco-completo-2026-11-06/`.

- `MARCO_HISTORICO_ROMANTICISMO_COMPLETO.pdf` e l'HTML omonimo: esemplare esattamente consegnato e sorgente impaginato.
- `media/`: caratteri OpenDyslexic e immagini locali.
- `sorgenti/CONTENUTI_ORIGINALI.json`: sezioni e materiali preesistenti; `NUEVOS_CONTENIDOS.json`: domande, chiave interna, nuove schede, fonti e richiami; `impagina.py`: costruisce l'HTML e il PDF.
- `qa/BASELINE.html`: precedente versione usata nel confronto; `QA_COMPLETO.json`, `box.json`, `flusso.json`, `box_fonti.json`: controlli dell'ultima versione. `sorgenti/verifica_completo.py` controlla regressione, ordine, geometria e link; `verifica_destinazioni.py` mostra le coordinate delle note.

**Mai eseguire il generatore nel template originale**: sovrascrive la baseline. Copiare l'intera directory in un nuovo spazio di lavoro; solo in tale copia modificare sorgenti e lanciare `python3 sorgenti/impagina.py`. Dipendenze: WeasyPrint, BeautifulSoup4 e PyMuPDF, oltre ai font e alle immagini inclusi. Il rendering può cambiare con librerie diverse: ricontrollare il PDF effettivo. La chiave delle risposte è solo per il docente/QA e non va stampata nel PDF senza richiesta.

## Verifiche per futuri interventi

1. Confrontare testo, neretti, schema, cronologia, immagini e attività con la versione corretta; modificare solo gli elementi autorizzati. Controllare che la dicitura eliminata non ricompaia **nella mappa**, ma che resti il titolo distinto della cronologia nell'unità 5.
2. Controllare almeno un box per ognuna delle sei sezioni di questo documento, i sei nodi precedenti, correttezza delle parole chiave e delle immagini, misure, tagli e leggibilità. Nelle nuove mappe non imporre automaticamente dodici box: scegliere quantità e copertura secondo il documento e la richiesta.
3. Contare le 10 domande e le quattro opzioni, verificare che ciascuna risposta sia sostenuta dal testo e sia univoca; la sola presenza delle lettere nella chiave non dimostra la correttezza del quiz. Non inserire la chiave nel PDF studente.
4. Per ogni richiamo numerico verificare nel PDF area cliccabile e destinazione precisa della relativa voce, non solo della pagina della bibliografia; controllare anche gli URL e la pertinenza delle fonti. Non inventare attribuzioni o consultazioni. Controllare ad una ad una corrispondenza e numero stampato delle voci dell'indice: il test incluso verifica gli ancoraggi, ma la sua verifica testuale dei numeri **non accoppia rigorosamente** ciascuna riga al proprio numero.
5. Eseguire `sorgenti/verifica_completo.py` sulla copia di lavoro e, per il profilo della skill, i controlli `scripts/verifica_box_semantici.py`, `scripts/verifica_flusso_fonti_blog.py` e `scripts/verifica_box_fonti.py --bibliography-id referencias`. Il controllo bibliografico originario passa con un avviso sul paragrafo introduttivo `Fuentes consultadas para completar este cuaderno`, che non è una voce bibliografica: non nascondere l'avviso né presentarlo come errore nelle fonti.
6. Rivedere visivamente copertina, indice, domande, ciascuna pagina di mappa, schemi e bibliografia. L'ultima versione è taggata, ma non dichiararla conforme PDF/UA senza una validazione indipendente; i test di geometria/link non dimostrano la correttezza scientifica, l'accessibilità completa né la qualità didattica.

