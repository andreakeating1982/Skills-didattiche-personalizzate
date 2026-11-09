# Music with media_generate_music

The tool renders on Suno in the background (2-4 minutes) and returns two versions. Never poll and never call it twice for the same track.

## Three modes

| Mode                              | Set                                                                                               | Use for                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Instrumental (default)            | `instrumental: true`, `prompt` describing the sound, plus `genre`, `mood`, `tempo`, `instruments` | Background music, beds for videos and podcasts, intros, game loops            |
| Song, lyrics written by you       | `instrumental: false`, `lyrics`, `style`, optional `vocalGender` (`m` or `f`)                     | Songs where the words matter: birthdays, brand anthems, jingles, lyric videos |
| Song, lyrics written by the model | `instrumental: false`, `prompt` describing the song's story and feel, no `lyrics`                 | Quick songs where the exact words don't matter                                |

In every mode, pass `title`: the name the user gave, or a short one you choose. It is shown while the song renders and saved with it.

## Describing the sound

Build it from concrete musical terms in this order:

1. **Genre and subgenre, with era:** "late-90s UK garage", "modern Afrobeats", "cinematic orchestral trailer".
2. **Mood and energy arc:** "warm and hopeful, builds to an euphoric final chorus".
3. **Tempo:** set `tempo` in BPM. As a guide:
   - ballads 60-80;
   - pop and hip-hop 90-110;
   - house 120-128;
   - drum and bass about 174.
4. **Key instruments and sounds:** "fingerpicked nylon guitar, brushed drums, upright bass, soft Rhodes".
5. **Vocals (for songs):** voice type and delivery, such as "breathy female alto, close-mic'd", "gritty male baritone", "gang-vocal chorus".
6. **Production:** "lo-fi tape warmth", "wide stereo synth pads", "punchy modern mix", "sparse arrangement leaving room for voice-over".

Never name real artists or songs. Describe their sound instead. For music under narration, ask for "sparse, steady dynamics, no lead melody in the vocal range, no drops" so it sits under a voice.

## Writing lyrics

- Mark the structure with section tags on their own lines: `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Verse 2]`, `[Bridge]`, `[Outro]`. Use `[Instrumental Break]` for a solo.
- A 2-3 minute song is usually 2 verses, the chorus 2-3 times and a bridge. Repeat the chorus words exactly each time.
- Keep lines short and singable, with similar syllable counts within a section and clear end rhymes in the chorus.
- Put the hook (the song's title line) in the first and last line of the chorus.
- Write in the language the song should be sung in. Up to 3,000 characters.
- For names and brands, write them as they should be pronounced if they are unusual.

```text
[Verse 1]
Morning light on the harbour wall
Coffee steam and the seagulls call
[Chorus]
We're coming home, coming home tonight
Every window in the town is bright
```

## Fitting a video

Suno decides the length (usually 2-4 minutes for songs, often shorter for instrumentals). For a video, generate once, pick the version whose section changes fall best on the cuts, then trim and fade it with ffmpeg (`afade`, `atrim`). Never generate repeatedly to hit an exact length.

## Choosing between the two versions

Listen-check both with `file_view` on each audio URL (ask whether it matches the brief and whether the vocals are clear). Recommend the one that fits the brief better and offer the other as an alternative.
