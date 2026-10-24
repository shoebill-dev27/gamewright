---
kind: handoff
goal: G-002
seq: 6
from: game-designer
to: technical-director
stage: Plan
outcome: done
---
# 06: game-designer → technical-director — Plan the enemy-side combat depth (Option A)

## Task

Plan the technical approach and work breakdown for the spec in `design/combat-enemy-depth.md`: enemy telegraphs, Charger, Shieldbearer and the 5-room composition. Answer feasibility and cost questions Q2 below.

## Context

G-002 「戦闘が単調なので改善したい」. The playtest and diagnosis found monotonous combat (one tactic clears every room, dash unused in combat, enemies fought identically). The Owner chose Option A, enemy-side depth with one-button combat kept (D-002). The spec is now written.

## Findings

Spec summary (full numbers and acceptance criteria are in `design/combat-enemy-depth.md`):

- **Time basis:** all timings in real seconds; minimum telegraph 0.4 s; outcomes identical at 30 and 60 FPS (D-003).
- **Telegraph for every damaging attack,** in the orange/red threat palette, showing which enemy and where. At most 2 enemies in telegraph/attack at once (D-003).
- **Grub:** stops 1.5 tiles away, 0.5 s telegraph, lunge 2 tiles in 0.15 s, 0.6 s recovery. Walking contact no longer damages.
- **Spitter:** 0.6 s aim telegraph, aim locks 0.2 s before firing, interval 2 s.
- **Charger (HP 3):** 0.8 s windup (tracks 0.5 s, locks 0.3 s), shows the charge lane; charges 12 tiles/s up to 8 tiles; 1.0 s cooldown; 0.8 s recovery in the open, 1.5 s stun after a wall hit.
- **Shieldbearer (HP 3):** 120° guard arc, 90°/s turn rate, front attacks deal 0 with a block cue, blocks Spitter shots; bash with 0.6 s telegraph and 0.8 s guard-down recovery.
- **Rooms:** 1: 3 Grubs. 2: 2 Grubs + Charger. 3: 2 Spitters + Shieldbearer. 4: 2 Chargers + 2 Grubs. 5: Shieldbearer + Charger + Spitter + 2 Grubs.
- **Acceptance:** V1–V11 (QA checks at 30 and 60 FPS) and E1–E5 (experience signals, kept for Review and not for the Playtester).

## Decisions already made

- D-001: one attack button plus dash; no new input buttons.
- D-002 (Owner): enemy-side depth; the spec contains only the items listed above.
- D-003 (Game Designer): time-based telegraphs with a 0.4 s floor and a limit of 2 simultaneous attackers.

## Constraints

- No new inputs. Small team: reuse the shared enemy controller where possible.
- Must play correctly at 30 and 60 FPS.
- Scope: the 5-room slice only. No new biomes, meta-progression or run-length changes.
- Dry-run project: a Build step states the change exactly in its Handoff (what, where, how to exercise it); it then counts as made.

## Open questions

- Q1 (visual cues): handled by the Studio in parallel. The `art-director` designs the telegraph cues, Charger lane indicator, and block and stun cues in step 6b (`07-studio-to-art-director.md`). Do not decide their visuals; plan the telegraph/cue system so that cue visuals can be swapped without logic changes, and note any technical limits on cues (e.g., lane indicator drawing, draw cost) in your plan for the Studio to pass on.
- Q2 (Technical Director): do rooms 2–5 need layout changes (walls, obstacles) for charge lanes and wall-stun? Does the 2-attacker cap fit the existing enemy controller? Rough cost and risks.
- Q3: first tuning values (turn rate, windup, stun) are to be retuned after playtest; the plan should keep them easy to change (data-driven where the existing systems allow).

## Expected output

A technical plan and work breakdown (Technical Director's own contract, `technical-plan`), with answers to Q2 and any spec questions, including tests (with 30 and 60 FPS checks) and sequencing for the Build step. Address the result to `studio`: the Studio merges it with the Art Director's cue design (step 6b) before writing the Build Handoff.

## Sender assessment

Routing instructions from the Studio for later steps:

- The Verify and Build steps must address their result Handoffs to `studio` when the route reaches them.
- The Playtester step (9) needs a fresh Handoff composed by the Studio from the build only. Nothing in sections 7.2 (experience signals) or design-side files should be put into the Playtester's Handoff.

Confidence: the structure and values are first tuning guesses; the biggest risks are readability of mixed rooms (room 5) and whether the Shieldbearer's turn rate makes flanking too easy or too hard.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/combat-enemy-depth.md, design/combat.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md
- Previous handoff: goals/G-002-combat-monotony/05-studio-to-game-designer.md
