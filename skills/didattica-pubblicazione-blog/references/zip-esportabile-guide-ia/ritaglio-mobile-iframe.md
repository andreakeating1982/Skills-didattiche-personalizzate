# Esportare finestre mobile in iframe: contratto e dipendenze

## Modello verificato

Latino Facile, produzione **8731**, codice
`3a4159402cb0f674ca2e269007d4cfcefe86bedd`, 28/10/2026.
Le indicazioni di questo riferimento sostituiscono la variante iniziale 8728.

Non prescrivere modal=false universalmente: nel ritaglio attuale il dialogo
è MODALE, la pagina dietro FERMA. Titolo RITAGLIA LA FOTO, nessuna istruzione
sotto né icona centrale. Intera selezione trascinabile direttamente con
mouse/touch; pan nei margini e aree esterne, quando necessario. Quattro
comandi marroni compatti RUOTA SINISTRA/DESTRA, CHIUDI e RITAGLIA in un solo
riquadro centrato, senza AZZERA. Non estendere questo contratto al ColorDialog.

## File inseparabili

- CropDialog.tsx, hook useCropDialogViewport.ts, geometria cropBox.ts.
- CSS .lf-crop-* e guardia data-lf-crop-open/evento lf:crop-closed in heightSync.
- imagePrep/EXIF, UI Dialog/Button/utils, callback File PNG locale.
- tests/crop-mobile.e2e.mjs (9 scenari) e crop-drag.e2e.mjs (4 scenari).
- SCROLLING-MOBILE.md, OCR-FOTO.md, manifest aggiornato.

Dentro iframe alto, 100dvh NON misura il telefono: usare visualViewport
oppure IntersectionObserver.intersectionRect cross-origin, rootBounds può
essere null. Body fixed important con ripristino stili/scroll; sospendere
heightSync per non fare collassare la cornice. Non accedere al DOM del parent.

## Drag corretto

Selezione pointer-events:auto/touch-action:none anche mobile; capture sul
wrapper stabile della foto, un pointerId, fine su up/cancel/lostcapture.
Calcolare delta dall'ultimo evento e dal box aggiornato: delta dall'inizio
produce zona morta invertendo dopo un limite (difetto riprodotto nel 8730).
Preservare confirm(), cropBox e viewport durante correzioni di presentazione.

## Checklist export

1. Registrare deploy e commit runtime, distinta revisione documentale.
2. Includere tutti i file sopra, non solo JSX. Conservare font/tema ospite.
3. Verificare la guida: niente istruzioni attive per ripristinare icona,
   AZZERA, due pannelli o modal=false nel crop. Annotazioni storiche marcate.
4. Non importare backend OCR/IA specifico della sorgente in un clone crop.
5. Export da commit pulito: CRC, SHA-256 di ogni file, no segreti/runtime.
6. Se richiesto foglio autonomo, includere sorgenti interi in Markdown e
   SHA-256; ricostruirlo automaticamente e confrontare con il kit separato.
   Modello: PHOTO-CROP-CLONABILE.md di Latino Facile (anche nella sua skill).
7. Riprovare una fixture indipendente. Riferimento: 6 scenari portabili.
8. Dichiarare limiti: Chromium touch emulato non è iOS/Android fisico;
   canvas reale e risposta OCR simulata non misurano OCR né grammatica.
9. Consegnare kit crop E ZIP completo come file distinti. Controllare byte
   nella scheda consegna. Nessun deploy autorizzato da una richiesta export.

Rilascio 8731: check/build, 64 unitari; 9 layout/201 controlli e 4 drag/143
controlli ripetuti sul pubblico. Nessun nuovo codice embed richiesto.

