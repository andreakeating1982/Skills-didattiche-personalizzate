---
name: quiz-adapter
description: "SUPERSEDED — usa invece la skill `parole-chiave-sorgente`. Adattava l'app Shakespeare Quiz a nuovi set di domande modificando i file in-place. Ora la ricostruzione di un'app identica con domande diverse si fa con scripts/rebuild_app.py della skill parole-chiave-sorgente (clona l'app sorgente e cambia solo le domande)."
---

# Quiz Adapter — SUPERSEDED

Questa skill è **deprecata**. La logica di "cambiare le domande" è stata spostata e migliorata nella skill **`parole-chiave-sorgente`**.

## Perché è deprecata

Lo script `scripts/change_quiz_theme.py` di questa skill:
- Modificava l'app **in-place** (sovrascriveva l'app sorgente) invece di creare una nuova app.
- Cercava token ormai inesistenti (`QUESTIONARIO SU WILLIAM SHAKESPEARE`, `.max(10)`, `/10`): l'app è stata rinominata in «PAROLE CHIAVE SORGENTE» e il conteggio domande è GIÀ parametrizzato (`TOTAL_QUESTIONS = SHAKESPEARE_QUESTIONS.length`).

## Cosa usare ora

Per ricostruire una nuova app identica cambiando solo il set di domande:

```bash
python /home/user/skills/parole-chiave-sorgente/scripts/rebuild_app.py \
  --name <slug-nuova-app> \
  --questions <percorso/questions.json> \
  [--app-title "TITOLO UI"] [--pdf-title "TITOLO PDF"]
```

Vedi la skill **`parole-chiave-sorgente`** per il workflow completo (modello JSON, struttura fissa 8 domande, deploy, note sull'audio topic-specifico).

Lo script `scripts/change_quiz_theme.py` resta qui solo come riferimento storico e **non va più usato**.
