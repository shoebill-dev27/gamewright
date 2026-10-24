---
kind: handoff
goal: G-001
seq: 14
from: studio
to: art-director
stage: Design
outcome: routed
---
# 14: studio → art-director — Telegraph visuals for Phase 2 and the Phase 1 spawn marker

## Task

Specify what the player sees for (a) the 0.8 s spawn marker in Phase 1, (b) the Lunge Grub 0.6 s wind-up and (c) the Fan Spitter 0.6 s charge in Phase 2, so each reads clearly in the dark cave (pillar 3). Say whether an existing spawn effect can serve as the marker or whether a new one is needed.

## Context

Goal G-001 (combat monotony). D-002 chose encounter escalation (Phase 1) then telegraphed enemy behaviors (Phase 2). The game-designer's spec is `design/g001-combat-escalation.md`. Phase 1 introduces second and third spawn edges and waves with a 0.8 s spawn marker; Phase 2 proposes the two telegraphed attacks. Phase 2 will not be built until you and the technical-director have answered. Phase 1 can be built once the dash fix is verified, so please answer the spawn-marker question first.

## Findings

From the designer's handoff (`11-game-designer-to-studio.md`):
- The marker may need a new visual if no spawn effect exists.
- Lunge Grub: 0.6 s wind-up, then 5-tile lunge in 0.3 s, then 0.8 s recovery.
- Fan Spitter: 0.6 s charge, then 3 projectiles at ±25°.
- Spawn marker: 0.8 s, with a 5-tile minimum spawn distance from the player.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve.

## Constraints

- Art direction: warm light against cold blue-black; threats use saturated orange/red.
- Every threat must be visible before it can hurt the player (pillar 3). Telegraphs must read against the dark and at 30 and 60 FPS.
- Small team: prefer reusing existing assets and effects.
- Do not change the timings or player-facing rules in the spec. If a telegraph needs a different duration, say so for the designer.

## Open questions

- Does a spawn effect already exist that can act as the marker, or is a new one needed?
- Does the lunge's path/direction need to be shown (not just the wind-up)? How should the fan's three directions be shown?
- Can the three markers be told apart from each other and from the existing Grub and Spitter attacks?

## Expected output

A visual specification (or review) with player-observable acceptance criteria, addressed to `studio` (the Studio waits for the technical-director's answer too, then routes both to `game-designer`). `outcome: done`, or `question` if blocked.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/combat.md; project.md#art-direction; project.md#vision; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/11-game-designer-to-studio.md
