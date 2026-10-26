/* Glow radius and visibility (spec 3). UMD-style, D-001. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  // Spec 3 table.
  function radiusFor(E) {
    if (E >= 80) return 6;
    if (E >= 60) return 5;
    if (E >= 40) return 4;
    if (E >= 20) return 3;
    if (E >= 1) return 2;
    return 0;
  }

  function tileAt(fd, x, y) {
    if (x < 0 || y < 0 || x >= fd.w || y >= fd.h) return '#';
    return fd.tiles[y].charAt(x);
  }

  // Bresenham line; intermediate tiles (not the endpoints) must not be walls.
  function los(fd, x0, y0, x1, y1) {
    var dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
    var sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    var err = dx - dy, x = x0, y = y0;
    for (;;) {
      if (x === x1 && y === y1) return true;
      var e2 = 2 * err;
      if (e2 > -dy) { err -= dy; x += sx; }
      if (e2 < dx) { err += dx; y += sy; }
      if (x === x1 && y === y1) return true;
      if (tileAt(fd, x, y) === '#') return false;
    }
  }

  // Grid (w*h array of 0/1) of tiles visible from (px,py) with glow radius r:
  // dx^2+dy^2 <= (r+0.5)^2 and a clear line of sight.
  function visibleGrid(fd, px, py, r) {
    var w = fd.w, h = fd.h, grid = new Array(w * h);
    for (var i = 0; i < grid.length; i++) grid[i] = 0;
    var R = r + 0.5, R2 = R * R, m = Math.ceil(R);
    for (var y = py - m; y <= py + m; y++) {
      for (var x = px - m; x <= px + m; x++) {
        if (x < 0 || y < 0 || x >= w || y >= h) continue;
        var dx = x - px, dy = y - py;
        if (dx * dx + dy * dy > R2) continue;
        if (los(fd, px, py, x, y)) grid[y * w + x] = 1;
      }
    }
    grid[py * w + px] = 1;
    return grid;
  }

  EH.light = { radiusFor: radiusFor, tileAt: tileAt, los: los, visibleGrid: visibleGrid };
  if (typeof module === 'object' && module.exports) module.exports = EH.light;
})(typeof globalThis !== 'undefined' ? globalThis : this);
