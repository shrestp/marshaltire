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
</body>
</html>
'''

# ---------------------------------------------------------------- HOME
SHIELD = '''<svg class="shield" viewBox="0 0 280 349" role="img" aria-label="Limited treadwear warranty, up to 60,000 miles">
  <path d="M142.45 348.24C141.05 348.79 140.01 349.19 138.86 348.75C108.54 337.08 80.66 320.11 56.42 298.38C33.66 277.97 12.57 251.05 4.27 221.41C1.88 212.9 .04 204.52 .04 195.57L0 68.16L.2 52.21C.22 50.86 .83 49.77 1.84 48.95C11.08 41.47 21 35.5 31.7 30.15C65.85 13.2 102.23 5.49 139.96 0C177.83 5.46 214.35 13.32 248.74 30.35C259.12 35.66 268.72 41.54 277.84 48.68C278.78 49.41 279.65 50.54 279.66 51.79L279.84 72.64L279.9 195.99C278.28 234.37 255.19 268.67 227.9 294.3C203.15 317.55 174.12 335.79 142.45 348.23Z" fill="#010101"/>
  <path transform="translate(6.31 6.3)" d="M133.67 336.17C92.5 320.12 52.23 292 25.98 256.52C11.41 236.83 .05 212.08 .04 187.24L0 67.17L.2 46.82C9 39.92 18.02 34.49 27.84 29.57C61.06 12.98 97.33 5.06 133.97 0C152.94 2.73 171.29 6.15 189.7 10.98C207.67 15.79 224.76 22.12 241.32 30.48C250.42 35.21 259.13 40.42 267.1 46.92L267.31 182.72C267.33 195.92 265.56 208.27 260.96 220.6C256.2 233.37 249.73 245.04 241.64 256.09C232.31 268.74 221.66 280.1 209.7 290.41C187.23 309.78 161.71 325.15 133.67 336.17Z" fill="#fff"/>
  <path transform="translate(16 15)" d="M126.7 317.32C124.73 318.16 123.52 318.23 121.77 317.48C95.48 306.26 71.23 290.92 50.03 271.68C32.39 255.69 15.77 235.17 7.07 213.02C3.18 203.11 .13 192.95 .12 182.09L0 44.68C0 42.99 .48 41.82 1.7 40.92C8.8 35.64 16.2 31.34 24.2 27.38C55.52 12.22 89.21 5.04 123.81 0C143.21 2.53 162.35 6.27 181.38 11.55C196.34 15.69 210.47 20.86 224.36 27.64C232.06 31.52 239.22 35.57 246.04 40.71C247.38 41.73 248 42.77 248 44.69L247.87 182.11C247.86 194.83 243.9 206.86 238.76 218.22C226.95 244.42 205.27 267.14 182.6 284.56C165.38 297.79 146.78 308.74 126.71 317.33Z" fill="#010101"/>
  <g fill="#fff"><rect x="78.3" y="69.6" width="19.6" height="1.8"/><rect x="182.1" y="69.6" width="19.6" height="1.8"/><rect x="64.4" y="236.5" width="151.2" height="1.8"/></g>
  <g font-family="Inter, sans-serif" text-anchor="middle" fill="#fff">
    <text x="140" y="76.3" font-size="16" font-weight="800" letter-spacing=".64">LIMITED</text>
    <text x="140" y="108.2" font-size="21.34" font-weight="800" letter-spacing=".43">TREADWEAR</text>
    <text x="140" y="134" font-size="14.23" font-weight="700" letter-spacing="2.85" fill="#E3B21E">UP TO</text>
    <text x="140" y="191.5" font-size="53.36" font-weight="900" letter-spacing="-2.13">60,000</text>
    <text x="140" y="224.9" font-size="20" font-weight="800" letter-spacing="1.2">MILES</text>
    <text x="140" y="266.4" font-size="21.34" font-weight="800" letter-spacing=".43">WARRANTY</text>
  </g></svg>'''

def card(name, line, img, tag):
    return f'''<article class="pcard">
  <span class="badge">{tag}</span>
  <h3>Marshal {name}</h3><p class="sub">{line}</p>
  <img src="assets/img/{img}" alt="Marshal {name} tire" width="220" height="250" loading="lazy">
  <a class="btn btn--outline-brand" href="tire-details.html">View Tire {ARROW}</a>
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
        <div class="actions"><a class="btn btn--primary btn--lg" href="#warranty">VIEW WARRANTY DETAILS {ARROW}</a></div>
      </div>
      <div class="slide-photo" style="background-image:url(assets/img/hero-warranty.jpg)"></div>
      <div class="slide-art slide-art--shield">{SHIELD}</div>
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
        <div class="actions"><a class="btn btn--primary btn--sm" href="dealers.html">FIND DEALER</a><a class="btn btn--outline btn--sm" href="#range">SEE ALL TIRES</a></div>
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
details = f'''
<section class="section section--subtle" style="padding-top:56px">
  <div class="container td-top">
    <div class="thumbs" aria-label="Product images">
      <button class="thumb-nav" data-dir="-1" type="button" aria-label="Previous image">{UPCH}</button>
      <button class="thumb" type="button" aria-pressed="true" data-src="assets/img/tire-mf41.webp" data-alt="Marshal All Terrain MF41, angled view"><img src="assets/img/tire-mf41.webp" alt="Angled view"></button>
      <button class="thumb" type="button" aria-pressed="false" data-src="assets/img/thumb-mf41-side.webp" data-alt="Marshal All Terrain MF41, side view"><img src="assets/img/thumb-mf41-side.webp" alt="Side view"></button>
      <button class="thumb" type="button" aria-pressed="false" data-src="assets/img/thumb-mf41-tread.webp" data-alt="Marshal All Terrain MF41, tread view"><img src="assets/img/thumb-mf41-tread.webp" alt="Tread view"></button>
      <button class="thumb thumb--dark" type="button" aria-pressed="false" data-overlay="off" data-src="assets/img/warranty-badges-dark.png" data-alt="Limited treadwear warranty: 55,000 miles on P-metric sizes, 50,000 miles on LT metric sizes"><img src="assets/img/warranty-badges-dark.png" alt="Warranty badges"></button>
      <button class="thumb-nav" data-dir="1" type="button" aria-label="Next image" style="transform:rotate(180deg)">{UPCH}</button>
    </div>
    <div class="main-image"><img id="main-image" src="assets/img/tire-mf41.webp" alt="Marshal All Terrain MF41, angled view" width="260" height="380"><img class="badge-overlay" src="assets/img/warranty-badges-dark.png" alt="Limited treadwear warranty: 55,000 miles P-metric, 50,000 miles LT metric" width="141" height="107"></div>
    <div class="td-info">
      <h1>MARSHAL ALL TERRAIN</h1>
      <p class="segment">SEGMENT | ALL TERRAIN</p>
      <h2 class="benefits-title">Key benefits</h2>
      <ul class="bul"><li>All-season performance</li><li>Improved highway ride</li><li>Off-road capability</li><li>Enhanced mileage</li><li>Enhanced wet &amp; snow performance</li></ul>
      <div class="td-attrs">
        <div><h2><span class="dash"></span>Vehicle Type</h2><div class="icon-row">{icons([('sedan','Sedan'),('big-sedan','Big sedan')])}</div></div>
      </div>
      <div class="size-hint">{INFO}<div><p>Your size is on your tire’s sidewall, like 225/35 R18 or check the vehicle manual.</p><a href="#available-sizes">See available sizes {DOWN}</a></div></div>
      <div><a class="btn btn--primary btn--sm" href="dealers.html">DEALER LOCATOR {ARROW}</a></div>
    </div>
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
      <img class="wb-badges" src="assets/img/warranty-badges.png" alt="Limited treadwear warranty: 55,000 miles on P-metric sizes, 50,000 miles on LT metric sizes" width="285" height="204" loading="lazy">
      <div class="wb-copy">
        <img class="wb-wordmark" src="assets/img/wordmark-all-terrain.png" alt="Marshal All Terrain" width="193" height="34" loading="lazy">
        <h3>Limited treadwear warranty</h3>
        <p>Marshal All Terrain comes with a limited treadwear warranty. P-metric and LT sizes carry different mileage, so check the size chart for yours.</p>
        <a class="link wb-link" href="#warranty">See full warranty terms <span aria-hidden="true">{ARROW_R}</span></a>
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
    <div class="acc" id="size-accordion"></div>
  </div>
</section>'''

# ---------------------------------------------------------------- DEALERS
dealers = f'''
<section class="page-intro" style="background:var(--surface-subtle);padding-bottom:24px">
  <div class="container"><span class="badge badge--dot">Find Dealer</span><h1>Find a Marshal dealer</h1><p>Use your location to find authorized Marshal Tire dealers.</p></div>
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
    <h2 id="shop-title">Buy Marshal tires online</h2>
    <p class="shop-sub">Pick your tire and shop it at a trusted online retailer.</p>
    <div class="shop-panel">
      <div class="shop-step">
        <h3><span class="step-num" aria-hidden="true">1</span><label for="shop-tire">Choose your tire</label></h3>
        <select class="select" id="shop-tire">
          <option value="Marshal All Terrain">Marshal All Terrain</option>
          <option value="Marshal Highway Terrain">Marshal Highway Terrain</option>
          <option value="Marshal Tour A/S">Marshal Tour A/S</option>
          <option value="Marshal Sport A/S">Marshal Sport A/S</option>
        </select>
        <p class="help">All four Marshal tire lines are listed.</p>
      </div>
      <div class="shop-step shop-step--retailers">
        <h3><span class="step-num" aria-hidden="true">2</span>Pick a retailer</h3>
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
  <div class="container"><h1>Contact us</h1><p>Let us know how we can help. We want to hear from you.<br>Please allow 48 hours for us to respond.</p></div>
</section>
<section style="background:var(--surface-subtle);padding-bottom:96px">
  <div class="container contact-layout">
    <div class="form-card" id="contact-card">
      <div class="aud-tabs" role="tablist" aria-label="Who are you contacting us as?">
        <button type="button" role="tab" data-type="general" aria-selected="true"><b>General</b><span>Product questions, warranty claims, where to buy</span></button>
        <button type="button" role="tab" data-type="business" aria-selected="false"><b>Business</b><span>Dealers, fleets, media and partners</span></button>
      </div>
      <form id="contact-form" novalidate>
        <div class="form-alert" role="alert"></div>
        <div data-pane="general" style="display:grid;gap:32px">
          <div class="form-section"><h2>How can we help?</h2>
            {fld('g-request','Request type',sel('g-request',[('support','Technical support'),('warranty','Warranty claim')],'Choose request type',True,'support'))}
          </div>
          <div class="form-section"><h2>Your details</h2>
            <div class="row-2">{fld('g-first','First name',inp('g-first',ph='ex. James',auto='given-name'))}{fld('g-last','Last name',inp('g-last',ph='ex. Smith',auto='family-name'))}</div>
            <div class="row-2">{fld('g-email','Email',inp('g-email','email','name@example.com',auto='email'))}{fld('g-phone','Phone',inp('g-phone','tel','(555) 555-0123',False,'tel'),False)}</div>
          </div>
          <div class="form-section panel" id="tire-details"><h2>Tire details</h2><p class="muted">Shown for warranty claims and product questions.</p>
            <div class="row-2">{fld('g-line','Tire line',sel('g-line',[('mf41','All Terrain (MF41)'),('ml41','Highway Terrain (ML41)'),('mh41','Tour A/S (MH41)'),('mu41','Sport A/S (MU41)')],'Choose tire line'))}
            <div class="field"><label for="g-size">Tire size</label>{inp('g-size',ph='ex. 265/70R17',req=False,help_=True)}<p class="help" id="g-size-help">Printed on the sidewall. <a class="link" href="tire-details.html#available-sizes" style="font-weight:600">Not sure?</a></p></div></div>
            <div class="row-2" id="warranty-extra" hidden>{fld('g-date','Purchase date',inp('g-date','date'))}{fld('g-dealer','Where you bought them',inp('g-dealer',ph='Dealer name and city',req=False),False)}</div>
          </div>
          {fld('g-message','Message',ta('g-message','Please leave a message.'))}
        </div>
        <div data-pane="business" hidden style="display:grid;gap:32px">
          <div class="form-section"><h2>How can we help?</h2>
            {fld('b-request','Request type',sel('b-request',[('dealer','Become a Marshal dealer'),('volume','Distributor or volume pricing'),('fleet','Fleet sales'),('pop','Merchandising and POP materials'),('media','Media and press'),('other','Something else')],'Choose request type'))}
          </div>
          <div class="form-section"><h2>Your business</h2>
            {fld('b-company','Company name',inp('b-company',ph='ex. Front Range Tire &amp; Auto',auto='organization'))}
            <div class="row-2">{fld('b-type','Business type',sel('b-type',[('dealer','Tire dealer'),('service','Auto service'),('dist','Distributor'),('fleet','Fleet'),('media','Media'),('other','Other')]))}{fld('b-web','Website',inp('b-web','url','www.example.com',False,'url'),False)}</div>
            <div class="row-2">{fld('b-city','City',inp('b-city',ph='ex. Denver',auto='address-level2'))}{fld('b-state','State',sel('b-state',STATES))}</div>
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
          <p>By submitting this form, you agree that Marshal Tire will use your information as described in our <a class="link" href="#privacy">Privacy Policy</a>.</p>
          <div><button class="btn btn--primary btn--lg" type="submit"><span id="submit-label">SEND MESSAGE</span></button></div>
        </div>
      </form>
    </div>
    <aside class="side-card" aria-labelledby="talk">
      <h2 id="talk">Talk to us</h2>
      <div class="side-line"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/></svg><div><small>Phone</small><a href="tel:18005550142">1-800-555-0142</a></div></div>
      <div class="side-line"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h18v12H3zM3 7l9 6 9-6"/></svg><div><small>Email</small><a href="mailto:info@marshaltire.com">info@marshaltire.com</a></div></div>
      <div class="side-line"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6.5 7-11.5C19 5.4 15.9 3 12 3S5 5.4 5 9.5C5 14.5 12 21 12 21z"/><circle cx="12" cy="9.5" r="2"/></svg><div><small>Mail</small><b>Marshal Tire, 1482 Wazee Street, Denver, CO 80202</b></div></div>
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
        <div class="actions"><a class="btn btn--primary btn--lg" href="#warranty">VIEW WARRANTY DETAILS {ARROW}</a><a class="hero-link" href="#warranty">See coverage</a></div>
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

LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">\n'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>\n'
pages = {
  'index.html': ('home', 'Marshal Tire | Built to perform', 'Practical tires with the right balance of performance, durability and value.', home_alt, '', ''),
  'index-alt.html': ('home', 'Marshal Tire | Built to perform (split hero)', 'Practical tires with the right balance of performance, durability and value.', home, '', ''),
  'about.html': ('about', 'About Us | Marshal Tire', 'Built around your everyday drive.', about, '', ''),
  'tire-details.html': ('tire-details', 'Marshal All Terrain MF41 | Marshal Tire', 'Marshal All Terrain: technology, warranty and all 25 available sizes.', details, '', f'<script src="assets/js/mf41.js?v={ver("assets/js/mf41.js")}"></script>\n'),
  'dealers.html': ('dealers', 'Find a Dealer | Marshal Tire', 'Find authorized Marshal Tire dealers near you.', dealers, LEAFLET_CSS, LEAFLET_JS),
  'contact.html': ('contact', 'Contact Us | Marshal Tire', 'Contact Marshal Tire: general and business inquiries.', contact, '', ''),
}
for fn, (pg, t, d, b, eh, ej) in pages.items():
    (ROOT / fn).write_text(shell(pg, t, d, b, eh, ej))
    print('wrote', fn)
