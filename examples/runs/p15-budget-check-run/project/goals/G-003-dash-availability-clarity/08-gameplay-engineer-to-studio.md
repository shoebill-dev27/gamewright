---
kind: handoff
goal: G-003
seq: 8
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 08: gameplay-engineer → studio — Dash availability display built (legacy route and public driver); Studio composes the QA Handoff

## Task

Compose the QA Handoff for G-003 from this report. The change is in `repo/` and `repo/manual.md`. Verification is open: I executed nothing in this step.

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Step 07 supplied the source files that step 05 lacked. This step implements `design/dash-availability.md` sections 3 and 8 on both routes (D-028). Dash rules, timing, inputs and game results are unchanged.

## Findings

**What was built (display and events only):**

- `repo/game.py` (EDIT blocks only; the previous attempt's both-ways error is fixed):
  - `dash_seconds(r)`: ceil of `(r − 0.001) × 10` as tenths, at least 0.1.
  - `Game.dash_state()`: `active`, `wait` or `ready`, using exactly the refusal conditions of `press("dash")`: `dash_left > 0`, `dash_cooldown > 0`, `stun_left > 0`.
  - `Game.dash_wait()`: R. While active it is `dash_left + 0.6`; otherwise `max(cooldown, stun)`.
  - `Game.dash_why()`: `dashing`, `hit-stun` when the stun is longer than the cooldown, otherwise empty.
  - New event `dash_ready`, logged at the end of the frame (after `_resolve_result`) when a dash was used (`dash_pending`) and the state is ready. It is not logged after death or a room clear. A new `Game` per room entry resets it.
  - The `ignored` event of a dash press now carries `wait` and `why`.
  - The existing `dash` event is the spec's `dash_start`; `dash_end` already existed. No duplicates were added.
- `repo/play.py`:
  - `dash_field(g)`; it is empty on terminal frames.
  - The legacy `[t s] hearts n/3` line now ends with `— dash: …`.
  - `describe` text: `you dash <dir> — usable again in 0.9 s`, `dash not ready — <R> s left[ (dashing|hit-stun)]`, `dash ready`.
  - `dash_ready` triggers an event picture.
  - The legacy trace state line gains `dash_cooldown=`.
- `repo/run_driver.py`: the status line gets the field at its end when the state is `combat`, including when paused. Messages come through `Player.describe`, so `mode run` and `mode room` use the same text.
- `repo/manual.md`: the Dash line, the `Dash status` section and a `text "dash ready"` example, per spec section 8.
- New `repo/tests/test_dash_display.py`.

**Observed from the code (not run):**

- **Q3 (hit during cooldown).** `_hurt` does not touch `dash_cooldown`. The cooldown end is unchanged and `R = max(cooldown, stun)`, as the spec says. This matches the spec; no escalation. Test: `test_a_hit_does_not_change_the_cooldown`.
- **Q4 (attack recovery).** The dash branch of `press` does not check `recovery`. Recovery does not block a dash, so no recovery suffix is needed. Test: `test_attack_recovery_does_not_block_a_dash`.
- **Q5 (room entry).** `RunSession._enter` builds a new `Game`, so cooldown, stun and `dash_pending` are cleared. No `dash ready` is printed at entry, and the entry picture shows `dash: ready`.
- **Cooldown start.** The cooldown is set to 0.6 at the frame the dash ends, and decrements from the next frame. The documented dash-end start point matches the code.
- **30 FPS.** Not run. Everything is in seconds on accumulated time, so the spec's ±1 frame applies. The tests are written for both rates.

**Behaviors to be aware of (not decided by me):**

- In the public driver every message already prints a picture. The accepted-dash and refusal messages therefore also get a picture there, as `(nothing happens)` did before. Spec 3.3 says "no extra picture" for them. The legacy route follows the spec. This is a possible spec/build difference for QA to confirm.
- Refusals caused by reaction rules stay quiet (the existing `quiet` rule for held buttons). `text "not ready"` therefore matches only refusals from scripted presses. `text "dash ready"` works for all.
- The refusal text applies only to dash presses. Other ignored inputs still print `(nothing happens)`.
- `dash ready` is emitted at the end of the frame that reaches ready, before the next frame's inputs, so a press at that time is accepted after the line.

**Tests and goldens:**

- Run: none in this step. The runtime Build check supplies `python3 -m unittest discover -s tests` against the built source.
- Edited: no existing test or golden. I found none that compares the `hearts n/3` line, the dash text or `(nothing happens)` for a dash.
- Added: `tests/test_dash_display.py`: rounding, script P at 30 and 60 FPS, no `dash ready` without a dash, hit-stun reason, Q3, Q4, state-equals-press, once per dash, the public driver and a `text "dash ready"` rule.
- sha: not computed (not executed). Take it from the Build check or the `source` line of `bots.py`.

## Decisions already made

- D-001: no new inputs.
- D-022: the legacy route stays limited; only the display was added.
- D-028: the indicator is on the legacy route including room 5.

## Constraints

- Game results must be identical with the dash field, dash text and `dash ready` lines and pictures stripped (Q8).
- Both 30 and 60 FPS apply.

## Open questions

- Public-driver pictures for the accepted-dash and refusal messages (above): confirm whether this is acceptable or Design must decide.
- Whether the bots' `ready` reading and printed state agree under float residue: QA's Q7 covers it. The display uses the same predicate as `press`.

## Expected output

- The Studio composes the QA Handoff (spec sections 5 and 6, Q1–Q12), stripping Sender assessment.
- If the Build check reports test failures, route back to gameplay-engineer.

## Sender assessment

Confidence is medium-high on logic and medium on first-run test results, because nothing was executed. Risks: exact printed times in my tests at 30 FPS (they rest on hand arithmetic), and `test_state_matches_press`, which builds probe games from copied timers.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.6 s).

```text
_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.34066059900214896, "source_id": "b62005468da6"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "b62005468da6", "trial_count_per_room_fps": 1}
.............................................................................................................................................................................
----------------------------------------------------------------------
Ran 173 tests in 3.520s

OK
```

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, repo/game.py, repo/play.py, repo/run_driver.py, repo/manual.md, repo/tests/test_dash_display.py
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/07-studio-to-gameplay-engineer.md
