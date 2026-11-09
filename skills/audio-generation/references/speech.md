# Speech with media_generate_speech

## Parameters

- `text`: exactly what is spoken. Everything in it is read aloud, so never put instructions such as "say this cheerfully:" here. Write it in the target language and script (Japanese in Japanese characters, and so on). Maximum 5,000 characters per call.
- `language`: for example English, Spanish, French, German, Portuguese, Japanese, Korean, Chinese, Arabic, Hindi. It sets which voices are eligible and how words are pronounced.
- `accent`: for example American, British, Australian, Indian or Irish. Use it for regional English or Spanish.
- `gender`: male or female.
- `speed`: 0.7-1.2. Keep the default 1.0 unless timing requires otherwise. Any other value switches to a model that ignores expressive tags.

## Writing text that sounds right

The delivery comes from the text itself:

- **Punctuation is pacing.** Commas give short pauses, full stops longer ones, and an ellipsis (...) a hesitation or trailing off. A paragraph break gives a longer pause.
- **Write for the ear.** Use short sentences, contractions and plain words. Spell out what must be read a particular way:
  - "twenty twenty-six" or "two thousand twenty-six";
  - "five hundred dollars" rather than "$500" when the format matters;
  - acronyms said letter by letter with spaces or dots ("A.I.");
  - a name the voice gets wrong, written the way it sounds (for example "Nguyen" as "Win").
- **Emotion in the words.** Exclamation marks and question marks shape intonation. A line written excitedly sounds excited.
- **Expressive tags.** Bracketed cues such as `[laughs]`, `[sighs]`, `[whispers]` or `[excited]` are acted out by some voices and silently skipped by others. They are never read aloud. Use them only as a bonus, never to carry meaning, and keep them few.

Timing: speech runs at roughly 2.5 words per second in English (150 words per minute). A 30-second voice-over is about 70-75 words. Check the real length with `ffprobe` after generating.

## Long texts and dialogue

1. **Split on paragraph or speaker boundaries,** each under 5,000 characters. Generate the parts in parallel.
2. **Download and join** with short pauses in the sandbox:
   ```bash
   cd /home/user/audio
   ffmpeg -y -f lavfi -t 0.4 -i anullsrc=r=44100:cl=stereo pause.mp3
   printf "file 'part1.mp3'\nfile 'pause.mp3'\nfile 'part2.mp3'\n" > list.txt
   ffmpeg -y -f concat -safe 0 -i list.txt -c:a libmp3lame -q:a 2 narration.mp3
   ```
3. **Dialogue:** each speaker keeps fixed `language`, `accent` and `gender` values. Generate line by line in order and join with 0.2-0.5 s gaps. For very different characters, vary the accent or gender so the voices are clearly distinct.

## Voice-over for video

Write the script to the shot timing, for example one sentence per shot. Generate it, measure it, then assemble the video to the voice, not the voice to the video. Keep the clip's own ambience under the voice-over unless it competes.
