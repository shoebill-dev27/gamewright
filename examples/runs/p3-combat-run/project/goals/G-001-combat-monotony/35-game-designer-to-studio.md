---
kind: handoff
goal: G-001
seq: 35
from: game-designer
to: studio
stage: Build
outcome: done
---
# 35: game-designer → studio — Phase 1 spec gaps resolved; route Phase 1 back to gameplay-engineer

## Task

Route Phase 1 of `design/g001-combat-escalation.md` (sections 1–3) back to `gameplay-engineer`. All six questions from handoff 33 are answered in the amended spec, and the existing-value question is answered.

## Context

G-001 (combat monotony). D-002 chose encounter escalation first. The engineer stopped Phase 1 (handoff 33) because of two contradictions and several gaps. Handoff 34 sent them to me. The amended spec is in `design/g001-combat-escalation.md`, and D-008 records the decision. `sim/build-0.5.md` is still the current build, and nothing is built yet.

## Findings

Answers (spec section in brackets):

1. **Wave trigger (3.3):** I accept the engineer's option (a). Wave N+1 starts when the earlier waves have 1 or fewer unresolved enemies, where pending, marker-phase and on-field enemies all count, or 8 s after wave N's first marker started. It starts on the frame of the kill that made the condition true. Because a not-yet-marked Grub counts, a wave can start before that Grub appears. That is intended.
2. **Spawn point choice (3.2a, 3.3):** I accept option (a) and give the data. Every edge has 3 points, 1 tile inside the wall at 25%, 50% and 75% of the edge. Every enemy has an ordered list in the table in 3.2a. The first point that is at least 5 tiles from the player and not occupied is used, with no RNG. If none qualifies, the farthest unoccupied candidate is used. I added an occupancy rule (no active marker at the point, no living enemy within 1.5 tiles) because two enemies of one wave can share an edge.
3. **Spitter corners (3.4, 3.2a):** room 3 NE on the N wall; room 4 wave 1 NW on the N wall, wave 2 SE on the S wall; room 5 SW on the S wall and NE on the N wall. Rooms 1–2 use E2 (E wall, mid-height). I chose them so every corner is covered at least once over rooms 3–5, and two different corners are covered in each of rooms 4 and 5. My choice differs from the engineer's example for room 5.
4. **Spitter versus the 5-tile rule (3.4):** I choose option (b), with a specific alternative. A corner-covering Spitter has two points on its wall: next to the covered corner, then at the far end of the same wall. If the player holds the covered corner, the Spitter spawns at the far end and fires down the wall, so it never appears beside the player. There is no exemption, so criterion 4 stands. Its only exception is the existing farthest-point fallback, which the Build reports.
5. **"Simul." (3.2, 3.7):** I accept the engineer's default (a). It means the same marker start only. The 0.3 s arrival gap is no longer a rule. It is a tuning value in section 7, and the playtest should report the arrival gaps.
6. **Marker starts (3.1, 3.3):** I accept the default. Wave 1 starts when the player gains control of the room (`T0`). A Spitter's marker starts at its wave start, with the first Grub marker. A second Grub "1.0 s apart" starts 1.0 s later. Held items stay as they are: the Spitter's first shot is no sooner than 1.0 s after it appears, and the marker visual is unchanged.

Existing values (3.8): Grub speed, player speed, projectile speed and range, hearts and room size are not in any design document, and I do not have them. I do not invent them. **Phase 1 proceeds without them.** The data uses only tiles, seconds and room-relative points. The Build reports what it can read from the game and writes "not available" otherwise. The first step that can observe them (QA, in its first Phase 1 verification handoff, then the playtest) records them. Criterion 1 now counts hits taken, which does not need the heart count.

Acceptance criteria changed: criterion 1 (hits taken, no heart note), criterion 4 (farthest-point fallback reported), criterion 5 (same points as well as times, no RNG), and a new Phase 1 criterion 10 covering first markers, the wave trigger, point choice, occupancy and the Spitter lists. Section 7 now lists the 1.5-tile values and the arrival gap as tuning values. Section 8 has a new question about room size.

Consequences:
- **Visuals / `art-director`:** none. The marker look is unchanged. The ring (1.5 tiles across) fits 1 tile inside a wall.
- **`game-director`:** none. No scope, pillar or input change.
- **Build:** one pass, data plus a small scheduler (D-004 is not triggered). It needs the wave counter, the point-choice routine with the occupancy rule, and the 1.0 s Spitter first-shot delay. All timers are timestamps on the accumulated game clock.
- **Build should report:** whether an existing spawn effect was reused, the values it could read, whether the room size supports the lists, and any fallback it saw.

## Decisions already made

- D-001: one-button combat, no new input.
- D-002: encounter escalation (Phase 1) before enemy behaviors (Phase 2).
- D-004: Phase 1 is one serial Build with no separate Plan. Gameplay numbers are data.
- D-005: Phase 2 enemy rules (not in Phase 1 scope).
- D-008 (new): Phase 1 spawn and wave rules, as above.

## Constraints

- Phase 1 only. No Phase 2 content.
- Do not change the verified dash, hit-stun or invulnerability behavior.
- Correct at 30 and 60 FPS. Spawn choice has no RNG.

## Open questions

- For Build and QA: is the room big enough for the point lists, or do many spawns use the fallback? (Spec section 8.)
- For the playtest: how far apart do "simul." Grubs arrive, and what are the five existing values? (Spec 3.8, section 7.)

## Expected output

The Studio routes Phase 1 to `gameplay-engineer` with the amended spec, then QA verifies it against criteria 1–5 and 10.

## Sender assessment

- Confidence is high on questions 1, 2, 4 and 6, which follow from the engineer's options. Confidence is medium on the corner choices and on the 1.5-tile offsets and occupancy distance. They are tuning values and not provable from a described walkthrough, which is why they are listed in section 7.
- The Spitter far-end alternative is my addition to the engineer's option (b). It keeps the corner threatened when the player is already in it.
- I cannot state the existing values. I chose to say so rather than guess, and made Phase 1 independent of them.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md, design/g001-telegraph-visuals.md, design/combat.md, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/34-studio-to-game-designer.md
