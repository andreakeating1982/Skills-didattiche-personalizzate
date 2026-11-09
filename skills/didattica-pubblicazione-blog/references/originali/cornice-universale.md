# Archivio di dettaglio — cornice-universale

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/cornice-universale.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Overview
- File Critici
- Password (⚠️ IN DUE FILE)
- Meccanismo di Sincronizzazione Cross-Device
- ⚠️ IMPORTANTE per il deploy
- Comportamenti Attuali (2026-08-21)
- Layout Barra Controlli
- Messaggio Documento Nascosto
- Iframe Documento
- Toast (sonner)
- Palette Colori
- Font
- Personalizzazioni Frequenti
- Cambiare password
- Cambiare intervallo sync
- Cambiare documento
- Cambiare altezza iframe
- Deploy
- Esportare ZIP per GitHub/Render
- Regole d'Oro

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Cornice Universale — Skill di Manutenzione

## Overview

App in `/home/user/cornice-universale`. Scaffold `web-static` + server Express aggiunto per la sincronizzazione. Stack: Vite + React + TypeScript + TailwindCSS + shadcn/ui + Express.

Scopo: cornice interattiva con protezione password che embedda un PDF Google Drive. Lo stato "nascosto/visibile" è **condiviso su tutti i dispositivi** tramite API server (`/api/state`), NON solo in localStorage.

**URL produzione**: `https://cornice-universale.easy-peasy.site`

**URL embed su Blogger**:
```html
<iframe src="https://cornice-universale.easy-peasy.site/?doc=1pASV4GUKQqKD_cZtNv7SfiRJg0WsDWUi" width="100%" height="560" style="border:none;max-width:900px;"></iframe>
```

## File Critici

| File | Ruolo |
|------|-------|
| `client/src/pages/Home.tsx` | ⭐ Componente principale (cornice, controlli, polling, invio stato) |
| `server/index.ts` | 🔧 Server Express — API `GET/POST /api/state` + serve i file statici |
| `render.yaml` | 🔧 Render Blueprint (Web Service Node.js, NON static) |
| `vite.config.ts` | Config Vite (root `client/`, outDir `dist/public`) |
| `package.json` | Script: `dev`, `build`, `start` |

## Password (⚠️ IN DUE FILE)

La password `[PASSWORD_RIMOSSA]` è definita **in entrambi** i file — cambiarne uno solo rompe la sincronizzazione:

1. `client/src/pages/Home.tsx` → `const PASSWORD = "[PASSWORD_RIMOSSA]";`
2. `server/index.ts` → `const PASSWORD = "[PASSWORD_RIMOSSA]";`

Quando si cambia password, modificare SEMPRE entrambi i file.

## Meccanismo di Sincronizzazione Cross-Device

- Il server mantiene `hiddenState` (boolean) **in memoria** (variabile a livello di modulo in `server/index.ts`).
- `GET /api/state` → `{ hidden: boolean }` — lettura stato.
- `POST /api/state` → body `{ password, hidden }` — verifica password, aggiorna stato. Risponde `401` se password errata.
- Il client:
  - Al mount: legge localStorage (`cd_hidden`) per render immediato, poi fetch `GET /api/state` per lo stato reale.
  - **Polling ogni 2500 ms** (`const POLL_INTERVAL = 2500`) su `GET /api/state`.
  - Su hide/show: aggiorna subito locale, poi `POST /api/state`; se fallisce → rollback locale + toast errore.
- **NOTA**: lo stato in-memory si resetta al riavvio del server (istanza Cloud Run/Render riavviata). Non è persistente su disco. Per un uso classe è accettabile.

### ⚠️ IMPORTANTE per il deploy

Questa app **NON è più un sito statico**: ha bisogno del server Express per `/api/state`. Su Render usare `runtime: node` (Web Service), MAI `runtime: static`.

`render.yaml` corretto:
```yaml
services:
  - type: web
    name: cornice-universale
    runtime: node
    plan: free
    buildCommand: pnpm install && pnpm build
    startCommand: pnpm start
    envVars:
      - key: NODE_VERSION
        value: "22"
    healthCheckPath: /api/state
```

Build: `vite build && esbuild server/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist`
Start: `NODE_ENV=production node dist/index.js`

## Comportamenti Attuali (2026-08-21)

### Layout Barra Controlli

Barra centrata (header) con questi elementi, **nessuna emoji**:

```
[ input password ]  [ Nascondi ]  [ Mostra ]  [ Visibile/Nascosto ]
```

- Input password: `type="password"`, larghezza `w-[140px] sm:w-[170px]`, bordo `#d9cec3`, focus ring `#9b7b62/15`.
- **Nessun pulsante toggle Mostra/Nascondi password** (rimosso). Serve SOLO l'input password.
- Pulsante **Nascondi**: rosso `#c0392b`, hover `#a93226`, uppercase, tracking-wide.
- Pulsante **Mostra**: verde `#27ae60`, hover `#219a52`, uppercase, tracking-wide.
- Badge stato (span): mostra "Nascosto" (sfondo `bg-red-100/70`, testo `#c0392b`) oppure "Visibile" (sfondo `bg-[#9b7b62]/10`, testo `#8b7355`). Maiuscolo, `text-[11px]`.
- Tutto dentro `div` con `bg-[#faf7f3]`, bordo inferiore `#d9cec3`.

### Messaggio Documento Nascosto

Quando `hidden === true`, al posto dell'iframe compare:

- Solo il titolo: **`DOCUMENTO MOMENTANEAMENTE NON DISPONIBILE`** — tutto MAIUSCOLO, `text-xl font-bold text-[#5c4332]`.
- **NESSUN sottotesto** (rimosso "Il docente ha temporaneamente nascosto...").
- **NESSUN emoji** (rimosso il placeholder 📄/🔒 — usato `&nbsp;`).
- Centrato verticalmente e orizzontalmente dentro il container (`minHeight: 480px`).

### Iframe Documento

- URL: `https://drive.google.com/file/d/${docId}/preview` dove `docId` arriva da `?doc=` nei query params.
- Se `docId` manca → schermata "Nessun documento specificato" con hint `?doc=ID_FILE`.
- Altezza iframe: `480px`, dentro container `minHeight: 480px`.
- Transizione `opacity` + `invisible` + `pointer-events-none` quando nascosto.

### Toast (sonner)

- Password errata: `toast.error("Password errata. Riprova.")`
- Già nascosto: `toast.info("Già nascosto.")`
- Nascosto OK: `toast.success("Documento nascosto a tutti!")`
- Già visibile: `toast.info("Già visibile.")`
- Visibile OK: `toast.success("Documento visibile a tutti!")`
- Errore sync: `toast.error("Errore di sincronizzazione. Riprova.")`
- **TUTTI i toast sono senza emoji.**

## Palette Colori

| Ruolo | Colore |
|---|---|
| Sfondo pagina | `#f5f0eb` |
| Card cornice | `#ffffff` |
| Bordo cornice | `#d9cec3` |
| Header controlli | `#faf7f3` |
| Testo scuro | `#5c4332` |
| Testo chiaro | `#8b7355` |
| Accent focus | `#9b7b62` |
| Pulsante Nascondi | `#c0392b` (hover `#a93226`) |
| Pulsante Mostra | `#27ae60` (hover `#219a52`) |

## Font

Font famiglia su tutti gli elementi: `Cambria, Georgia, 'Times New Roman', serif`.

Applicato via `style={{ fontFamily: "Cambria, Georgia, 'Times New Roman', serif" }}` sul container principale e `style={{ fontFamily: "inherit" }}` su input/button.

## Personalizzazioni Frequenti

### Cambiare password
Modificare `const PASSWORD` in **entrambi** `client/src/pages/Home.tsx` e `server/index.ts`.

### Cambiare intervallo sync
`client/src/pages/Home.tsx` → `const POLL_INTERVAL = 2500;` (millisecondi).

### Cambiare documento
NON nel codice: il documento arriva dal parametro `?doc=ID_FILE` nell'URL embed. Cambiare l'iframe su Blogger.

### Cambiare altezza iframe
`Home.tsx`: l'iframe ha `height: "480px"` (2 occorrenze: container iframe e placeholder). Cambiarle entrambe.

## Deploy

```bash
cd /home/user/cornice-universale
pnpm check    # verifica TypeScript
pnpm build    # build frontend + bundle server
```

Poi:
- `webdev_deploy` mode=`preview` per test.
- `webdev_deploy` mode=`production` per produzione.
- **Prima del deploy produzione**: sempre `webdev_save_checkpoint`.

## Esportare ZIP per GitHub/Render

```bash
cd /home/user && rm -rf cornice-package && mkdir -p cornice-package/cornice-universale
cp -r cornice-universale/* cornice-package/cornice-universale/
cp cornice-universale/.gitignore cornice-package/cornice-universale/ 2>/dev/null
cp cornice-universale/.prettierrc cornice-package/cornice-universale/ 2>/dev/null
cp cornice-universale/.prettierignore cornice-package/cornice-universale/ 2>/dev/null
rm -rf cornice-package/cornice-universale/node_modules cornice-package/cornice-universale/dist cornice-package/cornice-universale/.git cornice-package/cornice-universale/pnpm-lock.yaml
cd cornice-package && zip -r /home/user/cornice-universale.zip cornice-universale/
```

Consegnare lo ZIP con `send_attachment` (file_path `/home/user/cornice-universale.zip`).

## Regole d'Oro

1. **Password in DUE file** — `Home.tsx` e `server/index.ts` vanno sempre aggiornati insieme.
2. **Mai emoji** nell'app — nessuna icona in toast, badge, placeholder, pulsanti.
3. **Messaggio nascosto sempre MAIUSCOLO** — "DOCUMENTO MOMENTANEAMENTE NON DISPONIBILE", senza sottotesto.
4. **Mai toggle password** — solo input password + pulsanti Nascondi/Mostra.
5. **Controlli centrati** — l'header usa `flex items-center justify-center`.
6. **render.yaml = `runtime: node`** — MAI `runtime: static` (servono le API `/api/state`).
7. **Polling 2500 ms** — non rimuovere: è ciò che sincronizza i dispositivi.
8. **Font Cambria** con fallback `Georgia, 'Times New Roman', serif`.
9. **`style` in React è oggetto**, non stringa.
10. **Documento via `?doc=ID`**, mai hardcoded.
