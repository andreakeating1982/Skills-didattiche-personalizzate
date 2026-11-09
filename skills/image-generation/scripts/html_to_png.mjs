#!/usr/bin/env node
/**
 * Render an HTML file to a PNG image (for schedules, tables, cards, diagrams).
 *
 *   node html_to_png.mjs page.html out.png [--width 1080] [--scale 2] [--selector main] [--wait 0]
 *
 * --width     viewport width in CSS pixels (default 1080). Height follows the content.
 * --scale     device scale factor (default 2 = sharp on phones and slides)
 * --selector  capture only this element (default: the whole page)
 * --wait      extra milliseconds to wait before capturing (e.g. for charts or Mermaid)
 *
 * Needs Playwright with Chromium. Sandboxes made from the current template have
 * it (installed globally). Otherwise install it in the working folder, where the
 * script looks first:
 *   npm init -y >/dev/null; npm i playwright; npx playwright install --with-deps chromium
 */
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const args = process.argv.slice(2);
if (args.length < 2 || args.includes('--help')) {
  console.log(
    'usage: node html_to_png.mjs page.html out.png [--width 1080] [--scale 2] [--selector main] [--wait 0]',
  );
  process.exit(args.includes('--help') ? 0 : 1);
}
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] !== undefined ? args[i + 1] : fallback;
};
const htmlPath = path.resolve(args[0]);
const outPath = path.resolve(args[1]);
if (!fs.existsSync(htmlPath)) {
  console.error(`No such file: ${htmlPath}`);
  process.exit(1);
}

// The working folder first (a project's own install), then the global one.
const searchDirs = [process.cwd()];
try {
  searchDirs.push(
    path.dirname(execSync('npm root -g', { encoding: 'utf8' }).trim()),
  );
} catch {
  // npm missing: fall back to the usual global prefixes
}
searchDirs.push('/usr/lib', '/usr/local/lib');
let playwright;
search: for (const dir of new Set(searchDirs)) {
  const req = createRequire(path.join(dir, 'noop.js'));
  for (const name of ['playwright', 'playwright-core']) {
    try {
      playwright = req(name);
      break search;
    } catch {
      // try the next one
    }
  }
}
if (!playwright) {
  console.error(
    'Playwright is not installed. Run in this folder:\n  npm init -y >/dev/null; npm i playwright; npx playwright install --with-deps chromium',
  );
  process.exit(1);
}

const browser = await playwright.chromium.launch();
const page = await browser.newPage({
  viewport: { width: Number(opt('width', 1080)), height: 800 },
  deviceScaleFactor: Number(opt('scale', 2)),
});
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts?.ready);
const wait = Number(opt('wait', 0));
if (wait > 0) await page.waitForTimeout(wait);

const selector = opt('selector', null);
if (selector) {
  await page.locator(selector).first().screenshot({ path: outPath });
} else {
  await page.screenshot({ path: outPath, fullPage: true });
}
await browser.close();
console.log(outPath);
