# Documentario claymation didattico

Originale completo conservato: script plan_scene.py, assemble_claymation.py,
qa_frames.py e template stile/prompt/scena in cartelle col nome originale.
Leggere anche la skill generale video-generation e audio-generation per i
motori, non copiarne versioni obsolete dagli esempi storici.

## Pipeline

Sceneggiatura fedele → voce → riferimenti visivi coerenti → piano scene →
clip → assemblaggio → QA. Misurare l'audio con ffprobe; la somma scene deve
combaciare con la narrazione. I template del progetto storico1280x720@24
sono un riferimento, non un obbligo per un'altra richiesta.

Prompt per scena a3strati: contenuto/azione, camera, stile clay. Stessa
identità dei personaggi, ma riferimenti non garantiscono perfetta continuità.
Per immagini nuove/modificate usare gli strumenti media. Prima di una
rigenerazione per errori mostrarli e chiedere; non consumare altre immagini
in autonomia per correggere un testo.

Lo script plan_scene.py calcola durate proporzionali con chiusura esatta;
controllare compatibilità con durata nativa dei clip. Assemblare con trim/
stretch moderato, scala/fps coerenti, audio uniforme e faststart. Niente
captions/titoli/Fin finali nel profilo documentario senza testo. Non allungare
oltre il limite narrativo accettabile solo per riempire minuti.

QA mirato: inizio/metà/fine capitoli e scene con giornali/bandiere/documenti,
testi generati erronei, anacronismi, personaggi, sincronia e durata. Valutare
solo i clip effettivamente disponibili; non dichiarare vista l'intera durata
se è stata ispezionata per campioni.

Per lavori lunghi usare background con notifica, senza polling/ripetizioni.
Pubblicazione o upload esterni richiedono autorizzazioni separate. Dettagli
in references/video-claymation-didattico/workflow-report.md e originale.
