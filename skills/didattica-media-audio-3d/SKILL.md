---
name: didattica-media-audio-3d
description: "Produrre media didattici personalizzati: podcast MP4 senza musica con copertina fissa e audio integrale di PDF e quaderni a due voci italiane alternate, velocità approvata 1,12×, fonte esatta e testo/indice temporale; lettura italiana di circolari scolastiche in MP3, documentari claymation con narrazione/montaggio e diorami 3D GLB per Figmin XR/Sketchfab/blog. Usare per sostituire letture approvate senza rigenerarle, escludere le fonti solo su richiesta, formato fisso delle circolari, normalizzazione volume, piano scene, continuità visiva, QA e geometria/validazione GLB. Non usare per manutenzione delle app web. Per i motori di generazione leggere anche le skill generali audio-generation, video-generation o image-generation pertinenti; questo pacchetto conserva le regole didattiche personali."
---

# Media didattici — scegliere il flusso pertinente

## PRIORITÀ — PODCAST REALTÀ VIRTUALE APPROVATO (5 NOVEMBRE 2026)

L'utente ha approvato esplicitamente come perfetto il podcast «REALTÀ VIRTUALE A SCUOLA» e il suo PDF chiaro. Usare [baseline, MP4 identico, manifest e clip](references/podcast-vr-approvato-2026-11-05.md): **16:44**, lettura dell'ultimo PDF, due voci italiane alternate a **1,12×**, **nessuna musica**, copertina fissa e testo/indice; include sintesi, tutte le 10 domande con le 40 opzioni, mappa e fonti. Non rigenerare registrazioni o immagini approvate. Per i podcast didattici personali, anche chiamati file audio, la consegna predefinita è **MP4 leggero con titolo completo e PODCAST**, senza musica o sigle musicali; usare MP3 se richiesto esplicitamente e per le circolari, che restano un caso distinto. Se disponibili, leggere anche `podcast-didattici` e `audio-generation`. Pronuncia: X «ics», XR «ics erre»; 3D «tre dì» con pausa dopo la D. Controllare entrambe le voci nel file finale quando questi elementi compaiono. I numeri del caso approvato non sono quote o durate universali.

## PRIORITÀ SUCCESSIVA — CLIP APPROVATE E FONTI ESCLUSE SU RICHIESTA

Per «questa va bene, inseriscila nell’audio completo» o «elimina la lettura delle fonti» leggere **`references/montaggio-approvato-senza-fonti.md`**. Riutilizzare esattamente la clip approvata, senza rigenerarla, accelerarla di nuovo o applicare filtri aggiuntivi automaticamente. Se era richiesta una prova separata, inserirla solo dopo approvazione. Togliere gli elenchi bibliografici richiesti, compresi quelli nelle appendici, ma conservare le spiegazioni e i riferimenti pertinenti nel discorso. Il PDF conserva le fonti. Aggiornare capitoli, testo/indice e metadati; non chiamare integrale una lettura con esclusioni volontarie senza precisarlo.

**Metodologie correnti: MP3 v9 senza fonti (20:30), Peer tutoring approvato a 09:42, appendice a 17:25**. È compatibile con PDF v13 IMMAGINE OGNI UNITÀ (29 pagine): UNA immagine subito dopo il banner di ogni unità, nessuna seconda immagine, inizi su pagina nuova delle 10 unità e sezioni finali preservati. Testo e ordine invariati: nessuna nuova registrazione per questa grafica. Non ripristinare il vecchio MP3 da 26:24 con fonti. Registro e testo/indice portabili inclusi; i file audio non sono inclusi e vanno recuperati, non rigenerati automaticamente. Nessuna generazione per collaudare la skill.

## PRIORITÀ AUDIO PDF — APPROVATA IL 1 NOVEMBRE 2026

Per «crea/ricrea l’audio di questo PDF», «a due voci» o «alla velocità degli ultimi», leggere **`references/audio-pdf-due-voci.md`** e la skill generale `audio-generation`. Leggere il nuovo allegato completo, alternare **voce italiana femminile e maschile per capitolo** con **speed=1.12 in ogni chiamata**, senza musica né riassunti. Includere titolo/indice, esempi, sintesi, attività, mappe, appendici e fonti presenti. Escludere elementi non narrativi identificati ed eventuali sezioni esplicitamente escluse dall’utente (come le fonti nell’audio delle metodologie); non usare copioni superati. Ricomporre paragrafi spezzati dal PDF, controllare formule/unità ed esempi stranieri. Non applicare il formato breve delle circolari alle guide.

Usare gli script inclusi `scripts/estrai_pdf_audio.py` e `scripts/assembla_audio_pdf.py`, che non generano voci. Il montaggio normalizza in due passate, aggiunge pause brevi, produce MP3, testo/indice e report tecnico con ascolto ancora da completare. Ascoltare inizio/fine di ogni parte e passaggi rischiosi prima di dichiarare verificato. Per i podcast personali consegnare un MP4 leggero con copertina fissa e l’indice temporale; MP3 per richieste esplicite e circolari. Non rigenerare automaticamente errori o audio già compatibile dopo sole modifiche grafiche; chiedere consenso se serve una nuova generazione correttiva.

| Output richiesto | Leggere |
|---|---|
| Podcast didattico personale e versione VR approvata | [Podcast VR approvato](references/podcast-vr-approvato-2026-11-05.md), più `podcast-didattici` se disponibile e `audio-generation` |
| Audio integrale di PDF/guida/quaderno a due voci, 1,12× | [Audio PDF](references/audio-pdf-due-voci.md), più `audio-generation` |
| Sostituzione di clip approvata o audio senza lettura delle fonti | [Montaggio approvato](references/montaggio-approvato-senza-fonti.md) |
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

- PDF/guide/quaderni: **integrale salvo esclusioni esplicite, due voci italiane alternate, 1,12×**, PDF corretto verificato con SHA-256. Podcast personale: MP4 con copertina fissa più testo/indice; MP3 se espressamente richiesto o per circolari. Niente musica. Normalizzazione a due passate −16 LUFS / −1,5 dBTP, WAV intermedi e pause circa 0,3 s. Conservare il testo e dichiarare i limiti del QA a campioni. Non modificare la velocità un’altra volta nel montaggio.
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

