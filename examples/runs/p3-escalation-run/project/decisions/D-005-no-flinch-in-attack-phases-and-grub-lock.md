---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-11
supersedes: none
---
# D-005: Hits never interrupt an enemy's attack cycle, and the Grub's direction locks 0.3 s before its lunge

## Decision

- Enemy Flinch (0.2 s, build 0.3) applies only while an enemy is Idle, in Chase or Waiting. It is ignored in Telegraph, Active, Recovery, Stunned and Cooldown, for all enemy types. Damage still applies. A blocked swipe (0 damage) causes no Flinch.
- Attack slots (D-003 cap of 2) are taken when a Telegraph starts and released when Recovery starts, on death or at room end. A Spitter releases when it fires.
- The Grub's lunge direction locks 0.2 s into its 0.5 s telegraph, so it is fixed for the last 0.3 s. Total timings are unchanged.
- Hit areas: Grub lunge 1.0 × 2.0 tiles; Spitter projectile 0.25 tile wide with a 12 tile range; Shieldbearer bash 90° cone, 1.5 tiles.

Scope: build 0.4 enemies in `design/combat-enemy-depth.md`. D-001–D-004 are unchanged: no new inputs, 0.4 s telegraph floor, cap of 2.

## Rationale

- If one swipe can cancel a telegraph, "stand still and swipe" clears every room and the Charger rule (swipes never interrupt) cannot hold. This is the main risk to the Goal.
- Ignoring Flinch only in the attack cycle keeps hits satisfying on walking enemies, and makes the recovery window a real opening to hit, not a way to stop attacks.
- A Grub that locks at the end of the telegraph leaves almost no reaction time after the lock. A 0.3 s locked window matches the Charger and is above the 0.25 s dash duration, so sidestep and dash are real answers.

## Alternatives considered

- Keep the Flinch in all states: telegraphs become cancellable; rejected.
- Flinch ignored only for the Charger: leaves the tactic working on Grubs, Spitters and Shieldbearers; rejected.
- Lock the Grub 0.2 s before the lunge (like the Spitter): a shorter window, below a comfortable reaction time for a 1-tile sidestep; rejected for 0.3 s.
- Keep the lock at the end of the telegraph: the Grub's attack could not be answered by reaction; rejected.

## Revisit when

- Playtest shows enemies feel unresponsive to hits (tune the Flinch states, not the telegraphs).
- Playtest shows Grubs are too easy or too hard to dodge (retune the locked window; the 0.4 s telegraph floor stays).
