#!/usr/bin/env python3
"""Kora Klicks platform call-to-action overlay (owner request 18 Oct 2026).

Adds an animated «لايك + اشترك / فولو» banner to a finished video, one file per platform family:

  python3 endcard.py VIDEO.mp4 OUT_DIR [--theme dark|light] [--only yt|social]

Writes next to each other in OUT_DIR:
  <stem>-yt.mp4      «اعمل لايك 👍  ·  اشترك 🔔»   → YouTube (Shorts and long videos)
  <stem>-social.mp4  «اعمل لايك ❤️  ·  فولو ➕»    → Instagram Reel + TikTok (same Metricool post)

Vertical videos (shorts/reels): the banner slides up for the last 2.8 s.
Landscape videos (long YouTube): the banner shows twice, for 4 s at about 30 % of the video and for the last 6 s.
Music and length stay exactly the same (audio is copied); only the picture is re-encoded.
Generic calls only: never «لايك لو…», «منشن صاحبك» or similar bait (references/platform-rules.md).
"""
import argparse, json, subprocess, tempfile, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "assets" / "fonts"

CTA = {
    "yt": [("👍", "اعمل لايك", "soft"), ("🔔", "اشترك", "yt")],
    "social": [("❤️", "اعمل لايك", "soft"), ("➕", "فولو", "brand")],
}
THEME = {
    "dark": dict(panel="rgba(5,6,8,.86)", edge="#22272E", fg="#E3F4FF", mute="#8A97A3", soft="#1b232c", brand="#00C853", brandfg="#03110a"),
    "light": dict(panel="rgba(255,255,255,.94)", edge="#D5E0EA", fg="#0B1620", mute="#5B6B7A", soft="#EEF3F8", brand="#00A84F", brandfg="#ffffff"),
}


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    s = j["streams"][0]
    return int(s["width"]), int(s["height"]), float(j["format"]["duration"])


def banner_html(kind, theme, vertical):
    t = THEME[theme]
    scale = 1.0 if vertical else 0.62
    pills = []
    for emoji, text, style in CTA[kind]:
        if style == "yt":
            bg, fg = "#FF0033", "#ffffff"
        elif style == "brand":
            bg, fg = t["brand"], t["brandfg"]
        else:
            bg, fg = t["soft"], t["fg"]
        pills.append(f'<span class=pill style="background:{bg};color:{fg}"><span class=e>{emoji}</span>{html.escape(text)}</span>')
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:CA;src:url({(FONTS/'cairo-arabic-900-normal.woff2').as_uri()})}}
@font-face{{font-family:SM;src:url({(FONTS/'space-mono-latin-700-normal.woff2').as_uri()})}}
@font-face{{font-family:EM;src:url({(FONTS/'emoji'/'NotoColorEmoji.ttf').as_uri()})}}
html,body{{margin:0;background:transparent}}
.wrap{{display:inline-flex;flex-direction:column;align-items:center;gap:{18*scale}px;padding:{26*scale}px {34*scale}px;
  background:{t['panel']};border:2px solid {t['edge']};border-radius:{40*scale}px;direction:rtl}}
.row{{display:flex;gap:{20*scale}px}}
.pill{{display:inline-flex;align-items:center;gap:{14*scale}px;font-family:CA,EM;font-size:{58*scale}px;line-height:1;
  padding:{20*scale}px {38*scale}px;border-radius:999px;white-space:nowrap}}
.e{{font-family:EM;font-size:{52*scale}px}}
.h{{font-family:SM;font-size:{30*scale}px;color:{t['mute']};letter-spacing:.08em;direction:ltr}}
</style></head><body><div class=wrap id=b><div class=row>{''.join(pills)}</div></div></body></html>"""


def render_png(kind, theme, vertical, out_png):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 600})
        page_file = Path(out_png).with_suffix(".html")
        page_file.write_text(banner_html(kind, theme, vertical), encoding="utf-8")
        pg.goto(page_file.as_uri())          # file:// page so the bundled fonts load
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.locator("#b").screenshot(path=str(out_png), omit_background=True)
        b.close()


def overlay(video, png, out, W, H, dur, vertical):
    if vertical:
        windows = [(max(0.0, dur - 2.8), dur)]
        y_rest = int(H * 0.70)          # under the CTA text, above the IG/TikTok caption area
    else:
        windows = [(round(dur * 0.30, 2), round(dur * 0.30 + 4, 2)), (max(0.0, dur - 6.0), dur)]
        y_rest = int(H * 0.80)
    inputs, chains, last = ["-i", str(video)], [], "0:v"
    for k, (t0, t1) in enumerate(windows, start=1):
        inputs += ["-loop", "1", "-t", f"{t1 - t0:.2f}", "-i", str(png)]
        chains.append(f"[{k}:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={max(0.0, t1 - t0 - 0.25):.2f}:d=0.25:alpha=1,"
                      f"setpts=PTS+{t0:.2f}/TB[b{k}]")
        chains.append(f"[{last}][b{k}]overlay=x=(W-w)/2:y='{y_rest}+60*max(0\\,1-(t-{t0:.2f})/0.3)':eval=frame:"
                      f"enable='between(t,{t0:.2f},{t1:.2f})'[v{k}]")
        last = f"v{k}"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                    "-map", f"[{last}]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("out_dir")
    ap.add_argument("--theme", choices=list(THEME), default="dark")
    ap.add_argument("--only", choices=list(CTA))
    a = ap.parse_args()
    video, out_dir = Path(a.video), Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    W, H, dur = probe(video)
    vertical = H > W
    stem = video.stem
    result = {}
    with tempfile.TemporaryDirectory() as td:
        for kind in ([a.only] if a.only else list(CTA)):
            png = Path(td) / f"{kind}.png"
            render_png(kind, a.theme, vertical, png)
            out = out_dir / f"{stem}-{kind}.mp4"
            overlay(video, png, out, W, H, dur, vertical)
            result[kind] = str(out)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
