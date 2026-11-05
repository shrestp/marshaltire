/* Client feedback: click anywhere on a page to pin a note. Notes are listed per page in a drawer,
   and all of them on review.html. Storage is Supabase when configured, otherwise this browser only. */
(() => {
  const cfg = window.MT_FEEDBACK || {};
  const shared = !!(cfg.supabaseUrl && cfg.anonKey);
  const LKEY = 'mt-feedback-notes';

  /* ---------- storage ---------- */
  const local = {
    all: () => { try { return JSON.parse(localStorage.getItem(LKEY)) || []; } catch { return []; } },
    save(list) { try { localStorage.setItem(LKEY, JSON.stringify(list)); } catch {} }
  };
  const api = (path, opts = {}) => fetch(`${cfg.supabaseUrl.replace(/\/$/, '')}/rest/v1/${path}`, {
    ...opts,
    headers: { apikey: cfg.anonKey, ...(cfg.anonKey.startsWith('eyJ') ? { Authorization: `Bearer ${cfg.anonKey}` } : {}), 'Content-Type': 'application/json', Prefer: 'return=representation', ...(opts.headers || {}) }
  }).then(r => { if (!r.ok) throw new Error(`Feedback server error ${r.status}`); return r.status === 204 ? null : r.json(); });
  const store = {
    shared,
    list: page => shared
      ? api(`feedback?select=*&order=created_at.asc${page ? `&page=eq.${encodeURIComponent(page)}` : ''}`)
      : Promise.resolve(local.all().filter(n => !page || n.page === page)),
    add: note => {
      if (shared) return api('feedback', { method: 'POST', body: JSON.stringify(note) }).then(r => r[0]);
      const n = { ...note, id: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now())), created_at: new Date().toISOString(), status: 'open' };
      local.save([...local.all(), n]); return Promise.resolve(n);
    },
    update: (id, patch) => {
      if (shared) return api(`feedback?id=eq.${id}`, { method: 'PATCH', body: JSON.stringify(patch) });
      local.save(local.all().map(n => (n.id === id ? { ...n, ...patch } : n))); return Promise.resolve();
    },
    remove: id => {
      if (shared) return api(`feedback?id=eq.${id}`, { method: 'DELETE' });
      local.save(local.all().filter(n => n.id !== id)); return Promise.resolve();
    }
  };
  window.MTFeedbackStore = store;
  if (document.body.dataset.page === 'review') return; // review page only needs the store

  /* ---------- helpers ---------- */
  const page = location.pathname.split('/').pop() || 'index.html';
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const inWidget = el => el && el.closest && el.closest('.fb-root, .fb-pin, .fb-pop');
  const when = iso => { const d = new Date(iso); return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) + ', ' + d.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' }); };
  const nameKey = 'mt-feedback-name';
  const getName = () => { try { return localStorage.getItem(nameKey) || ''; } catch { return ''; } };
  const setName = v => { try { localStorage.setItem(nameKey, v); } catch {} };

  // A selector path to the clicked element, so a pin follows its element when the layout reflows.
  const pathTo = el => {
    const parts = [];
    while (el && el !== document.body && el.nodeType === 1) {
      if (el.id && !/^fb-/.test(el.id)) { parts.unshift('#' + CSS.escape(el.id)); break; }
      let i = 1, s = el; while ((s = s.previousElementSibling)) if (s.tagName === el.tagName) i++;
      parts.unshift(`${el.tagName.toLowerCase()}:nth-of-type(${i})`);
      el = el.parentElement;
    }
    return parts.length && parts[0][0] === '#' ? parts.join(' > ') : 'body > ' + parts.join(' > ');
  };
  const docW = () => document.documentElement.scrollWidth;
  const where = n => {
    let el = null; try { el = n.anchor && document.querySelector(n.anchor); } catch {}
    const r = el && el.getBoundingClientRect();
    if (r && r.width && r.height && el.getClientRects().length) return { x: r.left + scrollX + n.ax * r.width, y: r.top + scrollY + n.ay * r.height };
    return { x: n.x * docW(), y: n.y };
  };

  /* ---------- UI ---------- */
  const root = h('div', 'fb-root');
  root.innerHTML = `
    <button type="button" class="fb-fab" aria-expanded="false" aria-controls="fb-drawer">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>
      <span>Feedback</span><b class="fb-count" hidden></b>
    </button>
    <aside class="fb-drawer" id="fb-drawer" hidden aria-label="Feedback">
      <header><div><h2>Feedback</h2><p class="fb-sub"></p></div><button type="button" class="fb-x" aria-label="Close feedback">×</button></header>
      <button type="button" class="fb-add" aria-pressed="false"></button>
      <p class="fb-add-help"></p>
      <p class="fb-mode" hidden></p>
      <div class="fb-scope" role="tablist" aria-label="Which notes to show"><button type="button" role="tab" data-scope="page">This page <span></span></button><button type="button" role="tab" data-scope="all">All pages <span></span></button></div>
      <ol class="fb-list"></ol>
      <p class="fb-empty"></p>
      <footer><a href="review.html">See all feedback</a></footer>
    </aside>
    <div class="fb-banner" hidden role="status"><span class="fb-dot" aria-hidden="true"></span>Commenting: click anywhere to leave a note <button type="button">Done</button></div>
    <div class="fb-hint" hidden role="dialog" aria-label="Leave feedback"><b>Have feedback?</b><p>Click here, then click anywhere on the page to leave a note.</p><button type="button">Got it</button></div>
    <div class="fb-hover" hidden></div>`;
  document.body.appendChild(root);
  const $ = s => root.querySelector(s), $$ = s => [...root.querySelectorAll(s)];
  const fab = $('.fb-fab'), drawer = $('.fb-drawer'), list = $('.fb-list'), banner = $('.fb-banner'), hover = $('.fb-hover');
  $('.fb-sub').textContent = 'You’re on: ' + document.title.split('|')[0].trim();
  if (!shared) { const m = $('.fb-mode'); m.hidden = false; m.textContent = 'Demo mode: notes are saved in this browser only.'; }

  const PAGES = { 'index.html': 'Home', 'index-alt.html': 'Home (split hero)', 'about.html': 'About Us', 'tire-details.html': 'All Terrain', 'tire-highway-terrain.html': 'Highway Terrain', 'tire-tour-as.html': 'Tour A/S', 'tire-sport-as.html': 'Sport A/S', 'dealers.html': 'Find a Dealer', 'contact.html': 'Contact Us' };
  const SKEY = 'mt-feedback-scope';
  let notes = [], open = false, picking = false, pop = null, active = null;
  let scope = (() => { try { return localStorage.getItem(SKEY) || 'all'; } catch { return 'all'; } })();
  const pinLayer = h('div', 'fb-pins'); document.body.appendChild(pinLayer);
  const numOf = n => notes.filter(x => x.page === n.page).indexOf(n) + 1;
  const isOpenNote = n => n.status !== 'resolved';

  const item = n => {
    const num = numOf(n), here = n.page === page;
    const li = h('li', 'fb-item' + (isOpenNote(n) ? '' : ' is-resolved') + (active === n.id ? ' is-active' : ''));
    li.dataset.id = n.id;
    const top = h('div', 'fb-item-top');
    top.append(h('span', 'fb-num', num), h('b', null, n.author || 'Guest'), h('time', null, when(n.created_at)));
    if (!isOpenNote(n)) top.append(h('span', 'fb-tag', 'Resolved'));
    const acts = h('div', 'fb-item-acts');
    if (!here) { const go = h('a', 'fb-go', 'Go to note'); go.href = `${n.page}#fb-${n.id}`; go.addEventListener('click', e => e.stopPropagation()); acts.append(go); }
    const del = h('button', 'fb-del', 'Delete'); del.type = 'button'; del.setAttribute('aria-label', `Delete note ${num}`);
    // Inline confirm: browsers can block confirm() pop-ups, which would silently cancel every delete.
    const ask = h('span', 'fb-ask'); ask.hidden = true;
    const yes = h('button', 'fb-yes', 'Yes, delete'), no = h('button', 'fb-no', 'Cancel'); yes.type = no.type = 'button';
    ask.append(h('span', null, 'Delete this note?'), yes, no);
    del.addEventListener('click', e => { e.stopPropagation(); del.hidden = true; ask.hidden = false; yes.focus(); });
    no.addEventListener('click', e => { e.stopPropagation(); ask.hidden = true; del.hidden = false; });
    yes.addEventListener('click', e => {
      e.stopPropagation(); yes.disabled = true; yes.textContent = 'Deleting…';
      store.remove(n.id).then(() => { notes = notes.filter(x => x.id !== n.id); if (active === n.id) active = null; render(); })
        .catch(() => { yes.disabled = false; yes.textContent = 'Try again'; });
    });
    // Resolve toggle: circle-check, filled once the note is resolved. Click again to reopen.
    const done = !isOpenNote(n), res = h('button', 'fb-res' + (done ? ' is-on' : '')); res.type = 'button';
    res.title = done ? 'Reopen note' : 'Mark resolved';
    res.setAttribute('aria-label', `${done ? 'Reopen' : 'Resolve'} note ${num}`); res.setAttribute('aria-pressed', done);
    res.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>';
    res.addEventListener('click', e => {
      e.stopPropagation(); res.disabled = true; const st = done ? 'open' : 'resolved';
      store.update(n.id, { status: st }).then(() => { n.status = st; render(); }).catch(() => { res.disabled = false; });
    });
    acts.append(del, ask, res);
    li.append(top, h('p', null, n.body), acts);
    li.addEventListener('click', () => { if (here) focusNote(n.id, true); else location.href = `${n.page}#fb-${n.id}`; });
    return li;
  };

  const render = () => {
    const here = notes.filter(n => n.page === page);
    const c = $('.fb-count'), live = here.filter(isOpenNote).length; c.hidden = !live; c.textContent = live;
    $$('.fb-scope button').forEach(b => { b.setAttribute('aria-selected', b.dataset.scope === scope); b.querySelector('span').textContent = (b.dataset.scope === 'page' ? here : notes).filter(isOpenNote).length || ''; });
    list.innerHTML = ''; pinLayer.innerHTML = '';
    const shown = scope === 'page' ? here : notes;
    const empty = $('.fb-empty'); empty.hidden = shown.length > 0;
    empty.textContent = scope === 'page' && notes.length ? 'No notes on this page yet. Click anywhere on the page to add one.' : 'No notes yet. Click anywhere on the page to add one.';
    if (scope === 'page') here.forEach(n => list.append(item(n)));
    else {
      const order = [page, ...Object.keys(PAGES), ...notes.map(n => n.page)].filter((p, i, a) => a.indexOf(p) === i);
      order.forEach(pg => {
        const grp = notes.filter(n => n.page === pg); if (!grp.length) return;
        const head = h('li', 'fb-group'); head.textContent = (PAGES[pg] || pg) + (pg === page ? ' (this page)' : '');
        list.append(head); grp.forEach(n => list.append(item(n)));
      });
    }
    if (!open) return;
    here.forEach(n => {
      const num = numOf(n), p = where(n), pin = h('button', 'fb-pin' + (isOpenNote(n) ? '' : ' is-resolved') + (active === n.id ? ' is-active' : ''), num);
      pin.type = 'button'; pin.title = `${n.author || 'Guest'}: ${n.body}`; pin.setAttribute('aria-label', `Note ${num} by ${n.author || 'Guest'}`);
      pin.style.left = p.x + 'px'; pin.style.top = p.y + 'px';
      pin.addEventListener('click', e => { e.stopPropagation(); focusNote(n.id, false); });
      pinLayer.append(pin);
    });
  };
  $$('.fb-scope button').forEach(b => b.addEventListener('click', () => { scope = b.dataset.scope; try { localStorage.setItem(SKEY, scope); } catch {} render(); }));
  const focusNote = (id, scrollPage) => {
    active = id; render();
    const n = notes.find(x => x.id === id); if (!n || n.page !== page) return;
    if (scrollPage) { const p = where(n); scrollTo({ top: Math.max(0, p.y - innerHeight / 3), behavior: 'smooth' }); }
    const li = list.querySelector(`[data-id="${CSS.escape(id)}"]`); li && li.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  };
  const fromHash = () => { if (location.hash.startsWith('#fb-')) { setOpen(true); setTimeout(() => focusNote(location.hash.slice(4), true), 300); } };
  addEventListener('hashchange', fromHash);
  const load = () => store.list().then(r => { notes = r || []; render(); fromHash(); })
    .catch(() => { $('.fb-empty').hidden = false; $('.fb-empty').textContent = 'Couldn’t load feedback. Check the connection and refresh.'; });

  const setOpen = v => { open = v; drawer.hidden = !v; fab.setAttribute('aria-expanded', v); document.documentElement.classList.toggle('fb-open', v); if (v) startPick(); else { closePop(); stopPick(); } render(); };
  fab.addEventListener('click', () => { hideHint(); setOpen(!open); });
  $('.fb-x').addEventListener('click', () => setOpen(false));

  /* pick a spot */
  // Comment mode: while it is on, every click on the page starts a note. It stays on until turned off.
  const addBtn = $('.fb-add'), addHelp = $('.fb-add-help');
  const syncMode = () => {
    addBtn.setAttribute('aria-pressed', picking);
    addBtn.textContent = picking ? 'Commenting is on' : '+ Add notes';
    addHelp.textContent = picking ? 'Click anywhere on the page to add a note. Turn this off to click links and buttons normally.' : 'Turn on to click anywhere on the page and leave notes.';
  };
  const startPick = () => { picking = true; banner.hidden = false; document.documentElement.classList.add('fb-picking'); syncMode(); };
  const stopPick = () => { picking = false; banner.hidden = true; hover.hidden = true; document.documentElement.classList.remove('fb-picking'); syncMode(); };
  addBtn.addEventListener('click', () => (picking ? (closePop(), stopPick()) : startPick()));
  banner.querySelector('button').addEventListener('click', () => { closePop(); stopPick(); });
  syncMode();

  /* first-visit hint */
  const HKEY = 'mt-feedback-hint-seen', hint = $('.fb-hint');
  const hideHint = () => { hint.hidden = true; try { localStorage.setItem(HKEY, '1'); } catch {} };
  hint.querySelector('button').addEventListener('click', hideHint);
  let seen = false; try { seen = !!localStorage.getItem(HKEY); } catch {}
  if (!seen && !location.hash.startsWith('#fb-')) setTimeout(() => { if (!open) hint.hidden = false; }, 1200);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (pop) closePop(); else if (picking) stopPick(); } });
  document.addEventListener('mousemove', e => {
    if (!picking || pop || inWidget(e.target)) { hover.hidden = true; return; }
    const r = e.target.getBoundingClientRect();
    Object.assign(hover.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' }); hover.hidden = false;
  });
  const swallow = e => { if (picking && !inWidget(e.target)) { e.preventDefault(); e.stopPropagation(); } };
  ['mousedown', 'pointerdown', 'touchstart', 'submit'].forEach(t => document.addEventListener(t, swallow, { capture: true, passive: false }));
  document.addEventListener('click', e => {
    if (!picking || inWidget(e.target)) return;
    e.preventDefault(); e.stopPropagation();
    // a half-written note stays put; an empty one moves to the new spot
    if (pop && pop.body.value.trim()) { pop.body.focus(); pop.classList.remove('fb-nudge'); void pop.offsetWidth; pop.classList.add('fb-nudge'); return; }
    const t = e.target, r = t.getBoundingClientRect();
    const draft = {
      page, anchor: pathTo(t),
      ax: r.width ? (e.clientX - r.left) / r.width : 0, ay: r.height ? (e.clientY - r.top) / r.height : 0,
      x: e.pageX / docW(), y: e.pageY, vw: innerWidth
    };
    hover.hidden = true; openPop(draft, e.pageX, e.pageY);
  }, true);

  /* note form */
  const closePop = () => { if (pop) { pop.remove(); pop = null; } };
  const openPop = (draft, x, y) => {
    closePop();
    pop = h('form', 'fb-pop');
    pop.innerHTML = `<span class="fb-pin fb-pin--new" aria-hidden="true">+</span>
      <label><span>Your name <span class="fb-opt">(optional)</span></span><input name="author" autocomplete="name" placeholder="e.g. Sam from Marshal"></label>
      <label>Note<textarea name="body" rows="4" placeholder="What should change here?" required></textarea></label>
      <p class="fb-err" hidden></p>
      <div class="fb-actions"><button type="button" class="fb-cancel">Cancel</button><button type="submit" class="fb-save">Save note</button></div>`;
    document.body.appendChild(pop);
    const w = 300, left = Math.min(Math.max(8, x - 12), docW() - w - 8);
    pop.style.left = left + 'px'; pop.style.top = y + 'px';
    pop.querySelector('.fb-pin--new').style.left = (x - left) + 'px';
    pop.author.value = getName();
    pop.body.focus({ preventScroll: true });
    pop.querySelector('.fb-cancel').addEventListener('click', closePop);
    pop.addEventListener('submit', e => {
      e.preventDefault();
      const author = pop.author.value.trim(), body = pop.body.value.trim(); if (!body) return;
      if (author) setName(author);
      const btn = pop.querySelector('.fb-save'); btn.disabled = true; btn.textContent = 'Saving…';
      store.add({ ...draft, author: author || null, body: body.slice(0, 2000) })
        .then(n => { notes.push(n); closePop(); focusNote(n.id, false); })
        .catch(() => { const er = pop.querySelector('.fb-err'); er.hidden = false; er.textContent = 'Couldn’t save. Please try again.'; btn.disabled = false; btn.textContent = 'Save note'; });
    });
  };

  let raf; const reflow = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => open && render()); };
  addEventListener('resize', reflow); new ResizeObserver(reflow).observe(document.body);
  load();
})();
