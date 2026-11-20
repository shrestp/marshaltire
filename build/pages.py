import re
"""Generates the mockup's HTML pages from one shared shell. Run: python3 build/pages.py"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO = (ROOT / 'assets/img/logo.svg').read_text().strip()
import hashlib
def ver(rel):  # cache-busting tag: changes whenever the file changes
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4M10 6l-6 6 6 6"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'
INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.5"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
UPCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>'
EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>'
DLD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v12M6 11l6 6 6-6M5 20h14"/></svg>'

# Client asked (Nov 2026) to hide every Find Dealer / Dealer Locator button for now.
# Flip to True to bring them all back (the header button is SHOW_FIND_DEALER in assets/js/main.js).
SHOW_DEALER_BUTTONS = False
FIND_DEALER_BTN = '<a class="btn btn--primary btn--sm" href="dealers.html">FIND DEALER</a>' if SHOW_DEALER_BUTTONS else ''
DEALER_LOCATOR_BTN = f'      <div><a class="btn btn--primary btn--sm" href="dealers.html">DEALER LOCATOR {ARROW}</a></div>\n' if SHOW_DEALER_BUTTONS else ''

def shell(page, title, desc, body, extra_head='', extra_js=''):
    logo = LOGO.replace('role="img" aria-label="Marshal Tire"', 'aria-hidden="true" focusable="false"')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow"><link rel="icon" href="/marshaltire/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
{extra_head}<link rel="stylesheet" href="assets/css/styles.css?v={ver('assets/css/styles.css')}">
<link rel="stylesheet" href="assets/css/feedback.css?v={ver('assets/css/feedback.css')}">
</head>
<body data-page="{page}">
<a class="skip-link" href="#main">Skip to content</a>
<template id="logo-tpl">{logo}</template>
<header id="site-header"></header>
<main id="main">
{body}
</main>
<footer id="site-footer"></footer>
{extra_js}<script src="assets/js/main.js?v={ver('assets/js/main.js')}"></script>
<script src="assets/js/feedback-config.js?v={ver('assets/js/feedback-config.js')}"></script>
<script src="assets/js/feedback.js?v={ver('assets/js/feedback.js')}"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- WARRANTY BADGES
# Source art from the client (Images/Badges in Dropbox) lives in build/badges/<slug>.svg, drawn in white.
# We write two colourways next to the other images:
#   badge-<slug>-light.svg  dark ink, for light backgrounds (warranty band)
#   badge-<slug>-dark.svg   brand yellow on black-filled shields, for photos and dark tiles
BADGE_ALT = {
  'mf41': 'Limited treadwear warranty: 55,000 miles on P-metric sizes, 50,000 miles on LT metric sizes',
  'ml41': 'Limited treadwear warranty: 60,000 miles on P-metric sizes, 50,000 miles on LT metric sizes',
  'mh41': 'Limited treadwear warranty: 60,000 miles',
  'mu41': 'Limited treadwear warranty: 50,000 miles',
}
def badge_files(slug):
    src = (ROOT / 'build/badges' / f'{slug}.svg').read_text()
    src = src.replace('#F4F4F4', 'white')
    w, h = re.search(r'width="([\d.]+)" height="([\d.]+)"', src).groups()
    light = src.replace('"white"', '"#1a1a1a"')
    # shield outlines are the stroked curve paths (no fill); fill them black for the dark version
    dark = re.sub(r'<path d="(M[^"]*C[^"]*)"([^>]*stroke="white")', r'<path d="\1" fill="#000"\2', src)
    dark = dark.replace('"white"', '"#e3b21e"')
    if float(w) > float(h):  # P-metric / LT pair: sit it on a black tile so the small labels read over a photo
        W, H, pad = float(w), float(h), 8
        dark = dark.replace(f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"', f'<svg width="{W+2*pad:g}" height="{H+2*pad:g}" viewBox="{-pad} {-pad} {W+2*pad:g} {H+2*pad:g}"', 1)
        dark = dark.replace('xmlns="http://www.w3.org/2000/svg">', f'xmlns="http://www.w3.org/2000/svg">\n<rect x="{-pad}" y="{-pad}" width="{W+2*pad:g}" height="{H+2*pad:g}" rx="10" fill="#000"/>', 1)
    out = {'w': w, 'h': h}
    for kind, svg in (('light', light), ('dark', dark)):
        fn = f'badge-{slug}-{kind}.svg'
        (ROOT / 'assets/img' / fn).write_text(svg)
        out[kind] = 'assets/img/' + fn
    return out

# ---------------------------------------------------------------- HOME
HERO_BADGE = badge_files('mh41')['dark']
TIRE_URL = {'All Terrain': 'tire-details.html', 'Highway Terrain': 'tire-highway-terrain.html', 'Tour A/S': 'tire-tour-as.html', 'Sport A/S': 'tire-sport-as.html'}
def card(name, line, img, tag):
    return f'''<article class="pcard">
  <span class="badge">{tag}</span>
  <h3>Marshal {name}</h3><p class="sub">{line}</p>
  <img src="assets/img/{img}" alt="Marshal {name} tire" width="220" height="250" loading="lazy">
  <a class="btn btn--outline-brand" href="{TIRE_URL[name]}">View Tire {ARROW}</a>
</article>'''

home = f'''
<section class="hero" data-slider aria-roledescription="carousel" aria-label="Marshal Tire highlights">
  <div class="slides">
    <div class="slide is-active" role="group" aria-roledescription="slide" aria-label="1 of 2">
      <div class="slide-copy">
        <p class="eyebrow">Marshal Tire</p>
        <h1>Built to perform.</h1>
        <div class="slide-text"><p>Dependable performance. Extensive coverage. Backed by US support.</p><p>Marshal is built around what matters most on the road: <strong>confidence, safety, and dependable performance.</strong> Engineered to deliver reliable handling, braking, and control across everyday driving conditions, Marshal gives drivers the assurance they need mile after mile.</p></div>
        <div class="actions"><a class="btn btn--primary btn--lg" href="#range">EXPLORE LINEUP {ARROW}</a></div>
      </div>
      <div class="slide-photo" style="background-image:url(assets/img/hero-truck.jpg)">
        <div class="stats" aria-label="Lineup at a glance"><div><strong>4</strong><span>tire lines</span></div><div><strong>122</strong><span>fitments</span></div><div><strong>14–22"</strong><span>rim sizes</span></div></div>
      </div>
      <div class="slide-art"><img class="tire" src="assets/img/tire-mf41.webp" alt="Marshal All Terrain MF41 tire" width="330" height="505"></div>
    </div>
    <div class="slide" role="group" aria-roledescription="slide" aria-label="2 of 2">
      <div class="slide-copy">
        <p class="eyebrow">Mileage warranty</p>
        <h2>Confidence for the miles ahead.</h2>
        <p>Dependable performance. Extensive coverage. Backed by US support.</p>
        <div class="actions"><a class="btn btn--primary btn--lg" href="warranty.html#replacement">VIEW WARRANTY DETAILS {ARROW}</a></div>
      </div>
      <div class="slide-photo" style="background-image:url(assets/img/hero-warranty.jpg)"></div>
      <div class="slide-art slide-art--shield"><img class="shield" src="{HERO_BADGE}" alt="Limited treadwear warranty: up to 60,000 miles" width="100" height="134"></div>
    </div>
  </div>
  <div class="hero-controls">
    <div class="dots" role="group" aria-label="Choose slide"></div>
    <div class="ctrl-group">
      <button class="ctrl" data-prev type="button" aria-label="Previous slide">{ARROW_L}</button>
      <button class="ctrl" data-next type="button" aria-label="Next slide">{ARROW_R}</button>
    </div>
  </div>
</section>

<section class="section section--subtle">
  <div class="container">
    <form class="finder" id="finder" aria-labelledby="finder-title">
      <div class="intro">
        <span class="badge badge--dot">Tire Finder</span>
        <h2 id="finder-title">Find your fit</h2>
        <p>Search by vehicle or tire size to find the right Marshal tires for your drive.</p>
        <div class="actions">{FIND_DEALER_BTN}<a class="btn btn--outline btn--sm" href="#range">SEE ALL TIRES</a></div>
      </div>
      <div>
        <div class="seg" role="tablist" aria-label="Search by">
          <button type="button" role="tab" aria-selected="true" aria-controls="by-vehicle">By Vehicle</button>
          <button type="button" role="tab" aria-selected="false" aria-controls="by-size">By Size</button>
        </div>
        <div class="finder-fields" id="by-vehicle" role="tabpanel">
          <label class="sr-only" for="f-year">Year</label><select class="select" id="f-year"><option value="">Year</option></select>
          <label class="sr-only" for="f-make">Make</label><select class="select" id="f-make"><option value="">Make</option></select>
          <label class="sr-only" for="f-model">Model</label><select class="select" id="f-model" disabled><option value="">Model</option></select>
          <label class="sr-only" for="f-trim">Trim</label><select class="select" id="f-trim" disabled><option value="">Trim</option></select>
        </div>
        <div class="finder-fields" id="by-size" role="tabpanel" hidden style="grid-template-columns:repeat(3,1fr)">
          <label class="sr-only" for="s-width">Width</label><select class="select" id="s-width"><option value="">Width</option>{''.join(f'<option>{w}</option>' for w in [175,185,195,205,215,225,235,245,255,265,275,285])}</select>
          <label class="sr-only" for="s-aspect">Aspect ratio</label><select class="select" id="s-aspect"><option value="">Aspect ratio</option>{''.join(f'<option>{a}</option>' for a in [40,45,50,55,60,65,70,75,85])}</select>
          <label class="sr-only" for="s-rim">Rim</label><select class="select" id="s-rim"><option value="">Rim diameter</option>{''.join(f'<option>{r}</option>' for r in [14,15,16,17,18,19,20,22])}</select>
        </div>
        <div class="finder-submit"><button class="btn btn--secondary btn--sm" type="submit">FIND TIRES</button></div>
      </div>
    </form>
  </div>
</section>

<section class="section" id="range">
  <div class="container">
    <div class="range-head">
      <div><span class="badge badge--dot">Product Catalog</span><h2>Explore the range</h2><p>Whether it’s your daily commute or your next adventure, Marshal has the right tires for your journey.</p></div>
      <a class="link" href="#range" style="display:inline-flex;gap:6px;align-items:center;font-size:14px">View all tires <span style="display:inline-flex;width:16px">{ARROW_R}</span></a>
    </div>
    <div class="cards-4">
      {card('Sport A/S', 'All-Season', 'tire-mu41.webp', 'All Season')}
      {card('Tour A/S', 'Touring', 'tire-mh41.webp', 'All Season')}
      {card('Highway Terrain', 'Highway Terrain', 'tire-ml41.webp', 'Summer')}
      {card('All Terrain', 'All Terrain', 'tire-mf41.webp', 'Summer')}
    </div>
  </div>
</section>

<section class="cta-dark">
  <div class="container">
    <h2>Let’s stay connected</h2>
    <p>Have a question about Marshal tires, warranty coverage, or anything else? We’re here to help.</p>
    <p>Count on Marshal Tire for reliable tire information, warranty guidance, and customer support, every mile of the way.</p>
    <a class="btn btn--primary btn--lg" href="contact.html">CONTACT US</a>
  </div>
</section>'''

# ---------------------------------------------------------------- ABOUT
about = f'''
<section class="about-hero">
  <div class="container">
    <p class="eyebrow">About Marshal</p>
    <h1>Built to Perform.</h1>
    <p>Whether it’s your daily commute or your next adventure, Marshal has the right tires for your journey.</p>
    <a class="btn btn--primary" href="index.html#range">EXPLORE OUR TIRES {ARROW}</a>
  </div>
</section>
<section class="section mission" aria-labelledby="mission-title">
  <div class="container">
    <span class="dash" aria-hidden="true"></span>
    <h2 class="eyebrow" id="mission-title">Our mission</h2>
    <p class="mission-quote">Marshal is built around what matters most on the road: <strong>confidence, safety, and dependable performance</strong>. Engineered to deliver reliable handling, braking, and control across everyday driving conditions, Marshal gives drivers the assurance they need mile after mile.</p>
  </div>
</section>
<section class="dealer-band">
  <div class="container">
    <div><h2>Closer than you think.</h2><p style="opacity:.85;margin-top:8px">Find a Marshal dealer near you.</p></div>
    <form action="dealers.html" method="get">
      <label class="sr-only" for="about-zip">ZIP code</label>
      <input class="input" id="about-zip" name="q" type="text" inputmode="numeric" placeholder="Enter your zipcode." autocomplete="postal-code" required>
      <button class="btn btn--primary" type="submit">SEARCH</button>
    </form>
  </div>
</section>'''

# ---------------------------------------------------------------- TIRE DETAILS
def tech(img, h, p):
    return f'<article class="tech"><img src="assets/img/{img}" alt="" width="250" height="124" loading="lazy"><h3>{h}</h3><p>{p}</p></article>'
icons = lambda names: ''.join(f'<img src="assets/img/icon-{n}.png" alt="{a}" width="72" height="72">' for n, a in names)
# Vehicle category pictograms (client art, Images/Icons/SVG). Labels are set in HTML so they use the site font.
# Which tire fits which category comes from MS_Applicable vehicle.xlsx (vehicles listed per size).
VEHICLE_LABEL = {'compact': 'Compact', 'sedan': 'Sedan', 'truck': 'Truck', 'suv': 'SUV', 'van': 'Van', 'sport': 'Sports'}
def vehicle_icons(names):
    out = []
    for n in sorted(names, key=list(VEHICLE_LABEL).index):
        vb = re.search(r'viewBox="([^"]+)"', (ROOT / f'assets/img/vehicle-{n}.svg').read_text()).group(1).split()
        w, h = round(float(vb[2]) / 5.8), round(float(vb[3]) / 5.8)
        out.append(f'<div class="vt"><img src="assets/img/vehicle-{n}.svg" alt="" width="{w}" height="{h}"><span>{VEHICLE_LABEL[n]}</span></div>')
    return ''.join(out)
MF41_BADGE = badge_files('mf41')
details = f'''
<section class="section section--subtle" style="padding-top:56px">
  <div class="container td-top">
    <div class="thumbs" aria-label="Product images">
      <button class="thumb-nav" data-dir="-1" type="button" aria-label="Previous image">{UPCH}</button>
      <button class="thumb" type="button" aria-pressed="true" data-src="assets/img/tire-mf41.webp" data-alt="Marshal All Terrain MF41, angled view"><img src="assets/img/tire-mf41.webp" alt="Angled view"></button>
      <button class="thumb" type="button" aria-pressed="false" data-src="assets/img/thumb-mf41-side.webp" data-alt="Marshal All Terrain MF41, side view"><img src="assets/img/thumb-mf41-side.webp" alt="Side view"></button>
      <button class="thumb" type="button" aria-pressed="false" data-src="assets/img/thumb-mf41-tread.webp" data-alt="Marshal All Terrain MF41, tread view"><img src="assets/img/thumb-mf41-tread.webp" alt="Tread view"></button>
      <button class="thumb thumb--dark" type="button" aria-pressed="false" data-overlay="off" data-src="{MF41_BADGE['dark']}" data-alt="{BADGE_ALT['mf41']}"><img src="{MF41_BADGE['dark']}" alt="Warranty badges"></button>
      <button class="thumb-nav" data-dir="1" type="button" aria-label="Next image" style="transform:rotate(180deg)">{UPCH}</button>
    </div>
    <div class="main-image"><img id="main-image" src="assets/img/tire-mf41.webp" alt="Marshal All Terrain MF41, angled view" width="260" height="380"><img class="badge-overlay" src="{MF41_BADGE['dark']}" alt="{BADGE_ALT['mf41']}" width="189" height="135"></div>
    <div class="td-info">
      <h1>MARSHAL ALL TERRAIN</h1>
      <p class="segment">SEGMENT | ALL TERRAIN</p>
      <h2 class="benefits-title">Key benefits</h2>
      <ul class="bul"><li>All-season performance</li><li>Improved highway ride</li><li>Off-road capability</li><li>Enhanced mileage</li><li>Enhanced wet &amp; snow performance</li></ul>
      <div class="td-attrs">
        <div><h2><span class="dash"></span>Vehicle Type</h2><div class="icon-row">{vehicle_icons(['truck', 'suv', 'van'])}</div></div>
      </div>
      <div class="size-hint">{INFO}<div><p>Your size is on your tire’s sidewall, like 225/35 R18 or check the vehicle manual.</p><a href="#available-sizes">See available sizes {DOWN}</a></div></div>
{DEALER_LOCATOR_BTN}    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="section-title" style="margin-bottom:32px">Applied Technology</h2>
    <div class="tech-grid">
      {tech('tech-grooves.jpg','Circumferential Grooves','Application of a tier designed full depth circumferential groove improves all-season traction.')}
      {tech('tech-pitch.jpg','Special Pitch Design','Zig-Zag dual pitch design in the center block improves off-road traction &amp; enhances stiffness for a quality everyday drive.')}
      {tech('tech-blocks.jpg','Angular Tread Blocks','Angular chamfer cut tread blocks enhance off-road capabilities.')}
      {tech('tech-polymer.jpg','Optimal Polymer','Optimal polymer blend ratio improves wear, resists cracking, chipping and tearing.')}
    </div>
  </div>
</section>
<section class="section section--subtle" id="warranty-coverage">
  <div class="container">
    <h2 class="section-title" style="margin-bottom:40px">Warranty &amp; coverage</h2>
    <div class="warranty-band">
      <img class="wb-badges" src="{MF41_BADGE['light']}" alt="{BADGE_ALT['mf41']}" width="189" height="135" loading="lazy">
      <div class="wb-copy">
        <img class="wb-wordmark" src="assets/img/wordmark-all-terrain.png" alt="Marshal All Terrain" width="193" height="34" loading="lazy">
        <h3>Limited treadwear warranty</h3>
        <p>Marshal All Terrain comes with a limited treadwear warranty. P-metric and LT sizes carry different mileage, so check the size chart for yours.</p>
        <a class="link wb-link" href="warranty.html#replacement">See full warranty terms <span aria-hidden="true">{ARROW_R}</span></a>
      </div>
    </div>
  </div>
</section>
<section class="section" id="available-sizes">
  <div class="container">
    <div class="sizes-head"><h2 class="section-title">Available sizes</h2></div>
    <div class="filter-row">
      <div class="field"><label for="size-filter" style="font-weight:400">Filter by tire size</label><div class="filter-wrap"><input class="input" id="size-filter" type="search" placeholder="e.g. 225 or R18 or 225/35 R18" autocomplete="off">{SEARCH}</div></div>
      <button class="howto-toggle" id="howto-toggle" type="button" aria-expanded="true" aria-controls="howto">Where can I find my tire size? {UPCH}</button>
    </div>
    <div class="howto" id="howto">
      <div><h3>Check the side of your tire.</h3><p class="muted">Or check the vehicle manual.</p></div>
      <div class="code" aria-label="Example size 225/35 R18"><div><b>225</b><small>Width</small></div><span class="slash">/</span><div><b>35</b><small>Profile</small></div><div><b>R18</b><small>Rim diameter</small></div></div>
      <img src="assets/img/sidewall.png" alt="" width="295" height="120">
    </div>
    <div class="acc" id="size-accordion" data-line="MF41" data-name="All Terrain"></div>
  </div>
</section>'''

# ---------------------------------------------------------------- OTHER TIRE LINES
# Copy comes from the "Explore the range" tabs in Figma (Layout page). Their per-size spec sheets
# aren't in the project yet, so the size chart shows a placeholder until we get them.
OTHER_TIRES = [
  dict(file='tire-highway-terrain.html', code='ML41', slug='ml41', name='Highway Terrain', segment='HIGHWAY ALL-SEASON', war='60,000',
       war_note='P-metric sizes carry up to 60,000 miles and LT sizes up to 50,000 miles, so check the size chart for yours.',
       bullets=['Enhanced handling &amp; traction', 'Stable &amp; comfortable driving', 'Excellent wet &amp; snow performance', 'Improved all-weather capability', 'Enhanced mileage'],
       vehicles=['truck', 'suv', 'van'],
       tech=[('Side Block Rib Design', 'Provides grip during acceleration and improves braking in wet and dry conditions.'),
             ('Solid Center Rib', 'Application of a solid center rib tread design enhances stable driving and a comfortable ride.'),
             ('Special Sipe Design', 'Sipe design provides enhanced wet and snow performance.'),
             ('Optimal Polymer', 'Optimal polymer blend in the compound improves wear and durability.')]),
  dict(file='tire-tour-as.html', code='MH41', slug='mh41', name='Tour A/S', segment='GRAND TOURING ALL-SEASON', war='60,000',
       war_note='Every size carries up to 60,000 miles of coverage.',
       bullets=['Superb wet traction', 'Smooth, comfortable ride', 'Excellent dry &amp; wet braking', 'Dependable mileage', 'Exceptional winter handling'],
       vehicles=['compact', 'sedan', 'truck', 'suv', 'van', 'sport'],
       tech=[('Wide Grooves', 'Four wide grooves evacuate water quickly for excellent wet traction.'),
             ('Asymmetric Tread Design', 'Advanced asymmetric tread creates an oversized contact area.'),
             ('Innovative Compound', 'Innovative compound &amp; balanced contact patch for enhanced wear resistance and even wear across the tread.'),
             ('Angled Snow Sipes', 'Precisely angled snow sipes create tiny gripping edges that are fine-tuned for traction on cold, slick surfaces.')]),
  dict(file='tire-sport-as.html', code='MU41', slug='mu41', name='Sport A/S', segment='ULTRA HIGH PERFORMANCE ALL-SEASON', war='50,000',
       war_note='Every size carries up to 50,000 miles of coverage.',
       bullets=['Exceptional comfort: reduced noise', 'All-season capability', 'Enhanced traction in dry and wet', 'Precise handling and cornering', 'Excellent dry &amp; wet braking', 'Upgraded mileage'],
       vehicles=['compact', 'sedan', 'suv', 'sport'],
       tech=[('Groove Angle/Ground Shape', 'Groove angle considering ground shape along with pitch arrangement of different lengths.'),
             ('Wide Straight Grooves', 'Four wide straight grooves in the driving direction.'),
             ('Advanced Tie Bars', 'Application of tie bars within the tread design improves handling and stability.'),
             ('New Generation Polymer', 'New generation polymer to improve wear &amp; grip.')]),
]

def other_details(t):
    full = f"Marshal {t['name']}"
    badge = badge_files(t['slug'])
    war_alt = BADGE_ALT[t['slug']]
    pair = ' badge-pair' if t['slug'] == 'ml41' else ''
    img = lambda kind: f"assets/img/thumb-{t['slug']}-{kind}.webp"
    return f'''
<section class="section section--subtle" style="padding-top:56px">
  <div class="container td-top">
    <div class="thumbs" aria-label="Product images">
      <button class="thumb-nav" data-dir="-1" type="button" aria-label="Previous image">{UPCH}</button>
      <button class="thumb" type="button" aria-pressed="true" data-src="assets/img/tire-{t['slug']}.webp" data-alt="{full} {t['code']}, angled view"><img src="assets/img/tire-{t['slug']}.webp" alt="Angled view"></button>
      <button class="thumb" type="button" aria-pressed="false" data-src="{img('side')}" data-alt="{full} {t['code']}, side view"><img src="{img('side')}" alt="Side view"></button>
      <button class="thumb" type="button" aria-pressed="false" data-src="{img('tread')}" data-alt="{full} {t['code']}, tread view"><img src="{img('tread')}" alt="Tread view"></button>
      <button class="thumb thumb--dark" type="button" aria-pressed="false" data-overlay="off" data-src="{badge['dark']}" data-alt="{war_alt}"><img src="{badge['dark']}" alt="Warranty badge"></button>
      <button class="thumb-nav" data-dir="1" type="button" aria-label="Next image" style="transform:rotate(180deg)">{UPCH}</button>
    </div>
    <div class="main-image"><img id="main-image" src="assets/img/tire-{t['slug']}.webp" alt="{full} {t['code']}, angled view" width="260" height="380"><img class="badge-overlay{'' if pair else ' badge-overlay--single'}" src="{badge['dark']}" alt="{war_alt}" width="{badge['w']}" height="{badge['h']}"></div>
    <div class="td-info">
      <h1>{full.upper()}</h1>
      <p class="segment">SEGMENT | {t['segment']}</p>
      <h2 class="benefits-title">Key benefits</h2>
      <ul class="bul">{''.join(f'<li>{b}</li>' for b in t['bullets'])}</ul>
      <div class="td-attrs">
        <div><h2><span class="dash"></span>Vehicle Type</h2><div class="icon-row">{vehicle_icons(t['vehicles'])}</div></div>
      </div>
      <div class="size-hint">{INFO}<div><p>Your size is on your tire’s sidewall, like 225/35 R18 or check the vehicle manual.</p><a href="#available-sizes">See available sizes {DOWN}</a></div></div>
{DEALER_LOCATOR_BTN}    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="section-title" style="margin-bottom:32px">Applied Technology</h2>
    <div class="tech-grid">
      {''.join(tech(f"tech-{t['slug']}-{i}.jpg", h, d) for i, (h, d) in enumerate(t['tech'], 1))}
    </div>
  </div>
</section>
<section class="section section--subtle" id="warranty-coverage">
  <div class="container">
    <h2 class="section-title" style="margin-bottom:40px">Warranty &amp; coverage</h2>
    <div class="warranty-band">
      <div class="wb-badges wb-badges--shield{pair}"><img src="{badge['light']}" alt="{war_alt}" width="{badge['w']}" height="{badge['h']}" loading="lazy"></div>
      <div class="wb-copy">
        <p class="wb-name">{full.upper()}</p>
        <h3>Limited treadwear warranty</h3>
        <p>{full} comes with a limited treadwear warranty. {t['war_note']}</p>
        <a class="link wb-link" href="warranty.html#replacement">See full warranty terms <span aria-hidden="true">{ARROW_R}</span></a>
      </div>
    </div>
  </div>
</section>
<section class="section" id="available-sizes">
  <div class="container">
    <div class="sizes-head"><h2 class="section-title">Available sizes</h2></div>
    <div class="filter-row">
      <div class="field"><label for="size-filter" style="font-weight:400">Filter by tire size</label><div class="filter-wrap"><input class="input" id="size-filter" type="search" placeholder="e.g. 225 or R18 or 225/35 R18" autocomplete="off">{SEARCH}</div></div>
      <button class="howto-toggle" id="howto-toggle" type="button" aria-expanded="true" aria-controls="howto">Where can I find my tire size? {UPCH}</button>
    </div>
    <div class="howto" id="howto">
      <div><h3>Check the side of your tire.</h3><p class="muted">Or check the vehicle manual.</p></div>
      <div class="code" aria-label="Example size 225/35 R18"><div><b>225</b><small>Width</small></div><span class="slash">/</span><div><b>35</b><small>Profile</small></div><div><b>R18</b><small>Rim diameter</small></div></div>
      <img src="assets/img/sidewall.png" alt="" width="295" height="120">
    </div>
    <div class="acc" id="size-accordion" data-line="{t['code']}" data-name="{t['name']}"></div>
  </div>
</section>'''

# ---------------------------------------------------------------- DEALERS
dealers = f'''
<section class="page-intro" style="background:var(--surface-subtle);padding-bottom:24px">
  <div class="container"><span class="badge badge--dot">Find Dealer</span><h1>Find a Marshal Dealer</h1><p>Use your location to find authorized Marshal Tire dealers.</p></div>
</section>
<section style="background:var(--surface-subtle);padding-bottom:80px">
  <div class="container dealer-layout">
    <div id="map" role="region" aria-label="Map of Marshal dealers"></div>
    <div class="dealer-panel">
      <form class="dealer-search" id="dealer-form">
        <label for="dealer-q" style="font-size:14px">Search Address</label>
        <div class="inline"><input class="input" id="dealer-q" type="search" placeholder="Enter your address" autocomplete="postal-code"><button class="btn btn--primary" type="submit">SEARCH</button></div>
        <button class="link geo" id="use-location" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/><circle cx="12" cy="12" r="8"/></svg>Use my location</button>
      </form>
      <p class="dealer-status" id="dealer-status" role="status">Showing all dealers. Search to sort by distance.</p>
      <ul class="dealer-list" id="dealer-list"></ul>
    </div>
  </div>
</section>
<section class="shop-online" aria-labelledby="shop-title">
  <div class="container">
    <span class="badge badge--dot">Shop online</span>
    <h2 id="shop-title">Buy Marshal Tires Online</h2>
    <p class="shop-sub">Pick your tire and shop it at a trusted online retailer.</p>
    <div class="shop-panel">
      <div class="shop-step">
        <h3><span class="step-num" aria-hidden="true">1</span><label for="shop-tire">Choose Your Tire</label></h3>
        <select class="select" id="shop-tire">
          <option value="Marshal All Terrain">Marshal All Terrain</option>
          <option value="Marshal Highway Terrain">Marshal Highway Terrain</option>
          <option value="Marshal Tour A/S">Marshal Tour A/S</option>
          <option value="Marshal Sport A/S">Marshal Sport A/S</option>
        </select>
        <p class="help">All four Marshal tire lines are listed.</p>
      </div>
      <div class="shop-step shop-step--retailers">
        <h3><span class="step-num" aria-hidden="true">2</span>Pick a Retailer</h3>
        <div class="retailers">
          <a class="retailer" data-retailer="discounttire" href="https://www.discounttire.com/" target="_blank" rel="noopener"><span class="retailer-logo"><img src="assets/img/retailer-discount-tire.png" alt="" width="200" height="58"></span><span class="retailer-action">Shop at Discount Tire {EXT}<span class="sr-only">(opens in a new tab)</span></span></a>
          <a class="retailer" data-retailer="tirerack" href="https://www.tirerack.com/" target="_blank" rel="noopener"><span class="retailer-logo"><img src="assets/img/retailer-tire-rack.png" alt="" width="200" height="42"></span><span class="retailer-action">Shop at Tire Rack {EXT}<span class="sr-only">(opens in a new tab)</span></span></a>
        </div>
        <p class="help">Prices, stock and shipping are set by each retailer.</p>
      </div>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- CONTACT
def opts(items, ph):
    return f'<option value="">{ph}</option>' + ''.join(f'<option value="{v}">{t}</option>' for v, t in items)
def fld(id_, label, ctl, req=True, help_=''):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    h = f'<p class="help" id="{id_}-help">{help_}</p>' if help_ else ''
    return f'<div class="field"><label for="{id_}">{label}{star}</label>{ctl}{h}</div>'
def inp(id_, type_='text', ph='', req=True, auto='', help_=False):
    a = f' autocomplete="{auto}"' if auto else ''
    d = f' aria-describedby="{id_}-help"' if help_ else ''
    return f'<input class="input" id="{id_}" name="{id_}" type="{type_}" placeholder="{ph}"{" required" if req else ""}{a}{d}>'
def sel(id_, items, ph='Choose one', req=True, default=None):
    o = opts(items, ph)
    if default: o = o.replace(f'value="{default}"', f'value="{default}" selected')
    return f'<select class="select" id="{id_}" name="{id_}"{" required" if req else ""}>{o}</select>'
def ta(id_, ph):
    return f'<textarea class="textarea" id="{id_}" name="{id_}" maxlength="1000" placeholder="{ph}" required></textarea><p class="help counter" style="text-align:right">0 / 1,000</p>'
STATES = [(s, s) for s in 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()]
contact = f'''
<section class="page-intro" style="background:var(--surface-subtle)">
  <div class="container"><h1>Contact Us</h1><p>Let us know how we can help. We want to hear from you.<br>Please allow 48 hours for us to respond.</p></div>
</section>
<section style="background:var(--surface-subtle);padding-bottom:96px">
  <div class="container contact-layout">
    <div class="form-card" id="contact-card">
      <div class="aud-tabs" role="tablist" aria-label="Who are you contacting us as?">
        <button type="button" role="tab" data-type="general" aria-selected="true"><b>Customer</b><span>Product questions, warranty claims, where to buy</span></button>
        <button type="button" role="tab" data-type="business" aria-selected="false"><b>Business</b><span>Dealers, fleets, media and partners</span></button>
      </div>
      <form id="contact-form" novalidate>
        <div class="form-alert" role="alert"></div>
        <div data-pane="general" style="display:grid;gap:32px">
          <div class="form-section"><h2>How can we help?</h2>
            {fld('g-request','Request type',sel('g-request',[('support','Technical support'),('warranty','Warranty'),('other','Other questions')],'Choose request type',True,'support'))}
          </div>
          <div class="form-section"><h2>Your details</h2>
            <div class="row-2">{fld('g-first','First name',inp('g-first',ph='ex. James',auto='given-name'))}{fld('g-last','Last name',inp('g-last',ph='ex. Smith',auto='family-name'))}</div>
            <div class="row-2">{fld('g-email','Email',inp('g-email','email','name@example.com',auto='email'))}{fld('g-phone','Phone',inp('g-phone','tel','(555) 555-0123',False,'tel'),False)}</div>
            <div class="row-2">{fld('g-zip','ZIP code',inp('g-zip',ph='ex. 80202',auto='postal-code').replace('type="text"','type="text" inputmode="numeric" maxlength="10" data-rule="zip"'))}</div>
          </div>
          <div class="form-section panel" id="tire-details"><h2>Tire details</h2><p class="muted">Shown for warranty claims and product questions.</p>
            <div class="row-2">{fld('g-line','Tire line',sel('g-line',[('mf41','Marshal All-Terrain'),('ml41','Marshal Highway Terrain'),('mh41','Marshal Tour A/S'),('mu41','Marshal Sport A/S')],'Choose tire line'))}
            <div class="field"><label for="g-size">Tire size</label>{inp('g-size',ph='ex. 265/70R17',req=False,help_=True)}<p class="help" id="g-size-help">Printed on the sidewall. <a class="link" href="tire-details.html#available-sizes" style="font-weight:600">Not sure?</a></p></div></div>
            <div class="row-2">{fld('g-dot','DOT code',inp('g-dot',ph='ex. DOT H2U1 YC7L',req=False,help_=True),False,'Printed on the sidewall after the letters DOT.')}</div>
            <div class="row-2" id="warranty-extra" hidden>{fld('g-date','Purchase date',inp('g-date','date'))}{fld('g-dealer','Where you bought them',inp('g-dealer',ph='Dealer name and city',req=False),False)}</div>
          </div>
          {fld('g-message','Message',ta('g-message','Please leave a message.'))}
        </div>
        <div data-pane="business" hidden style="display:grid;gap:32px">
          <div class="form-section"><h2>How can we help?</h2>
            {fld('b-request','Request type',sel('b-request',[('dealer','Become a Marshal dealer'),('fleet','Fleet sales'),('pop','Merchandising and POP materials'),('media','Media and press'),('other','Something else')],'Choose request type'))}
          </div>
          <div class="form-section"><h2>Your business</h2>
            {fld('b-company','Company name',inp('b-company',ph='ex. Front Range Tire &amp; Auto',auto='organization'))}
            <div class="row-2">{fld('b-type','Business type',sel('b-type',[('dealer','Tire dealer'),('service','Auto service'),('dist','Distributor'),('fleet','Fleet'),('media','Media'),('other','Other')]))}{fld('b-web','Website',inp('b-web','url','www.example.com',False,'url'),False)}</div>
            <div class="row-3">{fld('b-city','City',inp('b-city',ph='ex. Denver',auto='address-level2'))}{fld('b-state','State',sel('b-state',STATES))}{fld('b-zip','ZIP code',inp('b-zip',ph='ex. 80202',auto='postal-code').replace('type="text"','type="text" inputmode="numeric" maxlength="10" data-rule="zip"'))}</div>
            <div class="row-2">{fld('b-locations','Number of locations',sel('b-locations',[('1','1'),('2-5','2–5'),('6-20','6–20'),('20+','More than 20')],req=False),False)}{fld('b-brands','Tire brands you carry now',inp('b-brands',ph='List your main brands',req=False),False)}</div>
          </div>
          <div class="form-section"><h2>Your details</h2>
            <div class="row-2">{fld('b-first','First name',inp('b-first',ph='ex. James',auto='given-name'))}{fld('b-last','Last name',inp('b-last',ph='ex. Smith',auto='family-name'))}</div>
            <div class="row-2">{fld('b-title','Job title',inp('b-title',ph='ex. Store manager',req=False,auto='organization-title'),False)}{fld('b-phone','Phone',inp('b-phone','tel','(555) 555-0123',True,'tel'))}</div>
            {fld('b-email','Work email',inp('b-email','email','name@company.com',auto='email'))}
          </div>
          {fld('b-message','Message',ta('b-message','Tell us about your business and what you’re looking for.'))}
        </div>
        <div class="consent" style="margin-top:32px">
          <label class="check"><input type="checkbox" name="optin"> <span>Send me Marshal Tire news and offers (optional). You can unsubscribe at any time.</span></label>
          <p>By submitting this form, you agree that Marshal Tire will use your information as described in our <a class="link" href="privacy-policy.html">Privacy Policy</a>.</p>
          <div><button class="btn btn--primary btn--lg" type="submit"><span id="submit-label">SEND MESSAGE</span></button></div>
        </div>
      </form>
    </div>
    <aside class="side-card" aria-labelledby="talk">
      <h2 id="talk">Talk to us</h2>
      <div class="side-line"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/></svg><div><small>Phone</small><a href="tel:18444936277">1-844-493-6277</a></div></div>
      <div class="side-line"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h18v12H3zM3 7l9 6 9-6"/></svg><div><small>Email</small><a href="mailto:info@marshaltire.com">info@marshaltire.com</a></div></div>
      <div class="side-line"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6.5 7-11.5C19 5.4 15.9 3 12 3S5 5.4 5 9.5C5 14.5 12 21 12 21z"/><circle cx="12" cy="9.5" r="2"/></svg><div><small>Mail</small><b>Marshal Tire<br>1001 Summit Blvd NE<br>Suite 1800<br>Atlanta, GA 30319</b></div></div>
    </aside>
  </div>
</section>'''

HERO_ALT = f'''
<section class="hero hero--full" data-slider aria-roledescription="carousel" aria-label="Marshal Tire highlights">
  <div class="slides">
    <div class="slide is-active" role="group" aria-roledescription="slide" aria-label="1 of 2" style="--m-size:220% auto;--m-pos:85% 0">
      <div class="slide-bg slide-bg--truck" aria-hidden="true"></div>
      <div class="slide-copy">
        <p class="eyebrow">Marshal Tire</p>
        <h1>Built to perform.</h1>
        <div class="slide-text"><p>Dependable performance. Extensive coverage. Backed by US support.</p><p>Marshal is built around what matters most on the road: <strong>confidence, safety, and dependable performance.</strong> Engineered to deliver reliable handling, braking, and control across everyday driving conditions, Marshal gives drivers the assurance they need mile after mile.</p></div>
        <div class="actions"><a class="btn btn--primary btn--lg" href="#range">EXPLORE LINEUP {ARROW}</a></div>
      </div>
    </div>
    <div class="slide" role="group" aria-roledescription="slide" aria-label="2 of 2" style="--m-size:200% auto;--m-pos:78% 0">
      <div class="slide-bg slide-bg--tires" aria-hidden="true"></div>
      <div class="slide-copy">
        <p class="eyebrow">Mileage warranty</p>
        <h2>Confidence for the miles ahead.</h2>
        <p>Dependable performance. Extensive coverage.<br>Backed by US support.</p>
        <p class="warranty-stat"><span class="ws-prefix">Up to</span><span class="ws-row"><b>60,000</b><span class="ws-unit">Miles<br>Warranty</span></span></p>
        <div class="actions"><a class="btn btn--primary btn--lg" href="warranty.html#replacement">VIEW WARRANTY DETAILS {ARROW}</a><a class="hero-link" href="warranty.html#replacement">See coverage</a></div>
      </div>
    </div>
  </div>
  <div class="hero-controls">
    <div class="dots" role="group" aria-label="Choose slide"></div>
    <div class="ctrl-group">
      <button class="ctrl" data-prev type="button" aria-label="Previous slide">{ARROW_L}</button>
      <button class="ctrl" data-next type="button" aria-label="Next slide">{ARROW_R}</button>
    </div>
  </div>
</section>'''
_a = home.index('<section class="hero" data-slider'); _b = home.index('</section>', _a) + len('</section>')
home_alt = home[:_a] + HERO_ALT.strip() + home[_b:]

# ---------------------------------------------------------------- FEEDBACK REVIEW
review = """
<section class="section fbr">
  <div class="container">
    <p class="eyebrow">Mockup review</p>
    <h1 class="fbr-title">Client feedback</h1>
    <p class="lede fbr-mode"></p>
    <div class="fbr-bar">
      <div class="seg" role="tablist" aria-label="Filter notes">
        <button type="button" role="tab" aria-selected="true" data-f="open">Open</button>
        <button type="button" role="tab" aria-selected="false" data-f="resolved">Resolved</button>
        <button type="button" role="tab" aria-selected="false" data-f="all">All</button>
      </div>
      <button type="button" class="btn btn--outline fbr-csv">Download CSV</button>
    </div>
    <div class="fbr-list" aria-live="polite"><p class="muted">Loading notes…</p></div>
  </div>
</section>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const store = window.MTFeedbackStore, box = document.querySelector('.fbr-list');
  const NAMES = { 'index.html': 'Home', 'index-alt.html': 'Home (split hero)', 'about.html': 'About Us', 'tire-details.html': 'All Terrain', 'tire-highway-terrain.html': 'Highway Terrain', 'tire-tour-as.html': 'Tour A/S', 'tire-sport-as.html': 'Sport A/S', 'dealers.html': 'Find a Dealer', 'contact.html': 'Contact Us', 'tire-registration.html': 'Tire Registration', 'warranty.html': 'Warranty', 'privacy-policy.html': 'Privacy Policy' };
  document.querySelector('.fbr-mode').textContent = store.shared ? 'Every note your client leaves on the stage site, grouped by page.' : 'Demo mode: this list only shows notes saved in this browser. Connect Supabase in assets/js/feedback-config.js to collect notes from everyone.';
  let notes = [], filter = 'open';
  const el = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; };
  const when = iso => new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  const render = () => {
    box.innerHTML = '';
    const shown = notes.filter(n => filter === 'all' || (filter === 'resolved') === (n.status === 'resolved'));
    if (!shown.length) { box.append(el('p', 'muted', filter === 'open' ? 'No open notes. Nice.' : 'Nothing here yet.')); return; }
    const pages = [...new Set(shown.map(n => n.page))];
    pages.forEach(pg => {
      const all = notes.filter(n => n.page === pg), grp = el('section', 'fbr-group');
      const head = el('div', 'fbr-head'); head.append(el('h2', null, NAMES[pg] || pg));
      const a = el('a', 'link', 'Open page'); a.href = pg; head.append(a); grp.append(head);
      shown.filter(n => n.page === pg).forEach(n => {
        const card = el('article', 'fbr-card' + (n.status === 'resolved' ? ' is-resolved' : ''));
        const top = el('div', 'fbr-top');
        top.append(el('span', 'fb-num', all.indexOf(n) + 1), el('b', null, n.author || 'Guest'), el('span', 'muted', when(n.created_at) + (n.vw ? ' · ' + (n.vw < 700 ? 'Mobile' : n.vw < 1100 ? 'Tablet' : 'Desktop') + ' ' + n.vw + 'px' : '')));
        const body = el('p', 'fbr-body', n.body);
        const acts = el('div', 'fbr-acts');
        const view = el('a', 'btn btn--outline', 'View on page'); view.href = pg + '#fb-' + n.id;
        const res = el('button', 'btn ' + (n.status === 'resolved' ? 'btn--outline' : 'btn--primary'), n.status === 'resolved' ? 'Reopen' : 'Mark resolved'); res.type = 'button';
        res.onclick = () => { const st = n.status === 'resolved' ? 'open' : 'resolved'; res.disabled = true; store.update(n.id, { status: st }).then(() => { n.status = st; render(); }); };
        const del = el('button', 'fbr-del', 'Delete'); del.type = 'button';
        const ask = el('span', 'fbr-ask'); ask.hidden = true;
        const yes = el('button', 'fbr-del', 'Yes, delete for everyone'), no = el('button', 'fbr-no', 'Cancel'); yes.type = no.type = 'button';
        ask.append(yes, no);
        del.onclick = () => { del.hidden = true; ask.hidden = false; };
        no.onclick = () => { ask.hidden = true; del.hidden = false; };
        yes.onclick = () => { yes.disabled = true; store.remove(n.id).then(() => { notes = notes.filter(x => x !== n); render(); }).catch(() => { yes.disabled = false; yes.textContent = 'Couldn’t delete. Try again'; }); };
        acts.append(view, res, del, ask);
        card.append(top, body, acts); grp.append(card);
      });
      box.append(grp);
    });
  };
  document.querySelectorAll('.fbr .seg button').forEach(b => b.onclick = () => { filter = b.dataset.f; document.querySelectorAll('.fbr .seg button').forEach(x => x.setAttribute('aria-selected', x === b)); render(); });
  document.querySelector('.fbr-csv').onclick = () => {
    const q = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
    const rows = [['Page', 'Author', 'Date', 'Status', 'Note', 'Screen width'], ...notes.map(n => [NAMES[n.page] || n.page, n.author, n.created_at, n.status, n.body, n.vw])];
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([rows.map(r => r.map(q).join(',')).join('\\n')], { type: 'text/csv' })); a.download = 'marshal-feedback.csv'; a.click();
  };
  store.list().then(r => { notes = r || []; render(); }).catch(() => { box.innerHTML = '<p class="muted">Couldn’t load feedback. Check the Supabase settings and refresh.</p>'; });
});
</script>
"""

# ---------------------------------------------------------------- TIRE REGISTRATION
DOT_ROWS = [
  ('1-manufacturing-plant', 'Manufacturing Plant', 'H2', 'identifies the plant that manufactured the tire.', 'Sidewall close-up with H2, the plant code, circled in red'),
  ('2-tire-size-code', 'Tire Size Code', 'U1', 'is the tire size code.', 'Sidewall close-up with U1, the tire size code, circled in red'),
  ('3-option-code', 'Option Code', 'YC7L', 'an optional code that refers to a brand or other characteristics specific to the tire.', 'Sidewall close-up with YC7L, the option code, circled in red'),
  ('4-date-of-manufacturing', 'Date of Manufacturing', '3805', 'identifies the manufacturing date. The first two digits represent the week and the last two digits represent the year. Therefore, in this example, the tire was manufactured in the 38th week of 2005.', 'Sidewall close-up with 3805, the date code, circled in red'),
]
def dot_row(f, h, code, text, alt):
    return f'''<div class="dot-row">
          <img src="assets/img/dot-{f}.jpg" alt="{alt}" width="584" height="290" loading="lazy">
          <div class="dot-copy"><span class="reg-bar reg-bar--sm" aria-hidden="true"></span><h4>{h}</h4><p class="dot-point"><b>{code}</b>: {text}</p></div>
        </div>'''
TIRE_FIELDS = f'''<div class="row-2">{fld('r-dot','DOT Code',inp('r-dot',ph='DOT H2U1 YC7L'))}{fld('r-mfg','Date of MFG',inp('r-mfg',ph='3805').replace('type="text"','type="text" inputmode="numeric" maxlength="4" data-rule="mfg"'))}</div>
            {fld('r-qty','Quantity',sel('r-qty',[(str(i), str(i)) for i in range(1, 9)],'Number of tires'))}'''
registration = f'''
<section class="page-intro reg-intro">
  <div class="container">
    <h1>Register your Tire Method</h1>
    <p class="reg-sub">Let us know how we can help. We want to hear from you.<br>Please allow 48 hours for us to respond.</p>
    <div class="reg-tabs" role="tablist" aria-label="Tire registration">
      <button type="button" role="tab" id="tab-method" aria-controls="pane-method" aria-selected="true">REGISTER YOUR TIRE METHOD</button>
      <button type="button" role="tab" id="tab-register" aria-controls="pane-register" aria-selected="false" tabindex="-1" data-hash="register">REGISTER YOUR TIRE</button>
    </div>
  </div>
</section>
<section class="reg-body">
  <div class="container">
    <div class="reg-pane" id="pane-method" role="tabpanel" aria-labelledby="tab-method">
      <p class="reg-lede">All Marshal tires are manufactured to a rigid set of manufacturing standards. In the unlikely event of a tire recall, it’s necessary for us to have your contact information on file, so that Marshal Tire USA can notify you quickly.</p>
      <div class="reg-block">
        <span class="reg-bar" aria-hidden="true"></span>
        <h2>How Will This Information Be Used?</h2>
        <p>Your information will be used only to contact you in the event of a recall. Marshal Tire will not sell or rent your contact information to any third party.</p>
        <p>Please enter your contact information and DOT Code(s) below and select “Submit.” Each online submission form allows for up to 8 different DOT Codes to be entered.</p>
      </div>
      <div class="reg-block">
        <span class="reg-bar" aria-hidden="true"></span>
        <h2>What Is a DOT Code?</h2>
        <p>The DOT code is an alphanumeric code that appears on the sidewall of the tire. This code is sometimes referred to as a serial number. Mandated by the U.S. Department of Transportation, it identifies where a tire was manufactured, specific characteristics about the tire and its age.</p>
        <p>The code starts with the DOT designation, followed by a series of letters and numbers. Here’s how to read it</p>
      </div>
      <div class="dot-example">
        <h3>Example Code: DOT H2U1 YC7L 3805</h3>
        {''.join(dot_row(*r) for r in DOT_ROWS)}
      </div>
    </div>
    <div class="reg-pane" id="pane-register" role="tabpanel" aria-labelledby="tab-register" hidden>
      <div class="form-card reg-card" id="reg-card">
        <form id="reg-form" novalidate>
          <div class="form-alert" role="alert"></div>
          <div class="form-section"><h2>Contact Information</h2>
            <div class="row-2">{fld('r-first','First Name',inp('r-first',ph='ex. James',auto='given-name'))}{fld('r-last','Last Name',inp('r-last',ph='ex. Smith',auto='family-name'))}</div>
            {fld('r-email','Email',inp('r-email','email','name@example.com',auto='email'))}
            <div class="row-2">{fld('r-addr','Address',inp('r-addr',ph='Street address',auto='address-line1'))}{fld('r-addr2','Address 2',inp('r-addr2',ph='Apt, suite, unit',req=False,auto='address-line2'),False)}</div>
            <div class="row-3">{fld('r-city','City',inp('r-city',ph='City',auto='address-level2'))}{fld('r-state','State',sel('r-state',STATES,'Select state').replace('<select','<select autocomplete="address-level1"'))}{fld('r-zip','ZIP Code',inp('r-zip',ph='30319',auto='postal-code').replace('type="text"','type="text" inputmode="numeric" maxlength="10" data-rule="zip"'))}</div>
          </div>
          <hr class="reg-rule">
          <div class="form-section"><h2>Dealer Information</h2>
            {fld('r-dealer','Dealer Name',inp('r-dealer',ph='Enter store name'))}
            {fld('r-daddr','Dealer Address',inp('r-daddr',ph='Enter store address'))}
            <div class="row-3">{fld('r-dcity','City',inp('r-dcity',ph='City'))}{fld('r-dstate','State',sel('r-dstate',STATES,'Select state'))}{fld('r-dzip','ZIP Code',inp('r-dzip',ph='30319').replace('type="text"','type="text" inputmode="numeric" maxlength="10" data-rule="zip"'))}</div>
          </div>
          <div class="form-section"><h2>Tire Information</h2>
            {TIRE_FIELDS}
          </div>
          <div class="reg-consent">
            <p class="reg-note"><b aria-hidden="true">*</b> This information will only be used for the purpose of notifying you regarding a recall. Marshal Tire will not sell or rent your contact information to third parties.</p>
            <label class="check reg-check"><input type="checkbox" name="optin"> <span><b>(Optional)</b> Yes, I would like to receive marketing communications from Marshal Tire. My information will be used in accordance with Marshal Tire’s <a class="link" href="privacy-policy.html">Privacy Policy</a>. I may unsubscribe at any time.</span></label>
            <p class="reg-ack">By submitting this form, you acknowledge that your information will be processed in accordance with our <a class="link" href="privacy-policy.html">Privacy Policy</a>.</p>
            <div><button class="btn btn--primary btn--lg reg-submit" type="submit">SUBMIT</button></div>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="cta-dark">
  <div class="container">
    <h2>Let’s stay connected</h2>
    <p>Have a question about Marshal tires, warranty coverage, or anything else? We’re here to help.</p>
    <p>Count on Marshal Tire for reliable tire information, warranty guidance, and customer support, every mile of the way.</p>
    <a class="btn btn--primary btn--lg" href="contact.html">CONTACT US</a>
  </div>
</section>'''

CTA_DARK = '''<section class="cta-dark">
  <div class="container">
    <h2>Let’s stay connected</h2>
    <p>Have a question about Marshal tires, warranty coverage, or anything else? We’re here to help.</p>
    <p>Count on Marshal Tire for reliable tire information, warranty guidance, and customer support, every mile of the way.</p>
    <a class="btn btn--primary btn--lg" href="contact.html">CONTACT US</a>
  </div>
</section>'''
# ---------------------------------------------------------------- WARRANTY + PRIVACY (Figma 697:3624, 697:4155, 698:4464)
# Copy for accordion I and the page heads is from the Marshal Tires file; accordions II+ come from the
# open-state frames in Claude Explorations (92:1246, 93:1253), with Kumho changed to Marshal as in item I.
DOWNLOAD_ICO = '<svg viewBox="0 0 14 15" width="12" height="13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 1v9M3 6.5 7 10.5l4-4M1 14h12"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
ARROW_DN = '<svg viewBox="0 0 10 12" width="10" height="12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 1v10M1.5 7.5 5 11l3.5-3.5"/></svg>'
FOOT = '<p class="w-foot">* See warranty brochure PDF for further details.</p>'

def dots(items):
    return '<ul class="w-dots">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def letters(items):
    # items: list of (letter, html)
    return '<ol class="w-letters">' + ''.join(f'<li><b class="w-ltr" aria-hidden="true">{l}.</b><div>{h}</div></li>' for l, h in items) + '</ol>'
def sub(t):
    return f'<p class="w-sub">{t}</p>'
def note(t='* Not available on Original Equipment Tires'):
    return f'<p class="w-note">{t}</p>'
def wtable(head, rows, cls=''):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    tb = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="w-table-wrap"><table class="w-table {cls}"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'
def acc(pfx, n, roman, title, body, open_=False):
    i = f'{pfx}-acc-{n}'
    return f'''<div class="w-acc{' is-open' if open_ else ''}">
          <h3><button type="button" class="w-acc-head" aria-expanded="{'true' if open_ else 'false'}" aria-controls="{i}"><span class="w-roman">{roman}</span><span class="w-acc-title">{title}</span><span class="w-chev">{CHEV}</span></button></h3>
          <div class="w-acc-body" id="{i}" role="region"{'' if open_ else ' hidden'}>{body}</div>
        </div>'''
EXAMPLE = '<p class="w-example">If R.T.D. = 5 and O.T.D. = 10, the calculation is (5 – 2 : remaining usable tread depth) ÷ (10 – 2 : {w} tread depth) = 38%</p>'
DEALER_LINK = '<a class="w-link" href="dealers.html">www.marshaltireusa.com/dealers</a>'

OE_ACCS = [
  ('I.', 'What Is Covered and for How Long', '<p>Marshal warrants that a tire manufactured by Marshal and/or equipped originally on the vehicle is free from defects in materials and/or workmanship in normal use for the life of the original usable tread. The life of the original usable tread ends when the tire tread has been worn down with only 2/32” (1.6 mm) remaining, at which point the tire is considered to be fully worn out.</p>'
    + sub('PASSENGER AND LIGHT TRUCK TIRES')
    + letters([('A', '<p class="w-strong">Free replacement</p><p>If a Marshal Radial Passenger or Light Truck tire fails as a result of defect in materials and/or workmanship within the first 2/32” of the original tread depth, the tire will be replaced with a new, comparable Marshal tire at no charge including mounting and balancing charges.</p>'),
               ('B', '<p class="w-strong">Pro-rata replacement</p><p>A tire not qualifying for free replacement will be given a credit toward the purchase of a new, comparable Marshal tire based upon the amount of tread actually worn. The cost of mounting, balancing and any other service charges or applicable taxes should be paid by the user. Otherwise adjustment for compensation will be made on a pro-rata basis calculated by multiplying the actual current dealer selling price by the percentage of remaining usable tread depth.</p><p>To obtain the credit percentage, please refer to Adjustment Credit Percentage Table or utilize the following example:</p>' + dots(['R.T.D.: Remaining Tread Depth', 'O.T.D.: Original Tread Depth']) + EXAMPLE.format(w='original usable'))])
    + sub('MARSHAL TEMPORARY TIRE')
    + letters([('A', '<p>A Temporary Tire weighs less and provides more trunk storage space than a conventional tire. To conserve tire tread life, the temporary tire should be returned to the trunk as soon as it is convenient to have your standard tire repaired or replaced.</p>'),
               ('B', '<p>If a Marshal Temporary Tire fails as a result of defect in materials and/or workmanship during the first 50% of usable tread wear, the tire will be replaced with a new, comparable tire at no charge including mounting and balancing charges. No adjustment will be made for tires that are worn more than 50%.</p>')])
    + FOOT),
  ('II.', 'What Is Not Covered by the Warranty', letters([
      ('A', '<p>Irregular wear or tire damage due to:</p>' + dots(['Road hazards such as punctures, cuts, snags, scuffs, carcass bruised or impact breaks.', 'Fire, wreck or collision.', 'Improper inflation, overloading, high speed spinning, improper mounting or demounting, running flat, off-road use, racing, vandalism, willful damage or abuse.', 'Misalignment, wheel imbalance, defective brakes or shock absorber use of tire chains.', 'Any tire which has failed as a result of adding material(e.g. tire fillers, sealant, or balancing substances)'])),
      ('B', '<p>Tires fitted on anything other than original vehicle.</p>'),
      ('C', '<p>Tire worn beyond tread wear indicator (2/32" or 1.6 mm).</p>'),
      ('D', '<p>Tire presented by anyone other than the actual owner-user.</p>'),
      ('E', '<p>Tire branded "NA" (meaning non-adjustable) or "blem" (meaning blemished).</p>'),
      ('F', '<p>Loss of time inconvenience, use of vehicle, or consequential damage.</p>'),
      ('G', '<p>Ride disturbance after free-replacement period.</p>'),
      ('H', '<p>Ozone or weather cracking on tires over four (4) years from the date of manufacture stamped on the tire.</p>'),
      ('I', '<p>No Flat Spot Warranty.</p>'),
      ('J', '<p>NO extended warranties on original equipment tires.</p>'),
      ('K', '<p>Limited warranty applies only to the original owner and is non-transferable.</p>')]) + FOOT),
  ('III.', 'Marshal Obligations', '<p>Replacement tires qualifying under this warranty will be made by a participating Marshal Dealer or a participating Car Dealer.</p>' + FOOT),
  ('IV.', 'Owner’s Obligations', letters([
      ('A', '<p>Conform to all pertaining policies detailed herein.</p>'),
      ('B', '<p>Present tire to any authorized Marshal dealer or a participating Car Dealer along with proof indicating you are the original vehicle owner. Respective dealer will inspect tire in order to identify whether or not it qualifies for warranty based on the policies detailed herein.</p>'),
      ('C', f'<p>To locate an authorized Marshal dealer, use our web address {DEALER_LINK} or call 1-800-HI-MARSHAL (445-8646).</p>')])
    + sub('WARNING FOR YOUR SAFETY') + dots(['AIR PRESSURE', 'LOAD LIMITS', 'SPEED-RATED TIRES', 'HAZARDS', 'DISMOUNTING AND MOUNTING', 'WORN TIRES', 'RIDE DISTURBANCE', 'FOAM TIRE', 'TIRE ROTATION'])),
]
MARSHAL_LINES = 'ALL TERRAIN | HIGHWAY TERRAIN | TOUR A/S | SPORT A/S'
RE_ACCS = [
  ('I.', 'What Is Covered by the Warranty and How Long', '<p>Marshal Tire U.S.A. Inc, 1001 Summit Blvd., NE Suite 1800 Atlanta, GA, 30319, warrants to the original consumer purchaser that all MARSHAL replacement radial tires either directly or through an authorized MARSHAL dealer, and which are mounted on cars within the U.S.A., and becomes unserviceable for any reason within the manufacturers control, such tire will be replaced with an equivalent MARSHAL tire. Should any tire manufactured by Marshal Tire Co., Inc. covered by this warranty become unserviceable due to a material or workmanship condition during its useable tread life (more than 2/32" remaining tread) before 6 years from the date of manufacture or purchase date supported with proof of purchase for every passenger and light truck tire (whichever comes first), and before 5 years (6 years of KLS02e, KLD11e, KLD02(e), KLD01e and KLT12e) from the date of manufacture or purchase date for commercial truck tires (whichever comes first), MARSHAL will do either of the following:</p>'
    + letters([('A', '<p>During the first 2/32" of the original usable tread, Marshal will replace such tire with a comparable new MARSHAL or Marshal tire free of charge. Applicable taxes on the new tire and costs of mounting and balancing and any other service charges are payable by the owner.</p>'),
               ('B', '<p>After the first 2/32" of the original usable tread, a credit percentage will be given toward the purchase price of a comparable new Marshal or Marshal tire effective at the time of adjustment. Applicable taxes on the new tire and costs of mounting and balancing service are payable by the owner.</p><p>To obtain the credit percentage, please refer to Adjustment Credit Percentage Table or utilize the following example:</p>' + dots(['R.T.D.: Remaining Tread Depth', 'O.T.D.: Original Tread Depth']) + EXAMPLE.format(w='original useable')),
               ('C', '<p>Temporary Spare Tire<br>During the first 1/32" of the original usable tread, Marshal will replace such temporary tire with a comparable new Marshal temporary tire free of charge. After the first 1/32" of the original usable tread, but less than 2/32", a credit of 50% towards a comparable new Marshal temporary tire will be given. Applicable taxes and costs of mounting and balancing and any other service charges are payable by the owner.</p>'),
               ('D', '<p>Adjustment on ride complaint or out-of-round is allowed only during the first 2/32" of the original tread depth, and a max of 2 tire can be adjusted per vehicle.</p>')])
    + '<p>The authorized MARSHAL or Marshal dealer will determine the adjustment cost by multiplying the percentage of the original usable tread worn by the current MARSHAL or Marshal dealer\'s price list in effect at the time of adjustment.</p>' + FOOT),
  ('II.', 'What Is Not Covered by the Warranty', letters([
      ('A', '<p>This limited warranty is applicable only in the United States, and any tires used or equipped on a vehicle registered or operated outside the U.S. are not covered by this warranty.</p>'),
      ('B', '<p>Tires branded or marked "Non-Adjustable" (NA) or Blemished (Blem) or DOT/Serial numbers previously cut will not be adjusted.</p>'),
      ('C', '<p>Any tire worn beyond the wear bars (less than 2/32" remaining tread).</p>'),
      ('D', '<p>The cost of applicable taxes and mounting and balancing and any other service charges (Only available for OE tires within 2/32" of original tread depth).</p>'),
      ('E', '<p>Ride Disturbance</p>' + dots(['Worn past the first 2/32nd of tread', 'Three (3) or more tires per vehicle'])),
      ('F', '<p>Tire damage or irregular wear due to:</p>' + dots(['Road hazard, including puncture, cut, impact break, bulge, snag, stone drill, and/or collision.', 'Continued use while run flat or under acute under-inflation.', 'Improper use or operation, without limitation, improper inflation pressure, overloading, use of an improper rim, tire/wheel assembly imbalance or other vehicle condition, worn suspension components, improper mounting or de-mounting, misuse, misapplication, fire or other externally generated heat, water or other material trapped inside the tire during mounting, tire alteration, racing or competition purposes, improper inserting of sealant, balance filler materials and/or chemical corrosion.'])),
      ('G', '<p>Failure to rotate tires at least every 5,000 to 7,500 or according to owner\'s manual.</p>'),
      ('H', '<p>Ozone or weather cracking on tires over four (4) years from the date of manufacture.</p>'),
      ('J', '<p>Loss of time, use, or inconvenience, due to any incidental or consequential damage.</p>'),
      ('K', '<p>Tires that have been modified by the addition or removal of material or any tire intentionally altered to change its appearance.</p>'),
      ('L', '<p>Tire unserviceability caused by tire operation in excess of tire/wheel manufacturers specifications and recommendations.</p>'),
      ('M', '<p>Tires that have become unserviceable due to chemical corrosion, vandalism, chains and flat spotting.</p>'),
      ('N', '<p>Tires involved in any racing-related and commercial activities.</p>'),
      ('O', '<p>This limited warranty applies only to the original purchaser and is non-transferable.</p>')]) + FOOT),
  ('III.', 'Limited Tread Wear Warranty', note()
    + wtable(['TREADWEAR<br>WARRANTY', 'PATTERN', 'COMMENTS'], [
        ['60,000', 'HIGHWAY TERRAIN (ML41)', 'P-METRIC'],
        ['60,000', 'TOUR A/S (MH41)', ''],
        ['55,000', 'ALL TERRAIN (MF41)', 'P-METRIC'],
        ['50,000', 'ALL TERRAIN (MF41) | HIGHWAY TERRAIN (ML41)', 'LT-METRIC'],
        ['50,000', 'SPORT A/S (MU41)', '']], 'w-table--3')
    + FOOT),
  ('IV.', 'Unauthorized Dealer', '<p>Tires purchased from unauthorized MARSHAL dealers do not qualify for the MARSHAL Replacement Equipment Warranty. It is impossible for us to verify that these tires were stored properly, mounted correctly, or originally intended for sale in the United States. For this reason, MARSHAL cannot guarantee the safety or quality of the products purchased from unauthorized marketplace.</p>'
    + '<p>As a consumer, you should only purchase MARSHAL products from an authorized MARSHAL Dealer in order to ensure that the manufacturer\'s warranty is preserved. Please see the Dealer Locator on our website to find an authorized MARSHAL dealer near you.</p>'
    + f'<p>To locate an authorized MARSHAL dealer, use our web address<br>{DEALER_LINK} or call (800) HI-MARSHAL (445-8646).</p>' + FOOT),
  ('V.', 'Replacement Recommendations', letters([
      ('A', '<p>Replacement of two tires: Marshal Tire recommends replacing all four tires at the same time. However, when only two tires are replaced, the new tires should be put on the rear. The newer tires, with deeper tread, may provide better grip and water evacuation in wet driving conditions.</p>'),
      ('B', '<p>Mixing tire manufacturers or models can cause the vehicle to ride differently, depending on the location of the tire.</p>'),
      ('C', '<p>When replacing existing tires, note that different categories like Performance, Touring and Grand Touring have their own characteristics and are not designed to perform the same.</p>'),
      ('D', '<p>Changing performance categories and/or performance ranges can change the way the vehicle performs and can increase noise, harshness, and vibrations (NHV). You should NOT have tires installed that do not meet the requirements of the vehicle.</p>')]) + FOOT),
]
def dl_btn(label):
    return f'<a class="btn btn--primary w-dl" href="#brochure">{DOWNLOAD_ICO}<span>{label}</span></a>'
CALLOUT = '<div class="w-callout"><p>All warranties claims are facilitated by the original seller of the tires. For the most immediate assistance please contact the original retailer.</p></div>'
warranty = f'''
<section class="page-intro reg-intro">
  <div class="container">
    <h1 id="w-title">Replacement Equipment Tire Warranty</h1>
  </div>
</section>
<section class="reg-body w-body">
  <div class="container">
    <div class="reg-pane" id="pane-re">
      <div class="w-head">
        <h2>Replacement Equipment Warranty Policies</h2>
        <p class="w-kicker">Marshal Consumer Warranty for Passenger and Light Truck Tires Marshal Limited Warranty</p>
        <p class="w-lede">Congratulations! You have just purchased high quality tires from Marshal Tire U.S.A. Inc. This limited warranty covers the MARSHAL passenger and light truck tires.</p>
        {CALLOUT}
        <div class="w-dls">{dl_btn('PCR/LTR WARRANTY BROCHURE PDF')}</div>
      </div>
      <div class="w-contact">
        <h3>Warranty Contact Information</h3>
        <p class="w-contact-org">Marshal Tire U.S.A., Incorporated Warranty Department</p>
        <ul class="w-dots">
          <li>1001 Summit Boulevard NE, Suite 1800, Georgia 30319</li>
          <li><a href="tel:18004458646">(800) HI-MARSHAL (445-8646)</a></li>
          <li><a class="w-link" href="mailto:warranty@Marshaltire.com">warranty@Marshaltire.com</a></li>
        </ul>
      </div>
      <div class="w-details">
        <p class="w-effective">Effective : Tires sold on or after Jan 1, 2023</p>
        <div class="w-accs">{''.join(acc('re', k, *a, open_=(k == 0)) for k, a in enumerate(RE_ACCS))}</div>
      </div>
    </div>
  </div>
</section>
{CTA_DARK}'''

PP_SECTIONS = [
  ('legal-notices', 'I.', 'LEGAL NOTICES', 'I. Legal Notices', ''.join(f'<div class="pp-item"><h3>{h}</h3>{b}</div>' for h, b in [
    ('Forward Cross', '<p>Except as otherwise noted, all content and the arrangement of content included on this site, such as text, graphics, logos, icons and images ("Content") is the property of Marshal Tire U.S.A. ("Marshal Tire").</p>'),
    ('Use Limitation', '<p>Unless specifically authorized, you may use this content only for personal, non-commercial purposes, provided this copyright permission notice is included in any copies made for such use. This foregoing limited right does not give you ownership of or a license in any content. You may not otherwise copy, modify, distribute, transmit, display, perform, reproduce, publish, license, any content of this site, or create derivative works from such content, transfer or sell any images, graphics, files, products, information, or services obtained from this site without the express prior written permission of Marshal Tire. By using this site you further agree that you will not "frame" any of the content of this site with advertising, promotional material, information, or other content without the express prior written consent of Marshal Tire. Your unauthorized use of content may violate intellectual property and other laws and may result in your personal, including criminal, liability.</p>'),
    ('No Unlawful or Prohibited Use', '<p>As a condition of your use of this site you guarantee to Marshal Tire that you will not use this site for any purpose that is unlawful or prohibited by these terms, conditions and notices, including, but not limited to, using the copyrighted material, trademarks and trade dress of Marshal Tire without express prior authorization. Further, by using this site you agree that you will not violate or attempt to violate the security or integrity of the site, including, without limitation, accessing data not intended for users of the site; attempting to probe, scan, or test the vulnerability of the site to security breaches; attempting to interfere with service to users of the site (including, without limitation, submitting a virus or corrupted data to the site, overloading the site, or continuously posting repetitive material on the site); attempting to decompile, disassemble, or otherwise reverse engineer the content or software comprising or making up any part of the site; and sending unsolicited advertising or other communications to users of the site.</p>'),
    ('Liability and Warranties Disclaimer', '<p>Marshal Tire makes no representations or warranties of any kind, express or implied, as to the operation of the site, or the information, content, materials, or products included herein that are provided on an "as is" basis. While Marshal Tire endeavors to provide accurate and up-to-date information on this site, this site is provided to you "as is" and "as available" and any use of this site is entirely at your own risk. TO THE FULL EXTENT PERMISSIBLE BY APPLICABLE LAW, MARSHAL TIRE DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, TITLE, NON-INFRINGEMENT, AND MERCHANTABILITY. MARSHAL TIRE WILL NOT BE LIABLE FOR DAMAGES OF ANY KIND ARISING FROM THE USE OF THIS SITE, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, PUNITIVE AND CONSEQUENTIAL DAMAGES OR DAMAGES FOR LOSS OF USE, DATA, OR PROFITS ARISING IN ANY WAY CONNECTED WITH THE USE OR PERFORMANCE OF THIS SITE. The information on this site is of a general nature. Individual driving patterns, tire care, vehicle care and other factors may affect recommendations. Please consult your authorized Marshal Tire dealer before deciding to purchase a tire.</p><p>Marshal Tire also does not represent that any material or products displayed on this site are appropriate or available in any locations outside the United States. Persons outside the United States accessing this site do so at their own risk and are solely responsible for compliance with applicable local laws.</p>'),
    ('Links to Third-Party Vendor Sites', '<p>This site contains links to third-party vendor sites for purposes of tire education and offering merchandise, among others. These links are provided solely as a convenience to you, and the inclusion of any such link does not imply endorsement by Marshal Tire of such third-party site(s) or the contents thereof. MARSHAL TIRE IS NOT RESPONSIBLE FOR THE CONTENTS OF THE LINKED THIRD-PARTY VENDOR SITE(S) AND MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, REGARDING THE CONTENTS, ACCURACY, OR FUNCTIONALITY OF THE LINKED THIRD-PARTY VENDOR SITE(S). IF YOU USE THE LINKED THIRD-PARTY VENDOR SITE(S), YOU DO SO AT YOUR OWN RISK.</p>'),
    ('Access Restriction', '<p>Marshal Tire, in its sole discretion, reserves the right to deny any user access to this site or any portion thereof without notice.</p>'),
    ('Modification of These Terms and Conditions', '<p>Marshal Tire reserves the right to make changes to this site and the disclaimers, terms and conditions herein at any time. Any amendments to these terms will posted on this site and will become effective when posted.</p>'),
    ('Applicable Law', '<p>This site is created and controlled by Marshal Tire U.S.A. Corp., which is located in California. Consequently, the laws of the state of California will govern the use of this site, the Marshal Tire privacy policy, these terms of use and all disclaimers, terms and conditions herein without giving effect to any conflicts of laws rules.</p><p>Effective Date: September 13, 2011</p>')])),
  ('privacy-policy', 'II.', 'PRIVACY POLICY', 'II. Privacy Policy',
    '<p class="pp-lede">Marshal Tire is committed to protecting your privacy. We use any information we obtain about you to communicate with you only. Please read on for more details about our privacy &amp; use policy. Please note that this privacy policy applies only to this website for the United States, and does not apply to information we may obtain from other sources or locations.</p>'
    + '<div class="pp-item"><h3>Marshal Tire’s Collection and Use of Information</h3><div class="pp-subs">'
    + ''.join(f'<div class="pp-sub"><h4>{h}</h4>{b}</div>' for h, b in [
      ('A. Personally Identifiable Information', '<p>We will collect personally identifiable information about you, such as your name, postal address, telephone and mobile numbers, email address, when you provide it to us while on this site such as when you create an account, enter a sweepstake, sign up for newsletters, participate in a survey, contact customer service or otherwise interact with this website. Your personally identifiable information may be used by us for all legal purposes, which may include, but are not limited to, responding to your requests, processing your transactions, for administrative purposes such as conducting contests, tracking which parts of the site are of interest to you and processing prizes. If you choose to opt-in, we may share your personally identifiable information with Marshal Tire\'s subsidiaries or affiliated entities ("Affiliated Entities") for purposes of sending you information about the programs of Marshal Tire or its affiliated entities and, occasionally, sending you advertising/promotional material from some of their advertising and strategic partners. We may also use your personally identifiable information for internal business purposes, such as optimizing site experiences and analyzing and managing our businesses. You may opt-in to receive certain future information or communications (see the Opt-In/Choice section below).</p>'),
      ('B. Demographic Information', '<p>We may also collect demographic data, such as your date of birth, gender and zipcode. Demographic data may be used to tailor your experience at this site, such as showing you content including special events and advertising that you might be interested in, and displaying the content according to your zipcode.</p><p>On occasion, aggregate information that does not identify any particular user may be compiled and shared with subsidiaries and affiliates of Marshal Tire, strategic partners, merchants and advertisers.</p>'),
      ('C. Passive Collection of Non-Personal Information', '<p>This site often requires the use of encrypted or non-encrypted cookies. Cookies are data that a web server transfers to an individual\'s computer for recordkeeping purposes. Cookies are an industry standard used by most websites and help facilitate users\' ongoing access to and use of a particular website; for example, by providing information used to deliver content specific to your interests and for other purposes, such as security and other account administrative functions, and which may track personal identifying information.</p><p>Cookies do not cause damage to your computer systems or files, and only the website that transferred a particular cookie to you can read, modify or delete such cookie. If you do not want information collected through the use of cookies, there are simple procedures in most browsers that allow you to delete existing cookies, to automatically decline cookies or to be given the choice of declining or accepting the transfer of particular cookies to your computer. Please refer to your browser instructions or help screen to learn more about these functions. You should note, however, that declining cookies may make it difficult or impossible for you to use portions of the site.</p><p>Some uses of cookies in connection with the site may be under the control of unaffiliated entities that the company retains for the management of certain programs and fulfillment of specific visitor/customer requests. The company requires these entities to confine their use of cookies to the uses permitted by this policy, but the company cannot be responsible for third-party uses of cookies.</p><p>This information is collected for Marshal Tire\'s internal use such as to enhance website security, to detect broad demographic trends, to assist Marshal Tire in providing content tailored to your interests and to otherwise enhance your experience on this site. This information may also be shared with third parties on an aggregate and non-personally identifiable basis.</p>')])
    + '</div></div>'),
  ('links-third-parties', 'III.', 'LINKS AND THIRD PARTIES\' PRIVACY PRACTICES', 'III. Links and Third Parties’ Privacy Practices',
    '<p class="pp-lede">This site may contain links to other sites that are not operated by Marshal Tire. <b>MARSHAL TIRE U.S.A. COMPANY IS NOT RESPONSIBLE FOR THE PRIVACY PRACTICES OR THE CONTENT OF SUCH OTHER WEBSITES, INCLUDING WEBSITES OPERATED BY AFFILIATED ENTITIES.</b> We provide such links only as a convenience and the inclusion of a link on the site does not imply endorsement of the linked site by Marshal Tire. If you provide any personally identifiable information through any such third-party website, your transaction will occur on such third-party\'s website (and not on this site) and the personally identifiable information you provide will be collected by and controlled by the privacy policy of that third-party. Marshal Tire recommends that you review the privacy policy of third-party websites arrived at from links on this site.</p>'),
  ('security', 'IV.', 'SECURITY', 'IV. Security', '<p class="pp-lede">This site has security measures in place to help protect against the loss, misuse and alteration of the personally identifiable information under its control. Marshal Tire employs security measures consistent with standard industry practice to help protect against public access to personally identifiable and account activity information collected on and used by Marshal Tire at this site.</p>'),
  ('opt-in-choice', 'V.', 'OPT-IN/CHOICE', 'V. Opt-In/Choice', '<p class="pp-lede">This site may provide you with the opportunity to opt-in to receive marketing communications from Marshal Tire. If you do not opt-in, Marshal Tire will not send you its promotional offers. However, regardless of your opt-in preferences, Marshal Tire may still at times need to send program emails for administrative reasons. If you opt to receive communications and then change your election, your opt-out preference may not be effective in certain instances where you agreed to receive brand-specific communications.</p>'),
  ('updates', 'VI.', 'UPDATES TO THIS PRIVACY POLICY', 'VI. Updates to This Privacy Policy', '<p class="pp-lede">Marshal Tire reserves the right to make changes in this privacy policy. In the event that Marshal Tire makes a material change to this privacy policy, it will be posted here. We encourage you to check this page regularly since your continued use of this site following any changes to this privacy policy will be deemed to constitute your acceptance of such change. In the event that Marshal Tire makes a material change to this privacy policy, a notice will be posted regarding such a change.</p>'),
  ('contacting-marshal-tire', 'VII.', 'CONTACTING MARSHAL TIRE', 'VII. Contacting Marshal Tire', '<p class="pp-lede">If you have any questions about this privacy policy or the practices of this site, you may contact:</p><address class="pp-card"><b>Marshal Tire U.S.A.</b><span>Website Customer Care</span><span>1001 Summit Boulevard NE, Suite 1800</span><span>Atlanta, GA 30319</span><span>TEL : <a href="tel:18004458646">1-800-445-8646</a></span></address>'),
]
def toc_link(s):
    return f'<li><a href="#{s[0]}"><span class="pp-roman">{s[1]}</span><span class="pp-toc-t">{s[2]}</span>{ARROW_DN}</a></li>'
privacy = f'''
<section class="page-intro reg-intro">
  <div class="container"><h1>Privacy Policy</h1></div>
</section>
<section class="reg-body pp-body">
  <div class="container pp">
    <p class="pp-intro">Kumho Tire Company, headquartered in the United States (the "Company"), has created this privacy policy for www.Marshaltireusa.com (the "Site") in order to demonstrate its firm commitment to privacy. The following discloses Marshal Tire's information gathering and dissemination practices for the information collected through this site. We encourage you to read this policy before using this site. Your use of this site signifies that you agree with all terms of this policy, so please do not use this site if you disagree with any part of this policy.</p>
    <nav class="pp-toc" aria-label="On this page">
      <ul>{''.join(toc_link(s) for s in PP_SECTIONS[:4])}</ul>
      <ul>{''.join(toc_link(s) for s in PP_SECTIONS[4:])}</ul>
    </nav>
    {''.join(f'<section class="pp-sec" id="{s[0]}" aria-labelledby="{s[0]}-h"><span class="reg-bar" aria-hidden="true"></span><h2 id="{s[0]}-h">{s[3]}</h2><div class="pp-sec-body">{s[4]}</div></section>' for s in PP_SECTIONS)}
  </div>
</section>
{CTA_DARK}'''

LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">\n'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>\n'
SPECS_JS = f'<script src="assets/js/specs.js?v={ver("assets/js/specs.js")}"></script>\n'
pages = {
  'index.html': ('home', 'Marshal Tire | Built to perform', 'Practical tires with the right balance of performance, durability and value.', home_alt, '', ''),
  'index-alt.html': ('home', 'Marshal Tire | Built to perform (split hero)', 'Practical tires with the right balance of performance, durability and value.', home, '', ''),
  'about.html': ('about', 'About Us | Marshal Tire', 'Built around your everyday drive.', about, '', ''),
  'tire-details.html': ('tire-details', 'Marshal All Terrain MF41 | Marshal Tire', 'Marshal All Terrain: technology, warranty and all 25 available sizes.', details, '', SPECS_JS),
  **{t['file']: ('tire-details', f"Marshal {t['name']} {t['code']} | Marshal Tire", f"Marshal {t['name']}: key benefits, warranty and available sizes.", other_details(t), '', SPECS_JS) for t in OTHER_TIRES},
  'dealers.html': ('dealers', 'Find a Dealer | Marshal Tire', 'Find authorized Marshal Tire dealers near you.', dealers, LEAFLET_CSS, LEAFLET_JS),
  'review.html': ('review', 'Client feedback | Marshal Tire mockup', 'All feedback notes left on the mockup.', review, '', ''),
  'contact.html': ('contact', 'Contact Us | Marshal Tire', 'Contact Marshal Tire: customer and business inquiries.', contact, '', ''),
  'tire-registration.html': ('tire-registration', 'Tire Registration | Marshal Tire', 'Register your Marshal tires so we can reach you in the unlikely event of a recall.', registration, '', ''),
  'warranty.html': ('warranty', 'Warranty | Marshal Tire', 'Marshal Replacement Equipment tire warranty policies.', warranty, '', ''),
  'privacy-policy.html': ('privacy', 'Privacy Policy | Marshal Tire', 'How Marshal Tire collects, uses and protects your information.', privacy, '', ''),
}
for fn, (pg, t, d, b, eh, ej) in pages.items():
    # cache-bust every local image so replaced photos show up right away instead of a stale cached copy
    html = re.sub(r'(assets/img/[\w.-]+\.(?:webp|png|jpg|jpeg|svg|avif))(?![?\w])', lambda m: f"{m.group(1)}?v={ver(m.group(1))}" if (ROOT / m.group(1)).exists() else m.group(1), shell(pg, t, d, b, eh, ej))
    (ROOT / fn).write_text(html)
    print('wrote', fn)
