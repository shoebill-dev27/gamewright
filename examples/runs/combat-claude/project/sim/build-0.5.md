# Simulated build 0.5 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. Lengths are in seconds, distances in tiles, speeds in tiles per second. Everything below holds the same at 30 FPS and 60 FPS unless a difference is stated.

## Rooms and waves

- Every room sends its enemies in two waves. The first wave appears when the room starts. The second wave appears when the number of living enemies drops to the room's threshold, or when the room's timer runs out, whichever happens first.
- Enemies that are fading in count as living. Enemies still waiting to appear do not count.
- The timer starts when the last enemy of the earlier wave has finished fading in. If that enemy had to wait at its spot first, the timer starts after the wait and the fade-in.
- Room 1: wave 1 is two ordinary Grubs, left and right. Wave 2 is one ordinary Grub at the far side. It comes when one or fewer enemies are alive, or 10 s after the last wave-1 Grub finished fading in. 3 enemies in total, at most 2 at once. No charging Grubs.
- Room 2: wave 1 is one charging Grub at the far side. Wave 2 is two ordinary Grubs (left, right) and one more charging Grub (far side). It comes when no enemy is alive, or 15 s after the wave-1 Grub finished fading in. 4 enemies in total, at most 3 at once.
- Room 3: wave 1 is a Spitter at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in whichever far corner is farther from you at the moment the wave is triggered, and an ordinary Grub on the right. It comes when one or fewer are alive, or 12 s after the last wave-1 enemy finished fading in. 4 enemies in total, at most 3 at once. Spitters fire every 2.0 s. No charging Grubs.
- Room 4: wave 1 is a Spitter in the far-left corner, a charging Grub at the far side and an ordinary Grub on the left. Wave 2 is a Spitter in the far-right corner and a charging Grub on the right. It comes when one or fewer are alive, or 12 s. 5 enemies in total, at most 3 at once. Spitters fire every 1.8 s.
- Room 5: wave 1 is a Spitter at the far side and two ordinary Grubs, left and right. Wave 2 is a Spitter in the farther far corner and two charging Grubs, left and right. It comes when one or fewer are alive, or 12 s. 6 enemies in total, at most 4 at once. Spitters fire every 1.6 s.
- A room ends when every wave has appeared and every enemy is dead.
- The farther-corner choice is made when the wave is triggered, before any waiting. The two corners are compared by distance from the center of you to the center of each spot. If the distances are exactly equal, the front-left corner is used. If you move while the wave waits, the choice does not change. A corner that a room names for a specific enemy is not part of this choice.

### How fast Grubs walk

Ordinary and charging Grubs in the same room walk at the same speed:
- Room 1: 2.0
- Room 2: 2.0
- Room 3: 2.2
- Room 4: 2.2
- Room 5: 2.4

This is walking speed only. A charge always runs at 8.0. Spitters stand still.

### Standing near a spawn point

- If you are closer than 4 tiles (center to center) to the spot where an enemy would appear, that enemy does not appear yet. It appears as soon as you are 4 tiles or farther away, or after 2.0 s of waiting, whichever comes first.
- Each spot of a wave waits on its own. All spots of one wave start waiting at the same moment, when the wave is triggered. A spot that has finished waiting does not wait again if you walk back to it. You are not pushed away from a spot, and the enemy can appear on top of you.
- While some enemies of a wave are still waiting, the next wave's threshold and timer are not running. They start only once every enemy in the wave has begun fading in.
  - If one or fewer enemies are alive at that moment, the next wave comes immediately. Otherwise it comes when the count drops to the threshold, or when the timer runs out.
  - Room 1: stand near the left spot only. The right Grub appears and the second wave does not come while the left spot waits. If you kill the right Grub during the wait, then when the left Grub begins fading in only one enemy is alive, and the wave-2 Grub comes at once. If you did not kill it, the second wave comes after one is killed, or 10 s after the later one finished fading in.
  - Room 2: if the charging Grub's spot is waiting, the second wave cannot come until it begins fading in. After that it comes when the Grub is dead, or 15 s after it finished fading in. The Grub cannot be hurt during its first 0.8 s of fading in, so the earliest kill is after that.
  - Waves with no waiting spots start counting the moment they appear.

## Enemies appearing

- Every enemy fades in for 0.8 s: from 40% to full opacity, with a pale blue ring at its feet. During this time it does not move, does not attack, does not hurt you, and your swipes do nothing to it (no damage, no flinch).
- A Spitter fires its first shot 1.0 s after it finishes fading in, then at the room's interval. A Spitter shot travels at 4.0, straight at where you stood when it fired, costs 1 heart, vanishes on walls, and passes through enemies without hurting them. Spitters flinch for 0.2 s when hit, as before.

## Charging Grubs

Charging Grubs (rooms 2, 4, 5) look like ordinary Grubs with a dark ember-colored ridge on the back, visible from the moment they fade in. Ordinary Grubs have no ridge. They have 2 HP, and walk and bite like ordinary Grubs. While walking they flinch for 0.2 s when hit.

A charging Grub starts a charge only when all of the following hold:
- at least 1.5 s have passed since it finished fading in;
- at least 2.5 s have passed since its last recovery ended, that is, since it went back to walking after its last charge. The 0.8 s of recovery is not part of the 2.5 s. For example, if a charge ends at time t, the Grub stands in recovery until t+0.8, and its next wind-up can begin no earlier than t+3.3. A Grub that has never charged has no such wait;
- you are 3.0 to 6.0 tiles away (center to center);
- no other living charging Grub is currently winding up or charging.

Flinching does not reset these waits. If two charging Grubs qualify in the same moment (room 5, wave 2, left and right), one of them goes first, in a fixed but not obvious order. The other waits until the first has finished charging.

The sequence:
1. **Wind-up, 0.7 s.** The Grub stops where it stands and its walking animation stops. A red-orange lane appears on the floor from the Grub toward where you were when the wind-up began. The lane is as long as the charge will be, 7 tiles or less if a wall is in the way, and as wide as the Grub's body (within 0.1 tile). It has a bright edge, a dark underline and a chevron every tile pointing along the lane. It stays lit regardless of floor darkness. Spitter shots, fading-in enemies and other enemies are drawn on top of it. The lane fades from 35% to full brightness over the wind-up. The Grub squashes to 80% height, widens a little and leans back from the lane. The ridge and eyes warm from dark to red-orange, turning pale-yellow in the final 0.1 s. The direction is fixed; moving afterwards does not turn the lane. The Grub does no damage during the wind-up.
2. **Charge.** The Grub rushes along the lane at 8.0 for up to 7 tiles (about 0.875 s), or until it hits a wall, and stretches long and thin with a bright core and red-orange edge. The lane flashes extra bright once at the start, stays at full brightness, and disappears behind the Grub as it passes. The part in front stays until the charge ends, then everything fades out over 0.1 s. Afterimages appear every half tile and fade over 0.2 s, with dust at its feet. It passes through other enemies without hurting them. Hitting a wall has no special effect; the Grub simply stops and goes into recovery.
3. **Recovery, 0.8 s.** The Grub stands still, sunk to 90% height and tinted a dull grey-blue, fully opaque, with thin steam rising from its feet every 0.3 s. Ridge and eyes go dark within 0.1 s. It returns to normal in the last 0.2 s and goes back to walking toward you. It cannot start another wind-up for 2.5 s after this moment.

### Getting hit by a charge

- A charge can hurt you at most once. The first time the Grub's body overlaps you during a charge decides it. If it was already overlapping you as the charge began, that counts as the first moment.
  - If you are invulnerable at that moment (for example, mid-dash), you take nothing. A thin pale white-blue ring appears around you for 0.15 s, and the Grub keeps running through you. The Grub's core dims to a darker red-orange for the rest of the charge. Staying inside it afterward, or the dash ending while it still overlaps you, does not hurt you.
  - If you are not invulnerable, you lose 1 heart, with the normal hit reaction and the normal invulnerability afterward. The core dims in the same way. No ring appears.
- Overlap during the wind-up or recovery does nothing. A new charge starts the count again.
- The invulnerability check uses the state you are in at that frame. At 30 FPS the end of the dash's 0.25 s protection can differ from 60 FPS by up to one frame (about 0.034 s).

### Hitting a charging Grub

- During the wind-up, charge and recovery, your swipes lower its HP only. It does not flinch, is not pushed back, and does not change direction, speed or timing. It flashes white for 0.1 s with small sparks at the point of impact. The lane and ridge do not change.
- With 1 HP left, a small crack mark appears on its body.
- At 0 HP it dies immediately in any state. A dying winder or charger removes its lane within 0.1 s, and another charging Grub may then start its own wind-up.
- Charging Grubs that are walking, ordinary Grubs and Spitters flinch 0.2 s as before.

## Your own numbers

Nothing about you has changed:
- Your swipe does 1 damage and takes 0.35 s to recover.
- Your dash covers 4 tiles in 0.25 s, you are invulnerable for all of it, and it has a 0.6 s cooldown. A swipe pressed during a dash comes out when the dash ends.
- A hit costs 1 heart, locks your input for 0.3 s, and you are invulnerable until 0.8 s after the hit.
- Movement speed, swipe reach and your size are unchanged. No new buttons.

## Timing at 30 and 60 FPS

- Fade-in, wind-up, charge distance, recovery, the 2.5 s wait, wave timers and spawn waiting are all counted in real time. Durations at 30 FPS are within about 0.034 s of those at 60 FPS.
- Whether a charge touches you does not depend on the frame rate.
- Pausing freezes all timers and animations, including lanes, steam and rings. Resuming after a long pause does not skip ahead more than a short step (0.05 s).
- Nothing flashes more than three times per second, apart from single flashes.

## What play feels like now

- Rooms 1 and 3 behave like before but with two waves, so there is a second arrival to deal with.
- In rooms 2, 4 and 5, standing still in a corner and swiping no longer works: a lane appears, and about 0.7 s later a Grub runs the length of it. Moving off the lane or dashing through the Grub avoids damage. Swiping the Grub during the run only chips it and does not stop it.
- A single charging Grub charges again about 3.3 s or more after its previous charge ended, and later if you are out of the 3.0–6.0 range or another one is busy.
- Only one charging Grub is ever winding up or charging at a time.
- No new sounds. No new buttons.
- As before, occasionally, if you dash right after being hit, you take damage partway through the dash. This also applies to a charge that reaches you at that moment.

## Development build only

- A tester can pick room 1–5, switch charging Grubs on or off per room (off turns every charging Grub into an ordinary Grub, with no ridge, no lane and no charge; the room's counts, waves and spots stay the same), and switch between 30 and 60 FPS.
- A log lists state changes with game time, enemy and type, charge direction, contact result (unresolved, slipped through, hit), wave arrivals with spots, which corner was chosen, the distance to you when a wind-up began, and the moment all enemies of a wave have begun fading in.
- The log also records the time each charging Grub's recovery ended and it went back to walking, so the gap to its next wind-up can be read directly.
