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
