#!/usr/bin/env bash
# Duplicate check before publishing anything.
# Usage: bash .claude/skills/newsroom-rules/scripts/already_posted.sh TERM [TERM...]
#   TERM = team or player names, Arabic and/or English (e.g. كومو Como روما Roma)
# Searches today's and yesterday's Cairo logs (logs/YYYY-MM-DD.md) for every line that
# mentions any term. Lines with a plannerUrl / PUBLISHED are marked "POSTED".
# Exit code 1 = at least one POSTED line found -> do NOT post the story again
# (only a different stage is allowed, e.g. FT after HT, or a missing network).
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
[ $# -ge 1 ] || { echo "usage: $0 TERM [TERM...]" >&2; exit 2; }
today=$(TZ=Africa/Cairo date +%F)
yday=$(TZ=Africa/Cairo date -d yesterday +%F)
pattern=$(printf '%s\n' "$@" | paste -sd'|' -)
found=0
for f in "logs/$yday.md" "logs/$today.md"; do
  [ -f "$f" ] || continue
  while IFS= read -r line; do
    if echo "$line" | grep -qE 'openWithPostUuid|PUBLISHED'; then
      echo "POSTED  $f: $line"; found=1
    else
      echo "seen    $f: $line"
    fi
  done < <(grep -iE -- "$pattern" "$f" || true)
done
if [ "$found" -eq 1 ]; then
  echo ">>> Already posted. Do not post it again; also confirm in getScheduledPosts from 00:00 today." >&2
  exit 1
fi
echo ">>> No posted line found in the logs. Still check getScheduledPosts (00:00 today → now) before posting."
