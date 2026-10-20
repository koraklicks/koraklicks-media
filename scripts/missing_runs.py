#!/usr/bin/env python3
"""List scheduled newsroom cycles that left no log line.

Usage: python3 scripts/missing_runs.py logs/YYYY-MM-DD.md
The 2-hour cycle runs at 01:07 and 09:07-23:07 every 2 h (Cairo). A cycle counts as
logged if a log line containing «cycle» starts with a Cairo time within 0-45 min after the slot, or a
line mentions the slot in UTC as «cycle HH:08Z». Review 19 Oct: 13:07/15:07/17:07/19:07
on 18 Oct were silent (3rd day running).
Also prints STUCK for «STARTED · cycle» lines with no result line within 60 min.
Also checks the daily pieces (review 21 Oct: on 20 Oct the 10:51 UCL desk died with no line and no
UCL task was created, so the MD3 night got nothing): PLAN, noon, «رقم اليوم», «ليلة العرب», night
results, and on UCL nights (a PLAN/noon line mentions UCL) the «UCL plan» and «ليلة الأبطال» lines.
"""
import re
import sys

SLOTS = ["01:07"] + [f"{h:02d}:07" for h in range(9, 24, 2)]
CAIRO_UTC_OFFSET = 3  # EEST; change to 2 after summer time ends


def mins(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def main(path):
    text = open(path, encoding="utf-8").read()
    times = [mins(t) for t in re.findall(r"^- (\d{2}:\d{2}) ·.*\bcycle\b", text, re.M)]
    utc_cycles = {(int(h) + CAIRO_UTC_OFFSET) % 24 for h in re.findall(r"cycle (\d{2}):0\dZ", text)}
    missing = []
    for slot in SLOTS:
        s = mins(slot)
        hit = any(0 <= t - s <= 45 for t in times) or (s // 60) in utc_cycles
        if not hit:
            missing.append(slot)
    print("MISSING " + ", ".join(missing) if missing else "OK all cycles logged")
    # Review 20 Oct: 19:12 and 21:09 cycles on 19 Oct logged «STARTED · cycle» and then nothing (died mid-plan).
    lines = re.findall(r"^- (\d{2}:\d{2}) · (.*)$", text, re.M)
    stuck = []
    for i, (t, rest) in enumerate(lines):
        if "STARTED" in rest and "cycle" in rest:
            later = [mins(t2) for t2, r2 in lines[i + 1:] if "STARTED" not in r2]
            if not any(0 < m - mins(t) <= 60 for m in later):
                stuck.append(t)
    if stuck:
        print("STUCK (STARTED, no result line within 60 min) " + ", ".join(stuck))


DAILY = [  # (label, regex that proves the piece ran or was skipped with a line)
    ("PLAN (planner 08:47 / cycle)", r"· PLAN ·"),
    ("noon story 12:47", r"NOON|ماتشات النهارده|يوم الكبار"),
    ("«رقم اليوم» 16:47", r"-NUM\b|رقم اليوم|خبر اليوم"),
    ("«ليلة العرب» 23:22", r"LAYLAT-ARAB|ليلة العرب"),
    ("night results 23:47", r"-RES\b|نتايج النهارده"),
]
UCL_DAILY = [
    ("UCL plan (UCL desk 10:51)", r"UCL plan|UCL-PLAN"),
    ("«ليلة الأبطال» 00:20", r"LAYLAT-ABTAL|ليلة الأبطال ·|«ليلة الأبطال» .*(PUBLISHED|SKIPPED)"),
]


def daily(text):
    missing = [lab for lab, rx in DAILY if not re.search(rx, text)]
    ucl_day = re.search(r"· PLAN ·.*UCL|NOON.*UCL", text)
    if ucl_day:
        missing += [lab for lab, rx in UCL_DAILY if not re.search(rx, text)]
    print("DAILY MISSING " + ", ".join(missing) if missing else "OK daily pieces logged")


if __name__ == "__main__":
    main(sys.argv[1])
    daily(open(sys.argv[1], encoding="utf-8").read())
