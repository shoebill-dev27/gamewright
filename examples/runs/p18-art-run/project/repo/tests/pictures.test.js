'use strict';
// G-002: drawing (criteria 31, 33, 35, 36, 41, 47) with a recording fake ctx at TILE 22.
const test = require('node:test');
const assert = require('node:assert/strict');
const P = require('../src/pictures.js');
const { fakeCtx } = require('./pic-helpers.js');

const TILE = 22, PX = 50, PY = 50;

function render(name, tone, opts) {
  const rec = fakeCtx();
  P.draw(rec.ctx, name, PX, PY, TILE, tone, opts);
  return rec;
}
function hsl(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255, g = parseInt(hex.slice(3, 5), 16) / 255, b = parseInt(hex.slice(5, 7), 16) / 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  if (!d) return { h: 0, s: 0, l };
  const s = d / (1 - Math.abs(2 * l - 1));
  let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  h = (h * 60 + 360) % 360;
  return { h, s, l };
}

test('pictures: there is one picture per entity and pose (13 entities, hound in 2 poses)', () => {
  const want = ['player', 'moth', 'shade', 'hound', 'hound-crouch', 'gloom', 'brazier', 'brazier-lit', 'salve', 'oil',
    'wall', 'floor', 'stairs-up', 'stairs-down'];
  assert.deepEqual(P.NAMES.slice().sort(), want.slice().sort());
});

test('pictures: every picture draws in both tones, inside its tile, without throwing', () => {
  for (const name of P.NAMES) for (const tone of ['full', 'dim']) {
    const rec = render(name, tone);
    assert.ok(rec.fills.length > 0, name);
    const b = rec.bbox();
    assert.ok(b.x0 >= PX - 1e-6 && b.y0 >= PY - 1e-6 && b.x1 <= PX + TILE + 1e-6 && b.y1 <= PY + TILE + 1e-6, name + ' ' + JSON.stringify(b));
    if (name !== 'wall' && name !== 'floor') {
      // entity pictures leave the 3 px mark border free
      assert.ok(b.x0 >= PX + 3 && b.y0 >= PY + 3 && b.x1 <= PX + TILE - 3 && b.y1 <= PY + TILE - 3, name + ' margin ' + JSON.stringify(b));
    }
  }
  for (let step = 1; step <= 5; step++) assert.doesNotThrow(() => P.drawFlame(fakeCtx().ctx, PX, PY, TILE, step, 'full'));
});

test('pictures: the palette is small; no red or orange main fill', () => {
  const full = new Set(), dimmed = new Set();
  for (const name of P.NAMES) {
    for (const [tone, set] of [['full', full], ['dim', dimmed]]) {
      const rec = render(name, tone);
      rec.fills.forEach((f) => set.add(f.color));
      const main = rec.fills.slice().sort((a, b) => b.area - a.area)[0].color;
      const c = hsl(main);
      assert.ok(!(c.s > 0.35 && (c.h < 40 || c.h >= 340)), name + ' ' + tone + ' main ' + main);
    }
  }
  assert.ok(full.size <= 12, 'full colors: ' + full.size);
  assert.ok(dimmed.size <= 12, 'dim colors: ' + dimmed.size);
  for (const k of Object.keys(P.PALETTE)) { const c = hsl(P.PALETTE[k]); assert.ok(!(c.s > 0.35 && (c.h < 40 || c.h >= 340)), k); }
});

test('pictures: dim differs from full for every picture', () => {
  for (const name of P.NAMES) {
    const a = render(name, 'full').fills.map((f) => f.color).join(), b = render(name, 'dim').fills.map((f) => f.color).join();
    assert.notEqual(a, b, name);
  }
  assert.notEqual(P.dim('#f0c640'), '#f0c640');
});

test('pictures: shapes differ (silhouettes are not copies of each other)', () => {
  const sigs = P.NAMES.map((n) => render(n, 'full').ops.join(';'));
  assert.equal(new Set(sigs).size, sigs.length);
  const h = (n) => { const b = render(n, 'full').bbox(); return b.y1 - b.y0; };
  assert.ok(h('hound-crouch') < h('hound'), 'crouching hound is lower');
  assert.ok(h('shade') > h('hound') && h('shade') > h('moth') - 1e-9 || h('shade') >= h('moth'), 'shade is tall');
});

test('flame: height grows with every step', () => {
  const hs = [1, 2, 3, 4, 5].map((s) => { const rec = fakeCtx(); P.drawFlame(rec.ctx, PX, PY, TILE, s, 'full'); const b = rec.bbox(); return b.y1 - b.y0; });
  for (let i = 1; i < hs.length; i++) assert.ok(hs[i] > hs[i - 1], hs.join());
  const p1 = render('player', 'full', { flame: 1 }).ops.join(), p5 = render('player', 'full', { flame: 5 }).ops.join();
  assert.notEqual(p1, p5);
});
