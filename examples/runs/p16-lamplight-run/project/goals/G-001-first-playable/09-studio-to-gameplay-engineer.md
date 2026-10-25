---
kind: handoff
goal: G-001
seq: 9
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 09: studio → gameplay-engineer — fix the one erroring test, deliver a green run_tests

## Task

Make `run_tests` (`python3 -m unittest discover -s tests`) pass completely. One test errors because of a typo in the test itself. Fix it without changing any game rule.

## Context

Goal G-001, first playable of Lamplight Keeper. Handoff 08 applied the Night 3 first-screen answer and aligned the tests with the spec. The runtime's Build check on that work was not green: 31 tests ran, 30 passed, 1 errored. QA cannot start until the build is green.

The Build check output:

```text
ERROR: test_first_screen_lit_matches_aim (test_game.StartScreens)
  File "/work/tests/test_game.py", line 51, in test_first_screen_lit_matches_aim
    self.assertIn("Forecast: L -> UP, H -> RIGHT, R -> RIGHT", out)
NameError: name 'out' is not defined
Ran 31 tests, FAILED (errors=1)
```

## Findings

- The only failure is a NameError in `test_first_screen_lit_matches_aim` (tests/test_game.py, around line 51). The variable `out` is used but never assigned in that test. It is a test bug, not a game bug.
- All other 30 tests passed, including the forecast-order and pinned-edge tests changed in handoff 08.
- When you fix the test, check that the expected forecast string for the Night 3 start (aim RIGHT) is correct under the `L, H, R` order and the spec (§4 and §6 of `design/first-playable.md`). Fix the test string if it is wrong; do not change the game to match a wrong string.
- Re-read the whole of `tests/test_game.py` for other undefined names or typos before finishing. Nothing can be run during this step, so a second round trip costs an operation.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Not reopened.
- Handoff 06: option (a), the first screen draws `~` under the starting aim.
- Forecast order `L, H, R` (engineer's choice in handoff 08, kept).

## Constraints

- Python 3 standard library only, deterministic, text output.
- Change only what is needed to make the tests green and consistent with the spec and `manual.md`. No new nights, no new mechanics, no edits to design documents or Decisions.
- `manual.md` must remain consistent with the build.

## Open questions

None. For `game-director` at Review, unchanged: mid-night arrivals, and whether a wreck always loses the night.

## Expected output

- A green `run_tests`, with the fix and any other test corrections described in Findings of your outgoing Handoff.
- Address the result to `studio`, which then composes the QA Handoff from permitted information only. Put your self-evaluation in `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/first-playable.md; repo/manual.md; repo/lamplight.py; repo/play.py; repo/tests/test_game.py
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/08-gameplay-engineer-to-studio.md
