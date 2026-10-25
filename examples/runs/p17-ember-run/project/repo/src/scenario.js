/* Hand-made states for tests. Rows: # wall, . floor, @ player, < > stairs, B brazier,
   m s h G creatures (ids in row-major order), + salve, o oil. UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') require('./game.js');
  var G = EH.game;
  var TYPES = { m: 'moth', s: 'shade', h: 'hound', G: 'gloom' };

  function fromAscii(rows, opts) {
    opts = opts || {};
    var h = rows.length, w = rows[0].length, tiles = [], spawns = [], items = [], braziers = [], start = null, stairs = null;
    for (var y = 0; y < h; y++) {
      var line = '';
      for (var x = 0; x < w; x++) {
        var ch = rows[y].charAt(x) || '#', t = '.';
        if (ch === '#' || ch === ' ') t = '#';
        else if (ch === '@') start = { x: x, y: y };
        else if (ch === '<') { t = '<'; if (!start) start = { x: x, y: y }; }
        else if (ch === '>') { t = '>'; stairs = { x: x, y: y }; }
        else if (ch === 'B') { t = 'B'; braziers.push({ x: x, y: y }); }
        else if (TYPES[ch]) spawns.push({ type: TYPES[ch], x: x, y: y });
        else if (ch === '+') items.push({ x: x, y: y, type: 'salve' });
        else if (ch === 'o') items.push({ x: x, y: y, type: 'oil' });
        line += t;
      }
      tiles.push(line);
    }
    var fd = { w: w, h: h, tiles: tiles, start: start, stairsDown: stairs, braziers: braziers, items: items,
      creatureSpawns: spawns, rooms: [], arena: opts.arena || { x0: 1, y0: 1, x1: w - 2, y1: h - 2 } };
    var s = G.newRunFromFloor(opts.seed || 'scenario', fd, opts.floor || 1);
    if (opts.ember !== undefined) s.ember = opts.ember;
    if (opts.hp !== undefined) s.hp = opts.hp;
    if (opts.inv) s.inv = opts.inv.slice();
    if (opts.lit) opts.lit.forEach(function (p) { s.lit.push(p[0] + ',' + p[1]); });
    G.updateSeen(s);
    return s;
  }

  EH.scenario = { fromAscii: fromAscii };
  if (typeof module === 'object' && module.exports) module.exports = EH.scenario;
})(typeof globalThis !== 'undefined' ? globalThis : this);
