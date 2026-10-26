#!/usr/bin/env python3
"""Final scores from ESPN's public scoreboard (owner allowed site.api.espn.com, 26 Oct 2026).

Usage: python3 scripts/espn_scores.py 20261025                 # all default leagues, that date (ESPN date, UTC-based)
       python3 scripts/espn_scores.py 20261025 esp.1 eng.1     # chosen leagues
       python3 scripts/espn_scores.py 20261025 --team Barcelona  # only matches with that team

Prints one line per match: league | home x-y away | status | goals (minute + scorer).
STATUS_FULL_TIME = ESPN counts as ONE source for the final-score rule (source_check.py ft "ESPN" "<2nd source>").
A match that ended after midnight UTC can sit on the next date: check both dates for late kick-offs.
Not on ESPN: the Egyptian Premier League (use Yallakora/FilGoal/Ahram). Scorer names: ESPN spelling; minutes can differ
by 1' from club reports — prefer the official club report when both exist.
"""
import gzip, json, sys, urllib.request

LEAGUES = ["eng.1", "esp.1", "ita.1", "ger.1", "fra.1", "ksa.1", "tur.1", "uefa.champions", "uefa.europa",
           "uefa.europa.conf", "caf.champions", "caf.confed", "afc.champions"]


def get(league, date):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard?dates={date}"
    req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw)


def main():
    args = [a for a in sys.argv[1:]]
    if not args or not args[0].isdigit():
        sys.exit(__doc__)
    date, team = args[0], None
    if "--team" in args:
        i = args.index("--team"); team = args[i + 1].lower(); del args[i:i + 2]
    leagues = args[1:] or LEAGUES
    for lg in leagues:
        try:
            d = get(lg, date)
        except Exception as e:  # league not on ESPN / no data
            print(f"{lg} | not available ({type(e).__name__})"); continue
        name = (d.get("leagues") or [{}])[0].get("name", lg)
        for e in d.get("events", []):
            c = e["competitions"][0]
            t = {x["homeAway"]: x for x in c["competitors"]}
            h, a = t["home"], t["away"]
            if team and team not in (h["team"]["displayName"] + a["team"]["displayName"]).lower():
                continue
            ids = {h["team"]["id"]: h["team"]["displayName"], a["team"]["id"]: a["team"]["displayName"]}
            goals = [f'{x.get("clock", {}).get("displayValue", "")} {", ".join(p["displayName"] for p in x.get("athletesInvolved", []))}'
                     f'{" (pen)" if x.get("penaltyKick") else ""}{" (og)" if x.get("ownGoal") else ""} [{ids.get(x.get("team", {}).get("id"), "?")}]'
                     for x in c.get("details", []) if x.get("scoringPlay")]
            print(f'{name} | {h["team"]["displayName"]} {h.get("score", "-")}-{a.get("score", "-")} {a["team"]["displayName"]} | '
                  f'{e["status"]["type"]["name"]} | {e["date"]} | goals: {"; ".join(goals) or "-"}')


if __name__ == "__main__":
    main()
