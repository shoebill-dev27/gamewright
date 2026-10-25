/* view(state): the render model shared by play.js and the page (spec 9). UMD-style (D-001).
   Marks (D-002) use the ember as it will be after this turn's dimming, and come from the same
   planner the creatures act with (planAction), evaluated with a hypothetical player position. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./light.js'); require('./game.js'); }
  var L = EH.light, G = EH.game;

  var DAMAGING = { attack: true, lunge: true, slam: true };
  var DIR_ORDER = ['N', 'E', 'S', 'W'];

  function manh(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); }

  // Shallow copy of the state with the player moved (planAction only reads).
  function withPlayer(s, pos) {
    var o = {};
    Object.keys(s).forEach(function (k) { o[k] = s[k]; });
    o.player = { x: pos.x, y: pos.y };
    return o;
  }

  // Planner context for "the player ends the turn on pos": E after that turn's dimming.
  // null when the ember would be out (creatures do not act).
  function hypo(s, pos, base) {
    var s2 = withPlayer(s, pos), e = Math.max(0, (base === undefined ? s.ember : base) - G.drainRate(s2));
    if (e <= 0) return null;
    var r = L.radiusFor(e);
    return { s: s2, ctx: { dist: G.bfsFromPlayer(s2), vis: L.visibleGrid(s.floorData, pos.x, pos.y, r), r: r } };
  }

  function occupied(s, x, y) {
    return s.creatures.some(function (c) { return c.hp > 0 && c.x === x && c.y === y; });
  }

  // Damage the creature would do to s2.player at its next action given its planned intent (0 = none).
  function hurtsAt(s2, c, it) {
    var p = s2.player, i;
    if (it.kind === 'attack') return it.damage;
    if (it.kind === 'slam') return Math.max(Math.abs(p.x - c.x), Math.abs(p.y - c.y)) <= 1 ? it.damage : 0;
    if (it.kind === 'lunge') {
      var dv = G.DIRS[c.dir], k = 0;
      for (i = 1; i <= 2; i++) if (p.x === c.x + dv[0] * i && p.y === c.y + dv[1] * i) k = i;
      if (!k) return 0;
      for (i = 1; i < k; i++) {
        var x = c.x + dv[0] * i, y = c.y + dv[1] * i;
        if (L.tileAt(s2.floorData, x, y) !== '.' || occupied(s2, x, y)) return 0;
      }
      return 3;
    }
    return 0;
  }

  function view(s) {
    var fd = s.floorData, w = fd.w, h = fd.h, E = s.ember, r = L.radiusFor(E), pl = s.player;
    var vis = L.visibleGrid(fd, pl.x, pl.y, r);
    var litSet = {}, itemAt = {}, tt = {}, rk = {}, creatures = [], threats = [], reach = [], x, y;
    s.lit.forEach(function (k) { litSet[k] = 1; });
    s.items.forEach(function (it) { itemAt[it.x + ',' + it.y] = it.type; });

    // Neighbour tiles the player could step onto (not walls).
    var nbs = [];
    DIR_ORDER.forEach(function (d) {
      var dv = G.DIRS[d], nx = pl.x + dv[0], ny = pl.y + dv[1];
      if (L.tileAt(fd, nx, ny) !== '#') nbs.push({ dir: d, x: nx, y: ny });
    });

    // Shown creatures: visible ones, plus any orthogonally adjacent to the player or a neighbour tile.
    var shown = s.creatures.filter(function (c) {
      if (c.hp <= 0) return false;
      if (vis[c.y * w + c.x]) return true;
      if (manh(c, pl) === 1) return true;
      return nbs.some(function (n) { return manh(c, n) === 1; });
    });

    var cur = s.end ? null : hypo(s, pl);
    var planS = cur ? cur.s : s, planCtx = cur ? cur.ctx : { dist: G.bfsFromPlayer(s), vis: vis, r: r };

    shown.forEach(function (c) {
      var it = G.planAction(planS, c, planCtx), th = !!cur && !!DAMAGING[it.kind], reason = null;
      if (th) {
        if (it.kind === 'attack') reason = 'hits for ' + it.damage + ' at its next action';
        else if (it.kind === 'lunge') reason = 'crouched: lunges along the marked line for 3';
        else reason = 'slam on the marked area for ' + it.damage;
        (it.line || it.area || []).forEach(function (t) { tt[t.x + ',' + t.y] = 1; });
      }
      var cv = { id: c.id, type: c.type, letter: G.DEFS[c.type].letter, name: G.DEFS[c.type].name,
        hp: c.hp, maxHp: c.maxHp, x: c.x, y: c.y, state: it.label, threat: th, reason: reason };
      creatures.push(cv);
      if (th) threats.push(cv);
    });

    // Reach marks (D-002): per neighbour tile, which shown creatures would hurt the player there.
    // None on walls, creature tiles or the down stairs. An unlit brazier is lit by the step (E+60 first) and the
    // flare stuns every stunnable creature there, so only the Gloom (not stunned) is evaluated on it.
    nbs.forEach(function (n) {
      var t = fd.tiles[n.y].charAt(n.x);
      var unlit = t === 'B' && !litSet[n.x + ',' + n.y];
      if (s.end || t === '>' || occupied(s, n.x, n.y)) return;
      var hp = hypo(s, n, unlit ? Math.min(100, s.ember + 60) : undefined);
      if (!hp) return;
      var list = [];
      shown.forEach(function (c) {
        if (unlit && c.type !== 'gloom') return;
        var dmg = hurtsAt(hp.s, c, G.planAction(hp.s, c, hp.ctx));
        if (dmg) list.push({ id: c.id, letter: G.DEFS[c.type].letter, damage: dmg });
      });
      if (list.length) {
        reach.push({ dir: n.dir, x: n.x, y: n.y, creatures: list });
        rk[n.x + ',' + n.y] = list.map(function (e) { return e.letter; });
      }
    });

    var cells = [];
    for (y = 0; y < h; y++) {
      var row = [];
      for (x = 0; x < w; x++) {
        var seen = !!(s.seen[y][x] || vis[y * w + x]), k = x + ',' + y, ch = fd.tiles[y].charAt(x), terrain = null;
        if (seen) terrain = ch === '#' ? 'wall' : ch === '<' ? 'up' : ch === '>' ? 'down'
          : ch === 'B' ? (litSet[k] ? 'lit' : 'brazier') : 'floor';
        row.push({ terrain: terrain, item: seen && itemAt[k] ? itemAt[k] : null, vis: !!vis[y * w + x], seen: seen,
          threat: !!(tt[k] && vis[y * w + x]), reach: rk[k] || [] });
      }
      cells.push(row);
    }
    return {
      seed: s.seed, floor: s.floor, floors: G.FLOORS, turn: s.turn, hp: s.hp, maxHp: G.MAX_HP,
      ember: E, radius: r, dim: G.drainRate(s), inv: s.inv.slice(), w: w, h: h, cells: cells,
      player: { x: pl.x, y: pl.y }, creatures: creatures, threats: threats, reach: reach,
      messages: s.messages.slice(), end: s.end
    };
  }

  EH.view = { view: view, visibleGrid: L.visibleGrid, radiusFor: L.radiusFor };
  if (typeof module === 'object' && module.exports) module.exports = EH.view;
})(typeof globalThis !== 'undefined' ? globalThis : this);
