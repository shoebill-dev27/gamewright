---
kind: handoff
goal: G-002
seq: 9
from: game-designer
to: gameplay-engineer
stage: Build
outcome: done
---
# 09: game-designer → gameplay-engineer — Answers to Q1 and Q2; finish the Build

## Task

Finish the Charger and Shieldbearer attack sequences using the answers below.

## Context

G-002. The engineer's questions are in 08.

## Findings

- **Q1 → (b), recorded as D-003.** Telegraphs and attacks are committed: hits deal damage but do
  not interrupt. Flinch only outside telegraph/attack. Reason: interruption would restore the
  corner-and-swipe strategy.
- **Q2 →** the lunge stops at the wall and recovery starts there. Noted in the spec, no Decision:
  it does not constrain other work.
- `design/enemy-telegraphs.md` now has an "Edge cases" section and criteria V8–V9. The flinch is
  documented there.

## Decisions already made

- D-001, D-002, D-003.

## Constraints

As in 07.

## Open questions

None.

## Expected output

The completed change and a Handoff to `qa` covering V1–V9.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/enemy-telegraphs.md, sim/repo-notes.md
- Decisions: decisions/D-003-committed-telegraphed-attacks.md
- Previous handoff: goals/G-002-combat-monotony/08-gameplay-engineer-to-game-designer.md
