---
name: didattica-app-matematica
description: "Mantenere e clonare le app matematiche accessibili: Equazioni Biquadratiche, Equazioni di Secondo Grado, Operazioni con le Frazioni/math-input-panel, Espressioni Monomi e Polinomi/Widget Metacognitivo e Widget Matematico Sorgente. Usare per passi guidati, scrittura ONNX/ink-on, riconoscimento, motore esatto, decimali italiani, foto, NotebookGuide, PDF e varianti di grado/disequazioni. Non usare per PDF di mappe richiesti in chat: usare didattica-documenti-accessibili; per deploy e ZIP usare didattica-pubblicazione-blog."
---

# App di matematica — cinque profili, tre schede

| Richiesta | Leggere |
|---|---|
| Equazioni di grado 2/4; nuovo grado o disequazioni | [Equazioni](references/equazioni.md) |
| Addizione/sottrazione, moltiplicazione/divisione frazioni | [Frazioni](references/frazioni.md) |
| Espressioni, monomi/polinomi, widget metacognitivo e foto | [Espressioni](references/espressioni.md), [layout e pacchetto8756](references/espressioni-8756.md) |
| Script, template, dettagli precedenti | [Risorse](references/risorse.md) |
| Nomi precedenti e disponibilità delle fonti | [Copertura](references/copertura.md) |

Risolvere l'alias senza caricare tutte le schede:
`python3 scripts/trova_profilo.py "secondo grado"`.

## Prima di modificare

1. Distinguere manutenzione dell'app corrente e NUOVA variante. Verificare
   progetto/README/AGENTS; non usare la chat di Latino per pubblicare un'altra app.
2. Individuare separatamente parser, calcolo, validazione, rappresentazione
   LaTeX, input manoscritto e guida pedagogica: un difetto UI non autorizza
   a riscrivere il motore o a cambiare le risposte accettate.
3. Conservare contenuti e filosofia del profilo. Nel widget metacognitivo
   non anticipare la soluzione, nemmeno in testo scritto o TTS.
4. Per nuova app inizializzare il progetto corretto; scegliere un backend
   se usa IA/API. Gli script di clonazione non creano un nuovo contesto deploy.

## Invarianti da rispettare

- IA propone, motore dispone: auditare conti e passaggi; non validare un
  risultato perché lo ha scritto l'IA. Usare verifiche deterministiche.
- Conservare virgola decimale e separare trascrizione fedele da normalizzazione
  per il calcolo. Non trasformare 2,5 in 25 o una frazione in una sottrazione.
- Mai sostituire globalmente cifre 2/4 per cambiare grado: romperebbe 2a/4ac.
- Verificare condizioni di esistenza, denominatori nulli, radici negative,
  segni e grado effettivo; non presentare la formula del clone come universale
  per equazioni di qualsiasi forma.
- ONNX: verificare modello/WASM, caricamento ed errori reali; non toccare la
  geometria di input per correggere testo, font o scroll.
- PDF: verificare frazioni, radici esatte, wrapping, margini e corrispondenza
  con RICOPIA SUL QUADERNO. Non trasferire font/formato di un'altra app.
- Se si trapianta il cropper, portare hook/CSS/heightSync: vedere la scheda
  espressioni e il riferimento del crop in didattica-app-lingue.

## Collaudo e rilascio

Eseguire tipi/test/build pertinenti; provare casi esatti e limite, mobile,
input/riconoscimento e PDF. Registrare separatamente motore reale e IA mock.
Non cambiare dati di produzione per fare test. Checkpoint → preview condivisa
→ fermarsi → consenso in un nuovo messaggio → checkpoint → produzione.
Usare didattica-pubblicazione-blog per ZIP e documentazione ricostruibile.

## Copertura e precedenza

Sono disponibili le cartelle complete di equazioni-biquadratiche,
math-input-panel e widget-matematico-sorgente. Il profilo Espressioni è
aggiornato alla produzione8756: pagina2 a640px, pagina3 adattiva fino a640px,
con scroll interno e toolbar fuori. Leggere `references/espressioni-8756.md`;
gli originali8744 e il loro audit sono conservati come cronologia.
Per equazioni-secondo-grado mancano ancora gli allegati originali; conservarli
se disponibili altrove prima di disattivare la vecchia skill.
Le guide correnti prevalgono sugli originali datati: nuova variante non
significa solver di qualunque grado né quiz già implementato.

