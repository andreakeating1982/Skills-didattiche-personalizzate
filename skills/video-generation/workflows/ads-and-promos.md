# Ads, promos and social clips

For product ads, launch teasers, app promos, UGC-style recommendations, service promos and short social hooks.

## Brief

Fill these in from the request and the user's assets. Ask only for what blocks a good result (usually the product images or the offer).

- **Product or offer:** what it is, the one benefit that matters most, the proof (number, demo, testimonial).
- **Audience and platform:** sets the aspect ratio, the length and the pace. Reels, TikTok and Shorts mean 9:16 and 6-30 s. YouTube pre-roll means 16:9 and 15-30 s. A website hero means 16:9 and a silent-friendly loop.
- **Assets:** product photos, logo, app screenshots, brand colours, an existing voice or spokesperson.
- **Call to action:** the exact words and where they appear (an end card, rendered in code).

## Structure

A reliable shape for 15-30 seconds:

1. **Hook (0-2 s).** The most striking result, contrast or question, already moving and with sound from the first frame. No slow establishing shots and no logos first.
2. **Problem or desire (2-6 s).** Shown, not told: a person or situation the viewer recognises.
3. **Product in action (6-20 s).** The benefit happening on screen, with 2-3 quick shots of the product, hands and results.
4. **Proof (optional).** A stat, a review or a before/after.
5. **End card (last 2-3 s).** Logo, offer and call to action as exact text in code, held long enough to read.

Cut every 1.5-3 seconds for social feeds, and give shots longer when they demonstrate something.

## Production

1. **Product consistency first.**
   - Use the user's product photos as `references` (cite "the bottle from Image 1") or as `keyframes.first`.
   - With no photos, generate one clean product reference with `media_generate_image` and confirm it with the user before building the ad around it.
   - Never let the video model invent the product's label or logo. Keep packaging text simple or cover it with an overlay.
2. **People.**
   - For a recurring presenter or UGC creator, generate one character reference image (face, hair, outfit) and reuse it in every clip.
   - Spoken lines go in the prompt in quotes, with "lip-synced dialogue" or "speaks directly to camera".
3. **Clips.**
   - One H3 Max clip can hold 2-4 short shots (up to 15 s). Seedance 2.5 holds several shots in up to 30 s with the most realistic people and motion, at a higher price.
   - Use WAN 3.0 for a single flowing 20-30 s take.
   - For 30-60 s, plan 3-5 clips that share the same references, style sentence and lighting so they cut together.
4. **Sound.**
   - Keep each clip's generated sound (dialogue, ambience, action effects).
   - Add music under it with ffmpeg at a lower level. A music bed never replaces action sounds.
   - When the clips carry no dialogue, generate one continuous music track for the whole ad so it does not restart at every cut.
5. **Assemble.** Join, add the end card and captions, normalise loudness. See `../references/ffmpeg.md`.

## Variants

When the user wants several versions (A/B hooks, platforms), keep the core clips and change only the hook, the end card or the crop. Reformat 16:9 to 9:16 with a crop or a blurred-background pad rather than regenerating.

## Check

- The product looks like the product in every shot.
- The hook moves in the first second.
- Every word on screen is correct.
- The call to action is readable.
- The music does not bury dialogue.
- The length fits the platform.
