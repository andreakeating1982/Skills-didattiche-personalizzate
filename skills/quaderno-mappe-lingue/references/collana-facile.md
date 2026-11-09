# Collana FACILE — riferimento approvato il 28 ottobre 2026

## Richiesta che determina lo standard

«Fai una copertina simile per il quaderno di inglese, di francese e di spagnolo chiamandoli INGLESE FACILE, FRANCESE FACILE e SPAGNOLO FACILE. Pur conservando tutte le mappe create (senza cambiarle in alcun modo), il quaderno deve essere pensato come e il più simile possibile al quaderno di latino allegato.»

Usare `/home/user/uploads/Latino_Facile_colori_app.pdf` (97 pagine) come modello editoriale, non come contenuto da tradurre. Non ridisegnare o semplificare ulteriormente le mappe linguistiche per assomigliare a quelle latine.

## File canonici e stato

| Lingua | Build dei contenuti | HTML base | PDF base sincronizzato |
|---|---|---|---|
| Inglese | `/home/user/inglese_build/build_v3.py` | `/home/user/inglese_build/inglese_accessibile_v3.html` | `/home/user/inglese_build/Mappe_concettuali_grammatica_inglese_inclusivo_v3.pdf` |
| Francese | `/home/user/mappe-fr/build_fr.py` | `/home/user/mappe-fr/mappe_fr.html` | `/home/user/mappe-fr/Quaderno_fr.pdf` |
| Spagnolo | `/home/user/mappe-es/build_es.py` | `/home/user/mappe-es/mappe_es.html` | `/home/user/mappe-es/Quaderno_es.pdf` |

Edizione completa attuale: `/home/user/facile_edizione/{Inglese_Facile,Francese_Facile,Spagnolo_Facile}.{html,pdf}`.

- Inglese: 96 mappe, 51 pagine di mappe e 60 pagine totali; mappe da pagina 10. PREPOSITIONS OF TIME già ampliata; ASKING FOR AND GIVING DIRECTIONS n. 20, a pagina 21 dell’edizione FACILE, subito dopo le preposizioni di tempo. Contiene sightseeing, walk, cyclists e underground; nessun riferimento al livello B1.
- Francese: 79 mappe, 40 pagine di mappe e 49 totali; mappe da pagina 10.
- Spagnolo: 72 mappe, 36 pagine di mappe e 44 totali; mappe da pagina 9. SER Y ESTAR è la mappa n. 9: usare l’indice nuovo per la pagina, non il vecchio riferimento pagina 8.

Non dare per completate vecchie richieste sospese (per esempio accorpamenti francesi o altre correzioni) se non sono state verificate nel sorgente. Il restyling non autorizza ad applicarle di nascosto. Mantenere un solo livello di pagine editoriali: ripartire dall’HTML base, non concatenare nuove copertine alla precedente edizione FACILE.

I conteggi sono la baseline di questa edizione; dopo aggiunte autorizzate aggiornarli da sorgenti reali, mai forzare un numero storico.

## Anatomia editoriale

1. **Copertina (pagina 1 autonoma, senza numero visibile).** Titolo italiano esatto su banner terracotta `#934a30`, OpenDyslexic Bold 30pt. Tre righe 15pt: `IL QUADERNO DI GRAMMATICA INGLESE/FRANCESE/SPAGNOLA`; `Schede, mappe e strumenti di lettura`; `Un percorso adattabile in cinque anni`. Illustrazione landscape clay adulta al centro. Box «Questo quaderno appartiene a», riga nome, Classe e Anno.
2. **Una scheda alla volta.** Leggere un’idea, guardare lo schema, seguire tre passi con aiuto e usare la tabella senza memorizzare tutto. Riferirsi al box reale IN PRATICA; non annunciare soluzioni/quiz/atlante assenti.
3. **Cinque anni: come orientarsi.** Cinque tappe flessibili, diverse per lingua e basate sulle mappe già disponibili; non cambiare l’ordine delle mappe per simulare un programma rigido. Nota: non è un corso completo né l’intero curricolo del liceo linguistico.
4. **Per chi accompagna lo studio.** Distinguere PEI e PDP; non spacciare il percorso per «obiettivi minimi ministeriali»; sottolineare aiuti individuali, comunicazione e verifica delle preferenze di leggibilità.
5. **Colori e parole-guida.** Ricavare i colori effettivi dai banner e collegare un esempio reale per colore. Non importare le categorie morfologiche della legenda latina nelle lingue moderne. Precisare che colore, numero e titolo lavorano insieme.
6. **Indice delle mappe.** Una colonna, ripartita in 4 pagine inglese, 4 francese, 3 spagnolo nella baseline. Titoli e numeri sono collegamenti. Paginazione automatica `target-counter(attr(href),page)`; mai numeri scritti a mano.
7. **Mappe verbatim.** Preservare la sequenza HTML delle `section.pg` e il CSS preesistente. Aggiungere soltanto la navigazione nel footer. Pagina numerata in basso al centro; «Torna all’indice ↑» a destra.

### Geometrie consolidate

- A4; frontespizio: margini 13mm sopra, 15mm laterali, 16mm sotto; guide e indice 18mm sotto. **Non cambiare i margini delle pagine delle mappe**.
- Testo `#2e2018`, card crema `#fbf7ee`, bordi `#e6ddce`, link blu `#1f536e`.
- Intestazioni guide 18pt; corpo 14pt; tappe anni 13pt; note 11,5pt; tabella legenda 12–13pt; footer ritorno indice 10pt. Font sempre OpenDyslexic; dimensione mappe invariata.
- CSS editoriale con prefisso `.lf-*` e pagine nominate `lf-cover`, `lf-front`, `lf-index`, per non alterare i selettori delle mappe (`.pg`, `.blk`, `.mapcard`).
- Indice: font 14pt, line-height 1,3 e padding verticale delle celle **3pt**. Con 4pt, la prima pagina inglese produceva una pagina quasi vuota con la sola voce 24: correggere il solo padding dell’indice, non rimpicciolire le mappe.

## Immagini già approvate — nessuna nuova generazione necessaria

`templates/collana-facile/cover_en.png`, `cover_fr.png`, `cover_es.png`, `Copertine_Facile.png`.
Stesso insegnante adulto a destra, barba e gilet caldo ocra/senape, fondo avorio, oggetti culturali a sinistra: Big Ben/autobus/libro; Torre Eiffel/libri/lavanda; architettura spagnola/libro/piastrella. Asset senza testo: titoli composti nell’HTML per evitare errori ortografici. Riferimento originale estratto dalla pagina 1 latina: `/home/user/facile_edizione/latino_cover_asset_0.png`.

Riutilizzare le immagini esistenti. Per nuovi soggetti/nuove lingue leggere la skill immagini, usare il riferimento originale con `media_generate_from_images`, mantenere stile clay adulto e non rigenerare errori a pagamento senza consenso.

## Ricostruzione operativa

Dipendenze: Python, WeasyPrint, BeautifulSoup4, PyMuPDF, numpy e OpenDyslexic installato. I sorgenti originali restano necessari per icone, CSS e font; gli asset delle copertine sono inclusi nella skill. Se mancano HTML o PDF base chiedere il file/repository corretto, non ricostruire a memoria.

```bash
S=/home/user/skills/quaderno-mappe-lingue
export LF_WORKDIR=/home/user/facile_edizione
# Leggere dai sorgenti correnti, creare inventory.json e copiare solo gli asset mancanti.
python3.11 "$S/scripts/prepara_collana_facile.py"
# Rigenerare tutte le lingue oppure passare en, fr o es.
python3.11 "$S/scripts/build_collana_facile.py"
# Verificare ogni pagina rispetto ai PDF base, escluso il solo footer.
python3.11 "$S/scripts/verifica_collana_facile.py"
```

Per prova isolata: impostare `LF_WORKDIR` a un’altra cartella. Preparazione: opzioni `--languages en fr es`, `--en-html`, `--en-pdf` e analoghe per cambiare sorgenti. Build: `en --html-only` per testare solo HTML. Verifica: `en` per una sola lingua. Cambiare esplicitamente la lista se si prepara un sottoinsieme; non usare il build senza argomenti con inventario parziale.

Per una mappa nuova, rigenerare prima HTML e PDF BASE con il build della lingua e `render_quaderno.py`, poi preparare di nuovo l’inventario e costruire FACILE. Il confronto della versione editoriale deve essere fatto con il PDF base che contiene la stessa modifica autorizzata; confrontare separatamente la nuova mappa con la precedente quando occorre accertare l’assenza di modifiche collaterali.

Non sovrascrivere gli originali. I manifest indicano SHA-256 della sezione mappe, numero mappe e percorsi di origine. Non confondere file `build_collana.py` della cartella storica con `scripts/build_collana_facile.py` incorporato e parametrizzabile.

## Checklist tecnica e visiva

- Assicurare identità byte della sezione HTML mappe; identità delle singole schede; CSS preesistente non riscritto.
- Confrontare **tutte** le pagine delle mappe per testo esatto e pixel. Baseline verificata: inglese 51/51; francese 40/40; spagnolo 36/36. Escludere solo gli ultimi 55pt dei fogli, riservati al footer; se un modello ha contenuti più bassi adattare il ritaglio verificando di non escludere parti della mappa.
- Non fermarsi al solo flag PDF taggato. Controllare `Lang`, segnalibri, immagine con alt, ordine di lettura e collegamenti; non promettere certificazione PDF/UA completa senza validatore specialistico.
- Gestire link interni PyMuPDF sia `LINK_GOTO` sia `LINK_NAMED` (nel render WeasyPrint possono essere `kind=4` con `nameddest`, `page` e `to`). Controllare i numeri stampati dell’indice e tutte le destinazioni `mNN`.
- Verificare copertine, le quattro guide, tutte le pagine dell’indice, almeno una coppia di mappe per lingua, pagina DIRECTIONS e ultima pagina. Non accettare righe orfane, tagli o sovrapposizioni.
- Rispettare i vincoli dell’originale: non «risolvere» densità o buchi preesistenti cambiando mappe dichiarate immutabili.
- Usare `send_attachment` con tutti i PDF richiesti e, se utile, l’anteprima delle copertine; non allegare log o JSON come sostituti dei documenti finali.

