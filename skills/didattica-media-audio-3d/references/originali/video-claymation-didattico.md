# Archivio di dettaglio — video-claymation-didattico

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/video-clay.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Panoramica (8 fasi)
- Fase 1 — Sceneggiatura
- Fase 2 — Voce narrante
- Fase 3 — Riferimenti visivi (stile)
- Fase 4 — Piano scene
- Fase 5 — Generazione dei clip
- Fase 6 — Assemblaggio
- Fase 7 — Controllo qualità
- Fase 8 — Correzioni
- Errori comuni (sintesi)
- Risorse della skill
- Esempio reale

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Video Claymation Didattico

Workflow completo per creare documentari didattici in stile claymation con l'IA:
sceneggiatura → voce narrante → riferimenti visivi → piano scene → generazione clip →
assemblaggio ffmpeg → QA → correzioni. Estrae la ricetta dal progetto reale
`/home/user/claymation-espana-xix/` (documentario «Marco histórico del Romanticismo
en España», 35 scene, 5 min 19 s, 1280×720@24, nessun testo a schermo).

## Panoramica (8 fasi)

1. **Sceneggiatura**: 25–40 frasi brevi e autosufficienti (una frase = una scena).
2. **Voce narrante**: TTS o registrazione; misurare la durata con `ffprobe`.
3. **Riferimenti visivi**: 5–8 immagini chiave (personaggi/ambienti ricorrenti) nello stesso stile.
4. **Piano scene**: `/home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/plan_scene.py` → JSON con durate proporzionali al testo.
5. **Generazione clip**: un clip AI per scena (~10 s, 1280×720, 24 fps) da prompt a 3 strati + riferimenti.
6. **Assemblaggio**: `/home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/assemble_claymation.py` (ffmpeg: trim/stretch, concat, fades, mux).
7. **QA**: `/home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/qa_frames.py` — fogli di verifica con frame estratti a timestamp strategici.
8. **Correzioni**: rigenerare SOLO i clip difettosi; riassemblare.

## Fase 1 — Sceneggiatura

- Scrivere le frasi in ordine narrativo (apertura → capitoli → chiusura riflessiva).
- Ogni frase deve evocare una scena visiva chiara e descrivere un solo momento.
- Mediamente 8–15 parole per frase. Nessuna didascalia prevista nel montaggio finale.
- Per un documentario storico: precisione dei fatti + linguaggio semplice.

## Fase 2 — Voce narrante

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 voce.m4a
```

- La durata totale dell'audio è il VINCOLO di sincronizzazione: la somma delle durate
  delle scene deve eguagliarla.
- Formato: file singolo, senza silenzi lunghi, bitrate ≥ 128 kbps, voce chiara e uniforme.
- Se la voce cambia, ricalcolare il piano con la nuova durata.

## Fase 3 — Riferimenti visivi (stile)

- Generare 5–8 immagini chiave con il suffisso di stile costante
  `/home/user/skills/didattica-media-audio-3d/templates/video-claymation-didattico/clay-style.txt` (il blocco `CLAY`), una per personaggio/ambiente ricorrente.
- Usare `media_generate_from_images` passando la STESSA immagine di riferimento per lo
  stesso personaggio in tutte le scene → coerenza garantita.
- Il suffisso CLAY standard: "Claymation stop-motion diorama, plasticine clay texture with
  visible fingerprints, miniature figures and sets, warm cinematic lighting, dramatic sky,
  epic documentary style, 16:9 widescreen."

## Fase 4 — Piano scene

```bash
python3 /home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/plan_scene.py --audio 318.483 --scenes scene.tsv --out clips_plan.json
```

- `scene.tsv`: `caption<TAB>testo[<TAB>descrizione visiva[<TAB>ref1,ref2]]`.
- Formula durate: `dur_i = AUDIO_DUR × len(text_i) / Σ len(text_j)`, poi riscalatura esatta;
  l'ultimo clip assorbe l'arrotondamento.
- Il campo `visual` = descrizione scena + movimento camera + suffisso CLAY; il campo
  `refs` contiene gli URL dei riferimenti.
- Se il file TSV non ha la colonna visual, completare i prompt PRIMA della generazione
  (struttura in `/home/user/skills/didattica-media-audio-3d/templates/video-claymation-didattico/prompt-scena.md`).

## Fase 5 — Generazione dei clip

- Un clip per scena, durata nativa ~10 s, 1280×720, 24 fps (H.264). I clip generati
  possono contenere una cover MJPEG embedded: ribakere se serve (vedi Errori).
- Prompt a 3 strati (vedi `/home/user/skills/didattica-media-audio-3d/templates/video-claymation-didattico/prompt-scena.md`):
  1. CONTENUTO (azione concreta: "hands the crown", "tearing up a paper document");
  2. CAMERA (movimento lento: slow push-in / pan / zoom / tracking / orbit / pull-back);
  3. STILE (suffisso CLAY, identico in tutte le scene).
- Passare 1–2 immagini di riferimento per clip (personaggi/ambienti presenti).
- NON chiedere testi nel prompt; prevedere comunque il QA sulle scene "a rischio"
  (documenti, giornali, bandiere, insegne).

## Fase 6 — Assemblaggio

```bash
python3 /home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/assemble_claymation.py --plan clips_plan.json --clips clips_v2 \
    --audio narrazione.m4a --out video_finale.mp4
```

- Per ogni clip: se `target ≤ dn + 0.05` → `trim=0:target,setpts=PTS-STARTPTS`
  (accorcia); altrimenti → `setpts=PTS*(target/dn)` (allunga, max ~1.5×).
- Poi `scale=1280:720:flags=lanczos,fps=24,format=yuv420p,setsar=1`; concat; fade in 0.5 s,
  fade out 0.7 s; audio `aresample=48000, stereo`.
- Encoding: `libx264, preset medium, crf 19, -r 24, yuv420p`; audio `aac 192k 48 kHz`;
  `-movflags +faststart`, `-shortest`.
- Montaggio finale: SENZA testi (non usare `--captions-dir`). La variante con didascalie
  (`--captions-dir`) serve solo come bozza di lavoro.

## Fase 7 — Controllo qualità

```bash
python3 /home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/qa_frames.py video.mp4 --times 78.5,80,82,84,86,87 --out verify.jpg
```

- Scegliere timestamp strategici: inizio/metà/fine di ogni capitolo + le scene dove l'IA
  potrebbe scrivere testi (documenti, giornali, bandiere).
- Controllare: testi errati/inventati, coerenza personaggi, sincronia audio/ritmo, assenza
  di titoli/didascalie/"Fin" nel montaggio finale.

## Fase 8 — Correzioni

- Rigenerare SOLO il clip difettoso (es. con il testo corretto esplicito nel prompt) e
  riassemblare: nel progetto di riferimento è stato rigenerato solo clip09
  («CONSTITUCIÓN» → «CONSTITUCIÓN ESPAÑOLA»).
- Dopo ogni correzione, rifare il QA sui frame interessati.

## Errori comuni (sintesi)

| Errore | Soluzione |
|---|---|
| Testi inventati dall'IA su documenti/giornali | Rigenerare il clip col testo esplicito corretto o "no text"; QA mirato |
| Personaggi incoerenti | Stessi riferimenti per lo stesso personaggio |
| Clip più corto/lungo del segmento | `setpts=PTS*(target/dn)` / `trim=0:target` |
| Audio fuori sincrono | Somma durate = durata audio; `-shortest`; 48 kHz stereo |
| Cover MJPEG embedded nei clip | Ribake: `-an -c:v libx264 -pix_fmt yuv420p -r 24 -s 1280x720` |
| Titoli/«Fin» indesiderati | Nessun drawtext nel montaggio finale; verifica frame |

## Risorse della skill

- `/home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/plan_scene.py` — generatore del piano scene (durate proporzionali).
- `/home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/assemble_claymation.py` — assemblaggio ffmpeg (con/senza didascalie).
- `/home/user/skills/didattica-media-audio-3d/scripts/video-claymation-didattico/qa_frames.py` — foglio QA con frame estratti e timestamp.
- `/home/user/skills/didattica-media-audio-3d/templates/video-claymation-didattico/clay-style.txt` — suffisso di stile CLAY (costante).
- `/home/user/skills/didattica-media-audio-3d/templates/video-claymation-didattico/prompt-scena.md` — struttura prompt a 3 strati + 3 esempi reali.
- `/home/user/skills/didattica-media-audio-3d/templates/video-claymation-didattico/scena.json` — template di una voce del piano.
- `/home/user/skills/didattica-media-audio-3d/references/video-claymation-didattico/workflow-report.md` — report completo del progetto reale (scheda tecnica,
  versioni, correzioni, tabella errori, comando ffmpeg completo, appendice con tutte le 35
  scene e i testi narrati). Leggerlo per massima fedeltà o come esempio integrale.

## Esempio reale

Progetto di riferimento: `/home/user/claymation-espana-xix/` — piano
`clips_plan_final.json` (35 scene), clip in `clips_v2/`, finale
`Espana_siglo_XIX_claymation_v3_sin_titulos.mp4`, fogli QA `qa_*.jpg`, `verify_*.jpg`.
