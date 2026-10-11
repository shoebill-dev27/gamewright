---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-11
supersedes: none
---
# D-003: Telegraphs are time-based with a 0.4 s floor, and at most 2 enemies attack at once

## Decision

- All enemy attack telegraphs are specified in real seconds. Timers run on elapsed time, not frame count. No telegraph is shorter than 0.4 s (12 frames at 30 FPS). Outcomes must match at 30 and 60 FPS.
- At most 2 enemies may be in a telegraph or attack phase at the same time. Spitter projectiles already in flight do not count.
- Damage is never applied in the update in which a telegraph begins, and the telegraph is shown for at least one rendered frame first.

Scope: build 0.4 enemy attacks in `design/combat-enemy-depth.md`. First tuning values (Charger windup 0.8 s, Shieldbearer turn rate 90°/s, and so on) are starting points and can be retuned after playtest without a new Decision.

## Rationale

- The project must play correctly at 30 and 60 FPS; frame-count timings would change difficulty between them.
- Pillar 3 (readable threats): a floor on the telegraph and a cap on simultaneous attacks keep mixed rooms fair and readable.
- Reuses the existing timer approach in the player kit (all in seconds).

## Alternatives considered

- Frame-based telegraphs: simpler to code, but breaks the 30/60 FPS requirement.
- No attack cap: more chaos in rooms 4–5, but unreadable stacking of threats. Rejected for pillar 3.
- A longer floor (0.6 s): more forgiving, but Grub and Spitter attacks would feel slow and the Grub's pace would drop.

## Revisit when

- Playtest shows telegraphs feel too slow or too fast, or the attack cap makes rooms feel passive.
- The Technical Director finds the cap cannot be built within the existing enemy controller at reasonable cost.
