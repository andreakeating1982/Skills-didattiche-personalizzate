---
name: espana-xix-match
description: "Manutenzione completa e personalizzazione dell'app «Marco histórico del Romanticismo en España» (espana-xix-match, Vite + React + TS + Tailwind, web-static): ascolto-abbinamento audio → puntino sulla linea del tempo. Usare per: generare una NUOVA app simile (linea del tempo o audio-mappa); modificare eventi/anni/audio/posizioni puntini, titolo, testi, colori, font, immagine; gestire l'accessibilità (barra italiana, OpenDyslexic UI/immagine/PDF, TTS auto-lingua per elementi con pause e ordinali spagnoli, contrasto, righello, maiuscole via CSS); modificare il PDF (icone sopra l'asse, margini ~3 cm, senza istruzioni); modificare la schermata finale «Actividad completada» (overlay sopra la barra, senza pulsante PDF, titolo responsive); embed Blogger (cornice v3 in cornice-dinamica/, token + ping, WOFF2 -v2, CORS /fonts); deploy preview/produzione. NON usare per app schema/quiz con dashboard docente (schema-quiz-builder) né per la Mappa Concettuale Interattiva (romanticismo-interattivo)."
---

# Espana XIX Match — App di ascolto-abbinamento sulla linea del tempo

Workflow per mantenere e, soprattutto, **generare nuove app identiche** a
«Marco histórico del Romanticismo en España»: un'attività in cui l'alunno
ascolta l'audio di un avvenimento e tocca il puntino giusto su una linea del
tempo. Progetto reale: `/home/user/espana-xix-match` (scaffold web-static,
nessun database, nessuna dashboard docente).

## Cosa fa l'app (in breve)

1. Schermata iniziale: «Pulsa en cualquier parte para empezar.» → intro parlata.
2. Gli eventi vengono **mescolati** (`shuffleIds`) per ogni alunno.
3. A ogni turno il pulsante «Escuchar el audio» fa partire la narrazione
   dell'evento corrente (un solo canale audio: niente sovrapposizioni).
4. L'alunno tocca il puntino corrispondente: corretto → suono ok + ✓ e passo
   successivo; sbagliato → suono ko + flash rosso (nessuna penalità).
5. Tutti e 7 azzeccati → fin.mp3 → overlay «Actividad completada» (senza
   pulsante PDF: il PDF si scarica solo dal modulo della barra; overlay
   scroll-safe con z-index 120 sopra la barra, titolo responsive).
6. In iframe (Blogger) invia `{type:"labvisivo:height"}` e
   `{type:"romanticismo:height"}` (legacy) per il resize automatico,
   rispecchiando il token `cornice` se presente, e risponde al ping
   `labvisivo:ping` della cornice (Home.tsx + lib/corniceToken.ts).

## Lavoro consolidato nella chat del 9/9/2026 (stato attuale verificato)

Tutto ciò che è stato fatto e VERIFICATO in questa sessione è già riflesso
nel codice e nei punti sopra; in sintesi i deliverable:

- **Accessibilità completa** sul modello PAROLE-CHIAVE-INTERATTIVE: barra
  italiana 5+1 moduli (Font A−/A+, Interlinea, Righello, Modalità, Ascolto,
  PDF), OpenDyslexic in UI + immagine timeline v13 + PDF, alto contrasto,
  TTS auto-lingua per elementi con pause, stato persistente (`exm_access`).
- **PDF**: 7 icone ritagliate dinamicamente sopra l'asse, anni/titoli sotto,
  OpenDyslexic, istruzioni di gioco RIMOSSE, margini ~3 cm sui 4 lati;
  download solo dal modulo PDF della barra (etichetta «LINEA DEL TEMPO IN
  PDF» a riga singola); verificato con script QA dedicato.
- **Cornice dinamica v3 impermeabile** (`cornice-dinamica/`): dedicata +
  universale + test anti-furto + README; token `cornice` rispecchiato,
  ping `labvisivo:ping`, WOFF2 -v2 e CORS /fonts; embed Blogger aggiornato.
- **TTS**: pause minime tra elementi (350 ms) e tra frasi (90 ms), lettura
  per elementi (titolo, «Audio N de 7», pin, dock), ordinali spagnoli
  («Primera Guerra Carlista»), numeri/romani espansi, MAIUSCOLO → minuscole.
- **Schermata finale**: nessun pulsante PDF, titolo mai tagliato su
  cellulare (overlay z-index 120 + scroll-safe + font fluido).
- **Deploy**: preview e produzione Cloud Run aggiornate
  (https://espana-xix-match.easy-peasy.site).

## Workflow A — Generare una NUOVA app simile (8 passi)

1. **Base**: copiare `/home/user/espana-xix-match` (o inizializzare lo stesso
   scaffold web-static) e mantenere TUTTA la logica di Home.tsx invariata:
   si cambiano solo dati e risorse.
2. **Immagine**: creare la nuova `timeline.png` (stesso aspect ratio di
   `MAP_W:MAP_H` = 1376:821 dichiarato in Home.tsx) e annotare la posizione %
   (x, y) di ogni punto sulla nuova immagine. I testi dell'immagine (frase di
   istruzioni in alto, anni e titoli in basso) devono usare OpenDyslexic come
   il resto dell'app: dopo aver creato la grafica eseguire
   `scripts/riscrivi_testi_immagine_opendyslexic.py [root] [output]` dopo
   aver adattato CX/YEARS/TITLES/INSTR nel file.
3. **Audio**: generare con TTS/registrazione la narrazione di ogni evento +
   intro/ok/ko/fin in `client/public/audio/` (nomi come `e1808.mp3`).
4. **Dati**: compilare `templates/app-config.json` (titolo, theme-color,
   eventi con id/anno/titolo/audio/x/y, sfx, dimensioni) ed eseguire:

```bash
python3 /home/user/skills/espana-xix-match/scripts/adatta_app.py \
    --config nuovo-argomento.json --root /home/user/espana-xix-match
# prima prova: aggiungere --dry-run per vedere cosa verrebbe scritto
```

   Lo script riscrive SOLO: `client/src/data/events.ts` (EVENTS + SFX +
   shuffleIds), l'`<h1>`/`alt` di Home.tsx, `MAP_W`/`MAP_H`, e il
   `<title>`/`theme-color` di index.html. Non tocca logica né stili.
5. **Verifica**: `pnpm check` senza errori TS; provare in locale il flusso
   completo (intro → ascolto → corretto/sbagliato → fine).
6. **Cache busting**: incrementare i `?v=N` su immagine e audio appena
   sostituiti (es. `?v=12` → `?v=13`), altrimenti browser/Cloud Run servono i
   file vecchi.
7. **Deploy**: `webdev_deploy` mode="preview" → verifica → checkpoint →
   mode="production" (sempre con conferma esplicita dell'utente).
8. **Embed (cornice dinamica v3)**: incollare
   `cornice-dinamica/embed-espana-xix-dedicata.html` nel post Blogger (⭐;
   copia pronta in `/home/user/embed-blogger-romanticismo.html`). Per una
   NUOVA app completare la checklist embed qui sotto: mai usare cornici v1 a
   id fissi (non impermeabili).

   **Checklist embed per una nuova app** (replicata da
   PAROLE-CHIAVE-INTERATTIVE e verificata in questa chat):
   - copiare la cartella `cornice-dinamica/` nel nuovo progetto e adattare
     nel file dedicato: APP_URL, titolo, palette (carta #f8f0e2 / bordeaux
     #7a1f2b / oro #c9a227) e gli URL dei font
     `.../fonts/OpenDyslexic-{Regular,Bold}-v2.woff2`; in alternativa
     partire dal template `embed-universale.html`;
   - lato app DEVE esistere `client/src/lib/corniceToken.ts` (legge
     `?cornice=`) e Home.tsx deve rispecchiare il token in `postHeight()` e
     rispondere al ping `labvisivo:ping` (Regola d'oro 4);
   - generare i WOFF2 `-v2` dai TTF con
     `scripts/gen_woff2_cornice.py [--root …]` e servire `/fonts/*` con
     CORS `Access-Control-Allow-Origin: *` in server/index.ts (senza header
     il @font-face da Blogger è bloccato);
   - provare con `cornice-dinamica/test-impermeabile-espana.html` (2 cornici
     della stessa app + un intruso che posta altezze false: ogni cornice deve
     restare isolata, altezza corretta, furto respinto) PRIMA di pubblicare;
   - pubblicare in produzione e verificare su URL live: curl sui font
     (header CORS) + test token/ping in iframe cross-origin.

## Workflow B — Manutenzione dell'app esistente

- **Modificare gli eventi**: aggiornare `client/src/data/events.ts` (o usare
  `adatta_app.py` con la config aggiornata); gli `id` devono essere unici e le
  posizioni x/y percentuali (0–100).
- **Modificare i testi**: i prompt di gioco sono in `promptText()` di
  Home.tsx; il titolo va cambiato in 3 punti (h1 di Home.tsx, `alt`
  dell'immagine, `<title>` di index.html) — lo script lo fa insieme.
- **Colori/font**: token in `client/src/index.css` (`--primary #7a1f2b`,
  `--chart-1 #c9a227`, `--background #1a0f12`, font
  `Cambria, "Caladea", "Liberation Serif", Georgia, serif`); le classi custom
  dell'attività (.pin, .listen-btn, .dock, …) stanno sempre lì. Il font
  accessibile OpenDyslexic è dichiarato con `@font-face` in coda a index.css e
  ha priorità nella pila (Cambria resta come fallback).
- **Barra di accessibilità**: è IN ITALIANO ed è sempre la prima riga di
  `.game-root` (AccessibilityToolbar.tsx): Font (A−/A+), Interlinea,
  Righello, Modalità (alto contrasto), Ascolto (TTS) e PDF. Il modulo PDF non
  ha etichetta visibile (niente doppio «PDF»): il bottone mostra solo
  «LINEA DEL TEMPO IN PDF». Le etichette/aria sono in italiano ma il contenuto
  didattico resta in spagnolo; la voce TTS (useReadAloud.ts) rileva
  automaticamente la lingua (spagnolo/italiano).
- **Titolo/header e pulsanti in MAIUSCOLO** (stile comune delle app didattiche
  di riferimento): applicato via CSS con `text-transform: uppercase` su
  `.brand h1`, `.panel h2`, `.cta`, `.meta` — il DOM resta in minuscolo così
  screen reader e TTS leggono le parole nella forma corretta.
- **Immagini/audio**: in `client/public/`; ricordare il cache busting `?v=`.
- **Deploy**: vedi Workflow A punto 7.

## Accessibilità (funzionalità da mantenere in ogni app generata)

- **Font OpenDyslexic**: TTF/OTF in `client/public/fonts/`, `@font-face` in
  `client/src/index.css` (Regular/Bold/Italic), base64 in
  `client/src/lib/opendyslexicBase64.ts` per il PDF.
- **Barra accessibilità** (`components/AccessibilityToolbar.tsx` + CSS
  `.accbar/.accgroup/.acclabel/.accbtn/.accbtn-on/.accbtn-pdf`) — IN
  ITALIANO: 5 moduli + PDF; `lang="it"` su barra e avvisi sr-only; ogni
  capsula ha `role="group"` + aria-label; live region `role="status"`.
- **Contesti/stato**: `contexts/AccessibilityContext.tsx` (fontScale 0.8–1.6,
  lineHeight 1.5–2.6, ruler, mode normale/contrasto; salvati in localStorage
  `exm_access`; applicati su `<html>` via CSS vars `--lf-scale`/`--lf-lh` e
  classi `lf-ruler`/`lf-hc`).
- **TTS auto-lingua**: `hooks/useReadAloud.ts` legge la pagina ELEMENTO per
  ELEMENTO — titolo, contatore «Audio N de 7», ogni pulsante-punto della
  linea del tempo (dal suo aria-label), messaggi e pulsanti del dock — con
  MINIME PAUSE tra gli elementi (ITEM_PAUSE_MS 350 ms; tra frasi dello stesso
  elemento CHUNK_PAUSE_MS 90 ms), così nessun testo risulta «incollato».
  Riconosce la lingua frase per frase (marcatori spagnolo/italiano in
  `detectLang`) e sceglie la voce migliore per lingua; converte il testo in
  MAIUSCOLO (da text-transform) in minuscole; espande numeri e numerali
  romani nella lingua rilevata — in spagnolo un romano ORDINALE davanti a un
  nome (es. «I Guerra Carlista») è letto come ordinale («Primera Guerra
  Carlista»), con genere dedotto dalla parola seguente. Esclude dalla lettura
  la barra (`role=toolbar`) e gli avvisi sr-only/status (`role=status`,
  `.sr-only`, righello). Velocità di lettura rate 0.95.
- **PDF accessibile**: `lib/timelinePdf.ts` genera in A4 orizzontale la linea
  del tempo SENZA hotspot ma CON le 7 illustrazioni della mappa (ritagliate
  al volo dalla `<img>` timeline stessa, stessa-origin → nessun CORS) sopra
  l'asse, anni e titoli sotto, in OpenDyslexic incastonato (≥14 pt,
  interlinea 1.5), con MARGINI di ~3 cm sui 4 lati (`M = 30` mm: mappa
  rimpicciolita e incorniciata) e SENZA le istruzioni di gioco (è un
  materiale di ripasso/copia). Il ritaglio delle figure è DINAMICO per cella
  (vedi architettura). Accessibile SOLO dal bottone della barra (modulo
  PDF) — l'overlay finale «Actividad completada» NON ha più il pulsante di
  download (rimosso su richiesta) e copre tutta la barra (`z-index 120`,
  sopra `.accbar` z 30): così il titolo finale non viene tagliato sul
  cellulare. Il bottone PDF della barra è a UNA riga: solo «LINEA DEL TEMPO
  IN PDF», senza etichetta «PDF» accanto (niente doppio «PDF») e senza parole
  extra tipo «SCARICA».
- **WOFF2 per la cornice**: `client/public/fonts/OpenDyslexic-{Regular,Bold}-v2.woff2`
  (generati dai TTF con `scripts/gen_woff2_cornice.py`) — la cornice dinamica
  v3 li carica dall'app via CORS: /fonts/* deve rispondere con
  `Access-Control-Allow-Origin: *` (server/index.ts).
- **Alto contrasto e righello**: `html.lf-hc` (filtro + sfondo nero) e
  `html.lf-ruler .lf-ruler-band` (banda che segue il puntatore).
- **Focus e riduzione movimento**: `:focus-visible` dorato, `::selection` ad
  alto contrasto, `prefers-reduced-motion` rispettato.
- **Prompt iniziale centrato**: nella schermata di avvio il testo «Pulsa en
  cualquier parte para empezar.» usa la classe `.prompt.start` (flex:1,
  text-align:center) dentro `.dock`.
- **Immagine con testi OpenDyslexic**: la grafica della linea del tempo ha
  istruzione/anni/titoli ridisegnati con OpenDyslexic (script
  `scripts/riscrivi_testi_immagine_opendyslexic.py`); geometria dell'immagine
  invariata (1376×821), quindi pin/embed non cambiano.

## Regole d'oro (imparate a caro prezzo)

1. **Un solo canale audio**: un unico `<audio>` (audioRef) + copie silenziose
   `preload="auto"`. Ogni `play()` mette in pausa il resto: le sovrapposizioni
   non possono esistere. Non introdurre mai un secondo elemento audio attivo.
2. **`error` → settle**: i listener `ended` E `error` chiudono la coda; un
   file audio mancante non deve bloccare il gioco.
3. **Pin ancorati all'area DIPINTA**: l'immagine usa `object-fit: contain`;
   `syncOverlay()` calcola l'area dipinta con `getBoundingClientRect` +
   `naturalWidth/naturalHeight`. Mai posizionare i pin sul box dell'elemento.
4. **postMessage**: i tipi `labvisivo:height` e `romanticismo:height` NON si
   cambiano mai; `postHeight()` va rilanciato quando cambiano phase/needsTap/
   heard/cue (il footer cambia altezza). Se l'app è caricata con
   `?cornice=<token>` (cornice dinamica v3 impermeabile), ogni messaggio deve
   rispecchiare il token (lib/corniceToken.ts) e l'app deve rispondere al ping
   `labvisivo:ping` inviando l'altezza corrente: è così che la cornice filtra
   i messaggi delle altre app presenti nella stessa pagina.
5. **MAP_W/MAP_H**: devono corrispondere alla dimensione naturale della nuova
   immagine, o i pin andranno fuori posizione.
6. **Cache busting**: ogni file sostituito (immagine, audio) → nuovo `?v=` in
   tutti i riferimenti.
7. **h1/title/alt in 3 punti**: Home.tsx h1, Home.tsx alt, index.html title.
8. **Niente logica toccata**: per una nuova app si cambiano SOLO dati e
   risorse; la macchina a stati di Home.tsx resta identica.
9. **Embed**: la radice usa la classe `embedded` quando `window.parent !==
   window`; non rimuoverla.
10. **Testi guida**: i messaggi del gioco restano in spagnolo (o nella lingua
    del nuovo argomento) e sono centrati; «¡Correcto!» e «No es ese punto…»
    sono testi fissi in promptText().

## Risorse della skill

- `scripts/adatta_app.py` — riscrive dati/titolo/dimensioni per una nuova app
  (supporta `--dry-run` e `--root`).
- `scripts/riscrivi_testi_immagine_opendyslexic.py` — ridisegna i testi di
  `timeline.png` in OpenDyslexic (istruzione, anni, titoli) senza cambiare la
  geometria; adattare CX/YEARS/TITLES/INSTR alla nuova linea del tempo.
- `scripts/gen_woff2_cornice.py` — genera i WOFF2 `-v2` (Regular/Bold) dai
  TTF in `client/public/fonts/`, necessari alla cornice dinamica v3
  (`--root` per puntare a un'altra app).
- `scripts/qa_pdf_layout.mjs` — verifica RAPIDA del layout del PDF (margini
  ~3 cm, centratura, assenza di sbordi) SENZA browser: replica in Node la
  geometria esatta di timelinePdf.ts con jsPDF e i font veri del progetto
  (disegna rettangoli al posto delle icone). Uso: `node scripts/qa_pdf_layout.mjs
  --root <progetto>` poi `pdftoppm -png -r 120` e ispezione visiva. Tenere le
  costanti ALLINEATE a timelinePdf.ts.
- `templates/app-config.json` — config di esempio con i 7 eventi reali.
- `references/architettura.md` — scheda tecnica completa: struttura file,
  macchina a stati, matematica di syncOverlay, canale audio, embed/cornice
  dinamica v3, token di stile, comandi deploy, checklist 8 passi, errori
  comuni. Leggerlo per la massima fedeltà.
- `cornice-dinamica/` (nel progetto, non nella skill) — cornice v3 dedicata
  per Blogger + universale + test: vedi la sezione Embed dell'architettura.

## Esempio reale

Progetto: `/home/user/espana-xix-match/` · Produzione:
`https://espana-xix-match.easy-peasy.site` · Embed nel post Blogger
`https://blogdelprofessoreandreacentinaro.blogspot.com/2026/08/letteratura-spagnola.html` ·
Immagine `client/public/timeline.png` (1376×821) · Audio in `client/public/audio/`
(e1808.mp3…e1898.mp3, intro/ok/ko/fin.mp3).
