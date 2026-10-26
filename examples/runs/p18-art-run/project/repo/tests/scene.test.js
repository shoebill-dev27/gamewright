'use strict';
// G-002: scene mapping (criteria 31, 33, 35, 36, 38, 40, 46).
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { G, V, A, run, world } = require('./helpers.js');
const SCN = require('../src/scene.js');

const tileAt = (sc, x, y) => sc.tiles.find((t) => t.x === x && t.y === y);
const rows = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};

test('scene: full mapping table for terrain, stairs, braziers, items and creatures', () => {
  const sc = SCN.build(V.view(world(['#########', '#@<>B+o..#', '#.msh.G..#'])));
  const expect = [[0, 0, 'wall', null], [1, 1, 'floor', null], [2, 1, 'floor', 'stairs-up'], [3, 1, 'floor', 'stairs-down'],
    [4, 1, 'floor', 'brazier'], [5, 1, 'floor', 'salve'], [6, 1, 'floor', 'oil'], [7, 1, 'floor', null]];
  for (const [x, y, base, object] of expect) {
    const t = tileAt(sc, x, y);
    assert.ok(t, 'tile ' + x + ',' + y);
    assert.equal(t.base, base, 'base ' + x + ',' + y);
    assert.equal(t.object, object, 'object ' + x + ',' + y);
    assert.equal(t.tone, 'full');
  }
  const lit = SCN.build(V.view(world(['#@B..#'], { lit: [[2, 0]] })));
  assert.equal(tileAt(lit, 2, 0).object, 'brazier-lit');
  const at = (x, y) => sc.actors.find((a) => a.x === x && a.y === y);
  assert.equal(at(2, 2).picture, 'moth'); assert.equal(at(3, 2).picture, 'shade');
  assert.equal(at(4, 2).picture, 'hound'); assert.equal(at(6, 2).picture, 'gloom');
  assert.equal(at(1, 1).picture, 'player');
  assert.ok(sc.actors.every((a) => a.wash === false));
  const names = sc.actors.map((a) => a.picture);
  assert.equal(new Set(names).size, names.length, 'all different');
});

test('scene: a crouching hound has its own picture; a standing one does not', () => {
  const s0 = world(['#@.h..#']);
  assert.equal(SCN.build(V.view(s0)).actors.find((a) => a.x === 3).picture, 'hound');
  const s1 = run(s0, A.wait);
  const v = V.view(s1);
  assert.equal(v.creatures[0].state, 'crouching');
  assert.equal(SCN.build(v).actors.find((a) => a.x === 3).picture, 'hound-crouch');
});

test('scene: wash only for stunned and staggered', () => {
  const st = run(world(['#@Bm..#']), A.E);
  const v = V.view(st);
  assert.equal(v.creatures[0].state, 'stunned');
  const sc = SCN.build(v);
  assert.equal(sc.actors.find((a) => a.picture === 'moth').wash, true);
  assert.equal(sc.actors.find((a) => a.picture === 'player').wash, false);
  const g = world(rows(3, 4), { floor: 5 });
  g.creatures[0].staggered = 3;
  const gv = V.view(g);
  assert.equal(gv.creatures[0].state, 'staggered');
  assert.equal(SCN.build(gv).actors.find((a) => a.picture === 'gloom').wash, true);
  // a hunting moth, a crouching hound and a gathering Gloom are not washed
  assert.equal(SCN.build(V.view(world(['#@.m.#']))).actors.some((a) => a.wash), false);
  assert.equal(SCN.build(V.view(run(world(['#@.h..#']), A.wait))).actors.some((a) => a.wash), false);
  assert.equal(SCN.build(V.view(run(world(rows(2, 4), { floor: 5 }), A.wait))).actors.some((a) => a.wash), false);
});

test('flame: five distinct, strictly increasing steps for r = 2..6, from real views', () => {
  const steps = [];
  for (const [E, r] of [[10, 2], [30, 3], [50, 4], [70, 5], [90, 6]]) {
    const v = V.view(world(['#@..#'], { ember: E }));
    assert.equal(v.radius, r);
    steps.push(SCN.build(v).flame);
  }
  for (let i = 1; i < steps.length; i++) assert.ok(steps[i] > steps[i - 1], steps.join());
  assert.equal(new Set(steps).size, 5);
  const one = G.newRun('flame-1');
  assert.equal(SCN.build(V.view(one)).flame, 5); // E = 100
});

test('memory: tone follows vis; unseen tiles get no request', () => {
  let st = G.newRun('mem-1');
  const acts = [A.E, A.S, A.E, A.S, A.E, A.E, A.S, A.W, A.N, A.E, A.E, A.E, A.S, A.S, A.E];
  for (let i = 0; i < 40 && !st.end; i++) st = G.step(st, acts[i % acts.length]).state;
  const v = V.view(st), sc = SCN.build(v);
  let seen = 0, dim = 0;
  v.cells.forEach((r) => r.forEach((c) => { if (c.seen) { seen++; if (!c.vis) dim++; } }));
  assert.equal(sc.tiles.length, seen);
  assert.equal(sc.tiles.filter((t) => t.tone === 'dim').length, dim);
  sc.tiles.forEach((t) => {
    const c = v.cells[t.y][t.x];
    assert.equal(t.tone, c.vis ? 'full' : 'dim');
    assert.ok(c.seen);
  });
  const keys = new Set(sc.tiles.map((t) => t.x + ',' + t.y));
  v.cells.forEach((r, y) => r.forEach((c, x) => { if (!c.seen) assert.ok(!keys.has(x + ',' + y)); }));
  assert.ok(dim > 0, 'the sample has remembered tiles');
  const ids = new Set(v.creatures.map((c) => c.x + ',' + c.y));
  sc.actors.slice(0, -1).forEach((a) => assert.ok(ids.has(a.x + ',' + a.y)));
  assert.equal(sc.actors.length, v.creatures.length + 1);
});

test('scene.js and pictures.js use no DOM, network or Image', () => {
  for (const f of ['scene.js', 'pictures.js']) {
    const src = fs.readFileSync(__dirname + '/../src/' + f, 'utf8');
    assert.ok(!/\b(window|document|Image|fetch|XMLHttpRequest|localStorage|navigator|require)\b/.test(src.replace(/\/\*[\s\S]*?\*\//, '')), f);
  }
});
