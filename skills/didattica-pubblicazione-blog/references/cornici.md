# Cornici Blogger e DOCX CODICI-EMBED-CORNICI

## Identificare l'oggetto

- HTML dentro una singola app: lavorare nel progetto app.
- Documento DOCX con codici numerati: lavorare sulla copia corrente dell'utente.
- App Cornice Universale: profilo distinto, iframe fisso senza height dinamico.
Non scambiarli anche se condividono parole o colori.

## Modificare il DOCX dei codici

1. Leggere documento attuale, indice Post del blog → Codici da usare e le
   parti per materia. Lo storico parla di16/17codici e slot14riutilizzati:
   non assumere che siano ancora liberi o associati alla stessa app.
2. Per nuova cornice scegliere slot realmente libero; per sostituzione
   conservare numero e modificare solo contenuto/titolo richiesti.
3. Estrarre l'HTML, modificare APP_URL/font/titolo con assert sul numero di
   occorrenze. Ricostruire la cella mantenendo Consolas7pt e hyperlink/indice.
4. Se richiesto dividere per materia e rinumerare da1IN OGNI file; mantenere
   una tabella di corrispondenza per non confondere numeri locali e globali.
5. Riaprire DOCX e provare HTML nel browser. Un falso COEP del dev server
   non basta a dichiarare l'embed errato: verificare same-origin/produzione.

## Conservare il protocollo reale

Token per istanza, filtro e.source e misure contenuto/anti-loop se previsti;
font OpenDyslexic self-hosted/CORS e nessun resize CSS con loop. Conservare
altri canali storici presenti nelle app. Se c'è microfono, iframe allow
microphone è necessario; non chiedere credenziali o aggirare permessi.
Non aggiornare automaticamente i post pubblici: modifiche/conferme separate.

## Fonte e risorse

Ricostruito da descrizione ed estratti chat: il23/10furono usate cornici reali
del blog e aggiunto allow microphone, ma questo non è un nuovo censimento.
Gli script originari estrai_codice.py, sostituisci_codice.py,
suddividi_in_parti.py e rinumera_parti.py NON sono disponibili qui; non
inventarli né affermare DOCX aggiornato senza aprire un file reale. Recuperare
l'originale per una sostituzione completa della skill precedente.
