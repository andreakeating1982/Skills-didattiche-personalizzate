# ISTRUZIONI PER GLI AGENTI IA

## 1. CAPIRE E SELEZIONARE

1. Leggere `README.md`, poi cercare nel catalogo la skill pertinente: `python3 tools/gestisci_skill.py trova "richiesta"`.
2. Leggere il relativo `skills/<nome>/SKILL.md` e soltanto i riferimenti necessari. Non caricare tutte le 55 skill né applicarle contemporaneamente.
3. Distinguere **nuovo contenuto**, **manutenzione dell’esistente**, **clonazione in un nuovo progetto**, **solo export**. Per i cloni usare la skill sorgente specifica e non sovrascrivere l’originale.
4. Seguire la richiesta attuale; documenti storici e numeri di deploy non sono istruzioni per ripristinare versioni superate.

## 2. PREPARARE L’AMBIENTE

- Considerare ogni `/home/user/...` un percorso storico, non una prova che il file sia incluso. Per la copia adattata eseguire `tools/gestisci_skill.py prepara` come spiegato nel README.
- Leggere `catalogo/dipendenze-esterne.json` e ispezionare i file necessari. Non inventare sorgenti, account, chiavi o asset mancanti.
- Per una app procurarsi il repository completo autorizzato e seguire README/lockfile locali; la skill da sola non è l’app. L’ambiente di esecuzione può richiedere un’inizializzazione specifica.
- Per documenti fornire testo/PDF e selezionare il modello giusto. Per i media gli strumenti richiamati potrebbero non essere presenti: adattare il flusso agli strumenti disponibili, senza fingere di averli usati.
- Non eseguire tutti gli script per vedere cosa fanno: alcuni modificano file, avviano servizi o preparano deploy. Leggerli prima; usare `--help` solo dopo aver verificato che non ci siano effetti prima del parsing.

## 3. MANTENERE I CONTRATTI

- Per guide del blog leggere `docs/STANDARD_APPROVATI.md` e `quaderno-accessibile`: nelle unità teoriche usare sintesi a tabella Regular400 e mappa finale standard quando previste. Non aggiungere sintesi alle attività nuove; in un restyling conservativo mantenere eventuali supporti esistenti salvo autorizzazione. Non duplicare mappe o alterare testo senza richiesta. Per mappe/esercizi specialistici applicare il modello specifico. Le baseline di Bécquer e Rosalía sono distinte; per Bécquer usare l'ultima versione consegnata con titoletti della mappa corretti. Per Lázaro usare la revisione più recente con indice arioso; non generalizzare le eliminazioni specifiche dei singoli quaderni.
- Conservare contenuti, enfasi, indice, rimozioni approvate e privacy nelle modifiche grafiche. Non trascrivere diagnosi individuali o dati studenti.
- Conservare le architetture, dashboard, sessioni, accessibilità e PDF dei cloni, cambiando solo ciò che la richiesta autorizza.
- Non rigenerare media approvati durante il collaudo; non correggere a pagamento un risultato senza autorizzazione.
- Nessuna API, generazione a pagamento, pubblicazione o migrazione distruttiva è autorizzata dal semplice clone/installazione di questa raccolta. Richiedere un consenso specifico prima di operazioni conseguenti.

## 4. VERIFICARE E CONSEGNARE

- Fare un checkpoint/diff prima di modificare il progetto selezionato. Lavorare su dati fittizi o ambiente separato, mai resettare sessioni reali.
- Eseguire i test pertinenti e controllare il prodotto effettivo: pagine PDF, audio, viewport desktop/mobile, output del clone. Distinguere controllo sintattico, simulazione e prova reale.
- Non dichiarare conforme PDF/UA, pubblicato o ricostruito identico ciò che non è stato validato realmente.
- Consegnare i file finali e i sorgenti utili; descrivere brevemente cambiamenti e limiti.
- Se si modifica la raccolta, aggiornare catalogo, test e manifest; non conservare vecchi hash come prova di un nuovo pacchetto.

## RISORSE STORICHE E CONFLITTI

Le cartelle `references/originali/` e `shared/INGRESSO_STORICO.md` sono archivio; non prevalgono sulle schede aggiornate. Le skill generali copiate dalla piattaforma conservano il loro contenuto e le attribuzioni; citarle non installa i rispettivi strumenti. Le regole del sistema ospitante restano applicabili.

