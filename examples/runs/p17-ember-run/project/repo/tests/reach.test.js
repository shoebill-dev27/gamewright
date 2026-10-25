'use strict';
// D-002 / checks 14 and 29: threat marks and reach marks, strict form.
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, world } = require('./helpers.js');
const TV = require('../src/textview.js');

const reachOf = (v, dir) => { const e = v.reach.find((r) => r.dir === dir); return e ? e.creatures.map((c) => c.letter) : []; };

test('reach: a step next to a moth shows a reach mark before the step', () => {
  const v = V.view(world(['#@.m.#']));
  assert.deepEqual(reachOf(v, 'E'), ['m']);
  assert.equal(v.threats.length, 0);
  const text = TV.renderFrame(v);
  assert.match(text, /Danger: E \(m\)/);
  const s = G.step(world(['#@.m.#']), A.E);
  assert.equal(s.state.hp, 11);
});

test('reach: a step next to a hound shows a reach mark; the hound is not a threat while the player stays', () => {
  const v = V.view(world(['#@.h.#']));
  assert.deepEqual(reachOf(v, 'E'), ['h']);
  assert.equal(v.threats.length, 0);
  assert.equal(G.step(world(['#@.h.#']), A.E).state.hp, 9);
});

test('reach: a step next to a shade at r=2 shows a reach mark', () => {
  const s = world(['#@.s.#'], { ember: 19 });
  assert.deepEqual(reachOf(V.view(s), 'E'), ['s']);
  assert.equal(G.step(s, A.E).state.hp, 10);
});

test('threat: a Wait at E=20 beside a shade is already a strike; at E=21 it is not', () => {
  const a = world(['#@s..#'], { ember: 20 });
  assert.equal(V.view(a).threats.length, 1);
  assert.equal(G.step(a, A.wait).state.hp, 10);
  const b = world(['#@s..#'], { ember: 21 });
  assert.equal(V.view(b).threats.length, 0);
  assert.equal(G.step(b, A.wait).state.hp, 12);
});

test('reach: no mark on an unlit brazier or the down stairs; a lit brazier is marked', () => {
  assert.deepEqual(reachOf(V.view(world(['#@Bm.#'])), 'E'), []);
  assert.deepEqual(reachOf(V.view(world(['#@>m.#'])), 'E'), []);
  assert.deepEqual(reachOf(V.view(world(['#@Bm.#'], { lit: [[2, 0]] })), 'E'), ['m']);
});

test('reach: no mark on walls or on a tile holding a creature', () => {
  const v = V.view(world(['#@m.#']));
  assert.deepEqual(reachOf(v, 'E'), []);
  assert.deepEqual(reachOf(v, 'W'), []);
  assert.deepEqual(reachOf(v, 'N'), []);
});

test('text frame: reach tiles are drawn with ? and differ from the threat glyph', () => {
  const text = TV.renderFrame(V.view(world(['#@.m.#'])));
  assert.ok(text.split('\n').some((l) => l.startsWith('#@?m')), text);
});

function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ACTS = [A.N, A.E, A.S, A.W, A.wait];

test('check 14 (strict): every damage event was shown and marked on the tile where the player ended the turn', (t) => {
  const counts = { threat: 0, reach: 0 };
  for (let i = 0; i < 20; i++) {
    let st = G.newRun('c14-' + i);
    const rnd = lcg(i + 7);
    for (let n = 0; n < 600 && !st.end; n++) {
      const before = V.view(st);
      const res = G.step(st, ACTS[rnd() % 5]);
      const moved = res.state.floor === st.floor && (res.state.player.x !== st.player.x || res.state.player.y !== st.player.y);
      for (const e of res.events.filter((x) => x.t === 'damage')) {
        const where = 'seed c14-' + i + ' command ' + n + ' creature #' + e.src + ' ' + e.type;
        if (moved) {
          const p = res.state.player;
          const rc = before.reach.find((r) => r.x === p.x && r.y === p.y);
          assert.ok(rc && rc.creatures.some((c) => c.id === e.src), 'no reach mark: ' + where);
          counts.reach++; t.diagnostic('reach  ' + where);
        } else {
          assert.ok(before.threats.some((c) => c.id === e.src), 'no threat mark: ' + where);
          counts.threat++; t.diagnostic('threat ' + where);
        }
      }
      st = res.state;
    }
  }
  t.diagnostic('damage events: threat ' + counts.threat + ', reach ' + counts.reach);
});

test('sampled states: threat flags equal what the planner does with the ember after dimming', () => {
  for (let i = 0; i < 6; i++) {
    let st = G.newRun('mark-' + i);
    const rnd = lcg(i + 31);
    for (let n = 0; n < 200 && !st.end; n++) {
      const v = V.view(st);
      const after = Math.max(0, st.ember - G.drainRate(st));
      const s2 = Object.assign({}, st, { ember: after });
      for (const cv of v.creatures) {
        const c = st.creatures.find((o) => o.id === cv.id);
        const it = G.planAction(s2, c, G.makeCtx(s2));
        const expect = after > 0 && (it.kind === 'attack' || it.kind === 'lunge' || it.kind === 'slam');
        assert.equal(cv.threat, expect, 'seed mark-' + i + ' command ' + n + ' creature #' + cv.id);
      }
      st = G.step(st, ACTS[rnd() % 5]).state;
    }
  }
});
