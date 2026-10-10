---
kind: handoff
goal: G-002
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — specify enemy-side combat depth (Option A) with player-observable acceptance criteria

## Task

Write a design spec for the Option A changes: telegraphed enemy attacks, a Charger enemy, a Shieldbearer enemy, and room compositions across the 5-room slice. The spec must be precise enough to plan, build and verify, and its acceptance criteria must be observable by a player.

## Context

Goal G-002: the Owner said "戦闘が単調なので改善したい" (combat feels monotonous). A playtest (01–02) found monotony. The diagnosis (03) offered options. The Game Director escalated the choice between enemy-side depth (A) and a heavy-attack button (B). The Owner chose **A** on 2026-10-10 and recorded it as D-002. The intended outcome: across the 5 rooms the player must make different decisions (where to stand, when to dash, which enemy first) instead of repeating one pattern.

## Findings

From the Owner's decision and the escalation (04); the playtest and diagnosis detail is in 02 and 03, which you load:

- Option A content: telegraphed attacks; new enemy **Charger** (rushes the player); new enemy **Shieldbearer** (guards the front); room compositions that ask where to stand, when to dash and which enemy first. The Game Director folded room-composition tuning (former Option C) into A.
- Symptoms Option A is meant to address (3 of the 4 observed): the same tactic clears every room; dash is not used in combat; enemies do not differ in how they must be fought. The 4th symptom, wanting a heavy hit, is deliberately not addressed in this Goal.
- The Owner's condition: keep one-button combat. Hold-to-charge on the attack button may be considered in the future but is **not** part of this Goal.

## Decisions already made

- D-001: combat uses one attack button plus dash. Unchanged.
- D-002 (Owner, 2026-10-10): fix the monotony through enemy behavior and room composition. No heavy-attack button, no new input, and no hold-to-charge in this Goal.

## Constraints

- No new input buttons beyond attack, dash and pause. Do not specify hold, charge or any new player action (D-001, D-002).
- Pillar 3, readable threats: every threat must be visible before it can hurt the player. Telegraphs must be visible and use the saturated orange/red threat language from the art direction. If a telegraph's visual treatment needs art direction beyond that, name it as an open question for `art-director` rather than deciding it.
- Must play correctly at both 30 and 60 FPS. Express timings so they are not frame-rate dependent (for example in seconds, or with an explicit statement of how they scale).
- Small team: prefer changes that reuse existing systems. Say which existing rules, such as damage and invulnerability rules in `design/combat.md`, each new behavior reuses.
- Stay inside the existing 5-room cave slice. No new biomes, meta-progression or run-length changes.
- Acceptance criteria must be qualitative and observable by a player or tester (for example what the player sees and can react to, and how rooms differ in the decisions they require). Numeric parameters belong in the spec's parameter section.

## Open questions

- Which of the 5 rooms get which compositions, so the player faces different decisions rather than a repeated pattern? Decide this in the spec.
- Whether any telegraph or Shieldbearer-guard presentation needs an `art-director` visual spec. If so, list it as a follow-up in your output instead of designing it yourself.
- Any case where D-001 or pillar 3 seems to conflict with the intended behavior. Do not resolve it yourself: hand back to `studio` with outcome `question`, and the Studio will route it to `game-director`.

## Expected output

A design spec with parameters and player-observable acceptance criteria, covering:

1. Enemy attack telegraphs (what the player sees, how long, and how dash interacts with them under the existing invulnerability rules).
2. Charger behavior.
3. Shieldbearer behavior, including how the player gets past the guard using only attack and dash.
4. Room-by-room compositions for the 5 rooms.

Write the spec into the project's design documents. Extend `design/combat.md` or add a new file, and name the file in Findings. Then write the outgoing Handoff to `technical-director` (stage Plan, Skill `technical-plan`). If the spec shows that scope must change, or needs a direction choice, hand back to `studio` with a question instead.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/combat.md, sim/build-0.3.md (current state of the slice), goals/G-002-combat-monotony/02-playtester-to-game-designer.md (playtest observations)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-depth-one-button.md
- Previous handoff: goals/G-002-combat-monotony/03-game-designer-to-game-director.md (the diagnosis and options; the Owner's answer is in goals/G-002-combat-monotony/04-game-director-to-owner.md)
