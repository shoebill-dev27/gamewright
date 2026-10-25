'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, run, cr, world } = require('./helpers.js');

test('check 9: moth moves 1 toward the player within r+3, stays beyond, hits for 1, dies to one hit', () => {
  let s = run(world(['#@....m.#']), A.wait);
  assert.equal(cr(s, 1).x, 5);                               // path distance 5 <= 9: moves
  s = run(world(['#@' + '.'.repeat(10) + 'm#']), A.wait);
  assert.equal(cr(s, 1).x, 12);                              // distance 11 > 9: stays
  s = run(world(['#@m.#']), A.wait);
  assert.equal(s.hp, 11);                                    // adjacent: exactly 1
  s = run(world(['#@m.#']), A.E);
  assert.equal(s.creatures.length, 0); assert.equal(s.hp, 12); assert.equal(s.defeated, 1);
});

test('check 10: shade flees when r>=3, hits only when cornered; at r=2 it hunts and hits for 2; takes 2 hits', () => {
  let s = world(['#@..s....#']);
  let prev = cr(s, 1).x - 1;
  for (let i = 0; i < 3; i++) {
    s = run(s, A.wait);
    assert.ok(cr(s, 1).x - 1 > prev, 'moved away'); prev = cr(s, 1).x - 1;
    assert.equal(s.hp, 12);
  }
  assert.equal(run(world(['#@s#']), A.wait).hp, 10);          // cornered and adjacent
  s = world(['#@...s...#'], { ember: 19 });
  s = run(s, A.wait, A.wait, A.wait);
  assert.equal(cr(s, 1).x, 2); assert.equal(s.hp, 12);        // adjacent now, has not attacked yet
  s = run(s, A.wait);
  assert.equal(s.hp, 10);
  s = world(['#@s#'], { ember: 19 });
  s = run(s, A.E);
  assert.equal(cr(s, 1).hp, 2);
  s = run(s, A.E);
  assert.equal(s.creatures.length, 0);
});

const ROOM = ['#########', '#.......#', '#..@.h..#', '#.......#', '#########'];

test('check 11: hound crouches at distance 2 in a clear line; stepping out avoids the bite; staying takes 3; adjacent bites 3', () => {
  let s = run(world(ROOM), A.wait);
  assert.equal(cr(s, 1).crouching, true); assert.equal(s.hp, 12);
  const v = V.view(s);
  assert.equal(v.creatures[0].threat, true); assert.equal(v.creatures[0].state, 'crouching');
  assert.equal(v.cells[2][4].threat, true);                   // its line is marked
  const out = run(s, A.N);
  assert.equal(out.hp, 12); assert.equal(cr(out, 1).crouching, false);
  const stay = run(s, A.wait);
  assert.equal(stay.hp, 9); assert.equal(cr(stay, 1).x, 4);
  assert.equal(run(world(['#########', '#..@h...#', '#########']), A.wait).hp, 9);
  assert.equal(cr(run(world(['#@....h..#']), A.wait), 1).x, 5);   // hunts within 6
  assert.equal(cr(run(world(['#@......h#']), A.wait), 1).x, 8);   // distance 7: idle
});

test('check 12: a creature moves or attacks, never both; it appears adjacent one turn before its first attack', () => {
  let s = world(['#@..m.#']);
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 3); assert.equal(s.hp, 12);
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 2); assert.equal(s.hp, 12);   // now adjacent, no damage yet
  const r = G.step(s, A.wait);
  assert.equal(r.state.hp, 11);
  assert.equal(r.events.filter((e) => e.t === 'damage').length, 1);
});

test('check 13: brazier flare stuns visible creatures within 7 for 2 turns and labels them stunned', () => {
  let s = world(['#@B..m.#']);
  s = run(s, A.E);
  assert.equal(cr(s, 1).stunned, 1);
  assert.equal(V.view(s).creatures[0].state, 'stunned');
  assert.equal(V.view(s).creatures[0].threat, false);
  assert.equal(cr(s, 1).x, 5);
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 5);            // second skipped action
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 4);            // acts again
  const far = run(world(['#@B' + '.'.repeat(9) + 'm#']), A.E);
  assert.equal(cr(far, 1).stunned, 0);                        // farther than 7
  const gl = run(world(['#@B.G..#'], { floor: 5 }), A.E);
  assert.equal(cr(gl, 1).stunned, 0);                         // the Gloom is not stunned
});
