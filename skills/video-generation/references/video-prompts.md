# Writing video model prompts

How to write prompts for `media_generate_video`, whichever model it uses. The model sees only the prompt and the attached images. Everything that matters must be in them.

## Contents

- Principles
- Prompt template
- Camera language
- Sound
- Using references and keyframes
- Examples
- Before you submit

## Principles

- **Write what can be seen and heard.** Write "she drops the keys, they hit the tiled floor and she looks at the door", not "she feels anxious". Translate emotions, themes and intentions into faces, hands, objects, light and sound.
- **Be specific about the look.** Give the kind of image (a 35 mm film still, a glossy 3D product render, a 2D cel animation), the lens and depth of field, the colour temperature, the key light direction and the visible materials.
  - Never rely on "cinematic", "premium" or "beautiful". They carry no information.
  - Reuse the same style sentence in every clip of one video.
- **Give every shot motion.** Every shot needs subject action and a camera behaviour. A locked-off camera is a choice: say what it holds and why.
- **Order the events.** For a multi-shot clip (H3 Max or Seedance 2.5), write `Shot 1:`, `Shot 2:` in order and let the duration parameter set the total. For WAN 3.0, write one continuous take with the events in sequence.
- **Plan the first two seconds.** Make one point readable at a glance, with movement already happening and sound starting on the first frame.
- **Keep text out.** Video models garble writing. Ask for blank signs and screens and add exact text later with ffmpeg or code.

## Prompt template

Delete the lines you don't need and fill in every bracket.

```text
[References]
Image 1 is [character] - use the face, hair and outfit, not the background or pose.
Image 2 is [location] - use the layout, materials and light, not the people.
Image 3 is [product] - use the exact shape, colour and material.

[Look]
[kind of image], [lens and depth of field], [colour temperature, saturation], key light from [direction], [visible materials and atmosphere: steam, rain streaks, dust in light].

[Overview]
[Who] in [where]; [one sentence with the visible sequence of events].

[Shots]
Shot 1: Start on [shot size, camera height, angle]. The camera [one move, direction, speed], ending on [final framing]. [Who moves from where to where, how fast, with what visible result]. [Dialogue in quotes with the speaker named; synced sound effects and ambience]. Cut on [an action point].
Shot 2: ...

[Close]
Keep characters, wardrobe, setting and look consistent with the references. No captions, no watermark, no on-screen text.
```

## Camera language

| Move                               | Use it to                                         |
| ---------------------------------- | ------------------------------------------------- |
| Push in / pull out                 | Build emphasis / reveal context                   |
| Tracking shot (side, follow, lead) | Travel with the subject's action                  |
| Orbit / arc                        | Show a product or hero moment in 3D               |
| Crane up / down                    | Open or close a scene, reveal scale               |
| Handheld, slight shake             | Documentary or UGC feel, urgency                  |
| Whip pan                           | Energetic transition between subjects             |
| Locked-off                         | Comparison, reading, a performance, comedy timing |

Pair one main move with the subject's own motion. "Close-up", "selfie view" and "handheld" describe framing or method, not a move. Still say where the camera goes.

## Sound

Both models generate sound with the picture:

- **Dialogue:** the speaker and the line in quotes, plus "lip-synced". Keep lines short enough to fit the shot.
- **Ambience and effects:** the source, the action and the timing. For example: "the espresso machine hisses as the milk foams; a cup clinks on the saucer at the end".
- **Music:** the style, tempo and mood when the clip should carry music. When music will be added later in the edit, write "no music, natural ambience and effects only" so the clips cut together cleanly.
- **Silence** only when the user asks for it.

## References and keyframes

- **References (up to 9):** use them for identity (characters, products, logos as objects, locations). Cite each by position ("Image 1"). Say what to take from it and what to ignore.
- **`keyframes.first`:** the clip starts from this exact image. This gives the best control over composition and is the way to continue from the last frame of a previous clip.
- **`keyframes.first` + `keyframes.last`:** for transformations, before/after and time-lapses. The two images must share the framing, and the prompt describes the change between them. This mode cannot be combined with references.
- **Images must match the aspect ratio** you request (landscape or portrait). Crop or regenerate mismatched images first. Sandbox paths and URLs both work.

## Examples

**Product hero, H3 Max, 8 s, landscape:**

```text
Image 1 is the product - match the bottle shape, amber glass and gold cap exactly.
Look: glossy commercial product film, 85mm macro, shallow depth of field, warm 3200K key light from the left, dark walnut surface with water droplets.
Shot 1: Start on an extreme close-up of droplets sliding down the amber glass. The camera slowly pushes in as one drop runs off the edge; a soft liquid drip sound.
Shot 2: Cut to a medium shot. The bottle rotates a quarter turn on a turntable while the camera arcs left around it, ending centred and still. A low synth swell rises and lands as the motion stops.
No text, no watermark.
```

**Continuous motion-design take, WAN 3.0, 15 s, landscape, 720p:**

```text
Look: clean 3D motion design render, soft global illumination, seamless off-white studio, palette of tangerine, cobalt and cream, materials chrome, frosted glass and matte clay.
One continuous take, no cuts: a glossy tangerine sphere drops in and bounces with squash and stretch (0-3s); it bursts into a grid of small spheres that ripple in a wave and shift to cobalt (3-6s); the grid folds into a frosted glass cube that the camera orbits (6-10s); the cube shatters into thousands of particles that swirl into a tight vortex (10-13s); the vortex collapses into one bright point and the frame settles on the empty studio (13-15s).
Camera: slow continuous orbit that tightens toward the end.
Sound: minimal electronic beat at 110 BPM; a soft thump on each bounce, a rising whoosh into the vortex, a glass shatter at 10 seconds, a deep bass hit on the final point.
```

## Before you submit

1. Every bracket is filled, unused lines are deleted, and the prompt is in English with quoted dialogue in the requested language.
2. The model, duration, aspect ratio, resolution and references fit the tool's limits (see `SKILL.md`).
3. Someone reading only the prompt could describe each shot's action, camera path and ending.
4. Sound is planned: dialogue fits the time, effects are tied to events, and music is either included or deliberately left out.
5. People and products have references. Text is left for the overlay.
