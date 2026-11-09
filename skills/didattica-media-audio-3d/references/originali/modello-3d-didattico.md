# Archivio di dettaglio — modello-3d-didattico

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/modelli-3d.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- Panoramica (8 fasi)
- Fase 1 — Sorgente
- Fase 2 — Ritaglio
- Fase 3 — Testi
- Fase 4 — Geometria
- Fase 5–6 — Export e validazione
- Fase 7 — Anteprime
- Fase 8 — Distribuzione
- Errori comuni (sintesi)
- Risorse della skill
- Esempio reale

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Modello 3D Didattico

Workflow completo per trasformare un'immagine 2D (linea del tempo, cartellone,
mappa) in un **diorama 3D espositivo** in formato GLB: ritaglio figure →
testi/targhette → geometria con estrusione → export trimesh → validazione →
anteprime → distribuzione (Sketchfab, Figmin XR, Blogger). Estratto dal
progetto reale `/home/user/modello3d/` (diorama della Spagna del XIX secolo,
26 oggetti, 26.384 triangoli, 2,2 MB, validato 0 errori/0 avvisi).

## Panoramica (8 fasi)

1. **Sorgente 2D**: immagine con figure su fondo chiaro; annotare dimensioni, fascia verticale e colonne X delle figure.
2. **Ritaglio figure**: `/home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/ritaglia_figure.py` → `tex/figura_N.png` (RGBA) + `meta.json` + provino.
3. **Testi**: targhette 2:1 (anno + nome), insegna opzionale; stesso font dell'identità visiva.
4. **Geometria**: `/home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/costruisci_modello.py` → estrusione sagome, basamento, freccia, sfere, targhette inclinate.
5. **Export GLB**: trimesh, texture embeddate (file autonomo).
6. **Validazione**: `node /home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/valida_glb.js` → obiettivo 0 errori / 0 avvisi.
7. **Anteprime**: render.html (three.js) + save_server.py (porta 8099).
8. **Distribuzione**: Sketchfab (embed), Figmin XR (visore), Blogger.

## Fase 1 — Sorgente

- L'immagine deve avere **sfondo chiaro e uniforme** (il flood fill parte dai bordi).
- Annotare: larghezza in px (SRC_W), fascia verticale delle figure (band Y0–Y1), colonne X di ogni figura (COLS) e i centri percentuali (CENTERS_PCT).

## Fase 2 — Ritaglio

```bash
python3 /home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/ritaglia_figure.py --source source.png \
    --cols 90-225,245-405,439-576,605-775,803-940,961-1098,1146-1308 \
    --band 366-542 --centers 11.45,23.62,36.88,50.15,63.34,74.82,89.17 \
    --events "1808|Guerra de Independencia,1812|Constitución de Cádiz,..."
```

- Flood fill dai bordi con **FLOODFILL_FIXED_RANGE** (tol 16): le parti chiare DENTRO la figura restano; sparisce solo lo sfondo collegato ai bordi.
- Erode 3 px (via l'alone), rimozione sacche di bianco piatto, MORPH_CLOSE, componenti connesse ≥45 px, **bleed 8 iterazioni** (colori verso l'esterno, niente aloni), alfa sfumato.
- `UP = 3`: ingrandire PRIMA del ritaglio → contorni morbidi e texture nitide.
- Controllare `provino_ritagli.png` (fondo a scacchi) prima di proseguire.

## Fase 3 — Testi

- Targhette **2:1** (2048×1024 con S=2): anno in bordeaux, filetto oro, testo con auto-wrap e shrink automatico (104→60 ×S, tetto 76 ×S per due righe).
- La larghezza sul modello è vincolata dalla distanza fra le scene: per ingrandire il testo si **alza** la targa, non la si allarga.

## Fase 4 — Geometria

```bash
python3 /home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/costruisci_modello.py --src-w 1376 --px 0.0199 \
    --fig-t 0.42 --label-tilt 52 --out linea_del_tempo_3d.glb
```

- **Tutto discende da UNA scala** `PX` (unità/pixel): SPAN = SRC_W × PX; figure e distanze restano nelle proporzioni dell'originale.
- Estrusione sagome reali (`polygons_from_alpha`: SS=4 + blur + risoglia → contorni curvi; buchi = contorni interni); piede azzerato (niente oggetti sospesi); UV proiettate con V già capovolta (compensare trimesh).
- Basamento: zoccolo (noce) + basamento (pergamena) + gradino (scene); freccia a **nastro piatto** (shaft buffer + punta triangolare, `unary_union`, extrude, rotazione −90° X); 7 sfere icosphere dorate; targhette inclinate 52°.
- Materiali PBR: solidi con `baseColorFactor`, texture con **alphaMode MASK e alphaCutoff 0.4** (mai BLEND: bordi traslucidi).
- Nomi parlanti: `scena_0_1808`, `targa_3_1868`, `sfera_5`, ecc. — utili per isolare oggetti.

## Fase 5–6 — Export e validazione

```bash
# export (già fatto dallo script) + validazione
cd <cartella> && npm install gltf-validator
node /home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/valida_glb.js linea_del_tempo_3d.glb
```

- Esito atteso: `errors: 0, warnings: 0`. Validare dopo OGNI modifica.

## Fase 7 — Anteprime

- `render.html` (three.js 0.160 + GLTFLoader + RoomEnvironment, ombre su tutte le mesh) + `save_server.py` (porta 8099, `POST /save` base64).
- Il diorama è largo e basso: camera **arretrata e poco alta** (es. hero pos (−15, 7.6, 22), look (0, 1.2, 0), fov 36) altrimenti le targhette si schiacciano.
- 4 inquadrature tipiche: hero tre quarti, frontale, 2 dettagli sugli eventi.

## Fase 8 — Distribuzione

- **Sketchfab**: categoria Cultural heritage & history; Background `#EEF1F6`; Environment Studio/Soft Box ≈1.6 con ombre; Camera tre quarti + Save view; **Materials → Opacity = Mask**.
- **Figmin XR** (Meta Quest 3): il GLB è l'oggetto espositivo; bandiere/interazione si allestiscono nella scena Figmin.
- **Blogger**: iframe di embed Sketchfab nella cornice del post.

## Errori comuni (sintesi)

| Errore | Soluzione |
|---|---|
| Alone chiaro sui bordi | Erode 3 px + bleed 8 iterazioni |
| Bordi traslucidi | alphaMode MASK + cutoff 0.4; in Sketchfab Opacity = Mask |
| Contorni a scalini | UP=3 nel ritaglio, SS=4 nella geometria |
| Figure sospese | Azzerare il piede: `apply_translation([0, -foot, 0])` |
| Targhette schiacciate | Camera arretrata e bassa; rapporto targa 2:1 |
| UV capovolte | Fornire UV con origine in basso (trimesh capovolge la V) |
| Basamento sbilanciato dopo una rimozione | Ricentrare Z_BASE; ridurre BASE_D/PLINTH_D/RISER_D |

## Risorse della skill

- `/home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/ritaglia_figure.py` — ritaglio figure + targhette + meta.json (CLI).
- `/home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/costruisci_modello.py` — geometria + export GLB (CLI, flag `--insegna` per il titolo).
- `/home/user/skills/didattica-media-audio-3d/scripts/modello-3d-didattico/valida_glb.js` — validatore Khronos (richiede `npm install gltf-validator`).
- `/home/user/skills/didattica-media-audio-3d/templates/modello-3d-didattico/meta.json` — struttura dell'input della geometria.
- `/home/user/skills/didattica-media-audio-3d/templates/modello-3d-didattico/palette.json` — palette + parametri chiave del progetto reale.
- `/home/user/skills/didattica-media-audio-3d/references/modello-3d-didattico/report-3d.md` — scheda tecnica, pipeline dettagliata, parametri numerici, inquadrature camera, storico modifiche, errori. Leggerlo per massima fedeltà.

## Esempio reale

Progetto di riferimento: `/home/user/modello3d/` — sorgente `source.png` (1376×930),
script `1_ritaglia_figure.py` / `2_costruisci_modello.py` (versioni originali del
workflow), `tex/` (figure + targhette), `linea_del_tempo_3d.glb` (2,2 MB, 0/0),
`render.html` + `save_server.py`, anteprime `anteprima_1..4.png`, guide
`COME-CARICARE-SU-SKETCHFAB.md` e `COME-INSERIRE-SU-BLOGGER.md` in /home/user/.
