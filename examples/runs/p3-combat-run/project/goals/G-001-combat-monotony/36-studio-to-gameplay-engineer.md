---
kind: handoff
goal: G-001
seq: 36
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 36: studio → gameplay-engineer — Build Phase 1 (encounter escalation), attempt 2, with the amended spec

## Task

Implement Phase 1 (sections 1–3) of `design/g001-combat-escalation.md` as amended by the Game Designer (D-008). State the whole change exactly: what changes, where, and how to exercise it. Under the project constraints, a change stated this way counts as made. Stop and hand back with a `question` only if something is still ambiguous, contradictory or missing, and name each point.

## Context

G-001 (combat monotony). D-002 chose encounter escalation (Phase 1) first. Your first attempt (handoff 33) stopped on two contradictions and four gaps in spec sections 3.2–3.4. The Game Designer resolved all six in the amended spec (handoff 35, D-008). The dash-damage fix and the hit-stun input change are verified (QA pass, handoff 31) against `sim/build-0.5.md`, which is the current build. Nothing of Phase 1 is built yet.

## Findings

This is a summary of the Designer's answers. The amended spec and D-008 are authoritative.

1. **Wave trigger (3.3):** wave N+1 starts when earlier waves have 1 or fewer unresolved enemies (pending, marker-phase and on-field all count), or 8 s after wave N's first marker started. It starts on the frame of the kill that made the condition true. A pending Grub counts, so a wave may start before that Grub appears.
2. **Spawn point choice (3.2a, 3.3):** each edge has 3 points, 1 tile inside the wall at 25%, 50% and 75% of the edge. Every enemy has an ordered candidate list in the table in 3.2a. Use the first point that is at least 5 tiles from the player and unoccupied. There is no RNG. If none qualifies, use the farthest unoccupied candidate and report it. Occupied means an active marker at the point, or a living enemy within 1.5 tiles.
3. **Spitter corners (3.4, 3.2a):** room 3 NE on the N wall. Room 4: wave 1 NW on the N wall, wave 2 SE on the S wall. Room 5: SW on the S wall and NE on the N wall. Rooms 1–2 use E2 (E wall, mid-height). The Designer's room 5 choice differs from your example.
4. **Spitter versus the 5-tile rule (3.4):** a corner-covering Spitter has two points on its wall, next to the covered corner and then at the far end of the same wall. If the player holds the covered corner, it spawns at the far end. There is no exemption from the 5-tile rule, except the farthest-point fallback.
5. **"Simul." (3.2, 3.7):** it means the same marker start only. The 0.3 s arrival gap is a tuning value in section 7, not a rule.
6. **Marker starts (3.1, 3.3):** wave 1 starts when the player gains control of the room (`T0`). A Spitter's marker starts at its wave start, with the first Grub marker. A second Grub "1.0 s apart" starts 1.0 s later. The Spitter's first shot is no sooner than 1.0 s after it appears. The marker visual is unchanged.

**Existing values (3.8):** Grub speed, player speed, projectile speed and range, heart count and room size are not in any design document. The Designer does not have them either and decided that Phase 1 proceeds without them. The data uses only tiles, seconds and room-relative points. Report the values you can read from the game, and write "not available" for the rest. Do not invent them.

Changed acceptance criteria: 1 (hits taken, no heart note), 4 (farthest-point fallback reported), 5 (same points as well as times, no RNG), and new criterion 10 (first markers, wave trigger, point choice, occupancy, Spitter lists).

## Decisions already made

- D-001: one-button combat, no new input.
- D-002: encounter escalation (Phase 1) before enemy behaviors (Phase 2).
- D-004: Phase 1 is one serial Build with no separate Plan. Gameplay numbers are data. Timers are timestamps on the accumulated game clock.
- D-008: Phase 1 spawn and wave rules, as summarized above.

## Constraints

- Phase 1 only. Do not build any Phase 2 content (Lunge Grub, Fan Spitter, Flinch changes).
- Do not change the verified dash, hit-stun or invulnerability behavior (D-003 and the fix verified in handoff 31).
- Correct at 30 and 60 FPS. Spawn choice has no RNG.
- No new input buttons (D-001). Prefer reusing existing systems.
- Marker rule from the telegraph visuals document: reuse an existing spawn effect if it passes criteria A1–A5, otherwise build the minimal ring. The ring (1.5 tiles across) must fit 1 tile inside a wall.

## Open questions

Answer these in your Build report:
- Was an existing spawn effect reused? If not, what minimal ring did you build?
- Which of the five existing values (3.8) could you read, and what are they?
- Does the room size support the point lists, or would many spawns use the farthest-point fallback? (Spec section 8.) Report any fallback you see.

If a point is still ambiguous, name it, say which spec section it is in, and give the options and the default you would take. Do not decide it yourself.

## Expected output

A Build report with the complete change statement for Phase 1, the values used, and the answers to the open questions. Address it to `studio`, so the Studio can compose the QA handoff from permitted information. Put your own reasoning in `## Sender assessment`, which is removed before QA receives it. Verification will be against criteria 1–5 and 10.

Loop note: if you hand back `question` again for the same missing input with nothing new supplied, the Studio escalates to the Owner for it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/g001-combat-escalation.md (sections 1–3, 7, 8 and the acceptance criteria; skip Phase 2 content), design/g001-telegraph-visuals.md (spawn marker and criteria A1–A5), design/combat.md, sim/build-0.5.md, sim/repo-notes.md, goals/G-001-combat-monotony/16-technical-director-to-studio.md (task list and plan), goals/G-001-combat-monotony/33-gameplay-engineer-to-studio.md (your earlier questions)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/35-game-designer-to-studio.md
