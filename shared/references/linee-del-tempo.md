# Linea del tempo: ascolto → abbinamento

Profilo Espana XIX Match: app web-static senza dashboard o DB. Per nuova
attività copiare contenuto/risorse in un nuovo progetto, mantenendo macchina
a stati e accessibilità. Non aggiungere sessioni docente.

## Dati e script

Compilare templates/espana-xix-match/app-config.json e usare
scripts/espana-xix-match/adatta_app.py --config FILE --root DEST --dry-run.
Lo script aggiorna dati eventi, titoli, dimensioni e riferimenti; controllare
il diff prima dell'esecuzione reale. Per una nuova app non puntare --root
alla sorgente. id univoci, coordinate percentuali e MAP_W/H coerenti.

## Contratto corrente

- Un solo canale audio attivo; ended/error devono liberare la coda.
- Pin allineati all'area dipinta dell'immagine con object-fit:contain.
- Preservare accessibilità italiana, TTS auto-lingua, pause/ordinali, righello,
  contrasto e OpenDyslexic self-hosted di UI/immagine/PDF. I font Cambria dei
  primi appunti sono storici: verificare versione prima di applicarli.
- PDF con icone sopra asse, margini circa3cm e senza istruzioni se così richiesto.
- Finale Actividad completada sopra la barra, titolo responsive, senza
  pulsante PDF nell'overlay.
- Cornice v3: token/ping, font WOFF2-v2 e CORS; preservare i protocolli
  labvisivo:height e romanticismo:height dove realmente presenti.
- Cache busting di immagini/audio sostituiti; h1/title/alt coerenti.

Provare intro, ascolto, errore/corretto, fine, dispositivo touch e iframe.
La cartella completa della skill è disponibile; le indicazioni nuove sopra
vengono dalla descrizione corrente e precedono lo storico archiviato.
Dettagli in references/espana-xix-match/architettura.md e originale.
