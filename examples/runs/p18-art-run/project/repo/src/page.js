/* Browser page. Calls only newRun, step and view from the shared rules; no rule logic here (D-001).
   Pictures come from scene.js (mapping) and pictures.js (drawing); marks are drawn here from view fields only.
   This is the only file that may use window/document/Math.random. */
(function () {
  'use strict';
  var EH = window.EmberHollow, G = EH.game, V = EH.view, SCN = EH.scene, P = EH.pictures;
  var TILE = 28, BORDER = 3;
  var CHIP = '#150f22';
  var state = null, seed = '';
  var canvas = document.getElementById('board'), ctx = canvas.getContext('2d');

  function $(id) { return document.getElementById(id); }

  function start(newSeed) {
    try {
      seed = String(newSeed);
      state = G.newRun(seed);
      $('err').textContent = '';
      render();
    } catch (e) { $('err').textContent = 'Could not start: ' + e.message; }
  }
  function randomSeed() { return 'ember-' + Math.floor(Math.random() * 1000000000); }

  function act(a) {
    if (!state) return;
    state = G.step(state, a).state;
    render();
  }

  function glyph(ch, x, y, color, alpha) {
    ctx.globalAlpha = alpha;
    ctx.fillStyle = color;
    ctx.fillText(ch, x * TILE + TILE / 2, y * TILE + TILE / 2 + 1);
    ctx.globalAlpha = 1;
  }

  // Dark chip in the top-left corner inside the 3 px border, with one character centered in it (D-005 item 3).
  function chip(x, y, ch, color) {
    ctx.globalAlpha = 0.9; ctx.fillStyle = CHIP;
    ctx.fillRect(x * TILE + BORDER, y * TILE + BORDER, 8, 11);
    ctx.globalAlpha = 1;
    ctx.font = 'bold 10px monospace'; ctx.fillStyle = color;
    ctx.fillText(ch, x * TILE + BORDER + 4, y * TILE + BORDER + 6);
  }

  // Threat border: 3 px, on the tile edge.
  function threatBorder(x, y) {
    ctx.strokeStyle = '#ff3030'; ctx.lineWidth = BORDER;
    ctx.strokeRect(x * TILE + BORDER / 2, y * TILE + BORDER / 2, TILE - 1 - BORDER, TILE - 1 - BORDER);
  }

  function render() {
    var v = V.view(state), sc = SCN.build(v), x, y;
    canvas.width = v.w * TILE; canvas.height = v.h * TILE;
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = 'bold 10px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';

    // 1. terrain picture, then item / brazier / stairs picture
    sc.tiles.forEach(function (t) {
      P.draw(ctx, t.base, t.x * TILE, t.y * TILE, TILE, t.tone);
      if (t.object) P.draw(ctx, t.object, t.x * TILE, t.y * TILE, TILE, t.tone);
    });
    // 2. area marks (hound line, Gloom 3x3): red tint and border, from cell.threat
    for (y = 0; y < v.h; y++) for (x = 0; x < v.w; x++) {
      var c = v.cells[y][x];
      if (!c.seen) continue;
      if (c.threat) {
        ctx.fillStyle = 'rgba(255,40,40,0.35)'; ctx.fillRect(x * TILE, y * TILE, TILE - 1, TILE - 1);
        threatBorder(x, y);
      }
    }
    // 3. reach marks: dashed orange tile with the creature letters (unchanged)
    v.reach.forEach(function (rc) {
      ctx.fillStyle = 'rgba(255,170,0,0.30)'; ctx.fillRect(rc.x * TILE, rc.y * TILE, TILE - 1, TILE - 1);
      ctx.strokeStyle = '#ffb000'; ctx.lineWidth = 2; ctx.setLineDash([4, 3]);
      ctx.strokeRect(rc.x * TILE + 1, rc.y * TILE + 1, TILE - 3, TILE - 3); ctx.setLineDash([]);
      var letters = rc.creatures.map(function (cc) { return cc.letter; }).join(''), n = letters.length;
      var bw = Math.min(TILE - 6, n >= 3 ? n * 5.5 + 4 : n * 6 + 4);
      ctx.globalAlpha = 0.85; ctx.fillStyle = CHIP;
      ctx.fillRect(rc.x * TILE + (TILE - bw) / 2, rc.y * TILE + (TILE - 12) / 2, bw, 12);
      ctx.globalAlpha = 1;
      ctx.font = 'bold ' + (n >= 3 ? 9 : 10) + 'px monospace';
      glyph(letters, rc.x, rc.y, '#ffd070', 1);
    });
    // 4. creatures and the player (always full tone); stunned/staggered get a pale-blue wash and a badge
    sc.actors.forEach(function (a) {
      P.draw(ctx, a.picture, a.x * TILE, a.y * TILE, TILE, 'full', a.picture === 'player' ? { flame: sc.flame } : null);
      if (a.wash) {
        ctx.fillStyle = 'rgba(150,200,255,0.45)';
        ctx.fillRect(a.x * TILE + 4, a.y * TILE + 4, TILE - 9, TILE - 9);
        chip(a.x, a.y, a.state === 'stunned' ? 'z' : '~', '#cfe6ff');
      }
    });
    // 5. threat border and badge on creatures that can hurt at their next action
    v.creatures.forEach(function (cr) {
      if (cr.threat) {
        threatBorder(cr.x, cr.y);
        chip(cr.x, cr.y, '!', '#ff4040');
      }
    });

    $('floorline').textContent = 'Floor ' + v.floor + '/' + v.floors + '   Turn ' + v.turn;
    $('hpline').textContent = 'HP ' + v.hp + '/' + v.maxHp;
    $('emfill').style.width = v.ember + '%';
    $('emtext').textContent = v.ember + '/100  r=' + v.radius + '  dims ' + v.dim + '/turn';
    $('seedtext').textContent = v.seed;
    var inv = $('inv'); inv.innerHTML = '';
    v.inv.forEach(function (it, i) {
      var b = document.createElement('button');
      if (it) {
        var ic = document.createElement('canvas');
        ic.width = 24; ic.height = 24; ic.style.border = 'none'; ic.style.verticalAlign = 'middle'; ic.style.marginRight = '4px';
        P.draw(ic.getContext('2d'), it, 0, 0, 24, 'full');
        b.appendChild(ic);
      }
      b.appendChild(document.createTextNode('[' + (i + 1) + '] ' + (it || 'empty')));
      b.onclick = function () { act({ type: 'use', slot: i + 1 }); };
      inv.appendChild(b);
    });
    var msgs = $('msgs'); msgs.innerHTML = '';
    v.messages.forEach(function (m) { var d = document.createElement('div'); d.textContent = m; msgs.appendChild(d); });
    $('threats').innerHTML = '';
    if (v.creatures.length) {
      var t = document.createElement('div');
      t.textContent = 'In sight: ' + v.creatures.map(function (cc) {
        return cc.letter + ' ' + cc.hp + '/' + cc.maxHp + ' ' + cc.state + (cc.threat ? ' !' : '');
      }).join(' | ');
      $('threats').appendChild(t);
    }
    var dg = document.createElement('div');
    dg.textContent = 'Danger: ' + (v.reach.length ? v.reach.map(function (rc) {
      return rc.dir + ' (' + rc.creatures.map(function (cc) { return cc.letter; }).join(', ') + ')';
    }).join(', ') : 'none');
    $('threats').appendChild(dg);
    var sm = $('summary');
    if (v.end) {
      var e = v.end, label = { victory: 'Victory', dead: 'Dead', ember: 'Ember out' }[e.result];
      $('summarybox').innerHTML = '<h2></h2><div id="sf"></div><div style="margin-top:12px"><button id="s1">Same seed (R)</button><button id="s2">New seed (N)</button></div>';
      $('summarybox').querySelector('h2').textContent = label + ': ' + e.message;
      $('sf').innerHTML = ['Floor reached: ' + e.floor + '/' + v.floors, 'Turns: ' + e.turns, 'Creatures defeated: ' + e.defeated,
        'Final HP: ' + e.hp + '/' + v.maxHp, 'Final ember: ' + e.ember, 'Seed: ' + e.seed].join('<br>');
      $('s1').onclick = function () { start(seed); };
      $('s2').onclick = function () { start(randomSeed()); };
      sm.style.display = 'flex';
    } else sm.style.display = 'none';
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.target && ev.target.tagName === 'INPUT') { if (ev.key === 'Enter') $('seedgo').click(); return; }
    var k = ev.key, a = null;
    if (k === 'ArrowUp' || k === 'w' || k === 'W') a = { type: 'move', dir: 'N' };
    else if (k === 'ArrowDown' || k === 's' || k === 'S') a = { type: 'move', dir: 'S' };
    else if (k === 'ArrowLeft' || k === 'a' || k === 'A') a = { type: 'move', dir: 'W' };
    else if (k === 'ArrowRight' || k === 'd' || k === 'D') a = { type: 'move', dir: 'E' };
    else if (k === '.' || k === ' ') a = { type: 'wait' };
    else if (k >= '1' && k <= '4') a = { type: 'use', slot: parseInt(k, 10) };
    else if (k === 'r' || k === 'R') { start(seed); ev.preventDefault(); return; }
    else if (k === 'n' || k === 'N') { start(randomSeed()); ev.preventDefault(); return; }
    if (a) { ev.preventDefault(); act(a); }
  });

  canvas.addEventListener('click', function (ev) {
    if (!state) return;
    var rect = canvas.getBoundingClientRect();
    var x = Math.floor((ev.clientX - rect.left) * (canvas.width / rect.width) / TILE);
    var y = Math.floor((ev.clientY - rect.top) * (canvas.height / rect.height) / TILE);
    var dx = x - state.player.x, dy = y - state.player.y;
    if (Math.abs(dx) + Math.abs(dy) !== 1) return;
    act({ type: 'move', dir: dy < 0 ? 'N' : dy > 0 ? 'S' : dx > 0 ? 'E' : 'W' });
  });

  $('waitbtn').onclick = function () { act({ type: 'wait' }); };
  $('restartbtn').onclick = function () { start(seed); };
  $('newbtn').onclick = function () { start(randomSeed()); };
  $('seedgo').onclick = function () { var t = $('seedinput').value.trim(); if (t) start(t); };

  var fromHash = location.hash.length > 1 ? decodeURIComponent(location.hash.slice(1)) : '';
  start(fromHash || randomSeed());
})();
