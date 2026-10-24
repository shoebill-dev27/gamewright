---
kind: decision
id: D-002
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-10
supersedes: none
---
# D-002: Fix combat monotony through enemy behavior; keep one-button combat

## Decision

The Owner chose Option A of escalation `goals/G-002-combat-monotony/04-game-director-to-owner.md`.
Combat depth for G-002 is built on the enemy side while the player kit stays attack plus dash:

- Telegraphed enemy attacks.
- Two new enemy types: a Charger (rushes the player) and a Shieldbearer (guards the front).
- Room compositions that ask the player where to stand, when to dash and which enemy to hit first.
  This is the former "Option C", folded into A by the Game Director.

D-001 (one attack button plus dash) stays in force and is not changed. No heavy-attack button and no
new input are added.

Owner's own words (2026-10-10):

> Aで。ワンボタンは守りたい。ただ、同じボタンの長押しで溜め攻撃、みたいな案なら将来は検討してもいい。今回はやらない。

Conditions and limits:

- Hold-to-charge on the same attack button is **not** part of G-002 and must not appear in the spec,
  plan or build for this Goal.
- The Owner is open to hold-to-charge as a possible future direction. It would be a separate Goal
  and a new Owner decision. This note does not approve it.

## Rationale

The observed monotony comes mainly from enemies that demand no positioning or timing. Option A
addresses that directly. It protects pillar 1 (one-button combat) and D-001, is reversible, and
leaves Option B (or a hold-charge variant) open for later. The only evidence for B was one player
remark.

## Alternatives considered

- **Option B: add a heavy-attack button.** It would replace D-001 and answers the "I want a heavy
  hit" remark, but only partly addresses "the same tactic clears every room". The Owner declined it.
- **Room-composition tuning alone.** The Game Director judged its ceiling too low on its own, so it
  is included in A.
- **Hold-to-charge on the attack button.** Raised by the Owner as a possible future idea. Explicitly
  not for this Goal.

## Revisit when

- The re-playtest after Option A is built still shows that the cause is "the player has too few
  actions available". This matches D-001's own revisit condition.
- The Owner wants to explore hold-to-charge or any other player-side option. That would be a new Goal
  and a new Owner decision.
