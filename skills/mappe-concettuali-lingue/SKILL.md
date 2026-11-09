---
name: mappe-concettuali-lingue
description: "Manutenzione completa e personalizzazione dell'app MAPPE CONCETTUALI DI LINGUE STRANIERE (in /home/user/mappe-concettuali-lingue, Vite + React + TypeScript + Tailwind + tRPC + Drizzle, scaffold web-db-user; produzione https://mappe-concettuali-lingue.easy-peasy.site). Trasforma foto o testo di esercizi di inglese/francese/spagnolo in mappe concettuali PDF. Usare per: modificare la UI studente, le regole del PDF (titolo MAPPA/MAPPE, footer, frecce centrate, STRUMENTO fino a 1600 caratteri, passi 0-3 anche assenti), il pulsante di download, l'anteprima PDF su mobile (scheda APRI IL PDF al posto dell'iframe), la cornice dinamica per Blogger (protocollo labvisivo:height), la sincronizzazione altezza anti-tremolio (heightSync), l'accessibilità embed (lf-embedded), il collaudo nel browser e il deploy preview/produzione. NON usare per: produrre mappe da foto incollate in chat (usare mappe-concettuali-matematica), manutenere l'app matematica sorgente, modificare il DOCX dei codici embed (usare codici-embed-cornici)."
---

# Mappe concettuali di lingue straniere

App web che trasforma foto o testo incollato di esercizi di **inglese, francese o spagnolo** in **mappe concettuali PDF** (COSA CHIEDE → STRUMENTO → passi numerati). È la variante «lingue» dell'app di matematica (repo di riferimento: `MAPPE-CONCETTUALI-DI-MATEMATICA` di andreakeating1982, copia locale `/home/user/mappe-matematica-repo`). Accessibile: font OpenDyslexic auto-ospitato, OCR da foto (tesseract.js, dati in `client/public/tessdata`), embed in Blogger con cornice dinamica.

## Percorsi chiave

- `client/src/pages/Home.tsx` — pagina principale (upload foto → controllo schede → generazione PDF)
- `client/src/pages/WelcomePage.tsx` — prima pagina (nome, classe, data, selettore lingua)
- `client/src/lib/heightSync.ts` — **sincronizzazione altezza per embed** (vedi `references/heightsync-anti-tremolio.md` PRIMA di toccarla)
- `client/src/lib/ocr.ts`, `ocrClean.ts`, `cropBox.ts`, `imagePrep.ts` — OCR e ritaglio foto
- `server/mappe/pdf.ts` (~800 righe) — motore PDF (layout, frecce, footer, pagina per mappa)
- `server/mappe/extract.ts`, `rich.ts` — parsing testo/AI in schede strutturate
- `client/src/index.css` — regole `html.lf-embedded` (embed) e `html.lf-welcome-top` (autonoma)
- `cornice-dinamica/embed-mappe-lingue-dedicata.html` — cornice Blogger (Codice 15 del DOCX CODICI-EMBED-CORNICI)

## Regole FISSE del PDF (decisioni dell'utente — non cambiare senza richiesta esplicita)

1. **Titolo dinamico**: `MAPPA CONCETTUALE` con una sola mappa, `MAPPE CONCETTUALI` solo con più mappe.
2. **Footer**: solo `PAGINA X DI Y`, niente «Mappe concettuali» nel footer.
3. **Frecce centrate** (colore `#a8b3c6`, slot 12 px, tipo `Connector = "gap" | "arrow"`): nessuna freccia tra head e COSA CHIEDE (solo gap 5 px); freccia prima dello STRUMENTO e prima di **ogni** passo numerato, inclusa quella tra gli ultimi due passi (il bug off-by-one era in `connectors` in pdf.ts ~riga 510).
4. **Una mappa per pagina**, con flusso su più pagine se la mappa è lunga.
5. **STRUMENTO**: estendibile fino a **1600 caratteri**; **passi da 0 a 3, anche assenti** (schema, prompt AI, motore PDF e UI lo supportano ovunque).
6. Niente box «Occhio a», niente soluzioni nel PDF.
7. Font OpenDyslexic auto-ospitato (`server/mappe/fontData`).

## Convenzioni UI (stabilite in chat)

- **Pulsante finale di download** (in Home.tsx, sezione `pdfUrl`): marrone `bg-[#8b5a2b]`, hover `hover:bg-[#6e451f]`, testo esatto **«SCARICA IL PDF DELLA MAPPA»** con icona `FileDown` — era verde `#27ae60`, cambiato su richiesta.
- **Titolo app tutto maiuscolo**: «MAPPE CONCETTUALI DI LINGUE STRANIERE» in Home.tsx e WelcomePage.tsx.
- **Editor schede**: box STRUMENTO **sotto** COSA CHIEDE (non affiancato), come nel PDF.
- **Miniature foto caricate**: sempre **centrate e a dimensione originale** (mai ingrandite) — stili inline su `ul`/`li` per garantirlo anche nell'embed.
- Palette: carta `#f8f1e4`, inchiostro `#2e2018`, barra `#fdfbf8`; pulsante principale rosso `#b71c1c` (`.btn-mappe`).

## Anteprima PDF su mobile (scheda «APRI IL PDF»)

**Limitazione nativa dei telefoni**: i browser mobile (Chrome Android, Safari iOS) NON sanno renderizzare un PDF dentro un `<iframe>` — mostrano un segnaposto grigio (icona PDF, nome-codice blob, pulsante «Apri») o un box vuoto. Dal PC l'iframe funziona: per questo il problema si vede solo sul telefono, da sola e nel blog.

Fix v2 (checkpoint `5e68338`, in Home.tsx): la limitazione dipende dalla PIATTAFORMA, non dalla larghezza — la v1 usava `max-width: 768px` e mostrava la scheda a torto anche sul PC in embed stretto ≤768 px (la cornice del blog è spesso più stretta!). Stato `inlinePdf` con `isMobile()`: TRUE se puntatore primario tattile (`window.matchMedia("(pointer: coarse)")`) OPPURE user-agent mobile (`/Android|iPhone|iPod|IEMobile|Opera Mini|Silk|Mobile/i`) OPPURE iPad (`/iPad/i` nell'UA) OPPURE iPadOS 13+ (`navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1`, si spaccia per Mac ma resta un iPad senza PDF in iframe); `try/catch` → in dubbio comportamento desktop; listener `change` su `(pointer: coarse)` per i tablet che collegano/scollegano il mouse (coarse ↔ fine).

- **Mobile/tablet** (rilevamento v2 sopra) → scheda `.lf-pdf-card`: icona `FileText` marrone in cerchio, «Mappe-concettuali.pdf», nota («L'anteprima del PDF non è supportata da questo dispositivo…»), pulsante **APRI IL PDF** marrone `#8b5a2b` con `href={pdfUrl}` (blob:) e `target="_blank"` (apre a schermo intero dove il visualizzatore nativo funziona sempre), e sotto il consueto **SCARICA IL PDF DELLA MAPPA**.
- **Desktop** → l'iframe `.lf-pdf-preview` classico SEMPRE, a qualunque larghezza di finestra o cornice (75vh; 520 px fissi in embed).

Non rimuovere la condizione né tornare all'iframe su mobile: il segnaposto grigio è inaccettabile per gli studenti. MAI reintrodurre `max-width` nel rilevamento: falso positivo da desktop. Su desktop il comportamento resta identico a prima, a qualunque larghezza.

Test di regressione: pagina `/test-embed-680.html` (in `client/public`) — l'app in un iframe da 680 px su desktop deve mostrare `.lf-pdf-preview` presente e `.lf-pdf-card` assente dopo il flusso completo fino al PDF.

## Embed e sincronizzazione altezza (leggere SEMPRE prima di toccare heightSync)

Protocollo con la cornice Blogger: l'app invia `{type:"labvisivo:height", height, cornice}` al parent; la cornice risponde ai `labvisivo:ping` dell'app. **Il tremolio su mobile/blog si corregge SOLO lato app, mai modificando il codice embed nel blog** (la cornice ha già debounce 200 ms, filtro ±2 px, finestra di silenzio e anti-loop). Regole d'oro in `heightSync.ts`: misurare **solo il contenuto** (`#root`, mai `documentElement`/`innerHeight`), deduplica dei valori invariati, quantizzazione 2 px, throttle 150 ms, isteresi di riduzione 250 ms. Dettagli, sintomi→cause e test: `references/heightsync-anti-tremolio.md`.

CSS embed (`index.css`): in `html.lf-embedded` i `min-h-screen/min-h-dvh` e il body vanno a `min-height:0 !important`; l'anteprima PDF `.lf-pdf-preview` ha altezza **FISSA 520 px** in embed (il `h-[75vh]` fuori dall'embed crea un loop di crescita infinito della cornice — è già successo). Prima pagina: `.lf-welcome` (margini pareggiati) e `.lf-welcome-top` (canvas bianco quando aperta da sola).

## Collaudo nel browser

Leggere `references/collaudo-browser.md` per: pattern console (prima exec dopo navigate spesso fallisce → riprovare; output via `throw new Error('ETICHETTA ' + JSON.stringify(dati))`; driver asincrono unico per tutto il flusso), guida dell'app dentro iframe same-origin, e pagina di test anti-tremolio `/test-oscillazione.html` (in `client/public`, servita dal dev server; esito atteso: 3 messaggi di altezza per l'intero flusso, 0 oscillazioni).

## Deploy

1. `pnpm check` (TypeScript) e `pnpm build` prima di ogni deploy.
2. `webdev_save_checkpoint` con descrizione significativa — **obbligatorio prima della produzione**.
3. Deploy preview → collaudo → chiedere conferma all'utente → deploy produzione (vedi skill deploy-app-produzione).
4. **Verifica post-deploy con cache-busting**: la CDN serve HTML vecchio per qualche minuto dopo il deploy — verificare con `curl "...?cb=$(date +%s)" -H "Cache-Control: no-cache"` e confrontare l'hash del bundle in produzione con `dist/public/assets/` locale (hash identico = versione giusta). Non «correggere» di fretta: la cache si rinnova da sola.

## Cronologia decisioni (git log dell'app, per contesto)

`fbaa6b4` creazione app → `f0689bc` cornici dinamiche + guide (README, ADATTARE, REBUILD, ACCESSIBILITA, AGENTS, RENDER) → `515d024` STRUMENTO 1600 car. e passi 0-3 → `edda4e5` STRUMENTO sotto COSA CHIEDE + titolo maiuscolo → `5d5503a` titolo PDF dinamico + footer solo pagine → `f376bc8` miniature centrate inline → `bc00bf7` frecce tra i box + mappa per pagina → `8ef78a9` anteprima PDF 520 px in embed (fix loop crescita) → `910225e` freccia anche tra gli ultimi passi → `bcd90c8` pulsante marrone + testo → `1f929f6` heightSync anti-tremolio → `6252003` anteprima PDF su mobile: scheda APRI IL PDF al posto dell'iframe (i telefoni non renderizzano PDF in iframe) → `5e68338` rilevamento mobile v2: puntatore coarse + UA mobile + iPadOS (MacIntel+touch), rimosso max-width che dava falsi positivi da desktop embed ≤768 px + pagina test-embed-680.html.
