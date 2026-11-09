# Report di riferimento — Documentario claymation «Marco histórico del Romanticismo en España»

Riferimento completo del progetto reale (`/home/user/claymation-espana-xix/`) da cui è stata
estratta questa skill. Contiene i dettagli verificati: scheda tecnica, versioni, correzioni,
errori comuni e l'appendice con tutte le 35 scene. Leggere questo file quando serve la massima
fedeltà al progetto originale o un esempio completo.

## Scheda tecnica del video finale

| Proprietà | Valore |
|---|---|
| File | `Espana_siglo_XIX_claymation_v3_sin_titulos.mp4` |
| Contenitore | MP4, `+faststart` |
| Video | H.264 (libx264), 1280×720, 24 fps, CRF 19, preset medium, YUV 4:2:0 |
| Audio | AAC 192 kbps, 48 kHz, stereo (FLTP) |
| Durata | 318.79 s ≈ 5 min 19 s (narrazione 318.48 s) |
| Dimensione | ≈ 113 MB (≈ 2.8 Mbps) |
| Struttura | 35 clip concatenati, fade in 0.5 s, fade out 0.7 s |
| Testi | Nessuno (nessun drawtext, nessuna didascalia, nessuna schermata "Fin") |

## Le 8 fasi (sintesi operativa)

1. **Sceneggiatura** — 35 frasi brevi e autosufficienti in spagnolo; una frase = una scena.
2. **Voce narrante** — voce maschile peninsulare; due versioni usate: `narrazione.mp3`
   (311.458 s) e `Video_Project_3.m4a` (318.483 s, definitiva).
3. **Riferimenti visivi** — 7 immagini chiave (palazzo, Fernando VII, Isabel II, María
   Cristina, carlista, Napoleone, impero) per coerenza personaggi/ambienti.
4. **Piano scene** — `plan_final.py`: durate proporzionali ai caratteri, riscalate
   esattamente sull'audio; output `clips_plan_final.json`.
5. **Generazione clip** — 35 clip AI ~10 s (10.042 s), 1280×720, 24 fps; prompt a 3 strati;
   coerenza garantita dai riferimenti.
6. **Assemblaggio** — ffmpeg: trim/stretch per scena, scale, concat, fades, mux audio.
7. **QA** — estrazione frame a timestamp strategici e fogli di verifica (griglia 6 frame
   con timestamp gialli).
8. **Correzioni** — rigenerazione del singolo clip difettoso; montaggio finale senza testi.

## Versioni del progetto (storico reale)

| File | Scene | Voce | Testi | Note |
|---|---|---|---|---|
| `Espana_siglo_XIX_claymation.mp4` | 31 | narrazione.mp3 | no | v1, workflow Shakespeare (ribake: -an, crf 20) |
| `Espana_siglo_XIX_claymation_nueva_voz.mp4` | 31 | Video_Project_3.m4a | no | seconda voce + «Constitución Española» |
| `Espana_siglo_XIX_claymation_v2.mp4` | 35 | Video_Project_3.m4a | sì (didascalie, titolo, Fin) | piano a 35 scene |
| `Espana_siglo_XIX_claymation_v3_sin_titulos.mp4` | 35 | Video_Project_3.m4a | **no** | **finale consegnata**; clip09 rigenerato |

## Le due correzioni chiave (documentate con fogli QA)

1. **Testo errato in una scena.** La scena delle Cortes di Cádiz mostrava un documento con la
   scritta «CONSTITUCIÓN»; la dicitura corretta è «CONSTITUCIÓN ESPAÑOLA». Il clip09 è stato
   rigenerato con l'indicazione esplicita del testo corretto e la verifica
   (`verify_const_final.jpg`, t=78.5–87 s) conferma la scritta leggibile sul documento.
2. **Testi sovraimpressi.** La v2 conteneva titoli, didascalie con date, «EL REY DE BARRO» e
   la schermata «Fin». Il montaggio finale è stato rifatto senza drawtext
   (`assemble_v4.py`) e la verifica (`verify_sin_titulos.jpg`) conferma l'assenza di testi.

## Errori comuni e soluzioni (tabella completa)

| Errore | Sintomo | Soluzione |
|---|---|---|
| Testi generati dall'IA nelle immagini | Scritte inventate/errate su documenti, giornali, bandiere | QA sui frame "a rischio"; rigenerare il singolo clip col testo esplicito corretto o chiedendo "no text" |
| Personaggi incoerenti tra scene | Lo stesso re cambia aspetto | Stessa immagine di riferimento per lo stesso personaggio (media_generate_from_images) |
| Clip più corto del segmento narrato | Il video finisce prima della frase | Allungare con `setpts=PTS*(target/dn)` (max ~1.5×) |
| Clip più lungo del segmento | La scena prosegue mentre inizia la frase successiva | Tagliare con `trim=0:target,setpts=PTS-STARTPTS` |
| Audio non sincronizzato | Video più lungo o più corto dell'audio | Somma durate = durata audio; `-shortest`; ricampionare 48 kHz stereo |
| Clip con poster MJPEG embedded | Stream video extra nel file | Ribake: `-an -c:v libx264 -pix_fmt yuv420p -r 24 -s 1280x720` |
| Titoli/date/«Fin» indesiderati | Testo sovraimpresso | Non usare drawtext; verificare con frame estratti |
| Durate sballate dopo cambio voce | Scene fuori sincrono | Ricalcolare il piano con la nuova AUDIO_DUR |
| Salto brusco tra scene | Transizioni secche | Fade in 0.5 s e fade out 0.7 s; camera lenta in ogni clip |

## Comando ffmpeg completo (sintesi del filter_complex, 35 clip)

```bash
ffmpeg -y -i clip01.mp4 … -i clip35.mp4 -i voce.m4a \
  -filter_complex "\
[0:v]setpts=PTS*(10.091/10.042),scale=1280:720:flags=lanczos,fps=24,format=yuv420p,setsar=1[v0]; \
… \
[34:v]trim=0:10.0,setpts=PTS-STARTPTS,scale=1280:720:flags=lanczos,fps=24,format=yuv420p,setsar=1[v34]; \
[v0][v1]…[v34]concat=n=35:v=1:a=0,fade=t=in:st=0:d=0.5,fade=t=out:st=318.09:d=0.7[vout]; \
[35:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -preset medium -crf 19 -r 24 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -shortest output.mp4
```

## QA — comandi utili

```bash
# durata clip / audio
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 clip09.mp4
# foglio di verifica (6 frame + timestamp)
python3 qa_frames.py video.mp4 --times 78.5,80,82,84,86,87 --out verify.jpg
```

## Appendice A — Le 35 scene del documentario (id, durata, didascalia, testo narrato)

Vedi tabella generata da `clips_plan_final.json` qui sotto.

| ID | Durata (s) | Didascalia | Testo narrato (spagnolo) |
|---|---|---|---|
| clip01 | 10.091 | Marco histórico del Romanticismo en España | Marco histórico del Romanticismo en España. El siglo XIX español empieza con una invasión y termina con un imperio que se hunde. |
| clip02 | 14.820 | Reyes, guerra y esperanza | En medio hay reyes que van y vuelven, una constitución nacida en guerra, una niña en el trono, una reina que se exilia, una república que no llega a envejecer y una corona que se restaura. |
| clip03 | 8.593 | 1808 — Carlos IV abdica | En 1808 el rey es Carlos IV, pero el poder ya no está en sus manos. Abdica en favor de su hijo, Fernando VII. |
| clip04 | 12.061 | 1808 — José I, rey impuesto | Napoleón aprovecha esa debilidad y coloca en el trono a su propio hermano, José I. Para muchos españoles no es un cambio de dinastía, es una humillación. |
| clip05 | 4.572 | 1808 — El Dos de Mayo | El 2 de mayo Madrid se subleva. La chispa recorre el país. |
| clip06 | 11.983 | 1808-1814 — Guerra de Independencia | Campesinos, soldados y civiles se lanzan a una guerra larga contra el ejército francés. No es solo una guerra de batallas. Es una guerra de resistencia. |
| clip07 | 4.888 | 1814 — Vuelve Fernando VII | En 1814 los franceses se van y Fernando VII recupera el trono. |
| clip08 | 9.539 | 1812 — La pregunta | España ha expulsado al invasor, pero queda una pregunta más difícil: ¿el rey lo puede todo o el pueblo también tiene voz? |
| clip09 | 10.958 | 1812 — Las Cortes de Cádiz | Esa pregunta se responde, al menos sobre el papel, en 1812. Mientras tanto, en Cádiz, las Cortes aprueban la primera Constitución española. |
| clip10 | 13.480 | 1812 — La soberanía nacional | Es un texto nuevo y valiente. Limita el poder del rey y dice algo que cambia el lenguaje de la política: la soberanía no pertenece solo a la corona, pertenece a la nación. |
| clip11 | 3.153 | 1812 — Los ciudadanos | Los ciudadanos existen. Tienen derechos. |
| clip12 | 8.829 | 1823 — El absolutismo | Cuando Fernando VII vuelve, sin embargo, no quiere esa España. Deroga la Constitución y restaura el absolutismo. |
| clip13 | 5.361 | 1823 — La semilla liberal | La semilla liberal ya está plantada, pero el rey intenta enterrarla. |
| clip14 | 6.070 | 1833 — La tensión estalla | En 1833 esa tensión estalla otra vez, ahora dentro de la propia familia real. |
| clip15 | 5.361 | 1833 — Muere Fernando VII | Muere Fernando VII. El trono pasa a su hija Isabel II, todavía niña. |
| clip16 | 3.469 | 1833 — La regencia | La madre, María Cristina, asume la regencia. |
| clip17 | 7.647 | 1833 — Carlos María Isidro | El hermano del rey muerto, Carlos María Isidro, no lo acepta. Para él, una mujer no puede reinar. |
| clip18 | 11.510 | 1833-1840 — Guerra carlista | Estalla la primera guerra carlista, carlistas contra isabelinos. No es solo una pelea entre tío y sobrina. Es un choque entre dos ideas de España. |
| clip19 | 11.667 | 1833-1840 — Dos ideas de España | Una mira hacia atrás, hacia la tradición, el trono fuerte y la religión como eje. La otra, con Isabel II, se apoyan los liberales. El país se parte. |
| clip20 | 7.804 | 1840-1868 — Una herida abierta | La guerra dura años y deja una herida que volverá a abrirse. Isabel II crece en un trono inestable. |
| clip21 | 5.597 | 1868 — La Gloriosa | En 1868 los militares se levantan. Es la Gloriosa. Derrocan a la reina. |
| clip22 | 8.356 | 1868 — Exilio de Isabel II | Isabel II se exilia en Francia. Por primera vez en mucho tiempo, España se queda sin Borbón en el palacio. |
| clip23 | 11.115 | 1868-1874 — El Sexenio | Empieza el Sexenio Democrático, seis años de ensayos, de esperanza y de caos. El país quiere otra forma de gobierno y no está seguro de cuál. |
| clip24 | 13.638 | 1871 — Amadeo I de Saboya | Durante ese sexenio se busca una solución intermedia. Se elige a Amadeo I de Saboya, un rey extranjero, para intentar una monarquía democrática, corona sí, pero con límites. |
| clip25 | 6.780 | 1873 — Abdica Amadeo | La idea es elegante, la realidad no lo es. Amadeo no logra sostenerse. En 1873 abdica. |
| clip26 | 10.485 | 1873 — La Primera República | Entonces España da un paso que muchos soñaban y pocos consiguen controlar, se proclama la Primera República. Dura poco más de un año. |
| clip27 | 8.672 | 1873-1874 — Frágil y breve | Hay divisiones, revueltas, gobiernos que se suceden demasiado rápido. La República nace frágil y muere pronto. |
| clip28 | 8.672 | 1875 — La Restauración | El experimento se cierra antes de convertirse en costumbre. En 1875 el péndulo vuelve atrás, pero no del todo. |
| clip29 | 7.095 | 1875 — Alfonso XII | Alfonso XII, hijo de Isabel II, restaura la monarquía borbónica. Entra en España en enero. |
| clip30 | 12.771 | 1875 — Orden y corona | El país, agotado, acepta otra vez a un rey. No es el absolutismo de Fernando VII. Es una restauración, orden, corona y la promesa de que el siglo deje de temblar. |
| clip31 | 3.784 | 1875 — La promesa | Durante un tiempo, esa promesa parece funcionar. |
| clip32 | 13.323 | 1898 — El desastre | El final, sin embargo, no es una victoria. Es 1898. Alfonso XII ya ha muerto. Gobierna su viuda, María Cristina de Habsburgo, como regente de Alfonso XIII, todavía niño. |
| clip33 | 8.908 | 1898 — Guerra contra EE. UU. | España entra en guerra contra Estados Unidos y pierde. Con la derrota se van Cuba, Puerto Rico, Filipinas y Guam. |
| clip34 | 11.904 | 1898 — El imperio se hunde | El imperio de ultramar, que durante siglos había sido parte de la identidad española, se deshace de golpe. Los periódicos lo llaman el desastre del 98. |
| clip35 | 15.527 | 1898 — ¿Qué país queda? | No es solo una pérdida de islas. Es la sensación de que el siglo se cierra con una pregunta amarga después de tantas guerras, constituciones, reinas, republicanos y restauraciones, ¿qué país queda? |
