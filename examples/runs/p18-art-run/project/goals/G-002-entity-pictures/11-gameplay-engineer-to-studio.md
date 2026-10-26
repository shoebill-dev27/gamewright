---
kind: handoff
goal: G-002
seq: 11
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 11: gameplay-engineer → studio — D-005 applied (criterion 44 backing, TILE 28, chips, player outline); ready for Verify with screenshots

## Task

Route to QA and the Art Director in parallel, with screenshots. Verify criterion 44 and the visual criteria 31 to 46 against the build with D-005 applied. This is not a verdict.

## Context

Goal G-002. Handoff 10 asked for D-005 in full. QA (08) had failed criterion 44 for the missing dark backing behind the reach letters. Only `repo/src/page.js` and `repo/src/pictures.js` changed. `scene.js`, rules, `textview.js`, `script.js`, `play.js`, `index.html`, tests and golden hashes are untouched.

## Findings

**Files changed:** `repo/src/page.js`, `repo/src/pictures.js`.

**D-005 items:**
1. **Tile size.** `TILE` is 28 (was 22). The picture inset is `max(round(2.8), 4)` = 4, so the picture is 20 px. Click mapping uses `TILE`, so it follows. I could not read `v.w`, so I did not check that board plus the 360 px panel fits 1280 px. If it does not, change `TILE` to 26 (one constant in `page.js`).
2. **Fonts.** The base font is now bold 10 px. The `!`, `z`/`~` badges and 1 to 2 reach letters use bold 10 px. Reach marks with 3 or more letters use 9 px.
3. **Chips.** A new `chip()` helper draws the badge at (x*TILE+3, y*TILE+3), 8x11 px, `#150f22` at alpha 0.9, with the character centered. The threat `!` is `#ff4040`. The stun/stagger `z`/`~` is `#cfe6ff`. The old `cr.y - 0.55` placement is removed. The threat chip is drawn after the threat border, in step 5. I did not implement the "state chip goes bottom-left" fallback, because D-005 says the two badges do not co-occur (rules never set `threat` on stunned or staggered creatures). The wash is unchanged.
4. **Reach backing.** After the orange tint and dashed border and before the letters: a rect centered on the tile, 12 px tall, width = letters*6+4 (letters*5.5+4 for 3 or more), capped at TILE-6, `#150f22` at alpha 0.85. At TILE 28 the cap is 22 px, so the backing stays inside the 3 px border zone. This is the criterion 44 fix.
5. **Player outline.** The player draws night shapes first: head circle radius 3, cloak triangle `[[5.5,6.4],[10.8,16.5],[0.2,16.5]]`, a staff rect, and a grown flame polygon. The flame function takes a `grow` parameter (added to `h` and `w`, base extended by `grow`). Only the existing `night` color is used, and the staff outline is my addition. The outline stays within the 3 px margin at TILE 22 (checked by arithmetic: lowest point about 18.4 px of 22, highest about 3.56 px).
6. **Shade and Gloom.** `violet` is `#7566a8`. The Gloom inner `night` disc is radius 5.5, so the ring is 1.5 units.
7. **Dim palette.** Factor kept at 0.55. A screenshot decides whether to raise it to 0.65.

**Tests:** I did not run `node --test` in this step; the runtime appends the result under Build check. I expect no test change to be needed. `pictures.test.js` draws at its own TILE 22 and does not read the page TILE. The palette test (12 colors at most, no red or orange main fill) still holds because I added no color. The golden test is unaffected, since no text-player file was touched. I changed no test file and regenerated no hash.

**For the screenshots to look at:**
- Board width at TILE 28 next to the panel, and whether 26 is needed.
- Reach letters on a salve tile, a lit brazier tile, a stairs tile, and with 2 or 3 letters (backing width, and that it does not cover the dashed border).
- Reach tile inside a Gloom area or hound line: do the 2 px dashes and the 3 px red border merge? (Art Director's open question; I changed nothing.)
- Threat chip on a creature in row 0, and on a creature next to another marked tile. The chip covers the creature picture's top-left corner: check it hides no key feature (the shade's head, the moth's antenna).
- Stunned and staggered chips on the wash.
- Player on `<`, on a lit brazier and on plain floor: does the outline separate them?
- Shade and Gloom against the floor. Remembered wall against remembered floor (item 7).
- Flame steps at r = 6 and r = 2 with the outline (the grown flame is about 1 unit wider).

## Decisions already made

- D-002 (marks), D-003 (style and layering), D-004 (code-drawn pictures, pure scene), D-005 (applied as written, no conflict with the spec or a tested criterion).

## Constraints

- No rule, content, dependency, network or asset change. The palette is still 11 colors, no red or orange main fill. The page opens from the file system. `scene.js` is pure and unchanged.
- The text player output is untouched.

## Open questions

1. Does the board fit at 28 px? Screenshots decide (fallback 26).
2. Reach border merging with the red border: for the Art Director.
3. Remembered wall and floor contrast: for the Art Director.

## Expected output

QA and the Art Director each get a fresh Handoff. The next step is Verify in parallel, using screenshots, with QA checking criterion 44 and 31 to 49, and the Art Director giving the visual verdict.

## Sender assessment

Confidence is medium. The code follows D-005 item by item, but nothing was run or seen. The main risks are the chip hiding creature details at the top-left, the board width, and the player outline looking heavy next to the grown flame.

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (1.7 s).

```text
ember after dimming (66.42548ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (8.324194ms)
✔ check 2: waiting costs 1 E; radius thresholds (1.990395ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.263461ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.283286ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.306781ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.481581ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.730983ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.181634ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.298766ms)
✔ check 20: after an end state further commands change nothing (0.278858ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (0.995213ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (3.515996ms)
✔ scene: full mapping table for terrain, stairs, braziers, items and creatures (7.371235ms)
✔ scene: a crouching hound has its own picture; a standing one does not (1.622656ms)
✔ scene: wash only for stunned and staggered (1.480051ms)
✔ flame: five distinct, strictly increasing steps for r = 2..6, from real views (4.892969ms)
✔ memory: tone follows vis; unseen tiles get no request (3.117751ms)
✔ scene.js and pictures.js use no DOM, network or Image (0.254763ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (11.682071ms)
✔ visibility: walls block line of sight; the glow is circular (0.538449ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (1.25768ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.476271ms)
ℹ tests 69
ℹ suites 0
ℹ pass 69
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1668.524901
```

## Load

- Role: studio/roles/qa.md (and studio/roles/art-director.md for the visual verdict)
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, repo/src/scene.js, repo/index.html, repo/tests/golden.test.js, repo/tests/golden/hashes.json
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/10-studio-to-gameplay-engineer.md
