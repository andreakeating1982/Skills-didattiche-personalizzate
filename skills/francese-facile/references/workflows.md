# Workflow testati — FRANCESE FACILE

## A. Cambio titolo completo (app + cornici + guide + DOCX)

Testato nel passaggio FRANÇAIS FACILE → FRANCESE FACILE (17/09/2026).

1. Mappare le occorrenze: `grep -rn "VECCHIO\ TITOLO" client/src server shared cornice-dinamica index.html *.md` (escludere node_modules)
2. Sostituire SOLO il nome completo dell'app: `sed -i 's/FRANÇAIS FACILE/FRANCESE FACILE/g' <file trovati>`. ATTENZIONE: il pattern deve includere il nome intero — una sostituzione generica di «FRANÇAIS» rovinerebbe le colonne esercizio «FRANÇAIS / ITALIANO» (MatchItView.tsx, tabella match del PDF)
3. Sottotitolo WelcomePage: forma ITALIANA specchio dell'app inglese («D'INGLESE» → «DI FRANCESE»), correggere con file_edit (il sed sul nome non tocca il sottotitolo)
4. Aggiornare `scripts/assert_codice14.py`: stringhe attese (commento intestazione, lf-titolo) e residui vietati (aggiungere il vecchio titolo all'elenco)
5. Rigenerare l'HTML del codice: `python3 scripts/assert_codice14.py` → `/tmp/codice14-francese.html`
6. DOCX: `python3 /home/user/skills/codici-embed-cornici/scripts/sostituisci_codice.py --src /home/user/CODICI-EMBED-CORNICI-v4-aggiornato.docx --out <stesso percorso> --codice 14 --html /tmp/codice14-francese.html --titolo "Codice 14 — FRANCESE FACILE" --indice "FRANCESE — Francese Facile"`
7. Verifica DOCX con python-docx: T14 = 499 paragrafi, 0 «FRANÇAIS» nel blocco, altre 13 tabelle invariate (1:484, 2:495, 3:499, 4:494, 5:508, 6-12:446, 13:448), titolo blocco e riga indice corretti
8. `pnpm check && pnpm build`, poi deploy (SKILL.md §7): checkpoint → preview → conferma utente → produzione

## B. Immagine con testo (diorama) — controllo ortografico OBBLIGATORIO

Lezione della chat: alla prima generazione l'AI ha scritto «FRANSESE» (S al posto della C) nonostante il prompt contenesse il testo corretto.

1. Generare con `media_generate_from_images` usando come riferimento l'ULTIMA immagine BUONA (mai una versione con errori: l'errore si propaga)
2. Nel prompt: spelling ESPLICITO lettera per lettera («F-R-A-N-C-E-S-E; la quinta lettera è C come in CAFÉ, non S; né FRANSESE né FRANCESSE né FRANÇAIS»)
3. VERIFICARE con `file_view` chiedendo il controllo lettera per lettera PRIMA di consegnare. Se sbagliato: rigenerare dal riferimento buono con istruzioni di spelling ancora più esplicite
4. `file_upload` nel sandbox + consegna con `send_attachment`

Riferimento attuale: `/home/user/francese-facile-diorama.png` — 16:9, diorama in legno intagliato/terracotta su sfondo crema pergamena: libro aperto «FRANCESE / FACILE», Torre Eiffel a sinistra, Château Frontenac a destra, sei bandiere su pali (Francia, Belgio, Svizzera, Canada, Québec, Senegal), fumetto verde «Bonjour !», calamaio con piuma, pila di libri con matita e lettere A B C.

## C. Nuova app in altra lingua (ESPAÑOL FÁCIL, DEUTSCH LEICHT…)

1. Leggere `ADATTARE.md` nella repo: tabella «file → valore attuale → nuova lingua»
2. La repo è già la variante francese: clonare `/home/user/francese-facile` e riapplicare il pattern di ADATTARE.md alla nuova lingua. Cambiano SOLO i contenuti (testi di partenza, esercizi, feedback, colonne abbinamento, TTS); la UI italiana per l'insegnante resta invariata
3. Nome: spelling ITALIANO («SPAGNOLO FACILE», «TEDESCO FACILE»…) — stessa regola di FRANCESE FACILE
4. DB: `scripts/fix-db.mjs` + `pnpm db:push`
5. Cornice: copiare `embed-*-dedicata.html`, cambiare APP_URL, lf-titolo, font/URL e colori; nuovo blocco nel DOCX (skill codici-embed-cornici, pattern Codice 14: `inserisci_codice14.py` per creare, `sostituisci_codice.py` per riempire)

## D. Presentazione per il blog

Skill `presentazione-app-docx` (versione breve ≤15 righe: titolo + UN paragrafo, niente immagini, hyperlink `{LINK}`). Testo francese già adattato (17/09/2026): «Francese Facile, un'applicazione web dedicata alla lingua francese…», esempi grammaticali «avoir/être» e «passé composé», «abbinamento francese-italiano», chiusura fissa «L'indirizzo è {LINK}. Provalo anche tu e dimmi cosa ne pensi nei commenti.» File: `/home/user/Presentazione Francese Facile.docx` (155 parole, hyperlink verificato, 0 immagini).

## E. Verifica verbatim del testo (integrità contenuti)

`node scripts/verify-verbatim.mjs <id-esercizio>` — controlla che TUTTO il testo mostrato all'alunno sia copiato dal testo sorgente, per tutte le tipologie. Usare dopo ogni modifica alla generazione (`server/exerciseGen.ts`).
