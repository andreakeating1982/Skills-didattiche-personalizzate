# Espressioni 8744 — pacchetto riordinato e clonazione

Stato: runtime8744 invariato; audit documentale/distribuzione 29/10/2026.
Le guide correnti del repository prevalgono su originali e vecchio README.
Il caso di esportazione è dettagliato nella skill pubblicazione, riferimento
`audit-zip-github-render.md`; non duplicare qui gli strumenti di packaging.

## Mappa da non confondere

- WelcomePage → /espressione (EspressioniExercises, input) → costruzione IA
  in server/costruisci → /esercizio (EsercizioFrazioni, sessione sid e PDF).
- espressioni.ts/pdf.ts/mappaPdf.ts conservano anche percorsi locali storici:
  non attribuire soltanto a questi moduli il flusso universale e il PDF corrente.
- Clone identico: nuova app/repo, lockfile/patch e asset completi; baseline
  install/check/test/build prima delle variazioni; nuova chiave e proprio DB.
- Non copiare mai .env, shared/env.generated.ts, bundle server, sessioni o DB
  della sorgente. Copiare sync-env.mjs e rigenerare nel nuovo ambiente.

## Varianti: limiti onesti

Cambiare testi/lingua non crea un nuovo solver. La sostituzione t=x^k vale
per famiglie strutturate, non qualsiasi polinomio di grado arbitrario.
Disequazioni/fratte richiedono studio segno, domini e controllo sugli
originali; nuovi tipi di box richiedono verificatori, UI e PDF coerenti.
Per quiz scegliere sorgente con schema domande e dashboard appropriata:
questa app non li include. Non promettere una variante V/F con solo titolo.

## Invarianti

Mai dire la soluzione per iscritto/TTS; risultati soltanto dello studente,
validazione esatta. Frazioni impilate, puntino, parentesi fedeli, decimali
separati dalla normalizzazione. Conservare photo crop8731 modale con
hook/CSS/heightSync e seconda pagina con scroll limitato/toolbar esterna,
header8744, INDIETRO marrone e piece-display per formule lunghe.

## Verifica del pacchetto

Comandi reali: install frozen --prod=false (anche NODE_ENV=production),
pnpm check, Vitest da client, pnpm build. Baseline 738 passati /28 saltati;
14 test Python packaging sono separati. Confrontare tutti i file client,
non server compilato con segreti; test HTTP asset reali/header, IA503
senza chiave. Nessuna nuova IA live/DB/Render o prova fisica implicita.
Rapporto e hash finali consegnati insieme allo ZIP, non dedotti dallo storico.

Aggiornare soltanto le skill pertinenti: matematica e pubblicazione.
Non riscrivere le altre quattro tematiche per un audit della sola app.
La consegna di skill non è automaticamente l’aggiornamento nell’account.

