# Formato fisso della lettura (deciso dall'utente il 10/10/2026)

Riferimento gold standard: lettura della circolare «Consegna documentazione e caricamento sul registro elettronico Classeviva» (Istituto Magistrale "G. Milli" – Teramo, 01/10/2026).

## Struttura dell'audio

1. **NO intestazione**: mai leggere protocollo, codice fiscale/CM, nome istituto, indirizzo, telefono, sito, e-mail, destinatari («A tutti i docenti...»), data della circolare.
2. **INIZIO**: si parte dalla riga «Oggetto: ...».
3. **CORPO**: tutto il resto del documento verbatim, in ordine.
4. **FINE**: ultima frase = «Il Dirigente Scolastico, Dott.ssa/Dott. <Nome Cognome>.» — escludere SEMPRE la nota «Firma autografa omessa ai sensi dell'art. 3 c. 2 D.L. n. 39/1993» o simili.
5. Allegati/elencati dopo la firma: NON leggerli (chiedere all'utente).

## Adattamenti TTS (stessa frase, forma diversa)

| Nel PDF | Nello speech |
|---|---|
| `P.E.I.` / `P.D.P.` / `P.F.P.` | `PEI`, `PDP`, `PFP` (sigle senza punti) |
| `B.E.S.` | `BES` |
| date (`01/10/2026`, `30/11/2026`) | in lettere: «primo ottobre duemilaventisei», «trenta novembre duemilaventisei» |
| `art. 3 c. 2 D.L. n. 39/1993` | «articolo tre, comma due, del Decreto Legge numero trentanove del millenovecentonovantatré» |
| numeri a cifre nel corpo | in lettere |
| elenchi puntati | frase unica con pause (punti e virgole / frasi) |
| titoli di sezione (es. `PROGRAMMA`, `RELAZIONI`) | «La sezione PROGRAMMA contiene...» — lettura naturale, non letterale della tabella |

## Impostazioni voice

- `language: Italian`, `speed: 1`
- Voce consolidata: **Lorenzo Prada - Refined Italian Accent** (voce maschile; è quella usata nei file approvati dall'utente)

## Volume / loudness (richiesta fissa dell'utente, dal 10/10/2026)

Tutti gli MP3 prodotti dalla skill devono avere lo stesso volume, uniforme per l'intera durata del file. Si usa `scripts/normalizza_audio.sh` (loudness EBU R128 in due passate):

- Target: **I = -16 LUFS**, **TP = -1.5 dBTP**, **LRA = 11** — identico per ogni file, così tutti i file sono tra loro uniformi;
- applicare alla fine del workflow, DOPO l'eventuale concatenazione delle parti, SUBITO prima della consegna;
- verifica rapida (opzionale): `ffmpeg -i file.mp3 -af loudnorm=print_format=summary -f null - 2>&1 | grep "Input Integrated"` deve restituire circa -16.0 LUFS.

## Esempio di inizio testo speech

```
Oggetto: consegna documentazione e caricamento sul registro elettronico Classeviva.

Come previsto nel Piano delle attività, la data di consegna per le
programmazioni disciplinari individuali, per le programmazioni di classe,
per i PEI e per i PDP è fissata al trenta novembre duemilaventisei.
...
Il Dirigente Scolastico, Dottoressa Manuela Divisi.
```
