---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-10
supersedes: none
---
# D-003: Telegraphed enemy attacks are committed

## Decision

Once an enemy starts a telegraph, the telegraph and the attack always complete. Player hits during
the telegraph or attack deal damage but cause no flinch. Enemies flinch (0.2 s) only when hit
outside a telegraph or attack. Applies to every telegraphed attack, current and future.

## Rationale

Telegraphs exist to make the player read and respond (D-002). If hits cancelled them, continuous
swiping would cancel threats and restore the corner-and-swipe strategy G-002 is removing.

## Alternatives considered

- Hits cancel the telegraph: rewards aggression but recreates the dominant strategy.
- Per-enemy rules: more tuning freedom, but players could not learn one consistent rule.

## Revisit when

Playtests show committed attacks feel unfair for a specific enemy, or a future enemy is designed
around being interrupted.
