# Archivio di dettaglio — latino-facile

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/latino-facile.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

# Latino Facile — stato consolidato al 29/10/2026

## Selezionare il lavoro

| Richiesta | Leggere |
|---|---|
| Colori, legenda, suffissi, PDF generato | `/home/user/skills/didattica-app-lingue/references/latino-facile/palette-8754.md` |
| Struttura, analisi, traduzione, foto/OCR | `/home/user/skills/didattica-app-lingue/references/latino-facile/architettura.md` |
| Ritaglio, touch, viewport iframe, heightSync | `/home/user/skills/didattica-app-lingue/references/latino-facile/ritaglio-mobile.md` |
| Trapiantare SOLO il ritaglio | `/home/user/skills/didattica-app-lingue/references/latino-facile/photo-crop-clonabile.md` |
| Quaderno didattico statico | Profilo latino-facile-quaderno in didattica-documenti-accessibili |
| Deploy, ZIP, cornici blog | didattica-pubblicazione-blog |

## Identità e precedenza

- Progetto: `/home/user/latino-facile-app`, scaffold web-db-user; Vite/React/TS/Tailwind, Express/tRPC/Drizzle.
- URL stabile: `https://latino-facile-app-2.easy-peasy.site`.
- Produzione **8754**, codice `5fbfc61fc64036b442bca07703162cd70f1d28a3`.
- Checkpoint successivo `e48e24c73d9f959a1c2007b694fbc1476809056e`: sole note, runtime invariato.
- Leggere README, AGENTS, REBUILD, ADATTARE, ACCESSIBILITA e manifest della repo prima di intervenire; verificare il contesto progetto corrente prima di usare il deploy.
- Questi dati sostituiscono gli appunti storici. Non ripristinare sconosciuti bianchi, colori medi precedenti, modal=false per il ritaglio o istruzioni/icona centrale rimosse.

## Conservare la palette approvata in tutta l'app

| Categoria | Colore |
|---|---|
| Avverbi | Blu intenso `#0057D9` |
| Preposizioni | Grigio chiaro `#BDBDBD` |
| Congiunzioni | Grigio scuro `#4A4A4A` |
| Altri modi verbali | Marrone `#795548` |
| Sconosciuto | Chip nero `#000000`, scritta bianca |

- `shared/types.ts`: SERVICE_COLORS → POS_COLORS, LEGEND_ITEMS; fonte unica per motore, ruoli IA, chip, palette manuale e PDF. Casi e sfumature di numero invariati.
- Testo scuro sui chip chiari, anche dopo ricolorazione manuale di uno sconosciuto; testo chiaro sui chip scuri. Override manuale finale: non risfumare.
- `legendExplanationColor` mantiene leggibili le didascalie dei due grigi.
- Nel PDF grigio chiaro: fill #BDBDBD + contorno 0,35 pt #595959; niente sfondo, rasterizzazione o doppio testo. Isolare con q/Q. Non applicare il bordo agli altri colori.
- Enclitiche attaccate alla base: APP contorno del colore della base e lettere nero/bianco opposto; PDF `colorForEnclitic`: -cum chiaro, -que/-ve/-ne scuro, anche da dati vecchi.
- Il PDF dinamico segue questa palette. Non dichiarare aggiornati i quaderni statici o i PDF già scaricati senza rigenerarli.
- Il fill chiaro da solo NON supera 4,5:1 sul bianco: non certificare accessibilità globale dal solo contrasto del contorno.

## Preservare UI, foto e quaderno

- `/` WelcomePage; `/app` Home. Verificare i testi reali nel codice, non ricostruire dalla memoria.
- Limite corrente verificato: **MAX_PAROLE = 50** in Home.tsx. Non cambiarlo in questa attività; eventuali richieste diverse vanno trattate separatamente.
- Textarea e traduzione allineate a sinistra; bottone SALVA con h-auto per testo multilinea. Salvataggio traduzione senza download automatico; scaricare solo dal pulsante SCARICA IL PDF.
- Sconosciuti neri; nessun banner di avviso ripristinato. PDF OpenDyslexic con font incorporati; numero centrato in grassetto solo se multipagina.
- Foto: SCATTA/CARICA → normalizePhoto → CropDialog → PNG → POST /api/ai/transcribe → ripiego Tesseract → testo. Non avviare automaticamente l'analisi dal riconoscimento.
- Non reintrodurre la vecchia mutation latino.foto, caricamento foto/PDF, incolla immagini o drag-and-drop eliminati.
- Quaderni `quaderno-unico-v*.pdf` = asset storici: nessun pulsante/link nell'app senza nuova richiesta esplicita.

## Non far regredire il ritaglio (baseline autonoma 8731)

- Il deploy 8754 cambia la palette, NON il cropper: baseline 8731 e app 8754 possono coesistere. Confrontare hash dei sorgenti, non pretendere ID deploy uguali.
- Solo titolo RITAGLIA LA FOTO; nessun sottotitolo, icona centrale o AZZERA.
- modal=true, pagina dietro ferma, corpo interno scorrevole; footer separato con RUOTA SINISTRA/DESTRA, CHIUDI, RITAGLIA in un solo riquadro.
- Trascinare direttamente tutta la selezione con mouse/touch. Pointer capture su wrapper stabile, un pointerId, delta dall'ultimo evento; gestire up/cancel/lostcapture.
- MIN_BOX 8%, handle 44px, MIN_IMG_W 560 solo a schermo, frecce 2% e Shift 10%; PNG lossless max 2200px. JPEG max 1800 appartiene all'invio IA successivo.
- Portare insieme componente, hook viewport, CSS, heightSync e test. Conservare confirm() e geometria moveBox/resizeBox/resizeCorner.
- In iframe: visualViewport o intersectionRect, lock ripristinabile, data-lf-crop-open sospende heightSync; rimisurare su lf:crop-closed.

## Embed, dati e IA

- Misurare il contenuto reale, non scrollHeight assoluto del documento. Azzerare min-h-screen/min-h-dvh in lf-embedded; spazi Welcome simmetrici.
- Conservare labvisivo:height, token cornice, filtro e.source, CORS /fonts e protezioni anti-loop. Nessun nuovo embed per il solo cambio palette.
- CHUNK_SIZE corrente 1, MAX_PARALLEL 8; verificare nel codice prima di ottimizzare. Non promettere pochi secondi o accuratezza totale.
- Non toccare dati di studenti/classi per testare. Non trasferire credenziali da altre app automaticamente; configurare variabili solo per il progetto autorizzato e non consegnare .env.

## Verificare e consegnare

```bash
cd /home/user/latino-facile-app
pnpm check
pnpm exec vitest run --no-file-parallelism
pnpm build
# server attivo, UI con IA simulata:
pnpm exec tsx tests/service-colors.e2e.ts
node tests/crop-drag.e2e.mjs
```

- Rilascio 8754 verificato: 84/84 unitari, endpoint analyze reale HTTP 200 con i tre colori, 2 scenari UI desktop/mobile, 6 PDF scaricati, 4 drag sul pubblico.
- Distinguere prove reali/simulate: UI API simulate, touch emulato; non sono nuova misura di OCR, grammatica o certificazione BES.
- Corpus e percentuali storiche non sono una nuova accuratezza certificata. Gli script /home/user/skills/didattica-app-lingue/scripts/latino-facile/qa fanno chiamate esterne: non eseguirli nella validazione offline delle skill.
- Prima di un nuovo rilascio: checkpoint → preview → condividere e fermarsi → nuova conferma → checkpoint → produzione. Ripristinare solo l'eventuale Dockerfile rimosso dallo strumento, dopo confronto con HEAD.
- ZIP dal commit pulito: /home/user/skills/didattica-app-lingue/scripts/latino-facile/export_zip.sh + /home/user/skills/didattica-app-lingue/scripts/latino-facile/verify_export.py. L'export deve distinguere baseline crop e rilascio app. Aggiornare le guide senza fare deploy non richiesti.

