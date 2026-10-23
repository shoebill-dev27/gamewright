---
kind: handoff
goal: G-003
seq: 14
from: gameplay-engineer
to: studio
stage: Route (compose the QA re-check from this report)
outcome: partial
---
# 14: gameplay-engineer → studio — Legacy rule-driven dash refusals now print; manual updated; same-code comparison not done

## Task

Route the QA re-check. Note the one gap below (before/after comparison) before deciding.

## Context

Goal G-003, handoff 13. Wanted: a refused dash prints `dash not ready — …` on the legacy rule path too, `text "not ready"` can fire on it, the manual carries the four spec changes, no timing or result changes.

## Findings

**Answer to the open question: yes, the legacy rule path can print the refusal without changing results.**

Root cause: `play.py` `react()` (legacy rules only) marks every `ignored` event produced by a rule press with `details["quiet"] = True` ("a held button, not news"). `Player.describe` returns nothing for quiet events, so the refusal was silent and `text "not ready"` could not see it. The public driver does not set `quiet`, which is why it already printed.

Change (one condition, `repo/play.py`): `quiet` is no longer set when the event is a dash refusal (`action == "dash"` and `"wait"` in details). All other ignored events from rules (e.g. attacks during recovery, `(nothing happens)`) stay quiet as before. The flag is display-only. `Game` is untouched: no event, timing, RNG or order changes. A refusal line does not trigger a picture on the legacy route (the picture triggers are hurt, windup, aim, dash_ready).

Side effects to know:
- Legacy trace view prints event details, so dash-refusal events from legacy rules no longer show `'quiet': True` in their detail dict. That is the only trace difference expected (not a game event change).
- A legacy rule such as `text "dash"` would now also match the refusal line (it contains "dash"); `text "dash ready"` does not match it.

Files changed:
- `repo/play.py` (above).
- `repo/manual.md`: 30 FPS dash line plus the "usual event pictures in a `mode` run" note; rule refusals print and `text "not ready"` is usable (Dash status paragraph). The Reactions table already listed `text "dash ready"`.
- `repo/public-driver.md`: note on event pictures after dash/refusal messages, refusals from any source, 0.85 s / 0.9 s.
- `repo/tests/test_dash_refusal.py` (new): legacy rule refusal (30 and 60 FPS); `text "not ready"` firing a move rule (and not moving without it); public-driver rule refusal; scripted-press refusal; rule attack stays quiet; periodic pictures stay on the 0.5 s grid (except pictures right after `dash ready`) at 30 and 60 FPS; start-to-start 51 frames at 60 FPS and 27 frames at 30 FPS.

**What I could not do**
- I ran nothing myself (no `@run` used), so there is no test count from me, no before/after trace or bot comparison (item 3), and I have not confirmed the new tests pass. The runtime's Build check will report the test result. The new timing assertions (51 and 27 frames) are taken from QA's measured values and should be checked there.
- The "before" recordings can no longer be made, since the edits apply to the project. The no-change argument is the code argument above; QA can add an after-only check (game events identical between player and trace view, stripped of `quiet`).
- Source ids: I could not compute them. `source_id.py` reports a 12-hex sha256 over game.py, session.py, play.py, run_driver.py, bots.py, source_id.py and tests/*.py (path and bytes). The BUILD string `0.6-g002-public-32` is separate. Whether `aa28af2ce710` is the same kind of id as QA's `b62005468da6` I cannot tell from the packet; it changes with my edits and the new test file. Read the new value from any `summary:` block or `bots.py` header line.

## Decisions already made

- D-001, D-028, D-029 (rulings 1–4). No timing change.

## Constraints

- Dash rules and timing unchanged; both 30 and 60 FPS.

## Open questions

- Confirm the source-id relationship and read the post-change id from a run.

## Expected output

QA re-check per handoff 12 (P13 on both routes with both action types, P6/P7/Q1/Q2 at 30 FPS against 0.90 s, Q5, Q7, 60 FPS 1.433/1.450, P12, Q8/Q12 under D-029), with the unverifiable parts listed. Also run `python3 -m unittest discover -s tests` and report the count.

## Sender assessment

Low risk: a display-only flag changed on one path. Confidence that results are unchanged is high by reading, not by measurement. The test file was not executed by me.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.5 s).

```text
nds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.332875691994559, "source_id": "3951a3656940"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "3951a3656940", "trial_count_per_room_fps": 1}
....................................................................................................................................................................................
----------------------------------------------------------------------
Ran 180 tests in 3.428s

OK
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/play.py, repo/tests/test_dash_refusal.py
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/13-studio-to-gameplay-engineer.md
