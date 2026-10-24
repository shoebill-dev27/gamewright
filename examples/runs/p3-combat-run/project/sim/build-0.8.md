# Simulated build 0.8: what playing it looks like

Rooms 1 to 5 bring enemies in from the room edges in timed arrivals, some in a second wave. Each arrival is announced by a ground ring. Enemy health, speeds and attacks are as before. A Grub still takes two swipes. Room size, Grub speed, player speed, projectile speed and range, hearts and hitbox sizes are not stated here.

## What a room looks like

A room does not start with its enemies already on the floor. When you gain control, the first rings appear. Enemies arrive 0.8 s later. The room ends when every enemy of every wave is dead.

| Room | Wave 1 | Wave 2 | Total |
|---|---|---|---|
| 1 | 2 Grubs and 1 Spitter | none | 3 |
| 2 | 2 Grubs and 1 Spitter | 1 Grub | 4 |
| 3 | 2 Grubs and 1 Spitter | 2 Grubs | 5 |
| 4 | 3 Grubs and 1 Spitter | 1 Grub and 1 Spitter | 6 |
| 5 | 3 Grubs and 2 Spitters | 2 Grubs | 7 |

Arrival edges and timing, by room:

- **Room 1:** the first Grub rings at the west edge at the start. The second Grub rings 1.0 s later, also at the west edge, further along the wall. The Spitter rings at the start at the east edge.
- **Room 2:** wave 1 is the same as room 1. The wave 2 Grub rings at the east edge.
- **Room 3:** wave 1 is the same two Grubs from the west edge, with a Spitter at the north edge near the north-east corner. Wave 2 is two Grubs, both ringing at the same moment on the east edge, one nearer the north and one nearer the south.
- **Room 4:**
  - Wave 1 has two Grubs ringing at once on the west edge, one Grub on the east edge, and a Spitter at the north edge near the north-west corner.
  - Wave 2 has a Grub at the north edge and a Spitter at the south edge near the south-east corner.
- **Room 5:**
  - Wave 1 has two Grubs on the west edge, one Grub on the east edge, one Spitter at the south edge near the south-west corner and one Spitter at the north edge near the north-east corner.
  - Wave 2 has a Grub at the north edge and a Grub at the south edge, ringing together.

Enemies on an edge appear about 1 tile in from the wall. Grubs appear a quarter, half or three quarters of the way along the edge. In rooms 1 and 2 the Spitter appears on the east edge at mid-height (the other two east points are alternatives). In rooms 3 to 5 each Spitter appears about 1.5 tiles along its wall from a corner.

## Choice of arrival point

Each enemy has an ordered list of points, and nothing about the choice is random. The same player position and timing always give the same point. The choice is made once per enemy, at the moment its ring starts, and works like this:

1. The first point on the list that is at least 5 tiles from you and free is used. A point is not free if a ring is active there or a living enemy is within 1.5 tiles of it.
2. If no point passes both tests, the farthest free point is used, even if it is closer than 5 tiles. A near free point is therefore chosen over a far occupied one.
3. If every point is occupied, the farthest point overall is used.
4. In steps 2 and 3, if two points are equally far, the one earlier in the enemy's list is used.

- In steps 2 and 3 the enemy can appear closer than 5 tiles to you, and you get the same 0.8 s ring warning.
- Enemies whose rings start at the same moment are handled one after another in the order they are listed in the room's arrival data (rows in room order, and within a row in the order the row gives). A ring started by an earlier one counts as occupying its point when the next is chosen.
- Enemies that have not yet started their ring do not count as occupying a point.
- Your position and the occupancy of the points are read at the first game update at or after the scheduled ring start. At 30 FPS that can be up to one frame (about 0.034 s) later than at 60 FPS, so a very fast move across a 5-tile boundary, or an enemy moving across a 1.5-tile occupancy boundary, in that gap can change the point at one frame rate and not the other.
- For Spitters the second point is the other end of the same wall. A player standing in the covered corner makes the Spitter appear at the far end of that wall.
- A Spitter has no exception to the 5-tile distance.
- Whether any room is too small for this to be rare is not known from the build. A tester can count how often the fallback happens.
- Arrivals are inside the room and on screen.

## The arrival ring

- A flat orange-red ring (`#FF5A1F`) about 1.5 tiles across sits on the floor with a dim amber dot at its centre.
- Over 0.8 s the ring shrinks steadily to about 0.75 tiles.
- The ring and its dot are lit by themselves, not by the lantern. They look the same inside and outside the lantern's light.
- Brightness rises linearly in game time from 0.0 s. At 0.0 s the ring is at 40% of its full brightness, and it reaches full brightness at 0.6 s.
- In the last 0.2 s (0.6 to 0.8 s) the ring is solid at full brightness and the dot is amber `#FFC14D` at full brightness. The dot does not turn white or blue-tinted. Any glow around the dot is only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot is a dimmer amber.
- At 0.8 s there is one short burst of at most 0.15 s, and the new enemy is visible through it. The burst uses only `#FF5A1F` and `#FFC14D`. No part of it is white, near-white or cold-white.
- The ring is an outline with no fill. It is drawn under characters and under walls. It is the same for Grubs and Spitters.
- Where two rings overlap or touch, the overlap is no brighter than a single ring at its full brightness. Each ring keeps its own dot. Rooms 3 (wave 2), 4 (wave 1, west edge) and 5 (wave 1, west edge) have rings at the same moment.
- Standing in a ring does nothing to you. The ring has no effect on damage.
- It is visible for its whole 0.8 s from 8 or more tiles away, including outside the lantern's light.
- Its look and timing are the same at 30 and 60 FPS.
- It is a placeholder.

## Enemy arrival

- No enemy exists, moves or attacks while its ring is on the floor.
- The enemy appears at the ring's centre 0.8 s after the ring's scheduled start.
- At 30 FPS the ring start and the appearance can each land up to one frame (about 0.034 s) later than the exact moment. At 60 FPS the difference is half that.
- A Spitter does not fire when it appears. Its first shot comes 1.0 s after its scheduled appearance, and then one every 2 s. The shot times follow the schedule, not the frame on which they are noticed.
- The Spitter's projectile is as before: slow, and one step sideways avoids it.

## Wave timing

- The first wave's rings start the moment you gain control in the room. The second Grub of rooms 1 to 3 (the +1.0 s Grub) starts 1.0 s later.
- Wave 2, in rooms 2 to 5, starts at the earlier of these two moments:
  - the kill that leaves only one enemy still to deal with from wave 1 (the count includes an enemy whose ring has not yet started, one in its ring, and one on the floor);
  - 8.0 s after wave 1's first ring started.
- With no kills, wave 2's rings start 8.0 s after wave 1's first rings.
- Killing enemies quickly can start wave 2 while a wave 1 Grub still has not yet appeared. In that case the wave 2 ring starts at once and that Grub still arrives on its own schedule.
- Wave 2 does not start early while two or more wave 1 enemies are still alive or pending.
- At 30 FPS and 60 FPS, ring starts, appearances, wave starts and Spitter shots match within one frame at 30 FPS (0.034 s). The points chosen are identical except in the boundary case described under the choice of arrival point.
- Wave 2 starts from the kill moment, so it can begin before the room looks nearly empty.

## What it plays like

- Standing still in a spot and swiping is no longer a constant answer. Enemies come from several edges, at different times and in a second wave.
- A player holding a corner sees arrivals on the other edges, 5 or more tiles away unless the fallback applies. A Spitter near a held corner appears at the far end of its wall.
- Grubs from opposite edges can reach you at about the same time. Whether you take hits then depends on the room size and speeds, which are not stated here.
- Dashing is available as before. This build does not change what it does.

## Test output

- The debug log is a diagnostic only and does not change play. It has timestamped lines for each ring start, each appearance, each wave start and each Spitter shot. A Spitter shot line carries the scheduled shot time. Each ring start line and each appearance line carries the scheduled time (the frame time may also be given), as the Spitter shot line already carries the scheduled shot time.
- Each normal point choice writes `SPAWN_POINT room wave enemy chosenPoint clockTime`.
- Each fallback choice (steps 2 and 3) writes `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`.

## Values not available

Grub speed, player speed, projectile speed, projectile range, player hearts, room size (width by height), and the Grub, player and Spitter hitbox sizes are not available from this build. A tester or playtest has to measure them.

## Dash and hit protection

This is unchanged from the previous build. It is the same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs.

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned for the first 0.3 s.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash and none after it ends. You stay protected until 0.8 s after the hit.
- Dash started between 0.55 s and just under 0.8 s after a hit: protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later.
- Dash started at 0.8 s or later after a hit: the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection. At 30 FPS versus 60 FPS this can differ by one frame.

Input during the 0.3 s stun after a hit:

- Pressing dash or attack at any moment in the first 0.3 s does nothing. Nothing happens when the stun ends either.
- Holding a button through the end of the stun does nothing. A fresh press is needed.
- A press just after 0.3 s works normally. A press exactly at 0.3 s may be accepted one frame earlier or later at 30 FPS than at 60 FPS.
- A swipe pressed during a dash still fires when the dash ends.
- A hit cancels any dash or attack request that was waiting.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. There is no new input.
