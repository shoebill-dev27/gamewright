'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, FG, SC, A, run, world } = require('./helpers.js');

test('check 21: same seed + same commands gives byte-identical text output', () => {
  const cmds = 'dddddwwwaaasssdd....ddddwwww'.split('');
  const a = SC.renderRun(SC.runScript('det-1', cmds), { trace: true });
  const b = SC.renderRun(SC.runScript('det-1', cmds), { trace: true });
  assert.equal(a, b);
  assert.notEqual(a, SC.renderRun(SC.runScript('det-2', cmds), { trace: true }));
});

test('check 21: floor 2 does not depend on what the player did on floor 1', () => {
  const a = run(world(['#@>.#'], { seed: 'xfloor' }), A.E);
  const b = run(world(['#@>.#'], { seed: 'xfloor' }), A.wait, A.wait, A.E);
  assert.equal(a.floor, 2); assert.equal(b.floor, 2);
  assert.equal(JSON.stringify(a.floorData), JSON.stringify(b.floorData));
  assert.deepEqual(a.creatures.map((c) => [c.type, c.x, c.y]), b.creatures.map((c) => [c.type, c.x, c.y]));
  assert.deepEqual(a.items, b.items);
});

test('check 22: at least 9 of 10 seeds give different floor 1 layouts', () => {
  const set = new Set();
  for (let i = 0; i < 10; i++) set.add(FG.generateFloor('layout-' + i, 1).tiles.join('/'));
  assert.ok(set.size >= 9, 'distinct layouts: ' + set.size);
});

test('check 23: 50 seeds x floors 1-5 satisfy every generator guarantee', () => {
  for (let i = 0; i < 50; i++) {
    for (let n = 1; n <= 5; n++) {
      const seed = 'bulk-' + i;
      const f = FG.generateFloor(seed, n);
      const errs = FG.validateFloor(f, n);
      assert.deepEqual(errs, [], 'seed ' + seed + ' floor ' + n);
      const flat = f.tiles.join('');
      assert.equal((flat.match(/</g) || []).length, 1);
      assert.equal((flat.match(/>/g) || []).length, n < 5 ? 1 : 0);
      assert.equal((flat.match(/B/g) || []).length, n < 5 ? 2 : 3);
      assert.equal(f.creatureSpawns.length, ({ 1: 4, 2: 5, 3: 6, 4: 8, 5: 4 })[n]);
      // same inputs, same floor
      assert.equal(JSON.stringify(FG.generateFloor(seed, n)), JSON.stringify(f));
    }
  }
});

test('check 20: after an end state a script ignores later commands', () => {
  const a = SC.runScript('end-test', '.'.repeat(150).split(''));
  const b = SC.runScript('end-test', '.'.repeat(200).split(''));
  assert.ok(a.state.end, 'the run ended');
  assert.ok(a.ignored > 0);
  assert.equal(JSON.stringify(a.state), JSON.stringify(b.state));
});

test('script format: seed line, comments, spaces, unknown characters', () => {
  const p = SC.parseScript('# comment\nseed my seed 7 # trailing\nw a s d . 1 2\n3 4 # x\n');
  assert.equal(p.seed, 'my seed 7');
  assert.deepEqual(p.commands, ['w', 'a', 's', 'd', '.', '1', '2', '3', '4']);
  assert.equal(SC.parseScript('ddd').seed, SC.DEFAULT_SEED);
  assert.throws(() => SC.parseScript('seed 1\nwx'), /unknown command/);
});
