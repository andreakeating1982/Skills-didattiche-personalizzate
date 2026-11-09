# AUDIO INTEGRALE DEI PDF — DUE VOCI, VELOCITÀ 1,12×

> **Priorità successiva per podcast didattici personali:** usare [il profilo MP4 senza musica e il podcast VR esplicitamente approvato il 5 novembre](podcast-vr-approvato-2026-11-05.md). Anche se chiamati «file audio», i podcast personali si consegnano abitualmente in MP4 leggero con copertina fissa; MP3 solo se esplicitamente richiesto o per circolari. Il montaggio MP3 descritto sotto può essere un intermedio. Non modificare né rigenerare la versione approvata per aggiornare la skill.

Standard personale approvato il **1 novembre 2026** per guide e quaderni PDF. Leggere anche `audio-generation/SKILL.md` e `audio-generation/references/speech.md`. Non modificare queste skill generali di sistema. Le circolari conservano il loro formato speciale (dall’Oggetto al nome del Dirigente), non ereditano automaticamente questa lettura integrale a due voci.

## PRIORITÀ SUCCESSIVA — ESCLUSIONI E REGISTRAZIONI APPROVATE

Per sostituire una clip già approvata o togliere la lettura delle fonti leggere `montaggio-approvato-senza-fonti.md`. La lettura completa è il default, non un obbligo contro le esclusioni esplicite dell’utente. Per le metodologie usare ora l’MP3 **v9 senza fonti, 20:30**, con la metodologia 7 approvata; bibliografia nel PDF conservata. La revisione grafica v13 (29 pagine), con UNA immagine subito dopo ogni banner, senza seconde illustrazioni e con gli inizi pagina della v12 mantenuti, conserva testo/ordine e non richiede nuova registrazione. Non riusare come corrente l’esempio storico da 26:24 sotto.

## CONTRATTO DI LETTURA

- Usare **due voci italiane, femminile e maschile alternate per capitolo/sezione**, con `language="Italian"`, `accent="Italian"`, `speed=1.12`. Questa è la velocità leggermente accelerata approvata, da riusare nelle richieste «come gli ultimi audio». Una nuova indicazione esplicita prevale.
- Mantenere la stessa voce per tutte le parti di un capitolo lungo. Non alternare a ogni frase e non trasformare il testo in dialogo. La copertina può essere femminile e il primo capitolo maschile, come nei lavori verificati; conta l’alternanza coerente, non un ruolo teatrale.
- La selezione automatica ha restituito **Aida** e **Lorenzo Prada** negli esempi recenti. Registrare il nome effettivamente restituito, ma non promettere selezione nominale o identità garantita: il tool espone genere/lingua/accento, non un voice_id.
- Leggere **integralmente, salvo sezioni esplicitamente escluse dall’utente**, il documento scelto: titolo, sottotitolo, indice, introduzione, capitoli, esempi, sintesi, attività, tabelle, mappe, quiz/opzioni e soluzioni se già presenti, appendici e fonti. Niente musica, effetti, riassunti o soluzioni aggiunte.
- Per un podcast personale consegnare **un MP4 finale con copertina fissa per PDF**, non soltanto clip né l'MP3 intermedio. Per richiesta esplicita di MP3 usare il formato richiesto; per più PDF mantenere file separati. Aggiungere testo letto e indice temporale in Markdown; comunicare durata misurata.

## 1. FONTE ESATTA E PROVENIENZA

Individuare l’allegato effettivo, leggerlo per intero e registrare nome, pagine e SHA-256. La richiesta di leggere un nuovo allegato non autorizza a usare il copione di una versione precedente. Se non compare, verificare i file disponibili e chiedere di ricaricarlo; non dichiarare di averlo ricevuto. Per aggiornare un PDF scegliere la baseline approvata con `quaderno-accessibile/references/versioni-appendici-2026-11.md`.

Eseguire `scripts/estrai_pdf_audio.py input.pdf --out lavoro/fonte`. Produce blocchi e coordinate di ogni pagina, estratto completo e impronta della fonte. **Non rimuove nulla e non decide l’ordine narrativo**: rivedere copertina, intestazioni, colonne, mappe e moduli visivamente. Scansioni, testo mancante o OCR dubbio richiedono lettura visiva/OCR verificato prima del TTS.

## 2. ESTRARRE SENZA SPEZZARE LE FRASI

- Il PDF può dividere una frase in più blocchi per il neretto o per l’andata a capo. Ricomporre il paragrafo logico prima di aggiungere punteggiatura: non mettere un punto a ogni blocco estratto e non usare un algoritmo geometrico senza revisione.
- **Conservare tutte le parole del testo**, con confronto pagina per pagina prima delle trasformazioni di pronuncia. Un confronto per inventario di parole aiuta a trovare omissioni ma non verifica ordine, significato o corrispondenza del parlato.
- Oltre alle eventuali sezioni escluse esplicitamente dall’utente, escludere soltanto elementi non narrativi identificati: numeri di pagina, localizzatori dell’indice, badge decorativi, righe vuote da compilare e codici tecnici non stampati. Conservare numeri di capitoli/esempi, dati, formule, date, numeri delle fonti e vere istruzioni. Documentare le esclusioni per pagina; non eliminare ogni riga numerica con una regex generica.
- Leggere tabelle per etichetta e contenuto della riga; mappe per gruppo e nodo, con titolo/spiegazione affiancati correttamente. Nella mappa di studio le due colonne non vanno lette riga per riga mescolando frasi dei due nodi.
- Per il **foglio Cornell**, leggere entrambe le spiegazioni operative e tutte le etichette (Data, Materia, Argomento, Parole chiave o domande, Appunti, Sintesi). Omettere solo le righe vuote. Non perdere il secondo paragrafo mentre si sostituisce la griglia con etichette.
- Non leggere alt delle immagini come se fossero testo del PDF né inventare descrizioni o istruzioni aggiuntive. Se un’immagine contiene contenuto didattico essenziale non presente nell’estratto, verificarlo e includerlo fedelmente.

## 3. COPIONE PRONUNCIABILE, NON RISCRITTURA

Conservare una trascrizione fedele e una versione per TTS. Registrare le trasformazioni, evitando sostituzioni che cambino significato o sintassi:

| Stampato | Lettura possibile |
|---|---|
| BES / DSA | bisogni educativi speciali / disturbi specifici dell’apprendimento |
| un DSA | un disturbo specifico dell’apprendimento, non «un disturbi…» |
| PEI, PDP | piano educativo individualizzato / piano didattico personalizzato, oppure lettere scandite quando appropriato |
| x; 3x + 4 = 19 | ics; tre per ics più quattro uguale diciannove |
| v = s ÷ t; s = v × t | vu uguale esse diviso ti; esse uguale vu per ti |
| cm²; m/s | centimetri quadrati; metri al secondo |
| ___ in una frase da completare | spazio vuoto |
| → con significato sequenziale | poi, oppure il collegamento semanticamente corretto |
| Regole_di_classe.docx | Regole di classe, documento Word |

Non convertire tutto in minuscolo: nomi propri, sigle e formule hanno significato. Non confondere unità m/metri, s/secondi e lettere delle variabili. Pronunciare leggi, date, numeri e articoli senza alterarne il valore; non «correggere» la bibliografia durante la sola lettura. Negli esempi inglesi/francesi/spagnoli conservare le parole originali: un accento italiano comprensibile non autorizza una riscrittura o rigenerazione.

## 4. SEGMENTARE E GENERARE UNA SOLA VOLTA

Preparare `manifest.json` con titolo, percorso e SHA-256 del PDF, pagine, velocità e lista ordinata `parts`. Ogni parte deve avere `name` univoco, `chapter`, `title`, `pages: [inizio,fine]`, `gender`, `speed: 1.12`, `text`; facoltativi `voice_name` effettivo e `clip_path`/`source_url`. Esempio in `templates/manifest-audio-esempio.json`.

- Mirare a 3.900–4.400 caratteri **per testo intero passato al tool**, sempre meno di 5.000. Spezzare tra paragrafi senza lasciare solo il titolo nell’ultima parte se evitabile. Conservare ordine e genere del capitolo.
- Chiamare `media_generate_speech` con il testo definitivo, senza istruzioni di recitazione nel campo `text`. Richiedere lingua/genere/accento coerenti e **speed=1.12 in ogni chiamata**. Non accelerare in seguito con ffmpeg: evitare doppia accelerazione o stretching.
- Salvare subito ogni URL e il nome voce realmente restituito nel manifest. Scaricare in `clip/<name>.mp3`; non richiamare il generatore dopo un timeout senza controllare se esiste già un risultato. Non usare API alternative o script per consumare generazioni aggirando i tool.
- Se si trova un difetto, conservare il risultato, spiegare il problema e chiedere consenso prima di rigenerare. I test delle skill riusano clip già disponibili e non generano audio nuovo.

## 5. ASSEMBLAGGIO RIPRODUCIBILE

Usare `scripts/assembla_audio_pdf.py manifest.json --out lavoro --offline` dopo aver salvato le clip locali, oppure senza `--offline` per scaricare gli URL già restituiti. Lo script non genera voci; valida il manifest, decodifica, normalizza, concatena, misura ed esporta. Dipendenze: Python 3, requests, ffmpeg/ffprobe. Per estrarre il PDF serve PyMuPDF. Percorsi relativi nel manifest riferiti alla sua cartella.

- Normalizzazione EBU R128 a due passate di ciascuna clip, target **−16 LUFS**, **true peak −1,5 dBTP**, **LRA 11**. Non promettere volume istantaneo identico; misurare il risultato finale e controllare i cambi voce. Il target non equivale a un valore raggiunto esatto.
- Intermedi **WAV PCM mono, 44.100 Hz**, poi concatenazione ordinata con circa **0,3 s** di pausa fra clip. Non tagliare attacchi/finali e non applicare crossfade sulle parole. Per scene o musica usare altri flussi, non questi parametri automaticamente.
- Esportazione **MP3 128 kbps**, metadati e capitoli opzionali; indice Markdown sempre disponibile perché non tutti i lettori mostrano i capitoli MP3. Nessuna copertina generata non richiesta.
- Cache basata su hash della clip e parametri: non riusare un WAV dal solo nome dopo che il suo MP3 è cambiato. Conservare `manifest_con_durate.json`, rapporti e SHA-256 finale.
- Verificare che la durata finale corrisponda alla somma delle clip più le pause, ammettendo il piccolo padding MP3; controllare errori di decodifica. Il rapporto tecnico deve lasciare l’ascolto **in sospeso**, non impostarlo automaticamente come superato.
- Se il lavoro può durare minuti, eseguirlo in background con notifica; attendere l’evento finale, senza polling e senza lanciare il montaggio una seconda volta.

## 6. QA: NON BASTA CHE IL FILE ESISTA

1. Verificare testo completo contro il PDF, esclusioni documentate e manifest in ordine, stesso genere nelle parti dello stesso capitolo, tutte le velocità 1.12.
2. Controllare presenza/decodifica di tutte le clip, durata, silenzi anomali e loudness. Parole al minuto sono solo un indicatore: non sostituiscono la verifica del parlato né devono raggiungere un numero fisso.
3. Ascoltare campioni iniziali e finali di **ogni** parte, segnando che i salti fra campioni sono intenzionali. Controllare voci alternate, intelligibilità, volume e assenza di troncamenti. Ascoltare anche almeno un passaggio del file finale attraverso un cambio voce, non soltanto le clip sorgenti.
4. Controlli mirati su elementi rischiosi: formule/dati/unità in matematica e fisica, esempi stranieri, attività Cornell, ordine della mappa, appendici e conclusione delle fonti. Campionare non equivale a dichiarare ascoltato integralmente l’intero MP3.
5. Registrare controlli realmente eseguiti e limiti. «Verifica tecnica superata» e «nessuna anomalia evidente nei campioni ascoltati» sono più corretti di una certificazione assoluta di perfezione. Generare i campioni non dimostra che siano stati ascoltati.

## 7. CONSEGNA E VALIDITÀ DELL’AUDIO

Per un podcast personale inviare MP4 finale con copertina fissa e Markdown con testo/indice in un’unica consegna; indicare durata e **1,12× / due voci italiane alternate**, senza musica. MP3 finale se esplicitamente richiesto o per il formato delle circolari. Per più PDF usare una sola consegna di tutti i risultati. Non includere solo campioni QA o file temporanei.

Non rifare l’audio per una modifica puramente grafica del PDF se testo e ordine sono invariati: verificarne la compatibilità. Una rimozione di sezione, una nuova appendice o un aggiornamento delle fonti possono invece renderlo superato. Non rigenerare senza richiesta.

## ESEMPI REALI, NON VINCOLI DI DURATA

| Documento effettivamente letto | Impostazione | Durata misurata |
|---|---|---|
| REALTÀ VIRTUALE A SCUOLA, PDF chiaro 17 pagine, podcast approvato il 5 novembre | MP4, copertina fissa, due voci, 1,12×, nessuna musica; domande e fonti lette | 16:44 |
| 10 METODOLOGIE DIDATTICHE INCLUSIVE, corrente v9 senza fonti, Peer tutoring approvato, compatibile con PDF v13 | due voci, 1,12×, esclusioni dichiarate | 20:30 |
| STORICO SUPERATO: metodologie, contenuto v7 compatibile con v8, fonti lette e vecchio Peer tutoring | due voci, 1,12× | 26:24 |
| Come_studiare_meglio.pdf, allegato di 23 pagine | due voci, 1,12× | 21:28 |
| Come_adattare_gli_esercizi_per_DSA_e_BES.pdf, allegato di 23 pagine | due voci, 1,12× | 26:10 |
| Una_classe_serena_si_costruisce_insieme_-_Come_gestire_una_classe_che_disturba.pdf, 12 pagine | due voci, 1,12× | 14:50 |

Le durate non sono obiettivi da imporre a una nuova lettura. L’audio BES v20 precedente (29:47) appartiene a un’altra lavorazione: non consegnarlo al posto del nuovo audio del PDF allegato. Progetti locali di provenienza: `/home/user/metodologie_v7_audio`, `/home/user/due_guide_audio_112`, `/home/user/classe_serena_audio_112`; non sono prerequisiti per usare gli script portabili inclusi.

