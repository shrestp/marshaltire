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
    <aside class="fb-drawer" id="fb-drawer" hidden aria-label="Feedback on this page">
      <header><div><h2>Feedback on this page</h2><p class="fb-sub"></p></div><button type="button" class="fb-x" aria-label="Close feedback">×</button></header>
      <button type="button" class="fb-add">+ Add a note</button>
      <p class="fb-mode" hidden></p>
      <ol class="fb-list"></ol>
      <p class="fb-empty">No notes yet. Click “Add a note”, then click the spot on the page you want to talk about.</p>
      <footer><a href="review.html">See all feedback</a></footer>
    </aside>
    <div class="fb-banner" hidden role="status">Click the spot you want to comment on. <button type="button">Cancel</button></div>
    <div class="fb-hover" hidden></div>`;
  document.body.appendChild(root);
  const $ = s => root.querySelector(s);
  const fab = $('.fb-fab'), drawer = $('.fb-drawer'), list = $('.fb-list'), banner = $('.fb-banner'), hover = $('.fb-hover');
  $('.fb-sub').textContent = document.title.split('|')[0].trim();
  if (!shared) { const m = $('.fb-mode'); m.hidden = false; m.textContent = 'Demo mode: notes are saved in this browser only.'; }

  let notes = [], open = false, picking = false, pop = null, active = null;
  const pinLayer = h('div', 'fb-pins'); document.body.appendChild(pinLayer);

  const render = () => {
    const live = notes.filter(n => n.status !== 'resolved');
    const c = $('.fb-count'); c.hidden = !live.length; c.textContent = live.length;
    list.innerHTML = ''; pinLayer.innerHTML = '';
    $('.fb-empty').hidden = notes.length > 0;
    notes.forEach((n, i) => {
      const num = i + 1;
      const li = h('li', 'fb-item' + (n.status === 'resolved' ? ' is-resolved' : '') + (active === n.id ? ' is-active' : ''));
      li.dataset.id = n.id;
      const top = h('div', 'fb-item-top');
      top.append(h('span', 'fb-num', num), h('b', null, n.author || 'Guest'), h('time', null, when(n.created_at)));
      if (n.status === 'resolved') top.append(h('span', 'fb-tag', 'Resolved'));
      const del = h('button', 'fb-del', 'Delete'); del.type = 'button'; del.setAttribute('aria-label', `Delete note ${num}`);
      del.addEventListener('click', e => {
        e.stopPropagation();
        if (!confirm('Delete this note? This can’t be undone.')) return;
        del.disabled = true;
        store.remove(n.id).then(() => { notes = notes.filter(x => x.id !== n.id); if (active === n.id) active = null; render(); })
          .catch(() => { del.disabled = false; alert('Couldn’t delete the note. Please try again.'); });
      });
      li.append(top, h('p', null, n.body), del);
      li.addEventListener('click', () => focusNote(n.id, true));
      list.append(li);
      if (!open) return;
      const p = where(n), pin = h('button', 'fb-pin' + (n.status === 'resolved' ? ' is-resolved' : '') + (active === n.id ? ' is-active' : ''), num);
      pin.type = 'button'; pin.title = `${n.author || 'Guest'}: ${n.body}`; pin.setAttribute('aria-label', `Note ${num} by ${n.author || 'Guest'}`);
      pin.style.left = p.x + 'px'; pin.style.top = p.y + 'px';
      pin.addEventListener('click', e => { e.stopPropagation(); focusNote(n.id, false); });
      pinLayer.append(pin);
    });
  };
  const focusNote = (id, scrollPage) => {
    active = id; render();
    const n = notes.find(x => x.id === id); if (!n) return;
    if (scrollPage) { const p = where(n); scrollTo({ top: Math.max(0, p.y - innerHeight / 3), behavior: 'smooth' }); }
    const li = list.querySelector(`[data-id="${CSS.escape(id)}"]`); li && li.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  };
  const load = () => store.list(page).then(r => { notes = r || []; render(); if (location.hash.startsWith('#fb-')) { setOpen(true); setTimeout(() => focusNote(location.hash.slice(4), true), 300); } })
    .catch(() => { $('.fb-empty').hidden = false; $('.fb-empty').textContent = 'Couldn’t load feedback. Check the connection and refresh.'; });

  const setOpen = v => { open = v; drawer.hidden = !v; fab.setAttribute('aria-expanded', v); document.documentElement.classList.toggle('fb-open', v); if (!v) stopPick(); render(); };
  fab.addEventListener('click', () => setOpen(!open));
  $('.fb-x').addEventListener('click', () => setOpen(false));

  /* pick a spot */
  const startPick = () => { closePop(); picking = true; banner.hidden = false; document.documentElement.classList.add('fb-picking'); };
  const stopPick = () => { picking = false; banner.hidden = true; hover.hidden = true; document.documentElement.classList.remove('fb-picking'); };
  $('.fb-add').addEventListener('click', startPick);
  banner.querySelector('button').addEventListener('click', stopPick);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (pop) closePop(); else if (picking) stopPick(); } });
  document.addEventListener('mousemove', e => {
    if (!picking || inWidget(e.target)) { hover.hidden = true; return; }
    const r = e.target.getBoundingClientRect();
    Object.assign(hover.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' }); hover.hidden = false;
  });
  const swallow = e => { if (picking && !inWidget(e.target)) { e.preventDefault(); e.stopPropagation(); } };
  ['mousedown', 'pointerdown', 'touchstart', 'submit'].forEach(t => document.addEventListener(t, swallow, { capture: true, passive: false }));
  document.addEventListener('click', e => {
    if (!picking || inWidget(e.target)) return;
    e.preventDefault(); e.stopPropagation();
    const t = e.target, r = t.getBoundingClientRect();
    const draft = {
      page, anchor: pathTo(t),
      ax: r.width ? (e.clientX - r.left) / r.width : 0, ay: r.height ? (e.clientY - r.top) / r.height : 0,
      x: e.pageX / docW(), y: e.pageY, vw: innerWidth
    };
    stopPick(); openPop(draft, e.pageX, e.pageY);
  }, true);

  /* note form */
  const closePop = () => { if (pop) { pop.remove(); pop = null; } };
  const openPop = (draft, x, y) => {
    closePop();
    pop = h('form', 'fb-pop');
    pop.innerHTML = `<span class="fb-pin fb-pin--new" aria-hidden="true">+</span>
      <label>Your name <span class="fb-opt">(optional)</span><input name="author" autocomplete="name" placeholder="e.g. Sam from Marshal"></label>
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
