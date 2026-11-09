#!/usr/bin/env node
/**
 * Render a time-driven HTML animation to video, frame by frame.
 *
 *   node render_html_video.mjs scene.html out.mp4 [options]
 *
 * Options:
 *   --width 1920 --height 1080   frame size in CSS pixels (default 1920x1080)
 *   --fps 30                     frames per second (default 30)
 *   --duration 10                seconds to render (default: window.DURATION or 10)
 *   --audio music.mp3            mux this audio track (trimmed to the video)
 *   --stills 0.5,3,7.2           only write PNG stills at these times, for checking
 *   --alpha                      transparent background: writes ProRes 4444 (.mov)
 *                                or VP9 with alpha (.webm) depending on out's extension
 *
 * The page sets the picture for any time t. Use ONE of these:
 *   1. window.renderAt = (t) => { ... }   (t in seconds; may return a promise)
 *   2. CSS animations / element.animate() (the script pauses and seeks them)
 *   3. GSAP timelines                     (the script seeks gsap.globalTimeline)
 * Never use setTimeout, setInterval, requestAnimationFrame clocks or Date.now()
 * for motion: frames are captured as fast as they render, not in real time.
 *
 * Needs: ffmpeg on PATH and Playwright with Chromium. Sandboxes made from the
 * current template have both (Playwright installed globally). Otherwise install
 * them in the working folder, where the script looks first:
 *   npm init -y >/dev/null; npm i playwright; npx playwright install --with-deps chromium
 */
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const args = process.argv.slice(2);
if (args.length < 2 || args.includes('--help')) {
  console.log(
    'usage: node render_html_video.mjs scene.html out.mp4 [--width W] [--height H] [--fps N] [--duration S] [--audio file] [--stills t1,t2] [--alpha]',
  );
  process.exit(args.includes('--help') ? 0 : 1);
}
const [htmlArg, outArg] = args;
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] !== undefined ? args[i + 1] : fallback;
};
const width = Number(opt('width', 1920));
const height = Number(opt('height', 1080));
const fps = Number(opt('fps', 30));
const audio = opt('audio', null);
const stills = opt('stills', null);
const alpha = args.includes('--alpha');

const htmlPath = path.resolve(htmlArg);
const outPath = path.resolve(outArg);
if (!fs.existsSync(htmlPath)) {
  console.error(`No such file: ${htmlPath}`);
  process.exit(1);
}

// The working folder first (a project's own install), then the global one.
function playwrightSearchDirs() {
  const dirs = [process.cwd()];
  try {
    dirs.push(
      path.dirname(execSync('npm root -g', { encoding: 'utf8' }).trim()),
    );
  } catch {
    // npm missing: fall back to the usual global prefixes
  }
  dirs.push('/usr/lib', '/usr/local/lib');
  return [...new Set(dirs)];
}

function loadPlaywright() {
  for (const dir of playwrightSearchDirs()) {
    const req = createRequire(path.join(dir, 'noop.js'));
    for (const name of ['playwright', 'playwright-core']) {
      try {
        return req(name);
      } catch {
        // try the next one
      }
    }
  }
  console.error(
    'Playwright is not installed. Run in this folder:\n  npm init -y >/dev/null; npm i playwright; npx playwright install --with-deps chromium',
  );
  process.exit(1);
}

async function seek(page, t) {
  await page.evaluate(async (time) => {
    if (typeof window.renderAt === 'function') {
      await window.renderAt(time);
    } else {
      for (const animation of document.getAnimations()) {
        animation.pause();
        animation.currentTime = time * 1000;
      }
      if (window.gsap?.globalTimeline) {
        window.gsap.globalTimeline.pause();
        window.gsap.globalTimeline.seek(time, false);
      }
    }
    // Let layout and styles settle for this frame.
    await new Promise((resolve) =>
      requestAnimationFrame(() => requestAnimationFrame(resolve)),
    );
  }, t);
}

const { chromium } = loadPlaywright();
const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width, height },
  deviceScaleFactor: 1,
});
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts?.ready);

const pageDuration = await page.evaluate(() => window.DURATION);
const duration = Number(opt('duration', pageDuration || 10));

if (stills) {
  const base = outPath.replace(/\.[^.]+$/, '');
  for (const value of stills.split(',')) {
    const t = Number(value);
    await seek(page, t);
    const file = `${base}_t${String(t).replace('.', '_')}.png`;
    await page.screenshot({ path: file, omitBackground: alpha });
    console.log(file);
  }
  await browser.close();
  process.exit(0);
}

const totalFrames = Math.round(duration * fps);
const isWebm = outPath.endsWith('.webm');
const encode = alpha
  ? isWebm
    ? ['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '4M']
    : ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le']
  : [
      '-c:v',
      'libx264',
      '-crf',
      '18',
      '-preset',
      'medium',
      '-pix_fmt',
      'yuv420p',
    ];
const ffmpegArgs = [
  '-y',
  '-loglevel',
  'error',
  '-f',
  'image2pipe',
  '-framerate',
  String(fps),
  '-i',
  '-',
  ...(audio ? ['-i', path.resolve(audio)] : []),
  ...encode,
  ...(audio ? ['-c:a', 'aac', '-b:a', '192k', '-shortest'] : []),
  ...(!alpha && !isWebm ? ['-movflags', '+faststart'] : []),
  outPath,
];
const ffmpeg = spawn('ffmpeg', ffmpegArgs, {
  stdio: ['pipe', 'inherit', 'inherit'],
});
const ffmpegDone = new Promise((resolve, reject) => {
  ffmpeg.on('error', reject);
  ffmpeg.on('close', (code) =>
    code === 0 ? resolve() : reject(new Error(`ffmpeg exited with ${code}`)),
  );
});

const started = Date.now();
for (let frame = 0; frame < totalFrames; frame += 1) {
  await seek(page, frame / fps);
  const image = await page.screenshot(
    alpha
      ? { type: 'png', omitBackground: true }
      : { type: 'jpeg', quality: 95 },
  );
  if (!ffmpeg.stdin.write(image)) {
    await new Promise((resolve) => ffmpeg.stdin.once('drain', resolve));
  }
  if (frame % fps === 0) {
    process.stdout.write(`frame ${frame}/${totalFrames}\r`);
  }
}
ffmpeg.stdin.end();
await ffmpegDone;
await browser.close();
console.log(
  `\nWrote ${outPath}: ${totalFrames} frames at ${fps} fps (${duration}s) in ${Math.round(
    (Date.now() - started) / 1000,
  )}s`,
);
