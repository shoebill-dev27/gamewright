---
kind: handoff
goal: G-002
seq: 45
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 45: studio → gameplay-engineer — Split B: V1 supplements and bots.play_run pause/retry extension

## Task

Implement Split B: (1) the V1 supplements, (2) extend `bots.play_run` with pause and retry and add tests for it. Run the full suite and report the source id with the results. Split C is a later step; do not start it.

## Context

G-002 Build. 44 added `repo/tests/test_boss_contract_details.py` (18 tests; B3, B6, B7, B9, B10, T1–T4, C2, C3). Result: 130 tests OK at source id 7670da50793b, no production change, no spec gap. Remaining Build work is Split B (this step) and Split C (6l). Independent QA waits until both are done.

## Findings

From 44 (summary):

- `RunSession.control("pause"|"resume"|"retry")` returns True/False and logs `pause`, `resume`, `retry`, `control_rejected`.
- Discarding future-timed old inputs on retry lives in the driver (`drive`) and is not yet tested.
- The README still says "112 tests".
- The 112-test baseline at 5145454ab956 was not re-confirmed separately; it is not required now.

Split B scope:

1. **V1 supplements** (per design/final-boss-and-continuous-run.md and D-017/D-019): legacy-route boss display, bullet IDs and removal reasons, long observation. Take the exact wording from the design document; if it is ambiguous or missing a case, hand back with a question rather than deciding.
2. **bots.play_run**: add `pause_at`, `pause_seconds`, `retries` parameters using `RunSession.control`; reset reaction memory on a new generation (after retry). Add tests, including that old future-timed inputs are discarded on retry in the driver.
3. Update the README test count / source id only if the file set is final after this step; otherwise leave it and say so.

## Decisions already made

- D-017: two attacks, boundary recovery, death priority, terminal retry, clock and display contract.
- D-019: old aggregates retired; shared regressions; boss-adapted bot comparison; Designer judgment after measurement.
- D-021: Build on the current repo with Studio-internal text verification; no real device, sha check, purchase or extra spending.

## Constraints

- Rooms 1–4, shared combat rules and the independent 1–4 bot policy stay unchanged. No new input, checkpoint, HP padding, or tuning toward 15–20 minutes.
- Must hold at both 30 and 60 FPS.
- Any code or test change gives a new source id; report results only against the final id.
- Do not weaken or edit existing tests to pass; if one fails, fix the cause or report it.

## Open questions

None expected. If the spec is ambiguous for V1, hand back as `question` with the exact case.

## Expected output

Handoff to `studio` (address the result to `studio`) containing: files changed, tests added, full-suite result and final source id, per-item table for V1 and pause/retry (what was run, at which id, 30/60 FPS), and what remains for Split C. Keep verification claims separate from self-assessment.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/manual.md
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_run_driver.py
- Project: repo/tests/test_boss_contract_details.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/44-gameplay-engineer-to-studio.md
