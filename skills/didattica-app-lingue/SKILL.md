---
name: didattica-app-lingue
description: "Mantenere Latino Facile, Lingue Facili (inglese/francese/spagnolo, solo-riordino), la precedente Francese Facile e Mappe Concettuali di Lingue Straniere. Usare per UI studente, testo/foto/OCR, cropper mobile clonabile, accessibilità, TTS, esercizi, colorazione grammaticale, traduzione e PDF. Latino pubblicato 8754: avverbi blu, preposizioni grigio chiaro, congiunzioni grigio scuro; crop baseline 8731 invariato. Non usare per quaderni/mappe PDF richiesti in chat (didattica-documenti-accessibili), né per quiz con dashboard docente (didattica-app-classe)."
---

# App di lingue — profili separati, conoscenza condivisa

| App o problema | Leggere |
|---|---|
| LATINO FACILE: analisi, colori, PDF, traduzione | [Latino Facile aggiornato](../../shared/references/latino-facile.md) |
| Palette app/PDF e enclitiche | [Palette pubblicata 8754](../../shared/references/latino-facile/palette-8754.md) |
| Crop touch/iframe, pagina dietro ferma | [Ritaglio mobile](../../shared/references/latino-facile/ritaglio-mobile.md) |
| Clonare SOLO il cropper in un'altra app | [Foglio autonomo con 18 sorgenti](../../shared/references/latino-facile/photo-crop-clonabile.md) |
| LINGUE FACILI: riordino inglese/francese/spagnolo | [Lingue Facili](../../shared/references/lingue-facili.md) |
| Vecchia app FRANCESE FACILE | [Profilo precedente](../../shared/references/francese-facile.md) |
| MAPPE CONCETTUALI DI LINGUE STRANIERE, app | [Mappe Lingue](../../shared/references/mappe-lingue.md) |
| Fonti, script e alias | [Risorse](references/risorse.md), [copertura](references/copertura.md) |

Caricare solo la scheda necessaria. Per un nome storico usare
`python3 scripts/trova_profilo.py "latino"`.

## Procedere senza regressioni

1. Verificare progetto corrente, README/AGENTS e app precisa; la presenza
   della scheda non cambia il contesto di deploy della chat.
2. Applicare solo la richiesta: non unificare automaticamente contenuti,
   modelli di esercizio, titolo, legenda o formati PDF delle diverse app.
3. Conservare font auto-ospitati/accessibilità, testi italiani della barra,
   lingua corretta di esercizi/TTS, touch e tastiera; provare anche iframe.
4. Conservare foto normalizzata → ritaglio → trascrizione → conferma prevista
   dal profilo. Non confondere modifica visiva e output ritagliato.
5. Allineare la modifica a UI, scelta manuale, PDF, legenda e guide pertinenti.
   Un quaderno statico non cambia quando cambia il generatore PDF dell'app.
6. Verificare tipi/test/build e il comportamento specifico; non esporre chiavi,
   non copiare .env da altre app né modificare dati reali per testare.

## Non perdere le decisioni consolidate di Latino

- Produzione 8754, runtime 5fbfc61; URL stabile latino-facile-app-2.easy-peasy.site.
- Avverbi #0057D9; preposizioni #BDBDBD; congiunzioni #4A4A4A. Fonte unica
  SERVICE_COLORS; testo chip adattato, contorno PDF chiaro 0,35pt #595959,
  q/Q isolato; didascalie via legendExplanationColor.
- APP enclitiche attaccate, contorno base e nero/bianco opposto. PDF -cum
  chiaro, -que/-ve/-ne scuro secondo legenda.
- Crop baseline autonoma 8731: titolo RITAGLIA LA FOTO senza icona/istruzioni,
  drag diretto; modal=true, scroll interno, lock pagina, viewport iframe.
  Non modificare confirm() o cropBox per correzioni di layout.
- 8754: 84 test, 2 scenari colori UI, 6 PDF, 4 drag e backend reale con palette.
  UI IA simulata e touch emulato: non promettere nuova accuratezza linguistica.
- Non riportare come correnti sconosciuti bianchi, vecchi grigi, CHUNK_SIZE 2,
  modal=false del ritaglio o i pulsanti del quaderno storico.

## Pubblicare solo quando autorizzato

Checkpoint → preview condivisa → fermarsi → nuova conferma → checkpoint →
produzione. Skill/ZIP aggiornati non sono consenso al deploy. Per il flusso
completo usare didattica-pubblicazione-blog.

## Disponibilità

Latino ha sorgenti skill e risorse complete qui disponibili. Lingue Facili,
Francese Facile e Mappe Lingue hanno profili ricostruiti dalle descrizioni
(e per Lingue anche da estratti chat), senza tutti gli allegati originali.
Non cancellare quei tre originali fino al recupero e alla verifica delle
risorse mancanti. Le skill generali di sistema non sono sostituite.

