---
name: image-generation
description: 'Make and edit images: posters, social graphics, thumbnails, product shots, logos, icons, illustrations, characters, UI mockups, infographics, photo edits and restyles. Also decides between an AI image, a chart, a diagram and a rendered layout.'
---

# Image generation

A good image does its job: it sells, explains, identifies or decorates in the place it will be used. Decide the job and the route before writing a prompt.

## Pick the route

| The image must...                                                                                                                                                   | Route                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Plot data with real axes, scales or numbers                                                                                                                         | Python chart (see the `data-analysis` skill). Never an AI image                                              |
| Show exact facts: times, prices, schedules, itineraries, timetables, comparison or spec tables, checklists                                                          | HTML layout rendered to PNG: `references/static-layouts.md`                                                  |
| Show a structure: flowchart, sequence, org chart, architecture, mind map                                                                                            | Mermaid rendered to PNG: `references/static-layouts.md`. Make a polished AI version afterwards only if asked |
| Be a visual asset: poster, ad, social post, thumbnail, illustration, product shot, character, logo concept, icon, UI mockup image, infographic with a few key facts | AI image: `media_generate_image`                                                                             |
| Change an existing image: edit, restyle, swap the background, add or remove objects, translate its text, combine people or products, upscale or restore             | AI edit: `media_generate_from_images`                                                                        |
| Resize, crop, convert, compress or stitch with no new content                                                                                                       | Pillow or ffmpeg in the sandbox                                                                              |
| Be a working web page, app or prototype                                                                                                                             | Build the software. An image is the wrong deliverable                                                        |

For real people, places, products or events the user wants to see as they are, find real photos with the `search` tool (type `image`). Do not generate them.

## Tools

- **`media_generate_image(prompt, orientation)`** generates with the image model the user selected (GPT Image by default, which renders text well). `orientation` is `square`, `landscape` or `portrait`.
- **`media_generate_from_images(prompt, image_urls, orientation)`** edits or combines images. `image_urls` takes URLs or sandbox paths such as `/home/user/uploads/photo.jpg`. Pass several images to combine them ("put the person from the first image into the scene of the second").
- Reading this skill unlocks the media tools. If they are still missing, call `media_generate` with a one-line brief.
- Each image uses the user's image credits. When the plan limit is reached, say so and suggest upgrading. Never fall back to drawing the image with Python.

## Brief, then prompt

Settle these before prompting. Ask only for what you cannot sensibly assume (usually exact text, brand colours or reference photos):

- **Purpose:** what the image must achieve, and where it goes (feed post, website hero, print, slide, app store).
- **Format:** orientation and safe areas (text away from edges, room for a headline).
- **Subject:** the specific person, product, scene or concept.
- **Style:** photographic, illustration, 3D, flat vector, brand style, or matching a reference.
- **Text:** the exact words, organised as headline, subhead, labels and call to action, or "no text".
- **Must keep:** identity, product shape, logo, colours, everything outside the edit.

Prompt patterns for new images, edits and each scenario are in `references/prompt-recipes.md`. Read it for anything beyond a simple single image.

## Rules

- **Text in images.** Put the exact words in quotes inside the prompt and let the model render them. Keep it to a headline and a few short lines. Never generate a blank background and then type text over it with Python. For dense exact information, use the HTML layout route instead.
- **Consistency.** For a recurring character or product, make one master image, then derive other poses and scenes from it with `media_generate_from_images`.
- **Sets.** For icon packs, card decks, product variants and poster series, make one image per item with the same style sentence. Do not combine them into one sheet unless asked.
- **Edits keep everything else.** Say exactly what changes and what must stay the same (face, pose, product, background, lighting, colours).
- **Transparent assets.** The tools return opaque images. Generate on a plain solid background that does not appear in the subject, then remove it: a colour key with Pillow for flat graphics, or `pip install rembg` and `rembg i in.png out.png` for photos. Check the edges.
- **Check once, lightly.** Look at the result (`file_view` with the image URL works). Confirm the request is met and the required text, names and numbers are right.
- **Never generate an image again on your own.** Every image costs credits. If a result has a real mistake (a misspelled word, a wrong number, a missing element), show it, say in one sentence what is wrong, and ask whether to make a corrected version. Generate again without asking only when the user told you to keep fixing it until it is right. HTML layout renders cost nothing: fix those yourself.

## Deliver

Show generated images in the reply as markdown, `![Short title](url)`. Sandbox files (renders, processed images) can also be embedded by path, `![Chart](/home/user/out/chart.png)`. Deliver final files the user should keep with `send_attachment`. After delivering, stop. Offer one useful next step instead of making extra variants nobody asked for.
