---
name: video-generation
description: Plan and produce videos. Use for any request to generate, animate or edit video, including ads and promos, motion graphics, logo and text animation, social clips, music videos, character stories, and trimming, joining, subtitling or reformatting existing footage.
---

# Video generation

Make the video the user asked for as a playable file or link. Two ways to make the picture, often combined:

- **Model generation** with `media_generate_video`: people, products, places, cinematic camera work, stylised or 3D animation, transformations.
- **Code rendering** in the sandbox: anything that must be exact, such as text, logos, numbers, charts and UI. Frames are drawn in HTML or Python and encoded with ffmpeg.

ffmpeg in the sandbox joins, trims, subtitles, mixes and exports.

## Start here

1. Work out what the video must communicate, for whom and where it will play. Settle the aspect ratio (landscape 16:9 for YouTube and desktop, portrait 9:16 for Reels, TikTok and Shorts), the approximate length, and which assets already exist (photos, logos, footage, voice). Use what the request implies and ask only when a missing answer would change the result.
2. Pick the route in the table below and read its files in one parallel batch. Skip files that the task does not need.
3. Plan before generating: one central idea, then a shot or beat list with what happens, the camera, the sound and the length of each part.
4. Generate, inspect, assemble if needed, deliver.

| Request                                                                                   | Read                                                                                                                                    |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Motion graphics, kinetic type, logo stings, animated data, UI animation, design showreels | `workflows/motion-graphics.md`, then `references/code-rendering.md` for code renders or `references/video-prompts.md` for model renders |
| Ads, product promos, launch teasers, UGC-style clips, social hooks                        | `workflows/ads-and-promos.md` and `references/video-prompts.md`                                                                         |
| Short films, music videos, recurring characters, story clips                              | `workflows/stories-and-characters.md` and `references/video-prompts.md`                                                                 |
| The user's own footage: trim, highlights, join, subtitles, music, resize                  | `workflows/editing-footage.md` and `references/ffmpeg.md`                                                                               |
| Joining generated clips, adding music or titles                                           | `references/ffmpeg.md`                                                                                                                  |

## The video tool

Reading this skill unlocks the media tools. If `media_generate_video` is still missing, call `media_generate` with a one-line brief. Video is not available on the Free plan.

- The tool's description lists every model with its lengths, resolutions and credits per second, and says which model fits which request. Use the model the user names; otherwise follow that guidance.
- MiniMax H3 Max (the default) returns the finished `videoUrl` in the same call. WAN 3.0, Kling 4.0 and the Seedance models render in the background: the call returns a `jobId` at once and you are resumed automatically with the video after a few minutes. Never poll and never call the tool again for the same clip. When a plan needs several background clips, start them all in the same step so you are resumed once.
- H3 Max and Seedance 2.5 can follow a multi-shot prompt (`Shot 1`, `Shot 2`, ...) inside one clip. WAN 3.0 renders one continuous take with strong camera work.
- Every model generates audio with the picture. Describe dialogue (quoted), ambience, sound effects and music in the prompt.
- Modes: text-to-video; image-to-video (`keyframes.first`); first-to-last frame (`keyframes.first` + `keyframes.last`); reference images (cited as "Image 1", "Image 2" in list order — @Image1, @Image2 with Kling 4.0 — not combinable with `keyframes.last`). An image start frame gives better, more controllable results than text alone.

## Rules that decide quality

- **People and products need image references.** Use the user's photos or generate a reference with `media_generate_image` first, then pass it as `keyframes.first` or in `references`. Settings, lighting and style can be described in words.
- **Exact text, logos, prices and UI are never left to the video model.** It garbles them. Render them in code or overlay them with ffmpeg.
- **One clip per request whenever it fits the model.** Split only for real limits (a 45-second ad is several clips joined with ffmpeg) or when the user wants separate clips.
- **Write the model prompt in English.** Quote spoken lines and on-screen words in the language the user wants.
- **Spend deliberately.** For several clips or long background renders, state the shot plan and the total credits in one line. Ask for a go-ahead only when the total is far above what the user would expect.

## Check and deliver

- Inspect every result before delivering. Use `ffprobe` for duration, size and audio, and a contact sheet of frames (see `references/ffmpeg.md`) viewed with `file_view`. `file_view` also analyzes a video file or URL directly when you need to check motion, speech or sound.
- **Never generate a clip again on your own.** Every clip costs credits. If a result has a real failure (wrong subject, broken identity, garbled required text, a missing action), show it, say in one sentence what is wrong, and ask whether to make a corrected version. Generate again without asking only when the user told you to keep fixing it until it is right.
- Code renders and ffmpeg edits cost no credits: fix real problems in them yourself, but stop polishing once a frame works.
- Delivery: a single model clip is shown in the chat from its `videoUrl`. Files you assembled or rendered in the sandbox go out with `send_attachment`. In one or two lines, state the format, aspect ratio, length and whether there is sound.
- For a narrated explainer, a talking avatar or long timeline editing, the platform's Video Agent, Talking Videos or Video Editor can fit better. Offer the link when it does.
