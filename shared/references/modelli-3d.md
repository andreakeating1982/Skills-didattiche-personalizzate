# Diorami didattici GLB/glTF

Originale completo conservato: script geometria/validatore e template dati.
Il ritaglio Python2D e la produzione di targhette raster citati nello storico
NON sono il percorso operativo per modificare immagini: usare i motori media
appropriati. Conservare lo script ritaglia_figure.py come risorsa storica,
non eseguirlo per eludere questa regola.

## Costruire la scena

Verificare fonte e coordinate/proporzioni, ottenere texture lecite con
trasparenza pulita; modellare a una scala unica PX. Creare basamento,
freccia/linea, sfere e targhe come geometria, con figure appoggiate e UV
corrette. Il codice per geometria/trimesh è distinto dall'editing2D.
Usare scripts/modello-3d-didattico/costruisci_modello.py solo con gli input
verificati e dopo controllo delle dipendenze; non presumere che una singola
immagine implichi un modello volumetrico completo.

Texture incorporate nel GLB; materiali PBR, alphaMode MASK/cutoff0.4 come
modello per evitare bordi traslucidi, senza imporlo a oggetti realmente
trasparenti. Nomi di mesh parlanti e nessuna risorsa esterna mancante.

## Validare e visualizzare

Il validatore scripts/modello-3d-didattico/valida_glb.js richiede il pacchetto
Node gltf-validator. Validare dopo ogni modifica; dichiarare0errori/0avvisi
solo se ottenuti realmente. Anteprime three.js con camera arretrata e poco
alta per leggere targhette del diorama largo/basso; controllare frontale e
dettagli oltre all'inquadratura hero.

Per FigminXR/MetaQuest e Sketchfab verificare dimensioni, materiali e
compatibilità. Il modello non contiene automaticamente interazioni di Figmin;
allestirle separatamente. Non caricare/postare su account o blog senza
conferma e accesso autorizzato. Consegnare GLB e supporti richiesti, non
soltanto uno screenshot. Dettagli nel report-3d conservato.
