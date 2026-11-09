# Archivio di dettaglio — mappa-concettuale

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/mappe-interattive.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

# Mappa Concettuale — Manutenzione

L'app si trova in `/home/user/mappa-concettuale`. È un'app `web-db-user` standalone (NON condivide codebase con altre app).

## File chiave

| File | Contenuto |
|------|-----------|
| `client/src/pages/Home.tsx` | **Tutta l'app**: welcome, 6 passi, mappa completata, footer |
| `client/src/lib/tipi-mappa.ts` | Tipi TypeScript (`MappaConcettuale`, `Ramo`, `ImmagineMappa`), colori, messaggi |
| `client/src/components/ConceptMapCanvas.tsx` | Canvas della mappa concettuale completata |
| `client/src/index.css` | Palette terracotta, variabili CSS |

## Deploy

- **Preview**: `webdev_deploy` con `mode="preview"` sul project_dir `/home/user/mappa-concettuale`
- **Produzione**: `webdev_deploy` con `mode="production"` — URL permanente: `https://mappa-concettuale-2.easy-peasy.site`
- **Prima della produzione**: eseguire `webdev_save_checkpoint` con descrizione significativa
- **TypeScript check**: `pnpm check` nella directory del progetto

## Modificare l'UI

Tutta l'interfaccia è nel file `client/src/pages/Home.tsx`. I passi sono numerati da 0 (welcome) a 6 (immagini), più lo stato `mappa.completata`.

### Welcome (passo 0)
- Min-height: `min-h-[50vh]` (nell'attuale implementazione usa `flex-1` con layout flex)
- Card: `max-w-[400px]` con icona libro, titolo, 4 input (nome, cognome, data, classe), bottone ENTRA
- Data predefinita: `useState(new Date().toLocaleDateString("it-IT", {...}))`

### Passi 1–6
- Card principale: `rounded-2xl p-4 md:p-5 shadow-lg`
- Box istruzioni: `rounded-xl p-3 md:p-4 mb-3` con testo `text-sm md:text-base`
- Titolo passo: `text-lg md:text-xl font-extrabold`
- Bottoni AVANTI/INDIETRO nel footer di ogni passo

### Mappa completata
- Visualizzazione canvas + immagini posizionabili trascinandole (supporto **mouse** + **touch** per mobile)
- Handler: `handleImageMouseDown` / `handleImageTouchStart`, `handlePosizionaMouseMove` / `handlePosizionaTouchMove`, `handlePosizionaMouseUp` / `handlePosizionaTouchEnd`
- Bottoni SCARICA PDF e CREA UN'ALTRA MAPPA
- **⚠️ CRITICO:** `completaMappa()` DEVE impostare `setCurrentStep(6)` e NON `setCurrentStep(7)` — il rendering finale controlla `currentStep === 6 && mappa.completata`. Se `currentStep` è 7 la vista completata non appare mai (schermo bianco).
- I pallini verdi: quando `mappa.completata === true`, TUTTI i 6 passi mostrano `bg-green-400` con ✓

### Footer
- Testo: `REALIZZATO DA EMANUELA E ANDREA CENTINARO` in `text-xs uppercase`
- Posizionato in fondo con layout `min-h-screen flex flex-col`

### Colori
Palette terracotta: primary `#B8846A`, secondary-foreground `#8B3A1A`, background `#FAF8F5`.

## Embed Blogger

Codice embed con iframe ad altezza dinamica. L'app usa `ResizeObserver` + `postMessage` con tipo `'mappaconcettuale:height'`. La cornice Blogger ha gradiente `rgb(230, 205, 171)` e stessi stili della cornice Shakespeare Quiz.

## Esportazione ZIP

```bash
cd /home/user && zip -r mappa-concettuale-esportabile.zip mappa-concettuale \
  -x "mappa-concettuale/node_modules/*" \
  -x "mappa-concettuale/.git/*" \
  -x "mappa-concettuale/dist/*" \
  -x "mappa-concettuale/.env" \
  -x "mappa-concettuale/.DS_Store" \
  -x "mappa-concettuale/embed-blogger.html"
```

## Step indicator

La barra di avanzamento include: INIZIO (step 0), 1–6, FINE (step 7). Il passo corrente è evidenziato con `bg-primary text-primary-foreground`. Quando `mappa.completata` è true, tutti i 6 passi diventano verdi (`bg-green-400`) con spunta ✓ (condizione aggiuntiva prima delle altre nel ternario).

## Note

- I dati sono salvati in `localStorage` con chiave `"mappa-concettuale"`
- Il type `MappaConcettuale` contiene: `studente`, `riassunto`, `appunti`, `hashtags`, `titoloCentrale`, `rami`, `immagini`, `stepCorrente`, `completata`
- PDF generato lato client con `jsPDF` + `html2canvas`
- NON ci sono skill separate per cambiare le domande — quest'app non è un quiz, è un costruttore di mappe
