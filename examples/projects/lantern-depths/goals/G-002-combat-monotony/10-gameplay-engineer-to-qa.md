---
kind: handoff
goal: G-002
seq: 10
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 10: gameplay-engineer → qa — Verify enemy telegraphs, Charger, Shieldbearer (build 0.4)

## Task

Verify build 0.4 against V1–V9 in `design/enemy-telegraphs.md`.

## Context

G-002. Spec D-002/D-003, plan in 07, answers in 09.

## Findings

- **Changed:** shared enemy controller (Telegraph and Recovery states; flinch suppressed during
  Telegraph/Attack); Spitter shot routed through Telegraph; new Charger and Shieldbearer types;
  Shieldbearer frontal-arc check in the damage step; room compositions.
- **How to exercise:** rooms 3–5 contain the new enemies. Room 3 has a wall near the spawn to check
  V9.
- **Own tests:** unit tests for V1 (30/60 FPS), V2, V4, V8 pass.
- **Risk:** Shieldbearer turn rate feels slow in play; it matches the spec (V5) — not changed.

## Decisions already made

- D-001, D-002, D-003.

## Constraints

30 and 60 FPS.

## Open questions

None.

## Expected output

Verification report. Next is a blind playtest, so address the report to `studio`, not to the
Playtester.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/enemy-telegraphs.md
- Decisions: decisions/D-003-committed-telegraphed-attacks.md
- Previous handoff: goals/G-002-combat-monotony/09-game-designer-to-gameplay-engineer.md
