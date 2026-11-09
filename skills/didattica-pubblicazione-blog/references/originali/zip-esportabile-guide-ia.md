# Archivio di dettaglio — zip-esportabile-guide-ia

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/zip-guide.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Scopo e quando usarla
- Flusso di lavoro
- 1. Individuare l'app e il suo stato
- 2. Inventario dei contenuti del pacchetto
- 3. Scrivere o aggiornare le guide IA
- 4. Pulizia della repository prima dell'export
- 5. Generare lo ZIP
- 6. Verificare il pacchetto
- 7. Foglio autonomo per clonare solo il photo cropper
- 8. Consegna
- Regole d'oro
- Risorse della skill

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Pacchetto ZIP esportabile con guide IA — Pattern riutilizzabile

> **Aggiornamento 28/10/2026 — finestre mobile e iframe:** non prescrivere
> `modal={false}` come regola universale. Per un ritaglio che deve tenere
> ferma la pagina, il modello attuale Latino Facile è `modal={true}`, lock
> ripristinabile, viewport visibile anche cross-origin e corpo interno touch
> scorrevole. Leggere `/home/user/skills/didattica-pubblicazione-blog/references/zip-esportabile-guide-ia/ritaglio-mobile-iframe.md` quando si esporta
> o si clona questo comportamento. Non basta copiare CropDialog da solo.

## Scopo e quando usarla

Generare/aggiornare il **pacchetto ZIP esportabile** di un'app Easy-Peasy AI:
una repository GitHub-ready che un agente AI (o un docente) può usare senza altri
contesti. Il pacchetto soddisfa 4 requisiti:

1. **Ricostruzione IA**: un'IA può ricostruire l'app **identica** (`REBUILD.md`)
   o crearne una **variante in altra lingua/argomento** (`ADATTARE.md`) partendo
   dalla repository.
2. **Trasferimento Easy-Peasy → Render via GitHub** (`RENDER.md` + `render.yaml`
   + CI + `.env.example`).
3. **Sezione ACCESSIBILITÀ ben segnalata** (`ACCESSIBILITA.md`) con misure
   riutilizzabili su altre app simili.
4. **Cornice dinamica inclusa** (cartella `cornice-dinamica/` con embed iframe).

Riferimento reale già applicato: `latino-facile-app` (vedi la skill
`latino-facile`). Questa skill generalizza il pattern per QUALSIASI app.

## Flusso di lavoro

### 1. Individuare l'app e il suo stato

- Cartella del progetto: `/home/user/<nome-app>` (scaffold web-db-user o
  web-static). Nome repo = nome cartella.
- Verificare che sia una repo git con commit recenti: `git log --oneline -5`.
- Controllare che la versione sia quella definitiva (deploy produzione
  confermato dall'utente se applicabile). Registrare ID deploy, commit del
  codice pubblicato e limiti dei test in manifest/nota di rilascio. Una nuova
  esportazione o modifica alle guide NON è un'autorizzazione a fare deploy.

### 2. Inventario dei contenuti del pacchetto

Il pacchetto è il **contenuto del commit HEAD** via `git archive` (pulito:
niente `.git`, `node_modules`, `dist/`, `.env`, log, script di sviluppo
temporanei). Deve contenere:

- sorgenti complete (client + server + shared), `package.json`, `pnpm-lock.yaml`;
- patch pnpm se presenti (`patches/*.patch`);
- `.env.example` (MAI `.env`);
- `render.yaml` (Blueprint Render);
- `.github/workflows/ci.yml` (install → check → test → build);
- guide: `README.md`, `AGENTS.md`, `REBUILD.md`, `ADATTARE.md`, `RENDER.md`,
  `ACCESSIBILITA.md`, `manifest.json`;
- `cornice-dinamica/` (embed per il blog: html + README + fonts);
- asset statici dell'app (font, tessdata OCR, PDF, ecc.).

### 3. Scrivere o aggiornare le guide IA

Ogni guida vive nella **radice della repo** ed è scritta per un agente AI senza
altri contesti (ogni passo operativo, file esatti citati, codice bash pronto).
Se le guide esistono già, aggiornarle in parallelo a ogni modifica del codice.

- `README.md` — porta d'ingresso del pacchetto (cosa contiene, tabella guida→uso,
  stack, installazione, variabili, Render, cornice, struttura).
- `AGENTS.md` — punto d'ingresso per l'agente: quale guida seguire per quale
  compito + regole d'oro + comandi.
- `REBUILD.md` — ricostruzione completa e IDENTICA (mappa file, comportamenti da
  replicare, checklist, deploy Render, file esclusi).
- `ADATTARE.md` — creare una nuova app simile/tradotta (passi per testi, motore
  di contenuto, OCR, PDF, traduzione; accessibilità e cornice da NON toccare).
- `SCROLLING-MOBILE.md` (se l'app ha dialog su mobile) — guida IA clonabile dello
  scrolling mobile delle finestre.
- `RENDER.md` — trasferimento Easy-Peasy → Render via GitHub (passo-passo anche
  per non-tecnici, Blueprint, variabili d'ambiente, verifica, aggiornamenti).
- `ACCESSIBILITA.md` — SEZIONE DI RIFERIMENTO: tabella misure, dettaglio,
  mini-pacchetto riuso su altre app, checklist verifica.
- `manifest.json` — metadati macchina (stack, script, env, asset, guide, fileMap).

**Modelli sezione-per-sezione:** leggi `/home/user/skills/didattica-pubblicazione-blog/references/zip-esportabile-guide-ia/modelli-guide.md` e adattali
all'app concreta.

### 4. Pulizia della repository prima dell'export

- Rimuovere (o non tracciare) file indesiderati: `.env`, `.DS_Store`, log,
  `test-*.ts` usa-e-getta in radice, cartelle di utilità di sviluppo
  (`scripts/` con check-*.ts non referenziati), `dist/`, `node_modules/`.
- Le guide dichiarano (§8 di REBUILD.md) che la repo NON li contiene: mantenere
  la dichiarazione VERA.
- Verificare coerenza doc↔codice: ogni file/feature/font citato nelle guide deve
  esistere davvero (es. se il PDF usa il font dell'interfaccia, le guide NON
  devono citare un vecchio font PDF inesistente).
- Esaminare lo stato completo, anche lo STAGING, prima di salvare il checkpoint:
  non includere cancellazioni prodotte dal deploy (caso noto: Dockerfile) o
  modifiche estranee. Aggiungere solo i file previsti; lo ZIP nasce da HEAD.
- Non procedere con sorgenti/guide non committati: lo script di export deve
  fallire se working tree o staging non sono puliti. File runtime ignorati
  da git restano esclusi dal pacchetto.

### 5. Generare lo ZIP

```bash
# script pronto (consigliato)
/home/user/skills/didattica-pubblicazione-blog/scripts/zip-esportabile-guide-ia/export_zip.sh \
  /home/user/<nome-app> /home/user/<nome-app>-export-aggiornato-<DATA>.zip

# oppure manualmente
cd /home/user/<nome-app>
git archive --format=zip --prefix=<nome-app>/ HEAD \
  -o /home/user/<nome-app>-export-aggiornato-<DATA>.zip
```

Convenzione nome: `<nome-app>-export-aggiornato-<AAAA-MM-GG>.zip`.

### 6. Verificare il pacchetto

- `unzip -t` senza errori; conteggio file.
- Guide presenti: `ACCESSIBILITA.md`, `ADATTARE.md`, `REBUILD.md`, `RENDER.md`,
  `AGENTS.md`, `README.md`, `manifest.json`. Se l'app ha scatto/ritaglio/OCR:
  anche `OCR-FOTO.md` (riferimento: latino-facile-app).
- Se l'app ha finestre/dialog usate su mobile: includere `SCROLLING-MOBILE.md`
  con il contratto REALE (pagina dietro ferma o meno), gesti distinti e limiti.
  Nel modello Latino Facile pubblicato con deploy 8731: `modal={true}`, hook
  `useCropDialogViewport.ts`, CSS `.lf-crop-*`, guardia `data-lf-crop-open`
  in `heightSync.ts`, `tests/crop-mobile.e2e.mjs` (9 scenari) e
  `tests/crop-drag.e2e.mjs` (4). Titolo RITAGLIA LA FOTO senza istruzioni,
  niente icona centrale: intera selezione trascinabile con mouse/touch,
  delta incrementali e capture sul wrapper; pan su margini/zone esterne.
  Un solo riquadro con quattro comandi centrati, senza AZZERA. Non
  regredire a `modal={false}` né a `100dvh` dell'intero iframe come unica misura.
- `cornice-dinamica/` presente (README + embed dedicata/lite/universale +
  test impermeabile se l'app usa iframe).
- `render.yaml`, `.github/workflows/ci.yml`, `.env.example` presenti.
- Asset dell'app presenti (font, tessdata, PDF).
- NIENTE di indesiderato: `.env` reali, chiavi private, `node_modules`, `dist`,
  `.cache`, `.git`, log o DB di runtime. `.env.example`, `.github/` e `.gitignore`
  sono consentiti. Verificare CRC dell'archivio e dimensione reale in byte.
- Confrontare SHA-256 dei file archiviati con la repo committata, specialmente
  nuovi hook/test, font, tessdata e PDF: evitare uno ZIP formalmente integro
  ma vecchio/incompleto. Test mobile con OCR simulato non misura l'OCR reale.
- Controllare la dimensione della scheda di consegna rispetto al file locale;
  se è diversa, verificare e riconsegnare il file corretto senza scaricare
  l'onere della verifica sull'utente.

### 7. Foglio autonomo per clonare solo il photo cropper

Se richiesto, consegnare anche un Markdown con TUTTI i sorgenti testuali
necessari, CSS, hook viewport, guardia heightSync, dipendenze, adattatore
File→PNG→callback e test portabili. Modello: `PHOTO-CROP-CLONABILE.md` di
Latino Facile. Il foglio non deve richiedere vecchie chat o percorsi sandbox;
lo ZIP piccolo del kit deve contenere gli stessi file separati. Ricostruire
i blocchi Markdown e confrontare SHA-256, poi provare una fixture senza
analizzatore/backend della sorgente. Distinguere kit crop da ZIP completo.
Registrare deploy e commit effettivamente pubblicati, senza chiamare preview
un codice già in produzione. Non aggiornare l'embed se non è cambiato.

### 8. Consegna

- `send_attachment` con lo ZIP come file finale.
- Spiegare i 4 scopi coperti (ricostruzione IA, Render, ACCESSIBILITÀ, cornice)
  e come usare il pacchetto (estrarre → GitHub → `RENDER.md` o `ADATTARE.md`).

## Regole d'oro

1. **ZIP = commit HEAD pulito** (git archive), mai copia della working dir con
   spazzatura. Documentazione e repo devono essere allineate e committate prima.
2. **Guide per un'IA senza altri contesti**: ogni passo operativo con file
   esatti; nessun rimando a conversazioni passate; codice bash pronto.
3. **ACCESSIBILITÀ ben segnalata** in cima al documento (`>` ben visibile +
   navigazione rapida) e sempre con una guida al RIUISO su altre app (mini-
   pacchetto di file da copiare).
4. **Cornice dinamica sempre inclusa** quando l'app è pensata per il blog:
   cartella con README che spiega quale versione usare e come cambiare dominio.
5. **Mai `.env`, segreti, node_modules, dist, script temporanei** nel pacchetto;
   `.env.example` sì.
6. **RENDER.md per non-tecnici**: il percorso ZIP → GitHub → Render deve essere
   eseguibile da un docente (Blueprint consigliato; flusso alternativo per repo
   private) e deve dire come aggiornare la cornice col nuovo dominio.
7. **manifest.json e guide allineati al codice reale** (niente riferimenti a
   file o font che non esistono più).
8. Le guide dell'app restano **fonte di verità**: questa skill fornisce il
   pattern; la skill di manutenzione dell'app fornisce i dettagli specifici.

## Risorse della skill

- `/home/user/skills/didattica-pubblicazione-blog/scripts/zip-esportabile-guide-ia/export_zip.sh` — genera lo ZIP pulito da HEAD di qualsiasi repo
  (parametri: cartella-repo e file-output).
- `/home/user/skills/didattica-pubblicazione-blog/references/zip-esportabile-guide-ia/ritaglio-mobile-iframe.md` — dipendenze minime e controlli per esportare il ritaglio con pagina bloccata anche nel blog.
- `/home/user/skills/didattica-pubblicazione-blog/references/zip-esportabile-guide-ia/modelli-guide.md` — modelli sezione-per-sezione per scrivere
  README/AGENTS/REBUILD/ADATTARE/RENDER/ACCESSIBILITA/manifest su una nuova app.
