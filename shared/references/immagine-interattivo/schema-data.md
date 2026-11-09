# Schema Data Reference

Copia fedele di `server/schema-data.ts` — definizione autoritativa dei paragrafi e keyword.

## ALL_KEYWORDS (10 parole)

```typescript
export const ALL_KEYWORDS: string[] = [
  "COSTUMBRISMO",
  "INDIVIDUALISMO",
  "JOSÉ DE ESPRONCEDA",
  "GUSTAVO ADOLFO BÉCQUER",
  "ROSALÍA DE CASTRO",
  "ARTÍCULOS DE COSTUMBRES",
  "MARIANO JOSÉ DE LARRA",
  "AMOR IMPOSIBLE",
  "DUQUE DE RIVAS",
  "JOSÉ ZORRILLA",
];
```

## PARAGRAPH_ROWS (4 paragrafi, 10 slot totali)

| id | Label | Subtitle | Color | Slots | audioStopAt |
|---|---|---|---|---|---|
| parrafo1 | 1. HUIDA HACIA LO IRRACIONAL | Le due tendenze e i tratti comuni del Romanticismo | #8B1A1A | COSTUMBRISMO, INDIVIDUALISMO | 58s |
| parrafo2 | 2. POESÍA | I poeti romantici: dal Duque de Rivas a Bécquer e Rosalía | #B8860B | JOSÉ DE ESPRONCEDA, GUSTAVO ADOLFO BÉCQUER, ROSALÍA DE CASTRO | 109s |
| parrafo3 | 3. PROSA | Il ritorno del genere narrativo: Larra e Bécquer | #2E5E2E | ARTÍCULOS DE COSTUMBRES, MARIANO JOSÉ DE LARRA | 175s |
| parrafo4 | 4. TEATRO | Il dramma romantico: amor imposible, fuerza del sino | #4A6FA5 | AMOR IMPOSIBLE, DUQUE DE RIVAS, JOSÉ ZORRILLA | 999s |

**TOTAL_SLOTS = 10**

## Struttura tipi

```typescript
interface ParagraphRow {
  id: string;              // "parrafo1"..."parrafo4"
  paragraphLabel: string;  // Titolo completo col numero
  paragraphSubtitle: string;
  color: string;           // Hex colore
  slots: string[];         // Keyword corrette in ordine
  audioStopAt: number;     // Secondo in cui fermare l'audio
}
```

## Note

- `audioStopAt: 999` per l'ultimo paragrafo significa "fine traccia".
- I timestamp devono corrispondere a `audioData.ts` (`startTime`/`endTime`): par.1=58s, par.2=109s, par.3=175s, par.4=999.
- Le keyword usano caratteri speciali spagnoli (accenti, ü) — MAI rimuoverli.
- ⚠️ I confini audio sono sincronizzati: ogni paragrafo finisce PRIMA che il narratore pronunci il numero del successivo.
