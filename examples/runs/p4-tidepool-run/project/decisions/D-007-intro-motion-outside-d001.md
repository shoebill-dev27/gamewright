---
kind: decision
id: D-007
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-13
supersedes: none
---
# D-007: The level 1 start-of-level intro motion is outside D-001

## Decision

The level 1 intro motion (the pool slides about 25% toward the home and back, 0.8 s each way, once per level load) does not conflict with D-001. This confirms the designer's judgment. D-001 is unchanged and remains the Owner's pillar. This Decision interprets it and does not amend it.

Limits that keep it outside D-001. If any of these changes, this Decision no longer applies:
- It plays once per level load (including a level restart the player chose). It does not repeat.
- It is not tied to inactivity, to a countdown or to a score. Nothing happens on its own if the screen is left untouched afterwards.
- Cancelling it has no consequence. The pool eases back (D-002), and the intro is never in the undo history.
- It is a fixed demonstration of the goal, not a rule the child must obey. No state is lost, and any touch is answered.

## Rationale

D-001 forbids failure, timers and irreversible moves. The intro is a one-off animation on load. It does not pressure the player, measure time against them, or limit what they can do. It is also not the idle hint (Option C): that would trigger from inactivity, and this does not.

## Alternatives considered

- Treat the intro as touching D-001 and escalate to the Owner: not needed, because none of the three things D-001 forbids is present.
- Remove the intro: it would drop the only non-text teaching motion without any evidence against it.

## Revisit when

The intro is made to repeat, is triggered by waiting, or becomes a countdown. Also if real-child play shows the intro confuses children (D-002 trigger). An idle hint of any kind needs a Decide step and an Owner reading of D-001.
