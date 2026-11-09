# Audio Data Reference

Copia dei 4 segmenti audio in `client/src/lib/audioData.ts`.

## Segmenti

| id | Titolo (SENZA numero) | startTime | endTime |
|---|---|---|---|
| 0 | Huida hacia lo irracional | 0s | 58s |
| 1 | Poesía | 58s | 109s |
| 2 | Prosa | 109s | 175s |
| 3 | Teatro | 175s | 999s |

Il player si stoppa automaticamente a `endTime` di ogni segmento. `999` = fine traccia.

⚠️ I confini sono sincronizzati per evitare che il numero del paragrafo successivo venga pronunciato nel segmento sbagliato:
- Segmento 0 finisce a 58s (prima di "2. Poesía" a 58.3s) → Segmento 1 include "2. Poesía" completo
- Segmento 2 finisce a 175s (prima di "4. Teatro" a 175.4s) → Segmento 3 include "4. Teatro" completo

## Struttura tipi

```typescript
interface AudioSegment {
  id: number;
  title: string;     // SENZA numero davanti
  text: string;      // Testo descrittivo (non usato direttamente nel player)
  startTime: number; // secondi
  endTime: number;   // secondi
}

interface AudioTrack {
  id: string;
  title: string;
  src: string;       // percorso relativo in /public
  segments: AudioSegment[];
}
```

## Regole

- I titoli NON devono avere il numero del paragrafo (es. "Huida hacia lo irracional", NON "1. Huida hacia lo irracional").
- I timestamp di `audioData.ts` devono coincidere con `audioStopAt` in `schema-data.ts` (par.1=58, par.2=109, par.3=175, par.4=999).
- Il file audio fisico è `client/public/audio.m4a` (copia da upload).
- Se si aggiungono/rimuovono segmenti, aggiornare anche `schema-data.ts`.
- Per risincronizzare: trascrivi l'audio con `file_view`, individua i punti esatti in cui il narratore dice i titoli, e sposta i confini di conseguenza.
