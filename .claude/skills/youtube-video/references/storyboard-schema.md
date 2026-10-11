# Storyboard schema (input for scripts/render.py)

One JSON file per video. All text is Arabic (Egyptian dialect for narration-style lines, exact
names/numbers). Output: 1920×1080 MP4 at 25 fps.

```json
{
  "slug": "europe-roundup-r08",          // file name, latin letters/digits/hyphens
  "episode": "الحلقة 12",                 // small label top-left (optional)
  "format": "europe-roundup | egypt-saudi-roundup | top-news",
  "theme": "major",                       // "major" (default, cinematic black) or "classic" (navy cards)
  "audio": "voiceover.mp3",               // optional; path relative to the JSON. Video is cut to the shorter of the two
  "scenes": [ ... ]
}
```

Every scene may also set `image` (a licensed photo, path relative to the storyboard; shown full-bleed with a dark grade and slow push-in) and `ghost` (the giant faint word behind the scene; defaults: intro/outro «KORA», result «FT», others the title; set `""` for none).

Every scene has `type` and `duration` (seconds). Any scene may add `source` (shown as `📌 المصدر:`),
`narration` (the Egyptian-dialect voice-over line for that scene) and `min_duration`.
After `voiceover.py`, durations follow the voice; see `voiceover.md`.

| type | fields | use |
|---|---|---|
| `intro` | `title`, `subtitle?`, `date?` | opening, 4–6 s |
| `section` | `title`, `subtitle?` | green divider between leagues/topics, 3 s |
| `result` | `competition?`, `home`, `away`, `home_score`, `away_score`, `home_short?`, `away_short?` (1–3 letters for the team circle), `scorers_home?` [..], `scorers_away?` [..], `note?` (yellow badge) | one match, 6–8 s |
| `headline` | `title`, `body?`, `tag?` (yellow pill), `index?` (big faint number for countdowns) | one news story, 7–10 s |
| `table` | `title`, `rows` [{`pos`, `team`, `played`, `points`, `highlight?`}], `columns?` | standings top 4–6, 7–9 s |
| `stat` | `value`, `label`, `sub?` | one big number, 5 s |
| `list` | `title`, `items` [3–5 strings] | quick round-ups (Arab players corner, other results), 7–9 s |
| `outro` | `title?`, `cta?`, `handles?` | closing, 5 s |

## Timing rules

- Give viewers time to read: about **1 second per 3 Arabic words** on screen, minimum 5 s for result/headline scenes.
- If a voice-over exists, each scene's `duration` = the length of its narration line + 0.8 s.
- Scorers: `"اسم اللاعب · 23'"`; use `(ج)` after the minute for a penalty and `(ع)` for an own goal.
- On-screen Arabic text: avoid Latin words/abbreviations inside Arabic sentences (they break right-to-left order). Write «الفار» not «VAR». Latin is fine on its own (a source name, a handle).
- Keep `title` ≤ 9 words, `body` ≤ 25 words, list items ≤ 8 words.

## Rendering

```
python3 .claude/skills/youtube-video/scripts/render.py storyboard.json OUT_DIR --preview   # fast 12 fps check
python3 .claude/skills/youtube-video/scripts/render.py storyboard.json OUT_DIR             # final 25 fps
```

Outputs in OUT_DIR: `<slug>.mp4`, `<slug>-thumbnail.jpg`, `<slug>-contact-sheet.jpg` (a grid of
frames for review), `<slug>.html` (the animated page, for debugging).
Needs Python Playwright with Chromium, and ffmpeg. A 10-minute video takes roughly 10–15 minutes to render.
