# RICOSTRUIRE QUESTA RACCOLTA DI SKILL

1. Estrarre lo ZIP in una cartella nuova oppure clonare il proprio repository. Non servono chiavi API.
2. Usare Python 3.11 o successivo. Il gestore usa solo la libreria standard; per eseguire il validatore YAML e i test delle integrazioni didattiche installare `requirements.txt` in un ambiente virtuale.
3. Lanciare `python3 tools/gestisci_skill.py verifica`. Devono risultare 55 skill, nessun errore e tutti gli hash del manifest validi.
4. Lanciare `python3 -m unittest discover -s tests -v`. I test del repository e quelli delle sintesi/mappe sono offline e creano soltanto copie temporanee.
5. Cercare una skill e leggerne il `SKILL.md`: `python3 tools/gestisci_skill.py trova "quiz con audio"`.
6. Per evitare dipendenze dai vecchi percorsi preparare una copia con `python3 tools/gestisci_skill.py prepara --dest ../skills-runtime --workspace ../lavoro`.
7. Procurarsi input e progetti esterni necessari; installare solo le dipendenze della skill scelta. Non eseguire un rendering/clone che si aspetta risorse mancanti.

## NON CONFONDERE TRE VERIFICHE

- **Integrità della raccolta:** manifest, metadati, link attivi, sintassi e preparazione portabile.
- **Esecuzione di una skill:** dipende da input, strumenti, asset e test del caso concreto.
- **Ricostruzione di una app:** richiede anche il suo repository completo, lockfile, configurazione e test/build reali. Questa raccolta non li sostituisce.

## AGGIORNARE IL MANIFEST DOPO MODIFICHE VOLUTE

Verificare prima diff, segreti e test. Poi lanciare `python3 tools/aggiorna_manifest.py` e rieseguire `verifica`. Il manifest è un controllo d’integrità, non una firma crittografica autenticata; l’hash dello ZIP originale consegnato resta un riferimento separato.

