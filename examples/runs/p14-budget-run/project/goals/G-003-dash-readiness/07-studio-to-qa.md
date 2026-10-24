---
kind: handoff
goal: G-003
seq: 7
from: studio
to: qa
stage: Verify
outcome: routed
---
# 07: studio → qa — verify the dash readiness display at 30 and 60 FPS

## Task

Verify the built change against the dash readiness acceptance criteria (DR numbers in `design/dash-readiness.md`) and check for regressions. Changed or new criteria: DR2, DR4, DR5, DR6, DR7, DR12, DR13, DR14. Regression criteria, unchanged: DR1, DR3, DR8, DR9, DR10, DR11. Run every check at both 30 and 60 FPS.

## Context

Goal G-003. Owner request: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. The intent is that the player can tell from the player view and `repo/manual.md` whether dash is usable now and, if not, when it will be usable again. The build now shows dash state in the player view and gives specific refusal messages. The dash rules and numbers were not meant to change: the 0.25 s dash, the 0.6 s cooldown and the hit-stun length stay as they were. Decision D-028 settles three points that the spec left open: the tolerance on the ready time, how hit-stun is shown, and when the cooldown starts counting.

## Findings

Nothing to report from earlier steps. Verify from the spec, the Decisions, the manual and the build.

How to exercise the build: use the project's run commands (`run_play` for the player view, `run_trace` for state, `run_tests` for the suite). Useful scenarios:
- Dash, then press dash again at several moments before the dash is ready, and at the moment it becomes ready.
- Practice room, spawn a grub at 8.5 4 so that its lunge hits the player, then give a `dash` input within 0.3 s of the hit.
- Compare the header, the refusal text, the `dash ready` line, the trace value of `dash_ready_in`, and whether the game actually accepts or refuses the dash. They must agree.
- Check that `repo/manual.md` describes what the player view shows.

## Decisions already made

- D-001: one attack button plus dash; no new buttons, no input buffering.
- D-028: dash readiness rulings (ready-time tolerance, hit-stun display, cooldown start, build number).

## Constraints

- Must play correctly at 30 and 60 FPS.
- Judge only against the acceptance criteria and the Decisions. If a case has no defined expected behavior, report it as undefined instead of deciding it.
- Do not change the game or the spec.

## Open questions

None.

## Expected output

A Verify report with a pass or fail verdict per criterion (DR1 to DR14, at 30 and 60 FPS), reproduction steps for any failure, and a list of regressions found or "none". Address the result to `studio`, because a Play step follows and needs a clean Handoff.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-readiness.md, design/combat.md, repo/manual.md, repo/public-driver.md, the build in repo/ (run through the project's run commands)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-readiness-rulings.md
- Previous handoff: none
