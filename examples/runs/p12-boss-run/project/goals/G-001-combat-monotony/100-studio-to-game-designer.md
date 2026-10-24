---
kind: handoff
goal: G-001
seq: 100
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 100: studio → game-designer — Correct the contradictory W1 bullet for the spitter at (15,7)

## Task

In `design/combat-step94.md`, fix the W1 bullet for the spitter at (15,7) so it is not self-contradictory. Look for other places in W1–W8 where the same kind of inconsistency appears and correct them. Change no rule, number or intended behavior.

## Context

Goal G-001. QA verified the wording-only build (98). The build and the direction formula agree: at (15,7) the cue is (-0.92,-0.39), the reversed vector is (0.92,0.39), its ratio 0.42 is above 0.4142, so the hit line says `from the south-east`. QA reports that the W1 bullet for this case is labelled `from the east` and then says the diagonal is expected. QA judged by the formula and passed it.

## Findings

QA's observation (98, W1): the bullet labels the case `from the east` and then says the diagonal is expected. The only open question is the label. The formula is the intended rule.

## Decisions already made

- D-011: variant names in messages (accepted).
- D-013: wording-only round, then Close.

## Constraints

- Documents only. No change to the formula, thresholds, timing or the build.
- If you find that the label is the right intent and the formula wrong, do not decide it here: hand back with outcome `question`.

## Open questions

None.

## Expected output

An updated `design/combat-step94.md` (edited in place) and a handoff to `studio` with `outcome: done`, saying what was changed and noting any other inconsistency found. Studio routes onward.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step94.md, design/combat.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/98-qa-to-studio.md
