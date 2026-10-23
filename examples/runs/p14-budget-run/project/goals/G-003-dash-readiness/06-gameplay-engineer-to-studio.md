---
kind: handoff
goal: G-003
seq: 6
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 06: gameplay-engineer → studio — dash readiness fix list applied; ready for Verify

## Task

Route to `qa` (Verify), then Play. Check DR2, DR4, DR5, DR6, DR7, DR12, DR13 and the new DR14 at 30 and 60 FPS, plus the unchanged criteria DR1, DR3 and DR8–DR11.

## Context

G-003 (Owner: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」). Handoff 05 ruled on three spec points (D-028) and gave a fix list. This step applies that list. No dash rule or number was changed.

## Findings

What changed and where:
- `repo/game.py`
  - `dash_usable()` now also requires `stun_left <= 0`. It is still the only state that decides whether a dash is accepted.
  - `dash_ready_in()` returns the larger of the recharge-based time and `stun_left`. `dash_status()`, the refusal text and the trace `dash_ready_in` all read it, so header, refusal and acceptance share one state.
  - `press()`: a dash input during hit-stun now logs `ignored` with reason `dash not ready` and `left` (rounded up 0.01 s). It prints `dash not ready: R s left` instead of `(nothing happens)`. Other inputs in stun still log `stunned`.
  - The `dash_ready` event is driven by a new flag, `dash_pending`. It is set when a dash is accepted. It is cleared, with the line logged, at the first frame where `dash_usable()` is true. So the line prints at the stun end if the stun outlasts the recharge. A stun alone prints no line.
  - The dash timers and the stun length are untouched.
- `repo/tests/test_dash_readiness.py`
  - The ready-time assertion is now `0.85 - 1e-6 <= ready <= 0.85 + 2/fps + 1e-6` at fps 30 and 60. The message carries the fps.
  - New hit-stun tests (DR14): header and refusal state during the stun, `dash_ready_in` equal to the displayed R, refusal text, no `dash ready` line, and the dash is usable after the stun.
  - New test for the exact text printed for a stun refusal.
- `repo/manual.md`: the Dash bullet now says "about 0.85 s" and "the dash, the recharge or the moment after you are hit". "Dash readiness" has the new hit-stun sentence.

How to exercise: practice room, spawn a grub at 8.5 4 (lunge hit), then a `dash` input within 0.3 s of the hit. Expected: header `dash: recharging R s`, `dash not ready: R s left`, no `dash ready` line afterwards.

Not run in this step: I made no `@run`. The runtime's Build check follows this handoff. Nothing here is measured. The 0.9 s at 30 FPS ready time is accepted by the ruling; I did not look for an off-by-one cause.

Known risks for QA:
- `stun_left` is not snapped to 0 at the end. A float residual could keep the stun, and so the "recharging 0.01 s" display, one frame longer. Header and acceptance stay consistent, because both read the same state. Only the exact stun-end frame could differ by one.
- The `dash ready` line is now logged only when the dash is usable. If a hit lands in the same frame as the recharge end, the line moves to the stun end. That is the ruled behavior.
- Hit-stun refusals made by reaction rules are marked quiet (the existing rule for held buttons). So the refusal text is not printed for a rule-driven dash.

## Decisions already made

- D-001: one attack button plus dash; no buffering.
- D-028: the ready-time bound (0.85 s to 0.85 s + 2 frames), the hit-stun display, the cooldown wording, build number 0.6 kept.

## Constraints

- No change to 0.25 s, 0.6 s or the hit-stun length.
- Works at 30 and 60 FPS.
- Header, messages and manual agree.

## Open questions

None.

## Expected output

A `qa` Verify handoff covering DR numbers 2, 4, 5, 6, 7, 12, 13 and 14 (changed or new), plus DR1, 3 and 8–11 as regression. Then Play.

## Sender assessment

The root cause of the 0.9 s reading is not established; it is consistent with frame rounding of the dash end and the recharge end. Confidence is moderate, because I did not run the code. The edits are small and the paths are shared.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.5 s).

```text
"driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3416647360427305, "source_id": "04e368b0f6ed"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "04e368b0f6ed", "trial_count_per_room_fps": 1}
.......................................................................................................................................................................
----------------------------------------------------------------------
Ran 167 tests in 3.418s

OK
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-readiness.md, design/combat.md, repo/manual.md, repo/game.py, repo/play.py, repo/run_driver.py, repo/tests/test_dash_readiness.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-readiness-rulings.md
- Previous handoff: goals/G-003-dash-readiness/05-game-designer-to-gameplay-engineer.md
