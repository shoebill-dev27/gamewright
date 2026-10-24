---
kind: handoff
goal: G-002
seq: 10
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 10: studio → game-designer — Answer the spec questions raised by the Plan and the visual design, before Build

## Task

Rule on the open spec questions below (SQ1–SQ5, N1, Q-A, Q-B). Update `design/combat-enemy-depth.md` where an answer changes or fills in the spec. Do not change anything outside your authority: visuals belong to the Art Director, technical approach to the Technical Director.

## Context

G-002 "戦闘が単調なので改善したい": the Owner chose enemy-side depth with one-button combat kept (D-002; no hold-to-charge attack). You wrote `design/combat-enemy-depth.md`. Two parallel steps have finished:
- The Technical Director's plan (`08-technical-director-to-studio.md`) fits Option A and the constraints. The D-003 cap fits the existing controller. Nothing in the spec is infeasible.
- The Art Director's cue design (`design/combat-enemy-visuals.md`, summary in `09-art-director-to-studio.md`) changes no timings or rules.

Both found places where the spec is silent or ambiguous. The Engineer must not decide those (Build returns to Design on ambiguity), so they are settled now.

## Findings

Questions for you. Each has the default the Technical Director will build to if you do not change it.

- **SQ1 (Flinch), the most important.** Build 0.3 has a 0.2 s Flinch when an enemy is hit, and it interrupts any state including Attack. It is not in `design/combat.md`. If it stays, one swipe cancels every telegraph, "stand still and swipe" survives, and the Charger rule "swipes never interrupt windup, charge or recovery" breaks. Default: Flinch applies only while the enemy is in Chase or Waiting. It is ignored in Telegraph, Active, Recovery, Stunned and Cooldown, for all types. Please rule per enemy type. Spec 3.1, 3.2 and 4.2 are silent.
- **SQ2 (slot lifetime).** The slot is taken before a telegraph starts, held through Telegraph and Active, and released at the start of Recovery. A Spitter releases when the shot is fired, and shots in flight hold no slot. Release also happens on death or room end. Is this what "in a telegraph or attack phase" means (D-003)?
- **SQ3 (obstacles).** Does a Charger charge that ends on an obstacle (not only a wall) also cause the 1.5 s stun? Default: yes, any static solid.
- **SQ4 (waiting behavior).** What does an enemy do while it waits for a free slot? Default: Grub holds about 1.5 tiles away or circles slowly; Charger repositions; Shieldbearer keeps walking toward the player but does not start a bash; Spitter stays put. Waiting enemies show no threat cue.
- **SQ5 (guard reference point).** Is the Shieldbearer's guard check made against the player's position at swipe time, or against the swipe hitbox center? Default: the player's position at swipe time (projectiles: the projectile's position when it reaches the shield).
- **N1 (Grub lock timing, from the Art Director).** The Grub's lunge direction locks at the end of its 0.5 s telegraph and the lunge takes 0.15 s, so there is almost no reaction time after the lock. Intended? If not, give the lock point (for example 0.2 s before the lunge, like the Spitter). The Art Director's visual works either way, but if you change the timing, say so explicitly, because Studio will route the cue update back to the Art Director.
- **Q-A / Q-B.** Fix the numbers the visual design had to assume: Spitter projectile range, Grub lunge width (assumed about 1 tile), Spitter line width, and the Shieldbearer bash cone angle (assumed about 90°; the Technical Director's plan says 1.5-tile range over 0.1 s). These are rules values, not visuals.

For awareness (no decision needed from you unless you object): the Technical Director's plan puts every spec number in one per-enemy data table and rejects any telegraph under 0.4 s at load. The Charger lane is cut at the first solid. Rooms 2, 4 and 5 may need a layout audit, but layout is Build's task (T7).

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002 (Owner): enemy-side depth; no hold-to-charge attack in this Goal.
- D-003: time-based telegraphs with a 0.4 s floor; at most 2 enemies attacking at once.
- D-004: bounded combat sub-steps and a central attack-slot arbiter.

## Constraints

- Keep D-001–D-004: no new inputs, 0.4 s telegraph floor, attack cap of 2. If an answer would need one of them to change, hand back with that stated instead of ruling.
- The Playtester's later handoff must not include implementation details or experience signals; keep spec section 7.2 (experience signals) separate from anything a player would be told.
- Stay within the 5-room slice and the existing controller and data approach.

## Open questions

None beyond the list above. If any answer changes a timing or shape that appears in `design/combat-enemy-visuals.md`, name which cue is affected.

## Expected output

1. `design/combat-enemy-depth.md` updated with the answers (in the spec itself, so Build and QA can verify from it).
2. A handoff addressed to `studio` (not directly to Build) containing: each answer (SQ1–SQ5, N1, Q-A, Q-B) with a one-line reason, which acceptance criteria changed, and whether the Art Director must revise any cue. The Studio will then merge the Technical Director's plan, the visual design and your answers into the Build Handoff.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-enemy-depth.md, design/combat.md, design/combat-enemy-visuals.md, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-004-combat-timing-substeps-and-attack-slots.md
- Previous handoff: goals/G-002-combat-monotony/08-technical-director-to-studio.md (also read goals/G-002-combat-monotony/09-art-director-to-studio.md)
