# Costruttori di mappe: 3 passi e 6 passi

Queste sono APP per costruire una mappa, non PDF di esercizi generati in chat.
Per quelli usare didattica-documenti-accessibili.

| Variante | Percorso storico | Passi |
|---|---|---|
| Mappa Concettuale | /home/user/mappa-concettuale | leggi/ripeti, appunti, hashtag, tronco, rami, immagini |
| Mappa 3 Passi | /home/user/mappa-3passi-preview | tronco, rami, foglie/immagini |

Verificare il progetto reale. File chiave: Home.tsx, lib/tipi-mappa.ts,
ConceptMapCanvas.tsx e index.css. Conservare titolo/rami/foglie configurabili,
PDF/PNG, dati studente e flusso proprio della variante.

## Evitare i bug noti

- Sei passi: completaMappa deve portare allo stato di rendering finale
  effettivo (storicamente currentStep=6, NON7).
- Tre passi: drag basato su ref, capture e requestAnimationFrame; non usare
  setState diretto a ogni pointermove che faccia perdere la presa. Callback
  recenti in ref, niente stale closure su endDrag.
- Preservare proporzioni/padding reali dei box, larghezza stimata e wrapping;
  non ridurre tutto il font per correggere un solo nodo lungo.
- Sfondo del canvas di stampa bianco; scaricare PDF/PNG con tutti gli elementi
  all'interno e senza alterare le posizioni dopo resize.
- Welcome embed: margini simmetrici, lf-welcome-top/lf-embedded se adottati;
  no min-height viewport che inneschi crescite. Mantenere il canale postMessage
  effettivo (mappaconcettuale:height o labvisivo:height secondo la versione).

Provare drag mouse/touch, nodi/immagini, resize, testo lungo, export e iframe.
Approfondimenti originali: mappa-concettuale.md e mappa-3passi.md.
