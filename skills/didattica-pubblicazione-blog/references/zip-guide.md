# ZIP esportabili e guide per IA

L'originale zip-esportabile-guide-ia è conservato con script e modelli.
Preferire `scripts/zip-esportabile-guide-ia/export_verified.py` dopo averne
verificato i REQUIRED e i contratti per la famiglia. Il vecchio
`export_zip.sh` è storico: git archive da solo non scansiona tutti i segreti
né produce il manifest richiesto. Non usarlo come export finale sicuro.
Per il caso corrente Espressioni8756 leggere
[espressioni-8756.md](espressioni-8756.md) e il toolkit specifico8756.
L'[audit riutilizzabile](audit-zip-github-render.md) e il toolkit8744
conservano la cronologia; non confrontare la8756 con hash8744.

## Aggiornamento recuperato dalla chat Espressioni (29/10/2026)

Per il pattern di export verificato più recente leggere
`originali/zip-esportabile-guide-ia-SKILL.md` e
`originali/zip-esportabile-guide-ia-export-sicuro-cropper.md`.
È incluso anche `scripts/zip-esportabile-guide-ia/export_verified.py`:
leggerne le opzioni prima dell'uso; esporta da HEAD e verifica il pacchetto.
Il profilo è completato con risorse locali 8744, senza sostituire i modelli
recuperati dall'altra chat. Un riordino documentale non autorizza un deploy.

## Contratto del pacchetto

- Contenuto del commit HEAD pulito, con package/lockfile, patch, client/server/
  shared pertinenti e tutti gli asset necessari. Non archiviare la workingdir
  sporca e non cancellare file utente per renderla pulita.
- Guide README, AGENTS, REBUILD, ADATTARE, RENDER, ACCESSIBILITA e manifest
  coerenti col codice. REBUILD ricostruisce identico, ADATTARE spiega varianti,
  RENDER trasferisce via GitHub e ACCESSIBILITA rende riusabili le misure.
- .env.example senza valori sensibili, render.yaml e CI se applicabili;
  nessun .env reale, segreto, DB runtime, .git, node_modules, dist o log.
- Cornice solo se pertinente; non reintrodurre cornice dinamica nell'app
  Cornice Universale che usa iframe fisso.

## Verifica

CRC, prefisso/percorsi sicuri, file richiesti, dimensioni reali e hash
sorgenti/asset rispetto al commit. Ricostruire l’archivio definitivo in una nuova estrazione
isolata, con chiavi/DB rimossi e dipendenze di build incluse anche con
NODE_ENV=production. Se la ricostruzione non è eseguibile, dichiarare il
limite e non presentare il pacchetto come collaudato da zero. Registrare controlli effettivi, non solo archivio apribile.
Gli script/tests di regressione referenziati sono sorgenti utili: non
escluderli come spazzatura; distinguere da file temporanei usa-e-getta.
Consegnare lo ZIP finale e i documenti/supporti pertinenti, non il solo report.

## Componenti clonabili e rilasci indipendenti

Per il solo cropper usare il foglio autonomo in didattica-app-lingue:
18sorgenti, hash, dipendenze e test. Non basta copiare il componente; non
clonare tutto Latino né il backend OCR. Preservare tema e dati destinazione.
La baseline crop8731 può restare corretta con app8754: verificare gli hash,
non forzare stessi ID. Non rigenerare il foglio per cambiare solo un numero.
Un nuovo ZIP non autorizza un deploy né aggiorna GitHub o il blog da solo.
Modelli di guida in references/zip-esportabile-guide-ia/modelli-guide.md.
