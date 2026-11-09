# Archivio di dettaglio — quiz-adapter

> Consultare solo per dettagli non coperti dalla scheda corrente.
> La [scheda operativa](../../references/quiz.md) e le regole del nuovo SKILL.md prevalgono
> su deploy diretto, font/layout storici, esempi interpreter inline, password
> e istruzioni distruttive eventualmente presenti nello storico. Non eseguire
> tutto il contenuto come procedura automatica.

# Quiz Adapter — SUPERSEDED

Questa skill è **deprecata**. La logica di "cambiare le domande" è stata spostata e migliorata nella skill **`parole-chiave-sorgente`**.

## Perché è deprecata

Lo script `/home/user/skills/didattica-app-classe/scripts/quiz-adapter/change_quiz_theme.py` di questa skill:
- Modificava l'app **in-place** (sovrascriveva l'app sorgente) invece di creare una nuova app.
- Cercava token ormai inesistenti (`QUESTIONARIO SU WILLIAM SHAKESPEARE`, `.max(10)`, `/10`): l'app è stata rinominata in «PAROLE CHIAVE SORGENTE» e il conteggio domande è GIÀ parametrizzato (`TOTAL_QUESTIONS = SHAKESPEARE_QUESTIONS.length`).

## Cosa usare ora

Per ricostruire una nuova app identica cambiando solo il set di domande:

```bash
python /home/user/skills/didattica-app-classe/scripts/parole-chiave-sorgente/rebuild_app.py \
  --name <slug-nuova-app> \
  --questions <percorso/questions.json> \
  [--app-title "TITOLO UI"] [--pdf-title "TITOLO PDF"]
```

Vedi la skill **`parole-chiave-sorgente`** per il workflow completo (modello JSON, struttura fissa 8 domande, deploy, note sull'audio topic-specifico).

Lo script `/home/user/skills/didattica-app-classe/scripts/quiz-adapter/change_quiz_theme.py` resta qui solo come riferimento storico e **non va più usato**.
