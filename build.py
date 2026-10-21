#!/usr/bin/env python3
"""Builds the TaasMaster static site into ./dist.

Usage:  python3 build.py [--base https://your-domain.com]
Set BASE_URL to your real domain before deploying — canonical, hreflang and sitemap URLs use it.
"""
import argparse, datetime, hashlib, html, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_en, content_ne, content_tools  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, DIST = os.path.join(ROOT, "src"), os.path.join(ROOT, "dist")
BASE_URL = "https://nbnaryal.github.io/TaasMaster"   # GitHub Pages; use your own domain later
SITE = {"en": "TaasMaster", "ne": "तासमास्टर"}
THEME = "#020617"
BRAND = {"en": "Taas<span>Master</span>", "ne": "तास<span>मास्टर</span>"}
LANGJS = '<script>(function(){var L=document.documentElement.lang==="ne"?"ne":"en";try{var p=localStorage.getItem("tm-lang"),a=document.querySelector(\'link[rel=alternate][hreflang="\'+(L==="ne"?"en":"ne")+\'"]\');if(p&&p!==L&&a){location.replace(new URL(a.href).pathname+location.search+location.hash);return}}catch(e){}document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest("a[data-setlang]");if(t)try{localStorage.setItem("tm-lang",t.getAttribute("data-setlang"))}catch(e){}},true)})();</script>'
TODAY = datetime.date.today().isoformat()

SLUGS = {
    "home": "", "cb_tool": "call-break-score", "mar_tool": "marriage-calculator", "tp_tool": "teen-patti-tracker",
    "cb_rules": "call-break-rules", "mar_rules": "marriage-rules", "tp_rules": "teen-patti-rules", "faq": "faq",
}
GAME = {"cb_tool": "callbreak", "mar_tool": "marriage", "tp_tool": "teenpatti"}
RULES_OF = {"cb_tool": "cb_rules", "mar_tool": "mar_rules", "tp_tool": "tp_rules"}
CONTENT = {"en": content_en.PAGES, "ne": content_ne.PAGES}
for _lang in CONTENT:
    CONTENT[_lang].update(content_tools.TOOLS[_lang])
APPS = os.path.join(ROOT, "apps")

UI = {
    "en": dict(
        short={"home": "Home", "cb_tool": "Call Break Score", "mar_tool": "Marriage Calculator", "tp_tool": "Teen Patti Tracker",
               "cb_rules": "Call Break Rules", "mar_rules": "Marriage Rules", "tp_rules": "Teen Patti Rules", "faq": "FAQ"},
        nav=[("home", "Home", "⌂"), ("cb_tool", "Call Break", "♠"), ("mar_tool", "Marriage", "♥"), ("tp_tool", "Teen Patti", "♣")],
        switch="नेपाली", faqH="Frequently asked questions", tools="Score trackers", rules="Rules & guides",
        foot="TaasMaster records games played in person. It never takes bets, holds money or processes payments.", noscript="Please turn on JavaScript to use the tracker.",
        rulesLink="Read the rules", locale="en_US", nav_label="Main", loading="Loading tracker…",
    ),
    "ne": dict(
        short={"home": "गृहपृष्ठ", "cb_tool": "कल ब्रेक स्कोर", "mar_tool": "म्यारिज क्याल्कुलेटर", "tp_tool": "तीन पत्ती ट्र्याकर",
               "cb_rules": "कल ब्रेकको नियम", "mar_rules": "म्यारिजको नियम", "tp_rules": "तीन पत्तीको नियम", "faq": "प्रश्नोत्तर"},
        nav=[("home", "गृह", "⌂"), ("cb_tool", "कल ब्रेक", "♠"), ("mar_tool", "म्यारिज", "♥"), ("tp_tool", "तीन पत्ती", "♣")],
        switch="English", faqH="बारम्बार सोधिने प्रश्न", tools="स्कोर ट्र्याकर", rules="नियम र जानकारी",
        foot="तासमास्टरले आमनेसामने खेलिने खेल मात्र रेकर्ड गर्छ। यसले दाउ लिँदैन, पैसा राख्दैन र भुक्तानी गर्दैन।", noscript="ट्र्याकर चलाउन JavaScript खोल्नुहोस्।",
        rulesLink="नियम पढ्नुहोस्", locale="ne_NP", nav_label="मुख्य", loading="ट्र्याकर खुल्दैछ…",
    ),
}

LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#f5f1e6"/>'
        '<path fill="#0e4d30" d="M32 10C26 20 14 26 14 36a9 9 0 0 0 15 6.7L26 54h12l-3-11.3A9 9 0 0 0 50 36c0-10-12-16-18-26z"/></svg>')


CURRENT = ' aria-current="page"'
# The site's four bottom tabs, added to every tracker app too. App bottom bars and toasts move up above it.
NAV_H = "64px"
APP_NAV_CSS = """<style id="tm-nav-css">
.tm-nav{position:fixed;left:0;right:0;bottom:0;z-index:35;background:rgba(2,6,23,.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
 border-top:1px solid #1e293b;display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:6px 8px calc(6px + env(safe-area-inset-bottom));
 font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans","Noto Sans Devanagari",sans-serif}
.tm-nav a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;height:52px;border-radius:12px;text-decoration:none;
 color:#94a3b8;font-size:12px;font-weight:600;line-height:1.2}
.tm-nav a .ic{font-size:19px;line-height:1}
.tm-nav a[aria-current="page"]{background:#1e293b;color:#fcd34d}
.tm-nav a:hover{color:#fcd34d}
body{padding-bottom:calc(%(h)s + env(safe-area-inset-bottom))!important}
/* Teen Patti / Marriage: action bar and toast sit above the tabs */
.fixed.bottom-0{bottom:calc(%(h)s + env(safe-area-inset-bottom))!important}
.fixed.bottom-0>div{padding-bottom:.75rem!important}
#toast{bottom:calc(6rem + %(h)s + env(safe-area-inset-bottom))!important}
/* Call Break: round controls and toast sit above the tabs */
body.entering #roundControls{bottom:calc(%(h)s + env(safe-area-inset-bottom))!important;padding-bottom:10px!important}
.toast{bottom:calc(20px + %(h)s + env(safe-area-inset-bottom))}
body.entering .toast{bottom:calc(150px + %(h)s + env(safe-area-inset-bottom))}
</style>
""" % {"h": NAV_H}
# Call Break Ledger uses CSS variables; these match the Teen Patti / Marriage trackers (Tailwind slate + amber)
CB_THEME = """<meta name="theme-color" content="#020617"><meta name="color-scheme" content="dark">
<style id="tm-theme">
:root,:root:not(#x){--bg:#020617;--card:#0f172a;--text:#f1f5f9;--muted:#94a3b8;--line:#1e293b;
 --accent:#fbbf24;--accent-hover:#fcd34d;--accent-soft:rgba(251,191,36,.12);--gold:#fcd34d;--gold-soft:rgba(251,191,36,.10);
 --neg:#fda4af;--neg-soft:rgba(244,63,94,.14);--pos:#6ee7b7;--radius:16px;color-scheme:dark}
body{-webkit-font-smoothing:antialiased;font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.card{background:rgba(15,23,42,.8)}
.btn-primary,.btn-chip.on{color:#020617!important;font-weight:700}
.field input,.pct input,.pair input,.modal-box input{background:#1e293b!important;border-color:#334155!important;color:#f1f5f9}
.btn-ghost{background:#1e293b;border-color:#334155;color:#f1f5f9}
.modal-box{background:#0f172a;border:1px solid #334155;border-radius:24px}
.toast{background:#f1f5f9;color:#020617}
h1{letter-spacing:-.025em}
</style>
"""
PREFIX = ""  # path part of BASE_URL, e.g. "/taasmaster" on GitHub Pages project sites


def pre(s):
    """Prefix root-relative href/src links so the site also works inside a sub-folder."""
    return re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{PREFIX}/', s)


def path(lang, key):
    slug = SLUGS[key]
    p = "/" + ("ne/" if lang == "ne" else "") + (slug + "/" if slug else "")
    return p


def absu(lang, key):
    return BASE_URL + path(lang, key)


def fill_links(s, lang):
    s = re.sub(r"\{link:(\w+)\}", lambda m: path(lang, m.group(1)), s)
    s = re.sub(r"\{link_ne:(\w+)\}", lambda m: path("ne", m.group(1)), s)
    s = re.sub(r"\{link_en:(\w+)\}", lambda m: path("en", m.group(1)), s)
    return s


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def schema(lang, key, pg):
    ui, out = UI[lang], []
    url = absu(lang, key)
    if key == "home":
        out.append({"@context": "https://schema.org", "@type": "WebSite", "name": SITE[lang], "url": url, "inLanguage": lang,
                    "description": pg["desc"]})
    else:
        out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["short"]["home"], "item": absu(lang, "home")},
            {"@type": "ListItem", "position": 2, "name": ui["short"][key], "item": url}]})
    if key in GAME:
        out.append({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": pg["app_name"], "url": url,
                    "description": pg["desc"], "applicationCategory": "GameApplication", "operatingSystem": "Android, iOS, Windows, macOS (web browser)",
                    "inLanguage": lang, "isAccessibleForFree": True,
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NPR"}})
    if pg.get("faq"):
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pg["faq"]]})
    return "".join(jsonld(o) for o in out)


def page(lang, key, version):
    pg, ui = CONTENT[lang][key], UI[lang]
    other = "ne" if lang == "en" else "en"
    e = html.escape
    head = f"""<!doctype html>
<html lang="{lang}" data-root="{PREFIX}/">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(pg['title'])}</title>
<meta name="description" content="{e(pg['desc'])}">
<link rel="canonical" href="{absu(lang, key)}">
<link rel="alternate" hreflang="en" href="{absu('en', key)}">
<link rel="alternate" hreflang="ne" href="{absu('ne', key)}">
<link rel="alternate" hreflang="x-default" href="{absu('en', key)}">
{LANGJS}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE[lang]}">
<meta property="og:title" content="{e(pg['title'])}">
<meta property="og:description" content="{e(pg['desc'])}">
<meta property="og:url" content="{absu(lang, key)}">
<meta property="og:locale" content="{ui['locale']}">
<meta property="og:image" content="{BASE_URL}/icons/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{THEME}">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{SITE[lang]}">
<link rel="manifest" href="{'/ne' if lang == 'ne' else ''}/manifest.webmanifest">
<link rel="icon" href="/icons/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/icons/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css?v={version}">
{schema(lang, key, pg)}
</head>
<body class="page-{key.replace('_', '-')}">
<header class="top">
  <a class="brand" href="{path(lang, 'home')}">{BRAND[lang]}</a>
  <div class="top-actions">
    <button id="install" class="pill" hidden type="button">Install</button>
    <a class="pill lang" href="{path(other, key)}" hreflang="{other}" lang="{other}" data-setlang="{other}">{UI[lang]['switch']}</a>
  </div>
</header>
<main>
"""
    crumbs = "" if key == "home" else f'<p class="crumbs"><a href="{path(lang, "home")}">{e(ui["short"]["home"])}</a> › {e(ui["short"][key])}</p>'
    body = crumbs + f"<div class=\"intro\"><h1>{e(pg['h1'])}</h1>\n<p class=\"lede\">{e(pg['lede'])}</p></div>\n"
    if key in GAME:
        body += f'<p><a class="btn" href="{path("en", key)}">{content_tools.OPEN[lang]}</a></p>\n'
    body += fill_links(pg["body"], lang)
    if pg.get("faq"):
        body += f'<section class="faq"><h2>{ui["faqH"]}</h2>' + "".join(
            f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in pg["faq"]) + "</section>"
    if key in RULES_OF:
        body += f'<p><a class="btn ghost" href="{path(lang, RULES_OF[key])}">{ui["rulesLink"]}</a></p>'

    links = lambda keys: " ".join(f'<a href="{path(lang, k)}">{e(ui["short"][k])}</a>' for k in keys)
    foot = f"""</main>
<footer>
  <nav aria-label="{ui['tools']}"><strong>{ui['tools']}:</strong> {links(['cb_tool', 'mar_tool', 'tp_tool'])}</nav>
  <nav aria-label="{ui['rules']}"><strong>{ui['rules']}:</strong> {links(['cb_rules', 'mar_rules', 'tp_rules', 'faq'])}</nav>
  <p>{ui['foot']}</p>
</footer>
<nav class="bottom-nav" aria-label="{ui['nav_label']}">
""" + "".join(
        f'<a href="{path(lang, k)}"{CURRENT if k == key else ""}><span class="ic" aria-hidden="true">{ic}</span>{e(lab)}</a>'
        for k, lab, ic in ui["nav"]) + f"""
</nav>
<script src="/assets/app.js?v={version}" defer></script>
</body>
</html>
"""
    return pre(head + body + foot)


def ne_dictionary(game):
    """Load apps/i18n/ne_<game>.py into the {exact, patterns} shape runtime.js expects."""
    ns = {}
    exec(open(os.path.join(APPS, "i18n", f"ne_{game}.py"), encoding="utf-8").read(), ns)
    exact = {k: v for k, v in ns["EXACT"].items() if not re.search(r"\{\d+#?\}", k)}
    pats = [[k, v] for k, v in ns.get("PATTERNS", [])]
    return {"exact": exact, "patterns": pats}


def app_page(key, version, lang="en"):
    """Copy one of the user's tracker apps into its page folder and add the SEO layer around it.
    The Nepali copy also gets the translation layer (apps/i18n)."""
    pg, ui, e = CONTENT[lang][key], UI[lang], html.escape
    src, out = os.path.join(APPS, GAME[key]), os.path.join(DIST, path(lang, key).strip("/"))
    shutil.copytree(src, out)
    f = os.path.join(out, "index.html")
    s = open(f, encoding="utf-8").read()
    if lang == "ne":
        s = s.replace('<html lang="en"', '<html lang="ne"', 1)
        layer = ("<script>window.TM_I18N=" + json.dumps(ne_dictionary(GAME[key]), ensure_ascii=False) + ";</script>\n<script>"
                 + open(os.path.join(APPS, "i18n", "runtime.js"), encoding="utf-8").read() + "</script>\n")
        m = re.search(r"<body[^>]*>", s)
        s = s[:m.end()] + "\n" + layer + s[m.end():]
        mf = os.path.join(out, "manifest.webmanifest")
        man = json.load(open(mf, encoding="utf-8"))
        man.update({"name": pg["app_name"], "short_name": {"cb_tool": "कल ब्रेक", "mar_tool": "म्यारिज", "tp_tool": "तीन पत्ती"}[key], "lang": "ne"})
        json.dump(man, open(mf, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{e(pg['title'])}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{e(pg["desc"])}">', s, count=1)
    if GAME[key] == "callbreak":
        s = re.sub(r'<meta name="theme-color"[^>]*>\n?', '', s)
        s = s.replace("</head>", CB_THEME + "</head>", 1)
        s = s.replace('<span class="suit">♠</span>Call Break Ledger</h1>', '<span class="suit">♠</span>Call Break <span style="color:#fbbf24">Ledger</span></h1>', 1)
    extra = f"""<link rel="canonical" href="{absu(lang, key)}">
<link rel="alternate" hreflang="en" href="{absu('en', key)}">
<link rel="alternate" hreflang="ne" href="{absu('ne', key)}">
<link rel="alternate" hreflang="x-default" href="{absu('en', key)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE[lang]}">
<meta property="og:title" content="{e(pg['title'])}">
<meta property="og:description" content="{e(pg['desc'])}">
<meta property="og:url" content="{absu(lang, key)}">
<meta property="og:image" content="{BASE_URL}/icons/og.png">
<meta name="twitter:card" content="summary_large_image">
{LANGJS}
{schema(lang, key, pg)}
</head>"""
    assert s.count("</head>") == 1
    s = s.replace("</head>", extra)
    links = lambda keys: " ".join(f'<a href="{path(lang, k)}">{e(ui["short"][k])}</a>' for k in keys)
    other = "ne" if lang == "en" else "en"
    section = pre(f"""
<section class="tm-seo" aria-labelledby="tm-seo-h">
<style>
.tm-seo{{max-width:880px;margin:0 auto;padding:28px 16px calc(150px + env(safe-area-inset-bottom));font:15px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:inherit}}
.tm-seo>hr{{border:0;border-top:1px solid #1e293b;margin:0 0 22px}}
.tm-seo h2{{font-size:19px;font-weight:700;margin:0 0 6px}}.tm-seo h3{{font-size:16px;font-weight:700;margin:18px 0 6px}}.tm-seo p{{margin:0 0 10px}}.tm-seo strong{{font-weight:700}}
.tm-seo p,.tm-seo li{{color:#94a3b8}}.tm-seo strong{{color:#f1f5f9}}.tm-seo ul{{list-style:disc;padding-left:20px;margin:6px 0}}.tm-seo li{{margin:3px 0}}.tm-seo li::marker{{color:#fbbf24}}.tm-seo a{{color:#fcd34d;text-underline-offset:3px}}
.tm-seo .tm-rules{{display:block;text-align:center;padding:13px;background:#1e293b;border:1px solid #334155;border-radius:12px;margin:18px 0;font-weight:700;text-decoration:none;color:#f1f5f9}}
.tm-seo nav{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px;margin-top:8px}}.tm-seo small{{opacity:.7}}
</style>
<hr>
<h2 id="tm-seo-h">{e(pg['h1'])}</h2>
<p>{e(pg['lede'])}</p>
{fill_links(pg['body'], lang)}
<a class="tm-rules" href="{path(lang, RULES_OF[key])}">{e(ui['rulesLink'])}: {e(ui['short'][RULES_OF[key]])}</a>
<nav aria-label="{ui['tools']}"><strong>{ui['tools']}:</strong> {links(['cb_tool', 'mar_tool', 'tp_tool'])}</nav>
<nav aria-label="{ui['rules']}"><strong>{ui['rules']}:</strong> {links(['cb_rules', 'mar_rules', 'tp_rules', 'faq'])}</nav>
<nav><a href="{path(lang, 'home')}">{SITE[lang]} – {e(ui['short']['home'])}</a> <a href="{path(other, key)}" hreflang="{other}" lang="{other}" data-setlang="{other}">{UI[lang]['switch']}</a></nav>
</section>
""")
    nav = pre('<nav class="tm-nav" aria-label="' + ui["nav_label"] + '">' + "".join(
        f'<a href="{path(lang, k)}"{CURRENT if k == key else ""}><span class="ic" aria-hidden="true">{ic}</span>{e(lab)}</a>'
        for k, lab, ic in ui["nav"]) + '</nav>\n')
    s = s.replace("</head>", APP_NAV_CSS + "</head>", 1)
    i = s.rindex("</body>")
    s = s[:i] + nav + s[i:]
    markers = {"callbreak": '<div id="toast" class="toast"', "teenpatti": '<div id="app" class="max-w-3xl mx-auto px-4 pb-32"></div>',
               "marriage": '<div id="app" class="max-w-3xl mx-auto px-4 pb-32"></div>'}
    m = markers[GAME[key]]
    assert s.count(m) == 1, (key, m)
    s = s.replace(m, section + m) if GAME[key] == "callbreak" else s.replace(m, m + section)
    open(f, "w", encoding="utf-8").write(s)
    return [path(lang, key) + os.path.relpath(os.path.join(r, n), out).replace(os.sep, "/")
            for r, _, fs in os.walk(out) for n in fs
            if n not in ("index.html", "sw.js") and "screenshots" not in r]


def write(rel, data, mode="w"):
    p = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(data)


def icons():
    from PIL import Image, ImageDraw, ImageFont
    INK, PAPER, PIP = "#020617", "#fbbf24", "#fda4af"
    def spade(size, pad, bg=INK, fg=PAPER):
        img = Image.new("RGB", (size, size), bg)
        d = ImageDraw.Draw(img)
        s = size - 2 * pad
        P = lambda x, y: (pad + x * s / 64, pad + y * s / 64)
        d.polygon([P(32, 8), P(52, 30), P(12, 30)], fill=fg)
        d.ellipse([P(10, 22), P(34, 46)], fill=fg)
        d.ellipse([P(30, 22), P(54, 46)], fill=fg)
        d.polygon([P(32, 32), P(40, 56), P(24, 56)], fill=fg)
        return img
    os.makedirs(os.path.join(DIST, "icons"), exist_ok=True)
    for size, pad, name in [(192, 30, "icon-192.png"), (512, 80, "icon-512.png"), (512, 130, "maskable-512.png"), (180, 28, "apple-touch-icon.png")]:
        spade(size, pad).save(os.path.join(DIST, "icons", name), optimize=True)
    og = Image.new("RGB", (1200, 630), INK)
    d = ImageDraw.Draw(og)
    for r in range(520, 0, -8):   # the trackers' green felt, as a soft radial
        t = r / 520
        col = tuple(int(a + (b - a) * t) for a, b in zip((6, 95, 70), (2, 44, 34)))
        d.ellipse([600 - r * 1.6, -r * 0.5, 600 + r * 1.6, r * 1.3], fill=col)
    def font(names, size):
        for n in names:
            for d in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/", ""):
                try:
                    return ImageFont.truetype(d + n, size)
                except Exception:
                    pass
        try:
            return ImageFont.load_default(size=size)
        except Exception:
            return ImageFont.load_default()
    bold = font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "DejaVuSans.ttf"], 108)
    sym = font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"], 90)
    reg = font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"], 38)
    w1 = d.textlength("Taas", font=bold); w2 = d.textlength("Master", font=bold)
    x = (1200 - w1 - w2) / 2
    d.text((x, 170), "Taas", font=bold, fill="#f1f5f9"); d.text((x + w1, 170), "Master", font=bold, fill="#fbbf24")
    for k, (ch, col) in enumerate([("♠", "#f1f5f9"), ("♥", "#fda4af"), ("♣", "#f1f5f9"), ("♦", "#fda4af")]):
        d.text((600 - 200 + k * 100, 320), ch, font=sym, fill=col)
    msg = "Call Break, Marriage and Teen Patti score trackers"
    d.text(((1200 - d.textlength(msg, font=reg)) / 2, 470), msg, font=reg, fill="#d1fae5")
    og.save(os.path.join(DIST, "icons", "og.png"), optimize=True)
    write("icons/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#020617"/>'
          '<path fill="#fbbf24" d="M32 10C26 20 14 26 14 36a9 9 0 0 0 15 6.7L26 54h12l-3-11.3A9 9 0 0 0 50 36c0-10-12-16-18-26z"/></svg>')


def manifest(lang):
    ui = UI[lang]
    m = {
        "id": "/" if lang == "en" else "/ne/", "name": SITE[lang] + (" – Card Game Score Tracker" if lang == "en" else " – तास खेल स्कोर"),
        "short_name": SITE[lang], "lang": lang, "start_url": path(lang, "home") + "?source=pwa", "scope": "/",
        "display": "standalone", "orientation": "portrait", "background_color": "#020617", "theme_color": THEME,
        "description": CONTENT[lang]["home"]["desc"], "categories": ["games", "utilities"],
        "icons": [
            {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "shortcuts": [{"name": ui["short"][k], "url": path(lang, k), "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192"}]}
                      for k in ("cb_tool", "mar_tool", "tp_tool")],
    }
    return re.sub(r'"/', f'"{PREFIX}/', json.dumps(m, ensure_ascii=False, indent=2))


def main():
    global BASE_URL, PREFIX
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("BASE_URL", BASE_URL))
    BASE_URL = ap.parse_args().base.rstrip("/")
    from urllib.parse import urlparse
    PREFIX = urlparse(BASE_URL).path.rstrip("/")

    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DIST, "assets"))
    h = hashlib.sha1()
    for r, _, fs in sorted(os.walk(os.path.join(SRC, "assets"))):
        for fn in sorted(fs):
            h.update(open(os.path.join(r, fn), "rb").read())
    for r, _, fs in sorted(os.walk(APPS)):
        for fn in sorted(fs):
            h.update(open(os.path.join(r, fn), "rb").read())
    h.update(json.dumps([CONTENT, BASE_URL], ensure_ascii=False, default=str).encode())
    version = h.hexdigest()[:10]

    pages, app_files = [], []
    for lang in ("en", "ne"):
        for key in SLUGS:
            p = path(lang, key)
            if key in GAME:
                app_files.extend(app_page(key, version, lang))
            else:
                write(p.lstrip("/") + "index.html", page(lang, key, version))
            pages.append((lang, key, p))
        write(("ne/" if lang == "ne" else "") + "manifest.webmanifest", manifest(lang))

    write("404.html", pre(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found – TaasMaster</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/style.css?v={version}"></head>
<body><main><h1>Page not found</h1><p>Try the <a href="/call-break-score/">Call Break</a>, <a href="/marriage-calculator/">Marriage</a> or <a href="/teen-patti-tracker/">Teen Patti</a> tracker, or go <a href="/">home</a>.</p>
<p lang="ne">पेज भेटिएन। <a href="/ne/">गृहपृष्ठमा जानुहोस्</a>।</p></main></body></html>"""))
    icons()

    # Service worker: precache everything so the site works fully offline after the first visit.
    precache = [p for _, _, p in pages] + ["/404.html", f"/assets/style.css?v={version}", f"/assets/app.js?v={version}",
                "/manifest.webmanifest", "/ne/manifest.webmanifest", "/icons/favicon.svg", "/icons/icon-192.png",
                "/icons/icon-512.png", "/icons/maskable-512.png", "/icons/apple-touch-icon.png"] + app_files
    precache = [PREFIX + u for u in precache]
    write("sw.js", open(os.path.join(SRC, "sw.template.js"), encoding="utf-8").read()
          .replace("__VERSION__", version).replace("__ROOT__", PREFIX + "/").replace("__PRECACHE__", json.dumps(precache)))

    # sitemap.xml with hreflang alternates
    urls = []
    for lang, key, _ in pages:
        pri = "1.0" if key == "home" else ("0.9" if key in GAME else "0.7")
        urls.append(f"""  <url>
    <loc>{absu(lang, key)}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{pri}</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{absu('en', key)}"/>
    <xhtml:link rel="alternate" hreflang="ne" href="{absu('ne', key)}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{absu('en', key)}"/>
  </url>""")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    # Cache headers for Netlify / Cloudflare Pages (ignored elsewhere)
    write("_headers", "/sw.js\n  Cache-Control: no-cache\n/*.webmanifest\n  Content-Type: application/manifest+json\n"
          "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/icons/*\n  Cache-Control: public, max-age=604800\n")
    print(f"Built {len(pages)} pages into dist/ (version {version}, base {BASE_URL})")


if __name__ == "__main__":
    main()
