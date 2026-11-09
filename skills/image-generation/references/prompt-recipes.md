# Image prompt recipes

## Contents

- New image pattern
- Edit pattern
- Recipes by scenario: poster or ad, social post, thumbnail, product shot, portrait or character, logo, icon set, UI mockup, infographic, illustration
- Edit recipes: background swap, remove or add objects, translate text, restyle, combine images, upscale or restore, extend to another aspect ratio
- Common failures

## New image pattern

```text
Create [kind of image] for [use and audience].
Subject: [specific subject: who/what, key details, action or pose].
Composition: [orientation, framing, focal point, camera angle, where the empty space is for text].
Style: [medium and finish: photo/illustration/3D/flat vector], lighting [direction, quality], palette [colours], mood [one or two words].
Text to render: "[HEADLINE]" as the headline; "[subhead]" smaller below; "[CTA]" on a button at the bottom. (Or: no text.)
Avoid: [failure modes for this scenario].
```

## Edit pattern

```text
Edit the provided image. Change only [the region, object or text].
Keep exactly: [identity and face, pose, product shape and label, background, lighting, perspective, colours, all other objects].
Result: [what the changed part should look like].
New text, if any: "[exact words]" at [location], matching the original typography.
Avoid: [unwanted changes, style drift, extra objects].
```

## Recipes by scenario

**Poster or ad.** Name the format ("event poster", "Instagram ad"). One focal visual, a clear hierarchy (headline, then details), the exact text in quotes, the brand colours, and generous margins. Put the date, time and venue as separate short lines, not a paragraph.

**Social post (square or portrait).** Make it readable at phone size: one idea, at most about 12 words of text, strong contrast. In portrait, leave the bottom fifth free of key content, where the platform puts its interface.

**YouTube thumbnail (landscape).** A face with a strong expression or a striking object, 2-4 huge words, high contrast, a simple background, and a clear subject at the left or right third. Check it would read at 320 px wide.

**Product shot.** Use the user's product photo through `media_generate_from_images` so the shape, label and colours stay true. Describe the surface, the props, the light direction and the background ("on wet black slate, rim light from behind, soft fill from the left"). For marketplace images: pure white background, the whole product visible, no props.

**Portrait or character sheet.** Fix the identity anchors: age, face shape, skin tone, hair, eyes, build, outfit and colour palette. For a reusable character, ask for "a character reference: full body front view, neutral pose, plain light-grey background". Derive other poses from this image later.

**Logo concept.** Ask for a simple, flat mark that is recognisable at 32 px, with 1-2 colours and a plain background. Treat generated wordmarks as concepts. For production use, recommend recreating the final logo as a vector.

**Icon set.** For each icon, write one shared style sentence ("flat duotone icon, 2 px rounded strokes, indigo and soft teal, centered on a white background, no text") plus the subject. Generate them one by one with that exact sentence.

**UI mockup image.** Name the screen type, the device frame or browser, light or dark mode, the navigation, the main components and realistic sample data and labels in quotes. Describe it as "a high-fidelity UI design mockup". When the user wants working software, build it instead.

**Infographic.** Organise the content first: a title, 3-6 sections each with a short label and one number or line, and a footer source. Keep the copy short. For many exact numbers, use a chart or an HTML layout instead.

**Illustration.** Name the medium (watercolour, gouache, flat vector, risograph, children's book, editorial line art), the palette, the composition and the mood. Reuse the same style sentence across a series.

## Edit recipes

| Edit                         | Prompt core                                                                                                                                                                              |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Background swap              | "Replace only the background with [new scene]. Keep the person/product, their edges, pose, lighting direction and colours exactly; match the new background's light to the subject."     |
| Remove an object             | "Remove the [object] and fill the area naturally with the surrounding [surface/texture]. Change nothing else."                                                                           |
| Add an object                | "Add a [object] on the [location], at a realistic scale and with shadows matching the scene's light. Keep everything else unchanged."                                                    |
| Translate text               | "Replace the English text '[old]' with the [language] text '[new]' in the same position, font style, size and colour. Keep the rest of the design identical."                            |
| Restyle                      | "Redraw this image as [style], keeping the composition, the subjects and their poses."                                                                                                   |
| Combine images               | "Place the [person/product] from image 1 into the [scene] from image 2. Match the lighting and perspective; keep the [person/product] identical to image 1."                             |
| Upscale or restore           | "Restore and upscale this image: sharper details, natural textures, no new objects, same composition, colours and identity."                                                             |
| Extend to a new aspect ratio | "Extend this image to a [landscape/portrait] format by continuing the scene naturally on the [sides/top and bottom]; keep the original content unchanged." Use the target `orientation`. |

## Common failures

| Failure                            | Fix                                                                                                       |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Misspelt or extra text             | Shorter text, every word in quotes, fewer text blocks. Ask once more. For dense text, use an HTML layout  |
| The product changed shape or label | Use the user's photo in `media_generate_from_images`. Never generate the product from a description alone |
| The face changed across images     | Derive every image from one master image. Name the features that must not change                          |
| Cluttered composition              | One focal point, name the empty area for text, fewer props                                                |
| Generic look                       | A specific medium, lighting, palette and reference era instead of "beautiful" or "professional"           |
