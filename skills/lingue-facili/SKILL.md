---
name: lingue-facili
description: "Manutenzione completa dell'app LINGUE FACILI (/home/user/lingue-facili, Vite+React+TS+Tailwind+tRPC+Drizzle, web-db-user; produzione https://lingue-facili.easy-peasy.site). App UNIFICATA multi-lingua (inglese, francese, spagnolo) con flusso SOLO-RIORDINO: incolla o fotografa l'esercizio → correzione automatica → esercizio di riordino delle parole (niente scelta tipologia né istruzioni manuali). Barra accessibilità a 5 moduli con ASCOLTO (TTS auto-lingua), drag-and-drop multi-rigo, PDF OpenDyslexic. Usare per: modificare UI/testi/colori/esercizi/PDF, cambiare i testi di una lingua (SOLO shared/languages.ts), gestire ASCOLTO o drag-and-drop, cornice Blogger (Codice 3), deploy preview/produzione. NON usare per: la vecchia Francese Facile (skill francese-facile, app superseded), il DOCX dei codici embed (skill codici-embed-cornici), altre app didattiche."
---

# LINGUE FACILI — manutenzione dell'app unificata

App in `/home/user/lingue-facili` (scaffold web-db-user). Produzione: **https://lingue-facili.easy-peasy.site**. Nasce dall'unificazione delle repo `andreakeating1982/INGLESE-FACILE` e `andreakeating1982/FRANCESE-FACILE` + Spagnolo nuovo. È un CLONE di Francese Facile con un layer multi-lingua sopra: quasi tutto il codice è quello di Francese Facile, la differenza sta in `shared/languages.ts` e nei punti elencati sotto.

## Principio architetturale

TUTTO ciò che dipende dalla lingua del CONTENUTO vive in **`shared/languages.ts`** (unica fonte di verità per client e server: `LANGS: Record<LangCode, LangConfig>` con `en`/`fr`/`es`). Per cambiare qualsiasi testo di una lingua (titolo, pulsanti, prompt AI, PDF, feedback) si edita SOLO quel file. La UI per l'insegnante resta in italiano.

La lingua viaggia: selettore WelcomePage → localStorage `lingue-facili-lang` → query string → **colonna `lang` della tabella `exercises`** (la riga DB è la fonte di verità per PDF e pagina finale; ExercisePage la ri-applica).

## Flusso SOLO-RIORDINO (novità architetturale)

L'insegnante incolla il testo o fotografa l'esercizio: l'app **corregge, completa e genera direttamente il riordino di parole**. NIENTE scelta tipologia, NIENTE istruzioni manuali di creazione. L'insegnante vede solo il testo corretto e le frasi complete generate, poi gioca.

- `client/src/pages/SetupPage.tsx`: fasi `idle → correcting → generating`, poi `doGenerate(finalText)` direttamente (niente selezione carta/tipologia).
- Il DB (schema `shared/exercise.ts`) conserva TUTTE le 5 `ExerciseType` (mc/tf/match/matchIt/reorder) e le relative view in `client/src/components/exercise/`: servono per gli **esercizi vecchi salvati**, che restano apribili e generano i loro PDF (con e senza risposte). NON cancellarle.
- La generazione di SOLO item `reorder` avviene in `server/exerciseGen.ts`: prompt AI + fallback deterministico senza AI (mappa di frasi complete → chip). Gli altri tipi non vengono più generati.

## Normalizzazione AI (server/exerciseGen.ts) — regole di prompt già calibrate, NON regredire

Ordine dei tentativi: prompt principale → salvataggi successivi a istruzioni minime. Regole chiave del prompt: COVERAGE (partire dalla PRIMA frase utile del testo), IGNORE THE INSTRUCTIONS (le istruzioni incollate con l'esercizio NON diventano mai item), SKIP numerazioni e titoli anche se terminano con punto, ogni frase CON GAP o DOMANDA diventa un item completato con la risposta corretta, le frasi GIÀ COMPLETE vengono conservate ESATTAMENTE (lo scompigliamento avviene nel gioco, non nella generazione), frasi con pochissime parole date vengono comunque completate, niente sotto-testo nei gap (`...............`).

## Drag-and-drop (ReorderView.tsx + usePointerDrop.ts) — regole non ovvie

- Input: mouse, penna, dito (pointer events, `touch-action: none` per bloccare lo scroll), tap, tastiera (Enter/Spazio). Multi-touch: un solo gesto attivo alla volta; gestione dei `pointercancel`.
- **Inserimento consapevole del RIGO**: con `flex-wrap` l'inserimento basato solo sulla coordinata x manda sempre all'inizio della PRIMA riga quando il dito è all'estrema sinistra di una riga successiva. Fix: prima si sceglie la RIGA più vicina al dito (y), poi si ordina SOLO dentro quella riga; oltre l'ultima tessera della riga = fine di QUESTA riga (non della frase). Testare sempre estremità sinistra/destra di OGNI riga su LIM/tablet.
- Bersagli di rilascio rigorosi: ogni mossa produce un inserimento valido; nessuna tessera può perdersi o duplicarsi.

## Schermata finale (ExercisePage.tsx) — stato DECISO con l'utente

- **5 stelline** proporzionali al punteggio: `Math.round((score/total) * 5)` (minimo 1), `size-9`, piene `fill-[#FFB300]`.
- Testo «Risposte giuste al primo colpo: X su Y» MANTENUTO. La scritta «Le risposte sono state salvate: le trovi nel PDF "con le mie risposte"» è stata ELIMINATA su richiesta (non reintrodurla).
- Pulsanti finali ESATTI: «SCARICA L'ESERCIZIO SENZA RISPOSTE» su `bg-[#B08050]` (marrone chiaro) e «SCARICA L'ESERCIZIO CON RISPOSTE» su `bg-[#5D4037]` (marrone scuro), testo bianco, `rounded-[14px]`.

## PDF (client/src/lib/exportWorkout.ts)

- **Riordino in disordine deterministico**: le tessere nel PDF NON vanno mai nell'ordine giusto. `hashStr` (FNV-1a) + `shuffleDeterministic` (Fisher-Yates con PRNG seedato dal contenuto dell'item: `item.answer` + testi chip) in `renderReorder`. Lo stesso seed genera lo STESSO disordine nel PDF «senza risposte» e in quello «con le risposte», così la scheda stampata si può correggere con la versione con soluzioni. Se il seme producesse per caso l'ordine giusto (con più di 1 chip), ruotare di una posizione.
- **Spaziatura risposte** (solo versione «con risposte»): la soluzione sta VICINO alla sua frase scomposta (`ctx.y -= 18` dopo i chip) e DISTANZIATA dalla risposta successiva (`ctx.y -= (lines.length-1)*19 + 26`). Non toccare il ramo «senza risposte».
- Titolo `L.appTitle` ("SPAGNOLO FACILE" ecc.), istruzioni per lingua (`pdfInstructions`), legenda colori dei ruoli grammaticali (subject/verb/adverb/other).
- Debug del PDF generato: con pdftotext o decomprimendo gli stream; nota che DecompressionStream('deflate') nel browser cloud ha dato errori ("Failed to fetch") — verificare in sandbox con Python zlib o replicare la logica pura in node.

## ASCOLTO (TTS multilingua) — regole non ovvie

- `useReadAloud(prefer?)` divide la pagina in frasi e per OGNI frase chiama `detectLanguage(chunk, prefer)`: accenti forti (ñ¿¡ → es, çàùèê → fr) e parole caratteristiche; i pareggi vanno a `prefer`. `UTTER_LANG` mappa it/en/fr/es → BCP-47; voce migliore per lingua in cache `voicesByLang`.
- La pagina viene letta TUTTA (body); skip di `role="toolbar"`, `aria-hidden="true"`, `.sr-only`, BUTTON/INPUT/SELECT, KaTeX parlato, MAIUSCOLE → minuscolo (`toNaturalCase`).
- **Bug noto (già corretto, non regredire):** in browser headless/alcuni engine `onstart` NON scatta → `setSpeaking(true)` OTTIMISTICO + sonda periodica 500ms su `speechSynthesis.speaking/pending`.

## Cornice Blogger

- File: `cornice-dinamica/embed-lingue-facili-dedicata.html` (+ `-lite`). È il **Codice 3** del DOCX CODICI-EMBED-CORNICI. Le cornici già incollate nei post si aggiornano da sole al republish. Workflow DOCX: skill **codici-embed-cornici**.

## Deploy

`pnpm check` → commit → `webdev_save_checkpoint` → preview → confirm utente → produzione (verificare curl 200 + `<title>Lingue Facili</title>`). DB Neon: usare `drizzle-kit push` diretto (le vecchie migrazioni ereditate da Francese Facile non sono riapplicabili). Il log "[Auth] Authentication failed: 403" è rumore benigno. ATTENZIONE: `REBUILD.md` e `ADATTARE.md` (pacchetto ZIP esportabile) descrivono ancora l'architettura a 5 tipologie e la cornice di Francese Facile: da riallineare prima di riesportare lo ZIP.

## Aggiungere una quarta lingua

1. `shared/languages.ts`: aggiungere a `LangCode`, `LANG_CODES`, `LANG_LABELS`, `LANG_ACCENT` e una `LangConfig` completa (~200 righe: copiare EN come base).
2. OCR: modello da tessdata_fast in `client/public/tessdata/` e mappa in `client/src/lib/ocr.ts`.
3. Fallback server: frasi complete → chip in `server/exerciseGen.ts`.
4. Ascolto: `UTTER_LANG`, `STRONG_MARKS`/`HINT_WORDS`, `primary` in `scoreVoice`.
5. La cornice del Codice 3 serve l'app intera: nessuna cornice nuova per lingua.
