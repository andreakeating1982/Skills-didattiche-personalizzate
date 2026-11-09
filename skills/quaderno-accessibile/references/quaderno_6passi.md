# Variante del quaderno «Come costruire una mappa concettuale in 6 passi» con un argomento diverso

Leggi questo file quando devi **ricreare un documento IDENTICO** al quaderno PDF/UA-1 «Come costruire una mappa concettuale in 6 passi» (8 pagine, una sezione per pagina) cambiando **solo l'argomento didattico** (es. l'esempio di studio passa dalla fotosintesi ai vulcani, all'acqua, a un testo narrativo…). Vale anche se l'utente chiede di cambiare i testi dei passi mantenendo lo stesso modello di quaderno.

## 1. Sorgente canonica e regola d'oro

- Sorgente (finale, validato dall'utente): `/home/user/mappa_build/mappa_accessibile.html` + cartella `/home/user/mappa_build/media/` con `orig-p1-0.png` (cover) e `p1.png`…`p6.png` (sezioni 1–6). PDF di riferimento: `/home/user/mappa_build/Mappa_Concettuale_6_passi_quaderno_accessibile.pdf`.
- **Regola d'oro: NON modificare MAI il CSS né la struttura delle sezioni** (palette, card crema, icone ✔, indice, box IN SINTESI, mappa finale, paginazione). Per un "documento uguale con argomento diverso" si cambiano **SOLO testi e immagini**, mai le regole di stile: il CSS è già calibrato e ogni ritocco sposta l'impaginazione (8 pagine, niente pagine quasi vuote).
- Copia il sorgente in una cartella di lavoro nuova, es. `/home/user/<slug>_build/` (html + `media/`), quindi edita la copia. Script di render e verifica: `/home/user/skills/quaderno-accessibile/scripts/render_quaderno.py` e `verify_quaderno.py`.
- Backup: se `/home/user/mappa_build/` non esiste (sandbox ripulita), usa `templates/quaderno_6passi.html` (struttura + CSS finale identici, senza immagini) e ricava le 7 immagini estraendole dal PDF consegnato (PyMuPDF, vedi guida §5) oppure rigenerandole in stile claymation coi criteri della sezione 4; in alternativa chiedi all'utente di ri-allegare il PDF.

## 2. Anatomia fissa del documento (non cambiarla)

1. **Pagina 1 — copertina + indice**: `h1.title-banner` viola (titolo metodo), immagine cover `orig-p1-0.png` albero-metafora (~92%), banner navy `INDICE`, `div.indwrap` crema con tabella indice a 7 voci (cerchi numerati colorati `ind1`…`ind6` + `★` per la mappa, **senza riga di intestazione**, pagina 1 senza numero di pagina).
2. **Pagina 2**: card crema `div.blk.intro-blk` (paragrafo introduttivo, **senza immagine**, `page-break-before: always`) → banner rosso sezione 1 → card `.blk` (immagine + elenco ✔) → box `IN SINTESI · 1`. Nota: `#sec1 { page-break-before: auto; }`: la sezione 1 NON inizia a pagina nuova, scorre dopo la card introduttiva.
3. **Pagine 3–7 — sezioni 2–6**, ognuna a pagina nuova (`#sec2`…`#sec6` con `page-break-before: always`): banner colorato con cerchio numerato → card `.blk` (immagine + elenco con spunte ✔) → box `IN SINTESI · N`.
4. **Pagina 8 — mappa finale**: `#mappa { page-break-before: always; }`, banner navy `LA MAPPA IN SINTESI`, `div.map-root` navy, due `div.map-group` crema (`PRIMA · LEGGERE E CAPIRE (PASSI 1–3)` e `POI · COSTRUIRE LA MAPPA (PASSI 4–6)`) con 3 nodi `.m-node.w3` ciascuno (bordo superiore e cerchio `m-num` del colore del passo). **Non ci sono** paragrafo introduttivo né legenda "💡 Suggerimento" (rimossi per volontà dell'utente: non reintrodurli).

Palette sezioni: 1 rosso `#b3261e`, 2 blu `#1a5fb4`, 3 verde `#2e7d32`, 4 arancio `#a35400`, 5 viola `#5e35b1`, 6 acquamarina `#0e7c66`; navy `#1f3864` (INDICE, LA MAPPA IN SINTESI, map-root); titolo di copertina viola `#5e35b1`. Card e box: sfondo crema `#fffaf0`, bordo `#e6d5ae`, angoli 14px. Testo corpo `#111111`, OpenDyslexic, giustificato.

Standard grafici validati (da preservare):
- **Parole chiave sempre in GRASSETTO NERO** (`<span class="k|m|f|o|p">`, CSS: `.k,.m,.f,.o,.p { color:#111111; font-weight:700; }`): concetti chiave `k`, hashtag/parole da ricordare `m`, azioni/fasi `f`, esempi `o`, parole importanti `p`. Nessun colore sul testo delle parole chiave (richiesta esplicita dell'utente, come nel quaderno «10 metodologie»).
- Colori riservati a elementi grafici: spunte ✔ e frecce ➜ degli elenchi (colorate per sezione via `#secN ul.bx li::before`), cerchi numerati, banner, etichette dei box IN SINTESI, bordo del box sintesi (inline `style="border-color:…"`).
- Elenchi nelle card: `ul.bx` (✔) / `ul.ax` (➜), `padding-left:0` sul `ul`, voci con `padding-left:26px; text-indent:-26px` (rientro sospeso: le righe a capo si allineano all'inizio del testo, mai sotto l'icona), font 14pt, interlinea 1.5.
- Immagini delle card: larghezze gestite dal CSS (`img.ilust` in `.blk` = 56%; `#sec1` = 44%; `#sec2` = 50%; cover 92%): non cambiare larghezze/`margin` nell'HTML.
- Pagina 2 è la più piena: il box IN SINTESI · 1 arriva ~752/790 pt senza sforare. Geometrie di riferimento: card da x≈51 a ≈544 pt; spunta a ≈62.6 pt (≈11.6 pt dal bordo card); testo a capo a ≈82 pt.

## 3. Parametrizzazione per argomento

Il sorgente usa come esempio didattico ricorrente **la fotosintesi** (un "brano di studio" di scienze). Per un nuovo argomento X sostituisci **tutte** le occorrenze legate all'argomento in modo coerente (stesso brano di studio per tutto il quaderno). Comando utile: `grep -n 'fotosintesi\|foglie sono di colore verde' <file>.html`.

Occorrenze da sostituire (cerca per stringa, non per numero di riga):

| Dove | Testo attuale (fotosintesi) | Cosa scrivere per il nuovo argomento |
|---|---|---|
| Card sez. 1, bullet «Per esempio» | `«<span class="o">Questo brano spiega perché le foglie sono di colore verde</span>»` | Una sola frase che riassume il nuovo brano studiato, es. «Questo brano spiega come nascono i vulcani». |
| Box IN SINTESI · 1, riga «Esempio» | `«Questo brano spiega perché le foglie sono di colore verde».` | La **stessa** frase dell'esempio della card (devono combaciare). |
| Card sez. 3, bullet «Per esempio, se studi…» | `Per esempio, se studi la fotosintesi, scrivi <span class="m">#fotosintesi</span>, <span class="m">#piante</span> e <span class="m">#luce</span>.` | `Per esempio, se studi <argomento>, scrivi <span class="m">#hashtag1</span>, <span class="m">#hashtag2</span> e <span class="m">#hashtag3</span>.` |
| Box IN SINTESI · 3, riga «Che cosa fai» | `Trasforma ogni idea importante in un <span class="m">hashtag</span>: per esempio <span class="m">#fotosintesi</span>, <span class="m">#piante</span> e <span class="m">#luce</span>.` | Stessi 3 hashtag del nuovo argomento. |
| Immagine `media/p3.png` + relativo `alt` (card sez. 3) | Etichette di plastilina con `#fotosintesi #piante #luce` | Rigenerare l'immagine con i **3 nuovi hashtag** e riscrivere l'`alt` di conseguenza. |

Altri testi (intro di pagina 2, istruzioni dei passi, «Risultato», mappa finale, ecc.) sono **generici sul metodo** e restano invariati: riguardano "come si costruisce una mappa concettuale", non l'argomento di esempio. Se l'utente chiede un contenuto diverso **anche nel metodo** (nuovi titoli dei 6 passi, nuove istruzioni), usa la stessa struttura ma riscrivi: `h1.title-banner`, le 7 voci dell'indice (testo + `href`), i 6 `h2.banner`, i bullet delle card (4–5 per card, con gli span `f/k/o/m`), le righe dei box IN SINTESI (2–3 righe), i nodi della mappa finale (`.t` maiuscolo breve + `.m-idea` di ~1 riga). Mantieni volumi di testo simili all'originale per conservare le 8 pagine senza pagine quasi vuote né sforamenti.

## 4. Immagini

7 immagini stile claymation/plastilina (orizzontali): `orig-p1-0.png` (albero-metafora della mappa, cover), `p1`…`p6` (una per sezione: studente che ripete; appunti a lato; quaderno con etichette hashtag; cerchio «IL TITOLO»; mappa con rami; mappa completa con QR). Regole:
- Per il nuovo argomento rigenera con `media_generate_from_images` **usando l'immagine originale come riferimento** (stile identico) almeno le immagini che mostrano contenuti dell'argomento (minimo: `p3.png` con i nuovi hashtag; se l'esempio è illustrato anche in `p1.png`, rigenera anche quella).
- Le altre immagini del metodo si possono tenere; se l'utente vuole un set completamente nuovo, rigenerale **tutte** sempre dai riferimenti originali (mai da prompt senza riferimento: cambierebbe lo stile).
- Aggiorna **sempre** l'`alt` (in italiano, descrittivo, coerente con la nuova immagine) e salva i file nella stessa cartella `media/` mantenendo gli stessi nomi o aggiornando gli `src`.

## 5. Workflow

1. `cp -r /home/user/mappa_build /home/user/<slug>_build` (o copia html + `media/`), poi lavora sulla copia.
2. Sostituisci i contenuti-argomento (sezione 3) e, se richiesto, testi del metodo (sezione 3 ultimo capoverso) e immagini (sezione 4).
3. Rendi il PDF: `python /home/user/skills/quaderno-accessibile/scripts/render_quaderno.py <slug>_accessibile.html <Nome>_quaderno_accessibile.pdf`.
4. Verifica: `python /home/user/skills/quaderno-accessibile/scripts/verify_quaderno.py <file>.pdf --secs "LEGGI E RIPETI CON LA TUA VOCE|RILEGGI E PRENDI APPUNTI|CREA GLI HASHTAG|DISEGNA IL TRONCO|AGGIUNGI I RAMI|COMPLETA CON LE FOGLIE|LA MAPPA IN SINTESI"`. Obiettivi: 8 pagine; inizio sezioni a pagina 2–8; **nessuna pagina quasi vuota**; riempimenti massimi ~752/790 (pag. 2); `Marked: True`, `Lang: it`, 9 segnalibri; numeri di pagina dalla 2 in poi, assenti in copertina.
5. Anteprime `pdftoppm -png -r 140 <file>.pdf sv` e controllo visivo con `file_view` su: copertina, pagina 2, una pagina con hashtag (sez. 3), pagina 8 (mappa).
6. Se una pagina sfora o resta quasi vuota: ritocca **solo i volumi di testo** (accorcia/allunga frasi della sezione interessata) oppure, in ultima istanza, le regole per-sezione già esistenti in coda al blocco elenchi (`#sec1 .blk img.ilust { width: 44%; }` / `#sec2 … 50%`): non modificare i valori base condivisi.
7. Consegna con `send_attachment` (PDF, nome `<Nome>_quaderno_accessibile.pdf`), messaggio breve in italiano.

## 6. Checklist finale

- [ ] Copia del sorgente; CSS e struttura NON modificati
- [ ] Tutte le occorrenze "fotosintesi" sostituite in modo coerente (card + IN SINTESI sez. 1 e 3)
- [ ] 3 hashtag nuovi e identici in card, IN SINTESI · 3 e immagine `p3.png` (+ `alt`)
- [ ] Parole chiave in grassetto nero con span `k/m/f/o/p`; colori solo su icone/banner/etichette
- [ ] Assenti «💡 Suggerimento…» e «Dalla lettura al foglio…»
- [ ] 8 pagine, sezioni 2–8, nessuna pagina quasi vuota, PDF/UA-1 (`Marked`, `Lang: it`, 9 segnalibri), numeri di pagina da pag. 2
- [ ] Controllo visivo con `file_view`
- [ ] PDF consegnato con `send_attachment`
