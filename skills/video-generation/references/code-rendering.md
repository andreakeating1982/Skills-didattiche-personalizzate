# Rendering motion graphics in code

Use code when the picture must be exact: words, logos, numbers, charts, UI, captions and transparent overlays. The animation is a function of time, so every frame is reproducible and the user can edit it later.

## Contents

- Pick an engine
- HTML route (recommended)
- Python route
- Overlays with transparency
- Fonts and assets
- Checking and encoding

## Pick an engine

| Engine                                        | Best for                                                                                                            | Setup                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| HTML/CSS/JS + `scripts/render_html_video.mjs` | Typography, layouts, UI mockups, brand pieces, SVG logo animation, anything a designer would build in After Effects | Playwright + Chromium (installed) |
| Python + Pillow/NumPy                         | Simple shapes, particles, generative patterns, data-driven frames                                                   | Nothing beyond ffmpeg             |
| matplotlib `FuncAnimation`                    | Animated charts that must stay numerically exact                                                                    | Nothing beyond ffmpeg             |

ffmpeg, Playwright, Chromium and Noto fonts for every script are installed in the sandbox. An older sandbox may lack them: install ffmpeg with `which ffmpeg || (sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg)`, and Playwright as shown in step 1.

## HTML route (recommended)

1. **Make a project folder:** `mkdir -p /home/user/mg && cd /home/user/mg`. The render script finds the installed Playwright. Only if it reports that Playwright is not installed (an older sandbox), install it in this folder once, which takes 1-2 minutes:
   ```bash
   npm init -y >/dev/null && npm i playwright && npx playwright install --with-deps chromium
   ```
2. **Write `scene.html`** at the exact output size, for example `1920x1080` or `1080x1920`. Set `html, body { margin: 0; width: 1920px; height: 1080px; overflow: hidden; }`. Drive every movement from time with one of:

   - **CSS animations** with explicit `animation-delay`s. This is simplest for sequenced reveals. The script pauses them and seeks each frame.
   - **`window.renderAt = (t) => { ... }`**, which sets the whole picture for time `t` in seconds. Use it for canvas, SVG path drawing, counters and anything computed.
   - **GSAP timelines.** The script seeks `gsap.globalTimeline`. Load GSAP from a local file or a CDN.

   Set `window.DURATION = 15;` so the script knows the length. Never animate with `setTimeout`, `setInterval`, a free-running `requestAnimationFrame` loop or `Date.now()`: frames are captured as fast as they render, not in real time.

3. **Check stills at the key moments** before the full render:
   ```bash
   cd /home/user/mg && node /home/user/skills/video-generation/scripts/render_html_video.mjs scene.html check.png --stills 0.5,3,7.5,14.5
   ```
   Look at them with `file_view`. Fix the layout in HTML and check again.
4. **Render:**
   ```bash
   cd /home/user/mg && node /home/user/skills/video-generation/scripts/render_html_video.mjs scene.html out.mp4 --fps 30 --audio music.mp3
   ```
   A 15-second 1080p piece at 30 fps renders in roughly 1-3 minutes. Use `shell` with `background: true, notify: true` for long ones.

A useful timing helper in the page:

```js
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const easeInOut = (t) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
// progress of a segment that runs from start to end seconds
const seg = (t, start, end) => clamp((t - start) / (end - start));
window.renderAt = (t) => {
  const p = easeOut(seg(t, 0.4, 1.2));
  title.style.opacity = p;
  title.style.transform = `translateY(${(1 - p) * 40}px)`;
  counter.textContent = Math.round(
    easeInOut(seg(t, 1.5, 3.5)) * 1250,
  ).toLocaleString();
};
```

## Python route

Draw each frame with Pillow at twice the size and downscale for smooth edges, then encode:

```python
from PIL import Image, ImageDraw, ImageFont
W, H, FPS, DUR, SS = 1920, 1080, 30, 6, 2
font = ImageFont.truetype("/home/user/fonts/Inter.ttf", 140 * SS)
ease = lambda t: 1 - (1 - min(max(t, 0), 1)) ** 3
for i in range(FPS * DUR):
    t = i / FPS
    img = Image.new("RGB", (W * SS, H * SS), "#0f1020")
    d = ImageDraw.Draw(img)
    r = int(60 * SS * ease(t / 0.8))
    d.ellipse([W * SS / 2 - r, H * SS / 2 - r, W * SS / 2 + r, H * SS / 2 + r], fill="#ff7a1a")
    img.resize((W, H), Image.LANCZOS).save(f"frames/{i:05d}.png")
```

```bash
mkdir -p frames && python3 frames.py && ffmpeg -y -framerate 30 -i frames/%05d.png -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart out.mp4
```

Pillow does not wrap text or lay it out. For text-heavy designs, use the HTML route.

## Overlays with transparency

For a lower third, title or logo sting that goes over other footage, render with a transparent background and `--alpha`:

```bash
node /home/user/skills/video-generation/scripts/render_html_video.mjs lower-third.html lower-third.mov --alpha    # ProRes 4444 with alpha
node /home/user/skills/video-generation/scripts/render_html_video.mjs lower-third.html lower-third.webm --alpha   # VP9 with alpha, small, plays on the web
```

Keep `background: transparent` on `html` and `body`. Composite it with ffmpeg's `overlay` filter (see `ffmpeg.md`), or deliver the .mov or .webm when the user will edit it themselves.

## Fonts and assets

- **Fonts:** download what you need into `/home/user/fonts` (see `ffmpeg.md`) and load it with `@font-face { src: url("file:///home/user/fonts/Inter.ttf"); }`. The script waits for `document.fonts.ready`. Inter and the Noto fonts (including Noto Sans CJK, Arabic, Devanagari, Thai and Noto Color Emoji) are installed, so `font-family: "Inter", "Noto Sans", "Noto Sans CJK SC", sans-serif` works without downloads.
- **Brand assets:** the logo as SVG or a transparent PNG from the user. Never redraw a logo by hand.
- **Generated stills:** illustrations, textures and backgrounds from `media_generate_image` can be placed in the HTML as images. Download them into the project folder first.

## Checking and encoding

- Contact sheet of the render (see `ffmpeg.md`) and a final `ffprobe`.
- Look for clipped or overlapping text, elements that never fully arrive, holds too short to read and frames where nothing moves for long.
- Social platforms: H.264, yuv420p, 30 fps, `-movflags +faststart`, loudness around -14 LUFS when there is sound.
