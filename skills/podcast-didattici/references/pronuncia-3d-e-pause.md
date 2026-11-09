# 3D: pronunciare «tre dì» e separare la parola successiva

Leggere prima di preparare un podcast con la sigla 3D o correggerne la lettura. Regola consolidata il 1 novembre 2026: **terminare il nome della lettera D, poi fare una breve pausa, poi iniziare la parola successiva**. Applicarla a entrambe le voci e a tutte le occorrenze, incluse sintesi e mappe.

## Risultato da ottenere

| Testo del documento | Lettura desiderata |
|---|---|
| modelli 3D generati dal computer | modelli tre dì **[breve pausa]** generati dal computer |
| elementi digitali 3D mostrati | elementi digitali tre dì **[breve pausa]** mostrati |
| elementi 3D (filtri, Pokémon GO) | elementi tre dì **[breve pausa]** filtri, Pokémon GO |

Le parentesi quadre di questa tabella sono annotazioni di montaggio, **non testo da inviare al TTS**. Non unire la D alla parola seguente: evitare «tre dimostrati» e non spostare semplicemente la pausa tra «tre» e «dì». Non spezzare la vocale /i/ della lettera D.

- Conservare `3D` in `source_text`, PDF, titoli e testo integrale consegnato. Usare gli adattamenti fonetici solo in `speech_text` e le pause in metadati separati.
- Per una nuova sintesi, preparare una resa come `tre dì, generati...`, verificandone l'effetto nella frase reale: la sola grafia `tre di` aveva causato la fusione. **Non presentare «dì» o la virgola come una nuova soluzione TTS già collaudata**: il risultato riuscito è stato ottenuto con una pausa locale sui file esistenti.
- Non sostituire autonomamente 3D con «tridimensionale», «tre dimensioni» o altre spiegazioni nella lettura fedele. Distinguere la sigla da codici, nomi propri o formule che richiedono una lettura diversa.
- Conservare le regole X → «ics» /iks/, XR → «ics erre», con grafia TTS `ìks` / `ìks erre`, senza regredire alla vecchia pronuncia.

## Correzione locale di una lettura già generata

1. Individuare e contare ogni 3D nel documento e nel manifest; annotare ID, genere, parola seguente e posizione. Partire dall'ultima versione con X già corretta.
2. Se il problema è soltanto la separazione, **riutilizzare le voci esistenti**. Non generare altro audio, musica o copertina. Una richiesta di aggiornare le skill non autorizza neppure a rimontare il podcast già riuscito.
3. Lavorare sullo stem vocale PCM/WAV pulito. **Dal 2 novembre 2026 il podcast va montato sempre senza musica**; non usare vecchi mix come sorgente. Localizzare per ascolto il confine **dopo la vocale finale completa della D**, usando forma d'onda e spettrogramma quando necessario. L'ASR aiuta a trovare il passaggio, ma i suoi timestamp non certificano il confine fonetico.
4. Inserire soltanto una pausa breve al confine corretto. Nel caso approvato: **0,28 s per occorrenza**, tre occorrenze, **0,84 s aggiunti in totale**. È un riferimento di ritmo, non un tempo universale né un punto di taglio riutilizzabile su altri file. Non tagliare o ripetere fonemi, non applicare fade alle parole e non cambiare velocità o altezza.
5. Scegliere un punto a bassissima ampiezza vicino al confine già individuato, per evitare clic. **Il silenzio più vicino non basta**: può trovarsi prima della D anziché dopo. Nel primo tentativo questo errore lasciava la D ancora attaccata alla parola seguente.
6. Verificare l'integrità: togliendo dalla versione modificata le sole pause aggiunte, i campioni vocali originali devono risultare identici e nello stesso ordine. Controllare che ogni altro segmento, ogni `source_text`, la X corretta e la velocità 1,12× siano rimasti invariati.
7. Ascoltare ogni passaggio modificato nel suo contesto: «tre dì» deve finire prima della pausa e «generati»/«mostrati»/«filtri» deve iniziare intero dopo. Se il confine è sbagliato, correggere il montaggio locale, non rigenerare la voce. Se occorre davvero una nuova generazione, chiedere il consenso prima di procedere.
8. Rimontare **senza alcuna musica**, con la copertina approvata; ricalcolare i tempi dell'indice dalle durate effettive. Esportare il **podcast MP4 integrale**, preferendo il master WAV per l'AAC ed evitando ricodifiche MP3 superflue.

## Verifica finale obbligatoria

- Ascoltare **tutte le occorrenze di 3D nel video esportato**, non soltanto nelle anteprime WAV: D completa prima della pausa, parola successiva integra, niente «dimostrati», clic o distorsioni.
- Se le analisi degli estratti sono discordanti, ascoltare anche i corrispondenti intervalli del **MP4** con qualche secondo di contesto e confrontarli con lo stem e il confine acustico. Non segnare PASS per un'analisi inaccessibile o contraddittoria e non scegliere soltanto il responso favorevole.
- Ricontrollare X/XR nelle due voci, finale completo, assenza totale di musica, copertina leggibile, durata, loudness, picco reale e decodifica dell'AAC. Il solo codice di uscita 0 non certifica la pronuncia.
- Consegnare l'MP4 con copertina e indice aggiornato. Non rigenerare un risultato già riuscito e non sostituire la consegna con un MP3.

## Esempi di ascolto inclusi

Gli estratti seguenti sono copie pulite degli **stem vocali WAV corretti della v5**, prive di sottofondo. Dal 2 novembre 2026 sostituiscono nel pacchetto i vecchi campioni ricavati dall'AAC con musica:

- `templates/PRONUNCIA_3D_MASCHILE_GENERATI.wav`: «tre dì» separato da «generati».
- `templates/PRONUNCIA_3D_FEMMINILE_MOSTRATI.wav`: «tre dì» separato da «mostrati», senza fusione in «dimostrati».
- `templates/PRONUNCIA_3D_MASCHILE_FILTRI.wav`: «tre dì» separato da «filtri».

Usarli come riferimenti di ritmo e ascolto, non per imitare persone reali, non come ritagli da inserire in nuove frasi e non come prova che un nuovo audio sia corretto. Per file, durate, hash e posizioni del caso concreto leggere `references/caso-realta-virtuale-v5.md`.

