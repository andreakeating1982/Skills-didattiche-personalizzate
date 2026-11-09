# Schema del JSON contenuto (`contenuto.json`)

Questo file documenta lo schema del JSON che `clone_app.py` legge per generare la nuova app. Il modo più semplice per ottenerne uno valido è `clone_app.py --dump -o contenuto.json`, che estrae tutto il contenuto corrente della sorgente: poi si modificano solo i campi di testo.

## Struttura completa

```json
{
  "app": {
    "name": "nome-nuova-app",              // slug cartella (minuscolo, trattini)
    "title": "Mappa Concettuale Interattiva",  // <title> HTML
    "hubTitle": "LA LITERATURA DEL\nROMANTICISMO\nEN ESPAÑA",  // titolo centrale mappa (\n = capo riga)
    "pdfTitle": "MAPPA CONCETTUALE — ROMANTICISMO SPAGNOLO",
    "pdfBlankTitle": "MAPPA CONCETTUALE IN BIANCO — ROMANTICISMO SPAGNOLO",
    "pdfSlug": "Romanticismo"               // prefisso nomi file PDF
  },
  "audio": {
    "trackId": "romanticismo",              // chiave di AUDIO_TRACKS
    "trackTitle": "El Romanticismo en España",
    "src": "/audio.m4a",                    // non cambiare
    "file": ""                              // path assoluto file audio da copiare (opzionale)
  },
  "paragraphs": [ /* 4 elementi, vedi sotto */ ],
  "segments": [ /* 4 elementi, vedi sotto */ ],
  "map": {
    "imgW": 1376, "imgH": 768,
    "hub": { "cx": 687, "cy": 383, "w": 307, "h": 151 },
    "slots": [ /* 10 elementi: SOLO coordinate */ ],
    "paraBoxes": [ /* 4 elementi: label + coordinate */ ]
  },
  "image": { "file": "" }                  // path assoluto immagine sfondo da copiare (opzionale)
}
```

## `paragraphs[]`

Ordine = ordine dei rami della mappa. Ogni elemento:

```json
{
  "id": "parrafo2",                              // parrafo1..parrafo4
  "label": "2. POESÍA",                          // titolo CON numero
  "subtitle": "I tre più importanti poeti romantici spagnoli oltre al Duque de Rivas",
  "color": "#B8860B",                            // colore ramo (hex)
  "slots": ["JOSÉ DE ESPRONCEDA", "GUSTAVO ADOLFO BÉCQUER", "ROSALÍA DE CASTRO"],  // keyword corrette in ordine
  "audioStopAt": 109                             // secondo in cui fermare l'audio (ultimo = 999)
}
```

- La concatenazione di tutti i `slots` forma `ALL_KEYWORDS` (10 keyword totali).
- `TOTAL_SLOTS` viene calcolato automaticamente (somma degli slot).
- Il numero di slot per paragrafo deve restare 2-3-2-3 (cioè uguale alla sorgente) a meno di ricalcolare la geometria.

## `segments[]`

Ordine = stesso dei paragrafi. Ogni elemento:

```json
{
  "title": "Poesía",                              // titolo SENZA numero
  "text": "La poesía romántica española...",      // testo descrittivo (non mostrato nell'UI)
  "startTime": 58,
  "endTime": 109
}
```

- `segments.length` deve essere uguale a `paragraphs.length`.
- `segments[i].endTime` deve combaciare con `paragraphs[i].audioStopAt`.

## `map.slots[]`

Solo coordinate (10 elementi, in ordine di slot). Lo script **deriva** `slotId`, `rowId` e `keyword` dai paragrafi; qui servono solo le coordinate:

```json
{ "cx": 161, "cy": 133, "w": 180, "h": 74 }
```

Non serve specificare `slotId`/`rowId`/`keyword`: vengono generati automaticamente nell'ordine in cui appaiono.

## `map.paraBoxes[]`

Coordinate + etichetta del ramo (4 elementi, in ordine):

```json
{
  "label": "1. HUIDA HACIA\nLO IRRACIONAL",       // \n = capo riga
  "cx": 433, "cy": 195, "w": 194, "h": 86
}
```

`rowId` e `color` vengono **derivati** dai paragrafi (stesso colore del ramo).

## Esempio minimo (nuovo tema)

Cambiare solo il testo, lasciando le coordinate:

```json
{
  "app": {
    "name": "illuminismo-mappa",
    "title": "Mappa Concettuale — Illuminismo",
    "hubTitle": "LA LETTERATURA\nDELL'ILLUMINISMO\nIN EUROPA",
    "pdfTitle": "MAPPA CONCETTUALE — ILLUMINISMO EUROPEO",
    "pdfBlankTitle": "MAPPA CONCETTUALE IN BIANCO — ILLUMINISMO EUROPEO",
    "pdfSlug": "Illuminismo"
  },
  "audio": { "trackId": "illuminismo", "trackTitle": "L'Illuminismo in Europa", "src": "/audio.m4a", "file": "" },
  "paragraphs": [
    { "id": "parrafo1", "label": "1. LA RAGIONE",  "subtitle": "Il primato della ragione", "color": "#8B1A1A", "slots": ["RAZIONALISMO", "ENCICLOPEDIA"], "audioStopAt": 58 },
    { "id": "parrafo2", "label": "2. LA SCIENZA",  "subtitle": "Il metodo scientifico",     "color": "#B8860B", "slots": ["NEWTON", "GALILEO", "EMPIRISMO"], "audioStopAt": 109 },
    { "id": "parrafo3", "label": "3. LA POLITICA", "subtitle": "Le idee liberali",          "color": "#2E5E2E", "slots": ["MONTESQUIEU", "VOLTAIRE"], "audioStopAt": 175 },
    { "id": "parrafo4", "label": "4. L'ECONOMIA",  "subtitle": "Il liberismo",               "color": "#4A6FA5", "slots": ["ADAM SMITH", "FISIOCRAZIA", "MERCATO"], "audioStopAt": 999 }
  ],
  "segments": [
    { "title": "La ragione",  "text": "...", "startTime": 0,   "endTime": 58 },
    { "title": "La scienza",  "text": "...", "startTime": 58,  "endTime": 109 },
    { "title": "La politica", "text": "...", "startTime": 109, "endTime": 175 },
    { "title": "L'economia",  "text": "...", "startTime": 175, "endTime": 999 }
  ],
  "map": { /* identico a quello estratto con --dump */ },
  "image": { "file": "" }
}
```

## Costruire il JSON da testo libero

Quando l'utente dà solo un testo (argomento + parole chiave), procedi così:

1. Esegui `--dump` sulla sorgente per ottenere la geometria esatta (`map`, `imgW/imgH`).
2. Mantieni intatta la sezione `map` del JSON estratto.
3. Dividi il testo dell'utente in 4 paragrafi, ciascuno con 2-3-3-2… **attenzione**: il numero di keyword per paragrafo DEVE restare 2-3-2-3 per rispettare i 10 slot della mappa. Se l'utente dà un numero diverso di parole, ridistribuisci le keyword in slot da 2/3 in modo da totalizzare 10.
4. Assegna un colore a ogni paragrafo (riusa la palette: `#8B1A1A`, `#B8860B`, `#2E5E2E`, `#4A6FA5`).
5. `audioStopAt`/`endTime`: se non c'è un nuovo audio, mantieni i timestamp della sorgente; se c'è un nuovo audio, trascrivilo con `file_view` e individua i punti di stop (un segmento finisce PRIMA che il narratore dica il numero del paragrafo successivo).
