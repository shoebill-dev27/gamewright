---
kind: handoff
goal: G-003
seq: 7
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 07: studio → gameplay-engineer — Build the dash availability display (A+B+C) with the source files now supplied

## Task

Implement `design/dash-availability.md` in `repo/` and `repo/manual.md`: the always-visible dash field, the refusal and ready messages, and the manual text. Change no game result, dash rule, timing or input.

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Diagnose (02) found missing display information, and Design (04) specified the fix. The first Build attempt (05, answered by 06) stopped without changing anything, because `repo/game.py`, `repo/run_driver.py`, `repo/session.py` and the tests were not in its packet. They are in the Load list below. No sha was built and nothing has been verified yet. The step 05 Expected output still applies.

## Findings

From 06 (engineer's own hand-back; the spec had no ambiguity):

- Legacy route: `Player.snapshot` prints `[t s] hearts n/3`, so the dash field can be appended there. `Player.describe` produces the event messages (`you dash <dir>`, and `(nothing happens)` for `ignored`). The ready moment can be detected per frame, before the next input is processed (spec 3.3 order).
- Reaction rules read `view.messages` and `game.hearts` only. A `dash ready` message and the refusal text must therefore be added to `messages` so that `text "dash ready"` and `text "not ready"` work.
- `bots.py` reads `game.dash_left` and `game.dash_cooldown` directly, so the extra text cannot affect bot input.
- Still to find in the now-supplied files:
  - Which condition makes `press("dash")` refuse (cooldown, active dash, hit-stun, attack recovery).
  - Whether `dash_cooldown` counts during the dash or only after it. The documented start point is the dash end.
  - How a refusal is reported.
  - Where hit-stun and room entry clear the state (Q3, Q5).
  - How the public driver and `RunSession` print their status line.

## Decisions already made

- D-001: no new input buttons.
- D-022: the legacy route stays limited; only the display is added.
- D-028: the dash indicator is shown on the legacy route too, including room 5.

## Constraints

- No change to dash rules, recovery length, invulnerability, timing or inputs. Game results must be identical with the new field and text stripped (spec Q8).
- Must work at 30 and 60 FPS.
- Reuse the existing text view and message system. The field must appear on both the legacy route and the public driver (`mode run` and `mode room`).
- Edit only the tests and goldens that compare the new field or text, and name each one in your report.
- If the file volume forces a split (legacy route first, public driver second), return `partial`. The Studio will route the rest back to you. QA is only routed once both routes are done.
- If the code shows a spec ambiguity or a real cooldown difference the spec cannot document as is (Q3, Q4), hand back to the Studio for Design. Do not decide it yourself.
- Do not edit decisions.

## Open questions

- Q3 (hit during cooldown), Q4 (attack recovery vs dash), Q5 (room-transition clear) and 30 FPS behavior: observe them in the code and by running the build, and report what you saw. Do not assume.

## Expected output

The change in `repo/` and `repo/manual.md`, then a Handoff addressed to `studio` (the Studio composes the QA Handoff) with:

- the new sha;
- the files changed;
- the tests run (`python3 -m unittest discover -s tests`) and their results;
- the tests and goldens edited;
- what was observed for Q3, Q4, Q5 and at 30 FPS.

Put your own reasoning in `## Sender assessment`, which is removed before QA receives the Handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, repo/play.py, repo/game.py, repo/run_driver.py, repo/session.py, repo/source_id.py, repo/bots.py, repo/README.md, repo/tests/test_game.py, repo/tests/test_session.py, repo/tests/test_run_driver.py, repo/tests/test_play_run_controls.py, repo/tests/test_terminal.py, repo/tests/test_split_c.py, repo/tests/test_d022_observation.py, repo/tests/test_d022_shots_and_note.py, design/final-boss-and-continuous-run.md#2-ランと入場, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/06-gameplay-engineer-to-studio.md (the original task and Expected output are in goals/G-003-dash-availability-clarity/05-studio-to-gameplay-engineer.md)
