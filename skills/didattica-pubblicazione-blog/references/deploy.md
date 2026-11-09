# Deploy: identità del progetto, gate e verifica

## Scegliere il contesto corretto

La pubblicazione è legata al progetto corrente della chat, non al nome della
repo passata a un comando. Se si sta riordinando le skill o lavorando su Latino,
non pubblicare un'app diversa solo perché compare in un riferimento. Usare
la chat della singola app. I repository GitHub esportati permettono Render;
non cambiano da soli il binding di Cloud Run.

## Prima di pubblicare

1. Verificare richiesta, progetto/README, branch, diff/staging, URL e versione
   approvata. Non includere file estranei o dati reali.
2. Tipi, test e build adeguati; verificare UI/PDF/asset interessati.
3. Salvare checkpoint e creare preview. Condividere l'URL, fermarsi e chiedere
   conferma per la produzione. Anche costruisci e deploy iniziale significa
   preview, non consenso preventivo alla produzione.
4. Solo con consenso esplicito in un NUOVO messaggio: confermare checkpoint
   della versione approvata e pubblicare. Non ricambiare codice durante il
   rilascio per aggiungere feature non richieste.

## Verificare il risultato reale

- Aprire l'URL restituito e controllare pagina, bundle/versione e asset.
- Provare il percorso modificato su desktop/mobile/iframe e il PDF scaricato,
  dichiarando API simulate e touch emulato. HTTP200 da solo non prova un PDF:
  controllare MIME/contenuto e checksum quando applicabile.
- Non dichiarare guasto per un403di bot/COEPdev senza confronto nel browser.
- Ripristinare solo eventuale Dockerfile eliminato dal deploy confrontandolo
  con HEAD. Non eseguire reset/clean globale.
- Registrare deploymentId e commit di runtime separati dal successivo commit
  di sole note. Non ripubblicare per aggiornare la documentazione locale.
- Se URL resta uguale, l'embed normalmente resta valido; non modificarlo a
  caso. Se cambia, aggiornare solo i riferimenti effettivamente coinvolti.

## Coerenza cross-app senza refactoring indiscriminato

Per armonizzare stili confrontare header, dimensioni, margini Welcome, barra,
pulsanti multilinea, font e PDF; conservare le differenze di contratto e non
cambiare tutte le app per una richiesta su una sola. Il database di preview e
produzione può essere condiviso: nessun DELETE/reset/seed per fare test.

Fonte originale assente: ricostruzione dalla descrizione e dal flusso realmente
eseguito qui. Non presentarla come copia byte-identica della vecchia skill.
