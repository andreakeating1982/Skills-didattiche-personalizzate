# Latino Facile — architettura attuale (29/10/2026)

## Indice
- Stato e fonti
- Mappa file
- Flussi
- Embed e ritaglio
- Verifiche e limiti

## Stato e fonti

App pubblicata 8754, runtime 5fbfc61fc64036b442bca07703162cd70f1d28a3,
URL https://latino-facile-app-2.easy-peasy.site. Il checkpoint e48e24c aggiorna
solo le note. La baseline del photo cropper resta 8731: non imporre la
coincidenza fra rilascio app e rilascio di un componente invariato.
Leggere README/AGENTS/REBUILD/ADATTARE/ACCESSIBILITA/manifest della repo.

## Mappa file

| File | Ruolo |
|---|---|
| client/src/pages/WelcomePage.tsx | `/`, dati studente e ingresso |
| client/src/pages/Home.tsx | `/app`, MAX_PAROLE=50, token, legenda, override, traduzione, foto e PDF |
| shared/types.ts | CASE/MOOD/POS/SERVICE_COLORS, LEGEND_ITEMS, colorForEnclitic, legendExplanationColor, shadeForNumber |
| client/src/lib/export.ts | pdf-lib/fontkit, OpenDyslexic, segmenti base/suffisso, contorno grigio chiaro, traduzioni e pagine |
| client/src/components/CropDialog.tsx | Ritaglio free-box modale con drag diretto |
| client/src/hooks/useCropDialogViewport.ts | Viewport autonomo/iframe, lock e ripristino |
| client/src/lib/cropBox.ts | Geometria; non cambiare per correggere UI/scroll |
| client/src/lib/heightSync.ts | labvisivo:height, lf-embedded e sospensione durante crop |
| client/src/index.css | Tema, font, accessibilità, regole crop/iframe |
| client/src/contexts/AccessibilityContext.tsx | Preferenze testo/interlinea/righello/contrasto |
| client/src/components/AccessibilityToolbar.tsx | Barra accessibilità |
| client/src/hooks/useReadAloud.ts | TTS |
| client/src/lib/aiTranscribe.ts | Riduzione immagine per IA e controllo trascrizione |
| server/analyzer/aiTranscribeLatino.ts | POST /api/ai/transcribe; non la vecchia mutation latino.foto |
| client/src/lib/ocr.ts, imagePrep.ts | Ripiego Tesseract ed EXIF |
| server/routers.ts | Analyze e translate |
| server/analyzer/index.ts | Analisi morfologica e colori delle opzioni |
| server/analyzer/translationColors.ts | Ruoli e numeri, vocativo, desinenze ed enclitiche |
| server/analyzer/verifyAI.ts | Validazione risposte IA; chunk 1, parallelismo max 8 |
| server/_core/llm.ts, chat.ts | Client IA e ripieghi configurati |
| client/public/fonts/, tessdata/ | Font locali e modello OCR |
| cornice-dinamica/ | Cornici dedicate e test |

## Flussi

1. Testo: analyze restituisce regole; translate prefetch aggiorna traduzione e
   ruoli IA. Conservare gestione race e applicazione una sola volta per non
   sovrascrivere gli override manuali.
2. Foto: normalizzazione → crop PNG → trascrizione IA via REST → ripiego OCR
   → textarea. Solo immagini, non PDF; niente analisi automatica.
3. Colori: shared/types → motore/ruoli → chip e PDF; legenda/palette derivano
   da LEGEND_ITEMS. Colore manuale finale senza risfumatura. Casi declinabili
   singolare/plurale via shadeForNumber; invariabili senza sfumature.
4. PDF dinamico: colori app, font incorporati, dati studente e traduzioni
   salvate; numero centrato grassetto solo con più pagine. Grigio chiaro
   bordato con q/Q isolato. Dettagli in palette-8754.md.
5. Quaderni statici: asset storici; nessun pulsante nell'app. Non confonderli
   con il PDF generato dall'attività.

## Embed e ritaglio

- Non usare scrollHeight del documento come altezza assoluta in iframe.
- lf-embedded azzera min-height viewport; Welcome con margini simmetrici.
- Messaggio labvisivo:height con token; cornice filtra e.source, mantiene
  clamp/debounce/protezioni anti-loop. Font self-hosted e CORS /fonts.
- Crop modal=true; pagina dietro ferma, corpo touch scorrevole, footer separato.
- Capture wrapper stabile, delta incrementali, niente icona centrale.
- Portare hook/CSS/heightSync insieme al componente. Prima di intervenire
  leggere ritaglio-mobile.md; per il trapianto leggere photo-crop-clonabile.md.
- Non toccare confirm(), moveBox, resizeBox o la geometria per risolvere layout.

## Verifiche e limiti

- 8754: 84/84 unitari, 2 scenari colori UI, 6 PDF verificati, 4 drag sul pubblico;
  endpoint analyze reale HTTP200 con i nuovi tre colori.
- UI con API IA simulate e touch emulato. I 9 scenari generali appartengono
  alla baseline crop 8731, non a una nuova esecuzione completa nel 8754.
- Nessuna nuova misura esaustiva di grammatica, OCR o carico cognitivo BES.
- Verificare presenza delle variabili senza mostrarne valori; non copiare
  segreti di altri progetti. Test su dati reali non devono cancellare record.
- Preview condivisa e nuova conferma prima della produzione. ZIP/skill non
  autorizzano un deploy. Usare il contesto della singola app, non questa chat
  per pubblicare una famiglia di progetti differenti.

