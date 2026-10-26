'use strict';
// Shared helpers for the picture tests: a recording fake 2D context, and the mark-set comparison (criterion 45).

function fakeCtx() {
  const rec = { fills: [], pts: [], ops: [] };
  let cur = null;
  const bb = (ps) => {
    const xs = ps.map((p) => p[0]), ys = ps.map((p) => p[1]);
    return { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) };
  };
  const ctx = {
    fillStyle: '',
    fillRect(x, y, w, h) {
      rec.ops.push(['r', x, y, w, h].join());
      rec.fills.push({ color: ctx.fillStyle, area: Math.abs(w * h) });
      rec.pts.push([x, y], [x + w, y + h]);
    },
    beginPath() { cur = []; rec.ops.push('b'); },
    moveTo(x, y) { cur.push([x, y]); rec.pts.push([x, y]); rec.ops.push(['m', x, y].join()); },
    lineTo(x, y) { cur.push([x, y]); rec.pts.push([x, y]); rec.ops.push(['l', x, y].join()); },
    closePath() { rec.ops.push('z'); },
    arc(x, y, r) {
      cur.push([x - r, y - r], [x + r, y + r]); rec.pts.push([x - r, y - r], [x + r, y + r]);
      rec.ops.push(['a', x, y, r].join());
    },
    fill() {
      const b = bb(cur);
      rec.fills.push({ color: ctx.fillStyle, area: (b.x1 - b.x0) * (b.y1 - b.y0) });
      rec.ops.push('f');
    }
  };
  rec.ctx = ctx;
  rec.bbox = () => bb(rec.pts);
  return rec;
}

// Marks the page draws, from the same view fields page.js uses.
function pageMarks(v) {
  const threatTiles = new Set(), reachTiles = new Set(), threatCreatures = new Set();
  v.cells.forEach((row, y) => row.forEach((c, x) => { if (c.seen && c.threat) threatTiles.add(x + ',' + y); }));
  v.reach.forEach((rc) => reachTiles.add(rc.x + ',' + rc.y));
  v.creatures.forEach((c) => { if (c.threat) threatCreatures.add(c.id); });
  return { threatTiles, reachTiles, threatCreatures };
}

// Marks in the text frame.
function textMarks(v, renderFrame) {
  const lines = renderFrame(v).split('\n');
  const rows = lines.slice(4, 4 + v.h);
  const threatTiles = new Set(), reachTiles = new Set(), chars = {};
  rows.forEach((r, y) => {
    for (let x = 0; x < v.w; x++) {
      const ch = r.charAt(x) || ' ';
      chars[x + ',' + y] = ch;
      if (ch === '!') threatTiles.add(x + ',' + y);
      if (ch === '?') reachTiles.add(x + ',' + y);
    }
  });
  const threatCreatures = new Set();
  lines.forEach((l) => { const m = /^ {2}! .#(\d+) /.exec(l); if (m) threatCreatures.add(Number(m[1])); });
  const dl = lines.find((l) => l.startsWith('Danger: ')) || '';
  const danger = [];
  const re = /([NESW]) \(([^)]*)\)/g;
  let m;
  while ((m = re.exec(dl))) danger.push(m[1] + ':' + m[2].replace(/[ ,]/g, ''));
  return { threatTiles, reachTiles, threatCreatures, chars, danger };
}

// Returns a list of problems (empty = page and text mark the same things).
function compareMarks(v, renderFrame) {
  const pg = pageMarks(v), tx = textMarks(v, renderFrame), bad = [];
  const hidden = (k) => ['.', ',', ' '].indexOf(tx.chars[k]) >= 0; // a mark tile the text would show as plain floor
  tx.threatTiles.forEach((k) => { if (!pg.threatTiles.has(k)) bad.push('text ! not on page: ' + k); });
  pg.threatTiles.forEach((k) => { if (!tx.threatTiles.has(k) && hidden(k)) bad.push('page threat tile missing in text: ' + k); });
  tx.reachTiles.forEach((k) => { if (!pg.reachTiles.has(k)) bad.push('text ? not on page: ' + k); });
  pg.reachTiles.forEach((k) => { if (!tx.reachTiles.has(k) && hidden(k)) bad.push('page reach tile missing in text: ' + k); });
  const a = [...pg.threatCreatures].sort().join(), b = [...tx.threatCreatures].sort().join();
  if (a !== b) bad.push('threat creatures differ: page [' + a + '] text [' + b + ']');
  const pd = v.reach.map((rc) => rc.dir + ':' + rc.creatures.map((c) => c.letter).join('')).join('|');
  if (pd !== tx.danger.join('|')) bad.push('Danger differs: page ' + pd + ' text ' + tx.danger.join('|'));
  return bad;
}

module.exports = { fakeCtx, pageMarks, textMarks, compareMarks };
