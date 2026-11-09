# Risorse incluse e condizioni d’uso

I percorsi seguenti sono interni a questa skill. I file originari restano
integri nel backup privato; qui sono ricollocati e i percorsi adattati.
Le schede canoniche sostituiscono le prescrizioni storiche non più valide.

| Profilo | Risorsa | Nota |
|---|---|---|
| video-claymation-didattico | [assemble_claymation.py](../scripts/video-claymation-didattico/assemble_claymation.py) | Controllare dipendenze e --help; non eseguire durante validazione offline. |
| video-claymation-didattico | [plan_scene.py](../scripts/video-claymation-didattico/plan_scene.py) | Controllare dipendenze e --help; non eseguire durante validazione offline. |
| video-claymation-didattico | [qa_frames.py](../scripts/video-claymation-didattico/qa_frames.py) | Controllare dipendenze e --help; non eseguire durante validazione offline. |
| video-claymation-didattico | [Dettagli originali](originali/video-claymation-didattico.md) | Solo ricerca mirata, subordinati alla scheda corrente. |
| video-claymation-didattico | [workflow-report.md](video-claymation-didattico/workflow-report.md) | Riferimento a richiesta. |
| modello-3d-didattico | [costruisci_modello.py](../scripts/modello-3d-didattico/costruisci_modello.py) | Controllare dipendenze e --help; non eseguire durante validazione offline. |
| modello-3d-didattico | [ritaglia_figure.py](../scripts/modello-3d-didattico/ritaglia_figure.py) | Editing2D storico: non usare; preferire strumenti media. |
| modello-3d-didattico | [valida_glb.js](../scripts/modello-3d-didattico/valida_glb.js) | Controllare dipendenze e --help; non eseguire durante validazione offline. |
| modello-3d-didattico | [Dettagli originali](originali/modello-3d-didattico.md) | Solo ricerca mirata, subordinati alla scheda corrente. |
| modello-3d-didattico | [report-3d.md](modello-3d-didattico/report-3d.md) | Riferimento a richiesta. |
| circolari-audio | Nessun allegato originale recuperato | Non dichiarare inclusi: scripts/normalizza_audio.sh originale. |


## PODCAST REALTÀ VIRTUALE — APPROVATO 5 NOVEMBRE 2026

[Profilo e baseline approvati](podcast-vr-approvato-2026-11-05.md): il template `../templates/realta-virtuale-podcast-approvato-2026-11-05/` include il PDF preciso, il video finale identico, la copertina originale, la trascrizione con indice e le nove clip con manifest locale e hash. Non comprende la skill separata `podcast-didattici` se non disponibile; non presentarla come recuperata. Nessuna generazione necessaria per verificare i file.

## AUDIO PDF — AGGIORNAMENTO 1 NOVEMBRE 2026

Risorse nuove incluse: `audio-pdf-due-voci.md`, `../scripts/estrai_pdf_audio.py`, `../scripts/assembla_audio_pdf.py` e `../templates/manifest-audio-esempio.json`. Gli script non richiamano motori TTS: richiedono clip già generate, estraggono/montano/verificano e lasciano l’ascolto in sospeso. Sono portabili, senza URL privati o percorsi dei lavori recenti incorporati come dipendenze. Le skill generali audio-generation/video-generation/image-generation restano separate e invariate.

