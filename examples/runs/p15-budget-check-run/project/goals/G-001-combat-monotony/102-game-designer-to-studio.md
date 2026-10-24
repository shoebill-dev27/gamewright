---
kind: handoff
goal: G-001
seq: 102
from: game-designer
to: studio
stage: Route (document fix done)
outcome: done
---
# 102: game-designer → studio — W1 (15,7) bullet corrected; no other contradiction found

## Task

Report the wording fix to `design/combat-step94.md` and route onward.

## Context

QA 98 found the W1 bullet for the spitter at (15,7) labelled `from the east` while saying the diagonal is expected. The formula was the intended rule, so the label was wrong.

## Findings

Changes in `design/combat-step94.md` (edited in place, wording only):

1. **W1, spitter at (15,7).** The label is now `from the south-east`. The bullet shows the working: travel vector about (-0.92,-0.39), reversed (0.92,0.39), ratio 3/7 = 0.43 > 0.4142, so the diagonal applies. QA checks the traced value against this. This matches the build and QA's trace at 30 and 60 FPS.
2. **W5, brute case.** The timing note covered only the grub ("after the 0.5 s wind-up"). It now adds "for the brute, after its 0.7 s wind-up". Without it the brute case had no stated timing and could be misread as 0.5 s. Not a contradiction, just a gap, and the value comes from the parameter table in `combat.md`.
3. **Changed documents section.** It said the pointer in `combat.md` was "edit below", but no edit exists and the pointer is already in `combat.md` (the "Step 94" paragraph). It now says "done".

Checked W1–W8 and found no other contradiction.
- The other five W1 labels and ratios agree with the formula. For (15,0) the ratio is 4/7 = 0.57, which gives north-east.
- W2 to W4 and W6 to W8 agree with Messages A and B and the Edge cases.

Not touched, outside the task:
- `repo/manual.md` has a stray `>>>REPLACE_PLACEHOLDER` marker (QA 98). I cannot edit it from here. It needs a Build fix, and the manual wording in the note itself is correct.
- The "Manual wording (for the Build step)" section still says the manual could not be edited. That is history, and the Build step has already applied it.

## Decisions already made

- D-011: variant names in messages.
- D-013: wording-only round, then Close.

## Constraints

Documents only. No change to formula, thresholds, timing or build.

## Open questions

None for design. The Studio decides how to handle the QA 98 manual defect and the unshown items.

## Expected output

Studio routes onward. The manual marker goes to Build as a manual-only fix. The W1 (15,7) criterion is now unambiguous, so QA's earlier result for it stands without re-running.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step94.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/100-studio-to-game-designer.md
