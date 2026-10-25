/* Seeded floor generator + validator (spec 5). UMD-style, D-001.
   Floor n depends only on (seed, n). Attempt k uses rng(seed, n, k); first valid attempt wins. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') require('./rng.js');

  var SIZES = { 1: [28, 16], 2: [30, 18], 3: [32, 18], 4: [34, 20], 5: [30, 18] };
  var COUNTS = {
    1: { moth: 4 },
    2: { moth: 3, shade: 2 },
    3: { moth: 2, shade: 3, hound: 1 },
    4: { moth: 2, shade: 3, hound: 3 },
    5: { gloom: 1, shade: 2, hound: 1 }
  };
  var MIN_STAIRS = { 1: 30, 2: 30, 3: 30, 4: 40 };
  var MAX_ATTEMPTS = 400;
  var DX = [0, 1, 0, -1], DY = [-1, 0, 1, 0];

  function kk(x, y) { return x + ',' + y; }

  // Walking distance map from (sx,sy) over all non-wall tiles (Infinity = unreachable).
  function bfs(f, sx, sy) {
    var w = f.w, h = f.h, dist = new Array(w * h);
    for (var i = 0; i < dist.length; i++) dist[i] = Infinity;
    dist[sy * w + sx] = 0;
    var q = [sy * w + sx];
    for (var qi = 0; qi < q.length; qi++) {
      var cur = q[qi], cx = cur % w, cy = (cur - cx) / w;
      for (var k = 0; k < 4; k++) {
        var nx = cx + DX[k], ny = cy + DY[k];
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        if (f.tiles[ny].charAt(nx) === '#') continue;
        var ni = ny * w + nx;
        if (dist[ni] !== Infinity) continue;
        dist[ni] = dist[cur] + 1;
        q.push(ni);
      }
    }
    return dist;
  }

  function blankGrid(w, h) {
    var gr = [];
    for (var y = 0; y < h; y++) { var row = []; for (var x = 0; x < w; x++) row.push('#'); gr.push(row); }
    return gr;
  }
  function carveRect(gr, x0, y0, x1, y1) {
    for (var y = y0; y <= y1; y++) for (var x = x0; x <= x1; x++) gr[y][x] = '.';
  }
  function carveH(gr, y, xa, xb) { for (var x = Math.min(xa, xb); x <= Math.max(xa, xb); x++) gr[y][x] = '.'; }
  function carveV(gr, x, ya, yb) { for (var y = Math.min(ya, yb); y <= Math.max(ya, yb); y++) gr[y][x] = '.'; }
  function joinTiles(gr) { return gr.map(function (r) { return r.join(''); }); }

  // Floors 1-4: rooms joined in a random chain by L-shaped corridors.
  function genRegular(rng, n) {
    var w = SIZES[n][0], h = SIZES[n][1], gr = blankGrid(w, h);
    var rooms = [], want = 5 + rng.int(4), i, t;
    for (t = 0; t < 300 && rooms.length < want; t++) {
      var rw = 4 + rng.int(5), rh = 3 + rng.int(4);
      var rx = 1 + rng.int(w - 1 - rw), ry = 1 + rng.int(h - 1 - rh), ok = true;
      for (i = 0; i < rooms.length; i++) {
        var o = rooms[i];
        if (!(rx + rw + 1 <= o.x || o.x + o.w + 1 <= rx || ry + rh + 1 <= o.y || o.y + o.h + 1 <= ry)) { ok = false; break; }
      }
      if (ok) rooms.push({ x: rx, y: ry, w: rw, h: rh });
    }
    if (rooms.length < 5) return null;
    var roomTiles = [];
    rooms.forEach(function (r) {
      carveRect(gr, r.x, r.y, r.x + r.w - 1, r.y + r.h - 1);
      for (var y = r.y; y < r.y + r.h; y++) for (var x = r.x; x < r.x + r.w; x++) roomTiles.push({ x: x, y: y });
    });
    function center(r) { return { x: r.x + Math.floor(r.w / 2), y: r.y + Math.floor(r.h / 2) }; }
    var order = rng.shuffle(rooms.map(function (_, ix) { return ix; }));
    for (i = 1; i < order.length; i++) {
      var a = center(rooms[order[i - 1]]), b = center(rooms[order[i]]);
      if (rng.int(2) === 0) { carveH(gr, a.y, a.x, b.x); carveV(gr, b.x, a.y, b.y); }
      else { carveV(gr, a.x, a.y, b.y); carveH(gr, b.y, a.x, b.x); }
    }
    var f0 = { w: w, h: h, tiles: joinTiles(gr) };
    var start = center(rooms[order[0]]);
    var dS = bfs(f0, start.x, start.y);
    var sd = null, best = -1;
    roomTiles.forEach(function (tl) {
      var d = dS[tl.y * w + tl.x];
      if (isFinite(d) && d > best) { best = d; sd = tl; }
    });
    if (!sd || best < MIN_STAIRS[n]) return null;
    var dG = bfs(f0, sd.x, sd.y), D = best;
    var occ = {}; occ[kk(start.x, start.y)] = 1; occ[kk(sd.x, sd.y)] = 1;
    function idx(tl) { return tl.y * w + tl.x; }
    function off(tl) { return dS[idx(tl)] + dG[idx(tl)] !== D; } // strict: not on ANY shortest path
    function free(tl) { return !occ[kk(tl.x, tl.y)]; }
    var candA = roomTiles.filter(function (tl) { return free(tl) && off(tl) && dS[idx(tl)] <= 25; });
    if (!candA.length) return null;
    var A = rng.pick(candA); occ[kk(A.x, A.y)] = 1;
    var dA = bfs(f0, A.x, A.y);
    var candB = roomTiles.filter(function (tl) { return free(tl) && off(tl) && dA[idx(tl)] >= 10; });
    if (!candB.length) return null;
    var B = rng.pick(candB); occ[kk(B.x, B.y)] = 1;
    var candS = roomTiles.filter(function (tl) { return free(tl) && off(tl); });
    if (!candS.length) return null;
    var salve = rng.pick(candS); occ[kk(salve.x, salve.y)] = 1;
    var candO = roomTiles.filter(free);
    if (!candO.length) return null;
    var oil = rng.pick(candO); occ[kk(oil.x, oil.y)] = 1;
    var spots = rng.shuffle(roomTiles.filter(function (tl) { return free(tl) && dS[idx(tl)] >= 6; }));
    var spawns = [], si = 0, counts = COUNTS[n], bad = false;
    ['moth', 'shade', 'hound'].forEach(function (type) {
      for (var k = 0; k < (counts[type] || 0); k++) {
        if (si >= spots.length) { bad = true; return; }
        var tl = spots[si++]; spawns.push({ type: type, x: tl.x, y: tl.y });
      }
    });
    if (bad) return null;
    gr[start.y][start.x] = '<'; gr[sd.y][sd.x] = '>'; gr[A.y][A.x] = 'B'; gr[B.y][B.x] = 'B';
    return {
      w: w, h: h, tiles: joinTiles(gr), start: start, stairsDown: { x: sd.x, y: sd.y },
      braziers: [{ x: A.x, y: A.y }, { x: B.x, y: B.y }],
      items: [{ x: salve.x, y: salve.y, type: 'salve' }, { x: oil.x, y: oil.y, type: 'oil' }],
      creatureSpawns: spawns, rooms: rooms, arena: null
    };
  }

  // Floor 5: start room, long corridor, one open arena with the Gloom and 3 braziers.
  function genBoss(rng) {
    var w = 30, h = 18, gr = blankGrid(w, h);
    var x0 = 12 + rng.int(3), x1 = 28, y0 = 4 + rng.int(2), y1 = 15 + rng.int(2);
    carveRect(gr, x0, y0, x1, y1);
    carveRect(gr, 1, 12, 5, 16);
    var xe = x0 + 2 + rng.int(x1 - x0 - 3);
    carveV(gr, 3, 2, 11); carveH(gr, 2, 3, xe); carveV(gr, xe, 2, y0 - 1);
    var start = { x: 1 + rng.int(5), y: 12 + rng.int(5) };
    var entrance = { x: xe, y: y0 };
    var occ = {}; occ[kk(start.x, start.y)] = 1;
    var gl = { x: x0 + 2 + rng.int(x1 - x0 - 3), y: y1 };
    occ[kk(gl.x, gl.y)] = 1; occ[kk(entrance.x, entrance.y)] = 1;
    function man(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); }
    var arenaTiles = [], x, y;
    for (y = y0; y <= y1; y++) for (x = x0; x <= x1; x++) arenaTiles.push({ x: x, y: y });
    function fr(tl) { return !occ[kk(tl.x, tl.y)]; }
    var bc = rng.shuffle(arenaTiles.filter(function (tl) {
      return fr(tl) && tl.x > x0 && tl.x < x1 && tl.y > y0 && tl.y < y1 && man(tl, gl) >= 2;
    }));
    if (bc.length < 3) return null;
    var braziers = bc.slice(0, 3);
    braziers.forEach(function (b) { occ[kk(b.x, b.y)] = 1; });
    var cc = rng.shuffle(arenaTiles.filter(function (tl) { return fr(tl) && man(tl, entrance) >= 4 && man(tl, gl) >= 3; }));
    if (cc.length < 3) return null;
    var spawns = [{ type: 'gloom', x: gl.x, y: gl.y }];
    ['shade', 'shade', 'hound'].forEach(function (type, i) { spawns.push({ type: type, x: cc[i].x, y: cc[i].y }); });
    cc.slice(0, 3).forEach(function (tl) { occ[kk(tl.x, tl.y)] = 1; });
    var srt = [];
    for (y = 12; y <= 16; y++) for (x = 1; x <= 5; x++) srt.push({ x: x, y: y });
    var salve = rng.pick(srt.filter(fr)); occ[kk(salve.x, salve.y)] = 1;
    var oil = rng.pick(arenaTiles.filter(fr));
    gr[start.y][start.x] = '<';
    braziers.forEach(function (b) { gr[b.y][b.x] = 'B'; });
    return {
      w: w, h: h, tiles: joinTiles(gr), start: start, stairsDown: null,
      braziers: braziers.map(function (b) { return { x: b.x, y: b.y }; }),
      items: [{ x: salve.x, y: salve.y, type: 'salve' }, { x: oil.x, y: oil.y, type: 'oil' }],
      creatureSpawns: spawns, rooms: [],
      arena: { x0: x0, y0: y0, x1: x1, y1: y1, entrance: entrance }
    };
  }

  // Returns the list of violated guarantees (spec 5); empty = valid.
  function validateFloor(f, n) {
    var errs = [], size = SIZES[n], w = f.w, h = f.h, x, y, i;
    if (w !== size[0] || h !== size[1]) errs.push('size ' + w + 'x' + h + ' != ' + size.join('x'));
    if (f.tiles.length !== h) { errs.push('tile rows != h'); return errs; }
    for (y = 0; y < h; y++) if (f.tiles[y].length !== w) { errs.push('row ' + y + ' width'); return errs; }
    var dS = bfs(f, f.start.x, f.start.y);
    if (f.tiles[f.start.y].charAt(f.start.x) !== '<') errs.push('start is not <');
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      if (f.tiles[y].charAt(x) !== '#' && !isFinite(dS[y * w + x])) { errs.push('disconnected tile ' + x + ',' + y); y = h; break; }
    }
    var cnt = {};
    f.creatureSpawns.forEach(function (c) { cnt[c.type] = (cnt[c.type] || 0) + 1; });
    ['gloom', 'moth', 'shade', 'hound'].forEach(function (t) {
      if ((cnt[t] || 0) !== (COUNTS[n][t] || 0)) errs.push('creature count ' + t + ' ' + (cnt[t] || 0));
    });
    if (f.braziers.length !== (n < 5 ? 2 : 3)) errs.push('brazier count ' + f.braziers.length);
    f.braziers.forEach(function (b) { if (f.tiles[b.y].charAt(b.x) !== 'B') errs.push('brazier tile char'); });
    var sal = 0, oil = 0;
    f.items.forEach(function (it) {
      if (it.type === 'salve') sal++; else if (it.type === 'oil') oil++;
      if (f.tiles[it.y].charAt(it.x) !== '.') errs.push('item not on plain floor');
    });
    if (sal !== 1 || oil !== 1 || f.items.length !== 2) errs.push('item counts');
    var seen = {};
    f.items.forEach(function (it) { seen[kk(it.x, it.y)] = 1; });
    f.creatureSpawns.forEach(function (c) {
      if (f.tiles[c.y].charAt(c.x) !== '.') errs.push('creature not on floor');
      if (seen[kk(c.x, c.y)]) errs.push('creature on item/creature ' + c.x + ',' + c.y);
      seen[kk(c.x, c.y)] = 1;
      if (!(dS[c.y * w + c.x] >= 6)) errs.push('creature within 6 steps of <');
    });
    if (n < 5) {
      if (!f.stairsDown || f.tiles[f.stairsDown.y].charAt(f.stairsDown.x) !== '>') { errs.push('no >'); return errs; }
      var D = dS[f.stairsDown.y * w + f.stairsDown.x];
      if (!(D >= MIN_STAIRS[n])) errs.push('< to > distance ' + D + ' < ' + MIN_STAIRS[n]);
      var dG = bfs(f, f.stairsDown.x, f.stairsDown.y);
      var near = f.braziers.some(function (b) { return dS[b.y * w + b.x] <= 25; });
      if (!near) errs.push('no brazier within 25 steps of <');
      var dB = bfs(f, f.braziers[0].x, f.braziers[0].y);
      if (!(dB[f.braziers[1].y * w + f.braziers[1].x] >= 10)) errs.push('braziers closer than 10 steps');
      f.braziers.forEach(function (b) {
        if (dS[b.y * w + b.x] + dG[b.y * w + b.x] === D) errs.push('brazier on a shortest path');
      });
      var offItem = f.items.some(function (it) { return dS[it.y * w + it.x] + dG[it.y * w + it.x] !== D; });
      if (!offItem) errs.push('no item off the shortest path');
      if (!f.rooms || f.rooms.length < 5 || f.rooms.length > 8) errs.push('room count');
    } else {
      if (f.stairsDown) errs.push('floor 5 has >');
      var a = f.arena;
      if (!a) { errs.push('no arena'); return errs; }
      if (a.x1 - a.x0 + 1 < 14 || a.y1 - a.y0 + 1 < 10) errs.push('arena smaller than 14x10');
      if (!(dS[a.entrance.y * w + a.entrance.x] >= 20)) errs.push('arena entrance < 20 steps from <');
      f.braziers.forEach(function (b) {
        if (b.x < a.x0 || b.x > a.x1 || b.y < a.y0 || b.y > a.y1) errs.push('brazier outside arena');
      });
      var dE = bfs(f, a.entrance.x, a.entrance.y);
      f.creatureSpawns.forEach(function (c) {
        if (c.type !== 'gloom') return;
        if (c.x < a.x0 || c.x > a.x1 || c.y < a.y0 || c.y > a.y1) errs.push('Gloom outside arena');
        if (!(dE[c.y * w + c.x] >= 8)) errs.push('Gloom < 8 steps from arena entrance');
      });
    }
    return errs;
  }

  function generateFloor(seed, n) {
    for (var k = 0; k < MAX_ATTEMPTS; k++) {
      var rng = EH.rng.make(seed, n, k);
      var f = n === 5 ? genBoss(rng) : genRegular(rng, n);
      if (!f) continue;
      if (validateFloor(f, n).length === 0) { f.attempt = k; return f; }
    }
    throw new Error('floorgen: no valid floor for seed "' + seed + '" floor ' + n + ' after ' + MAX_ATTEMPTS + ' attempts');
  }

  EH.floorgen = { generateFloor: generateFloor, validateFloor: validateFloor, bfs: bfs, SIZES: SIZES, COUNTS: COUNTS };
  if (typeof module === 'object' && module.exports) module.exports = EH.floorgen;
})(typeof globalThis !== 'undefined' ? globalThis : this);
