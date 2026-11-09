# BOX PER NUCLEI DI SIGNIFICATO — STANDARD APPROVATO

Applicare alle guide e agli articoli discorsivi del blog, insieme alle altre regole di `documenti-lunghi-blog.md`. Questo criterio deriva dalla revisione approvata delle dieci metodologie v5, non sostituisce i modelli specialistici delle mappe/esercizi.

## PRIORITÀ SUCCESSIVA — CONTROLLO ANTI-FRAMMENTAZIONE (3 NOVEMBRE 2026)

L’utente ha osservato che anche riquadri entro cinque righe possono essere eccessivamente frammentati. Prima del collaudo tipografico, leggere le coppie adiacenti e verificare se completano **lo stesso concetto**, senza isolare soggetto/azione, antecedente/pronome o causa/conseguenza. Unire solo quando il nucleo resta entro cinque righe effettive, anche dopo eventuali richiami bibliografici; restano separati i concetti autonomi. Non usare la lunghezza come unico criterio. Caso documentato: Shakespeare e Romeo and Juliet, 31→20 box narrativi dopo 11 accorpamenti motivati, **non quota universale**. Dettagli e versione corrente in `revisione-shakespeare-box-mappe-fonti-2026-11-03.md`.

## DECIDERE I CONFINI PRIMA DI IMPAGINARE

1. Leggere l’unità per intero e riconoscere le funzioni: definizione, spiegazione, esempio, consegna, aiuto, osservazione, confronto, fase operativa o riferimento.
2. Creare **un box per un nucleo di significato**, non uno per ogni frase e non un contenitore da riempire meccanicamente. Unire due brevi paragrafi contigui quando il secondo completa lo stesso concetto e l’insieme resta entro cinque righe reali.
3. Tenere nello stesso box la descrizione di uno strumento e la spiegazione necessaria a capire come usarlo, quando l’ingombro lo consente. Non lasciare in un box isolato un inciso, una coda di frase, un pronome senza antecedente o «a sinistra…» separato dalla tabella cui si riferisce.
4. Separare invece passaggi numerati autonomi, categorie/alternative da confrontare, obiettivi e modalità di valutazione, esempi autonomi e fonti diverse. Due pezzi brevi NON vanno uniti solo perché entrano in cinque righe. Conservare le tre fasi TBL, i passaggi Jigsaw, le forme del tutoraggio e i principi UDL riconoscibili.
5. Il limite di **cinque righe effettive complessive** è un tetto, non un obiettivo da raggiungere. Contare tutti i paragrafi e l’eventuale sottotitolo del box, con il font, la larghezza e l’interlinea definitivi. Due paragrafi da tre righe NON possono diventare un box da sei. Uno-due righi sono corretti per una regola autonoma.
6. Quando un nucleo supera cinque righe, dividerlo al confine fra sottoidee/frasi complete mantenendo sequenza e collegamenti, non a una soglia di caratteri. Non riscrivere, tagliare, riordinare frasi, ridurre font/interlinea/immagini/margini o nascondere testo per farlo entrare.
7. Se un documento è già composto da nuclei coerenti da quattro-cinque righe, **verificarlo e conservarlo**, senza promettere o forzare accorpamenti. I 74→56 box delle metodologie sono un risultato di quel documento, non una quota valida per tutti.

## ESEMPI OPERATIVI

- **UNIRE:** breve definizione di adattamento + frase sul suo valore inclusivo; definizione di appaiamento + spiegazione dell’associazione. Conservare i due paragrafi e i neretti dentro lo stesso box, con stacco discreto.
- **SEPARARE:** le cinque regole numerate di una guida, ognuna autosufficiente; «compito di partenza», «adattamento» e «che cosa osservare» quando chiedono letture diverse. Non fondere regole diverse per riempire spazio.
- **SPOSTARE SOLO IL CONFINE:** un box contiene strumenti di laboratorio e inizio della relazione, quello dopo soltanto le domande finali. Separare il nucleo «strumenti» dal nucleo «relazione per immagini e verifica», spostando il paragrafo completo senza cambiarlo.
- **CONSERVARE:** una spiegazione di quattro righe e il suo esempio autonomo di quattro righe: rimangono due box, anche se tematicamente vicini.

## IMPLEMENTAZIONE E VERIFICA

- Salvare sotto un nuovo nome; ripartire dalle ultime versioni approvate, non da bozze con diagnosi, riferimenti ad app esclusi o box rimossi. Mantenere il box «Limiti» escluso da «Una classe serena».
- Applicare raggruppamenti **espliciti e motivati** per id dei nodi. Non usare un algoritmo greedy di accorpamento per lunghezza come sostituto della lettura. Conservare integralmente paragrafi, tag di enfasi, titoli, immagini, alt, link e ordine; non appiattire il DOM.
- Usare `.coherent-group > p + p { margin-top:4px; }` solo per il lieve stacco fra paragrafi dello stesso box. Mantenere bianco esterno e crema interno, box interi su pagina, nessun marcatore decorativo ripetuto. Titoli sempre IN MAIUSCOLO.
- Eseguire `scripts/verifica_box_semantici.py guida.html --report box.json --strict`, oltre ai QA esistenti per blocchi, maiuscole, flusso/fonti, immagini/indice e confronto neretti.
- Il controllo conta tutte le LineBox nel box, anche quelle su nodi inline, ed elenca separatamente celle di sintesi e nodi della mappa. **Non certifica automaticamente la coerenza semantica**: richiede una decisione editoriale umana/di lettura dell’assistente. Riportare come «verificato, invariato» un raggruppamento già opportuno.
- Nei controlli del flusso non confondere il margine interno di un sottotitolo scartato dal renderer a inizio pagina con un box che sarebbe entrato prima: `verifica_flusso_fonti_blog.py` rimisura i candidati dubbi mantenendo i margini interni solo nel render di controllo. Non ridurre padding/font né forzare il box per azzerare un falso allarme; le interruzioni premature reali restano un errore.
- Ricontrollare l’indice e i numeri automatici dopo il reflow. Il totale pagine può variare; non forzare simmetria tra pagine né spostare avanti box per bilanciarle. Se il successivo non entra, una coda più corta è corretta.
- Confrontare testo completo ed enfasi, non solo il numero di tag. L’estrazione PDF può cambiare l’ordine dei glifi con font separati: usare anche ordine spaziale e DOM, senza scartare parole. Conservare l’audio esistente perché il contenuto letto non cambia.

## BASELINE

**Aggiornamento 1 novembre 2026:** il corpo approvato qui descritto è incorporato in **10 METODOLOGIE DIDATTICHE INCLUSIVE v8 BASE CORRETTA**, con appendice e fonti a pagina 33–35. Le versioni dell’appendice v4–v7 ripartivano dalla vecchia v2 e reintroducevano marcatori e box superati: non usarle come base. Leggere `versioni-appendici-2026-11.md` prima di nuove modifiche. In un’aggiunta di appendice non ridividere il corpo v5 già corretto: conservarne i gruppi esattamente.

Metodologie approvate: `/home/user/metodologie_box_rivisti_v5/LE_10_METODOLOGIE_DIDATTICHE_INCLUSIVE_BOX_RIVISTI_v5.html` e PDF (32 pagine, testo principale 56 box, da 74; tutte le schede al massimo cinque righe). La v5 prevale su v3 con marcatori e v4 senza marcatori ma ancora più frammentata. Le cinque edizioni verificate con questo standard sono raccolte in `/home/user/pdf_box_semantici_2026_10_31/`, con `manifest.json` e rapporti. Sono percorsi locali di provenienza, non prerequisiti per applicare lo standard.

