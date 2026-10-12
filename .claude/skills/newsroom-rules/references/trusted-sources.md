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

## Owner additions

The owner may add or demote sources at any time. Keep this list as the single truth; agents do
not add sources on their own.
