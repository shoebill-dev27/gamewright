---
kind: handoff
goal: G-001
seq: 28
from: studio
to: qa
stage: Verify
outcome: routed
---
# 28: studio → qa — Verify the dash-damage fix (including hit-stun input) against build 0.5

## Task

Verify the dash-damage fix against the acceptance criteria 1–6 in handoff 23, using `sim/build-0.5.md` as the build under verification. Give a verdict (pass / fail) per criterion, or hand back `question` only if a criterion truly cannot be judged from the build description.

## Context

Goal G-001 (combat monotony). The fix for damage during a dash after being hit (defect confirmed earlier) is built and has to be verified before Phase 1 work starts. Earlier verification attempts ended without a verdict because the build description then in use did not state what happens when dash or attack is pressed during hit-stun. The Owner has since supplied the current build description, `sim/build-0.5.md` (D-007). `sim/build-0.4.md` is an outdated version: do not use it as the build under verification. `sim/build-0.3.md` is the baseline for comparison only.

## Findings

Nothing from implementation is passed on. Verify from the criteria and the build description.

Statements to observe in the build description, as the hit-stun part of criteria 2 and 5 (intended behavior per D-003):
1. During the 0.3 s hit-stun, a dash press does not start a dash and does not start the dash cooldown.
2. During hit-stun, an attack press produces no swing and does not enter the "attack queued during dash" buffer.
3. At the end of hit-stun (0.3 s), neither press fires or has been stored.
4. Holding a button until hit-stun ends does not fire it; releasing and pressing again works normally.
5. Presses after 0.3 s are accepted normally (the boundary frame may differ between 30 and 60 FPS).
6. The hit-stun length is the same at 30 and 60 FPS.

Optional items to note if visible in the build: the frame right after a dash ends while a damage source is in contact; any mismatch between a version heading in a build file and its file name.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered.
- D-007 (Owner): verify against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated.

## Constraints

- Both 30 FPS and 60 FPS must be correct (project constraint).
- Judge from the build description and the spec, not from any explanation of why it should work.
- Do not widen or narrow the acceptance criteria; handoff 23 defines them.

## Open questions

None. If a statement above is not stated by `sim/build-0.5.md`, say exactly which one and in which file. This would be the fourth hand-back on the same missing input, and the Studio will then escalate to the Owner instead of routing again.

## Expected output

A verification report with a verdict per criterion and an overall verdict, plus any regressions and the optional notes. Address the result to `studio`. Set `outcome` to `pass`, `fail` or `question`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md (build under verification), sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/23-studio-to-qa.md (acceptance criteria 1–6)
