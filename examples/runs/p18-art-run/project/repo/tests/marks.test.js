'use strict';
// G-002 criterion 45: pictures change no mark. scene.build leaves the view untouched; the marks the page draws
// (cell.threat, creature.threat, reach) equal the marks in the text frame at every turn of scripted runs.
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, world } = require('./helpers.js');
const TV = require('../src/textview.js');
const SCN = require('../src/scene.js');
const { compareMarks } = require('./pic-helpers.js');

const rows = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};
function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ACTS = [A.N, A.E, A.S, A.W, A.wait];

function walk(name, st, acts, seen) {
  for (let i = 0; i < acts.length; i++) {
    const v = V.view(st), before = JSON.stringify(v);
    const sc = SCN.build(v);
    assert.equal(JSON.stringify(v), before, name + ' view changed by scene.build at ' + i);
    assert.deepEqual(compareMarks(v, TV.renderFrame), [], name + ' step ' + i);
    if (sc.actors.some((a) => a.picture === 'hound-crouch')) seen.crouch++;
    if (v.creatures.some((c) => c.type === 'gloom' && c.state === 'gathering' && c.threat)) seen.gather++;
    if (v.creatures.some((c) => c.threat)) seen.threat++;
    if (v.reach.length) seen.reach++;
    if (sc.actors.some((a) => a.wash)) seen.wash++;
    st = G.step(st, acts[i]).state;
  }
}

test('criterion 45: scripted runs with a hound crouch, a Gloom gather, a flare and random walks', () => {
  const seen = { crouch: 0, gather: 0, threat: 0, reach: 0, wash: 0 };
  walk('hound', world(['#@.h..#']), [A.wait, A.wait, A.wait, A.E, A.wait], seen);
  walk('gloom', world(rows(2, 4), { floor: 5 }), [A.wait, A.wait, A.wait, A.wait, A.E, A.wait], seen);
  walk('flare', world(['#@.m.B..s.#']), [A.E, A.E, A.E, A.wait, A.E, A.W, A.wait], seen);
  for (const sd of ['pic-a', 'pic-b', 'pic-c']) {
    const rnd = lcg(sd.charCodeAt(4) * 13);
    const acts = []; for (let i = 0; i < 120; i++) acts.push(ACTS[rnd() % 5]);
    walk(sd, G.newRun(sd), acts, seen);
  }
  assert.ok(seen.crouch > 0, 'a crouching hound was seen');
  assert.ok(seen.gather > 0, 'a gathering Gloom was seen');
  assert.ok(seen.threat > 0 && seen.reach > 0 && seen.wash > 0, JSON.stringify(seen));
});
