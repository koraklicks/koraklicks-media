#!/usr/bin/env python3
"""Club logos (ESPN) and free player photos (Wikimedia Commons) for Kora Klicks visuals (owner, 19 Nov 2026).

  python3 scripts/media.py crests YYYYMMDD LEAGUE [LEAGUE ...]
      Downloads the logo of every team playing that day (ESPN scoreboard) into .claude/assets/crests/<espn_id>.png
      and prints one line per team:  <ESPN name> | <path>
  python3 scripts/media.py crest "Team name" [LEAGUE]
      Path of a cached logo (searches the cache index); downloads via the league's team list if missing.
  python3 scripts/media.py photo "Mohamed Salah" [--n 5]
      Searches Wikimedia Commons for a FREE photo (CC BY / CC BY-SA / CC0 / public domain only), saves it into
      .claude/assets/photos/ and prints JSON: {"path", "credit", "source_url", "license"}.
      The "credit" text MUST be shown on the image (cards.py / render.py do it from "photo_credit").

Rules (newsroom-rules SKILL §4): never take photos from news sites, agencies (Getty/Reuters/AP/AFP/Imago) or club
social accounts; only this script's Commons results or files the owner supplied. Logos only from ESPN, no edits.
Needs the owner to allow a.espncdn.com, commons.wikimedia.org, upload.wikimedia.org (claude.ai Settings > Capabilities).
"""
import json, re, sys, urllib.parse, urllib.request, gzip, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREST_DIR = ROOT / ".claude" / "assets" / "crests"
PHOTO_DIR = ROOT / ".claude" / "assets" / "photos"
UA = "KoraKlicksNewsroom/1.0 (football news; contact via github.com/koraklicks)"
FREE = re.compile(r"^(cc[- ]by(-sa)?( \d\.\d)?|cc0|public domain|pd)", re.I)


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw if binary else json.loads(raw)


def _index():
    f = CREST_DIR / "index.json"
    return json.loads(f.read_text()) if f.exists() else {}


def _save_index(ix):
    CREST_DIR.mkdir(parents=True, exist_ok=True)
    (CREST_DIR / "index.json").write_text(json.dumps(ix, ensure_ascii=False, indent=1, sort_keys=True))


def _store(team, ix):
    tid, name = team["id"], team.get("displayName", "")
    path = CREST_DIR / f"{tid}.png"
    if not path.exists():
        url = team.get("logo") or (team.get("logos") or [{}])[0].get("href") or \
            f"https://a.espncdn.com/i/teamlogos/soccer/500/{tid}.png"
        path.write_bytes(get(url, binary=True))
    ix[tid] = {"name": name, "short": team.get("shortDisplayName", ""), "file": path.name}
    return path


def crests(date, leagues):
    ix = _index()
    CREST_DIR.mkdir(parents=True, exist_ok=True)
    for lg in leagues:
        d = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}")
        for ev in d.get("events", []):
            for c in ev["competitions"][0]["competitors"]:
                try:
                    print(f'{c["team"]["displayName"]} | {_store(c["team"], ix)}')
                except Exception as e:
                    print(f'{c["team"]["displayName"]} | FAILED ({type(e).__name__}: {e})')
    _save_index(ix)


def crest(name, league=None):
    ix, low = _index(), name.lower()
    for tid, v in ix.items():
        if low in (v["name"].lower(), v["short"].lower()) or low in v["name"].lower():
            return CREST_DIR / v["file"]
    if league:
        d = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams")
        for t in d["sports"][0]["leagues"][0]["teams"]:
            t = t["team"]
            if low in t["displayName"].lower() or low == t.get("shortDisplayName", "").lower():
                p = _store(t, ix); _save_index(ix); return p
    return None


def _clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def photo(query, n=5):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
                                "gsrsearch": f'filetype:bitmap "{query}"', "gsrlimit": 25, "prop": "imageinfo",
                                "iiprop": "url|extmetadata|size", "iiurlwidth": 1600})
    pages = get(f"https://commons.wikimedia.org/w/api.php?{q}").get("query", {}).get("pages", {})
    cands = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = _clean(md.get("LicenseShortName", {}).get("value"))
        if not FREE.match(lic) or ii.get("width", 0) < 800:
            continue
        title = p["title"]
        if query.split()[-1].lower() not in title.lower():   # the person's name must be in the file name
            continue
        date = _clean(md.get("DateTimeOriginal", {}).get("value"))[:4]
        cands.append((date, title, ii, lic, _clean(md.get("Artist", {}).get("value")) or "Unknown author"))
    if not cands:
        return None
    cands.sort(key=lambda c: c[0], reverse=True)   # newest first
    date, title, ii, lic, artist = cands[0]
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", title.split(":", 1)[-1])[:80]
    path = PHOTO_DIR / safe
    if not path.exists():
        path.write_bytes(get(ii.get("thumburl") or ii["url"], binary=True))
    return {"path": str(path), "credit": f"📷 {artist[:60]} · {lic} · Wikimedia Commons",
            "source_url": ii.get("descriptionurl"), "license": lic, "year": date,
            "others": [c[1] for c in cands[1:n]]}


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "crests" and len(a) >= 3:
        crests(a[1], a[2:])
    elif a[0] == "crest" and len(a) >= 2:
        print(crest(a[1], a[2] if len(a) > 2 else None) or "NOT FOUND")
    elif a[0] == "photo" and len(a) >= 2:
        r = photo(a[1])
        print(json.dumps(r, ensure_ascii=False, indent=1) if r else "NOT FOUND (no free photo on Commons)")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
