# Studio operation packet

operation: Step
goal: G-002
role: qa
incoming_handoff: goals/G-002-entity-pictures/12-studio-to-qa.md
next_seq: 14
runs: tests, play, trace, shot (2 rounds left; results in @run-results)
run_tests: node --test
run_play: node play.js {script}
run_trace: node play.js --trace {script}
run_shot: screenshots of index.html ({script}: keys to press)
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-entity-pictures/14-qa-to-<recipient>.md
- @run/<tests|play|trace|shot>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-002-entity-pictures/12-studio-to-qa.md
---
kind: handoff
goal: G-002
seq: 12
from: studio
to: qa
stage: Verify
outcome: routed
---
# 12: studio → qa — second verification of the entity pictures, with real screenshots

## Task

Verify the current build against the acceptance criteria 31 to 49 in `design/entity-pictures.md`. Re-check criterion 44 first (the reach letters need a dark backing). Use real screenshots of the browser page wherever a criterion is visual.

## Context

Goal G-002 gives each kind of thing on the floor grid its own picture on the browser page. Your first verification (08) failed criterion 44, passed 45 and 48 with limits, and could not check the rest without a viewer. The build was changed after that. D-005 sets a larger tile, dark chips behind badges and reach letters, a player outline, and shade and Gloom contrast. The Art Director reviews the same build visually in parallel; you do not depend on that review.

## Findings

Nothing from the implementer is passed on. Verify from the spec, the criteria and the build.

## Decisions already made

- D-003: flat dark-cave pictures; marks are always drawn over pictures.
- D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast.

## Constraints

- Run the build only through the project's run commands (`node --test`, `node play.js {script}`, and the page `repo/index.html`).
- In your earlier pass, the `shot` call failed because of how keys were passed. Use one key name per press in each `shot` call.
- Do not change files in `repo/`.
- If a criterion cannot be checked with your means, say so plainly. Do not mark it pass by inference.
- Also check that the page layout (board plus side panel) fits a 1280 px wide window. If it does not, report the measured widths.

## Open questions

None.

## Expected output

A pass/fail report per criterion 31 to 49, with evidence (screenshot or run output) and any limit stated. Address the result to `studio`. A failing criterion goes in the report with steps to reproduce.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, design/acceptance-criteria.md, repo/manual.md, repo/index.html, the build in repo/
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/08-qa-to-studio.md
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots, shot
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
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

<<<FILE design/acceptance-criteria.md
# Ember Hollow: acceptance criteria for the first complete run (G-001)

Rules referenced here are in `design/game-spec.md`. "Text output" means what `node play.js {script}` prints. "Page" means `repo/index.html` opened from the file system.

## A. Verification checks (QA, through text output unless marked Page)

### Ember and light
1. A new run shows E = 100 and r = 6, HP 12/12, floor 1/5.
2. After 1 wait on a quiet floor, E = 99; after 20 waits, E = 80 and r is still 6; after 21 waits, E = 79 and r = 5. r equals 6/5/4/3/2 at the E thresholds in spec section 3 (checked at E = 100, 80, 79, 60, 59, 40, 39, 20, 19, 1).
3. Moving, waiting, fighting and using an item each cost exactly 1 E. A refused action (wall, item refused at full HP/E) costs 0 E and does not advance the turn counter.
4. Stepping onto an unlit brazier at E = 30 gives E = 89 after the turn (30 + 60 − 1). At E = 80 it gives E = 99... (min 100 − 1). A lit brazier gives nothing on later visits.
5. Reaching E = 0 ends the run with "The ember went out" and the floor number. Creatures do not act on that turn (HP is unchanged by them).
6. A message is shown when E falls to 20, 10 and 5 or below, and when r drops.
7. Map memory: after walking away, previously seen tiles stay shown as remembered; creatures out of sight are not listed.
8. Oil flask: +30 E up to 100, then dimming; refused at E = 100 with no turn passing. Salve: +5 HP up to 12; refused at 12 HP with no turn passing.

### Creatures
9. Moth: with the player at path distance ≤ r + 3 it moves 1 tile toward the player per turn; beyond that it stays. Adjacent at the start of its action it deals exactly 1. Dies to 1 player hit (2 damage).
10. Shade, r ≥ 3: a visible shade moves away from the player (never closer) and deals no damage unless cornered and adjacent (2 damage). r = 2 (E ≤ 19): a shade moves toward the player and deals 2 damage when adjacent at the start of its action. Takes 2 player hits (4 HP).
11. Hound: starts hunting at path distance ≤ 6. At Manhattan distance 2 in a clear straight line it crouches and is marked as a threat with its line for exactly one turn. If the player leaves the line during that turn, no damage is dealt; if the player stays within 2 tiles in the line, the player takes exactly 3. Adjacent hound bites for 3. Takes 2 player hits.
12. A creature moves or attacks, never both in one turn (except the hound lunge). Verified by a turn log that shows a creature appearing adjacent one turn before its first attack.
13. Brazier flare: non-boss creatures visible within distance 7 after lighting skip exactly 2 actions: the one in the lighting turn's own creature phase and the one in the next turn. They are labeled stunned in the frame after the lighting turn and act again in the second turn after it. A crouching hound's crouch is cancelled.
14. Threat and reach marks (D-002): in every turn where the player takes damage from a creature, that creature was visible in the previous turn's output and carried a mark on the tile where the player ended the turn. That is a threat mark if the player did not move, or a reach mark on the neighbour tile the player moved onto. Over 20 scripted runs on different seeds, no damage comes from a creature that was not shown and marked this way before it hit. The test log lists each damage event with the case that applied (threat or reach). Also checked on hand-made scenarios: a step next to a moth, a hound and a shade at r = 2 each shows a reach mark before the step. A Wait at E = 20 beside a shade shows the threat mark as a strike, because the creature phase sees r = 2. A step onto the down stairs shows no reach mark. A step onto an unlit brazier shows no reach mark for creatures the flare stuns, but does show one for the Gloom if it would hurt; a lit brazier is marked like a floor tile.

### The Gloom and the win
15. On floor 5, the Gloom has 24 HP. While within Manhattan distance 4 of the player the ember loses 2 per turn and the output shows "dims 2/turn".
16. When the player is within distance 2 it shows a 3×3 marked area for one turn, then the next turn deals exactly 4 to a player standing in that area and 0 to a player outside it.
17. After a slam it is staggered for 3 turns and does nothing; hits on it during those turns deal 4 damage, otherwise 2.
18. Reducing the Gloom to 0 HP gives Victory at once, with the victory message and the summary (floor, turns, defeated count, HP, ember, seed). A scripted fight is possible in which the player wins with E ≤ 5.
19. HP 0 gives "You fell on floor N" and the summary. If HP 0 and E 0 would both happen in one turn, the result is "The ember went out".
20. After an end state further commands change nothing.

### Floors and seeds
21. Same seed + same commands → byte-identical text output on two runs. Same seed with different commands on floor 1 → floor 2 layout, items and creature start positions identical.
22. Of 10 different seeds, at least 9 give a different floor 1 layout.
23. For 50 seeds × floors 1–5: sizes match the table (spec section 5), all walkable tiles connected, creature, brazier and item counts match the table, `<`→`>` shortest path ≥ 30 (floors 1–3) / ≥ 40 (floor 4), at least one brazier within 25 steps of `<` on floors 1–4, no creature within 6 steps of `<`, floor 5 has no `>` and 3 braziers in the arena.
24. Descending: the player appears on `<` of the next floor with E and HP unchanged apart from that turn's dimming, and the floor number increases; the player cannot go back up.
25. Inventory holds 4 items; a fifth stays on the floor with a message.

### Run length
26. A scripted, reasonable run (walk to `>` while lighting braziers within 10 steps of the path, fight what blocks the way, fight the Gloom) of at least 3 different seeds takes between 250 and 700 player turns and reaches either Victory or a loss. At least one seed is won by a bot that follows the threat marks.

### Page (checked by looking at it)
27. `repo/index.html` opens from the file system with no server and shows the grid, ember bar with E and r, HP, floor n/5, turn count, inventory slots, the last 5 messages and the seed.
28. Arrow keys / WASD, `.` / Space, `1`–`4`, `R`, `N` work as in spec section 9. Clicking an adjacent tile moves or fights; clicking an inventory slot uses the item.
29. Visible tiles are clearly brighter than remembered tiles. As E falls through each threshold, the visible area visibly shrinks by about one tile of radius. Creature types are distinguishable at a glance. Threat marks are clearly visible and different from the normal creature display. Reach marks on the neighbour tiles are visible and distinct from the threat marks. A lit brazier differs from an unlit one.
30. The summary screen appears for each of the three end states with the fields from spec section 8, and a new run can be started from it.

## B. Experience signals (for Play and Review; not given to the Playtester as pass/fail)

- A new player understands from the first floor that the ember dims and braziers refill it, without a tutorial text beyond the manual.
- Within the first two floors the player can say what a moth and a shade do, and why shades keep their distance when the light is bright.
- The player makes at least one choice per floor of the form "detour for a brazier/item or save ember".
- The player is hurt by something they did not notice at most rarely; when it happens they can name the mark that warned them.
- The hound's crouch is understood the first time it is seen (the player steps out of the line, or strikes first).
- The Gloom fight reads as a rhythm: approach, gather, dodge, stagger, strike; and the extra drain makes the player feel the clock.
- A lost run leaves the player with a specific thing to do differently.
- A full run feels like 15–30 minutes; a second run on a new seed feels different, a repeat of the same seed feels familiar.
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

## Pictures on the browser page

Every kind of thing on the floor grid has a drawn picture (nothing is loaded from files): wall (stone blocks) and floor (dark
speckled ground); `<` blue rising steps, `>` green descending steps; unlit brazier (grey bowl) and lit brazier (the same bowl with
a gold flame); salve (green jar with a cross) and oil flask (blue flask with a gold cap); moth (pale wings), shade (tall violet
wisp with pale eyes), hound (low grey four-legged, lower and stretched when crouching), the Gloom (large dark many-limbed mass
with pale eyes); you (a small figure with a gold flame that is larger when your light is wider). Remembered tiles show the same
pictures dimmer; creatures are never shown from memory. A stunned or staggered creature gets a pale-blue wash and a small badge
(`z` stunned, `~` staggered), never a red mark. Marks are unchanged: red tint and 3 px red border (threat), dashed orange tile with
letters (reach). Inventory buttons show the item picture beside their text.

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

<<<FILE @run-results
### Round 1: @run/tests — `node --test`

Exit: 0 (1.7 s). Output:

```text
✔ check 14 (strict, D-002): every bot damage event was shown and marked on the tile where the player ended the turn (20 seeds) (1618.735025ms)
ℹ damage events by case: {"threat":105,"reach":114}
✔ check 26: bot runs end in a result; at least 3 land in 250-700 turns; at least one wins (0.199418ms)
ℹ bot-1:ember@322/f5 bot-2:dead@311/f4 bot-3:victory@432/f5 bot-4:dead@290/f4 bot-5:victory@287/f5 bot-6:victory@483/f5 bot-7:victory@309/f5 bot-8:dead@341/f4 bot-9:ember@386/f5 bot-10:victory@434/f5 bot-11:victory@375/f5 bot-12:ember@415/f5 bot-13:victory@388/f5 bot-14:dead@246/f4 bot-15:victory@392/f5 bot-16:victory@344/f5 bot-17:victory@390/f5 bot-18:victory@380/f5 bot-19:dead@338/f4 bot-20:victory@371/f5
✔ check 9: moth moves 1 toward the player within r+3, stays beyond, hits for 1, dies to one hit (6.07755ms)
✔ check 10: shade flees when r>=3, hits only when cornered; at r=2 it hunts and hits for 2; takes 2 hits (0.810664ms)
✔ check 11: hound crouches at distance 2 in a clear line; stepping out avoids the bite; staying takes 3; adjacent bites 3 (1.736606ms)
✔ check 12: a creature moves or attacks, never both; it appears adjacent one turn before its first attack (0.224164ms)
✔ check 13: brazier flare stuns visible creatures within 7 for 2 turns and labels them stunned (0.550121ms)
✔ check 21: same seed + same commands gives byte-identical text output (40.728299ms)
✔ check 21: floor 2 does not depend on what the player did on floor 1 (1.805757ms)
✔ check 22: at least 9 of 10 seeds give different floor 1 layouts (2.230169ms)
✔ check 23: 50 seeds x floors 1-5 satisfy every generator guarantee (76.881407ms)
✔ check 20: after an end state a script ignores later commands (33.256389ms)
✔ script format: seed line, comments, spaces, unknown characters (0.626815ms)
✔ unlit brazier beside a gathered Gloom: reach mark from the Gloom; the slam lands (4.014486ms)
✔ unlit brazier beside an ungathered Gloom: no mark (it only gathers), no damage (0.353259ms)
✔ crouching hound at distance 2: a step toward it is marked beforehand and is bitten for 3 (0.471132ms)
✔ flare timing: a moth acts on the third turn counting the lighting turn as the first (0.405037ms)
✔ trace fields: damage entries carry case and the matching mark (0.982379ms)
✔ node play.js runs a script from stdin (39.40354ms)
ℹ play.js stdout lines: 109
✔ node play.js --trace prints trace lines (37.286806ms)
ℹ [trace] command 1 ("d") turn 1 consumed=true E=99 drain=1/turn || [trace] command 2 ("d") turn 2 consumed=true E=98 drain=1/turn || [trace] command 3 (".") turn 3 consumed=true E=97 drain=1/turn
✔ check 15: the Gloom has 24 HP; within 4 the ember loses 2 and the HUD says dims 2/turn (4.002102ms)
✔ check 16: gather marks 3x3 for one turn; the next turn deals 4 inside, 0 outside (0.717647ms)
✔ check 17: staggered for 3 turns doing nothing; hits deal 4 then, 2 otherwise (0.432909ms)
✔ check 18: killing the Gloom wins at once, before dimming, with the summary (0.271203ms)
✔ golden text output (criterion 48): seed-a (47.935729ms)
✔ golden text output (criterion 48): seed-b (25.506892ms)
✔ golden text output (criterion 48): seed-c (26.801506ms)
✔ golden text output (criterion 48): seed-d (26.646077ms)
✔ golden text output (criterion 48): scenario-hound (0.996436ms)
✔ golden text output (criterion 48): scenario-gloom (0.852523ms)
✔ golden text output (criterion 48): scenario-flare (0.393013ms)
✔ criterion 45: scripted runs with a hound crouch, a Gloom gather, a flare and random walks (134.729893ms)
✔ pictures: there is one picture per entity and pose (13 entities, hound in 2 poses) (0.874585ms)
✔ pictures: every picture draws in both tones, inside its tile, without throwing (3.072613ms)
✔ pictures: the palette is small; no red or orange main fill (1.863436ms)
✔ pictures: dim differs from full for every picture (0.636163ms)
✔ pictures: shapes differ (silhouettes are not copies of each other) (0.530745ms)
✔ flame: height grows with every step (0.334002ms)
✔ reach: a step next to a moth shows a reach mark before the step (3.608612ms)
✔ reach: a step next to a hound shows a reach mark; the hound is not a threat while the player stays (0.376463ms)
✔ reach: a step next to a shade at r=2 shows a reach mark (0.355663ms)
✔ threat: a Wait at E=20 beside a shade is already a strike; at E=21 it is not (0.431657ms)
✔ reach: no mark on an unlit brazier or the down stairs; a lit brazier is marked (0.427839ms)
✔ reach: no mark on walls or on a tile holding a creature (0.214195ms)
✔ text frame: reach tiles are drawn with ? and differ from the threat glyph (0.33329ms)
✔ check 14 (strict): every damage event was shown and marked on the tile where the player ended the turn (258.218626ms)
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
✔ sampled states: threat flags equal what the planner does with the ember after dimming (59.036563ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (5.937718ms)
✔ check 2: waiting costs 1 E; radius thresholds (5.424028ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.393361ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.238101ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.270131ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.420215ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.705354ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.181423ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.355933ms)
✔ check 20: after an end state further commands change nothing (0.314725ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.137874ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.350623ms)
✔ scene: full mapping table for terrain, stairs, braziers, items and creatures (3.802986ms)
✔ scene: a crouching hound has its own picture; a standing one does not (0.832054ms)
✔ scene: wash only for stunned and staggered (1.577434ms)
✔ flame: five distinct, strictly increasing steps for r = 2..6, from real views (6.929269ms)
✔ memory: tone follows vis; unseen tiles get no request (5.407372ms)
✔ scene.js and pictures.js use no DOM, network or Image (0.267155ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (14.069729ms)
✔ visibility: walls block line of sight; the glow is circular (0.782811ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (0.912346ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.358398ms)
ℹ tests 69
ℹ suites 0
ℹ pass 69
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1676.208877
```

### Round 1: @run/play/hollow-walk — `node play.js {script}`

Script:

```text
seed 42
dddd ss ..
```

Exit: 0 (0.0 s). Output:

```text
--- start ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 0 | HP 12/12
Ember 100/100 [####################] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     #######
                     #.....#
                     #.....#
                  ......@..#
                     #.....#
                     #######










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 1: "d" ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 1 | HP 12/12
Ember 99/100 [####################] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     #######
                     #.....#
                     #.....#
                  ,.....<@.#
                     #.....#
                     #######










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 2: "d" ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 2 | HP 12/12
Ember 98/100 [####################] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....#
                     #.....#
                  ,,....<.@#
                     #.....#
                     %######










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 3: "d" (refused: no turn passed) ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 2 | HP 12/12
Ember 98/100 [####################] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....#
                     #.....#
                  ,,....<.@#
                     #.....#
                     %######










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 4: "d" (refused: no turn passed) ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 2 | HP 12/12
Ember 98/100 [####################] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....#
                     #.....#
                  ,,....<.@#
                     #.....#
                     %######










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 5: "s" ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 3 | HP 12/12
Ember 97/100 [###################-] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....%
                     #.....#
                  ,,....<..#
                     #....@#
                     %%%####










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 6: "s" (refused: no turn passed) ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 3 | HP 12/12
Ember 97/100 [###################-] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....%
                     #.....#
                  ,,....<..#
                     #....@#
                     %%%####










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 7: "." ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 4 | HP 12/12
Ember 96/100 [###################-] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....%
                     #.....#
                  ,,....<..#
                     #....@#
                     %%%####










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.

--- command 8: "." ---
Ember Hollow | seed: 42
Floor 1/5 | Turn 5 | HP 12/12
Ember 95/100 [###################-] r=6 | dims 1/turn
Items: [1] empty  [2] empty  [3] empty  [4] empty
                     ######%
                     #.....%
                     #.....#
                  ,,....<..#
                     #....@#
                     %%%####










Danger: none
Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! threat mark  ? reach mark (step there and be hit)  , % remembered
Creatures: none in sight
Messages:
  - You descend into Ember Hollow with one ember.
```

### Round 1: @run/shot/start — `screenshots of index.html ({script}: keys to press)`

Exit: 0 (1.0 s). Output:

```text
{"page":"index.html","keys_pressed":0,"screenshots":1,"screenshots_not_taken":0,"console_errors":[]}

Attached to this packet: image 1 (shot-round1-1.png)
```

### Round 1: @run/shot/walk — `screenshots of index.html ({script}: keys to press)`

Script:

```text
d
d
d
d
s
s
Space
Space
```

Exit: 0 (0.6 s). Output:

```text
{"page":"index.html","keys_pressed":8,"screenshots":1,"screenshots_not_taken":0,"console_errors":[]}

Attached to this packet: image 2 (shot-round1-2.png)
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-entity-pictures/14-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
