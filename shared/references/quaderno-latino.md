# Quaderno statico Latino Facile

## Fonte e differenza rispetto all'app

La cartella originale di questa skill è disponibile, con lo script
scripts/latino-facile-quaderno/rilascio_quaderno.py. Sorgenti del quaderno:
/home/user/quaderno-unico, contenuti anche in /home/user/quaderno2/sezioni.
Versione storica documentata v16,124pagine: verificare i file presenti e la
versione corrente prima di chiamarla ultima. Non confondere questo quaderno
con altri quaderni latini prodotti in chat (per esempio quello97pagine)
né con il PDF dinamico delle frasi dell'app.

## Regole di impaginazione

Pastello/crema solo dentro card e schemi, uniforme/continuo. Tabelle e celle
vuote bianche, con eccezione esplicita della tabella sinottica v16: righe
colorate per caso. Timeline passato/presente/futuro con tre card uguali e
continue. Corpo14pt, paragrafi a sinistra, titoli/schemi centrati; numero di
pagina centrato grassetto senza marchio. Niente overflow. Copertina clay
richiesta; usare strumenti media per modifiche immagini, non PIL storico.

## Generazione e controllo

Leggere build_quaderno.py, style-accessibile.css, quaderno_v7_contenuti.py
e dati_coniugazioni.py. Lo script di rilascio accetta NN, --no-master e
QUADERNO_BASE; non usare --force su una versione esistente senza consenso.
Salvare script prima di eseguirli, anche per una semplice chiamata WeasyPrint.
Confrontare testo pagina per pagina, indice, conteggio, dimensione/hash e
render di copertina/pagine toccate. Non promettere che il totale resti124
se cambia contenuto.

## Pubblicazione separata

Nell'app corrente NON esiste più un pulsante/link al quaderno: non ripristinare
PDF_LINK dal vecchio esempio della skill. Generare un quaderno non autorizza
copia in client/public, deploy o nuovo ZIP. Se la pubblicazione è richiesta,
leggere il progetto attuale, propagare soltanto gli asset necessari e seguire
preview/consenso/produzione; mantenere vecchie versioni, guide e manifest coerenti.
Per dettagli strutturali consultare l'originale archiviato, subordinato a
queste correzioni. I colori nuovi dell'app non implicano che v16 sia rigenerato.
