# Studio operation packet

operation: Step
goal: G-002
role: art-director
incoming_handoff: goals/G-002-entity-pictures/07-studio-to-art-director.md
next_seq: 9
runs: shot (up to 3 rounds)
run_shot: screenshots of index.html ({script}: keys to press)
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-entity-pictures/09-art-director-to-<recipient>.md
- design/<name>
- decisions/D-005-<name>.md
- @run/<shot>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-002-entity-pictures/07-studio-to-art-director.md
---
kind: handoff
goal: G-002
seq: 7
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 07: studio → art-director — visual review of the built entity pictures

## Task

Review what the player sees on the browser page against your spec `design/entity-pictures.md` and D-003. Judge readability and consistency: can each kind of thing be told apart at a glance, do the pictures fit the cave and ember mood, and do the threat and reach marks and the light levels stay readable over the pictures. Answer the two open questions below.

## Context

Goal G-002 (pictures for each kind of thing on the floor grid). Design and Plan are done, and the engineer has built the pictures per D-004 (code-drawn, 16x16 design grid, inset 4 px so 14 px in a 22 px tile). QA verifies the testable criteria in parallel. Nobody has yet seen the page. Tests only prove the mapping, palette size and text output.

## Findings

Facts about the build:

- 14 pictures (13 entities, the hound with 2 poses), 11-color palette (spec allows at most 12), no red or orange main fills.
- Marks as drawn: threat tile/area = red tint `rgba(255,40,40,0.35)` plus 3 px `#ff3030` border; creature threat = same border plus red `!` badge above the center; reach = `rgba(255,170,0,0.30)` tint, 2 px dashed `#ffb000` border, bold 10 px `#ffd070` creature letters at the tile center, with no dark backing; stunned/staggered = `rgba(150,200,255,0.45)` pale-blue wash plus badge `z` or `~` at top-left, no red.
- Remembered tiles use the dimmed tone and visible tiles the full tone. The flame has five growing steps for light radius 2 to 6.
- `TILE` is one constant in `repo/src/page.js` (22; also used for click mapping), so raising it (for example to 28) is a one-line change.

## Decisions already made

- D-003: flat dark-cave pictures, marks always drawn over pictures. D-004: pictures drawn by code.

## Constraints

- Your authority is visual direction within the vision. No rule or content change; no assets other than code-drawn pictures; no dependencies or network use; the page must open from the file system.
- If you have no means to see the page (no browser or screenshot), say so. You may then judge only from the drawing code and the palette. Mark any visual verdict you cannot give as unverified, not as met.

## Open questions

1. Do the 14 pictures read at 14 px? If not, should `TILE` be raised or the pictures simplified? State which pictures and what you would change.
2. Spec section 5 asks for a dark backing behind the reach-mark creature letter. It was not added. Is it required, and if so what exactly?

## Expected output

A visual-review report: per picture and per mark, readable / not readable / unverified, with required changes if any, and answers to the open questions. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/entity-pictures.md, repo/src/pictures.js, repo/src/scene.js, repo/src/page.js, repo/index.html
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
- Previous handoff: goals/G-002-entity-pictures/05-gameplay-engineer-to-studio.md
>>>END

<<<FILE studio/roles/art-director.md
---
kind: role
id: art-director
writes: design/*, decisions/*
runs: shot
---
# Role: Art Director

## Responsibility

Owns visual expression and visual consistency: style, readability, and the clarity of everything
the player sees.

## Decides

- Visual direction within the vision: colors, shapes, effects, UI presentation for a change.
- Visual acceptance: whether a change is readable and consistent with the art direction.

## Must not

- Change gameplay rules or parameters — that is `game-designer`.
- Change the art style pillars of the vision — escalate.
- Write production code.

## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).

## Produces

- Visual spec for a change: what must be visible, how, and visual acceptance criteria.
- Visual review verdict with evidence.

## Hands back / escalates when

- The visual problem is really a rules problem → `game-designer`.
- A style pillar would change → `game-director`, for an Owner escalation.

## Typical skills

visual-review, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/visual-review.md
---
name: visual-review
description: Review what the player sees for readability and consistency with the project's art direction, producing a verdict with evidence.
---
# Skill: Visual review

Typical roles: art-director.

## When to use

A problem may be visual, or a change affects what the player sees.

## Inputs

The build or captures, the art direction in the Project Context, the spec's visual criteria.

## Method

1. Check readability first: can the player tell what matters (threats, interactables, state) at a
   glance, in every environment and lighting condition the game has?
2. Check consistency with the art direction: palette, shapes, effects, UI style.
3. Check the spec's visual acceptance criteria.
4. Separate visual issues from rule issues; route rule issues to `game-designer`.

## Output

Visual verdict: pass/fail per criterion, readability issues with evidence and where they occur,
consistency notes, proposed visual direction for fixes.

## Do not

Change gameplay rules. Do not judge by personal taste over the project's art direction.
>>>END

<<<FILE design/entity-pictures.md
---
kind: design-spec
goal: G-002
author: art-director
status: draft-for-build
---
# Ember Hollow: pictures for each kind of thing (G-002)

Rules and numbers are in `design/game-spec.md`. This document changes no rules, balance or content, and does not touch the text player. "Page" means `repo/index.html` opened from the file system.

## 1. Intent

The Owner asked for pictures on "each of them". The Studio reads this as: every kind of thing the player meets on the floor grid gets its own picture, so the player tells things apart by looking, not by reading letters. The cave stays dark and the ember is the light. Pictures must never hide or weaken a threat mark or reach mark (pillar 1, D-002).

Caveat: nobody has seen the page yet (project.md#current-state). This spec is written from the specs and manual, not from a look at the current page. Tile size, the current colors and how marks are drawn are unknown to me. The criteria below are phrased so they hold whatever the current values are. The first look at the page belongs to the Build and QA steps (see Open questions).

## 2. Entity list

### In scope (each gets its own picture)

| # | Entity | Source in game-spec | Notes |
|---|---|---|---|
| E1 | Player with ember | sections 2, 3 | A small figure carrying a flame. |
| E2 | Cave moth `m` | section 4 | |
| E3 | Shade `s` | section 4 | |
| E4 | Ash hound `h` | section 4 | Two poses: normal and crouching. |
| E5 | The Gloom `G` | section 7 | One tile. Its 3x3 marked area is a mark, not a picture (see 5). |
| E6 | Unlit brazier `B` | section 3 | |
| E7 | Lit brazier `b` | section 3 | |
| E8 | Salve `+` | section 6 | |
| E9 | Oil flask `o` | section 6 | |
| E10 | Wall `#` | section 2 | Low-contrast cave-rock texture. |
| E11 | Floor `.` | section 2 | Low-contrast ground texture. |
| E12 | Stairs up `<` | section 2 | |
| E13 | Stairs down `>` | section 2 | |

The Gloom is a creature, not a terrain tile, so it is listed as E5.

Inventory slots use the same item pictures as E8 and E9 (the empty slot stays empty).

### Excluded

- Unseen tiles: stay blank by spec (section 9). A picture would leak information.
- Marks (threat, hound line, Gloom area, reach marks): these stay marks, not pictures (section 5).
- Ember bar, HP, message list, summary screens and buttons: not floor-grid entities. They keep their present look. The Gloom's picture and the end screens may be revisited in a later Goal.
- Any new creature, item or tile type: out of scope (game-spec section 12).
- The text player (`node play.js`): unchanged.

## 3. Style

- Dark cave: the background and unlit areas are near black. Only the ember lights the scene.
- Flat shapes with a strong silhouette, drawn with a small, fixed palette (about 12 colors in total). Shapes read first, color second. No photographic or noisy textures.
- Warm light is the ember's: the warmest and brightest colors in the scene belong to the player's flame, lit braziers and the light they cast. Cool colors (blue-grey, violet) belong to the cave, shades and the Gloom.
- Red and orange are reserved for marks. No picture uses red as its main color, and none uses orange dashed outlines (the reach mark). The warm flame of the player and lit braziers is yellow-gold, not red.
- Terrain is quiet: wall and floor have low contrast with each other and a fair margin below items, creatures and the player, so things stand out.
- Each picture sits inside the tile with an inner margin of about 10% on every side, which leaves the tile edge free for mark borders.

Creature identity (what the silhouette should say, so the player learns the behavior):

- Moth: small, winged, light-colored, pale body (drawn to light).
- Shade: tall, thin, hooded wisp in dark violet-grey with pale eyes (fears light).
- Hound: low, four-legged, heavy-shouldered, in ash grey with ember-colored eyes. The crouching pose is visibly lower, with the head down and the body stretched.
- Gloom: a large, many-limbed dark mass with a faint outline and two pale eyes, the largest and darkest creature picture. It still fits one tile.

## 4. Light and memory

- Visible tiles: pictures at full color.
- Remembered tiles (terrain, stairs, braziers, items): the same pictures, but visibly dimmer and less saturated than visible tiles. Creatures are never drawn from memory (game-spec section 3).
- Unseen tiles: blank, no picture.
- Every visible tile is drawn at the same brightness, including tiles at the edge of the glow. There is no brightness falloff inside the glow. This keeps the edge of the light easy to see and keeps the rule "visible is clearly brighter than remembered" simple. Revisit if Play wants more atmosphere.
- Ember flame on the player picture: its size follows r. The flame at r = 6 is visibly larger than at r = 2, with five distinguishable steps for r = 6, 5, 4, 3, 2 if feasible, and at least a large, medium and small flame (6-5, 4-3, 2) if not. The flame size is a reading aid, not a rule source.

## 5. Readability: pictures and marks

Layering order, bottom to top: tile background and terrain picture, item or brazier picture, area marks (Gloom 3x3, hound line), reach mark, creature or player picture, threat mark border and badge.

| Mark (D-002 / spec 9) | How it coexists with the picture |
|---|---|
| Threat mark on a creature | A red border of at least 3 px inside the tile edge, plus a corner badge (the `!`). The creature picture stays fully visible and unchanged inside it. The mark is drawn on top and never replaces the picture. |
| Hound crouch line | The tiles on the line get a red tint and a `!` over their terrain. The terrain, items and brazier pictures on those tiles stay recognisable (tint of at most about 40% opacity). |
| Gloom 3x3 area | The same as the crouch line: a red tint over all nine tiles. The Gloom stays visible in the middle. If the player or an item is within the area, the picture stays on top of the tint. |
| Reach mark on a neighbour tile | A dashed orange border and the creature letter(s) in a corner. The picture under it (floor, item, brazier, stairs) stays recognisable. The letter has a dark backing so it reads on any picture. |
| Stunned or staggered creature | The picture stays, with a pale-blue wash and a state badge. No red mark. It must not look like a threat. |

Additional rules:

- Marks are the same in position and meaning as before. Pictures change what is under them, not where marks appear.
- A mark must stay recognisable on top of the lightest and the busiest picture (a lit brazier, the Gloom). Where a conflict is found, the picture is simplified, not the mark.
- Shape, not only color, must tell creature types apart: each of E2 to E5 must be told apart when the picture is shown in greyscale.
- A creature letter is not needed on the picture. The reach mark letter stays. The creature list keeps names and states.

## 6. Acceptance criteria (player-observable)

Checks 31 to 49 are new. Each is checked by looking at the page (screenshots or live). The existing checks 1 to 30 stay in force.

### Pictures exist and differ
31. Every entity E1 to E13 appears on the page with its own picture. No creature, item, brazier or stair is shown only as a letter or a plain colored square.
32. Shown on their own on a floor tile, a moth, shade, hound and the Gloom can each be named by a viewer who has read the list of pictures, also in greyscale.
33. The salve and the oil flask differ in shape. An unlit and a lit brazier differ in shape and in light (the lit one is clearly warmer and brighter). `<` and `>` differ in shape.
34. Wall and floor are told apart at a glance. An item, a creature or the player on a floor tile stands out from the plain floor.
35. The player's picture is different from every creature picture and is visible when the player stands on `<`, a lit brazier or any floor tile.
36. The player's flame is visibly larger at r = 6 (E 80 to 100) than at r = 2 (E 1 to 19), seen in two screenshots from one run.
37. Inventory slots show the same pictures as the items on the floor. An empty slot shows no item picture.

### Light, memory and mood
38. Remembered tiles keep their pictures (same shapes) and are visibly dimmer than visible tiles. No creature picture is shown on a remembered tile. Unseen tiles are blank.
39. A visible tile at the very edge of the glow is still clearly brighter than a remembered tile next to it, at r = 6 and at r = 2.
40. As E falls across a threshold, the visible area with its pictures shrinks as before (check 29), and no picture outside it stays at full brightness.
41. The overall look is dark: unlit and unseen areas are near black, and the brightest, warmest spots on a typical frame are the player's flame and lit braziers.

### Marks over pictures (pillar 1, D-002)
42. Every creature that carries a threat mark in the text output (`!` line in the creature list) shows a threat border on the page, and the creature picture is still recognisable inside it. Checked on at least: an adjacent moth, an adjacent hound, a shade at r = 2, a crouching hound, the Gloom after gathering.
43. The crouch line and the Gloom 3x3 area are visible on the page, including nine tiles that hold floor, wall-adjacent floor, an item or a brazier. The tile pictures under the tint are still recognisable.
44. Every reach mark (`?` and the `Danger:` line in the text output) shows on the page as a dashed orange border with its creature letter(s) readable, also on an item tile and on a lit brazier tile. The picture under it is still recognisable.
45. For the same seed and the same commands, the set of tiles marked on the page equals the set of tiles marked in the text output (`!` tiles, threat creatures, `?` tiles) at every turn. Pictures change no mark. Checked on at least 3 scripted runs that include a hound crouch and a Gloom gather.
46. A stunned or staggered creature keeps its picture, has a state badge and a pale-blue wash, and has no red threat border. A crouching hound looks different from a standing hound, with the picture alone and no mark.

### Technical and unchanged parts
47. `repo/index.html` still opens from the file system with no server and no network. All pictures appear on first load, with no missing picture and no blocked-resource error in the browser console.
48. The text output of `node play.js` is byte-identical to before for the same scripts, and `node --test` still passes (at least the present 49 tests).
49. Checks 27 and 28 (page contents and controls) and check 30 (summary screens) still hold with pictures. Clicking a tile or a slot still works.

### Existing checks touched

- Check 27 (page contents): must still hold; the pictures change the grid drawing only.
- Check 28 (controls) and 30 (summary): unchanged, to be re-checked with pictures on.
- Check 29 (visible versus remembered, creature types distinguishable, threat and reach marks distinct, lit versus unlit brazier): the pictures touch each part. 31 to 46 refine it. Check 29 stays in force as written.
- Checks 1 to 26: text output and rules only. Untouched, covered by 48.

## 7. Experience signals (for Play and Review)

- A new player says what a moth, a shade, a hound and the Gloom are, without reading the list, from the pictures after one floor.
- The player finds braziers and items in the dark by shape, not by trial.
- Threat and reach marks are still the first thing the eye goes to when something can hurt. Nobody says a picture hid a warning.
- The page reads as a dark cave lit by the player's ember.
- Nobody confuses a stunned creature with a threatening one.

## 8. Edge cases

- Several marks on one tile (a neighbour tile that holds a reach mark and lies inside the Gloom area or a hound line): both stay visible; the area tint is under, the reach border and letter are over it.
- The player on a tile under a Gloom area or hound line: the player picture stays on top, and the threat border on the creature follows the rules of section 5.
- A creature on a tile that is both a threat tile and a remembered tile cannot happen: creatures show only while visible.
- Creatures that are orthogonally adjacent to the player or to a neighbour tile are shown even if a wall blocks line of sight (spec 9). Their pictures show as for any visible creature, with their marks.
- Very small tiles: if the tile is too small for the inner-margin picture plus the mark border to stay readable, the picture shrinks. The mark border keeps its size. See Open questions on tile size.

## 9. Changed design documents

- New: this file, `design/entity-pictures.md`.
- `design/acceptance-criteria.md` is not changed by this step. The new checks 31 to 49 live here. The Studio may fold them into that file when routing to Build or QA.
- `design/game-spec.md` is unchanged.
- Decision D-003 records the style and the layering rule.

## 10. Open questions

1. **Plan: yes, a short one.** The visuals do not need a particular method, but the method is risky enough to decide it first. The risks: (a) the page must work from `file://`, so how the pictures are made and stored matters (drawn by code, inline vector shapes, embedded data, or separate image files; loading separate files into a canvas works from `file://` for drawing but not for reading pixels, and some stricter browser settings may block it); (b) D-001 requires classic scripts, so the picture code must load in dependency order and keep rules code free of drawing; (c) which part of the code maps an entity and a state (crouching, stunned, lit) to a picture, kept out of the shared rules code and fed by the same state the marks use, so that pictures cannot change a mark (criterion 45); (d) whether the five flame sizes and the dimmed copies for remembered tiles are produced by code or stored. The Technical Director should settle these.
2. **Tile size and the current look are unknown.** Nobody has seen the page. The Build step should report the tile size in pixels and the current mark colors. If the tile is below about 20 px, the Studio should tell the Art Director, because the pictures in section 3 may need to be simplified or the tile size raised.
3. **Is the first Owner look (the proposed Goal 1: Owner checks the page) done before or after this Goal?** The pictures cannot be reviewed first-hand before someone has seen the page working at all. I recommend QA takes screenshots of the page before and after Build.
4. **Gloom size.** The spec has it as one tile. If the Owner wants a bigger boss picture, that is a rules and layout change for the Game Designer, not part of this Goal.
>>>END

<<<FILE repo/src/pictures.js
/* Pictures drawn by code (D-004). Each picture is authored on a 16x16 grid and scaled to the tile.
   draw(ctx, name, px, py, size, tone, opts). UMD-style (D-001). Uses only a 2D context passed in. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  var BORDER = 3, TWO_PI = Math.PI * 2;

  // Fixed palette: 11 colors. No red, no orange. Warm gold belongs to the ember and lit braziers.
  var PAL = {
    floorA: '#332b22', floorB: '#40372c', wallA: '#54493c', wallB: '#6f6352',
    ash: '#8c8f99', violet: '#5b4d80', pale: '#dfe3f0', gold: '#f0c640',
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
  function flame(k, step) {
    var cx = 11.5, cy = 7.5, h = 1.5 + step * 1.1, w = 0.8 + step * 0.5;
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
      k.c('violet', 8, 8, 7); k.c('night', 8, 8, 6);
      [[0, 3, 4, 2], [12, 3, 4, 2], [0, 11, 4, 2], [12, 11, 4, 2], [3, 0, 2, 3], [11, 0, 2, 3], [3, 13, 2, 3], [11, 13, 2, 3]]
        .forEach(function (b) { k.r('night', b[0], b[1], b[2], b[3]); });
      k.r('pale', 5, 6, 2, 2); k.r('pale', 9, 6, 2, 2);
    },
    player: function (k, opts) {
      k.c('pale', 5.5, 6, 2);
      k.p('blue', [[5.5, 8], [9.5, 15.5], [1.5, 15.5]]);
      k.r('ash', 11, 8.5, 1, 6.5);
      flame(k, opts && opts.flame ? opts.flame : 3);
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
>>>END

<<<FILE repo/src/scene.js
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
>>>END

<<<FILE repo/src/page.js
/* Browser page. Calls only newRun, step and view from the shared rules; no rule logic here (D-001).
   Pictures come from scene.js (mapping) and pictures.js (drawing); marks are drawn here from view fields only.
   This is the only file that may use window/document/Math.random. */
(function () {
  'use strict';
  var EH = window.EmberHollow, G = EH.game, V = EH.view, SCN = EH.scene, P = EH.pictures;
  var TILE = 22, BORDER = 3;
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

  // Threat border: 3 px, on the tile edge.
  function threatBorder(x, y) {
    ctx.strokeStyle = '#ff3030'; ctx.lineWidth = BORDER;
    ctx.strokeRect(x * TILE + BORDER / 2, y * TILE + BORDER / 2, TILE - 1 - BORDER, TILE - 1 - BORDER);
  }

  function render() {
    var v = V.view(state), sc = SCN.build(v), x, y;
    canvas.width = v.w * TILE; canvas.height = v.h * TILE;
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = 'bold ' + (TILE - 6) + 'px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';

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
      var big = ctx.font; ctx.font = 'bold 10px monospace';
      glyph(rc.creatures.map(function (cc) { return cc.letter; }).join(''), rc.x, rc.y, '#ffd070', 1);
      ctx.font = big;
    });
    // 4. creatures and the player (always full tone); stunned/staggered get a pale-blue wash and a badge
    sc.actors.forEach(function (a) {
      P.draw(ctx, a.picture, a.x * TILE, a.y * TILE, TILE, 'full', a.picture === 'player' ? { flame: sc.flame } : null);
      if (a.wash) {
        ctx.fillStyle = 'rgba(150,200,255,0.45)';
        ctx.fillRect(a.x * TILE + 4, a.y * TILE + 4, TILE - 9, TILE - 9);
        var f0 = ctx.font; ctx.font = 'bold 9px monospace';
        glyph(a.state === 'stunned' ? 'z' : '~', a.x - 0.25, a.y - 0.25, '#cfe6ff', 1);
        ctx.font = f0;
      }
    });
    // 5. threat border and badge on creatures that can hurt at their next action
    v.creatures.forEach(function (cr) {
      if (cr.threat) {
        threatBorder(cr.x, cr.y);
        glyph('!', cr.x, cr.y - 0.55, '#ff4040', 1);
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
>>>END

<<<FILE repo/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Ember Hollow</title>
<style>
  body { background: #0b0907; color: #d8cdb8; font-family: monospace; margin: 12px; }
  #app { display: flex; gap: 16px; flex-wrap: wrap; align-items: flex-start; }
  canvas { background: #000; border: 1px solid #4a3d2e; cursor: pointer; }
  #panel { min-width: 300px; max-width: 360px; }
  .row { margin: 6px 0; }
  #embar { width: 260px; height: 14px; border: 1px solid #7a5a2a; background: #1a120a; display: inline-block; vertical-align: middle; }
  #emfill { height: 100%; background: #e8902a; }
  button { background: #2a2118; color: #d8cdb8; border: 1px solid #7a5a2a; font-family: monospace; padding: 3px 8px; cursor: pointer; margin: 2px; }
  button:hover { background: #3a2f22; }
  #inv button { min-width: 84px; }
  #msgs div { color: #bfb399; }
  #msgs div:last-child { color: #fff; }
  #seedline input { background: #1a120a; color: #d8cdb8; border: 1px solid #7a5a2a; font-family: monospace; width: 130px; }
  #summary { position: fixed; left: 0; top: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.82); display: none; align-items: center; justify-content: center; }
  #summary .box { background: #1a120a; border: 2px solid #e8902a; padding: 20px 28px; min-width: 320px; }
  #summary h2 { margin-top: 0; color: #e8902a; }
  #err { color: #f66; }
  .hint { color: #8a7a62; font-size: 12px; }
</style>
</head>
<body>
<h1 style="margin:0 0 8px 0;">Ember Hollow</h1>
<div id="app">
  <canvas id="board"></canvas>
  <div id="panel">
    <div class="row" id="floorline"></div>
    <div class="row" id="hpline"></div>
    <div class="row">Ember <span id="embar"><div id="emfill"></div></span> <span id="emtext"></span></div>
    <div class="row" id="inv"></div>
    <div class="row"><button id="waitbtn">Wait (. / Space)</button><button id="restartbtn">Restart (R)</button><button id="newbtn">New seed (N)</button></div>
    <div class="row" id="seedline">Seed: <b id="seedtext"></b> <input id="seedinput" placeholder="type a seed"><button id="seedgo">Start</button></div>
    <div class="row"><b>Messages</b><div id="msgs"></div></div>
    <div class="row" id="threats"></div>
    <div class="row hint">Arrows/WASD move or fight, . or Space waits, 1-4 use item, R restart, N new seed. Click an adjacent tile to move or fight. Red marks = danger next turn.</div>
    <div id="err"></div>
  </div>
</div>
<div id="summary"><div class="box" id="summarybox"></div></div>
<script src="src/rng.js"></script>
<script src="src/floorgen.js"></script>
<script src="src/light.js"></script>
<script src="src/game.js"></script>
<script src="src/view.js"></script>
<script src="src/scene.js"></script>
<script src="src/pictures.js"></script>
<script src="src/page.js"></script>
</body>
</html>
>>>END

<<<FILE decisions/D-002-threat-and-reach-marks.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-26
supersedes: none
---
# D-002: threat marks plus reach marks on the four neighbour tiles

## Decision

Threat marks keep their meaning: a visible creature that can hurt the player at its next action, with the player where they stand. A new reach mark is added. Each of the four orthogonal neighbour tiles of the player is marked with the creature letter(s) that would hurt the player at their next action if the player ended the turn on that tile. All marks are computed with the ember as it will be after this turn's dimming (current E minus 1, or minus 2 near the Gloom). Check 14 is strict: every damaging creature had a mark on the tile where the player ended the turn, in the previous output.

Limits: reach marks cover only the four neighbours, not the whole map. No creature behaviour, number or content changes. A creature that is orthogonally adjacent to the player or to a neighbour tile the player could step on is always shown, even if a wall blocks line of sight.

## Rationale

Pillar 1 says every threat that can hurt the player next turn is readable before it does. Stepping next to a moth or a hound is a legal next-turn move that leads to damage. Leaving it unmarked would let a player be hurt by a rule they had no way to read. The mark costs no new content, and the same planner can produce it. It makes check 14 verifiable without exceptions.

## Alternatives considered

- Build's interim reading, with exceptions for the player's own move: it needs no change, but it contradicts the pillar in spirit and leaves check 14 weak.
- Marking every tile in the creature's reach across the map: more clutter and no extra benefit beyond the next step.

## Revisit when

Play shows that reach marks clutter the screen or that players ignore them, or a new creature has an area effect that the neighbour-only marks cannot express.
>>>END

<<<FILE decisions/D-003-picture-style-and-mark-layering.md
---
kind: decision
id: D-003
status: accepted
decided_by: art-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-003: flat dark-cave pictures, and marks always drawn over pictures

## Decision

1. Pictures use a flat, strong-silhouette style in a small fixed palette, on a near-black background. The warmest, brightest colors belong to the ember (the player's flame, lit braziers). Cool colors belong to the cave and the creatures of the dark.
2. Red and dashed orange are reserved for threat marks and reach marks (D-002). No picture uses them as a main color.
3. Layering is fixed: terrain, then item or brazier, then area marks (tint), then reach marks, then creature or player, then threat border and badge. Marks are never replaced by or merged into a picture. A conflict is solved by simplifying the picture.
4. Visible tiles are drawn at one full brightness, with no falloff. Remembered tiles use the same pictures, dimmer and less saturated. Creatures are never drawn from memory.
5. Creature types must be told apart by silhouette alone (greyscale test).
6. The set of marked tiles on the page must equal the set in the text output; pictures change no mark.

Limits: this covers the floor grid and the inventory item pictures. It does not choose how the pictures are made or stored (a Plan question), and it changes no rule.

## Rationale

Pillar 1 says every threat must stay readable. Fixing the layering and the reserved colors makes that a check (criteria 42 to 45) rather than a hope. The vision's dark cave lit by the ember is served by reserving warm light for the ember. Equal brightness inside the glow keeps the edge of the light and the visible-versus-remembered rule (check 29) unambiguous.

## Alternatives considered

- Brightness falloff inside the glow: more atmosphere, but it risks making tiles near the edge look remembered, and weakens check 29. Can be revisited.
- Keeping letters on the creatures with pictures only as decoration: weaker for telling things apart at a glance, which is the point of the Goal.
- Colored mark tints that blend into pictures: rejected, a blended mark can vanish on a busy picture.

## Revisit when

Play or QA finds that marks are hard to see over some picture, the tile size turns out too small, or the Owner wants a different mood or a bigger boss picture.
>>>END

<<<FILE decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-004: pictures are drawn by code on the canvas; a pure scene module maps the view model to pictures

## Decision

1. **Method.** Every picture is vector drawing code (canvas 2D paths and fills) in a new classic-script module `repo/src/pictures.js` (UMD, D-001). There are no image files, no embedded data URIs and no inline SVG. Each picture is authored once on a 16x16 design grid and scaled to the tile size, so the tile size is one constant.
2. **Mapping.** A second module, `repo/src/scene.js` (UMD, pure, no `window`/`document`/canvas), turns the view model from `view()` into a list of picture requests: `{x, y, picture, tone, ...}`. Tone is `full` (visible) or `dim` (remembered). It reads only the view model and returns new objects. It never mutates the view and never computes a mark. Marks (threat tint, reach border, letters, threat border, badges) keep being drawn by `page.js` from the same view fields as before.
3. **Remembered tiles and flame.** Both are made in code at draw time. Remembered tiles use the same drawing routine with a dimmed palette, derived from the fixed palette by one function (move toward grey, darken). Nothing is stored twice. The flame has five steps, one per r = 6, 5, 4, 3, 2, taken from `v.radius` through a table in `scene.js`.
4. **Layering** follows D-003: terrain, item or brazier, area tint, reach mark, creature or player, threat border and badge. Creature and player pictures are always drawn at full tone.

Limits: this does not choose the look of any picture (Art Director, D-003 and `design/entity-pictures.md`). It changes no rule, mark or text output.

## Rationale

- Code drawing works from `file://` with no loading, no blocked resource and no canvas taint, and has no network. Criterion 47 is met by construction.
- The page already draws everything on a canvas, so no new technology is needed.
- A pure `scene.js` can be tested in Node. The mapping tables, the flame steps, the crouch pose and the "pictures change no mark" rule can be checked without a browser.
- `pictures.js` takes a ctx as an argument, so Node tests can run it with a recording fake ctx.
- Rules code (`game.js`, `light.js`, `view.js`) is not touched, so D-001 holds.

## Alternatives considered

- Separate PNG/SVG files drawn into the canvas: they work on `file://` for drawing only, may be blocked by stricter browser settings, and cannot be tested in Node. Rejected.
- Embedded base64 data: needs an authoring tool and a binary-looking blob nobody can review. Rejected.
- Inline SVG/DOM per tile: up to 680 elements to re-render each turn and a second render path next to the canvas marks. Rejected.
- Stored dimmed copies and stored flame sprites: more data to keep in sync, with no gain at this size. Rejected.
- Putting the mapping inside `page.js`: untestable in Node and it would mix picture choice with mark drawing. Rejected.

## Revisit when

Tiles prove too small for readable code-drawn pictures, a viewer finds the vector style too crude, or the project allows a build step or assets.
>>>END

<<<FILE goals/G-002-entity-pictures/05-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 5
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 05: gameplay-engineer → studio — entity pictures built; QA and the Art Director verify next

## Task

Verify the build of `design/entity-pictures.md` (criteria 31 to 49). QA checks the testable criteria and the page with screenshots or live viewing; the Art Director judges the look. Nothing visual has been seen by anyone.

## Context

Goal G-002 (pictures for each thing on the floor grid). The Technical Director's plan (04) and D-004 were followed: code-drawn pictures, a pure `scene.js` mapping, marks kept in `page.js`. No rule, balance, content or text-player change.

## Findings

**Files added**
- `repo/src/scene.js`: `scene.build(view)` returns `{tiles, actors, flame}`. Tile request: `{x, y, terrain, item, tone, base, object}`. Actor request: `{x, y, picture, wash, state}`. Does not read `threat` or `reach` for anything and does not write to the view.
- `repo/src/pictures.js`: `draw(ctx, name, px, py, size, tone, opts)`, `drawFlame`, `dim`, `PALETTE` (11 colors), `NAMES`. 16x16 design grid.
- Tests: `repo/tests/pic-helpers.js` (fake ctx and mark comparison), `scene.test.js`, `pictures.test.js`, `marks.test.js`, `golden.test.js`, `golden/hashes.json`.

**Files changed**
- `repo/index.html`: two script tags (`scene.js`, `pictures.js`) after `view.js`, before `page.js`.
- `repo/src/page.js`: `render()` in D-003 order; inventory icons; threat border 3 px.
- `repo/manual.md`: one paragraph "Pictures on the browser page" (text-frame description untouched).
- Not touched: `game.js`, `light.js`, `floorgen.js`, `rng.js`, `view.js`, `textview.js`, `play.js`, `script.js`.

**Draw order in `render()`**: terrain picture, item/brazier/stairs picture, area tint (`cell.threat`, red 35% plus border), reach mark (orange 30% tint, dashed border, letters), creatures and player at full tone (stunned/staggered: pale-blue wash plus badge), then threat border and `!` badge for `creature.threat`.

**Tests**: the build check before this answer reported 69 passed, 0 failed (49 existing, 6 scene/flame/memory/no-DOM, 6 pictures, 1 marks, 7 temporary capture tests). In this answer the 7 capture tests are replaced by 7 golden comparison tests in `golden.test.js`; the runtime's Build check after this handoff gives the final count.
- Scene tests: full mapping table (terrain, stairs, braziers, items, 4 creatures, player, all pictures different), hound crouch pose, wash only for stunned/staggered, flame steps 5 distinct strictly increasing for r = 2..6 from real views plus E=100 gives 5, tone follows `vis`, unseen has no request, one actor per shown creature plus the player. (31, 33, 35, 36, 38, 40, 46 mapping part)
- Picture tests: 14 pictures (13 entities, hound 2 poses), draw in both tones inside the tile with the 3 px border area free, 11-color palette (at most 12), no red/orange main fill, dim differs from full, silhouettes differ, crouching hound lower, flame grows; module loads in Node with no globals and uses no DOM/network/Image (source scan). (31, 33, 36, 41 partly, 46, 47 partly)
- Marks test (45): 3 hand-made scripts (hound crouch, Gloom gather and stagger, flare with stun) and 3 seeded random walks of 120 turns, turn by turn: `JSON.stringify(view)` unchanged by `scene.build`, and the page's marked set (derived from `cell.threat`, `creature.threat`, `reach`) equals the `!`, `?` and `Danger:`/creature `!` lines of `renderFrame`. The run confirmed it saw crouching, gathering, threats, reach and washes.

**Golden (criterion 48) — deviation from the plan**: I could not store the full outputs (up to ~100 KB each) byte for byte here. I stored sha256 and byte count taken before any change, with the text modules untouched, in `tests/golden/hashes.json`; `golden.test.js` rebuilds the same output and compares both. It is the same check, but a failure does not show a diff. Scripts (seeds/commands from a fixed generator, all via `runScript` + `renderRun`, equal to what `play.js` prints without `--trace`):
- seed-a (`g-a`, 250 cmds, 127 frames, 48 hit lines, 36 kills), seed-b (`g-b`, 250 cmds), seed-c (`hollow`, 250 cmds, includes stun labels), seed-d (`42`, 250 cmds): random walks on floor 1.
- scenario-hound (crouch, 4 waits), scenario-gloom (gather), scenario-flare (brazier stun, kills).
Note: no random walk reached a crouch/gather/hits-with-gloom, so these are covered by the three hand-made scenarios. `play.js` itself was not run as a process in the golden test (existing tests do run it).

**Answers to the open questions**
1. Tile size: `TILE = 22`, unchanged. Picture inset 4 px (14 px picture). Marks as drawn after the change: threat tile/area = red tint `rgba(255,40,40,0.35)` plus 3 px `#ff3030` border (was 2 px) on the tile edge; creature threat = same 3 px red border plus a red `!` badge above the center (unchanged position); reach = `rgba(255,170,0,0.30)` tint, 2 px dashed `#ffb000` border (4/3 dash), bold 10 px `#ffd070` creature letters at the tile center (unchanged; I did not add a dark backing to the letter, which the spec section 5 asks for — see risks); stunned/staggered = `rgba(150,200,255,0.45)` wash on the inner area plus badge `z`/`~` at the top-left, no red.
2. State labels found by running: `crouching`, `stunned`, `staggered` (also `gathering` for the Gloom). Used as is.
3. Pictures I could not make distinct: I cannot judge this without a viewer. No hand-back for `TILE < 20` was needed. Silhouettes differ in code (tests), whether they read at 14 px is unknown.
4. `TILE` not raised. It is one constant in `page.js` (also used for the click mapping); raising it to 28 is a one-line change.

**Criteria and how covered**
- Tested by `node --test`: 31 (partly: a picture exists and is mapped for each entity), 33/35/46 (distinct names, crouch pose, wash flags), 36 (flame steps, grows in the drawing), 38/40 (tone, no request for unseen, no creature picture without a creature in the view), 41 (no red/orange main fill, palette size only), 45, 47 (partly: pure modules, no DOM/network/Image), 48 (hash). Existing 49 tests still pass.
- Not checked by anyone, needs someone to see the page: 32 (pictures look like what they are, greyscale), 34 (wall/floor/things stand out), 37 (inventory icons show and an empty slot shows none — the code does it but is unexercised), 39 and 40 (brightness difference visible, incl. glow edge), 41 (looks dark, warmest spots are the flame and lit braziers), 42 to 44 (marks stay recognisable over pictures), 46 (stunned does not read as a threat; badge legibility), 47 (no console error on opening; `page.js` was never run), 28, 30, 49 (controls, summary, clicking a tile or slot), 36 in two screenshots.

## Decisions already made

- D-001, D-002, D-003, D-004 followed. No new Decision.

## Constraints

- No rule/balance/content change; text player byte-identical (hash test); no dependencies, network, image files or ES modules; `window`/`document` only in `page.js`.

## Open questions

1. For the Art Director/QA: do the 14 pictures read at 14 px (TILE 22)? If not, raise `TILE` or simplify; mine is the first look.
2. Spec section 5 asks that the reach-mark letter have a dark backing. The plan said keep reach styling as is, so I did not add one. Art Director or TD to decide whether to add it.
3. Risk: hash-based golden shows no diff on failure.

## Expected output

QA: run `node --test`, open `repo/index.html`, take screenshots (r=6 and r=2, remembered tiles, each creature, threat/reach/area marks over pictures, stunned creature, inventory with items, summary screen, click a tile and a slot, console empty) and verify the criteria above. The Art Director reviews the look from the screenshots. Do not mark any visual criterion as met before that.

## Sender assessment

Confidence is high for the mapping, the mark equality and text output; unknown for everything visual. `page.js` is only exercised by reading; changes there are thin (draw order, inventory canvas, threat border). Likely first problems to look for: icon canvas size in buttons, wash badge legibility, reach letters over busy pictures, the very low contrast of dimmed colors.

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (1.7 s).

```text
 ember after dimming (65.055557ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (7.236505ms)
✔ check 2: waiting costs 1 E; radius thresholds (1.857766ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.698531ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.27466ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.290529ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.384678ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.836102ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.18479ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.431023ms)
✔ check 20: after an end state further commands change nothing (0.35936ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.299149ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.278668ms)
✔ scene: full mapping table for terrain, stairs, braziers, items and creatures (3.106828ms)
✔ scene: a crouching hound has its own picture; a standing one does not (0.786549ms)
✔ scene: wash only for stunned and staggered (4.902805ms)
✔ flame: five distinct, strictly increasing steps for r = 2..6, from real views (5.735359ms)
✔ memory: tone follows vis; unseen tiles get no request (3.917903ms)
✔ scene.js and pictures.js use no DOM, network or Image (0.297724ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (12.485276ms)
✔ visibility: walls block line of sight; the glow is circular (0.563206ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (0.948425ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.362977ms)
ℹ tests 69
ℹ suites 0
ℹ pass 69
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1666.899222
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, repo/manual.md, repo/index.html, repo/src/page.js, repo/src/scene.js, repo/src/pictures.js, repo/tests/golden.test.js
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
- Previous handoff: goals/G-002-entity-pictures/04-technical-director-to-gameplay-engineer.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-entity-pictures/09-art-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
