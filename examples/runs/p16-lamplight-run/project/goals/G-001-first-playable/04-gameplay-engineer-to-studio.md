---
kind: handoff
goal: G-001
seq: 4
from: gameplay-engineer
to: studio
stage: Routing (spec question to game-designer; QA after it is resolved)
outcome: question
---
# 04: gameplay-engineer → studio — first playable built; one spec contradiction to settle before QA

## Task

Route the open spec question below to `game-designer`. When it is answered, route the build to `qa` (against AC-1..AC-15). Nothing is delivered to QA yet.

## Context

Goal G-001: build Lamplight Keeper's first playable from `design/first-playable.md` (handoff 03). The build is written in `repo/`. All of it is unblocked except one small display question; applying either answer is a one-line change.

## Findings

**Files created (all in `repo/`):**
- `play.py`: entry point.
- `lamplight.py`: game logic, the night data and the script parser.
- `tests/test_game.py`: unit tests.
- `manual.md`: rules, symbols, script format. It has no solutions.
- `README.md`: updated.

**Script format** (defined in `manual.md`):
- Whitespace-separated words. The first two are `night N` (N = 1, 2 or 3).
- Then commands `L`, `R`, `H` (capitals only), one per turn.
- `#` starts a comment to the end of the line.
- Choices of mine inside the spec's "build's to define": a non-command word is reported and skipped; capital letters are required, so `l` counts as unrecognized; a missing `night N` header gives an error and exit code 2.

**How to run** (from `repo/`):
- `python3 play.py SCRIPT`
- `python3 play.py --trace SCRIPT`: adds a `[trace]` line (turn, aim, lit tiles, ship positions, docked, wrecked, status) after every screen.
- `python3 -m unittest discover -s tests`

**Output shape:**
- Each turn shows the header, the board with row and column numbers, the ship list, and the forecast line.
- After a command, the turn's event lines follow, each with positions (slid west or east, moved south, pinned, DOCKED or WRECKED at a position).
- At the end of the night it prints the final board and ship list, then `NIGHT WON on turn N.`, `NIGHT LOST on turn N: ship X wrecked at (r,c).` or `DAWN: ships still at sea ...`.
- Ignored and unrecognized commands, and an unfinished script, are each reported on their own line.

**Tests:** they cover the first screens of all three nights, the aim transitions, `~` display, the three solutions with the position tables, all failure scripts (including dawn and the same-turn dock and wreck), a dock on turn 10 winning, pinning at both edges, determinism, invalid and short scripts, commands after the end, header errors and the trace output. Results are in the Build check below. I could not run anything myself.

**Spec contradiction (blocking the delivery to QA):**
- Night 3 starts with aim RIGHT. §8 draws its first screen with no `~` (`3 ...T...`). AC-3 and §2 say that under RIGHT, (3,4)-(3,6) show `~`, and AC-1 says the first screen shows the board "exactly as in §8".
- It does not change any ship's movement, because lit status is judged after the first command. It only changes the first Night 3 screen.
- Options:
  - (a) Draw `~` under the starting aim. This matches AC-3 and the screen of every later turn. The §8 drawing is then layout only.
  - (b) Draw the first screen with no `~` until a command has been given. This matches the §8 drawing literally, but the lit state would then disagree with the aim shown in the header.
- Cost of either is one constant, `DRAW_LIT_ON_FIRST_SCREEN` in `repo/lamplight.py`. It is currently `True` (option a) so the build runs, but this is provisional until the designer decides. The tests do not depend on it.
- Proposed default: (a), with the designer amending the §8 drawing or AC-1 wording.

**Not checked:** the E-1..E-5 signals (playtest only), and whether the manual alone is enough to derive positions (AC-15), which QA must judge. I did not check how the output looks to a first-time player.

**Other deviations:** none. No mechanics were added.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Implemented as written.

## Constraints

- Python 3 standard library only, text output, deterministic, input scripts only.
- QA must receive this handoff without the Sender assessment, and the manual is all a player is told.
- Do not apply the open-question answer in the code without the designer's decision (the current value is provisional).

## Open questions

- For `game-designer`: should the first screen of Night 3 draw `~` on (3,4)-(3,6), since the starting aim is RIGHT (option a, proposed), or not (option b)? If (a), amend the §8 Night 3 drawing or AC-1. If (b), say how the first-screen lit state should be shown.
- Non-blocking, for `game-director` at Review: the designer's questions on mid-night arrivals and on wrecks always losing the night.

## Expected output

Studio routing (done in Route after seq 4): the display question went to `game-designer` (05). Then `gameplay-engineer` applies the answer, fixes the failing tests reported in the Build check (4 failures, e.g. forecast order `L, R, H` in the build against `L, H, R` in the tests) and reports a green `run_tests`. Only then does the build go to `qa`, with that Build handoff minus Sender assessment.

## Sender assessment

- All three solutions and every failure script in §8 were re-derived by hand against the implemented rules while writing the tests, and they agree with the spec's tables. This is not a substitute for the runtime result.
- Confidence is high on rule logic, medium on the tests until the Build check is read, since I never executed the code.
- The risk is a typo in the test expectations (for example the exact screen strings), not in the rules.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 1 (0.0 s).

```text
\n4 .......\n5 .......\n6 H######\nShips:\n  Ship 1: (1,2)\nForecast: L -> LEFT, R -> RIGHT, H -> UP\n> Turn 1 command: L\n  Ship 1 moved south (1,2) -> (2,2).\n=== Night 1 "First light" | Turn 2 of 10 | Beam: LEFT ===\n  0123456\n0 .......\n1 .......\n2 ..1....\n3 ~~~T...\n4 .......\n5 .......\n6 H######\nShips:\n  Ship 1: (2,2)\nForecast: L -> LEFT, R -> UP, H -> LEFT\nSCRIPT ENDED: the night is unfinished at turn 2 of 10.\n'

======================================================================
FAIL: test_night1 (test_game.StartScreens)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 30, in test_night1
    self.assertIn("Forecast: L -> LEFT, H -> UP, R -> RIGHT", out)
AssertionError: 'Forecast: L -> LEFT, H -> UP, R -> RIGHT' not found in '=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===\n  0123456\n0 .......\n1 ..1....\n2 .......\n3 ...T...\n4 .......\n5 .......\n6 H######\nShips:\n  Ship 1: (1,2)\nForecast: L -> LEFT, R -> RIGHT, H -> UP\nSCRIPT ENDED: the night is unfinished at turn 1 of 10.\n'

======================================================================
FAIL: test_night3_ships_and_coast (test_game.StartScreens)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 44, in test_night3_ships_and_coast
    self.assertIn("Forecast: L -> UP, H -> RIGHT, R -> RIGHT", out)
AssertionError: 'Forecast: L -> UP, H -> RIGHT, R -> RIGHT' not found in '=== Night 3 "Keep it dark" | Turn 1 of 10 | Beam: RIGHT ===\n  0123456\n0 .....3.\n1 ..2....\n2 .1.....\n3 ...T~~~\n4 .......\n5 .......\n6 H#H###H\nShips:\n  Ship 1: (2,1)\n  Ship 2: (1,2)\n  Ship 3: (0,5)\nForecast: L -> UP, R -> RIGHT, H -> RIGHT\nSCRIPT ENDED: the night is unfinished at turn 1 of 10.\n'

----------------------------------------------------------------------
Ran 30 tests in 0.004s

FAILED (failures=4)
```

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/first-playable.md; repo/manual.md; repo/play.py; repo/lamplight.py; repo/tests/test_game.py
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/03-studio-to-gameplay-engineer.md
