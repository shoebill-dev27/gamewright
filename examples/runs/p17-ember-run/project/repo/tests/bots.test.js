'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const bot = require('./bot.js');

const SEEDS = Array.from({ length: 20 }, (_, i) => 'bot-' + (i + 1));
let cache = null;
const runs = () => (cache = cache || SEEDS.map((s) => bot.playRun(s, { maxCommands: 1500 })));

test('check 14 (strict, D-002): every bot damage event was shown and marked on the tile where the player ended the turn (20 seeds)', (t) => {
  const counts = { threat: 0, reach: 0 };
  const bad = [];
  for (const r of runs()) {
    for (const e of r.log) {
      for (const d of e.damage) {
        if (!d.visibleBefore) bad.push({ seed: r.seed, turn: e.turn, why: 'not shown before', d });
        else if (!d.markedBefore) bad.push({ seed: r.seed, turn: e.turn, why: 'shown but not marked for case ' + d.case, d });
        else counts[d.case]++;
      }
    }
  }
  t.diagnostic('damage events by case: ' + JSON.stringify(counts));
  assert.deepEqual(bad.slice(0, 5), [], 'unmarked damage (' + bad.length + ' total)');
});

test('check 26: bot runs end in a result; at least 3 land in 250-700 turns; at least one wins', (t) => {
  const all = runs();
  const summary = all.map((r) => r.seed + ':' + (r.state.end ? r.state.end.result : 'unfinished') + '@' + r.state.turn + '/f' + r.state.floor);
  t.diagnostic(summary.join(' '));
  for (const r of all) assert.ok(r.state.end, r.seed + ' did not finish in 1500 commands');
  const inRange = all.filter((r) => r.state.turn >= 250 && r.state.turn <= 700);
  assert.ok(inRange.length >= 3, 'runs in 250-700 turns: ' + inRange.length + ' of ' + all.length + ' (' + summary.join(' ') + ')');
  assert.ok(all.some((r) => r.state.end.result === 'victory'), 'no bot victory (' + summary.join(' ') + ')');
});
