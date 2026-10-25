/* Seeded randomness for floor generation only (no randomness during play). UMD-style, D-001. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  // FNV-1a 32-bit string hash.
  function hash(str) {
    var h = 2166136261 >>> 0;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    return h >>> 0;
  }

  function mulberry32(a) {
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Sub-seeded generator: a pure function of (seed, floor, attempt).
  function make(seed, floor, attempt) {
    var next = mulberry32(hash(String(seed) + '|' + floor + '|' + attempt));
    var r = {
      next: next,
      int: function (n) { return Math.floor(next() * n); },
      pick: function (arr) { return arr[r.int(arr.length)]; },
      shuffle: function (arr) {
        var a = arr.slice();
        for (var i = a.length - 1; i > 0; i--) {
          var j = r.int(i + 1), t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
      }
    };
    return r;
  }

  EH.rng = { hash: hash, make: make };
  if (typeof module === 'object' && module.exports) module.exports = EH.rng;
})(typeof globalThis !== 'undefined' ? globalThis : this);
