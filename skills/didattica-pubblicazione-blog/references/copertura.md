# Alias, disponibilità e precedenza

Caricare la scheda corrente, non tutti gli originali. Fonte completa significa
cartella della skill disponibile, NON app ricostruita o ricollaudata.

| Nome storico | Scheda corrente | Disponibilità | Sostituzione originale |
|---|---|---|---|
| deploy-app-produzione | [deploy](deploy.md) | Parziale, ricostruita | Conservare fino al recupero risorse |
| zip-esportabile-guide-ia | [zip-guide](zip-guide.md) | Completa + originali 8744 in references/originali/ | Dopo installazione nuova skill |
| codici-embed-cornici | [cornici](cornici.md) | Parziale, ricostruita | Conservare fino al recupero risorse |
| cornice-universale | [cornice-universale](cornice-universale.md) | Completa | Dopo installazione nuova skill |
| presentazione-app-docx | [presentazioni-blog](presentazioni-blog.md) | Parziale, ricostruita | Conservare fino al recupero risorse |

## Originali integrati in questa installazione (chat del progetto, 29/10/2026)

In references/originali/ sono conservati gli originali locali aggiornati:
zip-esportabile-guide-ia-SKILL.md (stato 8744) e
zip-esportabile-guide-ia-export-sicuro-cropper.md (stato 8744, JS
index-BnuQEBUp.js, CSS index-D1FTbNg8.css). Stato: produzione 8744
verificata online al precedente rilascio. Nuovo audit del 29/10: guide
separate dallo storico, CI client-only/Vitest in client, Render
--prod=false e toolkit Python con 14 test. Nuovo ZIP da 333 payload +1
manifest; hash/esiti in verifica-pacchetto-2026-10-29.json. Nessun nuovo
deploy o verifica online è implicito in questo riordino.

## Fonti parziali e dati non verificati

- **deploy-app-produzione**: Descrizione corrente + rilascio effettivamente eseguito in questa chat. Mancano: sorgente originale SKILL.md.
- **codici-embed-cornici**: Descrizione corrente + estratti chat03/10 e23/10; numerazione storica da verificare. Mancano: scripts/estrai_codice.py, scripts/sostituisci_codice.py, scripts/suddividi_in_parti.py, scripts/rinumera_parti.py, DOCX corrente dell’utente (non una risorsa skill permanente).
- **presentazione-app-docx**: Solo descrizione corrente, allegati originali non presenti. Mancano: scripts/genera_presentazione.py originale.

## Precedenza

Richiesta attuale e codice verificato → scheda canonica → riferimenti tecnici
pertinenti → storico originale. Non ripristinare regole superate né usare
le vecchie istruzioni di deploy senza preview/consenso.

Nessuna vecchia skill è stata disattivata dall’account durante questo lavoro.
Le skill generali di sistema non sono sostituite o modificate.

