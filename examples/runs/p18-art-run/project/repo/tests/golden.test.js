'use strict';
// G-002 criterion 48: the text player output is unchanged. Compares sha256 + byte count of the full text output
// (renderRun, as play.js prints it) with the values captured before the picture work (tests/golden/hashes.json).
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { world } = require('./helpers.js');
const SC = require('../src/script.js');

const GOLD = JSON.parse(fs.readFileSync(path.join(__dirname, 'golden', 'hashes.json'), 'utf8'));

function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ALPHA = 'wasd.wasdwasd1';
function gen(n, k) { const r = lcg(k), out = []; for (let i = 0; i < n; i++) out.push(ALPHA.charAt(r() % ALPHA.length)); return out; }
const rowsG = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};

const CASES = [
  ['seed-a', () => SC.runScript('g-a', gen(250, 11))],
  ['seed-b', () => SC.runScript('g-b', gen(250, 23))],
  ['seed-c', () => SC.runScript('hollow', gen(250, 37))],
  ['seed-d', () => SC.runScript('42', gen(250, 59))],
  ['scenario-hound', () => SC.runScript('scenario', '....'.split(''), { state: world(['#@.h..#']) })],
  ['scenario-gloom', () => SC.runScript('scenario', '....w.'.split(''), { state: world(rowsG(2, 4), { floor: 5 }) })],
  ['scenario-flare', () => SC.runScript('scenario', 'dddd..'.split(''), { state: world(['#@.m.B..s.#']) })]
];

for (const [name, mk] of CASES) {
  test('golden text output (criterion 48): ' + name, () => {
    const text = SC.renderRun(mk());
    const sha = crypto.createHash('sha256').update(text, 'utf8').digest('hex');
    assert.equal(Buffer.byteLength(text, 'utf8'), GOLD[name].bytes, 'byte count');
    assert.equal(sha, GOLD[name].sha256, 'sha256');
  });
}
