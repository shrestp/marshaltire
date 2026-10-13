/* Marshal Tire — clickable mockup. Plain JS, no build step (runs on GitHub Pages or from disk). */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const icon = {
    chevDown: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
    chevRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
    arrowRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>',
    arrowLeft: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4M10 6l-6 6 6 6"/></svg>',
    arrowDown: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M12 6v12M6 12h12"/></svg>',
    minus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M6 12h12"/></svg>',
    pause: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M9 6v12M15 6v12"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.5"/></svg>',
    alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5v.5"/></svg>',
    youtube: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1" y="4" width="22" height="16" rx="5" fill="#1e1e1e"/><path d="M10 8.5v7l6-3.5z" fill="#fff"/></svg>',
  };
  const LOGO = document.getElementById('logo-tpl')?.innerHTML || '';

  /* ---------- header + footer ---------- */
  const page = document.body.dataset.page;
  const menus = [
    { id: 'tires', label: 'Tires', links: [['Marshal All Terrain - MF41', 'tire-details.html'], ['Marshal Highway Terrain - ML41', 'tire-details.html'], ['Marshal Sport A/S - MU41', 'tire-details.html'], ['Marshal Tour A/S - MH41', 'tire-details.html']], all: ['View All Tires', 'index.html#range'] },
    { id: 'marshal', label: 'Marshal', links: [['About Us', 'about.html'], ['General Contact Us', 'contact.html'], ['Business Contact Us', 'contact.html?type=business']] },
    { id: 'support', label: 'Support', links: [['Warranty', '#warranty'], ['Privacy Policy', '#privacy']] },
  ];
  const current = { 'tire-details': 'tires', about: 'marshal', contact: 'marshal' }[page];
  const header = $('#site-header');
  if (header) {
    header.className = 'site-header';
    header.innerHTML = `<div class="container bar">
      <a class="brand" href="index.html" aria-label="Marshal Tire home">${LOGO}</a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">${icon.menu}</button>
      <nav class="nav" id="primary-nav" aria-label="Primary">
        <ul class="nav-list">${menus.map(m => `<li class="nav-item">
          <button class="nav-trigger${current === m.id ? ' is-current' : ''}" aria-expanded="false" aria-controls="menu-${m.id}">${m.label}${icon.chevDown}</button>
          <div class="mega" id="menu-${m.id}">${m.links.map(([t, h]) => `<a href="${h}">${t}</a>`).join('')}${m.all ? `<a class="mega-all" href="${m.all[1]}">${m.all[0]}</a>` : ''}</div>
        </li>`).join('')}</ul>
        <a class="btn btn--primary btn--sm" href="dealers.html">FIND DEALER</a>
      </nav></div>`;
    const triggers = $$('.nav-trigger', header);
    const closeAll = except => triggers.forEach(t => { if (t !== except) { t.setAttribute('aria-expanded', 'false'); $('#' + t.getAttribute('aria-controls')).classList.remove('is-open'); } });
    triggers.forEach(t => {
      const panel = $('#' + t.getAttribute('aria-controls'));
      t.addEventListener('click', e => { e.stopPropagation(); const open = t.getAttribute('aria-expanded') !== 'true'; closeAll(t); t.setAttribute('aria-expanded', open); panel.classList.toggle('is-open', open); });
      const li = t.parentElement;
      li.addEventListener('mouseenter', () => { if (matchMedia('(min-width: 901px) and (hover: hover)').matches) { closeAll(t); t.setAttribute('aria-expanded', 'true'); panel.classList.add('is-open'); } });
      li.addEventListener('mouseleave', () => { if (matchMedia('(min-width: 901px) and (hover: hover)').matches) { t.setAttribute('aria-expanded', 'false'); panel.classList.remove('is-open'); } });
    });
    document.addEventListener('click', () => { if (matchMedia('(min-width: 901px)').matches) closeAll(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeAll(); setNav(false); } });
    const toggle = $('.menu-toggle', header), nav = $('#primary-nav');
    const setNav = open => { toggle.setAttribute('aria-expanded', open); toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu'); toggle.innerHTML = open ? icon.close : icon.menu; nav.classList.toggle('is-open', open); document.body.classList.toggle('nav-open', open); };
    toggle.addEventListener('click', () => setNav(toggle.getAttribute('aria-expanded') !== 'true'));
  }
  const footer = $('#site-footer');
  if (footer) {
    footer.className = 'site-footer';
    footer.innerHTML = `<div class="container">
      <div class="footer-top">
        <div class="footer-brand">${LOGO}<a class="footer-phone" href="tel:18005550142">1-800-555-0142</a><p><a href="mailto:info@marshaltire.com">info@marshaltire.com</a></p><p style="margin-top:12px">1482 Wazee Street<br>Denver, CO 80202</p></div>
        <div class="footer-col"><h3>Tires</h3><ul><li><a href="tire-details.html">Marshal All Terrain MF41</a></li><li><a href="tire-details.html">Marshal Highway Terrain ML41</a></li><li><a href="tire-details.html">Marshal Tour A/S MH41</a></li><li><a href="tire-details.html">Marshal Sport A/S MU41</a></li><li><a href="index.html#finder">Tire Search</a></li></ul></div>
        <div class="footer-col"><h3>Marshal</h3><ul><li><a href="about.html">About Us</a></li><li><a href="contact.html">General Contact Us</a></li><li><a href="contact.html?type=business">Business Contact Us</a></li></ul></div>
        <div class="footer-col"><h3>Support</h3><ul><li><a href="#warranty">Warranty</a></li><li><a href="#privacy">Privacy Policy</a></li></ul></div>
      </div>
      <div class="footer-bottom"><span>© 2026 Marshal Tire. All rights reserved.</span><a href="#youtube" aria-label="Marshal Tire on YouTube">${icon.youtube}</a></div></div>`;
  }
  // pages not in this mockup
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (a && ['#warranty', '#privacy', '#youtube', '#terms'].includes(a.getAttribute('href'))) { e.preventDefault(); toast('That page isn’t part of this mockup yet.'); }
  });
  function toast(msg) {
    let t = $('#toast'); if (!t) { t = document.createElement('div'); t.id = 'toast'; t.setAttribute('role', 'status'); t.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#111;color:#fff;padding:12px 18px;border-radius:8px;font-size:14px;z-index:99;box-shadow:0 8px 24px rgba(0,0,0,.2);transition:opacity .2s'; document.body.appendChild(t); }
    t.textContent = msg; t.style.opacity = 1; clearTimeout(t._h); t._h = setTimeout(() => (t.style.opacity = 0), 2600);
  }
  window.mtToast = toast;

  /* ---------- HOME: hero slider ---------- */
  const hero = $('.hero[data-slider]');
  if (hero) {
    const slides = $$('.slide', hero), dots = $('.dots', hero), prev = $('[data-prev]', hero), next = $('[data-next]', hero), pause = $('[data-pause]', hero);
    let i = 0, paused = matchMedia('(prefers-reduced-motion: reduce)').matches;
    dots.innerHTML = slides.map((_, n) => `<button type="button" aria-label="Go to slide ${n + 1}"><span class="fill"></span></button>`).join('');
    const bars = $$('.fill', dots);
    const go = n => {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => { s.classList.toggle('is-active', k === i); s.setAttribute('aria-hidden', k !== i); s.inert = k !== i; });
      $$('button', dots).forEach((d, k) => d.setAttribute('aria-current', k === i));
      // restart the progress bar on the active dot; when it fills, advance
      bars.forEach(b => b.classList.remove('run'));
      void bars[i].offsetWidth;
      bars[i].classList.add('run');
    };
    bars.forEach((b, k) => b.addEventListener('animationend', () => { if (k === i) go(i + 1); }));
    const setPaused = p => { paused = p; hero.classList.toggle('is-paused', p); if (pause) { pause.innerHTML = p ? icon.play : icon.pause; pause.setAttribute('aria-label', p ? 'Play slideshow' : 'Pause slideshow'); } };
    $$('button', dots).forEach((d, k) => d.addEventListener('click', () => { if (k !== i) go(k); }));
    prev.addEventListener('click', () => go(i - 1));
    next.addEventListener('click', () => go(i + 1));
    if (pause) pause.addEventListener('click', () => setPaused(!paused));
    // hold progress while the pointer is over the hero
    hero.addEventListener('mouseenter', () => hero.classList.add('is-hovering'));
    hero.addEventListener('mouseleave', () => hero.classList.remove('is-hovering'));
    // hold progress while a keyboard user is inside the hero
    hero.addEventListener('focusin', e => { if (e.target.matches(':focus-visible')) hero.classList.add('is-holding'); });
    hero.addEventListener('focusout', e => { if (!hero.contains(e.relatedTarget)) hero.classList.remove('is-holding'); });
    let x0 = null; hero.addEventListener('touchstart', e => (x0 = e.touches[0].clientX), { passive: true });
    hero.addEventListener('touchend', e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1)); x0 = null; });
    go(0); setPaused(paused);
  }

  /* ---------- HOME: tire finder ---------- */
  const finder = $('#finder');
  if (finder) {
    const tabs = $$('.seg button', finder);
    tabs.forEach(t => t.addEventListener('click', () => {
      tabs.forEach(x => x.setAttribute('aria-selected', x === t));
      $$('.finder-fields', finder).forEach(f => (f.hidden = f.id !== t.getAttribute('aria-controls')));
    }));
    const models = { Chevrolet: ['Silverado 1500', 'Tahoe', 'Colorado'], Ford: ['F-150', 'Explorer', 'Ranger'], Toyota: ['Tacoma', '4Runner', 'RAV4'], Jeep: ['Wrangler', 'Grand Cherokee'], Ram: ['1500', '2500'] };
    const year = $('#f-year'), make = $('#f-make'), model = $('#f-model'), trim = $('#f-trim');
    for (let y = 2026; y >= 2010; y--) year.add(new Option(y, y));
    Object.keys(models).forEach(m => make.add(new Option(m, m)));
    make.addEventListener('change', () => { model.length = 1; trim.length = 1; (models[make.value] || []).forEach(m => model.add(new Option(m, m))); model.disabled = !make.value; trim.disabled = true; markPh(); });
    model.addEventListener('change', () => { trim.length = 1; ['Base', 'Mid', 'Off-road'].forEach(t => trim.add(new Option(t, t))); trim.disabled = !model.value; markPh(); });
    const markPh = () => $$('select', finder).forEach(s => s.classList.toggle('is-placeholder', !s.value));
    $$('select', finder).forEach(s => s.addEventListener('change', markPh)); markPh();
    finder.addEventListener('submit', e => {
      e.preventDefault();
      const bySize = !$('#by-size').hidden;
      if (bySize) { const w = $('#s-width').value, a = $('#s-aspect').value, r = $('#s-rim').value; const q = [w && a ? `${w}/${a}` : w, r ? 'R' + r : ''].filter(Boolean).join(' '); location.href = 'tire-details.html' + (q ? '?size=' + encodeURIComponent(q) : '') + '#available-sizes'; }
      else { if (!make.value) { make.focus(); toast('Choose a make to find tires.'); return; } location.href = 'tire-details.html#available-sizes'; }
    });
  }

  /* ---------- TIRE DETAILS ---------- */
  const acc = $('#size-accordion');
  if (acc) {
    // All Terrain MF41 — from MS_Spec.xlsx
    const D = window.MF41 || [];
    const cols = [['Product code', r => r.code], ['Tire size', r => r.size, 'size'], ['Service desc.', r => r.svc], ['Load index', r => r.svc.slice(0, -1)], ['Speed rating', r => r.svc.slice(-1)], ['Construction', r => r.cons], ['Sidewall', () => 'BSW'], ['UTQG', r => r.utqg], ['Rim width range (in.)', r => r.rim], ['Section width on measured rim (in.)', r => r.secw], ['Overall diameter (in.)', r => r.od.toFixed(1)], ['Tire weight (lb)', r => r.wt.toFixed(1)], ['Static loaded radius (in.)', r => r.slr], ['Revs per mile', r => fmt(r.rpm)], ['Tread depth (1/32")', r => r.tread.toFixed(1)], ['Max load single (lb)', r => fmt(r.ls)], ['Max load dual (lb)', r => (r.ld ? fmt(r.ld) : '—')], ['Max inflation (psi)', r => r.psi], ['Mileage warranty', r => fmt(r.war)], ['3PMSF', () => 'Yes'], ['Country of origin', r => r.orig], ['UPC', r => r.upc]];
    const fmt = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    const rimOf = s => +s.match(/R(\d+)/)[1];
    const groups = {}; D.forEach(r => (groups[rimOf(r.size)] ||= []).push(r));
    const label = r => `${r.size} ${r.svc} ${r.cons}`;
    acc.innerHTML = Object.keys(groups).sort((a, b) => a - b).map((rim, gi) => `
      <section class="acc-group" data-rim="${rim}">
        <h3 style="margin:0"><button class="acc-head" aria-expanded="${gi === 0}" aria-controls="g-${rim}"><span><b>${rim} Inch</b> <span class="count">(${groups[rim].length} sizes)</span></span><span class="acc-icon">${gi === 0 ? icon.minus : icon.plus}</span></button></h3>
        <div class="acc-body" id="g-${rim}" ${gi === 0 ? '' : 'hidden'}>
          ${groups[rim].map((r, k) => `<div class="size-row" data-size="${r.size}">
            <button class="size-btn" aria-expanded="${gi === 0 && k === 0}" aria-controls="s-${r.code}"><span class="lbl">${label(r)}</span>${icon.chevDown}</button>
            <div class="spec-scroll" id="s-${r.code}" ${gi === 0 && k === 0 ? '' : 'hidden'} tabindex="0" role="region" aria-label="Specifications for ${r.size}">
              <table class="spec"><thead><tr>${cols.map(c => `<th scope="col">${c[0]}</th>`).join('')}</tr></thead>
              <tbody><tr>${cols.map(c => { const v = c[1](r); return `<td class="${c[2] || ''}${v === '—' ? ' none' : ''}">${v}</td>`; }).join('')}</tr></tbody></table>
            </div></div>`).join('')}
        </div></section>`).join('') + `<p class="no-results" hidden>No All Terrain sizes match “<span></span>”. Try just the width (e.g. 265) or the rim (e.g. R17).</p>`;
    const setGroup = (btn, open) => { btn.setAttribute('aria-expanded', open); $('#' + btn.getAttribute('aria-controls')).hidden = !open; $('.acc-icon', btn).innerHTML = open ? icon.minus : icon.plus; };
    const setSize = (btn, open) => { btn.setAttribute('aria-expanded', open); $('#' + btn.getAttribute('aria-controls')).hidden = !open; };
    $$('.acc-head', acc).forEach(b => b.addEventListener('click', () => setGroup(b, b.getAttribute('aria-expanded') !== 'true')));
    $$('.size-btn', acc).forEach(b => b.addEventListener('click', () => setSize(b, b.getAttribute('aria-expanded') !== 'true')));
    // filter
    const input = $('#size-filter');
    const norm = s => s.toUpperCase().replace(/^LT/, '').replace(/[^0-9XR.]/g, '');
    const apply = () => {
      const q = input.value.trim(); const nq = norm(q);
      let any = 0;
      $$('.acc-group', acc).forEach(g => {
        let n = 0;
        $$('.size-row', g).forEach(row => {
          const size = row.dataset.size, hit = !nq || norm(size).includes(nq);
          row.hidden = !hit; if (hit) n++;
          const r = D.find(d => d.size === size), lbl = $('.lbl', row); lbl.textContent = label(r);
          if (q && hit) { const raw = q.toUpperCase().replace(/\s+/g, ''); const idx = size.toUpperCase().indexOf(raw); if (idx >= 0 && raw.length > 1) lbl.innerHTML = `${size.slice(0, idx)}<mark>${size.slice(idx, idx + raw.length)}</mark>${size.slice(idx + raw.length)} ${r.svc} ${r.cons}`; }
        });
        g.hidden = n === 0; any += n;
        $('.count', g).textContent = q ? `(${n} of ${$$('.size-row', g).length} sizes)` : `(${$$('.size-row', g).length} sizes)`;
        if (q && n) setGroup($('.acc-head', g), true);
      });
      const nr = $('.no-results', acc); nr.hidden = any > 0; $('span', nr).textContent = q;
    };
    input.addEventListener('input', apply);
    const pre = new URLSearchParams(location.search).get('size'); if (pre) { input.value = pre; apply(); }
    // "where can I find my size" toggle
    const how = $('#howto-toggle'); how?.addEventListener('click', () => { const open = how.getAttribute('aria-expanded') !== 'true'; how.setAttribute('aria-expanded', open); $('#howto').hidden = !open; });
    // anchor link focuses the filter after scrolling
    $$('a[href="#available-sizes"]').forEach(a => a.addEventListener('click', () => setTimeout(() => input.focus({ preventScroll: true }), 500)));
    // thumbnails
    const main = $('#main-image');
    $$('.thumb').forEach(t => t.addEventListener('click', () => { $$('.thumb').forEach(x => x.setAttribute('aria-pressed', x === t)); main.src = t.dataset.src; main.alt = t.dataset.alt; }));
    $$('.thumb-nav').forEach(b => b.addEventListener('click', () => { const th = $$('.thumb'); const cur = th.findIndex(x => x.getAttribute('aria-pressed') === 'true'); th[(cur + (+b.dataset.dir) + th.length) % th.length].click(); }));
    // CSV download of the real data
    $('#download-data')?.addEventListener('click', () => {
      const rows = [cols.map(c => c[0]), ...D.map(r => cols.map(c => String(c[1](r)).replace('—', '')))];
      const csv = rows.map(r => r.map(v => /[",]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v).join(',')).join('\n');
      const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' })); a.download = 'marshal-all-terrain-mf41-specs.csv'; a.click(); URL.revokeObjectURL(a.href);
    });
  }

  /* ---------- DEALERS ---------- */
  const mapEl = $('#map');
  if (mapEl) {
    const hasMap = !!window.L;
    const dealers = [
      { name: 'Rocky Mountain Tire', addr: '1482 Wazee Street', city: 'Denver, CO 80202', lat: 39.7527, lng: -104.9997 },
      { name: 'Front Range Auto', addr: '88 Pearl Street', city: 'Boulder, CO 80302', lat: 40.0176, lng: -105.2797 },
      { name: 'Mile High Tire & Wheel', addr: '2150 S Broadway', city: 'Denver, CO 80210', lat: 39.6787, lng: -104.9873 },
      { name: 'Foothills Tire Pros', addr: '14200 W Colfax Ave', city: 'Lakewood, CO 80401', lat: 39.7400, lng: -105.1590 },
      { name: 'Aurora Auto & Tire', addr: '15300 E Iliff Ave', city: 'Aurora, CO 80014', lat: 39.6750, lng: -104.8100 },
      { name: 'Summit Tire & Service', addr: '410 Main Avenue', city: 'Durango, CO 81301', lat: 37.2753, lng: -107.8801 },
      { name: 'Cascade Tire Co.', addr: '2201 Camino del Rio', city: 'Durango, CO 81301', lat: 37.2600, lng: -107.8770 },
      { name: 'Peak Tire Center', addr: '1820 N Academy Blvd', city: 'Colorado Springs, CO 80909', lat: 38.8640, lng: -104.7600 },
    ];
    const places = { '80202': [39.7527, -104.9997], denver: [39.7392, -104.9903], '80302': [40.0150, -105.2705], boulder: [40.0150, -105.2705], '81301': [37.2753, -107.8801], durango: [37.2753, -107.8801], 'colorado springs': [38.8339, -104.8214], '80909': [38.8640, -104.7600], aurora: [39.7294, -104.8319], lakewood: [39.7047, -105.0814] };
    let map = null, pin = () => null, you = null, origin = null;
    if (hasMap) {
      map = L.map(mapEl, { scrollWheelZoom: false }).setView([39.74, -104.99], 9);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
      pin = active => L.divIcon({ className: '', html: `<div class="pin${active ? ' is-active' : ''}"></div>`, iconSize: [28, 28], iconAnchor: [14, 28] });
    } else {
      mapEl.innerHTML = '<p style="display:grid;place-items:center;height:100%;margin:0;padding:24px;text-align:center;color:var(--text-muted)">The map couldn’t load. The dealer list still works.</p>';
    }
    dealers.forEach((d, k) => { d.id = k; if (map) d.marker = L.marker([d.lat, d.lng], { icon: pin(false), title: d.name, keyboard: false }).addTo(map).on('click', () => select(k, true)); });
    const list = $('#dealer-list'), status = $('#dealer-status');
    const miles = (a, b) => { const R = 3958.8, r = x => x * Math.PI / 180, dLat = r(b[0] - a[0]), dLng = r(b[1] - a[1]); const h = Math.sin(dLat / 2) ** 2 + Math.cos(r(a[0])) * Math.cos(r(b[0])) * Math.sin(dLng / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(h)); };
    const render = () => {
      const arr = dealers.map(d => ({ ...d, dist: origin ? miles(origin, [d.lat, d.lng]) : null })).sort((a, b) => (a.dist ?? 0) - (b.dist ?? 0));
      list.innerHTML = arr.map(d => `<li class="dealer" data-id="${d.id}" tabindex="0" aria-label="${d.name}, ${d.addr}, ${d.city}">
        <h3>${d.name}${d.dist != null ? `<span>${d.dist < 10 ? d.dist.toFixed(1) : Math.round(d.dist)} mi</span>` : ''}</h3>
        <p>${d.addr}<br>${d.city}</p>
        <div class="dir"><a href="https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(d.addr + ', ' + d.city)}" target="_blank" rel="noopener">Get directions ${icon.arrowRight}</a></div></li>`).join('');
      $$('.dealer', list).forEach(li => { li.addEventListener('click', e => { if (!e.target.closest('a')) select(+li.dataset.id, false); }); li.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(+li.dataset.id, false); } }); });
    };
    const select = (id, fromMap) => {
      $$('.dealer', list).forEach(li => li.classList.toggle('is-active', +li.dataset.id === id));
      const d = dealers[id];
      if (map) { dealers.forEach(x => x.marker.setIcon(pin(x.id === id))); map.flyTo([d.lat, d.lng], Math.max(map.getZoom(), 12), { duration: .6 }); }
      if (fromMap) $(`.dealer[data-id="${id}"]`, list)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    };
    const setOrigin = (ll, labelText) => {
      origin = ll; if (map) { if (you) you.remove(); you = L.marker(ll, { icon: L.divIcon({ className: '', html: '<div class="you"></div>', iconSize: [16, 16] }) }).addTo(map); }
      render(); const near = dealers.filter(d => miles(ll, [d.lat, d.lng]) <= 15).length;
      status.textContent = near ? `${near} dealer${near > 1 ? 's' : ''} within 15 miles of ${labelText}. Showing nearest first.` : `No dealers within 15 miles of ${labelText}. Showing the nearest ones instead.`;
      const nearest = $('.dealer', list); if (nearest) select(+nearest.dataset.id, false);
      if (map) map.fitBounds(L.latLngBounds([ll, ...dealers.slice().sort((a, b) => miles(ll, [a.lat, a.lng]) - miles(ll, [b.lat, b.lng])).slice(0, 3).map(d => [d.lat, d.lng])]).pad(.3));
    };
    $('#dealer-form').addEventListener('submit', async e => {
      e.preventDefault(); const q = $('#dealer-q').value.trim(); if (!q) { $('#dealer-q').focus(); status.textContent = 'Enter a ZIP code, city or address.'; return; }
      const key = q.toLowerCase().replace(/,?\s*(co|colorado)$/, '').trim();
      if (places[key]) return setOrigin(places[key], q);
      status.textContent = 'Searching…';
      try { const r = await fetch('https://nominatim.openstreetmap.org/search?format=json&countrycodes=us&limit=1&q=' + encodeURIComponent(q)); const j = await r.json(); if (j[0]) setOrigin([+j[0].lat, +j[0].lon], q); else status.textContent = `We couldn’t find “${q}”. Try a ZIP code like 80202.`; }
      catch { status.textContent = `We couldn’t look up “${q}” right now. Try a ZIP code like 80202.`; }
    });
    $('#use-location').addEventListener('click', () => {
      if (!navigator.geolocation) return (status.textContent = 'Your browser can’t share location. Enter a ZIP code instead.');
      status.textContent = 'Finding your location…';
      navigator.geolocation.getCurrentPosition(p => setOrigin([p.coords.latitude, p.coords.longitude], 'your location'), () => (status.textContent = 'Location is turned off. Enter a ZIP code instead.'), { timeout: 8000 });
    });
    render(); select(0, false);
    const pre = new URLSearchParams(location.search).get('q'); if (pre) { $('#dealer-q').value = pre; $('#dealer-form').requestSubmit(); }
  }

  /* ---------- CONTACT ---------- */
  const cform = $('#contact-form');
  if (cform) {
    const tabs = $$('.aud-tabs button'), panes = $$('[data-pane]', cform);
    const setTab = (type, push) => {
      tabs.forEach(t => t.setAttribute('aria-selected', t.dataset.type === type));
      panes.forEach(p => { const on = p.dataset.pane === type; p.hidden = !on; $$('input,select,textarea', p).forEach(el => (el.disabled = !on)); });
      $('#submit-label').textContent = type === 'business' ? 'SEND INQUIRY' : 'SEND MESSAGE';
      if (push) history.replaceState(null, '', type === 'business' ? '?type=business' : location.pathname);
      clearErrors();
    };
    tabs.forEach(t => t.addEventListener('click', () => setTab(t.dataset.type, true)));
    tabs.forEach((t, k) => t.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const n = tabs[(k + 1) % 2]; n.focus(); n.click(); } }));
    // conditional: tire details only for general requests about tires
    const req = $('#g-request'), tirePanel = $('#tire-details');
    const syncTire = () => { const show = ['support', 'warranty'].includes(req.value); tirePanel.hidden = !show; $$('input,select', tirePanel).forEach(el => (el.disabled = !show)); $('#warranty-extra').hidden = req.value !== 'warranty'; $$('#warranty-extra input').forEach(el => (el.disabled = req.value !== 'warranty')); };
    req.addEventListener('change', syncTire);
    const msg = $$('textarea', cform);
    msg.forEach(t => { const c = t.closest('.field').querySelector('.counter'); const up = () => (c.textContent = `${t.value.length} / 1,000`); t.addEventListener('input', up); up(); });
    $$('select', cform).forEach(s => { const up = () => s.classList.toggle('is-placeholder', !s.value); s.addEventListener('change', up); up(); });
    // validation
    const rules = { email: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || 'Enter an email like name@example.com.', tel: v => !v || v.replace(/\D/g, '').length >= 10 || 'Enter a 10-digit phone number.' };
    const fieldError = el => {
      if (el.disabled) return '';
      const v = el.value.trim(); const lab = el.closest('.field').querySelector('label').textContent.replace('*', '').trim();
      if (el.required && !v) return el.tagName === 'SELECT' ? `Choose a ${lab.toLowerCase()}.` : `Enter your ${lab.toLowerCase()}.`;
      const r = rules[el.type]; if (r && v) { const res = r(v); if (res !== true) return res; }
      return '';
    };
    const show = (el, err) => { const f = el.closest('.field'); f.classList.toggle('has-error', !!err); $('.error-msg span', f).textContent = err; el.setAttribute('aria-invalid', !!err); };
    const clearErrors = () => { $$('.field.has-error', cform).forEach(f => f.classList.remove('has-error')); $('.form-alert', cform).classList.remove('is-on'); };
    $$('input,select,textarea', cform).forEach(el => {
      if (el.closest('.field') && !el.closest('.field').querySelector('.error-msg')) { const d = document.createElement('p'); d.className = 'error-msg'; d.id = el.id + '-err'; d.innerHTML = icon.alert + '<span></span>'; el.closest('.field').appendChild(d); el.setAttribute('aria-describedby', [el.getAttribute('aria-describedby'), d.id].filter(Boolean).join(' ')); }
      el.addEventListener('blur', () => { if (el.closest('.field')) show(el, fieldError(el)); });
      el.addEventListener('input', () => { if (el.closest('.field')?.classList.contains('has-error')) show(el, fieldError(el)); });
    });
    cform.addEventListener('submit', e => {
      e.preventDefault();
      const bad = $$('input,select,textarea', cform).filter(el => el.closest('.field') && !el.disabled).map(el => { const err = fieldError(el); show(el, err); return err ? el : null; }).filter(Boolean);
      const alert = $('.form-alert', cform);
      if (bad.length) { alert.textContent = `Please fix ${bad.length} field${bad.length > 1 ? 's' : ''} to send your message.`; alert.classList.add('is-on'); bad[0].focus(); return; }
      const name = $('#g-first:not(:disabled), #b-first:not(:disabled)').value.trim();
      $('#contact-card').innerHTML = `<div class="success" role="status"><div class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg></div><h2>Thanks, ${name.replace(/[<>&]/g, '')}. We’ve got your message.</h2><p class="muted">Our team will reply within 48 hours. This is a mockup, so nothing was actually sent.</p><a class="btn btn--outline" href="index.html">Back to home</a></div>`;
      $('#contact-card').scrollIntoView({ block: 'start' });
    });
    setTab(new URLSearchParams(location.search).get('type') === 'business' ? 'business' : 'general', false);
    syncTire();
  }
})();
