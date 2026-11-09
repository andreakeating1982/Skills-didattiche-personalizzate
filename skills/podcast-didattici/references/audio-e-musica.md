# Audio integrale a due voci — senza musica

Il nome del file è storico. **Dal 2 novembre 2026 l'utente ha eliminato per sempre la musica di sottofondo dai podcast.** La richiesta sostituisce le precedenti preferenze per basi tranquille o allegre. Nessun brano, intro, jingle, rumore ambientale aggiunto o coda musicale; soltanto le due voci e pause silenziose. Non generare né recuperare basi. Modificare questa impostazione solo dopo una nuova istruzione esplicita dell'utente.

## Fedeltà alla fonte aggiornata

**Prima di nuove edizioni o ricostruzioni leggere `references/fedelta-pdf-e-revisioni.md`. La fonte corrente prevale sulla precedente conservazione selettiva: eliminare anche parti e righe cancellate, non limitarsi alle aggiunte.**

1. Usare l'allegato corrente; registrare hash, titolo esatto, sottotitolo, versione e pagine. Un aggiornamento non autorizza a riciclare una vecchia lettura diversa.
2. Estrarre con `pdftotext -layout` e, per controllare l'ordine, anche `-raw`. Verificare visivamente tutte le pagine, incluse tabelle, verifiche, mappe e fonti.
3. Leggere titolo, sottotitolo, indice attuale con pagine corrette, spiegazioni, tutte le sintesi, ogni domanda con **tutte le opzioni nell'ordine A–D**, mappa finale, fonti e attribuzione finale. Non aggiungere risposte corrette, commenti, saluti, etichette «Domanda/Risposta» non stampate o un dialogo inventato. Non conservare vecchie sezioni autonome o righe assenti; non cancellare invece esempi brevi realmente presenti.
4. Non leggere numeri di pagina di servizio, icone e marcatori decorativi. Conservare invece numeri di esercizio, anni, volumi, DOI e citazioni scientifiche: rendere `[2, 3]` come «riferimenti due e tre», senza cancellarle come se fossero decorazioni. I numeri dell'indice possono essere letti come riferimenti di pagina.
5. Conservare `source_text` fedele e `speech_text` con soli adattamenti orali. VR → `vi erre`; AR → `a erre`; MR → `emme erre`; XR → `ìks erre` (suono /iks/); 3D → «tre dì», pausa **dopo la D completa**. Leggere `references/pronuncia-x-e-sigle.md` e `references/pronuncia-3d-e-pause.md`. Non sostituire ogni x né cambiare il significato di sigle e termini scientifici.
6. Le note di pausa non vanno lette dal sintetizzatore. Per una separazione 3D certa, si può dividere il copione alla fine di «tre dì» mantenendo lo stesso genere prima e dopo e aggiungere localmente circa 0,28 s; verificare la prosodia. Nessun testo va ripetuto o omesso.
7. Confrontare contenuti **e ordine**, non soltanto il conteggio delle parole. Mantenere la corrispondenza tra pagine, righe di sintesi, opzioni, nodi della mappa e ID vocali. URL/DOI possono essere scanditi per l'orecchio, ma conservarli integri nel testo consegnato.

## Due voci e velocità

- Usare `media_generate_speech`, lingua italiana, accento coerente e `speed: 1.12` per entrambe le voci; alternare `female` e `male` per nuclei di significato, non per singola parola.
- Suddividere ogni chiamata sotto 5.000 caratteri. Mantenere lo stesso genere se una frase viene divisa solo per inserire una pausa tecnica.
- Prima di generare preparare un manifest con `id`, `title`, `pdf_pages`, `gender`, `speed`, `source_text`, `speech_text` e `audio_path`; dopo aggiungere `audio_url`, `voice_name`, durata e hash.
- Associare ogni risultato all'ID della chiamata, non all'ordine di completamento, ai caratteri o al costo. Il tool sceglie le voci: non promettere nomi selezionabili o identità fisse fra sessioni.
- Se i risultati non sono più associati, scaricarli una volta e riconoscerli dal contenuto trascritto; conservare le trascrizioni in cache. I riferimenti con titoli inglesi, cifre e URL scanditi possono avere una somiglianza testuale bassa pur essendo corretti: confermare direttamente gli specifici file all'ascolto, non abbassare indiscriminatamente tutte le soglie e non rigenerare il parlato per un errore del controllo automatico.
- Riutilizzare parti già approvate soltanto dopo confronto completo di contenuto e ordine con la nuova fonte, registrando testo e hash dello stem. Preparare il manifest dalla nuova fonte, non dalla vecchia playlist. Non usare `atempo` sul risultato né applicare una seconda accelerazione oltre alla velocità TTS 1,12×.
- Per questa serie, salvo nuova istruzione, leggere tutta la verifica con voce femminile e tutta la bibliografia con voce maschile, anche se divise in più file.
- Uniformare le parti vocali in PCM 48 kHz, quindi unirle con pause circa 0,2–0,5 s. Non usare fade sulle parole. Per domande o separazioni tematiche sono ammesse pause silenziose più lunghe se utili, non tempi di attesa invasivi.
- Registrare tempi iniziali/finali reali e generare l'indice dalle durate misurate. Inizio e coda possono avere soltanto pochi decimi di secondo di silenzio tecnico, mai musica.

## Montaggio del solo parlato

Preparare un WAV integrale già ordinato, ottenuto esclusivamente dagli stem TTS. Non passare il vecchio mix con musica a un filtro di volume: per rimuoverla occorrono gli stem vocali puliti. Non usare `amix`, ducking, loop musicali o una base «a volume zero».

```bash
python3 /home/user/skills/podcast-didattici/scripts/normalizza_narrazione.py \
  --audio /home/user/progetto/NARRAZIONE_INTEGRALE.wav \
  --out /home/user/progetto/PODCAST_DUE_VOCI_SENZA_MUSICA.wav
```

Lo script accetta **una sola sorgente audio**, non argomenti per musica; produce WAV stereo 48 kHz con normalizzazione in due passaggi intorno a -16 LUFS e margine di true peak. Non modifica tempo o contenuti. Usare questo WAV direttamente per l'AAC del video, senza un passaggio MP3 superfluo. Per un MP3 esplicitamente richiesto, esportare dal master e ricontrollarne i picchi.

- Obiettivo indicativo: parlato finale fra circa -16 e -17 LUFS, picco reale dell'AAC ≤ -1 dBTP. Misurare sempre il **file codificato**, non attribuirgli i valori del WAV. Nella v7, il master con margine -2,5 dBTP aveva comunque picchi AAC eccessivi: riesportare localmente con `--true-peak -6` ha risolto, senza nuove voci e senza modificare la velocità. Non assumere che il picco WAV sia il picco AAC.
- Se un controllo tecnico fallisce, ripartire dal WAV e riesportare localmente senza nuove generazioni. Registrare i diagnostici; non confondere il successo del comando con la verifica dei contenuti.
- Per il formato consolidato e la copertina leggere `references/copertina-e-video.md`: la consegna principale è **MP4**, anche se chiamata «file audio del podcast»; l'MP3 è extra solo su richiesta esplicita.

## QA obbligatorio

- Verificare fonte esatta, tutte le sezioni e l'ordine, con particolare attenzione ai materiali aggiunti nella nuova versione. Un PDF v7 non va letto usando il copione v5.
- Trascrivere, confrontare e ascoltare **l'intero AAC finale per sezioni**, comprese le parti riutilizzate, e tutti i raccordi. Verificare voci, sigle, citazioni, opzioni, nodi e attribuzione. Esaminare tutte le differenze dell'ASR sul suono reale: non trasformare una trascrizione a memoria in certificazione.
- Controllare i titoli bibliografici come stampati, senza sottotitoli aggiunti, e cifre/URL/DOI una per una. L'ASR può completare un identificativo noto o saltare cifre ripetute: isolare e riascoltare la sequenza senza rigenerare automaticamente.
- Tenere separati conformità della fonte, esito tecnico e revisione semantica/fonetica; registrare gli hash di PDF, manifest e ultimo MP4. I soli conteggi o il confronto PCM/AAC non dimostrano fedeltà al documento.
- Verificare assenza di musica **in tutto il grafo di montaggio e nell'MP4 finale**: soltanto gli stem vocali sono ingressi audio; pause e coda non devono avere sottofondo. Un solo stream audio nel video, da solo, non dimostra l'assenza di musica.
- Per X/XR ascoltare il suono /iks/ in entrambe le voci. L'ASR che trascrive XR può normalizzare una lettura errata: non usarla come certificazione fonetica.
- Per 3D controllare ogni occorrenza nel video: D completa prima della pausa, parola successiva integra; niente «dimostrati», sillabe spezzate o clic. Se gli estratti danno responsi discordanti, ascoltare gli stessi intervalli dell'MP4 con contesto.
- Ascoltare gli ultimi 25–40 s **dell'MP4** e trascrivere l'ultima frase; non dedurne l'integrità dalla sola durata. Controllare l'eventuale attribuzione finale dell'autore.
- Misurare durata, dimensione, loudness e true peak dell'AAC, eseguire la decodifica completa e controllare fotogrammi di inizio/metà/fine.
- Consegnare MP4, copertina e testo con indice aggiornato; i log e gli stem restano materiale di lavoro. Non rigenerare risultati riusciti.

