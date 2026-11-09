# Archivio di dettaglio — latino-facile-quaderno

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/quaderno-latino.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

## Indice di ricerca

- File e percorsi (verificati)
- Regole grafiche VINCOLANTI (frutto di lunga iterazione con l'utente — non cambiarle)
- Storia versioni (direzione del gusto utente, in ordine)
- Pipeline di generazione
- Struttura contenuti
- Rimuovere/aggiungere un'area della mappa finale
- Copertina: immagine (stile CLAY) e posizione
- Rilascio di una nuova versione (checklist completa, usata per v10→v15)
- QA ricorrente (snippet pymupdf)
- Regole d'oro
- Risorse della skill

Cercare il titolo pertinente; non caricare tutte le sezioni.

---

# Latino Facile — Quaderno PDF (skill di produzione del quaderno)

Quaderno didattico associato all'app «Latino Facile»: 124 pagine A4 ad alta leggibilità (OpenDyslexic, DSA/BES), percorso di grammatica latina dalla 1ª alla 5ª con colori uguali a quelli dell'app. Il PDF viene servito dall'app come `quaderno-unico-v<NN>.pdf` (pulsante download in `Home.tsx`).

## File e percorsi (verificati)

| Percorso | Ruolo |
|---|---|
| `/home/user/quaderno-unico/` | Cartella sorgente del quaderno |
| `build_quaderno.py` | Genera `master-unico.html` (importa `sezioni_parte1`, `quaderno_v7_contenuti`, `dati_coniugazioni`; `BASE=/home/user/quaderno-unico`, `SEZ2=/home/user/quaderno2/sezioni`) |
| `master-unico.html` | HTML unico (~235 KB) da cui WeasyPrint produce il PDF |
| `style-accessibile.css` | Tutte le regole grafiche (card, schemi `.m-area`, timeline `.timeline/.tl`, copertina `.cover*`, tabelle) |
| `quaderno_v7_contenuti.py` | `SINTESI_ANNI`, `QUIZ_ANNI`, `MAPPA_FINALE`, `ANNO_ARGOMENTI` (dati di riepiloghi, quiz e mappa finale) |
| `sezioni_parte1.py`, `dati_coniugazioni.py` | Sezioni iniziali e coniugazioni |
| `/home/user/quaderno2/sezioni/` | Sezioni d'anno (contenuto delle pagine) |
| `img/anno1..5.jpg` | Immagini divisori d'anno |
| `img/copertina.jpg` | Immagine di copertina (stile clay, 2752×888 px circa) |
| `/home/user/latino-facile-app/` | App che serve il PDF (v. skill `latino-facile`) |

Versione corrente: **v16** — md5 `35d096568404a1ac11db320bf2213702`, 124 pp. Tabella sinottica delle 5 declinazioni: intera riga tinta del caso (pastello sulle desinenze, cella CASO a tinta piena). URL produzione: `https://latino-facile-app-2.easy-peasy.site` (diretta: `https://deploy-2a7acf3f-6363-wmoltmgh5q-uc.a.run.app`). Preview sandbox: `https://3000-i4nq7yqdswtyddr7hb8sj.sandbox.easy-peasy.ai`.

## Regole grafiche VINCOLANTI (frutto di lunga iterazione con l'utente — non cambiarle)

1. **Riempimenti giallo pallido/crema/pastello SOLO dentro card e box di schema**, e devono essere **uniformi e continui**: mai interrotti da elementi interni con fondo proprio, mai riempimenti parziali ("card solo parziali" = bug da correggere). Se un elemento interno crea uno stacco bianco dentro una card, il riempimento va esteso/completato, non tolto.
2. **Righe delle tabelle (anche zebrate/alternate) e celle vuote: SEMPRE bianco puro `#FFFFFF`.** Mai giallo/crema su spazio vuoto o fuori da card/schemi (regola nata da: righe GENITIVO con fondo giallo = errore). **Eccezione v16:** solo `table.sinottica` ha l'intera riga tinta del caso (pastello + cella CASO piena) — richiesta esplicita dell'utente.
3. **Card della timeline (`.tl` PASSATO/PRESENTE/FUTURO dentro `.timeline`) uguali in larghezza** e insieme che coprono **tutta la larghezza** della striscia dello schema (v13: 32,6% ciascuna, `table-layout: fixed`) — nessuna card deve "assorbire" lo spazio vuoto lasciato dalle altre.
4. Paragrafi `text-align: left`; titoli/schemi/mappe centrati; corpo `14pt`; **numero di pagina centrato in grassetto, singolo**, senza footer di marca.
5. Tabelle e diagrammi **strettamente dentro i margini**; nessuno schema fuori margine.

### Storia versioni (direzione del gusto utente, in ordine)
- **v10** righe GENITIVO a fondo bianco (mai giallo su spazio vuoto)
- **v11** eliminati TUTTI i riempimenti chiari: bianco ovunque, colore solo su barre/chip/bordi/titoli
- **v12** righe tabelle bianche + riempimenti pastello ripristinati SOLO dentro card/schemi (card PASSATO-PRESENTE-FUTURO, box soft, tip, alert, paradigmi, soluzioni)
- **v13** card PASSATO/PRESENTE/FUTURO a larghezza uguale e continue su tutta la striscia dello schema
- **v14** rimossa l'area «COME SI CONSOLIDA TUTTO IL PERCORSO?» dalla mappa di sintesi + **prima immagine di copertina** (illustrazione piatta)
- **v15** immagine di copertina rigenerata in **stile clay/claymation** (richiesta esplicita dell'utente: l'illustrazione piatta non piaceva)
- **v16** tabella sinottica delle 5 declinazioni: **intera riga** colorata caso per caso (eccezione alla regola «tabelle bianche»; pastello sulle desinenze, cella CASO a tinta piena). Altre tabelle restano bianche.

## Pipeline di generazione

```bash
cd /home/user/quaderno-unico
python3 build_quaderno.py     # rigenera master-unico.html dai dati
python3 - <<'PY'
from weasyprint import HTML
HTML(filename='master-unico.html', base_url='.').write_pdf('quaderno-unico-v<NN>.pdf')
PY
```

In alternativa usare lo script della skill: `python3 /home/user/skills/didattica-documenti-accessibili/scripts/latino-facile-quaderno/rilascio_quaderno.py <NN>` (rigenera master + PDF + QA: pagine, md5, diff testo vs versione precedente, rect immagine copertina; NON sovrascrive un PDF esistente senza `--force`).

## Struttura contenuti

- **Pagine 1**: copertina (`section.cover`: banda rossa, titolo, sottotitoli, descrizione, legenda colori `.cover-chips` con `.chip`, immagine `.cover-img` in basso). L'indice occupa le pagine 2-5 (generato da `build_indice(gruppi)` con i numeri di pagina calcolati al volo).
- **Sezioni d'anno** (pagine ~6-121): contenuto da `/home/user/quaderno2/sezioni/`, con bande divisorie d'anno (`img/annoN.jpg`), tabelle di coniugazione, schemi, card.
- **Mappa di sintesi** = `section.part id="mappa-sintesi"` (da p. **123**): h1 + intro + aree `MAPPA_FINALE`. **p. 124** ospita le ultime aree. Attualmente **4 aree** (anni 1-4); l'area anno 5 «COME SI CONSOLIDA TUTTO IL PERCORSO?» è stata **rimossa in v14**.
- L'**indice elenca solo l'inizio della sezione** ("Mappa concettuale di sintesi … 123"), NON le singole aree: aggiungere/rimuovere un'area NON cambia l'indice finché la pagina d'inizio sezione non cambia.

### Rimuovere/aggiungere un'area della mappa finale
Ogni area = un dict in `MAPPA_FINALE` (in `quaderno_v7_contenuti.py`): `{anno, titolo, domanda, colore: "m-orange|m-blue|m-teal|m-green|m-red", box: [(titolo, descrizione), …]}`. Ogni area renderizza `<div class="m-area m-<colore>">` con `.m-band` (banda con `.m-q` = domanda in MAIUSCOLO) e `.m-boxes` (4 box: `.m-num` numerato + `.m-txt`). Esempio di rimozione (fatta in v14):

```python
# eliminare dalla lista MAPPA_FINALE l'ultimo dict, chiudendo la lista con "]"
# attenzione alle virgole: il dict che precede non deve terminare con virgola orfana
```

Poi rigenerare master e ricompilare; QA: il testo della pagina della mappa cambia, il numero di pagine può restare uguale (se la pagina ospita altre aree).

## Copertina: immagine (stile CLAY) e posizione

- Il markup vive in `master-unico.html` (riga ~29): `<img class="cover-img" src="img/copertina.jpg" alt="…"/>` **dopo** `.cover-chips` e **prima** di `</section>`.
- CSS in `style-accessibile.css` (~riga 115):
  ```css
  .cover-img { display: block; width: 15cm; margin: 22pt auto 0 auto;
               border: 2.5px solid #1a1a1a; border-radius: 16px; }
  ```
- Geometria A4 copertina (`.cover` height 29.7cm, padding 3.0cm top / 2.0cm bottom): il contenuto finisce a ~y785 pt; i chip colorati finiscono a ~y616; l'immagine deve stare in **y≈635-775**. Rect atteso su pagina 1: **x 86.9→508.4, y 634.8→770.8** (≈421×136 pt). Verificare sempre con pymupdf `get_image_rects` che non sbordi sotto ~y785 e che la pagina 2 resti l'indice.
- **Preparazione immagine**: generare in landscape, poi **center-crop a rapporto larghezza/altezza ≈ 3.1** (PIL) e salvare `img/copertina.jpg` (JPEG, niente alpha, quality 85-88, es. 2752×888 ≈ 265-280 KB).
- **Stile preferito dall'utente: clay/claymation** (plastilina, effetto stop-motion — MAI più illustrazione piatta/vettoriale). Soggetto collaudato: pergamena aperta al centro, calamo/penna, calamaio, due colonne classiche ai lati, ramo d'alloro con bacche; palette crema `#fdf8ef` con accenti rosso mattone `#b71c1c`, ambra, verde salvia, contorni grafite; **NESSUN testo/lettera/numero**; luce morbida; composizione orizzontale ampia. Prompt dettagliato in inglese, stile "clay animation stop-motion (Aardman/Laika), visible fingerprints, soft studio lighting".
- **Sempre ispezionare l'immagine generata con file_view** prima di incorporarla (lettere/scritte = da rigenerare). Tenere un backup (`img/copertina_v<NN>_backup.jpg`).

## Rilascio di una nuova versione (checklist completa, usata per v10→v15)

1. Modifiche ai sorgenti in `/home/user/quaderno-unico` (contenuti/CSS/immagini) e **ricompilazione** del PDF come `quaderno-unico-v<NN>.pdf` (build_quaderno.py + WeasyPrint, ~8 s).
2. **QA**: numero pagine (124), md5, **diff testo pagina-per-pagina vs versione precedente** → devono cambiare SOLO le pagine toccate; verificare l'indice (numeri pagina coerenti); render ad alta risoluzione (dpi 110-150) di copertina e pagine toccate e ispezione visiva con file_view (sfondi uniformi, niente card parziali, immagine copertina ok).
3. **Propagazione** nell'app:
   ```bash
   cd /home/user/latino-facile-app
   cp /home/user/quaderno-unico/quaderno-unico-v<NN>.pdf client/public/quaderno-unico-v<NN>.pdf
   cp /home/user/quaderno-unico/quaderno-unico-v<NN>.pdf dist/public/quaderno-unico-v<NN>.pdf
   ```
   - `client/src/pages/Home.tsx`: aggiornare `const PDF_LINK = "/quaderno-unico-v<NN>.pdf";` (~riga 43; `href={PDF_LINK}` ~riga 607).
   - Docs/manifest: sostituire la stringa `quaderno-unico-v<N-1>.pdf` → `quaderno-unico-v<NN>.pdf` in `README.md` (aggiornare anche "Il nome file è **versionato** (v<NN>)" e la riga "Contenuto attuale: **quaderno alta leggibilità v<NN>** (NN pp., …)" con descrizione delle novità), `REBUILD.md` (stessa riga contenuto), `ADATTARE.md`, `AGENTS.md`, `manifest.json`.
4. **Commit pulito** (`git add -A && git commit`) e `webdev_save_checkpoint` con descrizione significativa.
5. `webdev_deploy mode="preview"` → verificare `md5` del PDF servito: `curl -sL <preview>/quaderno-unico-v<NN>.pdf | md5sum` (deve corrispondere al locale).
6. **Produzione SOLO dopo conferma esplicita dell'utente**: `webdev_deploy mode="production"`. Verificare il checksum su **entrambi** gli URL produzione.
7. **L'app è una SPA**: il link al PDF sta nel **bundle JS** (`/assets/index-*.js`), NON nell'`index.html`. Per verificare la home: `curl -sL <url>/ | grep -o 'src="[^"]*\.js"'` → scaricare il bundle → `grep -o "quaderno-unico-v1[0-9]\.pdf"` (deve esserci solo v<NN>, nessun residuo v<N-1>).
8. **Rollout Cloud Run**: subito dopo il deploy il primo fetch può colpire un'istanza in fase di rollout → checksum NON corrispondente per qualche secondo (visto con v15: md5 diverso poi corretto). Riprovare con `sleep 8` fino a 5 volte. Per escludere Content-Encoding confrontare anche byte-size e md5 del file gzip-ato locale.
9. **ZIP esportabile** rigenerato dal commit HEAD (prefisso `latino-facile-app/`, commento = hash commit):
   ```python
   python3 - <<'PY'
   import zipfile, subprocess, os
   repo='/home/user/latino-facile-app'
   out=f'/home/user/latino-facile-app-export-aggiornato-v<NN>-<DATA>.zip'
   files=subprocess.run(['git','ls-files'],cwd=repo,capture_output=True,text=True).stdout.split()
   with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
       for f in files: z.write(os.path.join(repo,f), arcname='latino-facile-app/'+f)
       z.comment=subprocess.run(['git','rev-parse','HEAD'],cwd=repo,capture_output=True,text=True).stdout.strip().encode()
   PY
   ```
   Verificare: nessun residuo `quaderno-unico-v<N-1>` nei sorgenti (grep escluso node_modules/dist), PDF v<NN> presente nello ZIP.
10. Consegna finale: `send_attachment` con ZIP + PDF; mostrare il render della copertina in markdown.

## QA ricorrente (snippet pymupdf)

```python
import pymupdf, hashlib
d=pymupdf.open('quaderno-unico-v<NN>.pdf')
print('pagine:', len(d))
print('md5:', hashlib.md5(open('quaderno-unico-v<NN>.pdf','rb').read()).hexdigest())
# diff per-pagina vs versione precedente
# immagine di copertina su pagina 1:
print(d[0].get_image_rects(d[0].get_images(full=True)[0][0]))
d[0].get_pixmap(dpi=140).save('v<NN>_p001.png')
```

## Regole d'oro

1. Pastello SOLO dentro card/schemi e **sempre uniforme**; tabelle e spazi vuoti **bianco puro**.
2. Card timeline uguali e continue su tutta la striscia (mai card che assorbono il vuoto).
3. Ogni rilascio = **nuovo numero di versione** nel nome file e ovunque (Home.tsx, docs, manifest) — mai sovrascrivere la versione precedente.
4. Verifica SEMPRE con checksum md5 (locale = preview = produzione) e con diff testo per pagina.
5. Home SPA: verificare il **bundle JS**, non l'HTML; rollout Cloud Run può dare mismatch transitorio → retry.
6. Immagine copertina in **stile clay** finché l'utente non chiede altro; mai testo dentro l'immagine.
7. Checkpoint PRIMA del deploy produzione; produzione solo dopo conferma esplicita dell'utente.

## Risorse della skill

- `/home/user/skills/didattica-documenti-accessibili/scripts/latino-facile-quaderno/rilascio_quaderno.py` — rigenera master + compila `quaderno-unico-v<NN>.pdf` e stampa QA (pagine, md5, diff vs precedente, rect copertina). `QUADERNO_BASE` (env) per override percorso. Non sovrascrive versioni esistenti senza `--force`; `--no-master` per saltare `build_quaderno.py`.
