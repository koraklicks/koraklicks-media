# Kora Klicks newsroom: lessons learned

Every run reads this file before starting work and follows it. When a run hits a new problem,
it adds one line here (date · what happened · the rule from now on). The end-of-day review
cleans the list up and turns repeated lessons into rules in `newsroom-rules`.
Newest first.

## 11 Oct 2026 (first day)
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
