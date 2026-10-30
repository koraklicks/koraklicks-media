# Kora Klicks newsroom: lessons learned

Every run reads this file before starting work and follows it. When a run hits a new problem,
it adds one line here (date · what happened · the rule from now on). The end-of-day review
cleans the list up and turns repeated lessons into rules in the skill/agent files.
Newest first.

## Open lessons

- **30 Oct night results · FilGoal /matches and FotMob match pages were cached pre-match (Ittihad Alexandria 0-0 stayed Yallakora-only); FilGoal's finished list did confirm the SPL FTs.** → Night results: ESPN API first, FilGoal /matches for SPL second source, Goal article via WebFetch for others; Egyptian-league FT with only Yallakora = HOLD.

- **30 Oct growth review · the 10:00 «ماتشات النهارده» went to TikTok as VIDEO all week (8 posts, avg 172) while photo posts averaged 310; TikTok Creator Academy page is robots-blocked for WebFetch.** → 10:00 fixtures task: TikTok = photo post (cover + one slide per match), video only to Reel/Short; TikTok monetization thresholds: owner checks in the app (Creator tools) until an official page is readable.

- **30 Oct · WebFetch of btolat/dostor/masrawy listings works but they are not approved sources; Yallakora/FilGoal article URLs are too long, yet `yallakora.com/matches-center?date=MM%2FDD%2FYYYY` and the FilGoal championship page are short and readable.** → Fixtures task: confirm kick-offs with the Yallakora date URL + ESPN API/club site; use btolat/dostor only to find the slate. Egypt is UTC+2 from 30 Oct (Cairo = UTC+2).

- **30 Oct · Nassr 5-3 stayed ESPN-only for 3 h in standard/Arabic searches; an English search limited to allowed_domains goal.com/skysports.com returned Goal's player-ratings page with the full score.** → For SPL/European FTs with one source, run an English `allowed_domains` search (goal.com, skysports.com, beinsports.com) with "<team> player ratings"/"report" before giving up; WebFetch the Goal page to read the score.

- **29 Oct · Metricool createScheduledPost with Africa/Cairo scheduled everything +1 h (22:38 → 23:38) on the night Egypt's DST ends; the same minute given in timezone UTC landed correctly.** → Until 30 Oct (and re-check after any DST change): send publicationDate in UTC (Cairo−3 h until midnight 29→30 Oct, then Cairo−2 h) and check the returned Cairo time before moving on; fix with updateScheduledPost.

- **29 Oct · Modern×Ahly line-ups task fired at KO−20 (not −70); FilGoal/Yallakora article URLs are too long for WebFetch and short FilGoal URLs need a permission prompt, so only headlines were readable.** → Line-ups task: search with allowed_domains filgoal.com/yallakora.com first; fetch the FilGoal related-link URL list from any short FilGoal page; if only headlines are readable, post only the facts both headlines show; proofread text before createScheduledPost (a garbled line was caught and fixed before it published).

- **29 Oct · the 01:15 late-FT task left no log line or post again (Liverpool/City pens, Genoa, Monza went out at 09:30).** → 09:xx cycle checks late FTs first (ESPN API + extended search "<teams> result"); Sky titles say "fifth round", ESPN says "quarter-finals" for the same EFL Cup tie, so leave the round out.

- **28 Oct review · Liverpool XI 21:50, Zamalek FT 22:05 and Serie A early FT 22:40 tasks left no log line and no post; the 4 results went out at 00:01 (~2 h late).** → Watchdog 09:37 checks the previous evening's XI/FT task logs and catches up; an FT task that cannot finish must still write a «HOLD/NOT RUN» line.

- **28 Oct · night results task prompt says «short → TikTok», but the viral rule says TikTok = photo post.** → Follow the rule: TikTok gets story+scene JPGs (5 slides, with IG carousel); the video goes to IG Reel + YT Short only.

- **28 Oct · «مين أحسن؟» player-stat comparison: ESPN stats page/API returned nothing readable, FotMob alone is one source.** → Wednesday series: pick the pair AFTER finding two approved sources (ESPN/Sky/beIN article with the numbers); otherwise skip with one line.

- **28 Oct · late-night FTs (KO ≥ 22:45) stayed HOLD at 01:15 because standard searches returned old pages; at 09:10 a single extended search "<teams> <competition> result report" gave Sky/beIN/ESPN titles at once.** → In the 01:xx cycle use extended mode first for late FTs; Sky title and URL can disagree on penalty score, so leave the shootout score out.

- **27 Oct review · Night results 00:05 went to TikTok as VIDEO (IG Reel + TikTok in one post) against the photo rule (REPEATED 22 Oct); Dortmund 2-2 Bremen / Fleetwood 1-1 Arsenal (22:45/23:00 KO) were still live at 23:55 so no FT; the 26 Oct review claimed EXPIRED lines that were not in the repo.** → Results = separate posts: TikTok photo slides, Reel/Short video elsewhere; on cup nights with KO ≥ 22:45 the 01:07 cycle posts the FTs; after writing EXPIRED/log lines, `git diff --stat` must show them before the push.

- **27 Oct · night results at 23:50 Cairo: Roma, Dortmund, Torino, Arsenal still live; Abha 0-1 Faisaly had only ESPN (FilGoal /matches cached pre-match); ESPN vs FotMob disagreed on the Sassuolo 7' scorer.** → Results task: ESPN API first, FotMob page fetch is the fastest 2nd source; leave out scorers that disagree.

- **26 Oct · night results: Qadsiah 1-1 Sadd had only ESPN API + Arab News (not an approved FT source); Goal/beIN title searches gave the 2nd source for the other three.** → Search «<teams> <score> Goal beIN» extended; a match with no 2nd approved source is left out and listed as HOLD.

- **26 Oct · ليلة العرب: Ahram English/beIN/Goal pages blocked or stale, 365Scores cached pre-match; Salah role in Rizespor 3-4 Trabzonspor conflicted (Ahram "helps", Fanzword "blank").** → Rabia/En-Nesyri confirmed via ESPN API + Ahram Arabic title / le360 page (source_check PASS); a player whose contribution sources disagree is left out; check ESPN API first.
- **26 Oct (owner) · The Clasico (Barça 1-2 Real, 25 Oct 23:00) was never posted: PLAN named «Clasico+late FT 01:00» but no task existed; the 23:47 night task ran while it was live; the 01:12 cycle's standard searches returned only old pages.** → Every BIG match in PLAN must have its own FT task in list_triggers. For FT results run `scripts/espn_scores.py` first (26 Oct: ESPN allowed); otherwise WebSearch **mode "extended"** with an English query «<home> vs <away> <Month D, YYYY> final score report»: it returned the ESPN «Final Score» title + the club's official report at once when standard search returned only old pages.

- **26 Oct · results task: story_short.py also writes a *-short.mp4 with the same slug as motion_short.py (overwritten, harmless); WebSearch gives titles only, the FilGoal /matches page listed all finished scores in one fetch.** → Night results: fetch filgoal.com/matches first for the slate, then pair each score with an ESPN/Sky title via "<score> report Sky Sports ESPN" extended search.
- **25 Oct · Ahly×Kitara FT task (21:10) produced no post/log; cycle at 23:14 found the 4-0 confirmed (club site + Dostor) and published it 2 h late; also story_short title «الأهلي في المجموعات» wrapped to 2 lines.** → Cycles after a planned FT task: check its match first (log + Metricool); story_short titles ≤ 14 chars.
- **25 Oct · story_short.py: a subtitle + 3-item results spec overlaps the first row, and «أهم نتايج الجولة 8» wraps to 2 lines.** → Results shorts: no subtitle, title ≤ 14 chars («نتايج الجولة 8»); check the story.jpg once before rendering the endcard.
- **25 Oct · 24 Oct 23:55 HOLDs (Arsenal 2-0 Everton, Zamalek 1-0 APR) were OLD results: search titles were Sky 1 Mar 2015 and CAF 16 Oct first leg.** → A search-title score is never an FT: fetch the page and check the match date is today and the season is 2026/27 (CAF CL 2nd-leg ties have a first leg a week earlier) before treating it as a HOLD or posting.
- **23 Oct growth review · 2 of 3 weekly experiments never ran (0 IG carousels, 0 YT 10:00 round-up Shorts) and 22 Oct TikTok results went out as VIDEO (8 views) against the photo rule.** → Planner/09:07 cycle: check playbook §7 each morning; TikTok = photo posts only (except round-up); round-up Short uses the owner's 22 Oct 2-of-list FT rule.
- **22 Oct · Noon list/PLAN had «Ahli SA×Khaleej 21:00 today» but FotMob + ESPN list it Fri 23 Oct 18:00 UTC.** → Night results task: check each planned match's date on FotMob/ESPN before expecting an FT; a match not played today is not a HOLD.

- **22 Oct · UCL table card blocked: uefa.com standings page is script-rendered, WebFetch gets no rows.** → Owner to decide if two agreeing outlets (Sky Sports table + NBC Sports) may replace uefa.com for the table card; until then post nothing and notify.
- **22 Oct 00:40 · UCL MD3 day 2 FT: 90 min after the whistle only 2 of 9 results had an approved FT (uefa.com pages not updated until morning; Sky/ESPN/Fox pages cached on live minutes; search showed only titles).** → For the 00:20 package, fetch each club's report (`sofascore.com/news`, Sky `/report/` URL, beIN «ALL GOALS») instead of live pages; a title alone is one source; whatever is still HOLD at 01:00 goes to the 09:07 catch-up, never a second round-up the same night.

- **21 Oct review · UCL MD3 day 1 (PSG×Barça, Liverpool×Villarreal, City×AEK, Stuttgart×Atlético, 22:00) got only the noon short: the 10:51 UCL desk run hung (PENDING, no log line, no tasks); 19:15/21:15/23:10 cycles wrote «left to live/FT tasks» that never existed.** → `run-newsroom` 2b + `ucl.md` backstop: from 11:07 the cycle runs `missing_runs.py` (now checks UCL plan/«ليلة الأبطال») and `list_triggers`; no `UCL plan` line on a matchday → the cycle builds the UCL tasks. MD3 day 2 (Wed 21 Oct, Bayern×Arsenal) is the test.
- **21 Oct review · PLAN (13:25) said «tasks: SPL FT round-up 00:30» but no task was created (list_triggers empty for 20 Oct); slate came from fbref «times unverified».** → A task named in PLAN must be seen in `list_triggers`; slate from FilGoal/Yallakora/365Scores league page, never fbref alone. Night results covered SPL by luck.
- **21 Oct review · Home/away doubt: PLAN «Ettifaq×Ittihad», night short «الاتحاد 4-1 الاتفاق».** → Morning cycle: check order + score on the 365Scores SPL league page; if wrong, «تصحيح» on IG/TikTok/YT.
- **19–21 Oct · Owner track `.claude/assets/music/house.mp3` still missing (only README) — 3rd review in a row; every short since 18 Oct used code-made music.** → Owner to upload; tasks keep the music.py fallback, never download from suno.


- **20 Oct review · Trabzonspor 2-0 Beşiktaş (19 Oct 20:00, Salah starred; AA + Hürriyet + Fotomaç) got NOTHING: not in the noon fixtures, «ليلة العرب» said «no Arab player found».** → `coverage.md` «Arab stars' clubs» list (Salah → Trabzonspor) is checked every day by planner, noon and «ليلة العرب».
- **20 Oct review · Al Fayha 2-3 Al Ahli Saudi (FT ≈20:00, Fox «Final Score») never searched; the 23:12 cycle looked only at Spurs×Coventry and Hilal×Hazm.** → A cycle with no PLAN still checks every match from the noon story that has passed FT+30, oldest first.
- **20 Oct review · Night results task (23:47) ran while Spurs×Coventry (22:00 KO) was still live → «نتايج النهارده» skipped (REPEATED 18 Oct, owner proposal pending).** → Until the owner moves it: the 01:07 cycle publishes the late FTs + the results story if 23:47 skipped.
- **19 Oct review · Noon fixtures post and results reel had empty firstCommentText; Real XI feed post too.** → Every feed post AND reel gets the open question as `firstCommentText` (growth-playbook §0.3), no exceptions.

- **17 Oct review · APR×Zamalek (CAF CC, 16 Oct) never published; Qadsiah 2-1 Abha held 43 h (confirmed only on 18 Oct by 365Scores league page + ESPN).** → Any Al Ahly/Zamalek/Pyramids result missing after FT+3 h: search «<club> result report» in English + «الزمالك <opponent> نتيجة» extended mode, and the club's own site; never let it pass the next morning.
- **17 Oct · ليلة العرب skipped with one confirmed item (Ezzalzouli goal).** → One confirmed Arab goal/assist is enough for an X post + IG story (no short); short only with ≥ 2 rows.
- **18 Oct 11:42 · EGY+SPL video: the 14 Oct edition was lost and no video existed for 4 days; 365Scores league page (`365scores.com/en-us/football/league/saudi-league-649`) gave all SPL MD9 scores + top-7 table in one fetch, where match pages were stale.** → For SPL round results fetch that 365Scores league page first, then pair each score with an ESPN «Final Score» or Goal title.


- **16 Oct 21:08 · FT round-up: Pyramids 1-0 confirmed by Ahram Online + Goal English pages (found via «<teams> result report» English search, 2 h after FT); Qadsiah 2-1 Abha only ESPN title + non-approved sites; APR×Zamalek nothing indexed.** → For CAF/Saudi FTs search English «<home> <away> result report <date>» extended mode; Ahram Online/Goal pairs count as 2 Tier-1.
- **15 Oct · Salah goal+assist (KuPS 2-4 Trabzonspor) and 3 SPL results held all night: approved live services were stale/unreadable, so nothing was published.** → After FT+60, search for Tier-1 match reports by name (beIN Sports, Goal, ESPN, Sky) instead of only live-score pages; beIN + Goal reports = confirmed. Egyptian player news never waits for the next day.
- **15 Oct 21:50 · كوبس×طرابزون FT (≈21:40): only Fanatik live blog showed FT 4-2; Sky/FotMob/ESPN/uefa.com/Sofascore pages stayed stale (61'/84') 10+ min after the whistle; WebSearch index lagged ~15 min → HOLD again.** → For Turkish clubs search «<club> maç sonucu» + fetch the club's own post-match page (trabzonspor.org.tr) and NTV/aspor FT report; owner question (3rd time today): may Fanatik/NTV/Hürriyet/Habertürk count as Tier 1 for Turkish-club matches?

- **15 Oct 20:45 · كوبس×طرابزون HT 0-2: only 365Scores team page showed «Halftime 0-2» (no scorers); Sofascore cached at 37' (0-1, Onuachu 3' assist Salah); the 44' Salah goal only on Turkish live blogs (Hürriyet, T24, 61saat, Habertürk) → HT HOLD, 2nd approved source missing.** → For Turkish clubs the 365Scores team «matches» page updates at HT fastest; Sofascore needs a 2nd refresh. Owner question (repeat of 19:20): may Hürriyet/Habertürk/NTV/TRT Spor count as Tier 1 for Turkish-club matches?

- **15 Oct 20:25 · SPL round-up: 3 matches, only 1 FT on a single approved source (Sofascore); 365Scores/ESPN/Sofascore pages for the other two were pre-match/HT snapshots ~2 h after FT; no Saudi Tier-1 report (SPA/Al Riyadiyah) found.** → Owner question: may one approved service (Sofascore FT + scorers) alone confirm Saudi league FTs? Until then Saudi round-ups need Sofascore/365Scores/Al Riyadiyah FT pair, else HOLD.

- **15 Oct 19:20 · كوبس×طرابزون XI: out 18:34 on 5 Turkish outlets (Salah starter) but Sofascore/365Scores/FilGoal/Yallakora pages had no XI in search/fetch, club site + uefa.com lineups URL blocked → HOLD.** → For Turkish clubs search «<club> ilk 11 belli oldu» to find the XI fast, then look for a second approved source; if none by KO − 25, drafts to owner. Owner question: may dunya.com / haber61 / TRT Spor count as Tier 1 for line-ups?

- **15 Oct 11:00 · uefa.com/…/standings WebFetch withdrawn (permission unanswered), so no table card.** → Add uefa.com standings to `.claude/settings.json` allowlist; until then table card HOLD, never self-computed.

- **15 Oct review · ACL2 Arab-clubs round-up (fired 23:10) left no log line and its run still showed PENDING the next morning; 6 Arab-club matches got no post.** → Every round-up task writes one log line in its first 5 min («started …») and one at the end, even if nothing is found; the review checks `last_run` of every one-off and lists stuck ones.
- **15 Oct review · TikTok near zero for the 2nd day: 4 videos on 14 Oct = 11 views in total (13 Oct: 4 videos ≈ 23).** → Condition from the 14 Oct lesson met: owner told at once. Keep ≤ 4 TikToks/day, each with its own facts and angle (no two shorts of the same score); proposal to the owner: 2/day until he checks TikTok Account status.
- **15 Oct review · Usage limit again (REPEATED 13 Oct): no runs 10:12–14:20, so the noon fixtures story (14:35), the UCL desk (10:51) and the EGY+SPL video (12:00) were lost or late.** → Token economy (14 Oct 14:28) is the fix; the first run after a gap does the noon story first if it is still before 16:00.
- **15 Oct 00:20 · Typed «17 goals» in a TikTok caption; real total was 22 (6+7+9).** → Add up goal totals in code (python) before writing them in a caption.
- **14 Oct 21:35 · City×PSG XI was on mancity.com (18:45) but search only showed old fixtures.** → For line-ups fetch the club's match-preview page and follow its «team news» link; for the other club search «<club> XI» on realmadrid.com/asroma.com. Only Yahoo/SB Nation/voetbalwedden for Roma×Real → HOLD.
- **14 Oct 16:05 · ACLE East 13:00 KO: 2 h after FT still no AFC report; Sofascore/365Scores/ESPN pages fetched stale (pre-match), only search titles showed FT (365Scores «5 - 1 … Match Report», ESPN «Final Score»).** → For Asian midday matches use search-result titles of approved/Tier-1 pages as the FT evidence (state it in the log); owner question: may JP/KR national outlets (Football Channel, Gekisaka, Yonhap) count as Tier 1 for ACLE East?
- **13 Oct 23:50 · «نتايج النهارده»: YouTube was already at 5/5 Shorts, so the night results short went to 01:45 next day.** → Night results short: schedule it on the next Cairo day (≈ 01:45, ≥ 60 min after «ليلة الأبطال»); the story still goes right away. Owner proposal in the 13 Oct review: keep one Short slot free for the night.
- **13 Oct 23:50 · ACLE round-up: search results mixed in last season's identical fixture (AFC report «MD2: Al Ittihad 0-1 Shabab Al Ahli» = 30 Sep 2025).** → For a repeat fixture, check the date on the AFC report/match page before using it. Al-Ahram gate reports ACLE matches with Arab clubs ~20 min after FT.
- **13 Oct 22:40 · EGY round-up: the 20:00 results were on Yallakora FT articles within 15 min, but the Tier-1 Ahram report came only at 22:43 and was found at 23:52 → those two results went out ~2 h after FT.** → Round-up tasks for late EGY matches: run at last KO + 125 and search «بوابة الأهرام الجولة <n> <teams>» first and again every 10 min; publish the confirmed part and list the rest for the owner. Owner question pending: may Yallakora FT + Vetogate/btolat confirm EGY scores?
- **13 Oct 19:30 · Owner decision: Egyptian league and ACLE results go out ONCE per competition, after its last match of the day** (one X post + one IG story with all results). → Planner/hourly runs: no HT/line-ups/per-match tasks for EGY or ACLE; one round-up task per competition at last KO + 115–125 min. UCL keeps its own live plan (`ucl.md`).
- **13 Oct 19:20 · Scheduled runs at 15:37 and 16:47 failed with «usage limit reached»; hourly runs 12:10–18:10 left no line, so the live plan only came at 19:13 (REPEATED: plan late on 12 Oct too).** → Every run first checks today's log for tasks that should have run since the last run and left no line; if one is missing and still relevant, do it now (respect budgets). The match planner must build the plan before 12:00; a run that finds no plan builds it before anything else. Numbers inside Arabic sentences in motion_short.py are written as words.
- **13 Oct 19:15 · Metricool posts stayed «PUBLISHING» for 10+ min with no error (they published later).** → Never re-send a post that is PUBLISHING (it duplicates); the next run checks the status/publicUrl; if it turns ERROR, re-post once.
- **13 Oct 11:00 · Meta permanently disabled the owner's personal Facebook profile (the page's only admin); the page is closed.** → **Facebook is OFF until the owner says otherwise**: no posts, tests or account/page changes; never suggest new accounts to get around the ban. If an Instagram post fails with an auth/permission/connection error, stop Instagram for that run and tell the owner at once (no retry loop). Platform rules: `references/platform-rules.md`.
- **13 Oct · YouTube long video published but the custom thumbnail failed (status ERROR, video live).** → Read `publicUrl` before calling a YouTube post failed; owner to verify the channel in YouTube Studio (Settings → Channel → Feature eligibility).
- **13 Oct · WebFetch of FilGoal/Kooora/Yallakora/btolat/Sky "withdrawn (permission request not answered)" in unattended runs, even for allowlisted domains (REPEATED 13 Oct 01:10, 09:20, 19:15, 23:56); long Arabic-slug URLs are rejected.** → Don't wait: switch to WebSearch with the site name in the query or the next source in the playbook. 14 Oct review added btolat, match.uefa.com, sporza, kooora to `.claude/settings.json`.
- **13 Oct · The repo clone starts on a detached HEAD (REPEATED every review run).** → Run `git fetch origin main && git checkout -B main origin/main` first, then pull/rebase.
- **20 Oct 01:20 · render.py --preview of a 3:19 video took >10 min (shell timeout).** → Long renders with nohup in the background; check layout with a scene-screenshot sheet (`seek(t)`).
- **12 Oct · Metricool: "TikTok title is required".** → Always set `tiktokData.title`.
- **12 Oct · Unconfirmed match results from one region only (Iranian outlets) stay HOLD.** → Morning run: search the AFC report title first.
- **12 Oct · render.py (theme major): a list with 4–5 items or a table with 5 rows hits the source line.** → Max 3 list items / 4 table rows; re-check every score from a source before reusing it from logs.
- **12 Oct · Cairo font renders digits/Latin in serif on card lines.** → Numbers and source names in Arabic words on card lines.
- **12 Oct · WebSearch with `allowed_domains` (4+ sports domains) → HTTP 400.** → Put the site name in the query instead.
- **11 Oct · music.py needs `soundfile`.** → `pip install soundfile --break-system-packages` (setup_session.sh does it).
- **11 Oct · Unconfirmed stories sit in the queue all day.** → Re-list them once in the owner report; after 24 h with no official statement, propose ❌.

## Became rules (moved out of this list)
21 Oct review (day 20 Oct):
- Sources not on the list used for results — **REPEATED (12–13 Oct, 20 Oct ×6: btolat/101greatgoals/allfootballapp, ajel/ysscores/hihi2, AA/Hürriyet/Takvim, KingFut/Anews)** → new `scripts/source_check.py`, required in `newsroom-rules` §1.
- «الأهلي» for Al Ahli Saudi — **REPEATED (12 Oct, 20 Oct 09:25 X)** → `newsroom-rules` §1.
- Planner 08:47 dead again (ABANDONED 20 Oct; PLAN only at 13:25, after the noon story) — **REPEATED 7th day** → still owner proposal b (drop it; 09:07 cycle owns the plan).
20 Oct review (day 19 Oct):
- Live plan missing — **REPEATED 6th time (12, 13, 16, 17, 18, 19 Oct)**: 09:20/11:12 deferred to a «still running» planner, 13:15 «noon ran», 19:12/21:09 STARTED and died → `run-newsroom` 2b «No excuses» (PLAN slate line pushed before tasks) + `missing_runs.py` prints STUCK cycles.
- Partial slate — **REPEATED (17, 18, 19 Oct)**: noon had 3 matches; Salah's Trabzonspor×Beşiktaş, Getafe×Rayo, Monza×Cagliari, Parma×Torino missing → `coverage.md` «Arab stars' clubs» + growth-playbook §0.2.
- 19 Oct review lines «Real FT re-arm» and «PL XI» → already rules in `live-match` (moved here).
19 Oct review (day 18 Oct):
- Partial slate — **REPEATED (17, 18 Oct)**: plan/noon/night covered 4 of 12 Tier A matches (Juventus×Lazio, Brighton×Palace, Bournemouth×Sunderland + 5 Liga/Serie A missed) → `run-newsroom` 2b: full-slate PLAN line from a full schedule page; noon + night tasks read it.
- Silent cycles — **REPEATED (13, 16, 17, 18 Oct)**: 13:07, 15:07, 17:07, 19:07 left no line on 18 Oct; the plan tasks were created ~14:30 with no PLAN line → `run-newsroom` 2b (log + push a «started» line first) + `scripts/missing_runs.py` in every review.
- FT slow / HOLD-and-stop — **REPEATED (12–15 Oct, 18 Oct)** → `live-match`: FT re-arm +25 min, Tier-1 title search order.
18 Oct review (day 17 Oct):
- Live plan missing — **REPEATED (12, 13, 16, 17, 18 Oct)**; cycles read «From 12:00» and on 17 Oct skipped it as «only evening matches left» → `run-newsroom` step 2b: any cycle from 09:00 builds it if `PLAN` is missing, never skipped.
15 Oct review (day 14 Oct):
- Line-ups late/missing — **REPEATED (11, 13, 14 Oct)**: 14 Oct lean plan fired at KO − 45, Real's XI never posted → `ucl.md`: task at KO − 70, never later than KO − 60; planners copy times from the table.
- «ليلة الأبطال» at 00:07 again (fixed to 00:20 on 13 Oct) and parallel with the FT-big task → `ucl.md`: planners copy the table; one short per match per night.
- Spacing after a reschedule — **REPEATED (13 Oct)**: YT Shorts 01:03 and 01:20 → `ucl.md`: re-run `budget_check.py` for every network of a moved package.
- LASK 3-6 Liverpool confirmed 22:15 but «no card tool found», posted 00:38 → `ucl.md` «Card tools» + «post in the same run».
- 6 of 9 UCL 22:00/19:45 results left HOLD overnight (pages stale) — **REPEATED (FT slow 12, 13 Oct)** → `ucl.md`: Sofascore «Full time» + ESPN «Final Score», date in the query, next-morning catch-up row.
- TikTok views lesson (14 Oct review) → replaced by the 15 Oct line above.
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
