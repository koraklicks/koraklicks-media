# Trusted sources and tiers

Always prefer the **official** source. Re-check accounts are verified and genuine; parody
accounts copying real names are common.

## Official (instantly CONFIRMED)

- Club official websites and verified club accounts (X, Instagram, Facebook, YouTube)
- League / organiser official sites and accounts:
  - Premier League (premierleague.com)
  - LaLiga (laliga.com)
  - Serie A (legaseriea.it)
  - Saudi Pro League (spl.com.sa) and the Saudi Arabian Football Federation
  - Egyptian Premier League / Egyptian Football Association (efa.com.eg)
- FIFA, UEFA, CAF, AFC, CONMEBOL and UAFA (Arab Football Association) official channels
- National federations' official channels (e.g. Egyptian FA, Saudi FA, Royal Moroccan FF, Algerian FF, Tunisian FF, Qatar FA, The FA, RFEF, FIGC, FFF, DFB, Brazil's CBF, Argentina's AFA)
- A player's or coach's own verified account (for their own news only)

## Tier 1 (two independent Tier-1 reports = CONFIRMED)

International: BBC Sport, Sky Sports, The Athletic, ESPN, Reuters, AP, AFP, Marca, AS,
Mundo Deportivo, Gazzetta dello Sport, Corriere dello Sport, Sky Sport Italia, Fabrizio Romano
("here we go" only).
South America: Globo/ge, Olé, TyC Sports.
Arabic/regional: beIN Sports, Le360 Sport and Hesport (Morocco), Al Kass, Al-Ahram sports desk, Saudi Press Agency (SPA), Al Riyadiyah (official Saudi sports channel).

## Tier 2 (never enough alone = UNCONFIRMED)

Tabloids, transfer-gossip sites, aggregator accounts, single journalists without an
established track record, fan pages, "مصادر خاصة" reports, screenshots without a link.

## Live-score data

Owner-approved live-score services (added 11 Oct 2026), for live scores, line-ups, goals, scorers,
cards, final results and fixture times:
- **Sofascore** (sofascore.com)
- **365Scores** (365scores.com)
- **FilGoal** (filgoal.com), Arabic
- **Yallakora** (yallakora.com), Arabic; best for the Egyptian league

Rule for match facts (scores, goals, scorers, red cards, kick-off times, line-ups):
**two of these four agree = CONFIRMED**, or one of them plus an official club/league source, **or one of them plus one Tier-1 full-time report** (e.g. SPA/واس, الأهرام, Sky, beIN, BBC, ESPN) — owner decision 12 Oct 2026.
Credit them in «📌 المصدر:» (e.g. «📌 المصدر: Sofascore · يلاكورة»).
If they disagree on a goal, scorer or minute, wait until they agree.
These services are for match data only. Transfer news, injuries, statements and off-pitch stories
still need an official source or two Tier-1 outlets.
Always check the page shows **today's date** and the right match (FilGoal's matches page can show a cached older day). Reading tips: Yallakora `yallakora.com/match-center` and FilGoal `filgoal.com/matches/` read well; Sofascore and 365Scores are app-like pages, so use their match pages or web search.
If a site blocks reading, use the next one on the list; use web search results for the same match as a fallback.

### Reading tips (tested on 11 Oct 2026, unattended runs)
- **Search first, then fetch only URLs that came back in WebSearch results.** Typed URLs to FilGoal, Yallakora,
  Sky Sport Italia, legaseriea.it, premierleague.com, BBC and ESPN timed out (permission) all day; curl to them is blocked by the proxy.
  Don't retry a blocked site: move to the next source at once.
- **Never take a score from a page that still shows a live minute.** Sofascore (`/lineups/embed` and often the slug page),
  365Scores, FotMob and Sky Sport Italia live pages stay cached pre-match or mid-match; 365Scores header and summary disagreed (0-2 vs 0-1).
- **Full time, fastest sources that worked:** FilGoal `filgoal.com/matches?date=YYYY-MM-DD` opened from a search result (check the date;
  the undated page showed the day before); Al-Ahram gate (`gate.ahram.org.eg`, Tier 1) HT/FT reports ~10 min after the whistle for
  Egyptian matches (search «بوابة الأهرام» + teams + النتيجة); Sky Sports news reports and `sofascore.com/news` reports; club sites'
  post-match reports (juventus.com, mancity.com via its Yahoo syndication, cpfc.co.uk); spl.com.sa highlight pages for the Saudi league.
- Long Arabic Yallakora/Masrawy URLs are too long for WebFetch: use the search-result title, or the Ahram gate page.
- Scorers/minutes that only one source gives are left out; numbers like table points or «القمة N» only when an approved source gives them.

### HT/FT playbook per competition (firm; built from 12 Oct, when 12+ lessons were about cached pages)
General (all competitions):
- Open only URLs that a WebSearch returned; typed URLs time out ("permission request not answered").
- **Never take FT from a page that shows a live minute, even 90+**: on 12 Oct 365Scores froze at 90+1 (1-2) when the real FT was 3-1,
  and Korabia/365Scores froze at 82' (1-0) when the real FT was 1-1. Wait for «انتهت»/«Final»/«FT»/«afgelopen».
- A page from search that looks stale: re-fetch it with a new `#fragment` (e.g. `#t2`) to beat the 15-min cache; every 2 min from FT − 5.
  (Stopped working for some pages late on 12 Oct; then switch source instead of retrying.)
- So3ody and Korabia use one data feed: they count as ONE source, and neither is on the approved list (owner question pending).
- Kick-off time and opponent names come from FilGoal/Yallakora/the club, never only from listing sites (12 Oct: «الشرقية للدخان»
  was really «إنبي», «استقلال خوزستان» was really «الاستقلال»).

| Competition | HT (start at KO + 44) | FT (start at the whistle) |
|---|---|---|
| EGY | search «بوابة الأهرام <teams> نهاية الشوط الأول» (Tier 1) + FilGoal team page `filgoal.com/teams/ID` from search | English search «365scores ar football match <home> <away>» → 365Scores + Sofascore pages (often FT within 5 min); FilGoal today-strip on any `filgoal.com/articles/N` page from search |
| ACLE / Saudi | Al Riyadiyah match centre `matches.arriyadiyah.com/matches/ID` (search «نتيجة مباراة X و Y arriyadiyah»); Kooora team «مباريات» page | AFC report title search «MD<n>: <home> <score> <away>» (the-afc.com = official, publish alone); FilGoal homepage strip with a fresh `#fragment`; Kooora team page «انتهت»; national news agency (SPA, INA/واع, WAM) |
| Serie A | 365Scores/FilGoal team page | Italian search «<home>-<away> risultato finale» or English «<home> <away> full time <scorers>» + FilGoal team/matches page |
| EPL / LaLiga | Sky/BBC live report from search | search «sporza <home> <away>» (shows «afgelopen» + scorers right after the whistle) + FilGoal strip/365Scores |
| Saudi/ACLE line-ups | Al Riyadiyah match centre (Tier 1) or the club's official X post + one more outlet with the same XI | — |

## Owner additions

The owner may add or demote sources at any time. Keep this list as the single truth; agents do
not add sources on their own.

- **Final score rule (owner ✅ 22 Oct 2026, after Ahly 3-3 Qanah was never posted on 21 Oct):** a FINAL SCORE is CONFIRMED when
  any **two** of ESPN, Sky Sports, beIN Sports, Goal, FotMob, Yallakora, FilGoal show the **same** final score. A search-result
  title or snippet that states the final score counts (no need to open a page that is still cached). Run
  `python3 scripts/source_check.py ft "<source1>" "<source2>"` → PASS. Score only: scorers, red cards and any news still follow
  the normal rules (name only the scorers both sources agree on, or none). Never from a page that shows a live minute.
