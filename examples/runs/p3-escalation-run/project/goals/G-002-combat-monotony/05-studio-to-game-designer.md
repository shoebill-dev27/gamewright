---
kind: handoff
goal: G-002
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — Specify enemy-side combat depth (Option A)

## Task

Write a design spec for Option A of G-002, with player-observable acceptance criteria. The spec must be precise enough for the Technical Director to plan and for QA and a Playtester to verify.

## Context

Goal G-002: the Owner said "戦闘が単調なので改善したい". The playtest and diagnosis (steps 1–3) found that combat is monotonous. The main cause is that enemies do not demand positioning or timing. Four symptoms were recorded: one tactic clears every room, dash is not used in combat, enemies do not differ in how they must be fought, and a request for a heavier hit. The Game Director escalated the direction choice to the Owner. On 2026-10-11 the Owner chose Option A, enemy-side depth with one-button combat kept (D-002).

## Findings

Direction approved in D-002 and the escalation (`04-game-director-to-owner.md`). The spec must cover:

- **Telegraphed enemy attacks.** Every threat is visible before it can hurt the player (pillar 3).
- **Charger.** A new enemy that charges at the player.
- **Shieldbearer.** A new enemy that guards the front.
- **Room composition adjustments** across the 5-room slice (the former "Option C", folded into A by the Game Director). Rooms should ask different questions: where to stand, when to dash, which enemy first.

The spec should target the symptoms Option A addresses: the one tactic that clears every room, dash unused in combat, and no difference in how each enemy is fought.

The diagnosis and options are in `03-game-designer-to-game-director.md` and `02-playtester-to-game-designer.md`. They are listed in Load as background, so use them to keep the spec tied to the observed problems.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval.
- D-002 (Owner, 2026-10-11): The monotony is solved on the enemy side with one-button combat kept. **A hold-to-charge attack is explicitly not part of this work.** The Owner may consider it in future, but it must not appear in this spec, not even as an optional extra.

## Constraints

- No new input buttons. Do not add hold or charge behavior to attack (D-001, D-002).
- Must play correctly at both 30 and 60 FPS. Timings, such as telegraph durations, must be specified so they hold at both frame rates.
- Small team: prefer reusing existing systems (see `design/combat.md` and the existing enemies).
- Threats use saturated orange/red so they read against the dark (art direction). Tell the Art Director if a visual question arises that you cannot settle; do not decide visual direction yourself.
- Scope stays within the 5-room slice. No new biomes, meta-progression, or run-length changes.
- Acceptance criteria must be player-observable and must not depend on implementation detail. A numeric tuning value is fine in the spec where the Design stage needs it. The final verdict on whether the monotony is addressed belongs to Review.

## Open questions

- None to the Owner. If the spec needs a choice of direction, priority or scope beyond D-002, hand back to `game-director` per the return rules. Do not escalate it yourself.

## Expected output

- A design spec (a design document under `design/`; update `design/combat.md` or add a new file and link it from the Design index in `project.md` if your Role contract allows) covering telegraphs, Charger, Shieldbearer and per-room composition, with player-observable acceptance criteria.
- An outgoing Handoff (templates/handoff.md) to `technical-director` (stage Plan) summarizing the spec. Record a Decision if you make a significant tuning or design choice that constrains later work.

## Sender assessment

Studio routing note: the route is unchanged from the original plan, because the Owner's choice matched Option A's "If chosen" path. Later, the Playtester step (9) needs a fresh Handoff composed by the Studio. Address the Plan Handoff accordingly, and tell the Verify and Build steps to address their results to `studio` when the route reaches them.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/combat.md, sim/build-0.3.md (current state of the slice); background: goals/G-002-combat-monotony/02-playtester-to-game-designer.md, goals/G-002-combat-monotony/03-game-designer-to-game-director.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md
- Previous handoff: goals/G-002-combat-monotony/04-game-director-to-owner.md
