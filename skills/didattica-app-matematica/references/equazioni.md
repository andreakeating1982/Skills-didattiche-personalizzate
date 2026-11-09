# Equazioni e varianti del Widget Matematico

## Indice
- Manutenzione della sorgente o grado2
- Creare un grado diverso
- Input e PDF
- Copertura

## Manutenzione della sorgente o grado2

Equazioni Biquadratiche: /home/user/equazioni-biquadratiche, web-static,
BiquadraticExercises.tsx, NumberInputCanvas e useMathRecognition. La forma
è a*x^(2k)+b*x^k+c=0; sorgente k2. Secondo grado: profilo separato k1,
/home/user/equazioni-secondo-grado, cinque passi, React19/Tailwind4 secondo
la scheda corrente. Non trattare differenze di versione come errori.

## Creare un grado diverso

Usare scripts/widget-matematico-sorgente/clone_app.py --source PATH_O_REPO
--name SLUG --degree GRADO_PARI. Inizializzare il contesto nuovo prima del
clone. Il programma sostituisce token precisi, NON completa tutta la logica:
finire estrazione x da t e casi limite. Leggere references/widget-matematico-sorgente/
grado.md e disequazioni.md.

- t=x^k riduce a una quadratica in t; delta e formula in t non cambiano.
- k pari: t<0 non ha x reali, t>=0 richiede le radici ± salvo duplicazione zero.
- k dispari: radice reale unica per ogni t anche negativo; k1 non necessita
  sostituzione/estrazione. Non fare replace globali di 2,4,2a,4ac.
- Disequazioni: aggiungere verso, dominio, segni e intervalli; non basta
  sostituire = con >. La famiglia non copre qualsiasi polinomio arbitrario.

## Input e PDF

Verificare COMER encoder/decoder/vocab e WASM. Per il profilo grado2 la
patch ink-on numThreads=1 evita il blocco del modello: controllarla prima
di attribuire il problema alla UI. Non applicare patch cieche ad altre versioni.
Conservare NotebookGuide/RICOPIA derivazioni e ordine delle radici; usare
un solo array di record radice, non array paralleli disallineati.
Trascrivere forme incomplete SENZA zeri visibili e semplificare al massimo
radici esatte nel grado2. Verificare tutti i punti di rendering e il PDF.
Embed anti-loop/Welcome simmetrica; un 403/404 o falso COEP in dev non prova
che la pubblicazione sia rotta: controllare same-origin e bundle.

## Copertura

Sorgenti complete disponibili per biquadratiche e clone. Il profilo
secondo-grado è ricostruito dalla descrizione; il suo bundle e le patch
originali non sono inclusi. Non disattivare quell'originale prima del recupero.
