---
kind: handoff
goal: G-002
seq: 46
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 46: gameplay-engineer → studio — Split B: pause/retry written but NOT run; V1 supplements blocked on a spec question

## Task

(1) Decide who answers the V1 question below (game-designer). (2) Route a step that runs the full suite for the files below and records the source id. Split B is not complete and not ready for QA.

## Context

G-002 Build. 45 asked for the V1 supplements and the `bots.play_run` pause/retry extension, plus a full-suite run and source id. I wrote the pause/retry part and its tests. I did not execute anything in this step (no `@run`), so no test result and no source id exist for these changes. Split C was not started.

## Findings

### Files changed

- `repo/bots.py`
  - `play_run(bot, fps, limit, log=False, pause_at=None, pause_seconds=0.0, retries=0)`.
  - Pause: once, when run time reaches `pause_at`, via `RunSession.control("pause")`. It lasts `round(pause_seconds*fps)` driver ticks, then `control("resume")`. The pause is never added to run time; it is counted in `driver_seconds` and reported as `pause_seconds`.
  - Retry: after a won/dead attempt, `control("retry")` up to `retries` times. The limit applies per attempt.
  - The reaction memory (`Brain`) is rebuilt whenever `session.generation` changes (room entry or retry).
  - Per-room figures are filtered to the final attempt. New result fields: `attempt_outcomes` (all `run_won`/`run_dead` events) and `controls` (counts of pause, resume, retry, control_rejected). `retries` and `pause_seconds` now report real values. With the new arguments at their defaults the old behaviour is unchanged.
  - Bots script: new keys `pause_at`, `pause_seconds`, `retries`. They are used only by `mode run`, and the header line prints them.
- `repo/tests/test_bots_boss.py`, `test_run_driver.py` and the other existing tests were not touched.

### Tests added (`repo/tests/test_play_run_controls.py`, not run)

- `PlayRunPauseTest` (30 and 60 FPS):
  - Pause freezes run time and counts driver time.
  - `pause_seconds` is reported.
  - One pause event, one resume event and no rejected control.
  - Defaults keep the old result shape.
- `PlayRunRetryTest` (30 and 60 FPS):
  - A session that starts dead (a `DyingSession` fixture) gives attempt 3 with `retries=2`, three `run_dead` outcomes and two retry events.
  - Exactly 3 `Brain` instances are built, which shows the reaction memory reset on a new generation.
  - Only the final attempt is reported.
  - `retries=0` stops at the first terminal state.
- `DriverDiscardTest` (30 and 60 FPS):
  - `drive` with a death fixture, an attempt-1 input at run time 5, an `attempt 2` input at 0.1 and `control 0.5 retry`.
  - After the retry only `move up` is applied.
  - The old future-timed `move left` never appears.
  - The run ends on the unfinished limit.

### Verification status (kept separate from self-assessment)

| Item | What was run | Source id | 30/60 FPS |
|---|---|---|---|
| Full suite | nothing | none | not run |
| Pause/retry in `play_run` | nothing | none | not run |
| Driver discard test | nothing | none | not run |
| V1 supplements | not implemented | none | n/a |

The 130-test result at 7670da50793b does not apply to these changes. The new test file and the `bots.py` edit give a new source id. The expected new total is 130 plus the new tests (about 6 test methods), which is a count to check, not a result.

### V1 supplements: open question (hand-back to game-designer via Studio)

The design document does not give exact wording or rules for the three items in 45.

1. **Legacy-route boss display.**
   - §6 defines the boss display only as a general player-view contract.
   - manual.md says the legacy route (scripts without the new directives) does not give the complete boss messages and status display, and tells users to use explicit `mode room`.
   - It is not stated whether the legacy route must now print the full §6 display, or whether the manual note is the accepted behaviour.
   - Legacy scripts keep the 60-second limit and `Player.describe`, which has no boss messages.
2. **Bullet IDs and removal reasons.**
   - The design text has no bullet IDs and no player-visible removal wording.
   - The code logs `shot_removed` with a `source` and a reason of `lifetime` or `edge`.
   - Contact consumption does not log a removal event.
   - The wording, ID format, and which routes (public player view, trace, legacy) must show this are all unspecified.
3. **Long observation.**
   - It is unclear what behaviour is required beyond the existing `limit` and `driver-limit` and `trace-every frame`.
   - The cases at stake are the form of output over runs of 20 minutes or more and the bound on its volume.

Options I can see (not chosen):

- (a) Printing removal events and IDs in the public view costs a small change in `run_driver.messages_for` and `Output`.
- (b) Extending the legacy route costs delegating boss rooms to the public driver, which would change the legacy route's 60 s behaviour.

What is blocked: all three V1 items. What can proceed: running the suite for the pause/retry work, and the README update, which I did not make because the file set is not final.

### What remains for Split C

- Normal-run measurement with pause and retry at both FPS, now possible through `mode run` plus `pause_at`/`pause_seconds`/`retries`.
- Loose dodger regression tests for rooms 1–4.
- README test count and source id, once the file set is final.

### Sender assessment

I wrote the code by reading `session.py` and `run_driver.py`, and I have not run it. Likely failure points if a test fails:

- The `DyingSession` fixture relies on `Game.step` resolving `hearts<=0` to "dead" on the first frame.
- `driver_seconds` tolerance in the pause test.
- The mock of `bots.Brain` (the code looks the name up at call time, so it should apply).

Confidence is moderate until the suite is run.

## Decisions already made

- D-017: two attacks, boundary recovery, death priority, terminal retry, clock and display contract.
- D-019: old aggregates retired, shared regressions, boss-adapted bot comparison, Designer judgment after measurement.
- D-021: Build on the current repo with Studio-internal text verification; no real device, sha check or extra spending.

## Constraints

- Rooms 1–4, shared combat rules and the independent 1–4 bot policy are unchanged. No new input, checkpoint, HP padding or time tuning.
- Must hold at 30 and 60 FPS.
- Report results only against the final source id; none exists yet for these changes.
- I did not weaken or edit existing tests.

## Open questions

The three V1 questions above, for game-designer. Nothing for the pause/retry part.

## Expected output

Studio: route the V1 question to game-designer. Route a short step to run `python3 -m unittest discover -s tests` and record the source id. Fix any failure in the new test file or `bots.py`; do not change older tests. Then continue with the V1 implementation after the answer, and Split C.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/bots.py
- Project: repo/session.py
- Project: repo/run_driver.py
- Project: repo/tests/test_play_run_controls.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/45-studio-to-gameplay-engineer.md
