---
kind: handoff
goal: G-001
seq: 60
from: game-director
to: studio
stage: Close
outcome: goal-not-met
---
# 60: game-director → studio — Review G-001: goal-not-met (Phase 1 built and verified; the Goal's intent is not shown; criteria 1 and 2 not judged)

## Task

Close G-001 on this Review result. Record the verdict `goal-not-met`, with criteria 1 and 2 as "not judged", and list the findings and proposed next Goals below in the Outcome. Do not return to Diagnose and do not build Phase 2 in this Goal (D-010).

## Context

Goal G-001 (Owner: 「戦闘が単調なので改善したい」): a player from the player profile should experience combat as varied and engaging rather than repetitive, inside one-button combat (D-001). I compared the evidence with that success condition, not with the plan.

What exists:
- The dash-damage defect fix passed QA (handoff 31).
- Phase 1, encounter escalation, is built in `sim/build-0.8.md`. QA passed criteria 3, 4 (first-shot basis), 5 and 10 (c, d, g) with no regression (handoff 50). The Art Director passed the arrival ring on the described look (handoff 51).
- Both passes rest on build descriptions. No counted or scripted run exists.
- The Playtester run (handoff 57) was a text-only dry run. Part A (50 attempts) is missing, and Part B and the measured parts of Part C are "not available".
- By D-010 the Owner accepted criteria 1 and 2 as "not judged" and skipped Phase 2.

## Findings

### Verdict: `goal-not-met`

This means the Goal's intent is not demonstrated. It does not mean the work failed. Phase 1 is built and verified as far as a description allows. It is not shown to deliver the experience the Owner asked for. I am not calling the Goal `goal-met` because the plan was executed (review-outcome, "Do not").

### Reasoning

1. **No evidence of the experience.**
   - The Goal is about how combat feels to a player: varied and engaging, not repetitive.
   - The only experience evidence is the Playtester's notes, which describe the build text and are not play.
   - They show no hit counts, no dashes, no movement and no run time. They do not say whether a player stops holding one position.
   - QA and Art Director passes show the rules and visuals are as described. They do not show that the player experiences the change.
2. **Criterion 1 is the core test of the Goal and is not judged.** It asks whether rooms 4–5 can still be cleared from one position. Without counts I cannot say the one-stance problem (C1, "enemy behavior gives no reason to move") is gone. I do not substitute reasoning from the room table for it. The existing speeds and room size are also not known, so no calculation supports it either (D-009).
3. **Criterion 2 cannot be met by Phase 1, by design.**
   - D-002 and the spec say Phase 1 creates pressure to move, and the dash gets a purpose only in Phase 2.
   - The dash having no purpose (S3) and shallow enemies (S5) were named symptoms of the Goal. With Phase 2 left out (D-010), the Goal's own diagnosis says these remain unaddressed. This is a gap in the build, independent of the missing counts.
4. **What Phase 1 does support (build description only):**
   - Criterion 3: later rooms differ structurally from room 1. Room 5 differs from room 1 in count, mix, edges and waves. This addresses C3 (no escalation across rooms) as a structure.
   - Arrivals are readable (a 0.8 s ring before each enemy appears, no damage from nowhere). Pillar 3 is respected on the text.
   - The dash fix removes a real defect.
   These are necessary conditions. They are not the experience.
5. **Run length (criterion 6) was never measured.** D-002 set the 15–20 minute target as a limit that must hold. Nothing shows whether more enemies and waves keep a run inside it.

### Criteria status

| Criterion | Status |
|---|---|
| 1 (no one-position clear, rooms 4–5) | **Not judged.** Neither pass nor fail. Not recorded as met. |
| 2 (dash used in combat, Phase 1 part) | **Not judged.** Phase 2 part not built, by Owner decision. |
| 3 (rooms differ) | Pass (QA, description) |
| 4 (threats visible first), P1 | Pass (QA, description; Art Director on the look) |
| 5 (30/60 FPS) | Pass (QA, description) |
| 6 (run length) | Not measured |
| 10 (spawn and wave rules) | Pass for c, d, g (QA, description) |

Others (10a, b, e, f; 7–9) were not re-judged here. 7–9 are Phase 2 and do not apply.

### How far "not judged" limits confidence

- Confidence that Phase 1 is built to its spec is medium to high, within the limits of description-based checks.
- Confidence that the Goal's intent is met, or that it is not met in practice, is low in both directions. I cannot say the result is bad. I can say it is not shown.
- The Playtester notes do not change this. Their one feel-related note, that wave 2 may start before the room looks nearly empty, is a possible suddenness and was not observed. I keep it as a tuning note only.

### Decisions: "revisit when" check

- **D-002:** conditions not shown either way. No post-Phase-1 play shows the one-stance problem solved or passivity persisting, no run time was measured, and Phase 2 was left out by the Owner, not by a TD finding. Option C stays unadopted. It should not be reconsidered before counted play of Phase 1 and a Phase 2 build exist.
- **D-009:** the "dry run's playtest also cannot produce counts" condition was reached. The Owner accepted "not judged" in D-010. No further action in this Goal.
- **D-008 and spec 3.8:** the `SPAWN_FALLBACK` and room-size triggers cannot be checked. No log or room size exists. They stay pre-agreed for the next counted run.
- **D-010:** its revisit condition (real counted records become available) has not been met. The proposed Goals below depend on it.

## Decisions already made

- D-001, D-002, D-009 and D-010 as in the Context. This Review changes none of them.
- No D-011 is written. The Review result is this handoff, and no new Decision is needed.

## Constraints

- Criteria 1 and 2 are "not judged" and must not be recorded as met anywhere in the Outcome.
- Description-based notes are not measured play.
- Phase 2 is not requested in this Goal. It is named only as a proposed next Goal.
- No new input, pillar change or D-001 change is involved in any finding. All findings stay inside the vision.

## Open questions

None for the Studio to answer before closing. Owner-side matters are listed next.

### Items for the Owner

- No escalation trigger fires. Nothing needs the Owner's approval to close.
- For information: closing as `goal-not-met` leaves the original complaint (monotonous combat) not shown as fixed. The Owner decides whether and when to open the proposed Goals. In particular, the dash-purpose and enemy-depth symptoms will only be addressed if the Owner chooses Proposed Goal 2.

## Expected output

The Studio closes G-001 with Outcome `goal-not-met`. It lists the following in the Outcome.

### Proposed next Goals

1. **Counted playtest of the Phase 1 build (criteria 1, 2, 6).**
   - Needs an environment that can run the build, with a clock, the debug log and controller or scripted input.
   - It supplies the 6a record sheet:
     - Part A: hits and deaths for 5 positions × 5 attempts in rooms 4 and 5.
     - Dash use per room 1–5, with the player's reasons.
     - Real run time and clear time per room.
     - The existing values (speeds, hearts, room size, hitboxes).
     - `SPAWN_FALLBACK` counts per room.
     - Arrival gaps of simultaneous Grubs.
     - Whether the early wave 2 start feels sudden.
   - A re-Review follows (D-010, "revisit when"). If criterion 1 fails there, the fallback is the room layout variant (spec 3.6), then tuning knobs 3.5 and section 7.
2. **Phase 2: telegraphed behavior variants (Lunge Grub, Fan Spitter).**
   - Addresses the dash's purpose and enemy depth, which Phase 1 does not.
   - It is specified in `design/g001-combat-escalation.md` section 4.
   - Before Build it still needs:
     - the Art Director's realignment of the lunge committed stage and check A5 (spec 4.6, D-006);
     - Build's report of hitbox sizes and speeds to confirm the "confirm after the report" values;
     - the Technical Director's sub-step check if the lunge speed knob is used.
   - It should go after, or together with, Proposed Goal 1 so that Phase 1's effect is known first.
3. **Wording and housekeeping for the next build description.**
   - Name "table order" as the fixed same-start order.
   - Limit the "1.5 tiles from a corner" Spitter sentence to rooms 3–5.
   - State whether the appearance log line carries the scheduled time.
   - Fix the heading "0.3.3" to the real build number.
   - Name the room 3 Spitter corner as NE.
   - Art Director to confirm the "solid" ring wording.
   - None of these reopens a verdict (handoffs 50 and 51). They can be folded into Goal 1 or 2.
4. **Option C (attack/dash reward rules)** only if passivity persists after counted play of Phases 1 and 2. It would need its own Goal and Decision, and it must not add combo vocabulary.

## Sender assessment

- Confidence in `goal-not-met`: high that `goal-met` cannot be justified on this evidence. Medium that `partially-met` would be the better label. I chose `goal-not-met` because the Owner's expected output allows only two verdicts, and the Goal's stated experience is not shown.
- The most probable real state is that Phase 1 helps with escalation (C3) but leaves the dash and enemy behavior (C1, C2) as they were. This is an inference from D-002's own rationale, not an observation.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/g001-combat-escalation.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-009-judging-basis-criteria-1-and-2.md, decisions/D-010-owner-accepts-unjudged-criteria-and-skips-phase-2.md
- Previous handoff: goals/G-001-combat-monotony/59-studio-to-game-director.md
