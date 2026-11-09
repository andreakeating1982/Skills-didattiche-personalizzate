# Stories, short films and recurring characters

For narrative shorts, music videos, story clips for kids or brands, and any video where the same character appears in several shots.

## Shape the story

- **Scope.** Keep it to one theme, one or two characters and one to three locations, with a clear beginning, turn and resolution. Thirty seconds holds about 6-10 shots, sixty seconds 12-20.
- **Telling.** Let the characters' actions and dialogue carry the story. Use a narrator only when the user asks or the format needs it (a fairy tale, a documentary voice).
- **Shot list.** Write it before generating. For each shot give:
  - the starting framing;
  - who does what, with a visible result;
  - the camera move;
  - the spoken line, if any, and the sound;
  - the duration;
  - how it ends, so the next shot can pick up.

## Character consistency

1. **Master reference first.**
   - Generate one hero image per character with `media_generate_image`: full body, neutral pose, plain background, the exact outfit, and a clear description of face, hair, age and build.
   - Show it to the user when the character matters to them.
2. **Derive views from the master.** For close-ups or other angles, use `media_generate_from_images` with the master as input. Never generate a fresh identity for each view.
3. **Location references.** When the setting repeats, a location image keeps the space and light consistent. Otherwise one reusable style sentence is enough.
4. **Pass references to every clip.**
   - In `references`, cite them in the prompt by role: "the girl from Image 1, the kitchen from Image 2".
   - Keep the same style sentence in every prompt.
   - Never change wardrobe or hair unless the story does.

## Generating

- **Fewest clips that fit.**
  - Group consecutive shots into one request when they share a location: H3 Max up to 15 s, Seedance 2.5 up to 30 s with the most realistic acting.
  - Use WAN 3.0 for a long single take, such as a tracking shot that follows the character.
- **Joins.**
  - When a shot must continue exactly where the last one ended, extract the last frame of the previous clip (`../references/ffmpeg.md`) and use it as `keyframes.first`.
  - Otherwise cut on action. A clean cut between angles hides small differences.
- **Dialogue.**
  - Put lines in quotes with the speaker named ("the old man says: ...").
  - Keep each line short enough to fit its shot (about 2.5 words per second).
  - Name the language and accent when it isn't English.
- **Music videos.**
  - Make or get the song first (`media_generate_music`, or the user's track).
  - Plan shots on the song's sections and cut on the beat when assembling.
  - Generate clips without competing music ("no music, ambient sound only") and lay the song over them.

## Assemble and check

- Join with ffmpeg, keeping each clip's dialogue and ambience. Add the score underneath.
- Watch for identity drift (face, outfit), a story beat that didn't happen, and broken joins.
- Re-generate only the failing shot, with a more specific action line or a better reference.
