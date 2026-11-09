# Archivio di dettaglio — espana-xix-match

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/linee-del-tempo.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Cosa fa l'app (in breve)
- Workflow A — Generare una NUOVA app simile (8 passi)
- Workflow B — Manutenzione dell'app esistente
- Regole d'oro (imparate a caro prezzo)
- Risorse della skill
- Esempio reale

Cercare il titolo pertinente; non caricare tutte le sezioni.

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
5. Tutti e 7 azzeccati → fin.mp3 → overlay «Actividad completada».
6. In iframe (Blogger) invia `postMessage {type:"labvisivo:height"}` e
   `{type:"romanticismo:height"}` per il resize automatico.

## Workflow A — Generare una NUOVA app simile (8 passi)

1. **Base**: copiare `/home/user/espana-xix-match` (o inizializzare lo stesso
   scaffold web-static) e mantenere TUTTA la logica di Home.tsx invariata:
   si cambiano solo dati e risorse.
2. **Immagine**: creare la nuova `timeline.png` (stesso aspect ratio di
   `MAP_W:MAP_H` = 1376:821 dichiarato in Home.tsx) e annotare la posizione %
   (x, y) di ogni punto sulla nuova immagine.
3. **Audio**: generare con TTS/registrazione la narrazione di ogni evento +
   intro/ok/ko/fin in `client/public/audio/` (nomi come `e1808.mp3`).
4. **Dati**: compilare `/home/user/skills/didattica-app-classe/templates/espana-xix-match/app-config.json` (titolo, theme-color,
   eventi con id/anno/titolo/audio/x/y, sfx, dimensioni) ed eseguire:

```bash
python3 /home/user/skills/didattica-app-classe/scripts/espana-xix-match/adatta_app.py \
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
8. **Embed**: iframe nel post Blogger; il resize automatico è già gestito.

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
  dell'attività (.pin, .listen-btn, .dock, …) stanno sempre lì.
- **Immagini/audio**: in `client/public/`; ricordare il cache busting `?v=`.
- **Deploy**: vedi Workflow A punto 7.

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
   heard/cue (il footer cambia altezza).
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

- `/home/user/skills/didattica-app-classe/scripts/espana-xix-match/adatta_app.py` — riscrive dati/titolo/dimensioni per una nuova app
  (supporta `--dry-run` e `--root`).
- `/home/user/skills/didattica-app-classe/templates/espana-xix-match/app-config.json` — config di esempio con i 7 eventi reali.
- `/home/user/skills/didattica-app-classe/references/espana-xix-match/architettura.md` — scheda tecnica completa: struttura file,
  macchina a stati, matematica di syncOverlay, canale audio, embed,
  token di stile, comandi deploy, checklist 8 passi, errori comuni. Leggerlo
  per la massima fedeltà.

## Esempio reale

Progetto: `/home/user/espana-xix-match/` · Produzione:
`https://espana-xix-match.easy-peasy.site` · Embed nel post Blogger
`https://blogdelprofessoreandreacentinaro.blogspot.com/2026/08/letteratura-spagnola.html` ·
Immagine `client/public/timeline.png` (1376×821) · Audio in `client/public/audio/`
(e1808.mp3…e1898.mp3, intro/ok/ko/fin.mp3).
