# UEFA Champions League desk (owner request 13 Oct 2026: «تغطية أحسن وأقوى لدوري أبطال أوروبا»)

On UCL matchdays the Champions League is covered like a **Tier A** league: every match gets at least its result,
the big ones get the full live package, and the night ends with a «ليلة الأبطال» story + short.
The daily **«دوري الأبطال · ديسك»** task (10:51 Cairo) plans each matchday; the match planner (08:47) leaves UCL to it.
**Backstop (review 21 Oct):** on 20 Oct (MD3 day 1) the desk run hung (PENDING) and left no line, so the night had no coverage.
If there is no `UCL plan` line in today's log by the 11:07 cycle on a matchday, that cycle builds the UCL tasks itself (`run-newsroom` 2b).

## Calendar 2026/27 (official: uefa.com)

| Stage | Dates | Notes |
|---|---|---|
| League phase MD1 | 8–10 Sep 2026 | done |
| MD2 | **Tue 13 + Wed 14 Oct** | |
| MD3 | Tue 20 + Wed 21 Oct | PSG × Barcelona, Bayern × Arsenal |
| MD4 | Tue 3 + Wed 4 Nov | Atlético × Bayern, Barcelona × Aston Villa |
| MD5 | 24–25 Nov | |
| MD6 | 8–9 Dec | |
| MD7 | 19–20 Jan 2027 | table decides top 8 / play-offs |
| MD8 | Wed 27 Jan 2027 | all 18 matches at the same time |
| Knockout play-offs, R16, QF, SF, final | Feb–May/Jun 2027 | treat every knockout tie as BIG |

Full fixtures per matchday: uefa.com «2026/27 Champions League: All the league phase fixtures and results».
Europa League / Conference League (Thursdays): cover matches with Egyptian or Arab players and heavyweight clubs.

## Kick-off times in Cairo

UEFA lists 18:45 and 21:00 CET/CEST → **19:45 and 22:00 Cairo** (Cairo is 1 h ahead of Central Europe).
Careful in the last week of October: Europe leaves summer time on Sun 25 Oct 2026, Egypt on the last Thursday of October,
so between those dates the gap is 2 h. Always convert from UTC when in doubt. No UCL matchday falls in that week this season.

## Sources

- **uefa.com match pages and official match reports are OFFICIAL**: one of them confirms a score, scorer, line-up or table alone.
- Live data: the four approved services (Sofascore, 365Scores, FilGoal, Yallakora) as in `trusted-sources.md`.
- UCL search tips: «<home> <away> Champions League full time», «<home> <away> report uefa.com», Arabic «نتيجة مباراة X و Y دوري الأبطال».
- League-phase table: uefa.com standings page only (never compute it yourself from partial results).

## What is BIG in the UCL (full live: line-ups, HT, FT + result short)

1. Two heavyweights meet (Real Madrid, Barcelona, Man City, Liverpool, Arsenal, Man United, Chelsea, Bayern, PSG, Inter, Milan,
   Juventus, Napoli, Atlético, Dortmund).
2. An **Egyptian** player is in the squad (always), or a top Arab player is expected to start (Hakimi, Brahim Díaz, Mazraoui, Saibari, Aït-Nouri…).
3. Every knockout match; MD7–MD8 matches that decide the top 8.
Every other UCL match: in the slot round-up and the «ليلة الأبطال» story.

## Arab players to check each matchday

From ihata.ma (8 Sep 2026) and 365Scores (26 Aug 2026). **Re-check squads, injuries and transfers every matchday**; this list goes stale.
Hakimi (PSG) · Brahim Díaz (Real Madrid) · Mazraoui (Man United) · Saibari (Bayern) · Aït-Nouri (Man City) · Bouaddi (Man City) ·
Hamza Abdelkarim (Barcelona) · El Khannouss (Stuttgart) · El Aynaoui (Leipzig) · Ezzalzouli (Real Betis) · Igamane, Sahraoui (Lille) ·
Akhomach (Villarreal) · Targhalline (Feyenoord) · Bouhamidi (PSV) · Zakri (Sporting CP).
**Egyptians:** check this season's clubs of Mohamed Salah and Omar Marmoush and any Egyptian in UCL/UEL/UECL squads
(a 28 Aug 2026 Al Khaleej report places Salah at Trabzonspor in the Conference League: confirm before using).
Egyptian players in Europe get full coverage in any UEFA competition.

## The matchday package (who does what)

| When (Cairo) | Content | Made by |
|---|---|---|
| D−1 ~19:00 | «بكره ليلة الأبطال» preview short (motion, `--theme light`) + X/IG post: the 3–4 biggest matches + «عرب الليلة» | UCL desk (one-off) |
| Matchday 12:47 | Noon fixtures story/short leads with the UCL night | existing noon task |
| Matchday ~15:30 | Fun short (`motion_short.py`, meme/versus format, light tone) about the night's top match | UCL desk (one-off) |
| KO − 3 h | «توقعوا النتيجة» for the top 1–3 matches (X + IG + IG Story) | one-off |
| KO − 70 → KO − 25 (task fires at KO − 70, never later than KO − 60: REPEATED 11/13/14 Oct, the 14 Oct «lean» plan put it at KO − 45 and Real's XI was never posted) | Line-ups of BIG matches; flag Arab/Egyptian starters («حكيمي أساسي»). Search «<club> XI» for the club's own post embedded in outlets; uefa.com line-up pages are script-rendered (squad list only). No official/approved XI by KO − 25 → drafts to the owner + notification | one-off |
| KO + 40 | Half-time ONLY for matches with an Egyptian club/player, derbies or finals (token economy, 14 Oct; keep a running goal note from KO; search «<home> <away> half-time» + beIN/NBC live blogs; skip at HT + 10) | one-off |
| KO + 110 | FT for BIG matches: X + IG feed card first; the result REEL ≥ 30 min after the feed card. Sources in order: yallakora.com/tour-fixtures/105 + skysports.com/champions-league-scores-fixtures, «sofascore news <home> <away>», 365Scores en-uk report. **14 Oct: what worked at night was the Sofascore page «Full time» + the ESPN search title «Final Score»; uefa/Sky pages stayed pre-match until morning.** Put the date in every query («14 October 2026») — searches return last season's fixtures. FT round-up for the rest of the slot. A result confirmed in a retry is **posted in that same run** (X + IG story card), never left for a later task (14 Oct: LASK 3-6 Liverpool confirmed 22:15, posted 00:38) | one-off |
| 00:20 (22:00-slot nights) | «ليلة الأبطال» results story + short (top 5 on screen, all results in the caption) + «العرب في الأبطال» line. First read the FT task's posts (getScheduledPosts + log) and any running FT re-check: **once the round-up X post is out, no separate X post repeats a score in it** (re-check tasks then add an IG story only). If the FT task already made a short for a match, this short leaves that match off screen or the night gets one short only. After moving any post, re-run `budget_check.py` for **every** network of the package (14 Oct: YT Shorts 01:03 and 01:20 = 17 min) | one-off |
| Next morning, first newsroom run | Catch-up of every UCL result still HOLD (uefa.com/Sky scores page are fresh by then): one X post + one IG story with all of them, no repeat of scores already out (14 Oct: 6 of 9 matches left HOLD overnight) | newsroom run |
| Next day 10:51 | League-phase table card (top 8 + cut lines) from uefa.com, plus «رقم الجولة» stat | UCL desk |
| Thursday after MD | Long YouTube video «ملخص جولة دوري الأبطال» → **owner ✅ before upload** | UCL desk (Thursday) |

**Planners copy the times from this table** (the 14 Oct lean plan reused the old 00:07 «ليلة الأبطال» slot and line-ups at KO − 45; both had been fixed on 13 Oct).

**Card tools (there is always one):** result/fixture card = `story_short.py spec.json OUT --theme dark` with `"kind": "results"` → `<slug>-story.jpg` (IG story, 1080×1920) + short; feed card 1080×1350 = `motion_short.py` cover (`<slug>-cover.jpg`) or a centre crop of the story jpg. A confirmed result is never held for lack of a card (14 Oct 22:15 «no card tool found»).

The 23:22 «ليلة العرب» and 23:47 «نتايج النهارده» tasks leave UCL matches that kick off at 22:00 to «ليلة الأبطال» (00:20).

## Tone and look

Calm Egyptian dialect, never mock the losing side, no فرم/سحق/اكتسح/فضيحة, no betting odds.
No match footage, no club crests, licensed photos only. Use `motion_short.py` (motion graphics + original music) and alternate
`--theme dark` (nights, results) with `--theme light` (daytime previews, memes, tables).
