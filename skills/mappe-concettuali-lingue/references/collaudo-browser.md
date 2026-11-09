# Collaudo nel browser e verifica deploy

## Pattern console (fondamentali)

1. **Dopo `browser_navigate`, la PRIMA `browser_console_exec` spesso fallisce** con «Execution context was destroyed, most likely because of a navigation»: la pagina si ricarica quando la sessione console si aggancia. **Ritentare** la stessa chiamata: la seconda va a buon fine. Non modificare il codice credendo a un errore reale.
2. **L'output si recupera con l'error-trick**: il risultato di `browser_console_exec` non sempre mostra il valore di ritorno; fare `throw new Error('ETICHETTA ' + JSON.stringify(dati))` e leggere l'errore restituito.
3. **Il flusso completo in UNA sola chiamata asincrona** (IIFE async/await con sleep interni): evita illeciti scaduti di sessione del browser tra le chiamate. Se l'output viene assorbito, salvare i dati in variabili `window.*` e rileggerli con una seconda exec.
4. **Guidare l'app dentro un iframe same-origin**: `document.getElementById('app').contentDocument`; per le textarea controllate da React usare il setter nativo `Object.getOwnPropertyDescriptor(win.HTMLTextAreaElement.prototype,'value').set` + `dispatchEvent(new Event('input',{bubbles:true}))`; selezionare i pulsanti con regex sul testo (`/estrai/i`, `/genera il pdf/i`).
5. L'app persiste nome/classe/data in **localStorage**: alla riapertura la welcome è precompilata (es. «Rossi Giulia · Classe 2A»), utile per i test.
6. **Quando l'output viene assorbito**: a volte `browser_console_exec` restituisce solo «Action completed» senza mostrare l'errore lanciato (con l'JSON dei risultati). Salvare i risultati in variabili `window.*` (es. `window.__stato = out`) e rileggerli con una seconda exec, oppure affidarsi allo screenshot finale di `file_view`.
7. **Driver «riassuntivo» (state-aware)**: i reload di pagina a metà flusso azzerano l'app ma le schede estratte restano. Prima di ogni passo controllare lo stato: se il pulsante Entra non c'è, saltare; se l'estrazione è già fatta (testarea assente), andare dritti a Genera. Mai dare per scontato il punto di partenza.
8. **Attendere il pulsante ABILITATO**: cliccare «Genera il PDF» mentre l'estrazione AI è ancora in corso NON fa nulla (pulsante disabilitato → clic perso, il flusso resta bloccato alle schede e il PDF non appare mai). Nei test fare polling fino a 15 s: `[...document.querySelectorAll('button')].find(x => /genera il pdf/i.test(x.textContent) && !x.disabled)`.
9. **Il browser cloud NON renderizza i PDF negli iframe**: il Chrome gestito non ha il plugin visualizzatore PDF, quindi i SUOI screenshot mostrano il segnaposto grigio con «Open» in QUALUNQUE versione dell'app (anche dove su un PC reale l'anteprima si vede). NON è una regressione: per l'anteprima PDF sono autorevoli solo le sonde DOM (`.lf-pdf-preview` presente / `.lf-pdf-card` assente), non i screenshot. Nota: il driver asincrono ha restituito prima che il flusso finisse, quindi il SUO screenshot mostra lo stato a metà flusso — affidarsi alla sonda dopo il completamento.
10. **Testare la logica mobile senza un telefono**: copiare verbatim la funzione `isMobile` di Home.tsx in una exec e provarla con valori simulati (pointer coarse, UA Android/iPhone/iPad, `MacIntel` + `maxTouchPoints > 1`): i 9 casi attesi sono desktop/embed stretto/PC touchscreen → false; Android, iPhone, iPad, iPadOS-spoof-Mac, Android con mouse → true.

## Tempi del flusso (sleep consigliati)

«Estrai» (AI lato server): **variabile, può superare i 4 s** — nei test attendere il pulsante «Genera il PDF» ABILITATO (poll, non sleep fissi). «Genera il PDF» → sezione PDF pronta: ~12-14 s. Attendere sempre qualche secondo di stabilizzazione prima di leggere i log (retry/isteresi).

## Pagina di test anti-tremolio

`client/public/test-oscillazione.html` → servita dal dev server a `/test-oscillazione.html` (i file in `client/public` sono serviti così come sono, anche nel build). Contiene un iframe 390 px con viewport frazionario 703.37 px, log di tutti i messaggi `labvisivo:height` (`window.__log`), analisi oscillazioni (`window.__analizza()`), simulazione dell'applicazione altezza con debounce 200 ms. Dettagli e risultati attesi: `heightsync-anti-tremolio.md` nella stessa cartella.

Altre pagine di test della cornice (`cornice-dinamica/test-dedicata.html`, `test-impermeabile.html`) NON sono servite dal dev server: sono per collaudi locali della cornice.

## Pagina di test anteprima PDF (embed stretto)

`client/public/test-embed-680.html` → `/test-embed-680.html`: l'app in un iframe da **680 px su desktop** (sotto la vecchia soglia v1 dei 768 px, dove la scheda appariva a torto). Procedura: flusso completo dentro l'iframe (entra → testarea → estrai → attendi Genera ABILITATO → genera, ~14 s) e poi sonda DOM. **Esito atteso (contratto v2)**: `.lf-pdf-preview` **presente** e `.lf-pdf-card` **assente** — su desktop l'anteprima iframe resta a qualunque larghezza. Aggiorna l'altezza dell'iframe con il protocollo `labvisivo:height` come la cornice reale.

## Verifica post-deploy (anti-cache CDN)

Dopo `webdev_deploy` (anche in produzione) la CDN può servire **HTML vecchio per qualche minuto**: il bundle letto subito dopo il deploy può sembrare quello precedente. Procedura:

```bash
CB=$(date +%s)
for u in "https://mappe-concettuali-lingue.easy-peasy.site" "https://deploy-…a.run.app"; do
  curl -s -o /tmp/p.html -H "Cache-Control: no-cache" -H "Pragma: no-cache" "$u/app?cb=$CB"
  JS=$(grep -o '/assets/index-[^"]*\.js' /tmp/p.html | head -1)   # hash servito
  curl -s "$u$JS" | grep -c "STRINGA-NELLA-MODIFICA"              # 1 = fix presente
done
ls dist/public/assets/   # hash atteso dal build locale
```

Regola: **hash del bundle servito == hash in `dist/public/assets/`** = versione corretta (hash content-based). Se l'hash è vecchio, attendere 60-90 s e riverificare: la cache si rinnova da sola. Verificare SEMPRE entrambi gli URL (Cloud Run e dominio `.easy-peasy.site`). Per il lato server (`server/mappe/pdf.ts`) il bundle è `dist/index.js`: le modifiche al PDF non cambiano l'hash del bundle client.

## Comandi

- `pnpm check` — TypeScript (sempre prima del build)
- `pnpm build` — build completo (client + server esbuild)
- `pnpm dev` — dev server (le modifiche al sorgente sono subito visibili in preview)
