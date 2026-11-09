# STANDARD APPROVATO — 2 NOVEMBRE 2026

Leggere `../../references/sintesi-e-mappa-finale.md`. Sintesi tabellari a due colonne, tutte le righe necessarie, **NESSUN GRASSETTO anche in IN SINTESI/IN SHORT e nelle parole chiave**: ogni testo deve essere Regular400. Neretti del corpo conservati.

Mappe = modello Realtà Virtuale v6 approvato: **tutti i box78×78mm**, due colonne, ultimo nodo dispari centrato e mai allargato; solo poche **PAROLE CHIAVE**, immagini clay adulte interne **52×29,373mm**. Nessuna frase discorsiva, connettore o fascia riquadrata a tutta larghezza. Titolo esatto MAPPA CONCETTUALE FINALE. Stessa dimensione del corpo e interlinea **1,85**. Se non entra, usare altri nodi/pagine; mai allargare i box o ridurre la tipografia.

```sh
python3 ../../scripts/integra_sintesi_mappe.py base.html integrazioni.json nuovo.html
python3 ../../scripts/verifica_specchietti_box.py nuovo.html integrazioni.json --report QA.json
python3 -m unittest discover -s ../../tests -v
```

Output NUOVO, nessuna API. `esempio-completo.html` è già integrato. Copiare l’intera `templates/` per conservare font e immagini. Percorsi immagini nel JSON relativi all’HTML. `summaries`: `{id,color,rows:[[PAROLA CHIAVE,SPIEGAZIONE]],lang}`; frasi ammesse nelle spiegazioni, non Bold. `maps`: `{id,root,groups:[{title,nodes:[{title:[RIGA1,RIGA2],keywords:[CHIAVE1,CHIAVE2]}],images:[{src,alt}],new_page:true}]}`. Anche immagine/colore possono essere dati nel singolo nodo con `image:{src,alt}` e `color`. Tutte le immagini obbligatorie. Il vecchio `[TITOLO,TESTO]` resta compatibile solo con espressioni brevi, mai spiegazioni.

Non importare `intro`/`notes` discorsivi nella mappa; conservarne i dettagli nel corpo o nelle sintesi. Niente auto-riassunti/troncamenti: preparare e leggere le parole chiave. I controlli di lunghezza non dimostrano da soli che una sequenza breve non sia una frase.

Manifest: `unit_ids`, `final_map_ids`, `body_font_size_px`, `body_line_height`, misurati dai paragrafi ordinari. Nel modello 13pt e1,85; nel documento delle metodologie preservare14pt, distribuendo i concetti su altri box/pagine se necessario. Per il corpo vale il suo profilo, non il limite fisso dei nodi di mappa. Titoli in maiuscolo e colori preservati, nessuna immagine nelle fonti o nelle sintesi.

`standard-approvato-2026-11-02.json` registra misure e provenienza; le due vecchie foto sono storiche e superate per grassetto/dimensioni mappe. I test coprono Regular400 per tutta la sintesi, CSS inline/ereditato, b/strong, integrità neretti del corpo, nodi dispari, dimensioni/overflow, immagini e frasi rifiutate. Ispezionare anche il PDF reale. L’aggiornamento della skill non aggiorna automaticamente PDF o ZIP consegnati prima.

