---
kind: handoff
goal: G-001
seq: 13
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 13: studio → technical-director — Assess feasibility and cost of the Phase 2 enemy behaviors

## Task

Review section 4 (Phase 2 proposals) of `design/g001-combat-escalation.md` and say whether the Lunge Grub and the Fan Spitter can be built cheaply by a small team, reusing existing systems. Name which to drop or replace if cost is high.

## Context

Goal G-001 (combat monotony). D-002 chose encounter escalation first (Phase 1, data and tuning), then enemy behaviors that demand movement and the dash (Phase 2), with rule rewards in reserve. The game-designer's spec is done (`11-game-designer-to-studio.md`). Phase 2 does not go to Build until you and the art-director have answered.

## Findings

From the designer's handoff:
- Lunge Grub: 0.6 s wind-up, then 5 tiles in 0.3 s, then 0.8 s recovery.
- Fan Spitter: 0.6 s charge, then 3 projectiles at ±25°.
- Both replace existing enemies in the room table, so room totals do not change.
- Designer's flagged concern for you: lunge speed is about 0.55 tile per frame at 30 FPS, so the hit check needs to sweep along the path, not test only the end position. The designer also listed a repositioning Spitter as an alternative to the fan.
- Designer notes that all numbers are their choice and not backed by measurement.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B (encounter escalation) then A (telegraphed behaviors), C in reserve; 5 rooms and 15–20 min runs stay.
- D-003: input during hit-stun is ignored, not buffered.

## Constraints

- Frame-rate independent at 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input; no pillar change. If your assessment shows the behaviors cannot be built inside these limits, say so; scope changes go to `game-director`.
- Do not change the spec's player-facing behavior; if it must change, say what and why, and the designer will decide.

## Open questions

- Can both behaviors be built cheaply, with a swept hit check for the lunge? Which should be dropped if cost is high?
- Is a Plan needed for Phase 1 (room data, waves, spawn marker, Spitter first-shot delay)? Say whether it is risky or cross-system.
- Which enemy and player values (Grub speed, player speed, projectile speed, room size) are already in the code, so Build can report them?

## Expected output

A technical assessment (or plan) with risks, cost and sequencing, addressed to `studio` (the Studio waits for the art-director's answer too, then routes both to `game-designer`). `outcome: done`, or `question` if something blocks you.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: design/g001-combat-escalation.md; design/combat.md; sim/repo-notes.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/11-game-designer-to-studio.md
