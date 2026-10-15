---
kind: handoff
goal: G-001
seq: 82
from: studio
to: qa
stage: Verify (V-17 defeat and dash-off draws, verbatim captures)
outcome: routed
---
# 82: studio → qa — Capture and check the V-17 draws that earlier captures did not cover

## Task

Exercise two cases in the build and check each against V-17, giving verbatim captures at both 30 and 60 FPS.

1. A grub on the player's tile ("on you") is defeated: capture the draw in which the grub is defeated and the draws just before and after it.
2. The player dashes off the tile with an enemy on it: capture the dash-off draw and the draws just before and after it.

## Context

Goal G-001 (combat feels monotonous), Option A. Verify so far found no failing criterion. The visual review of the earlier captures passed everything it could assess, but the defeat draw and the dash-off draw (V-17) were not in the captures, so those two cases are unchecked. The art-director will read your verbatim captures, so they are the main output.

## Findings

Nothing from earlier steps is passed on as an assessment. Verify from the spec, the criteria and the build.

## Decisions already made

- D-011, D-012, D-013, D-014, D-015 (the criteria in the Load list apply as written).

## Constraints

- Both frame rates, 30 and 60 FPS.
- Do not change the repository, `manual.md` or the tests.
- If `manual.md` is not in your environment, the `ManualTest` errors are an environment matter for the Owner's AC-15 run, not a failure of this step. Say so and carry on.
- Colour and the reverse-video cell cannot be shown in a text view. Do not claim them either way.

## Open questions

- Does each case draw what V-17 requires at both rates? If a case cannot be set up with an input script, say exactly why.

## Expected output

A verification report to `studio`: pass / fail / not assessable per case and per frame rate, the scripts used so they can be re-run, and an appendix of verbatim captures (draw text with times) for the art-director. Include any other criterion failure you notice, with a reproduction.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-visuals.md (V-17 and V-9…V-18), design/combat-visuals-verify-rulings.md, design/combat.md, manual.md, the build in repo/ (`run_play`, `run_trace`, `run_tests`)
- Decisions: decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md, decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
- Previous handoff: goals/G-001-combat-monotony/77-qa-to-studio.md
