# Simulated repository notes: lantern-depths (build 0.8)

Dry-run stand-in for reading the game's code. Implementation facts only. Never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Per-controller, not per-type. Not described in `design/combat.md`. Unchanged.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Player invulnerability: two expiry timestamps on the accumulated game clock: `hitInvulnUntil` (hit time + 0.8 s) and `dashInvulnUntil` (dash start + 0.25 s). `isInvulnerable(now)` returns `now < max(hitInvulnUntil, dashInvulnUntil)`. Every damage source calls it. Unchanged.
- Hit-stun: `hitStunUntil` = hit time + 0.3 s, set where `hitInvulnUntil` is set. Presses during it are dropped, with no buffering. A hit clears pending dash and attack requests. Presses are edge-triggered. Unchanged.
- Dash distance, duration and 0.6 s cooldown unchanged. An attack queued during a dash still fires on dash end.
- Movement: simple steering; walls stop movement.

## Phase 1 additions (encounter escalation)

- **Room data table (data per D-004).**
  - Coordinates are room-relative. The floor area is W×H tiles, measured from the wall faces, x east and y south. No absolute room size is stored.
  - Edge points are 1 tile inside the wall face at 25%, 50% and 75% of the edge length:
    - W1..W3 = (1, 0.25H / 0.50H / 0.75H)
    - E1..E3 = (W−1, same y)
    - N1..N3 = (0.25W / 0.50W / 0.75W, 1)
    - S1..S3 = (same x, H−1)
  - `SP(wall, corner)` is 1 tile inside the wall face and 1.5 tiles along the wall from the named wall-face corner: SP(N,NW) = (1.5, 1), SP(N,NE) = (W−1.5, 1), SP(S,SW) = (1.5, H−1), SP(S,SE) = (W−1.5, H−1).
  - Each enemy entry holds type, wave, marker offset from the wave start, and an ordered candidate list. Entries are in the order of spec table 3.2a (rows in room order, and within a row in the order the row gives). Enemies with the same marker start are processed in that table order on the same frame.
  - Room totals are 3, 4, 5, 6 and 7 enemies. Rooms 1 to 3 use the same wave 1 Grub pair (W1,W2,W3 and W3,W2,W1; the second at +1.0 s).
  - Spitter lists are E2,E1,E3 in rooms 1 and 2 (no corner-covering pair); SP(N,NE),SP(N,NW) in room 3; SP(N,NW),SP(N,NE) in room 4 wave 1; SP(S,SE),SP(S,SW) in room 4 wave 2; SP(S,SW),SP(S,SE) and SP(N,NE),SP(N,NW) in room 5. The "other end of the same wall" second point applies to the corner-covering Spitters of rooms 3 to 5 only.
- **Tuning values stored as data:** marker duration 0.8 s, wave timeout 8.0 s, minimum spawn distance 5 tiles, occupancy radius 1.5 tiles, Spitter offset 1.5 tiles, Grub marker gap 1.0 s, Spitter first-shot delay 1.0 s. Spitter interval after the first shot is 2 s. Marker brightness at 0.0 s is 40% of peak (one data value).
- **Wave scheduler (small module, game-clock timestamps only).**
  - `T0` is the clock time of the first logic frame on which the player has control in the room. Wave 1 starts at `T0`.
  - An enemy's marker start is `waveStart + markerOffset`, a scheduled timestamp. The marker end is `markerStart + 0.8` using the scheduled value, not the frame time.
  - Unresolved count = enemies of the current and earlier waves that are not dead. It includes pending (marker not started), in-marker and on-field enemies.
  - Wave N+1's start is set once, to the earlier of:
    - the clock time of the logic frame of the kill that makes the unresolved count 1 or fewer (checked on each kill event);
    - `firstMarkerStart(wave N) + 8.0 s`, as a scheduled timestamp.
  - Wave 2 can start while a wave 1 Grub is still pending.
  - The room ends when every enemy of every wave is dead.
- **Spawn point choice (routine, no RNG).**
  - It runs once per enemy at its marker start. Player position and occupancy (including enemy positions against the 1.5-tile radius) are both read on the first logic frame at or after the scheduled marker start. At 30 FPS this can be up to one frame (0.034 s) later than at 60 FPS.
  - Step A: walk the candidate list in order; take the first candidate that is at least 5 tiles from the player (centre to centre) and unoccupied. Occupied = an active marker at the point, or a living enemy within 1.5 tiles.
  - Step B: if none passes both, take the farthest unoccupied candidate (a near free point beats a far occupied one).
  - Step C: if all are occupied, take the farthest overall.
  - Ties in B or C go to the earlier list entry.
  - Enemies with the same marker start are processed in table order on the same frame, so an earlier enemy's new marker is active (occupying its point) when the next is evaluated.
  - Spitters have no exemption from the distance rule.
  - Pending enemies do not count toward occupancy. Active markers do.
  - Every step B or C choice writes a `SPAWN_FALLBACK` line.
- **Enemy creation timing.** No enemy object exists, moves or attacks before its marker ends. The enemy is created at `markerStart + 0.8` at the chosen point.
- **Spawn marker visual.**
  - Built from `design/g001-telegraph-visuals.md` section 3; reviewed by `art-director` under handoff 45, with the changes below.
  - It is a flat, non-directional ground ring 1.5 tiles across with a centre dot. The ring is `#FF5A1F`. The dot is `#FFC14D`, dim before 0.6 s and at full brightness from 0.6 s to 0.8 s, with no white or blue tint. Any glow uses only `#FFC14D` or `#FF5A1F`.
  - Ring and dot are drawn self-lit and do not read the lantern's light radius.
  - The ring contracts linearly to about 0.75 tiles over 0.8 s. Brightness ramps linearly in game time from 40% of peak at 0.0 s to 100% at 0.6 s, and stays 100% from 0.6 to 0.8 s.
  - At 0.8 s there is one burst of at most 0.15 s that does not hide the enemy. The burst palette is only `#FF5A1F` and `#FFC14D`; no white, near-white or cold-white element (`#E8F4FF` is reserved for hit feedback, D-006).
  - The ring is an outline with no fill and does no damage. Where markers overlap or touch, brightness is capped at a single marker's peak and each marker draws its own dot. It is drawn on the ground under characters and under walls. It is the same for Grub and Spitter.
  - The animation is a function of elapsed game time, so it is identical at 30 and 60 FPS.
- **Spitter first shot.** The first shot is a scheduled timestamp on the game clock: scheduled appearance (`markerStart + 0.8 s`) + 1.0 s, then every 2 s. The log line carries the scheduled value. A Spitter never fires on the frame it appears.
- **Debug log (diagnostic only, no gameplay effect).**
  - Normal choices write `SPAWN_POINT room wave enemy chosenPoint clockTime`.
  - Fallback use writes `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`.
  - Each marker start, spawn, wave start and Spitter shot also writes a timestamped line. Marker start and spawn lines carry the scheduled time (frame time may also be given), as the Spitter shot line carries the scheduled shot time.
- **Not changed:** dash, hit-stun, hit and dash invulnerability, the 0.2 s Flinch, enemy speeds and HP, attack and dash input. No new input. No Phase 2 content (Lunge Grub, Fan Spitter, Flinch changes). The latest change (handoff 55) altered build description wording only; no code, timing or data changed.
- **Values not present in these notes (not available, none estimated):** Grub speed, player speed, projectile speed and range, player hearts, room size, Grub, player and Spitter hitbox sizes. QA and the playtest record them.
- **Tests:**
  - Existing unit tests for `isInvulnerable` and hit-stun input are unchanged. They run on a simulated game clock at fixed steps of 1/30 s and 1/60 s and with varying delta times.
  - Tests of the same pattern cover marker timing, wave trigger (timeout and kill), point choice and fallback, tie-break, occupancy, the Spitter lists, the Spitter first-shot delay, and equal results at 1/30 s, 1/60 s and variable delta time.
  - No test results are recorded.
- **Game loop:** variable delta time; 30 and 60 FPS supported.
- **Naming:** this file is the current notes; the latest build description is `sim/build-0.8.md`, headed 0.8. `build-0.7.md` and `build-0.6.md` were both headed 0.3.3.
