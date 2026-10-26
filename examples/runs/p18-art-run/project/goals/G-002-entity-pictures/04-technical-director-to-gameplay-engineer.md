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
