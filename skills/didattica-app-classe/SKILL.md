---
name: didattica-app-classe
description: "Creare, mantenere e clonare le app didattiche con classe/docente: Shakespeare/Parole Chiave, Bécquer/Quiz con audio, Immagine Interattiva/Romanticismo, Laboratorio Aumentato/3D, Mappe 3 e 6 passi e ascolto-abbinamento Espana XIX. Usare per dashboard, codici classe, sessioni, re-entry, contatori, report PDF, contenuti e cloni. Selezionare manutenzione o nuova app prima di intervenire. Non usare per app di calcolo/lingue né per creare PDF di mappe da esercizi: usare le rispettive skill didattica-app-matematica, didattica-app-lingue e didattica-documenti-accessibili."
---

# App di classe — un solo ingresso, profili mirati

## Selezionare un solo profilo

| App o richiesta | Riferimento |
|---|---|
| Shakespeare, Parole Chiave, quiz senza audio; domande nuove | [Quiz](../../shared/references/quiz.md) |
| Bécquer, quiz con pause e segmenti audio | [Quiz](../../shared/references/quiz.md), sezione audio |
| Immagine Interattiva, Romanticismo, hotspot e audio | [Immagini interattive](../../shared/references/immagini-interattive.md) |
| Laboratorio Aumentato, laboratorio 3D e rubrica in 6 passi | [Laboratori](../../shared/references/laboratori.md) |
| Costruttore di mappe in 3 o 6 passi | [Mappe interattive](../../shared/references/mappe-interattive.md) |
| Espana XIX: audio → puntino su linea del tempo | [Linee del tempo](../../shared/references/linee-del-tempo.md) |
| Script, template, dettagli storici per un bug specifico | [Inventario delle risorse](references/risorse.md) |

Non caricare tutte le schede. Se il nome è storico, risolverlo con
[alias e provenienza](references/copertura.md) o `python3 scripts/trova_profilo.py "nome app"`.

## Applicare il flusso comune

1. Identificare progetto e richiesta: correggere l'esistente oppure clonare
   cambiando contenuto. Per il clone non riscrivere o sovrascrivere la sorgente.
2. Leggere README/AGENTS e la scheda pertinente; verificare file e stack reali.
   Le vecchie cartelle/preview sono indizi, non un contesto di deploy attuale.
3. Conservare dashboard, codici numerici a 4 cifre, sessioni, rientro studente,
   conteggio attivi, report/PUNTEGGIO e palette del profilo selezionato.
4. Applicare un diff mirato. Cambiare contenuto tramite JSON/script appropriato,
   non replace globale. Non trasferire automaticamente credenziali o dati.
5. Eseguire tipi/test/build disponibili e verificare il flusso modificato,
   desktop/touch/iframe e report PDF. Dichiarare cosa è simulato o non provato.
6. Salvare checkpoint e consegnare preview; fermarsi. Produzione solo dopo
   esplicito consenso in un nuovo messaggio, col progetto di quella chat.

## Non mescolare contratti

- Non imporre Cambria a un profilo già OpenDyslexic; non uniformare colori o
  PDF fra app senza richiesta. La scheda specifica e il codice verificato
  prevalgono sulle indicazioni generiche dei vecchi archivi.
- Non trasformare la mappa a 3 passi in quella a 6; non aggiungere dashboard
  alla linea del tempo standalone. Non alterare il numero delle fasi del clone.
- Preservare i protocolli embed esistenti (labvisivo:height e, dove presenti,
  altri canali storici); non sostituire tutti con un unico messaggio.
- Test della classe: usare fixture o database separato. Mai reset/DELETE/seed
  distruttivi su dati veri per collaudare; anche i presunti dati di prova sono reali.
- Alcuni adapter storici sono deprecati: leggere avvertenze e --help; non
  invocarli alla cieca. La validazione sintattica non certifica un clone completo.
- Per ZIP, deploy e cornici usare didattica-pubblicazione-blog. Gli script
  originari sono inclusi, ma non sostituiscono l'inizializzazione del progetto
  prevista dall'ambiente né autorizzano migrazioni o pubblicazioni.

## Stato del riordino

I 16 profili di questa famiglia hanno sorgenti skill disponibili. Guide e
risorse originali sono conservate come dettagli a richiesta, non come altre
16 skill da attivare. Non affermare che tutte le app siano state ricollaudate
nel riordino: in questa attività sono stati verificati i pacchetti e gli script,
non tutte le applicazioni. Le skill generali di sistema restano separate.

