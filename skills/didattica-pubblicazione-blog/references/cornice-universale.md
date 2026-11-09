# App Cornice Universale — stato sincronizzato e iframe fisso

## Contratto corrente

La descrizione corrente prevale sullo storico: OpenDyslexic auto-ospitato
ovunque; viste Documento/Lettura testo, cerca parole, TTS e pannello
accessibilità in6gruppi su2colonne centrate. Password/Nascondi/Mostra,
focus gestito, aria-label/pressed/expanded/controls, group/status e live
region come appropriati. Messaggio nascosto ESATTO:
DOCUMENTO MOMENTANEAMENTE NON DISPONIBILE, maiuscolo e senza sottotesto.

Niente cornice dinamica: il codice labvisivo:height/embed.html è stato rimosso
su richiesta; mantenere l'iframe fisso. Lo storico Cambria e il vecchio ZIP
che perdeva il lockfile sono superati. Non diffondere la password storica.

## Modifica e sincronizzazione

Progetto storico /home/user/cornice-universale, Vite/React/TS/Tailwind più
Express; verificare cartella/README attuali. La password se hardcoded va
allineata nei DUE file Home.tsx e server/index.ts: leggere/configurare il
valore autorizzato, non copiarlo da questa skill. Una password nel client
non protegge realmente un PDF pubblico: non descriverla come cifratura.

GET/POST /api/state gestiscono hidden; polling nel client, rollback se POST
fallisce. L'implementazione storica usa memoria del processo: reset al riavvio
e incoerenza possibili fra più istanze; verificare codice/deploy corrente
prima di promettere sincronizzazione persistente su tutti i dispositivi.
Per modificare un sistema che chiama API automaticamente leggere anche la
skill generale automation-and-scheduling; non crearvi una schedulazione se
serve solo la sincronizzazione dell'app.

## Verifica e distribuzione

Serve server Node, non hosting statico, per /api/state. Provare due contesti
browser separati, password errata/corretta, nascondi/mostra, cambio vista,
TTS/ricerca, tastiera/screenreader e layout mobile. Non mostrare password nei
report o inserirle nei pacchetti. ZIP pulito con lockfile, README,
ACCESSIBILITA e configurazione Render attuali; preview e nuovo consenso
prima di produzione. L'originale completo è conservato come storico redatto.
