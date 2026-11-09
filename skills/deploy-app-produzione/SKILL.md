---
name: deploy-app-produzione
description: "Guida al deploy in produzione delle app web Easy-Peasy (scaffold web-db-user e web-static, incluse le app didattiche). Regola fondamentale: il deploy va eseguito NELLA chat della singola app, perché webdev_deploy è legato al progetto corrente di quella chat; le repo GitHub esportate servono per Render, non per Cloud Run. Include la checklist di coerenza UI cross-app. Usare per: deploy preview/produzione, capire perché un deploy punta all'app sbagliata, pubblicare su Cloud Run (*.easy-peasy.site) o Render, armonizzare lo stile tra più app."
---

# Deploy in produzione delle app Easy-Peasy

## Regola fondamentale (non ovvia)

Il sistema webdev di Easy-Peasy (`webdev_deploy`, `webdev_save_checkpoint`, ecc.) è legato al **progetto corrente della chat in cui ti trovi**. Ogni chat ha un proprio "progetto corrente" con un proprio servizio Cloud Run associato.

Conseguenze operative:

- Pubblica un'app **sempre nella chat di quella stessa app** (dove è il progetto corrente).
- Se provi a deployare un'app diversa dalla chat sbagliata, il deploy punta al servizio dell'app corrente e la **sovrascrive** (non crea un servizio nuovo).
- Non fidarti ciecamente dell'URL restituito: verifica cosa viene realmente servito controllando il `<title>` della pagina (curl) e i processi attivi (es. `ss -tlnp | grep 3000`).
- `webdev_view_project` legge correttamente un `project_dir` arbitrario, ma `webdev_deploy` usa il progetto corrente della chat: questo è il motivo per cui un deploy "riuscito" può mostrare l'app sbagliata.

## Workflow deploy in produzione

1. **Verifica stato** — `git status`: committa eventuali modifiche non salvate con messaggio chiaro (`git add <file> && git commit -m "..."`).
2. **Checkpoint** — `webdev_save_checkpoint` (obbligatorio prima della produzione).
3. **Preview** — `webdev_deploy` con `mode="preview"`. Verifica HTTP 200 + `<title>` corretto con curl.
4. **Conferma** — condividi l'URL di preview e chiedi esplicitamente il via alla produzione.
5. **Produzione** — dopo conferma esplicita in un messaggio nuovo, salvare nuovamente `webdev_save_checkpoint` e usare `webdev_deploy` con `mode="production"`. Una richiesta successiva di ZIP/skill non autorizza altri deploy.
6. **Verifica post-deploy** — URL `.run.app` e `.easy-peasy.site`: HTTP200 e titolo corretto, hash dei bundle/client effettivi, asset/font reali (non la SPA servita al posto del file) e smoke browser del comportamento richiesto. Non scrivere dati reali per collaudare il deploy.

## Preview vs Produzione

- **Preview**: URL temporaneo della sandbox (porta 3000), legato alla vita della sandbox.
- **Produzione**: URL Cloud Run permanente (`*.run.app`) + URL friendly (`*.easy-peasy.site`). Aggiornare la produzione = aggiornare il servizio esistente, non ricrearlo.

## Repo GitHub esportate e Render

Le app esportate come repo GitHub (con `render.yaml`) sono configurate per **Render**, non per il deploy Cloud Run di Easy-Peasy.

Per pubblicarle:

- **Su Cloud Run Easy-Peasy**: vai nella chat dell'app → `git pull origin main` (o clona la repo) → deploy in produzione da lì.
- **Su Render**: collegare la repo e verificare il Blueprint prima di Apply; confermare operazioni conseguenti. L'autodeploy non attende automaticamente la CI. Se il Chrome personale è connesso, l'utente può fare login nel proprio tab; in browser gestito aprire prima il login e usare il passaggio interattivo previsto. Non chiedere password in chat.

## Caso consolidato: Widget Metacognitivo8756,29/10/2026

Produzione8756 già approvata: pagina2 a640px, pagina3 adattiva fino a640px,
scroll interno e toolbar ferma. Il dominio espressioni-monomi-polinomi
resta lo stesso e l'embed non deve essere sostituito. Verificati titolo,
asset JS/CSS, font WOFF2 e scroll delle due pagine nel Chrome personale.
Le guide dettagliate sono nella skill manutenzione e nel repo dell'app;
non applicare automaticamente questo limite a tutte le app.
Distinguere aggiornamento del pacchetto8756 da un nuovo rilascio: aggiornare
skill/documenti, salvarne la versione e consegnare ZIP non significa deploy.
Non attribuire all'installazione di skill locali un aggiornamento automatico
della libreria account, di tutte le chat o del repository GitHub.

## Coerenza UI cross-app

Per armonizzare lo stile tra più app didattiche (MAIUSCOLO, header centrato, casella studente, fix rientro, pulizia file morti), leggi `references/coerenza-ui-cross-app.md`.
