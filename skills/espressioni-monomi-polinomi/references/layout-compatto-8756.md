# Widget Metacognitivo — baseline pubblicata8756

## Quando e quale progetto

Leggere prima di intervenire su layout, altezza embed, scroll, PDF o ZIP
della versione corrente. Usare il progetto della chat
`/home/user/espressioni-monomi-polinomi` (symlink locale alla variante
universale `/home/user/espressione-frazioni-potenze`, non un'altra app).
Sito: https://espressioni-monomi-polinomi.easy-peasy.site
Il rilascio8756 del29/10/2026 è già approvato e pubblicato. Non ripubblicare
per richieste del solo ZIP/skill; non cambiare dati per verificare un archivio.

## Contratti da conservare

| Route | Frame | Regione scroll | Altezza |
|---|---|---|---|
| `/` | nessuno compatto | flusso prima pagina | naturale, non limitata |
| `/espressione` | `expr-input-frame` | `expr-input-page` |640px |
| `/esercizio` | `expr-exercise-frame` | `expr-exercise-scroll` |naturale fino a640px |

- Montare toolbar fuori dalle regioni di scroll. Regione nominata con
  `role=region`, `tabIndex=0`, focus visibile, overflow-y:auto, min-height:0.
- Pagina3: `height:auto`, `max-height:640px`, `flex:0 1 auto` sul figlio.
  NON basis0 con altezza naturale: può collassare. Un esercizio corto può
  comunque eccedere640px a causa di font/card reali: non ridurli per forzarlo.
- NON chiamare la regione `expr-exercise-page`: esiste una regola tipografica
  storica con quel nome che cambierebbe i font del flusso corrente.
- Fuori iframe limitare anche dal viewport visibile con l'effetto già in
  App.tsx; in iframe640px indipendenti da innerHeight. Unico heightSync,
  token/ping/source filter esistenti. Nessun nuovo observer locale.
- `position:relative` su frame/regione contiene MathML KaTeX invisibile.
  Preservare `piece-display`, scrollbar4px, contrasto e touch.
- In print rimuovere max-height/clipping; PDF reale di EsercizioFrazioni
  già su documento separato, con dati/svolgimento effettivo.
- Non toccare motore, sessioni, risposte, generatore PDF o cropper8731 per
  sistemare il layout. Ogni risultato resta dello studente; mai anticiparlo.
- Cropper modale8731: componente+hook+CSS+guardia heightSync invariati;
  drag diretto,8maniglie,PNG,quattro comandi. Regole8736 ancora valide.

## Asset e precedenza

Runtime approvato `82602edcb86273a2c2ae997cc97ac30dcaef2dba`, checkpoint
deploy `4868ef6e873ac659cc64581fc346dc60cca649e6`; documentazione post-verifica
`dcef03ceae59002422d2af3c5416de6b520c2a66`. Per il nuovo ZIP usare il commit
nel suo MANIFEST, non presumere che coincida con quello runtime.

- JS `index-4q0PEhNN.js`, SHA-256
  `734e0af599b2e49ae52bc3660155b241af6fc7223b2b3ea356ed05a4dc340d7c`.
- CSS `index-G2fFP9TG.css`, SHA-256
  `d86a90702741b80a751a8c76ee9f7e5a68fcf13cd939a768c1c941a1655eb2e8`.

Le note8737/8744 restano storiche. Nel repository leggere VERSIONE-8756,
REBUILD, AGENTS, docs/TERZA-PAGINA-ADATTIVA, docs/DEPLOY-8756; le guide
correnti prevalgono. Il codice embed Blogger non è cambiato.

## Collaudo ripetibile e limiti

- Tipi/build passati;738unitari passati/28saltati.
- Pagina3:7scenari/168controlli, test `exercise-scroll.e2e.mjs` incluso
  in `scripts/layout-8756/` con la regressione `input-scroll.e2e.mjs`.
- Pagina2/cropper:7scenari/151controlli. Rapporti della build in
  `references/collaudo-layout-8756.json`; non sono un nuovo test del ZIP.
- Eseguire gli E2E in sequenza con Playwright QA, non aggiungere route runtime.
  Sessioni/IA simulate, touch/viewport Chromium emulati, nessun telefono
  fisico o test live IA implicito. PDF HTML catturato con stub locale,
  non prova di stampante. Test print DOPO i messaggi altezza screen:
  print rimuove640px e produce volutamente altezze maggiori.
- Il clone DOM isolato del test prova solo il contratto di restringimento;
  non è uno stato reale dell'esercizio né un cambiamento del sorgente.
- Ricostruire il nuovo ZIP in cartella nuova senza chiavi/DB, confrontare
  TUTTO dist/public e conservare report esterno con SHA del definitivo.
  Non distribuire dist/index.js o shared/env.generated.ts, che possono
  incorporare credenziali. L'aggiornamento locale non installa la skill
  nell'account: consegnare SKILL.md con la scheda Aggiungi/Download.


## Nuovo ZIP8756 effettivamente ricostruito

Archivio ESPRESSIONI-MONOMI-POLINOMI-8756-GITHUB-RENDER-2026-10-29.zip,
commit52e4e8c69b168855b22d75e7212ff2d4d3d09d88,342payload+1manifest.
SHA-256 `d7929f16d31537983d9431cfed5e55b6169986e240aa823668dc803a06544b75`.
Nuova estrazione senza chiave/DB: install/check,738test+28saltati,
14test packaging e build riusciti; tutti i37file client identici alla
build pubblicata8756. Express/11asset e IA503atteso verificati.
Rapporto esatto incluso: [verifica-pacchetto-8756.json](verifica-pacchetto-8756.json).
L'archivio definitivo non è stato rigenerato dopo questo test.

