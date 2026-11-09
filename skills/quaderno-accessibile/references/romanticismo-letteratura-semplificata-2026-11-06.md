# ROMANTICISMO LETTERARIO — CONSEGNA E MAPPA SEMPLIFICATE, 6 NOVEMBRE 2026

## Richiesta dell'utente

Nel quaderno «LA LITERATURA DEL ROMANTICISMO EN ESPAÑA», la consegna precedente non rispecchiava la foto. L'immagine allegata indica **«Elige una sola respuesta para cada pregunta.»**; riprodurla esattamente in un box crema arrotondato, allineato a sinistra. Semplificare le domande e sintetizzare la mappa in meno riquadri, preservando dieci domande, una sola risposta corretta per ciascuna e la bibliografia finale. Non inserire nella mappa riferimenti alle attività.

## Revisione corrente — non dichiarata approvata

- [PDF completo](../templates/romanticismo-letteratura-semplificata-2026-11-06/LITERATURA_ROMANTICISMO_SEMPLIFICATA.pdf), 18 pagine, SHA-256 `0e9ec989a8082070454176c258574d7fdca7defec2b1918a735f45c6cbab5fb4`. È una revisione preparata su richiesta, senza attestare approvazione non dichiarata.
- Pagine 14–15: 10 domande in spagnolo, semplici e dirette, quattro opzioni. La chiave è solo nel JSON sorgente, non nel PDF; la consegna esatta è in un box come la foto `consegna-riferimento.png` nel template. Domande su caratteristiche, poesia, prosa e teatro, non sulle attività.
- Pagine 16–17: 8 box in due pagine invece dei 16 su quattro. Quattro argomenti mantenuti e riconoscibili: huida hacia lo irracional, poesía, prosa, teatro. Box da 78×78 mm, immagini di 52 mm, parole chiave in spagnolo; ogni box contiene una scena diorama. La sintesi elimina alcune parole chiave secondarie dalla mappa ma non cambia il testo del quaderno. Non trasformare 8 nodi in una quota universale.
- Pagina 18: le quattro fonti del PDF precedente, senza immagini e in box crema, prima fonte ripartita in due box; 12 note numerate nel testo puntano alle rispettive voci. Indice cliccabile aggiornato.
- Le sei sezioni del precedente quaderno, attività comprese, e i quattro riferimenti sono invariati. Non confondere questo quaderno di **letteratura** con l'altro quaderno del **marco histórico**. La vecchia versione di 21 pagine con domande non semplificate e 16 nodi è storica; vedere `romanticismo-letteratura-verifica-fonti-2026-11-06.md`.

## Materiali e riproducibilità

Il template include HTML finale, PDF, `impagina.py`, copia degli stili base, JSON editoriali, la foto della consegna e tutti gli asset usati (font OpenDyslexic e immagini). Da una copia del template:

```bash
python3 impagina.py
python3 /home/user/skills/quaderno-accessibile/scripts/render_sfondo_uniforme.py LITERATURA_ROMANTICISMO_SEMPLIFICATA.html nuovo.pdf
python3 /home/user/skills/quaderno-accessibile/scripts/verifica_quiz_fonti_obbligatori.py LITERATURA_ROMANTICISMO_SEMPLIFICATA.html --pdf nuovo.pdf --expected-instruction 'Elige una sola respuesta para cada pregunta.'
```

L'ultimo comando richiede il selettore `.quiz-intro` e confronta il testo con esattezza; usare l'opzione soltanto quando la consegna attesa è specificata. Per altre lingue adattare il testo e passare la traduzione scelta; non imporre la lingua spagnola a tutti i documenti.

## QA e limiti

- Due ispezioni visive delle domande e dei 2 fogli di mappa. Verifica computazionale di 10 quesiti × 4 alternative, numerazione, esattezza consegna, 8 nodi, immagini, 4 fonti e 12 destinazioni bibliografiche. Confronto strutturale delle sei sezioni e della bibliografia con la revisione precedente; geometria: nessuna riga dei box esce dal bordo. Verificare anche il significato e l'unicità delle risposte manualmente.
- La semplicità è richiesta per questo quaderno; non modificare automaticamente le domande approvate di Rosalía o di altri lavori e non attribuire tale livello a ogni futura verifica. La mappa è una sintesi, non un sostituto del testo completo. I controlli non certificano conformità PDF/UA o diritti sulle immagini.

