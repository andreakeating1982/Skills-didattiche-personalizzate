# Caso corrente8756 — export fedele dopo modifica del layout

Usare per aggiornare ZIP del Widget Metacognitivo già pubblicato8756.
I documenti8744 restano storia; non richiedere identità col vecchio client.
La richiesta di ZIP/skill non autorizza un altro deploy o modifiche ai dati.

## Contratti del runtime pubblicato

Pagina2 /espressione frame640px e scroll interno; pagina3 /esercizio naturale
fino a640px, expr-exercise-frame/expr-exercise-scroll, toolbar fuori.
Regione pagina3 con flex:0 1 auto, min-height:0; NON expr-exercise-page per
collisione font. Prima pagina non limitata; viewport solo standalone,
iframe indipendente dal child, unico heightSync. Cropper8731 modale con
hook/CSS/guardia heightSync invariati. Print senza limite, PDF separato.
Risposte solo dello studente, motore/IA/sessioni non toccati per il layout.

## Guide e verificatore

Allineare README, REBUILD, VERSIONE-8756, AGENTS, ADATTARE, RENDER,
ACCESSIBILITA e docs/PACCHETTO-ESPORTABILE. Non eliminare i documenti
storici per ottenere una consegna apparentemente pulita.
`scripts/verify-package.py` del progetto deve usare:
- assets/index-4q0PEhNN.js:
  `734e0af599b2e49ae52bc3660155b241af6fc7223b2b3ea356ed05a4dc340d7c`;
- assets/index-G2fFP9TG.css:
  `d86a90702741b80a751a8c76ee9f7e5a68fcf13cd939a768c1c941a1655eb2e8`.

Il toolkit8756 è anche nella skill didattica-pubblicazione-blog, separato da
quello8744. Verificare prima dell'uso i REQUIRED specifici di questa app.
Export con deployment8756 dal commit pulito: scansione valori segreti e
firme note senza stamparli, CRC/hash payload e manifest, nessun env/DB/dist.

## Rebuild del definitivo e consegna

Estrarre in cartella nuova senza chiave/API/DB ereditati; NODE_ENV=production,
frozen-lockfile --prod=false, check, Vitest da client,14test Python e build.
Baseline unitari738/28saltati; confrontare TUTTO dist/public, non il server
che può incorporare chiavi. Smoke root/header e font/ONNX/WASM/Tesseract/PDF
per hash reale; IA503 atteso senza chiave. Non creare sessioni o usare API live.
Tenere report e SHA del definitivo FUORI dall'archivio per evitare circoli.
Non rigenerare dopo la ricostruzione; se serve cambiare documenti descrivere
il delta esatto o ripetere il test. Non spacciare vecchio esito per nuovo.

I rapporti layout8756 hanno7scenari/168controlli pagina3 e7/151 pagina2/cropper,
ma sono test sintetici distinti dalla ricostruzione del nuovo archivio.
Per skill aggiornate consegnare le cartelle complete con riferimenti/script,
validazione e schede SKILL.md: l'account non si aggiorna da un file locale.


## Verifica reale del nuovo archivio

Commit52e4e8c69b168855b22d75e7212ff2d4d3d09d88,342payload+1manifest,
SHA-256 `d7929f16d31537983d9431cfed5e55b6169986e240aa823668dc803a06544b75`.
Ricostruzione isolata del definitivo riuscita:738test/28saltati,14packaging,
check/build,37file client tutti identici alla produzione8756.
HTTP/11asset reali e IA503senza chiave verificati; nessuna IA live o DB.
Rapporto [verifica-pacchetto-8756.json](verifica-pacchetto-8756.json) incluso.
Questa prova è nuova e non riciclata dai rapporti8744.

