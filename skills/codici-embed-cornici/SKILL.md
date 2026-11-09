---
name: codici-embed-cornici
description: "Manutenzione del documento CODICI-EMBED-CORNICI (DOCX «Cornici dinamiche v4»: 16 codici embed dedicati per Blogger + indice «Post del blog → Codici da usare»; esiste anche la versione suddivisa in 3 parti per materia con numerazione per file). Usare per: aggiungere una NUOVA cornice in uno slot libero (es. Codice 14), sostituire un codice con un'altra app, aggiornare titoli e indici, estrarre e trasformare l'HTML di un codice (APP_URL, font OpenDyslexic auto-ospitati, titolo testata) con verifiche assert, ricostruire la cella mantenendo Consolas 7pt, suddividere in parti per materia, rinumerare le cornici da 1 in ogni file, testare nel browser (attenzione al falso negativo COEP del dev server). Script pronti: estrai_codice.py, sostituisci_codice.py, suddividi_in_parti.py, rinumera_parti.py. NON per l'app cornice-universale né per le cornici incluse nel codice delle singole app."
---

# CODICI-EMBED-CORNICI — come aggiornare il documento

Il DOCX (negli upload, es. «…_CODICI-EMBED-CORNICI-v4-…docx») è la raccolta delle cornici dinamiche dedicate usate nei post del blog. Verificare SEMPRE la struttura con un dump via python-docx (iterare `body.iterchildren()`): non dare per scontati gli indici.

- Titolo «Cornici dinamiche v4»
- Tabella indice T[0] «Post del blog | Codici da usare»: sinistra = materia/app, destra = «Codice N» (o «Codici 7 e 8» — righe multi-codice possibili)
- Per ogni codice: paragrafo (Heading 1 o Normal) «Codice N — NOME APP» + tabella del codice (1×1; cella = HTML completo, un paragrafo per riga, Consolas 7pt)
- Tutte le cornici usano classi CSS `lf-` (CSS identico duplicato in ogni codice: innocuo) e isolamento JS per istanza (token `'lf'+random`, filtro `e.source`, protocollo «labvisivo:height» con anti-loop e anti-tremolio). NON rinominare classi e token.
- Stato attuale: 16 codici; la numerazione può avere SLOT LIBERI (il 14 è stato assegnato a Espressioni Letterali; prima era libero). Ogni nuova app del blog deve ricevere il PROSSIMO numero libero.

## Workflow di sostituzione di un codice
1. **Dump della struttura** per trovare il paragrafo «Codice N — …» e la tabella subito dopo.
2. **Estrai l'HTML attuale**: `python scripts/estrai_codice.py --src file.docx --codice N --out codiceN-attuale.html` (stampa APP_URL, domini, font, titolo testata: è la lista di ciò che va adattato).
3. **Trasforma l'HTML per la nuova app** con sostituzioni verificate da assert (ognuna ESATTAMENTE una volta): commento di intestazione «CORNICE DINAMICA — <APP> (embed DEDICATO · v4 impermeabile + anti-loop + anti-tremolio)»; riga «⭐ Versione DEDICATA: serve SOLO «…».» + descrizione dell'app; `var APP_URL = 'https://<app>.easy-peasy.site/';`; URL @font-face `https://<app>.easy-peasy.site/fonts/OpenDyslexic-Regular-v2.woff2` e `-Bold-` (verificare con curl: 200); `<p class="lf-titolo">NOME APP</p>`; attributo `title` dell'iframe; commento «⚙️ CONFIGURAZIONE — DEDICATA a …». Alla fine: ZERO residui dell'app precedente; contare le occorrenze del nuovo dominio.
4. **Sostituisci nel DOCX**: `python scripts/sostituisci_codice.py --src orig.docx --out aggiornato.docx --codice N --html nuovo.html --titolo "Codice N — NOME APP" --indice "MATERIA — Nome app"`. Lo script ricostruisce la cella clonando pPr/rPr originali (Consolas 7pt, `xml:space="preserve"`).
5. **Verifica ricaricando il DOCX**: paragrafi della cella = righe dell'HTML; zero residui; ALTRE tabelle intatte (confronto byte-per-byte); totale tabelle invariato. Con 16 codici: la tabella del codice N è `doc.tables[N]` (indice a posizione 0).
6. **QA nel browser** (obbligatorio): copia l'HTML in `client/public/test-cornice.html` del dev server dell'app, apri `{preview}/test-cornice.html`, verifica: titolo e pulsanti (Schermo intero, Ricarica) sulla stessa riga; app caricata; altezza adattata; stato «App online — buon lavoro!». Poi ELIMINA il file di test. ⚠️ **Falso negativo COEP**: il dev server Vite (`server.headers`) aggiunge `COEP: require-corp` a TUTTE le risposte → un iframe cross-origin verso la produzione viene BLOCCATO e la cornice mostra «app non raggiungibile» anche se è a posto. Diagnostica: test same-origin (APP_URL = URL del dev server) per validare cornice+protocollo; prova definitiva con l'APP_URL di produzione servendo la pagina da un server SENZA COEP (es. `python3 -m http.server 8000` e URL `https://8000-<sessione>.e2b.app/`). L'«Â» mojibake del titolo con http.server è solo charset del server di prova, non un difetto.
7. **Consegna** con send_attachment, versione nel nome del file (es. «…-v4-aggiornato-<app>.docx»). Se si aggiunge un codice nuovo, aggiornare anche le 3 parti (vedi sotto).

## Workflow per AGGIUNGERE un codice NUOVO (slot libero, provato con il Codice 14)
1. Dump: individuare il paragrafo del codice SUCCESSIVO a quello libero (es. «Codice 15 — …») e la sua tabella 1×1.
2. Script python-docx (vedi `suddividi_in_parti.py` per gli helper `set_testo` ecc.):
   - `deepcopy` del paragrafo titolo successivo → sostituire il testo con «Codice N — NOME APP» (cambiare `runs[0].text`, rimuovere i run extra);
   - `deepcopy` della tabella 1×1 successiva come segnaposto (tenere un solo paragrafo nella cella);
   - inserire ENTRAMBI con `addprevious()` PRIMA del paragrafo successivo (ordine: titolo poi tabella);
   - riga indice: `deepcopy` di una riga esistente con `row._tr`, inserirla con `addprevious` nella posizione giusta (ordine numerico), poi RITROVARLA con `row._tr is new_tr` (⚠️ NON cercarla per testo: la copia ha ancora il testo della riga sorgente) e impostare i testi delle celle.
   - ⚠️ Identificare la tabella indice dal testo della prima cella (`.startswith("Post del blog")`), MAI con `doc.tables[0] is obj`: python-docx ricrea gli oggetti Table ad ogni accesso e il confronto `is` non funziona mai.
3. Eseguire `python scripts/sostituisci_codice.py --src con-segnaposto.docx --out finale.docx --codice N --html nuovo.html --titolo "Codice N — NOME APP" --indice "MATERIA — Nome app"`.
4. Verifiche: titoli in ordine «Codice 1..16» (confrontare con `startswith("Codice N")` o `split(" — ")[0]`, MAI slicing `[:14]`: la «—» è multibyte e il troncamento rompe l'assert); cella N = righe HTML; occorrenze dominio nuovo; altre celle intatte.

## Suddivisione in parti per materia
`python scripts/suddividi_in_parti.py` (config `SRC` + `PARTI` in testa: file, titolo, lista codici — ADATTARE alle parti volute). Metodo: parte dal documento COMPLETO e RIMUOVE i blocchi estranei (preserva stili, sectPr, formattazione) invece di ricostruire. Regole: tenere il paragrafo Titolo (rinominato «… — Parte N · MATERIA»), riempire il primo paragrafo vuoto con un sottotitolo che elenca i codici, filtrare le righe dell'indice estraendo i numeri dalla colonna destra con regex (righe multi-codice tipo «Codici 7 e 8» vanno tenute se ALMENO UN codice appartiene alla parte), tracciare il «codice corrente» per associare i paragrafi vuoti al loro blocco. La numerazione originale resta invariata (coerenza con i post pubblicati).

## Rinumerazione per file (preferenza attuale dell'utente)
`python scripts/rinumera_parti.py`: come sopra MA i titoli diventano «Cornice k — NOME APP» (k riparte da 1 IN OGNI FILE), l'intestazione destra dell'indice diventa «Cornici da usare» e ogni riga mostra la corrispondenza: «Cornice 3 (Codice 14)», «Cornici 3, 4 e 5 (Codici 8, 9 e 10)» (helper `elenca` con virgole ed «e» finale). Il sottotitolo spiega che tra parentesi c'è il numero originale da citare nei post del blog. Le celle HTML restano byte-per-byte identiche al documento completo. NOTE: il documento COMPLETO resta intatto come archivio; dopo ogni aggiornamento rigenerare le parti; per la regex di verifica usare `Cornic[ei]` (⚠️ `Cornici?` rende opzionale l'«i», non l'«e»).

## Note
- L'indice richiede l'aggiornamento di ENTRAMBE le rappresentazioni: paragrafo-titolo del blocco E riga «Post del blog».
- Se l'app non implementa `labvisivo:height` (`client/src/lib/heightSync.ts` che risponde al ping e rispecchia il token `?cornice=`), la cornice non si adatta: prima aggiungere heightSync e ridistribuire.
- LibreOffice (`soffice`) può fallire la conversione DOCX→PDF in sandbox («source file could not be loaded»): affidarsi alle verifiche python-docx.
