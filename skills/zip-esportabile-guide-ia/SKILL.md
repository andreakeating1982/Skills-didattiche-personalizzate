---
name: zip-esportabile-guide-ia
description: "Pattern riutilizzabile per creare o aggiornare il PACCHETTO ZIP ESPORTABILE di app generate su Easy-Peasy AI (scaffold web-db-user o web-static), pronto per agenti IA e/o GitHub. Requisiti: (1) l'IA deve poter RICOSTRUIRE l'app identica dal repository GitHub (REBUILD.md) e creare VARIANTI (ADATTARE.md): grado equazione diverso, disequazioni di qualunque grado, equazioni/disequazioni fratte, altra lingua straniera (inglese/spagnolo/francese), o nuovo set di domande (contenuto, numero e tipologia: VERO/FALSO, risposta multipla 3-4 opzioni, risposta breve); (2) trasferire l'app da Easy-Peasy AI a Render via GitHub (RENDER.md); (3) sezione ACCESSIBILITA' ben segnalata (ACCESSIBILITA.md) con misure riusabili (font OpenDyslexic ecc.) su altre app simili. Includere anche AGENTS.md. NON usare per modificare il codice di una singola app: usare la skill di manutenzione specifica di quell'app."
---

# ZIP Esportabile con Guide per l'IA

## ARCHIVI DI SKILL E DOCUMENTI — SINCRONIZZARE LE REVISIONI

**Ritiro successivo del codice 05 (2 novembre 2026):** leggere [l’esclusione corrente](../quaderno-accessibile/references/documento-ritirato-2026-11-02.md). Il nuovo ZIP esplicitamente richiesto include le skill correnti e tutte le loro risorse, ma non il documento ritirato né percorsi di recupero o record attivi che lo reinseriscano. La raccolta di articoli è ora di otto; questo non riduce il numero delle skill. Verificare esclusione, catalogo, hash e test anche dopo estrazione in una cartella nuova. Non modificare i messaggi o dichiarare cancellati gli allegati già pubblicati in chat.

**Aggiornamento articoli del2novembre2026:** nei futuri archivi richiesti includere anche `quaderno-accessibile/references/articoli-scientifici-quiz.md`, il verificatore/schema e i test: riscrittura scientifica accessibile senza rimandi al video del blog, quiz medio5–10domande/4opzioni prima della mappa, RIFERIMENTI BIBLIOGRAFICI senza FONTE e firma ANDREA CENTINARO. Conservare lo standard Regular400 delle sintesi e mappe78mm. L’utente che richiede di aggiornare le skill e ricevere **solo il PDF** non sta chiedendo un nuovo ZIP né skill scaricabili: aggiornare internamente, non allegare pacchetti e non modificare archivi già consegnati.

Se si aggiorna una raccolta di skill anziché una app, usare la cartella del repository esportato come sorgente: includere SKILL.md, script, riferimenti, modelli, catalogo e AGENTS aggiornati; non pretendere un deploy o inventare sorgenti delle app esterne. Per le guide didattiche rispettare **IN SINTESI in tabella a due colonne con tutte le righe necessarie e MAI GRASSETTO, neppure in etichetta/intestazioni/chiavi/celle (OpenDyslexic Regular, peso400); MAPPA CONCETTUALE FINALE (titolo esatto) con tutti i box78×78mm uniformi, solo poche PAROLE CHIAVE, immagini clay interne52×29,373mm, due colonne e ultimo nodo centrato senza allargarlo, senza connettori né fasce a tutta larghezza; interlinea1,85 e dimensione del corpo per entrambi**, secondo [lo standard aggiornato](../quaderno-accessibile/references/sintesi-e-mappa-finale.md). Registrare l’approvazione del modello Realtà Virtuale v6 (2novembre2026) e il divieto di Bold nelle sintesi, mantenendo i neretti del corpo e delle mappe approvate. Se viene richiesto un NUOVO ZIP, ricopiare le skill correnti e le risorse effettivamente aggiornate (non riusare solo la copia di un vecchio pacchetto), adattare guide radice/catalogo, rigenerare manifest e report, estrarre lo ZIP in una cartella nuova e ripetere i test offline, inclusi peso400 delle sintesi, misure78mm e parole chiave. Il semplice aggiornamento delle skill non autorizza la ricostruzione di ZIP/PDF; i pacchetti già consegnati non si aggiornano da soli. Non riutilizzare un vecchio rapporto di verifica come prova della nuova versione. Se si consegna anche un archivio dei PDF, selezionare soltanto l’ultima edizione di ogni documento dal registro verificato, con sorgenti riproducibili e relativi controlli: non includere PDF intermedi/superati. Nessuna pubblicazione GitHub o generazione audio automatica è autorizzata da una richiesta di ZIP.

## Quando usare questa skill

Usala quando l'utente chiede: pacchetto ZIP esportabile, ZIP per GitHub/Render, guide per l'IA (`REBUILD.md`, `ADATTARE.md`, `RENDER.md`, `ACCESSIBILITA.md`, `AGENTS.md`), pacchetto con sezione accessibilità ben segnalata, trasferimento da Easy-Peasy AI a Render tramite repository GitHub, o aggiornamento di un pacchetto già consegnato dopo modifiche all'app.

Il pacchetto si costruisce SEMPRE a partire dal repository dell'app in sandbox (es. `/home/user/cornice-universale`). Non inventare contenuti: leggi i sorgenti e i documenti esistenti dell'app e allineali al pattern qui sotto.

## Stato corrente del caso Widget Metacognitivo — produzione8756

Per lo ZIP attuale leggere prima
[export8756](references/espressioni-8756.md), che supera i limiti e gli hash
8744 sotto: pagina2 a640px e pagina3 adattiva fino a640px con scroll interno.
Conservare i wrapper e il selettore `expr-exercise-scroll`; non chiamarlo
`expr-exercise-page` per collisione con font storici. Validare il definitivo
con il verificatore8756 del progetto o della skill pubblicazione, non con
quello8744. Manifest e rapporto esterno devono identificare il nuovo archivio.
L'esportazione non cambia runtime e non autorizza un deploy.

## Cronologia del pattern — 28/10/2026

Per ZIP con segreti server, manifest/hash e **photo cropper mobile/iframe**, leggere
[references/export-sicuro-cropper.md](references/export-sicuro-cropper.md).
Usare `scripts/export_verified.py` per esportare file tracciati con scansione
credenziali e manifest; non basta `git archive` per garantire la sicurezza.
Non cambiare codice funzionale per preparare uno ZIP. Conservare modello ONNX,
WASM/Tesseract, font, PDF pubblici, lockfile e patches; non copiare `.env`,
`shared/env.generated.ts` o `dist` (server con chiave incorporata).
Ricostruire da nuova estrazione, confrontare il build CLIENT approvato;
non richiedere identità del bundle server con la chiave di produzione.
I dialoghi mobile hanno contratti diversi: il cropper 8731 usa `modal=true`,
viewport hook + CSS + guardia heightSync, NON il vecchio `modal=false`.

### Cronologia: scrollbar, header e overflow — produzione8744

Per il widget con scrollbar interna stile Latino Facile, preservare nel
pacchetto wrapper App, classi CSS, contratto heightSync unico e regola
`piece-display` per le rese KaTeX. Leggere il riferimento
`seconda-pagina-8737.md` della skill manutenzione (stato 8744). Includere
`SECONDA-PAGINA-SCROLL.md`, test E2E, istruzioni e risultati. Dopo un
deploy autorizzato aggiornare le guide al nuovo ID e ai nuovi hash senza
ripubblicare: confrontare il client con gli hash 8744
(`index-BnuQEBUp.js`), NON con 8742/8737/8736. Distinguere 738 test
unitari dalle prove browser. Se il sito serve ancora gli asset vecchi
subito dopo il deploy (propagazione), ricontrollare dopo attesa prima di
dichiarare riuscita la verifica online; i tentativi falliti («14
UNAVAILABLE») vanno riprovati dopo attesa e annotati nel rapporto.

### Header e pezzi della pagina 2 (8742/8744, da foto utente)

Nella pagina 2 NON reintrodurre titolo dell'app né riga dati studente
(rimossi su richiesta; restano in prima pagina e nel PDF). Il pulsante home
è il piccolo bottone marrone **INDIETRO** (token primary, text-xs,
aria-label «Torna alla pagina iniziale»), sempre visibile. Didascalia SOLO
«SCRIVI QUI L'ESPRESSIONE» in grassetto scuro. Ogni resa KaTeX (pezzi,
trascrizione, conferma) va in un contenitore `piece-display` con
scorrimento interno, mai fuori dai bordi; i pezzi corti restano centrati.
Quando aggiorni ZIP/skill dopo queste rifiniture, annota che il titolo e i
dati restano richiesti in prima pagina e nel PDF generato.

## Requisito utente (riassunto operativo)

Il pacchetto ZIP aggiornato deve essere **funzionale a un'intelligenza artificiale** per:

1. **Ricostruire la stessa app** partendo dalla repository GitHub dell'app.
2. **Creare varianti della stessa app** cambiando solo contenuti/configurazione, ad esempio:
   - matematica: grado dell'equazione diverso, trasformazione in disequazioni di qualunque grado, equazioni e disequazioni fratte di qualunque grado;
   - lingua straniera: nuova app per lo studio dell'inglese, dello spagnolo o del francese;
   - quiz: set di domande diverso (contenuto), numero di domande diverso, tipologia diversa (VERO/FALSO, risposta multipla a 3 o 4 opzioni, risposta breve).
3. **Trasferire l'app da Easy-Peasy AI a Render** mediante repository su GitHub.
4. Avere **ben segnalata la sezione ACCESSIBILITA'** con tutte le misure (font OpenDyslexic, ecc.) facilmente implementabili su altre app simili via repository GitHub.

## Struttura obbligatoria del pacchetto

Alla radice del repository/ZIP devono esserci questi file (oltre ai sorgenti completi):

| File | Scopo | Contenuti minimi |
|---|---|---|
| `README.md` | Panoramica per umani e IA | contesto, funzionalità, avvio locale, deploy Render, embed, indice delle guide |
| `REBUILD.md` | Ricostruire l'app IDENTICA dal repo | comandi esatti (`corepack enable && pnpm install --frozen-lockfile && pnpm check && pnpm build && pnpm start`), contratto di verifica, invarianti, struttura, test di ricostruzione |
| `ADATTARE.md` | Creare VARIANTI cambiando solo contenuti | scenari per famiglia di app (vedi sotto) + checklist finale |
| `RENDER.md` | Trasferimento Easy-Peasy → GitHub → Render | passo 1 repo GitHub, passo 2 Blueprint (`render.yaml`), passo 3 manuale, troubleshooting, aggiornamento embed |
| `ACCESSIBILITA.md` | SEZIONE ACCESSIBILITÀ ben segnalata | misure con tabella "Dove nel codice" + guida al riuso su altre app + checklist di verifica |
| `AGENTS.md` | Regole per agenti IA che lavorano nel repo | mappa dei file, comandi, invarianti assoluti, flusso di lavoro |
| `FILOSOFIA-DSA.md` | (app DSA) Filosofia dell'app CLONABILE dall'IA | principi invariabili (mai la soluzione, frazioni impilate, feedback rosso fisso, l'IA propone il motere dispone…), tabella regola→implementazione→test, checklist di clonazione, prompt di clonazione pronto da incollare |
| `render.yaml` | Deploy Render | `runtime: node` (o static solo se l'app è davvero statica), build/start, `NODE_VERSION`, health check |
| `package.json`, `pnpm-lock.yaml`, `patches/` | Install riproducibile | NON eliminare lockfile né patches |

**Da escludere sempre dallo ZIP**: `node_modules/`, `dist/`, `.git/`, `data/` (file di stato runtime), file diagnostici (`diag_*.mjs`, `template.json`), log (`dev-server.log`), `.DS_Store`. Escludere anche ogni artefatto di funzionalità rimosse (es. pagine `embed.html` di cornici dinamiche) e ogni riferimento nel codice/doc.

## Linee guida per scrivere le guide (per un'agente IA)

Scrivi le guide in italiano, in forma imperativa, con comandi esatti e checklist spuntabili. Ogni guida deve poter essere eseguita da un agente IA senza altra documentazione.

- `REBUILD.md`: inizia con "Ricostruire questa identica app". Includi prerequisiti (Node 22), comandi, cosa deve essere vero alla fine (check/build/API/UI), la mappa dei file essenziali, gli invarianti da non modificare (password su due file se presente, niente emoji, palette, font, ARIA), e la verifica tramite hash degli asset (`dist/public/assets/index-*.js`).
- `ADATTARE.md`: per ogni famiglia di app documenta gli scenari di variazione. Regola d'oro: **mai riscrivere l'architettura; sostituire solo contenuti/stringhe/configurazione**, poi ricostruire e verificare.
- `RENDER.md`: repo pubblico su GitHub (necessario per il free tier), Blueprint che legge `render.yaml`, alternativa Web Service manuale (Runtime Node), troubleshooting frequente (lockfile mancante, `corepack enable`, deploy statico al posto di node, free tier sleep), aggiornamento dell'iframe embed.
- `ACCESSIBILITA.md`: deve avere un titolo esplicito, una tabella "Sommario delle misure" con colonne `# / Misura / Area / Dove nel codice / Beneficio`, la sezione "Come implementare queste misure su altre app simili (guida al riuso via GitHub)" e una "Checklist di verifica". Misure tipiche riusabili: font OpenDyslexic auto-ospitato, modello di preferenze in `localStorage`, pannello regolazioni, contrasto, TTS, screen reader/ARIA, niente emoji, messaggi chiari, focus gestito.
- `AGENTS.md`: mappa dei file, comandi, invarianti assoluti (le stesse regole d'oro dell'app), flusso di lavoro, cosa deve contenere il pacchetto prima della consegna.

## Catalogo variazioni per famiglia di app (contenuto di ADATTARE.md)

1. **App matematiche (equazioni → disequazioni → fratte)** — es. widget equazioni con sostituzione `t = x^k`: la variante cambia il grado (2, 4, 6, 8...), oppure trasforma le equazioni in disequazioni (studio del segno), oppure passa a equazioni/disequazioni fratte di qualunque grado. Cambiano SOLO la mappa grado/tipo nel generatore dei passi e i testi; UI, input scrittura e PDF invariati. Documentare dove vive la mappa del grado nel codice.
2. **App per lingue straniere (inglese, spagnolo, francese)** — cambia il contenuto linguistico e, se richiesto, la localizzazione dell'interfaccia; architettura, OCR/analisi e report invariati. Documentare dove stanno le stringhe UI e come si cambia la lingua del contenuto.
3. **Quiz e attività a schema** — cambia SOLO il set di domande: contenuto diverso, numero di domande diverso, tipologia diversa (VERO/FALSO, risposta multipla a 3 o 4 opzioni, risposta breve). Dashboard docente, codici classe, sessioni, contatore studenti, report PDF e aspetto invariati. Documentare il formato del set di domande (JSON/sorgente) e come si rigenera.

## Come costruire/aggiornare il pacchetto

1. Identifica il progetto in sandbox (es. `/home/user/<app>`) e leggi `README.md` e `package.json` per contesto e script.
2. Verifica quali guide esistono già e quali mancano; allinea i contenuti allo stato ATTUALE del codice (non a versioni passate).
3. Se un file di guida esiste già, aggiornalo con `file_edit` mirato invece di riscriverlo.
4. Aggiungi/aggiorna l'indice delle guide nel `README.md` (tabella delle guide + struttura del progetto).
5. Rigenera lo ZIP con lo **script verificato**, dopo checkpoint e Git pulito:
   ```sh
   python3.11 /home/user/skills/zip-esportabile-guide-ia/scripts/export_verified.py \
     --project /home/user/<app> --output /home/user/<app>.zip \
     --prefix <app> --deployment <ID-PUBBLICATO>
   ```
   Lo script controlla file tracciati, credenziali, percorsi, CRC e manifest.
   Il vecchio comando tar/zip non escludeva tutti i file riservati ed è
   RIMOSSO: non riutilizzarlo. Non applicare lo script a un'altra famiglia
   senza verificarne i file obbligatori e i contratti specifici.
6. **Testa la ricostruzione da zero** prima di consegnare: estrai lo ZIP in una cartella vuota (`/home/user/recon-<app>`), esegui `corepack enable && pnpm install --frozen-lockfile && pnpm check && pnpm build`, poi confronta l'hash dell'asset JS con quello del progetto sorgente (uguale = ricostruzione fedele).
7. Controlla il contenuto dello ZIP (`unzip -l`) per verificare inclusi/esclusi e presenza delle guide.
8. Consegnare con `send_attachment` il file ZIP (`/home/user/<app>.zip`).

## Accessibilità: requisito trasversale

Prima di chiudere il pacchetto verifica che `ACCESSIBILITA.md`:
- sia citata e ben segnalata nel `README.md` (sezione dedicata con rimando);
- elenchi le misure con riferimento esatto al codice (file/riga/componente);
- contenga la procedura di riuso su altre app della stessa famiglia;
- sia aggiornata alle ultime modifiche dell'app (es. nuovi gruppi del pannello, nuovi colori, nuovi annunci ARIA).

## Verifica finale e consegna

- [ ] Tutte le guide presenti e coerenti con il codice attuale.
- [ ] `pnpm check` e `pnpm build` passano nel test di ricostruzione da zero.
- [ ] Lo ZIP non contiene percorsi vietati né artefatti di funzionalità rimosse.
- [ ] `ACCESSIBILITA.md` è la sezione ben segnalata e riusabile richiesta.
- [ ] Consegna: `send_attachment` con `/home/user/<app>.zip` (e, se richiesto, la skill di manutenzione dell'app aggiornata).

## Aggiunte (6/10/2026, da «Espressioni, monomi e polinomi»)
- `git archive` è solo un'alternativa per selezionare file tracciati: NON garantisce l'assenza di segreti. Preferire lo script verificato sopra; con altri metodi sono comunque obbligatorie esclusioni esplicite di credenziali/runtime, scansione e manifest, prima della consegna.
- Il confronto hash deve riguardare gli asset client e le risorse pubbliche; non il bundle server che incorpora credenziali. Non distribuire quel bundle. Allineare README/REBUILD/RENDER/.env.example e report allo stato veramente pubblicato; niente affermazioni obsolete «nessuna chiave API» se l'app ora usa IA.
- Prima di consegnare, cercare `/home/user` e `/tmp` nei file di codice e nei test sempre attivi: percorsi del sandbox rompono `pnpm test` su GitHub/Render (un `dbg3.test.ts` con import assoluti è stato rimosso così). I test che usano risorse locali devono saltarsi da soli (`describe.skipIf`).
- Collaudo: ricostruire da zero e confrontare gli hash degli asset (`index-*.js`) con la build diretta, poi lanciare la suite anche nell'albero ricostruito.
- File ereditati da un'altra app (es. `GUIDA-UNICA.html`, `ISTRUZIONI-GITHUB.txt`) vanno segnalati all'utente, non rimossi in silenzio.
