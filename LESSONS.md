# Kora Klicks newsroom: lessons learned

Every run reads this file before starting work and follows it. When a run hits a new problem,
it adds one line here (date · what happened · the rule from now on). The end-of-day review
cleans the list up and turns repeated lessons into rules in the skill/agent files.
Newest first.

## Open lessons

- **12 Oct · YouTube roundup: in render.py (theme major) a `list` with 4–5 items or a `table` with 5 rows runs into the bottom source line; an older note had Alavés–Atlético as 2-1 (it was 1-2).** → Max 3 items per list and 4 table rows in the long video (split extra results into `result` scenes); re-check every score from a source before reusing it from logs.
- **12 Oct 09:46 · Facebook FEED still blocked (ERROR 400 rate limit) after ~10 h with no feed attempt and 0 feed posts today; Stories keep working.** The block is longer than the 2 h back-off assumes. → Stop Facebook FEED/REEL tries until the owner checks the page in Meta Business Suite (Page quality / restrictions); until then Facebook gets Stories only. Also: story_short.py card lines in the Cairo font show digits/Latin in serif — write numbers and source names in Arabic words on cards.
- **12 Oct 01:15 · Three 11 Oct results (Racing 2-2 Valencia, Al Shabab 3-0 Al Taawoun, Elche 0-0 Celta) sat on HOLD for 4–7 h: wide agreement from EFE and Saudi dailies (Sabq, Al Yaum, Al Jazirah) but only one approved source; WebSearch with `allowed_domains` (4+ sports domains) was rejected by the proxy (HTTP 400).** → Don't use `allowed_domains` for sports sites; search with the site name in the query. **Owner decided 12 Oct:** one Tier-1 FT report + one of the four live-score services is enough (see trusted-sources).
- **12 Oct review · Como 0-0 Roma (17:15 and 00:20) and Crystal Palace 3-1 Forest (18:36 and 23:20) were each published twice, and the Zamalek–Ahly line-ups went out twice on X (20:02, 20:20).** A run trusted an earlier "not yet posted" note and checked Metricool only for the last few hours. → Firm rule now in `run-newsroom` step 3 and `live-match` step 3: run `scripts/already_posted.sh <teams>` and check `getScheduledPosts` from 00:00 today before every post.
- **12 Oct review · Facebook feed: 5 posts in 88 min in the morning, then every feed post and reel failed for 9 hours, so Zamalek 0-2 Ahly and Liverpool 0-3 City never reached the feed. Stories always worked.** → Firm rule now in `references/metricool.md`: ≥ 60 min between feed posts, max 2 in any 3 h, big results as a Facebook Story right away.
- **12 Oct review · Half-time was late or missing on both big matches (Liverpool–City HT never posted; Zamalek–Ahly HT 15 min late) because live pages were cached.** → `live-match` step 3: HT within 5 min; if live pages are cached, use a searched HT report (Ahram gate for Egypt, Sky/BBC report pages for England).
- **12 Oct review · Saturday's Alavés 2-1 Atlético was never posted; the morning catch-up took only 3 Saturday games.** → `boss.md`: the morning run covers every Tier A result of the previous evening that is not in the log.
- **12 Oct review · Posts made by the line-ups task (20:20–20:21) and a manual Palmer post (morning) are not in the log.** → Every task and the owner session log every post with its plannerUrl; the review counts from Metricool, not only the log.
- **11 Oct · Line-up tasks started 5 min before kick-off (Liverpool XI 5 min after kick-off, Zamalek–Ahly XIs posted by the owner by hand).** Happened twice in one day → now firm: the match planner creates line-up tasks at kick-off − 45 min (planner prompt updated 11 Oct 16:43) and `live-match` step 3 says post text on X first if late.
- **11 Oct · music.py failed on a missing `soundfile` module.** Run `pip install soundfile --break-system-packages` if music.py fails.
- **11 Oct · Unconfirmed stories sit in the queue all day (KK-20261011-04 Danilo Pereira, 13:58 → midnight).** Re-list them once in the owner report; after 24 h with no official statement, propose ❌.

## Became rules (removed from this list on 12 Oct)
- Speed rule for match data (two of Sofascore/365Scores/FilGoal/Yallakora), big results alone within 10 min, no waiting for BBC/Sky → `newsroom-rules` SKILL.md.
- Facebook rate limit → `references/metricool.md`.
- Fonts, base64 `@font-face`, Lalezar on every Arabic line, RTL score order, home × away order, look before hosting → `agents/creative.md`.
- Source reading tips (search first, cached live pages, FilGoal date, Ahram gate, Sky/club reports, long URLs, unsupported numbers like «القمة N») → `references/trusted-sources.md`.
- Story with 5 matches overflowing → fixed in `story_short.py` (compact list for 4–5 items).
