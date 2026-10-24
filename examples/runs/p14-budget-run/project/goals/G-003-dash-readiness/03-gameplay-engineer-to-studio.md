---
kind: handoff
goal: G-003
seq: 3
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 03: gameplay-engineer → studio — dash readiness display built; ready for independent verification

## Task

Route independent verification of the dash readiness display (header status, use message, refusal with time left, `dash ready` line) against `design/dash-readiness.md` DR1–DR13 at 30 and 60 FPS.

## Context

G-003. Owner request (verbatim): 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. The display from the spec was built on the existing header, message log and `text` reaction. No dash rule or number was changed.

## Findings

What changed (files in `repo/`):
- `game.py`: new events `dash_recharge` (logged right after `dash`) and `dash_ready` (logged once at the frame the recharge ends, after that frame's warnings and hits). A refused dash now logs `left` (R, rounded up to 0.01 s). Helpers `dash_usable()` (the same state that accepts or refuses a dash), `dash_ready_in()`, `dash_status()`.
- `play.py`: header line gets `  dash: ready` or `  dash: recharging R s`; messages `dash recharging: ready again in 0.85 s`, `dash not ready: R s left`, `dash ready`; the trace line carries `dash_ready_in`.
- `run_driver.py`: the same header suffix (after all other items, so after the boss/paused items); the trace record carries `dash_ready_in`; the three dash lines do not cause an extra picture.
- `manual.md`: Dash bullet, new "Dash readiness" section, and the `text "dash ready"` note and example, as in the spec, with the real values (same as the spec's).
- `tests/test_dash_readiness.py`: new tests (ready time, refusal text, no ready line at start, player view lines).

Open questions, answers:
1. Ready time (from the source, not from a run): the recharge timer is set to 0.6 s when the dash ends (0.25 s) and counts down on accumulated time. A dash is refused while the dash or the timer is above 0. So the ready time is the dash start plus 0.85 s, as expected. The spec's rule section and the manual are correct. `design/combat.md` still says "Cooldown 0.6 s" without a start and is not mine to edit; the designer may add "from the end of the dash".
2. Causes for which a dash input does nothing: (a) dash or recharge active → now `dash not ready: R s left`; (b) hit-stun (first 0.3 s after a hit) → existing `(nothing happens)` kept; (c) pause, room-clear screen, terminal or stopped session → the session rejects the input silently (`input_rejected` event, no player message, unchanged); (d) player down or run over → dropped silently, unchanged. A refusal produced by a `when` reaction rule stays hidden, as before.
3. Room entry and retry: every entry makes a new `Game`, so the dash timers start at 0. The header shows `dash: ready` and no `dash ready` line is printed.

Known deviations and gaps:
- During hit-stun the header follows the dash timer and can say `dash: ready` while a dash would be refused for stun (text `(nothing happens)`). The spec's rule "ready iff accepted" and its edge case "display follows the timer" differ here. I followed the timer and did not choose; the designer should rule.
- The build number was not changed (still 0.6, banner and `BUILD`): existing tests check the banner, and the spec leaves the number to the engineer. Say if a new number is wanted.
- In the public driver, a refused dash used to cause a picture (as every message did); it no longer does, as the spec says dash lines add no picture. The `you dash <dir>` line is unchanged.

Not run in this step (no runs were made): DR1–DR13 at 30 and 60 FPS, the DR9 old-versus-new diff, the four DR8 probe scripts, the full existing test suite. The runtime's Build check below is the only test result. Nothing here shows how a human reads the wording.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons (none added; a too-early dash is not buffered).

## Constraints

- Verification should cover both 30 and 60 FPS, times ±1 frame.
- The Playtester must receive only player-visible behavior: the manual's "Dash readiness" section and the lines above. No design experience signals and no implementation detail.

## Open questions

- Hit-stun case above (header says ready, dash refused): designer ruling needed.
- `design/combat.md` wording of the cooldown start (designer).
- Build number: keep 0.6 or bump.

## Expected output

1. QA verifies DR1–DR13 independently at both rates, including the DR9 diff against an unchanged build and the DR8 probe scripts, and says which checks it could not run.
2. The Studio routes the hit-stun question to `game-designer`.
3. A later Playtester gets only the manual and player-visible lines.

## Sender assessment

Confidence is medium-high on the logic: the header, messages and refusal all read the same state, and the ready line is logged at the end of the frame after warnings. Risks: (a) existing tests that compare full player or trace output or event lists could fail because of the new header suffix, trace key and `dash_recharge` events; check the Build check result; (b) the 1e-6 tolerance in the round-up to 0.01 s keeps exact values like 0.35 from rounding to 0.36, which is checked only by the new tests; (c) the 0.5 s picture value R≈0.35 at 30 FPS was not measured.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 1 (3.5 s).

```text
"seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "b9023df69ea2", "trial_count_per_room_fps": 1}
.................................................................F...................................................................................................
======================================================================
FAIL: test_ready_time_is_dash_end_plus_cooldown (test_dash_readiness.DashReadinessTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_dash_readiness.py", line 26, in test_ready_time_is_dash_end_plus_cooldown
    self.assertAlmostEqual(ready[0], 0.85, delta=1.0 / fps + 1e-9, msg=fps)
AssertionError: 0.9 != 0.85 within 0.03333333433333333 delta (0.050000000000000044 difference) : 30

----------------------------------------------------------------------
Ran 165 tests in 3.384s

FAILED (failures=1)
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-readiness.md, repo/manual.md, the build in `repo/` (run commands in project.md)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-003-dash-readiness/02-game-designer-to-gameplay-engineer.md
