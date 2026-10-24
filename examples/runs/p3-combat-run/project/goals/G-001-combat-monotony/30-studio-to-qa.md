---
kind: handoff
goal: G-001
seq: 30
from: studio
to: qa
stage: Verify
outcome: routed
---
# 30: studio → qa — Verify the dash-damage fix (incl. hit-stun input) against build 0.5, with the criteria text supplied

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` and give a per-criterion verdict for criteria 1–6 plus an overall `pass` or `fail`. This repeats the verification of handoff 28. The only change is that the text of the acceptance criteria is now in your Load list.

## Context

- Goal G-001 (combat monotony). Before Phase 1 of the chosen direction is built, the earlier dash-damage fix and the hit-stun input change must be verified.
- Build under verification: `sim/build-0.5.md` (D-007). `sim/build-0.3.md` is the baseline only. `sim/build-0.4.md` is outdated; do not use it.
- Your previous report (handoff 29) found every observable statement in `sim/build-0.5.md` consistent with the criteria. It could not give a verdict because the criteria text was missing. That text is in `goals/G-001-combat-monotony/05-qa-to-studio.md` (your defect report with the acceptance criteria), and handoff 23 restates and numbers the criteria. Both are in the Load list now.
- The hit-stun statements are present in build 0.5. That question is closed. This is not a hand-back on the same missing input.

## Findings

Nothing from the implementation side is passed to you. Your own handoff 29 (sections A to D) is in the Load list. You may reuse its observations from `sim/build-0.5.md`, but re-check each against the criteria text, since that text is new to you.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered.
- D-007: verify against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated.

## Constraints

- Do not widen or narrow the criteria. Use the wording in handoff 05 and the numbering in handoff 23. If the two disagree, report exactly where and judge against 05.
- Must hold at both 30 and 60 FPS. A one-frame difference at an exact boundary is allowed where the spec allows it.
- Do not modify the build.
- Loop limit: if the criteria text for any numbered criterion is still not available after this Handoff, say exactly which criterion and what is missing. The Studio will then escalate to the Owner for that input and will not route it to a Role again.

## Open questions

- Is the wording of criteria 1–6 now sufficient to give a verdict on each? If not, which criterion is unclear?
- Keep your optional notes: the frame after a dash ends with a source in contact; the file name versus heading mismatch (`sim/build-0.5.md` reads "0.3.2").

## Expected output

A verification report (verify-change) with a verdict for each of criteria 1–6, an overall `pass` or `fail`, and the regression check against the baseline. Write it as a handoff addressed to `studio`. Do not hand back `question` unless a criterion's text is truly missing or contradictory; if it is, name it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
- Also: goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria text), goals/G-001-combat-monotony/23-studio-to-qa.md (criteria numbering), goals/G-001-combat-monotony/28-studio-to-qa.md (the previous request)
