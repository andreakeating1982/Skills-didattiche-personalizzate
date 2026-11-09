# Archivio di dettaglio — widget-matematico-sorgente

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/equazioni.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Quando usare questa skill
- App sorgente
- Filosofia (BES)
- Workflow di clonazione con grado diverso
- Sorgente: cartella locale O repository GitHub
- Disequazioni
- Regole d'oro

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Widget Matematico Sorgente — Skill di clonazione

## Quando usare questa skill

Usare quando l'utente chiede una **nuova app identica alla sorgente** ma con:
- un **grado diverso** dell'equazione (es. "fammi la stessa app ma di secondo/sesto grado"),
- oppure una versione per le **disequazioni** (stessa filosofia, con studio del segno).

**NON** usare per modificare, correggere o mantenere l'app sorgente: per quello usare la
skill `equazioni-biquadratiche` (manutenzione). Questa skill **clona** e **adatta**.

## App sorgente

- Percorso: `/home/user/equazioni-biquadratiche`
- Scaffold: `web-static` (Vite + React 18 + TypeScript + TailwindCSS 4 + shadcn/ui + KaTeX). Nessun backend, nessun database.
- URL produzione sorgente: `https://equazioni-biquadratiche.easy-peasy.site`
- Input: **canvas di scrittura a mano** (ONNX/ink-on) → lo studente scrive l'equazione e i risultati.
- Output: passi guidati + box "RICOPIA SUL QUADERNO" + PDF scaricabile.

L'app guida lo studente nella risoluzione di una **trinomia** della forma

```
a · x^(2k) + b · x^k + c = 0
```

con sostituzione **`t = x^k`**, che riduce tutto a una quadratica `a·t² + b·t + c = 0`.
Il **grado** in `x` è `2k`. Il sorgente attuale è **k = 2 → grado 4** (biquadratica).

## Filosofia (BES)

Obiettivo trasversale: **accompagnare passo-passo** lo studente, mostrando ogni passaggio
e facendogli eseguire **solo i conti finali più semplici** (delta, radici t, radici x).
Tutto è pensato per studenti con BES/DSA: pochi passi chiari, colori, box "RICOPIA SUL
QUADERNO" da copiare, feedback immediato CORRETTO/SBAGLIATO, PDF finale.

## Workflow di clonazione con grado diverso

### Sorgente: cartella locale O repository GitHub

La sorgente può essere la cartella locale `/home/user/equazioni-biquadratiche` oppure un
**repository GitHub** fornito dall'utente. Il flag `--source` accetta entrambi:

```bash
# da cartella locale (default)
python3 .../clone_app.py --name "equazioni-sesto-grado" --degree 6

# da repository GitHub (l'app deve essere alla root del repo o in una subfolder)
python3 .../clone_app.py --source https://github.com/utente/widget-matematico.git \
    --name "equazioni-sesto-grado" --degree 6
```

Se l'utente dice di avere il sorgente "su GitHub", usare **sempre** `--source <URL del
repo>`. Lo script esegue `git clone` e rileva automaticamente se l'app è alla root o in
una subfolder (cerca `package.json`).

1. **Clonare** con lo script (copia la cartella + sostituzioni meccaniche su potenze,
   titoli, placeholder, testo della sostituzione):
   ```bash
   python3 /home/user/skills/didattica-app-matematica/scripts/widget-matematico-sorgente/clone_app.py \
       --name "equazioni-sesto-grado" --degree 6
   ```
   - `--source` per cartella locale o URL git (default: `/home/user/equazioni-biquadratiche`).
   - `--degree` pari ≥ 2: 2 (quadratica), 4 (biquadratica), 6 (bicubica), 8, ...
   - Lo script stampa una **checklist dei passi manuali**: leggerla e completarla.

2. **Completare la logica del passo 6** (estrazione x da t) — lo script NON la tocca:
   - k pari: `x = ±(t)^(1/k)` → `\pm\sqrt[k]{t}` e `Math.pow(t, 1/k)`.
   - k dispari: `x = (t)^(1/k)` (senza `±`).
   - k=1: nessuna estrazione (x = t), rimuovere il passo di sostituzione e quello di estrazione.

3. **Verificare** (MAI saltare):
   ```bash
   cd /home/user/<name> && pnpm install && pnpm check && pnpm dev
   grep -rn "x^{4}\|x^{2}\|x⁴\|x²" client/src   # residui da sistemare
   ```

4. **Deploy**:
   ```bash
   webdev_deploy mode="preview" project_dir="/home/user/<name>"
   # dopo conferma esplicita dell'utente:
   webdev_save_checkpoint description="..." project_dir="/home/user/<name>"
   webdev_deploy mode="production" project_dir="/home/user/<name>"
   ```

5. **Consegnare**: export ZIP della nuova cartella (escludendo `node_modules`, `dist`, `.git`).

Per la mappa esatta di dove è codificato il grado, le tabelle radici per k pari/dispari,
i casi speciali e la rinominazione dei simboli interni, leggere **`/home/user/skills/didattica-app-matematica/references/widget-matematico-sorgente/grado.md`**.

## Disequazioni

Per adattare l'app alle disequazioni (`a·x^(2k) + b·x^k + c ≷ 0`): mantenere input,
sostituzione, delta e radici t; aggiungere il **riconoscimento del verso** nel parser,
un passo di **studio del segno** (parabola/tabella), la **traduzione in intervalli** e la
verifica dell'intervallo finale. Dettagli su struttura passi, tabella dei segni e linee
guida BES in **`/home/user/skills/didattica-app-matematica/references/widget-matematico-sorgente/disequazioni.md`**.

## Regole d'oro

1. **Non** fare replace globale di cifre `4`/`2`: romperebbe `4ac`, `2a`, ecc. Sostituire
   solo i **token di grado** (vedi `/home/user/skills/didattica-app-matematica/scripts/widget-matematico-sorgente/clone_app.py` e `/home/user/skills/didattica-app-matematica/references/widget-matematico-sorgente/grado.md`).
2. `buildTEquationLatex` (equazione in `t`) **non cambia** con k: produce sempre `at² + bt + c = 0`.
3. Il calcolo di `delta`, `t₁`, `t₂` è **identico** per ogni k: la differenza è solo nel passo di estrazione x.
4. Il canale postMessage `'labvisivo:height'` è condiviso: **non** cambiarlo nell'embed.
5. `pnpm check` prima di ogni deploy.
6. Per il mantenimento dell'app sorgente (non clonazione) usare la skill `equazioni-biquadratiche`.
