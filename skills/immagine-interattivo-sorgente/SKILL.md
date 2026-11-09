---
name: immagine-interattivo-sorgente
description: "Clona l'app IMMAGINE INTERATTIVA SORGENTE (in /home/user/romanticismo-interattivo) in una NUOVA app identica cambiando SOLO il set di domande (immagine di sfondo, audio, hotspot, segmenti audio, testo esplicativo). Usare quando l'utente chiede una nuova app simile/uguale alla sorgente con un contenuto diverso (nuovo argomento/tema), lasciando invariati: dashboard docente, codici classe a 4 cifre, sessioni, contatore studenti attivi, report PDF (una pagina per studente + griglia PUNTEGGIO), palette plum/gold e embed iframe. Copre: costruzione del JSON contenuto (anche da testo libero), clonazione da cartella locale o repo GitHub (flag --source di clone_app.py), verifica automatica, deploy preview/produzione, export ZIP per GitHub/Render. NON usare per modificare o mantenere l'app sorgente (usare immagine-interattivo)."
---

# IMMAGINE INTERATTIVA — Clonazione (nuova app con contenuto diverso)

Clona l'app sorgente in una nuova app identica, cambiando solo il set di domande.

## Riferimenti

| Risorsa | Valore |
|---------|--------|
| App sorgente | `/home/user/romanticismo-interattivo` |
| Script clonazione | `/home/user/skills/immagine-interattivo-sorgente/scripts/clone_app.py` |
| Esempio JSON | `/home/user/skills/immagine-interattivo-sorgente/templates/contenuto-esempio.json` |
| Repo GitHub sorgente | `https://github.com/<UTENTE>/<REPO>.git` (chiedere l'URL all'utente) |

## Cosa cambia vs cosa resta uguale

**Cambia solo** (il set di domande):
- `shared/exploraData.ts` → HOTSPOTS, AUDIO_SEGMENTS, SECTION_THEMES, TEXTO_EXPLICATIVO
- `client/public/romanticismo-sintesi.png` (immagine di sfondo)
- `client/public/audio/explicacion.m4a` (audio narrazione)
- (opzionale) titolo mostrato

**Resta identico**: dashboard docente, codici classe, sessioni, contatore studenti, report PDF, palette plum/gold, embed, rientro studente, logica hotspot/audio, e l'accessibilità completa (font OpenDyslexic UI+PDF, barra 5 moduli, TTS, alto contrasto, righello).

## Vincoli rigidi (rispettare SEMPRE)

- ESATTAMENTE **5 segmenti audio** (id 0-4): il flag "completato" usa `subs.length >= 5` e i 5 pallini usano `SEGMENT_COLORS[i]` (5 colori fissi).
- Punteggio totale **10** (somma di `hotspotIds.length` sui 5 segmenti): la UI mostra `X/10` e il server valida `max(10)`.
- ESATTAMENTE **5 sezioni** in `sections` (colori degli hotspot sull'immagine).
- Ogni `hotspot.section` deve esistere in `sections`; ogni `hotspotIds` deve riferirsi a id esistenti in `hotspots`.

## Workflow

1. Raccogliere dall'utente: immagine, audio (o testo della narrazione + timing), e il contenuto (hotspot con posizione/etichetta/info, 5 segmenti, 5 sezioni, testo esplicativo). Se mancano immagine o audio, chiederli.
2. Costruire `contenuto.json` con lo schema qui sotto (partire da `contenuto-esempio.json` come template).
3. Clonare — da cartella locale (default) OPPURE da repository GitHub:
   ```
   # cartella locale (default /home/user/romanticismo-interattivo)
   python3 /home/user/skills/immagine-interattivo-sorgente/scripts/clone_app.py \
     --name <nuova-cartella> --json contenuto.json \
     [--image immagine.png] [--audio audio.m4a] [--title "TITOLO"]

   # da repository GitHub (repo con l'app sorgente)
   python3 /home/user/skills/immagine-interattivo-sorgente/scripts/clone_app.py \
     --name <nuova-cartella> --source https://github.com/<UTENTE>/<REPO>.git \
     --json contenuto.json [--image immagine.png] [--audio audio.m4a]
   ```
4. Installare e verificare: `cd /home/user/<nuova-cartella> && pnpm install && pnpm check`
5. Deploy preview → verifica → production (previo checkpoint con `webdev_save_checkpoint`).
6. Aggiornare `client/public/embed.html` con il NUOVO URL di produzione (attributo `src` dell'iframe e id univoco).
7. Export ZIP per GitHub/Render.

## Schema JSON contenuto

```json
{
  "titolo": "IMMAGINE INTERATTIVA",
  "hotspots": [
    { "id": "libro-central", "section": "centro", "x": 50, "y": 49, "size": "lg", "label": "1. ...", "info": "..." }
  ],
  "audioSegments": [
    { "id": 0, "startTime": 0, "endTime": 31.5, "label": "...", "subtitle": "...", "hotspotIds": ["libro-central"], "prompt": "Tocad el punto 1" }
  ],
  "sections": {
    "centro": { "name": "Centro", "ring": "ring-amber-500/60", "dot": "bg-amber-500", "glow": "shadow-amber-500/30", "badge": "bg-amber-950/50 text-amber-300 border border-amber-500/30" }
  },
  "textoExplicativo": "..."
}
```

- `size`: `sm` | `md` | `lg`.
- `x`/`y`: percentuali 0-100 sull'immagine.
- `textoExplicativo`: testo mostrato dal pulsante "TESTO" (paragrafi separati da riga vuota).
- `subtitle`: trascrizione del segmento audio.

## Verifica automatica

`clone_app.py` verifica (ed esce con errore se violati): 5 segmenti, punteggio totale 10, hotspot validi, sezioni valide; stampa i "punti per domanda" (D1..D5) e il totale. Poi `pnpm check` valida i tipi TypeScript.
