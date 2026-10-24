---
kind: handoff
goal: G-001
seq: 73
from: game-designer
to: studio
stage: Build (the Studio composes the step for gameplay-engineer)
outcome: done
---
# 73: game-designer → studio — Rulings for the three spec gaps (cell at .5, "on you", hit-line word); criteria changed

## Task

Compose the Build step for `gameplay-engineer`. The engineer applies the rulings below and fixes the failing suite test and the display defects from 70. QA then re-verifies the items listed under "QA must re-verify".

## Context

G-001, Option A (D-002). QA's verification (70) failed on three spec gaps (D-A, D-B, D-C). All three are settled in `design/combat.md` ("Cells, sides and 'on you'") and `design/combat-visuals.md`, and recorded in D-014. These are the first Design returns for these items (AC-19…AC-28 and V-9…V-17 were new at 70). I did not edit `manual.md` and did not run `play`/`bots`; the rulings come from reading 70 and `repo/game.py`.

## Findings

### Rulings

1. **Cell at .5 (Gap 1, D-A).** `cell(v) = floor(v + 0.5 + 0.005)` on each axis, used for the player and for enemies. An exact .5 (or up to 0.005 below it) goes to the larger index (right/down). The built code uses `int(round(...))` (`cell_of`), which is Python's round-half-even and is float-noise sensitive at .5, the likely reason for the 30 FPS mismatch. For QA's case the player (14.5) is cell 15 and the grub at 13.5 is cell 14, so the grub is drawn **left** at both rates. Also, the display side of an on-you enemy may only be a cell inside the room: for `player 14.5`, a grub on the tile cannot be shown to the right (cell 16 does not exist), so it is shown and knocked left from the first draw. AC-28(b) now says so.
2. **"On you" (Gap 2, D-B).** On you = true distance to the player ≤ 0.5 tile (the body-hit radius, same test as the swipe; tolerance 1e-6). It is defined once and used for the `on you:` entry, the displaced glyph, "(on you)" in telegraph/open/hit lines, and the knockback. The old 0.05-tile `ON_TILE` for text and knockback goes away. A grub 0.2 tile away now reads "(on you)" in every line, has an entry in the `on you:` line, and is drawn displaced; no draw has a side word and an entry for the same enemy. An enemy farther than 0.5 tile gets a side word and no entry, even when it shares the player's cell (it is then drawn in the cell on the side of its true offset, and that is the side the word names).
3. **Side/corner word of an enemy not on you.** From the cell offset to `P` (left/right/above/below for straight, corner words otherwise). If it shares the player's cell, the side of the larger true-offset axis (tie: horizontal). So the word always matches where the glyph is drawn (new V-18). The distance suffix rule is unchanged (compare words, as before).
4. **Hit-line word (Gap 3, D-C).** For a grub: the position word fixed at the instant the Strike begins (end of Wind-up), stored for that strike and used in the `hurt` event and the hit line. Not the lunge position at the damage tick. A still player gets the same word as in the "rears back" line. For QA's 4.3 s case the expected word is the corner word at both rates (the grub wound up from the top right). A draw made during the 0.15 s Strike may show the lunged glyph; the line still names the Wind-up position. Spitter hit lines are unchanged.
5. **Knockback of an on-you grub (D-013 reworded).** Direction: the side it is drawn on. End point: 1.0 tile from the player's true position on that side (so the glyph lands in the cell it was already drawn in). The normal case (more than 0.5 tile away) stays "straight away". Exactly on the tile the result is the same as before; the only behavioral change is for a grub 0.05–0.5 tile away (before: straight away from the true offset; now: toward its display side, ending 1.0 from the player).

### Changed criteria

- `design/combat.md`: **AC-17** (now AC-1…AC-30, adds identical cells/words), **AC-28** (a) adds the 0.2-tile case, (b) rewritten for the edge (`player 14.5`, shown left from the first draw, ends at x 13.5, same cell and words at both rates), **AC-29** (new, cell at an exact half tile: grub at x 13.5 with player 14.5; ±1 pairs at 8.5), **AC-30** (new, one meaning of on you and of position words, and the hit-line word). AC-23, AC-26 (note only) and the knockback text are reworded without changing their pass conditions.
- `design/combat-visuals.md`: **V-10** (adds: no side word for an entry, no "(on you)" without one), **V-12** (adds the 0.2-tile room 2 case), **V-14** (general sentence now compares with the Wind-up start draw), **V-16** (adds half-tile cells and the Strike-start word), **V-18** (new).
- Unchanged: V-9, V-11, V-13, V-17, V-1…V-8, and every other AC.

### QA must re-verify (both frame rates)

AC-17; AC-28 (a, b, and c if a room 2 on-you run is possible); AC-29; AC-30; V-10, V-12, V-14, V-16, V-18; V-15 after the Owner places the manual text. Also the items from 70 §6 that were not observed (AC-1, AC-3, AC-9, AC-10, AC-12, AC-14 real clear, AC-13 restart, V-2/V-4/V-7/V-8 spitter views) remain open for that round. AC-22 (suite part) is the engineer's `test_hit_stun_is_short` matter.

### Previously passing behavior that changes

- Knockback end point of a grub 0.05–0.5 tile from the player (see ruling 5). AC-28(a) as QA ran it (`spawn grub 8 4`) is unaffected: still 9.00.
- The `_pos`-based words: positions near cell borders may now be named by cell (matches the picture). Scripted left/right cases (V-14, V-11) are unaffected. The `ON_TILE` 0.05 test is replaced by the 0.5 test (the same as `BODY_HIT`) for words and knockback. No timing, damage, hit-test, cap or spacing value changes. AC-2, 4, 5, 7, 11, 19, 21, 23–27 and AC-28 a/d/e do not depend on these and should still pass. If the engineer finds that one does, report it back; do not change a number.
- AC-23(c) note: a grub 0.8 tile behind can share the player's cell (for example the player at x 8.4) and is not on you; it is drawn beside `P` on the side it is offset toward and a swipe prints "(miss) not in front". This is the scenario of AC-30(b).

### Notes for the Studio

- The strike cancel window (AC-26, D-58-1) is one tick wide (0.033 s at 30 FPS). No change; written as is. I added a known-note to AC-26.
- AC-21 has a thin margin (1.97 s, limit 1.9). No change; it will move if the engineer changes spacing or the cap, which these rulings do not.
- The art-director reviews the new wording at Verify (D-006 / D-012 stay valid). One point to look at: a draw during the Strike can show the lunged grub nearer than the hit line names (alternative rejected in D-014).
- This was not an escalation case: no direction, scope or pillar change.

### Final V-15 manual lines (for the Owner to place; manual.md not edited)

The existing draft (65, 71) holds for the glyph table, `x`, arcs, practice room and the `on you:` meaning; the points below replace or sharpen the position wording only.

For `manual.md#on-screen`:
- "If a grub is on you, a line starting `on you:` appears under your hearts. It lists each one with its letter, what it is doing (`walking`, `biting soon`, `open`, `charging`, `idle`) and the side where it is drawn, for example `on you: G biting soon (shown right)`. A letter beside `P` that is named on that line is on your own tile, not beside you. A grub that is on you is always hit by your swipe. When no line appears, nothing is on you."

For `manual.md#what-you-hear-and-read`:
- "Lines that tell you where an enemy is use the same words: `on you` (it is within half a tile of you), `left`, `right`, `above`, `below`, and `top left`, `top right`, `bottom left`, `bottom right`. The word names the side of `P` where the letter is drawn. When two enemies of the same kind would get the same word, a distance is added, for example `left, 1 tile`."
- "When you lose a heart the line says what hit you and where it came from: `YOU ARE HIT by a grub (left)`, `(on you)`, `(top right)`, or `YOU ARE HIT by a spit shot from spitter (top right)`. The place named is where the grub was when it started its bite, which is the place you saw it wind up."
- (Outdated line, not required by a criterion) "`(miss)` alone means nothing was within 2.5 tiles; `(miss) too far` means something is within 2.5 tiles but beyond your reach; `(miss) not in front` means something is within reach but outside your swing."

## Decisions already made

- D-001, D-005, D-007, D-011, D-012, D-013 as in 72.
- **D-014 (new):** the rulings above. D-013 stays in force; its direction/end-point wording is superseded by D-014 where they differ, as described in ruling 5.

## Constraints

- The engineer implements; I specify no code structure. Build must not change any number (timings, 0.5 tile, cap, spacing) beyond the new `on you` radius that equals the existing body-hit radius.
- Must play correctly at both 30 and 60 FPS. `manual.md` is the Owner's.

## Open questions

None for the designer. For the Studio: the art-director's review of the wording at Verify; the Owner's suite run and manual text (as in 70); the engineer's explanation of `CrowdTest.test_hit_stun_is_short`.

## Expected output

Build (`gameplay-engineer`): code changes for rulings 1–5 plus the failing test and the display defects from 70; trace/play evidence at 30 and 60 FPS for AC-28(b), AC-29 and AC-30 before handing to QA. Then Verify (`qa`) with the list above.

## Sender assessment

I am confident in rulings 1–3 and 5 (they follow from the cause that QA reported and from the code). Ruling 4 is a choice between the Strike-start position and the last draw the player saw; I took the Strike-start position because the grub stands still then and it does not depend on the frame. The residual risk is the visual mismatch of a lunged glyph in a draw made inside the 0.15 s Strike, noted for the art-director.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, repo/ (build)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/70-qa-to-studio.md
