# Operazioni con le Frazioni

Profilo math-input-panel: /home/user/math-input-panel, web-static. File:
FractionExercises.tsx, NumberInputCanvas, MathDrawCanvas, FractionDisplay,
index.css e server minimale se presente. Verificare la versione corrente
prima di applicare font o grandezze dei vecchi appunti.

## Preservare le operazioni

- Addizione/sottrazione: mcm, fattori, moltiplicazioni e numeratore finale
  verificati separatamente; denominatori non nulli.
- Moltiplicazione/divisione: rispettare parentesi e associatività. Non
  invertire indiscriminatamente tutte le frazioni dopo la prima: invertire
  gli operandi divisori secondo la sequenza reale di operazioni. La regola
  storica sulle catene di sole divisioni non è una regola generale.
- RICOPIA: prodotti centrati con items-center, nessun offset magico su ×;
  barrature monocromatiche, annotazioni e frazioni coerenti.
- Conservare la semplificazione, gli arrotondamenti previsti e le risposte
  accettate. Non cambiare calcolo per un problema di margine o colore.

## PDF, embed e accessibilità

Preservare l'export effettivo. Nella versione storica stampa i notebook
copiando gli stili pagina e forzando Cambria Math12pt; non imporre questo
font alle altre app. Verificare DOM, font, wrapping e SVG stampati reali.
Per la cornice dinamica mantenere tokenv3/anti-loop se implementati; Welcome
lf-embedded e altezza reale, non min-h-screen in iframe. Aggiornare README,
ACCESSIBILITA, DEPLOY-RENDER e GUIDA-IA quando realmente toccati.

Provare le quattro operazioni, zeri/negativi/semplificazioni, input manoscritto,
PDF e touch. Sorgenti skill complete e template embed inclusi; il progetto
applicativo completo è un prerequisito, non è contenuto in questo pacchetto.
