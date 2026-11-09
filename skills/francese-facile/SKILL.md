---
name: francese-facile
description: "Manutenzione completa dell'app FRANCESE FACILE (/home/user/francese-facile, Vite+React+TS+Tailwind+tRPC+Drizzle, web-db-user; produzione https://francese-facile.easy-peasy.site). Variante francese di «Inglese Facile», clonata dalla repo GitHub andreakeating1982/INGLESE-FACILE: trasforma testi francesi (incollati o da foto OCR) in 5 esercizi interattivi (scelta multipla, VRAI/FAUX, riordino, abbinamento parola/immagine, abbinamento francese-italiano) con copia verbatim, PDF e OpenDyslexic. Usare per: modificare UI/testi/colori/esercizi/PDF; gestire il TITOLO (FRANCESE FACILE, spelling italiano — decisione fissa, MAI «FRANÇAIS FACILE»; colonne esercizio FRANÇAIS/ITALIANO restano in francese); cornice dinamica Blogger e Codice 14 del DOCX CODICI-EMBED-CORNICI; immagine diorama con controllo ortografico; deploy; varianti in altre lingue (ADATTARE.md). NON per: presentazione blog (presentazione-app-docx), codici embed DOCX generici (codici-embed-cornici), altre app didattiche."
---

# FRANCESE FACILE — guida di manutenzione

App web didattica inclusiva di francese per la scuola secondaria, appartenente alla famiglia di app dell'utente (docente italiano, blog didattico). Regole, mappa del codice e workflow testati.

## 1. Identità e regole fisse

- Percorso progetto: `/home/user/francese-facile` (package npm `francais-facile`, scaffold web-db-user)
- Produzione: `https://francese-facile.easy-peasy.site`
- **TITOLO DELL'APP: «FRANCESE FACILE»** — spelling ITALIANO, decisione esplicita dell'utente (17/09/2026): MAI «FRANÇAIS FACILE». Dove appare:
  - `client/src/pages/WelcomePage.tsx`: H1 «FRANCESE FACILE»; sottotitolo «ESERCIZI STRUTTURATI **DI FRANCESE**» (span colore #8B3A1A — specchio italiano di «D'INGLESE» dell'app inglese, NON «DE FRANÇAIS»)
  - `client/src/lib/exportWorkout.ts`: titolo del PDF «FRANCESE FACILE»
  - `cornice-dinamica/embed-francese-facile-dedicata.html` + lite: commento di intestazione e `<p class="lf-titolo">` «FRANCESE FACILE»
  - `index.html`: `<title>Francese Facile</title>`
  - **ECCEZIONE VOLUTA**: le colonne dell'esercizio di abbinamento restano «FRANÇAIS / ITALIANO» (in francese: etichetta della lingua dei contenuti, NON il nome dell'app) → `MatchItView.tsx` e `exportWorkout.ts` (drawText della tabella match PDF)
- Palette: crema `#f8f1e4` (stessa di «Latino Facile»), inchiostro `#2E2018`, accenti caldi
- Font OpenDyslexic auto-ospitato in `client/public/fonts` (servito a `/fonts/OpenDyslexic-Regular-v2.woff2` e `-Bold-v2.woff2` — usati anche dalla cornice)

## 2. Mappa del progetto

- `client/src/pages/`: `WelcomePage.tsx` (prima pagina: H1, sottotitolo, form studente), `ExercisePage.tsx`, `Home.tsx`, `SetupPage.tsx`, `Login.tsx`
- `client/src/components/exercise/`: `McView`, `TfView`, `MatchView`, `MatchItView`, `ReorderView` + `common.tsx`, `usePointerDrop.ts`
- `client/src/lib/`: `exportWorkout.ts` (PDF con pdf-lib), `heightSync.ts` (protocollo altezza), `ocr.ts`, `ocrClean.ts`, `cropBox.ts`, `imagePrep.ts`, `upload.ts`, `trpc.ts`, `auth-client.ts`
- `client/src/components/`: `AccessibilityToolbar.tsx` (barra accessibilità), `CropDialog.tsx`
- `server/`: `exerciseGen.ts` (generazione AI degli esercizi), `routers.ts`, `db.ts`, `storage.ts`
- `shared/`: `exercise.ts` (schemi Zod dei 5 tipi), `types.ts`, `const.ts`
- `cornice-dinamica/`: embed per Blogger + test + README
- `scripts/`: vedi §6 e §8
- Guide repo: `AGENTS.md`, `ADATTARE.md`, `REBUILD.md`, `RENDER.md`, `ACCESSIBILITA.md`, `README.md`

## 3. Le 5 tipologie di esercizio e il PDF

Tipi in `shared/exercise.ts`: `mc` (scelta multipla), `tf` (vero/falso — VRAI/FAUX), `match` (abbinamento francese-italiano), `matchIt` (abbinamento parola/immagine emoji), `reorder` (riordino delle parole).

Il testo dell'alunno è copiato VERBATIM dal sorgente (incollato o OCR da foto): verificare con `node scripts/verify-verbatim.mjs <id-esercizio>`. PDF scaricabile con o senza risposte (`exportWorkout.ts`, titolo FRANCESE FACILE).

## 4. Accessibilità

Barra accessibilità + TTS + alto contrasto + righello di lettura + OpenDyslexic. Dettagli in `ACCESSIBILITA.md` (repo). Protocollo altezza per l'embed: `client/src/lib/heightSync.ts` — l'app invia `{ type: "labvisivo:height", height }` e risponde ai ping `{ type: "labvisivo:ping", cornice: token }`.

## 5. Cornice dinamica per Blogger

`cornice-dinamica/embed-francese-facile-dedicata.html` — versione DEDICATA v4: impermeabile (scoping via `document.currentScript`, id rinominati con token univoco, filtro `e.source`), anti-loop (niente transizioni CSS sull'altezza, debounce 200 ms, clamp 100–15000 px, conferma salti >2×, congelamento), anti-tremolio (silenzio 300 ms post-applicazione, ping ogni 3 s), pulsanti Schermo intero ⟶/Ricarica sulla stessa riga del titolo, spinner, stato online/errore con Riprova, APP_URL fisso `https://francese-facile.easy-peasy.site/`. Versione ridotta: `embed-francese-facile-lite.html`. Test locali: `test-dedicata.html`, `test-impermeabile.html`. Guida: `cornice-dinamica/README.md`.

## 6. DOCX «CODICI-EMBED-CORNICI-v4» — Codice 14

- File utente: `/home/user/CODICI-EMBED-CORNICI-v4-aggiornato.docx`. Il Codice 14 contiene la cornice dedicata di FRANCESE FACILE: titolo blocco «Codice 14 — FRANCESE FACILE», riga indice «FRANCESE — Francese Facile → Codice 14», cella 499 paragrafi, 0 residui «FRANÇAIS».
- Aggiornare il blocco: `python3 scripts/assert_codice14.py` (estrae la cornice, applica trasformazioni, verifica con assert → `/tmp/codice14-francese.html`) poi, dalla skill codici-embed-cornici: `sostituisci_codice.py --src /home/user/CODICI-EMBED-CORNICI-v4-aggiornato.docx --out <stesso file> --codice 14 --html /tmp/codice14-francese.html --titolo "Codice 14 — FRANCESE FACILE" --indice "FRANCESE — Francese Facile"`
- Verifica post-sostituzione con python-docx: T14 = 499 paragrafi, 0 «FRANÇAIS» nel blocco, altre 13 tabelle intatte, titolo e indice corretti
- Storico: `scripts/inserisci_codice14.py` (creazione blocco), `scripts/dump_docx.py` (ispezione)

## 7. Deploy

- Verifiche pre-deploy: `pnpm check && pnpm build`
- Preview: `webdev_deploy` mode="preview" (auto-checkpoint)
- Produzione: SEMPRE `webdev_save_checkpoint` descrittivo PRIMA, poi preview, poi conferma esplicita dell'utente in un messaggio nuovo, solo allora `webdev_deploy` mode="production". Checklist cross-app: skill `deploy-app-produzione`
- Post-deploy produzione: `curl` del bundle JS servito cercando «FRANCESE FACILE» (zero «FRANÇAIS FACILE») + apertura nel browser

## 8. Database

Scaffold web-db-user (Drizzle + postgres, `.env` → `DATABASE_URL`). `scripts/fix-db.mjs`: ripristina da zero (drop tabelle scaffold + registro migrazioni, poi `pnpm db:push` riapplica le 3 migrazioni della repo). Query dirette con `webdev_execute_sql`.

## 9. Nuove lingue e guide della repo

Per varianti (ESPAÑOL FÁCIL, DEUTSCH LEICHT…) leggere `ADATTARE.md` (tabella file→valori) e `references/workflows.md` §C. Regola nome: l'utente usa lo spelling ITALIANO per il nome dell'app → «SPAGNOLO FACILE», «TEDESCO FACILE», ecc.

## 10. Immagine diorama e presentazione

- Diorama 16:9 del libro con «FRANCESE / FACILE»: `/home/user/francese-facile-diorama.png`. Rigenerazione con controllo ortografico: `references/workflows.md` §B (l'AI ha sbagliato «FRANSESE» alla prima prova: verificare SEMPRE lettera per lettera)
- Presentazione per il blog: skill `presentazione-app-docx` (versione breve ≤15 righe, hyperlink `{LINK}`). Testo già adattato: esempi «avoir/être» e «passé composé», «abbinamento francese-italiano»

→ Per il cambio titolo completo, la gestione immagini con testo e la clonazione per nuove lingue: `references/workflows.md`
