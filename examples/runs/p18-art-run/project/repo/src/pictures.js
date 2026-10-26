/* Pictures drawn by code (D-004). Each picture is authored on a 16x16 grid and scaled to the tile.
   draw(ctx, name, px, py, size, tone, opts). UMD-style (D-001). Uses only a 2D context passed in. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  var BORDER = 3, TWO_PI = Math.PI * 2;

  // Fixed palette: 11 colors. No red, no orange. Warm gold belongs to the ember and lit braziers.
  var PAL = {
    floorA: '#332b22', floorB: '#40372c', wallA: '#54493c', wallB: '#6f6352',
    ash: '#8c8f99', violet: '#7566a8', pale: '#dfe3f0', gold: '#f0c640',
    green: '#58b868', blue: '#6f9fd0', night: '#150f22'
  };

  function hex2rgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function toHex(a) {
    return '#' + a.map(function (n) {
      n = Math.max(0, Math.min(255, Math.round(n)));
      return (n < 16 ? '0' : '') + n.toString(16);
    }).join('');
  }
  var dimCache = {};
  // Remembered palette: toward grey, darker. One place to tune.
  function dim(color) {
    if (dimCache[color]) return dimCache[color];
    var c = hex2rgb(color), gray = 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2];
    var out = toHex(c.map(function (v) { return (v * 0.45 + gray * 0.55) * 0.55; }));
    dimCache[color] = out;
    return out;
  }

  function kit(ctx, px, py, size, tone, bg, opts) {
    var inset = bg ? 0 : (opts && typeof opts.inset === 'number' ? opts.inset : Math.max(Math.round(0.1 * size), BORDER + 1));
    var span = bg ? size - 1 : size - 2 * inset, u = span / 16, ox = px + inset, oy = py + inset;
    function col(n) { return tone === 'dim' ? dim(PAL[n]) : PAL[n]; }
    return {
      r: function (n, x, y, w, h) { ctx.fillStyle = col(n); ctx.fillRect(ox + x * u, oy + y * u, w * u, h * u); },
      p: function (n, pts) {
        ctx.fillStyle = col(n); ctx.beginPath();
        ctx.moveTo(ox + pts[0][0] * u, oy + pts[0][1] * u);
        for (var i = 1; i < pts.length; i++) ctx.lineTo(ox + pts[i][0] * u, oy + pts[i][1] * u);
        ctx.closePath(); ctx.fill();
      },
      c: function (n, x, y, rad) {
        ctx.fillStyle = col(n); ctx.beginPath();
        ctx.arc(ox + x * u, oy + y * u, rad * u, 0, TWO_PI); ctx.fill();
      }
    };
  }

  // Flame: step 1..5 (r = 2..6). Grows in height and width.
  function flame(k, step, grow) {
    var cx = 11.5, cy = 7.5, h = 1.5 + step * 1.1, w = 0.8 + step * 0.5;
    if (grow) {
      h += grow; w += grow;
      k.p('night', [[cx, cy - h], [cx + w, cy - h * 0.25], [cx + w * 0.7, cy + 1 + grow], [cx - w * 0.7, cy + 1 + grow], [cx - w, cy - h * 0.25]]);
      return;
    }
    k.p('gold', [[cx, cy - h], [cx + w, cy - h * 0.25], [cx + w * 0.7, cy + 1], [cx - w * 0.7, cy + 1], [cx - w, cy - h * 0.25]]);
    if (step >= 2) k.p('pale', [[cx, cy - h * 0.55], [cx + w * 0.45, cy - h * 0.1], [cx + w * 0.3, cy + 0.8],
      [cx - w * 0.3, cy + 0.8], [cx - w * 0.45, cy - h * 0.1]]);
  }

  function bowl(k) {
    k.p('ash', [[3, 7], [13, 7], [11, 12], [5, 12]]);
    k.r('ash', 7, 12, 2, 3);
    k.r('ash', 4, 14, 8, 1.5);
    k.r('night', 4, 7, 8, 1);
  }

  var PIC = {
    wall: function (k) {
      k.r('wallA', 0, 0, 16, 16);
      [[1, 1, 6, 4], [9, 1, 6, 4], [0, 6, 3, 4], [5, 6, 6, 4], [13, 6, 3, 4], [1, 11, 6, 4], [9, 11, 6, 4]].forEach(function (b) {
        k.r('wallB', b[0], b[1], b[2], b[3]);
      });
    },
    floor: function (k) {
      k.r('floorA', 0, 0, 16, 16);
      [[3, 3, 2, 2], [10, 6, 2, 1], [6, 11, 3, 2], [13, 13, 1, 1]].forEach(function (b) { k.r('floorB', b[0], b[1], b[2], b[3]); });
    },
    'stairs-up': function (k) {
      k.r('blue', 1, 12, 3, 3); k.r('blue', 5, 8, 3, 7); k.r('blue', 9, 4, 3, 11); k.r('blue', 13, 1, 3, 14);
    },
    'stairs-down': function (k) {
      k.r('green', 1, 1, 3, 3); k.r('green', 5, 1, 3, 7); k.r('green', 9, 1, 3, 11); k.r('green', 13, 1, 3, 14);
    },
    brazier: function (k) { bowl(k); },
    'brazier-lit': function (k) {
      bowl(k);
      k.p('gold', [[8, 1], [12, 7], [4, 7]]);
      k.p('pale', [[8, 3.5], [10, 7], [6, 7]]);
    },
    salve: function (k) {
      k.r('green', 4, 6, 8, 8); k.r('pale', 5, 3, 6, 3);
      k.r('pale', 7, 8, 2, 4); k.r('pale', 6, 9, 4, 2);
    },
    oil: function (k) {
      k.r('blue', 7, 2, 2, 4); k.r('gold', 6, 1, 4, 2);
      k.p('blue', [[7, 6], [9, 6], [13, 10], [12, 15], [4, 15], [3, 10]]);
      k.r('pale', 5, 10, 1, 3);
    },
    moth: function (k) {
      k.p('pale', [[8, 8], [1, 2], [0.5, 9]]);
      k.p('pale', [[8, 8], [15, 2], [15.5, 9]]);
      k.p('pale', [[8, 9], [2, 13], [5, 15]]);
      k.p('pale', [[8, 9], [14, 13], [11, 15]]);
      k.r('ash', 7, 4, 2, 10); k.r('ash', 6, 2, 1, 3); k.r('ash', 9, 2, 1, 3);
    },
    shade: function (k) {
      k.p('violet', [[8, 0], [12, 4], [11, 11], [12.5, 15], [10, 13.5], [8, 15.5], [6, 13.5], [3.5, 15], [5, 11], [4, 4]]);
      k.r('pale', 6, 4, 1.5, 2); k.r('pale', 8.5, 4, 1.5, 2);
    },
    hound: function (k) {
      k.r('ash', 2, 6, 10, 5); k.r('ash', 2, 4, 5, 3); k.r('ash', 11, 4, 5, 4);
      k.p('ash', [[12, 4], [13, 2], [14, 4]]);
      [2, 5, 9, 12].forEach(function (lx) { k.r('ash', lx, 11, 2, 4); });
      k.p('ash', [[2, 6], [0, 4], [0.5, 7]]);
      k.r('gold', 13.5, 5, 1, 1);
    },
    'hound-crouch': function (k) {
      k.r('ash', 1, 9, 11, 4); k.r('ash', 2, 8, 4, 1.5); k.r('ash', 11, 10, 5, 3);
      k.p('ash', [[12, 10], [13, 8.5], [14, 10]]);
      k.r('ash', 2, 13, 3, 2); k.r('ash', 9, 13, 3, 2); k.r('ash', 13, 13, 2, 2);
      k.r('ash', 0, 10, 1.5, 1.5);
      k.r('gold', 13.5, 10.5, 1, 1);
    },
    gloom: function (k) {
      k.c('violet', 8, 8, 7); k.c('night', 8, 8, 5.5);
      [[0, 3, 4, 2], [12, 3, 4, 2], [0, 11, 4, 2], [12, 11, 4, 2], [3, 0, 2, 3], [11, 0, 2, 3], [3, 13, 2, 3], [11, 13, 2, 3]]
        .forEach(function (b) { k.r('night', b[0], b[1], b[2], b[3]); });
      k.r('pale', 5, 6, 2, 2); k.r('pale', 9, 6, 2, 2);
    },
    player: function (k, opts) {
      var fs = opts && opts.flame ? opts.flame : 3;
      // night outline: same shapes grown by 1 design unit (D-005 item 5)
      k.c('night', 5.5, 6, 3);
      k.p('night', [[5.5, 6.4], [10.8, 16.5], [0.2, 16.5]]);
      k.r('night', 10, 7.5, 3, 8.5);
      flame(k, fs, 1);
      k.c('pale', 5.5, 6, 2);
      k.p('blue', [[5.5, 8], [9.5, 15.5], [1.5, 15.5]]);
      k.r('ash', 11, 8.5, 1, 6.5);
      flame(k, fs);
    }
  };

  function draw(ctx, name, px, py, size, tone, opts) {
    var fn = PIC[name];
    if (!fn) throw new Error('unknown picture: ' + name);
    fn(kit(ctx, px, py, size, tone || 'full', name === 'wall' || name === 'floor', opts), opts || {});
  }

  function drawFlame(ctx, px, py, size, step, tone, opts) {
    flame(kit(ctx, px, py, size, tone || 'full', false, opts), step);
  }

  EH.pictures = { draw: draw, drawFlame: drawFlame, dim: dim, PALETTE: PAL, NAMES: Object.keys(PIC), BORDER: BORDER };
  if (typeof module === 'object' && module.exports) module.exports = EH.pictures;
})(typeof globalThis !== 'undefined' ? globalThis : this);
