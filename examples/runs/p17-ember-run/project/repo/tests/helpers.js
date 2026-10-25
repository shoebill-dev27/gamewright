'use strict';
const G = require('../src/game.js');
const V = require('../src/view.js');
const S = require('../src/scenario.js');
const L = require('../src/light.js');
const FG = require('../src/floorgen.js');
const SC = require('../src/script.js');

const A = {
  wait: { type: 'wait' },
  N: { type: 'move', dir: 'N' }, E: { type: 'move', dir: 'E' }, S: { type: 'move', dir: 'S' }, W: { type: 'move', dir: 'W' }
};
const use = (n) => ({ type: 'use', slot: n });
function run(s, ...acts) { let st = s; for (const a of acts) st = G.step(st, a).state; return st; }
const cr = (s, id) => s.creatures.find((c) => c.id === id);
const world = S.fromAscii;

module.exports = { G, V, S, L, FG, SC, A, use, run, cr, world };
