# Studio operation packet

operation: Step
goal: G-002
role: gameplay-engineer
incoming_handoff: goals/G-002-entity-pictures/10-studio-to-gameplay-engineer.md
next_seq: 11
runs: tests, trace (up to 3 rounds)
run_tests: node --test
run_trace: node play.js --trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-entity-pictures/11-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-002-entity-pictures/10-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 10
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 10: studio → gameplay-engineer — fix criterion 44 and apply D-005 (picture and mark legibility)

## Task

Edit `repo/src/page.js` and `repo/src/pictures.js` to apply Decision D-005 in full. This includes the dark backing behind the reach letters, which fixes the QA failure on criterion 44. Run `node --test` and report to `studio`.

## Context

Goal G-002 (a picture for each kind of thing on the floor grid). The first build (sha ed0ad983accb, 69/69 tests) went through two parallel checks:

- QA (08): criterion 44 **fails**. `design/entity-pictures.md` section 5 requires a dark backing behind the reach letter, and `page.js` draws the letters (`#ffd070`, 10 px) with none. QA could not check the other visual criteria because it had no viewer.
- Art Director (09): judged from the code only and accepted **D-005**. It requires TILE 28, explicit badge fonts, dark chips behind the threat `!` badge, the stun/stagger badge and the reach letters, a night outline on the player, a lighter shade violet and a thicker Gloom ring. It also checked the remembered wall/floor contrast (item 7). The details and exact values are in D-005. It is the authority for this step.

This is the first failure of criterion 44, so it goes back to Build, not to Plan.

## Findings

Points from the two reports that the engineer needs:

- QA R2: the threat `!` badge is centered on the creature tile's top edge (`cr.y - 0.55` tiles, 16 px font). Half of it lies on the tile above and is clipped in row 0. D-005 items 2 and 3 address this.
- QA R1 / Art Director: the player body is the same blue as `<`, and the player flame is the same gold as the lit-brazier flame. D-005 item 5 (outline, `grow` flame parameter) addresses this.
- The Art Director could not read the board width (`v.w`). The board at TILE 28 plus the 360 px panel must fit a 1280 px window. If it does not, use TILE 26 (D-005's fallback) and say which TILE you used.
- The Art Director expects reach marks inside a Gloom area or hound line to possibly merge with the 3 px red border. Do not change this now. Screenshots will decide.

## Decisions already made

- D-002: threat marks plus reach marks. Their meaning and tile sets do not change.
- D-003: flat dark-cave style, marks always drawn over pictures.
- D-004: pictures drawn by code, pure `scene.js` mapping.
- D-005: tile size, badge fonts, dark chips, player outline, shade violet, Gloom ring.

## Constraints

- Do not touch `scene.js`, the rules, `textview.js`, `script.js`, `play.js` or the mark logic. `scene.js` must stay pure and must not read `threat` or `reach`.
- No rule, content, dependency, network or asset change. The palette stays at 12 colors at most, with no red or orange main fill. The page must still open from the file system.
- The text player output must stay byte-identical. The golden hashes in `repo/tests/golden/hashes.json` must not change. Do not regenerate them to make a test pass.
- The existing tests (the picture tests, the marks tests for criteria 42 to 46 and the golden test) must pass. Adjust a picture test only where D-005 deliberately changes the value it checks (for example the TILE size), and say which one you changed and why.
- If D-005 conflicts with the spec or with a tested criterion, stop and hand back with the conflict. Do not decide the look yourself.

## Open questions

None for the engineer. The Studio sends the results of the screenshots to the Art Director and QA later.

## Expected output

Build notes in the handoff template, addressed to `studio` (`to: studio`), so that the next Verify steps get fresh Handoffs. They list:

- the files changed, and how each D-005 item (1 to 7) was applied, or why one was not applied;
- which TILE was used (28 or 26) and why;
- the `node --test` result with counts, with the golden test unchanged;
- anything the Art Director or QA should look at in screenshots.

The notes are not a verification verdict.

## Sender assessment

Studio routing note: this step is the first return to Build for criterion 44. The next step is Verify in parallel, with screenshots (QA and Art Director). Budget is tight: 13 planned in total, 10 used after this Route.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, repo/src/scene.js, repo/index.html, repo/tests/pictures.test.js, repo/tests/golden.test.js, repo/tests/golden/hashes.json, project.md#constraints
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/09-art-director-to-studio.md (also read goals/G-002-entity-pictures/08-qa-to-studio.md for the criterion 44 failure)
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).
- The change is not finished but nothing is missing → `outcome: partial`, saying what is done and
  what remains (not `question`).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
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

<<<FILE repo/tests/pictures.test.js
'use strict';
// G-002: drawing (criteria 31, 33, 35, 36, 41, 47) with a recording fake ctx at TILE 22.
const test = require('node:test');
const assert = require('node:assert/strict');
const P = require('../src/pictures.js');
const { fakeCtx } = require('./pic-helpers.js');

const TILE = 22, PX = 50, PY = 50;

function render(name, tone, opts) {
  const rec = fakeCtx();
  P.draw(rec.ctx, name, PX, PY, TILE, tone, opts);
  return rec;
}
function hsl(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255, g = parseInt(hex.slice(3, 5), 16) / 255, b = parseInt(hex.slice(5, 7), 16) / 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  if (!d) return { h: 0, s: 0, l };
  const s = d / (1 - Math.abs(2 * l - 1));
  let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  h = (h * 60 + 360) % 360;
  return { h, s, l };
}

test('pictures: there is one picture per entity and pose (13 entities, hound in 2 poses)', () => {
  const want = ['player', 'moth', 'shade', 'hound', 'hound-crouch', 'gloom', 'brazier', 'brazier-lit', 'salve', 'oil',
    'wall', 'floor', 'stairs-up', 'stairs-down'];
  assert.deepEqual(P.NAMES.slice().sort(), want.slice().sort());
});

test('pictures: every picture draws in both tones, inside its tile, without throwing', () => {
  for (const name of P.NAMES) for (const tone of ['full', 'dim']) {
    const rec = render(name, tone);
    assert.ok(rec.fills.length > 0, name);
    const b = rec.bbox();
    assert.ok(b.x0 >= PX - 1e-6 && b.y0 >= PY - 1e-6 && b.x1 <= PX + TILE + 1e-6 && b.y1 <= PY + TILE + 1e-6, name + ' ' + JSON.stringify(b));
    if (name !== 'wall' && name !== 'floor') {
      // entity pictures leave the 3 px mark border free
      assert.ok(b.x0 >= PX + 3 && b.y0 >= PY + 3 && b.x1 <= PX + TILE - 3 && b.y1 <= PY + TILE - 3, name + ' margin ' + JSON.stringify(b));
    }
  }
  for (let step = 1; step <= 5; step++) assert.doesNotThrow(() => P.drawFlame(fakeCtx().ctx, PX, PY, TILE, step, 'full'));
});

test('pictures: the palette is small; no red or orange main fill', () => {
  const full = new Set(), dimmed = new Set();
  for (const name of P.NAMES) {
    for (const [tone, set] of [['full', full], ['dim', dimmed]]) {
      const rec = render(name, tone);
      rec.fills.forEach((f) => set.add(f.color));
      const main = rec.fills.slice().sort((a, b) => b.area - a.area)[0].color;
      const c = hsl(main);
      assert.ok(!(c.s > 0.35 && (c.h < 40 || c.h >= 340)), name + ' ' + tone + ' main ' + main);
    }
  }
  assert.ok(full.size <= 12, 'full colors: ' + full.size);
  assert.ok(dimmed.size <= 12, 'dim colors: ' + dimmed.size);
  for (const k of Object.keys(P.PALETTE)) { const c = hsl(P.PALETTE[k]); assert.ok(!(c.s > 0.35 && (c.h < 40 || c.h >= 340)), k); }
});

test('pictures: dim differs from full for every picture', () => {
  for (const name of P.NAMES) {
    const a = render(name, 'full').fills.map((f) => f.color).join(), b = render(name, 'dim').fills.map((f) => f.color).join();
    assert.notEqual(a, b, name);
  }
  assert.notEqual(P.dim('#f0c640'), '#f0c640');
});

test('pictures: shapes differ (silhouettes are not copies of each other)', () => {
  const sigs = P.NAMES.map((n) => render(n, 'full').ops.join(';'));
  assert.equal(new Set(sigs).size, sigs.length);
  const h = (n) => { const b = render(n, 'full').bbox(); return b.y1 - b.y0; };
  assert.ok(h('hound-crouch') < h('hound'), 'crouching hound is lower');
  assert.ok(h('shade') > h('hound') && h('shade') > h('moth') - 1e-9 || h('shade') >= h('moth'), 'shade is tall');
});

test('flame: height grows with every step', () => {
  const hs = [1, 2, 3, 4, 5].map((s) => { const rec = fakeCtx(); P.drawFlame(rec.ctx, PX, PY, TILE, s, 'full'); const b = rec.bbox(); return b.y1 - b.y0; });
  for (let i = 1; i < hs.length; i++) assert.ok(hs[i] > hs[i - 1], hs.join());
  const p1 = render('player', 'full', { flame: 1 }).ops.join(), p5 = render('player', 'full', { flame: 5 }).ops.join();
  assert.notEqual(p1, p5);
});
>>>END

<<<FILE repo/tests/golden.test.js
'use strict';
// G-002 criterion 48: the text player output is unchanged. Compares sha256 + byte count of the full text output
// (renderRun, as play.js prints it) with the values captured before the picture work (tests/golden/hashes.json).
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { world } = require('./helpers.js');
const SC = require('../src/script.js');

const GOLD = JSON.parse(fs.readFileSync(path.join(__dirname, 'golden', 'hashes.json'), 'utf8'));

function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ALPHA = 'wasd.wasdwasd1';
function gen(n, k) { const r = lcg(k), out = []; for (let i = 0; i < n; i++) out.push(ALPHA.charAt(r() % ALPHA.length)); return out; }
const rowsG = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};

const CASES = [
  ['seed-a', () => SC.runScript('g-a', gen(250, 11))],
  ['seed-b', () => SC.runScript('g-b', gen(250, 23))],
  ['seed-c', () => SC.runScript('hollow', gen(250, 37))],
  ['seed-d', () => SC.runScript('42', gen(250, 59))],
  ['scenario-hound', () => SC.runScript('scenario', '....'.split(''), { state: world(['#@.h..#']) })],
  ['scenario-gloom', () => SC.runScript('scenario', '....w.'.split(''), { state: world(rowsG(2, 4), { floor: 5 }) })],
  ['scenario-flare', () => SC.runScript('scenario', 'dddd..'.split(''), { state: world(['#@.m.B..s.#']) })]
];

for (const [name, mk] of CASES) {
  test('golden text output (criterion 48): ' + name, () => {
    const text = SC.renderRun(mk());
    const sha = crypto.createHash('sha256').update(text, 'utf8').digest('hex');
    assert.equal(Buffer.byteLength(text, 'utf8'), GOLD[name].bytes, 'byte count');
    assert.equal(sha, GOLD[name].sha256, 'sha256');
  });
}
>>>END

<<<FILE repo/tests/golden/hashes.json
{
  "note": "sha256 of renderRun(...) (no trace) taken BEFORE any G-002 change, with textview.js/script.js/play.js unchanged. Scripts are defined in tests/golden.test.js.",
  "seed-a": { "sha256": "d120b8efd1d1318348da052523733aad285d8ec0920dc5508af0fe94048b0707", "bytes": 76794 },
  "seed-b": { "sha256": "1742fb17ed0c25ca3beb4135483aa7dbc7e503a44c9e199f7c4f6d21fdf32fd6", "bytes": 88573 },
  "seed-c": { "sha256": "1a49b49fbcaa6b872d3cc47a48b0e602eff1d064c8ed039502fd6ab5df1669ec", "bytes": 98545 },
  "seed-d": { "sha256": "169dd502c10c74626ff739d9600b50f863ab5a0b9483896e149d1436c64c9305", "bytes": 101251 },
  "scenario-hound": { "sha256": "d800fd2d4f5e3b304f1179fe409804f908d7dfb0eed13abdb708389f28959ab8", "bytes": 2942 },
  "scenario-gloom": { "sha256": "f752844b4673cdc3c12932aa3ac864c038ff6b99bf9425b05139f0ff7fd66872", "bytes": 4304 },
  "scenario-flare": { "sha256": "9618902d1e0142427f2602e17624576205616428fc1935fcde361d6a4bc24f5f", "bytes": 3876 }
}
>>>END

<<<FILE project.md#constraints
## Constraints

- The build is JavaScript for Node.js 20 and the browser, with no dependencies and no network
  use, in `repo/`. The game's rules live in code that both ways of playing share.
- **For people: a browser page.** `repo/index.html` opens straight from the file system (no
  server) and is played with the keyboard or the mouse. It draws the floor as a grid.
- **For the team: input scripts.** `run_play` (`node play.js {script}`) plays a script and prints
  what the player sees, as text, turn by turn; `run_trace` adds the internal state; `run_tests`
  (`node --test`) runs the build's tests. The script format (including how a run's seed is
  chosen) is the build's to define, in `repo/manual.md`, which ships with the build and is all a
  player is told.
- Deterministic: the same seed and the same commands always give the same run.
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

<<<FILE decisions/D-005-tile-size-and-mark-chips.md
---
kind: decision
id: D-005
status: accepted
decided_by: art-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast

## Decision

All of this is visual direction. No rule, mark meaning, mark position (which tiles) or text output changes.

1. **Tile size.** `TILE` goes from 22 to 28 in `repo/src/page.js`. The picture inset stays 4 px, because `pictures.js` takes `max(round(0.1*size), BORDER+1)`, which is 4 at 28. The picture is then 20 px, so one design unit is 1.25 px instead of 0.875 px. The 3 px threat border keeps 1 px of gap to the picture. If the board plus the 360 px panel is too wide for the Owner's screen, 26 is acceptable (unit 1.125 px). The panel already wraps below the board via flex-wrap. The click mapping uses `TILE`, so it follows.
2. **Fonts.** `render()` sets the base font to `TILE-6` px bold (22 px at 28). That is far too big for the `!` badge. Set explicit fonts: the `!` and the `z`/`~` badges use bold 10 px, the reach letters bold 10 px.
3. **Badges on a dark chip, inside the tile.** The threat `!` is no longer centered on the top tile edge (that put half of it on the tile above and red on red against the border).
   - It is drawn after the creature picture, as a chip in the top-left corner inside the 3 px border: rect at (x*TILE+3, y*TILE+3), 8 px wide, 11 px tall, fill `#150f22` at alpha 0.9, `!` in `#ff4040` centered in it.
   - The stunned/staggered badge uses the same chip position and shape, with `z` or `~` in `#cfe6ff`.
   - A stunned or staggered creature is not a threat, so the two badges do not co-occur. If they could, the threat chip wins and the state chip goes bottom-left.
   - The wash keeps `rgba(150,200,255,0.45)` over the inner area, and still no red on it.
4. **Reach letters get the dark backing (spec section 5 is required).**
   - After the orange tint and dashed border, and before the letters, fill a rect centered on the tile: height 12 px, width = letter count * 6 + 4 px, capped at TILE-6. Fill `#150f22` at alpha 0.85.
   - Letters stay bold 10 px `#ffd070`. With 3 or more letters, use 9 px and a width of letter count * 5.5 + 4.
   - The backing must not cover the dashed border, which lies in the outer 3 px.
5. **Player outline.** The player's blue cloak sits on blue stairs-up, and the player's gold flame sits on the lit brazier's gold flame.
   - Before the player shapes, draw the same head, cloak and flame polygons in `night` grown by 1 design unit on every side. The flame takes a `grow` parameter on `h` and `w`.
   - This is the player picture only. It adds no color.
6. **Shade and Gloom contrast.** The shade (`violet #5b4d80`, luminance about 86 against a floor of about 44) and the Gloom ring (1 unit thick) are the weakest against the floor.
   - Change `violet` to `#7566a8` (12th palette slot not needed, same slot).
   - Reduce the Gloom's inner `night` disc from radius 6 to 5.5, so the ring is 1.5 units.
7. **Dim palette.** Keep the 0.55 factor for now. If a screenshot shows remembered wall and remembered floor merging, raise the factor from 0.55 to 0.65 in `dim()`.

## Rationale

- At 14 px, one design unit is 0.875 px. Sub-pixel features are the moth antennae (1 unit), the hound eye (1x1), the oil-flask highlight (1x3), the staff, and the gaps between stair bars. At 20 px they are 1.25 px and survive. Simplifying all of them would lose the ember-eye cue that the spec asks for.
- The reach letter sits at the tile center, where the salve's pale cross, the lit brazier's gold flame and the stair bars all have colors close to `#ffd070`. Without a backing the letter can vanish on exactly those tiles, which breaks pillar 1 (D-002) and check 44.
- The old `!` placement came from the pre-picture page. Over pictures it lands on the creature's head and on the neighbor tile.

## Alternatives considered

- Simplify the pictures and keep 22 px: loses detail the spec asks for and still leaves 3 px of margin per side. Rejected.
- Backing the letters with a light fill: clashes with the dark mood. Rejected.
- Tile 32: the board would be about 1090 px wide for a 34-column map, too wide with the panel. Held back.

## Revisit when

A screenshot at 28 px shows any picture still unreadable, the board does not fit, or marks are lost on a picture.
>>>END

<<<FILE goals/G-002-entity-pictures/09-art-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 9
from: art-director
to: studio
stage: Route
outcome: partial
---
# 09: art-director → studio — visual review of the entity pictures: changes required (D-005), screenshots still needed

## Task

Route D-005 to the gameplay-engineer to apply. Then get screenshots of the page, and send them back to me for the final visual verdict.

## Context

Goal G-002. Handoff 07 asked for a visual review of the 14 pictures and the marks, and for answers to two open questions. This step could not see the page. It judged from the drawing code (`pictures.js`, `scene.js`, `page.js`) and the palette arithmetic only. A verdict is called "met" only for what the code proves. Everything visual is **unverified**, and the predictions below are code-based.

## Findings

**Basis.** The pictures are authored on 16x16 and drawn with inset 4 px at TILE 22, so the picture is 14 px and one design unit is 0.875 px. Marks are drawn after the pictures, in D-003 order.

**Answer to Q1: do the 14 pictures read at 14 px?**
- Not reliably. The silhouettes are fine, but several details fall under 1 px. Raise `TILE` to 28 (picture 20 px, unit 1.25 px) and do not simplify the silhouettes. D-005 item 1 has the details and a fallback of 26.

**Answer to Q2: is the dark backing for the reach letter required?**
- Yes. D-005 item 4 gives the exact backing.
- The letter is bold 10 px `#ffd070` at the tile center, over a 30% orange tint.
- At the center the pictures hold the salve's pale cross, the lit brazier's gold flame and the stair bars, all near the letter's color.

**Per picture** (readability at 14 px, predicted from the code; every visual verdict is unverified until seen):

| Picture | Verdict | Notes |
|---|---|---|
| Player | unverified, change required | Cloak is `blue`, the same as stairs-up, and the gold flame overlaps the lit brazier's gold flame (player on `<` or on a lit brazier, criterion 35). Add the night outline (D-005 item 5). The staff is 0.9 px wide, which is fine at 28. |
| Moth | unverified, likely readable | Wide pale X-wings are a strong silhouette. The 1-unit antennae are sub-pixel at 22, fine at 28. |
| Shade | unverified, change required | `violet` on the floor is low contrast (luminance about 86 against 44). Eyes are 1.3x1.75 px at 22. Lighten the violet (D-005 item 6). |
| Hound | unverified, likely readable | Body is wide and the legs are visible. The ember eye is 0.9 px at 22. Fine at 28. |
| Hound crouching | unverified, likely readable | The body is about 3 px lower than the standing one, so the pose difference exists at 22 and grows at 28. |
| Gloom | unverified, change required | `night` disc on a near-black floor, held only by a 0.9 px ring at 22. Thicken the ring to 1.5 units (D-005 item 6). Eyes are 1.75 px, fine. |
| Wall, floor | unverified | Intended low contrast. Full tone: wall `#54493c`, floor `#332b22`, a quiet and plausible difference. In dim tone the wall is about `#2c2926` against the floor at about `#1a1816`, only about 18 levels apart. Watch this in the screenshot (D-005 item 7). |
| Stairs up, down | unverified, likely readable | Blue ascending and green descending bars. The gaps between bars are 0.9 px at 22 and may blur into a wedge. Shape and color both differ, so it is acceptable. |
| Salve, oil flask | unverified, likely readable | Green square with a cross against a blue round flask with a gold stopper. Their luminances are close (about 146 and 154), but the shapes differ (greyscale test, criterion 33). The oil highlight (1 unit) is nearly invisible at 22. |
| Unlit, lit brazier | unverified, likely readable | The same bowl. The lit one adds a gold and pale flame, so shape and light both differ. |
| Flame steps | unverified | Heights grow about 1.2 px per step at 22, so adjacent steps may not be told apart. Large, medium and small (6-5, 4-3, 2) are very likely distinguishable, which the spec accepts as a fallback. |
| Remembered tone (all) | unverified | Math: gold dims to about `#776c4b`, green to about `#425a46`, still readable on the dim floor. Visible floor against remembered floor is about 25 levels apart, so check 39 is probably met but needs a look. |

**Per mark:**

| Mark | Verdict | Notes |
|---|---|---|
| Threat border, 3 px (creature, hound line, Gloom area) | unverified, likely readable | The 4 px picture inset leaves 1 px free of the border, so the border does not touch the pictures. Adjacent area tiles form a red grid (6 px lines with 1 px gap), which still reads as an area. |
| Area tint 35% (hound line, Gloom 3x3) | unverified, likely readable | Drawn under the creature and player pictures, which is correct. |
| Threat `!` badge on creatures | **not readable as built, change required** | Centered on the top tile edge at the 16 px base font (`TILE-6`). Half of it lies on the neighbor tile, and its lower half sits on the red border (red on red) and on the creature's head. In row 0 it is cut off. See D-005 items 2 and 3. |
| Reach mark (tint, dashed border, letters) | **not readable on some tiles, change required** | The dashed border is fine. The letters need the backing (Q2). Also, in D-002 and edge case 8 a reach tile can lie inside a Gloom area or hound line. Then the 2 px orange dashes sit over the inner 2 px of the 3 px red border and leave 1 px of red outside. Unverified. If the screenshot shows the two marks merging, QA reports it and I will specify an offset. |
| Stun/stagger wash and badge | unverified, change required | The `z`/`~` is `#cfe6ff` over the pale-blue wash, so light on light. Use the dark chip (D-005 item 3). The wash has no red, which is right. |

**Q2 and the open questions are answered above. Nothing here changes a rule, a mark's meaning, or a mark's tile set** (criterion 45 stays valid). The engineer must re-run the marks and golden tests after the edit.

**Criteria status for the visual ones** (31 to 46 that need eyes): 32, 34, 37 to 41, 44 and 46 stay **unverified**. 42 and 44 are expected to fail as built (badge and reach letter), per the table. Nothing is marked met. 47 to 49 are not my part.

## Decisions already made

- D-003 (style, layering) and D-004 (code-drawn pictures) followed.
- **D-005 (new, accepted)**: TILE 28, explicit badge fonts, dark chips for badges and reach letters, player outline, lighter shade violet and thicker Gloom ring.

## Constraints

- Visual direction only. No rule, content, dependency, network or asset change. Palette stays at 11 colors (12 allowed); no red or orange main fill is added.
- The page must open from the file system. `scene.js` must stay pure and must not read `threat` or `reach`.

## Open questions

1. For QA and the screenshots: the board width at 28 px depends on `v.w`, which I could not read. If the board plus the 360 px panel does not fit a 1280 px window, use TILE 26. Report which one was used.
2. Do the reach border and the red border merge on a tile that has both (see the mark table)? A screenshot decides.
3. Do remembered wall and remembered floor merge? A screenshot decides (D-005 item 7).

## Expected output

1. The Studio routes D-005 to **gameplay-engineer**. The engineer edits `repo/src/page.js` (TILE, fonts, chips, backing) and `repo/src/pictures.js` (player outline with a `grow` flame parameter, `violet`, Gloom ring), and runs `node --test`. The engineer should not touch `scene.js` or mark logic.
2. Then run **shot** screenshots of `index.html` with scripts that show: r=6 and r=2 (criterion 36); a remembered area; each of the four creatures; a hound crouch line and a Gloom 3x3 area; reach marks on an item tile, on a lit brazier tile and on a stairs tile; a stunned creature; the player on `<`, on a lit brazier and on a plain floor; the inventory with items; and a reach tile inside a threat area. Add a greyscale view if possible.
3. Send the screenshots back to **art-director** for the final visual verdict, covering criteria 31 to 46 (visual part).

## Load

- Role: none, because the recipient is the Studio (routing). The next Role is gameplay-engineer, then art-director.
- Skills: none
- Project: design/entity-pictures.md, repo/src/pictures.js, repo/src/scene.js, repo/src/page.js, repo/index.html
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/07-studio-to-art-director.md
>>>END

<<<FILE goals/G-002-entity-pictures/08-qa-to-studio.md
---
kind: handoff
goal: G-002
seq: 8
from: qa
to: studio
stage: Verify
outcome: fail
---
# 08: qa → studio — verification of the entity pictures build (criteria 31 to 49): fail on 44, visual criteria not checkable

## Task

Route the result. One criterion (44) fails on a code-evident spec deviation. Most visual criteria could not be checked with my means. Studio decides: send the fix to `gameplay-engineer`, and get a real look at the page (screenshots or the Owner) before the Goal counts as done.

## Context

Goal G-002, build `repo/` sha ed0ad983accb. I verified against `design/entity-pictures.md` criteria 31 to 49 and regressions in 1 to 30. I did not change the repository. I did not use the implementer's assessment.

## Findings

### Means used

- `node --test` (round 1): exit 0, 69 tests, 69 pass, 0 fail. This is above the 49 required by criterion 48.
- `node play.js` with a 27-command script on seed 42 (round 1): exit 0. Frames are well-formed, refused commands are marked "(refused: no turn passed)", `Danger:` and `Legend:` lines are present, and the summary and empty-slot message work. I have no pre-change output to compare it with.
- Source reading of `page.js`, `scene.js`, `pictures.js`, `index.html`, `golden.test.js` and `hashes.json`.
- `shot` (round 1) **failed** on input format, not on the page: `keyboard.press: Unknown key: "dddd....ssss..dddd"`. The tool presses one key name per press, and my multi-key string was passed as a single key. I produced no screenshots and did not retry in this step. **I have no browser, no screenshot and no pixel output.** The only canvas-like means is the fake recording ctx in the Node tests (`pictures.test.js`).
- Code reading is not counted as a pass for any look or legibility criterion.

### What the fake ctx can and cannot show

It can show structure only: a picture exists per entity and pose, drawing stays inside the tile, drawing does not throw in either tone, the palette is small with no red or orange main fill, dim differs from full, silhouettes are not copies, and flame height grows per step. These tests pass.

It cannot show how anything looks: legibility, contrast against neighbours, greyscale distinction, brightness steps, mood, mark legibility on top of pictures, or console errors in a real browser.

I could not add my own test or tooling files in this step, because the only writable path was this handoff.

### Per-criterion result

| # | Result | How checked / evidence |
|---|---|---|
| 31 | not checkable (display) | Node: `scene` mapping table covers every terrain, stair, brazier, item and creature type, and each maps to a named picture (tests: scene full mapping table, one picture per entity and pose). Nobody has seen them on the page. |
| 32 | not checkable | Needs a viewer and greyscale. Node only shows that silhouettes are not copies. |
| 33 | not checkable (look) | In code the salve (jar with cross) and the oil flask (flask with gold cap) differ in shape. The lit brazier adds a gold flame to the same bowl. `<` and `>` differ in shape and color (blue and green). Visual confirmation is missing. |
| 34 | not checkable | Wall and floor are different colors in code, but contrast cannot be judged without a viewer. |
| 35 | not checkable, risk | See risk R1. |
| 36 | not checkable (visual), mapping ok | `flameFor` maps r = 6..2 to steps 5..1. Tests pass: five distinct, strictly increasing steps from real views, and flame height grows with every step. Two screenshots from one run were not possible. |
| 37 | not checkable (visual) | Code: the inventory button draws the same `P.draw` item picture on a 24 px canvas. An empty slot adds no icon. |
| 38 | not checkable (visual), logic ok | Code and test "memory: tone follows vis; unseen tiles get no request". Creatures come only from `v.creatures` (visible only). Dim palette is a separate function. |
| 39 | not checkable | All visible tiles use `full`, remembered use `dim`. The size of the difference needs a viewer. |
| 40 | not checkable (visual) | Visibility rules are untouched, and tests for checks 2 and visibility pass. No full-tone picture outside the visible set is produced by the scene mapping. |
| 41 | not checkable | Mood needs a viewer. Wall colors (up to `#6f6352`) are not near black, but unseen tiles are drawn black. |
| 42 | not checkable (visual) | Code: `page.js` draws a 3 px red border plus `!` for every `cr.threat`, after the creature picture, so the picture is not replaced. Recognisability inside the border is unchecked. See risk R2. |
| 43 | not checkable (visual) | Code: red tint at alpha 0.35 (under the 40% limit) plus a 3 px red border per marked cell, drawn after the terrain and item pictures and before the actors. Recognisability under the tint is unchecked. |
| 44 | **fail** | Spec section 5 requires the reach letter to have "a dark backing so it reads on any picture". `page.js` draws the letters (`#ffd070`, 10 px) directly on the 30% orange fill with **no backing**. This is code-evident, not a look judgement. On a lit-brazier tile (gold flame `#f0c640`) the letters will likely have low contrast; this needs a viewer to confirm. The dashed orange border and the letters are otherwise present. |
| 45 | pass at view level, not on the page | Test "criterion 45: scripted runs with a hound crouch, a Gloom gather, a flare and random walks" passes. I did not load its source, so I cannot say exactly what it compares. `scene.js` never decides a mark, and `page.js` draws marks from the same view fields as before. Marked tiles on the drawn canvas were not compared with the text output. |
| 46 | not checkable (visual) | Code: `crouching` hounds get their own picture (`hound-crouch`); `stunned` and `staggered` get a pale-blue wash plus a `z` or `~` badge. The threat border follows `cr.threat`, which the rules never set for stunned or staggered creatures. Test "wash only for stunned and staggered" passes. |
| 47 | not checkable (console) | Only local `<script src>` tags in classic order: `view`, `scene`, `pictures`, `page`. Test "scene.js and pictures.js use no DOM, network or Image" passes. A clean console on a real open was not observed. |
| 48 | pass, with limits (see below) | 7 of 7 golden tests pass (4 seeds × 250 commands, 3 scenarios). `node --test` passes 69 of 69. |
| 49 | not checkable | Code structure of the controls, key handling, click handling and summary screen in `page.js` looks unchanged apart from the inventory icons. Not exercised in a browser. |

### Criterion 48: is the golden test adequate? (open question 1)

Mostly yes, for what it covers:

- It hashes the full `renderRun` text of 7 runs (about 380 KB) and also checks the byte count.
- The 4 seeds × 250 commands plus the hound, Gloom and flare scenarios cover a wide range of frames.

What is missing:

- **Provenance.** I cannot verify that the hashes really were taken before the change. The baseline came from the same party that built the change, and I have no pre-change checkout to re-hash.
- **No `--trace` output** and no real `node play.js` CLI output (args and stdin paths) is hashed. The existing play.js tests only check that it runs and prints lines.
- **No diff on failure.** A mismatch shows two hashes only.
- **Unchanged files not diffed.** The claim that `textview.js`, `script.js` and `play.js` are untouched cannot be checked from the packet.

Recommended: a hashed `--trace` case, one CLI-level case, and a failure message that prints the first differing line (by storing the expected text in a git-ignored fixture, or by hashing per command).

### Regressions, criteria 1 to 30 (open question about regression)

Checks 1 to 25 (rules, text output, generator, bots) are covered by named tests in the round-1 run, all passing, including the strict check 14 (damage events: threat 105 and reach 114 in the 20-seed run) and check 26. The rules and view files are stated as untouched; I cannot verify that from the packet. The text player ran correctly in my play run. Check 27 (page contents), 28 (controls), 29 (visible versus remembered, distinguishable types, marks, brazier lit/unlit) and 30 (summary screens) need a browser. **Regression statement: no regression found in 1 to 26; not checkable in 27 to 30.**

### Risks seen in the code (not confirmed visually)

- **R1 (criterion 35).** The player body is `blue` (`#6f9fd0`), the same color as the `<` stairs. The player flame is `gold`, the same color as the lit-brazier flame. Standing on `<` or a lit brazier, parts of the player picture may blend into the picture below. The pale head and the flame size still help. Needs a screenshot.
- **R2 (criterion 42, edge case).** The threat `!` badge is drawn at `cr.y - 0.55` tiles, i.e. centered on the creature tile's top edge with a 16 px font. Half of it lies on the tile above, and for a creature in row 0 half is clipped. It is not a corner badge. It may overlap the reach letters or the picture of a neighbour tile to the north. Needs a screenshot.
- **R3 (minor).** The picture inset is 4 px on 22 px tiles (about 18%), not the 10% in the spec. The code takes `max(10%, border + 1)` so the 3 px border stays free. This looks intended and consistent with the spec's rule on small tiles, but it is a deviation from "about 10%".
- The tile size is 22 px, above the 20 px threshold in open question 2 of the spec.

### Verdict

**fail**: criterion 44 fails on the missing letter backing. No other criterion is shown to fail. About 14 criteria (31 to 43, 46, 47, 49) are not checkable with my means, so the change cannot count as verified. Passing: 45 (view level only) and 48 (with limits).

## Decisions already made

- D-002: threat marks plus reach marks. D-003: flat dark-cave pictures, marks always over pictures (the letter backing comes from the spec's section 5, not from a decision). D-004: pictures drawn by code, pure scene mapping.

## Constraints

- I verified from the spec and the build only.
- I changed no repository file.
- I did not decide intended look or behaviour.

## Open questions

1. Studio: route the fix for 44 (draw a dark backing behind the reach letters) to `gameplay-engineer`. This is the first failure of this criterion, so no technical-director escalation yet.
2. Studio: get the page seen. Options are a corrected `shot` run (one key name per press, whatever separator the tool wants) or the Owner. The screenshots should cover:
   - a fresh frame at r = 6, and at r = 2;
   - the player on `<` and on a lit brazier (R1);
   - a threat border and `!` badge on a creature in row 0 and below another marked tile (R2);
   - a reach mark on an item tile and on a lit brazier;
   - a crouch line and a Gloom area over items;
   - a stunned creature;
   - the inventory with a salve and an oil flask;
   - the browser console on first load.
3. Engineer or Art Director: decide whether R1 and R2 need picture or badge changes once seen.
4. Is the golden test enough for 48? Accepted as a pass with the limits listed above. Strengthening it is optional.

## Expected output

The Studio routes the 44 fix to `gameplay-engineer`, then a second QA pass with screenshots. Success: every criterion in 31 to 49 is marked pass, or a stated not-checkable with a named reason that the Owner accepts.

## Load

- Role: none (addressed to studio); QA role for the re-verification: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, repo/src/scene.js, repo/tests/golden.test.js, repo/tests/golden/hashes.json, build (`node --test`, `node play.js {script}`, screenshots of `index.html`)
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
- Previous handoff: goals/G-002-entity-pictures/06-studio-to-qa.md
>>>END

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/README.md
- repo/index.html
- repo/manual.md
- repo/play.js
- repo/src/floorgen.js
- repo/src/game.js
- repo/src/light.js
- repo/src/page.js
- repo/src/pictures.js
- repo/src/rng.js
- repo/src/scenario.js
- repo/src/scene.js
- repo/src/script.js
- repo/src/textview.js
- repo/src/view.js
- repo/tests/bot.js
- repo/tests/bots.test.js
- repo/tests/creatures.test.js
- repo/tests/floors.test.js
- repo/tests/g001-final.test.js
- repo/tests/gloom.test.js
- repo/tests/golden/hashes.json
- repo/tests/golden.test.js
- repo/tests/helpers.js
- repo/tests/marks.test.js
- repo/tests/pic-helpers.js
- repo/tests/pictures.test.js
- repo/tests/reach.test.js
- repo/tests/rules.test.js
- repo/tests/scene.test.js
- repo/tests/view.test.js
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

## Your answer

- Write the outgoing Handoff as goals/G-002-entity-pictures/11-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
