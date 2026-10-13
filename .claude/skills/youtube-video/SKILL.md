---
name: youtube-video
description: >
  This skill should be used when the owner wants a Kora Klicks YouTube video: "make the weekly
  Europe roundup video", "فيديو ملخص الدوريات الأوروبية", "فيديو ملخص الدوري المصري والسعودي",
  "فيديو أهم الأخبار", "YouTube video", "motion graphics video", or when a scheduled YouTube run fires.
  It runs youtube-scriptwriter → editor → motion-producer → review, then sends the video to the
  owner for approval. Nothing is uploaded to YouTube without the owner's explicit approval.
  Accepts an optional format: europe-roundup, egypt-saudi-roundup, or top-news.
metadata:
  version: "0.1.0"
---

# Kora Klicks YouTube video

Load the `newsroom-rules` skill first, then read `references/video-formats.md`.

## Pipeline

1. **Pick the format** from the argument; if none, ask BOSS which is due (Europe roundup after
   the European round, Egypt/Saudi roundup after those rounds, top-news 2–3 times a week).
2. **Facts**: ask news-desk and live-score-desk for the verified facts the format needs (results,
   scorers, standings, confirmed news) with sources. Only CONFIRMED facts, plus any UNCONFIRMED
   story the owner already approved.
3. **Script**: the **youtube-scriptwriter** agent writes (a) the narration script, (b) the
   storyboard JSON per `references/storyboard-schema.md`, and (c) the YouTube metadata.
4. **Edit**: the **editor** agent fact-checks every scene, number and name against the sources.
   Fix and repeat until it passes.
5. **Sound (default: original music, no voice-over)**: run
   `python3 .claude/skills/youtube-video/scripts/music.py <storyboard.json> <out_dir> --bpm 124 --mood drive --grid 1`.
   It composes an original electronic sports track in code (no samples, so no copyright claims),
   snaps every scene to the beat, adds a build-up into the first cut, an impact on every scene change
   and a clean ending, normalises to −14 LUFS, and writes `<slug>-timed.json`.
   Vary `--mood` (drive / dark / anthem) and `--seed` between videos so episodes don't sound identical.
   Voice-over is **optional**: only when the owner asks for it or sends recordings, use the
   **voiceover-artist** agent and `scripts/voiceover.py` (see `references/voiceover.md`).
6. **Produce**: the **motion-producer** agent renders a `--preview` from the timed storyboard first, checks it, then renders
   the final video with `scripts/render.py`.
7. **Review**: the motion-producer and editor review the contact sheet and key frames (checklist
   in the motion-producer agent). Re-render until the review passes.
8. **Send to the owner** (never upload first). Deliver with the file-sending tool: the MP4, the
   thumbnail, and a short Arabic message:

   ```
   🎬 فيديو جاهز للمراجعة: [عنوان الفيديو]
   المدة: [mm:ss] · النوع: [format]
   اتراجع: ✔ الأرقام والأسماء ✔ المصادر ✔ النص العربي ✔ التوقيت مع الصوت
   الصوت: [موسيقى أصلية · mood · BPM] (أو: تسجيلك)
   العنوان والوصف والتاجز جاهزين تحت.
   رد بـ: ✅ ارفع | ✏️ عدّل (قولّي إيه) | ❌ الغي
   ```

   Then paste the title, description (with chapters and sources) and tags.
9. **Upload** only after the owner's ✅: hand to the **youtube-publisher** agent. On ✏️, apply the
   changes, re-render, and send again.

## Notes

- Owner decision (11 Oct 2026): videos use **original music and no voice-over** by default, so the on-screen text must tell the whole story.
- Music: only the generated track from `music.py`, or a file the owner has rights to. Never use commercial songs.
- Rendering needs Python Playwright (Chromium) and ffmpeg. Install them if missing (`pip install playwright`, then install Chromium with Playwright).
- Example storyboard: `examples/example-storyboard.json`.


## Daily story + short (vertical)

For the noon "top matches today" and the night "today's results" pieces, use
`python3 .claude/skills/youtube-video/scripts/story_short.py spec.json OUT_DIR` (spec format in the script's docstring).
It writes `<slug>-story.jpg` (1080x1920 still for Instagram/Facebook stories) and `<slug>-short.mp4`
(~15 s vertical video with original music for Reels, TikTok and YouTube Shorts). Check a few frames before publishing.

## Motion-graphics shorts with music and memes (owner request 13 Oct 2026)

**Owner approved this style (13 Oct 11:46): `motion_short.py` is the DEFAULT for every Reel/Short/TikTok** (results, fixtures, numbers, Arab players, memes). Use `story_short.py` only for the Story still.

`scripts/motion_short.py spec.json OUT_DIR [--theme dark|light] [--mood fun|drive|anthem|dark] [--preview]`
makes a 15–30 s vertical short with kinetic text, beat-synced camera punches, flashes, pops and whooshes on original
music (music.py; `fun` mood = bouncy pluck track for memes). Scene types: `hook`, `versus`, `score`, `stat`, `expect`
(expectation vs reality), `when` («لما…»), `chat` (fans' group chat), `pov`, `list`, `cta`. Spec format is in the
script's docstring. Always run `--preview` first and look at the sheet (one frame per scene), then render the video.
It writes `<slug>-short.mp4` and `<slug>-cover.jpg` (use the cover as Story/thumbnail).

Two looks side by side (neither replaces the other):
- `--theme dark` = the cinematic house look: night results, FT shorts, «ليلة الأبطال».
- `--theme light` = bright version (ice/mint/sky, black wordmark): daytime previews, fixtures, memes, tables.
  `story_short.py` also takes `--theme light`. Aim for about half of the day's shorts in each look.

Memes: original typographic + emoji jokes about the fan experience (late kick-offs, last-minute goals, predictions
gone wrong, the group chat during the match). Never mock a club, player or fan base, never use film/series stills
or other people's photos, no crests, no betting; chat names are invented generic first names. Facts on screen
(scores, times, numbers) still need sources. One meme short a day at most; big-match days are the best fit.
