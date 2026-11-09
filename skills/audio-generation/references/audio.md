# Audio with media_generate_audio

Seed Audio 1.0 makes the whole soundtrack of a moment from one description: voices, dialogue, effects, ambience and music, mixed together. The call waits and returns the finished file: about 20-40 seconds for a clip under a minute, 1-2 minutes (rarely 3) for longer ones. When a long clip is on its way, tell the user it takes a minute or two.

## Parameters

- `prompt`: everything that should be heard, in plain sentences, up to 2,048 characters. Spoken words go in quotes, exactly as they should be said, in the language they are spoken in. The description around them can stay in English.
- `title`: a short name. It is shown in the chat and saved in the user's Audio Generator creations.
- `duration`: target length in seconds, 1-120. Only a guide: the model decides the exact length. Leave it out when the content sets the length (a line of dialogue).
- `output_format`: `mp3` (default), or `wav` when the user asks for it or the clip will be edited further.
- `speed` (0.5-2) and `pitch` (-12 to 12 semitones): shift how the voices are delivered. Keep the defaults unless the user asks. Describing the pace in the prompt usually sounds more natural.
- `reference_audios`: up to 3 MP3 or WAV clips, each 30 seconds at most and under 10 MB. Cite them in the prompt as `@Audio1`, `@Audio2`, `@Audio3`, in list order.
- `reference_image`: one JPG, PNG or WebP image. It cannot be combined with audio references.

References are sandbox paths (`/home/user/...`) or links to media made in this chat (`https://media.easy-peasy.ai/...`). Download anything else into the sandbox first and pass the path. Cut a longer clip below 30 seconds before using it:

```bash
mkdir -p /home/user/audio
ffmpeg -y -ss 5 -i long.mp3 -t 20 -c:a libmp3lame -q:a 2 /home/user/audio/voice-ref.mp3
```

## Writing the prompt

Write it like a sound designer's brief, in the order things happen:

1. **The place and its ambience:** "a busy street café at noon: chatter, cutlery, an espresso machine hissing".
2. **Each voice:** gender, age, accent, emotion and pace, then the exact words in quotes. Give every speaker a clearly different voice.
3. **The effects, tied to the events they belong to:** "a door slams, then footsteps fade down a wooden corridor".
4. **The music, if any:** style, instruments, tempo and how loud it sits. Write "no music" when there should be none.
5. **The ending:** what fades or stops, and how ("the rain eases off and stops").

Rules:

- Non-verbal sounds belong in the description: laughter, sighs, breaths, hesitations, whispering, shouting ("she sighs, then says...").
- For an effect on its own, start with "Sound effects only, no speech and no music." Then name the source, the material, the size, the distance and the space ("a heavy oak door creaking open slowly in a stone hall, close").
- Tie effects to events, not to timestamps: the model does not follow exact timing for effects and music. When a sound must land on a frame, generate it alone and place it with ffmpeg.
- One moment per clip. A clip that tries to cover several scenes comes out muddled: make one clip per scene and join them.
- Never ask for a real person's voice by name. Describe the voice instead.

## Examples

Sound effect (`duration: 5`):

```text
Sound effects only, no speech and no music. A heavy wooden door in a stone castle hall creaks open slowly, close to the listener, and swings against the wall with a dull thud. A cold draft of wind follows.
```

Ambience to loop (`duration: 30`):

```text
Rain on a tin roof at night, steady and even, with distant rolling thunder twice. No voices and no music. Keep the level even from start to end so it can loop.
```

Dialogue scene:

```text
A small radio studio with quiet room tone. A warm male host in his fifties with a slight Texan drawl says slowly, "Welcome back. Our next caller has been waiting a while." A phone line clicks open. A nervous young woman on a crackly line laughs, then says quickly, "Hi! Sorry, I've never done this before." The host chuckles, "You're doing great." No music.
```

Narration with a described voice:

```text
An elderly British woman with a soft, kind voice tells a bedtime story slowly, close to the microphone: "Once, in a village at the edge of the sea, there lived a lighthouse keeper who was afraid of the dark." A fire crackles quietly in the background. No music.
```

Music sting (`duration: 3`):

```text
A short, bright "level complete" jingle for a mobile game: a rising synth arpeggio, a cheerful marimba hit and a sparkle on the final note. No voice. It ends cleanly.
```

## Keeping a voice across clips, and pieces longer than 2 minutes

Each call starts fresh, so a voice drifts between calls unless you pass a reference:

1. Generate the first part.
2. Cut a clean 10-25 second stretch of the voice to keep (that speaker only, no music) with ffmpeg.
3. Pass it in `reference_audios` and say so in the prompt: "The narrator has the same voice and delivery as @Audio1. She continues: "By morning, the storm had passed..."".
4. Join the parts with ffmpeg and listen to the joins.

The same works for continuing a soundscape or matching the style of a sound the user supplied.

A voice reference must be the user's own voice or one they have permission to use. Never use a clip to make a real person say something they did not say.

## Sound for a picture

Pass the image as `reference_image` and say what to hear: "The sound of the place in this picture, as if standing in it: ...". Use it for ambience that matches a generated scene, or for a voice that suits a pictured character.

## Cost and checking

- Each call uses 1,000 of the user's audio characters, whatever the length. Plan the clips before generating.
- For several short effects, one call can ask for them in sequence with about a second of silence between them. Split them with ffmpeg's `silencedetect`, check each part, and generate them one by one if they run together.
- When the result matters, listen to it with `file_view` on the audio URL (does it match the brief, are the words right, any glitches?). Measure the length with `ffprobe` before timing anything to it.
- Never generate again on your own to fix a detail: say what is off and ask the user first.
