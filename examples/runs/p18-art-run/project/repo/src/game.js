/* Ember Hollow rules engine: pure, deterministic. One entry point step(state, action).
   UMD-style (D-001). No Date, no Math.random, no DOM. Spec section numbers in comments. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./rng.js'); require('./floorgen.js'); require('./light.js'); }
  var FG = EH.floorgen, L = EH.light;

  var DIRS = { N: [0, -1], E: [1, 0], S: [0, 1], W: [-1, 0] };
  var DIR_ORDER = ['N', 'E', 'S', 'W'];
  var DEFS = {
    moth: { letter: 'm', name: 'Cave moth', hp: 2, dmg: 1 },
    shade: { letter: 's', name: 'Shade', hp: 4, dmg: 2 },
    hound: { letter: 'h', name: 'Ash hound', hp: 4, dmg: 3 },
    gloom: { letter: 'G', name: 'The Gloom', hp: 24, dmg: 4 }
  };
  var MAX_HP = 12, FLOORS = 5;
  // Spec 3 (flare): "skips its next 2 actions". Reading A: the creature phase of the lighting turn
  // already counts as the first skipped action (see manual.md, readings).
  var STUN_TURNS = 2;

  function manh(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); }
  function key(x, y) { return x + ',' + y; }
  function tileAt(fd, x, y) { return L.tileAt(fd, x, y); }
  function addMsg(s, t) { s.messages.push(t); if (s.messages.length > 5) s.messages.splice(0, s.messages.length - 5); }
  function nm(c) { return c.type === 'gloom' ? 'Gloom' : 'the ' + DEFS[c.type].name.toLowerCase(); }
  function cap(t) { return t.charAt(0).toUpperCase() + t.slice(1); }

  // Copy of the state; floorData is immutable and shared.
  function clone(s) {
    var c = {};
    Object.keys(s).forEach(function (k) {
      if (k === 'floorData' || s[k] === undefined) c[k] = s[k];
      else c[k] = JSON.parse(JSON.stringify(s[k]));
    });
    return c;
  }

  function creatureAt(s, x, y) {
    for (var i = 0; i < s.creatures.length; i++) {
      var c = s.creatures[i];
      if (c.hp > 0 && c.x === x && c.y === y) return c;
    }
    return null;
  }

  function makeCreature(sp, id) {
    return { id: id, type: sp.type, x: sp.x, y: sp.y, hp: DEFS[sp.type].hp, maxHp: DEFS[sp.type].hp,
      stunned: 0, crouching: false, dir: null, staggered: 0, gathering: false };
  }

  function emptySeen(fd) {
    var a = [];
    for (var y = 0; y < fd.h; y++) { var r = []; for (var x = 0; x < fd.w; x++) r.push(0); a.push(r); }
    return a;
  }

  function updateSeen(s) {
    if (s.ember <= 0) return;
    var fd = s.floorData;
    var vis = L.visibleGrid(fd, s.player.x, s.player.y, L.radiusFor(s.ember));
    for (var y = 0; y < fd.h; y++) for (var x = 0; x < fd.w; x++) if (vis[y * fd.w + x]) s.seen[y][x] = 1;
  }

  function installFloor(s, fd, n) {
    s.floor = n; s.floorData = fd;
    s.player = { x: fd.start.x, y: fd.start.y };
    s.lit = [];
    s.items = fd.items.map(function (i) { return { x: i.x, y: i.y, type: i.type }; });
    s.creatures = fd.creatureSpawns.map(function (sp, i) { return makeCreature(sp, i + 1); });
    s.seen = emptySeen(fd);
    updateSeen(s);
  }

  function newRunFromFloor(seed, fd, n) {
    var s = { seed: String(seed), floor: n, turn: 0, hp: MAX_HP, ember: 100, inv: [null, null, null, null],
      player: null, floorData: null, lit: [], items: [], seen: null, creatures: [], messages: [], end: null, defeated: 0 };
    installFloor(s, fd, n);
    addMsg(s, 'You descend into Ember Hollow with one ember.');
    return s;
  }

  function newRun(seed) { return newRunFromFloor(seed, FG.generateFloor(String(seed), 1), 1); }

  function bfsFromPlayer(s) { return FG.bfs(s.floorData, s.player.x, s.player.y); }
  function makeCtx(s) {
    var r = L.radiusFor(s.ember);
    return { dist: bfsFromPlayer(s), vis: L.visibleGrid(s.floorData, s.player.x, s.player.y, r), r: r };
  }

  // Spec 3/7: extra drain while the Gloom is within Manhattan 4 (measured at the player's position
  // after the player's action).
  function drainRate(s) {
    for (var i = 0; i < s.creatures.length; i++) {
      var c = s.creatures[i];
      if (c.type === 'gloom' && c.hp > 0 && manh(c, s.player) <= 4) return 2;
    }
    return 1;
  }

  // ---- creature planning (one planner for actions AND threat marks) ----

  function isFree(s, x, y) {
    if (tileAt(s.floorData, x, y) !== '.') return false; // creatures never enter walls, braziers, stairs
    if (s.player.x === x && s.player.y === y) return false;
    return !creatureAt(s, x, y);
  }

  // Spec 4: one step along a shortest path (ties N,E,S,W). Path distance ignores creatures;
  // the step itself needs a free tile.
  function stepToward(s, c, ctx, inRegion) {
    var w = s.floorData.w, d = ctx.dist[c.y * w + c.x];
    if (!isFinite(d)) return null;
    for (var i = 0; i < 4; i++) {
      var dv = DIRS[DIR_ORDER[i]], nx = c.x + dv[0], ny = c.y + dv[1];
      if (!isFree(s, nx, ny)) continue;
      if (inRegion && !inRegion(nx, ny)) continue;
      if (ctx.dist[ny * w + nx] === d - 1) return { x: nx, y: ny };
    }
    return null;
  }

  // Spec 4 (shade): a step that increases path distance from the player.
  function stepAway(s, c, ctx) {
    var w = s.floorData.w, d = ctx.dist[c.y * w + c.x];
    if (!isFinite(d)) return null;
    for (var i = 0; i < 4; i++) {
      var dv = DIRS[DIR_ORDER[i]], nx = c.x + dv[0], ny = c.y + dv[1];
      if (!isFree(s, nx, ny)) continue;
      if (ctx.dist[ny * w + nx] > d) return { x: nx, y: ny };
    }
    return null;
  }

  function dirKey(sx, sy) { return sy < 0 ? 'N' : sx > 0 ? 'E' : sy > 0 ? 'S' : 'W'; }
  function attackIntent(c, label) { return { kind: 'attack', label: label, damage: DEFS[c.type].dmg }; }

  function lineOf(s, c) { // spec 4: tiles of a crouching hound's lunge line
    var dv = DIRS[c.dir], out = [];
    for (var i = 1; i <= 2; i++) {
      var x = c.x + dv[0] * i, y = c.y + dv[1] * i;
      if (tileAt(s.floorData, x, y) !== '#') out.push({ x: x, y: y });
    }
    return out;
  }
  function areaOf(s, c) { // spec 7: 3x3 around the Gloom, diagonals included
    var out = [];
    for (var dy = -1; dy <= 1; dy++) for (var dx = -1; dx <= 1; dx++) {
      if (tileAt(s.floorData, c.x + dx, c.y + dy) !== '#') out.push({ x: c.x + dx, y: c.y + dy });
    }
    return out;
  }
  function inArena(fd, x, y) {
    var a = fd.arena;
    return !!a && x >= a.x0 && x <= a.x1 && y >= a.y0 && y <= a.y1;
  }

  // intent: idle | move{to} | attack{damage} | crouch{dir} | lunge{line} | gather | slam{area} | stunned | staggered
  function planAction(s, c, ctx) {
    if (c.stunned > 0) return { kind: 'stunned', label: 'stunned' };       // spec 3 flare
    if (c.staggered > 0) return { kind: 'staggered', label: 'staggered' }; // spec 7
    var fd = s.floorData, p = s.player, d = ctx.dist[c.y * fd.w + c.x];
    var adj = manh(c, p) === 1, to;
    switch (c.type) {
      case 'moth': // spec 4: drawn to light
        if (adj) return attackIntent(c, 'hunting');
        if (d <= ctx.r + 3) {
          to = stepToward(s, c, ctx);
          return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
        }
        return { kind: 'idle', label: 'idle' };
      case 'shade': // spec 4: fears bright light
        if (ctx.r >= 3) {
          if (ctx.vis[c.y * fd.w + c.x]) {
            to = stepAway(s, c, ctx);
            if (to) return { kind: 'move', to: to, label: 'fleeing' };
            if (adj) return attackIntent(c, 'cornered'); // cornered and adjacent
            return { kind: 'idle', label: 'cornered' };
          }
          if (d <= 12) {
            to = stepToward(s, c, ctx);
            return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
          }
          return { kind: 'idle', label: 'idle' };
        }
        if (adj) return attackIntent(c, 'hunting');
        if (isFinite(d)) {
          to = stepToward(s, c, ctx);
          if (to) return { kind: 'move', to: to, label: 'hunting' };
        }
        return { kind: 'idle', label: 'idle' };
      case 'hound': { // spec 4: bite, telegraphed lunge
        if (c.crouching) return { kind: 'lunge', label: 'crouching', dir: c.dir, line: lineOf(s, c) };
        if (adj) return attackIntent(c, 'hunting');
        var dx = p.x - c.x, dy = p.y - c.y;
        if ((dx === 0 && Math.abs(dy) === 2) || (dy === 0 && Math.abs(dx) === 2)) {
          var sx = dx === 0 ? 0 : (dx > 0 ? 1 : -1), sy = dy === 0 ? 0 : (dy > 0 ? 1 : -1);
          if (isFree(s, c.x + sx, c.y + sy)) return { kind: 'crouch', label: 'hunting', dir: dirKey(sx, sy) };
        }
        if (d <= 6) {
          to = stepToward(s, c, ctx);
          return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
        }
        return { kind: 'idle', label: 'idle' };
      }
      case 'gloom': // spec 7
        if (c.gathering) return { kind: 'slam', label: 'gathering', damage: 4, area: areaOf(s, c) };
        if (!inArena(fd, p.x, p.y)) return { kind: 'idle', label: 'idle' };
        if (manh(c, p) <= 2) return { kind: 'gather', label: 'hunting' };
        to = stepToward(s, c, ctx, function (x, y) { return inArena(fd, x, y); });
        return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
    }
    return { kind: 'idle', label: 'idle' };
  }

  function hurt(s, c, amount, ev) {
    s.hp = Math.max(0, s.hp - amount);
    addMsg(s, cap(nm(c)) + ' hits you for ' + amount + '.');
    ev.push({ t: 'damage', src: c.id, type: c.type, amount: amount, from: { x: c.x, y: c.y } });
  }

  function moveTo(c, to) { c.x = to.x; c.y = to.y; }

  // Spec 4 lunge: moves up to 2 tiles along the line; bites only if it ends adjacent with the player in the line.
  function doLunge(s, c, ctx, ev) {
    var dv = DIRS[c.dir], p = s.player, k = 0, i;
    for (i = 1; i <= 2; i++) if (p.x === c.x + dv[0] * i && p.y === c.y + dv[1] * i) k = i;
    c.crouching = false;
    if (k > 0) {
      for (i = 1; i < k; i++) {
        var nx = c.x + dv[0], ny = c.y + dv[1];
        if (isFree(s, nx, ny)) c.x = nx, c.y = ny; else break;
      }
      if (manh(c, p) === 1) hurt(s, c, 3, ev);
      else addMsg(s, 'The hound lunges but is blocked.');
    } else {
      for (i = 0; i < 2; i++) { var to = stepToward(s, c, ctx); if (!to) break; moveTo(c, to); }
      addMsg(s, 'The hound lunges and misses you.');
    }
  }

  function execute(s, c, it, ctx, ev) {
    switch (it.kind) {
      case 'stunned': c.stunned--; break;
      case 'staggered': c.staggered--; break;
      case 'move': moveTo(c, it.to); break;
      case 'attack': hurt(s, c, it.damage, ev); break;
      case 'crouch': c.crouching = true; c.dir = it.dir; addMsg(s, 'The hound crouches. Step out of its line!'); break;
      case 'lunge': doLunge(s, c, ctx, ev); break;
      case 'gather': c.gathering = true; addMsg(s, 'The Gloom gathers darkness around itself.'); break;
      case 'slam': {
        var p = s.player;
        if (Math.max(Math.abs(p.x - c.x), Math.abs(p.y - c.y)) <= 1) hurt(s, c, 4, ev);
        else addMsg(s, 'The Gloom slams the ground and misses you.');
        c.gathering = false; c.staggered = 3;
        addMsg(s, 'The Gloom staggers.');
        break;
      }
    }
  }

  // ---- end of run ----

  function endRun(s, result) {
    var msg = result === 'victory' ? 'The Gloom breaks. Light returns to the hollow.'
      : result === 'dead' ? 'You fell on floor ' + s.floor + '.'
        : 'The ember went out on floor ' + s.floor + '.';
    s.end = { result: result, message: msg, floor: s.floor, turns: s.turn, defeated: s.defeated, hp: s.hp, ember: s.ember, seed: s.seed };
    addMsg(s, msg);
  }

  function notifyEmber(s, before, after) { // spec 3 "Reading the ember"
    if (after <= 0) return;
    [20, 10, 5].forEach(function (t) { if (before > t && after <= t) addMsg(s, 'Ember low: ' + after + '.'); });
    if (L.radiusFor(before) > L.radiusFor(after)) addMsg(s, 'Your light shrinks.');
  }

  // Effects of arriving on a tile: brazier (spec 3), item pickup (spec 6), stairs.
  function landOn(s, ev) {
    var p = s.player, fd = s.floorData, t = tileAt(fd, p.x, p.y), k = key(p.x, p.y), i;
    if (t === 'B' && s.lit.indexOf(k) < 0) {
      s.lit.push(k);
      s.ember = Math.min(100, s.ember + 60); // before this turn's dimming
      addMsg(s, 'You rekindle the ember at the brazier (+60).');
      ev.push({ t: 'brazier', x: p.x, y: p.y });
      var vis = L.visibleGrid(fd, p.x, p.y, L.radiusFor(s.ember)), stunned = [];
      s.creatures.forEach(function (c) {
        if (c.type === 'gloom' || c.hp <= 0) return;
        if (manh(c, p) > 7 || !vis[c.y * fd.w + c.x]) return;
        c.stunned = STUN_TURNS; c.crouching = false; c.dir = null; stunned.push(c.id);
      });
      if (stunned.length) {
        addMsg(s, 'The flare stuns ' + stunned.length + ' creature' + (stunned.length > 1 ? 's' : '') + '.');
        ev.push({ t: 'flare', stunned: stunned });
      }
    }
    for (i = 0; i < s.items.length; i++) {
      var it = s.items[i];
      if (it.x !== p.x || it.y !== p.y) continue;
      var slot = s.inv.indexOf(null);
      if (slot < 0) {
        addMsg(s, 'Your pack is full; the ' + it.type + ' stays on the floor.');
        ev.push({ t: 'pack-full', item: it.type });
      } else {
        s.inv[slot] = it.type; s.items.splice(i, 1);
        addMsg(s, 'You pick up a ' + it.type + ' (slot ' + (slot + 1) + ').');
        ev.push({ t: 'pickup', item: it.type, slot: slot + 1 });
      }
      break;
    }
    return t === '>';
  }

  function refuse(state, msg) {
    if (!msg) return { state: state, turnConsumed: false, events: [], plans: [], drain: 0 };
    var s = clone(state); addMsg(s, msg); // only the message list changes
    return { state: s, turnConsumed: false, events: [{ t: 'refused', text: msg }], plans: [], drain: 0 };
  }

  // action: {type:'move',dir:'N|E|S|W'} | {type:'wait'} | {type:'use',slot:1..4}
  function step(state, action) {
    if (state.end) return { state: state, turnConsumed: false, events: [], plans: [], drain: 0 };
    var s = clone(state), ev = [], plans = [], fd = s.floorData, p = s.player;
    var descend = false, won = false, type = action && action.type;

    if (type === 'move') { // spec 2
      var dv = DIRS[action.dir];
      if (!dv) return refuse(state, null);
      var nx = p.x + dv[0], ny = p.y + dv[1];
      if (tileAt(fd, nx, ny) === '#') return refuse(state, null);
      s.turn++;
      var c = creatureAt(s, nx, ny);
      if (c) { // fight
        var dmg = (c.type === 'gloom' && c.staggered > 0) ? 4 : 2;
        c.hp -= dmg;
        addMsg(s, 'You hit ' + nm(c) + ' for ' + dmg + '.');
        ev.push({ t: 'hit', target: c.id, type: c.type, amount: dmg });
        if (c.hp <= 0) {
          s.creatures = s.creatures.filter(function (o) { return o !== c; });
          s.defeated++;
          addMsg(s, cap(nm(c)) + ' dies.');
          ev.push({ t: 'kill', target: c.id, type: c.type });
          if (c.type === 'gloom') won = true;
        }
      } else {
        p.x = nx; p.y = ny;
        descend = landOn(s, ev);
      }
    } else if (type === 'wait') {
      s.turn++;
    } else if (type === 'use') { // spec 6
      var slot = action.slot | 0, item = s.inv[slot - 1];
      if (!item) return refuse(state, 'Slot ' + slot + ' is empty.');
      if (item === 'salve') {
        if (s.hp >= MAX_HP) return refuse(state, 'You are already at full health.');
        s.turn++; s.hp = Math.min(MAX_HP, s.hp + 5); addMsg(s, 'You use the salve (+5 HP).');
      } else {
        if (s.ember >= 100) return refuse(state, 'Your ember is already at full strength.');
        s.turn++; s.ember = Math.min(100, s.ember + 30); addMsg(s, 'You pour oil on the ember (+30).');
      }
      ev.push({ t: 'use', item: item, slot: slot });
      s.inv[slot - 1] = null;
    } else {
      return refuse(state, null);
    }

    // Win check comes before dimming (spec 3, 7, 8).
    if (won) { endRun(s, 'victory'); updateSeen(s); return { state: s, turnConsumed: true, events: ev, plans: plans, drain: 0 }; }

    // Dimming.
    var drain = drainRate(s), before = s.ember;
    s.ember = Math.max(0, s.ember - drain);
    notifyEmber(s, before, s.ember);

    if (s.ember <= 0) {            // ember check: creatures do not act (spec 3, 8)
      endRun(s, 'ember');
    } else if (descend) {          // spec 2: next floor starts, no creature phase
      installFloor(s, FG.generateFloor(s.seed, s.floor + 1), s.floor + 1);
      addMsg(s, 'You descend to floor ' + s.floor + '.');
      ev.push({ t: 'descend', floor: s.floor });
    } else {                       // creature phase in id order (spec 2, 11)
      var ctx = makeCtx(s);
      s.creatures.slice().forEach(function (c) {
        if (c.hp <= 0 || s.creatures.indexOf(c) < 0) return;
        var d = ctx.dist[c.y * fd.w + c.x];
        var it = planAction(s, c, ctx);
        plans.push({ id: c.id, type: c.type, x: c.x, y: c.y, intent: it.kind, label: it.label, dist: isFinite(d) ? d : null });
        execute(s, c, it, ctx, ev);
      });
      if (s.hp <= 0) endRun(s, 'dead');
    }
    updateSeen(s);
    return { state: s, turnConsumed: true, events: ev, plans: plans, drain: drain };
  }

  EH.game = {
    newRun: newRun, newRunFromFloor: newRunFromFloor, step: step, planAction: planAction, makeCtx: makeCtx,
    bfsFromPlayer: bfsFromPlayer, drainRate: drainRate, DEFS: DEFS, DIRS: DIRS, FLOORS: FLOORS, MAX_HP: MAX_HP,
    STUN_TURNS: STUN_TURNS, updateSeen: updateSeen
  };
  if (typeof module === 'object' && module.exports) module.exports = EH.game;
})(typeof globalThis !== 'undefined' ? globalThis : this);
