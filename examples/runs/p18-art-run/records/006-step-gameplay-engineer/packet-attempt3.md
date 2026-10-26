# Studio operation packet

operation: Step
goal: G-002
role: gameplay-engineer
incoming_handoff: goals/G-002-entity-pictures/04-technical-director-to-gameplay-engineer.md
next_seq: 5
runs: tests, trace (2 rounds left; results in @run-results)
run_tests: node --test
run_trace: node play.js --trace {script}
context_request: used (the requested files are in Inputs)

## You may write

- goals/G-002-entity-pictures/05-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

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

<<<FILE goals/G-002-entity-pictures/04-technical-director-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 4
from: technical-director
to: gameplay-engineer
stage: Build
outcome: routed
---
# 04: technical-director → gameplay-engineer — build the entity pictures as planned

## Task

Implement `design/entity-pictures.md` (criteria 31 to 49) on the browser page following the plan below and D-004. Do not change rules, balance, content, marks or the text player. Write the build notes as a Handoff addressed to `studio`; QA and the Art Director verify next.

## Context

Goal G-002. The Owner asked for a picture for each of them (「それぞれに絵をつけてほしい」). The Art Director's spec is done (13 entities, flat dark-cave style, D-003). I have settled the method questions here so you do not have to decide them. Nobody has seen the page, and neither can I. This plan is based on reading `page.js`, `view.js`, `textview.js` and `index.html`.

## Findings

**Facts from the code**

- `page.js` draws on one canvas with `TILE = 22`. Terrain is a filled square; terrain, items and creatures are letters. Remembered tiles use `globalAlpha` 0.38.
- Marks today:
  - a threat tile (from `cell.threat`) gets a 35% red tint plus a 2 px red border;
  - a creature with `threat` gets a 2 px red border and a `!`;
  - a reach tile gets a 30% orange tint, a 2 px dashed orange border and a 10 px creature-letter text.
- The page already reads only `view()` output: `cells[y][x]` (`terrain`, `item`, `vis`, `seen`, `threat`, `reach`), `creatures` (`type`, `state`, `threat`, `x`, `y`), `reach`, `player`, `radius`. That is all the pictures need. No change to `view.js`, `game.js`, `light.js` or `textview.js` is needed or allowed.
- A creature shown only because it is orthogonally adjacent through a wall (spec 9) can stand on a tile with `vis` false. Draw every shown creature at full tone anyway; creatures are never dimmed.

**Plan: approach (answers to your open questions)**

1. *How pictures are made.* Code-drawn vector pictures on the canvas, no image files or data URIs (D-004). This works from `file://` and cannot raise a blocked-resource error.
2. *Where the mapping lives.* New `repo/src/scene.js`, pure and UMD, namespace `EmberHollow.scene`.
   - API: `scene.build(view)` returns `{ tiles: [...], actors: [...], flame: n }`, plain data only.
   - Tile requests are `{x, y, terrain, item, tone}` with `tone` = `full` or `dim`.
   - Actor requests are `{x, y, picture, wash}`:
     - `picture` is one of `player, moth, shade, hound, hound-crouch, gloom`;
     - `wash` is `true` for `stunned`/`staggered`;
     - the hound pose comes from `state === 'crouching'`.
   - Flame step: table r 6..2 to a size step 5..1.
   - It never writes to `view`, never decides a mark, and does not look at `threat` or `reach` (marks stay in `page.js`).
3. *Drawing.* New `repo/src/pictures.js`, UMD, namespace `EmberHollow.pictures`. `draw(ctx, name, px, py, size, tone, opts)` draws one picture in the square at (px, py). It has a fixed palette of at most 12 colors, a `dim(color)` function that makes the remembered palette, and `drawFlame(ctx, ..., step)`.
   - Authoring grid is 16x16, scaled by `size`.
   - Picture inset from the tile edge: `max(round(0.1*size), border + 1)`, which is 4 px at TILE 22 (a 14 px picture). Reason: the spec's 10% margin (2.2 px) would collide with a 3 px border.
   - Red and orange are never a picture's main color; the flame is yellow-gold. Creature silhouettes must differ in shape (greyscale rule).
4. *Remembered tiles and flame.* Done in code at draw time (see D-004). No stored copies.
5. *Page changes (`page.js`, `index.html` only).*
   - Add `<script src="src/scene.js">` and `<script src="src/pictures.js">` after `view.js` and before `page.js`.
   - In `render()`, draw in the D-003 order per tile: terrain picture, then item/brazier picture, then the existing area tint (`cell.threat`), then the existing reach tint/border/letters, then creatures and the player (the player flame follows `scene.flame`), then threat borders and `!` badges.
   - Stunned or staggered creatures get a pale-blue wash plus a small state badge, and never a red border (view already sets `threat` false for them; keep it that way).
   - The mark set drawn must stay exactly as today. Mark *styling* may change only as below.
   - Inventory slots: keep each button's text (`[1] salve`) and add a small `<canvas>` item icon (same drawing function) inside the button. An empty slot gets no icon. Keep the click handler.
   - Keep `TILE` a single constant, used for drawing and for the click mapping.
6. *Mark width.* The spec asks for a threat border of at least 3 px. Today it is 2 px. Make the threat border 3 px (inset 1.5 px so it stays on the tile edge). Keep the reach border dashed orange at its current width. A change of mark colors, shapes or positions is not in scope; report if you think one is needed.
7. *Tile size.* Keep `TILE = 22`. Report it in the build notes with the mark styling, listing what the page actually draws after your change. If you conclude that `TILE < 20` or that pictures at the chosen size cannot be told apart, do not shrink the spec yourself: stop and hand back to `art-director` via `studio` (outcome `question`). Raising `TILE` (e.g. to 28) is a one-constant change; if you do it, state it in the notes so QA can compare.

**Files to change or add**

- Add `repo/src/scene.js`, `repo/src/pictures.js`.
- Edit `repo/index.html` (two script tags) and `repo/src/page.js` (render and inventory).
- Add tests next to the existing tests (follow how `node --test` finds them today) and golden text files under a `golden/` folder beside them.
- Update `repo/manual.md` with one short paragraph on the pictures (legend). Do not touch the text-frame description.
- Do not edit `game.js`, `light.js`, `floorgen.js`, `rng.js`, `view.js`, `textview.js`, `play.js`.

**Tests (all via `node --test`)**

- *Golden text (criterion 48).* Before any other change, run `node play.js` on at least 4 scripts and save the output byte for byte as golden files. The scripts should include a moth fight, a brazier, a hound crouch and a Gloom gather (find seeds by running; use `--trace` to locate them). Add a test comparing current output to the golden files. Also keep the 49 existing tests passing.
- *Mapping tables (31, 33, 35, 46).* `scene.build` gives a distinct picture name for each entity E1 to E13 and each hound pose. A test fixes the full table: terrain/item/brazier/stairs/creature type/state to picture. Test that stunned and staggered set `wash`, and that nothing else does.
- *Flame (36).* Steps for r = 6..2 are five distinct, strictly increasing values. Test with two real view models from one run (E in 80..100 and E in 1..19).
- *Memory (38, 40).* In a scene built from a real view: `vis` false gives `dim`; `vis` true gives `full`; `seen` false gives no request; no creature request on a tile that is not in `view.creatures`.
- *Pictures change no mark (45).* Build the view for scripted runs (at least 3, including a hound crouch and a Gloom gather) turn by turn. Check that `JSON.stringify(view)` is identical before and after `scene.build`, and that the page's marked set is the text player's: derive the page set from the same view fields `page.js` draws marks from (`cell.threat`, `creature.threat`, `reach`), and compare to the `!`, `?` chars and creature `!` lines in `renderFrame`. The comparison code should be a small shared function used by the test, written to mirror the draw code; keep the mark-drawing path in `page.js` to those fields only.
- *Drawing (47, 41).* Run every picture with a recording fake ctx, at TILE 22: no throw, every call lands inside the tile, the number of distinct colors across all pictures is at most 12 plus the dimmed set, no picture uses a red or orange main fill (check the largest-area fill color against hue ranges), a `dim` render differs from a `full` render for the same picture, and no network, DOM or `Image` is used (the module loads in Node with no globals).

**What cannot be checked without a viewer** (say so in the notes; do not claim it)

- That the pictures look like a moth, shade, hound, Gloom and so on (32), and the greyscale test.
- That wall and floor are told apart at a glance, and that items and creatures stand out (34).
- That visible tiles look clearly brighter than remembered ones, including at the glow edge (39), that the cave looks dark and the warmest spots are the flame and lit braziers (41).
- That a threat border, hound line, Gloom area and reach mark stay recognisable over the lightest and busiest pictures (42 to 44), and that a stunned creature does not read as a threat (46).
- That `index.html` opens with no console error (47), that controls and summary screens work, and that clicking a tile or slot works (28, 30, 49).
- The first look at the page itself.

All of these are for QA and the Art Director with screenshots or live viewing.

**Sequencing (sequential, one engineer)**

1. Capture the golden text outputs. Confirm `node --test` passes 49/49.
2. `scene.js` with its tests.
3. `pictures.js` with its tests. Start with the creature silhouettes (the hardest to tell apart), then braziers, items, stairs, terrain, player and flame.
4. Wire `page.js` and `index.html`. Re-run all tests.
5. Write the build notes.

**Parallelization decision:** none, and no isolated workspaces. The work is small, `page.js` is the single integration point, and `scene.js` and `pictures.js` share a naming contract (picture names). A split would cost more in merging than it saves. Pictures could be drawn in parallel by several workers only if a later Goal adds many more entities.

**Risks and mitigations**

- *Pictures at 14 px are too crude to tell apart.* Mitigation: 16-unit design grid, silhouettes designed first, a one-constant tile size, hand-back to the Art Director on `TILE < 20` or on a picture you cannot make distinct.
- *A picture hides a mark.* Mitigation: fixed draw order, marks drawn last from unchanged fields, simplify the picture on conflict (D-003), mark-set test.
- *State label strings.* I have not seen `game.js`. Check the exact strings `planAction` returns (`crouching`, `stunned`, `staggered` per spec 4) by running a script, and fix the table in `scene.js` to them. Do not change the labels.
- *Text output drift.* Mitigation: do not edit `textview.js` or `play.js`; golden test.
- *Dim colors look muddy.* Mitigation: one `dim()` function, so it can be tuned in one place; QA/Art Director review.
- *Page code cannot be run here.* Any unexercised line in `page.js` is a risk. Keep `page.js` changes thin and move logic into `scene.js` and `pictures.js`.

**Flags:** the spec is feasible within the constraints. Nothing is irreversible. The cost fits the Goal. No hand-back to Design is needed now.

## Decisions already made

- D-001: classic-script UMD modules; rules code has no drawing. Followed by `scene.js` and `pictures.js`.
- D-002: threat and reach marks; unchanged.
- D-003: style, reserved colors, layering, same marked set on page and in text.
- D-004 (new, accepted): pictures drawn by code on the canvas; pure `scene.js` mapping; dim palette and flame steps made in code.

## Constraints

- No rule, balance or content change; no change to `game.js`, `light.js`, `floorgen.js`, `rng.js`, `view.js`, `textview.js`, `play.js`.
- Text player output byte-identical; `node --test` passes (at least the present 49 tests plus yours).
- No dependencies, no network, no server, no image files, no ES modules, no `window`/`document` outside `page.js`.
- Checks 1 to 30 stay in force.
- Mark positions, colors and meaning stay as they are, except the threat border width becoming 3 px.

## Open questions

For you to answer in the notes:

1. The tile size you ended up with, and the mark styling the page actually draws after your change (colors, widths, tints, badges).
2. The exact state labels found for the hound crouch, stunned and staggered.
3. Any picture you could not make distinct at the chosen size (hand back to `art-director` via `studio` if so).
4. Whether you raised `TILE`, and why.

## Expected output

Code and tests as above, then a Handoff `goals/G-002-entity-pictures/05-gameplay-engineer-to-studio.md` with `to: studio`, `stage: Build`. The notes list: files changed, the test results (count of tests and what each group checks), the golden scripts used, the answers to the open questions, the criteria 31 to 49 that tests cover (and how), and plainly which criteria nobody has checked because they need someone to see the page. QA and the Art Director verify next. Do not claim any visual criterion as met.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#current-state, design/entity-pictures.md, design/game-spec.md, repo/manual.md, repo/index.html, repo/src/page.js, repo/src/view.js, repo/src/textview.js, repo/src/game.js
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
- Previous handoff: goals/G-002-entity-pictures/03-studio-to-technical-director.md
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

<<<FILE project.md#current-state
## Current state

After G-001 (partly met): `repo/` holds a build with five floors, ember, three creature types,
the Gloom and seeded runs; rules are shared by the page and the text player (D-001); threats
and reach are marked (D-002). Design docs are in `design/` (30 acceptance checks).
`node --test` passes 49/49.

Run it: open `repo/index.html` (browser); `node play.js {script}` (add `--trace` for state);
`node --test`. Script format and player info: `repo/manual.md`.

Not verified: the browser page (checks 27-30) has been seen by no one. No whole run has been
observed: Play covered only seed 42, floor 1, 16 turns. Floors 2-5, braziers, items, hounds,
shades, Gloom, win/loss, run length and balance are unobserved. QA did not see per-test
results for checks 13, 14 (hand-made) and 26.

Known weakness: old messages stay in later frames (spec's "last 5"), so new events are hard
to tell from old.

Proposed next Goals: (1) Owner checks the page; (2) QA full test listing; (3) broad playtest
and balance; (4) message legibility.
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

<<<FILE design/game-spec.md
# Ember Hollow: game spec for the first complete run (G-001)

## 1. Intent

The player descends five floors with one ember. The ember is light and time. A brighter ember sees farther but burns the same per turn, and braziers are the only refill, so every detour for light or an item is paid for in ember. Each creature reacts to light in its own way. Every threat that can hurt the player on the next turn is already visible, with a visible warning when it is not simply adjacent. One run takes 15 to 30 minutes and ends in a win (the Gloom on floor 5 is defeated) or a loss.

This document is player-facing behavior only. The code structure, the script format and the rendering technology belong to the build. Numbers use Manhattan distance (|dx|+|dy|) unless stated otherwise.

## 2. The grid and turns

- Square tiles. Tile types: wall, floor, stairs up `<` (arrival point), stairs down `>`, brazier. Items and creatures sit on floor tiles.
- Movement and attacks are 4-directional (N, E, S, W). There are no diagonal moves or attacks. The one exception is the Gloom's slam area (section 7).
- The game is turn-based. One **turn** is: the player acts, then the effects of the action resolve, then the ember dims, then the creatures act in creature-id order (the order they were placed on the floor).
- Nothing depends on real time. All randomness comes from the run seed.

### Player actions (each takes exactly one turn unless stated)

| Action | Effect |
|---|---|
| Move | Step onto an adjacent walkable tile. Moving onto a brazier, an item or the down stairs triggers its effect (below). Moving into a wall does nothing and costs no turn. |
| Fight | Moving toward an adjacent creature attacks it instead of moving. It takes 2 damage. The player has no ranged attack. |
| Wait | Stay in place. It costs a turn and ember like any other action. |
| Use item | Use the item in an inventory slot (section 6). A refused use (see section 6) costs no turn. |

- Player HP is 12 at the start of the run. It carries across floors and has no natural regeneration.
- Ember carries across floors. A new floor does not refill it.
- Stairs down: stepping onto `>` ends the turn. The ember dims by 1 as normal, then the next floor starts with the player on its `<`. Creatures on the new floor do not act on the arrival turn. There is no going back up.

## 3. Ember and light

- **Ember value E**: integer 0 to 100. The run starts at E = 100.
- **Dimming**: after every turn in which the player acted (move, wait, fight, item use), E decreases by 1. Near the Gloom (see section 7), E decreases by 2.
- **Glow radius r** is a function of E:

| E | r |
|---|---|
| 80–100 | 6 |
| 60–79 | 5 |
| 40–59 | 4 |
| 20–39 | 3 |
| 1–19 | 2 |
| 0 | the run ends |

- **Visible tiles**: a tile is visible when it is within the glow (dx²+dy² ≤ (r+0.5)²) and a straight line of sight from the player to it is not blocked by a wall. Tiles next to the player are always visible. Because r is never below 2, every orthogonally adjacent tile and every tile at Manhattan distance 2 in a straight clear line is always visible.
- **Remembered tiles**: terrain, stairs, braziers and items that were seen stay on the map, drawn visibly dimmer than currently visible tiles. Creatures are shown only while visible, never from memory.
- **Brazier**: an unlit brazier is on each floor as a tile. When the player moves onto it:
  1. E = min(100, E + 60) (this happens before that turn's dimming).
  2. The brazier becomes lit and stays lit. A lit brazier has no further effect and can be walked over.
  3. **Flare**: every non-boss creature within Manhattan distance 7 that is visible after the rekindle is stunned for 2 turns. A stunned creature skips its next 2 actions, and a crouching hound's crouch is cancelled. The first skipped action is the one in the lighting turn's own creature phase, the second is in the next turn. The creature is labelled "stunned" in the frame after the lighting turn and acts again in the creature phase of the second turn after the lighting turn.
- **The ember goes out**: if E is 0 after the dimming, the run ends at once with the cause "The ember went out". Creatures do not act on that turn. The defeat of the Gloom on the same turn counts as a win, because the player's action resolves first.
- **Reading the ember**: the screen always shows E (number and bar), the current r, and the dimming rate ("dims 1/turn" or "dims 2/turn"). A message is shown when E first falls to 20, 10 and 5 or below, and when r shrinks ("Your light shrinks").

## 4. Creatures

General rules:
- Each creature either **moves one tile or acts, never both** in one turn, except the hound lunge (which is telegraphed one turn before).
- A creature cannot enter a tile with the player, another creature, a wall, a brazier, or stairs.
- "Toward the player" means one step along a shortest walkable path (ties broken in the order N, E, S, W). If no path exists or no step is free, the creature stays put.
- Creatures on a floor start where the floor generator places them (section 8) and do not follow the player downstairs.
- A creature whose HP reaches 0 is removed at once and does not act again.
- Visible creatures show their name or letter, HP, and state (idle, hunting, fleeing, crouching, stunned, staggered). A creature that can hurt the player on its next action is marked as a threat (see section 9).

| Creature | Letter | HP | Damage | Floors |
|---|---|---|---|---|
| Cave moth | `m` | 2 | 1 | 1–4 |
| Shade | `s` | 4 | 2 | 2–5 |
| Ash hound | `h` | 4 | 3 | 3–5 |
| The Gloom | `G` | 24 | 4 | 5 |

### Cave moth (reaction to light: drawn to it)
- If the shortest walkable path distance to the player is ≤ r + 3, it moves toward the player each turn. A brighter ember draws moths from farther away. Otherwise it stays still.
- If adjacent to the player at the start of its action, it attacks for 1 damage instead of moving.
- It teaches: brightness draws attention, and weak enemies can be fought in the open.

### Shade (reaction to light: fears bright light, strikes when it is dim)
- **While r ≥ 3** (E ≥ 20): a shade that is visible flees. It moves one step that increases its path distance from the player, or stays if there is none (cornered). A cornered shade adjacent to the player attacks for 2 damage. A shade that is not visible moves toward the player if its path distance is ≤ 12, so shades hover at the edge of the light and drift in and out of sight.
- **While r = 2** (E ≤ 19): shades are no longer afraid. Each shade moves toward the player, and attacks for 2 damage once adjacent at the start of its action.
- Because it moves or attacks and not both, a shade that steps adjacent can attack only on its next action. The player sees it adjacent first.
- It teaches: keep the ember up, and corner or leave shades when bright.

### Ash hound (reaction to light: ignores glow size, but a flare stuns it)
- Idle until the shortest path distance to the player is ≤ 6, then it hunts: moves one tile toward the player each turn.
- **Bite**: if adjacent at the start of its action, it attacks for 3 damage.
- **Lunge** (telegraphed): when a hound is at Manhattan distance exactly 2 in a straight row or column with an empty floor tile between it and the player, it **crouches** instead of moving, and shows a crouch mark and the line it threatens. On its next action it lunges: it moves up to 2 tiles along the line toward the player. If the player is still within 2 tiles in that line, the hound ends adjacent and the player takes 3 damage. If the player has left the line or is farther, the hound just moves up to 2 tiles toward the player and does not bite that turn. A lunge that cannot move (blocked) deals no damage. If the player stands directly adjacent to the hound when it acts, the hound simply bites for 3 (the adjacent-bite rule applies, and the line is irrelevant). "Blocked" means a wall or another creature stops the hound before it ends adjacent to the player.
- The crouch is always visible when it starts (distance 2 in a clear line), so the player always gets one turn to step out of the line, back away, or strike it first.
- It teaches: sidestep the line, or fight it from a corner.

## 5. Floors

- 5 floors. Floors 1–4 have `<` and `>`. Floor 5 has `<` and the boss arena, and no `>`.
- Floor sizes (tiles, width × height) and contents:

| Floor | Size | Creatures | Braziers | Items |
|---|---|---|---|---|
| 1 | 28 × 16 | 4 moths | 2 | 1 salve, 1 oil |
| 2 | 30 × 18 | 3 moths, 2 shades | 2 | 1 salve, 1 oil |
| 3 | 32 × 18 | 2 moths, 3 shades, 1 hound | 2 | 1 salve, 1 oil |
| 4 | 34 × 20 | 2 moths, 3 shades, 3 hounds | 2 | 1 salve, 1 oil |
| 5 | 30 × 18 | the Gloom, 2 shades, 1 hound | 3 (in the arena) | 1 salve, 1 oil |

- **Layout** is made of rooms joined by corridors (floors 1–4: 5 to 8 rooms; floor 5: a start room, a corridor, and a single open arena room of at least 14 × 10 tiles holding the Gloom and the 3 braziers). All walkable tiles are connected, so every item, brazier and exit is reachable by walking.
- **Stairs**: the shortest walking distance from `<` to `>` is at least 30 steps on floors 1–3 and at least 40 on floor 4. Floor 5 has the arena entrance at least 20 steps from `<`.
- **Braziers**: at least one brazier on each floor 1–4 is within 25 walking steps of `<`. The other is at least 10 steps from the first. Braziers are not on the shortest path from `<` to `>` for both of them (at least one needs a detour).
- **Creatures** are placed on floor tiles, at least 6 walking steps from `<`, not on items. The Gloom stands at the far end of the arena, at least 8 steps from the arena entrance.
- **Items** are on floor tiles, not on stairs or braziers, and at least one item per floor is not on the shortest path from `<` to `>`.
- **Seed**: a run is determined by its seed (an integer or text; the build defines how it is chosen). Floor n's layout, brazier positions, items and starting creature positions depend only on the seed and n, never on what the player did earlier. The same seed and the same commands always give the same run. Different seeds give different layouts (at least 9 of any 10 different seeds give different floor 1 layouts). The seed is always shown to the player.

## 6. Items

Inventory: 4 slots, one item per slot, items are picked up by walking onto them.

| Item | Effect |
|---|---|
| Salve | Restores 5 HP (up to 12). Refused with a message, at no cost, if HP is already 12. |
| Oil flask | Restores 30 ember (up to 100). Refused with a message, at no cost, if E is already 100. The effect happens before that turn's dimming. |

- Walking onto an item with a full inventory leaves the item on the floor and shows a message. The move still costs a turn.
- Using an item takes one turn, so creatures act.

## 7. Floor 5: the Gloom

The Gloom (`G`) keeps the hollow dark. It is a single 1-tile creature with 24 HP. It never leaves the arena unless pulled (it stalks the player if the player is in the arena, otherwise it stays).

- **Darkness drain**: while the Gloom is alive and within Manhattan distance 4 of the player at the end of a turn, the ember dims by an extra 1 that turn (2 total). The HUD shows "dims 2/turn" while this applies.
- **Cycle** (one state per turn):
  1. **Stalk**: while the player is not within Manhattan distance 2, it moves one tile toward the player each turn.
  2. **Gather** (telegraph): when the player is within Manhattan distance 2 at the start of its action, it stops and marks every tile in the 3×3 area around itself (diagonals included). It does not move this turn. The marked area stays visible.
  3. **Slam**: on its next action it deals 4 damage to the player if the player stands in the marked area, then becomes **staggered**.
  4. **Staggered**: for the next 3 turns it does nothing, and attacks against it deal 4 damage instead of 2. Then it returns to Stalk.
- The player can always avoid a slam: from any tile in the 3×3 area, one step in a straight line leaves it, unless walls block every such step.
- The Gloom is not stunned by flares. It is outside the 'non-boss creatures' rule.
- Because r is at least 2, the Gloom's gather is always visible when it starts (the player is within distance 2).
- **Win**: when the Gloom's HP reaches 0 the run ends in victory immediately, before the ember dims.

## 8. End of run

Three end states. Each shows a summary screen (browser) or summary lines (text output) with: the result, floor reached, turns taken, creatures defeated, final HP, final ember, and the seed.

| End | Trigger | Message |
|---|---|---|
| Victory | Gloom reaches 0 HP | "The Gloom breaks. Light returns to the hollow." |
| Dead | Player HP reaches 0 (checked after the creatures act) | "You fell on floor N." |
| Ember out | E reaches 0 after dimming | "The ember went out on floor N." |

- If HP 0 and ember 0 would both occur in one turn, "The ember went out" applies, because the ember check comes first and creatures never act.
- After an end state, no further commands change the game. The player can start a new run: same seed, or a new seed.

## 9. What the player can tell (screen contents)

The game is shown as a grid (browser page) and as text (`node play.js`). Both must give the same information:

1. **Map**: walls, floor, `<`, `>`, braziers (unlit vs. lit distinguishable), items (salve vs. oil distinguishable), the player, and visible creatures (type distinguishable). Visible tiles are clearly brighter than remembered tiles; unseen tiles are blank.
2. **Ember**: E as a number and a bar, the glow radius r, and the dimming rate.
3. **Health**: HP as current/12.
4. **Floor and turn**: floor number out of 5, and the number of turns taken.
5. **Inventory**: 4 slots, each showing the item or empty, with its key.
6. **Creatures**: for each visible creature, its type, HP, state, and position.
7. **Threats and reach** (decision D-002): all marks use the ember value the creatures will see, that is the current E minus this turn's dimming (1, or 2 near the Gloom). That E decides r, and so whether a shade is afraid.
   - **Threat mark**: a visible creature that can hurt the player at its next action, with the player where they stand now, is marked: an adjacent moth, an adjacent hound, a shade that is adjacent and either cornered or while r = 2, a crouching hound with its line, and the Gloom's marked area. The mark appears the same turn the threat becomes real (in text, e.g. `!`; in the browser, a visibly different highlight).
   - **Reach mark**: for each of the four orthogonal neighbour tiles the player could move onto, the screen shows which visible creatures would hurt the player at their next action if the player ended the turn on that tile (creatures themselves staying where they are). In text this is a line such as `Danger: N (m), E (h)`; in the browser, the tile gets a highlight and the creature letter. A tile that is a wall, holds a creature, or is the down stairs gets no reach mark (stairs end the turn with no creature phase). An unlit brazier tile gets no reach mark from creatures the flare stuns (every visible non-boss creature in range 7), but it does get one from the Gloom, which a flare does not stun. A lit brazier has no flare and is marked like a floor tile. The reach mark uses the same rules as the threat mark. It is a different display, not a different rule.
   - Every creature that is orthogonally adjacent to the player, or to a neighbour tile the player could move onto, is shown even if a wall blocks the line of sight to it, so a creature that can hurt the player after one step is never hidden.
   - Nothing that is unmarked on the tile where the player ends the turn can hurt the player next turn. A creature that only moves closer and cannot attack yet (for example a moth at distance 2) is not marked. It is seen adjacent, and marked, on the next turn.
8. **Messages**: the last 5 messages (attacks with damage, picked items, brazier lit, shrinking light, ember low, end of run).
9. **Seed**: shown at all times.

### Controls (browser)

- Keyboard: arrow keys or WASD to move or fight; `.` or Space to wait; `1`–`4` to use the item in that slot; `R` to restart with the same seed; `N` to start a new run with a new seed.
- Mouse: clicking an orthogonally adjacent tile moves or fights; clicking an inventory slot uses it; a Wait button; buttons for restart and new seed.
- Only the player's actions advance the game. Opening the page requires no server and no network.

## 10. Run shape

- Target: 15 to 30 minutes, which at an average of 2 to 4 seconds per decision is about 250 to 700 player turns.
- Ember supply: 100 at the start plus 11 braziers × 60 = 760 in total on offer, plus 5 oil flasks × 30. A direct walk uses about 40 turns per floor; a normal run with fights, detours and the boss fight is expected to use 300 to 600 turns, so ember is tight but not hopeless when the player lights about half of the braziers.
- Tuning is a first estimate. The Play step is expected to report where it is too easy or too hard, so numbers can be revised in the spec.

## 11. Edge cases and rules for simultaneous events

- Several creatures acting in one turn: in creature-id order. A creature killed earlier in the same turn (for example by the player) does not act.
- Creature phase and the ember out: the ember check comes before the creatures act, so a turn that empties the ember is never decided by creature damage.
- Descending with a stunned or adjacent creature: it does not follow.
- A lunging hound stopped by another creature: it moves as far as it can along the line; it bites only if it ends adjacent with the player still in the line.
- A brazier tile or the stairs can never be occupied by a creature, so a creature never blocks stairs or braziers.
- A flare stuns only creatures visible after the rekindle (radius computed from the new E), within Manhattan distance 7.
- Stunned or staggered creatures are still shown, labeled with their state, and not marked as a threat.
- Using an oil flask at a brazier tile cannot happen on the same turn (a move onto a brazier is the turn's action).
- A salve or oil flask used at 12 HP / 100 E is refused at no cost.
- A full inventory leaves the item where it lies.
- Fight on a creature that is at distance 1 diagonally is not possible (no diagonal actions).
- Marks and the player's step: the threat mark describes staying (Wait) or an action that does not move the player (a fight, an item use). The reach marks describe a move onto a neighbour tile. In both cases the damage a creature does in the creature phase was announced in the output before the action by the mark on the tile where the player ended the turn (D-002).
- A shade at E = 20 is still afraid now, but a Wait or step costs 1 E, so the creature phase sees E = 19 and r = 2. Its marks are already shown as a strike. Marks are computed from the E after dimming for this reason.

## 12. Out of scope

Saving, meta-progression, sound, mobile layouts, ranged player attacks, keys/doors, traps, more creatures or items than listed.
>>>END

<<<FILE repo/manual.md
# Ember Hollow: manual

You carry one ember down five floors. The ember is your light **and** your time: it loses 1 each turn you act
(2 while the Gloom is within 4 tiles). Braziers refill it (+60, once each). At 0 the run ends. Reach floor 5
and break the Gloom to win.

## Playing in the browser

Open `index.html` from the file system (no server needed).

- Arrow keys / WASD: move, or fight an adjacent creature (2 damage). `.` or Space: wait. `1`-`4`: use the item in that slot.
- `R`: restart with the same seed. `N`: new run with a new seed. Or type a seed in the box and press Start.
- Mouse: click an orthogonally adjacent tile to move or fight; click an inventory slot to use it; buttons for Wait, Restart, New seed.
- The seed is always shown. The same seed always gives the same floors. `index.html#my-seed` starts with the seed `my-seed`.
- Red marks (threat marks) show what can hurt you at its next action if you stay or fight (an adjacent biter, a crouching hound's line, the Gloom's gathered area).
- Dashed orange tiles with creature letters (reach marks) are the neighbour tiles where a visible creature would hurt you if you stepped there. The line `Danger: N (m), E (h)` under the map lists the same.

## Playing / scripting in text: `node play.js [--trace] <script>`

A script is a text file. `#` starts a comment (so a seed cannot contain `#`).

- The first non-comment line may be `seed <integer or text>`. No seed line means the default seed `hollow`.
- Every other non-space character is one command (spaces and newlines are only for readability):

| Char | Command |
|---|---|
| `w` `a` `s` `d` | move or fight north / west / south / east |
| `.` | wait |
| `1` `2` `3` `4` | use the item in that slot |

Example:

```
seed 42
dddd ss  # walk east, then south
..       # wait twice
```

`node play.js script.txt` prints the frame after every command; `-` reads the script from stdin.
`--trace` adds, per command, each creature's id, position, state, intent and path distance, the threats marked
before the action, the events with damage sources, E and the drain rate. Each damage line gives `case=threat` (the player
did not move) or `case=reach` (the player stepped onto a neighbour tile), `visibleBefore`, and `markedBefore`: whether the
creature was shown in the previous frame with the threat mark (threat) or the reach mark on the tile where the player ended
the turn (reach), per D-002. A command refused with no cost
(a wall, an item refused at full HP/E, an empty slot) prints its frame with "(refused: no turn passed)".
After an end state the summary lines are printed and later commands are ignored.

## Reading a frame

```
Floor 1/5 | Turn 12 | HP 12/12
Ember 87/100 [#################---] r=6 | dims 1/turn
Items: [1] salve  [2] empty  [3] empty  [4] empty
```

Map symbols: `@` you, `#` wall, `.` visible floor, `<` `>` stairs, `B` unlit brazier, `b` lit brazier, `+` salve, `o` oil,
`m` moth, `s` shade, `h` hound, `G` the Gloom. Remembered tiles are dimmer: `,` floor and `%` wall in text (terrain, stairs,
braziers and items stay shown). Unseen tiles are blank. Creatures are drawn only while visible.
`!` on the map marks a tile that is part of a marked danger (hound line, Gloom area). In the creature list a line starting
with `!` is a threat that can hurt you at its next action, with the reason.
`?` on the map marks a **reach mark**: a neighbour tile where stepping would get you hurt at the creatures' next action.
Under the map the line `Danger: N (m), E (h, s)` lists, per direction N/E/S/W, the creature letters that would hurt you if
you ended the turn on that neighbour tile (`Danger: none` when no step is marked). A wall, a tile holding a creature, the
down stairs never get a reach mark. An unlit brazier gets none from creatures the flare stuns, but does get one from the Gloom (not stunned) if it would hurt you there. Reach marks use the same planner as the creatures and the same ember
as they will see (current E minus this turn's dimming).
The last five messages and the seed are always printed.

## Rule readings the build chose (where the spec leaves room)

1. **Drain distance**: the Gloom's Manhattan distance is measured after the player's action (the player's position at the end of their half of the turn), before the creatures move.
2. **Path distance** (moth trigger r+3, hound 6, shade 12, "toward the player"): walking distance over all non-wall tiles, ignoring creatures. A creature's step must be a free floor tile (never a wall, brazier, stairs, the player or another creature); if the only shortest-path step is blocked it stays.
3. **Flare stun**: stunned = 2 skipped actions, counted from the creature phase of the lighting turn itself. A stunned creature is therefore labelled "stunned" in the frame after the lighting turn, skips its action in the lighting turn's own creature phase (first skipped action) and in the next turn (second), and acts in the creature phase of the second turn after the lighting turn (the third turn, counting the lighting turn as the first). Ratified by the game designer.
4. **Hound lunge**: with the player directly adjacent in the crouch line when it springs (the player stepped toward it), it bites for 3. A lunge blocked before it ends adjacent deals no damage. The hound hunts whenever the path distance is <= 6 (no memory of having hunted).
5. **Empty item slot**: using an empty slot is refused at no cost, with a message. Refused actions only add a message; turn, E, HP and position do not change.
6. **Threat marks** come from the same planner the creatures act with. Marked: an attack at the next action (adjacent moth/hound, shade that is cornered or at r=2), a crouched hound (always, with its line), the Gloom once it has gathered (with its area). A hound that is about to crouch is not marked yet. Stunned or staggered creatures are never marked.
   Marks and creature states use the ember after this turn's dimming (D-002), so at E = 20 a Wait beside a shade already shows the strike.
7. **Shade visibility** ("a visible shade flees") uses the visibility after the player's action and that turn's dimming.
8. Descending never triggers creature actions. A creature never follows.
9. **Reach marks** (D-002) are computed with `planAction` and a hypothetical player position (E after the dimming at that tile, visibility and path distances from that tile). A crouched hound counts only if the tile is on its line, within 2, and the tiles between are free. A creature orthogonally adjacent to the player or to a neighbour tile is listed even if a wall blocks line of sight.
10. **Lit brazier** (ratified by the game designer): the spec says "a brazier tile gets none" because of the flare. A lit brazier has no flare, so it gets reach marks like a floor tile; otherwise strict check 14 could not hold there.

## Not covered by this build

Saving, sound, mobile layout. Balance is a first estimate and unverified.
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
<script src="src/page.js"></script>
</body>
</html>
>>>END

<<<FILE repo/src/page.js
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
>>>END

<<<FILE repo/src/view.js
/* view(state): the render model shared by play.js and the page (spec 9). UMD-style (D-001).
   Marks (D-002) use the ember as it will be after this turn's dimming, and come from the same
   planner the creatures act with (planAction), evaluated with a hypothetical player position. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./light.js'); require('./game.js'); }
  var L = EH.light, G = EH.game;

  var DAMAGING = { attack: true, lunge: true, slam: true };
  var DIR_ORDER = ['N', 'E', 'S', 'W'];

  function manh(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); }

  // Shallow copy of the state with the player moved (planAction only reads).
  function withPlayer(s, pos) {
    var o = {};
    Object.keys(s).forEach(function (k) { o[k] = s[k]; });
    o.player = { x: pos.x, y: pos.y };
    return o;
  }

  // Planner context for "the player ends the turn on pos": E after that turn's dimming.
  // null when the ember would be out (creatures do not act).
  function hypo(s, pos, base) {
    var s2 = withPlayer(s, pos), e = Math.max(0, (base === undefined ? s.ember : base) - G.drainRate(s2));
    if (e <= 0) return null;
    var r = L.radiusFor(e);
    return { s: s2, ctx: { dist: G.bfsFromPlayer(s2), vis: L.visibleGrid(s.floorData, pos.x, pos.y, r), r: r } };
  }

  function occupied(s, x, y) {
    return s.creatures.some(function (c) { return c.hp > 0 && c.x === x && c.y === y; });
  }

  // Damage the creature would do to s2.player at its next action given its planned intent (0 = none).
  function hurtsAt(s2, c, it) {
    var p = s2.player, i;
    if (it.kind === 'attack') return it.damage;
    if (it.kind === 'slam') return Math.max(Math.abs(p.x - c.x), Math.abs(p.y - c.y)) <= 1 ? it.damage : 0;
    if (it.kind === 'lunge') {
      var dv = G.DIRS[c.dir], k = 0;
      for (i = 1; i <= 2; i++) if (p.x === c.x + dv[0] * i && p.y === c.y + dv[1] * i) k = i;
      if (!k) return 0;
      for (i = 1; i < k; i++) {
        var x = c.x + dv[0] * i, y = c.y + dv[1] * i;
        if (L.tileAt(s2.floorData, x, y) !== '.' || occupied(s2, x, y)) return 0;
      }
      return 3;
    }
    return 0;
  }

  function view(s) {
    var fd = s.floorData, w = fd.w, h = fd.h, E = s.ember, r = L.radiusFor(E), pl = s.player;
    var vis = L.visibleGrid(fd, pl.x, pl.y, r);
    var litSet = {}, itemAt = {}, tt = {}, rk = {}, creatures = [], threats = [], reach = [], x, y;
    s.lit.forEach(function (k) { litSet[k] = 1; });
    s.items.forEach(function (it) { itemAt[it.x + ',' + it.y] = it.type; });

    // Neighbour tiles the player could step onto (not walls).
    var nbs = [];
    DIR_ORDER.forEach(function (d) {
      var dv = G.DIRS[d], nx = pl.x + dv[0], ny = pl.y + dv[1];
      if (L.tileAt(fd, nx, ny) !== '#') nbs.push({ dir: d, x: nx, y: ny });
    });

    // Shown creatures: visible ones, plus any orthogonally adjacent to the player or a neighbour tile.
    var shown = s.creatures.filter(function (c) {
      if (c.hp <= 0) return false;
      if (vis[c.y * w + c.x]) return true;
      if (manh(c, pl) === 1) return true;
      return nbs.some(function (n) { return manh(c, n) === 1; });
    });

    var cur = s.end ? null : hypo(s, pl);
    var planS = cur ? cur.s : s, planCtx = cur ? cur.ctx : { dist: G.bfsFromPlayer(s), vis: vis, r: r };

    shown.forEach(function (c) {
      var it = G.planAction(planS, c, planCtx), th = !!cur && !!DAMAGING[it.kind], reason = null;
      if (th) {
        if (it.kind === 'attack') reason = 'hits for ' + it.damage + ' at its next action';
        else if (it.kind === 'lunge') reason = 'crouched: lunges along the marked line for 3';
        else reason = 'slam on the marked area for ' + it.damage;
        (it.line || it.area || []).forEach(function (t) { tt[t.x + ',' + t.y] = 1; });
      }
      var cv = { id: c.id, type: c.type, letter: G.DEFS[c.type].letter, name: G.DEFS[c.type].name,
        hp: c.hp, maxHp: c.maxHp, x: c.x, y: c.y, state: it.label, threat: th, reason: reason };
      creatures.push(cv);
      if (th) threats.push(cv);
    });

    // Reach marks (D-002): per neighbour tile, which shown creatures would hurt the player there.
    // None on walls, creature tiles or the down stairs. An unlit brazier is lit by the step (E+60 first) and the
    // flare stuns every stunnable creature there, so only the Gloom (not stunned) is evaluated on it.
    nbs.forEach(function (n) {
      var t = fd.tiles[n.y].charAt(n.x);
      var unlit = t === 'B' && !litSet[n.x + ',' + n.y];
      if (s.end || t === '>' || occupied(s, n.x, n.y)) return;
      var hp = hypo(s, n, unlit ? Math.min(100, s.ember + 60) : undefined);
      if (!hp) return;
      var list = [];
      shown.forEach(function (c) {
        if (unlit && c.type !== 'gloom') return;
        var dmg = hurtsAt(hp.s, c, G.planAction(hp.s, c, hp.ctx));
        if (dmg) list.push({ id: c.id, letter: G.DEFS[c.type].letter, damage: dmg });
      });
      if (list.length) {
        reach.push({ dir: n.dir, x: n.x, y: n.y, creatures: list });
        rk[n.x + ',' + n.y] = list.map(function (e) { return e.letter; });
      }
    });

    var cells = [];
    for (y = 0; y < h; y++) {
      var row = [];
      for (x = 0; x < w; x++) {
        var seen = !!(s.seen[y][x] || vis[y * w + x]), k = x + ',' + y, ch = fd.tiles[y].charAt(x), terrain = null;
        if (seen) terrain = ch === '#' ? 'wall' : ch === '<' ? 'up' : ch === '>' ? 'down'
          : ch === 'B' ? (litSet[k] ? 'lit' : 'brazier') : 'floor';
        row.push({ terrain: terrain, item: seen && itemAt[k] ? itemAt[k] : null, vis: !!vis[y * w + x], seen: seen,
          threat: !!(tt[k] && vis[y * w + x]), reach: rk[k] || [] });
      }
      cells.push(row);
    }
    return {
      seed: s.seed, floor: s.floor, floors: G.FLOORS, turn: s.turn, hp: s.hp, maxHp: G.MAX_HP,
      ember: E, radius: r, dim: G.drainRate(s), inv: s.inv.slice(), w: w, h: h, cells: cells,
      player: { x: pl.x, y: pl.y }, creatures: creatures, threats: threats, reach: reach,
      messages: s.messages.slice(), end: s.end
    };
  }

  EH.view = { view: view, visibleGrid: L.visibleGrid, radiusFor: L.radiusFor };
  if (typeof module === 'object' && module.exports) module.exports = EH.view;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/textview.js
/* Text renderer for the view model (play.js and tests). UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  function bar(E) {
    var n = Math.round(E / 5);
    return '[' + new Array(n + 1).join('#') + new Array(21 - n).join('-') + ']';
  }

  function cellChar(c) {
    if (!c.seen) return ' ';
    switch (c.terrain) {
      case 'wall': return c.vis ? '#' : '%';
      case 'up': return '<';
      case 'down': return '>';
      case 'brazier': return 'B';
      case 'lit': return 'b';
    }
    if (c.item) return c.item === 'salve' ? '+' : 'o';
    if (c.threat) return '!';
    if (c.reach && c.reach.length) return '?';
    return c.vis ? '.' : ',';
  }

  // Reach marks: "N (m), E (h, s)" = stepping N is met by a moth, stepping E by a hound and a shade.
  function dangerText(v) {
    var parts = (v.reach || []).map(function (rc) {
      return rc.dir + ' (' + rc.creatures.map(function (c) { return c.letter; }).join(', ') + ')';
    });
    return parts.length ? parts.join(', ') : 'none';
  }

  function renderFrame(v) {
    var out = [], x, y;
    out.push('Ember Hollow | seed: ' + v.seed);
    out.push('Floor ' + v.floor + '/' + v.floors + ' | Turn ' + v.turn + ' | HP ' + v.hp + '/' + v.maxHp);
    out.push('Ember ' + v.ember + '/100 ' + bar(v.ember) + ' r=' + v.radius + ' | dims ' + v.dim + '/turn');
    out.push('Items: ' + v.inv.map(function (it, i) { return '[' + (i + 1) + '] ' + (it || 'empty'); }).join('  '));
    var grid = [];
    for (y = 0; y < v.h; y++) { var row = []; for (x = 0; x < v.w; x++) row.push(cellChar(v.cells[y][x])); grid.push(row); }
    v.creatures.forEach(function (c) { grid[c.y][c.x] = c.letter; });
    grid[v.player.y][v.player.x] = '@';
    grid.forEach(function (r) { out.push(r.join('').replace(/\s+$/, '')); });
    out.push('Danger: ' + dangerText(v));
    out.push('Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered');
    out.push('Creatures:' + (v.creatures.length ? '' : ' none in sight'));
    v.creatures.forEach(function (c) {
      out.push('  ' + (c.threat ? '! ' : '  ') + c.letter + '#' + c.id + ' ' + c.name + ' HP ' + c.hp + '/' + c.maxHp +
        ' ' + c.state + ' at (' + c.x + ',' + c.y + ')' + (c.threat ? ' THREAT: ' + c.reason : ''));
    });
    out.push('Messages:' + (v.messages.length ? '' : ' none'));
    v.messages.forEach(function (m) { out.push('  - ' + m); });
    if (v.end) {
      out.push('');
      out.push('=== ' + v.end.message + ' ===');
      out.push('Result: ' + ({ victory: 'Victory', dead: 'Dead', ember: 'Ember out' })[v.end.result]);
      out.push('Floor reached: ' + v.end.floor + '/' + v.floors);
      out.push('Turns: ' + v.end.turns);
      out.push('Creatures defeated: ' + v.end.defeated);
      out.push('Final HP: ' + v.end.hp + '/' + v.maxHp);
      out.push('Final ember: ' + v.end.ember);
      out.push('Seed: ' + v.end.seed);
    }
    return out.join('\n');
  }

  function renderTrace(e) {
    var out = [];
    out.push('[trace] command ' + e.n + ' (' + JSON.stringify(e.cmd) + ') turn ' + e.turn + ' consumed=' + e.consumed +
      ' E=' + e.ember + ' drain=' + e.drain + '/turn');
    e.plans.forEach(function (p) {
      out.push('[trace]   creature #' + p.id + ' ' + p.type + ' at (' + p.x + ',' + p.y + ') state=' + p.label +
        ' intent=' + p.intent + ' pathdist=' + p.dist);
    });
    out.push('[trace]   threats before action: ' + (e.threatsBefore.length ? e.threatsBefore.map(function (t) {
      return '#' + t.id + ' ' + t.type + ' (' + t.reason + ')';
    }).join('; ') : 'none'));
    out.push('[trace]   events: ' + (e.events.length ? e.events.map(function (x) { return JSON.stringify(x); }).join(' ') : 'none'));
    e.damage.forEach(function (d) {
      out.push('[trace]   damage ' + d.amount + ' from #' + d.src + ' ' + d.type + ' visibleBefore=' + d.visibleBefore +
        ' case=' + d.case + ' markedBefore=' + d.markedBefore);
    });
    out.push('[trace]   no random numbers are drawn during play');
    return out.join('\n');
  }

  EH.textview = { renderFrame: renderFrame, renderTrace: renderTrace };
  if (typeof module === 'object' && module.exports) module.exports = EH.textview;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/game.js
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
>>>END

<<<FILE decisions/D-001-classic-scripts-shared-rules.md
---
kind: decision
id: D-001
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-26
supersedes: none
---
# D-001: Shared code is plain classic-script modules (UMD style), not ES modules

## Decision

All code under `repo/src/` that both `play.js` and the page use is written as classic scripts with a small UMD wrapper. In Node it exports with `module.exports`. In the browser it attaches to one global namespace, `EmberHollow`. `repo/index.html` loads the files with ordinary `<script src="src/...">` tags in dependency order. No `import`/`export` syntax and no bundler anywhere in `repo/`. Only the page's own UI code (`repo/src/page.js`) is browser-only. The rules code never touches `window`, `document`, `Date`, `Math.random` or any other real-time or environmental input.

## Rationale

`repo/index.html` must open from the file system. Browsers block `<script type="module">` files loaded over `file://` (origin and CORS rules), so ES modules would break the one requirement the Owner stated. Classic scripts work from `file://` and under Node 20 without a build step, and they keep the "no dependencies" constraint.

## Alternatives considered

- ES modules: rejected because they fail on `file://`.
- A bundler or a generated single file: rejected because it adds a build step and a tool dependency, and the generated file would drift from the sources.
- Duplicating the rules for the page: rejected because the constraint requires shared rules code.

## Revisit when

The project gains a server, or a build step is allowed by the constraints.
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

<<<FILE goals/G-002-entity-pictures/03-studio-to-technical-director.md
---
kind: handoff
goal: G-002
seq: 3
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 03: studio → technical-director — plan how to build the entity pictures

## Task

Write a technical plan for implementing the picture spec `design/entity-pictures.md` (criteria 31 to 49) on the browser page, and settle the method questions below so the Gameplay Engineer can build without deciding them.

## Context

Goal G-002. The Owner said 「それぞれに絵をつけてほしい」; the Studio read it as a picture for each kind of thing on the floor grid. The Art Director has finished the Design step: 13 entities (player with ember flame, cave moth, shade, ash hound in two poses, the Gloom, unlit and lit brazier, salve, oil flask, wall, floor, `<`, `>`), a flat dark-cave style (D-003), light and memory rules, and a fixed layering of marks over pictures. The Art Director advised a Plan because the method is risky. Nobody has seen the browser page, and your means may not show it either.

## Findings

From the Art Director's handoff (`02-art-director-to-studio.md`):

- Unseen tiles stay blank; remembered tiles are dimmer with the same shapes; creatures are never drawn from memory; visible tiles share one brightness inside the glow.
- Flame size on the player follows the ember radius r (criterion 36).
- Layering: threat border and badge on top of the creature; hound line and Gloom area are tints under the creature; reach border and letter over the tile picture; stunned or staggered creatures get a pale-blue wash and no red.
- The marked set on the page must equal the text player's (criterion 45).
- Existing checks 27 to 30 are refined or re-checked; checks 1 to 26 are untouched. The text player output must stay byte-identical (criterion 48).
- Tile size and current mark styling are unknown. The 10% inner margin and the 3 px border may not fit small tiles; below about 20 px per tile the Art Director wants to be consulted again.

## Decisions already made

- D-001: shared code is plain classic-script modules (UMD style); rules code stays free of drawing.
- D-002: threat marks plus reach marks on the four neighbour tiles.
- D-003: flat dark-cave pictures; marks always drawn over pictures; warm light reserved for the ember; red and orange reserved for marks.

## Constraints

- No rule, balance or content changes; the text player and its output unchanged; `node --test` must still pass.
- No dependencies, no network; the page opens from `file://` without a server.
- Rules code stays shared and separate from drawing (D-001).
- Checks 1 to 30 stay in force.

## Open questions

Decide, and record a Decision (`make-decision`) if one constrains later work or rejects a real alternative:

1. How pictures are made and stored: separate image files, drawing by code (canvas), inline vector, or embedded data. Which works from `file://` in the page as built.
2. Where the entity-and-state to picture mapping lives, so that it reads the same state the marks use and cannot alter a mark or a rule.
3. How remembered (dimmed) tiles and flame sizes are produced: in code, or stored.
4. How to check pictures with the means available: which criteria can be tested by `node --test` (for example mapping tables, marked-set equality, byte-identical text output) and which need someone to see the page. Say plainly which cannot be checked without a viewer.
5. Whether the build should report tile size and the current mark styling, and what the engineer must do if tiles are too small (hand back to the Art Director).
6. Sequencing, and whether any part can be built in parallel. Parallel code workspaces only if you decide it is worth it.

If the spec turns out infeasible within the constraints, hand back for Design (`game-designer` or `art-director`) instead of choosing for them.

## Expected output

A plan in Findings of your outgoing Handoff: approach, files to change, tests, risks, and sequencing. Set `to: gameplay-engineer` (Build). In Expected output for the engineer, ask that the build notes address the result to `studio`, since QA and the Art Director verify next. If the spec is infeasible, or a direction or scope change is needed, route per your Role contract.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md, studio/skills/make-decision.md
- Project: project.md#constraints, project.md#current-state, design/entity-pictures.md, design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, repo/index.html, repo/src/page.js, repo/src/view.js, repo/src/textview.js
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md
- Previous handoff: goals/G-002-entity-pictures/02-art-director-to-studio.md
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
- repo/src/rng.js
- repo/src/scenario.js
- repo/src/script.js
- repo/src/textview.js
- repo/src/view.js
- repo/tests/bot.js
- repo/tests/bots.test.js
- repo/tests/creatures.test.js
- repo/tests/floors.test.js
- repo/tests/g001-final.test.js
- repo/tests/gloom.test.js
- repo/tests/helpers.js
- repo/tests/reach.test.js
- repo/tests/rules.test.js
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

<<<FILE repo/tests/helpers.js
'use strict';
const G = require('../src/game.js');
const V = require('../src/view.js');
const S = require('../src/scenario.js');
const L = require('../src/light.js');
const FG = require('../src/floorgen.js');
const SC = require('../src/script.js');

const A = {
  wait: { type: 'wait' },
  N: { type: 'move', dir: 'N' }, E: { type: 'move', dir: 'E' }, S: { type: 'move', dir: 'S' }, W: { type: 'move', dir: 'W' }
};
const use = (n) => ({ type: 'use', slot: n });
function run(s, ...acts) { let st = s; for (const a of acts) st = G.step(st, a).state; return st; }
const cr = (s, id) => s.creatures.find((c) => c.id === id);
const world = S.fromAscii;

module.exports = { G, V, S, L, FG, SC, A, use, run, cr, world };
>>>END

<<<FILE repo/tests/reach.test.js
'use strict';
// D-002 / checks 14 and 29: threat marks and reach marks, strict form.
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, world } = require('./helpers.js');
const TV = require('../src/textview.js');

const reachOf = (v, dir) => { const e = v.reach.find((r) => r.dir === dir); return e ? e.creatures.map((c) => c.letter) : []; };

test('reach: a step next to a moth shows a reach mark before the step', () => {
  const v = V.view(world(['#@.m.#']));
  assert.deepEqual(reachOf(v, 'E'), ['m']);
  assert.equal(v.threats.length, 0);
  const text = TV.renderFrame(v);
  assert.match(text, /Danger: E \(m\)/);
  const s = G.step(world(['#@.m.#']), A.E);
  assert.equal(s.state.hp, 11);
});

test('reach: a step next to a hound shows a reach mark; the hound is not a threat while the player stays', () => {
  const v = V.view(world(['#@.h.#']));
  assert.deepEqual(reachOf(v, 'E'), ['h']);
  assert.equal(v.threats.length, 0);
  assert.equal(G.step(world(['#@.h.#']), A.E).state.hp, 9);
});

test('reach: a step next to a shade at r=2 shows a reach mark', () => {
  const s = world(['#@.s.#'], { ember: 19 });
  assert.deepEqual(reachOf(V.view(s), 'E'), ['s']);
  assert.equal(G.step(s, A.E).state.hp, 10);
});

test('threat: a Wait at E=20 beside a shade is already a strike; at E=21 it is not', () => {
  const a = world(['#@s..#'], { ember: 20 });
  assert.equal(V.view(a).threats.length, 1);
  assert.equal(G.step(a, A.wait).state.hp, 10);
  const b = world(['#@s..#'], { ember: 21 });
  assert.equal(V.view(b).threats.length, 0);
  assert.equal(G.step(b, A.wait).state.hp, 12);
});

test('reach: no mark on an unlit brazier or the down stairs; a lit brazier is marked', () => {
  assert.deepEqual(reachOf(V.view(world(['#@Bm.#'])), 'E'), []);
  assert.deepEqual(reachOf(V.view(world(['#@>m.#'])), 'E'), []);
  assert.deepEqual(reachOf(V.view(world(['#@Bm.#'], { lit: [[2, 0]] })), 'E'), ['m']);
});

test('reach: no mark on walls or on a tile holding a creature', () => {
  const v = V.view(world(['#@m.#']));
  assert.deepEqual(reachOf(v, 'E'), []);
  assert.deepEqual(reachOf(v, 'W'), []);
  assert.deepEqual(reachOf(v, 'N'), []);
});

test('text frame: reach tiles are drawn with ? and differ from the threat glyph', () => {
  const text = TV.renderFrame(V.view(world(['#@.m.#'])));
  assert.ok(text.split('\n').some((l) => l.startsWith('#@?m')), text);
});

function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ACTS = [A.N, A.E, A.S, A.W, A.wait];

test('check 14 (strict): every damage event was shown and marked on the tile where the player ended the turn', (t) => {
  const counts = { threat: 0, reach: 0 };
  for (let i = 0; i < 20; i++) {
    let st = G.newRun('c14-' + i);
    const rnd = lcg(i + 7);
    for (let n = 0; n < 600 && !st.end; n++) {
      const before = V.view(st);
      const res = G.step(st, ACTS[rnd() % 5]);
      const moved = res.state.floor === st.floor && (res.state.player.x !== st.player.x || res.state.player.y !== st.player.y);
      for (const e of res.events.filter((x) => x.t === 'damage')) {
        const where = 'seed c14-' + i + ' command ' + n + ' creature #' + e.src + ' ' + e.type;
        if (moved) {
          const p = res.state.player;
          const rc = before.reach.find((r) => r.x === p.x && r.y === p.y);
          assert.ok(rc && rc.creatures.some((c) => c.id === e.src), 'no reach mark: ' + where);
          counts.reach++; t.diagnostic('reach  ' + where);
        } else {
          assert.ok(before.threats.some((c) => c.id === e.src), 'no threat mark: ' + where);
          counts.threat++; t.diagnostic('threat ' + where);
        }
      }
      st = res.state;
    }
  }
  t.diagnostic('damage events: threat ' + counts.threat + ', reach ' + counts.reach);
});

test('sampled states: threat flags equal what the planner does with the ember after dimming', () => {
  for (let i = 0; i < 6; i++) {
    let st = G.newRun('mark-' + i);
    const rnd = lcg(i + 31);
    for (let n = 0; n < 200 && !st.end; n++) {
      const v = V.view(st);
      const after = Math.max(0, st.ember - G.drainRate(st));
      const s2 = Object.assign({}, st, { ember: after });
      for (const cv of v.creatures) {
        const c = st.creatures.find((o) => o.id === cv.id);
        const it = G.planAction(s2, c, G.makeCtx(s2));
        const expect = after > 0 && (it.kind === 'attack' || it.kind === 'lunge' || it.kind === 'slam');
        assert.equal(cv.threat, expect, 'seed mark-' + i + ' command ' + n + ' creature #' + cv.id);
      }
      st = G.step(st, ACTS[rnd() % 5]).state;
    }
  }
});
>>>END

<<<FILE repo/tests/gloom.test.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, run, cr, world } = require('./helpers.js');

const rows = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};

test('check 15: the Gloom has 24 HP; within 4 the ember loses 2 and the HUD says dims 2/turn', () => {
  let s = world(rows(1, 5), { floor: 5 });
  assert.equal(cr(s, 1).hp, 24);
  assert.equal(V.view(s).dim, 2);
  s = run(s, A.wait); assert.equal(s.ember, 98);
  const far = world(rows(1, 6), { floor: 5 });
  assert.equal(V.view(far).dim, 1);
  assert.equal(run(far, A.wait).ember, 99);
});

test('check 16: gather marks 3x3 for one turn; the next turn deals 4 inside, 0 outside', () => {
  // player outside the area (distance 2)
  let s = run(world(rows(2, 4), { floor: 5 }), A.wait);
  assert.equal(cr(s, 1).gathering, true);
  const v = V.view(s);
  assert.equal(v.cells[1][3].threat, true); assert.equal(v.cells[3][5].threat, true);
  assert.equal(v.creatures[0].threat, true);
  s = run(s, A.wait);
  assert.equal(s.hp, 12); assert.equal(cr(s, 1).staggered, 3);
  // player inside the area (adjacent)
  s = run(world(rows(3, 4), { floor: 5 }), A.wait, A.wait);
  assert.equal(s.hp, 8); assert.equal(cr(s, 1).staggered, 3);
});

test('check 17: staggered for 3 turns doing nothing; hits deal 4 then, 2 otherwise', () => {
  let s = world(rows(3, 4), { floor: 5 });
  s.creatures[0].staggered = 3;
  const hit = run(s, A.E);
  assert.equal(cr(hit, 1).hp, 20);
  const w = run(s, A.wait, A.wait, A.wait);
  assert.equal(cr(w, 1).staggered, 0); assert.equal(w.hp, 12); assert.equal(cr(w, 1).x, 4);
  assert.equal(cr(w, 1).gathering, false);
  assert.equal(cr(run(world(rows(3, 4), { floor: 5 }), A.E), 1).hp, 22);
});

test('check 18: killing the Gloom wins at once, before dimming, with the summary', () => {
  const s0 = world(rows(3, 4), { floor: 5, ember: 3 });
  s0.creatures[0].hp = 2;
  const s = run(s0, A.E);
  assert.equal(s.end.result, 'victory');
  assert.equal(s.end.message, 'The Gloom breaks. Light returns to the hollow.');
  assert.equal(s.ember, 3);                                   // no dimming on the winning turn
  assert.equal(s.end.turns, 1); assert.equal(s.end.defeated, 1); assert.equal(s.end.floor, 5);
  assert.equal(s.end.seed, 'scenario');
});
>>>END

<<<FILE repo/tests/view.test.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, L, FG, world } = require('./helpers.js');
const TV = require('../src/textview.js');

test('visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2', () => {
  for (const seed of ['vis-1', 'vis-2']) for (const n of [1, 3]) {
    const f = FG.generateFloor(seed, n);
    for (let y = 1; y < f.h - 1; y++) for (let x = 1; x < f.w - 1; x++) {
      if (f.tiles[y].charAt(x) === '#') continue;
      const vis = L.visibleGrid(f, x, y, 2);
      for (const [dx, dy] of [[0, -1], [1, 0], [0, 1], [-1, 0]]) {
        assert.equal(vis[(y + dy) * f.w + x + dx], 1, 'adjacent ' + x + ',' + y);
        const tx = x + 2 * dx, ty = y + 2 * dy;
        if (tx >= 0 && ty >= 0 && tx < f.w && ty < f.h && f.tiles[y + dy].charAt(x + dx) !== '#') {
          assert.equal(vis[ty * f.w + tx], 1, 'distance 2 ' + x + ',' + y);
        }
      }
    }
  }
});

test('visibility: walls block line of sight; the glow is circular', () => {
  const s = world(['#@.#.#']);
  const vis = L.visibleGrid(s.floorData, 1, 0, 6);
  assert.equal(vis[2], 1); assert.equal(vis[3], 1); assert.equal(vis[4], 0);
  const f = world(['#'.repeat(20), '#@' + '.'.repeat(17) + '#', '#'.repeat(20)]).floorData;
  const g = L.visibleGrid(f, 1, 1, 2);
  assert.equal(g[1 * 20 + 3], 1); assert.equal(g[1 * 20 + 4], 0);
});

test('check 9.1-9.9: the text frame shows every item of spec section 9', () => {
  const s = world(['#@..m.#', '#######'], { inv: ['salve', null, 'oil', null] });
  const text = TV.renderFrame(V.view(s));
  for (const needle of ['seed: scenario', 'Floor 1/5', 'Turn 0', 'HP 12/12', 'Ember 100/100', 'r=6', 'dims 1/turn',
    '[1] salve', '[2] empty', '[3] oil', '[4] empty', 'Creatures:', 'Cave moth', 'Messages:', '@']) {
    assert.ok(text.includes(needle), 'missing: ' + needle);
  }
});

test('view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not)', () => {
  const adj = V.view(world(['#@m.#']));
  assert.equal(adj.creatures[0].threat, true);
  assert.match(TV.renderFrame(adj), /! m#1/);
  assert.equal(V.view(world(['#@.m#'])).creatures[0].threat, false);
});
>>>END

<<<FILE repo/src/scenario.js
/* Hand-made states for tests. Rows: # wall, . floor, @ player, < > stairs, B brazier,
   m s h G creatures (ids in row-major order), + salve, o oil. UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') require('./game.js');
  var G = EH.game;
  var TYPES = { m: 'moth', s: 'shade', h: 'hound', G: 'gloom' };

  function fromAscii(rows, opts) {
    opts = opts || {};
    var h = rows.length, w = rows[0].length, tiles = [], spawns = [], items = [], braziers = [], start = null, stairs = null;
    for (var y = 0; y < h; y++) {
      var line = '';
      for (var x = 0; x < w; x++) {
        var ch = rows[y].charAt(x) || '#', t = '.';
        if (ch === '#' || ch === ' ') t = '#';
        else if (ch === '@') start = { x: x, y: y };
        else if (ch === '<') { t = '<'; if (!start) start = { x: x, y: y }; }
        else if (ch === '>') { t = '>'; stairs = { x: x, y: y }; }
        else if (ch === 'B') { t = 'B'; braziers.push({ x: x, y: y }); }
        else if (TYPES[ch]) spawns.push({ type: TYPES[ch], x: x, y: y });
        else if (ch === '+') items.push({ x: x, y: y, type: 'salve' });
        else if (ch === 'o') items.push({ x: x, y: y, type: 'oil' });
        line += t;
      }
      tiles.push(line);
    }
    var fd = { w: w, h: h, tiles: tiles, start: start, stairsDown: stairs, braziers: braziers, items: items,
      creatureSpawns: spawns, rooms: [], arena: opts.arena || { x0: 1, y0: 1, x1: w - 2, y1: h - 2 } };
    var s = G.newRunFromFloor(opts.seed || 'scenario', fd, opts.floor || 1);
    if (opts.ember !== undefined) s.ember = opts.ember;
    if (opts.hp !== undefined) s.hp = opts.hp;
    if (opts.inv) s.inv = opts.inv.slice();
    if (opts.lit) opts.lit.forEach(function (p) { s.lit.push(p[0] + ',' + p[1]); });
    G.updateSeen(s);
    return s;
  }

  EH.scenario = { fromAscii: fromAscii };
  if (typeof module === 'object' && module.exports) module.exports = EH.scenario;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/script.js
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
>>>END

<<<FILE repo/src/light.js
/* Glow radius and visibility (spec 3). UMD-style, D-001. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  // Spec 3 table.
  function radiusFor(E) {
    if (E >= 80) return 6;
    if (E >= 60) return 5;
    if (E >= 40) return 4;
    if (E >= 20) return 3;
    if (E >= 1) return 2;
    return 0;
  }

  function tileAt(fd, x, y) {
    if (x < 0 || y < 0 || x >= fd.w || y >= fd.h) return '#';
    return fd.tiles[y].charAt(x);
  }

  // Bresenham line; intermediate tiles (not the endpoints) must not be walls.
  function los(fd, x0, y0, x1, y1) {
    var dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
    var sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    var err = dx - dy, x = x0, y = y0;
    for (;;) {
      if (x === x1 && y === y1) return true;
      var e2 = 2 * err;
      if (e2 > -dy) { err -= dy; x += sx; }
      if (e2 < dx) { err += dx; y += sy; }
      if (x === x1 && y === y1) return true;
      if (tileAt(fd, x, y) === '#') return false;
    }
  }

  // Grid (w*h array of 0/1) of tiles visible from (px,py) with glow radius r:
  // dx^2+dy^2 <= (r+0.5)^2 and a clear line of sight.
  function visibleGrid(fd, px, py, r) {
    var w = fd.w, h = fd.h, grid = new Array(w * h);
    for (var i = 0; i < grid.length; i++) grid[i] = 0;
    var R = r + 0.5, R2 = R * R, m = Math.ceil(R);
    for (var y = py - m; y <= py + m; y++) {
      for (var x = px - m; x <= px + m; x++) {
        if (x < 0 || y < 0 || x >= w || y >= h) continue;
        var dx = x - px, dy = y - py;
        if (dx * dx + dy * dy > R2) continue;
        if (los(fd, px, py, x, y)) grid[y * w + x] = 1;
      }
    }
    grid[py * w + px] = 1;
    return grid;
  }

  EH.light = { radiusFor: radiusFor, tileAt: tileAt, los: los, visibleGrid: visibleGrid };
  if (typeof module === 'object' && module.exports) module.exports = EH.light;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/play.js
#!/usr/bin/env node
'use strict';
// Usage: node play.js [--trace] <script-file | ->    (format: see manual.md)
const fs = require('fs');
const SC = require('./src/script.js');

const USAGE = 'Usage: node play.js [--trace] <script-file | ->\nSee manual.md for the script format.';

function main(argv) {
  let trace = false;
  const files = [];
  for (const a of argv.slice(2)) {
    if (a === '--trace') trace = true;
    else if (a === '-h' || a === '--help') { console.log(USAGE); return 0; }
    else files.push(a);
  }
  if (files.length !== 1) { console.error(USAGE); return 2; }
  let text;
  try { text = files[0] === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(files[0], 'utf8'); }
  catch (e) { console.error('Cannot read script: ' + e.message); return 2; }
  let parsed;
  try { parsed = SC.parseScript(text); } catch (e) { console.error(e.message); return 2; }
  const res = SC.runScript(parsed.seed, parsed.commands);
  console.log(SC.renderRun(res, { trace: trace }));
  return 0;
}

process.exitCode = main(process.argv);
>>>END

<<<FILE repo/src/scene.js (proposed in a run round; not written)
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

<<<FILE repo/src/pictures.js (proposed in a run round; not written)
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

<<<FILE repo/index.html (proposed in a run round; not written)
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

<<<FILE repo/src/page.js (proposed in a run round; not written)
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

<<<FILE repo/tests/pic-helpers.js (proposed in a run round; not written)
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
>>>END

<<<FILE repo/tests/scene.test.js (proposed in a run round; not written)
'use strict';
// G-002: scene mapping (criteria 31, 33, 35, 36, 38, 40, 46).
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { G, V, A, run, world } = require('./helpers.js');
const SCN = require('../src/scene.js');

const tileAt = (sc, x, y) => sc.tiles.find((t) => t.x === x && t.y === y);
const rows = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};

test('scene: full mapping table for terrain, stairs, braziers, items and creatures', () => {
  const sc = SCN.build(V.view(world(['#########', '#@<>B+o..#', '#.msh.G..#'])));
  const expect = [[0, 0, 'wall', null], [1, 1, 'floor', null], [2, 1, 'floor', 'stairs-up'], [3, 1, 'floor', 'stairs-down'],
    [4, 1, 'floor', 'brazier'], [5, 1, 'floor', 'salve'], [6, 1, 'floor', 'oil'], [7, 1, 'floor', null]];
  for (const [x, y, base, object] of expect) {
    const t = tileAt(sc, x, y);
    assert.ok(t, 'tile ' + x + ',' + y);
    assert.equal(t.base, base, 'base ' + x + ',' + y);
    assert.equal(t.object, object, 'object ' + x + ',' + y);
    assert.equal(t.tone, 'full');
  }
  const lit = SCN.build(V.view(world(['#@B..#'], { lit: [[2, 0]] })));
  assert.equal(tileAt(lit, 2, 0).object, 'brazier-lit');
  const at = (x, y) => sc.actors.find((a) => a.x === x && a.y === y);
  assert.equal(at(2, 2).picture, 'moth'); assert.equal(at(3, 2).picture, 'shade');
  assert.equal(at(4, 2).picture, 'hound'); assert.equal(at(6, 2).picture, 'gloom');
  assert.equal(at(1, 1).picture, 'player');
  assert.ok(sc.actors.every((a) => a.wash === false));
  const names = sc.actors.map((a) => a.picture);
  assert.equal(new Set(names).size, names.length, 'all different');
});

test('scene: a crouching hound has its own picture; a standing one does not', () => {
  const s0 = world(['#@.h..#']);
  assert.equal(SCN.build(V.view(s0)).actors.find((a) => a.x === 3).picture, 'hound');
  const s1 = run(s0, A.wait);
  const v = V.view(s1);
  assert.equal(v.creatures[0].state, 'crouching');
  assert.equal(SCN.build(v).actors.find((a) => a.x === 3).picture, 'hound-crouch');
});

test('scene: wash only for stunned and staggered', () => {
  const st = run(world(['#@Bm..#']), A.E);
  const v = V.view(st);
  assert.equal(v.creatures[0].state, 'stunned');
  const sc = SCN.build(v);
  assert.equal(sc.actors.find((a) => a.picture === 'moth').wash, true);
  assert.equal(sc.actors.find((a) => a.picture === 'player').wash, false);
  const g = world(rows(3, 4), { floor: 5 });
  g.creatures[0].staggered = 3;
  const gv = V.view(g);
  assert.equal(gv.creatures[0].state, 'staggered');
  assert.equal(SCN.build(gv).actors.find((a) => a.picture === 'gloom').wash, true);
  // a hunting moth, a crouching hound and a gathering Gloom are not washed
  assert.equal(SCN.build(V.view(world(['#@.m.#']))).actors.some((a) => a.wash), false);
  assert.equal(SCN.build(V.view(run(world(['#@.h..#']), A.wait))).actors.some((a) => a.wash), false);
  assert.equal(SCN.build(V.view(run(world(rows(2, 4), { floor: 5 }), A.wait))).actors.some((a) => a.wash), false);
});

test('flame: five distinct, strictly increasing steps for r = 2..6, from real views', () => {
  const steps = [];
  for (const [E, r] of [[10, 2], [30, 3], [50, 4], [70, 5], [90, 6]]) {
    const v = V.view(world(['#@..#'], { ember: E }));
    assert.equal(v.radius, r);
    steps.push(SCN.build(v).flame);
  }
  for (let i = 1; i < steps.length; i++) assert.ok(steps[i] > steps[i - 1], steps.join());
  assert.equal(new Set(steps).size, 5);
  const one = G.newRun('flame-1');
  assert.equal(SCN.build(V.view(one)).flame, 5); // E = 100
});

test('memory: tone follows vis; unseen tiles get no request', () => {
  let st = G.newRun('mem-1');
  const acts = [A.E, A.S, A.E, A.S, A.E, A.E, A.S, A.W, A.N, A.E, A.E, A.E, A.S, A.S, A.E];
  for (let i = 0; i < 40 && !st.end; i++) st = G.step(st, acts[i % acts.length]).state;
  const v = V.view(st), sc = SCN.build(v);
  let seen = 0, dim = 0;
  v.cells.forEach((r) => r.forEach((c) => { if (c.seen) { seen++; if (!c.vis) dim++; } }));
  assert.equal(sc.tiles.length, seen);
  assert.equal(sc.tiles.filter((t) => t.tone === 'dim').length, dim);
  sc.tiles.forEach((t) => {
    const c = v.cells[t.y][t.x];
    assert.equal(t.tone, c.vis ? 'full' : 'dim');
    assert.ok(c.seen);
  });
  const keys = new Set(sc.tiles.map((t) => t.x + ',' + t.y));
  v.cells.forEach((r, y) => r.forEach((c, x) => { if (!c.seen) assert.ok(!keys.has(x + ',' + y)); }));
  assert.ok(dim > 0, 'the sample has remembered tiles');
  const ids = new Set(v.creatures.map((c) => c.x + ',' + c.y));
  sc.actors.slice(0, -1).forEach((a) => assert.ok(ids.has(a.x + ',' + a.y)));
  assert.equal(sc.actors.length, v.creatures.length + 1);
});

test('scene.js and pictures.js use no DOM, network or Image', () => {
  for (const f of ['scene.js', 'pictures.js']) {
    const src = fs.readFileSync(__dirname + '/../src/' + f, 'utf8');
    assert.ok(!/\b(window|document|Image|fetch|XMLHttpRequest|localStorage|navigator|require)\b/.test(src.replace(/\/\*[\s\S]*?\*\//, '')), f);
  }
});
>>>END

<<<FILE repo/tests/pictures.test.js (proposed in a run round; not written)
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

<<<FILE repo/tests/marks.test.js (proposed in a run round; not written)
'use strict';
// G-002 criterion 45: pictures change no mark. scene.build leaves the view untouched; the marks the page draws
// (cell.threat, creature.threat, reach) equal the marks in the text frame at every turn of scripted runs.
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, world } = require('./helpers.js');
const TV = require('../src/textview.js');
const SCN = require('../src/scene.js');
const { compareMarks } = require('./pic-helpers.js');

const rows = (px, gx) => {
  const mid = '#' + '.'.repeat(9) + '#';
  const line = mid.split('');
  line[px] = '@'; line[gx] = 'G';
  return ['#'.repeat(11), mid, line.join(''), mid, '#'.repeat(11)];
};
function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ACTS = [A.N, A.E, A.S, A.W, A.wait];

function walk(name, st, acts, seen) {
  for (let i = 0; i < acts.length; i++) {
    const v = V.view(st), before = JSON.stringify(v);
    const sc = SCN.build(v);
    assert.equal(JSON.stringify(v), before, name + ' view changed by scene.build at ' + i);
    assert.deepEqual(compareMarks(v, TV.renderFrame), [], name + ' step ' + i);
    if (sc.actors.some((a) => a.picture === 'hound-crouch')) seen.crouch++;
    if (v.creatures.some((c) => c.type === 'gloom' && c.state === 'gathering' && c.threat)) seen.gather++;
    if (v.creatures.some((c) => c.threat)) seen.threat++;
    if (v.reach.length) seen.reach++;
    if (sc.actors.some((a) => a.wash)) seen.wash++;
    st = G.step(st, acts[i]).state;
  }
}

test('criterion 45: scripted runs with a hound crouch, a Gloom gather, a flare and random walks', () => {
  const seen = { crouch: 0, gather: 0, threat: 0, reach: 0, wash: 0 };
  walk('hound', world(['#@.h..#']), [A.wait, A.wait, A.wait, A.E, A.wait], seen);
  walk('gloom', world(rows(2, 4), { floor: 5 }), [A.wait, A.wait, A.wait, A.wait, A.E, A.wait], seen);
  walk('flare', world(['#@.m.B..s.#']), [A.E, A.E, A.E, A.wait, A.E, A.W, A.wait], seen);
  for (const sd of ['pic-a', 'pic-b', 'pic-c']) {
    const rnd = lcg(sd.charCodeAt(4) * 13);
    const acts = []; for (let i = 0; i < 120; i++) acts.push(ACTS[rnd() % 5]);
    walk(sd, G.newRun(sd), acts, seen);
  }
  assert.ok(seen.crouch > 0, 'a crouching hound was seen');
  assert.ok(seen.gather > 0, 'a gathering Gloom was seen');
  assert.ok(seen.threat > 0 && seen.reach > 0 && seen.wash > 0, JSON.stringify(seen));
});
>>>END

<<<FILE repo/tests/capture-golden.test.js (proposed in a run round; not written)
'use strict';
// BUILD-CHECK ONLY. Prints sha256 of the text-player output (renderRun, no trace) for fixed scripts, taken with the
// text modules unchanged. The final step turns these hashes into tests/golden/hashes.json plus a comparing test.
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { A, world } = require('./helpers.js');
const SC = require('../src/script.js');

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
  test('capture ' + name, () => {
    const t1 = SC.renderRun(mk()), t2 = SC.renderRun(mk());
    assert.equal(t1, t2, 'deterministic');
    const sha = crypto.createHash('sha256').update(t1, 'utf8').digest('hex');
    const cnt = (re) => (t1.match(re) || []).length;
    console.log('GOLDEN ' + name + ' sha256=' + sha + ' bytes=' + Buffer.byteLength(t1, 'utf8') + ' frames=' + cnt(/^--- /gm) +
      ' crouching=' + cnt(/ crouching /g) + ' gathering=' + cnt(/ gathering /g) + ' stunned=' + cnt(/ stunned /g) +
      ' hits=' + cnt(/hits you/g) + ' kills=' + cnt(/ dies\./g) + ' floor2=' + cnt(/Floor 2\/5/g));
  });
}
>>>END

<<<FILE @run-results
### Round 1: @run/tests/build-check — `node --test`

Exit: 0 (1.7 s). Output:

```text
✔ check 14 (strict, D-002): every bot damage event was shown and marked on the tile where the player ended the turn (20 seeds) (1601.746669ms)
ℹ damage events by case: {"threat":105,"reach":114}
✔ check 26: bot runs end in a result; at least 3 land in 250-700 turns; at least one wins (0.19569ms)
ℹ bot-1:ember@322/f5 bot-2:dead@311/f4 bot-3:victory@432/f5 bot-4:dead@290/f4 bot-5:victory@287/f5 bot-6:victory@483/f5 bot-7:victory@309/f5 bot-8:dead@341/f4 bot-9:ember@386/f5 bot-10:victory@434/f5 bot-11:victory@375/f5 bot-12:ember@415/f5 bot-13:victory@388/f5 bot-14:dead@246/f4 bot-15:victory@392/f5 bot-16:victory@344/f5 bot-17:victory@390/f5 bot-18:victory@380/f5 bot-19:dead@338/f4 bot-20:victory@371/f5
GOLDEN seed-a sha256=d120b8efd1d1318348da052523733aad285d8ec0920dc5508af0fe94048b0707 bytes=76794 frames=127 crouching=0 gathering=0 stunned=0 hits=48 kills=36 floor2=0
GOLDEN seed-b sha256=1742fb17ed0c25ca3beb4135483aa7dbc7e503a44c9e199f7c4f6d21fdf32fd6 bytes=88573 frames=139 crouching=0 gathering=0 stunned=0 hits=0 kills=77 floor2=0
GOLDEN seed-c sha256=1a49b49fbcaa6b872d3cc47a48b0e602eff1d064c8ed039502fd6ab5df1669ec bytes=98545 frames=166 crouching=0 gathering=0 stunned=3 hits=0 kills=44 floor2=0
GOLDEN seed-d sha256=169dd502c10c74626ff739d9600b50f863ab5a0b9483896e149d1436c64c9305 bytes=101251 frames=147 crouching=0 gathering=0 stunned=0 hits=0 kills=0 floor2=0
GOLDEN scenario-hound sha256=d800fd2d4f5e3b304f1179fe409804f908d7dfb0eed13abdb708389f28959ab8 bytes=2942 frames=5 crouching=1 gathering=0 stunned=0 hits=6 kills=0 floor2=0
GOLDEN scenario-gloom sha256=f752844b4673cdc3c12932aa3ac864c038ff6b99bf9425b05139f0ff7fd66872 bytes=4304 frames=7 crouching=0 gathering=1 stunned=0 hits=0 kills=0 floor2=0
GOLDEN scenario-flare sha256=9618902d1e0142427f2602e17624576205616428fc1935fcde361d6a4bc24f5f bytes=3876 frames=7 crouching=0 gathering=0 stunned=0 hits=6 kills=5 floor2=0
✔ capture seed-a (75.824218ms)
✔ capture seed-b (46.749643ms)
✔ capture seed-c (51.352061ms)
✔ capture seed-d (44.025119ms)
✔ capture scenario-hound (1.265763ms)
✔ capture scenario-gloom (1.159904ms)
✔ capture scenario-flare (0.517629ms)
✔ check 9: moth moves 1 toward the player within r+3, stays beyond, hits for 1, dies to one hit (6.398271ms)
✔ check 10: shade flees when r>=3, hits only when cornered; at r=2 it hunts and hits for 2; takes 2 hits (0.791658ms)
✔ check 11: hound crouches at distance 2 in a clear line; stepping out avoids the bite; staying takes 3; adjacent bites 3 (1.669197ms)
✔ check 12: a creature moves or attacks, never both; it appears adjacent one turn before its first attack (0.423452ms)
✔ check 13: brazier flare stuns visible creatures within 7 for 2 turns and labels them stunned (0.630933ms)
✔ check 21: same seed + same commands gives byte-identical text output (40.707268ms)
✔ check 21: floor 2 does not depend on what the player did on floor 1 (2.509201ms)
✔ check 22: at least 9 of 10 seeds give different floor 1 layouts (2.631657ms)
✔ check 23: 50 seeds x floors 1-5 satisfy every generator guarantee (78.189237ms)
✔ check 20: after an end state a script ignores later commands (35.812325ms)
✔ script format: seed line, comments, spaces, unknown characters (0.571551ms)
✔ unlit brazier beside a gathered Gloom: reach mark from the Gloom; the slam lands (4.092981ms)
✔ unlit brazier beside an ungathered Gloom: no mark (it only gathers), no damage (0.356384ms)
✔ crouching hound at distance 2: a step toward it is marked beforehand and is bitten for 3 (0.439832ms)
✔ flare timing: a moth acts on the third turn counting the lighting turn as the first (0.421638ms)
✔ trace fields: damage entries carry case and the matching mark (0.763233ms)
✔ node play.js runs a script from stdin (39.368328ms)
ℹ play.js stdout lines: 109
✔ node play.js --trace prints trace lines (29.875296ms)
ℹ [trace] command 1 ("d") turn 1 consumed=true E=99 drain=1/turn || [trace] command 2 ("d") turn 2 consumed=true E=98 drain=1/turn || [trace] command 3 (".") turn 3 consumed=true E=97 drain=1/turn
✔ check 15: the Gloom has 24 HP; within 4 the ember loses 2 and the HUD says dims 2/turn (3.200043ms)
✔ check 16: gather marks 3x3 for one turn; the next turn deals 4 inside, 0 outside (0.563455ms)
✔ check 17: staggered for 3 turns doing nothing; hits deal 4 then, 2 otherwise (0.319865ms)
✔ check 18: killing the Gloom wins at once, before dimming, with the summary (0.199778ms)
✔ criterion 45: scripted runs with a hound crouch, a Gloom gather, a flare and random walks (141.630288ms)
✔ pictures: there is one picture per entity and pose (13 entities, hound in 2 poses) (1.045969ms)
✔ pictures: every picture draws in both tones, inside its tile, without throwing (6.101195ms)
✔ pictures: the palette is small; no red or orange main fill (1.574708ms)
✔ pictures: dim differs from full for every picture (0.40207ms)
✔ pictures: shapes differ (silhouettes are not copies of each other) (0.427068ms)
✔ flame: height grows with every step (0.23781ms)
✔ reach: a step next to a moth shows a reach mark before the step (3.316737ms)
✔ reach: a step next to a hound shows a reach mark; the hound is not a threat while the player stays (0.356654ms)
✔ reach: a step next to a shade at r=2 shows a reach mark (0.340444ms)
✔ threat: a Wait at E=20 beside a shade is already a strike; at E=21 it is not (0.3913ms)
✔ reach: no mark on an unlit brazier or the down stairs; a lit brazier is marked (0.381091ms)
✔ reach: no mark on walls or on a tile holding a creature (0.196281ms)
✔ text frame: reach tiles are drawn with ? and differ from the threat glyph (0.303053ms)
✔ check 14 (strict): every damage event was shown and marked on the tile where the player ended the turn (266.761561ms)
ℹ threat seed c14-1 command 11 creature #2 moth
ℹ threat seed c14-2 command 16 creature #4 moth
ℹ reach  seed c14-10 command 12 creature #4 moth
ℹ threat seed c14-10 command 16 creature #4 moth
ℹ reach  seed c14-10 command 19 creature #4 moth
ℹ threat seed c14-10 command 23 creature #4 moth
ℹ threat seed c14-10 command 26 creature #4 moth
ℹ reach  seed c14-13 command 5 creature #2 moth
ℹ reach  seed c14-13 command 7 creature #4 moth
ℹ threat seed c14-13 command 8 creature #4 moth
ℹ threat seed c14-14 command 6 creature #4 moth
ℹ threat seed c14-14 command 8 creature #4 moth
ℹ threat seed c14-15 command 16 creature #2 moth
ℹ reach  seed c14-15 command 76 creature #1 moth
ℹ reach  seed c14-16 command 17 creature #3 moth
ℹ threat seed c14-16 command 18 creature #3 moth
ℹ threat seed c14-16 command 32 creature #1 moth
ℹ threat seed c14-16 command 35 creature #1 moth
ℹ reach  seed c14-18 command 57 creature #1 moth
ℹ damage events: threat 12, reach 7
✔ sampled states: threat flags equal what the planner does with the ember after dimming (67.54153ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (7.667156ms)
✔ check 2: waiting costs 1 E; radius thresholds (1.936935ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.554705ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.247799ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.230876ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.455101ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.71354ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.171975ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.331838ms)
✔ check 20: after an end state further commands change nothing (0.282955ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.270864ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.31213ms)
✔ scene: full mapping table for terrain, stairs, braziers, items and creatures (3.555725ms)
✔ scene: a crouching hound has its own picture; a standing one does not (0.83527ms)
✔ scene: wash only for stunned and staggered (2.465093ms)
✔ flame: five distinct, strictly increasing steps for r = 2..6, from real views (9.247267ms)
✔ memory: tone follows vis; unseen tiles get no request (4.242675ms)
✔ scene.js and pictures.js use no DOM, network or Image (0.266093ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (15.586136ms)
✔ visibility: walls block line of sight; the glow is circular (0.49196ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (1.236409ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.484486ms)
ℹ tests 69
ℹ suites 0
ℹ pass 69
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1671.260714
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-entity-pictures/05-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
