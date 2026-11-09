# Quiz, parole chiave e audio

## Indice
- Scegliere variante e operazione
- Preservare sessioni e report
- Script e verifiche

## Scegliere variante e operazione

| Richiesta | Profilo/script incluso |
|---|---|
| Manutenzione Shakespeare/Parole Chiave | originale shakespeare-quiz; server/questions.ts, StudentQuiz, TeacherPage, reportPdf |
| Nuova app PAROLE CHIAVE SORGENTE | scripts/parole-chiave-sorgente/rebuild_app.py |
| Nuova app QUIZ INTERATTIVO SORGENTE | scripts/quiz-interattivo-sorgente/clone_quiz_app.py |
| Manutenzione QUIZ CON AUDIO (Bécquer) | originale becquer-quiz |
| Nuova app QUIZ INTERATTIVO CON AUDIO SORGENTE | scripts/quiz-interattivo-con-audio-sorgente/clone_audio_quiz_app.py |

Non usare scripts/quiz-adapter/change_quiz_theme.py: è deprecato e cercava
vecchi token hardcoded nell'app sorgente. I change_quiz_theme.py accanto ai
DUE cloner sono invece versioni specifiche differenti: non sostituirli con
quello deprecato. Per manutenzione domande intervenire in modo mirato sulla
versione reale; non trattare un clone come aggiornamento automatico dell'app.

## Preservare sessioni e report

- Conservare codice classe a 4 cifre, chiusura/riapertura, avvio/stop,
  rientro con risposte bloccate, contatore studenti attivi e punteggi.
- Non confondere studenti presenti con tutti quelli mai registrati: leggere
  l'implementazione di sessionId/heartbeat e i relativi tempi prima di cambiare.
- Preservare nome centrato, hotspot/stati previsti dalla variante e sidebar;
  non applicare a tutte le app il colore di uno screenshot storico.
- Report: una pagina per studente ove previsto, PUNTEGGIO su 10 coerente con
  ponderazione e risposte, blocco non spezzato; verificare anche questionario
  in bianco, nomi lunghi, accenti e non date.
- PAROLE CHIAVE: mantenere MAPA1/2, vincoli degli 8 item e multi-risposta
  specifici del template. Un altro conteggio richiede adattamento esplicito.
- Audio Bécquer: mantenere pause lettura e segmenti; domanda nuda può essere
  nascosta allo studente (PREGUNTA n). Non mostrare la risposta in anticipo.
- Accessibilità richiesta nel profilo Parole Chiave: OpenDyslexic, 5 moduli,
  TTS, contrasto e righello; non reimporre il Cambria delle versioni iniziali.

## Script e verifiche

Eseguire --help prima di invocare un cloner e usare un JSON della variante
corretta. I template sono in templates/<nome-originale>/. Per i nuovi progetti
inizializzare prima il contesto previsto dall'ambiente; usare sorgente
sanificata e destinazione distinta, senza --force su file esistenti.
Verificare esclusione di .env, database e dati reali anche se lo script
storico non li filtra tutti. Non eseguire migrazioni/seed distruttivi.

Provare in fixture: crea/riapri classe → join → avvio → risposta → refresh/
re-entry → chiusura → report. Per audio provare cambio segmento e assenza di
sovrapposizione. Per mirror di file verificare entrambe le copie ove esistono.
Tipi/test/build e PDF, poi preview; deploy solo con nuovo consenso.

Dettagli su richiesta: references/originali/shakespeare-quiz.md,
becquer-quiz.md, parole-chiave-sorgente.md, quiz-interattivo-sorgente.md e
quiz-interattivo-con-audio-sorgente.md. La scheda schema-quiz-builder è un
archivio di bug strutturali, non un ordine di applicarli tutti.
