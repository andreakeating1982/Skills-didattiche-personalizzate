# RIFERIMENTI BIBLIOGRAFICI IN BOX CREMA — 3 NOVEMBRE 2026

## QUANDO

Applicare a guide, articoli e quaderni discorsivi del blog che prevedono riferimenti bibliografici, salvo diversa istruzione esplicita o modello specialistico. Questa priorità aggiunge un requisito grafico: non autorizza a inventare fonti, riscrivere un documento o eliminare parti diverse da quelle indicate.

## AGGIORNAMENTO APPROVATO — NOTA NEL TESTO, FONTE UNA SOLA VOLTA

Nella Rosalía approvata il 4 novembre i riferimenti bibliografici completi ripetuti nel corpo sono stati tolti **solo dopo autorizzazione esplicita**, conservandoli nella bibliografia finale numerata; i richiami numerici in apice sono cliccabili verso la singola fonte pertinente. Applicare il criterio a lavori analoghi senza cancellare citazioni d'autore, nomi e contenuti discorsivi: preservare o spostare dati di provenienza utili, distinguere fonti originali da quelle consultate successivamente e non inventare attribuzioni. Controllare la corrispondenza semantica fonte-passaggio oltre alla destinazione e all'area positiva del link nel PDF. Per il caso e il CSS delle note vedere `rosalia-completa-approvata-2026-11-04.md`.

## IMPAGINAZIONE

- Conservare la sezione finale e il titolo **RIFERIMENTI BIBLIOGRAFICI**, coordinato ai banner e all’indice, salvo richiesta diversa. Nessuna immagine nella sezione.
- Presentare **anche le voci bibliografiche e i gruppi di riferimenti alle scene in box giallognoli/crema** come i normali box del corpo: sfondo `#fffaf0` e pagina bianca, bordi, font OpenDyslexic e interlinea coerenti col documento. Per altri colori esplicitamente approvati, rispettare il modello scelto.
- Ogni box rappresenta una voce o un nucleo bibliografico coerente; quando una voce lunga non entra, distribuirla in box consecutivi presso confini leggibili, **senza omettere o alterare dati, ordine, testo, URI, destinazioni o superfici cliccabili**. Non suddividere meccanicamente ogni frase. Le informazioni restano leggibili e in maiuscolo/minuscolo come originalmente citate; solo le intestazioni editoriali vanno in maiuscolo.
- Misurare **massimo cinque righe reali per ciascun box bibliografico**, inclusi eventuali titoli e link; non ridurre font, interlinea o margini per farlo entrare. Le sintesi e le mappe conservano le loro regole specifiche e non ereditano questo tetto. Non spezzare un box fra pagine, andare a capo negli URL senza troncarli e usare più pagine quando serve.
- Una nota sui riferimenti o la provenienza si inserisce solo se richiesta o prevista dal documento e non vietata. **Se l’utente chiede di eliminarla, non reinserirla**: conservare le informazioni di provenienza nella documentazione di lavoro, non come frase aggiunta nel PDF. Non retroattribuire fonti nuove all’autore originale.

## ESEMPIO TECNICO

```html
<section id="bibliografia">
  <h2>RIFERIMENTI BIBLIOGRAFICI</h2>
  <div class="ref-entry" id="rif-1">
    <div class="blk" data-bibliography-box>
      <p>[1] Autore, <em>Titolo</em>, Ente, anno.
        <a href="https://example.org/fonte">https://example.org/fonte</a></p>
    </div>
  </div>
</section>
```

I nomi, l’URL e i metadati dell’esempio sono segnaposto, non fonti reali. Il CSS effettivo usa `.blk { background:#fffaf0; break-inside:avoid; overflow-wrap:anywhere; }`, con tipografia e spaziature del documento. Marcare ogni voce `.ref-entry`/`[data-bibliography-entry]` e i gruppi di scene `.scene-entry`; usare `.blk`/`[data-bibliography-box]` per i box. Il controllo consente selettori e colore alternativi espliciti.

## COLLAUDO

```sh
python3 scripts/verifica_box_fonti.py documento.html --report box-fonti.json
python3 scripts/verifica_box_semantici.py documento.html --strict --report box.json
python3 scripts/verifica_fonti_bibliografia.py documento.html --pdf documento.pdf --report fonti.json
```

Il primo controllo esamina colore, cinque righe, box non frammentati e testo all’interno dei box **solo per le voci individuate dai selettori**; segnala i paragrafi non classificati. I test automatici non stabiliscono se le fonti siano pertinenti o veritiere, non certificano PDF/UA e non sostituiscono l’ispezione visiva, la verifica delle opere e l’esame di tutti i collegamenti nel PDF. Confrontare anche testo e pagine non modificate con la versione di partenza.

## CASO SPECIFICO SHAKESPEARE

Il 3 novembre l’utente ha chiesto di togliere il solo contenuto nella foto: frase iniziale «The original booklet did not list its sources…», titolo «NOTES ON HISTORICAL EVIDENCE» e relative quattro note. **Non reintrodurre questi elementi nel quaderno**; non togliere le cinque fonti o gli otto collegamenti alle scene. Mettere le fonti in cinque box e le scene in due box crema; sono risultati di questa edizione, non quote universali.

Versione verificata attuale (14 pagine): `WILLIAM_SHAKESPEARE_ROMEO_AND_JULIET_FONTI_IN_BOX.pdf`, SHA-256 `f67207768a8dfc7bccacdcdf165c815bb63cf1e61c09e379b34c418f18d59d8a`. Le pagine 1–12 sono identiche al pixel alla revisione precedente; nel corpo restano l’inglese e il quiz originali. I 15 rimandi interni e i 13 link esterni sono stati controllati strutturalmente. L’eliminazione delle precisazioni storiche è una scelta specifica dell’utente, non una regola generale per altri documenti. Nel registro `shakespeare-revisione-corrente-2026-11-03.json` sono riportati percorso, hash, sorgenti e QA; verificare la presenza della versione prima di procedere. L’approvazione esplicita della nuova edizione non è registrata.

