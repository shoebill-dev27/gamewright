/* Scene mapping (D-004): turns the view model into picture requests. Pure; plain data only.
   Never writes to the view, never decides a mark (threat/reach stay in page.js). UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  // Tile picture tables: terrain name (from view) -> base picture (wall/floor) and object picture.
  var BASE = { wall: 'wall', floor: 'floor', up: 'floor', down: 'floor', brazier: 'floor', lit: 'floor' };
  var OBJECT = { up: 'stairs-up', down: 'stairs-down', brazier: 'brazier', lit: 'brazier-lit' };
  var ITEM = { salve: 'salve', oil: 'oil' };
  var CREATURE = { moth: 'moth', shade: 'shade', hound: 'hound', gloom: 'gloom' };
  var WASH_STATES = { stunned: true, staggered: true };
  var CROUCH_STATE = 'crouching';
  // Glow radius r -> flame step (criterion 36).
  var FLAME = { 6: 5, 5: 4, 4: 3, 3: 2, 2: 1 };

  function flameFor(r) {
    if (r >= 6) return 5;
    if (r <= 2) return 1;
    return FLAME[r];
  }

  function build(v) {
    var tiles = [], actors = [], x, y;
    for (y = 0; y < v.h; y++) {
      for (x = 0; x < v.w; x++) {
        var c = v.cells[y][x];
        if (!c.seen || !c.terrain) continue;
        tiles.push({
          x: x, y: y, terrain: c.terrain, item: c.item || null, tone: c.vis ? 'full' : 'dim',
          base: BASE[c.terrain],
          object: OBJECT[c.terrain] || (c.item ? ITEM[c.item] : null) || null
        });
      }
    }
    v.creatures.forEach(function (cr) {
      var pic = CREATURE[cr.type];
      if (cr.type === 'hound' && cr.state === CROUCH_STATE) pic = 'hound-crouch';
      actors.push({ x: cr.x, y: cr.y, picture: pic, wash: !!WASH_STATES[cr.state], state: cr.state });
    });
    actors.push({ x: v.player.x, y: v.player.y, picture: 'player', wash: false, state: null });
    return { tiles: tiles, actors: actors, flame: flameFor(v.radius) };
  }

  EH.scene = { build: build, flameFor: flameFor,
    TABLE: { base: BASE, object: OBJECT, item: ITEM, creature: CREATURE, flame: FLAME, crouchState: CROUCH_STATE } };
  if (typeof module === 'object' && module.exports) module.exports = EH.scene;
})(typeof globalThis !== 'undefined' ? globalThis : this);
