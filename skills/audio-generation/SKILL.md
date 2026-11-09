---
name: audio-generation
description: Make speech, music, sound effects and any other audio. Use for voice-overs and narration, dialogue and character voices, podcasts or audiobook samples, songs with lyrics, background music and jingles, sound effects, ambience and soundscapes, sound for a picture or a video, and for mixing voice, music and effects.
---

# Audio generation

Three tools. Reading this skill unlocks them; if they are still missing, call `media_generate` with a one-line brief.

| Need                                                                                                           | Tool                               | Read                                                                              |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------- |
| Narration, voice-over, announcements read in a ready-made voice                                                | `media_generate_speech`            | `references/speech.md`                                                            |
| Songs with vocals, instrumentals, jingles, background music                                                    | `media_generate_music`             | `references/music.md`                                                             |
| Sound effects, ambience, soundscapes, voices described in words, acted dialogue, short music cues, full scenes | `media_generate_audio`             | `references/audio.md`                                                             |
| Voice, music and effects together, timing to a video                                                           | The tools above, mixed with ffmpeg | the references above + `../video-generation/references/ffmpeg.md` (Audio section) |

## What each tool does

- **`media_generate_speech`** (text, language, accent, gender, speed): picks a fitting voice from the platform's voice library for the language, accent and gender, and returns an MP3 URL right away.
  - Up to 5,000 characters per call; anything longer is cut off.
  - Speed 0.7-1.2.
  - You cannot pick a named voice or the user's cloned voice here. When they want that, point them to the Text to Speech page, where they choose any voice or their own clone.
- **`media_generate_music`** (Suno): instrumentals or songs with lyrics.
  - Runs as a background job of 2-4 minutes and returns a `jobId` at once. You are resumed automatically with the audio. Never poll and never call it again for the same track.
  - Each run normally returns two versions of the track.
- **`media_generate_audio`** (Seed Audio 1.0): any audio from a description, voices included, mixed in one take. Returns the audio URL in the same call: about 20-40 seconds for a clip under a minute, 1-2 minutes (rarely 3) for longer ones.
  - Up to about 2 minutes per call, in 20+ languages. The length is a target, not a promise.
  - Voices are described, not picked: gender, age, accent, emotion and pace. Up to 3 reference clips keep a voice or a sound the same across calls.
  - Each call uses 1,000 of the user's audio characters, whatever the length: as much as about 2,000 characters read by `media_generate_speech`.

## Speech or audio?

- **The words matter most** and a ready-made voice is fine (a voice-over, an announcement, a long script): `media_generate_speech`. The words come out exactly as written, and it is cheaper.
- **The performance or the setting matters** (a character, real emotion, laughter, people talking to each other, a voice on a phone line or in a hall, sound around the voice): `media_generate_audio`.
- **Anything that is not speech or a full song** (effects, ambience, a jingle sting, a notification sound, a foley track for a video): `media_generate_audio`.

## Workflow

1. **Settle the job.** Where the audio will be heard (video, podcast, ad, game, phone message), the language and accent, the length, the mood, and whether it must fit an exact duration.
2. **Write the words, the musical brief or the sound description** using the reference file, then generate.
3. **When timing matters** (a voice-over for a video, an effect on a cut), measure the result with `ffprobe` before building anything on it. Adjust with the speed parameter, by trimming the script, by trimming or padding with ffmpeg, or by re-timing the visuals. Never stretch speech with ffmpeg.
4. **Long or multi-voice work:**
   - With `media_generate_speech`, generate one file per paragraph or per speaker turn. Download them into the sandbox and join them with short silences (see the speech reference). Keep each character on the same language, accent and gender settings so the same kind of voice is picked.
   - With `media_generate_audio`, a whole scene of up to about 2 minutes is one call. For longer pieces, continue from the previous part with a reference clip (see the audio reference).
5. **Mixing:** put the music under the voice, about 15-20 dB lower, with ducking when someone speaks. Fade the music in and out. Keep effects clear of the words. Normalise the final mix to about -16 LUFS for spoken content or -14 LUFS for social video.
6. **Deliver:**
   - Share the audio URL for a single file. The chat shows a player.
   - Send mixed or joined files from the sandbox with `send_attachment`.
   - Say the length and, for songs, which of the two versions you recommend and why.

## Platform features without a tool here

Saved voice clones, AI dubbing of a video into another language, and choosing among thousands of named voices are separate Easy-Peasy.AI features (Text to Speech, Dubbing). Link them when the user needs them instead of improvising.
