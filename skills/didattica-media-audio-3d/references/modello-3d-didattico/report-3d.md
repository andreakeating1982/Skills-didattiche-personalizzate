# Riferimento — Diorama 3D «Marco histórico del Romanticismo en España»

Riferimento completo del progetto reale `/home/user/modello3d/` da cui è stata
estratta questa skill. Contiene la scheda tecnica verificata del GLB, la
pipeline dettagliata, i parametri numerici, lo storico delle modifiche e le
guide di distribuzione. Leggere questo file quando serve la massima fedeltà al
progetto originale o un esempio completo.

## Scheda tecnica del GLB finale

| Proprietà | Valore |
|---|---|
| File | `linea_del_tempo_3d.glb` (2.336.644 byte ≈ 2,2 MB) |
| Formato | glTF 2.0 Binary — generator: trimesh |
| Struttura | 1 scena · 26 nodi · 26 mesh · 46 accessor · 60 bufferView · 1 buffer BIN (2,32 MB) |
| Materiali | 20 (PBR metallic-roughness) |
| Texture | 14 PNG embeddate nel BIN (figure + targhette) |
| Triangoli | 26.384 |
| Ingombro | X 29,78 · Y 5,61 · Z 8,90 (Y up; Z da −4,30 a 4,60) |
| Nomi mesh | zoccolo, basamento, gradino, freccia, freccia_zoccolo, scena_0_1808…scena_6_1898, sfera_0…sfera_6, targa_0_1808…targa_6_1898 |
| Validazione | Khronos gltf-validator: **0 errori, 0 avvisi** |

## La pipeline (8 fasi)

1. **Sorgente 2D** — `source.png` (1376×930), fascia figure Y 366–542, 7 colonne X.
2. **Ritaglio** — `ritaglia_figure.py`: flood fill dai bordi (FIXED_RANGE, tol 16), erode 3 px, rimozione sacche di bianco piatto, MORPH_CLOSE, componenti connesse (≥45 px), bleed 8 iterazioni, alfa sfumato → `tex/figura_N.png` + `meta.json` + `provino_ritagli.png`.
3. **Testi** — targhette 2048×1024 (2:1), anno bordeaux, testo marrone scuro con auto-wrap/shrink (104→60 ×S), insegna opzionale; font Caladea-Bold.
4. **Geometria** — `costruisci_modello.py`: scala unica `PX = 0.0199` u/px (SPAN = 27.38), estrusione sagome (SS=4), basamento 2 livelli + gradino, freccia a nastro (shaft buffer 0.4975 + punta 0.995, AR_T 0.62), 7 sfere icosphere r 0.32, 7 targhette inclinate 52°, insegna opzionale.
5. **Export** — `scene.export("*.glb")` (trimesh), texture embeddate.
6. **Validazione** — `node valida_glb.js` (Khronos): 0/0.
7. **Anteprime** — render.html (three.js 0.160, RoomEnvironment, ombre) + save_server.py (porta 8099, POST /save): 4 inquadrature.
8. **Distribuzione** — Sketchfab, Figmin XR (visore), Blogger embed.

## Parametri chiave (tutti verificati)

`PX 0.0199 · FIG_H 3.50 · FIG_T 0.42 · BASE 28.98×0.80×7.6 · PLINTH 29.78×0.50×8.9 ·
RISER 28.18×1.00×2.10 · Z_BASE 0.15 · Z_RISER −2.10 · Z_FIG −2.10 · Z_ARROW 1.00 ·
Z_LABEL 3.35 · Z_TITLE −4.10 · LABEL_W 2.86 · LABEL_TILT 52° · R_SHAFT 0.4975 ·
R_HEAD 0.995 · AR_T 0.62 · sfera r 0.32 · SS 4 · UP 3 · alphaCutoff 0.4`

Palette: viola #603090 · viola scuro #46206c · oro #c9a227 · noce #4a2f21 ·
pergamena #efe3cd · gradino #e1d0af · bordeaux #7a1f2b · crema #f3e4cd.

## Inquadrature anteprima (render.html, three.js)

| File | Risoluzione | pos camera | lookAt | FOV |
|---|---|---|---|---|
| anteprima_1.png | 2000×1125 | (−15.0, 7.6, 22.0) | (0, 1.2, 0) | 36° |
| anteprima_2.png | 2000×1125 | (0, 3.2, 28.0) | (0, 1.3, 0) | 36° |
| anteprima_3.png | 1600×1000 | (3.4, 3.0, 7.4) | (3.7, 1.7, −2.1) | 38° |
| anteprima_4.png | 1600×1000 | (−9.6, 2.4, 7.0) | (−10.5, 1.1, 0.4) | 40° |

## Storico delle modifiche

| Quando | Cosa | Dettagli |
|---|---|---|
| 21/08 ~18:50 | Prima versione | Diorama con insegna del titolo, 26 oggetti, validato 0/0 |
| 21/08 ~20:59 | **Insegna rimossa** (richiesta docente) | `CON_INSEGNA = False` |
| 21/08 ~20:59 | Ricentratura | RISER_D 3.6→2.10, BASE_D 8.6→7.6, PLINTH_D 9.9→8.9, Z_BASE 0.15 |
| 21/08 ~20:59 | Inquadrature aggiornate | Camera più arretrata e meno alta |
| 21/08 21:00 | Consegna | GLB 2,2 MB, 26.384 triangoli, 0/0, ZIP Sketchfab |

## Distribuzione

- **Sketchfab**: Upload → categoria Cultural heritage & history; Scene → Background
  #EEF1F6; Lighting → Environment Studio/Soft Box intensità ≈1.6 con ombre;
  Camera → tre quarti + Save view; **Materials → Opacity = Mask** (mai Blend:
  bordi traslucidi).
- **Figmin XR** (Meta Quest 3): il GLB è l'oggetto espositivo; bandiere e zone di
  rilascio vivono nella scena Figmin allestita dal docente.
- **Blogger**: iframe fornito da Sketchfab nella cornice beige del post.

## Errori comuni (tabella sintetica)

| Errore | Soluzione |
|---|---|
| Alone chiaro attorno alle figure | Erosion 3 px + bleed 8 iterazioni; provino su scacchi |
| Bordi traslucidi in Sketchfab | alphaMode MASK, alphaCutoff 0.4; Opacity = Mask |
| Contorni a scalini | UP=3 + SS=4 con Gaussian blur e risoglia |
| Figure sospese | Azzerare il piede: `apply_translation([0, -foot, 0])` |
| Targhette schiacciate | Camera arretrata e bassa; targa 2:1 |
| Testo che non entra | Auto-wrap + shrink 104→60 ×S |
| Basamento sbilanciato | Ricentrare Z_BASE e ridurre BASE_D/PLINTH_D/RISER_D |
| UV capovolte | trimesh capovolge la V: fornire UV con origine in basso |
| Validatore con errori | `node valida_glb.js` dopo OGNI modifica |
| Z-fighting freccia | Nastro piatto + freccia_zoccolo sotto |
