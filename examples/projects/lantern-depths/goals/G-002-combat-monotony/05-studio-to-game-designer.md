---
kind: handoff
goal: G-002
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — Specify Option A (enemy-side combat depth)

## Task

Write the detailed design for Option A: telegraph rules, the Charger and Shieldbearer, and room
compositions, with acceptance criteria for QA and separate experience criteria for the Review.

## Context

G-002 resumed after the Owner's decision (escalation 04 → D-002). Diagnosis and options are in 03.

## Findings

Symptoms to address (from 03): S1 one dominant strategy; S2 dash has no combat purpose; S3 enemies
are fought the same way.

## Decisions already made

- D-001: one attack button plus dash.
- D-002 (Owner): Option A; hold-to-charge is out of scope for this Goal.

## Constraints

- No new inputs. Threats must be readable before they hurt (pillar 3).
- Small team: reuse the existing enemy controller and sprites where possible.
- 30 and 60 FPS.

## Open questions

None.

## Expected output

A design document under `design/`, and a Handoff to `technical-director` for planning.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md
- Previous handoff: goals/G-002-combat-monotony/03-game-designer-to-game-director.md
