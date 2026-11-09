# Typography

## Choosing a face

Start from the subject's voice, then find a typeface that has it.

- How does the subject speak: precise, warm, old, loud, quiet, technical, handmade, luxurious, civic, playful?
- Where does lettering appear in its world: shop signs, menus, labels, packaging, tickets, manuals, street signs? Its vernacular is a better source than any font list.
- One family with a wide range (weights, widths, optical sizes) often beats two.
- Two families need a clear difference in structure (a serif with a sans, a condensed display with a plain text face). Two similar sans-serifs look like a mistake.
- Keep it to two families and about four weights in total. Load only the weights and styles you use; never let the browser fake bold or italic.
- For languages beyond Latin (Cyrillic, Greek, Vietnamese, Arabic, CJK), check the family supports the script; the Noto families cover nearly everything.

## Google Fonts by voice

Starting points, not a menu: any Google Font that fits the subject is fine. The families in SKILL.md's "Defaults to avoid" are left out on purpose.

| Voice                               | Headlines                                                                             | Text and UI                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Precise, engineered, technical      | Schibsted Grotesk, Geologica, Red Hat Display, Archivo (condensed or expanded widths) | Hanken Grotesk, Public Sans, IBM Plex Sans, Onest |
| Neutral, calm, product              | Albert Sans, Plus Jakarta Sans, Manrope, Golos Text                                   | Albert Sans, Be Vietnam Pro, Inclusive Sans       |
| Warm, friendly, approachable        | Bricolage Grotesque, Gabarito, Fredoka                                                | Figtree, Nunito Sans, Karla, Mulish               |
| Loud, poster, sport                 | Anton, Archivo Black, Big Shoulders Display, Dela Gothic One, Unbounded               | Archivo, Work Sans                                |
| Editorial, literary                 | Gloock, Young Serif, Libre Caslon Display, Bodoni Moda, Spectral                      | Source Serif 4, Literata, Lora, Crimson Pro       |
| Classic, institutional, trustworthy | Libre Baskerville, EB Garamond, Gelasio, Brygada 1918                                 | Source Serif 4, Public Sans                       |
| Handmade, local, food and craft     | Caprasimo, Shrikhand, Bagel Fat One, Alegreya                                         | Alegreya Sans, Karla                              |
| Geometric, fashion, design          | Syne, Urbanist, Josefin Sans, Outfit                                                  | Urbanist, Albert Sans                             |
| Retro, vintage, signage             | Limelight, Righteous, Bungee, Rozha One, Abril Fatface                                | Josefin Sans, Work Sans                           |
| Code and real tabular data only     | JetBrains Mono, Martian Mono, Azeret Mono                                             | the same                                          |

## Loading the fonts (scaffold)

In web-static and web-db-user, replace the commented Google Fonts block in `client/index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Gloock&family=Hanken+Grotesk:wght@400;500;700&display=swap"
  rel="stylesheet"
/>
```

In web-app, put the same links first in the `links` array of `head()` in `src/routes/__root.tsx`, before the links already there:

```tsx
links: [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Gloock&family=Hanken+Grotesk:wght@400;500;700&display=swap",
  },
  { rel: "stylesheet", href: appCss },
  { rel: "icon", href: "/favicon.svg", type: "image/svg+xml" },
],
```

A malformed URL makes Google answer 400 and every font on the site silently falls back to Times or Arial. With several axes, each tuple needs a value for every axis, in the order listed, and tuples sorted: `Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400`, never `...;1,400`. If you don't need italics or optical sizes, ask only for weights (`Newsreader:wght@400;600`). Check the URL before using it:

```bash
curl -s -o /dev/null -w '%{http_code}\n' '<the fonts URL>'   # must print 200
```

In the stylesheet (`client/src/index.css`, or `src/styles.css` in web-app), add a `@theme` block. `--font-sans` becomes the body font; `--font-display` gives a `font-display` class for headlines; the `--text-*` entries give `text-display`, `text-h1`... classes that carry their own line height and letter spacing:

```css
@theme {
  --font-sans: 'Hanken Grotesk', ui-sans-serif, system-ui, sans-serif;
  --font-display: 'Gloock', ui-serif, Georgia, serif;

  --text-display: clamp(3rem, 5.5vw + 1rem, 6.5rem);
  --text-display--line-height: 1;
  --text-display--letter-spacing: -0.02em;
  --text-h1: clamp(2.5rem, 3.5vw + 1rem, 4.5rem);
  --text-h1--line-height: 1.05;
  --text-h1--letter-spacing: -0.015em;
  --text-h2: clamp(1.875rem, 2vw + 1rem, 3rem);
  --text-h2--line-height: 1.1;
  --text-h3: 1.5rem;
  --text-h3--line-height: 1.25;
  --text-body: 1.0625rem;
  --text-body--line-height: 1.6;
}
```

Adjust the sizes to the design: a quiet site needs a smaller display size than a poster-like one. Check the scale at 390px wide; the `clamp()` minimums are what phones get.

## Details that read as finished

- Headings: `text-wrap: balance` (Tailwind `text-balance`); running text: `text-pretty`, `max-w-[65ch]`.
- Prices, times and tables: tabular figures (`tabular-nums`) so columns line up.
- Real punctuation: ’ “ ” for quotes and apostrophes, an en dash for ranges (9:00–18:00, €12–18), × for dimensions, a non-breaking space between a number and its unit.
- Letter spacing: slightly negative on large headlines, normal on body text, slightly positive only on very short uppercase text (and then only where uppercase is right for the content).
- Weight does the hierarchy before color does: muted grey text below 4.5:1 contrast is a common, avoidable failure.
