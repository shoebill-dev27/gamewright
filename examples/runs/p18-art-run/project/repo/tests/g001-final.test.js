'use strict';
// Handoff 11: unlit brazier + Gloom, hound at distance 1, trace fields, and real play.js / --trace runs.
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const cp = require('node:child_process');
const { G, V, SC, A, run, cr, world } = require('./helpers.js');
const TV = require('../src/textview.js');

const reachOf = (v, dir) => { const e = v.reach.find((r) => r.dir === dir); return e ? e.creatures.map((c) => c.letter) : []; };
const PLAY = path.join(__dirname, '..', 'play.js');

test('unlit brazier beside a gathered Gloom: reach mark from the Gloom; the slam lands', () => {
  const s = world(['#.@BG..#'], { floor: 5 });
  s.creatures[0].gathering = true;
  const v = V.view(s);
  assert.deepEqual(reachOf(v, 'E'), ['G']);
  assert.deepEqual(reachOf(v, 'W'), []);
  assert.match(TV.renderFrame(v), /Danger: E \(G\)/);
  const after = G.step(s, A.E).state;
  assert.equal(after.hp, 8);
});

test('unlit brazier beside an ungathered Gloom: no mark (it only gathers), no damage', () => {
  const s = world(['#.@BG..#'], { floor: 5 });
  assert.deepEqual(reachOf(V.view(s), 'E'), []);
  assert.equal(G.step(s, A.E).state.hp, 12);
});

test('crouching hound at distance 2: a step toward it is marked beforehand and is bitten for 3', () => {
  const s = world(['#@.h.#']);
  s.creatures[0].crouching = true; s.creatures[0].dir = 'W';
  const v = V.view(s);
  assert.equal(v.threats.length, 1);
  assert.deepEqual(reachOf(v, 'E'), ['h']);
  assert.equal(G.step(s, A.E).state.hp, 9);
});

test('flare timing: a moth acts on the third turn counting the lighting turn as the first', () => {
  let s = world(['#@B..m.#']);
  s = run(s, A.E);                       // turn 1 (lighting): skipped
  assert.equal(cr(s, 1).x, 5);
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 5);   // turn 2: skipped
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 4);   // turn 3: acts
});

test('trace fields: damage entries carry case and the matching mark', () => {
  const s = world(['#@.m.#']);
  let r = SC.stepLogged(s, A.E, V.view(s), 1);
  assert.equal(r.entry.damage.length, 1);
  assert.equal(r.entry.damage[0].case, 'reach'); assert.equal(r.entry.damage[0].markedBefore, true);
  assert.match(TV.renderTrace(r.entry), /case=reach markedBefore=true/);
  const w = world(['#@m.#']);
  r = SC.stepLogged(w, A.wait, V.view(w), 1);
  assert.equal(r.entry.damage[0].case, 'threat'); assert.equal(r.entry.damage[0].markedBefore, true);
});

test('node play.js runs a script from stdin', (t) => {
  const res = cp.spawnSync(process.execPath, [PLAY, '-'], { input: 'seed 42\ndd.\n', encoding: 'utf8' });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /seed: 42/);
  assert.match(res.stdout, /--- command 3: "\." ---/);
  assert.match(res.stdout, /Danger: /);
  t.diagnostic('play.js stdout lines: ' + res.stdout.split('\n').length);
});

test('node play.js --trace prints trace lines', (t) => {
  const res = cp.spawnSync(process.execPath, [PLAY, '--trace', '-'], { input: 'seed 42\ndd.\n', encoding: 'utf8' });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /\[trace\] command 3/);
  assert.match(res.stdout, /threats before action:/);
  t.diagnostic(res.stdout.split('\n').filter((l) => l.startsWith('[trace] command')).join(' || '));
});
