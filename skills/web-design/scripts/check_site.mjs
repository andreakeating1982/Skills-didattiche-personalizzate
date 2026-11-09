#!/usr/bin/env node
/**
 * Look at a website the way a visitor would, at desktop and phone widths.
 *
 *   node check_site.mjs <base-url> [out-dir] [--pages / /menu /visit] [--widths 1440,390] [--wait 600]
 *
 * For every page and width it saves two screenshots in out-dir (default
 * /home/user/site-check): <page>-<width>-top.png (the first screen) and
 * <page>-<width>-full.png (the whole page, cut at 12,000px). Then it prints:
 *   Problems  what a visitor notices: sideways scrolling, broken, stretched or
 *             blurry images, text cut off or running out of its box, low
 *             contrast, fonts that did not load, console errors, content
 *             still invisible, missing title or description
 *   Tells     patterns that make a site look generated (the web-design
 *             skill's "Defaults to avoid"): fix each one unless design.md
 *             says it is intended
 * The same data is written to report.json.
 *
 * Needs Playwright with Chromium. Sandboxes made from the current template
 * have it (installed globally). Otherwise install it in the working folder,
 * where the script looks first:
 *   npm init -y >/dev/null; npm i playwright; npx playwright install --with-deps chromium
 */
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const USAGE =
  'usage: node check_site.mjs <base-url> [out-dir] [--pages / /about] [--widths 1440,390] [--wait 600]';
const args = process.argv.slice(2);
if (!args.length || args.includes('--help')) {
  console.log(USAGE);
  process.exit(args.includes('--help') ? 0 : 1);
}

const positional = [];
const pages = [];
let widths = [1440, 390];
let wait = 600;
for (let i = 0; i < args.length; i += 1) {
  const arg = args[i];
  if (arg === '--pages') {
    while (args[i + 1] !== undefined && !args[i + 1].startsWith('--')) {
      pages.push(args[(i += 1)]);
    }
  } else if (arg === '--widths') {
    widths = String(args[(i += 1)] ?? '')
      .split(',')
      .map(Number)
      .filter((n) => n >= 200);
  } else if (arg === '--wait') {
    wait = Number(args[(i += 1)]) || 0;
  } else {
    positional.push(arg);
  }
}
const base = positional[0];
const outDir = path.resolve(positional[1] ?? '/home/user/site-check');
if (!/^https?:\/\//.test(base ?? '') || !widths.length) {
  console.error(USAGE);
  process.exit(1);
}
if (!pages.length) pages.push('/');

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

/* ------------------------------------------------------------------------ */
/* In-page code. These functions run in the browser, so they can't use      */
/* anything from this module.                                               */
/* ------------------------------------------------------------------------ */

/** Text in the first screen that is still invisible after load. */
function markHiddenAtLoad() {
  // Text inside an <svg> is part of a graphic (and has no innerText).
  const textEls = [...document.body.querySelectorAll('*')].filter(
    (el) =>
      !el.closest('svg') &&
      [...el.childNodes].some(
        (n) => n.nodeType === 3 && n.textContent.trim().length > 1,
      ),
  );
  const opacityOf = (el) => {
    let o = 1;
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const s = getComputedStyle(e);
      if (s.visibility === 'hidden' || s.display === 'none') return 0;
      o *= Number(s.opacity);
    }
    return o;
  };
  window.__hiddenBeforeScroll = textEls.filter((el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && opacityOf(el) < 0.1;
  });
  return window.__hiddenBeforeScroll
    .filter((el) => el.getBoundingClientRect().top < window.innerHeight)
    .map((el) =>
      (el.innerText ?? el.textContent ?? '')
        .trim()
        .replace(/\s+/g, ' ')
        .slice(0, 60),
    );
}

/** Scroll down the whole page (lazy images, reveal-on-scroll), then back up. */
async function scrollThrough() {
  const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  // 'instant' beats `scroll-behavior: smooth`, which would still be gliding
  // back up when the first-screen screenshot is taken.
  const jump = (top) => window.scrollTo({ top, left: 0, behavior: 'instant' });
  const step = Math.round(window.innerHeight * 0.8);
  for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
    jump(y);
    await pause(120);
  }
  jump(document.documentElement.scrollHeight);
  await pause(400);
  jump(0);
  await pause(500);
}

function analyze({ phone }) {
  const W = window.innerWidth;
  const H = window.innerHeight;
  const problems = [];
  const tells = [];
  const info = {};

  // --- helpers ------------------------------------------------------------
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const colorCache = new Map();
  /** Any CSS color (oklch, hsl, named...) to sRGB 0-255 plus alpha 0-1. */
  const rgba = (css) => {
    if (colorCache.has(css)) return colorCache.get(css);
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = '#000';
    ctx.fillStyle = css;
    ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
    const value = { r, g, b, a: a / 255 };
    colorCache.set(css, value);
    return value;
  };
  const hex = ({ r, g, b }) =>
    '#' +
    [r, g, b]
      .map((v) => Math.round(v).toString(16).padStart(2, '0'))
      .join('')
      .toUpperCase();
  const over = (top, bottom) => ({
    r: top.r * top.a + bottom.r * (1 - top.a),
    g: top.g * top.a + bottom.g * (1 - top.a),
    b: top.b * top.a + bottom.b * (1 - top.a),
    a: 1,
  });
  const luminance = ({ r, g, b }) => {
    const ch = (v) => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b);
  };
  const contrast = (a, b) => {
    const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  };
  const distance = (a, b) =>
    Math.sqrt((a.r - b.r) ** 2 + (a.g - b.g) ** 2 + (a.b - b.b) ** 2);
  const saturated = ({ r, g, b }) => Math.max(r, g, b) - Math.min(r, g, b) > 40;
  /** Hue in degrees, saturation and lightness 0-1. */
  const hsl = ({ r, g, b }) => {
    const [R, G, B] = [r / 255, g / 255, b / 255];
    const max = Math.max(R, G, B);
    const min = Math.min(R, G, B);
    const l = (max + min) / 2;
    const d = max - min;
    if (!d) return { h: 0, s: 0, l };
    const s = d / (1 - Math.abs(2 * l - 1));
    const h =
      max === R
        ? 60 * (((G - B) / d + 6) % 6)
        : max === G
          ? 60 * ((B - R) / d + 2)
          : 60 * ((R - G) / d + 4);
    return { h, s, l };
  };
  const styleOf = (el) => getComputedStyle(el);
  const opacityOf = (el) => {
    let o = 1;
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const s = styleOf(e);
      if (s.visibility === 'hidden' || s.display === 'none') return 0;
      o *= Number(s.opacity);
    }
    return o;
  };
  // Visible to a sighted visitor: has a real box, isn't screen-reader-only
  // (sr-only clips to 1px) and isn't faded out.
  const shown = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width <= 2 || r.height <= 2) return false;
    const s = styleOf(el);
    if (s.clip !== 'auto' || s.clipPath !== 'none') return false;
    return opacityOf(el) > 0.05;
  };
  /** Laid out somewhere a visitor can reach (not display:none, not off to the side). */
  const placed = (el) => {
    if (!el.getClientRects().length) return false;
    const r = el.getBoundingClientRect();
    return r.right > 0 && r.left < W;
  };
  const textOf = (el) =>
    (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ');
  const ownText = (el) =>
    [...el.childNodes]
      .filter((n) => n.nodeType === 3)
      .map((n) => n.textContent)
      .join(' ')
      .trim()
      .replace(/\s+/g, ' ');
  const label = (el, max = 50) => {
    const tag = el.tagName.toLowerCase();
    const text = textOf(el) || el.getAttribute('alt') || '';
    return text
      ? `${tag} "${text.slice(0, max)}${text.length > max ? '…' : ''}"`
      : tag;
  };
  const list = (items, n = 4) =>
    items.slice(0, n).join('; ') +
    (items.length > n ? `; +${items.length - n} more` : '');
  const firstFamily = (s) =>
    s.fontFamily
      .split(',')[0]
      .trim()
      .replace(/^["']|["']$/g, '');
  const GENERIC = new Set([
    'serif',
    'sans-serif',
    'monospace',
    'cursive',
    'fantasy',
    'system-ui',
    'ui-serif',
    'ui-sans-serif',
    'ui-monospace',
    '-apple-system',
    'BlinkMacSystemFont',
  ]);
  const MONO = /mono|code|courier|consol|menlo/i;

  const all = [...document.body.querySelectorAll('*')];
  const textEls = all.filter(
    (el) =>
      !['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName) &&
      !el.closest('svg') &&
      ownText(el).length > 1 &&
      shown(el),
  );

  // --- page basics ----------------------------------------------------------
  const title = document.title.trim();
  const description = document
    .querySelector('meta[name="description"]')
    ?.getAttribute('content')
    ?.trim();
  if (!title || /\{\{|example page|vite \+ react/i.test(title)) {
    problems.push(`Page title is missing or a placeholder ("${title}").`);
  }
  if (!description || /one-sentence summary/i.test(description)) {
    problems.push('Meta description is missing or a placeholder.');
  }
  const h1s = [...document.querySelectorAll('h1')].filter(shown);
  if (h1s.length !== 1) {
    problems.push(
      `The page has ${h1s.length} visible h1 headings (want exactly one).`,
    );
  }
  info.headings = [...document.querySelectorAll('h1, h2')]
    .filter(shown)
    .slice(0, 14)
    .map((h) => `${h.tagName.toLowerCase()}: ${textOf(h).slice(0, 70)}`);
  info.pageHeight = document.documentElement.scrollHeight;

  // --- sideways scrolling ---------------------------------------------------
  const docWidth = document.documentElement.scrollWidth;
  const clippedByAncestor = (el) => {
    for (
      let e = el.parentElement;
      e && e !== document.body;
      e = e.parentElement
    ) {
      const ox = styleOf(e).overflowX;
      if (ox !== 'visible' && e.getBoundingClientRect().right <= W + 1)
        return true;
    }
    return false;
  };
  const tooWide = all.filter((el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.right > W + 1 && !clippedByAncestor(el);
  });
  const outermost = tooWide.filter(
    (el) => !tooWide.some((other) => other !== el && other.contains(el)),
  );
  if (docWidth > W + 1) {
    problems.push(
      `The page scrolls sideways (${docWidth}px of content in a ${W}px window). Too wide: ${list(outermost.map((el) => label(el)))}.`,
    );
  } else if (outermost.length) {
    problems.push(
      `Elements stick out past the right edge (hidden by overflow on html/body, but phones can still scroll to them): ${list(outermost.map((el) => label(el)))}.`,
    );
  }

  // --- images ---------------------------------------------------------------
  // Tracking pixels and images in off-screen carousels don't count.
  const images = [...document.images].filter(placed);
  const broken = images.filter(
    (img) =>
      img.complete && img.naturalWidth === 0 && (img.currentSrc || img.src),
  );
  if (broken.length) {
    problems.push(
      `Broken images (${broken.length}): ${list(broken.map((img) => img.currentSrc || img.src))}.`,
    );
  }
  const pending = images.filter((img) => !img.complete);
  if (pending.length) {
    problems.push(
      `${pending.length} images never finished loading, even after scrolling: ${list(pending.map((img) => img.currentSrc || img.src))}.`,
    );
  }
  const stretched = [];
  const blurry = [];
  const noAlt = [];
  for (const img of images) {
    if (!img.naturalWidth || !shown(img)) continue;
    const r = img.getBoundingClientRect();
    const isSvg = /\.svg(\?|$)/i.test(img.currentSrc || img.src);
    if (!img.hasAttribute('alt')) noAlt.push(img.currentSrc || img.src);
    if (isSvg) continue;
    const fit = styleOf(img).objectFit;
    const ratio = r.width / r.height / (img.naturalWidth / img.naturalHeight);
    if (fit === 'fill' && Math.abs(ratio - 1) > 0.04) {
      stretched.push(
        `${img.currentSrc || img.src} (${Math.round(r.width)}x${Math.round(r.height)})`,
      );
    }
    // Needed pixels: the box size, or more when object-fit: cover crops it.
    const scale =
      fit === 'cover'
        ? Math.max(r.width / img.naturalWidth, r.height / img.naturalHeight)
        : r.width / img.naturalWidth;
    if (scale > 1.35 && r.width > 200) {
      blurry.push(
        `${img.currentSrc || img.src} (file ${img.naturalWidth}px, shown ${Math.round(r.width)}px)`,
      );
    }
  }
  if (stretched.length) {
    problems.push(
      `Stretched images (add object-cover or fix the box ratio): ${list(stretched)}.`,
    );
  }
  if (blurry.length) {
    problems.push(
      `Images shown larger than the file, so they look soft: ${list(blurry)}.`,
    );
  }
  if (noAlt.length) {
    problems.push(`Images without an alt attribute: ${list(noAlt)}.`);
  }

  // --- text cut off or spilling ---------------------------------------------
  const cut = [];
  for (const el of textEls) {
    const s = styleOf(el);
    if (s.display.startsWith('inline') && s.display !== 'inline-block')
      continue;
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) {
      cut.push(
        `${label(el, 40)} (${s.overflowX === 'visible' ? 'runs out of its box' : 'cut off'})`,
      );
    }
  }
  if (cut.length) problems.push(`Text wider than its box: ${list(cut)}.`);

  // One word alone on the last line of a big heading.
  const orphans = [];
  for (const h of document.querySelectorAll('h1, h2')) {
    if (!shown(h) || textOf(h).split(' ').length < 4) continue;
    const walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
    const tops = [];
    const range = document.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const re = /\S+/g;
      let m;
      while ((m = re.exec(node.textContent))) {
        range.setStart(node, m.index);
        range.setEnd(node, m.index + m[0].length);
        const rect = range.getBoundingClientRect();
        if (rect.height) tops.push(Math.round(rect.top));
      }
    }
    const last = Math.max(...tops);
    const lines = new Set(tops).size;
    if (lines > 1 && tops.filter((t) => Math.abs(t - last) < 4).length === 1) {
      orphans.push(label(h, 60));
    }
  }
  if (orphans.length) {
    problems.push(
      `Headings that end with one word alone on the last line (rebalance with text-wrap: balance, width or wording): ${list(orphans)}.`,
    );
  }

  // --- contrast -------------------------------------------------------------
  const lowContrast = [];
  let onImage = 0;
  const seenText = new Set();
  // Background behind each text block, weighted by its amount of text: the
  // most common one is the page's real background (body is often transparent).
  const backgrounds = new Map();
  for (const el of textEls.slice(0, 2500)) {
    const s = styleOf(el);
    const layers = [];
    let unknown = false;
    for (let e = el; e; e = e.parentElement) {
      const es = styleOf(e);
      if (es.backgroundImage !== 'none') {
        unknown = true;
        break;
      }
      const bg = rgba(es.backgroundColor);
      if (bg.a > 0) layers.push(bg);
      if (bg.a >= 0.99) break;
    }
    if (unknown) {
      onImage += 1;
      continue;
    }
    let background = { r: 255, g: 255, b: 255, a: 1 };
    for (const layer of layers.reverse()) background = over(layer, background);
    const bgKey = hex(background);
    backgrounds.set(bgKey, (backgrounds.get(bgKey) ?? 0) + ownText(el).length);
    const color = rgba(s.color);
    const text = over(color, background);
    const size = parseFloat(s.fontSize);
    const large = size >= 24 || (size >= 18.6 && Number(s.fontWeight) >= 700);
    const ratio = contrast(text, background);
    const need = large ? 3 : 4.5;
    const key = ownText(el).slice(0, 40);
    if (ratio < need && !seenText.has(key)) {
      seenText.add(key);
      lowContrast.push({
        ratio,
        line: `"${key}" ${ratio.toFixed(1)}:1 (${hex(text)} on ${hex(background)}, ${Math.round(size)}px)`,
      });
    }
  }
  lowContrast.sort((a, b) => a.ratio - b.ratio);
  if (lowContrast.length) {
    problems.push(
      `Low-contrast text (needs 4.5:1, or 3:1 for large text): ${list(
        lowContrast.map((c) => c.line),
        5,
      )}.`,
    );
  }
  if (onImage) {
    info.textOnImages = `${onImage} text blocks sit on images or gradients: check them in the screenshots.`;
  }

  // --- fonts ----------------------------------------------------------------
  const families = new Map();
  for (const el of textEls) {
    const fam = firstFamily(styleOf(el));
    families.set(fam, (families.get(fam) ?? 0) + 1);
  }
  const faces = [...document.fonts];
  const statusOf = (fam) => {
    const own = faces.filter(
      (f) => f.family.replace(/^["']|["']$/g, '') === fam,
    );
    if (!own.length) return 'no web font';
    if (own.some((f) => f.status === 'loaded')) return 'loaded';
    if (own.some((f) => f.status === 'error')) return 'failed to load';
    return 'not loaded';
  };
  info.fonts = [...families.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(
      ([fam, n]) =>
        `${fam} (${GENERIC.has(fam) ? 'generic' : statusOf(fam)}, ${n} text blocks)`,
    );
  const missingFonts = [...families.keys()].filter(
    (fam) => !GENERIC.has(fam) && statusOf(fam) !== 'loaded',
  );
  if (missingFonts.length) {
    problems.push(
      `Fonts named in the CSS that did not load from the web (visitors get a fallback): ${missingFonts.join(', ')}. Add them to the Google Fonts link (client/index.html, or the head() links in src/routes/__root.tsx in web-app) with the weights used.`,
    );
  }

  // --- colors ---------------------------------------------------------------
  const mainBg =
    [...backgrounds.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '#FFFFFF';
  const pageBg = rgba(mainBg);
  const buttonColors = new Map();
  for (const el of document.querySelectorAll('button, a, [role="button"]')) {
    if (!shown(el)) continue;
    const bg = rgba(styleOf(el).backgroundColor);
    if (bg.a < 0.9 || !saturated(bg)) continue;
    const key = hex(bg);
    buttonColors.set(key, (buttonColors.get(key) ?? 0) + 1);
  }
  const accent = [...buttonColors.entries()].sort(
    (a, b) => b[1] - a[1],
  )[0]?.[0];
  info.colors = `main background ${hex(pageBg)}, body text ${hex(rgba(styleOf(document.body).color))}${accent ? `, main button color ${accent}` : ''}`;

  // --- tells ----------------------------------------------------------------
  const tell = (text) => tells.push(text);
  const OVERUSED =
    /^(inter|roboto|arial|helvetica|fraunces|instrument serif|instrument sans|playfair display|dm serif display|dm serif text|dm sans|newsreader|space grotesk|ibm plex mono|space mono|geist|geist mono|poppins|montserrat|open sans|lato)$/i;
  const overused = [...families.keys()].filter((fam) => OVERUSED.test(fam));
  if (overused.length) {
    tell(
      `Default-looking fonts: ${overused.join(', ')}. Pick families for this subject (references/typography.md).`,
    );
  }
  const bgHsl = hsl(pageBg);
  if (bgHsl.h >= 25 && bgHsl.h <= 60 && bgHsl.l >= 0.86 && bgHsl.s >= 0.12) {
    tell(
      `Warm cream or paper page background (${hex(pageBg)}), the most common generated look.`,
    );
  }
  if (bgHsl.l < 0.1) {
    tell(
      `Near-black page background (${hex(pageBg)}), the second most common generated look.`,
    );
  }
  const accentHsl = accent ? hsl(rgba(accent)) : null;
  if (
    accentHsl &&
    accentHsl.h >= 5 &&
    accentHsl.h <= 35 &&
    accentHsl.s >= 0.35 &&
    accentHsl.l >= 0.25 &&
    accentHsl.l <= 0.65
  ) {
    tell(
      `Terracotta, copper or rust accent (${accent}), the most common generated accent.`,
    );
  }
  const coordinates = textEls.filter((el) =>
    /\d+\.\d+\s?°\s?[NSEW]\b/.test(ownText(el)),
  );
  if (coordinates.length) {
    tell(
      `Map coordinates used as decoration ("${ownText(coordinates[0]).slice(0, 30)}"). Give the address instead.`,
    );
  }
  const marquees = all.filter((el) => {
    const s = styleOf(el);
    return (
      s.animationName !== 'none' &&
      el.scrollWidth > W * 1.2 &&
      textOf(el).length > 20 &&
      placed(el)
    );
  });
  const outerMarquees = marquees.filter(
    (el) => !marquees.some((o) => o !== el && o.contains(el)),
  );
  if (outerMarquees.length) {
    tell(
      `${outerMarquees.length} scrolling marquee strip(s) of words ("${textOf(outerMarquees[0]).slice(0, 40)}…").`,
    );
  }

  const eyebrows = textEls.filter((el) => {
    const s = styleOf(el);
    const text = ownText(el);
    const size = parseFloat(s.fontSize);
    const spacing =
      s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing) / size;
    const caps =
      s.textTransform === 'uppercase' ||
      (/[A-Z]{3}/.test(text) && text === text.toUpperCase());
    return caps && size <= 14 && spacing >= 0.05 && text.length <= 48;
  });
  const aboveHeading = eyebrows.filter((el) => {
    const next = el.nextElementSibling;
    return (
      next &&
      (/^H[1-4]$/.test(next.tagName) ||
        next.querySelector(':scope > h1, :scope > h2, :scope > h3'))
    );
  });
  if (aboveHeading.length >= 2 || eyebrows.length >= 5) {
    tell(
      `${eyebrows.length} small tracked-out uppercase labels (${aboveHeading.length} right above a heading), e.g. ${list(
        eyebrows.map((el) => `"${ownText(el)}"`),
        3,
      )}. Keep a label only where it tells the visitor something.`,
    );
  }

  const accentWords = [];
  for (const h of document.querySelectorAll('h1, h2, h3')) {
    if (!shown(h) || textOf(h).split(' ').length < 3) continue;
    const hs = styleOf(h);
    const marked = [...h.querySelectorAll('em, i, span, strong, b, mark')].find(
      (part) => {
        const ps = styleOf(part);
        return (
          textOf(part).length < textOf(h).length * 0.6 &&
          (ps.fontStyle !== hs.fontStyle ||
            distance(rgba(ps.color), rgba(hs.color)) > 30 ||
            firstFamily(ps) !== firstFamily(hs) ||
            ps.backgroundImage !== 'none')
        );
      },
    );
    if (marked)
      accentWords.push(
        `"${textOf(h).slice(0, 50)}" (${textOf(marked).slice(0, 20)})`,
      );
  }
  if (accentWords.length) {
    tell(
      `Headlines with one word or phrase set apart in italic, color or another font: ${list(accentWords, 3)}.`,
    );
  }

  const upperCtas = [
    ...document.querySelectorAll('a, button, [role="button"]'),
  ].filter((el) => {
    if (!shown(el)) return false;
    const text = textOf(el);
    return (
      /[A-Za-z]{3}/.test(text) &&
      (styleOf(el).textTransform === 'uppercase' || text === text.toUpperCase())
    );
  });
  if (upperCtas.length >= 3) {
    tell(
      `${upperCtas.length} buttons or navigation links in all caps, e.g. ${list(
        upperCtas.map((el) => `"${textOf(el).slice(0, 25)}"`),
        3,
      )}. Use sentence case.`,
    );
  }

  const arrowCtas = [...document.querySelectorAll('a, button')].filter(
    (el) =>
      shown(el) &&
      (/(→|->|↗|⟶)\s*$/.test(textOf(el)) ||
        el.querySelector(
          '[class*="arrow-right"], [class*="arrow-up-right"], [class*="move-right"]',
        )),
  );
  if (arrowCtas.length >= 2) {
    tell(
      `${arrowCtas.length} links or buttons end with an arrow, e.g. ${list(
        arrowCtas.map((el) => label(el, 30)),
        3,
      )}.`,
    );
  }

  const dots = textEls.filter((el) => /\S\s·\s\S/.test(ownText(el)));
  if (dots.length >= 2) {
    tell(
      `${dots.length} lines joined with middle dots, e.g. ${list(
        dots.map((el) => `"${ownText(el).slice(0, 40)}"`),
        2,
      )}.`,
    );
  }
  const dashLabels = textEls.filter((el) => {
    const text = ownText(el);
    // A spaced em dash after a word; not an en dash in a range ("10:00 – 18:00").
    return text.length <= 60 && /\p{L}\s—\s\S/u.test(text);
  });
  if (dashLabels.length >= 2) {
    tell(
      `${dashLabels.length} short labels built as "word — fragment", e.g. ${list(
        dashLabels.map((el) => `"${ownText(el)}"`),
        2,
      )}.`,
    );
  }
  const numbers = textEls.filter((el) =>
    /^(0\d|\d{2}|No\.\s?\d+)\s*[./)—–-]?$/.test(ownText(el)),
  );
  if (numbers.length >= 3) {
    tell(
      `${numbers.length} numbered markers (01, 02, ...). Keep them only if the content is a real sequence (steps, a timeline).`,
    );
  }
  const emoji = textEls.filter((el) =>
    /\p{Emoji_Presentation}|\p{Extended_Pictographic}️/u.test(ownText(el)),
  );
  if (emoji.length) {
    tell(
      `Emoji in the page text (${emoji.length}), e.g. ${list(
        emoji.map((el) => `"${ownText(el).slice(0, 30)}"`),
        2,
      )}. Use lucide icons or nothing.`,
    );
  }
  const monoLabels = textEls.filter((el) => {
    const s = styleOf(el);
    return (
      parseFloat(s.fontSize) <= 13 &&
      (MONO.test(firstFamily(s)) || firstFamily(s) === 'monospace')
    );
  });
  if (monoLabels.length >= 3) {
    tell(
      `${monoLabels.length} small labels in a monospace face, e.g. ${list(
        monoLabels.map((el) => `"${ownText(el).slice(0, 30)}"`),
        2,
      )}.`,
    );
  }
  const gradientText = all.filter(
    (el) =>
      shown(el) &&
      (styleOf(el).webkitBackgroundClip === 'text' ||
        styleOf(el).backgroundClip === 'text'),
  );
  if (gradientText.length)
    tell(`Gradient-filled text (${gradientText.length}).`);
  const blobs = all.filter((el) => {
    const s = styleOf(el);
    const blur = /blur\((\d+)/.exec(s.filter);
    return shown(el) && blur && Number(blur[1]) >= 40;
  });
  if (blobs.length)
    tell(
      `${blobs.length} heavily blurred shapes (glow blobs) used as decoration.`,
    );

  // Identical cards: a container whose children share one look and size.
  const cardGrids = [];
  for (const el of all) {
    const kids = [...el.children].filter(shown);
    if (kids.length < 3 || kids.length > 12) continue;
    const looks = kids.map((k) => {
      const s = styleOf(k);
      const framed =
        parseFloat(s.borderRadius) >= 6 &&
        (s.boxShadow !== 'none' ||
          parseFloat(s.borderTopWidth) > 0 ||
          rgba(s.backgroundColor).a > 0.05);
      const r = k.getBoundingClientRect();
      return framed
        ? `${s.borderRadius}|${s.boxShadow}|${s.backgroundColor}|${Math.round(r.width / 8)}`
        : null;
    });
    if (looks[0] && looks.every((l) => l === looks[0])) cardGrids.push(el);
  }
  const outerGrids = cardGrids.filter(
    (el) => !cardGrids.some((o) => o !== el && o.contains(el)),
  );
  if (outerGrids.length >= 2) {
    tell(
      `${outerGrids.length} groups of identical cards. Give each section the form its content needs (list, table, split, single feature) instead of cards everywhere.`,
    );
  }
  const shadows = new Map();
  for (const el of all) {
    const s = styleOf(el);
    if (s.boxShadow !== 'none' && shown(el))
      shadows.set(s.boxShadow, (shadows.get(s.boxShadow) ?? 0) + 1);
  }
  const topShadow = [...shadows.entries()].sort((a, b) => b[1] - a[1])[0];
  if (topShadow && topShadow[1] >= 8) {
    tell(
      `The same shadow on ${topShadow[1]} elements; let shadow follow hierarchy.`,
    );
  }

  // Reveal-on-scroll: text that was invisible until the page was scrolled.
  const revealed = (window.__hiddenBeforeScroll ?? []).filter(
    (el) => opacityOf(el) > 0.5,
  );
  const stillHidden = (window.__hiddenBeforeScroll ?? []).filter(
    (el) =>
      el.isConnected &&
      opacityOf(el) < 0.1 &&
      el.getBoundingClientRect().height > 0,
  );
  if (revealed.length >= 6) {
    tell(
      `${revealed.length} text blocks fade in on scroll. Keep at most one orchestrated moment; let the rest of the page simply be there.`,
    );
  }
  if (stillHidden.length) {
    problems.push(
      `Text still invisible after scrolling the whole page (a reveal animation never fired): ${list(stillHidden.map((el) => `"${textOf(el).slice(0, 40)}"`))}.`,
    );
  }

  // --- phone tap targets ----------------------------------------------------
  if (phone) {
    // Buttons and fields should be thumb-sized. A text link may be as small as
    // its text (WCAG 2.2 allows that when it has room around it); only flag
    // tiny icon-like links.
    const smallControls = [
      ...document.querySelectorAll(
        'button, [role="button"], input:not([type="hidden"]), select, textarea',
      ),
    ].filter((el) => {
      if (!shown(el)) return false;
      const r = el.getBoundingClientRect();
      return r.height < 40 || r.width < 40;
    });
    if (smallControls.length) {
      problems.push(
        `${smallControls.length} buttons or form fields smaller than 40px on a phone (aim for 44px), e.g. ${list(
          smallControls.map((el) => label(el, 25)),
          4,
        )}.`,
      );
    }
    const tinyLinks = [...document.querySelectorAll('a')].filter((el) => {
      if (!shown(el) || el.closest('p, li')) return false;
      const r = el.getBoundingClientRect();
      return r.height < 24 && r.width < 44;
    });
    if (tinyLinks.length) {
      problems.push(
        `${tinyLinks.length} tiny links (under 24px) on a phone, e.g. ${list(
          tinyLinks.map((el) => label(el, 25)),
          4,
        )}.`,
      );
    }
  }

  info.viewport = `${W}x${H}`;
  return { problems, tells, info };
}

/* ------------------------------------------------------------------------ */

fs.mkdirSync(outDir, { recursive: true });
const browser = await playwright.chromium.launch();
const report = [];
const slugOf = (p) =>
  p
    .replace(/^\/+|\/+$/g, '')
    .replace(/[^a-z0-9]+/gi, '-')
    .toLowerCase() || 'home';

for (const pagePath of pages) {
  for (const width of widths) {
    const phone = width < 768;
    const context = await browser.newContext({
      viewport: { width, height: phone ? 844 : 900 },
      deviceScaleFactor: 1,
      isMobile: phone,
      hasTouch: phone,
    });
    const page = await context.newPage();
    const consoleErrors = [];
    const failedRequests = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text().slice(0, 200));
    });
    page.on('pageerror', (err) =>
      consoleErrors.push(String(err.message ?? err).slice(0, 200)),
    );
    page.on('requestfailed', (req) => {
      const why = req.failure()?.errorText ?? 'failed';
      if (!/ERR_ABORTED/.test(why)) failedRequests.push(`${why} ${req.url()}`);
    });
    page.on('response', (res) => {
      if (res.status() >= 400)
        failedRequests.push(`${res.status()} ${res.url()}`);
    });

    const url = new URL(pagePath, base).toString();
    const entry = { page: pagePath, width, url };
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45_000 });
    } catch (err) {
      if (!/Timeout/i.test(String(err))) {
        entry.error = `Could not open ${url}: ${String(err.message ?? err).split('\n')[0]}`;
        report.push(entry);
        await context.close();
        continue;
      }
      // networkidle never came (polling, analytics): go on with what loaded
    }
    await page.evaluate(() => document.fonts?.ready).catch(() => {});
    if (wait > 0) await page.waitForTimeout(wait);
    const hiddenAtLoad = await page.evaluate(markHiddenAtLoad);
    await page.evaluate(scrollThrough);
    // Smooth-scroll libraries can still be easing back to the top.
    await page
      .waitForFunction(() => window.scrollY === 0, null, { timeout: 3000 })
      .catch(() => {});

    const slug = `${slugOf(pagePath)}-${width}`;
    entry.top = path.join(outDir, `${slug}-top.png`);
    entry.full = path.join(outDir, `${slug}-full.png`);
    await page.screenshot({ path: entry.top });
    const result = await page.evaluate(analyze, { phone });

    // In a whole-page capture, fixed and sticky elements (headers, chat
    // bubbles) get painted somewhere down the page, which looks like a bug
    // that isn't there. Pin them where they sit on the first screen.
    await page.evaluate(() => {
      for (const el of document.body.querySelectorAll('*')) {
        const { position } = getComputedStyle(el);
        if (position === 'fixed' || position === 'sticky') {
          el.setAttribute('data-check-site-pos', position);
        }
      }
      const style = document.createElement('style');
      style.textContent =
        '[data-check-site-pos="fixed"]{position:absolute!important}' +
        '[data-check-site-pos="sticky"]{position:relative!important;top:auto!important}';
      document.head.appendChild(style);
    });
    const height = await page.evaluate(
      () => document.documentElement.scrollHeight,
    );
    await page.screenshot({
      path: entry.full,
      fullPage: true,
      ...(height > 12_000
        ? { clip: { x: 0, y: 0, width, height: 12_000 } }
        : {}),
    });
    if (hiddenAtLoad.length) {
      result.problems.unshift(
        `Text in the first screen is invisible after load (entrance animation or opacity 0 until JavaScript runs; search engines and slow phones see nothing): ${hiddenAtLoad
          .slice(0, 4)
          .map((t) => `"${t}"`)
          .join('; ')}.`,
      );
    }
    if (consoleErrors.length) {
      result.problems.push(
        `Console errors: ${[...new Set(consoleErrors)].slice(0, 4).join(' | ')}`,
      );
    }
    if (failedRequests.length) {
      result.problems.push(
        `Failed requests: ${[...new Set(failedRequests)].slice(0, 5).join(' | ')}`,
      );
    }
    Object.assign(entry, result);
    report.push(entry);
    await context.close();
  }
}
await browser.close();

fs.writeFileSync(
  path.join(outDir, 'report.json'),
  JSON.stringify(report, null, 2),
);
// Tells, fonts and colors are the same at every width: print them once per
// page (at the widest width), and only problems for the narrower ones.
const lines = [];
const widest = Math.max(...widths);
for (const entry of report) {
  lines.push(`== ${entry.page} at ${entry.width}px ==`);
  if (entry.error) {
    lines.push(entry.error, '');
    continue;
  }
  lines.push(
    `Screens: ${entry.top} | ${entry.full} (page ${entry.info.pageHeight}px tall)`,
  );
  lines.push(entry.problems.length ? 'Problems:' : 'Problems: none found');
  for (const p of entry.problems) lines.push(`- ${p}`);
  if (entry.width === widest) {
    lines.push(
      entry.tells.length
        ? 'Tells (fix unless design.md says it is intended):'
        : 'Tells: none found',
    );
    for (const t of entry.tells) lines.push(`- ${t}`);
    lines.push(`Fonts: ${entry.info.fonts.join(', ')}`);
    lines.push(`Colors: ${entry.info.colors}`);
    if (entry.info.textOnImages) lines.push(entry.info.textOnImages);
    lines.push(`Outline: ${entry.info.headings.join(' | ')}`);
  }
  lines.push('');
}
lines.push(`Full data: ${path.join(outDir, 'report.json')}`);
console.log(lines.join('\n'));
