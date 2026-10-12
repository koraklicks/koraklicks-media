#!/usr/bin/env python3
"""Check an X (Twitter) post length before sending it to Metricool.

Usage:  python3 .claude/skills/newsroom-rules/scripts/x_len.py "النص كامل"
   or:  python3 .claude/skills/newsroom-rules/scripts/x_len.py < post.txt

Counts the way X does (approximately): every URL = 23, emoji and CJK = 2,
everything else (Arabic letters included) = 1. Exit code 1 if over the
house limit of 250 (X's hard limit is 280; Metricool rejected 338 and 292 on 12 Oct).
"""
import re
import sys
import unicodedata

LIMIT = 250
HARD = 280
URL = re.compile(r"https?://\S+")


def weight(ch: str) -> int:
    cp = ord(ch)
    if unicodedata.category(ch) in ("Mn", "Me", "Cf"):  # combining marks, ZWJ, variation selectors
        return 0
    if cp >= 0x1F000 or 0x2600 <= cp <= 0x27BF or 0x1100 <= cp <= 0x11FF or 0x2E80 <= cp <= 0x9FFF:
        return 2
    return 1


def x_length(text: str) -> int:
    n = 0
    for part in URL.split(text):
        n += sum(weight(c) for c in part)
    return n + 23 * len(URL.findall(text))


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    text = text.rstrip("\n")
    n = x_length(text)
    status = "OK" if n <= LIMIT else ("OVER HOUSE LIMIT" if n <= HARD else "OVER X LIMIT")
    print(f"{n} / {LIMIT} ({status})")
    sys.exit(0 if n <= LIMIT else 1)
