import sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path('/home/claude/koraklicks-media')
F = ROOT/'.claude/skills/youtube-video/assets/fonts'
LOGO = next((ROOT/'.claude/assets/logo').glob('*.png'), None)
def html(w,h):
    s = w/1080
    story = h>w*1.5
    big = 150 if story else 84
    nm = 54 if story else 36
    return f"""<html><head><meta charset=utf-8><style>
@font-face{{font-family:LZ;src:url(file://{F}/lalezar-arabic-400-normal.woff2)}}
@font-face{{font-family:AN;src:url(file://{F}/anton-latin-400-normal.woff2)}}
@font-face{{font-family:SM;src:url(file://{F}/space-mono-latin-700-normal.woff2)}}
@font-face{{font-family:CA;src:url(file://{F}/cairo-arabic-800-normal.woff2)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#050608;color:#E3F4FF}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,#0e1c27 0%,#050608 66%)}}
.ghost{{position:absolute;left:50%;top:50%;font-family:AN;font-size:{int(w*.42)}px;color:#0f1419;transform:translate(-50%,-50%);white-space:nowrap}}
.wrap{{position:absolute;inset:0;padding:{int(h*.06)}px {int(w*.07)}px;display:flex;flex-direction:column;justify-content:space-between;direction:rtl}}
.lab{{font-family:SM;font-size:{int(w*.024)}px;letter-spacing:.22em;color:#00C853;direction:ltr;text-align:left}}
.t{{font-family:LZ;font-size:{big}px;line-height:1.05}}
.s{{font-family:CA;font-size:{int(w*.037)}px;color:#8A97A3;margin-top:12px}}
.blk{{border-top:2px solid #22272E;padding-top:14px;margin-top:14px}}
.k{{font-family:SM;font-size:{int(w*.02)}px;letter-spacing:.2em;color:#00C853;direction:ltr;text-align:right}}
.n{{font-family:LZ;font-size:{nm}px;line-height:1.25}}
.n b{{color:#22272E;font-weight:400;margin:0 14px}}
.src{{font-family:CA;font-size:{int(w*.026)}px;color:#8A97A3}}
.brand{{font-family:AN;font-size:{int(w*.035)}px;letter-spacing:.06em;color:#E3F4FF;direction:ltr;text-align:left}}
</style></head><body><div class=bg></div><div class=ghost>XI</div><div class=wrap>
<div><div class=lab>LINE-UPS · WED 21 OCT</div>
<div class=t>{'التشكيل الرسمي<br>للأهلي' if story else 'التشكيل الرسمي للأهلي'}</div><div class=s>أمام القناة · الدوري المصري · الجولة السابعة</div></div>
<div>
<div class=blk><div class=k>GK</div><div class=n>مصطفى شوبير</div></div>
<div class=blk><div class=k>DEF</div><div class=n>محمد هاني<b>/</b>ياسين مرعي<b>/</b>أشرف داري<b>/</b>توفيق محمد</div></div>
<div class=blk><div class=k>MID · ATT</div><div class=n>مروان عطية<b>/</b>إمام عاشور<b>/</b>عمر الساعي<br>زيزو<b>/</b>أشرف بن شرقي<b>/</b>منصف بقرار</div></div>
</div>
<div style="display:flex;justify-content:space-between;align-items:center"><div class=src>المصدر: يلاكورة · بوابة الأهرام</div><div class=brand>KORA KLICKS</div></div>
</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium') if False else p.chromium.launch()
    for name,(w,h) in {'lineup-x':(1600,900),'lineup-story':(1080,1920)}.items():
        pg = b.new_page(viewport={'width':w,'height':h})
        pathlib.Path(f'{name}.html').write_text(html(w,h),encoding='utf-8')
        pg.goto(f'file://{pathlib.Path(name+".html").resolve()}'); pg.wait_for_timeout(800)
        pg.screenshot(path=f'{name}.jpg',type='jpeg',quality=90)
    b.close()
