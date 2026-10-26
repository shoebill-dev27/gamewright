'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, run, cr, world } = require('./helpers.js');

const rows = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};

test('check 15: the Gloom has 24 HP; within 4 the ember loses 2 and the HUD says dims 2/turn', () => {
  let s = world(rows(1, 5), { floor: 5 });
  assert.equal(cr(s, 1).hp, 24);
  assert.equal(V.view(s).dim, 2);
  s = run(s, A.wait); assert.equal(s.ember, 98);
  const far = world(rows(1, 6), { floor: 5 });
  assert.equal(V.view(far).dim, 1);
  assert.equal(run(far, A.wait).ember, 99);
});

test('check 16: gather marks 3x3 for one turn; the next turn deals 4 inside, 0 outside', () => {
  // player outside the area (distance 2)
  let s = run(world(rows(2, 4), { floor: 5 }), A.wait);
  assert.equal(cr(s, 1).gathering, true);
  const v = V.view(s);
  assert.equal(v.cells[1][3].threat, true); assert.equal(v.cells[3][5].threat, true);
  assert.equal(v.creatures[0].threat, true);
  s = run(s, A.wait);
  assert.equal(s.hp, 12); assert.equal(cr(s, 1).staggered, 3);
  // player inside the area (adjacent)
  s = run(world(rows(3, 4), { floor: 5 }), A.wait, A.wait);
  assert.equal(s.hp, 8); assert.equal(cr(s, 1).staggered, 3);
});

test('check 17: staggered for 3 turns doing nothing; hits deal 4 then, 2 otherwise', () => {
  let s = world(rows(3, 4), { floor: 5 });
  s.creatures[0].staggered = 3;
  const hit = run(s, A.E);
  assert.equal(cr(hit, 1).hp, 20);
  const w = run(s, A.wait, A.wait, A.wait);
  assert.equal(cr(w, 1).staggered, 0); assert.equal(w.hp, 12); assert.equal(cr(w, 1).x, 4);
  assert.equal(cr(w, 1).gathering, false);
  assert.equal(cr(run(world(rows(3, 4), { floor: 5 }), A.E), 1).hp, 22);
});

test('check 18: killing the Gloom wins at once, before dimming, with the summary', () => {
  const s0 = world(rows(3, 4), { floor: 5, ember: 3 });
  s0.creatures[0].hp = 2;
  const s = run(s0, A.E);
  assert.equal(s.end.result, 'victory');
  assert.equal(s.end.message, 'The Gloom breaks. Light returns to the hollow.');
  assert.equal(s.ember, 3);                                   // no dimming on the winning turn
  assert.equal(s.end.turns, 1); assert.equal(s.end.defeated, 1); assert.equal(s.end.floor, 5);
  assert.equal(s.end.seed, 'scenario');
});
