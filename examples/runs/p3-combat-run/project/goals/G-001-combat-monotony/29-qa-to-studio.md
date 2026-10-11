---
kind: handoff
goal: G-001
seq: 29
from: qa
to: studio
stage: Verify
outcome: question
---
# 29: qa → studio — Build 0.5 verification: every observable statement passes, but the wording of criteria 1–6 is not in my packet

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` per criteria 1–6 of handoff 23. This is a partial report. The hit-stun input part (the new part) is fully observable in build 0.5 and passes. I cannot give an overall pass or fail because the text of the six criteria is missing from my packet.

## Context

- The build under verification is `sim/build-0.5.md` (D-007). `sim/build-0.3.md` was used as baseline only. `sim/build-0.4.md` was not used.
- The hit-stun statements in the build description are present. This is **not** a fourth hand-back on the missing hit-stun statements. Nothing is missing from `sim/build-0.5.md`.
- The criteria themselves are the problem. Handoff 23 says they are in `goals/G-001-combat-monotony/05-qa-to-studio.md`, but neither that file nor handoff 23's list of the criteria is in my Load or inputs. Handoff 23 characterises only these:
  - criteria 1 and 2: dash protection, with criterion 2 covering a dash pressed during hit-stun;
  - criterion 5: hit-stun lasts 0.3 s with no input;
  - criterion 6: the frame right after a dash ends while a damage source is in contact.
- I know of criteria 3 and 4 only by number. I will not guess their wording, because that would widen or narrow them, which the handoff forbids.

## Findings

### A. The six hit-stun statements from handoff 28 (criteria 2 and 5), judged from `sim/build-0.5.md`

Each result is the same at 30 and 60 FPS, as the build states. The header says "same at 30 FPS and 60 FPS".

| # | Statement | Result | Evidence in build 0.5 |
|---|---|---|---|
| 1 | A dash press in hit-stun starts no dash and no cooldown | PASS | "Pressing dash at any moment in the first 0.3 s (about 0.05, 0.15 or 0.28 s)… does nothing. The player does not dash, the dash cooldown does not start, and no dash happens when the stun ends." |
| 2 | An attack press in hit-stun gives no swing and enters no dash-queue buffer | PASS | "Pressing attack at any moment in the first 0.3 s does nothing. No swipe appears then, and none appears when the stun ends." Also: "A hit that lands cancels any dash or attack request that was waiting." The description is player-observable, so the buffer is judged by its observable effect. Nothing fires later, which satisfies it. |
| 3 | Nothing fires or is stored at the end of the stun | PASS | The same two bullets: nothing at 0.3 s. |
| 4 | A held button does not fire. Release and re-press works | PASS | "Holding dash or attack down through the end of the stun does nothing at that moment. Nothing fires until the button is released and pressed again. A fresh press after the stun ends works normally." |
| 5 | Presses after 0.3 s are accepted normally. The boundary frame may differ between 30 and 60 FPS | PASS | "A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected." Also: "A press landing exactly at 0.3 s may be accepted on one frame earlier or later at 30 FPS than at 60 FPS." |
| 6 | Hit-stun length is the same at 30 and 60 FPS | PASS | The header says "same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs." The stun is "the first 0.3 s" in all bullets. |

The behavior matches D-003: input is ignored, not buffered.

### B. Dash/hit invulnerability matrix (original defect and related criteria)

I checked each case against `design/combat.md`: the two invulnerability timers are independent, a dash ending does not shorten hit invulnerability, and a hit cannot land during a dash.

| Case | Build 0.5 states | Result |
|---|---|---|
| Dash with no preceding hit | Invulnerable for the full 0.25 s. Damage can land right after the dash ends. | PASS |
| Dash started 0.3–0.55 s after a hit | No damage during the dash or after it, until 0.8 s after the hit. | PASS. This is the original defect case: the 0.3 baseline took damage partway through the dash. |
| Dash started 0.55 s to just under 0.8 s | Protected until the later of the dash end and 0.8 s. | PASS |
| Dash started at 0.8 s or later | Hit protection has ended. The dash gives its own 0.25 s. | PASS |
| Grub contact vs Spitter projectile, and dash toward vs away | Stated to hold for all combinations. | PASS |
| Boundary at exactly 0.8 s or 0.25 s | Counts as after protection. It can differ by one frame between 30 and 60 FPS. | PASS. This is the allowed edge-frame difference. |

### C. Regressions checked against 0.3

- The build states these are unchanged: dash distance, dash duration (0.25 s), the 0.6 s cooldown, enemies, rooms and attacks.
- "A swipe pressed during a dash still fires when the dash ends." This matches `design/combat.md`.
- The build states this never overlaps the stun, since a hit cannot land during a dash.
- The room and pacing observations match 0.3. This was expected, because Phase 1 is not yet built.
- I found no regression.

### D. Optional notes

- **Frame right after a dash ends with a damage source in contact (criterion 6):** damage can land on that frame. In the no-hit case it lands immediately. After a hit, the later of the dash end and 0.8 s governs. The build states the boundary frame counts as "after protection". It differs by at most one frame between 30 and 60 FPS, which is consistent with the spec.
- **Naming mismatch:** the file is `sim/build-0.5.md` but its heading reads "Simulated build 0.3.2". Handoff 23 recorded the same kind of mismatch for 0.4/"0.3.1". This is a labeling issue only, and I treated the file as build 0.5 per D-007.
- **Invulnerability flicker and sound cues:** none described, not checked.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered. Build 0.5 matches it.
- D-007: verify against `sim/build-0.5.md`. I did.

## Constraints

- I did not widen or narrow the criteria. I did not modify the build.
- I cannot assign per-criterion verdicts for criteria 1–6 by number without their text. The role forbids passing on unseen criteria.

## Open questions

1. Please re-route this verification with `goals/G-001-combat-monotony/05-qa-to-studio.md` (the text of acceptance criteria 1–6) added to the Load. The build description needs no further input.
2. With that file, I expect to confirm the verdict from the evidence above. No failure was observed, and every statement in sections A and B passes.

## Expected output

A re-run with the criteria text produces a per-criterion verdict and an overall `pass` or `fail`. This hand-back is for a different missing input from the three earlier ones, which were about the hit-stun description. Routing is therefore not the loop the D-007 limit describes. If the Studio disagrees, the pending decision is whether to accept the section A and B evidence as sufficient and proceed to Phase 1. I cannot make that call, because the role forbids passing a change when a criterion is unjudged.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/28-studio-to-qa.md
