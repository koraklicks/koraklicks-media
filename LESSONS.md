# Kora Klicks newsroom: lessons learned

Every run reads this file before starting work and follows it. When a run hits a new problem,
it adds one line here (date · what happened · the rule from now on). The end-of-day review
cleans the list up and turns repeated lessons into rules in the skill/agent files.
Newest first.

## Open lessons

- **13 Oct 19:20 · Scheduled runs at 15:37 and 16:47 failed with «usage limit reached» (account usage cap), so the meme short and «رقم اليوم» did not go out; the owner's chat caught them up at 19:30.** → Every run first checks today's log for tasks that should have run since the last run and left no line; if one is missing and still relevant, do it now (respect budgets). In motion_short.py too, write numbers inside Arabic sentences as words («الساعة عشرة») — Latin digits break the Lalezar lines.
- **13 Oct 19:15 · The X + IG predictions posts (19:05/19:06) stayed «PUBLISHING» in Metricool for 10+ min with no error and no publicUrl.** → Never re-send a post that is PUBLISHING (it duplicates); log it, and the next run checks the status/publicUrl before posting; if it turns ERROR, then re-post once.
- **13 Oct 12:00 · Platform rules reviewed after losing Facebook (owner request).** 12 Oct had 37 Instagram items and 9 TikToks in one day, above safe levels. → Follow `references/platform-rules.md`: daily budgets (IG 25 incl. stories, TikTok 6, YouTube 5 Shorts, X 25), spacing, hashtags (IG ≤ 5, X ≤ 2), open questions only, stop a network 24 h on any rate-limit error, no browser automation on accounts ever.
- **13 Oct 11:00 · Meta permanently disabled the owner's personal Facebook profile (the only admin of the page); the review was refused.** → **Facebook is OFF until the owner says otherwise (the page itself is closed too, checked by the owner 11:49)**: no Facebook posts of any kind, no tests, no account/page changes. Never suggest new accounts to get around the ban. Instagram may share the same Meta account centre: if an Instagram post fails with an auth/permission/connection error, stop Instagram for that run, log it and tell the owner at once (don't retry in a loop). X, TikTok, YouTube continue.
- **13 Oct 10:00 · The owner's personal Facebook profile (admin of the page) was suspended and is under appeal.** → **ALL Facebook posting is PAUSED (feed, reels AND stories)** until the owner says the appeal is accepted. Do not try Facebook at all, not even to test. Instagram, X, TikTok, YouTube continue as normal but keep a calm pace (no bursts).
- **13 Oct · YouTube long video published but the custom thumbnail failed ("Could not upload video thumbnail"; Metricool shows status ERROR although the video is live).** The channel probably isn't phone-verified for custom thumbnails. → Read `publicUrl` before calling a YouTube post failed; owner to verify the channel in YouTube Studio (Settings → Channel → Feature eligibility) and set the thumbnail by hand until then.
- **13 Oct 09:20 · WebFetch of FilGoal and Kooora was withdrawn again, and a Masrawy article URL with an Arabic slug was rejected ("url exceeds the maximum fetchable length").** → For long Arabic-slug URLs, search the headline instead of fetching; btolat.com fetch worked for today's fixture list (still confirm names/times on FilGoal/Yallakora per the playbook).
- **13 Oct 01:10 · In an unattended run a WebFetch of www.filgoal.com was withdrawn ("permission request not answered") although filgoal.com is in `.claude/settings.json`.** → Don't wait on it: switch to WebSearch with the site name in the query, or another approved service; end-of-day review checks why the allowlist was not applied.
- **13 Oct review · Several FTs were confirmed with sources that are not on the approved list** (Kooora «انتهت» for Al Nassr and Al Ahli Saudi, Football Italia for Torino, Italian local sites for Atalanta, Al-Ain News live blog, INA/واع for Al Ain) next to a FilGoal/365Scores page that still showed a live minute. All scores were right, but this bends the rule. → Until the owner decides (question in the 12 Oct review), an FT needs an approved service showing «انتهت/FT», or an official/AFC report; otherwise HOLD and keep searching with the playbook in `trusted-sources.md`.
- **13 Oct 00:20 · The repo clone started on a detached HEAD, so `git pull --rebase` failed and the first push was rejected.** → If `git pull --rebase` says "not currently on a branch", run `git fetch origin main && git checkout -B main origin/main` and cherry-pick the log commit before pushing. (Happened again in the 00:37 review run; the command works.)
- **12 Oct · The 08:47 match planner stalled ~6 h; today's live tasks were created only at 15:15.** → Every newsroom run from 12:00 checks that today's log has a "Live-coverage plan"; if not, it builds the plan itself (fixtures from FilGoal/Yallakora, create the one-off tasks) before anything else. Planner: create all match tasks in one batch right after fixtures are confirmed, before writing the log.
- **12 Oct · Unconfirmed match results from one region only (Iranian outlets for Tractor–Shamal and Gharafa–Esteghlal) stay HOLD.** Tractor–Shamal was cleared by the AFC report 1 h later; Gharafa–Esteghlal was still HOLD at 00:24. → Morning run: search the AFC report title first.
- **12 Oct 12:59 · Metricool rejected a TikTok video post: "TikTok title is required".** → Always set `tiktokData.title` (short Arabic line) on TikTok video posts. Write «الأهلي السعودي» (not «الأهلي») for Al Ahli Saudi.
- **12 Oct · YouTube roundup: in render.py (theme major) a `list` with 4–5 items or a `table` with 5 rows runs into the bottom source line.** → Max 3 items per list and 4 table rows in the long video; re-check every score from a source before reusing it from logs.
- **12 Oct 09:46 · story_short.py: the Cairo font renders digits/Latin in serif on card lines.** → Write numbers and source names in Arabic words on card lines.
- **12 Oct 01:15 · WebSearch with `allowed_domains` (4+ sports domains) was rejected by the proxy (HTTP 400).** → Don't use `allowed_domains` for sports sites; put the site name in the query.
- **11 Oct · music.py failed on a missing `soundfile` module (again 12 Oct).** → Run `pip install soundfile --break-system-packages` before music.py.
- **11 Oct · Unconfirmed stories sit in the queue all day.** → Re-list them once in the owner report; after 24 h with no official statement, propose ❌.

## Became rules (moved out of this list)
13 Oct review:
- HT late/missing on big matches — **REPEATED** (11 Oct Liverpool–City/Zamalek–Ahly, 12 Oct Al Wasl–Al Ahli Saudi not posted, Pyramids 12 min late, Al Nassr none) → `live-match` step 3: start searching at KO + 44, per-competition playbook, skip HT after HT + 10 and focus on FT; kick-off-delay check (Al Nassr 12 Oct).
- 12 Oct cached-page lessons (365Scores frozen at 90+1 and 82', `#fragment` refresh, Ahram HT search, «365scores ar football match» search, AFC report titles, Al Riyadiyah match centre, Kooora team page, FilGoal homepage strip, Italian «risultato finale», Sporza for EPL/LaLiga, So3ody = Korabia = one feed, typed URLs blocked) → `references/trusted-sources.md` → "HT/FT playbook per competition".
- `already_posted.sh` flagged CHECK lines containing "PUBLISHED" as POSTED — **REPEATED** (18:18, 18:45, 00:12) → script fixed: only plannerUrl lines and STATUS … PUBLISHED lines count.
- X text over 280 (338 at 18:35, 292 at 22:13) — **REPEATED** → `scripts/x_len.py` (≤ 250) in `x-publisher.md` and `metricool.md`.
- Story IDs used twice by parallel tasks (KK-20261012-06/10/13/15/16/17) → ID is now `KK-YYYYMMDD-HHMM` (`newsroom-rules` §6).
- No «توقعوا النتيجة» post before Pyramids, Al Nassr, Al Ahli Saudi → `live-match` step 8 + `run-newsroom` step 3: any run makes it if a big match is 1–4 h away.
- Facebook feed: paused 20 h, the 22:06 test worked, cadence (60 min / 2 per 3 h / 4–5 a day) holds → `references/metricool.md`.
- Fixture names taken from listing sites were wrong (الشرقية للدخان → إنبي, استقلال خوزستان → الاستقلال) → playbook: names/times only from FilGoal/Yallakora/club.

12 Oct review:
- Duplicates → `scripts/already_posted.sh` + `getScheduledPosts` from 00:00 (`run-newsroom` step 3, `live-match` step 3).
- Facebook rate limit → `references/metricool.md`.
- Line-ups late (twice on 11 Oct) → planner KO − 45, `live-match` step 3.
- Morning catch-up covers every Tier A result of the previous evening → `boss.md`.
- Every task logs every post with its plannerUrl → `live-match` step 3.
- Source rule: one Tier-1 FT report + one live-score service (owner 12 Oct) → `trusted-sources.md`.
- Speed rule for match data, fonts/RTL/home × away order, reading tips, story overflow → `newsroom-rules`, `creative.md`, `trusted-sources.md`, `story_short.py`.
