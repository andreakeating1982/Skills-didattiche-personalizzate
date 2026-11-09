---
name: didattica-media-audio-3d
description: "Produrre media didattici personalizzati: lettura italiana di circolari scolastiche in MP3, documentari claymation con narrazione/montaggio e diorami 3D GLB per Figmin XR/Sketchfab/blog. Usare per formato fisso delle circolari, normalizzazione volume, piano scene, continuità visiva, QA e geometria/validazione GLB. Non usare per manutenzione delle app web. Per i motori di generazione leggere anche le skill generali audio-generation, video-generation o image-generation pertinenti; questo pacchetto conserva le regole didattiche personali."
---

# Media didattici — tre flussi, non una procedura universale

| Output richiesto | Leggere |
|---|---|
| Audio di una circolare scolastica | [Circolari](references/circolari.md) |
| Documentario claymation narrato | [Video clay](references/video-clay.md) |
| Diorama 3D da immagine, GLB/glTF | [Modelli 3D](references/modelli-3d.md) |
| Script/template e provenienza | [Risorse](references/risorse.md), [copertura](references/copertura.md) |

Usare `python3 scripts/trova_profilo.py "circolari audio"` per risolvere alias.
Caricare solo il flusso scelto e la skill generale necessaria al motore.

## Regole condivise

1. Verificare la fonte: nomi, date, testo, pronuncia, contenuti delle scene.
   Non inventare audio trascritto o dettagli storici dal solo stile visivo.
2. Distinguere estrazione/trascrizione, generazione, montaggio e pubblicazione.
   Una skill che descrive uno script non prova che il media sia già prodotto.
3. Preservare formato richiesto, fonte e stile. Non trasformare una circolare
   in riassunto né mettere didascalie in un video che le esclude.
4. Usare i motori media per generare/modificare immagini; non usare gli script
   Python storici per ritocchi 2D o creare targhette/illustrazioni. Il codice
   resta utilizzabile per dati/geometria 3D, verifica e montaggio consentiti.
5. Le immagini di riferimento aiutano la coerenza, non la garantiscono: fare QA.
   Se un'immagine generata ha un errore, mostrarlo e chiedere prima di rigenerare.
6. Non produrre nuove immagini/video/audio solo per verificare questa skill:
   i test dei pacchetti devono restare offline e non consumare generazioni.
7. Per lavori lunghi usare esecuzione in background con notifica senza polling
   continuo o ripetizione dello stesso lavoro.
8. Collaudare output con metadati e ispezione/ascolto mirati, consegnare i file
   finali e sorgenti essenziali. Caricare/postare su servizi esterni solo con
   autorizzazione e passaggi di accesso gestiti correttamente.

## Contratti personali

- Circolari: partire dall'Oggetto, interrompersi dopo il nome del Dirigente;
  escludere intestazione e nota firma omessa. Un MP3 per documento, voce italiana.
  Chat storica: normalizzazione EBU R128 in due passate, target -16 LUFS e
  true peak -1,5 dBTP; non promettere volume istante per istante identico.
- Video clay: narrazione misura vincolante, riferimenti coerenti, prompt a tre
  strati, clip/assemblaggio e QA mirato. Nessun testo finale non richiesto.
- Diorami: una scala per geometria/proporzioni, texture incorporate, alfa MASK,
  validazione Khronos e anteprime; non dichiarare validato senza esecuzione.

## Disponibilità

Sono inclusi gli originali video-claymation-didattico e modello-3d-didattico,
con script/template. Per circolari-audio è stata ricostruita la procedura da
descrizione ed estratti chat, ma manca l'originale normalizza_audio.sh: non
presentarlo come allegato recuperato. Conservare la vecchia skill fino al
recupero. Le skill generali di sistema restano invariate.

