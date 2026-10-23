---
kind: handoff
goal: G-003
seq: 15
from: studio
to: qa
stage: Verify
outcome: routed
---
# 15: studio → qa — Re-verify the dash availability display against the D-029 spec

## Task

Verify the current build in `repo/` against the acceptance criteria in `design/dash-availability.md` as ruled by D-029, and report pass/fail per criterion. Address the result to `studio`.

## Context

Goal G-003: the Owner finds it unclear when dash can be used again. The display and wording were changed (not dash rules or timing). Your earlier verification (10) failed at 30 FPS because the spec was ambiguous; the designer then ruled in D-029 (30 FPS tolerance 0.90 s; public-driver pictures after dash messages; rule-driven refusals print; baseline-free Q8/Q12 evidence). A fix Build followed.

## Findings

Facts about the build, not reasoning:

- Files changed in this round: `repo/play.py`, `repo/manual.md`, `repo/public-driver.md`, and the new `repo/tests/test_dash_refusal.py`.
- Intended behavior change: a dash refused by a legacy rule press prints `dash not ready — …`, so `text "not ready"` can be used in rules. `Game` was not meant to change.
- The runtime's Build check ran `python3 -m unittest discover -s tests`: 180 tests, OK. The new timing assertions (51 frames at 60 FPS, 27 frames at 30 FPS start-to-start) were taken from your earlier measurements.
- The "before" build no longer exists, so no before/after comparison can be made.

## Decisions already made

- D-028: the dash indicator is shown on the legacy route too (including room 5).
- D-029: 30 FPS tolerance (0.90 s, ready at 1.500 s for a dash at 0.6 s), public-driver pictures after dash messages, rule-driven refusals print, Q8/Q12 evidence without a baseline.

## Constraints

- Dash rules and timing must be unchanged; the game must play correctly at 30 and 60 FPS.
- Verify from the spec, the acceptance criteria and the build, not from the implementer's explanation.
- Do not widen scope: other issues you find are reported, not fixed or judged here.

## Open questions

- Which source id does each tool show (`summary:` blocks, `bots.py` header), and are they the same kind of id? Report each value as shown.

## Expected output

A pass/fail report to `studio` (kind handoff, `to: studio`), covering:

- P6, P7, Q1, Q2 at 30 FPS against 0.90 s.
- P13 on both routes (legacy rules and public driver), for both attack and dash refusals.
- The Q5 script, and Q7 by trace.
- The 60 FPS press at 1.433 s and 1.450 s.
- P12 via the public replay scripts.
- Q8 and Q12 under D-029.
- An after-only check that game events are identical between the player view and the trace view, apart from the display-only `quiet` field.
- The full test run: `python3 -m unittest discover -s tests`, with the count.

List anything that cannot be verified (e.g., no baseline) in a separate section. Do not count it as pass. Give reproduction commands for any failure. Say plainly what your means cannot show.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, repo/play.py, repo/tests/test_dash_refusal.py, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/12-game-designer-to-studio.md
