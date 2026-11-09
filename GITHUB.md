# CARICARE SU GITHUB

## Opzione consigliata: repository privato

1. Estrarre `SKILLS_IA_GITHUB_2026-11-01_v2_SINTESI_MAPPE.zip` sul computer.
2. Aprire GitHub con il proprio account e creare un nuovo repository **privato** (per esempio `skills-didattiche-ia`). La creazione/pubblicazione non è stata effettuata automaticamente.
3. Caricare **il contenuto estratto** della cartella `skills-didattiche-ia`, non soltanto lo ZIP: README, AGENTS, tools, catalogo, skills e shared devono essere visibili come file/cartelle del repository.
4. Fare il primo commit e conservare il nome del branch scelto.
5. Su un altro computer clonare il proprio repository, entrare nella cartella e verificare:

   ```sh
   python3 tools/gestisci_skill.py verifica
   ```

Il pacchetto non contiene file singoli da100 MB, quindi non richiede Git LFS per i file inclusi. La cartella `.git` non è inclusa e non vengono distribuiti token di accesso.

## Alternativa con Git locale

Dalla cartella estratta eseguire, dopo aver controllato i file:

```sh
git init
git add .
git commit -m "Importa raccolta skill IA"
git branch -M main
```

Creare il repository nel proprio account e aggiungere come `origin` l’URL che GitHub mostra; poi eseguire il push usando le proprie credenziali gestite da Git. Non inserire token nell’URL né nei file. I comandi sopra preparano un commit locale: da soli non pubblicano nulla.

## Passare da privato a pubblico

Prima verificare `docs/LICENZE_E_PUBBLICAZIONE.md`, diritti su immagini/font/istruzioni, riferimenti a progetti personali, credenziali e dati scolastici. La scansione tecnica non concede diritti di redistribuzione. Non introdurre una licenza globale incompatibile con i materiali inclusi.

