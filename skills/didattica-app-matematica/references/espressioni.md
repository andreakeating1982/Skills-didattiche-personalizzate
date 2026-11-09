# Espressioni / Widget Metacognitivo

## Stato corrente8756 — precedenza

Leggere prima [espressioni-8756.md](espressioni-8756.md): layout pubblicato
pagina2 a640px, pagina3 adattiva fino a640px, scorrimento interno e toolbar
esterna. I limiti e il pacchetto8744 sotto sono una cronologia, non la
versione corrente. Nuovo ZIP8756 con manifest e ricostruzione distinta.

## Cronologia delle fonti recuperate8744

Profilo completato nella chat del progetto il 29/10/2026: recuperati gli
originali locali aggiornati alla produzione 8744. Leggere solo i riferimenti
pertinenti, inclusi nel pacchetto:
- `originali/espressioni-monomi-polinomi-SKILL.md`: procedura completa storica.
- `originali/espressioni-monomi-polinomi-seconda-pagina-8737.md`: layout,
  scorrimento interno e rifiniture 8744.
- `originali/espressioni-monomi-polinomi-photo-crop-8736.md`: trapianto cropper.

Non scambiare altre copie locali con la produzione senza confronto dei commit.
Pacchetto storico riordinato8744: ESPRESSIONI-MONOMI-POLINOMI-8744-GITHUB-RENDER-2026-10-29.zip,
333 payload +1 manifest, commit f5f3ace8f61d800c132c7cb3500aa8497ed9f419;
SHA-256 db3518a5904e0d705acef16b8379bcd334b1dbfa696b5605fc6f1a20606e8ede.
Leggere [espressioni-pacchetto-8744.md](espressioni-pacchetto-8744.md) per
mappa corrente, limiti delle varianti e procedure riordinate.
Esiti esatti della ricostruzione nel rapporto incluso
[verifica-pacchetto-2026-10-29.json](verifica-pacchetto-2026-10-29.json).
Nessun nuovo deploy/Render o test IA live: non confondere build e pubblicazione.

## Invarianti correnti

- App principale /home/user/espressioni-monomi-polinomi; variante universale
  /home/user/espressione-frazioni-potenze. Verificare contesto e sorgenti reali.
- IA propone, motore dispone: auditConti e verify-steps controllano i passaggi.
- Filosofia DSA: non dire mai la soluzione, neanche per iscritto/TTS; guidare.
- Decimali con virgola: trascrizione fedele 2,5; normalizzazione separata per
  calcolo, gestire anche 2{,}5. Box DECIMALI IN FRAZIONE, campo dec e test dedicati.
- Cropper della baseline Latino8731 mantenuto nella variante: modal=true,
  viewport mobile/iframe, drag diretto e PNG; trapiantare anche hook/CSS/heightSync.
- Pagine2/3 con altezza compatta e scrollbar interna, come specifica8756;
  le rifiniture produzione8744 restano valide:
  pezzi lunghi scorrono DENTRO piece-display senza uscire dai bordi. Non
  far scomparire cornici o pulsanti matita/cancella. Unica didascalia SCRIVI
  QUI L'ESPRESSIONE in grassetto scuro; titolo/dati studente rimossi dalla pagina2.
- PDF dinamico e cache: non considerare un risultato vecchio prova del nuovo
  motore; conservare rifiniture guida anche sui dati in cache.

## Procedere

Leggere le guide del progetto e recuperare ADATTARE-EQUAZIONI.md,
TRAPIANTO-FOTO.md, FILOSOFIA-DSA.md se presenti; non dichiararle incluse qui.
Prima di cambiare modulo usare banchi di prova per conti/decimali,
foto/ritaglio, flusso a5box, testo lungo con scroll e PDF. Non riusare
numeri o titoli della sorgente per una variante diversa. La pubblicazione
richiede la chat del progetto e una nuova approvazione; nessun deploy da qui.
