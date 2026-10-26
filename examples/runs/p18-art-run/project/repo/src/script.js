/* Script parsing and the single run path (play.js, tests, bots). Pure: no I/O. UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./game.js'); require('./view.js'); require('./textview.js'); }
  var G = EH.game, V = EH.view, T = EH.textview;
  var DEFAULT_SEED = 'hollow';

  // See manual.md. First non-comment line may be "seed <text>"; every other non-space character is a command.
  function parseScript(text) {
    var seed = DEFAULT_SEED, commands = [], first = true, lines = String(text).split(/\r?\n/);
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].replace(/#.*$/, '').trim();
      if (!line) continue;
      if (first) {
        first = false;
        var m = /^seed\s+(.+)$/i.exec(line);
        if (m) { seed = m[1].trim(); continue; }
      }
      for (var j = 0; j < line.length; j++) {
        var ch = line.charAt(j);
        if (/\s/.test(ch)) continue;
        var c = ch.toLowerCase();
        if ('wasd.1234'.indexOf(c) < 0) throw new Error('Line ' + (i + 1) + ': unknown command "' + ch + '"');
        commands.push(c);
      }
    }
    return { seed: seed, commands: commands };
  }

  function toAction(cmd) {
    switch (cmd) {
      case 'w': return { type: 'move', dir: 'N' };
      case 'a': return { type: 'move', dir: 'W' };
      case 's': return { type: 'move', dir: 'S' };
      case 'd': return { type: 'move', dir: 'E' };
      case '.': return { type: 'wait' };
      default: return { type: 'use', slot: parseInt(cmd, 10) };
    }
  }

  // One logged step. entry.damage classifies each damage event for the check-14 assertion.
  function stepLogged(state, action, prevView, n) {
    var pv = prevView || V.view(state);
    var res = G.step(state, action);
    var after = V.view(res.state);
    var moved = state.player.x !== res.state.player.x || state.player.y !== res.state.player.y;
    var dmg = [];
    res.events.forEach(function (e) {
      if (e.t !== 'damage') return;
      var b = pv.creatures.filter(function (c) { return c.id === e.src; })[0];
      var plan = res.plans.filter(function (p) { return p.id === e.src; })[0];
      // D-002 strict meaning: the mark that applied on the tile where the player ended the turn.
      var np = res.state.player, marked;
      if (moved) {
        var rc = pv.reach.filter(function (q) { return q.x === np.x && q.y === np.y; })[0];
        marked = !!(rc && rc.creatures.some(function (c) { return c.id === e.src; }));
      } else marked = !!(b && b.threat);
      dmg.push({ src: e.src, type: e.type, amount: e.amount, visibleBefore: !!b, markedBefore: marked,
        case: moved ? 'reach' : 'threat' });
    });
    var entry = { n: n || 0, cmd: action, turn: res.state.turn, consumed: res.turnConsumed, ember: res.state.ember,
      drain: res.drain, events: res.events, plans: res.plans, damage: dmg, threatsBefore: pv.threats.map(function (t) {
        return { id: t.id, type: t.type, reason: t.reason };
      }) };
    return { state: res.state, entry: entry, view: after, consumed: res.turnConsumed };
  }

  // Pure: returns frames, final state, log, ignored count. opts.state overrides the initial state.
  function runScript(seed, commands, opts) {
    opts = opts || {};
    var state = opts.state || G.newRun(seed), v = V.view(state), frames = [{ index: 0, cmd: null, consumed: true, view: v, entry: null }];
    var log = [], ignored = 0;
    for (var i = 0; i < commands.length; i++) {
      if (state.end) { ignored = commands.length - i; break; } // spec 8: nothing changes after the end
      var r = stepLogged(state, toAction(commands[i]), v, i + 1);
      r.entry.cmd = commands[i];
      state = r.state; v = r.view; log.push(r.entry);
      frames.push({ index: i + 1, cmd: commands[i], consumed: r.consumed, view: v, entry: r.entry });
    }
    return { seed: state.seed, frames: frames, state: state, log: log, ignored: ignored };
  }

  function renderRun(res, opts) {
    opts = opts || {};
    var out = [];
    res.frames.forEach(function (f) {
      if (f.index === 0) out.push('--- start ---');
      else out.push('--- command ' + f.index + ': "' + f.cmd + '"' + (f.consumed ? '' : ' (refused: no turn passed)') + ' ---');
      out.push(T.renderFrame(f.view));
      if (opts.trace && f.entry) out.push(T.renderTrace(f.entry));
      out.push('');
    });
    if (res.ignored) out.push('(' + res.ignored + ' further command(s) ignored: the run is over)');
    return out.join('\n');
  }

  EH.script = { parseScript: parseScript, toAction: toAction, stepLogged: stepLogged, runScript: runScript,
    renderRun: renderRun, DEFAULT_SEED: DEFAULT_SEED };
  if (typeof module === 'object' && module.exports) module.exports = EH.script;
})(typeof globalThis !== 'undefined' ? globalThis : this);
