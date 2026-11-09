# PHOTO CROPPER 8731 nella produzione 8736 — 28/10/2026

Leggere per il nucleo del ritaglio foto, mobile/iframe e contratto 8731.
**Stato corrente: produzione 8737** — leggere PRIMA `seconda-pagina-8737.md`
per layout della pagina 2, bundle/hash e ZIP attuali. I dati 8736 sotto sono
storici; il nucleo del cropper è preservato nel deploy 8737.

## Versione e perimetro

- Produzione approvata dall'utente: **deploy 8736**, 28/10/2026.
- Progetto corrente della chat: `/home/user/espressioni-monomi-polinomi`;
  in questa sandbox è un symlink a `/home/user/espressione-frazioni-potenze`.
  Usare il percorso del contesto corrente, verificare `pwd -P` e `git log`.
  Non scegliere il vecchio `/home/user/espressioni-widget-matematico` solo
  perché compare nelle sezioni storiche della skill.
- Checkpoint pubblicato `d5a5f5373f4156b9b244785f56b8d5c646a274fc`;
  integrazione `0448af3`, collaudo e pulizia `90974e3`.
- Bundle verificato pubblico `index-CYaBE4Bd.js`, SHA-256
  `6fafb4ca54358f45b95c6e48c18b07894c08428c321765567dd97e53b6e2da92`.
  Le successive modifiche del solo pacchetto/documentazione non costituiscono
  un nuovo deploy. Non promettere l'identità di nuovi bundle senza verificarla.

## Contratto da preservare

L'utente ha chiesto di SOSTITUIRE completamente la vecchia finestra con il
clone fedele dell'allegato `CLONARE-PHOTO-CROPPER-AGGIORNATO-8731.md`.
Nucleo identico byte per byte: `CropDialog.tsx`, `useCropDialogViewport.ts`,
`cropBox.ts`, `cropBox.test.ts` e `photo-crop.css` (percorsi nel rapporto
`COLLAUDO-PHOTO-CROP-8731.md` del repository).

- Beige uniforme, titolo RITAGLIA LA FOTO; niente sottotitolo e niente
  icona centrale. Quattro pulsanti marroni in UN riquadro centrato:
  RUOTA SINISTRA, RUOTA DESTRA, CHIUDI, RITAGLIA. Nessun AZZERA.
- Otto maniglie da 44px dentro la foto, frecce 2% / Maiusc+frecce 10%.
  Drag diretto dell'interno, delta dall'ultimo evento e pointer capture
  sul contenitore stabile. Non sostituire con icona di movimento.
- `modal={true}` SOLO per CropDialog: body lock con ripristino esatto degli
  stili/scroll; scroll nel corpo del dialogo, comandi sempre visibili.
  **Supera la regola storica `modal={false}` della sessione 27/10.**
- Hook viewport: visualViewport standalone e IntersectionObserver negli
  iframe cross-origin. Non leggere il DOM del blog esterno.
- Importare `photo-crop.css` dopo Tailwind. Conservare guardia
  `data-lf-crop-open` in heightSync e rimisura dopo `lf:crop-closed`;
  lasciare invariati protocollo, token, ping e anti-loop.
- NON cambiare `confirm()`/`cropBox.ts` per aggiustare il layout.
  Uscita PNG lossless, lato massimo 2200px; `onConfirm(File)` invariato.
  `imagePrep.ts`/normalizzazione EXIF e consumer OCR della destinazione
  restano invariati: foto → pezzo correggibile, MAI calcolo automatico.

## Test e falsi negativi già risolti

- `pnpm check`, build; `(cd client && pnpm exec vitest run)`:
  **738 test passati, 28 saltati; 51 file passati, 28 saltati**.
- 19 scenari E2E, 425 controlli + 7 controlli foto piccola/X/Escape/PNG 2200px.
  Chromium touch emulato, non telefoni fisici. Blog cross-origin simulato.
  OCR simulato nei test d'integrazione, non una prova live del modello IA.
- `tests/crop-mobile.e2e.mjs`: route reale `/espressione`, mock `{text:'2+3'}`;
  attendere `[aria-label="Pezzi trascritti"] .katex`, non body.innerText:
  «Pezzi trascritti» è aria-label, non testo visibile. Non usare frase latina.
- Acquisire altezza iframe di riferimento DOPO il lock; variazioni precedenti
  all'apertura non sono tremolio durante il ritaglio.
- Vite può servire una route fixture vecchia: riavviare prima di diagnosticare.
- Runtime finale: NIENTE `/photo-crop-test`, PhotoCropDemo o PhotoCropBridge.
  Le copie per ripetere il collaudo sono SOLO `tests/fixtures/photo-crop/`;
  montarle temporaneamente secondo `tests/PHOTO-CROP.md`, poi rimuoverle.

## Esportazione e manutenzione futura

Usare la skill `zip-esportabile-guide-ia`, esportare sorgenti + asset/modelli,
lockfile e patches, guide e test. Escludere sempre `.env` reali,
`shared/env.generated.ts`, `dist/` (server con chiave incorporata),
`node_modules/`, `.git/`, cache/log/sessioni/database. Tenere `.env.example`
solo con valori vuoti. Controllare credenziali prima di consegnare.

Ricostruire da una nuova estrazione con `pnpm install --frozen-lockfile`,
`pnpm check`, test e build. Senza chiave la build deve riuscire; IA non
configurata = 503 atteso, non promettere costruzioni IA senza configurazione.
Non accedere/modificare dati reali durante il test di ricostruzione.

Ricostruzione del pacchetto 8736 effettivamente verificata: nuova estrazione,
installazione frozen-lockfile, check, 738 test e build riusciti senza chiave;
**tutti i 37 file dist/public identici** al client pubblicato. Server Express
HTTP 200, font HTTP 200, IA senza chiave 503 atteso, nessun DB usato.
Rapporto nel pacchetto: `VERIFICA-PACCHETTO-8736.md`.

