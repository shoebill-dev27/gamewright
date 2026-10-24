---
kind: handoff
goal: G-001
seq: 46
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 46: studio → gameplay-engineer — Phase 1 narrow Build: ring dot colour and build statements S0–S3, plus clarification of four spec points

## Task

Make one narrow look change to the Phase 1 spawn marker ring, state four build statements (S0–S3), and confirm in writing four points of the amended Phase 1 spec (a–d below). Where the build as it stands differs from any of these, change it to match and say exactly what changed. State the whole result exactly, so the build description can be updated from it.

## Context

G-001, Phase 1 (encounter escalation), build 0.6. QA's Verify (handoff 40) judged criteria 3, 4, 5 and 10 as pass from the description, and left criteria 1 and 2 (Phase 1 part) open. The Art Director's visual review (handoff 41) passed the ring on its described look, with three capture checks open. Two follow-ups came back:

- The Game Designer (handoff 44, D-009) set the judging basis for criteria 1 and 2 (deferred to the playtest, judged from counts) and answered QA's design items. No rule changes. The Designer asks for a clarification in the build description (Part B).
- The Art Director (handoff 45) found that `sim/build-0.6.md` describes the ring's dot as "hot, near-white" in its last phase, which does not match the spec palette. The Art Director requires one look change and three added statements (Part A).

Both are small. After this Build, QA re-verifies a narrow set of criteria and the Art Director re-reviews the dot in parallel.

## Findings

### Part A — look change and statements (decided by the Art Director)

**Change (arrival ring, solid phase 0.6–0.8 s only):**

- The centre dot is `#FFC14D` (amber hot core) at full brightness. No tint toward white or blue, and no white or cold-white bloom or glow. Any glow around the dot uses only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot stays dim amber as built.
- Unchanged: ring colour `#FF5A1F`, all timings (solid phase starts at 0.6 s, burst at 0.8 s), the ring's size and shape, and all rules.
- Reason: D-006 reserves the cold-white family (`#E8F4FF`) for hit feedback on flinch-immune enemies. "Near-white" leaves the dot's hue unstated, and a white-looking core weakens the orange/red threat read (pillar 3) at the "now" moment.

**Statements to state exactly.** For each, say whether the build already behaved that way (documentation only) or you changed it:

- **S0:** "In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness." This replaces "hot, near-white core colour".
- **S1:** "The ring and its dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s." If the build differs, make it so.
- **S2:** "The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`. It contains no white, near-white or cold-white element."
- **S3:** "Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above a single ring's peak, and each ring keeps its own dot."

**Pass condition for the Art Director's re-review:** the build description states `#FFC14D` for the dot, and no element of the ring or burst is white or near-white.

### Part B — clarification of the amended spec (decided by the Game Designer, D-009)

Read `design/g001-combat-escalation.md` (3.3, 3.8, 6, 6a, criteria 4, 5, 10) and D-009. State each point as the build behaves. D-009 and the spec are authoritative.

- **(a) Point choice (3.3), including the mixed case and tie-break.** Order: first a far-and-free candidate; else the farthest not-occupied candidate (so a near, free point beats a far, occupied one, because a marker stacked on another marker or enemy hides the warning); else the farthest overall. Ties go to the earlier list entry. If the mixed case (near and free versus far and occupied) was built differently, change it to this order and report the change.
- **(b) Sampling.** The player position and the occupancy for the 5-tile and 1.5-tile tests are read on the first logic frame at or after the scheduled marker start. Handoff 37 already described this for the player position, so confirm that it also covers occupancy.
- **(c) Spitter first shot.** It is scheduled at the scheduled appearance + 1.0 s (then every 2 s, as built).
- **(d) Existing values (3.8).** State every existing value you can read (Grub speed, player speed, projectile speed and range, hearts, room size, hitbox sizes). For each one you cannot read, write "not available". Do not estimate.

## Decisions already made

- D-001: one-button combat. D-004: gameplay numbers are data.
- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies.
- D-008: Phase 1 spawn and wave rules. D-009: judging basis for criteria 1 and 2, and the D2–D6 answers. D-009 amends 3.3, 3.8 and criteria 1, 2, 4, 5, 10 without editing D-008.

## Constraints

- Change no timing or rule, and nothing in the verified dash, hit-stun or invulnerability behavior (build 0.5 baseline).
- Correct at 30 and 60 FPS. No random number use for spawn choice.
- Phase 2 content and the hit overlay for flinch-immune enemies are out of scope.
- No new input buttons.
- If part of this task is ambiguous or contradicts the spec, stop on that point and hand back `question` naming it, as in earlier Builds. The Studio escalates to the Owner only if the same missing input is handed back twice with nothing new supplied.

## Open questions

None for you to decide. Report back anything in Part B that the build did not do as stated, and every value you could not read.

## Expected output

A handoff with `outcome: done`, addressed to `studio` (QA and the Art Director follow, and QA must receive it without your Sender assessment). It states:

1. The change made (Part A) and S0–S3 in their exact final wording, each marked "already so" or "changed".
2. Points (a)–(d) as the build behaves, and what you changed to match them, if anything.
3. Whether the change leaves any other described behavior of build 0.6 different. If none, say "none".

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/g001-combat-escalation.md (3.3, 3.8, 6, 6a, criteria 4, 5, 10); design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.6.md; sim/repo-notes.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/44-game-designer-to-studio.md (also read goals/G-001-combat-monotony/45-art-director-to-studio.md for Part A, and goals/G-001-combat-monotony/37-gameplay-engineer-to-studio.md for your earlier Phase 1 report)
