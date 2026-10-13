#!/usr/bin/env python3
"""Kora Klicks motion-graphics short (1080x1920): kinetic text, versus slams, count-ups,
meme formats (expectation vs reality, «لما…», fan-group chat, POV), lists and a CTA,
on original music from music.py with beat-synced camera punches, flashes and pops.
Two looks that live side by side: --theme dark (cinematic, nights/results) and
--theme light (bright, daytime previews/memes/tables).

  python3 motion_short.py spec.json OUT_DIR [--theme dark|light] [--fps 30] [--bpm 124] [--mood fun|drive|anthem|dark]

spec.json:
{
  "slug": "ucl-md2-city-psg",
  "theme": "light",                         # optional, CLI --theme wins
  "mood": "fun",                            # optional, CLI --mood wins
  "label": "UCL · MD2",                     # small Latin label top-left
  "ghost": "UCL",                           # giant faint background word (Latin)
  "source": "المصدر: uefa.com",
  "cover": 1,                               # scene index used for the cover JPG (default 1)
  "scenes": [
    {"type": "hook",   "text": "ليلة نار في دوري الأبطال", "sub": "الأربع 10 بالليل", "emoji": "🔥"},
    {"type": "versus", "comp": "دوري الأبطال · الجولة 2", "home": "مانشستر سيتي", "away": "باريس سان جيرمان",
                       "time": "22:00", "home_star": "مرموش", "away_star": "حكيمي", "note": "بتوقيت القاهرة"},
    {"type": "score",  "comp": "...", "home": "...", "away": "...", "home_score": 2, "away_score": 1, "note": "..."},
    {"type": "stat",   "big": "8", "line": "أهداف في آخر 3 مواجهات", "note": "..."},
    {"type": "expect", "top": "أنا قبل الماتش", "top_emoji": "😎", "bottom": "أنا في الدقيقة 90", "bottom_emoji": "😵‍💫"},
    {"type": "when",   "text": "لما الماتش 10 بالليل وعندك شغل الصبح", "emoji": "🥲", "sub": "بس هنتفرج برضه"},
    {"type": "chat",   "title": "جروب الشلة ⚽", "messages": [{"from": "أحمد", "text": "...", "side": "r"}, ...]},
    {"type": "pov",    "text": "POV: ...", "emoji": "👀"},
    {"type": "list",   "title": "عرب الليلة", "rows": [{"name": "حكيمي", "club": "باريس", "emoji": "🇲🇦"}]},
    {"type": "cta",    "text": "توقعاتكم إيه؟", "sub": "اكتبوها في الكومنتات"}
  ]
}
Writes <slug>-short.mp4 and <slug>-cover.jpg (vertical still of the cover scene, usable as a Story).

Rules: memes are original typographic/emoji jokes about the fan experience. Never mock a club, player or
fan base, no film/series stills or other people's images, no crests, no betting. Chat names are invented
first names (generic), never real people. Facts on screen (times, scores, numbers) need sources like any post.
"""
import argparse, json, subprocess, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "assets" / "fonts"
LOGO_DIR = HERE.parent.parent.parent / "assets" / "logo"
W, H = 1080, 1920
E = html.escape

THEMES = {
    "dark": dict(bg="#050608", bg2="#0e1c27", bg3="#050608", fg="#E3F4FF", mute="#8A97A3", acc="#00C853", acc2="#5AC8FA",
                 line="#22272E", card="#0d1218", cardb="#1b232c", ghost="#0f1419", shadow="none", bub="#14202b", bub2="#00C853",
                 bub2fg="#03110a", flash="#ffffff", logo="kora-klicks-wordmark-transparent-ice.svg"),
    "light": dict(bg="#F3F8FC", bg2="#DDF5E7", bg3="#DCEBFA", fg="#0B1620", mute="#5B6B7A", acc="#00A84F", acc2="#2F80ED",
                  line="#D5E0EA", card="#FFFFFF", cardb="#E3ECF4", ghost="#E6EFF7", shadow="0 18px 50px rgba(20,60,90,.12)",
                  bub="#FFFFFF", bub2="#00A84F", bub2fg="#ffffff", flash="#ffffff", logo="kora-klicks-wordmark-transparent-black.svg"),
}

DUR = {"hook": 1.9, "versus": 3.9, "score": 3.9, "stat": 3.9, "expect": 5.8, "when": 3.9, "pov": 3.9, "cta": 3.9}

CSS = """
@font-face{font-family:LZ;src:url(FONTS/lalezar-arabic-400-normal.woff2)}
@font-face{font-family:AN;src:url(FONTS/anton-latin-400-normal.woff2)}
@font-face{font-family:SM;src:url(FONTS/space-mono-latin-700-normal.woff2)}
@font-face{font-family:CA;src:url(FONTS/cairo-arabic-800-normal.woff2)}
@font-face{font-family:CA;src:url(FONTS/cairo-latin-900-normal.woff2);unicode-range:U+0000-00FF}
EMOJICSS
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg);color:var(--fg)}
:root{VARS}
.stage{position:absolute;inset:0;transform-origin:50% 50%}
.bg{position:absolute;inset:-60px;background:radial-gradient(ellipse at 20% 15%,var(--bg2) 0%,transparent 55%),radial-gradient(ellipse at 85% 80%,var(--bg3) 0%,transparent 55%),var(--bg)}
.stripes{position:absolute;inset:-400px;opacity:.07;background:repeating-linear-gradient(-35deg,var(--acc) 0 4px,transparent 4px 90px)}
.orb{position:absolute;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,var(--acc) 0%,transparent 70%);opacity:.10}
.ghost{position:absolute;left:50%;top:52%;font-family:AN;font-size:330px;line-height:.8;color:var(--ghost);white-space:nowrap}
.top{position:absolute;top:150px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.top img{height:54px}
.lab{font-family:SM;font-size:24px;letter-spacing:.22em;color:var(--acc)}
.bars{position:absolute;top:110px;left:80px;right:80px;display:flex;gap:10px;z-index:5}
.bars i{flex:1;height:6px;background:var(--line);border-radius:3px;overflow:hidden;position:relative}
.bars i b{position:absolute;inset:0;width:0;background:var(--fg)}
.foot{position:absolute;bottom:160px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid var(--line);padding-top:28px;z-index:5}
.foot .h{font-family:SM;font-size:24px;color:var(--mute)}
.foot .s{font-family:CA;font-size:28px;color:var(--mute);direction:rtl}
.flash{position:absolute;inset:0;background:var(--flash);opacity:0;z-index:9;pointer-events:none}
.scene{position:absolute;inset:0;opacity:0}
.c{position:absolute;left:80px;right:80px;direction:rtl;text-align:right}
.a{will-change:transform,opacity}
.chip{display:inline-block;font-family:CA;font-size:36px;padding:10px 30px;border-radius:999px;background:var(--acc);color:#fff}
.huge{font-family:LZ,EM;font-size:168px;line-height:1.08}
.huge .w{display:inline-block;margin-left:26px}
.sub{font-family:CA,EM;font-size:52px;color:var(--mute);margin-top:26px}
.emo{font-family:EM;font-size:230px;line-height:1;display:inline-block}
.comp{font-family:CA;font-size:40px;color:var(--mute)}
.card{background:var(--card);border:2px solid var(--cardb);border-radius:40px;box-shadow:var(--shadow);padding:44px 50px}
.vs-wrap{position:relative;margin-top:44px}
.vs-wrap .card + .card{margin-top:150px}
.tn{font-family:LZ;font-size:110px;line-height:1.1}
.star{font-family:CA,EM;font-size:40px;color:var(--acc);margin-top:6px}
.vs{position:absolute;left:50%;top:50%;width:170px;height:170px;margin:-85px 0 0 -85px;border-radius:50%;background:var(--acc);color:#fff;
    font-family:AN;font-size:84px;line-height:170px;text-align:center;direction:ltr;z-index:3;box-shadow:0 0 0 14px var(--bg)}
.tm{font-family:AN;font-size:200px;line-height:1;direction:ltr;text-align:right;margin-top:20px}
.note{font-family:CA,EM;font-size:40px;color:var(--mute);margin-top:22px}
.ln{display:flex;justify-content:space-between;align-items:center;direction:rtl;padding:18px 0}
.ln + .ln{border-top:2px solid var(--line)}
.ln .tn{font-size:100px}
.sc{font-family:AN;font-size:190px;line-height:1;color:var(--fg)}
.fig{font-family:AN;font-size:330px;line-height:1;color:var(--acc);direction:ltr;text-align:right}
.fl{font-family:LZ,EM;font-size:80px;line-height:1.2;margin-top:10px}
.panel{position:relative;height:520px;display:flex;align-items:center;justify-content:space-between;gap:30px}
.panel + .panel{margin-top:40px}
.panel .cap{font-family:LZ,EM;font-size:84px;line-height:1.15;flex:1}
.panel .emo{font-size:250px}
.panel.bad{background:var(--acc2);color:#fff;border-color:transparent}
.tag{position:absolute;top:-26px;right:40px;font-family:SM;font-size:26px;letter-spacing:.2em;padding:8px 18px;border-radius:10px;background:var(--fg);color:var(--bg);direction:ltr}
.phone{background:var(--card);border:2px solid var(--cardb);border-radius:56px;box-shadow:var(--shadow);overflow:hidden}
.phone .hd{display:flex;align-items:center;gap:22px;padding:30px 40px;border-bottom:2px solid var(--line);font-family:CA,EM;font-size:42px;direction:rtl}
.phone .av{width:76px;height:76px;border-radius:50%;background:var(--acc);display:flex;align-items:center;justify-content:center;font-family:EM;font-size:44px}
.phone .bd{padding:30px 34px 40px;display:flex;flex-direction:column;gap:24px;min-height:860px}
.bb{max-width:80%;padding:22px 30px;border-radius:34px;font-family:CA,EM;font-size:44px;line-height:1.35;background:var(--bub);border:2px solid var(--cardb)}
.bb .nm{display:block;font-size:28px;color:var(--acc2)}
.bb.r{align-self:flex-start;border-top-right-radius:8px}
.bb.l{align-self:flex-end;background:var(--bub2);color:var(--bub2fg);border-color:transparent;border-top-left-radius:8px}
.bb.l .nm{color:inherit;opacity:.75}
.row{display:flex;align-items:center;justify-content:space-between;padding:26px 36px;margin-top:22px}
.row .nm{font-family:LZ;font-size:80px}
.row .cl{font-family:CA,EM;font-size:44px;color:var(--mute)}
.row .e{font-family:EM;font-size:70px;margin-left:26px}
.arrow{font-family:EM;font-size:120px;display:inline-block;margin-top:40px}
""".replace("FONTS", FONTS.as_uri())


def emoji_css():
    # bundled Noto Color Emoji (CBDT, OFL); the woff2 COLRv1 builds render blank in headless Chromium
    return "@font-face{font-family:EM;src:url(%s)}" % (FONTS / "emoji" / "NotoColorEmoji.ttf").as_uri()


def A(kind, delay=0.0, extra="", tag="div", cls="", inner=""):
    return f'<{tag} class="a {cls}" data-a="{kind}" data-d="{delay}" {extra}>{inner}</{tag}>'


def words(text, start=0.05, step=0.12):
    return "".join(A("pop", start + i * step, tag="span", cls="w", inner=E(w)) for i, w in enumerate(text.split()))


def scene_html(s):
    t = s["type"]
    if t == "hook":
        return (f'<div class=c style="top:470px">'
                f'{A("up", 0, inner="<span class=chip>"+E(s["chip"])+"</span>") if s.get("chip") else ""}'
                f'<div class=huge style="margin-top:30px">{words(s["text"])}</div>'
                f'{A("up", 0.5, cls="sub", inner=E(s["sub"])) if s.get("sub") else ""}'
                f'{A("bounce", 0.35, extra="style=margin-top:40px", inner="<span class=emo>"+E(s["emoji"])+"</span>") if s.get("emoji") else ""}</div>')
    if t == "versus":
        hs = f'<div class=star>⭐ {E(s["home_star"])}</div>' if s.get("home_star") else ""
        as_ = f'<div class=star>⭐ {E(s["away_star"])}</div>' if s.get("away_star") else ""
        return (f'<div class=c style="top:400px">{A("up", 0, cls="comp", inner=E(s.get("comp","")))}'
                f'<div class=vs-wrap>{A("right", 0.05, cls="card", inner="<div class=tn>"+E(s["home"])+"</div>"+hs)}'
                f'{A("left", 0.2, cls="card", inner="<div class=tn>"+E(s["away"])+"</div>"+as_)}'
                f'{A("slam", 0.45, cls="vs", inner="VS")}</div>'
                f'{A("up", 0.8, cls="tm", inner=E(s.get("time",""))) if s.get("time") else ""}'
                f'{A("up", 1.0, cls="note", inner=E(s["note"])) if s.get("note") else ""}</div>')
    if t == "score":
        def ln(team, sc, d):
            return A("right", d, cls="ln", inner=f'<span class=tn>{E(team)}</span>'
                     f'<span class="sc a" data-a="count" data-d="{d + 0.3}" data-n="{int(sc)}">0</span>')
        return (f'<div class=c style="top:470px">{A("up", 0, cls="comp", inner=E(s.get("comp","")))}'
                f'<div class=card style="margin-top:36px;padding:20px 50px">{ln(s["home"], s["home_score"], 0.1)}{ln(s["away"], s["away_score"], 0.25)}</div>'
                f'{A("up", 1.0, cls="note", inner=E(s["note"])) if s.get("note") else ""}</div>')
    if t == "stat":
        big = str(s["big"])
        fig = (f'<div class="fig a" data-a="count" data-d="0.1" data-n="{big}">0</div>' if big.isdigit()
               else A("slam", 0.1, cls="fig", inner=E(big)))
        return (f'<div class=c style="top:470px">{A("up", 0, cls="comp", inner=E(s.get("comp","")))}{fig}'
                f'{A("up", 0.5, cls="fl", inner=E(s.get("line","")))}'
                f'{A("up", 0.8, cls="note", inner=E(s["note"])) if s.get("note") else ""}</div>')
    if t == "expect":
        top = (f'<span class=tag>EXPECTATION</span><div class=cap>{E(s["top"])}</div>'
               f'<span class="emo a" data-a="bounce" data-d="0.4">{E(s.get("top_emoji",""))}</span>')
        bot = (f'<span class=tag>REALITY</span><div class=cap>{E(s["bottom"])}</div>'
               f'<span class="emo a" data-a="bounce" data-d="{s.get("_half", 2.9) + 0.35}">{E(s.get("bottom_emoji",""))}</span>')
        return (f'<div class=c style="top:330px">{A("right", 0.05, cls="card panel", inner=top)}'
                f'{A("shake", s.get("_half", 2.9), cls="card panel bad", inner=bot)}</div>')
    if t in ("when", "pov"):
        chip = "POV" if t == "pov" else None
        return (f'<div class=c style="top:430px">'
                f'{A("up", 0, inner="<span class=chip style=font-family:SM;letter-spacing:.2em>"+chip+"</span>") if chip else ""}'
                f'<div class=huge style="font-size:118px;margin-top:30px">{words(s["text"], 0.05, 0.09)}</div>'
                f'{A("bounce", 0.9, extra="style=margin-top:50px;text-align:center", inner="<span class=emo style=font-size:300px>"+E(s.get("emoji",""))+"</span>") if s.get("emoji") else ""}'
                f'{A("up", 1.3, cls="sub", inner=E(s["sub"])) if s.get("sub") else ""}</div>')
    if t == "chat":
        bubbles = "".join(A("bubble", 0.45 + i * s.get("_gap", 1.0), cls=f'bb {"l" if m.get("side","r")=="l" else "r"}',
                            inner=f'<span class=nm>{E(m.get("from",""))}</span>{E(m["text"])}')
                          for i, m in enumerate(s["messages"]))
        return (f'<div class=c style="top:300px">{A("up", 0, cls="phone", inner="<div class=hd><span class=av>⚽</span>"+E(s.get("title","جروب الشلة"))+"</div><div class=bd>"+bubbles+"</div>")}</div>')
    if t == "list":
        rows = "".join(A("right", 0.35 + i * 0.22, cls="card row",
                         inner=f'<span><span class=e>{E(r.get("emoji",""))}</span><span class=nm>{E(r["name"])}</span></span><span class=cl>{E(r.get("club",""))}</span>')
                       for i, r in enumerate(s["rows"]))
        return (f'<div class=c style="top:380px"><div class=huge style="font-size:140px">{words(s["title"])}</div>'
                f'{A("up", 0.2, cls="note", inner=E(s["sub"])) if s.get("sub") else ""}{rows}</div>')
    if t == "cta":
        return (f'<div class=c style="top:640px"><div class=huge style="color:var(--acc);font-size:170px">{words(s["text"])}</div>'
                f'{A("up", 0.5, cls="sub", inner=E(s.get("sub","")))}'
                f'{A("up", 0.8, cls="sub", extra="style=font-family:SM;font-size:40px;color:var(--fg);direction:ltr;text-align:right;margin-top:60px", inner="FOLLOW @koraklicks")}'
                f'{A("bounce", 1.0, inner="<span class=arrow>👇</span>")}</div>')
    raise SystemExit(f"unknown scene type {t}")


def base_duration(s):
    t = s["type"]
    if t == "chat":
        return 1.2 + s.get("_gap", 1.0) * len(s["messages"]) + 0.8
    if t == "list":
        return 1.6 + 0.4 * len(s["rows"]) + 1.0
    return float(s.get("duration", DUR.get(t, 3.9)))


def build_html(spec, theme, durs):
    th = THEMES[theme]
    vars_ = ";".join(f"--{k}:{v}" for k, v in th.items() if k != "logo")
    css = CSS.replace("EMOJICSS", emoji_css()).replace("VARS", vars_)
    wm = (LOGO_DIR / th["logo"]).as_uri()
    scenes = "".join(f'<div class=scene>{scene_html(s)}</div>' for s in spec["scenes"])
    bars = "".join("<i><b></b></i>" for _ in durs)
    js = """<script>
const D=%s, T=D.reduce((a,b)=>a+b,0), BEAT=%f;
const S=[...document.querySelectorAll('.scene')], B=[...document.querySelectorAll('.bars b')];
const G=document.getElementById('ghost'), ST=document.getElementById('stage'), F=document.getElementById('flash'),
      STR=document.getElementById('stripes'), O1=document.getElementById('o1'), O2=document.getElementById('o2');
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3);
const back=x=>{x=cl(x);const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
window.render=t=>{let s=0,acc=0;while(s<D.length-1&&t>=acc+D[s]){acc+=D[s];s++}const u=t-acc,d=D[s];
 S.forEach(el=>el.style.opacity=0);const el=S[s];
 el.style.opacity=s<D.length-1?cl((d-u)/0.15):1;
 el.querySelectorAll('.a').forEach(k=>{const dl=+k.dataset.d||0,p=(u-dl),kind=k.dataset.a;let o=1,tr='';
  if(kind==='up'){o=eo(p/0.45);tr=`translateY(${(1-eo(p/0.45))*80}px)`}
  else if(kind==='pop'){o=cl(p/0.12);tr=`scale(${0.2+0.8*back(p/0.38)})`}
  else if(kind==='right'){o=cl(p/0.2);tr=`translateX(${(1-eo(p/0.5))*900}px)`}
  else if(kind==='left'){o=cl(p/0.2);tr=`translateX(${-(1-eo(p/0.5))*900}px)`}
  else if(kind==='slam'){o=cl(p/0.08);tr=`scale(${p<0?3:1+2*Math.pow(1-cl(p/0.22),2)}) rotate(${(1-cl(p/0.22))*-12}deg)`}
  else if(kind==='bounce'){o=cl(p/0.1);const b=p<0?0:Math.abs(Math.sin(p*6))*Math.exp(-p*2.4);tr=`scale(${0.3+0.7*back(p/0.45)}) translateY(${-b*60}px)`}
  else if(kind==='bubble'){o=cl(p/0.1);tr=`scale(${0.4+0.6*back(p/0.3)})`;k.style.transformOrigin=k.classList.contains('l')?'0%% 0%%':'100%% 0%%'}
  else if(kind==='shake'){o=cl(p/0.06);const a=p<0?0:Math.exp(-p*5);tr=`translateX(${Math.sin(p*70)*28*a}px) rotate(${Math.sin(p*55)*2.5*a}deg) scale(${1+0.12*a})`}
  else if(kind==='count'){o=cl(p/0.1);const n=+k.dataset.n;k.textContent=Math.round(n*eo(p/0.8));tr=`scale(${1+0.25*Math.exp(-Math.max(p-0.8,0)*8)*(p>0.8?1:0)})`}
  k.style.opacity=o;k.style.transform=tr;});
 const bp=(t%%BEAT)/BEAT, punch=t<D[0]?0:Math.exp(-bp*9);
 ST.style.transform=`scale(${1+0.012*punch})`;
 F.style.opacity=(s>0&&u<0.18)?0.35*(1-u/0.18):0;
 B.forEach((b,i)=>{b.style.width=(i<s?100:i>s?0:Math.min(100,u/d*100))+'%%'});
 G.style.transform=`translate(${-50-6*t/T}%%,-50%%)`;
 STR.style.transform=`translateX(${(t*40)%%90}px)`;
 O1.style.transform=`translate(${120+Math.sin(t*0.7)*80}px,${300+Math.cos(t*0.5)*60}px)`;
 O2.style.transform=`translate(${520+Math.cos(t*0.6)*90}px,${1300+Math.sin(t*0.8)*70}px)`;};
render(0);</script>""" % (json.dumps(durs), 60.0 / spec["_bpm"])
    return (f'<html><head><meta charset=utf-8><style>{css}</style></head><body><div class=stage id=stage>'
            f'<div class=bg></div><div class=stripes id=stripes></div><div class=orb id=o1></div><div class=orb id=o2></div>'
            f'<div class=ghost id=ghost>{E(spec.get("ghost",""))}</div>'
            f'<div class=bars>{bars}</div><div class=top><img src="{wm}"><span class=lab>{E(spec.get("label",""))}</span></div>'
            f'{scenes}<div class=foot><span class=h>@koraklicks</span><span class=s>{E(spec.get("source",""))}</span></div></div>'
            f'<div class=flash id=flash></div>{js}</body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out_dir")
    ap.add_argument("--theme", choices=list(THEMES)); ap.add_argument("--mood")
    ap.add_argument("--fps", type=int, default=30); ap.add_argument("--bpm", type=float, default=124)
    ap.add_argument("--preview", action="store_true", help="only write <slug>-sheet.jpg (one frame per scene) to check the layout fast")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    theme = a.theme or spec.get("theme", "dark")
    mood = a.mood or spec.get("mood", "fun" if theme == "light" else "drive")
    spec["_bpm"] = a.bpm
    out = Path(a.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    slug = spec["slug"]

    # storyboard for music.py: durations + sfx per scene (pops for chat bubbles / meme reveals)
    sb_scenes = []
    for s in spec["scenes"]:
        t = s["type"]
        sc = {"type": t, "duration": base_duration(s),
              "sfx": "pop" if t in ("chat", "when", "pov", "list") else ("whoosh" if t in ("expect", "cta") else "impact")}
        if t == "chat":
            sc["pops"] = [0.45 + i * s.get("_gap", 1.0) for i in range(len(s["messages"]))]
        if t == "versus":
            sc["pops"] = [0.45]
        sb_scenes.append(sc)
    sb = out / f"{slug}-sb.json"
    sb.write_text(json.dumps({"slug": slug, "scenes": sb_scenes}))
    subprocess.run([sys.executable, str(HERE / "music.py"), str(sb), str(out), "--bpm", str(a.bpm), "--mood", mood, "--grid", "1"],
                   check=True, stdout=subprocess.DEVNULL)
    durs = [s["duration"] for s in json.loads((out / f"{slug}-timed.json").read_text())["scenes"]]
    for s, d in zip(spec["scenes"], durs):  # the reality panel lands in the middle of the snapped scene
        if s["type"] == "expect":
            s["_half"] = round(d / 2, 2)
    music = out / f"{slug}-music.wav"

    from playwright.sync_api import sync_playwright
    frames = out / f"{slug}-frames"; frames.mkdir(exist_ok=True)
    for f in frames.glob("*.jpg"):
        f.unlink()
    page = out / f"{slug}-motion.html"
    page.write_text(build_html(spec, theme, durs), encoding="utf-8")
    total = sum(durs); nf = int(round(total * a.fps))
    ci = min(int(spec.get("cover", 1)), len(durs) - 1)
    cover_t = sum(durs[:ci]) + durs[ci] * 0.8
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(page.as_uri()); pg.wait_for_timeout(300)
        pg.evaluate("document.fonts.ready.then(()=>1)")
        pg.evaluate("Promise.all([...document.fonts].map(f=>f.load().catch(()=>0)))")
        pg.wait_for_timeout(700)
        if a.preview:
            shots = []
            for k in range(len(durs)):
                pg.evaluate(f"render({sum(durs[:k]) + durs[k] * 0.85})")
                shots.append(str(out / f"{slug}-p{k}.jpg")); pg.screenshot(path=shots[-1], type="jpeg", quality=85)
            b.close()
            inputs = sum((["-i", x] for x in shots), [])
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex",
                            "".join(f"[{i}]" for i in range(len(shots))) + f"hstack={len(shots)},scale=-1:900",
                            str(out / f"{slug}-sheet.jpg")], check=True)
            print(json.dumps({"sheet": str(out / f"{slug}-sheet.jpg")})); return
        pg.evaluate(f"render({cover_t})")
        pg.screenshot(path=str(out / f"{slug}-cover.jpg"), type="jpeg", quality=92)
        for i in range(nf):
            pg.evaluate(f"render({i / a.fps})")
            pg.screenshot(path=str(frames / f"{i:05d}.jpg"), type="jpeg", quality=88)
        b.close()
    mp4 = out / f"{slug}-short.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(a.fps), "-i", str(frames / "%05d.jpg"),
                    "-i", str(music), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(mp4)], check=True)
    print(json.dumps({"short": str(mp4), "cover": str(out / f"{slug}-cover.jpg"), "theme": theme, "mood": mood,
                      "duration_s": round(total, 2), "scene_durations": durs}, ensure_ascii=False))


if __name__ == "__main__":
    main()
