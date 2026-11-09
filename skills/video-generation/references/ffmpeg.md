# ffmpeg recipes

Tested commands for assembling and checking video in the sandbox. Work in a project folder such as `/home/user/video/`, keep the sources untouched, and write the outputs to new files.

## Contents

- Setup and inspection
- Download generated clips
- Normalise and join
- Transitions
- Text, titles and subtitles
- Audio
- Reframe and export
- Quality checks
- Transcription with timestamps

## Setup and inspection

```bash
which ffmpeg ffprobe || (sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg)
ffprobe -v error -show_entries format=duration:stream=index,codec_type,width,height,r_frame_rate -of compact clip.mp4
```

If apt is busy or slow, `pip install imageio-ffmpeg` gives a static ffmpeg binary at `python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"` (no ffprobe; use `ffmpeg -i clip.mp4` to read the stream info).

Long renders and encodes: run them with `shell` exec `background: true` and `notify: true`.

## Download generated clips

```bash
mkdir -p /home/user/video && cd /home/user/video
curl -L -o shot1.mp4 "<videoUrl from media_generate_video>"
```

## Normalise and join

Clips from different sources differ in size, frame rate and audio. Normalise inside the join so it never fails on a mismatch:

```bash
ffmpeg -y -i a.mp4 -i b.mp4 -i c.mp4 -filter_complex "\
[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v0];\
[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v1];\
[2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v2];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[2:a]aresample=48000,aformat=channel_layouts=stereo[a2];\
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart joined.mp4
```

- For portrait output use `1080:1920`.
- A clip without an audio stream breaks `concat` with `a=1`. Give it silence first:
  `ffmpeg -y -i silent.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -c:v copy -c:a aac fixed.mp4`
- Trim precisely while re-encoding: `ffmpeg -y -ss 3.2 -to 9.8 -i in.mp4 -c:v libx264 -crf 18 -c:a aac out.mp4`

## Transitions

Cross-fade two normalised clips. The offset is where the fade starts, which is the first clip's length minus the fade:

```bash
ffmpeg -y -i a.mp4 -i b.mp4 -filter_complex \
"[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v];[0:a][1:a]acrossfade=d=0.5[a]" \
-map "[v]" -map "[a]" -c:v libx264 -crf 18 -c:a aac xfade.mp4
```

Other values for `transition=`: `wipeleft`, `slideup`, `circleopen`, `dissolve`, `smoothleft`. Use hard cuts by default. Use transitions only when they help the story.

## Text, titles and subtitles

`drawtext` and `subtitles` need a font file. Download a proper typeface instead of relying on system fonts. Inter is a clean text face; Anton is a bold display face for titles:

```bash
mkdir -p /home/user/fonts && cd /home/user/fonts
curl -L -o Inter.ttf "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf"
curl -L -o Anton.ttf "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
```

Title over video, fading in at 1 s and out at 4 s:

```bash
ffmpeg -y -i in.mp4 -vf "drawtext=fontfile=/home/user/fonts/Inter.ttf:text='Launch day':fontsize=96:fontcolor=white:x=(w-text_w)/2:y=h*0.72:alpha='if(lt(t,1),0,if(lt(t,1.4),(t-1)/0.4,if(lt(t,3.6),1,if(lt(t,4),(4-t)/0.4,0))))'" -c:a copy titled.mp4
```

For anything richer than one line (logos, cards, animated type), render an overlay with code (`code-rendering.md`) and composite it:

```bash
ffmpeg -y -i base.mp4 -i overlay.mov -filter_complex "[0:v][1:v]overlay=0:0:shortest=1" -c:v libx264 -crf 18 -c:a copy composite.mp4
```

Burn in subtitles from an SRT file, styled:

```bash
ffmpeg -y -i in.mp4 -vf "subtitles=subs.srt:fontsdir=/home/user/fonts:force_style='FontName=Inter,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=60'" -c:a copy subtitled.mp4
```

For CJK, Arabic, Thai or Devanagari text, download a Noto font that covers the script (for example Noto Sans SC) and point `fontfile` or `FontName` at it.

## Audio

Music under dialogue, with the music ducked whenever someone speaks:

```bash
ffmpeg -y -i video.mp4 -i music.mp3 -filter_complex \
"[1:a]volume=0.35,afade=t=in:d=1,afade=t=out:st=27:d=3[m];[m][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[duck];[0:a][duck]amix=inputs=2:duration=first:normalize=0[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k mixed.mp4
```

Other recipes:

- Replace the audio entirely: `ffmpeg -y -i video.mp4 -i voice.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest out.mp4`
- Normalise loudness for social (about -14 LUFS): add `-af loudnorm=I=-14:TP=-1.5:LRA=11` on the final encode.
- Speed change: `-filter_complex "[0:v]setpts=PTS/1.25[v];[0:a]atempo=1.25[a]"`

## Reframe and export

16:9 to 9:16 with a blurred fill instead of black bars:

```bash
ffmpeg -y -i wide.mp4 -filter_complex \
"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:2[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]" \
-map "[v]" -map "0:a?" -c:v libx264 -crf 18 -c:a aac vertical.mp4
```

Other exports:

- Centre crop to 9:16: `-vf "crop=ih*9/16:ih,scale=1080:1920"`
- Web-ready MP4: `-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`
- GIF: `ffmpeg -y -i in.mp4 -vf "fps=12,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif`

## Quality checks

Contact sheet (one frame every second in a grid), then view it with `file_view`:

```bash
ffmpeg -y -i final.mp4 -vf "fps=1,scale=384:-1,tile=5x4" -frames:v 1 contact.png
```

Other checks:

- Frames at exact times: `ffmpeg -y -ss 4.5 -i final.mp4 -frames:v 1 t4_5.png`
- Last frame of a clip, to continue the next clip from it with `keyframes.first`: `ffmpeg -y -sseof -0.1 -i shot1.mp4 -frames:v 1 shot1_last.png`
- Loudness: `ffmpeg -i final.mp4 -af ebur128 -f null - 2>&1 | tail -12`
- Final probe: `ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact final.mp4`

## Transcription with timestamps

- **Quick:** `file_view` on the video or audio with the prompt "Transcribe all speech as SRT subtitles with accurate start and end times, max 42 characters per line".
- **Precise word timing:** use faster-whisper on CPU.

  ```bash
  pip install -q faster-whisper
  python3 - <<'EOF'
  from faster_whisper import WhisperModel
  model = WhisperModel("small", device="cpu", compute_type="int8")
  segments, info = model.transcribe("in.mp4", word_timestamps=True)
  def ts(t):
      h, r = divmod(t, 3600); m, s = divmod(r, 60)
      return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")
  with open("subs.srt", "w") as f:
      for i, s in enumerate(segments, 1):
          f.write(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n\n")
  EOF
  ```

  On this sandbox's 2 CPUs the `small` model runs at roughly the speed of the audio. Use `base` for long files, and run long transcriptions in the background.
