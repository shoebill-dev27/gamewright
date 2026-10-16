---
kind: handoff
goal: G-001
seq: 29
from: studio
to: qa
stage: Observe
outcome: routed
---
# 29: studio → qa — Reproduce a possible defect: grub hit right after a lunge-cancelling swipe (room 2)

## Task

Try to reproduce the reported behavior in room 2 and decide whether it is a defect, a rules-conforming case (for example a second grub), or not reproducible. Address the result to `studio`.

## Context

Goal G-001 (combat feels monotonous). A fresh playtester played the current build through input scripts with the player view. In room 2 (2 runners, 1 grub, 2 brutes) they reported:

- a grub began rearing back at about 5.37 s;
- the player swiped and the output said "grub hit" at about 5.9 s;
- the player was hit by a grub at about 6.017 s, about 0.1 s after the swipe.

The manual says a swipe within 1.5 tiles of a rearing enemy cancels its lunge. The playtester could not tell whether the hit came from a different grub or whether the cancel failed, and is unsure it is a defect. Impact judged low. The room 2 start count they saw was probably 1 grub; they noted a second `G` later, which may be a brute, not a grub.

## Findings

Observations only. The playtester's run used a reaction-rule script (sidestep on "rears back", swipe things within about 1.4 tiles, approach). The exact script was not preserved, so reconstruct comparable play with the trace view. The playtester's report is in the previous handoff.

## Decisions already made

- D-002: per-frame contact sampling is kept; the contact-edge graze is an accepted limitation, so check that this case is not just that graze. A lunge-band note for D-002 is with the game-designer in a separate step.

## Constraints

- Verify from the design documents, the manual and the build, not from any explanation of how it should work.
- Check at both 30 and 60 FPS. Use `run_play`, `run_trace` and `run_tests` from `project.md`.
- Report only: do not change the build.

## Open questions

- In the trace, which enemy dealt the 6.017 s hit, and was its lunge cancelled, staggered or already in flight when the swipe landed (distance at swipe time versus the 1.5-tile rule)?
- Is the outcome consistent with the documented rules (design/combat.md, repo/manual.md, D-002)? If the documents are silent or conflict, say so; do not rule on intent.

## Expected output

A defect report with exact reproduction steps and acceptance criteria if it is a defect; otherwise a clear "not a defect / not reproducible" with the trace evidence and, if the documents are unclear, the question for the game-designer. Severity and reproducibility are yours. Address it to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/ (run_play, run_trace, run_tests)
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/27-playtester-to-studio.md
