---
name: circolari-audio
description: >
  Trasforma circolari scolastiche (PDF allegati dall'utente) in letture ad alta
  voce audio in italiano, con formato FISSO scelto dall'utente: senza
  intestazione (parte dall'Oggetto), si interrompe dopo il nome del Dirigente
  Scolastico (esclusa la nota «Firma autografa omessa...»), voce TTS italiana,
  un file MP3 per circolare consegnato come allegato. Usare per: leggere a voce
  una circolare, produrre l'audio di più circolari, aggiornare il formato della
  lettura. NON usare per documenti che non siano circolari o comunicazioni
  scolastiche, né per letture di altro tipo di PDF.
---

# Circolari → Audio

Produce, per ogni circolare PDF allegata dall'utente, UN file MP3 con la lettura ad alta voce in italiano, seguendo il formato fisso consolidato (vedi `references/formato.md`).

## Workflow (per ogni circolare)

1. **Estrarre il testo**: prima `file_read` sul PDF. Se il testo estratto è quasi vuoto o frammentato (PDF scansionato), usare `file_view` con prompt di trascrizione ESATTA pagina per pagina, senza riassumere. Se il PDF ha più pagine, analizare tutte.
2. **Verificare i nomi propri** (dirigente, istituto) direttamente dal testo del PDF: mai correggere o inventare nomi; se l'utente nomina un nome diverso da quello scritto nel documento, usare quello del DOCUMENTO e segnalarlo in una riga.
3. **Preparare il testo per il TTS** seguendo `references/formato.md`:
   - ESCLUDERE l'intestazione (protocollo, istituto, indirizzo/contatti, destinatari, data);
   - INIZIARE dall'**Oggetto**;
   - leggere TUTTO il corpo verbatim, con correzioni ortografiche per il TTS (sigle senza punti, date e numeri in lettere, sezioni PROTOCOLLO/RELAZIONI/PROGRAMMA citate come da documento);
   - TERMINARE dopo «Il Dirigente Scolastico, Dott.ssa/Dott. <Nome Cognome>» — ESCLUDERE la nota «Firma autografa omessa...».
4. **Generare l'audio**: `media_generate_speech` con `language: Italian`, `speed: 1` (voce maschile Lorenzo Prada, quella consolidata). Se il testo supera il limite di caratteri, spezzare in più chiamate in ordine. Se spezzato, unire le parti in UN SOLO MP3 (ffmpeg concat; salvare le parti temporanee in /tmp per non sporcare la cartella di lavoro).
5. **Normalizzare il volume (OBBLIGATORIO)**: TUTTI gli MP3 consegnati devono avere lo stesso volume percepito. Eseguire `bash /home/user/skills/circolari-audio/scripts/normalizza_audio.sh <file.mp3>` (normalizzazione loudness EBU R128 in due passate, target fisso I=-16 LUFS, TP=-1.5 dBTP, LRA=11, ricodifica 44100 Hz). Richiede ffmpeg (`sudo apt-get install -y ffmpeg` se assente). NON saltare mai questo passo, nemmeno se l'audio è già «quasi giusto».
6. **Consegnare**: `file_upload` dell'audioUrl restituito in `/home/user/lettura_circolare_<slug>.mp3` (slug corto dal titolo/oggetto, minuscolo, trattini bassi), normalizzare, poi `send_attachment` con messaggio breve che riassuma cosa contiene la lettura.

## Regole

- Un file audio per circolare; se l'utente allega più circolari, ripetere il workflow per ciascuna e consegnare tutti gli MP3 (o consegnarli man mano, in ordine).
- NON riassumere la circolare nell'audio: la lettura è verbatim (salvo le adattazioni TTS).
- NON leggere URL, numeri di protocollo, codici fiscali/CM dell'intestazione.
- Se il PDF contiene ALLEGATI (istruzioni, moduli) dopo la firma, NON leggerli; segnalarlo all'utente e chiedere se li vuole in un file audio separato.
- Se una circolare non termina con la firma del dirigente, terminare l'audio dopo l'ultimo paragrafo del corpo e segnalarlo.
- Costi: ogni `media_generate_speech` consuma crediti; non rigenerare senza richiesta dell'utente (se c'è un errore, mostrarlo e chiedere conferma).
