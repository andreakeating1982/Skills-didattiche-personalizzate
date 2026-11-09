# Fedeltà al PDF e revisioni senza contaminazione

Applicare la correzione dell'utente consolidata il 5 novembre 2026: «L'audio deve corrispondere al documento allegato». La richiesta di ricostruire dal PDF aggiornato annulla il precedente criterio di conservare automaticamente tutte le altre letture. Non aggiungere materiale di vecchie edizioni per rendere il podcast più completo.

## 1. Scegliere lo scopo prima di riutilizzare l'audio

- **Nuovo PDF / lettura integrale / ricostruzione fedele:** usare l'intero allegato corrente come unica fonte. Ricostruire inventario, copione, manifest e indice partendo dal documento, non dalla playlist precedente. Ricercare sia aggiunte sia eliminazioni, anche in pagine apparentemente immutate. Eliminare vecchi capitoli, righe, esempi, opzioni, fonti e numeri di pagina assenti dalla fonte attuale.
- **Riparazione soltanto acustica di sezioni esplicitamente indicate:** mantenere il resto dell'audio approvato soltanto entro lo scopo autorizzato. Non qualificare una revisione selettiva come lettura integrale dell'ultima edizione. Se un PDF nuovo contraddice le parti da conservare, segnalare il conflitto prima di consegnare una versione ibrida; la richiesta esplicita di corrispondenza integrale risolve il conflitto a favore della fonte corrente.
- **Solo montaggio/formato oppure aggiornamento skill:** non rigenerare o rimontare il podcast già verificato. Aggiornare la procedura, non il contenuto del risultato consegnato.

## 2. Bloccare e verificare la fonte

1. Leggere l'allegato attuale anche quando nome e percorso coincidono con il precedente. Registrare SHA-256, numero di pagine, titolo e sottotitolo; salvare una copia della fonte nel progetto.
2. Estrarre `pdftotext -raw` e `pdftotext -layout`; confrontare visivamente **tutte le pagine**. Se il PDF è scansionato, documentare l'OCR e verificarlo sulle immagini. Non sostituire l'estrazione con il ricordo di un documento dal titolo simile.
3. Preparare `PAGINE_CANONICHE.json`: numero e testo di ogni pagina nell'ordine visivo verificato. Elencare le sole esclusioni di servizio e le correzioni dell'ordine di estrazione. Non dichiarare il testo estratto automaticamente «verificato» senza averlo confrontato con il PDF.
4. Leggere tabelle per riga: etichetta poi testo della stessa riga. Leggere le mappe nodo per nodo, con tutti i termini del nodo. L'ordine grezzo delle colonne e il semplice inventario delle parole possono essere ingannevoli.

## 3. Preparare un inventario senza aggiunte

Includere, se presenti: titolo, sottotitolo, indice corrente con pagine corrette, ogni capitolo, tutte le sintesi, istruzioni, domande, opzioni, nodi della mappa, citazioni, bibliografia e attribuzione finale.

- Ricavare i conteggi **da quella versione del documento**; non usare come default i conteggi del caso di esempio.
- Non aggiungere saluti, dialoghi, spiegazioni, soluzioni, una conclusione, un capitolo d'esempio, un «Riepilogo» oppure etichette «Domanda» e «Risposta» non stampate. Leggere numeri e lettere delle domande/opzioni come sono presenti.
- Non cancellare ripetizioni, definizioni o richiami presenti nel PDF perché sembrano ridondanti. Rimuovere solo duplicazioni introdotte dal TTS e documentare il raccordo.
- Omettere soltanto numeri a piè di pagina, icone decorative o elementi di servizio non contenutistici; indicare le esclusioni. Conservare i numeri dell'indice, gli anni, le citazioni, i volumi, le pagine bibliografiche, gli URL e i DOI.
- Non inventare una descrizione dell'illustrazione. Distinguere le scritte illustrative ridondanti dal contenuto testuale unico da includere. In caso di dubbio verificare sul PDF, non completare per conoscenza dell'argomento.
- Conservare separati `source_text` (testo del documento, senza parafrasi) e `speech_text` (soltanto espansioni necessarie alla lettura orale). Esplicitare ogni espansione: `[1]` → «riferimento uno», B → «bi», `#` → «cancelletto», simboli degli URL, sigle e pronunce già approvate. Non usare una normalizzazione aggressiva per nascondere parole aggiunte.

## 4. Riutilizzare senza importare la vecchia edizione

Riutilizzare uno stem valido solo dopo aver dimostrato la corrispondenza del suo contenuto **e del suo ordine** con le pagine correnti. Un ID uguale, un titolo simile, lo stesso numero di parole o un ASR somigliante non bastano.

- Registrare file e hash dello stem, testo precedentemente letto, confronto con la fonte attuale e eventuali raccordi locali.
- Se il testo è cambiato, il vecchio audio non è riutilizzabile per quel passaggio. Generare le parti nuove autorizzate una sola volta; non rigenerare autonomamente un risultato difettoso già prodotto.
- Ricostruire il manifest da zero sulla nuova fonte e inserirvi solo segmenti giustificati. Non partire dal vecchio MP4 sostituendo soltanto i pezzi più evidenti.
- Aggiornare sia l'indice **parlato** (voci e pagine del nuovo PDF) sia l'indice **temporale** (durate effettive del nuovo montaggio).

## 5. Verificare l'intero MP4, non solo i pezzi nuovi

Tenere distinti tre esiti: conformità della fonte, controllo tecnico, controllo semantico/fonetico. Un comando terminato con codice zero, un hash corretto o un'elevata correlazione PCM/AAC non certificano che il contenuto sia quello giusto.

1. Estrarre dall'MP4 finale tutte le sezioni, comprese quelle riutilizzate. Trascriverle e confrontarle con il copione e il PDF corrente.
2. Ascoltare l'intera lettura suddivisa in estratti gestibili; verificare tutte le differenze rilevate. Controllare cambi di voce, citazioni, tutte le opzioni, mappa e bibliografia. Per questa serie, salvo nuova istruzione, usare voce femminile per tutta la verifica e maschile per tutta la bibliografia.
3. Trattare l'ASR come aiuto, non come verità: può inventare marcatori «musica», normalizzare un URL sbagliato, completare titoli scientifici a memoria o saltare cifre ripetute. Isolare gli intervalli dubbi, ascoltare il suono effettivo, eventualmente rallentare **solo una copia di controllo**. Non cambiare velocità o contenuto del master.
4. Verificare nei riferimenti i titoli esattamente stampati, senza aggiungere sottotitoli noti; controllare nomi, iniziali, anni, rapporti/revisioni, volume, numero, pagine. Ascoltare URL e DOI cifra per cifra; non ricostruirli dalla conoscenza dell'opera.
5. Ascoltare tutti i raccordi, in particolare dove è stata eliminata una sezione. Controllare che l'ultima sintesi passi direttamente alla sezione effettivamente successiva nella nuova fonte.
6. Misurare la durata e la decodifica dell'intero file; controllare loudness/picchi AAC, voci, assenza di musica, X/XR e 3D se presenti. Verificare fotogrammi di inizio/metà/fine e ultimi 25–40 secondi fino all'ultima frase completa.
7. Registrare la revisione con gli hash del **PDF, manifest e MP4 realmente verificati**. Ogni modifica successiva invalida la revisione finale: ripetere almeno i controlli coinvolti e dei raccordi nell'ultimo export. Non dichiarare completata una verifica ancora pendente.

## 6. Usare il controllo riutilizzabile

Leggere lo schema in `templates/SCHEMA_AUDIT_FEDELTA.json`. Eseguire:

```bash
python3 /home/user/skills/podcast-didattici/scripts/verifica_fedelta.py \
  --pages /home/user/progetto/PAGINE_CANONICHE.json \
  --manifest /home/user/progetto/MANIFEST_AUDIT.json \
  --out /home/user/progetto/qa/COPERTURA.json
```

Il controllo confronta la sequenza di `source_text` di ogni pagina con la pagina canonica, ammettendo **solo differenze di spaziatura**. Blocca omissioni, aggiunte, duplicazioni, ordine errato, hash della fonte mutato e riuso senza prova. Richiede una sola pagina per segmento oppure `source_units` esplicite per i segmenti multipagina. La preparazione corretta delle pagine canoniche resta un controllo umano/visivo obbligatorio: lo script non estrae né comprende il PDF al posto dell'agente.

Per verificare anche la registrazione del QA finale aggiungere:

```bash
  --mp4 /home/user/progetto/PODCAST.mp4 \
  --review /home/user/progetto/qa/REVISIONE_FINALE.json
```

Il flag di consegna resta falso nel solo controllo della fonte. Il secondo comando controlla hash, completezza e assenza di differenze non risolte nel verbale di revisione; **non ascolta l'audio e non sostituisce l'ASR, l'ascolto e il confronto semantico**. Non impostare i campi del verbale a vero per superare il validatore senza aver svolto i controlli.

Dopo modifiche allo script eseguire `python3 /home/user/skills/podcast-didattici/scripts/test_verifica_fedelta.py`: i test sintetici sono autonomi e non producono audio, video o documenti da consegnare. Eseguire separatamente una prova su una fonte reale con pagine già verificate; non scambiare i dati sintetici per un verbale del podcast.

## 7. Consegnare una sola versione corrente

Consegnare prima l'MP4 verificato senza musica, poi indice temporale/testo e copertina. Indicare durata e dimensione effettive. Se sostituisce una versione errata, identificarla chiaramente come sostitutiva. Non allegare un vecchio file o una revisione selettiva come se fossero la nuova lettura integrale.

Per il caso reale che ha originato queste regole leggere `references/caso-mappa-6-passi-pdf-unico.md`.

