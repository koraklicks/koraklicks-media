#!/usr/bin/env bash
# Upload images/videos to the public media branch and print one public URL per file.
# Usage: host_media.sh FILE [FILE...]
# Files go to branch "media" of github.com/koraklicks/koraklicks-media, folder YYYY-MM-DD/.
# Files older than 14 days are removed from the branch to keep it small (Metricool keeps its own copy).
set -euo pipefail
REPO_SLUG="koraklicks/koraklicks-media"
DIR="${KK_MEDIA_DIR:-/tmp/kk-media}"
# The repo was renamed; sessions may only be authorised for the old name, so try both.
GIT_URLS=("https://github.com/$REPO_SLUG" "https://github.com/Mohamed-koraklikcs/koraklicks-media")
if [ ! -d "$DIR/.git" ]; then
  for u in "${GIT_URLS[@]}"; do git clone -q --depth 1 --branch media "$u" "$DIR" >&2 2>/dev/null && break; done
  [ -d "$DIR/.git" ] || { echo "cannot reach the media repo" >&2; exit 1; }
else
  git -C "$DIR" pull -q --rebase origin media >&2 || true
fi
DAY=$(TZ=Africa/Cairo date +%F)
mkdir -p "$DIR/$DAY"
URLS=()
for f in "$@"; do
  [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
  [ "$(stat -c %s "$f")" -lt 95000000 ] || { echo "too big (>95MB): $f" >&2; exit 1; }
  name="$(TZ=Africa/Cairo date +%H%M%S)-$(basename "$f" | tr ' ' '-')"
  cp "$f" "$DIR/$DAY/$name"
  git -C "$DIR" add "$DAY/$name"
  URLS+=("https://raw.githubusercontent.com/$REPO_SLUG/media/$DAY/$name")
done
CUTOFF=$(TZ=Africa/Cairo date -d '14 days ago' +%F)
for d in "$DIR"/20??-??-??; do
  [ -d "$d" ] && [[ "$(basename "$d")" < "$CUTOFF" ]] && git -C "$DIR" rm -rq "$(basename "$d")"
done
git -C "$DIR" -c user.name="Kora Klicks Newsroom" -c user.email="noreply@anthropic.com" commit -qm "Media $DAY" >&2
ok=0; for u in "${GIT_URLS[@]}"; do git -C "$DIR" push -q "$u" HEAD:media >/dev/null 2>&1 && { ok=1; break; }; done
[ $ok = 1 ] || { echo "push failed" >&2; exit 1; }
printf '%s\n' "${URLS[@]}"
