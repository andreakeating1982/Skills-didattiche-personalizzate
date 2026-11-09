---
name: didattica-pubblicazione-blog
description: "Pubblicare le app didattiche e preparare ZIP GitHub/Render con guide IA, cornici Blogger, documento CODICI-EMBED-CORNICI, app Cornice Universale e presentazioni DOCX brevi per il blog. Usare per preview/produzione, checkpoint, verifica URL del progetto corretto, REBUILD/ADATTARE/RENDER/ACCESSIBILITA/AGENTS, esportazione pulita, postMessage e cornici numerate. Non usare come sostituto delle skill di manutenzione funzionale delle app. La pubblicazione richiede preview condivisa e consenso esplicito successivo; la richiesta di uno ZIP o skill non autorizza deploy."
---

# Pubblicazione e blog — un unico flusso affidabile

| Operazione | Riferimento |
|---|---|
| Preview, produzione, progetto sbagliato, verifica online | [Deploy](references/deploy.md) |
| ZIP ricostruibile, guide IA, GitHub → Render | [ZIP e guide](references/zip-guide.md), [audit riutilizzabile](references/audit-zip-github-render.md) |
| Widget Metacognitivo pubblicato8756 | [Pacchetto e rilascio8756](references/espressioni-8756.md) |
| Embed Blogger o DOCX dei codici numerati | [Cornici e codici](references/cornici.md) |
| App Cornice Universale con documento nascosto/visibile | [Cornice Universale](references/cornice-universale.md) |
| Presentazione breve di un'app in DOCX per il blog | [Presentazioni](references/presentazioni-blog.md) |
| Script, provenienza e alias | [Risorse](references/risorse.md), [copertura](references/copertura.md) |

Ricercare un alias senza leggere gli altri casi:
`python3 scripts/trova_profilo.py "codici embed cornici"`.

## Guardrail comuni

1. Verificare il contesto progetto corrente della chat. Non pubblicare altre
   app solo perché sono citate nelle skill o hanno un repository disponibile.
2. Leggere README/AGENTS e la skill funzionale pertinente prima di cambiare
   codice. In questa skill occuparsi solo della pubblicazione richiesta.
3. Checkpoint → preview → test → condividere URL → FERMARSI e chiedere consenso.
   Produzione in un turno successivo solo dopo un sì esplicito, con checkpoint.
4. Non trattare aggiornamenti di skill/guide/ZIP come autorizzazioni al deploy.
   Evitare cancellazioni o seed su dati veri anche in ambiente preview.
5. Esportare dal commit pulito con lockfile/patch/asset e guide coerenti. Mai
   .env, chiavi, database reali, log, node_modules, dist o cartelle .git.
6. Per Node/Render verificare install con `--prod=false` se il build usa
   devDependencies e NODE_ENV=production. CI nella directory reale dei test;
   artifact solo client se il server può incorporare chiavi. L’autodeploy
   Render non attende automaticamente CI. Verificare il servizio reale.
7. Non eliminare file utente per ottenere un albero pulito. Controllare diff e
   staging; il deploy può rimuovere Dockerfile: ripristinare solo l'artefatto
   noto confrontandolo con HEAD, senza annullare altre modifiche.
8. Verificare sito/bundle ed effettivi asset e PDF: HTTP200 non basta se la
   route restituisce la SPA invece del file. Descrivere limiti e simulazioni.
9. Consegnare allegati finali permanenti o sito. Non promettere che modificare
   un file locale aggiorni automaticamente GitHub, il blog o tutte le chat.

## Non confondere le cornici

- La cornice dinamica Blogger usa il protocollo specifico dell'app, token e
  filtro e.source. Preservare i canali reali, font self-hosted e anti-loop.
- L'app Cornice Universale usa un iframe FISSO e stato server condiviso;
  il suo vecchio resize dinamico è stato rimosso. Non reintrodurlo.
- Il DOCX dei codici contiene HTML numerato: non equivale al codice delle app
  né all'app Cornice Universale. Leggere la versione utente corrente prima
  di sostituire un codice o assegnarne uno libero.
- Presentazioni blog: titolo + un paragrafo, massimo 15 righe totali,
  circa 150 parole e hyperlink cliccabile; niente immagini o box salvo richiesta.

## Copertura e risorse mancanti

Sono disponibili gli originali zip-esportabile-guide-ia e cornice-universale.
Deploy, codici DOCX e presentazione sono profili ricostruiti da descrizioni;
gli script originari dei codici e il generatore DOCX non sono inclusi.
Per il Widget Metacognitivo il caso corrente è8756, con toolkit
`scripts/espressioni-8756/`;8744 resta storico con i suoi hash.
Gli aggiornamenti autorevoli prevalgono sugli appunti datati conservati in
references/originali. In particolare non includere password storiche nelle
guide, non perdere il lockfile e non usare gli esempi di deploy diretto.

