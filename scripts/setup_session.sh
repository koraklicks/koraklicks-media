#!/usr/bin/env bash
# Run at the start of every scheduled run: copies the repo's allowed sites (WebFetch/WebSearch)
# into the user settings, so news/score sites open without a permission prompt even when the
# session didn't start inside this repo.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/.claude"
python3 - "$REPO/.claude/settings.json" "$HOME/.claude/settings.json" <<'PY'
import json, sys, os
src, dst = sys.argv[1], sys.argv[2]
allow = json.load(open(src))["permissions"]["allow"]
d = json.load(open(dst)) if os.path.exists(dst) else {}
cur = d.setdefault("permissions", {}).setdefault("allow", [])
for a in allow:
    if a not in cur: cur.append(a)
json.dump(d, open(dst, "w"), indent=2)
print(f"allowed rules: {len(cur)}")
PY
pip install soundfile --break-system-packages -q 2>/dev/null || true
