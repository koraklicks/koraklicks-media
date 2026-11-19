# Weekly YouTube series (owner, 19 Nov 2026)

Long (16:9) YouTube videos, one per competition per week, made by the daily task «مكتب اليوتيوب» (11:21 Cairo).
**Auto-published** when confirmed (owner 19 Nov 2026 — replaces the long-video ✅ for this series). While publishing
is paused (no publishing connector) the task stays disabled.

| # | Video | Competition data | Made when | Length |
|---|---|---|---|---|
| 1 | الدوري الإنجليزي | ESPN `eng.1` | morning after the round's last match | ~60 s |
| 2 | الدوري الإسباني | ESPN `esp.1` | same | ~60 s |
| 3 | الدوري الإيطالي | ESPN `ita.1` | same | ~60 s |
| 4 | دوري أبطال أوروبا | ESPN `uefa.champions` | Thursday after the matchday (all matches) | **2–3 min** (the longest) |
| 5 | الدوري المصري | Yallakora / FilGoal / Ahram (not on ESPN) | after the round | ~60 s |
| 6 | الدوري السعودي | ESPN `ksa.1` | after the round | ~60 s |
| 7 | الأندية المصرية في أفريقيا | ESPN `caf.champions`, `caf.confed` (Egyptian clubs only) | after the CAF matchday | ~60 s |
| 8 | الأندية السعودية في آسيا | ESPN `afc.champions` (+ AFC Champions League Two) (Saudi clubs only) | after the AFC matchday | ~60 s |
| 9 | التوقف الدولي: أهم النتايج الأوروبية والعربية | ESPN national-team scoreboards + FIFA/UEFA/AFC/CAF sites | day after the window's last match day | ~60–90 s |

Rules
- Each video at most once a week; skip a competition with no completed round (say so in one log line). In an
  international-break week, video 9 replaces the league videos. At most 3 renders per run; the rest next run.
- A round is complete when every match is FT (`scripts/espn_scores.py`) or its last scheduled day has passed;
  list postponed matches as «اتأجلت».
- Facts: final-score rule (2 sources, ESPN counts as one; `source_check.py ft`). Scorers only when 2 sources agree,
  otherwise scores only. Never invent numbers. Source line on the outro: «📌 المصدر: ...».
- Structure (~60 s): intro 4 s (fact in frame 0: the round's biggest result as the title) → one `result` scene per
  match (~5 s; biggest/Egyptian-Arab-player matches first, with a short `note`) → outro question 5 s.
  UCL (2–3 min): intro → every match (5–6 s) → «ركن العرب» list (Arab players' confirmed goals/assists) →
  table top 8 + places 9–24 summary (official uefa.com table) → outro. Chapters in the description (first 0:00,
  each ≥ 10 s).
- Look: `render.py` theme `desk` (default). Club logos: `python3 scripts/logo_library.py find "<team>"` (library in the repo) →
  `home_logo`/`away_logo` per result scene; competition logo: `find "<competition>"`. Photos (optional, intro or headline scene): ONLY
  `python3 scripts/media.py photo "<player>"` (free Wikimedia Commons) with `image_credit`; never news/agency photos.
- Music: `music.py` (owner track). Then `endcard.py VIDEO OUT --theme dark` → upload the `-yt.mp4`.
- Title (≤ 70 chars, search words first): «نتايج الدوري الإنجليزي الجولة 12 | كل الأهداف والنتايج في دقيقة».
  Description: results list, sources, question, 3–5 hashtags. Thumbnail = `render.py` thumbnail.
- Log: `logs/YYYY-MM-DD.md` line «time · YT-WEEKLY-<comp>-<round> · published|skipped|waiting · url».
