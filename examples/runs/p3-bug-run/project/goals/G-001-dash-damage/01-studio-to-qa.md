---
kind: handoff
goal: G-001
seq: 1
from: studio
to: qa
stage: Observe
outcome: routed
---
# 01: studio → qa — Reproduce "damage taken while dashing" and write a defect report

## Task

Reproduce the reported defect in the current build and write a precise defect report with acceptance criteria. Determine from the design documents what the intended behavior is.

## Context

Goal G-001. The Owner reported (original wording in Japanese): "Sometimes I take damage even while dashing. It is reproducible, so please fix it." No reproduction steps were provided, so which enemy, which part of the dash, and which frame rate are all unknown. The game is a dry-run project: "running the build" means reading `sim/build-0.3.md`.

## Findings

Nothing yet. No Role has looked at this. The Studio has not read `design/combat.md`, which per the project's design index contains the damage and invulnerability rules. It is not known whether the documents say dash makes the player invulnerable, fully or partly.

## Decisions already made

None.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate.
- No new input buttons beyond attack, dash and pause (D-001). This limits any later fix; it is not for you to resolve.
- Do not propose or implement a fix. Root cause belongs to the gameplay engineer.

## Open questions

- What does the design say should happen to damage during a dash (fully invulnerable, a window of invulnerability, none)? If the design is silent, ambiguous, or contradicts the Owner's expectation, say so explicitly in the report rather than choosing an interpretation.
- Under which exact conditions does damage during a dash occur (enemy type, timing within the dash, frame rate, start/end of the dash)?
- If you cannot reproduce it from the build and documents, say exactly what is missing (conditions only the Owner can supply).

## Expected output

A defect report written in the outgoing Handoff (templates/handoff.md): reproduction steps, observed vs. expected behavior with the design source quoted, frequency/conditions, severity, and player-observable acceptance criteria, including a check at 30 and 60 FPS.

Set `to` by outcome:
- Defect confirmed and intended behavior specified: `gameplay-engineer`.
- Intended behavior undefined or ambiguous: `game-designer`, with the open point stated.
- Not reproducible or Owner information needed: `studio`, `outcome: question`, stating what is missing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md
- Decisions: none
- Previous handoff: none
