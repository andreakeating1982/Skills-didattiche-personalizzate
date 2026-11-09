# Export e skill — Widget Metacognitivo, produzione8756

## Stato e perimetro

App corrente `/home/user/espressioni-monomi-polinomi`, pubblicata8756 il29/10.
URL pubblico espressioni-monomi-polinomi.easy-peasy.site invariato.
Il pacchetto8756 sostituisce quello8744 senza un nuovo deploy: includere
sorgenti runtime già approvati, guide aggiornate e test/rapporti di layout.
Conservare gli originali8744 come storia, non istruzioni prioritarie.

## Layout che il pacchetto deve riprodurre

Pagina2 frame640px e regione expr-input-page; pagina3 altezza naturale
fino a640px, frame expr-exercise-frame e regione expr-exercise-scroll.
Toolbar fuori dallo scroll, ARIA/focus, nessun font ridotto; prima pagina
non limitata. In pagina3 flex-basis:auto, NON0; non usare expr-exercise-page
perché collide con vecchi font. Viewport solo standalone, iframe con limite
indipendente dal child. Unico heightSync/token e nessuna modifica all'embed.
PDF print senza limiti; cropper8731 modale invariato, come motore e sessioni.
Mai risposte automatiche o anticipazioni della soluzione.

## Toolkit corrente incluso

`scripts/espressioni-8756/scripts/export-verified.py`,
`scripts/espressioni-8756/scripts/verify-package.py` e
`scripts/espressioni-8756/tests/test_export_tools.py`:
14test stdlib; specifici di questa app e dei suoi hash, non solver generici.
Per eseguirli mantenere cartelle scripts/tests sotto la stessa radice.

- JS index-4q0PEhNN.js SHA-256
  `734e0af599b2e49ae52bc3660155b241af6fc7223b2b3ea356ed05a4dc340d7c`.
- CSS index-G2fFP9TG.css SHA-256
  `d86a90702741b80a751a8c76ee9f7e5a68fcf13cd939a768c1c941a1655eb2e8`.

Leggere README, REBUILD, VERSIONE-8756, AGENTS, RENDER, ACCESSIBILITA,
ADATTARE e docs/PACCHETTO-ESPORTABILE del progetto. Non cambiare runtime,
lockfile o patches per il solo export; aggiornare soltanto le guide obsolete.

## Workflow del definitivo

1. Registrare in checkpoint le guide/toolkit; verificare zero delta runtime
   rispetto al rilascio approvato. Usare Git pulito e output fuori dal repo.
2. Export con `--deployment 8756`,
   manifest con commit esatto e scanner credenziali. Escludere env,
   env.generated, dist/server, sessioni, DB, dipendenze, log e .git.
3. Estrarre il ZIP definitivo in una cartella NUOVA, non copiarvi .env,
   node_modules o credenziali. Togliere API/DB ereditati, NODE_ENV=production,
   install frozen-lockfile --prod=false, check, Vitest da client, test Python,
   build e confronto TUTTO dist/public, non soltanto JS/CSS.
4. Smoke Express su porta libera: root/header, font WOFF2/TTF, ONNX/WASM,
   Tesseract/PDF veri per hash; IA503 atteso senza chiave. Nessun endpoint
   di scrittura/sessione né IA live. Terminare il server dopo il test.
5. Calcolare SHA256 del definitivo e rapporto ESTERNO: non creare circolo
   inserendo nel ZIP il suo stesso checksum. Non mutare il ZIP dopo il test.
6. Validare le skill, controllare script e link attuali. Consegnare ZIP
   principale, rapporto leggibile, checksum e backup ZIP delle skill.
   SKILL.md uno per scheda aggiungibile, non soli file omonimi sciolti.

## Verifiche distinte

Build8756 già collaudata:738passati/28saltati; pagina3 7scenari/168controlli,
pagina2/cropper7/151. E2E con fixture e touch emulati, non telefoni fisici.
Rebuild ZIP è un nuovo test; consultare `verifica-pacchetto-8756.json` per
commit, numero payload e checksum finali, senza riciclarli dal8744.
In produzione8756 già verificati asset/font e scroll tramite Chrome;
questa richiesta di packaging non autorizza ripubblicare né creare Render.
Un file skill aggiornato localmente non sostituisce automaticamente quello
nella libreria account: consegnare la scheda, senza eliminare altre skill.


## Esito verificato del definitivo

ZIP8756:342payload+1manifest,48.919.795byte;
commit52e4e8c69b168855b22d75e7212ff2d4d3d09d88.
SHA-256 `d7929f16d31537983d9431cfed5e55b6169986e240aa823668dc803a06544b75`.
Ricostruito dall'archivio definitivo: install/check,738unitari/28saltati,
14test Python/build,37file client tutti identici. Smoke Express,11asset
reali e IA503senza chiave; nessun endpoint dati, DB o servizio IA utilizzato.
Conservare il [rapporto effettivo8756](verifica-pacchetto-8756.json) incluso.
Il definitivo non è stato modificato dopo la ricostruzione. I rapporti
esterni e la consegna delle skill non richiedono una nuova esportazione app.

