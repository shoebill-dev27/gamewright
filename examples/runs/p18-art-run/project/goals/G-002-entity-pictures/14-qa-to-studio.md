---
kind: handoff
goal: G-002
seq: 14
from: qa
to: studio
stage: Verify
outcome: partial
---
# 14: qa → studio — second verification of the entity pictures: no criterion fails, but most visual criteria are still unchecked; 44 not verified

## Task

Route the result. The first real screenshots exist, and nothing seen fails. The scenes that matter most (reach marks, threat marks, creatures other than a moth, the flame at r = 2) cannot be reached with the `shot` tool as it works. Studio decides how to get those scenes seen (see Open questions). This is not a pass.

## Context

Goal G-002, second QA pass, against `design/entity-pictures.md` criteria 31 to 49 on the build with D-005 applied. I changed nothing in `repo/`. I did not use implementer assessments.

Budget: I used 1 round each of `tests`, `play` and `shot` (two `shot` runs). I did not use the second round, because no further run available to me could reach the missing scenes (see Findings, "Why more runs did not help").

## Findings

### Means used

- `node --test`: exit 0, 69 tests, 69 pass, 0 fail.
- `node play.js` on a seed 42 script (`dddd ss ..`): exit 0. Frames are well-formed and refused moves are marked "(refused: no turn passed)".
- `shot` start: a fresh page, 0 keys, 1 screenshot, `console_errors: []`.
- `shot` walk: keys `d d d d s s Space Space` (one key name per press, as asked). 8 keys pressed, 1 screenshot, `console_errors: []`. The screenshot shows Turn 6, so two presses were refused moves.
- I did not read `page.js` or `pictures.js` this round, so I make no code-level claims about the D-005 changes.

### What the two screenshots show (1000x700 viewport, tile 28 px)

Observed on the page:

- Wall: stone-block texture, clearly lighter than the floor.
- Floor: dark speckled ground.
- Unlit brazier: a small grey bowl. It is visible but small and low in contrast on the floor.
- Player: pale head, blue cloak and a gold flame, with a dark outline. At turn 0 the player stands on `<` (confirmed by the text frame) and is still readable there.
- `<`: blue rising steps.
- Moth: pale winged picture on the floor about 3 to 4 tiles away. It has no threat border and no reach mark. Not adjacent, so none was expected.
- Remembered tiles: wall segments at the edge of the explored area are visibly darker than visible walls. Unseen tiles are black.
- The board is near black overall. The brightest warm spot on the board is the player's flame.
- Both loads had empty `console_errors`.
- The inventory buttons show text only (`[1] empty`), as expected with no items.
- The ember bar and the HP, turn and ember text are shown.

Layout: the canvas is about 786 px wide and 450 px high (x 12 to 798, y 51 to 500). At the 1000 px viewport the side panel wraps below the board, and the lower buttons (New seed) are cut off by the 700 px viewport height. I could not set a 1280 px window. By calculation, the board plus the gap plus the panel needs 12 + 786 + 16 + (300 to 360) + 12 = about 1126 to 1186 px, which is under 1280. So the panel should sit beside the board at 1280 px. This is computed, not measured.

### Why more runs did not help

- `shot` takes keys only. It cannot choose a seed, set the URL hash, or place the player next to a hound, a shade or the Gloom.
- With the default seed and the first few turns, only a quiet start room is reachable.
- I may not write `repo/` files (a fixture page or scenario harness), so I cannot build the missing scenes myself.

### Per-criterion result

| # | Result | Evidence and limit |
|---|---|---|
| 31 | not checkable (partial) | Seen with their own picture: wall, floor, unlit brazier, player, `<`, moth. Not seen on the page: shade, hound, Gloom, lit brazier, salve, oil, `>`. The Node mapping test covers all entities in structure only. |
| 32 | not checkable | Needs shade, hound and Gloom on the page, and greyscale. Not seen. |
| 33 | not checkable | Only the unlit brazier and `<` were seen. No salve, oil flask, lit brazier or `>`. |
| 34 | pass for what was seen | Wall and floor are told apart at a glance. The brazier, moth and player stand out from plain floor. The unlit brazier is the weakest of these. |
| 35 | partial | Player visible on `<` at turn 0 (screenshot 1). The lit brazier case was not seen. |
| 36 | not checkable | Only r = 6 seen. No r = 2 screenshot is reachable with keys. |
| 37 | not checkable | No items in inventory. |
| 38 | pass for terrain, partial overall | Remembered wall is visibly darker than visible wall, and the same shapes are kept. Unseen is black. The no-creature-on-memory part is untested on the page. |
| 39 | not checkable | Needs a tile at the edge of the glow next to a remembered tile at r = 6 and r = 2. Not seen at either. |
| 40 | not checkable | Needs a run through E thresholds. |
| 41 | pass, limited | Dark frame, warmest bright spot on the board is the flame. Only quiet start frames were seen; no lit brazier. |
| 42 | not checkable | No creature with a threat mark was seen. |
| 43 | not checkable | No crouch line or Gloom area seen. |
| 44 | **not verified (re-check order not fulfilled)** | No reach mark appeared in either screenshot, so I could not see the new letter backing. This is neither a pass nor a repeat fail. The earlier fail (no backing) stands as the last observed state until a reach mark on an item tile and on a lit brazier is seen. |
| 45 | pass at view level only | `criterion 45` test passes (scripted runs with hound crouch, Gloom gather, flare and random walks). Page marks vs text marks not compared pixel-wise. |
| 46 | not checkable | No stunned or crouching creature seen. |
| 47 | pass for first load | `console_errors` empty on both loads. All pictures that appeared loaded. The whole picture set was not exercised. |
| 48 | pass, with the limits stated in 08 | 69 of 69 tests pass, including 7 of 7 golden hash tests. `node play.js` runs. |
| 49 | not checkable | Controls only partly exercised: `d`, `s` and Space moved or waited (turn 0 to 6, E 100 to 94). Clicks, slots, R/N and summary screens not exercised. |

### Regressions

1 to 26: covered by the passing named tests above. 27: the page shows the grid, ember bar with E and r, HP, floor, turn, inventory slots and buttons in the screenshots. The last 5 messages and the seed line fall below the 700 px viewport, so I did not see them. 28 and 30 are not checked.

### Observations to pass on (visual, not criterion fails)

- At the 1000 px viewport the panel is under the board and the page needs scrolling. Expected from `flex-wrap`, not a defect, but the 1280 px fit is unmeasured.
- The unlit brazier is small and grey on dark floor. It reads, but is the least prominent picture in the frames.

### Verdict

No criterion is shown to fail this round. No criterion that needs a threat, reach, creature, item, flare or low-radius scene is verified. Criterion 44, which was to be re-checked first, is not verified. The change cannot count as verified.

## Decisions already made

- D-002: threat and reach marks. D-003: flat dark-cave pictures, marks over pictures. D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast.

## Constraints

- I changed no file in `repo/`, and I did not decide intended look or behaviour.
- I do not mark a criterion pass by inference from code or tests.

## Open questions

1. Studio: how to get the missing scenes seen. Options:
   a. Allow QA to write a QA-only fixture page and script under a new path (for example `qa/`) that loads the real `src/` files, sets a seed through the URL hash, and drives a scenario (hound crouch, Gloom gather, shade at r = 2, flare, items) before the screenshot. The role allows QA to add test tooling, but this packet's write list did not include such a path.
   b. Extend `shot` so its input can set the URL hash (seed) or a viewport width. The missing 1280 px measurement needs that too.
   c. Ask the Owner to look at the page at 1280 px.
2. Which scenes the next pass must capture. Criterion 44 first:
   - a reach mark on an item tile and on a lit brazier, letters readable on the dark chip;
   - a threat border and `!` chip on an adjacent moth and a hound, one of them in row 0;
   - a crouching hound with its line, and a Gloom area over items;
   - a stunned creature;
   - the player on a lit brazier, and at r = 2 next to r = 6 (flame size and glow edge);
   - a shade and the Gloom next to the floor (contrast, D-005 item 6);
   - the inventory with a salve and an oil flask;
   - the page at 1280 px (measure panel position and any horizontal scroll).
3. If a second QA pass is routed, give it the harness in 1a or 1b and at least one `shot` round with a seed that places a moth, hound and shade within the first 30 turns. The seed must come from a text trace (`node play.js --trace`) taken beforehand.

## Expected output

Studio chooses the means in Open question 1, then routes a third QA pass that covers the scenes in Open question 2. Success: every criterion 31 to 49 is marked pass, or a stated not-checkable with a named reason that the Owner accepts. A failing criterion goes to `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, design/acceptance-criteria.md, repo/manual.md, repo/index.html, the build in repo/ (`node --test`, `node play.js {script}`, `node play.js --trace {script}`, screenshots of `index.html`)
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/12-studio-to-qa.md
