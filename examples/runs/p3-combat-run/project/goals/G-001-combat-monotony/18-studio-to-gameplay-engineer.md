---
kind: handoff
goal: G-001
seq: 18
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 18: studio → gameplay-engineer — Make the hit-stun input behavior observable and consistent with D-003 (verification blocker)

## Task

State exactly how the build handles a dash or attack pressed during hit-stun, so that it is ignored and not buffered (D-003). Make the change if the current behavior differs. Record the result in build notes in player-observable terms. Also report the code-side values listed below. Do not change anything else.

## Context

Goal G-001 (combat monotony). The dash/hit invulnerability fix (handoff 08) is being verified by `qa`. QA's second attempt (handoff 15) found that everything described in `sim/build-0.4.md` is consistent with the six criteria in `05-qa-to-studio.md`. QA could not give a verdict on one case: a dash (or attack) pressed during the 0.3 s hit-stun. `sim/build-0.4.md` says only "behaves as it did in 0.3", and `sim/build-0.3.md` does not describe it. D-003 (decided by the designer) requires such input to be ignored, not buffered. Nothing fires during hit-stun or when it ends.

This is the second `question` from step 4a, but for a different missing input. The first was a missing build file, and the second is a missing build behavior. If QA again hands back for the same missing hit-stun observation, the Studio escalates to the Owner.

## Findings

From QA (handoff 15):
- The hit-stun dash press is undescribed in both builds. Neither is observed to be "ignored" or "buffered".
- `sim/build-0.4.md` has the heading "Simulated build 0.3.1" while the file is named 0.4. The Studio needs to know whether they are the same build.
- Flicker and sound cues around the hit and dash are not mentioned in the build text, so QA could not check them.
- The build files are prose and give no repeat counts or measured boundary timings.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-003: input during hit-stun is ignored, not buffered. Hit invulnerability and dash invulnerability are independent timers.
- D-004: Phase 2 technical approach (timestamps on the accumulated game clock, not frame counts). Phase 1 is a separate Build that waits for this fix to pass verification.

## Constraints

- Scope is the hit-stun input handling only. This is not the start of Phase 1; the Phase 1 wave scheduler, marker and room tables are not part of this step.
- The fix must be correct at 30 and 60 FPS. Use timestamps, not frame counts.
- Dry-run project: state the change exactly (what changes, where, how to exercise it). The change then counts as made and the simulator updates `sim/`. If nothing needs to change, say so, and say what the build does, in observable terms.
- If the spec is ambiguous, hand back. Do not decide it yourself.
- No new input buttons.

## Open questions

Answer in your handoff:
1. What does the build do today when dash is pressed during hit-stun, and when attack is pressed? Does anything fire during hit-stun, at its end (buffer), or both?
2. Is `sim/build-0.4.md` (heading "0.3.1") the latest build?
3. Report these code-side values, as the Technical Director and Art Director need them (technical-director handoff 16, task 0, and art-director handoff 17): Grub speed, player speed, projectile speed and range, hearts, room size in tiles, Grub and player hitbox sizes, whether a spawn effect or spawner exists, and where the Flinch is implemented. A value that `sim/repo-notes.md` does not contain should be reported as "not in the code notes".
4. Are there flicker or sound cues for hit invulnerability or dash invulnerability? Describe them in observable terms, so QA can check them.

## Expected output

A handoff with the change (or "no change needed") and the answers above, in observable terms. **Address the result to `studio`**, so that the Studio can compose a clean verification Handoff for `qa` without implementation history. Put your own reasoning only in `## Sender assessment`; it is removed before QA receives the handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md; project.md#constraints; sim/repo-notes.md; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md; decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/15-qa-to-studio.md
