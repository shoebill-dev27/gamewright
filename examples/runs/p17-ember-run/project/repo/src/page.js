/* Browser page. Calls only newRun, step and view from the shared rules; no rule logic here (D-001).
   This is the only file that may use window/document/Math.random. */
(function () {
  'use strict';
  var EH = window.EmberHollow, G = EH.game, V = EH.view;
  var TILE = 22;
  var COLORS = { m: '#d9a0e0', s: '#8fb4ff', h: '#ff9050', G: '#ff40ff' };
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

  function render() {
    var v = V.view(state), x, y;
    canvas.width = v.w * TILE; canvas.height = v.h * TILE;
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = 'bold ' + (TILE - 6) + 'px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (y = 0; y < v.h; y++) for (x = 0; x < v.w; x++) {
      var c = v.cells[y][x];
      if (!c.seen) continue;
      var a = c.vis ? 1 : 0.38; // remembered tiles are clearly dimmer
      ctx.globalAlpha = a;
      if (c.terrain === 'wall') ctx.fillStyle = '#6b5842';
      else ctx.fillStyle = c.vis ? '#3a3026' : '#1f1a14';
      ctx.fillRect(x * TILE, y * TILE, TILE - 1, TILE - 1);
      ctx.globalAlpha = 1;
      if (c.terrain === 'up') glyph('<', x, y, '#9cf', a);
      else if (c.terrain === 'down') glyph('>', x, y, '#9f9', a);
      else if (c.terrain === 'brazier') glyph('B', x, y, '#7788aa', a);      // unlit: cold blue-grey
      else if (c.terrain === 'lit') { glyph('B', x, y, '#ffb030', a); }      // lit: warm orange
      if (c.item === 'salve') glyph('+', x, y, '#5f5', a);
      else if (c.item === 'oil') glyph('o', x, y, '#ee5', a);
      if (c.threat) {
        ctx.fillStyle = 'rgba(255,40,40,0.35)'; ctx.fillRect(x * TILE, y * TILE, TILE - 1, TILE - 1);
        ctx.strokeStyle = '#ff3030'; ctx.lineWidth = 2; ctx.strokeRect(x * TILE + 1, y * TILE + 1, TILE - 3, TILE - 3);
      }
    }
    v.reach.forEach(function (rc) { // reach marks: dashed orange tile with the creature letters (threat marks are red)
      ctx.fillStyle = 'rgba(255,170,0,0.30)'; ctx.fillRect(rc.x * TILE, rc.y * TILE, TILE - 1, TILE - 1);
      ctx.strokeStyle = '#ffb000'; ctx.lineWidth = 2; ctx.setLineDash([4, 3]);
      ctx.strokeRect(rc.x * TILE + 1, rc.y * TILE + 1, TILE - 3, TILE - 3); ctx.setLineDash([]);
      var big = ctx.font; ctx.font = 'bold 10px monospace';
      glyph(rc.creatures.map(function (c) { return c.letter; }).join(''), rc.x, rc.y, '#ffd070', 1);
      ctx.font = big;
    });
    v.creatures.forEach(function (cr) {
      glyph(cr.letter, cr.x, cr.y, COLORS[cr.type] || '#fff', cr.state === 'stunned' || cr.state === 'staggered' ? 0.55 : 1);
      if (cr.threat) {
        ctx.strokeStyle = '#ff3030'; ctx.lineWidth = 2;
        ctx.strokeRect(cr.x * TILE + 1, cr.y * TILE + 1, TILE - 3, TILE - 3);
        glyph('!', cr.x, cr.y - 0.55, '#ff4040', 1);
      }
    });
    glyph('@', v.player.x, v.player.y, '#ffffff', 1);

    $('floorline').textContent = 'Floor ' + v.floor + '/' + v.floors + '   Turn ' + v.turn;
    $('hpline').textContent = 'HP ' + v.hp + '/' + v.maxHp;
    $('emfill').style.width = v.ember + '%';
    $('emtext').textContent = v.ember + '/100  r=' + v.radius + '  dims ' + v.dim + '/turn';
    $('seedtext').textContent = v.seed;
    var inv = $('inv'); inv.innerHTML = '';
    v.inv.forEach(function (it, i) {
      var b = document.createElement('button');
      b.textContent = '[' + (i + 1) + '] ' + (it || 'empty');
      b.onclick = function () { act({ type: 'use', slot: i + 1 }); };
      inv.appendChild(b);
    });
    var msgs = $('msgs'); msgs.innerHTML = '';
    v.messages.forEach(function (m) { var d = document.createElement('div'); d.textContent = m; msgs.appendChild(d); });
    $('threats').innerHTML = '';
    if (v.creatures.length) {
      var t = document.createElement('div');
      t.textContent = 'In sight: ' + v.creatures.map(function (c) {
        return c.letter + ' ' + c.hp + '/' + c.maxHp + ' ' + c.state + (c.threat ? ' !' : '');
      }).join(' | ');
      $('threats').appendChild(t);
    }
    var dg = document.createElement('div');
    dg.textContent = 'Danger: ' + (v.reach.length ? v.reach.map(function (rc) {
      return rc.dir + ' (' + rc.creatures.map(function (c) { return c.letter; }).join(', ') + ')';
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
