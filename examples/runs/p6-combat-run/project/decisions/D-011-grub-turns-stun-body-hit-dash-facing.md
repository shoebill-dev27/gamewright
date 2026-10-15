---
kind: decision
id: D-011
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-011: Grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing

## Decision

The A1–A3 package and the A5 gap rules, for `design/combat.md`:

1. **A1 wind-up spacing:** a grub may not start a Wind-up within 1.0 s [tune] of another grub's Wind-up start. A blocked grub waits.
2. **Engagement cap (added, the second rule):** at most 2 grubs within 1.5 tiles of the player at once, counted in every state. Others wait at 2.0 tiles. Without this, A1 alone would still leave four grubs on all sides of the player.
3. **A2 hit-stun:** 0.3 s → 0.15 s [tune]. Invulnerability until 0.8 s after the hit is unchanged. No input buffering.
4. **A3 body hit:** an enemy within 0.5 tile of the player (distance 0 included) is hit by every swipe, whatever the facing.
5. **A5 rules:**
   - A dash with a direction sets facing to that direction; a dash without a direction keeps facing.
   - A dash stops at the room edge (up to 4 tiles).
   - A swipe resolves against true positions in every grub state. A hit during Strike cancels the rest of that strike and puts the grub in a 0.6 s Recovery. Player attacks resolve before enemy damage within a tick.
   - "(miss)" gains a cause: "(miss) too far" (an enemy within 2.5 tiles, beyond reach) and "(miss) not in front" (an enemy within 1.5 tiles, outside the cone and the body radius).
6. New acceptance criteria are AC-19…AC-27, all at 30 and 60 FPS.

Limits:
- No new input (D-001). Knockback, the grub cycle (0.5 / 0.15 / 0.9 s), the 90° cone, reach and the room layouts are unchanged.
- Spitters are not affected.
- It does not decide the manual text; the Owner places the draft in handoff 59.
- It settles the unspecified dash and swipe cases by rule, so QA's results (55) are checked against these rules and not against what the build does.

## Rationale

- The second playtest (54) and the still-player runs (53) show four grubs arriving together and biting in turns from a ring, with no gap to answer in. A1 spaces the commitments. The cap keeps the ring from forming at all, so a swipe or a dash has a clear target and a clear exit. Both are rules on the existing grub states and reuse the spitter stagger idea.
- 1.0 s spacing is longer than the 0.65 s of Wind-up plus Strike, so at most one grub is committed at a time. It is also longer than the dash cooldown (0.6 s), so each bite can be answered with a dash, and equal to or longer than the 0.8 s invulnerability, so no bite is silently absorbed. The cost is that a still player is not saved by invulnerability overlap. That is fine, because a still player is a reference, not a target.
- Hit-stun at 0.3 s took away the best answer (hit the winding-up grub) right after being hit. 0.15 s is at least 4 frames at 30 FPS and still reads as a hit.
- The body-hit rule fixes "the grub is on me and I cannot hit it" without a facing mechanic. D-006 allows overlap and always displays the enemy, so a swipe must be able to hit it.
- Dash sets facing like movement does: the least change to an existing rule, with no new input. It leaves the "backstep" variant to the Director if the retest needs it.
- No escalation trigger fires: no pillar, D-001 or Goal change, small cost, tuning and rules only.

## Alternatives considered

- **A4 cone 120°:** rejected for now. It weakens positioning (pillar 1) and A3 already covers the nearest case. It comes in if the retest shows "(miss) not in front" on at least 1 in 4 swipes with an enemy in reach, or testers still report missing diagonal grubs.
- **D1 facing mechanic (turn in place, auto-face on swipe, backstep dash keeping facing, 360° swipe):** rejected for now. It is a direction decision and risks D-001. It goes to `game-director` if the retest still reports swipes into air after dashes after A3 and the dash-facing rule.
- **D2 room 1 composition (fewer grubs, uneven start distances):** rejected for now. Fewer than 3 enemies breaks the room spec, and uneven starts are staggered arrival, deferred as part of Option B (D-002). A1 and the cap reach a similar effect.
- **A1 alone (no cap):** rejected. Spacing alone still allows a ring of four grubs and the "cornered" feeling.
- **A cap of 1 grub near the player:** rejected. It removes the multi-hit and positioning play of groups and makes rooms 1 and 2 close to duels.
- **Spacing of 0.5 s:** rejected. With a 0.5 s wind-up the bites would follow each other without a gap.
- **Stun kept at 0.3 s with a buffered swipe:** rejected. It adds an input buffer for the swipe that must also work at both frame rates, with no gain over a shorter stun.
- **Dash keeps facing (backstep) now:** rejected for now, see D1.
- **Distance-0 swipe rule without A3 (enemy on you counts as inside the cone):** rejected. A3 covers it and also covers an enemy just behind the player.

## Revisit when

- The retest (room 1 and room 2 by a reactive player) shows a skilled player still cannot clear room 1 or 2 with hearts left, or the rooms become trivial. Retune spacing (0.8–1.5 s), the cap (2 or 3) and the stun first.
- The retest shows A4's trigger (see above) or D1's trigger.
- The retest shows four grubs still read as one clump that feels like a wall: consider D2 / Option B staggered arrival through `game-director`.
- QA's checks (55) show a rule above cannot be built as written.
- Option B is opened (room mix, moving spitters), which changes the grub crowding assumptions.
