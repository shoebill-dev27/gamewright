---
kind: handoff
goal: G-002
seq: 11
from: qa
to: studio
stage: Route
outcome: pass
---
# 11: qa → studio — Verification passed (build 0.4)

## Task

Route to the next step. This report goes to the Studio because the next recipient is a Playtester.

## Context

G-002, verification of build 0.4.

## Findings

| Criterion | 60 FPS | 30 FPS |
|---|---|---|
| V1 telegraph durations | pass | pass |
| V2 lunge direction lock | pass | pass |
| V3 lunge distance, damage window, recovery | pass | pass |
| V4 Shieldbearer frontal arc | pass | pass |
| V5 turn rate 90°/s | pass | pass |
| V6 dash protects against lunge and bash | pass | pass |
| V7 room compositions | pass | — |
| V8 hits during telegraph do not interrupt | pass | pass |
| V9 lunge stops at wall, then recovers | pass | pass |

Regressions checked: G-001 dash/hit invulnerability cases, Grub and Spitter damage, room clear
condition. No change. Verdict: **pass**.

## Decisions already made

- D-003.

## Constraints

None.

## Open questions

None.

## Expected output

The Studio composes the Playtester's handoff from player-observable information only.

## Load

- Studio: studio/orchestration.md, studio/workflows/development-loop.md
- Goal: goals/G-002-combat-monotony/goal.md
- Previous handoff: goals/G-002-combat-monotony/10-gameplay-engineer-to-qa.md
