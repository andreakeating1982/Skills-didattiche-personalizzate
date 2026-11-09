---
name: web-design
description: 'How websites, landing pages and web app screens should look: a direction drawn from the subject, palette and type tokens, layout, images, copy, and a screenshot check at desktop and phone widths before delivery. Read before designing, building or restyling any page.'
---

# Web design

Work like the design lead of a studio known for giving every client an identity nobody would mistake for anyone else's. This client has already turned down proposals that looked templated. They are paying for a point of view: palette, type and layout chosen for this subject, with one deliberate risk.

## Workflow

1. **Know the subject.** What it is, who it is for, and the one thing a visitor should do (buy, book, call, sign up, read). Collect the real content the brief gives: names, products, prices, places, hours. Fill gaps with specific, plausible content (real-sounding product names, actual prices, local details), never generic filler, and list what you invented in your final message. If the brief doesn't say what the site is for, ask with `message_ask_user` before designing; otherwise decide and say what you decided.
2. **Write the design plan** to `design.md` in the project root, before any page code (template below). Unless the user or their existing site already set the style, start with three distinct directions, one line each, with your estimate of how often a designer given this brief would land there. Choose one that is unlikely (under 10%) yet right for the subject and the visitor, not the most likely one, and expand only that.
3. **Check the plan against "Defaults to avoid".** For each part ask: would I have picked this for any similar site? If yes, change it and note the change under "Changed after review".
4. **Tell the user the direction** in two or three sentences (the idea, palette, type) and keep working. Don't wait for approval.
5. **Make the images** (see Images), all at once at the start.
6. **Build**: tokens first (colors in the stylesheet, fonts in the page head; see "Where things go"), then the header, footer and shared pieces, then each page section by section.
7. **Check it and fix it** (see "Check before delivering"). Required after the first build and after any change to layout or styling.
8. **Deliver**: `send_attachment` with `website_url`. In the message, name the direction in one line and list placeholders and invented content.

**Where things go** (web-static and web-db-user | web-app):

- Color and type tokens: `client/src/index.css` | `src/styles.css`.
- The Google Fonts link: `client/index.html` | the `links` of `head()` in `src/routes/__root.tsx`.
- Images: `client/public/images/` | `public/images/`.
- Each page's title and description: as the README shows | `head()` in each route file.

### design.md

```markdown
# <Site> design

Directions considered: <three one-liners with likelihood, and which one you chose>
Idea: <2-3 sentences: the concept, and the ONE element people will remember>
Visitor and main action: <who, and what they should do>
Voice: <two example lines: a headline and a button label>
Wordmark: <how the name is drawn: face, weight, spacing, a mark; not just the name in the body font>

## Palette (4-6 colors)

- <name> #RRGGBB: <role, e.g. page background>
- <name> #RRGGBB: <text>
- <name> #RRGGBB: <muted text, borders>
- <name> #RRGGBB: <the signature color this brand owns: main buttons and one highlight>

## Type

- <Family, weights>: <role>
- <Family, weights>: <role>
- Scale: display / h1 / h2 / h3 / body / small with size, line height, letter spacing

## Layout

- Grid, max width, alignment (left or centered), section spacing
- Hero in one sentence, plus an ASCII wireframe
- Every other section in one line (what it holds and its form: list, table, split, gallery...)

## Images

- Style sentence shared by every image: <light, palette, lens, texture, mood>
- <slot>: <subject>, <landscape | portrait | square>

## Motion

- <the one moment, or none>

## Changed after review

- <what changed and why>
```

## Defaults to avoid

Generated sites cluster around a few looks. Each suits some brief, but they appear whatever the subject, so visitors read them as "made by AI". When the brief asks for one of these, follow the brief. When the brief leaves that choice open, choose something else:

- **Palettes:** warm cream background (around #F4F1EA) with a high-contrast serif headline and a terracotta, clay, copper or ember accent (around #D97757); near-black (#0B0B0B, #111, dark brown-black) with one acid-green, vermilion, orange or electric-blue accent; purple-to-blue gradients on white; glow blobs, mesh gradients and grain as decoration.
- **Type:** Inter, Roboto, Arial or the system font as the brand's face; the fashionable defaults (Fraunces, Instrument Serif, Playfair Display, DM Serif, Newsreader as a display face, Space Grotesk, Instrument Sans, DM Sans); a monospace face for small labels, prices and data.
- **Template chrome:** a small tracked-out ALL-CAPS label (an eyebrow) above every heading; one word or phrase of a headline in italic, bold or another color; meta lines joined with middle dots ("Roasted · Lisbon · Est. 2019"); "Label — fragment" with a spaced em dash; "→" after link and button text; numbered markers (01 / 02 / 03) on content that isn't a sequence; uppercase buttons and nav; map coordinates, local times or "Est. 2019" as decoration; emoji as icons.
- **Layout kit:** every section a centered heading over three identical rounded cards; one border radius and the same soft grey shadow on everything; a hero built from a big number, a small label and a row of stats; a scrolling marquee strip of keywords; a strip of invented client logos; broadsheet layouts with hairline rules, zero radius and dense columns.
- **Motion:** fade-and-slide-up on every section; lift and shadow on every card hover; parallax for its own sake.
- **Copy:** "Elevate", "Unlock", "Seamless", "Crafted with care", "Experience the difference", "Where X meets Y", "More than just X"; questions as headlines; exclamation marks; invented testimonials, star ratings, customer counts, awards and press quotes.

## Design rules

**Hero.** Open with the most characteristic thing in the subject's world, in the form that suits it: a photograph, the product, a headline set as large type, a live demo, a map, a menu. On the first screen, on desktop and on a phone, a visitor understands what this is and sees the main action.

**Typography.** Type carries the personality.

- One family or two. With two, make them clearly different; never two similar sans-serifs.
- Choose for this subject, not the families you would use anywhere. `references/typography.md` lists Google Fonts by voice and shows how to load them.
- Set a type scale with intentional weights and spacing: large headlines with tight line height (1.0-1.1) and slightly negative letter spacing; body 16-18px with line height 1.5-1.7 (a serif body a little more).
- Lines under 80 characters (`max-w-[65ch]` on running text). `text-wrap: balance` on headings.
- When type is the visual, design with it (size, weight, width, line breaks, placement) rather than centering a sentence.
- Sentence case for headings, buttons, navigation and labels.

**Color.**

- The palette from design.md goes into the scaffold tokens in the stylesheet (see "Where things go"; `--background`, `--foreground`, `--primary`, `--secondary`, `--muted`, `--accent`, `--border`, `--ring`, and the card and popover pairs). Components use the tokens (`bg-primary`, `text-muted-foreground`), never hex values.
- One color sets the mood; the accent is rare (the main action, one highlight). Text contrast at least 4.5:1, large text 3:1.
- Choose light or dark for the subject; ThemeProvider's `defaultTheme` must match the variables you set. web-app has no ThemeProvider: put the palette straight into `:root`.

**Layout.**

- A grid with consistent gutters and a max width. Left-align most text; center only short statements.
- Give each section the form of its content: a menu or price list is a list, a schedule is a table, a story is text beside a picture, a product is a big image and specifics. Cards only for things that really are separate, comparable items.
- Structure is information: borders, numbers, dividers and labels only where they tell the visitor something. Number only real sequences (steps, a timeline).
- Radius and shadow follow hierarchy; use a small, deliberate set.
- One spacing scale for the vertical rhythm (for example `py-24` between sections on desktop, `py-16` on phones).
- Spend boldness in one place: one memorable element, everything around it quiet. Before delivering, remove the decoration that adds least.
- Write Tailwind classes on the element they style. Custom CSS classes for sections easily cancel each other's padding and margins.

**Images.**

- For real places, people and products the user names, use photos the user uploaded or find real ones with the `search` tool (type image). Don't generate a fake version of a real thing.
- Otherwise generate with `media_generate_image`. Put the same style sentence from design.md in every prompt so the set looks like one shoot. Plan the slots first: one hero in landscape, then 2-5 supporting images in the orientation each slot needs. No overlaid text in photos (packaging and signs are the exception below). Start them all in parallel at the beginning. Never use one image twice on a page.
- Products must look like this brand's products. For packaging, labels or signs, put the brand name and the product's own colors and words in quotes in the prompt (the image model renders text). A blank white label on a mockup bag reads as unfinished.
- Generated images are often only 1024-1536px wide. Ask for the orientation each slot needs, and don't stretch an image much wider than its file: a square image across a full-width hero looks soft on a wide screen. Frame it in a column or a max-width box instead.
- Download them into the images folder (see "Where things go") with descriptive names and a short content hash (`hero-3f9a2c.webp`): published files are cached for a long time, so a changed image needs a new name. Save them at a sensible size (WebP, about 2400px wide for a full-width hero, 1600px for others). Give every `<img>` width and height or an aspect ratio with `object-cover`, `loading="lazy"` below the first screen, and real alt text.
- Generate only images with a planned place. Internal tools and dashboards need no decorative images.
- No stock clichés unless the subject calls for them: handshakes, laptops on desks, people pointing at screens, abstract 3D shapes.
- Icons from lucide-react, one size and stroke throughout. No emoji.

**Motion.** Use motion nobody triggered sparingly, only to draw attention: at most one orchestrated moment (a page-load sequence or one reveal). Motion that answers an action (open, expand, add to cart, confirm) is welcome when it shows what changed. Respect `prefers-reduced-motion`. Never leave content at opacity 0 waiting for scroll or JavaScript (the README's prerendering rules).

**Words.** Words are there to make the site easier to understand and use.

- Write from the visitor's side, in plain words. Name things the way they would.
- Say what something is or does instead of selling it. Specific beats clever.
- Active voice. A button says exactly what happens ("Book a cupping", "Add to bag", not "Submit" or "Learn more"), and an action keeps its name through the flow: "Subscribe" leads to "Subscribed".
- Errors say what went wrong and how to fix it, without apologizing. An empty state invites the next action.
- Sentence case, plain verbs, no filler. Each piece of text does one job.

**Quality floor** (always; don't announce it):

- Works from 360px wide up with no sideways scrolling; the navigation becomes a menu on phones.
- Visible keyboard focus, real buttons and links, labels on form fields, alt text, tap targets of about 44px.
- Every button and link works or shows plainly what happens (placeholders show a toast and are listed in your final message).
- A form that collects something (sign-ups, a waitlist, bookings, orders, contact messages) really stores it. That needs a scaffold with a database (web-app or web-db-user); upgrade a web-static project with `webdev_add_feature` first. Never show "You're on the list" for a submission that went nowhere.
- Test such a form once in the preview: `browser_navigate` to it, fill it in with a test address, submit, and see the success state; then delete that one test row. Don't hand-write curl requests to `/api/trpc` (web-db-user) or to server functions (web-app): the page sends its own encoding, so a hand-made body fails in ways real visitors never hit.
- The wordmark from design.md is built (an inline SVG, or type with its own weight and spacing), and the favicon is made from it.
- Each page has its own title and description.

## Check before delivering

Run the check script against the dev server (it runs inside the sandbox; nothing leaves it). List the main pages:

```bash
node /home/user/skills/web-design/scripts/check_site.mjs http://localhost:3000 /home/user/site-check --pages / /shop /visit
```

It saves screenshots at 1440px and 390px (`<page>-<width>-top.png` is the first screen, `<page>-<width>-full.png` the whole page) and prints Problems (sideways scrolling, broken, stretched or blurry images, text cut off, low contrast, fonts that didn't load, console errors, hidden content) and Tells (the defaults above, found on the page). Then:

1. Look at the home page's `-top.png` and `-full.png` at both widths with `file_view`, in one step. Ask it what is broken or hard to read (overlaps, bad crops, misalignment, illegible text, crowded or empty areas), not whether the design looks premium: a second opinion on taste pulls the design back toward the defaults (in testing it advised swapping a deliberate accent for terracotta). design.md decides the look.
2. Judge them against design.md: Is the subject clear on the first screen? Is the memorable element there? Do sections differ in form? Is spacing even and are edges aligned? Any cramped or empty areas, bad crops, text over busy images, one word alone on a heading's last line?
3. Fix every Problem, every Tell you didn't choose on purpose, and what you saw. Run the script again. Two rounds are usually enough. Give one finding at most two attempts: if it is still there, list it in your final message and move on rather than spending the run debugging it.

If the script itself fails (an error instead of a report), open the preview with `browser_navigate` and look at it there instead, and say in your final message that the automated check didn't run.
