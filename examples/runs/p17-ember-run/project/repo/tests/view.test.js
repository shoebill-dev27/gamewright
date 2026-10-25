'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, L, FG, world } = require('./helpers.js');
const TV = require('../src/textview.js');

test('visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2', () => {
  for (const seed of ['vis-1', 'vis-2']) for (const n of [1, 3]) {
    const f = FG.generateFloor(seed, n);
    for (let y = 1; y < f.h - 1; y++) for (let x = 1; x < f.w - 1; x++) {
      if (f.tiles[y].charAt(x) === '#') continue;
      const vis = L.visibleGrid(f, x, y, 2);
      for (const [dx, dy] of [[0, -1], [1, 0], [0, 1], [-1, 0]]) {
        assert.equal(vis[(y + dy) * f.w + x + dx], 1, 'adjacent ' + x + ',' + y);
        const tx = x + 2 * dx, ty = y + 2 * dy;
        if (tx >= 0 && ty >= 0 && tx < f.w && ty < f.h && f.tiles[y + dy].charAt(x + dx) !== '#') {
          assert.equal(vis[ty * f.w + tx], 1, 'distance 2 ' + x + ',' + y);
        }
      }
    }
  }
});

test('visibility: walls block line of sight; the glow is circular', () => {
  const s = world(['#@.#.#']);
  const vis = L.visibleGrid(s.floorData, 1, 0, 6);
  assert.equal(vis[2], 1); assert.equal(vis[3], 1); assert.equal(vis[4], 0);
  const f = world(['#'.repeat(20), '#@' + '.'.repeat(17) + '#', '#'.repeat(20)]).floorData;
  const g = L.visibleGrid(f, 1, 1, 2);
  assert.equal(g[1 * 20 + 3], 1); assert.equal(g[1 * 20 + 4], 0);
});

test('check 9.1-9.9: the text frame shows every item of spec section 9', () => {
  const s = world(['#@..m.#', '#######'], { inv: ['salve', null, 'oil', null] });
  const text = TV.renderFrame(V.view(s));
  for (const needle of ['seed: scenario', 'Floor 1/5', 'Turn 0', 'HP 12/12', 'Ember 100/100', 'r=6', 'dims 1/turn',
    '[1] salve', '[2] empty', '[3] oil', '[4] empty', 'Creatures:', 'Cave moth', 'Messages:', '@']) {
    assert.ok(text.includes(needle), 'missing: ' + needle);
  }
});

test('view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not)', () => {
  const adj = V.view(world(['#@m.#']));
  assert.equal(adj.creatures[0].threat, true);
  assert.match(TV.renderFrame(adj), /! m#1/);
  assert.equal(V.view(world(['#@.m#'])).creatures[0].threat, false);
});
