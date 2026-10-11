# Kora Klicks newsroom: lessons learned

Every run reads this file before starting work and follows it. When a run hits a new problem,
it adds one line here (date · what happened · the rule from now on). The end-of-day review
cleans the list up and turns repeated lessons into rules in `newsroom-rules`.
Newest first.

## 11 Oct 2026 (first day)
- **11 Oct 23:10: the 22:22 Facebook feed post (Zamalek–Ahly FT) failed with the rate limit again, so the biggest result of the day never reached the Facebook feed, and live pages (365Scores, FotMob, Sky Sport Italia, FilGoal without a date) stayed cached pre-match.** Check the FB feed status in `getScheduledPosts` at the start of every run and retry the missing big result first once 2 h have passed; for FT confirmation use post-match report pages (Sky Sports news, sofascore.com/news, club websites) from WebSearch, not live pages.
- **Sofascore and 365Scores lagged or contradicted themselves at full time (Sofascore stuck at 4' on Zamalek–Ahly and 90+7' on Betis; 365Scores header 0-2 vs summary 0-1).** For FT, read FilGoal `filgoal.com/matches?date=YYYY-MM-DD` (open it from a WebSearch result) first, and for SPL use spl.com.sa highlight/report pages (official) as the second source.
- **Zamalek–Ahly FT run: FilGoal/Sofascore pages stayed cached at a live minute and Yallakora's match page showed no events, so FT confirmation came from the Al-Ahram gate FT report (fetches fine, posted ~10 min after the whistle) plus FilGoal's score and Yallakora's scorer headline.** For Egyptian matches, search «بوابة الأهرام» + the result straight after FT and fetch the gate.ahram.org.eg link from the results; leave out numbers (table points, «القمة N») that approved sources don't give or that disagree.
- **Unattended runs could not open FilGoal, Yallakora or Sky Sport Italia (WebFetch permission timeouts, curl blocked by the proxy), and a Sofascore embed page stayed cached at 89'.** Search first and fetch only URLs that come back in WebSearch results (those open fine); for Sofascore use the match slug page (e.g. sofascore.com/de/sassuolo-milan/RdbsTfb), not the `/lineups/embed` page, and never post a score from a page that still shows a live minute.
- **Score cards in an RTL row put the wrong number next to each team (first render showed الزمالك beside the 1).** In an RTL team row with an LTR score, write the score as away-home ("1 - 0" for الزمالك 0-1 الأهلي), and check each team sits next to its own goals before hosting. Long Arabic Yallakora URLs fail in WebFetch (too long): use gate.ahram.org.eg pages or search titles instead.
- **Playwright cards fell back to a serif font because `set_content` pages can't load `file://` fonts.** Embed the bundled woff2 fonts as base64 `data:` URLs in `@font-face`, and look at the card before hosting.
- **The bundled `cairo-arabic-800` font has no space, colon or «·» glyphs, so a source line in it shows empty boxes.** Use Lalezar for every Arabic line on cards (source line too), write sources in Arabic letters with «،» between them, and look at the rendered card before hosting it.
- **Big results were held for lack of BBC/Sky/official pages, so nothing went out at Liverpool–City half-time.** From now on, match facts are confirmed by two of Sofascore, 365Scores, FilGoal and Yallakora. Don't wait for anything else.
- **The line-ups task started 5 minutes before kick-off, so Liverpool's XI and the Zamalek–Ahly XIs were late.** Line-ups come out about 60 minutes before kick-off. Start line-up tasks at kick-off − 45 min, and post as soon as two sources show them.
- **A run that hasn't published 10 minutes before kick-off is too slow.** Post the line-ups as text on X and Facebook first (fast), then do the card for Instagram and stories.
- **Facebook rate-limited the new page after many posts in a row (error 400).** Keep about one Facebook post per hour. Combine small results. After an error, wait about 2 hours, then try the next important post. Don't stop Facebook for the rest of the day.
- **Cards came out in DejaVu because Google Fonts is blocked.** Always use the bundled fonts in `.claude/skills/youtube-video/assets/fonts/`.
- **Our «يوم الكبار» story wrote «الأهلي × الزمالك», but Zamalek was the home side.** Always write home × away exactly as Yallakora or FilGoal list it.
- **FilGoal's matches page sometimes shows an older day.** Check the page date before taking any score.
- **Many sites time out (premierleague.com, BBC, legaseriea.it, ESPN).** Don't retry the same site. Move to the next source on the list straight away.
- **Holding a big result for a round-up delays it.** Big matches go out alone within 10 minutes. Round-ups are for small matches only.
