---
kind: handoff
goal: G-002
seq: 7
from: technical-director
to: gameplay-engineer
stage: Build
outcome: done
---
# 07: technical-director → gameplay-engineer — Implement enemy telegraphs, Charger, Shieldbearer

## Task

Implement `design/enemy-telegraphs.md` following the plan below.

## Context

G-002, direction D-002. Spec from step 5; this plan from step 6.

## Findings

Plan:

1. **Telegraph state** in the shared enemy controller (Idle → Chase → Telegraph → Attack), with a
   per-type duration. Time-based timers on the game clock, not frame counts (G-001 lesson).
2. **Spitter:** route its shot through Telegraph.
3. **Charger:** new type as data plus a lunge routine; lock direction on entering Telegraph;
   Recovery state after the lunge.
4. **Shieldbearer:** new type; facing with a turn-rate limit; frontal-arc check added to the damage
   step (attacks arriving within ±60° of facing — the spec's front 120° arc — are blocked).
5. **Rooms:** update compositions to the table.

- **Risks:** the frontal-arc check is the first facing-aware rule in the damage system — keep it
  local to the Shieldbearer for now. Timer drift between 30/60 FPS — cover V1 at both rates.
- **Tests:** unit tests for telegraph durations at 30/60 FPS (V1), lunge direction lock (V2), arc
  check (V4). QA checks V3, V5–V7 in play.
- **Parallelization:** sequential. Steps 2–4 all depend on step 1 and touch the same controller;
  parallel workspaces would only create merge conflicts. No isolated workspaces.

## Decisions already made

- D-001, D-002.

## Constraints

Reuse the controller; 30 and 60 FPS; do not change the spec — raise questions to `game-designer`.

## Open questions

None known.

## Expected output

The change, and a Handoff to `qa` (or a hand-back if the spec does not define something).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/enemy-telegraphs.md, sim/repo-notes.md
- Decisions: decisions/D-002-enemy-side-combat-depth.md
- Previous handoff: goals/G-002-combat-monotony/06-game-designer-to-technical-director.md
