# Modelli delle guide IA (pattern «pacchetto ZIP esportabile»)

Modelli pronti da adattare quando si crea/aggiorna il pacchetto esportabile di
un'app. Le guide si scrivono nella **radice della repository** dell'app e sono
lette da un agente AI (o da un docente) SENZA altri contesti: ogni passo deve
essere operativo e citare i file esatti. Tutte in italiano, tono diretto,
formato Markdown. Nella tabella `### Tabella` di ogni guida si usano percorsi
relativi rispetto alla radice della repo.

## AGENTS.md (punto d'ingresso)

1. «AGENTS.md — Istruzioni per agenti AI che lavorano su questa repository»
   con blocco `>`: leggilo PRIMA di modificare qualsiasi cosa.
2. §1 Che cos'è questa repository (descrizione funzionale dell'app, URL
   produzione se esiste, scaffold, stack in una riga).
3. §2 Quale documento usare (tabella di routing):
   - ricostruire l'app IDENTICA → `REBUILD.md`
   - creare NUOVA app simile/tradotta (inglese/spagnolo/francese…) → `ADATTARE.md`
   - trasferire da Easy-Peasy a Render via GitHub → `RENDER.md`
   - riusare l'accessibilità su altre app → `ACCESSIBILITA.md`
4. §3 Regole d'oro (NON VIOLARLE): es. non toccare l'accessibilità, non
   modificare il protocollo `labvisivo:height`, documentazione allineata al codice.
5. §4 Comandi (pnpm check/build/start/test, ecc.).
6. §5 Dove vivono i testi dell'interfaccia (mappa dei file per il cambio lingua).
7. §6 Struttura essenziale (albero compatto).

## REBUILD.md (ricostruzione completa e identica)

1. Titolo «RICOSTRUZIONE COMPLETA DELL'APP — Guida per agenti AI» + blocco `>`
   con rimando a `ADATTARE.md` per la nuova lingua.
2. §0 Accessibilità (LEGGI PRIMA): elenco puntato delle misure da preservare
   (font, barra, contrasto, focus, reduced-motion, PDF accessibile, embed).
3. §1 Che cos'è questa app + requisiti (Node 22, pnpm >= 10, ecc.).
4. §2 Passi di ricostruzione (codice bash): ottenere il codice (git clone o
   estrazione ZIP), `pnpm install --frozen-lockfile`, creare `.env` da
   `.env.example`, `pnpm dev` → http://localhost:3000.
5. §3 Variabili d'ambiente (tabella nome/obbligatoria/uso).
6. §4 Mappa dei file (tabella File|Ruolo — completa ma essenziale).
7. §5 Comportamenti da replicare ESATTAMENTE: elenco numerato dei punti di
   personalizzazione osservabili (layout, testi, logica, embed, accessibilità).
8. §6 Checklist di verifica finale (per l'agente AI): es. `pnpm check` pulito,
   home ok, embed si restringe, PDF scaricabile, contrasto ok.
9. §7 Deploy su Render: Blueprint (consigliato) + manuale + note tecniche
   (build `pnpm install --frozen-lockfile && pnpm build`, start `pnpm start`,
   health `/_health`) + CI (`.github/workflows/ci.yml`).
10. §8 Nota sui file esclusi: la repo NON contiene `.env`, `node_modules`,
    `dist/`, `.git`, script di sviluppo temporanei, database di runtime.

## ADATTARE.md (nuova app simile / nuova lingua)

1. Titolo «🔀 ADATTARE L'APP A UNA NUOVA LINGUA — Guida per agenti AI e
   sviluppatori» con rimando a `REBUILD.md` per l'originale.
2. §0 Cosa ottieni (app identica con lingua/tema diverso; file da NON toccare).
3. §1 Strategia: cosa cambia (testi, motore di contenuto, OCR, PDF, traduzione)
   e cosa resta identico (accessibilità, layout, cornice, infra).
4. Passi numerati, uno per area di modifica, ciascuno con file esatti:
   - Passo 1 — clonare e rinominare il progetto (cartella, titoli, `<html lang>`).
   - Passo 2 — testi dell'interfaccia (mappa file → stringhe, tabella).
   - Passo 3 — il motore di contenuto/analisi per la nuova lingua (com'è oggi,
     cosa fare per la nuova lingua, come testare).
   - Passo 4 — OCR nella nuova lingua (es. `tessdata/<codice>.traineddata.gz`).
   - Passo 5 — PDF colorato/quaderno (font e testi; NON toccare i font se il PDF
     usa gli stessi dell'interfaccia).
   - Passo 6 — traduzione (motore e pulsante mostra/nascondi).
   - Passo 7 — Accessibilità: NON TOCCARE (copia tutto).
   - Passo 8 — Cornice dinamica per la nuova app (aggiornare `APP_URL`/dominio
     nei file `cornice-dinamica/`).
   - Passo 9 — Deploy su Render (GitHub → Render, rimando a `RENDER.md`).
5. §Checklist di verifica finale (per l'agente AI).
6. §Mappa file → modifica (tabella riepilogo).

## RENDER.md (trasferimento Easy-Peasy AI → Render via GitHub)

1. Titolo «🚀 Trasferire l'app da Easy-Peasy AI a Render (via GitHub)» + blocco
   `>`: pensata per persona senza competenze tecniche avanzate o agente AI.
2. §1 Il percorso in una riga (ZIP → repo GitHub → Blueprint Render → URL).
3. §2 Cosa serve prima di iniziare (account GitHub, account Render gratuito).
4. Passi: §3 creare la repository GitHub (caricare lo ZIP, init git se serve,
   push); §4 collegare Render (pulsante Deploy to Render per repo public /
   flusso Blueprint manuale per repo private); §5 variabili d'ambiente dopo il
   primo deploy (impostare TRUSTED_ORIGINS col dominio Render, ecc.); §6
   verifica (health check, URL); §7 aggiornare la cornice embed col nuovo
   dominio (dove sta il link: file `cornice-dinamica/*.html` o pagina del blog).
5. §8 Aggiornamenti futuri (push su GitHub → redeploy automatico).
6. §9 Risoluzione dei problemi (deploy fallito, pagina bianca, 404, font che
   non si vedono → CORS `/fonts`).
7. §10 Alternative e riferimenti.

## ACCESSIBILITA.md (sezione ben segnalata + riuso)

1. Titolo «♿ ACCESSIBILITÀ — <Nome App>» + blocco `>` ben visibile: «SEZIONE DI
   RIFERIMENTO DELLA REPOSITORY» con navigazione rapida alle sezioni.
2. §1 Panoramica: le misure in una tabella (n. | misura | file/meccanica).
3. §2 Dettaglio delle misure — una sottosezione per misura, ciascuna con:
   cosa fa, come è implementata, dove nel codice. Misure tipiche: font ad alta
   leggibilità auto-ospitato; barra di accessibilità; dimensione testo
   regolabile; interlinea regolabile; righello di lettura; alto contrasto;
   focus visibile; `prefers-reduced-motion`; testo base grande; ARIA e
   tastiera; PDF accessibile; preferenze persistenti; embed accessibile
   (iframe a altezza automatica); lettura ad alta voce.
4. §3 Guida al riuso: come portare le misure su un'altra app (tabella dei file
   da copiare = mini-pacchetto; passi di integrazione; adattare colori/testi;
   consiglio di creare un template riusabile su GitHub).
5. §4 Checklist di verifica dell'accessibilità.
6. §5 Riferimenti.

## README.md (porta d'ingresso del pacchetto)

Titolo app, descrizione 1-2 frasi, poi nell'ordine: sezione «📦 Contenuto del
pacchetto ZIP (funzionale per agenti AI)» che elenca le guide e cosa fa ognuna;
«📖 Documentazione della repository» (tabella guida → quando usarla);
caratteristiche; sezione ♿ accessibilità in sintesi; stack; requisiti;
installazione e avvio; variabili d'ambiente; controlli qualità; CI; build e
avvio in produzione; «Trasferimento da Easy-Peasy AI a Render (via GitHub)»
(con rimando a `RENDER.md`); «🚀 Creare una nuova app simile» (rimando a
`ADATTARE.md`); «🖼️ Cornice dinamica (embed per Blogger/siti)»; struttura del
progetto; note importanti; licenza.

## SCROLLING-MOBILE.md (se sono presenti finestre touch)

Descrivere il contratto per ciascun dialogo: pagina dietro ferma oppure
scorrevole, focus/chiusura, area di scroll interna e gesti di drag separati.
Per un iframe auto-alto documentare come si misura il viewport visibile e
come si sospende il resize durante il lock. Includere nella mappa dei file
hook, CSS, heightSync e test; non prescrivere `modal={false}` per tutte le
finestre. Riferimento attuale: `references/ritaglio-mobile-iframe.md`.
Indicare separatamente test touch emulati, hardware reale e OCR simulato.

## manifest.json (metadati macchina)

JSON con: `name` (nome repo), `version`, `description`, `stack` (frontend,
backend, db opzionale), `scripts` di package.json, `envVars` (da `.env.example`),
`assets` (font, tessdata, PDF, cornice), `guides` (elenco *.md con ruolo),
`fileMap` (percorsi chiave), `notes`. Mantenerlo allineato al codice reale:
font, percorsi e funzioni citati devono esistere davvero. Per un rilascio
pubblicato aggiungere `release` con ID deploy, URL, commit del codice,
risultati verificati e limiti del collaudo; includere gli eventuali hook e
test mobile nella mappa file. Non confondere un nuovo commit di sole guide
con una nuova versione di codice pubblicata.
