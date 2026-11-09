# Struttura del prompt di scena (3 strati)

Ogni clip video viene generato da un prompt composto da TRE strati, in quest'ordine:

```
[STRATO CONTENUTO — cosa succede: personaggi, oggetti, azione, emozione, ambiente] +
[STRATO CAMERA — movimento lento, sempre presente] +
[STRATO STILE — il suffisso CLAY (templates/clay-style.txt), identico per TUTTE le scene]
+ REFS: 1–2 immagini di riferimento (media_generate_from_images) per coerenza
```

## Movimenti di camera consigliati (lenti, da documentario)
- slow push-in · slow pull-back · slow pan · slow zoom · slow tracking shot · slow orbit · slow lateral camera · slow macro zoom

## Regole
- Chiedere SEMPRE un'azione concreta ("hands the crown", "tearing up a paper document", "placing a crown on his head"): il generatore anima meglio richieste esplicite.
- NON chiedere testi; se la scena contiene documenti/giornali/bandiere, prevedere comunque il controllo QA.
- Usare la stessa immagine di riferimento per lo stesso personaggio in tutte le scene.

## Esempi reali (progetto "Marco histórico del Romanticismo en España")

### Apertura (clip01)
"A majestic claymation diorama of Spain in the 19th century: a miniature Spanish royal palace on a hill with flag waving, on the left a French army with cannons invading, on the right a clay sailing ship sinking in the sea, dramatic clouds, slow camera push-in over the miniature landscape. Claymation stop-motion diorama, plasticine clay texture with visible fingerprints, miniature figures and sets, warm cinematic lighting, dramatic sky, epic documentary style, 16:9 widescreen."

### Scena centrale (clip09 — Cortes di Cádiz, testo corretto sul documento)
"Claymation scene: deputies of the Cortes gathered around a long table in a clay assembly hall, an open book being signed with a quill, a paper document unrolling showing a constitution, coastal city of Cádiz visible through windows, warm candlelight. Claymation stop-motion diorama, plasticine clay texture with visible fingerprints, miniature figures and sets, warm cinematic lighting, dramatic sky, epic documentary style, 16:9 widescreen."

### Chiusura (clip35)
"Claymation final symbolic scene: a lone clay figure standing on a hill looking at a horizon where the century's images fade — battle, constitution, queens, republic, restoration — as a big clay question mark forms in the sky, dusk light, slow pull-back. Claymation stop-motion diorama, plasticine clay texture with visible fingerprints, miniature figures and sets, warm cinematic lighting, dramatic sky, epic documentary style, 16:9 widescreen."
