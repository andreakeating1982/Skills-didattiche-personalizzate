# SKILL DIDATTICHE E STRUMENTI PER L’IA

**55 skill — aggiornamento del 5 novembre 2026**, inclusa la skill Podcast didattici e i modelli approvati di realtà virtuale, con le ultime revisioni consegnate di Lázaro Carreter e Bécquer, la versione approvata di Rosalía e lo standard per sintesi, mappe, fonti e rimpaginazioni conservative. Lázaro: indice più arioso e sola voce `TRADUCCIÓN AL ITALIANO`, conservazione della traduzione, quiz e mappa soltanto in spagnolo; Bécquer: titoletti della mappa corretti senza alterare le informazioni significative. Le revisioni più recenti sono state consegnate, senza un'ulteriore approvazione esplicita attestata. Sono inclusi script, riferimenti, modelli, immagini e font disponibili. Le risorse esterne citate restano da fornire separatamente.

> Questo repository contiene **le skill, non tutti i progetti/app/documenti che citano**. I loro sorgenti esterni vanno forniti quando necessari. Nessuna pubblicazione online è stata eseguita. Per la prima archiviazione è consigliato un repository **privato**, in attesa di verificare diritti e contenuti di terzi.

## COMINCIARE IN TRE PASSI

1. Estrarre lo ZIP oppure clonare il proprio repository GitHub, poi entrare nella cartella `skills-didattiche-ia`.
2. Cercare la skill e verificare l’archivio con Python 3.11 o successivo:

   ```sh
   python3 tools/gestisci_skill.py trova "quaderno accessibile"
   python3 tools/gestisci_skill.py verifica
   ```

3. Chiedere all’IA di leggere `AGENTS.md`, scegliere una skill dal [catalogo](catalogo/CATALOGO.md) e applicarla al nuovo contenuto. Copiare uno degli esempi in [PROMPT_PRONTI.md](PROMPT_PRONTI.md).

Lo strumento di catalogo/verifica/preparazione usa solo la libreria standard Python. Le dipendenze per produrre PDF, audio, 3D o app sono separate e vanno installate soltanto quando servono.

## RENDERE PORTABILI I VECCHI PERCORSI

Le skill originali citano cartelle storiche come `/home/user/skills` o `/home/user/nome-progetto`. Non sono cartelle da presumere esistenti su un altro computer. Per preparare una copia con percorsi coerenti, **senza eseguire alcuna skill**:

```sh
python3 tools/gestisci_skill.py prepara --dest ../skills-runtime --workspace ../lavoro
```

- La destinazione deve essere **nuova e fuori dal repository**: il comando rifiuta sovrascritture.
- Le skill adattate si trovano in `../skills-runtime/skills/`; le risorse condivise in `../skills-runtime/shared/`.
- I percorsi storici sono riscritti nella copia di lavoro, **non negli originali** del repository.
- I riferimenti alle app/input diventano percorsi nella cartella `lavoro`, ma i progetti esterni non vengono creati o scaricati automaticamente.
- Per una mappa personalizzata copiare `config/progetti.esempio.json` in `progetti.locali.json`, compilare i percorsi assoluti reali e aggiungere `--map progetti.locali.json`. Il file locale è escluso da Git.
- Su sistemi diversi da Linux verificare dipendenze e comandi shell; la sola sostituzione dei percorsi non rende universale ogni script.

Il comando `prepara` produce `PREPARAZIONE.json` con la mappa effettiva. Non pubblicare quella copia se contiene percorsi personali.

## COSA TROVI

| Percorso | Funzione |
|---|---|
| `AGENTS.md` | Punto di ingresso e regole per un’altra IA |
| `catalogo/CATALOGO.md` e `catalogo/skills.json` | Selezione delle 55 skill, descrizioni e risorse |
| `skills/<nome>/SKILL.md` | Istruzioni operative della singola skill |
| `skills/<nome>/scripts`, `references`, `templates` | Risorse presenti, non promesse di allegati mancanti |
| `shared/` | Risorse condivise recuperate dalla vecchia radice; non una55ª skill |
| `REBUILD.md` e `ADATTARE.md` | Recuperare la raccolta o adattarla a usi futuri |
| `ACCESSIBILITA.md` | Standard trasversali e distinzione fra modelli |
| `GITHUB.md` | Caricare il contenuto estratto nel proprio repository |
| `PROMPT_PRONTI.md` | Richieste pronte per l’IA |
| `docs/STANDARD_APPROVATI.md` | Ultime regole editoriali approvate e regola di flusso più recente |
| `docs/LIMITI_E_DIPENDENZE.md` | Confini reali di portabilità e sorgenti esterni |
| `docs/LICENZE_E_PUBBLICAZIONE.md` | Diritti, licenze e riservatezza |
| `VERIFICA-PACCHETTO.json` | Risultati del collaudo effettivamente svolto |
| `docs/AGGIORNAMENTO_SINTESI_MAPPE.md` | Sintesi dello standard e collegamenti ai modelli approvati |
| `MANIFEST.json` | SHA-256 e dimensioni dei file distribuiti |

## FAMIGLIE DI RIUSO

Documenti/quaderni accessibili; mappe matematiche e linguistiche; app con classe/docente; cloni di quiz, immagini interattive e laboratori; lingue e calcolo; audio, video clay e diorami3D; cornici e pubblicazione blog; strumenti generali per ricerca, dati, documenti e creazione di nuove skill.

Sono mantenute **tutte le 54 skill preesistenti e la skill Podcast didattici**, comprese le skill specifiche e gli ingressi di famiglia: non è stata eseguita una fusione che elimini dettagli. Leggere prima la descrizione, non caricare tutto il catalogo nel contesto dell’IA.

## SICUREZZA E LIMITI

Password storiche sono state rimosse dalla copia esportata. Non sono inclusi `.env`, database studenti o credenziali di servizi. Una scansione statica non è una garanzia assoluta: verificare ancora prima di rendere pubblico il repository. Non attribuire una nuova licenza generale alle risorse di terzi; conservare le attribuzioni presenti.

La verifica dell’archivio non ricostruisce automaticamente le app, non certifica conformità PDF/UA, non attiva strumenti proprietari e non effettua generazioni a pagamento o deploy. Leggere [limiti e dipendenze](docs/LIMITI_E_DIPENDENZE.md).

