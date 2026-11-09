---
name: presentazione-app-docx
description: "Creare la presentazione DOCX scaricabile di un'app didattica per il blog dell'utente, nel suo stile personale (riferimento: il post dell'app di latino). REGOLA FISSA dell'utente — versione BREVE di massimo 15 righe in tutto, cioè titolo + UN paragrafo (~150 parole), niente immagini, box o sottosezioni a meno che richieste esplicitamente (la prima versione lunga con screenshot è stata rifiutata come «troppo lunga»). Usare per: presentare una nuova app, rifare o accorciare una presentazione, generare il DOCX con hyperlink cliccabile all'app. Include script python pronto (genera_presentazione.py). NON usare per i quaderni PDF didattici (skill quaderno-accessibile) né per i codici embed delle cornici (skill codici-embed-cornici)."
---

# Presentazione breve di un'app (DOCX, max 15 righe)

## Stile dell'utente (dal post di riferimento sull'app di latino)
Un unico paragrafo che segue questo filo, con le sue formule ricorrenti:
1. Apertura: «In questo post vi presento {Nome app}, un'applicazione web dedicata a {materia}, pensata per le classi della scuola secondaria: …»
2. Cosa fa, in modo concreto (tipologie/contenuti tra parentesi o dopo un trattino)
3. Inclusività con la formula «I colori non sono un semplice abbellimento: …» (OpenDyslexic, alto contrasto, righello di lettura…)
4. Utilità pratica: «…perfetto per il ripasso a casa o per il lavoro in classe»
5. Chiusura fissa: «L'indirizzo è {LINK}. Provalo anche tu e dimmi cosa ne pensi nei commenti.»

## Regole di impaginazione
- TITOLO centrato, grassetto, ~22pt, colore dalla palette dell'app. Nessun sottotitolo se non richiesto.
- UN solo paragrafo: Calibri 11.5pt, interlinea 1.2, A4, margini ~2.2–2.4 cm. Totale ≈ 150 parole ≈ 10 righe — MAI superare 15 righe (~220 parole).
- Colori: leggerli dal `:root` di `client/src/index.css` dell'app. Per le app con palette crema (Latino Facile, Inglese Facile) usare bordeaux #7B2D26 per il titolo e oro #8A6400 per gli accenti.
- Il link deve essere un hyperlink VERO cliccabile: `part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)` + elemento `w:hyperlink` (vedi script).
- Screenshot: SOLO se l'utente li chiede (versione lunga su richiesta esplicita).

## Script pronto
```
python scripts/genera_presentazione.py \
  --titolo "INGLESE FACILE" \
  --testo paragrafo.txt \
  --link https://english-workout-app.easy-peasy.site \
  --out Presentazione.docx \
  [--colore-titolo 7B2D26] [--colore-accento 8A6400] [--dimensione-titolo 22]
```
`--testo` è un file UTF-8 con il paragrafo completo; il token `{LINK}` viene sostituito con l'hyperlink cliccabile verso `--link`. Lo script stampa parole e righe stimate e avvisa se si supera il limite di 15 righe.

## Verifica prima di consegnare
- Riaprire il DOCX e controllare: parole ≈ 150, hyperlink presente (controllare i rel in `word/_rels/document.xml.rels`), zero immagini nella versione breve.
- Consegnare con send_attachment.
