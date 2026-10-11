---
kind: decision
id: D-008
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-008: Phase 1 spawns are deterministic from ordered candidate lists; waves trigger on an unresolved-enemy count; Spitters keep the 5-tile rule through a far-end alternative

## Decision

1. **Wave trigger.** Wave N+1's markers start when waves N and earlier have 1 or fewer unresolved enemies (enemies not yet marker-started, in a marker phase or on the field all count), or 8 s after wave N's first marker started, whichever comes first.
2. **Spawn point choice.** There is no RNG. Each enemy has an ordered candidate list in the room data. At its marker start, it takes the first point that is at least 5 tiles from the player and is not occupied (no active marker there, no living enemy within 1.5 tiles). If none qualifies, it takes the farthest unoccupied candidate. Edges have 3 room-relative points (25%, 50%, 75%, 1 tile inside the wall). Lists are in `design/g001-combat-escalation.md` 3.2a.
3. **Spitters.** There is no exemption from the 5-tile rule. A corner-covering Spitter has two points on its wall: next to the covered corner, then at the far end of the same wall. Covered corners: room 3 NE; room 4 NW then SE; room 5 SW and NE.
4. **"Simul."** means the same marker start only. The 0.3 s arrival gap is a tuning intent, not a rule.
5. **Marker starts.** Wave 1 starts when the player gains control of the room. A Spitter's marker starts at its wave start. A second Grub "1.0 s apart" starts 1.0 s later.
6. **Existing values** (Grub speed, player speed, projectile speed and range, hearts, room size) are not supplied by the design documents. Phase 1 proceeds without them. The Build reports what it can read and writes "not available" otherwise. QA and the playtest record them.

Limits: no new input, no pillar change, no marker look change, no Phase 2 content. The Spitter's behavior is unchanged. This is placement data only.

## Rationale

- Counting pending enemies as unresolved is the only reading of "alive" that does not make wave 2 start at once. It keeps "the E wave comes after the W wave".
- Ordered lists make the scripted 30 vs 60 FPS run (criterion 5) checkable and keep each lane stable from run to run. Random choice would make both hard to verify.
- Putting the second Spitter point at the far end of the wall keeps the corner covered when the player is holding it, and never spawns a Spitter beside the player. That keeps the "threats readable before they can hurt" pillar and criterion 4 without exceptions.
- Corner choices give every corner coverage at least once in rooms 3–5, and two corners in each of the P1-1 rooms (4 and 5), so no single corner is a safe default.
- Dropping the 0.3 s arrival rule avoids a promise that cannot be verified without Grub speed, which nobody has supplied.

## Alternatives considered

- **Count only on-field enemies, with a guard until wave N has fully spawned (engineer's option b):** it gives about the same result, but the guard is an extra special case. Not needed.
- **Seeded RNG among qualifying points:** variety, but not checkable by a scripted run and not stable lanes. Rejected.
- **Spitters exempt from the 5-tile rule:** a Spitter could appear next to the player, against criterion 4. Rejected.
- **A scheduler check on the arrival gap for "simul.":** needs Grub speed, which is unknown. Rejected for now. Revisit after the playtest.
- **Wait to build until the existing values are found:** Phase 1 does not use them, so this would only delay it.

## Revisit when

- The room is too small for the 3-point edges and the 5-tile rule, so most spawns use the fallback.
- The playtest shows the "simul." Grubs arrive far enough apart that two-side pressure disappears (add the arrival-gap check).
- Criterion 1 fails after Phase 1 (use the layout variant in 3.6).
- The Build or QA finds the occupancy distance causes odd choices.
