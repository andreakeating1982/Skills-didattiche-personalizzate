# Quaderni inclusivi: creazione, restyling e allineamento palette

## Indice
- Scegliere entità dell'intervento
- Standard consolidato
- Allineare i colori a un'app
- Verifiche e risorse assenti

## Scegliere entità dell'intervento

Quaderno da PDF allegato: riferimento Pallavolo v2. Restyling di un quaderno
esistente: Rosalía v5. Rifinitura minima/indice/keyword: Shakespeare v4;
modifica di un solo elemento: modello Matematica Facile v7. Questi nomi
sono riferimenti recuperati, non file PDF allegati a questo pacchetto.
Non riscrivere contenuti e impaginazione per una semplice eliminazione di testo.

## Standard consolidato

OpenDyslexic, copertina con indice cliccabile, card crema #fffaf0 da frasi
complete (circa5righe massimo), keyword nere, box IN SINTESI e mappa finale.
Evitare pagine quasi vuote, card spezzate e testo fuori margini. Rispettare
la fonte, semplificare senza alterare concetti; usare supporti visivi pertinenti.
Non rendere grassetto tutto il testo. Non applicare al quaderno le restrizioni
senza-soluzioni di un modello di mappe diverso.

## Allineare i colori a un'app

1. Verificare la legenda pubblicata sia dal DOM/swatch sia dalle costanti
   nel bundle; non basarsi solo su un vecchio screenshot.
2. Registrare una palette unica di lavoro e mappare categorie. Non pubblicare
   l'app per cambiare un PDF.
3. Applicare a legenda, tag e marcature; per singolare/plurale usare le
   sfumature effettive e per passivo una sottolineatura visibile (il workflow
   storico usava border-bottom, non text-decoration). Ambigui/deponenti non
   verificati restano neutrali, non colorare a intuito.
4. Controllare colori vettoriali e contrasto nel PDF, confrontare testo e pagine.

Latino al29/10: avverbi #0057D9, preposizioni #BDBDBD, congiunzioni #4A4A4A,
altri modi #795548. Il grigio chiaro richiede un adattamento leggibile
coerente con il layout del quaderno; non assumere il fill su bianco accessibile.
La revisione dell'app8754 NON ha rigenerato i quaderni statici esistenti.

## Verifiche e risorse assenti

Puntare a PDF/UA-1, ma certificare solo con validazione effettiva. Controllare
font, tag, indice, testo, link e ordine di lettura oltre ai render. Per modifica
minima usare diff di testo pagina per pagina e confronto visivo.

Fonte parziale: descrizione ed estratti chat. Non sono stati recuperati
trasforma_card_intelligente.py, restyling_compatto.md, quaderno_6passi.md o
allineamento_colori_app.md originali. Questa scheda ne conserva le regole
note, non ne inventa l'implementazione. Recuperare gli originali prima di
disattivare la relativa skill o dichiarare riproducibilità esatta dei modelli.
