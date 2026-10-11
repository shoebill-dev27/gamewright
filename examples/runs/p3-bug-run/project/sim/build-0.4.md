# Simulated build 0.4 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

Observations are the same at 30 FPS and 60 FPS, apart from timing differences of up to about one frame (roughly 33 ms at 30 FPS, 17 ms at 60 FPS) at the moment protection after a hit runs out.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is still rarely needed. Most runs use it only to cross the room faster. It covers 4 tiles in 0.25 s, with a 0.6 s wait before you can dash again.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.
- Dashing right after being hit: dashing at about 0.3, 0.4, 0.55, 0.7 or 0.79 s after a hit, with a Grub touching you or a Spitter projectile crossing your path, you take no damage for the whole dash, including its last moment. This holds at both frame rates.
- Dashing with no recent hit, with enemies in contact range or projectiles crossing the path: no damage during the dash.
- After a hit you lose 1 heart and are stunned for 0.3 s. You are then untouchable until 0.8 s after the hit. If you dash early in that period and the dash ends before 0.8 s, you stay untouchable until 0.8 s after the hit; enemies in contact do not hurt you until then. After that, contact damages you normally.
- Once both the dash and the period after a hit are over, enemies and projectiles hurt you normally (1 heart per hit).
- An attack pressed during a dash is remembered and swings as soon as the dash ends.
- A dash that begins or ends while an enemy is touching you: no damage during the dash. Damage can land on the first frame after the dash ends if the 0.8 s period after a hit is also over.
- Because the period after a hit is no longer cut short by an early dash, you may feel slightly safer right after being hit than in build 0.3.
- Enemies hit by your swipe still briefly flinch and interrupt what they were doing.
