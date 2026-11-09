# Espressioni — manutenzione e pacchetto della produzione8756

Usare questa scheda come stato corrente del Widget Metacognitivo.
Gli originali8744 e `espressioni-pacchetto-8744.md` sono cronologia.
Non modificare profili di altre app solo per aggiornare questo caso.

## Identità e contratti riusabili

- Progetto chat `/home/user/espressioni-monomi-polinomi`, variante universale
  locale `/home/user/espressione-frazioni-potenze` (symlink), non due deploy.
- Pubblico https://espressioni-monomi-polinomi.easy-peasy.site, deploy8756.
- Pagina2 `/espressione`: `expr-input-frame`,640px, `expr-input-page` scorrevole.
- Pagina3 `/esercizio`: `expr-exercise-frame`, altezza naturale fino a640px;
  `expr-exercise-scroll`, flex:0 1 auto, min-height:0,overflow-y:auto.
- Toolbar fuori dallo scroll, regioni nominate con role=region/tabIndex=0,
  focus e contrasto. Prima pagina non limitata. Viewport visibile solo fuori
  iframe; nell'iframe limite indipendente dal child, unico heightSync.
- Non usare `expr-exercise-page` per la regione attuale: collisione con
  font storici. `position:relative` contiene MathML KaTeX invisibile.
- Stampa senza limite; PDF corrente EsercizioFrazioni su documento separato.
  Cropper8731, risposte, motore e sessioni invariati. Nessun risultato
  anticipato o autocompilato, neanche in TTS; mai reintrodurre il promemoria
  permanente della frazione impilata rimosso dall'utente.

## Cloni e limiti

Conservare input, cropper, accessibilità e filosofia DSA; nuova app/repo,
chiave personale e DB distinto se necessario. Non basta cambiare il titolo
per un solver di qualunque grado o un quiz con dashboard. Validare il nuovo
dominio e il PDF. Un limite640px non deve ridurre i font o eliminare card.
Se si trapiantano soltanto pagine1/2 non imporre un wrapper a una pagina3
diversa senza analizzarla. Per il cropper portare componente, hook, CSS e
heightSync insieme; non toccare confirm/cropBox per problemi di layout.

## Verifiche e pacchetto

Baseline runtime82602ed, pre-deploy4868ef6, post-verifica documentale dcef03c.
Nuovo ZIP: identificare commit e numero file dal suo MANIFEST-SHA256.json,
non dal vecchio pacchetto8744. Guide autorevoli VERSIONE-8756, REBUILD,
ADATTARE, RENDER, ACCESSIBILITA e AGENTS. Nessun deploy/Render per fare ZIP.

Asset client8756 da preservare:
- JS index-4q0PEhNN.js:
  `734e0af599b2e49ae52bc3660155b241af6fc7223b2b3ea356ed05a4dc340d7c`.
- CSS index-G2fFP9TG.css:
  `d86a90702741b80a751a8c76ee9f7e5a68fcf13cd939a768c1c941a1655eb2e8`.

738unitari/28saltati;7scenari/168controlli pagina3 e7/151 pagina2/cropper.
Sessioni/IA e viewport/touch sono simulati, non telefoni fisici o IA live.
Print verificato separatamente da screen; PDF HTML reale catturato localmente,
non stampa fisica. La ricostruzione del nuovo ZIP è un esito ulteriore,
registrato nel rapporto esterno e nella risorsa `verifica-pacchetto-8756.json`
quando disponibile; i vecchi rapporti non lo certificano.

Per packaging usare la skill pubblicazione: il toolkit specifico corrente è
scripts/espressioni-8756/, quello8744 conserva i suoi vecchi hash.
Consegnare skill complete tramite SKILL.md; aggiornare file locali non
modifica automaticamente la libreria account né richiede disattivare altri profili.


## Esito del pacchetto8756 consegnato

Nuovo ZIP8756, commit52e4e8c69b168855b22d75e7212ff2d4d3d09d88,
342payload+1manifest, SHA-256
`d7929f16d31537983d9431cfed5e55b6169986e240aa823668dc803a06544b75`.
Ricostruzione del definitivo riuscita senza chiavi/DB:738unitari/28saltati,
14test packaging, tipi/build e37file client identici; HTTP/font/ONNX/WASM/
Tesseract/PDF verificati e IA503atteso. Consultare il
[rapporto8756](verifica-pacchetto-8756.json) incluso. Non attribuire questi
esiti al vecchio ZIP8744 né alle varianti non ancora implementate.

