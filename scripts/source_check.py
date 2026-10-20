#!/usr/bin/env python3
"""Check a result/story's sources against trusted-sources.md BEFORE publishing.

Usage: python3 scripts/source_check.py match "Sofascore" "ESPN"
       python3 scripts/source_check.py news "Sky Sports" "BBC Sport"
Prints PASS or HOLD and why. Review 21 Oct: on 20 Oct six results went out on sources that
are not on the list (btolat, 101greatgoals, allfootballapp, ajel, ysscores, hihi2, sabq, AA,
Hürriyet, Takvim, KingFut, Anews) — the 13 Oct lesson repeated. Owner-pending sources
(Turkish outlets, Yallakora-only, single Sofascore) stay HOLD until he says ✅.
Keep these lists in sync with .claude/skills/newsroom-rules/references/trusted-sources.md.
"""
import sys

TIER1 = ["bbc", "sky", "athletic", "espn", "reuters", "ap ", "associated press", "afp", "marca", "as.com",
         "mundo deportivo", "gazzetta", "corriere dello sport", "globo", "ge.globo", "olé", "tyc",
         "bein", "le360", "hesport", "al kass", "الكأس", "ahram", "الأهرام", "spa", "واس", "riyadiyah",
         "الرياضية", "romano", "بي إن", "بي ان", "سكاي"]
LIVE = ["sofascore", "365scores", "filgoal", "في الجول", "yallakora", "يلا كورة", "يلاكورة"]
OFFICIAL_HINTS = ["official", "رسمي", "uefa", "يويفا", "fifa", "caf", "afc", "club site", "الموقع الرسمي", "spl.com.sa"]


def kind(name):
    n = name.lower().strip()
    if any(h in n for h in OFFICIAL_HINTS):
        return "official"
    if any(h in n for h in LIVE):
        return "live"
    if n in ("as", "ap") or any(h in n for h in TIER1):
        return "tier1"
    return "other"


def main(mode, names):
    kinds = {nm: kind(nm) for nm in names}
    c = {k: sum(1 for v in kinds.values() if v == k) for k in ("official", "live", "tier1", "other")}
    if mode == "match":
        ok = c["official"] >= 1 or c["live"] >= 2 or (c["live"] >= 1 and c["tier1"] >= 1) or c["tier1"] >= 2
        rule = "official, or 2 live services, or 1 live + 1 Tier-1, or 2 Tier-1"
    else:
        ok = c["official"] >= 1 or c["tier1"] >= 2
        rule = "official, or 2 independent Tier-1 (live services don't count for news)"
    for nm, k in kinds.items():
        print(f"  {nm}: {k}")
    print(("PASS" if ok else "HOLD") + f" · needs {rule}")
    if not ok and c["other"]:
        print("  'other' sources never count; credit only the sources that pass.")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("match", "news"):
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2:]))
