#!/usr/bin/env python3
"""Check a Cairo day against the platform budgets and spacing (platform-rules.md §2).

Usage:
  1. Save the getScheduledPosts JSON (brand 7358209, from 00:00 of the day to 06:00 next day) to a file.
  2. python3 scripts/budget_check.py posts.json 2026-10-13 [--add instagram:REEL@2026-10-13T19:30 ...]

Counts PUBLISHED + PENDING + PUBLISHING items (not ERROR/FAILED) per network for the day,
then lists spacing problems. With --add, also checks a post you are about to schedule.
Rules (13 Oct 2026): IG 25 items (≤ 8 feed, ≤ 5 reels), feed/reel ≥ 30 min apart, ≤ 3 stories in any 60 min;
TikTok 6, ≥ 60 min; YouTube 5 Shorts, ≥ 60 min; X 25, ≥ 10 min.
"""
import json, sys
from datetime import datetime, timedelta

BUDGET = {"instagram": 25, "tiktok": 6, "youtube": 5, "twitter": 25}
GAP = {"ig_feed": 30, "tiktok": 60, "youtube": 60, "twitter": 10}
LIVE = {"PUBLISHED", "PENDING", "PUBLISHING", "AWAITING_CONFIRMATION"}


def kind(net, typ):
    typ = (typ or "").upper()
    if net == "instagram":
        return "ig_story" if typ == "STORY" else ("ig_reel" if typ == "REEL" else "ig_post")
    if net == "youtube":
        return "yt_short" if typ == "SHORT" else "yt_video"
    return net


def load(path):
    d = json.load(open(path))
    d = d.get("data", d) if isinstance(d, dict) else d
    items = []
    for p in d:
        t = datetime.fromisoformat(p["publicationDate"]["dateTime"][:16])
        for pr in p.get("providers", []):
            if pr.get("status") not in LIVE:
                continue
            net = pr["network"]
            items.append((t, net, kind(net, (p.get(net + "Data") or {}).get("type")), p.get("text", "")[:40].replace("\n", " ")))
    return items


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__); sys.exit(1)
    items, day = load(a[0]), a[1]
    for i, x in enumerate(a):
        if x == "--add" and i + 1 < len(a):
            spec, at = a[i + 1].split("@")
            net, typ = spec.split(":")
            items.append((datetime.fromisoformat(at), net, kind(net, typ), "<< NEW >>"))
    start = datetime.fromisoformat(day + "T00:00")
    end = start + timedelta(days=1)
    today = sorted(x for x in items if start <= x[0] < end)
    problems = []
    c, k_ = {}, {}
    for t, net, k, _ in today:
        c[net] = c.get(net, 0) + 1
        k_[k] = k_.get(k, 0) + 1
    c.update({k: v for k, v in k_.items() if k not in BUDGET})
    print("Counts", day, {n: f"{c.get(n, 0)}/{b}" for n, b in BUDGET.items()},
          f"ig feed {c.get('ig_post', 0)}/8, reels {c.get('ig_reel', 0)}/5, stories {c.get('ig_story', 0)}, yt shorts {c.get('yt_short', 0)}/5")
    for n, b in BUDGET.items():
        if (c.get("yt_short", 0) if n == "youtube" else c.get(n, 0)) > b:
            problems.append(f"OVER BUDGET {n}")
    if c.get("ig_post", 0) > 8: problems.append("OVER ig feed 8")
    if c.get("ig_reel", 0) > 5: problems.append("OVER ig reels 5")
    # spacing uses all items (incl. the previous evening / next night) so midnight edges are caught
    allx = sorted(items)
    groups = {"ig_feed": ("ig_post", "ig_reel"), "tiktok": ("tiktok",), "youtube": ("yt_short",), "twitter": ("twitter",)}
    for g, kinds in groups.items():
        seq = [x for x in allx if x[2] in kinds]
        for p, q in zip(seq, seq[1:]):
            gap = (q[0] - p[0]).total_seconds() / 60
            if gap < GAP[g] and (start <= q[0] < end or start <= p[0] < end):
                problems.append(f"SPACING {g}: {p[0]:%H:%M} → {q[0]:%H:%M} = {gap:.0f} min (min {GAP[g]}) [{q[3]}]")
    st = [x[0] for x in allx if x[2] == "ig_story"]
    for i, t in enumerate(st):
        n = sum(1 for u in st if t <= u < t + timedelta(minutes=60))
        if n > 3 and start <= t < end:
            problems.append(f"STORIES {n} in the hour from {t:%H:%M} (max 3)")
            break
    print("\n".join(problems) if problems else "OK: budgets and spacing respected")


if __name__ == "__main__":
    main()
