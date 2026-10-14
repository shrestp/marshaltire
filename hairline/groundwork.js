/**
 * Groundwork: a tire lying on its side, half treaded. The carcass, sidewall and
 * rim are finished; the tread blocks round its edge are dashed footprints until
 * they are built. Where the pointer passes, blocks grow up out of their
 * footprints, staggered by distance, hold for the afterglow, then sink back to
 * the rest pose: two-thirds built, with a construction front of three blocks
 * part-way up. The lead block of that front is the rest's bright mark. The
 * slider is the afterglow, in seconds.
 *
 * The pattern: paint and decay. A spring per block chases a target that is
 * the larger of its rest height and a glow that holds, then fades. The pointer
 * is put on a fixed plane at mid-height and read as an angle round the tire.
 */
const {
  Cam, circ, clamp, facing, fit, hull, open, poly, prism, proj, ringAt, rings, run, seg,
  spring, stepS, unproj, disposer, mk, pointer, put, register, solid,
} = HL;

const N = 24, RC = 60, RO = 71, RB = 36, TH = 30, Z0 = 2, Z1 = TH - 2, BW = 12.4;
const STEP = (2 * Math.PI) / N, LEAD = 2, FRONT = [0.62, 0.3, 0.1], BUILT = 12;

/** A ring of samples turned by th about the tire's axis: positions and normals. */
const turn = (ring, th) => {
  const c = Math.cos(th), s = Math.sin(th);
  return ring.map((q) => ({ u: c * q.u - s * q.v, v: s * q.u + c * q.v, nu: c * q.nu - s * q.nv, nv: s * q.nu + c * q.nv }));
};
/** Rest height share of block i: built behind the lead, a front of three, then footprints. */
const restOf = (i) => {
  const k = (i - LEAD + BUILT + N) % N;
  return k < BUILT ? 1 : k < BUILT + FRONT.length ? FRONT[k - BUILT] : 0;
};
/** Blocks apart round the ring, the short way. */
const apart = (i, a) => { const d = Math.abs(i - a) % N; return Math.min(d, N - d); };

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let glowFor = value * 1000, over = null;
  const C = Cam(45, 0.5, 1.66);
  fit(C, [[-RO, -RO, 0], [RO, RO, 0], [RO, -RO, 0], [-RO, RO, 0], [0, 0, TH]], 200, 170);
  const P = proj(C), front = facing(C);
  const g = mk("g", {}, svg);

  // The tread blocks, each a rounded block standing on the carcass wall.
  const blocks = [];
  for (let i = 0; i < N; i++) {
    const th = i * STEP, [r0, r1] = rings(RC - 1.5, -BW / 2, RO, BW / 2, 2.4, 1);
    const ring = turn(r0, th), inner = turn(r1, th), mid = [(RC + RO) / 2 * Math.cos(th), (RC + RO) / 2 * Math.sin(th)];
    blocks.push({ i, th, ring, inner, mid, near: Math.cos(th) + Math.sin(th) > 0, rest: restOf(i), sp: spring(restOf(i), { eps: 0.002 }), glow: 0, seen: -1e9, drawn: NaN });
  }
  const byDepth = (a, b) => a.mid[0] + a.mid[1] - (b.mid[0] + b.mid[1]);
  const far = blocks.filter((b) => !b.near).sort(byDepth), near = blocks.filter((b) => b.near).sort(byDepth);
  const addBlock = (b) => {
    b.grp = mk("g", {}, g);
    mk("path", { d: poly(ringAt(P, b.ring, Z0)), class: "dash nf" }, b.grp);
    b.el = solid(b.grp);
  };
  far.forEach(addBlock);

  // The carcass: one wall, its top face, a sidewall rib, then the hole with the rim set down in it.
  const wall = circ(RC, 64), wallIn = circ(RC - 1.4, 64);
  put(solid(g), prism(P, front, wall, wallIn, 0, TH));
  const hole = circ(RB, 48);
  mk("path", { d: poly(ringAt(P, hole, TH)), class: "nf" }, g);
  mk("path", { d: open(ringAt(P, run(hole, (q) => !front(q)), TH - 9)), class: "nf lo" }, g);
  const lip = circ(RB - 3, 48), ZR = TH - 7;
  mk("path", { d: poly(ringAt(P, lip, ZR)), class: "nf" }, g);
  let spokes = "";
  for (let k = 0; k < 6; k++) {
    const a = k * (Math.PI / 3) + 0.3;
    spokes += seg(P(11 * Math.cos(a), 11 * Math.sin(a), ZR - 1), P((RB - 4) * Math.cos(a), (RB - 4) * Math.sin(a), ZR));
  }
  mk("path", { d: spokes, class: "nf lo" }, g);
  put(solid(g), prism(P, front, circ(10, 32), circ(8.6, 32), ZR - 6, ZR - 1));
  // The near strip of the top face, laid over the rim so the hole's near lip hides what is below it.
  const nH = ringAt(P, run(hole, front), TH), nO = ringAt(P, run(circ(RC - 2.6, 64), front), TH);
  const L = (pts) => (pts[0][0] <= pts[pts.length - 1][0] ? pts : pts.slice().reverse());
  const h2 = L(nH), o2 = L(nO);
  mk("path", { d: poly([...h2, ...o2.slice().reverse()]), class: "fo" }, g);
  mk("path", { d: open(h2), class: "nf" }, g);
  mk("path", { d: poly(ringAt(P, circ(48, 64), TH)), class: "nf lo" }, g);
  near.forEach(addBlock);

  const lead = blocks[LEAD];
  let hot = null;
  function draw(b) {
    const s = clamp(b.sp.x, 0, 1), h = s * (Z1 - Z0);
    if (h === b.drawn) return;
    b.drawn = h;
    put(b.el, h < 0.5 ? { sil: "", crease: "" } : prism(P, front, b.ring, b.inner, Z0, Z0 + h));
  }
  function light(b) {
    if (b === hot) return;
    if (hot) hot.el.sil.classList.remove("hi");
    hot = b; hot.el.sil.classList.add("hi");
  }

  /** Glow at a blocks' distance from the pointer: 1 under it, gone by 3.4 blocks. */
  const reach = (d) => clamp(1 - d / 3.4, 0, 1) ** 1.3;
  const B = register(stage, (dt, now) => {
    let moving = false;
    for (const b of blocks) {
      if (over) { const f = reach(apart(b.i, over.a)); if (f > 0.02) { b.glow = Math.max(b.glow, f); b.seen = now; } }
      const since = now - b.seen;
      const hold = since < glowFor ? 1 : clamp(1 - (since - glowFor) / 900, 0, 1);
      if (hold === 0) b.glow = 0; else moving = true;
      b.sp.t = Math.max(b.rest, b.glow * hold);
      if (stepS(b.sp, dt)) moving = true;
      draw(b);
    }
    return moving;
  });
  bag.add(B.unregister);

  function aim(p) {
    const [x, y] = unproj(C, p[0], p[1], TH / 2), r = Math.hypot(x, y);
    if (r < RB - 6 || r > RO + 30) return leave();
    const a = ((Math.round(Math.atan2(y, x) / STEP) % N) + N) % N;
    over = { a };
    light(blocks[a]);
    read.textContent = "block " + String(a + 1).padStart(2, "0");
    B.wake();
  }
  function leave() { over = null; light(lead); read.textContent = "rest"; B.wake(); }

  light(lead);
  blocks.forEach(draw);
  bag.add(pointer(stage, { move: aim, leave }));
  bag.add(() => svg.replaceChildren());

  return {
    set: (v) => { glowFor = v * 1000; B.wake(); },
    destroy: bag.dispose,
  };
}

hairline({
  name: "groundwork",
  means: "A tire mid-build: tread blocks rise from blueprint footprints where the pointer passes, then settle back.",
  rules: [1, 3, 5, 6],
  range: [0.6, 2, 5],
  tour: [[254, 195], [145, 195], [90, 148], [145, 101], null],
  mount,
});
