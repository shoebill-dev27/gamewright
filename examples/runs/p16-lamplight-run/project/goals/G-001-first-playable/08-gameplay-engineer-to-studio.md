---
kind: handoff
goal: G-001
seq: 8
from: gameplay-engineer
to: studio
stage: Routing (QA verifies the build against AC-1..AC-15, then the Playtester)
outcome: done
---
# 08: gameplay-engineer → studio — Night 3 first-screen answer applied, tests aligned with the spec, build ready for QA

## Task

Compose the next Handoffs from permitted information only: QA first (against AC-1..AC-15, without the Sender assessment), then the Playtester. Read the `## Build check` the runtime appends below.

## Context

Goal G-001, first playable of Lamplight Keeper. Handoff 07 asked to apply option (a) from handoff 06 and fix the 4 failing tests from handoff 04. This is done. I could not run anything myself; the result is the runtime's Build check.

## Findings

**What changed (all in `repo/`):**
- `lamplight.py`:
  - Removed the `DRAW_LIT_ON_FIRST_SCREEN` constant. `display_lit()` now always returns the tiles lit by the current aim, so the first screen of every night draws `~` under the starting aim. Night 1 and 2 (UP) show none; Night 3 (RIGHT) shows `3 ...T~~~` with `Beam: RIGHT`. No toggle remains.
  - Forecast order is now `L, H, R`, by changing `COMMANDS` to `("L", "H", "R")`. It is used only for the forecast line and for checking that a command is valid. No game rule or movement was touched.
- `tests/test_game.py`:
  - Added the Night 3 first-screen check (`3 ...T~~~`) and a test that Nights 1 and 2 show no `~` on their first screen and Night 3 shows exactly three.
  - Fixed `test_pinned_right_edge`. It played `H` six times on Night 3, but ship 1 is wrecked on turn 4 and the night ends at once (spec §4, step 6), so the test stepped a finished game. It now plays `L L R R R`: ship 3 slides to (3,6) on turn 4, is pinned there on turn 5, ships 1 and 2 dock, and the night is still playing. It also checks the pinned message.
  - Other tests are unchanged. Of the 4 failures in handoff 04, two were the forecast order in the start-screen tests (Night 1 and Night 3). Judging by the visible output, the third was `test_forecast_follows_aim`. The fourth was `test_pinned_right_edge`, whose cause I found by reading the code, not from the output (the output was cut off).
- `manual.md`: states the forecast order `L, H, R` and that lit tiles are drawn `~` on every screen including the first.

**Forecast order chosen: `L, H, R`.** It matches the spec's §6 example, the tests and the manual. The spec does not fix the order, so this is an implementation choice. I found no case that needs a fixed order in the spec.

**How to exercise:**
- `python3 play.py SCRIPT`, with a script of `night 3` alone, for the Night 3 first screen.
- `python3 -m unittest discover -s tests`.
- Scripts from spec §8 (solutions and check scripts).

**Criteria addressed:** AC-1 (first screens, including the `~` rule), AC-3 (beam display), AC-6 (edge pinning, left and right), and AC-15 (forecast aims). No other behavior was changed.

**Known risks:**
- I did not run the tests.
- I did not check AC-15's "derivable from `manual.md` alone" claim.
- E-1..E-5 are untested.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Not reopened.
- Handoff 06: option (a), first screen draws `~` under the starting aim.

## Constraints

- Python 3 standard library only, deterministic, text output.
- QA must receive this Handoff without the Sender assessment.
- Design documents and Decisions were not edited. No new nights or mechanics.

## Open questions

- None for this step.
- For `game-director` at Review, unchanged: mid-night arrivals, and whether a wreck always loses the night.

## Expected output

- Studio routes the build to `qa` for AC-1..AC-15 verdicts by playing scripts.
- If the Build check below is not green, route back to `gameplay-engineer` with the failing output.

## Sender assessment

- By reading the code, the 4 failures from handoff 04 are the 3 forecast-order assertions plus the stale `test_pinned_right_edge`. The visible output only showed the forecast ones.
- The root cause of the fourth failure was a test that stepped a finished game, not a game bug. The spec says a wreck ends the night at once, so the spec wins.
- Confidence is high that the rules are unchanged: the only code changes are the forecast order and removing the display toggle. Confidence in a green run is medium-high, since I have not seen it. If the Build check shows a failure, it is most likely a typo in an expected string in the tests.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 1 (0.0 s).

```text
...........................E...
======================================================================
ERROR: test_first_screen_lit_matches_aim (test_game.StartScreens)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 51, in test_first_screen_lit_matches_aim
    self.assertIn("Forecast: L -> UP, H -> RIGHT, R -> RIGHT", out)
NameError: name 'out' is not defined

----------------------------------------------------------------------
Ran 31 tests in 0.004s

FAILED (errors=1)
```

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/first-playable.md; repo/manual.md; repo/play.py; repo/lamplight.py; repo/tests/test_game.py
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/07-studio-to-gameplay-engineer.md
