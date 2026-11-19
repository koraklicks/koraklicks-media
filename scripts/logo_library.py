#!/usr/bin/env python3
"""Kora Klicks logo library (owner, 19 Nov 2026): club, national-team and competition logos kept in the repo,
so runs never search for them again.

  python3 scripts/logo_library.py build          # refresh the catalog from ESPN (teams, ids, Arabic names, logo URLs)
  python3 scripts/logo_library.py fetch          # download every missing logo (256 px PNG); safe to re-run
  python3 scripts/logo_library.py find "الأهلي"   # path of a logo by Arabic or English name (prints NOT FOUND if missing)
  python3 scripts/logo_library.py find "الدوري الإنجليزي dark"   # competition logo version for ink/blue backgrounds
  python3 scripts/logo_library.py status         # how many logos are in the library / missing

Files: .claude/assets/crests/catalog.json · .claude/assets/crests/<espn_id>.png (teams)
       .claude/assets/crests/comp-<slug>.png (competitions)
Use in specs: "home_logo": "<path from find>" (cards.py / motion_short.py / story_short.py / render.py).
Source: ESPN only (owner rule). Logos are used unedited. Egyptian league clubs that are not in a CAF competition are
not on ESPN: they have no logo here (show the name only) unless the owner supplies a file — put it in the folder as
<any-id>.png and add it to catalog.json "extra".
Needs a.espncdn.com allowed (claude.ai Settings > Capabilities); `build` only needs site.api.espn.com.
"""
import io, json, sys, urllib.request, gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / ".claude" / "assets" / "crests"
CAT = DIR / "catalog.json"
UA = "KoraKlicksNewsroom/1.0"

COMPS = {  # slug: Arabic name (the competitions we cover)
    "eng.1": "الدوري الإنجليزي", "esp.1": "الدوري الإسباني", "ita.1": "الدوري الإيطالي", "ksa.1": "الدوري السعودي",
    "uefa.champions": "دوري أبطال أوروبا", "uefa.europa": "الدوري الأوروبي", "caf.champions": "دوري أبطال أفريقيا",
    "caf.confed": "الكونفدرالية الأفريقية", "afc.champions": "دوري أبطال آسيا للنخبة", "afc.cup": "دوري أبطال آسيا 2",
    "uefa.nations": "دوري الأمم الأوروبية", "fifa.world": "كأس العالم", "fifa.friendly": "مباريات ودية دولية",
    "fifa.worldq.uefa": "تصفيات كأس العالم · أوروبا", "fifa.worldq.afc": "تصفيات كأس العالم · آسيا",
    "fifa.worldq.caf": "تصفيات كأس العالم · أفريقيا",
}
CLUB_COMPS = ["eng.1", "esp.1", "ita.1", "ksa.1", "uefa.champions", "uefa.europa", "caf.champions", "caf.confed",
              "afc.champions", "afc.cup"]

AR = {
    # Premier League
    "AFC Bournemouth": "بورنموث", "Arsenal": "آرسنال", "Aston Villa": "أستون فيلا", "Brentford": "برينتفورد",
    "Brighton & Hove Albion": "برايتون", "Chelsea": "تشيلسي", "Coventry City": "كوفنتري", "Crystal Palace": "كريستال بالاس",
    "Everton": "إيفرتون", "Fulham": "فولهام", "Hull City": "هال سيتي", "Ipswich Town": "إبسويتش", "Leeds United": "ليدز",
    "Liverpool": "ليفربول", "Manchester City": "مانشستر سيتي", "Manchester United": "مانشستر يونايتد",
    "Newcastle United": "نيوكاسل", "Nottingham Forest": "نوتنجهام فورست", "Sunderland": "سندرلاند",
    "Tottenham Hotspur": "توتنهام", "West Ham United": "وست هام", "Wolverhampton Wanderers": "وولفرهامبتون",
    "Burnley": "بيرنلي", "Leicester City": "ليستر سيتي", "Southampton": "ساوثهامبتون",
    # La Liga
    "Alavés": "ألافيس", "Athletic Club": "أتلتيك بيلباو", "Atlético Madrid": "أتلتيكو مدريد", "Barcelona": "برشلونة",
    "Celta Vigo": "سيلتا فيجو", "Deportivo": "ديبورتيفو لاكورونيا", "Elche": "إلتشي", "Espanyol": "إسبانيول",
    "Getafe": "خيتافي", "Levante": "ليفانتي", "Málaga": "مالاجا", "Osasuna": "أوساسونا", "Racing Santander": "راسينج سانتاندير",
    "Rayo Vallecano": "رايو فاييكانو", "Real Betis": "ريال بيتيس", "Real Madrid": "ريال مدريد", "Real Sociedad": "ريال سوسيداد",
    "Sevilla": "إشبيلية", "Valencia": "فالنسيا", "Villarreal": "فياريال", "Girona": "جيرونا", "Mallorca": "مايوركا",
    "Real Oviedo": "ريال أوفييدو",
    # Serie A
    "AC Milan": "ميلان", "AS Roma": "روما", "Atalanta": "أتالانتا", "Bologna": "بولونيا", "Cagliari": "كالياري", "Como": "كومو",
    "Fiorentina": "فيورنتينا", "Frosinone": "فروزينوني", "Genoa": "جنوى", "Internazionale": "إنتر ميلان", "Juventus": "يوفنتوس",
    "Lazio": "لاتسيو", "Lecce": "ليتشي", "Monza": "مونزا", "Napoli": "نابولي", "Parma": "بارما", "Sassuolo": "ساسولو",
    "Torino": "تورينو", "Udinese": "أودينيزي", "Venezia": "فينيسيا", "Cremonese": "كريمونيزي", "Pisa": "بيزا", "Verona": "فيرونا",
    # Saudi Pro League + AFC
    "Abha": "أبها", "Al Ahli": "الأهلي السعودي", "Al Diriyah": "الدرعية", "Al Ettifaq": "الاتفاق", "Al Faisaly": "الفيصلي",
    "Al Fateh": "الفتح", "Al Fayha": "الفيحاء", "Al Hazem": "الحزم", "Al Hilal": "الهلال", "Al Ittihad": "الاتحاد",
    "Al Khaleej": "الخليج", "Al Kholood": "الخلود", "Al Nassr": "النصر", "Al Qadsiah": "القادسية", "Al Riyadh": "الرياض",
    "Al Shabab": "الشباب", "Al Taawoun": "التعاون", "Neom SC": "نيوم", "Al Okhdood": "الأخدود", "Damac": "ضمك",
    "Al Ain": "العين", "Al Sadd": "السد", "Al Wasl": "الوصل", "Al-Gharafa": "الغرافة", "Shabab Al Ahli": "شباب الأهلي",
    "Al-Quwa Al-Jawiya": "القوة الجوية", "Al-Shamal": "الشمال", "Esteghlal FC": "استقلال طهران", "Tractor": "تراكتور",
    "Al Jazira Club": "الجزيرة", "Al Wahda FC": "الوحدة", "Al-Rayyan SC": "الريان", "Al-Shorta SC": "الشرطة",
    "Al-Muharraq SC": "المحرق", "Al-Hussein SC": "الحسين إربد", "Al-Faisaly SC": "الفيصلي الأردني", "Kuwait SC": "الكويت",
    "Al-Khaldiya SC": "الخالدية", "Al-Nahda Club": "النهضة", "Al-Seeb Club": "السيب",
    # Egyptian clubs (CAF) + Arab/African opponents
    "Al Ahly": "الأهلي", "Zamalek": "الزمالك", "Pyramids FC": "بيراميدز", "ZED FC": "زد", "Al Masry": "المصري",
    "Future FC": "مودرن سبورت", "Ceramica Cleopatra": "سيراميكا كليوباترا",
    "Esperance Sportive de Tunis": "الترجي", "Club Africain": "النادي الإفريقي", "Club Sportif Sfaxien": "الصفاقسي",
    "Raja Casablanca": "الرجاء", "Wydad Casablanca": "الوداد", "AS FAR": "الجيش الملكي", "RSB Berkane": "نهضة بركان",
    "Maghreb As De Fès": "المغرب الفاسي", "MC Alger": "مولودية الجزائر", "USM Alger": "اتحاد العاصمة",
    "CR Belouizdad": "شباب بلوزداد", "JS Saoura": "شبيبة الساورة", "Al Hilal Omdurman": "الهلال السوداني",
    "Al-Merrikh": "المريخ السوداني", "Al Ahli Tripoli": "الأهلي طرابلس", "Asswehly SC": "السويحلي",
    "Mamelodi Sundowns": "صن داونز", "Orlando Pirates": "أورلاندو بايرتس", "Kaizer Chiefs": "كايزر تشيفز",
    "TP Mazembe": "مازيمبي", "Simba SC": "سيمبا", "Young Africans": "يانج أفريكانز", "ASEC Mimosas": "أسيك ميموزا",
    "Petro de Luanda": "بترو أتلتيكو", "Horoya": "حوريا", "Stade Malien": "الملعب المالي", "FC Nouadhibou": "نواذيبو",
    # UCL / Europe others
    "Bayern Munich": "بايرن ميونخ", "Borussia Dortmund": "بوروسيا دورتموند", "RB Leipzig": "لايبزيج",
    "Bayer Leverkusen": "باير ليفركوزن", "VfB Stuttgart": "شتوتجارت", "Eintracht Frankfurt": "آينتراخت فرانكفورت",
    "Paris Saint-Germain": "باريس سان جيرمان", "Marseille": "مارسيليا", "AS Monaco": "موناكو", "Lille": "ليل", "Lens": "لانس",
    "FC Porto": "بورتو", "Benfica": "بنفيكا", "Sporting CP": "سبورتينج لشبونة", "PSV Eindhoven": "آيندهوفن",
    "Feyenoord Rotterdam": "فينورد", "Ajax Amsterdam": "أياكس", "Club Brugge": "كلوب بروج", "Galatasaray": "جالطة سراي",
    "Fenerbahce": "فنربخشة", "Besiktas": "بشكتاش", "Shakhtar Donetsk": "شاختار دونيتسك", "Slavia Prague": "سلافيا براج",
    "Slovan Bratislava": "سلوفان براتيسلافا", "Bodo/Glimt": "بودو جليمت", "AEK Athens": "أيك أثينا", "Celtic": "سيلتيك",
    "LASK Linz": "لاسك لينز", "Sabah FK": "صباح", "Viking FK": "فايكنج", "Olympiacos": "أولمبياكوس",
    # National teams: Arab
    "Egypt": "مصر", "Saudi Arabia": "السعودية", "Morocco": "المغرب", "Algeria": "الجزائر", "Tunisia": "تونس", "Qatar": "قطر",
    "United Arab Emirates": "الإمارات", "Iraq": "العراق", "Jordan": "الأردن", "Oman": "عُمان", "Bahrain": "البحرين",
    "Kuwait": "الكويت", "Lebanon": "لبنان", "Syria": "سوريا", "Palestine": "فلسطين", "Libya": "ليبيا", "Sudan": "السودان",
    "Yemen": "اليمن", "Mauritania": "موريتانيا", "Comoros": "جزر القمر", "Djibouti": "جيبوتي",
    # National teams: Europe (+ big others)
    "Albania": "ألبانيا", "Andorra": "أندورا", "Armenia": "أرمينيا", "Austria": "النمسا", "Azerbaijan": "أذربيجان",
    "Belarus": "بيلاروسيا", "Belgium": "بلجيكا", "Bosnia-Herzegovina": "البوسنة والهرسك", "Bulgaria": "بلغاريا",
    "Croatia": "كرواتيا", "Cyprus": "قبرص", "Czechia": "التشيك", "Denmark": "الدنمارك", "England": "إنجلترا",
    "Estonia": "إستونيا", "Faroe Islands": "جزر فارو", "Finland": "فنلندا", "France": "فرنسا", "Georgia": "جورجيا",
    "Germany": "ألمانيا", "Gibraltar": "جبل طارق", "Greece": "اليونان", "Hungary": "المجر", "Iceland": "آيسلندا",
    "Italy": "إيطاليا", "Kazakhstan": "كازاخستان", "Kosovo": "كوسوفو", "Latvia": "لاتفيا", "Liechtenstein": "ليختنشتاين",
    "Lithuania": "ليتوانيا", "Luxembourg": "لوكسمبورج", "Malta": "مالطا", "Moldova": "مولدوفا", "Montenegro": "الجبل الأسود",
    "Netherlands": "هولندا", "North Macedonia": "مقدونيا الشمالية", "Northern Ireland": "أيرلندا الشمالية", "Norway": "النرويج",
    "Poland": "بولندا", "Portugal": "البرتغال", "Republic of Ireland": "أيرلندا", "Romania": "رومانيا", "San Marino": "سان مارينو",
    "Scotland": "اسكتلندا", "Serbia": "صربيا", "Slovakia": "سلوفاكيا", "Slovenia": "سلوفينيا", "Spain": "إسبانيا",
    "Sweden": "السويد", "Israel": "إسرائيل", "Switzerland": "سويسرا", "Türkiye": "تركيا", "Ukraine": "أوكرانيا", "Wales": "ويلز",
    "Brazil": "البرازيل", "Argentina": "الأرجنتين", "Uruguay": "أوروجواي", "Colombia": "كولومبيا", "United States": "أمريكا",
    "Mexico": "المكسيك", "Japan": "اليابان", "South Korea": "كوريا الجنوبية", "Iran": "إيران", "Senegal": "السنغال",
    "Nigeria": "نيجيريا", "Ivory Coast": "كوت ديفوار", "Ghana": "غانا", "Cameroon": "الكاميرون", "Australia": "أستراليا",
}
ARAB_NT = ["Egypt", "Saudi Arabia", "Morocco", "Algeria", "Tunisia", "Qatar", "United Arab Emirates", "Iraq", "Jordan",
           "Oman", "Bahrain", "Kuwait", "Lebanon", "Syria", "Palestine", "Libya", "Sudan", "Yemen", "Mauritania", "Comoros",
           "Djibouti"]
BIG_NT = ["Brazil", "Argentina", "Uruguay", "Colombia", "United States", "Mexico", "Japan", "South Korea", "Iran",
          "Senegal", "Nigeria", "Ivory Coast", "Ghana", "Cameroon", "Australia"]


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw if binary else json.loads(raw)


def teams(slug):
    return [t["team"] for t in get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/teams")
            ["sports"][0]["leagues"][0].get("teams", [])]


def logo_url(t):
    for l in t.get("logos") or []:
        if "default" in (l.get("rel") or []) and "default-team-logo" not in l.get("href", ""):
            return l["href"]
    return f'https://a.espncdn.com/i/teamlogos/{"countries" if t.get("_nt") else "soccer"}/500/{t["id"]}.png'


def load():
    return json.loads(CAT.read_text()) if CAT.exists() else {"teams": {}, "comps": {}, "extra": {}}


def build():
    cat = load()
    T = cat["teams"]

    def add(t, comp, national=False):
        tid = str(t["id"])
        e = T.setdefault(tid, {"name": t["displayName"], "comps": []})
        e.update(name=t["displayName"], short=t.get("shortDisplayName", ""), abbr=t.get("abbreviation", ""),
                 ar=AR.get(t["displayName"], e.get("ar", "")), national=national, file=f"{tid}.png")
        t["_nt"] = national
        e["logo_url"] = logo_url(t)
        if comp not in e["comps"]:
            e["comps"].append(comp)

    for slug in CLUB_COMPS:
        for t in teams(slug):
            if "TBD" not in t["displayName"]:
                add(t, slug)
    for t in teams("fifa.worldq.uefa"):
        add(t, "nt.europe", True)
    for t in teams("fifa.friendly"):
        if t["displayName"] in ARAB_NT:
            add(t, "nt.arab", True)
        elif t["displayName"] in BIG_NT:
            add(t, "nt.world", True)
    for slug, ar in COMPS.items():
        L = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard")["leagues"][0]
        lg = {(tuple(x.get("rel") or [])[-1:] or ("",))[0]: x["href"] for x in L.get("logos", [])}
        ok = {k: v for k, v in lg.items() if "default-team-logo" not in v}
        cat["comps"][slug] = {"name": L.get("name", slug), "ar": ar, "logo_url": ok.get("default", ""),
                              "logo_dark_url": ok.get("dark", ""), "file": f"comp-{slug}.png" if ok else "",
                              "file_dark": f"comp-{slug}-dark.png" if ok.get("dark") else "",
                              "short": {"uefa.champions": "Champions League", "uefa.europa": "Europa League",
                                        "eng.1": "Premier League", "esp.1": "La Liga", "ita.1": "Serie A",
                                        "ksa.1": "Roshn Saudi League"}.get(slug, "")}
    DIR.mkdir(parents=True, exist_ok=True)
    CAT.write_text(json.dumps(cat, ensure_ascii=False, indent=1, sort_keys=True))
    no_ar = sum(1 for v in T.values() if not v.get("ar"))
    print(f"catalog: {len(T)} teams ({no_ar} without Arabic name → English used), {len(cat['comps'])} competitions")


def _png(raw, path):
    from PIL import Image
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    im.thumbnail((256, 256))
    im.save(path, optimize=True)


def fetch():
    cat = load()
    jobs = [(v["logo_url"], DIR / v["file"]) for v in cat["teams"].values()] + \
           [(v["logo_url"], DIR / v["file"]) for v in cat["comps"].values() if v.get("file")] + \
           [(v["logo_dark_url"], DIR / v["file_dark"]) for v in cat["comps"].values() if v.get("file_dark")]
    ok = fail = skip = 0
    for url, path in jobs:
        if path.exists():
            skip += 1; continue
        try:
            _png(get(url, binary=True), path); ok += 1
        except Exception as e:
            fail += 1
            if fail <= 3:
                print(f"FAILED {path.name}: {type(e).__name__}: {e}")
            if fail == 3 and ok == 0 and "404" not in str(e):
                print("Stopping: the logo server is not reachable (allow a.espncdn.com)."); break
    print(f"downloaded {ok} · already there {skip} · failed {fail}")


def find(name):
    cat, low = load(), name.strip().lower()
    pools = list(cat["teams"].values()) + list(cat.get("extra", {}).values()) + list(cat["comps"].values())
    dark = low.endswith(" dark")
    if dark:
        low = low[:-5].strip()
    best = None
    for v in pools:
        if not v.get("file") or not (DIR / v["file"]).exists():
            continue
        keys = [k for k in (v.get("name", ""), v.get("short", ""), v.get("ar", ""), v.get("abbr", "")) if k]
        if any(low == k.lower() for k in keys):
            best = (0, v); break
        part = [len(k) for k in keys[:3] if low in k.lower()]
        if part and (best is None or min(part) < best[0]):   # partial: the shortest matching name wins
            best = (min(part), v)
    if not best:
        return None
    v = best[1]
    if dark and v.get("file_dark") and (DIR / v["file_dark"]).exists():   # competition logo for ink backgrounds
        return DIR / v["file_dark"]
    return DIR / v["file"]


def status():
    cat = load()
    t = cat["teams"].values()
    have = sum(1 for v in t if (DIR / v["file"]).exists())
    ch = sum(1 for v in cat["comps"].values() if v.get("file") and (DIR / v["file"]).exists())
    print(f"teams: {have}/{len(cat['teams'])} logos · competitions: {ch}/{len(cat['comps'])} logos")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("build", "fetch", "find", "status"):
        sys.exit(__doc__)
    if a[0] == "find":
        print(find(" ".join(a[1:])) or "NOT FOUND")
    else:
        globals()[a[0]]()
