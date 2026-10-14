# Kora Klicks newsroom: lessons learned

Every run reads this file before starting work and follows it. When a run hits a new problem,
it adds one line here (date · what happened · the rule from now on). The end-of-day review
cleans the list up and turns repeated lessons into rules in the skill/agent files.
Newest first.

## Open lessons

- **14 Oct 16:05 · ACLE East 13:00 KO: 2 h after FT still no AFC report; Sofascore/365Scores/ESPN pages fetched stale (pre-match), only search titles showed FT (365Scores «5 - 1 … Match Report», ESPN «Final Score»).** → For Asian midday matches use search-result titles of approved/Tier-1 pages as the FT evidence (state it in the log); owner question: may JP/KR national outlets (Football Channel, Gekisaka, Yonhap) count as Tier 1 for ACLE East?
- **14 Oct review · TikTok views collapsed on 13 Oct: 0, 1, 0 and 22 views on the four videos (Metricool posts), vs 899 views on 11 Oct; Instagram reels on the same content got 37–102.** → Not a rule yet: keep TikTok at ≤ 4 videos/day, each with its own facts and angle (no near-identical result shorts the same day), and the owner checks the TikTok app inbox/Account status for a warning. If 14 Oct is also near zero, tell the owner at once.
- **13 Oct 23:50 · «نتايج النهارده»: YouTube was already at 5/5 Shorts, so the night results short went to 01:45 next day.** → Night results short: schedule it on the next Cairo day (≈ 01:45, ≥ 60 min after «ليلة الأبطال»); the story still goes right away. Owner proposal in the 13 Oct review: keep one Short slot free for the night.
- **13 Oct 23:50 · ACLE round-up: search results mixed in last season's identical fixture (AFC report «MD2: Al Ittihad 0-1 Shabab Al Ahli» = 30 Sep 2025).** → For a repeat fixture, check the date on the AFC report/match page before using it. Al-Ahram gate reports ACLE matches with Arab clubs ~20 min after FT.
- **13 Oct 22:40 · EGY round-up: the 20:00 results were on Yallakora FT articles within 15 min, but the Tier-1 Ahram report came only at 22:43 and was found at 23:52 → those two results went out ~2 h after FT.** → Round-up tasks for late EGY matches: run at last KO + 125 and search «بوابة الأهرام الجولة <n> <teams>» first and again every 10 min; publish the confirmed part and list the rest for the owner. Owner question pending: may Yallakora FT + Vetogate/btolat confirm EGY scores?
- **13 Oct 19:30 · Owner decision: Egyptian league and ACLE results go out ONCE per competition, after its last match of the day** (one X post + one IG story with all results). → Planner/hourly runs: no HT/line-ups/per-match tasks for EGY or ACLE; one round-up task per competition at last KO + 115–125 min. UCL keeps its own live plan (`ucl.md`).
- **13 Oct 19:20 · Scheduled runs at 15:37 and 16:47 failed with «usage limit reached»; hourly runs 12:10–18:10 left no line, so the live plan only came at 19:13 (REPEATED: plan late on 12 Oct too).** → Every run first checks today's log for tasks that should have run since the last run and left no line; if one is missing and still relevant, do it now (respect budgets). The match planner must build the plan before 12:00; a run that finds no plan builds it before anything else. Numbers inside Arabic sentences in motion_short.py are written as words.
- **13 Oct 19:15 · Metricool posts stayed «PUBLISHING» for 10+ min with no error (they published later).** → Never re-send a post that is PUBLISHING (it duplicates); the next run checks the status/publicUrl; if it turns ERROR, re-post once.
- **13 Oct 11:00 · Meta permanently disabled the owner's personal Facebook profile (the page's only admin); the page is closed.** → **Facebook is OFF until the owner says otherwise**: no posts, tests or account/page changes; never suggest new accounts to get around the ban. If an Instagram post fails with an auth/permission/connection error, stop Instagram for that run and tell the owner at once (no retry loop). Platform rules: `references/platform-rules.md`.
- **13 Oct · YouTube long video published but the custom thumbnail failed (status ERROR, video live).** → Read `publicUrl` before calling a YouTube post failed; owner to verify the channel in YouTube Studio (Settings → Channel → Feature eligibility).
- **13 Oct · WebFetch of FilGoal/Kooora/Yallakora/btolat/Sky "withdrawn (permission request not answered)" in unattended runs, even for allowlisted domains (REPEATED 13 Oct 01:10, 09:20, 19:15, 23:56); long Arabic-slug URLs are rejected.** → Don't wait: switch to WebSearch with the site name in the query or the next source in the playbook. 14 Oct review added btolat, match.uefa.com, sporza, kooora to `.claude/settings.json`.
- **13 Oct review (still open) · FTs confirmed with non-approved sources on 12 Oct.** → Until the owner decides, an FT needs an approved service showing «انتهت/FT», or an official/AFC report, plus a Tier-1 report; otherwise HOLD.
- **13 Oct · The repo clone starts on a detached HEAD (REPEATED every review run).** → Run `git fetch origin main && git checkout -B main origin/main` first, then pull/rebase.
- **12 Oct · Unconfirmed match results from one region only (Iranian outlets) stay HOLD.** → Morning run: search the AFC report title first.
- **12 Oct · Metricool: "TikTok title is required".** → Always set `tiktokData.title`. Write «الأهلي السعودي» (not «الأهلي») for Al Ahli Saudi.
- **12 Oct · render.py (theme major): a list with 4–5 items or a table with 5 rows hits the source line.** → Max 3 list items / 4 table rows; re-check every score from a source before reusing it from logs.
- **12 Oct · Cairo font renders digits/Latin in serif on card lines.** → Numbers and source names in Arabic words on card lines.
- **12 Oct · WebSearch with `allowed_domains` (4+ sports domains) → HTTP 400.** → Put the site name in the query instead.
- **11 Oct · music.py needs `soundfile`.** → `pip install soundfile --break-system-packages` (setup_session.sh does it).
- **11 Oct · Unconfirmed stories sit in the queue all day.** → Re-list them once in the owner report; after 24 h with no official statement, propose ❌.

## Became rules (moved out of this list)
14 Oct review (day 13 Oct):
- HT missed for all three big UCL matches — **REPEATED (11, 12, 13 Oct)** → `live-match` step 3 + `ucl.md`: HT task fires at KO + 40, running goal note from KO, live-blog searches.
- Line-ups: only Barça's XI out, Atlético–United and Arsenal–Lille never posted — **REPEATED (11 Oct late)** → `ucl.md` + `live-match`: line-ups task KO − 70, search «<club> XI» for the club post, by KO − 25 drafts to the owner + notification.
- UCL FT slow (Galatasaray–Barça, Arsenal–Lille ~45 min) — **REPEATED (12 Oct FTs slow)** → `ucl.md` KO + 110 row: Yallakora tour-fixtures/105 + Sky scores page first, «sofascore news», 365Scores en-uk report; ignore Yallakora KO times.
- Same scores posted twice on X (00:28 «ليلة الأبطال» round-up, then 00:38 Galatasaray–Barça and 00:48 Arsenal–Lille) → `live-match` step 3 «No repeated scores on X», `ucl.md` 00:20 row (round-up reads the FT posts first; re-checks then add IG stories only).
- IG feed→reel gaps of 25/14/28 min and 5 IG stories in 47 min (23:54–00:41) from parallel tasks → new `scripts/budget_check.py`, required in `platform-rules.md` §2 and `metricool.md`.
- «ليلة الأبطال» at 00:07 ran before the 22:00 FTs were confirmed → moved to 00:20 in `ucl.md`.

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
