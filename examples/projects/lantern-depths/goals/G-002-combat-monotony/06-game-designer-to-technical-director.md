---
kind: handoff
goal: G-002
seq: 6
from: game-designer
to: technical-director
stage: Plan
outcome: done
---
# 06: game-designer → technical-director — Plan the enemy telegraph changes

## Task

Turn the spec in `design/enemy-telegraphs.md` into an implementation plan.

## Context

G-002, direction D-002 (enemy-side depth). Spec written in step 5.

## Findings

Spec summary (full text in `design/enemy-telegraphs.md`):

- Telegraph state before every ranged or charging attack (Spitter 0.5 s, Charger 0.5 s,
  Shieldbearer 0.6 s).
- Charger: locked-direction lunge with a recovery window.
- Shieldbearer: frontal 120° shield, slow turn, telegraphed bash.
- Five rooms, each asking a different question.
- Verification criteria V1–V7. Experience criteria E1–E3 are for the Review only.

## Decisions already made

- D-001, D-002.

## Constraints

Reuse the enemy controller; 30 and 60 FPS; no new inputs.

## Open questions

None known to the designer.

## Expected output

A plan, as a Handoff to `gameplay-engineer`.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/enemy-telegraphs.md, sim/repo-notes.md
- Decisions: decisions/D-002-enemy-side-combat-depth.md
- Previous handoff: goals/G-002-combat-monotony/05-studio-to-game-designer.md
