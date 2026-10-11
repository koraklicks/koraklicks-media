#!/usr/bin/env python3
"""Kora Klicks motion-graphics renderer.

Turns a storyboard JSON into a branded 1920x1080 MP4 (Arabic, RTL) plus a
thumbnail and a contact sheet for review.

Usage:
  python3 render.py storyboard.json OUT_DIR [--fps 25] [--preview]

  --preview  renders at 12 fps for a fast check of layout and timing.

Needs: python playwright (with Chromium) and ffmpeg.
Scene types: intro, section, result, headline, table, stat, list, outro.
Themes: "major" (default for Kora Klicks: black cinematic, giant condensed type) or "classic" (navy cards).
Any scene may set "image": a licensed photo path (relative to the storyboard) shown full-bleed with a dark grade.
See ../references/storyboard-schema.md for every field.
"""
import argparse, html, json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = (HERE.parent / "assets" / "fonts").as_uri()
W, H = 1920, 1080
FADE = 0.45  # seconds of fade in/out per scene

NAVY, NAVY2, GREEN, YELLOW, WHITE, MUTED = "#0A1F44", "#13305F", "#00C853", "#FFD600", "#FFFFFF", "#A9C3E8"

KK_LOGO = """<svg viewBox="0 0 240 240" class="logo" aria-hidden="true"><rect width="240" height="240" rx="40" fill="#000000"/><g transform="translate(41.92 200.17) scale(0.07467 -0.09110)" fill="#E3F4FF" stroke="#E3F4FF" stroke-width="57.3" stroke-linejoin="miter"><path transform="translate(0.0 0)" d="M78 0V1760H426V1055L590 1760H944L747 954L985 0H620L428 852V0Z"/><path transform="translate(1028.4 0)" d="M78 0V1760H426V1055L590 1760H944L747 954L985 0H620L428 852V0Z"/></g></svg>"""

LOGO = """<svg viewBox="0 0 240 240" class="logo" aria-hidden="true"><rect width="240" height="240" rx="52" fill="#13305F"/><circle cx="112" cy="118" r="70" fill="none" stroke="#00C853" stroke-width="12" stroke-dasharray="300 140" stroke-linecap="round" transform="rotate(103 112 118)"/><g stroke="#FFD600" stroke-width="10" stroke-linecap="round"><line x1="14" y1="96" x2="30" y2="96"/><line x1="8" y1="118" x2="30" y2="118"/><line x1="14" y1="140" x2="30" y2="140"/></g><g transform="translate(112 118) scale(0.9)"><circle r="50" fill="#FFFFFF" stroke="#0A1F44" stroke-width="6"/><g stroke="#0A1F44" stroke-width="7" stroke-linecap="round"><line x1="0" y1="-18" x2="0" y2="-47"/><line x1="17.1" y1="-5.6" x2="44.7" y2="-14.5"/><line x1="10.6" y1="14.6" x2="27.6" y2="38"/><line x1="-10.6" y1="14.6" x2="-27.6" y2="38"/><line x1="-17.1" y1="-5.6" x2="-44.7" y2="-14.5"/></g><polygon points="0,-18 17.1,-5.6 10.6,14.6 -10.6,14.6 -17.1,-5.6" fill="#0A1F44"/></g><path d="M0 0 L0 58 L14 45 L24 66 L34 61 L24 41 L42 41 Z" transform="translate(140 146) scale(1.15)" fill="#FFD600" stroke="#0A1F44" stroke-width="5" stroke-linejoin="round"/></svg>"""

BALL = """<svg viewBox="-55 -55 110 110" class="ball" aria-hidden="true"><circle r="50" fill="#FFFFFF" stroke="#0A1F44" stroke-width="6"/><polygon points="0,-18 17.1,-5.6 10.6,14.6 -10.6,14.6 -17.1,-5.6" fill="#0A1F44"/></svg>"""

CSS = f"""
@font-face{{font-family:Cairo;font-weight:800;src:url({FONTS}/cairo-arabic-800-normal.woff2) format('woff2');unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F}}
@font-face{{font-family:Cairo;font-weight:900;src:url({FONTS}/cairo-arabic-900-normal.woff2) format('woff2');unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F}}
@font-face{{font-family:Cairo;font-weight:900;src:url({FONTS}/cairo-latin-900-normal.woff2) format('woff2');unicode-range:U+0000-024F}}
@font-face{{font-family:Outfit;font-weight:800;src:url({FONTS}/outfit-latin-800-normal.woff2) format('woff2')}}
@font-face{{font-family:Outfit;font-weight:900;src:url({FONTS}/outfit-latin-900-normal.woff2) format('woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{NAVY};color:{WHITE};font-family:Cairo,Outfit,sans-serif;font-weight:800}}
.stage{{position:absolute;inset:0;overflow:hidden}}
.bg-ring{{position:absolute;border-radius:50%;border:28px solid {GREEN};opacity:.08}}
.bug{{position:absolute;top:44px;right:60px;display:flex;align-items:center;gap:18px;z-index:5}}
.bug .logo{{width:84px;height:84px}}
.bug .name{{font-size:38px;font-weight:900;line-height:1}}
.bug .en{{font-family:Outfit;font-size:18px;letter-spacing:4px;color:{GREEN};font-weight:800;direction:ltr;text-align:right;margin-top:6px}}
.ep{{position:absolute;top:58px;left:60px;font-size:30px;color:{MUTED};z-index:5}}
.scene{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:150px 120px 110px;opacity:0}}
.in{{opacity:0}}
.ltr{{direction:ltr;unicode-bidi:isolate}}
.num{{font-family:Outfit;font-weight:900}}
.src{{position:absolute;bottom:56px;right:120px;font-size:28px;color:{MUTED}}}
.pill{{display:inline-block;padding:10px 34px;border-radius:999px;font-weight:900}}
/* intro */
.intro .logo{{width:260px;height:260px;margin-bottom:36px}}
.intro h1{{font-size:112px;font-weight:900;line-height:1.15;text-align:center}}
.intro h2{{font-size:52px;color:{GREEN};margin-top:18px;text-align:center}}
.intro .date{{font-size:34px;color:{MUTED};margin-top:22px}}
/* section */
.section{{background:{GREEN};color:{NAVY}}}
.section h1{{font-size:150px;font-weight:900;line-height:1.1;text-align:center}}
.section h2{{font-size:52px;margin-top:20px}}
.section .ball{{width:120px;height:120px;margin-bottom:30px}}
/* result */
.comp{{font-size:38px;color:{MUTED};margin-bottom:34px}}
.board{{width:100%;background:{NAVY2};border-radius:48px;padding:56px 70px;display:flex;flex-direction:column;gap:30px}}
.teams{{display:flex;align-items:center;justify-content:space-between}}
.team{{width:520px;display:flex;flex-direction:column;align-items:center;gap:20px}}
.crest{{width:150px;height:150px;border-radius:50%;background:{NAVY};border:6px solid {GREEN};display:flex;align-items:center;justify-content:center;font-size:72px;font-weight:900}}
.tname{{font-size:56px;font-weight:900;text-align:center;line-height:1.2}}
.score{{display:flex;align-items:center;gap:40px;font-size:230px;line-height:1}}
.score .dash{{font-size:120px;color:{GREEN}}}
.scorers{{display:flex;justify-content:space-between;border-top:4px solid #1F477F;padding-top:26px;font-size:36px}}
.scorers ul{{list-style:none;display:flex;flex-direction:column;gap:10px;width:46%}}
.scorers li{{display:flex;align-items:center;gap:14px}}
.scorers .ball{{width:34px;height:34px;flex:none}}
.scorers ul:last-child{{align-items:flex-end}}
.note{{margin-top:34px;background:{YELLOW};color:{NAVY};font-size:40px;font-weight:900;padding:12px 40px;border-radius:24px}}
/* headline */
.headline{{align-items:flex-start;justify-content:center}}
.headline .tag{{background:{YELLOW};color:{NAVY};font-size:44px;margin-bottom:36px}}
.headline .idx{{position:absolute;left:120px;top:190px;font-family:Outfit;font-weight:900;font-size:260px;color:{NAVY2};direction:ltr}}
.headline h1{{font-size:96px;font-weight:900;line-height:1.3;max-width:1500px;position:relative}}
.headline p{{font-size:48px;line-height:1.55;color:#DCE6F5;margin-top:30px;max-width:1500px;position:relative}}
.headline .bar{{width:220px;height:14px;border-radius:7px;background:{GREEN};margin-top:40px}}
/* table */
.table h1{{font-size:64px;font-weight:900;margin-bottom:30px;align-self:flex-start}}
.rows{{width:100%;display:flex;flex-direction:column;gap:14px}}
.row{{display:grid;grid-template-columns:110px 1fr 200px 200px;align-items:center;background:{NAVY2};border-radius:22px;padding:14px 36px;font-size:42px}}
.row.head{{background:transparent;color:{MUTED};font-size:30px;padding:0 36px}}
.row .pos{{font-family:Outfit;font-weight:900;color:{GREEN}}}
.row .c{{text-align:center}}
.row.hl{{background:{GREEN};color:{NAVY}}}
.row.hl .pos{{color:{NAVY}}}
/* stat */
.stat .big{{font-size:340px;color:{GREEN};line-height:1}}
.stat .label{{font-size:68px;font-weight:900;text-align:center;line-height:1.3;margin-top:20px;max-width:1500px}}
.stat .sub{{font-size:40px;color:{MUTED};margin-top:20px;text-align:center}}
/* list */
.list h1{{font-size:70px;font-weight:900;margin-bottom:36px;align-self:flex-start}}
.list ol{{list-style:none;width:100%;display:flex;flex-direction:column;gap:20px}}
.list li{{display:flex;align-items:center;gap:30px;background:{NAVY2};border-radius:24px;padding:18px 36px;font-size:46px}}
.list li .n{{font-family:Outfit;font-weight:900;color:{NAVY};background:{GREEN};width:70px;height:70px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none;font-size:40px}}
/* outro */
.outro .logo{{width:220px;height:220px;margin-bottom:30px}}
.outro h1{{font-size:96px;font-weight:900;text-align:center}}
.outro .cta{{background:{GREEN};color:{NAVY};font-size:54px;margin-top:36px}}
.outro .handles{{font-family:Outfit;font-size:40px;color:{MUTED};margin-top:30px;direction:ltr}}
@keyframes vis{{0%{{opacity:0}}100%{{opacity:1}}}}
@keyframes rise{{0%{{opacity:0;transform:translateY(60px)}}100%{{opacity:1;transform:none}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.6)}}70%{{opacity:1;transform:scale(1.06)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes slideR{{0%{{opacity:0;transform:translateX(120px)}}100%{{opacity:1;transform:none}}}}
@keyframes grow{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}
@keyframes drift{{0%{{transform:translate(0,0) rotate(0)}}100%{{transform:translate(-160px,90px) rotate(40deg)}}}}
@keyframes spin{{0%{{transform:rotate(0)}}100%{{transform:rotate(360deg)}}}}
@keyframes zoom{{0%{{transform:scale(1)}}100%{{transform:scale(1.08)}}}}
"""

MAJOR_CSS = f"""
@font-face{{font-family:Display;src:url({FONTS}/lalezar-arabic-400-normal.woff2) format('woff2');unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F}}
@font-face{{font-family:Display;src:url({FONTS}/anton-latin-400-normal.woff2) format('woff2');unicode-range:U+0000-024F,U+2000-206F}}
@font-face{{font-family:Anton;src:url({FONTS}/anton-latin-400-normal.woff2) format('woff2')}}
@font-face{{font-family:Mono;font-weight:700;src:url({FONTS}/space-mono-latin-700-normal.woff2) format('woff2')}}
html,body{{background:#050608;color:#E3F4FF}}
.bg-ring{{display:none}}
.glow{{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55}}
.bokeh{{position:absolute;border-radius:50%;background:#E3F4FF;filter:blur(6px);opacity:.10}}
.grain{{position:absolute;inset:-50px;opacity:.09;mix-blend-mode:overlay;pointer-events:none;z-index:8}}
.vignette{{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 45%,rgba(0,0,0,.75) 100%);z-index:7;pointer-events:none}}
.topbar{{position:absolute;top:40px;left:60px;right:60px;display:flex;align-items:center;justify-content:space-between;z-index:9;font-size:26px;color:#7F8B99}}
.topbar .brand{{display:flex;align-items:center;gap:14px;color:#E3F4FF;font-family:Display;font-size:44px;line-height:1}}
.topbar .brand .logo{{width:56px;height:56px}}
.topbar .mono{{font-family:Mono;font-size:20px;letter-spacing:2px;direction:ltr;color:#7F8B99}}
.bug,.ep{{display:none}}
.ghost{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:Display;font-size:560px;line-height:1;color:rgba(227,244,255,.05);white-space:nowrap;z-index:0;pointer-events:none}}
.progress{{position:absolute;left:60px;right:60px;bottom:40px;display:flex;gap:10px;z-index:9;direction:ltr}}
.progress .seg{{flex:1;height:4px;background:#22272E;overflow:hidden}}
.progress .fill{{height:100%;background:#00C853;transform-origin:left}}
.scene{{padding:150px 140px 120px;z-index:2}}
.photo{{position:absolute;inset:0;background-size:cover;background-position:center;filter:saturate(.9) contrast(1.08);z-index:0}}
.photo::after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,6,8,.25) 0%,rgba(5,6,8,.55) 45%,rgba(5,6,8,.92) 100%)}}
.src{{bottom:70px;right:140px;font-size:24px;color:#7F8B99}}
.num{{font-family:Anton;font-weight:400}}
.pill{{border-radius:4px;padding:8px 22px;font-weight:700}}
/* intro */
.intro .logo{{display:none}}
.intro h1{{font-family:Display;font-weight:400;font-size:220px;line-height:1.05;letter-spacing:0}}
.intro h2{{font-size:46px;color:#00C853;margin-top:26px;font-weight:700}}
.intro .date{{font-family:Cairo;font-size:30px;color:#7F8B99}}
/* section */
.section{{background:transparent;color:#E3F4FF}}
.section .ball{{display:none}}
.section h1{{font-family:Display;font-weight:400;font-size:260px;line-height:1.05}}
.section h2{{font-size:44px;color:#00C853;font-weight:700}}
/* result */
.comp{{font-size:32px;color:#00C853;margin-bottom:10px;font-weight:700}}
.board{{background:transparent;padding:0;gap:30px}}
.crest{{display:none}}
.tname{{font-family:Display;font-weight:400;font-size:96px;line-height:1.1}}
.team{{width:520px}}
.score{{font-size:330px;gap:44px}}
.score .dash{{font-size:150px;color:#00C853}}
.scorers{{border-top:2px solid #22272E;padding-top:26px;font-size:34px;font-weight:700}}
.scorers .ball{{width:26px;height:26px}}
.note{{background:#14181D;color:#E3F4FF;border-radius:4px;font-size:34px;padding:10px 30px;margin-top:30px}}
/* headline */
.headline .tag{{background:transparent;color:#00C853;border:2px solid #00C853;font-size:32px;margin-bottom:30px}}
.headline .idx{{font-family:Anton;font-size:520px;color:rgba(227,244,255,.06);top:120px;left:80px}}
.headline h1{{font-family:Display;font-weight:400;font-size:150px;line-height:1.12;max-width:1600px}}
.headline .bar{{background:#00C853;height:6px;border-radius:0;width:260px}}
.headline p{{font-size:44px;color:#B8C6D6;font-weight:700;max-width:1450px}}
/* table */
.table h1{{font-family:Display;font-weight:400;font-size:120px;margin-bottom:24px}}
.row{{background:transparent;border-bottom:2px solid #22272E;border-radius:0;padding:16px 10px;font-size:46px;font-weight:700}}
.row.head{{border-bottom:none;font-family:Mono;font-size:20px;letter-spacing:2px}}
.row .pos{{font-family:Mono;color:#7F8B99}}
.row.hl{{background:transparent;color:#00C853}}
.row.hl .pos{{color:#00C853}}
/* stat */
.stat .big{{font-family:Anton;font-size:460px;color:#E3F4FF}}
.stat .label{{font-family:Display;font-weight:400;font-size:96px}}
.stat .sub{{color:#00C853;font-weight:700}}
/* list (portfolio-index style) */
.list h1{{font-family:Display;font-weight:400;font-size:140px;margin-bottom:20px}}
.list ol{{gap:0}}
.list li{{background:transparent;border-radius:0;border-bottom:2px solid #22272E;padding:22px 6px;font-family:Display;font-size:76px;gap:40px}}
.list li .n{{background:transparent;color:#00C853;font-family:Mono;font-size:28px;width:auto;height:auto;letter-spacing:1px;direction:ltr}}
/* outro */
.outro .logo{{width:180px;height:180px}}
.outro h1{{font-family:Display;font-weight:400;font-size:170px}}
.outro .cta{{background:#00C853;color:#050608;font-size:48px}}
.outro .handles{{font-family:Mono;color:#7F8B99}}
"""

GRAIN = """<svg class="grain" xmlns="http://www.w3.org/2000/svg" width="2020" height="1180" aria-hidden="true"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""

DEFAULT_GHOST = {"intro": "KORA", "result": "FT", "stat": None, "outro": "KORA"}

e = html.escape


def anim(name, start, dur=0.6, ease="cubic-bezier(.2,.8,.2,1)"):
    return f"animation:{name} {dur:.3f}s {ease} {start:.3f}s both;"


def scene_vis(start, dur):
    """Fade the whole scene in and out using two stacked animations."""
    out_start = start + dur - FADE
    return (f"animation:vis {FADE}s linear {start:.3f}s both, "
            f"vis {FADE}s linear {out_start:.3f}s reverse forwards;")


THEME = "classic"
IMG_BASE = None  # folder that scene "image" paths are relative to (the storyboard folder)


def build_scene(s, t0, idx):
    typ, d = s["type"], float(s["duration"])
    a = lambda off, name="rise", dur=0.6: anim(name, t0 + off, dur)
    src = f'<div class="src in" style="{a(0.8, "vis")}">📌 المصدر: {e(s["source"])}</div>' if s.get("source") else ""
    if typ == "intro":
        body = (f'<div class="in" style="{a(0.1, "pop", 0.9)}">{LOGO}</div>'
                f'<h1 class="in" style="{a(0.6)}">{e(s["title"])}</h1>'
                + (f'<h2 class="in" style="{a(0.9)}">{e(s["subtitle"])}</h2>' if s.get("subtitle") else "")
                + (f'<div class="date in" style="{a(1.2)}">{e(s["date"])}</div>' if s.get("date") else ""))
    elif typ == "section":
        body = (f'<div class="in" style="{a(0.1, "pop", 0.7)}">{BALL}</div>'
                f'<h1 class="in" style="{a(0.3)}">{e(s["title"])}</h1>'
                + (f'<h2 class="in" style="{a(0.6)}">{e(s["subtitle"])}</h2>' if s.get("subtitle") else ""))
    elif typ == "result":
        def initial(name, short):
            if short:
                return short
            n = name.strip()
            return (n[2:] if n.startswith("ال") and len(n) > 2 else n)[:1]
        def team(name, off, short=None):
            return (f'<div class="team in" style="{a(off, "pop", 0.7)}"><div class="crest">{e(initial(name, short))}</div>'
                    f'<div class="tname">{e(name)}</div></div>')
        def sc(lst, off):
            items = "".join(f'<li class="in" style="{a(off + i * 0.25, "vis", 0.4)}">{BALL}<span>{e(x)}</span></li>' for i, x in enumerate(lst))
            return f"<ul>{items}</ul>"
        has_sc = s.get("scorers_home") or s.get("scorers_away")
        body = ((f'<div class="comp in" style="{a(0.1)}">{e(s["competition"])}</div>' if s.get("competition") else "")
                + f'<div class="board in" style="{a(0.2)}"><div class="teams">{team(s["home"], 0.4, s.get("home_short"))}'
                f'<div class="score num in" style="{a(0.9, "pop", 0.7)}"><span>{e(str(s["home_score"]))}</span><span class="dash">-</span><span>{e(str(s["away_score"]))}</span></div>'
                f'{team(s["away"], 0.6, s.get("away_short"))}</div>'
                + (f'<div class="scorers">{sc(s.get("scorers_home", []), 1.5)}{sc(s.get("scorers_away", []), 1.7)}</div>' if has_sc else "")
                + "</div>"
                + (f'<div class="note in" style="{a(2.2, "pop", 0.6)}">{e(s["note"])}</div>' if s.get("note") else ""))
    elif typ == "headline":
        body = ((f'<div class="idx in" style="{a(0.1, "vis", 0.8)}">{e(str(s["index"]))}</div>' if s.get("index") else "")
                + (f'<div class="pill tag in" style="{a(0.1, "slideR")}">{e(s["tag"])}</div>' if s.get("tag") else "")
                + f'<h1 class="in" style="{a(0.35)}">{e(s["title"])}</h1>'
                + f'<div class="bar" style="transform-origin:right;{a(0.7, "grow", 0.6)}"></div>'
                + (f'<p class="in" style="{a(0.9)}">{e(s["body"])}</p>' if s.get("body") else ""))
    elif typ == "table":
        cols = s.get("columns", ["#", "الفريق", "لعب", "نقاط"])
        head = f'<div class="row head in" style="{a(0.2, "vis")}">' + "".join(f'<span class="{"c" if i > 1 else ""}">{e(c)}</span>' for i, c in enumerate(cols)) + "</div>"
        rows = "".join(
            f'<div class="row {"hl" if r.get("highlight") else ""} in" style="{a(0.4 + i * 0.18, "slideR", 0.5)}">'
            f'<span class="pos">{e(str(r["pos"]))}</span><span>{e(r["team"])}</span>'
            f'<span class="c num">{e(str(r.get("played", "")))}</span><span class="c num">{e(str(r.get("points", "")))}</span></div>'
            for i, r in enumerate(s["rows"]))
        body = f'<h1 class="in" style="{a(0.1)}">{e(s["title"])}</h1><div class="rows">{head}{rows}</div>'
    elif typ == "stat":
        body = (f'<div class="big num ltr in" style="{a(0.2, "pop", 0.8)}">{e(str(s["value"]))}</div>'
                f'<div class="label in" style="{a(0.8)}">{e(s["label"])}</div>'
                + (f'<div class="sub in" style="{a(1.1)}">{e(s["sub"])}</div>' if s.get("sub") else ""))
    elif typ == "list":
        items = "".join(f'<li class="in" style="{a(0.5 + i * 0.35, "slideR", 0.5)}"><span class="n">{("#%02d" % (i + 1)) if THEME == "major" else (i + 1)}</span><span>{e(x)}</span></li>' for i, x in enumerate(s["items"]))
        body = f'<h1 class="in" style="{a(0.1)}">{e(s["title"])}</h1><ol>{items}</ol>'
    elif typ == "outro":
        body = (f'<div class="in" style="{a(0.1, "pop", 0.9)}">{KK_LOGO if THEME == "major" else LOGO}</div>'
                f'<h1 class="in" style="{a(0.5)}">{e(s.get("title", "شكراً للمشاهدة"))}</h1>'
                f'<div class="pill cta in" style="{a(0.9, "pop", 0.6)}">{e(s.get("cta", "اشترك وفعّل الجرس 🔔"))}</div>'
                + (f'<div class="handles in" style="{a(1.3)}">{e(s["handles"])}</div>' if s.get("handles") else ""))
    else:
        raise ValueError(f"unknown scene type: {typ}")
    ghost = ""
    if THEME == "major":
        word = s.get("ghost", DEFAULT_GHOST.get(typ, s.get("title")))
        if word:
            ghost = f'<div class="ghost in" style="{a(0.0, "vis", 1.2)}"><span style="display:inline-block;{anim("zoom", t0, d, "linear")}">{e(str(word))}</span></div>'
    photo = ""
    if s.get("image"):
        uri = (IMG_BASE / s["image"]).resolve().as_uri() if IMG_BASE else s["image"]
        photo = f'<div class="photo" style="background-image:url(\'{uri}\');{anim("zoom", t0, d, "linear")}"></div>'
    return f'<section class="scene {typ}" style="{scene_vis(t0, d)}">{photo}{ghost}{body}{src}</section>'


def build_html(sb, theme=None):
    global THEME
    THEME = theme or sb.get("theme", "major")
    t, scenes = 0.0, []
    for i, s in enumerate(sb["scenes"]):
        scenes.append(build_scene(s, t, i))
        t += float(s["duration"])
    total = t
    rings = "".join(
        f'<div class="bg-ring" style="width:{r}px;height:{r}px;left:{x}px;top:{y}px;animation:drift {total:.2f}s linear 0s both"></div>'
        for r, x, y in [(900, -300, 420), (520, 1500, -180), (300, 1250, 820)])
    ep = f'<div class="ep">{e(sb["episode"])}</div>' if sb.get("episode") else ""
    bug = ('<div class="bug"><div><div class="name">كورة كليكس</div><div class="en">KORA KLICKS</div></div>'
           f'{LOGO}</div>')
    extra_css, extra = "", ""
    if THEME == "major":
        extra_css = MAJOR_CSS
        glows = "".join(
            f'<div class="glow" style="width:{w}px;height:{w}px;left:{x}px;top:{y}px;background:{c};animation:drift {total:.2f}s linear 0s both"></div>'
            for w, x, y, c in [(900, -250, 520, "#00C85333"), (700, 1350, -260, "#2E6BFF2B"), (420, 760, 820, "#E3F4FF14")])
        bokeh = "".join(
            f'<div class="bokeh" style="width:{r}px;height:{r}px;left:{x}px;top:{y}px;animation:drift {total:.2f}s linear 0s both"></div>'
            for r, x, y in [(90, 1580, 160), (60, 1720, 330), (120, 140, 120), (50, 300, 900), (80, 1400, 880), (40, 980, 120)])
        n = len(sb["scenes"])
        segs, t2 = "", 0.0
        for s_ in sb["scenes"]:
            dd = float(s_["duration"])
            segs += f'<div class="seg"><div class="fill" style="animation:grow {dd:.3f}s linear {t2:.3f}s both"></div></div>'
            t2 += dd
        # scene counter "01 / 09" that changes with each scene
        counters, st = "", 0.0
        for i, sc_ in enumerate(sb["scenes"]):
            dd = float(sc_["duration"])
            counters += (f'<span style="position:absolute;left:0;opacity:0;animation:vis .01s linear {st:.3f}s both, '
                         f'vis .01s linear {st + dd - 0.01:.3f}s reverse forwards;">{i + 1:02d} / {n:02d}</span>')
            st += dd
        label = e(sb.get("episode", ""))
        extra = (f'{glows}{bokeh}<div class="vignette"></div>{GRAIN}'
                 f'<div class="topbar"><div class="brand">{KK_LOGO}<span>كورة كليكس</span></div>'
                 f'<div>{label}</div><div class="mono" style="position:relative;width:150px;height:28px">{counters}</div></div>'
                 f'<div class="progress">{segs}</div>')
    doc = (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{CSS}{extra_css}</style></head>'
           f'<body><div class="stage">{rings}{bug}{ep}{extra}{"".join(scenes)}</div>'
           '<script>window.seek=t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000;});};</script>'
           '</body></html>')
    return doc, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("out_dir")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--theme", choices=["classic", "major"], help="visual style; default from storyboard 'theme' or major")
    args = ap.parse_args()
    fps = 12 if args.preview else args.fps

    sb = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
    out = Path(args.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    slug = sb.get("slug", "kora-klicks-video")
    global IMG_BASE
    IMG_BASE = Path(args.storyboard).resolve().parent
    doc, total = build_html(sb, args.theme)
    page_path = out / f"{slug}.html"
    page_path.write_text(doc, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    video = out / (f"{slug}-preview.mp4" if args.preview else f"{slug}.mp4")
    silent = out / f"{slug}-silent.mp4"
    n = int(round(total * fps))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps),
                           "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
                           "-crf", "20", "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
    launch = {}
    if os.path.exists("/opt/pw-browsers/chromium"):
        launch["executable_path"] = "/opt/pw-browsers/chromium"
    with sync_playwright() as p:
        try:
            br = p.chromium.launch(**launch)
        except Exception:
            br = p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto(page_path.as_uri())
        pg.evaluate("document.fonts.ready")
        for i in range(n):
            pg.evaluate(f"seek({i / fps})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
            if i % (fps * 10) == 0:
                print(f"frame {i}/{n}", file=sys.stderr)
        # thumbnail: the moment the intro is fully built
        pg.evaluate(f"seek({min(2.5, total / 2)})")
        pg.screenshot(path=str(out / f"{slug}-thumbnail.jpg"), type="jpeg", quality=92)
        br.close()
    ff.stdin.close(); ff.wait()
    if ff.returncode != 0:
        sys.exit("ffmpeg failed")

    audio = sb.get("audio")
    if audio:
        apath = (Path(args.storyboard).parent / audio).resolve()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(apath), "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-shortest", str(video)], check=True)
        silent.unlink()
    else:
        shutil.move(silent, video)

    # contact sheet for review: one frame every ~3 s, 5 columns
    step = max(1.0, total / 25)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf",
                    f"fps=1/{step:.2f},scale=384:-1,tile=5x5:padding=6:color=white", "-frames:v", "1",
                    str(out / f"{slug}-contact-sheet.jpg")], check=True)
    print(json.dumps({"video": str(video), "duration_s": round(total, 1), "frames": n,
                      "thumbnail": str(out / f"{slug}-thumbnail.jpg"),
                      "contact_sheet": str(out / f"{slug}-contact-sheet.jpg")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
