#!/usr/bin/env node
/**
 * qa_pdf_layout.mjs — Verifica RAPIDA del layout del PDF della linea del tempo
 * (margini ~3 cm sui 4 lati, centratura, assenza di sbordi) SENZA aprire il
 * browser: replica in Node la geometria esatta di client/src/lib/timelinePdf.ts
 * usando jsPDF (dal progetto) e i font veri OpenDyslexic (dal progetto).
 *
 * Non disegna le 7 icone reali (il crop avviene nel browser): al loro posto
 * disegna un rettangolo tratteggiato con le stesse dimensioni/posizione, così
 * si controllano i MARGINI e l'incorniciatura. Uso tipico:
 *
 *   node scripts/qa_pdf_layout.mjs [--root /home/user/espana-xix-match]
 *   pdftoppm -png -r 120 /tmp/qa_timeline_pdf.pdf /tmp/qa_timeline_pdf
 *   # poi ispezionare visivamente /tmp/qa_timeline_pdf-1.png (file_view)
 *
 * Criteri di QA (requisiti docente, verificati in chat 9/9/2026):
 *   • aria bianca ≥ ~30 mm sui 4 lati (contenuto dentro [30..267]×[30..180]);
 *   • titolo, figure, eje, anni e titoli ben distanziati, niente sbordi;
 *   • il bordo esterno delle figure esterne sta a ~33 mm dal lato (EDGE).
 */
import { createRequire } from "module";
import { readFileSync, existsSync } from "fs";
import { join, resolve } from "path";
import { spawnSync } from "child_process";

const argRoot = process.argv.indexOf("--root");
const ROOT = argRoot !== -1 ? resolve(process.argv[argRoot + 1]) : process.cwd();

const require = createRequire(join(ROOT, "package.json"));
const { jsPDF } = require("jspdf");

// ── Costanti (SPECCHIO di timelinePdf.ts: tenere allineate) ────────────────
const PAGE_W = 297; // landscape A4 (mm)
const PAGE_H = 210;
const M = 30; // margine richiesto sui 4 lati
const MM_PER_PT = 0.352778;
const PLUM = [59, 24, 73];
const BORDEAUX = [122, 31, 43];
const GOLD = [201, 162, 39];
const INK = [44, 24, 16];
const GREY = [110, 100, 92];
const mmLH = (s, f) => s * f * MM_PER_PT;

const events = [
  ["1808", "Guerra de Independencia"],
  ["1812", "Constitución de Cádiz"],
  ["1833", "I Guerra Carlista"],
  ["1868", "La Gloriosa"],
  ["1873", "Primera República"],
  ["1875", "Restauración borbónica"],
  ["1898", "Desastre del 98"],
];
const n = events.length;

// ── Font veri dal progetto (se mancano, si usa times con avviso) ───────────
function loadFonts(doc) {
  const reg = join(ROOT, "client/public/fonts/OpenDyslexic-Regular.ttf");
  const bold = join(ROOT, "client/public/fonts/OpenDyslexic-Bold.ttf");
  if (existsSync(reg) && existsSync(bold)) {
    doc.addFileToVFS("OpenDyslexic-Regular.ttf", readFileSync(reg).toString("base64"));
    doc.addFileToVFS("OpenDyslexic-Bold.ttf", readFileSync(bold).toString("base64"));
    doc.addFont("OpenDyslexic-Regular.ttf", "OpenDyslexic", "normal");
    doc.addFont("OpenDyslexic-Bold.ttf", "OpenDyslexic", "bold");
    doc.setFont("OpenDyslexic", "normal");
    return "OpenDyslexic";
  }
  console.warn("⚠ Font OpenDyslexic non trovati in client/public/fonts/ — uso times.");
  doc.setFont("times", "normal");
  return "times";
}

// ── Geometria incassata (specchio di timelinePdf.ts) ───────────────────────
const EDGE = M + 3; // 33 mm
let iconW = 32;
for (let i = 0; i < 3; i++) {
  const span = (PAGE_W - EDGE * 2 - iconW) / (n - 1);
  iconW = Math.min(32, Math.max(12, span - 1));
}
const iconH = iconW * (200 / 176); // ICON_H_FR/ICON_W_FR = 200/176 ≈ 1.136
const first = EDGE + iconW / 2;
const span = (PAGE_W - EDGE * 2 - iconW) / (n - 1);
const iconTop = 66;
const axisY = iconTop + iconH + 16;
const axisH = axisY + 4;
const xAxis0 = M + 7;
const xAxis1 = PAGE_W - M - 7;
const yearSize = 16;
const titleSize = 15;
const titleLH = mmLH(titleSize, 1.5);
const yearTop = axisH + 7;
const titleY0 = yearTop + mmLH(yearSize, 1.25) + 5;

console.log(`QA layout PDF — root: ${ROOT}`);
console.log(`  M=${M}mm  EDGE=${EDGE}  iconW=${iconW.toFixed(2)}  iconH=${iconH.toFixed(2)}`);
console.log(`  first=${first.toFixed(2)}  span=${span.toFixed(2)}  iconTop=${iconTop}`);
console.log(`  axisY=${axisY.toFixed(2)}  axisH=${axisH.toFixed(2)}  eje ${xAxis0}→${xAxis1} (punta ${xAxis1 + 2})`);
console.log(`  yearTop=${yearTop.toFixed(2)}  titleY0=${titleY0.toFixed(2)}  ultima riga titolo≈${(titleY0 + 3 * titleLH).toFixed(2)}`);
const lastLine = titleY0 + 3 * titleLH;
console.log(`  Controllo margini: sx/figura≈${first - iconW / 2}mm  dx/figura≈${PAGE_W - (first + span * (n - 1) + iconW / 2)}mm  alto≈${46}mm  basso≈${(PAGE_H - lastLine).toFixed(1)}mm`);
if (lastLine > PAGE_H - M + 1 || first - iconW / 2 < M - 1) {
  console.error("❌ Il layout NON rispetta i margini ~3 cm: rivedere le costanti.");
  process.exitCode = 1;
} else {
  console.log("✓ Il layout sta dentro i margini ~3 cm.");
}

const doc = new jsPDF({ orientation: "landscape", unit: "mm", format: "a4" });
const font = loadFonts(doc);

// Intestazione (specchio)
doc.setTextColor(...PLUM);
doc.setFontSize(21);
doc.setFont(font, "bold");
doc.text("Marco histórico del Romanticismo en España", PAGE_W / 2, 46, { align: "center", baseline: "top" });
doc.setTextColor(...GREY);
doc.setFontSize(12);
doc.setFont(font, "normal");
doc.text("La línea del tiempo · siglo XIX (1808–1898)", PAGE_W / 2, 56, { align: "center", baseline: "top" });
doc.setDrawColor(...GOLD);
doc.setLineWidth(0.8);
doc.line(M, 61, PAGE_W - M, 61);

// Figure: rettangolo tratteggiato al posto del crop reale (QA dei margini)
for (let i = 0; i < n; i++) {
  const xi = first + i * span;
  doc.setDrawColor(150, 150, 150);
  doc.setLineWidth(0.3);
  doc.setLineDashPattern([1.2, 1.2], 0);
  doc.rect(xi - iconW / 2, iconTop, iconW, iconH, "S");
  doc.setLineDashPattern([], 0);
}

// Eje + freccia
doc.setDrawColor(...BORDEAUX);
doc.setLineWidth(1.1);
doc.line(xAxis0, axisH, xAxis1 - 3, axisH);
doc.line(xAxis1 - 3, axisH, xAxis1 + 2, axisH);
doc.line(xAxis1 - 1, axisH - 2.4, xAxis1 + 2, axisH);
doc.line(xAxis1 - 1, axisH + 2.4, xAxis1 + 2, axisH);

// Anni e titoli
for (let i = 0; i < n; i++) {
  const xi = first + i * span;
  const colW = span - 2;
  doc.setDrawColor(...BORDEAUX);
  doc.setLineWidth(0.6);
  doc.line(xi, axisH - 2, xi, axisH + 2);
  doc.setTextColor(...PLUM);
  doc.setFontSize(yearSize);
  doc.setFont(font, "bold");
  doc.text(events[i][0], xi, yearTop, { align: "center", baseline: "top" });
  doc.setTextColor(...INK);
  doc.setFontSize(titleSize);
  doc.setFont(font, "normal");
  const lines = doc.splitTextToSize(events[i][1], colW);
  let y = titleY0;
  for (const line of lines.slice(0, 3)) {
    doc.text(line, xi, y, { align: "center", baseline: "top" });
    y += titleLH;
  }
}

const out = "/tmp/qa_timeline_pdf.pdf";
doc.save(out);
console.log(`Salvato ${out} — convertire con: pdftoppm -png -r 120 ${out} /tmp/qa_timeline_pdf`);
