---
kind: decision
id: D-001
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-25
supersedes: none
---
# D-001: Lit ships slide along the beam row; the beam has three aims

## Decision

- The beam has three aims: LEFT, UP (lights nothing) and RIGHT. The commands `L`, `R` and `H` turn it one step or hold it, clamped at the ends.
- Only the lighthouse's row (row 3) can be lit.
- A ship on a lit tile does not advance south. It slides one tile along the row away from the lighthouse each turn it stays lit.
- A ship not on a lit tile moves one tile south.
- A wreck loses the night at once. A night has a 10-turn limit (dawn).

## Rationale

- The slide gives the player real control over how far a ship is pushed (one tile per held turn) and keeps everything predictable.
- UP as a neutral aim makes switching sides cost two turns, which gives planning depth with only three commands (Pillar 1).
- Every ship's path can be derived from the board and the rules (Pillar 2).
- Short nights of about 7 turns keep to Pillar 3.

## Alternatives considered

- **Beam pushes a ship back along its heading.** Ships would leave the map or stall, which is not "turned aside".
- **Two aims only (LEFT, RIGHT).** `L` and `R` would be redundant with `H` when already at an end, and switching sides would cost nothing, which loses the planning depth.
- **Diagonal rays from a lighthouse at the bottom.** Harder to read ahead from a character grid.
- **Ship-ship collisions as a loss.** This is a new mechanic beyond the vision, so ships pass through each other.

## Revisit when

- Playtests show the nights are too easy or too hard to read.
- Later nights need rocks in the beam row or mid-night arrivals (a scope question for `game-director`).
