# Copertina e MP4 con immagine fissa

## Copertina

- Usare l'immagine allegata dall'utente o estrarre quella del documento aggiornato con `pdfimages`. Non creare prima un'immagine diversa se la fonte è disponibile.
- Per aggiungere o correggere titolo/PODCAST su un'immagine, leggere `image-generation` e usare `media_generate_from_images` con il suo percorso sandbox. Non modificare l'immagine con Python.
- Mantenere stile, personaggi, oggetti e proporzioni. Se il documento usa clay adulta e calda, restare coerenti, senza introdurre decorazioni infantili.
- Conservare **tutto il titolo** e l'eventuale sottotitolo, con spelling e accenti esatti. Rendere **PODCAST** grande e leggibile.
- Preferire una testata per titolo/sottotitolo e una fascia inferiore separata per PODCAST. Estendere la tela o ridurre proporzionalmente l'illustrazione anziché coprire persone o lettere.
- Usare margini sicuri e contrasto elevato. Per un futuro video orizzontale preferire 16:9; non forzare però un formato quadrato se non richiesto.
- Controllare una volta con `file_view`: trascrivere titolo, sottotitolo e PODCAST; verificare soggetti integri e assenza di tagli o sovrapposizioni.
- Se un risultato generato ha un errore, mostrarlo e chiedere prima di rigenerarlo. Non nascondere il problema e non spendere per una correzione non autorizzata.

### Prompt adattabile

> Minimally adapt the provided source illustration into a polished landscape educational podcast cover. Preserve the people, poses, objects, handmade clay textures and warm lighting; do not crop or distort them. Create clearly separated header and footer bands outside the illustration. In the header render the complete exact Italian title “[TITOLO]” and, if present, “[SOTTOTITOLO]”, preserving all accents. In the footer render “PODCAST” in very large bold readable uppercase. Keep safe margins, strong contrast, no overlaps and no extra text. If space is needed, extend the canvas or proportionally shrink the entire illustration.

### Eccezione storica limitata

Per la sola copertina «Una classe serena si costruisce insieme» v2, l'utente ha accettato la parola INSIEME parzialmente coperta («No, va bene così»). Non correggerla autonomamente. Non applicare questa eccezione alle nuove copertine.

## MP4 leggero: formato finale consolidato

L'utente ha corretto esplicitamente la consegna: il podcast deve essere restituito in **MP4 e non soltanto in MP3**. Per questa serie usare quindi MP4 con copertina fissa come formato finale, anche quando la richiesta parla di «file audio del podcast», salvo diversa istruzione esplicita. **Dal 2 novembre 2026 usare solo narrazione senza musica**, preferibilmente il master WAV, senza rigenerare le voci. Non riutilizzare MP3 o MP4 storici con sottofondo: ripartire dagli stem puliti. Procedere così:

1. Riutilizzare la narrazione **integrale approvata senza musica** soltanto se si deve montare proprio quella versione. Per un PDF aggiornato verificare prima la corrispondenza dell'intero contenuto con `references/fedelta-pdf-e-revisioni.md`; non riutilizzare l'audio solo perché già approvato su una fonte precedente. Conservare la copertina valida. Non generare musica, non rigenerare voci o immagine riuscite e non creare clip video AI.
2. Mantenere la stessa immagine fissa per tutta la lettura. Non accelerare, tagliare né sfumare l'audio per rispettare un limite di peso.
3. Preferire 1280×720, H.264, `yuv420p`, AAC e `+faststart`; con immagine fissa sono sufficienti circa 2 fps.
4. Adattare l'immagine con `scale=...:force_original_aspect_ratio=decrease` e `pad`, senza crop né deformazioni. Non ritagliare la parte con PODCAST.
5. Per video lunghi codificare una sola clip statica di 120 s e ripeterla con stream copy; aggiungere l'intero audio. Questa ripetizione non riguarda il parlato.
6. Per due voci pulite AAC 128 kbit/s è un buon punto di partenza; 96 kbit/s mono è possibile se occorre maggiore leggerezza. Non aggiungere musica per «riempire» lo stereo o le pause.
7. Stimare il peso dalla durata e dal bitrate; misurarlo dopo l'export. Se si desidera meno di 100 MB, intervenire su codifica/video/bitrate, non sulla durata del contenuto.

Script riutilizzabile:

```bash
python3 /home/user/skills/podcast-didattici/scripts/video_statico.py \
  --cover /home/user/progetto/COPERTINA_PODCAST.png \
  --audio /home/user/progetto/PODCAST_DUE_VOCI_SENZA_MUSICA.wav \
  --out /home/user/progetto/PODCAST_INTEGRALE.mp4 \
  --title "TITOLO COMPLETO — PODCAST"
```

Lo script decodifica prima l'audio per misurarne la durata effettiva, preserva tutti i campioni nel montaggio e genera fotogrammi di controllo. Non modifica il contenuto della copertina.

## Controlli e consegna

Considerare il lavoro completato soltanto quando esiste un **MP4 verificato e consegnato**. Una copertina allegata accanto a un MP3 non equivale a un MP4. La richiesta del formato è già confermata: non domandare ogni volta se si desidera il video e non generare scene animate per sostituire l'immagine fissa.

- Confrontare e ascoltare l'intera traccia AAC con il PDF corrente, non solo le parti nuove. Confermare indice parlato e temporale aggiornati e assenza di capitoli o righe eliminati dalla fonte.
- Eseguire un test di decodifica completa.
- Verificare codec/resoluzione e durata dell'audio contro la sorgente decodificata, con la sola tolleranza tecnica della codifica.
- Esaminare almeno un fotogramma iniziale, uno centrale e uno finale e ascoltare gli ultimi 25–40 s del video, non soltanto del file audio originale.
- Confermare che titolo e PODCAST restino leggibili, che l'immagine sia intera e che l'ultima frase termini senza tagli. Verificare anche uniformità delle due voci, **assenza totale di musica** e assenza di distorsioni nell'AAC del video, non soltanto nel WAV sorgente.
- Il controllo tecnico dello script video non sostituisce la misura dei picchi AAC: eseguire `loudnorm` sull'MP4 e, se necessario, riesportare soltanto l'audio dal master con più margine. Conservare la traccia H.264 con `-c:v copy` per non ricodificare l'immagine fissa.
- Controllare che non sia stata applicata una seconda accelerazione oltre a 1,12×. Nessun jingle, intro o coda musicale; il video deve contenere l'intero parlato fino all'ultima frase.
- Registrare il verbale finale con hash del PDF, manifest e MP4 effettivamente ascoltato. Dopo una riesportazione ricontrollare il file aggiornato; un verbale riferito a un hash diverso non autorizza la consegna.
- Allegare **prima l'MP4**, poi copertina e testo con indice temporale. Aggiungere l'MP3 soltanto su richiesta; non usarlo come sostituto del video. Mostrare il link esatto restituito dalla consegna, non un percorso locale nudo. Se si corregge una versione errata, identificare il nuovo MP4 come sostitutivo.
- Se il video richiesto risulta già approvato e consegnato, non rimontarlo in occasione di un semplice aggiornamento delle skill: registrare il risultato e riutilizzare gli script collaudati.

