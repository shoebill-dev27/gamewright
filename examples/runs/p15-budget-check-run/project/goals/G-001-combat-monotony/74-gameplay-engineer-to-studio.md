---
kind: handoff
goal: G-001
seq: 74
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 74: gameplay-engineer → studio — Room 3 data change from D-012 built (grub at (15,0), second spitter at (10,6)); tests and bots NOT run

## Task

Route to QA (Verify) for Build 22a plus the room 3 change, against `design/combat-step72.md` R3-1 to R3-10 at 30 and 60 FPS.

## Context

Goal G-001. Handoff 73 asked for the D-012 room 3 data change on top of 22a (D-011 messages and manual wording), plus test and bot updates and runs. I could not run `run_tests`, `run_trace` or `run_bots` in this step. Nothing below is a measured result.

## Findings

### Build note

Files changed:
- `repo/game.py`: `ROOMS["3"]` is now `[("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)]`. This is the only code change.
- `repo/tests/test_game.py`:
  - `test_rooms_match_the_spec` also asserts the new room 3 list.
  - A new test checks that room 3 does not clear when only the spitters are dead, and clears when the grub is dead too, at 30 and 60 FPS.

Files checked and left unchanged:
- `repo/bots.py` does not key on room 3 contents, so no bot change was needed.
- `repo/manual.md` does not list any room's contents, so it needs no update.
- The banner stays `Lantern Depths 0.6`.

Position validity:
- (15,0) and (10,6) are inside the room (x 0–15, y 0–8).
- Neither is a wall, and neither overlaps the start at (8,4) or another spawn.
- No hand-back was needed.

Spitter cues:
- Spitter indexing counts spitters only. The order is unchanged, so k = 0, 1, 2 and the first shots stay at 1.8, 2.6 and 3.4 s.
- The grub is not a shot and is not counted by the cap or the cue gap logic.
- The existing test `test_room_3_first_shots_are_staggered...` was not edited. It asserts at most 3 shots in flight over 12 s with room 3 as built, and that should still hold.

How to exercise room 3: `python3 play.py --view trace {script}` with `room 3` and `fps 30` or `fps 60`.

Build name for the playtest brief: "Lantern Depths 0.6 + 22a + room 3 (D-012)". The base is sha 8cce4bb4ffa1, plus 22a, plus this room change. The in-game banner still reads 0.6.

### Results

- **`run_tests`:** not run, including the 22a `VariantMessageTest` cases. 22a's tests are still unrun and are the first thing to check.
- **`run_bots` on room 3:** not run, so there are no clear time, hearts lost or actions per bot. Expectation per D-012 and the design: the walker takes about one more lunge, and its criterion 13 limits may be exceeded. I do not know that. I tuned nothing.
- **R3-3 (grub's first wind-up for a still player):**
  - Not measured. A derived estimate only: the grub starts at (15,0) and the player at (8,4), which is about 8.06 tiles apart.
  - The grub must close to 2.0 tiles at 1.0 tile/s, about 6.06 tiles, so the first wind-up is at about 6.1 s. That is later than the 4.0 s the design wants.
  - If the trace shows otherwise, report the measured time and start position to `game-designer`.
- **Tests at risk:**
  - `test_walker_meets_criteria_13_and_14_at_each_rate` has a lower bound on the walker and requires the dodger to dash at least once in room 3.
  - `test_dodger_agrees_at_30_and_60_fps` covers room 3.
  - `test_bot_log_adds_state_and_changes_no_result` also runs room 3.
  - If one fails because of the grub, report the numbers to `game-designer` as a tuning question, not a build defect. I loosened nothing.

### For game-designer

`design/combat.md` still lists the old room 3 row (14,7 and no grub), criterion 12 and the room 3 purpose. `design/combat-step72.md` governs until the next edit, which should fold in the new row, the criterion 12 contents and the purpose line.

### Decisions made inside the spec

None.

## Decisions already made

D-012, D-007, D-005, D-010, D-011 and D-001 stand.

## Constraints

Room data only. No enemy code, rule, timing, cap, cue-gap or hearts change.

## Open questions

None for the design. The unrun checks above are open for Verify.

## Expected output

QA verifies R3-1 to R3-10 at both frame rates, runs the full suite and the bots, and measures R3-3.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step72.md, design/combat.md, design/combat-step-46-room3-cap.md, repo/game.py, repo/bots.py, repo/tests/test_game.py, repo/manual.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/73-studio-to-gameplay-engineer.md
