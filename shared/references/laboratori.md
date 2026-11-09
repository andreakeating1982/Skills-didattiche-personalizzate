# Laboratorio Aumentato e Laboratorio Aumentato 3D

## Distinguere le due app

Laboratorio Aumentato e Laboratorio Aumentato 3D SORGENTE condividono schemi
di aula ma non sono intercambiabili. Il progetto 3D era laboratorio-visivo;
verificare contesto e README, non pubblicare un altro servizio da questa chat.

## Manutenzione

Conservare crea/riapri/chiudi/elimina classe, rubrica, conteggi e report. Nel
3D la struttura è di SEI passi: tema/dati iniziali, materiali, elaborato
visivo (foto), spiegazione scritta, audio lettura e audio spiegazione secondo
il template reale. Non trasformarla in un quiz. Chiusura e riavvio cambiano
isActive; non cancellare consegne per simulare uno stato chiuso.

RIAPRI: validare al click con feedback, non disabilitare per input vuoti se
il profilo lo prevede. Eliminazione con conferma; sidebar informativa,
input/data centrati con overlay ove presente. Non reintrodurre schermate
legacy non instradate. Palette plum/gold/success propria dell'app.

## Nuovo laboratorio 3D con altro contenuto

Usare scripts/laboratorio-aumentato-3d-sorgente/clone_app.py con --source,
--dest, --title e --config. Modello in templates/laboratorio-aumentato-3d-sorgente/.
Modificare tema, istruzioni dei sei passi e label/descrizioni della rubrica;
lasciare invariate le chiavi collegate alle colonne DB e tutte le API.
Non applicare --force, tar o migrazioni a una destinazione con dati esistenti.

Verificare titoli/meta, chiave localStorage distinta, nessun residuo del tema,
consegna/upload/audio, valutazione e PDF. Provare chiusura/riapertura su fixture.
La clonazione non autorizza copia di .env/database né produzione automatica.
Dettagli: originali laboratorio-aumentato, laboratorio-aumentato-3d e
laboratorio-aumentato-3d-sorgente.
