---
kind: handoff
goal: G-002
seq: 8
from: gameplay-engineer
to: game-designer
stage: Design
outcome: question
---
# 08: gameplay-engineer → game-designer — Spec question: hits during a telegraph

## Task

Answer the spec questions below so the Build can finish. The engineer has not chosen an answer.

## Context

G-002 Build (step 7), implementing `design/enemy-telegraphs.md` per the plan in 07.

## Findings

Done so far: Telegraph state in the shared controller (time-based); Spitter routed through it;
room compositions updated; Shieldbearer arc check implemented.

**Q1 (blocking Charger and Shieldbearer) — what happens when an enemy is hit during its telegraph?**
The current build has an undocumented behavior: any enemy hit by the player flinches for 0.2 s,
which interrupts whatever it is doing. The spec does not say how this interacts with telegraphs.
The cases I can see:

- (a) Flinch interrupts the telegraph; the attack is cancelled.
- (b) The telegraph continues; the hit deals damage but the attack still happens.
- (c) Different per enemy.

Technical cost is the same for all three (a per-state flag). Observed effect, not a recommendation:
with (a), a player who keeps swiping can prevent Charger and Shieldbearer attacks entirely.

**Q2 (minor) — what happens when a Charger's lunge reaches a wall before 6 tiles?** The spec gives
distance and time only.

Not blocked: everything except the Charger/Shieldbearer attack sequences. Unit tests for V1 and V4
pass at 30 and 60 FPS.

## Decisions already made

- D-001, D-002.

## Constraints

The engineer does not decide player-facing behavior the spec leaves open (role contract).

## Open questions

- Q1 and Q2 above.

## Expected output

Answers, applied to `design/enemy-telegraphs.md`, then back to `gameplay-engineer`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md, design/enemy-telegraphs.md
- Decisions: decisions/D-002-enemy-side-combat-depth.md
- Previous handoff: goals/G-002-combat-monotony/07-technical-director-to-gameplay-engineer.md
