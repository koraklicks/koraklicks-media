#!/usr/bin/env python3
"""Kora Klicks photo cards, «Desk» format (owner, 19 Nov 2026): blue / ink / cream editorial cards.

  python3 .claude/skills/newsroom-rules/scripts/cards.py spec.json OUT_DIR [--preview]

Writes OUT_DIR/<slug>-01.jpg, -02.jpg ... (1080x1350, 4:5) = TikTok photo post + Instagram carousel slides.
--preview also writes <slug>-contact.jpg (all slides side by side) for one quick look.

spec.json:
{
  "slug": "ucl-2026-11-25",
  "lang": "ar",                     # "ar" (default, RTL) or "en"
  "arabic_digits": false,           # true = Arabic-Indic digits (default: 0-9, easier to read at score size)
  "section": "كرة القدم",           # header right/left label, slide number is added: «كرة القدم / ٠١»
  "cards": [
    {"t": "breaking", "tag": "خبر عاجل", "corner": "ورد الآن",
     "headline": "عصر جديد\\nيبدأ الآن.", "sub": "نورثسايد يعيّن\\nجيمي ريد", "body": "مدرب جديد. عقد لثلاث سنوات.",
     "tagline": "القصة تبدأ من هنا.", "label": "أخبار / يوميًا"},
    {"t": "result", "status": "نهاية المباراة", "comp": "الدوري / الجولة 8", "headline": "فوز\\nبجدارة.",
     "home": "نورثسايد", "home_score": 3, "away": "ريفرسايد", "away_score": 1,
     "tagline": "ثلاثة أهداف. ثلاث نقاط.", "label": "نتائج / يوميًا"},
    {"t": "preview", "status": "المباراة القادمة", "comp": "الدوري / الجولة 9", "headline": "المواجهة\\nالقادمة.",
     "home": "نورثسايد", "away": "إيستبورو", "kickoff_label": "موعد المباراة / 24 أغسطس", "time": "19:45",
     "tz": "بتوقيت القاهرة", "venue": "ملعب\\nنورثسايد", "label": "قبل المباراة / يوميًا"},
    {"t": "roundup", "kicker": "3 أخبار / دقيقة واحدة", "date": "24 أغسطس", "headline": "الحصاد\\nاليومي.",
     "items": [{"label": "01 / الخبر الأبرز", "title": "...", "body": "..."}],   # 2-3 items
     "cta": "احفظ. شارك. تابع الجديد."}
  ]
}
Optional on any card: "source" (shown small above the footer as «📌 المصدر: ...»), "handle" (default @KORAKLICKS).
Club logos (owner 19 Nov 2026): "home_logo"/"away_logo" on result + preview = paths from scripts/media.py crests.
Photo: "photo" + "photo_credit" on breaking = ONLY a free Wikimedia Commons photo from scripts/media.py photo (or an
owner-supplied file); never from news sites/agencies/club accounts. The credit is printed on the card.
Rules: real facts only (newsroom gate), no crests/photos needed, one idea per card, «\\n» = line break.
Templates: breaking = blue bg + ink footer · result = ink bg, home row in periwinkle · preview = cream + blue
kick-off block · roundup = blue head + cream list. Fonts: Barlow Condensed 800 (EN display), Changa (AR,
owner 19 Nov 2026), Inter 600/700 (labels). Palette: BLUE #3155E7 INK #0E1211 CREAM #F3F2EA PERI #A7BAFF.
"""
import argparse, base64, html, json, os, re, sys
from pathlib import Path

FONTS = Path(__file__).resolve().parent.parent / "assets" / "fonts"
LOGO = Path(__file__).resolve().parents[3] / "assets" / "logo" / "kk-mark-gold.svg"  # owner logo, 19 Nov 2026
W, H = 1080, 1350
C = dict(blue="#3155E7", ink="#0E1211", cream="#F3F2EA", peri="#A7BAFF", grey="#5B5F66", line_d="#2A2F33")
AR_DIG = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def font_face():
    out = []
    for fam, f, wt in [("Barlow", "barlow-condensed-latin-800-normal.woff2", 800),
                       ("Plex", "changa-arabic-400-normal.woff2", 400),
                       ("Plex", "changa-arabic-500-normal.woff2", 500),
                       ("Plex", "changa-arabic-700-normal.woff2", 700),
                       ("Inter", "inter-latin-500-normal.woff2", 500), ("Inter", "inter-latin-600-normal.woff2", 600),
                       ("Inter", "inter-latin-700-normal.woff2", 700)]:
        b = base64.b64encode((FONTS / f).read_bytes()).decode()
        out.append(f"@font-face{{font-family:{fam};font-weight:{wt};src:url(data:font/woff2;base64,{b}) format('woff2')}}")
    return "\n".join(out)


class T:
    def __init__(self, spec):
        self.ar = spec.get("lang", "ar") == "ar"
        # Western digits by default (owner review 20 Nov 2026: the Arabic-Indic zero «٠» is a dot at score size);
        # "arabic_digits": true switches to ٠١٢٣.
        self.dig = self.ar and bool(spec.get("arabic_digits"))

    def __call__(self, s, br=True):
        s = "" if s is None else str(s)
        if self.dig:
            s = s.translate(AR_DIG)
        if self.ar:   # «مصر 5-0 مالاوي»: an en dash keeps each score next to its team in RTL text
            s = re.sub(r"([0-9٠-٩])\s*-\s*([0-9٠-٩])", "\\1 – \\2", s)
        s = html.escape(s)
        return s.replace("\\n", "<br>").replace("\n", "<br>") if br else s


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
.card{position:relative;width:1080px;height:1350px;display:flex;flex-direction:column;padding:0 64px;
  font-family:Inter,Plex,sans-serif;-webkit-font-smoothing:antialiased}
.ar{direction:rtl;font-family:Plex,Inter,sans-serif}
.disp{font-family:Barlow,Plex,sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:-.5px;line-height:.92}
.ar .disp{font-family:Plex,Barlow,sans-serif;font-weight:700;letter-spacing:0;line-height:1.18;text-transform:none}
.lbl{font-family:Inter,Plex,sans-serif;font-weight:700;font-size:20px;letter-spacing:.6px;text-transform:uppercase}
.ar .lbl{font-family:Plex,Inter,sans-serif;font-weight:700;font-size:23px;letter-spacing:0}
.head{display:flex;justify-content:space-between;align-items:center;height:146px;border-bottom:3px solid currentColor}
.brand{font-family:Inter,Plex;font-weight:700;font-size:37px;letter-spacing:.3px}
.ar .brand{font-family:Plex,Inter;font-size:38px}
.row{display:flex;justify-content:space-between;align-items:center}
.foot{display:flex;justify-content:space-between;align-items:center;height:96px;margin-top:auto}
.src{font-size:22px;font-weight:500;opacity:.75;padding:0 0 10px}
.ar .src{font-size:24px}
.ph>*:not(.layer){position:relative;z-index:1}
.body{font-size:33px;font-weight:500;line-height:1.42}
.ar .body{font-size:34px;line-height:1.55}
"""


def header(t, spec, n, color):
    sec = spec.get("section") or ("كرة القدم" if t.ar else "FOOTBALL")
    num = f"{n:02d}"
    brand = "كورة كليكس" if t.ar else "KORA KLICKS"
    mark = LOGO.read_text().replace("<svg ", '<svg style="height:54px;width:auto;flex:none" ', 1)
    return (f'<div class="head" style="color:{color}"><div class="brand" style="display:flex;align-items:center;gap:18px">{mark}<span>{brand}</span></div>'
            f'<div class="lbl">{t(sec)} / {t(num)}</div></div>')


def handle(card):
    return '<bdi dir="ltr">' + html.escape(card.get("handle", "@KORAKLICKS")) + '</bdi>'


SPEC_DIR = Path(".")


def data_uri(path):
    f = (SPEC_DIR / path).resolve()
    mime = "image/png" if f.suffix.lower() == ".png" else "image/svg+xml" if f.suffix.lower() == ".svg" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()


def logo(c, k, h):
    return f'<img src="{data_uri(c[k])}" style="height:{h}px;width:{h}px;object-fit:contain;flex:none">' if c.get(k) else ""


def photo_layers(c):
    """Breaking card photo (owner 19 Nov 2026): ONLY free Commons photos from scripts/media.py or owner files, with credit."""
    if not c.get("photo"):
        return "", ""
    if not c.get("photo_credit"):
        sys.exit("photo without photo_credit: every photo needs its credit line (scripts/media.py photo gives it)")
    u = data_uri(c["photo"])
    return (f'<div class="layer" style="position:absolute;inset:0;background:url({u}) center 22%/cover;filter:grayscale(1) contrast(1.15)"></div>'
            f'<div class="layer" style="position:absolute;inset:0;background:{C["blue"]};mix-blend-mode:multiply"></div>'
            f'<div class="layer" style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(49,85,231,.25) 0%,rgba(49,85,231,.35) 40%,rgba(49,85,231,.9) 72%)"></div>'), \
           f'<div style="font-size:18px;opacity:.8;direction:ltr;text-align:left;padding-bottom:8px;font-family:Inter">{html.escape(c["photo_credit"])}</div>'


def src(t, card, color):
    if not card.get("source"):
        return ""
    pre = "📌 المصدر: " if t.ar else "📌 Source: "
    return f'<div class="src" style="color:{color}">{pre}{t(card["source"])}</div>'


def breaking(t, spec, c, n):
    layers, credit = photo_layers(c)
    return f"""<div class="card {'ar' if t.ar else ''} {'ph' if layers else ''}" style="background:{C['blue']};color:#fff">{layers}
 {header(t, spec, n, '#fff')}
 <div class="row" style="margin-top:66px"><span class="lbl" style="background:{C['ink']};padding:16px 22px">{t(c.get('tag', 'خبر عاجل' if t.ar else 'BREAKING NEWS'))}</span>
   <span class="lbl">{t(c.get('corner', 'ورد الآن' if t.ar else 'JUST IN'))}</span></div>
 <div class="disp" style="font-size:{c.get('size', 168 if not t.ar else 132)}px;margin-top:48px">{t(c['headline'])}</div>
 <div style="width:150px;height:9px;background:#fff;margin:60px 0 50px"></div>
 <div class="disp" style="font-size:{70 if not t.ar else 60}px">{t(c.get('sub', ''))}</div>
 <div class="body" style="margin-top:26px">{t(c.get('body', ''))}</div>
 <div style="margin-top:auto">{src(t, c, '#fff')}{credit}</div>
 <div style="margin:0 -64px;background:{C['ink']};padding:40px 64px 0;height:180px">
  <div class="disp" style="font-size:{40 if not t.ar else 38}px">{t(c.get('tagline', ''))}</div>
  <div class="row" style="margin-top:30px"><span class="lbl" style="color:{C['peri']}">{handle(c)}</span><span class="lbl">{t(c.get('label', ''))}</span></div>
 </div></div>"""


def score_row(t, name, score, side, color, top_line, lg=""):
    return f"""<div class="row" style="border-top:3px solid {top_line};height:252px">
  <div style="display:flex;align-items:center;gap:30px">{lg}<div><div class="disp" style="font-size:{94 if not t.ar else 84}px;color:{color}">{t(name)}</div>
   <div class="lbl" style="color:{C['cream']};opacity:.85;margin-top:18px;font-size:18px">{side}</div></div></div>
  <div class="disp" style="font-size:190px;color:{color};line-height:1">{t(score)}</div></div>"""


def result(t, spec, c, n):
    home_l, away_l = ("صاحب الأرض", "الضيف") if t.ar else ("HOME", "AWAY")
    return f"""<div class="card {'ar' if t.ar else ''}" style="background:{C['ink']};color:{C['cream']}">
 {header(t, spec, n, C['cream'])}
 <div class="row" style="margin-top:66px"><span class="lbl" style="color:{C['peri']}">{t(c.get('status', 'نهاية المباراة' if t.ar else 'FULL TIME'))}</span>
   <span class="lbl">{t(c.get('comp', ''))}</span></div>
 <div class="disp" style="font-size:{c.get('size', 150 if not t.ar else 124)}px;margin:40px 0 58px">{t(c['headline'])}</div>
 {score_row(t, c['home'], c['home_score'], home_l, C['peri'], C['blue'], logo(c, 'home_logo', 124))}
 {score_row(t, c['away'], c['away_score'], away_l, C['cream'], C['line_d'], logo(c, 'away_logo', 124))}
 <div style="border-top:3px solid {C['line_d']};padding-top:48px" class="disp"><span style="font-size:{44 if not t.ar else 40}px">{t(c.get('tagline', ''))}</span></div>
 <div style="margin-top:auto">{src(t, c, C['cream'])}</div>
 <div class="foot"><span class="lbl" style="color:{C['peri']}">{handle(c)}</span><span class="lbl">{t(c.get('label', ''))}</span></div></div>"""


def preview(t, spec, c, n):
    vs = "ضد" if t.ar else "VS"
    return f"""<div class="card {'ar' if t.ar else ''}" style="background:{C['cream']};color:{C['ink']}">
 {header(t, spec, n, C['ink'])}
 <div class="row" style="margin-top:66px"><span class="lbl">{t(c.get('status', 'المباراة القادمة' if t.ar else 'UP NEXT'))}</span><span class="lbl">{t(c.get('comp', ''))}</span></div>
 <div class="disp" style="font-size:{c.get('size', 160 if not t.ar else 128)}px;margin:40px 0 50px">{t(c['headline'])}</div>
 <div style="border-top:4px solid {C['ink']};padding-top:44px" class="disp"><span style="font-size:{100 if not t.ar else 92}px;display:inline-flex;align-items:center;gap:30px">{logo(c, 'home_logo', 104)}{t(c['home'])}</span></div>
 <div class="row" style="margin:30px 0 40px;gap:28px"><span class="lbl" style="background:{C['ink']};color:#fff;padding:12px 22px;font-size:24px">{vs}</span>
   <span style="flex:1;height:2px;background:#C9C8C0"></span></div>
 <div class="disp"><span style="font-size:{100 if not t.ar else 92}px;display:inline-flex;align-items:center;gap:30px">{logo(c, 'away_logo', 104)}{t(c['away'])}</span></div>
 <div style="margin-top:auto">{src(t, c, C['ink'])}</div>
 <div style="margin:0 -64px;background:{C['blue']};color:#fff;padding:46px 64px 0;height:300px">
  <div style="display:flex;height:150px">
   <div style="flex:1.45"><div class="lbl" style="font-size:19px">{t(c.get('kickoff_label', ''))}</div>
     <div class="row" style="justify-content:flex-start;gap:30px;margin-top:10px"><span class="disp" style="font-size:108px;font-family:Barlow,Plex;font-weight:800;line-height:1">{t(c.get('time', ''))}</span>
     <span class="lbl" style="font-size:19px;max-width:170px">{t(c.get('tz', 'بتوقيت القاهرة' if t.ar else 'CAIRO'))}</span></div></div>
   <div style="width:3px;background:rgba(255,255,255,.75);margin:6px 44px"></div>
   <div style="flex:1"><div class="lbl" style="font-size:19px">{'الملعب' if t.ar else 'THE VENUE'}</div>
     <div class="disp" style="font-size:{46 if not t.ar else 42}px;margin-top:14px">{t(c.get('venue', ''))}</div></div></div>
  <div class="row" style="border-top:2px solid rgba(255,255,255,.8);margin-top:12px;height:92px"><span class="lbl">{handle(c)}</span><span class="lbl">{t(c.get('label', ''))}</span></div>
 </div></div>"""


def roundup(t, spec, c, n):
    items = "".join(f"""<div style="padding:30px 0 30px;border-bottom:2px solid #D3D2CA">
   <div class="lbl" style="color:{C['blue']};font-size:{19 if not t.ar else 21}px">{t(it.get('label', f'0{i + 1}'))}</div>
   <div class="disp" style="font-size:{52 if not t.ar else 44}px;margin:12px 0 12px">{t(it['title'])}</div>
   <div class="body" style="font-size:{29 if not t.ar else 29}px;color:{C['grey']}">{t(it.get('body', ''))}</div></div>"""
                    for i, it in enumerate(c["items"][:3]))
    return f"""<div class="card {'ar' if t.ar else ''}" style="background:{C['cream']};color:{C['ink']}">
 <div style="margin:0 -64px;padding:0 64px 46px;background:{C['blue']};color:#fff">{header(t, spec, n, '#fff')}
  <div class="row" style="margin-top:38px"><span class="lbl" style="font-size:19px">{t(c.get('kicker', ''))}</span><span class="lbl" style="font-size:19px">{t(c.get('date', ''))}</span></div>
  <div class="disp" style="font-size:{c.get('size', 122 if not t.ar else 104)}px;margin-top:24px;color:{C['cream']}">{t(c['headline'])}</div></div>
 <div style="margin-top:20px">{items}</div>
 <div style="margin-top:auto">{src(t, c, C['grey'])}</div>
 <div class="foot" style="border-top:3px solid {C['ink']}"><span class="lbl">{handle(c)}</span><span class="lbl" style="color:{C['blue']}">{t(c.get('cta', 'احفظ. شارك. تابع الجديد.' if t.ar else 'SAVE. SHARE. STAY AHEAD.'))}</span></div></div>"""


TPL = dict(breaking=breaking, result=result, preview=preview, roundup=roundup)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out_dir"); ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    global SPEC_DIR
    SPEC_DIR = Path(a.spec).resolve().parent  # logo/photo paths are relative to the spec
    t, out = T(spec), Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ff = font_face()
    from playwright.sync_api import sync_playwright
    files = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, c in enumerate(spec["cards"], 1):
            doc = f"<!doctype html><html><head><meta charset=utf-8><style>{ff}{CSS}</style></head><body>{TPL[c['t']](t, spec, c, i)}</body></html>"
            pg.set_content(doc); pg.evaluate("document.fonts.ready")
            over = pg.evaluate("(()=>{const c=document.querySelector('.card');return c.scrollHeight>1350||c.scrollWidth>1080})()")
            f = out / f"{spec['slug']}-{i:02d}.jpg"
            pg.screenshot(path=str(f), type="jpeg", quality=92)
            files.append(f)
            print(f, "OVERFLOW: shorten the text" if over else "ok")
        b.close()
    if a.preview:
        from PIL import Image
        ims = [Image.open(f) for f in files]
        sheet = Image.new("RGB", (len(ims) * 560 - 20, 700), "white")
        for i, im in enumerate(ims):
            sheet.paste(im.resize((540, 675)), (i * 560, 12))
        sheet.save(out / f"{spec['slug']}-contact.jpg", quality=85)
        print(out / f"{spec['slug']}-contact.jpg")


if __name__ == "__main__":
    main()
