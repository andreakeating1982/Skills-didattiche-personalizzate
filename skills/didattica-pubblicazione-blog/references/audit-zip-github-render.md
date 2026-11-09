# Audit ZIP GitHub / clonazione / Render — pattern verificabile

Usare per ricontrollare un pacchetto già consegnato; un vecchio rapporto non
certifica un nuovo archivio. Caso storico: Espressioni8744; stato corrente
in [espressioni-8756.md](espressioni-8756.md). Applicare gli invarianti di
questo audit usando il toolkit8756 per la versione8756.

## 1. Inventario e precedenza

Leggere README, package/lockfile, CI, render.yaml, server e guide correnti.
Cercare istruzioni superate: flussi/routing/PDF cambiati, limiti rimossi,
modal=false del vecchio crop, copia di env.generated, solver universali
inesistenti o quiz non implementati. Non correggere il runtime per un audit
ZIP. Conservare integralmente le guide riscritte sotto docs/storico e
segnalarle come storiche, con le guide correnti chiaramente prioritarie.

## 2. GitHub e clonazione

Una radice con package/lock/patches e file nascosti inclusi; non caricare
il solo ZIP o una cartella annidata per errore. Mai chiavi, DB, sessioni,
.env reali o server compilato. Asset ONNX/WASM/Tesseract/font/PDF e test
sintetici sono necessari. Verificare dimensioni per singolo file e link
operativi. La clonazione esige nuovo contesto/app/repo/ambiente: nessun DB
condiviso né origin/deploy della sorgente. Le varianti di dominio richiedono
nuovi validatori/test, non soltanto titolo/prompt.

## 3. CI e Render

- Verificare il comando reale del package: Espressioni usa Vitest in client,
  non pnpm test; non mascherare zero test con passWithNoTests.
- In ambiente production forzare devDependencies per il build:
  pnpm install --frozen-lockfile --prod=false. Usare Corepack/packageManager.
- Blueprint Node/Express, non Static Site; PORT da piattaforma; chiave server
  personale con sync:false, nessun valore nel repo. DB opzionale: /tmp non
  garantisce persistenza dopo riavvii o tra istanze.
- Se il build server incorpora una chiave, artifact CI SOLO dist/public.
  Non impostare chiavi di produzione in CI per fare un controllo.
- CI non blocca automaticamente autoDeploy Render: documentare il gate da
  configurare o deploy manuale. Non affermare test su Render se solo locale.

## 4. Toolkit storico Espressioni8744 e successore8756

Per la versione corrente usare `scripts/espressioni-8756/`, stessi comandi
ma hash client8756 e font WOFF2 aggiunti allo smoke. Le copie8744 sotto
restano disponibili per ricostruire il vecchio archivio, non quello nuovo.


In `scripts/espressioni-8744/` sono inclusi:
- `scripts/export-verified.py`: export Git pulito, scanner e manifest;
- `scripts/verify-package.py`: integrità e ricostruzione opzionale;
- `tests/test_export_tools.py`: 14 test stdlib, nessun DB/API.

Lo script verifica è specifico della baseline8744 (JS/CSS, titolo, 738 test).
Non usarlo immutato per app diverse. I REQUIRED dell’export sono specifici.
Per applicarlo al repository copiare scripts e test nelle posizioni omonime,
o leggere il toolkit come riferimento; non riscrivere il runtime.

Dalla cartella del progetto:

```sh
python3 scripts/verify-package.py ../pacchetto.zip --report ../integrita.json
python3 scripts/verify-package.py ../pacchetto.zip --rebuild \
  --extract-to ../cartella-NUOVA --baseline-public dist/public \
  --report ../ricostruzione.json
python3 -m unittest discover -s tests -p 'test_export_tools.py' -v
```

Solo il controllo base non esegue codice dell’app. Rebuild: archivio fidato,
nuova estrazione, ambiente senza chiavi/DB, NODE_ENV=production e --prod=false,
install/check/Vitest/Python/build, chiave generata vuota, confronto client,
Express su porta libera, header e hash reali di font/modelli/WASM/PDF.
Nessun endpoint dati/sessioni e nessuna IA live. Arrestare il server al termine.

## 5. Consegna verificata

Distinguere N payload da N+1 entry con manifest; manifest non include sé
stesso. Consegnare checksum intero ZIP e rapporto esterno del nuovo archivio:
evitare il circolo di modificare lo ZIP per inserirvi il suo esito/hash.
Ricostruire il ZIP DEFINITIVO o documentare esattamente il delta successivo.
Conservare runtime e asset identici alla baseline approvata.

Consegna skill: pacchetto completo con risorse, non due soli file omonimi
SKILL.md. Per i file skill usare una scheda per ciascun percorso SKILL.md
e fornire backup ZIP. Un file locale aggiornato non aggiorna la libreria
account: distinguere consegna da installazione, confermare operazioni
account e verificare il pacchetto salvato. Nessun deploy autorizzato dal ZIP.

