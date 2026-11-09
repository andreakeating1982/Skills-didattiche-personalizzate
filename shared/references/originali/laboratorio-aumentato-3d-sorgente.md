# Archivio di dettaglio — laboratorio-aumentato-3d-sorgente

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/laboratori.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Percorsi
- Cos'è l'app (struttura FISSA, non cambia mai)
- Cosa significa "set di domande" (contenuto VARIABILE)
- Procedura di clonazione (script — consigliata)
- 1. Prepara il config JSON (opzionale ma consigliato)
- 2. Esegui lo script
- 3. Verifica
- Procedura di clonazione (manuale — fallback)
- Cosa NON toccare (struttura FISSA)
- Deploy, ZIP, embed
- Flusso GitHub
- Attenzione

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Laboratorio Aumentato 3D Sorgente

Clona l'app sorgente in una nuova app identica cambiando solo il contenuto dell'attività. Supporta il clone da **cartella locale** o da **repository GitHub**.

## Percorsi

- **App sorgente locale**: `/home/user/laboratorio-visivo`
- **Preview sorgente**: `https://3000-iycc2cajgdo49lj9lv8lq.sandbox.easy-peasy.ai/`
- **Production sorgente**: `https://laboratorio-visivo-2.easy-peasy.site`
- **Script di clonazione**: `/home/user/skills/didattica-app-classe/scripts/laboratorio-aumentato-3d-sorgente/clone_app.py`
- **Template config**: `/home/user/skills/didattica-app-classe/templates/laboratorio-aumentato-3d-sorgente/config_esempio.json`

> Se l'utente ha caricato l'app sorgente su GitHub, chiedigli l'URL del repository e usalo come `--source` (vedi sotto). Non serve che l'app sia presente in locale.

## Cos'è l'app (struttura FISSA, non cambia mai)

L'app NON è un quiz a risposte. È un **laboratorio di consegna elaborati a gruppi** con 6 passi per lo studente:

1. **PASSO 1** — scelta del gruppo (griglia di numeri cliccabili)
2. **PASSO 2** — componenti del gruppo (cognome + nome, fino a 3)
3. **PASSO 3** — elaborato visivo (upload foto/screenshot, max 3)
4. **PASSO 4** — spiegazione scritta (textarea)
5. **PASSO 5** — audio lettura (MP3)
6. **PASSO 6** — audio spiegazione (MP3)

Più la **dashboard docente** (crea/riapri/chiudi/elimina classe, rubrica di valutazione 1-4, report PDF stampabile, contatore lavori consegnati) e l'**embed iframe** con postMessage `labvisivo:height`.

Stack: Vite + React + TypeScript + Tailwind + tRPC + Drizzle + SQLite (scaffold `web-db-user`). Schema DB: `classes`, `submissions`, `evaluations` in `drizzle/schema.ts`.

## Cosa significa "set di domande" (contenuto VARIABILE)

Per questa app le "domande" sono il **contenuto dell'attività**: il tema trattato, i testi delle istruzioni dei 6 passi e i criteri della rubrica. Cambiare "solo il set di domande" = cambiare questi testi, lasciando intatta tutta la logica (flusso, DB, API, UI, colori, report).

## Procedura di clonazione (script — consigliata)

### 1. Prepara il config JSON (opzionale ma consigliato)

Usa `/home/user/skills/didattica-app-classe/templates/laboratorio-aumentato-3d-sorgente/config_esempio.json` come modello. Contiene:
- `theme_words` — parole-tema da sostituire globalmente (default: `"spagnolo" → "lingua straniera"`)
- `meta_description` — nuovo testo del `<meta name="description">`
- `steps` — i 10 testi delle istruzioni (step3_desc … step6_subtext)
- `rubric` — array di 5 criteri con `key`, `label`, `desc`

Le chiavi `key` della rubrica sono FISSE (legate alle colonne DB): `pertinenzaTema`, `originalita`, `qualitaTecnica`, `qualitaLettura`, `rispettoTempi`.

### 2. Esegui lo script

```bash
# Da cartella locale (default)
python3 /home/user/skills/didattica-app-classe/scripts/laboratorio-aumentato-3d-sorgente/clone_app.py \
  --dest /home/user/<nuova-app> \
  --title "NUOVO TITOLO" \
  --config config.json

# Da repository GitHub (l'utente l'ha caricata su GitHub)
python3 /home/user/skills/didattica-app-classe/scripts/laboratorio-aumentato-3d-sorgente/clone_app.py \
  --source https://github.com/USER/REPO.git \
  --dest /home/user/<nuova-app> \
  --title "NUOVO TITOLO" \
  --config config.json
```

Lo script esegue 5 passi:
1. **Clone** della sorgente (git clone per URL GitHub, copia `tar` per cartella locale, escludendo `node_modules`/`.git`/`dist`/`.vite`)
2. **Titolo** — sostituisce `LABORATORIO AUMENTATO 3D` e `Laboratorio Aumentato 3D` in `index.html`, `Home.tsx`, `StudentSubmit.tsx` (3×), `TeacherDashboard.tsx`
3. **Chiave localStorage** — `laboratorio_audiovisivo_classes` → `<slug>_classes` (slug derivato dal nome di `--dest`)
4. **Contenuto** (solo se `--config`) — istruzioni dei passi + rubrica (label mixed/uppercase + desc) + meta description. Eseguito PRIMA delle parole-tema: così la rubrica "…in spagnolo" viene sostituita dal config prima della conversione globale spagnolo→lingua straniera.
5. **Parole-tema** — sostituisce globalmente `spagnolo`→`lingua straniera` (e varianti di maiuscole) in `client/src` e `server`

### 3. Verifica

```bash
cd /home/user/<nuova-app>
pnpm install
pnpm check     # nessun errore TypeScript
pnpm build     # build produzione ok
# controlla che non restino stringhe del tema vecchio:
grep -rn "poesia\|spagnolo\|realtà aumentata\|Laboratorio Aumentato" client/src server/
```

## Procedura di clonazione (manuale — fallback)

Se lo script non è disponibile o serve un controllo fine, i punti da modificare sono:

| File | Cosa cambiare |
|------|---------------|
| `client/index.html` | `<title>` e `<meta name="description">` |
| `client/src/pages/Home.tsx` (~32) | `<h1>` |
| `client/src/pages/StudentSubmit.tsx` (~189, ~262) | `<h1>` (2×) + 4 blocchi istruzioni (PASSO 3-6) |
| `client/src/pages/TeacherDashboard.tsx` (~16-21, ~394-398, ~495-499) | rubrica in 3 punti (UI + 2 nel report PDF) + riga ~55 chiave localStorage + righe ~383 e ~951 "spagnolo" |
| `client/src/pages/TeacherClass.tsx` | file LEGACY non instradato (non usato) — contiene altri "spagnolo"; ignorabile |

Attenzione: i `key` della rubrica e le colonne dello schema (`coerenza`, `contributo`, `autonomia`, `riflessione`, ecc.) NON si rinominano.

## Cosa NON toccare (struttura FISSA)

- `drizzle/schema.ts` — tabelle `classes`, `submissions`, `evaluations` (NON rinominare le colonne dei criteri; il campo `is_active`/`isActive` di `classes` è parte della struttura fissa)
- `server/routers.ts` — endpoint tRPC e validatori (le chiavi dei criteri restano identiche; le procedure `close` e `reset` che gestiscono `isActive` sono parte della struttura fissa)
- Logica dashboard: crea/riapri/chiudi/elimina classe, `RIAPRI` mai disabilitato (validazione al click con toast), `ELIMINA CLASSE` con `confirm()`, `CHIUDI` (isActive=false) + `RIAVVIA CLASSE` (isActive=true)
- Schermata studente: `IL DOCENTE HA CHIUSO LA CLASSE` (quando isActive=false) e `CLASSE NON TROVATA` (quando eliminata) — fanno parte della struttura fissa
- Componenti UI shadcn (`Button`, `Input`), palette `--plum`/`--gold`/`--success`, font Cambria/Georgia con uppercase globale
- Input sidebar centrati (`!text-center`), data con overlay `gg/mm/aaaa` e icona calendario nascosta
- Embed iframe (`embed.html`) e postMessage `labvisivo:height` in `App.tsx`
- Il routing: `/` Home, `/studente/:classCode/:groupNumber`, `/docente` (NON aggiungere `TeacherClass.tsx`)

## Deploy, ZIP, embed

- **Preview**: `webdev_deploy project_dir="/home/user/<nuova-app>" mode="preview"`
- **Checkpoint** (obbligatorio prima di production): `webdev_save_checkpoint project_dir="/home/user/<nuova-app>" description="..."`
- **Production** (solo dopo conferma esplicita dell'utente): `webdev_deploy project_dir="/home/user/<nuova-app>" mode="production"`
- **ZIP**: `cd /home/user/<nuova-app> && zip -r /home/user/<nuova-app>.zip . -x "node_modules/*" ".git/*" "dist/*" ".vite/*" "*.log" ".env"` (includi `embed.html` se presente)
- **Embed**: il wrapper HTML (`embed.html`) usa `id="laboratorioAumentatoIframe"` e `src` della production della NUOVA app — aggiorna l'URL e l'ID prima di consegnarlo.

## Flusso GitHub

Quando l'utente dice di avere la sorgente su GitHub (o vuole caricarla), chiedigli l'URL del repository. Poi:
1. Usa `--source <url-github>` nello script (clona con `git clone --depth 1`).
2. Se il repo è privato, chiedi all'utente di renderlo accessibile o di passare le credenziali (non chiedere mai password in chat).
3. Dopo il clone, lo script rimuove la cartella `.git` per una copia pulita.

**Pacchetto ZIP / repo self-contained**: il pacchetto esportabile (ZIP) include l'app sorgente + la cartella `skills/` (questa skill con `clone_app.py` e il template config) + un README dettagliato. Quindi il repository GitHub creato dal pacchetto contiene già tutto il necessario: lo script è in `skills/laboratorio-aumentato-3d-sorgente/scripts/clone_app.py` e può essere eseguito direttamente dal repo (`python3 skills/laboratorio-aumentato-3d-sorgente/scripts/clone_app.py --source <url-github> …`). Se questa skill è disponibile in locale usa `/home/user/skills/didattica-app-classe/scripts/laboratorio-aumentato-3d-sorgente/clone_app.py`, altrimenti usa lo script incluso nel repo clonato.

## Attenzione

- Il tema dell'app sorgente è "poesia in realtà aumentata": quando l'utente fornisce il nuovo tema, deriva i testi dei 6 passi e i criteri della rubrica PRIMA di scrivere il config, per non lasciare residui del tema precedente.
- Dopo la clonazione controlla sempre con `grep` che non restino "poesia", "spagnolo" o "realtà aumentata".
- `TeacherClass.tsx` è un file legacy NON instradato (non appare nel routing); non è necessario aggiornarlo, ma se serve pulizia puoi ignorarlo.
