# Motion graphics

Motion graphics communicate with shape, type, colour and movement rather than with filmed action. This covers showreels, kinetic typography, logo stings, animated stats and charts, UI walkthroughs, lower thirds, title cards and transition elements.

## Choose how to make it

| Route        | Use for                                                                                                                                                                   | How                                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Model render | Abstract or 3D motion design, morphing shapes, particles, liquids, materials (chrome, glass, clay), camera moves through a stylised world, "show me something impressive" | `media_generate_video`, prompt written as a timed sequence of transformations (see `../references/video-prompts.md`) |
| Code render  | Exact words, brand logos, numbers that count up, charts, UI screens, captions, overlays with transparency, anything the user may want to edit later                       | HTML or Python frames encoded with ffmpeg (see `../references/code-rendering.md`)                                    |
| Hybrid       | A rich background with exact text or logo on top                                                                                                                          | Model render for the plate, code render for the type, composited with ffmpeg overlay                                 |

When the request is open ("show what you can do", "make it dynamic"), a model render usually gives the most impressive result per credit. For 15 seconds, H3 Max (60 credits) can carry a multi-shot sequence. WAN 3.0 at 720p (75 credits) gives one continuous take with smoother camera work. Seedance 2.5 at 720p (180 credits) gives the richest motion and physics but renders for several minutes. If the piece ends on a name or a slogan, finish it as a hybrid so the words are exact.

## Design the piece

1. **One idea.** Write it in a sentence ("a paper plane folds itself out of the logo, flies past three product benefits and lands on the sign-up button"). Every beat serves it.
2. **Beats.** Split the length into 3-7 beats. Each beat has an entrance, a readable hold and a transition into the next. Keep one focal point at a time.
3. **Timing.**
   - Give a held line of text about 0.3 seconds per word plus 0.5 seconds.
   - Transitions take 0.3-0.8 seconds.
   - Hold the final frame at least 1 second.
   - Make the first second move. Social feeds decide in two seconds.
4. **Look.**
   - Use 2-3 colours plus a neutral, and 1-2 typefaces.
   - Keep consistent corner radius, stroke weight and spacing.
   - Use the brand's palette, fonts and logo files when they exist. Never redraw a logo: use the file.
5. **Motion.**
   - Ease out on entrances, ease in on exits, and never move linearly except for constant drifts.
   - Use anticipation and overshoot for energy.
   - Stagger related elements by 40-80 ms.
   - Hand off motion from one element to the next so the eye always knows where to look.
6. **Sound.**
   - Pieces meant to be watched with sound need a music bed and hits on the key events (a whoosh on a reveal, a click or pop on a snap, an impact on the logo).
   - Model renders generate sound when the prompt describes it.
   - For code renders, generate a bed with `media_generate_music` (it runs in the background, so start it while you render frames), make the hits with `media_generate_audio` (see `../../audio-generation/references/audio.md`) and place them with ffmpeg, or deliver silent if the user asked for an overlay.

## Write the model prompt (model route)

Describe the sequence in order, with visible events only:

```text
Style: [render style, e.g. "glossy 3D motion design render, soft studio lighting, clean seamless background"], palette [colours], materials [chrome, frosted glass, matte clay].
Sequence (15 seconds, continuous, no cuts):
0-2s: [what appears and how it moves]
2-5s: [transformation into the next state]
...
Camera: [one move per phase: slow orbit, push in, crane up]
Sound: [music style and tempo], [sound effects tied to events: thump when the ball lands, glass shatter at 9s, bass hit on the final word]
End: [final composition held for 1-2 seconds]
```

Avoid asking the model for exact words longer than one short word. Put real text in a code overlay.

## Make it (code route)

Read `../references/code-rendering.md`. Build one self-contained scene (HTML with time-driven animation, or a Python frame function), render a few stills at the key beats, check them with `file_view`, then render the full video and encode it.

## Check

- Look at a contact sheet covering the opening, every hold, each transition and the final frame.
- Text is legible, inside safe margins (about 5% from each edge, more at the bottom of portrait video where platforms put captions), and never clipped.
- Motion settles before each hold, colours match the brand, transparency survives the output format when an overlay was requested.
- Run `ffprobe` for the dimensions, length, frame rate and audio stream.

Deliver the video and, when the user may want to change it later, the source (HTML or script) too.
