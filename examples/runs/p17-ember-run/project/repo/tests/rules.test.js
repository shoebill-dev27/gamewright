'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, L, A, use, run, cr, world } = require('./helpers.js');

const quiet = (opts) => world(['#'.repeat(30), '#@' + '.'.repeat(27) + '#', '#'.repeat(30)], opts);

test('check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5', () => {
  const v = V.view(G.newRun('check-1'));
  assert.equal(v.ember, 100); assert.equal(v.radius, 6);
  assert.equal(v.hp, 12); assert.equal(v.maxHp, 12);
  assert.equal(v.floor, 1); assert.equal(v.floors, 5); assert.equal(v.turn, 0);
});

test('check 2: waiting costs 1 E; radius thresholds', () => {
  let s = quiet();
  s = run(s, A.wait);
  assert.equal(s.ember, 99);
  for (let i = 0; i < 19; i++) s = run(s, A.wait);
  assert.equal(s.ember, 80); assert.equal(V.view(s).radius, 6);
  s = run(s, A.wait);
  assert.equal(s.ember, 79); assert.equal(V.view(s).radius, 5);
  const table = { 100: 6, 80: 6, 79: 5, 60: 5, 59: 4, 40: 4, 39: 3, 20: 3, 19: 2, 1: 2 };
  for (const E of Object.keys(table)) assert.equal(L.radiusFor(Number(E)), table[E], 'E=' + E);
});

test('check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn', () => {
  let s = quiet();
  let r = G.step(s, A.E); assert.equal(r.state.ember, 99); assert.equal(r.state.turn, 1);
  r = G.step(s, A.wait); assert.equal(r.state.ember, 99);
  r = G.step(world(['#@m#']), A.E); assert.equal(r.state.ember, 99); assert.equal(r.state.defeated, 1);
  r = G.step(world(['#@.#'], { hp: 5, inv: ['salve', null, null, null] }), use(1));
  assert.equal(r.state.ember, 99); assert.equal(r.state.hp, 10);
  r = G.step(world(['#@.#'], { ember: 50, inv: ['oil', null, null, null] }), use(1));
  assert.equal(r.state.ember, 79); // +30 then -1
  // refused: wall, oil at full E, salve at full HP, empty slot
  const w = world(['###', '#@#', '###']);
  r = G.step(w, A.N); assert.equal(r.turnConsumed, false); assert.equal(r.state.turn, 0); assert.equal(r.state.ember, 100);
  const o = world(['#@.#'], { inv: ['oil', 'salve', null, null] });
  r = G.step(o, use(1)); assert.equal(r.turnConsumed, false); assert.equal(r.state.turn, 0); assert.equal(r.state.ember, 100);
  assert.deepEqual(r.state.inv, ['oil', 'salve', null, null]);
  r = G.step(o, use(2)); assert.equal(r.turnConsumed, false); assert.equal(r.state.hp, 12);
  r = G.step(o, use(3)); assert.equal(r.turnConsumed, false);
});

test('check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later', () => {
  let s = world(['#@B..#'], { ember: 30 });
  s = run(s, A.E);
  assert.equal(s.ember, 89); assert.equal(s.lit.length, 1);
  s = run(s, A.E); assert.equal(s.ember, 88);
  s = run(s, A.W); assert.equal(s.ember, 87); // back on the lit brazier: only dimming
  assert.equal(run(world(['#@B..#'], { ember: 80 }), A.E).ember, 99);
});

test('check 5: E reaching 0 ends the run; creatures do not act', () => {
  const s = run(world(['#@m.#'], { ember: 1 }), A.wait);
  assert.equal(s.end.result, 'ember'); assert.equal(s.hp, 12);
  assert.match(s.end.message, /The ember went out on floor 1/);
});

test('check 6: messages at E 20, 10, 5 and when r drops', () => {
  const m = (E) => run(quiet({ ember: E }), A.wait).messages.join(' | ');
  assert.match(m(21), /Ember low: 20/);
  assert.match(m(11), /Ember low: 10/);
  assert.match(m(6), /Ember low: 5/);
  assert.match(m(80), /Your light shrinks/);
  assert.doesNotMatch(m(90), /shrinks/);
});

test('check 7: remembered tiles stay; out-of-sight creatures are not listed', () => {
  let s = world(['#'.repeat(41), '#@' + '.'.repeat(37) + 'm#', '#'.repeat(41)], { ember: 30 });
  for (let i = 0; i < 10; i++) s = run(s, A.E);
  const v = V.view(s);
  assert.equal(v.cells[1][1].seen, true); assert.equal(v.cells[1][1].vis, false);
  assert.equal(v.cells[1][1].terrain, 'floor');
  assert.equal(v.creatures.length, 0);
});

test('check 8: oil +30 up to 100 then dim; salve +5 up to 12', () => {
  assert.equal(run(world(['#@.#'], { ember: 90, inv: ['oil', null, null, null] }), use(1)).ember, 99);
  assert.equal(run(world(['#@.#'], { hp: 10, inv: ['salve', null, null, null] }), use(1)).hp, 12);
});

test('check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out', () => {
  let s = run(world(['#@m.#'], { hp: 1, ember: 50 }), A.wait);
  assert.equal(s.end.result, 'dead'); assert.equal(s.end.message, 'You fell on floor 1.');
  assert.equal(s.end.floor, 1);
  s = run(world(['#@m.#'], { hp: 1, ember: 1 }), A.wait);
  assert.equal(s.end.result, 'ember');
});

test('check 20: after an end state further commands change nothing', () => {
  const s = run(world(['#@m.#'], { hp: 1, ember: 50 }), A.wait);
  const before = JSON.stringify(s);
  const r = G.step(s, A.E);
  assert.equal(r.turnConsumed, false);
  assert.equal(JSON.stringify(r.state), before);
  assert.equal(JSON.stringify(G.step(s, use(1)).state), before);
});

test('check 24: descending keeps E and HP apart from dimming, increments floor, places on <', () => {
  const s0 = world(['#@>.#'], { hp: 7, ember: 50 });
  const r = G.step(s0, A.E);
  const s = r.state;
  assert.equal(s.floor, 2); assert.equal(s.ember, 49); assert.equal(s.hp, 7); assert.equal(s.turn, 1);
  assert.deepEqual(s.player, s.floorData.start);
  assert.equal(s.floorData.tiles[s.player.y].charAt(s.player.x), '<');
  assert.equal(s.end, null);
});

test('check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn', () => {
  const s = run(world(['#@+.#'], { inv: ['salve', 'salve', 'oil', 'oil'] }), A.E);
  assert.equal(s.items.length, 1); assert.equal(s.turn, 1); assert.equal(s.ember, 99);
  assert.match(s.messages.join(' '), /pack is full/);
  assert.deepEqual(s.inv, ['salve', 'salve', 'oil', 'oil']);
  const t = run(world(['#@+.#']), A.E);
  assert.equal(t.items.length, 0); assert.equal(t.inv[0], 'salve');
});
