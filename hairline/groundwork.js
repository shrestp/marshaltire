/**
 * Groundwork: a tire standing on its tread, three-quarters on, mid-build. The
 * carcass, the sidewall and the rim are finished; round the tread, thirty
 * blocks cut by the four straight grooves sit on the carcass, and a stretch of
 * them is still a dashed blueprint of where the tread will be. Where the
 * pointer passes, blocks grow out of the carcass to full depth, hold for the
 * afterglow, then settle back to the rest pose: built round most of the tire,
 * a front of three blocks part-way up, a gap over the top. The lead block of
 * that front is the rest's bright mark. The slider is the afterglow, in seconds.
 *
 * The pattern: paint and decay. A spring per block chases the larger of its
 * rest depth and a glow that holds, then fades. The tire's axis lies along y,
 * so its solids are built here from projected points, hulled and filleted.
 * The pointer picks the block whose rest centre on screen is nearest.
 */
const { Cam, clamp, fillet, fit, hull, poly, proj, rad, seg, spring, stepS, disposer, mk, place, pointer, register } = HL;

const N = 30, RO = 70, RC = 61, RR = 37, W = 46, WT = 21, ZC = RO, STEP = 360 / N, GAP = 1.1;
const LEAD = 3, FRONT = [0.62, 0.3, 0.1], BUILT = 20;
const V = [0.612, 0.612, 0.5]; // toward the camera, at Cam(45, 0.5)
const GROOVES = [-12.6, -4.2, 4.2, 12.6]; // the four wide straight grooves, across the tread

const restOf = (j) => { const k = (j - LEAD + BUILT + N) % N; return k < BUILT ? 1 : k < BUILT + FRONT.length ? FRONT[k - BUILT] : 0; };
const apart = (i, a) => { const d = Math.abs(i - a) % N; return Math.min(d, N - d); };
const faces = (deg) => V[0] * Math.cos(rad(deg)) + V[2] * Math.sin(rad(deg)); // the tread's outward normal, toward the camera

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let glowFor = value * 1000, over = null;
  const C = Cam(45, 0.5, 1.5);
  fit(C, [[-RO, -W / 2, 0], [RO, W / 2, 0], [-RO, W / 2, 2 * RO], [RO, -W / 2, 2 * RO], [0, W / 2, 0], [0, -W / 2, 2 * RO]], 200, 162);
  const P = proj(C);
  const at = (deg, y, r) => P(r * Math.cos(rad(deg)), y, ZC + r * Math.sin(rad(deg)));
  const circle = (y, r, n = 72) => Array.from({ length: n }, (_, k) => at((k * 360) / n, y, r));
  const round = (pts, r) => fillet(pts, pts.map(() => r), 3);
  const g = mk("g", {}, svg);

  /** Block j at depth share s: its silhouette, its outer face and its grooves. */
  function geom(j, s) {
    const gap = faces(j * STEP) > 0 ? GAP : 0.15; // the far side's edge reads as one band
    const a = j * STEP - STEP / 2 + gap, b = j * STEP + STEP / 2 - gap, m = (a + b) / 2, r1 = RC + s * (RO - RC);
    const pts = [];
    for (const d of [a, m, b]) for (const y of [-WT, WT]) for (const r of [RC, r1]) pts.push(at(d, y, r));
    const face = [at(a, -WT, r1), at(m, -WT, r1), at(b, -WT, r1), at(b, WT, r1), at(m, WT, r1), at(a, WT, r1)];
    return { sil: poly(round(hull(pts), gap > 1 ? 1.4 : 0.4)), face: poly(face), grooves: GROOVES.map((y) => seg(at(a, y, r1), at(b, y, r1))).join("") };
  }

  const blocks = [];
  for (let j = 0; j < N; j++) {
    const deg = j * STEP, c = [RO * Math.cos(rad(deg)), 0, ZC + RO * Math.sin(rad(deg))];
    blocks.push({ j, deg, front: faces(deg) > 0, depth: c[0] * V[0] + c[2] * V[2], rest: restOf(j), sp: spring(restOf(j), { eps: 0.002 }), glow: 0, seen: -1e9, drawn: NaN, pick: at(deg, 0, RO) });
  }
  const order = blocks.slice().sort((p, q) => p.depth - q.depth);
  const add = (b) => {
    const grp = mk("g", {}, g);
    if (b.front) mk("path", { d: geom(b.j, 1).face, class: "dash nf" }, grp); // the blueprint: where the tread will be
    b.sil = mk("path", { class: "sil" }, grp);
    b.face = mk("path", { class: "nf lo" }, grp);
    b.gr = mk("path", { class: "nf lo" }, grp);
  };

  // Back to front: the blocks turned away, the carcass over them, then the blocks facing us, then the sidewall and the rim.
  order.filter((b) => !b.front).forEach(add);
  mk("path", { d: poly(round(hull(circle(-W / 2 + 2, RC).concat(circle(W / 2 - 2, RC), circle(-W / 2 + 6, RC + 3), circle(W / 2 - 6, RC + 3))), 3)), class: "sil" }, g);
  order.filter((b) => b.front).forEach(add);
  const yF = W / 2 - 2;
  mk("path", { d: poly(circle(yF, RC + 2)), class: "" }, g);
  mk("path", { d: poly(circle(yF, RC - 9)), class: "nf lo" }, g);
  mk("path", { d: poly(circle(yF, RR)), class: "nf" }, g);
  mk("path", { d: poly(circle(yF, RR - 4)), class: "nf lo" }, g);
  let spokes = "";
  for (let k = 0; k < 6; k++) spokes += seg(at(k * 60 + 15, yF, 11), at(k * 60 + 15, yF, RR - 4));
  mk("path", { d: spokes, class: "nf lo" }, g);
  mk("path", { d: poly(circle(yF + 3, 10, 32)), class: "" }, g);
  for (let k = 0; k < 5; k++) place(mk("circle", { r: 0.9, class: "dot off" }, g), at(k * 72 + 90, yF + 3, 6.2));

  let hot = null;
  function draw(b) {
    const s = clamp(b.sp.x, 0, 1);
    if (s === b.drawn) return;
    b.drawn = s;
    if (s < 0.04) { b.sil.setAttribute("d", ""); b.face.setAttribute("d", ""); b.gr.setAttribute("d", ""); return; }
    const q = geom(b.j, s);
    b.sil.setAttribute("d", q.sil);
    b.face.setAttribute("d", b.front ? q.face : "");
    b.gr.setAttribute("d", b.front && s > 0.5 ? q.grooves : "");
  }
  function light(b) { if (b === hot) return; if (hot) hot.sil.classList.remove("hi"); hot = b; hot.sil.classList.add("hi"); }

  const reach = (d) => clamp(1 - d / 3.4, 0, 1) ** 1.3; // 1 under the pointer, gone by 3.4 blocks
  const B = register(stage, (dt, now) => {
    let moving = false;
    for (const b of blocks) {
      if (over !== null) { const f = reach(apart(b.j, over)); if (f > 0.02) { b.glow = Math.max(b.glow, f); b.seen = now; } }
      const since = now - b.seen, hold = since < glowFor ? 1 : clamp(1 - (since - glowFor) / 900, 0, 1);
      if (hold === 0) b.glow = 0; else moving = true;
      b.sp.t = Math.max(b.rest, b.glow * hold);
      if (stepS(b.sp, dt)) moving = true;
      draw(b);
    }
    return moving;
  });
  bag.add(B.unregister);

  const lead = blocks[LEAD], pickable = blocks.filter((b) => faces(b.deg) > -0.2);
  function aim(p) {
    let best = null, bd = 1e9;
    for (const b of pickable) { const d = Math.hypot(p[0] - b.pick[0], p[1] - b.pick[1]); if (d < bd) { bd = d; best = b; } }
    if (bd > 34) return leave();
    over = best.j; light(best);
    read.textContent = "block " + String(best.j + 1).padStart(2, "0");
    B.wake();
  }
  function leave() { over = null; light(lead); read.textContent = "rest"; B.wake(); }

  blocks.forEach(draw); light(lead);
  bag.add(pointer(stage, { move: aim, leave }));
  bag.add(() => svg.replaceChildren());
  return { set: (v) => { glowFor = v * 1000; B.wake(); }, destroy: bag.dispose };
}

hairline({
  name: "groundwork",
  means: "A tire mid-build: tread blocks grow out of a blueprint where the pointer passes, then settle back.",
  rules: [1, 3, 5, 6],
  range: [0.6, 2, 5],
  tour: [[300, 140], [250, 80], [170, 60], null],
  mount,
});
