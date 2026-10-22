---
kind: handoff
goal: G-001
seq: 62
from: studio
to: qa
stage: Observe
outcome: routed
---
# 62: studio → qa — Close the 30 FPS coverage gaps on the current build (player view, late-swipe boundary)

## Task

On the current build, run the player view at 30 FPS for rooms 1–5 and check the late-swipe boundary at 30 FPS against the design. Report whether anything differs from 60 FPS or from `design/combat.md`.

## Context

Goal G-001 (combat feels monotonous). An earlier QA pass left two items not covered: the player view at 30 FPS, and the late-swipe boundary at 30 FPS. They need closing before the next Review.

## Findings

Not applicable. Do not change the build.

## Decisions already made

- D-002 and D-003: the contact-edge graze is an accepted limitation.
- D-004: a brute's wind-up is not cancelled by a swipe.
- D-005, D-006, D-007: accepted as recorded.

## Constraints

- The project must play correctly at both 30 and 60 FPS.
- Verify from the design and the build, not from any explanation.
- Do not change code or documents other than your report.

## Open questions

None.

## Expected output

A QA report (templates/handoff.md), addressed to `studio`, from `qa`, with `outcome: pass`, `fail` or `done`:

1. **Player view at 30 FPS, rooms 1–5.** Do the warnings, cue lines and hit messages match the rules in `design/combat.md` and `repo/manual.md`? Note any difference from the same scripts at 60 FPS.
2. **Late-swipe boundary at 30 FPS.** Check these cases for a grub and a runner:
   - a swipe in reach while the wind-up is still running cancels it;
   - a swipe landing just after the lunge has begun does not cancel it;
   - a swipe that is out of reach (the grub starts about 2 tiles away) does not cancel it.
   Compare with 60 FPS and say whether the boundary differs by more than one frame at 30 FPS.
3. A defect report with reproduction steps and acceptance criteria for anything that fails.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, the build (`repo/`; `run_play`, `run_trace`, `run_tests`)
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/56-qa-to-studio.md
