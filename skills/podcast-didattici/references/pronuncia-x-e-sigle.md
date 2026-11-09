# Pronuncia verificata della X e della sigla XR

Leggere prima delle chiamate TTS quando il copione contiene la lettera X nominata come lettera, XR o una correzione di pronuncia. Regola confermata nella lavorazione del 1 novembre 2026.

## Regola italiana e grafia per il sintetizzatore

| Testo originale | Pronuncia italiana da ottenere | Scrittura in `speech_text` |
|---|---|---|
| X, nominata come lettera | «ics», /iks/, una sola sillaba | `ìks` |
| XR, sigla di extended reality | «ics erre», /iks ˈɛrre/ | `ìks erre` |
| `ics erre`, vecchio adattamento del copione | stesso suono /iks ˈɛrre/ | `ìks erre` |

Usare l'accento grave su **ì** e le lettere **ks**. Evitare di affidarsi alla sola stringa `ics`: nei podcast precedenti ha prodotto letture segnalate come errate dall'utente. Non scandire «i-ci-esse» e non leggere `ìks` come una sequenza di nomi di lettere.

- Conservare il documento, i titoli stampati e `source_text` esattamente come in origine: la resa fonetica appartiene solo al testo inviato al TTS.
- Contare e registrare tutte le occorrenze da correggere per ID del segmento, prima di generare.
- Non sostituire automaticamente ogni carattere x/X. Distinguere il nome della lettera dalla variabile matematica, dal segno di moltiplicazione, dai numeri romani (XIX, XX ecc.) e dalla x dentro parole, marchi, URL o nomi propri. In questi casi adattare la lettura al contesto, senza cambiare il significato.
- Conservare le altre espansioni già verificate: VR → `vi erre`, AR → `a erre`, MR → `emme erre`. Non trasformare un passaggio italiano in una lettura inglese delle sigle senza richiesta.
- Impostare lingua italiana, genere coerente con l'ID e **speed 1.12** per entrambe le voci. Non inviare al TTS note di regia o simboli IPA da leggere ad alta voce.

## Correzione di un podcast esistente

1. Leggere il manifest e individuare TUTTI i segmenti con la X interessata, inclusi titolo, sommario, sintesi e mappe. Non fermarsi al primo esempio.
2. Registrare ID, testo fedele, vecchio/nuovo testo fonetico, numero di occorrenze, genere e percorso di uscita. Una modifica di pronuncia non autorizza riassunti o tagli.
3. Se l'utente chiede di rigenerare, rigenerare solo i segmenti necessari. Conservare gli altri stem vocali puliti, la copertina e la velocità già approvati; **dal 2 novembre 2026 rimontare senza musica**, anche se una versione storica aveva sottofondo. Una richiesta di aggiornare le skill **non** autorizza altre generazioni.
4. Associare ogni risultato TTS all'ID della chiamata, non all'ordine di completamento, al costo o al numero di caratteri. Registrare URL e nome della voce effettivamente restituiti; controllare all'ascolto l'inizio e la fine prima del montaggio se l'associazione è dubbia.
5. Ascoltare le occorrenze sia nella voce femminile sia in quella maschile. Un'ASR che trascrive «XR» può aver normalizzato una pronuncia errata: usarla per i tempi, non come prova fonetica.
6. Se `file_view` non riesce ad accedere al clip o le analisi si contraddicono, estrarre gli stessi passaggi in un breve WAV locale e riascoltarli. Non segnare un controllo come superato da una mancata analisi; non rigenerare per un problema di accesso al file.
7. Uniformare i livelli e rimontare la lettura integrale **con il solo parlato, senza alcuna musica** e senza `atempo`. Usare il master PCM/WAV già disponibile per l'AAC, quando possibile, evitando una ricodifica MP3 intermedia non necessaria.
8. Aggiornare i tempi reali dell'indice. Esportare **MP4** con la copertina fissa; ascoltare nuovamente le sigle estratte dall'AAC finale e l'ultima frase. Verificare assenza totale di musica, picchi, durata e decodifica completa.
9. Se una generazione nuova presenta ancora un errore, mostrarla e chiedere se correggerla prima di un'altra generazione, salvo autorizzazione esplicita a continuare fino alla correzione. Non eseguire tentativi automatici a pagamento.

## Esempi sonori inclusi

- `templates/PRONUNCIA_XR_FEMMINILE.wav`: breve estratto sintetico verificato di «ìks erre» con voce femminile.
- `templates/PRONUNCIA_XR_MASCHILE.wav`: breve estratto sintetico verificato di «ìks erre» con voce maschile.

Usarli come riferimento di ascolto, non come prova che una nuova generazione sia corretta, né come riferimenti per imitare persone reali. Non inserirli come ritagli ripetuti nel parlato: preservare continuità e prosodia dei paragrafi.

Per l'esempio concreto e i dati dell'ultimo MP4 usare `references/caso-realta-virtuale-v5.md`.

