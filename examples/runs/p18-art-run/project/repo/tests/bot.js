'use strict';
// Threat-following bot. Uses only the public API: newRun, step (through stepLogged) and view.
const G = require('../src/game.js');
const V = require('../src/view.js');
const SC = require('../src/script.js');

const DIRS = [['N', 0, -1], ['E', 1, 0], ['S', 0, 1], ['W', -1, 0]];
const key = (x, y) => x + ',' + y;
const manh = (a, b) => Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
const dirTo = (a, b) => (b.y < a.y ? 'N' : b.y > a.y ? 'S' : b.x > a.x ? 'E' : 'W');

function chooseAction(v) {
  const me = v.player;
  const crea = new Map(v.creatures.map((c) => [key(c.x, c.y), c]));
  const cell = (x, y) => (x < 0 || y < 0 || x >= v.w || y >= v.h ? null : v.cells[y][x]);
  const walk = (c) => !!(c && c.seen && c.terrain && c.terrain !== 'wall');
  const move = (d) => ({ type: 'move', dir: d });
  const WAIT = { type: 'wait' };
  const here = cell(me.x, me.y);

  function search(goal, blockCreatures, avoidThreat) {
    const seen = new Set([key(me.x, me.y)]);
    const q = [{ x: me.x, y: me.y, first: null, d: 0 }];
    for (let qi = 0; qi < q.length; qi++) {
      const cur = q[qi];
      for (const [dn, dx, dy] of DIRS) {
        const nx = cur.x + dx, ny = cur.y + dy, k = key(nx, ny);
        if (seen.has(k)) continue;
        const c = cell(nx, ny);
        if (!walk(c)) continue;
        seen.add(k);
        const isGoal = goal(nx, ny, c);
        if (!isGoal) {
          if (blockCreatures && crea.has(k)) continue;
          if (avoidThreat && c.threat) continue;
        }
        const first = cur.first || dn;
        if (isGoal) return { dir: first, x: nx, y: ny, d: cur.d + 1 };
        q.push({ x: nx, y: ny, first, d: cur.d + 1 });
      }
    }
    return null;
  }
  const find = (goal) => search(goal, true, true) || search(goal, false, true) || search(goal, false, false);

  // 1. step out of a marked line / area
  if (here.threat) {
    for (const [dn, dx, dy] of DIRS) {
      const n = cell(me.x + dx, me.y + dy);
      if (walk(n) && !crea.has(key(me.x + dx, me.y + dy)) && !n.threat) return move(dn);
    }
  }
  // 2. fight what is adjacent (threats first)
  const adj = v.creatures.filter((c) => manh(c, me) === 1).sort((a, b) => (b.threat - a.threat) || (a.id - b.id));
  if (adj.length) return move(dirTo(me, adj[0]));
  // 3. items
  if (v.hp <= 6) { const i = v.inv.indexOf('salve'); if (i >= 0) return { type: 'use', slot: i + 1 }; }
  if (v.ember <= 25) { const i = v.inv.indexOf('oil'); if (i >= 0) return { type: 'use', slot: i + 1 }; }
  // 4. the Gloom: wait out the gather outside the area, otherwise close in
  const gl = v.creatures.find((c) => c.type === 'gloom');
  if (gl) {
    if (gl.state === 'gathering') return WAIT;
    const r = find((x, y) => manh({ x, y }, gl) === 1);
    return r ? move(r.dir) : WAIT;
  }
  // 5. braziers within about 10 steps, nearby items, stairs, exploration
  const br = find((x, y, c) => c.terrain === 'brazier');
  if (br && br.d <= 10 && v.ember <= 75) return move(br.dir);
  if (v.inv.includes(null)) {
    const it = find((x, y, c) => !!c.item);
    if (it && it.d <= 8) return move(it.dir);
  }
  const st = find((x, y, c) => c.terrain === 'down');
  if (st) return move(st.dir);
  const fr = find((x, y) => DIRS.some(([, dx, dy]) => { const n = cell(x + dx, y + dy); return n && !n.seen; }));
  if (fr) return move(fr.dir);
  return WAIT;
}

function playRun(seed, opts) {
  opts = opts || {};
  const max = opts.maxCommands || 1500;
  let st = G.newRun(seed), v = V.view(st), n = 0, refused = 0;
  const log = [];
  while (!st.end && n < max) {
    if (opts.onState) opts.onState(st, v);
    const a = refused > 0 ? { type: 'wait' } : chooseAction(v);
    const r = SC.stepLogged(st, a, v, n + 1);
    n++;
    refused = r.consumed ? 0 : refused + 1;
    log.push(r.entry); st = r.state; v = r.view;
  }
  return { seed, state: st, log, commands: n };
}

module.exports = { chooseAction, playRun };
