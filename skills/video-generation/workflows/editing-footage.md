# Editing the user's footage

For trims, highlight reels, joining clips, subtitles, adding music or a voice-over, removing silence, resizing for another platform and exporting.

## Steps

1. **Get the files into the sandbox.**
   - Uploads are listed under Sandbox Files.
   - Files at a URL: `file_upload`, or `curl -L -o` in the shell.
2. **Inspect before cutting.** Read the duration, resolution, frame rate, rotation and whether there is an audio stream:
   ```bash
   ffprobe -v error -show_entries format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate:stream_side_data=rotation -of compact input.mp4
   ```
3. **Understand the content.**
   - For "find the best moments", "cut the boring parts" or "add subtitles", call `file_view` on the video with a precise prompt. For example: "List every topic change with start and end timestamps" or "Transcribe the speech as SRT with accurate timestamps".
   - For exact word timing on long talks, transcribe locally with faster-whisper (see `../references/ffmpeg.md`).
4. **Write an edit list** before running commands: the source ranges, their order, transitions, text and audio decisions. Keep it in a small file so the edit can be reproduced and adjusted.
5. **Cut with re-encoding** for frame-accurate edits. Stream copy (`-c copy`) is only for quick trims where a slightly early cut is fine.
6. **Assemble** with the recipes in `../references/ffmpeg.md`:
   - normalise size, frame rate and audio before joining;
   - keep the original dialogue;
   - put music under speech, not over it.
7. **Export** H.264 + AAC MP4 with `-pix_fmt yuv420p -movflags +faststart` unless the user asks for something else.

## Common requests

| Request                              | Approach                                                                                                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Highlights / short from a long video | Find candidate moments with `file_view`, keep complete thoughts (never cut mid-sentence), 20-60 s total for social, add captions |
| Vertical version                     | Crop around the subject (center or a chosen x offset), or scale to fit width on a blurred copy of itself                         |
| Subtitles                            | Create an SRT (from `file_view` or faster-whisper), then burn it in with the `subtitles` filter or deliver it as a separate file |
| Remove silences                      | `silencedetect` to find gaps over 0.6 s, then trim and join the spoken parts                                                     |
| Background music                     | Lower the music to sit under speech (about -18 dB, or sidechain ducking) and fade in and out                                     |
| Sound effects or ambience            | Make them with `media_generate_audio` (see `../../audio-generation/references/audio.md`), then place and mix them with ffmpeg    |
| Speed up / slow down                 | `setpts` for video with `atempo` for audio (0.5-2.0 per filter)                                                                  |
| Make a GIF                           | Two-pass palette (`palettegen` then `paletteuse`), 10-15 fps, width 480-720                                                      |

## Check

- Play-test the cut points with a contact sheet around each edit.
- Confirm the audio is in sync after trims and speed changes.
- Subtitles stay readable and inside the frame.
- The output plays (`ffprobe` shows video and audio streams with the expected length).
