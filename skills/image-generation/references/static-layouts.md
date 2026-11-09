# Static layouts and diagrams rendered to PNG

Use this route when every fact in the image must be exact: schedules, itineraries, agendas, timetables, price lists, comparison or spec tables, checklists, summary cards and structured diagrams. The design is real HTML and CSS rendered by a browser, so text wraps, nothing is guessed, and fixing a mistake means editing one line.

## Setup

Playwright, Chromium, Inter and the Noto fonts (all scripts and emoji) are installed, and `scripts/html_to_png.mjs` finds them. Work in `mkdir -p /home/user/visuals && cd /home/user/visuals`. Only if the script reports that Playwright is not installed (an older sandbox), install it there once (1-2 minutes):

```bash
npm init -y >/dev/null && npm i playwright && npx playwright install --with-deps chromium
```

If the install is impossible, WeasyPrint is already installed and can render simpler layouts: `weasyprint page.html page.pdf && pdftoppm -png -r 192 -singlefile page.pdf page`. It supports flexbox and grid less fully, so keep those layouts simple.

## Build the page

- **Width.** Set it to the medium. About 540 CSS px for something read on a phone or in chat, 1080 for a square or portrait social graphic, 1200-1600 for slides and desktop. The height follows the content.
- **Layout.** Use normal flow, flexbox and grid. No fixed heights, no absolute positioning of text.
- **Hierarchy.** A clear title, sections, and one spacing scale (for example 8, 16, 24, 32 px). Use a readable type size at the final viewing size: body at least 16 px for a 540 px-wide phone graphic.
- **Colour.** A restrained palette. When colour encodes categories, keep it consistent and add a small legend.
- **Fonts.** Use a web font for polish (a Google Fonts `<link>`), or system-ui. For Chinese, Japanese, Korean, Arabic or Hindi, load a Noto font for that script.
- **Wrapper.** Wrap everything in `<main>` so it can be captured exactly.

## Render

```bash
cd /home/user/visuals
node /home/user/skills/image-generation/scripts/html_to_png.mjs schedule.html schedule.png --width 540 --selector main
```

`--scale 2` (the default) makes it sharp on phones. Look at the PNG once with `file_view`:

- Every time, date, price and name matches the source.
- No text is clipped or overlapping.
- No large empty areas.

Fix problems in the HTML and render again.

## Diagrams with Mermaid

Write the diagram in Mermaid, then render it with the same script:

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #fff;
      }
      main {
        display: inline-block;
        padding: 24px;
      }
    </style>
  </head>
  <body>
    <main>
      <pre class="mermaid">
flowchart LR
  A[Order placed] --> B{Paid?}
  B -- yes --> C[Ship]
  B -- no --> D[Send reminder]
</pre
      >
    </main>
    <script>
      mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
    </script>
  </body>
</html>
```

```bash
node /home/user/skills/image-generation/scripts/html_to_png.mjs diagram.html diagram.png --width 1200 --selector main --wait 800
```

When the user asked for the diagram code itself, give the Mermaid source as well as the PNG.

## Deliver

Embed the PNG in the reply (`![Schedule](/home/user/visuals/schedule.png)`) and send it with `send_attachment`. Add the HTML when the user wants to edit it later.
