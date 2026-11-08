"""Builds okamotodesigns.com from work/manifest.json and the content below.

Run: uv run --no-project python -I build.py
Edit copy here, never in the generated .html files. No em dashes in copy.
"""
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://okamotodesigns.com"
EMAIL = "shadow@okamotodesigns.com"
LANES = ["Lighting Design and Programming", "Media and Sceptron", "Electrics and Production"]

# Show copy keyed by work/ folder slug. Roles are exactly as Shadow confirmed them.
SHOWS = {
    "awhonn-2026": ("AWHONN 2026 Convention", "LD and Programmer", "2026", "General session lighting for the AWHONN national convention."),
    "sibos-miami-2026": ("Sibos Miami", "LD and Programmer", "2026", "Session lighting for Sibos in Miami."),
    "fnce-2025": ("FNCE 2025", "LD and Programmer", "2025", "General session lighting, from the keynote stage to the full room and ceiling."),
    "nea-2014": ("National Education Association", "LD and Programmer", "2014", "Convention general session."),
    "ucf-go-for-launch-2026": ("UCF Go For Launch", "Sceptron Tech", "2026", "LED tube tunnels in the arena hallways and the ballroom LED wall."),
    "organogenesis-live-2025": ("Organogenesis LIVE", "Sceptron Tech", "2025", "Sceptron LED across the general session sets, including the Sky Full of Stars and JCB sessions."),
    "cornerstone-young-living-2022": ("Young Living, with Cornerstone", "Media Servers", "2022", "Media servers for the general session stage."),
    "mtn-dew-nba-all-star-2020": ("Mtn Dew at NBA All-Star", "Sceptron Tech", "2020", "Sceptron LED for the Mtn Dew activation in Chicago."),
    "immersive-van-gogh": ("Immersive Van Gogh", "Production Electrician and EIC", "2020 to 2023", "Lighting and video power, network, and signal for immersive venues across the US and Canada, including the mirror forest in Denver."),
    "immersive-disney-animation": ("Immersive Disney Animation", "Production Electrician and EIC", "2023", "Power, network, and signal for the projection rooms."),
    "stadium-show-nov-2023": ("Stadium Show", "Master Electrician", "2023", "Stadium floor stage with LED towers."),
    "arena-show-oct-2024": ("Arena Show", "Master Electrician", "2024", "Arena stage with LED screens and beam rig."),
    "circular-truss-rig-2024": ("Circular Truss Rig", "Ground Control Tech", "2024", "Circular truss and LED ring rig, from build to rehearsal."),
}
ORDER = ["awhonn-2026", "sibos-miami-2026", "fnce-2025", "nea-2014",
         "ucf-go-for-launch-2026", "organogenesis-live-2025", "cornerstone-young-living-2022", "mtn-dew-nba-all-star-2020",
         "immersive-van-gogh", "immersive-disney-animation", "circular-truss-rig-2024", "arena-show-oct-2024", "stadium-show-nov-2023"]

CLIENTS = ["National Education Association", "Lighthouse Immersive", "PRG", "4Wall", "LMG", "Christie Lites", "Cornerstone",
           "NFL Kickoff", "NFL Super Bowl", "MLB All-Star Game", "General Electric", "Bentley Motors", "SpaceX",
           "Manhattan School of Music", "Steppenwolf Theatre Company", "Philadelphia Eagles", "Universal Studios",
           "Hard Rock", "Walt Disney Entertainment"]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Tilt+Neon&display=swap" rel="stylesheet">'
e = html.escape


def page(title, desc, body, depth, head_class="page", path=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/work/hero-poster.jpg">
<meta name="theme-color" content="#08090b">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="site-head {head_class}"><div class="wrap">
<a class="brand" href="{up}">okamoto<span>designs</span></a>
<nav class="nav"><a href="{up}#work">Work</a><a class="hide-sm" href="{up}#about">About</a><a class="hide-sm" href="{up}beamcalc/">Tools</a><a href="{up}#contact">Contact</a></nav>
</div></header>
{body}
<footer><div class="wrap"><span>&copy; okamotodesigns. Michael "Shadow" Okamoto, Orlando, Florida.</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div></footer>
</body>
</html>
"""


def media(item, base, cls=""):
    c = f' class="{cls}"' if cls else ""
    if item["type"] == "video":
        return f'<video{c} src="{base}{item["src"]}" poster="{base}{item["poster"]}" autoplay muted loop playsinline preload="metadata"></video>'
    return f'<img{c} src="{base}{item["src"]}" width="{item["w"]}" height="{item["h"]}" loading="lazy" alt="">'


def cover(item, base):
    src = item["poster"] if item["type"] == "video" else item["sm"]
    return f'<img src="{base}{src}" loading="lazy" alt="">'


def build():
    man = {m["slug"]: m for m in json.load(open(os.path.join(ROOT, "work", "manifest.json")))}
    missing = set(man) ^ set(SHOWS)
    assert not missing, f"manifest and SHOWS disagree: {missing}"

    tiles = []
    for slug in ORDER:
        title, role, year, _ = SHOWS[slug]
        lane = man[slug]["lane"]
        first = man[slug]["items"][0]
        alt_cover = next((i for i in man[slug]["items"] if i["type"] == "image"), first)
        tiles.append(f'<a class="tile" data-lane="{e(lane)}" href="work/{slug}/">{cover(alt_cover, f"work/{slug}/")}'
                     f'<div class="cap"><strong>{e(title)}</strong><span>{e(role)} &middot; {e(year)}</span></div></a>')

    filters = '<button type="button" aria-pressed="true" data-f="all">All work</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-f="{e(l)}">{e(l)}</button>' for l in LANES)

    index = f"""
<section class="hero">
<img class="poster" src="work/hero-poster.jpg" alt="">
<video src="work/hero.mp4" poster="work/hero-poster.jpg" autoplay muted loop playsinline></video>
<div class="copy"><div class="wrap">
<p class="eyebrow">Orlando, Florida &middot; Working nationally</p>
<h1>Michael <em>&ldquo;Shadow&rdquo;</em> Okamoto</h1>
<p class="lede">Lighting designer, lighting programmer, and media systems for corporate events, conventions, immersive venues, and arenas.</p>
<div class="btns"><a class="btn primary" href="#work">See the work</a><a class="btn" href="#contact">Get in touch</a></div>
</div></div>
</section>

<section id="work"><div class="wrap">
<h2>Work</h2>
<p class="sub">Selected shows, sorted by what I did on them.</p>
<div class="filters" role="group" aria-label="Filter work">{filters}</div>
<div class="grid">{''.join(tiles)}</div>
</div></section>

<section id="about" class="alt"><div class="wrap two">
<div class="about">
<h2>About</h2>
<p>I've designed, programmed, and run lighting and media systems since the early 1990s: automated lighting at Walt Disney World, national tours as lighting director, and freelance design and programming for conventions, corporate events, television, museums, and theme parks since 1998.</p>
<p>From 2020 to 2023 I was Production Electrician and EIC for Immersive Van Gogh and Immersive Disney Animation, building lighting and video power, network, and signal for more than 20 venues across the US and Canada.</p>
<p>Today I work as a lighting designer and programmer, media server operator, Sceptron tech, and master electrician, based in Orlando and available to travel.</p>
<p><a href="assets/michael-okamoto-resume.pdf">Download my resume (PDF)</a></p>
</div>
<ul class="facts">
<li><b>Consoles</b><span>grandMA3, grandMA2, Wholehog 4, ChamSys MagicQ, ETC</span></li>
<li><b>Media</b><span>Pixera, disguise, Green Hippo, Resolume</span></li>
<li><b>Paperwork</b><span>Vectorworks, AutoCAD, Lightwright 6, WYSIWYG</span></li>
<li><b>Roles</b><span>Lighting Designer, Programmer, Media Server Operator, Sceptron Tech, Master Electrician, Production Electrician, EIC</span></li>
<li><b>Training</b><span>disguise Essentials, Fundamentals, and Workflow Specialist; OSHA 30; Aerial Work Platforms; IATSE</span></li>
</ul>
</div></section>

<section><div class="wrap">
<h2>Clients and projects</h2>
<p class="sub">A partial list from over thirty years of shows.</p>
<ul class="clients">{''.join(f'<li>{e(c)}</li>' for c in CLIENTS)}</ul>
</div></section>

<section class="alt"><div class="wrap">
<h2>Tools I build</h2>
<p class="sub">Small apps for the job, made by a working LD.</p>
<a class="app" href="beamcalc/"><img src="beamcalc/img/icon.png" alt=""><div><h3>Photon BeamCalc</h3><p>Throw distance, beam size, lens angle, and raked floor pools. Android, iPhone coming.</p></div></a>
</div></section>

<section id="contact" class="contact"><div class="wrap">
<h2>Let's work together</h2>
<p class="sub">Booking a show, need a programmer, or want to talk about a rig? Send me a note.</p>
<div class="btns"><a class="btn primary" href="mailto:{EMAIL}">{EMAIL}</a></div>
</div></section>

<script>
const head = document.querySelector('.site-head');
const onScroll = () => head.classList.toggle('solid', scrollY > 40);
addEventListener('scroll', onScroll, {{passive: true}}); onScroll();
document.querySelectorAll('.filters button').forEach(b => b.addEventListener('click', () => {{
  document.querySelectorAll('.filters button').forEach(x => x.setAttribute('aria-pressed', x === b));
  document.querySelectorAll('.tile').forEach(t => t.hidden = b.dataset.f !== 'all' && t.dataset.lane !== b.dataset.f);
}}));
</script>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
        page("Michael \"Shadow\" Okamoto | Lighting Designer and Programmer | okamotodesigns",
             "Lighting design, programming, and media systems for live events. Orlando, Florida.", index, 0, head_class="", path=""))

    # Project pages, in ORDER so prev/next walks the grid.
    for k, slug in enumerate(ORDER):
        title, role, year, blurb = SHOWS[slug]
        items = man[slug]["items"]
        # First item and panoramas span the row. A half-width item that would sit alone
        # (before a wide one, or last with an odd count) spans too, so no row has a hole.
        wide = [i == 0 or (it["type"] == "image" and it["w"] / it["h"] > 2.1) for i, it in enumerate(items)]
        cells, col = [], 0
        for i, it in enumerate(items):
            w = wide[i] or (col == 0 and (i + 1 == len(items) or wide[i + 1]))
            cells.append(f'<div class="wide">{media(it, "")}</div>' if w else media(it, ""))
            col = 0 if w else (col + 1) % 2
        prev_s, next_s = ORDER[k - 1], ORDER[(k + 1) % len(ORDER)]
        body = f"""
<div class="wrap project-head">
<a class="back" href="../../#work">&larr; All work</a>
<h1>{e(title)}</h1>
<p class="meta"><b>{e(role)}</b> &middot; {e(year)} &middot; {e(man[slug]["lane"])}</p>
<p class="sub">{e(blurb)}</p>
</div>
<div class="wrap gallery">{''.join(cells)}</div>
<div class="wrap next"><a href="../{prev_s}/">&larr; {e(SHOWS[prev_s][0])}</a><a href="../{next_s}/">{e(SHOWS[next_s][0])} &rarr;</a></div>
<div class="lb" id="lb"><img alt=""></div>
<script>
const lb = document.getElementById('lb'), lbi = lb.querySelector('img');
document.querySelectorAll('.gallery img').forEach(i => i.addEventListener('click', () => {{ lbi.src = i.src; lb.classList.add('open'); }}));
lb.addEventListener('click', () => lb.classList.remove('open'));
addEventListener('keydown', ev => {{ if (ev.key === 'Escape') lb.classList.remove('open'); }});
</script>
"""
        open(os.path.join(ROOT, "work", slug, "index.html"), "w", encoding="utf-8").write(
            page(f"{title} | {role} | okamotodesigns", f"{title}, {year}. {role}. {blurb}", body, 2, path=f"work/{slug}/"))

    # BeamCalc landing page.
    bc = """
<div class="wrap prose">
<p><a href="../">&larr; okamotodesigns</a></p>
<div class="app" style="border:0;padding:0;background:none"><img src="img/icon.png" alt=""><div><h1>Photon BeamCalc</h1><p class="date">A lighting beam calculator from okamotodesigns</p></div></div>
<p>Photon BeamCalc answers the questions you get on a site visit or in the middle of a focus call, without a laptop or a signal.</p>
<h2>What it does</h2>
<ul>
<li>Throw distance and the angle off straight down, from floor distance and trim height, to the floor or to a face.</li>
<li>Beam size from lens angle and throw, lens angle from throw and beam size, or the throw you need for a beam size.</li>
<li>Raked floor pools: the pool's length and width, and where its near and far edges land.</li>
<li>Feet and inches or meters. Works offline. No accounts, ads, or data collection.</li>
</ul>
<div class="shots"><img src="img/1-throw-feet.jpg" alt="Throw distance screen"><img src="img/2-pool-feet.jpg" alt="Raked floor pool screen"></div>
<p>Results assume a round beam on a level floor. Check them before you rely on them on a show. Photon BeamCalc calculates lighting beams, not structural beams, and it isn't for rigging or load calculations.</p>
<p>Android on Google Play soon. iPhone in development. <a href="privacy/">Privacy policy</a>.</p>
</div>
"""
    open(os.path.join(ROOT, "beamcalc", "index.html"), "w", encoding="utf-8").write(
        page("Photon BeamCalc | okamotodesigns", "Lighting beam calculator for throw, beam size, lens angle, and raked floor pools.", bc, 1, path="beamcalc/"))

    # Privacy policy: same text as photon-beamcalc/play/privacy-policy.html, restyled.
    pp = """
<div class="wrap prose">
<p><a href="../">&larr; Photon BeamCalc</a></p>
<h1>Photon BeamCalc Privacy Policy</h1>
<p class="date">Effective November 6, 2026</p>
<p>Photon BeamCalc is a lighting beam calculator from okamotodesigns, for Android and iPhone.</p>
<h2>What the app collects</h2>
<p>Nothing. The app has no accounts, ads, or analytics, and it doesn't use the internet. The numbers you enter stay on your device and are never sent to okamotodesigns or anyone else.</p>
<h2>What stays on your device</h2>
<p>The app remembers whether you chose feet or meters. Uninstalling the app removes that setting.</p>
<h2>What the app stores may collect</h2>
<p>Google Play and the Apple App Store handle downloads and may collect information under their own privacy policies. okamotodesigns may see the summary sales, install, and crash reports those stores provide to developers.</p>
<h2>Children</h2>
<p>The app isn't directed at children and collects no information from anyone, including children.</p>
<h2>Changes</h2>
<p>If this policy changes, the new version will be posted here with a new effective date.</p>
<h2>Contact</h2>
<p>okamotodesigns: okamotodesigns@gmail.com</p>
</div>
"""
    open(os.path.join(ROOT, "beamcalc", "privacy", "index.html"), "w", encoding="utf-8").write(
        page("Photon BeamCalc Privacy Policy | okamotodesigns", "Privacy policy for the Photon BeamCalc app.", pp, 2, path="beamcalc/privacy/"))

    nf = '<div class="wrap prose"><h1>Nothing focused here</h1><p>That page isn\'t in the plot. <a href="/">Back to okamotodesigns</a>.</p></div>'
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(page("Not found | okamotodesigns", "Page not found.", nf, 0, path="404.html").replace('href="assets/', 'href="/assets/').replace('href=""', 'href="/"'))
    open(os.path.join(ROOT, "CNAME"), "w").write("okamotodesigns.com\n")
    print("built", len(ORDER), "projects")


if __name__ == "__main__":
    build()
