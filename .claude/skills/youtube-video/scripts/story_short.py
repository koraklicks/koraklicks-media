#!/usr/bin/env python3
"""Kora Klicks vertical story + short (1080x1920) in the cinematic "major" look.

  python3 story_short.py spec.json OUT_DIR [--fps 30] [--bpm 124] [--mood drive]

spec.json:
{
  "slug": "big-day-2026-10-11",
  "kind": "fixtures" | "results",
  "label": "MATCHDAY · SUN 11 OCT",          # small mono label (Latin)
  "title": "يوم الكبار",                      # big Arabic title
  "subtitle": "قمتين النهارده",               # optional
  "ghost": "BIG DAY",                         # giant faint background word (Latin)
  "items": [                                  # 1-5 matches
    {"comp": "الدوري الإنجليزي · أنفيلد", "home": "ليفربول", "away": "مانشستر سيتي",
     "time": "18:30",                         # fixtures
     "home_score": 2, "away_score": 1,        # results (instead of time)
     "note": "بتوقيت القاهرة"}
  ],
  "cta": "توقعاتكم إيه؟", "cta_sub": "اكتبوا النتيجة في الكومنتات",
  "source": "المصدر: بوابة الأهرام · مانشستر سيتي"
}

Writes <slug>-story.jpg (one still with all matches) and <slug>-short.mp4
(intro + one scene per match + outro, original music from music.py, cuts on the beat).
"""
import argparse, json, subprocess, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "assets" / "fonts"
LOGO_DIR = HERE.parent.parent.parent / "assets" / "logo"
W, H = 1080, 1920
E = html.escape

CSS = """
@font-face{font-family:LZ;src:url(FONTS/lalezar-arabic-400-normal.woff2)}
@font-face{font-family:AN;src:url(FONTS/anton-latin-400-normal.woff2)}
@font-face{font-family:SM;src:url(FONTS/space-mono-latin-700-normal.woff2)}
@font-face{font-family:CA;src:url(FONTS/cairo-arabic-800-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#050608;color:#E3F4FF}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 42%,#0e1c27 0%,#050608 64%)}
.grain{position:absolute;inset:0;opacity:.06;background-image:repeating-radial-gradient(circle at 17% 23%,#fff 0 1px,transparent 1px 3px)}
.top{position:absolute;top:150px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center}
.top img{height:56px}
.lab{font-family:SM;font-size:24px;letter-spacing:.22em;color:#00C853}
.bars{position:absolute;top:110px;left:80px;right:80px;display:flex;gap:10px}
.bars i{flex:1;height:6px;background:#22272E;border-radius:3px;overflow:hidden;position:relative}
.bars i b{position:absolute;inset:0;width:0;background:#E3F4FF}
.ghost{position:absolute;left:50%;top:50%;font-family:AN;font-size:300px;line-height:.8;color:#0f1419;white-space:nowrap;transform:translate(-50%,-50%)}
.scene{position:absolute;inset:0;opacity:0}
.c{position:absolute;left:80px;right:80px;direction:rtl;text-align:right}
.big{font-family:LZ;font-size:200px;line-height:1.05}
.sub{font-family:CA;font-size:52px;color:#8A97A3;margin-top:24px}
.comp{font-family:CA;font-size:40px;color:#8A97A3}
.row{display:flex;justify-content:space-between;align-items:center;direction:rtl;margin-top:50px}
.team{font-family:LZ;font-size:92px;line-height:1.1;width:330px}
.team.a{text-align:left}
.mid{font-family:AN;font-size:200px;line-height:1;text-align:center;direction:ltr;white-space:nowrap}
.note{font-family:CA;font-size:40px;color:#8A97A3;margin-top:44px}
.acc{width:180px;height:12px;background:#00C853;margin-top:50px}
.foot{position:absolute;bottom:170px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid #22272E;padding-top:30px}
.foot .h{font-family:SM;font-size:24px;color:#8A97A3}
.foot .s{font-family:CA;font-size:28px;color:#8A97A3;direction:rtl}
.foot img{height:44px}
.sb{margin-top:40px}
.sb .ln{display:flex;justify-content:space-between;align-items:center;direction:rtl;border-top:2px solid #22272E;padding:22px 0}
.sb .ln:last-child{border-bottom:2px solid #22272E}
.sb .nm{font-family:LZ;font-size:110px;line-height:1.1}
.sb .sc{font-family:AN;font-size:170px;line-height:1}
.sb .vs{font-family:SM;font-size:30px;color:#8A97A3;letter-spacing:.3em;text-align:center;padding:10px 0}
.tm{font-family:AN;font-size:260px;line-height:1;direction:ltr;text-align:right;margin-top:30px}
.list .it{border-top:2px solid #22272E;padding:34px 0}
.list .it:last-child{border-bottom:2px solid #22272E}
.list .row{margin-top:18px}
.list .team{font-size:62px;width:300px}
.list .mid{font-size:120px}
""".replace("FONTS", FONTS.as_uri())


def mid_text(it):
    if "home_score" in it:
        return f'{it["away_score"]} - {it["home_score"]}'  # LTR display: away left, home right (RTL layout)
    return E(it.get("time", ""))


def item_block(it):
    return (f'<div class=comp>{E(it.get("comp",""))}</div>'
            f'<div class=row><div class=team>{E(it["home"])}</div><div class=mid>{mid_text(it)}</div>'
            f'<div class="team a">{E(it["away"])}</div></div>')


def page(spec, body, bars=0):
    wm = (LOGO_DIR / "kora-klicks-wordmark-transparent-ice.svg").as_uri()
    bars_html = f'<div class=bars>{"".join("<i><b></b></i>" for _ in range(bars))}</div>' if bars else ""
    return (f'<html><head><meta charset=utf-8><style>{CSS}</style></head><body>'
            f'<div class=bg></div><div class=ghost id=ghost>{E(spec.get("ghost",""))}</div><div class=grain></div>'
            f'{bars_html}<div class=top><img src="{wm}"><span class=lab>{E(spec.get("label",""))}</span></div>'
            f'{body}<div class=foot><span class=h>@koraklicks</span><span class=s>{E(spec.get("source",""))}</span></div>'
            f'</body></html>')


def still_html(spec):
    items = "".join(f'<div class=it>{item_block(it)}</div>' for it in spec["items"])
    body = (f'<div class=c style="top:300px"><div class=big style="font-size:150px">{E(spec["title"])}</div>'
            f'{"<div class=sub>"+E(spec["subtitle"])+"</div>" if spec.get("subtitle") else ""}</div>'
            f'<div class="c list" style="top:{640 if spec.get("subtitle") else 560}px">{items}'
            f'{"<div class=note style=color:#00C853;font-family:LZ;font-size:64px>"+E(spec["cta"])+"</div>" if spec.get("cta") else ""}</div>')
    return page(spec, body)


def video_html(spec, durs):
    sc = [f'<div class=scene><div class=c style="top:640px"><div class=big>{E(spec["title"])}</div>'
          f'{"<div class=sub>"+E(spec["subtitle"])+"</div>" if spec.get("subtitle") else ""}<div class=acc></div></div></div>']
    for it in spec["items"]:
        if "home_score" in it:
            core = (f'<div class=sb><div class=ln><span class=nm>{E(it["home"])}</span><span class=sc>{it["home_score"]}</span></div>'
                    f'<div class=ln><span class=nm>{E(it["away"])}</span><span class=sc>{it["away_score"]}</span></div></div>')
        else:
            core = (f'<div class=sb><div class=ln><span class=nm>{E(it["home"])}</span></div><div class=vs>VS</div>'
                    f'<div class=ln><span class=nm>{E(it["away"])}</span></div></div><div class=tm>{E(it.get("time",""))}</div>')
        sc.append(f'<div class=scene><div class=c style="top:520px"><div class=comp>{E(it.get("comp",""))}</div>{core}'
                  f'{"<div class=note>"+E(it["note"])+"</div>" if it.get("note") else ""}<div class=acc></div></div></div>')
    sc.append(f'<div class=scene><div class=c style="top:700px"><div class=big style="color:#00C853;font-size:170px">{E(spec.get("cta",""))}</div>'
              f'<div class=sub>{E(spec.get("cta_sub",""))}</div><div class=sub style="font-family:SM;font-size:40px;color:#E3F4FF;direction:ltr;text-align:right;margin-top:60px">FOLLOW @koraklicks</div></div></div>')
    js = """<script>
const D=%s, T=D.reduce((a,b)=>a+b,0);
const S=[...document.querySelectorAll('.scene')], B=[...document.querySelectorAll('.bars b')], G=document.getElementById('ghost');
const ease=x=>1-Math.pow(1-Math.min(Math.max(x,0),1),3);
window.render=t=>{let s=0,acc=0;while(s<D.length-1&&t>=acc+D[s]){acc+=D[s];s++}const u=t-acc,d=D[s];
 S.forEach((el,i)=>{el.style.opacity=0});const el=S[s];
 const kids=[...el.querySelectorAll('.c > *')];
 const out=s<D.length-1?Math.min(1,Math.max(0,(d-u)/0.18)):1; el.style.opacity=out;
 kids.forEach((k,j)=>{const p=ease((u-0.08*j)/0.55);k.style.opacity=p;k.style.transform=`translateY(${(1-p)*70}px)`});
 B.forEach((b,i)=>{b.style.width=(i<s?100:i>s?0:Math.min(100,u/d*100))+'%%'});
 G.style.transform=`translate(-50%%,-50%%) scale(${1.08-0.08*t/T})`;};
render(0);</script>""" % json.dumps(durs)
    return page(spec, "".join(sc), bars=len(durs)).replace("</body></html>", js + "</body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out_dir")
    ap.add_argument("--fps", type=int, default=30); ap.add_argument("--bpm", type=float, default=124)
    ap.add_argument("--mood", default="drive")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = Path(a.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    slug = spec["slug"]
    n = len(spec["items"]) + 2
    sb = out / f"{slug}-sb.json"
    sb.write_text(json.dumps({"slug": slug, "scenes": [{"type": "x", "duration": 3.9}] * n}))
    subprocess.run([sys.executable, str(HERE / "music.py"), str(sb), str(out), "--bpm", str(a.bpm), "--mood", a.mood],
                   check=True, stdout=subprocess.DEVNULL)
    durs = [s["duration"] for s in json.loads((out / f"{slug}-timed.json").read_text())["scenes"]]
    music = out / f"{slug}-music.wav"

    from playwright.sync_api import sync_playwright
    frames = out / f"{slug}-frames"; frames.mkdir(exist_ok=True)
    (out / f"{slug}-still.html").write_text(still_html(spec), encoding="utf-8")
    (out / f"{slug}-video.html").write_text(video_html(spec, durs), encoding="utf-8")
    total = sum(durs); nf = int(round(total * a.fps))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto((out / f"{slug}-still.html").as_uri()); pg.wait_for_timeout(600)
        pg.screenshot(path=str(out / f"{slug}-story.jpg"), type="jpeg", quality=92)
        pg.goto((out / f"{slug}-video.html").as_uri()); pg.wait_for_timeout(600)
        for i in range(nf):
            pg.evaluate(f"render({i / a.fps})")
            pg.screenshot(path=str(frames / f"{i:05d}.jpg"), type="jpeg", quality=90)
        b.close()
    mp4 = out / f"{slug}-short.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(a.fps), "-i", str(frames / "%05d.jpg"),
                    "-i", str(music), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(mp4)], check=True)
    print(json.dumps({"story": str(out / f"{slug}-story.jpg"), "short": str(mp4), "duration_s": round(total, 2)}))


if __name__ == "__main__":
    main()
