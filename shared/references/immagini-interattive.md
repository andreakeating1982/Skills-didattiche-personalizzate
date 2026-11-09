# Immagini interattive e Romanticismo

## Selezionare sorgente e variante

Distinguere IMMAGINE INTERATTIVA (hotspot/audio, manutenzione in
romanticismo-interattivo), la variante Romanticismo e IMMAGINE INTERATTIVA
SORGENTE da clonare (storicamente romanticismo-mappa-concettuale). Verificare
la cartella nel contesto corrente: non scegliere solo dal nome simile.

## Per una nuova app

Usare scripts/immagine-interattivo-sorgente/clone_app.py; --source accetta
cartella o repo. --dump produce il contenuto corrente; --json/--name creano
il clone. Schema dati in references/immagine-interattivo-sorgente/contenuto-json.md.
Conservare geometria finché l'immagine è la stessa. Il template corrente ha
4 paragrafi e 10 slot (2-3-2-3), segmenti allineati ai paragrafi. Cambiare
solo paragrafi, keyword, titoli, audio/immagine richiesti. Nuova geometria
richiede coordinate coerenti, non una sostituzione di testo alla cieca.

## Per manutenzione

- Leggere server/schema-data.ts, lib/audioData.ts, conceptMapPositions.ts,
  reportPdf.ts, immagine mappa-vuota.png e audio effettivi.
- Sincronizzare audioStopAt con endTime: finire prima del numero successivo.
- Preservare dashboard, codice classe, sessioni, attivi, re-entry, PDF Report/
  Mappa Completa/Mappa in Bianco e palette del profilo.
- Calcolare hotspot sull'area dipinta, non sull'intero box se object-fit
  lascia bande vuote; provare mouse/touch e ridimensionamento.
- Per cambiare immagini usare gli strumenti media, non vecchi script Python
  di manipolazione 2D citati negli archivi.

Verificare flusso con fixture separata e report prima della preview.
Approfondimenti conservati: originali immagine-interattivo,
romanticismo-interattivo e immagine-interattivo-sorgente; riferimenti audio-data
/schema-data nella cartella references/immagine-interattivo/.
