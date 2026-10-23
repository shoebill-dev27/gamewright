---
kind: handoff
goal: G-002
seq: 49
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 49: studio → gameplay-engineer — implement the V1 supplements (D-022) and run the full suite

## Task

Implement the three V1 supplements exactly as specified in `design/final-boss-and-continuous-run.md` §11 and `decisions/D-022-g002-v1-supplements.md`, add the acceptance tests, update `repo/manual.md`, then run the full suite (including the still-unrun pause/retry tests from 46) and record the source id.

## Context

G-002 (final boss and continuous run). Handoff 46 stopped the V1 supplements for missing spec; the Game Designer answered in 48 (D-022). Pause/retry extension of `bots.play_run` and `tests/test_play_run_controls.py` were written in 46 but never run. Nothing from 46 or this step has been verified yet; results count only against the final source id.

## Findings

The Designer's answers (summary; the design doc §11 and D-022 are authoritative):

1. **Legacy route boss display.** Full §6 display stays on the public-driver routes (`mode run`, `mode room`). The legacy route keeps its 60 s limit and `Player.describe`. Only addition: the player view for legacy `room 5` prints one first line: `note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`. No change to state, events, times, results. No note for rooms 1–4, `room empty`, or the trace view. Tests L1–L4 at 30 and 60 FPS.
2. **Shot IDs and removal reasons (trace and public-driver event log only).** ID `S<n>` per attempt from `S1`, in creation order, boss and spitter shots on one counter, reset on retry. Exactly one `shot_removed` event per shot with `id`, `source`, `reason`, run time, room time. Reasons: `lifetime`, `edge`, `hit`, `absorbed`, `cleared`. The player view gets no IDs and no new wording. Tests S1–S5 at both FPS.
3. **Long observation.** `view-every <seconds>` (default 0.5, range 0.5–60) and `trace-every <seconds>` (alongside existing `frame`); event-driven draws and trace event lines are never thinned; output interval must not affect simulation. Final summary block always printed (end reason clear/death/unfinished, attempts, run time per attempt, per-room times, boss entry hearts, hits taken, swipes, run vs driver vs processing seconds). Periodic lines ≤ `ceil(limit/interval)+1`. Invalid values are rejected before the run with a reason. Option names are defaults; document them in `manual.md`. Tests O1–O6 at both FPS.

## Decisions already made

- D-017: two attacks, boundary recovery, death priority, terminal retry, clock and display contract.
- D-019: old aggregates retired; shared regressions; boss-adapted bot comparison; Designer judgment after measurement.
- D-021: Build on the current repo with Studio-internal text verification; no real device, sha check or extra spending.
- D-022: the three V1 supplements above.

## Constraints

- Rooms 1–4 and shared combat rules unchanged; no new input, checkpoint, HP padding or time tuning.
- Defaults of existing output stay the same (O3).
- Must play correctly at 30 and 60 FPS.
- Do not weaken or edit existing tests; prefer reusing existing systems.
- If a spec case is still ambiguous, stop and hand back `question` naming the case; do not decide it.
- Report results only against the final source id; separate what you ran from what you wrote but did not run.

## Open questions

None.

## Expected output

Address the result to `studio` (the Route will decide the next step): a Handoff reporting the implemented changes, the full-suite result (`run_tests`) with the final source id (including the 46 pause/retry tests), and any spec ambiguity. Do not start Split C (pause/retry normal-run measurement and dodger rooms 1–4 regression pinning) unless the suite is green and the Handoff says so; Split C may follow as the next step (6l).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/manual.md
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/game.py
- Project: repo/tests/test_play_run_controls.py
- Project: repo/tests/test_run_driver.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/48-game-designer-to-studio.md
