#!/usr/bin/env bash
# Upload images/videos to the public media branch and print one public URL per file.
# Usage: host_media.sh FILE [FILE...]
# Files go to branch "media" of github.com/Mohamed-koraklikcs/koraklicks-media, folder YYYY-MM-DD/.
# Files older than 14 days are removed from the branch to keep it small (Metricool keeps its own copy).
set -euo pipefail
REPO_SLUG="Mohamed-koraklikcs/koraklicks-media"
DIR="${KK_MEDIA_DIR:-/tmp/kk-media}"
if [ ! -d "$DIR/.git" ]; then
  git clone -q --depth 1 --branch media "https://github.com/$REPO_SLUG" "$DIR" >&2
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
git -C "$DIR" push -q origin HEAD:media >&2
printf '%s\n' "${URLS[@]}"
