# Esportazione verificata con cropper mobile/iframe

## Stato corrente — produzione 8744

Il deploy autorizzato **8744** aggiunge pezzi con scorrimento interno
(`piece-display`, niente più fuoriuscita dai bordi su schermo stretto) e
didascalia solo «SCRIVI QUI L'ESPRESSIONE» in grassetto scuro.
Riferimento manutenzione: `espressioni-monomi-polinomi/references/seconda-pagina-8737.md`.
Conservare wrapper App, CSS, heightSync unico e regola `piece-display`;
includere specifica e test. JS corrente `index-BnuQEBUp.js`, CSS
`index-D1FTbNg8.css`; hash nel riferimento. Se dopo il deploy il sito serve
ancora gli asset vecchi (propagazione), ricontrollare dopo attesa; se il
deploy fallisce con «14 UNAVAILABLE», riprovare dopo attesa e annotare i
tentativi nel rapporto; verificare SEMPRE gli asset online (HTTP 200 e hash
identici) prima di dichiarare riuscito il deploy. Ricostruzioni precedenti
già verificate senza chiave/DB (install/check/738 test/build OK, file client
identici, Express root/font 200 e IA senza chiave 503 atteso).
Nell'archivio finale consentire solo il delta documentale rapporto/checklist
rispetto all'estrazione collaudo, verificando CRC e hash di tutti i payload;
allegare checksum dell'intero ZIP. I rapporti precedenti sono storici: non
certificano da soli un nuovo ZIP, ricostruire il pacchetto 8744.

## Caso consolidato e perimetro

Widget metacognitivo, produzione **8736** (28/10/2026), clone del ritaglio
sorgente 8731. Per gli invarianti funzionali leggere la skill manutenzione
`espressioni-monomi-polinomi` e il suo riferimento `photo-crop-8736.md`.
Non cambiare codice runtime durante una richiesta del solo ZIP/skill.

Esito reale del caso 8736: installazione frozen-lockfile, check, 738 test e
build riusciti in una nuova estrazione senza chiavi/DB. Tutti i **37 file
client compilati identici** alla versione pubblicata; Express HTTP 200,
font HTTP 200 e IA senza chiave 503 atteso. Il report è incluso nello ZIP
come `VERIFICA-PACCHETTO-8736.md`; la produzione non è stata ridistribuita.

## Procedura sicura

1. Verificare progetto corrente, Git pulito e commit; allineare le guide allo
   stato pubblicato. Non scrivere «solo anteprima» dopo deploy approvato.
2. Eseguire lo script `scripts/export_verified.py` di questa skill:
   usa soltanto file tracciati, esclude segreti/generated/runtime, verifica
   asset obbligatori, ricerca valori sensibili senza stamparli e aggiunge
   manifest SHA-256. Richiede Git pulito; non esegue seed né database.
3. Estrarre in cartella NUOVA e installare da lockfile, senza copiare .env,
   env.generated o node_modules. Disattivare variabili API/DB ereditate.
4. Eseguire `pnpm check`, suite reale del package e build. La build senza
   chiave deve riuscire; `shared/env.generated.ts` viene generato vuoto.
5. Confrontare gli hash di TUTTI i file client build pubblici con quelli
   della versione pubblicata/approvata. Il bundle SERVER con una chiave
   incorporata non coincide, ed è giusto NON esportarlo.
6. Smoke test con server Express su porta libera, DB disabilitato e chiave
   assente: HTTP 200; servizio IA 503 atteso. Non creare sessioni reali.
7. Salvare rapporto di ricostruzione e consegnare ZIP + SKILL.md aggiornati.

## Distinzioni importanti

- Un `git archive` esclude gli untracked ma **non garantisce assenza di
  segreti nei file tracciati**: scansione obbligatoria.
- `dist/index.js` può contenere una chiave cotta al build; non esportare
  `dist` né `shared/env.generated.ts`. `.env.example` può restare solo se
  i valori sensibili sono vuoti. Non includere backup del .env.
- Mantenere ONNX/WASM/Tesseract/font/PDF pubblici e lockfile/patches: non
  sono runtime da escludere. Il PDF didattico pubblico non è dato studente.
- Escludere solo diagnostici identificati; conservare test di regressione
  e fixture sintetiche. Non eliminare banchi di prova utili alla manutenzione.
- `tests/fixtures/photo-crop` NON deve essere montato nel runtime finale.
  Documentare come montare temporaneamente la route di collaudo.
- Non imporre `modal={false}` indistintamente. Per il cropper 8731 il
  contratto è `modal={true}`, viewport visibile e lock pagina; servono
  insieme componente, hook, CSS e guardia/evento heightSync.
- Playwright usa pointer/touch reali emulati; PointerEvent sintetici possono
  dare falsi negativi. OCR mock nei test non significa test IA live.

## Uso dello script

```sh
python3.11 /home/user/skills/zip-esportabile-guide-ia/scripts/export_verified.py \
  --project /home/user/espressioni-monomi-polinomi \
  --output /home/user/ESPRESSIONI-MONOMI-POLINOMI-AGGIORNATO.zip \
  --prefix espressioni-monomi-polinomi --deployment 8737
```

Lo script non modifica né dati né produzione. Blocca l'export se trova
credenziali o incongruenze; segnala solo nomi dei file, mai i valori.

