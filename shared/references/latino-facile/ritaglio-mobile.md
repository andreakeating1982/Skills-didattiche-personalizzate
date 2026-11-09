# Photo cropper — contratto produzione 8731 (28/10/2026)

## Fonte autorevole e precedenza

- URL: `https://latino-facile-app-2.easy-peasy.site`.
- Codice pubblicato: `3a4159402cb0f674ca2e269007d4cfcefe86bedd`.
- Leggere nella repo `SCROLLING-MOBILE.md`, `OCR-FOTO.md`,
  `tests/crop-mobile.e2e.mjs` e `tests/crop-drag.e2e.mjs`.
- Per clonare SOLO questo strumento leggere `photo-crop-clonabile.md` in
  questa cartella: contiene istruzioni, 18 file testuali interi e SHA-256.
- Superate le vecchie istruzioni che richiedevano `modal={false}`, icona
  centrale, AZZERA, due riquadri di comandi o ANNULLA/CONFERMA TAGLIO.

## Contratto dell'utente

Titolo **RITAGLIA LA FOTO**, senza istruzioni visibili sotto. Nessuna icona
centrale. Spostare il ritaglio toccando QUALSIASI punto utile dell'interno
selezionato, con dito o mouse; otto maniglie bianche per ridimensionare.
Quattro comandi marroni compatti **RUOTA SINISTRA / RUOTA DESTRA / CHIUDI /
RITAGLIA** nello stesso riquadro centrato. Nessun AZZERA. Target minimi 44px.

Pagina dietro FERMA; scroll interno su margini beige, testata e aree della
foto ESTERNE alla selezione, quando il contenuto supera il viewport. Dentro
la selezione il gesto MUOVE il crop e non fa pan. Il blog fuori dall'iframe
cross-origin non è controllabile: non promettere lock dei tocchi esterni.
Non chiedere all'utente test o log: verificare in autonomia.

## Dipendenze da portare insieme

| File | Responsabilità |
|---|---|
| `client/src/components/CropDialog.tsx` | modal true, scroll, quattro comandi, pointer capture e delta incrementali |
| `client/src/hooks/useCropDialogViewport.ts` | lock ripristinabile html/body, viewport visibile cross-origin |
| `client/src/index.css` | `.lf-crop-*`, target 44px, safe-area, `lf-crop-move` auto/none |
| `client/src/lib/heightSync.ts` | sospendere invii durante `data-lf-crop-open`, ripresa con `lf:crop-closed` |
| `client/src/lib/cropBox.ts` | geometria pura: moveBox, resizeBox, resizeCorner |
| `client/src/lib/imagePrep.ts` | normalizzazione EXIF; non importare backend latino |
| `tests/crop-mobile.e2e.mjs` | nove scenari layout/scroll/PNG/tastiera |
| `tests/crop-drag.e2e.mjs` | quattro scenari otto prese/direzioni/limiti/cancel |

Il foglio clonabile include anche Dialog/Button/utils, adattatore generico,
fixture senza OCR, dipendenze e test portabile. Non sovrascrivere tema/font
né dati dell'app di destinazione. Il crop è locale: non richiede chiavi IA.

## Interazioni da preservare

1. `modal={true}` SOLO in CropDialog; non alterare ColorDialog.
2. Body fixed con `!important` e top negativo, salvataggio di scrollX/Y,
   valori e priorità CSS. Radix impone relative important: senza precedenza
   il lock non funziona. Ripristinare tutto alla chiusura o unmount.
3. Vista autonoma: visualViewport; iframe: sonda fixed e
   IntersectionObserver.intersectionRect. rootBounds può essere null
   cross-origin; 100dvh dell'intero iframe NON è il telefono.
4. Solo titolo e foto in `min-h-0 flex-1 overflow-y-auto overscroll-contain
   touch-pan-y`. Tutti i comandi figli di `data-crop-controls`/`data-crop-footer`,
   flex-wrap centrato, align-items stretch. Nessuna istruzione sotto il titolo;
   `aria-describedby={undefined}`, titolo/nome dialogo e ARIA maniglie presenti.
5. Selezione `.lf-crop-move`: pointer-events auto e touch-action none anche
   su telefono. Maniglie touch-none. Capture sul wrapper STABILE della foto,
   non sul target che cambia posizione. Salvare un pointerId, ignorare gli
   altri; rilasciare su up/cancel/lostcapture; pointermove passive:false.
6. Calcolare il delta dall'ULTIMO evento e applicarlo al box appena aggiornato.
   Il vecchio delta dall'inizio accumulava eccesso al limite: invertendo il
   dito il box restava fermo. Difetto riprodotto sul 8730 nei quattro scenari;
   corretto e verificato sul 8731. NON modificare la geometria pura per questo.
7. `MIN_BOX=8%`, HANDLE_SIZE 44px, frecce 2% / Maiusc 10%; box libero fino
   a qualunque bordo. Nessuna sidebar né limite 50% sul crop. Foto piccole
   ingrandite solo visivamente, MIN_IMG_W 560, clamp alla larghezza utile e
   sottrazione del bordo 4px, proporzioni conservate.
8. `confirm()` e cropBox.ts INVARIATI durante modifiche layout/gesti.
   Rotazione e conferma PNG lossless, lato max 2200. JPEG max 1800 appartiene
   all'eventuale invio OCR/IA SUCCESSIVO. Non confondere i due stadi.
9. Sospendere heightSync nel lock e rimisurare dopo chiusura; protocollo,
   token, ping e soglie anti-loop invariati. Non serve cambiare l'embed blog.

## Collaudo e limiti

```bash
pnpm check
pnpm exec vitest run --no-file-parallelism
pnpm build
# Server già attivo:
node tests/crop-mobile.e2e.mjs
node tests/crop-drag.e2e.mjs
# Sul sito pubblico, senza vere chiamate IA:
CROP_QA_BASE_URL=https://latino-facile-app-2.easy-peasy.site node tests/crop-mobile.e2e.mjs
CROP_DRAG_BASE_URL=https://latino-facile-app-2.easy-peasy.site node tests/crop-drag.e2e.mjs
```

Rilascio verificato: 64/64 unitari, check/build; 9/9 layout con 201 controlli
E 4/4 drag con 143 controlli ripetuti sul pubblico. Kit ricostruito in
fixture separata: check/build e 6/6 scenari portabili. Touch emulato Chromium,
non telefono fisico iOS/Android. Canvas reale, OCR simulato; nessuna nuova
misura di accuratezza OCR/grammatica né certificazione accessibilità completa.

## Export e deploy

Includere sorgenti, guide, font/tessdata/PDF, patch, lockfile, CI, Dockerfile,
render.yaml, .env.example; mai credenziali/DB/cache. Verificare CRC/hash e
runtime identico al commit pubblicato. Se deploy cancella Dockerfile,
ripristinare SOLO il file noto da HEAD prima del checkpoint/export.
Una richiesta di export/skill NON autorizza un nuovo deploy. Produzione solo
su conferma separata dopo preview. Il pacchetto può aggiornare solo guide
senza necessità di ridistribuire il runtime.

