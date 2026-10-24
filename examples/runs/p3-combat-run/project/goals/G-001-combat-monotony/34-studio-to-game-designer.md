---
kind: handoff
goal: G-001
seq: 34
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 34: studio → game-designer — resolve the Phase 1 spec gaps and contradictions the Build found

## Task

Answer the six questions below by amending `design/g001-combat-escalation.md` sections 3.2–3.4 (and the room table or section 7 where needed), and settle the existing-value question. The gameplay-engineer stopped Phase 1 Build because the spec is contradictory or misses cases. The engineer may not decide these, and neither may the Studio.

## Context

G-001 (combat monotony). D-002 chose encounter escalation (Phase 1) first. Handoff 32 opened the Phase 1 Build. The engineer's handoff 33 (`outcome: question`) applied no change, so `sim/build-0.5.md` remains the current build. The engineer listed every player-observable behavior of Phase 1 and found two contradictions and several gaps. The full text, cases and options are in handoff 33 (Findings); this handoff lists them so you can work from here.

## Findings

Questions from handoff 33 (read its Findings for the engineer's options and consequences):

1. **Wave trigger (contradiction in 3.3).** "1 or fewer enemies alive" is already true before wave 1 has spawned if "alive" means on the field. Do enemies in a marker phase count? Engineer's options: (a) count pending and on-field enemies of earlier waves; (b) count only on-field enemies, and don't evaluate until every enemy of wave N has spawned. Engineer's proposed default: (a). Blocking.
2. **Spawn point choice (gap in 3.2/3.3).** How many points per edge, where, and how is one chosen when several are at least 5 tiles from the player? Options: (a) an ordered candidate list per enemy in the room data, first qualifying point, no RNG; (b) seeded RNG among qualifying points. Proposed default: (a). Blocking. (Criterion 5, the scripted run at 30 and 60 FPS, needs determinism.)
3. **Spitter corners (gap in 3.4 and the room table).** Which corner and wall for room 3, room 4 wave 1 and wave 2, and room 5 (two Spitters)? Player-facing: it decides which stance the Spitter punishes. Blocking.
4. **Spitter versus the 5-tile minimum (contradiction between 3.3 and 3.4).** A Spitter pinned within 2 tiles of a corner can be asked to spawn near the player. Options: (a) Spitters are exempt from the 5-tile rule (conflicts with criterion 4); (b) each Spitter has an alternative corner-covering point list, falling back to the farthest. Proposed default: (b). Blocking.
5. **Meaning of "simul."** when the 5-tile rule relocates a point. Options: (a) same marker start only, the 0.3 s arrival figure is a playtest tuning value; (b) the scheduler checks the arrival gap and picks the next candidate. Proposed default: (a). Not blocking if you accept the default.
6. **Marker start times.** When do the first markers start after the player enters a room, and when does the Spitter's marker start inside wave 1? Proposed default: the first markers start when the player gains control; the Spitter's marker starts with the wave's first Grub marker. Not blocking if you accept the default.

Existing values: the engineer reports that Grub speed, player speed, projectile speed, heart count and room size are not in `sim/repo-notes.md`, and no repository exists in this dry run, so the engineer will not invent them. The Studio cannot supply them either. They are needed for criterion 1 (the 2-hit threshold), the "equal travel distance" and "on screen" checks, and the Grub-speed tuning knob in 3.5. Please state them from `design/combat.md` or your own design parameters if they are design-level values, or state explicitly that Phase 1 proceeds without them and which later step records them (for example, the playtest reports them). Either answer is yours to give, since gameplay numbers are data (D-004).

Held, not blocked: the Spitter's first shot no sooner than 1.0 s after it appears and the marker visual (per the engineer).

## Decisions already made

- D-001: one-button combat, no new input.
- D-002: encounter escalation (Phase 1) before enemy behaviors (Phase 2).
- D-004: Phase 1 is one serial Build with no separate Plan, only a small scheduler. Gameplay numbers are data.
- D-005: Phase 2 enemy rules (not in Phase 1 scope).

## Constraints

- Stay inside the vision, D-001 and the pillars (threats readable before they can hurt, 30/60 FPS correctness, no new buttons).
- Phase 1 only. Do not add Phase 2 content.
- Prefer deterministic, data-only answers so the Build is one pass and criterion 5 is checkable.
- If an answer would change scope, a pillar, or what the spawn markers must look like, say so, so the Studio can route to `game-director` or `art-director`. Do not decide those yourself.

## Open questions

None beyond the six above. Say, for each, whether you accept the engineer's proposed default or choose differently.

## Expected output

An amended `design/g001-combat-escalation.md` (full file) with every question answered and the acceptance criteria updated if an answer changes them, plus a handoff in `goals/G-001-combat-monotony/` addressed to `studio` stating: each answer, the existing-value answer, and any consequence for visuals, `game-director` or the Build. The Studio then routes Phase 1 back to `gameplay-engineer`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md, design/g001-telegraph-visuals.md, design/combat.md, project.md#constraints, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-005-phase-2-flinch-contact-and-dash-window.md
- Previous handoff: goals/G-001-combat-monotony/33-gameplay-engineer-to-studio.md
