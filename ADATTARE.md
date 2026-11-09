# RIAPPLICARE LE SKILL AD ALTRI USI

## Cambiare soltanto contenuto

1. Scegliere la skill specifica e leggere il modello pertinente.
2. Creare una nuova cartella di progetto/output. Non sovrascrivere l’originale.
3. Documentare che cosa cambia: argomento, lingua, domande, grado di equazione, immagini, voce oppure solo layout.
4. Usare JSON/configurazioni/script previsti quando disponibili. Non riscrivere l’architettura di una app per cambiare le domande.
5. Conservare gli invarianti non modificati: accessibilità, contratti di classe, privacy, modelli PDF o formato della lettura.
6. Eseguire test tecnici e controllo del risultato effettivo. Non considerare valida una app soltanto perché lo script di clonazione è compilabile.

## Creare una nuova variante di skill

Leggere `skills/skill-creator/SKILL.md`. Copiare la skill di partenza sotto un **nuovo nome**, aggiornare `name` e `description`, modificare soltanto le parti necessarie, aggiungere risorse riproducibili. Non alterare in-place le skill generali fornite dalla piattaforma.

Tenere i materiali riutilizzabili nelle sottocartelle `scripts/`, `references/`, `templates/`. Non incorporare segreti, contenuti scolastici personali o percorsi assoluti nel nuovo codice: preferire argomenti CLI, variabili d’ambiente locali e `Path(__file__)`.

Validare la nuova skill con il validatore originale fornendo il percorso assoluto:

```sh
python3 skills/skill-creator/scripts/quick_validate.py /PERCORSO/ASSOLUTO/ALLA/NUOVA-SKILL
```

Il catalogo e il controllo del numero54rappresentano lo snapshot iniziale. Se si aggiungono/rimuovono skill, aggiornare `catalogo/skills.json`, `CATALOGO.md`, i test e il numero atteso in `tools/gestisci_skill.py`; poi rigenerare il manifest. Non mantenere il numero54come un vincolo per sempre.

## Adattare gli strumenti all’ambiente

Le skill possono citare servizi disponibili nell’ambiente originale. Se il nuovo agente non li ha, dichiarare il limite e usare soltanto strumenti realmente accessibili e autorizzati. La copia di una skill non installa API, account o modelli di IA.

