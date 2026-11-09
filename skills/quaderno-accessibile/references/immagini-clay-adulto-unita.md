# IMMAGINI CLAY ADULTE — REGOLA PERMANENTE DEL 1 NOVEMBRE 2026

Applicare alle guide, agli articoli e ai quaderni discorsivi del blog, nuovi o rimpaginati. Questa richiesta successiva prevale sulle vecchie istruzioni «conservare le immagini originali», «solo se nuove» e «non aggiungere immagini alle unità» quando impediscono di ottenere lo standard richiesto. Non alterare i modelli specialistici di esercizi, i grafici scientifici o i documenti per cui l’utente chiede esplicitamente altro.

## CHIARIMENTO PRIORITARIO — UNA IMMAGINE DOPO OGNI BANNER, NON SELEZIONE DI UNITÀ

Se l’utente chiede meno immagini, rimuovere le **seconde illustrazioni nella stessa unità**, non quelle di apertura. Rispettare SEMPRE **banner → UNA immagine clay adulta → sottotitolo e testo**, senza box o paragrafi fra titolo del banner e immagine. È errata la precedente interpretazione «illustrare solo cinque unità» o «spostare l’immagine dopo il primo testo»: non riapplicarla. Metodologie correnti **v13 IMMAGINE OGNI UNITÀ**, 29 pagine, copertina + dieci immagini di apertura (11 totali), nessuna seconda immagine. Riusare i dieci asset di apertura originali inclusi in `../templates/metodologie-v13/`, senza generarli di nuovo.

Preservare anche tutti gli inizi su pagina nuova delle dieci unità, delle mappe finali, delle fonti e dell’appendice; compattare solo entro l’unità. Non aggiungere per analogia immagini a mappa, bibliografia o appendice: per queste sezioni conservare il modello, nessuna figura nelle fonti. Grafici, formule, screenshot probatori o diagrammi necessari non sono illustrazioni decorative da cancellare automaticamente. Leggere `titoli-centrati-reflow-metodologie-v11.md` per baseline, CSS e manifest.

## COPERTURA E COLLOCAZIONE

- Inserire un’illustrazione **in copertina e all’inizio di ogni unità tematica**, non soltanto in apertura del documento. Escludere l’intera sezione **FONTI E RIFERIMENTI** e le sue sottosezioni: nessuna immagine lì.
- Identificare prima le unità reali (capitoli, strategie, sottounità tematiche autonome); non confonderle con ogni paragrafo, box o semplice incipit in neretto. Compilare un manifest di unità, lingua, soggetto, file e alt. Se un articolo è bilingue, coprire tutte le unità in entrambe le lingue e riusare la stessa scena per le unità corrispondenti.
- Rispettare la sequenza **titolo nel banner → UNA immagine → sottotitolo e primo blocco di testo**, senza sottotitoli o testo prima dell’immagine. Niente titolo o didascalia ripetuti sotto l’immagine. Tenere insieme i tre elementi, senza imporre una nuova pagina a ogni unità se non richiesto.
- Mantenere il testo originale integralmente, enfasi, ordine, raggruppamenti, fonti e voci dell’indice. Il reflow e la crescita del numero di pagine sono conseguenze legittime; aggiornare automaticamente numeri e link dell’indice.

## STILE NON FACOLTATIVO

- Usare **sempre clay adulto** per le illustrazioni editoriali, comprese le immagini ereditate da un allegato: miniature tridimensionali in plastilina opaca, texture tattile, proporzioni mature, espressioni misurate, luce morbida e palette sobria coordinata.
- Non mantenere immagini flat/vettoriali, clipart, chibi, occhi/teste enormi o figure infantili soltanto perché si trovano nel Word originale. La regola di conservazione riguarda il testo; le illustrazioni fuori standard devono essere sostituite/rivisitate. Conservare la fonte originale intatta in una cartella distinta.
- Adattare età e soggetti al contenuto: per liceo, adolescenti e adulti; non trasformare in adulti bambini che il contenuto richiede realmente. Preservare correttezza, rispetto e pertinenza della scena. Non illustrare una punizione in modo umiliante per il solo titolo di una strategia.
- Non trasformare dati, formule, grafici, documenti probatori o screenshot in scene inventate; questa regola riguarda le illustrazioni editoriali. Separare fonti documentali e apparato illustrativo.

## UNIFORMITÀ VISIBILE

- Impostare **la stessa larghezza E altezza fisica** su tutte le illustrazioni, copertina compresa. Riferimento comune: riquadro 112×63,25mm, `object-fit:contain` e asset landscape con rapporto coerente.
- Controllare anche l’ingombro effettivo nel PDF, non solo il contenitore: due originali con rapporti diversi possono riempire la stessa scatola in modo differente. Non conservare questa eccezione per salvare immagini flat; sostituirle con asset clay coordinati.
- Non stirare i personaggi, ritagliare teste/mani o ridurre una sola immagine per conservare il vecchio numero di pagine. Nel Word usare larghezza comune e rapporto intrinseco, con immagini coerenti; controllare la conversione PDF.
- Aggiungere alt corrispondenti alla scena effettiva e **nella lingua dell’unità**, non etichette del vecchio asset. Preferire immagini senza scritte: titoli e spiegazioni restano testo accessibile fuori dalle figure.

## ASSET, GENERAZIONE E COSTI EVITABILI

1. Cercare prima scene clay già approvate e semanticamente pertinenti. Leggere `templates/clay-adulto/manifest.json`: sono inclusi sei asset riusabili della serie classe serena. Non usare il percorso di un progetto precedente come unica risorsa portabile.
2. Riusare la stessa scena per lo stesso tema in lingue diverse quando utile. **Nella mappa finale scegliere scene diverse e semanticamente utili per concetti diversi**, evitando di ripetere ovunque un asset generico; non imporre unicità meccanica a occorrenze del medesimo concetto. Leggere `revisione-shakespeare-box-mappe-fonti-2026-11-03.md` e usare le scene incluse quando pertinenti.
3. Se manca una scena, leggere `image-generation` e generarla/editare con gli strumenti media, usando una scena della serie come riferimento. Non usare Python per disegnare o restilizzare immagini. Non cercare fotografie reali quando è esplicitamente richiesta un’illustrazione clay.
4. Verificare una volta stile, soggetto reale, scritte e artefatti macroscopici. Dita tozze o superfici modellate non sono automaticamente errori in una figura di plastilina; distinguere stilizzazione da arti extra, fusioni estreme o parti mancanti.
5. **Non rigenerare un risultato riuscito.** Se c’è un errore reale, mostrarlo, spiegarlo e chiedere prima di spendere per una correzione. Non sostituire un asset approvato durante una revisione che non riguarda le immagini.

## VERIFICHE RIPRODUCIBILI

Contrassegnare i titoli delle unità con `data-editorial-unit="ID"`; mantenere gli id univoci. Posizionare l’immagine come sibling immediato del titolo (eventualmente in un wrapper `.unit-opening` con il primo box). Eseguire:

```bash
python3 scripts/verifica_copertura_immagini_unita.py documento.html --report copertura.json --strict
python3 scripts/verifica_immagini_indice.py documento.html --pdf documento.pdf --report immagini.json --strict
python3 scripts/verifica_box_semantici.py documento.html --report box.json --strict
```

Eseguire sempre il controllo della copertura completa nelle metodologie; «meno immagini» non autorizza un manifest selettivo. Aggiungere `scripts/verifica_aperture_unita.py HTML --manifest templates/metodologie-v13/aspettative-aperture.json --report aperture.json --strict` per rilevare sia immagini mancanti sia seconde immagini e collocazioni dopo il testo. Il primo controllo verifica copertina, copertura delle unità, alt, file esistenti ed esclusione fonti. Il secondo misura riquadri, ingombri PDF, indice e colori. **Nessuno dei due riconosce automaticamente lo stile clay**: ispezionare visivamente tutte le scene uniche e le pagine definitive. Confrontare testo ed enfasi con la base, verificare font incorporati e controllare il Word convertito. Non dichiarare conformità PDF/UA soltanto perché il renderer applica tag.

## CASI DA NON RIPETERE

- **Regole di classe:** la prima rimpaginazione conservava due JPEG flat e descrizioni alt scambiate. Edizione corretta `REGOLE_DI_CLASSE_CLAY_ADULTO_v2`: cinque pagine, 24 paragrafi invariati, tre occorrenze di due scene clay adulte (copertina inclusa), fonti prive di immagini. Non tornare all’edizione flat.
- **Come gestire una classe che disturba — originale e traduzione:** la prima raccolta di 27 pagine aveva solo la copertina illustrata. Edizione corretta `COME_GESTIRE_UNA_CLASSE_CHE_DISTURBA_CLAY_ADULTO_v2`: 43 pagine, 149 paragrafi invariati; copertina più 46 aperture (due parti linguistiche e 44 unità/sottounità), sei scene coordinate, nessuna figura nelle fonti. Quantità e pagine sono dati di questo caso, non quote per gli altri documenti.
- Consegnare PDF, Word se previsto e sorgenti aggiornati, senza lasciare vecchi asset flat o note false «illustrazioni originali conservate» nello ZIP. Aggiornare solo l’eventuale nota di provenienza delle immagini, dichiarando questa minima modifica verbale. Non rigenerare l’audio per una sola correzione grafica.

