# Coerenza UI cross-app (app didattiche)

Checklist delle modifiche di armonizzazione applicate alle app derivate dall'app sorgente "Mappa Concettuale Interattiva" (romanticismo). Riapplica quando crei una nuova app o allinei più app tra loro.

## Pulsanti e sottotitoli in MAIUSCOLO

Tutti i pulsanti di azione e i sottotitoli principali in maiuscolo, es. "AREA DOCENTE", "AREA STUDENTI", "CREA UNA NUOVA CLASSE", "INSERISCI IL CODICE FORNITO DAL DOCENTE...".

## Titoli Quiz distinti

Le app quiz "con audio" e "senza audio" devono avere H1 distinti ("QUIZ INTERATTIVO CON AUDIO" / "QUIZ INTERATTIVO SENZA AUDIO") nella Home e in tutte le schermate dello studente.

## Home uniforme

Titolo/header della Home allineato allo stile comune (maiuscole, punteggiatura uniforme).

## Header docente responsive (mobile)

Pulsante "AREA STUDENTI" e titolo centrati su mobile:

- header: `flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3`
- H1 con `text-center`
- pulsante con `mx-auto sm:mx-0`

## Casella studente (dashboard docente)

Allineata alla mappa concettuale: layout, tooltip del nome posizionato sopra (`side="top"`) e in MAIUSCOLO (`.toUpperCase()` dentro e fuori il tooltip), pallini, pulsante "rimuovi".

## Menu risposte corrette/errate

Dropdown/elenco risposte del docente allineato allo stile della mappa; leggibile su mobile (wrap invece di truncate).

## Fix rientro studente (anti-duplicati)

Normalizzare il nome studente (minuscole, accenti, spazi) prima del confronto, così un alunno che rientra con lo stesso nome completo recupera identità e risposte precedenti senza creare un duplicato.

## Pulizia file duplicati morti

Rimuovere eventuali copie duplicate "morte" alla radice della repo (es. `StudentQuiz.tsx`, `TeacherPage.tsx`, `questions.ts`, `reportPdf.ts`, `routers.ts`) quando esistono le copie vere in `client/src/…` e `server/…`. Verificare sempre con `git status` e con il build prima di rimuovere.

## Regole di preservazione (mai rimuovere)

- Non rimuovere MAI funzionalità esistenti: solo aggiungere elementi di inclusività, correggere glitch UI e adattare stile mappa/formattazione PDF.
- Preservare: meccaniche esatte, flusso di controllo docente, logica del generatore PDF, font Cambria, tooltip in maiuscolo, regole di layout, accessibilità.

## Convenzioni repo GitHub

Le repo esportate seguono il pattern `github.com/andreakeating1982/{nome-app}`. Le 6 app armonizzate: `COME-COSTRUIRE-UNA-MAPPA-CONCETTUALE-IN-3-PASSI`, `LABORATORIO-AUMENTATO-3D`, `PAROLE-CHIAVE-INTERATTIVE`, `QUIZ-INTERATTIVO-CON-AUDIO`, `QUIZ-INTERATTIVO-SENZA-AUDIO-SHAKESPEARE`, `SCHEMA-INTERATTIVO`.
