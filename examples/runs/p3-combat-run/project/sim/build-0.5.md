# Simulated build 0.3.2 — what playing it looks like

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

Dash and hit protection (same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs):

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned for the first 0.3 s.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after it ends. You stay protected until 0.8 s after the hit, then damage can land again.
- Dash started between 0.55 s and just under 0.8 s after a hit: no damage during the dash. Protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later.
- Dash started at 0.8 s or later after a hit: the hit protection has ended; the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection; at 30 FPS versus 60 FPS this can differ by one frame.

Input during the 0.3 s stun after a hit (same at 30 FPS and 60 FPS):

- Pressing dash at any moment in the first 0.3 s (for example about 0.05, 0.15 or 0.28 s after the hit) does nothing. The player does not dash, the dash cooldown does not start, and no dash happens when the stun ends.
- Pressing attack at any moment in the first 0.3 s does nothing. No swipe appears then, and none appears when the stun ends.
- Holding dash or attack down through the end of the stun does nothing at that moment. Nothing fires until the button is released and pressed again. A fresh press after the stun ends works normally.
- A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected as described above.
- A press landing exactly at 0.3 s may be accepted on one frame earlier or later at 30 FPS than at 60 FPS.
- If a swipe was pressed during a dash, it still fires when the dash ends. A hit cannot land during a dash, so this never overlaps the stun.
- A hit that lands cancels any dash or attack request that was waiting, so nothing carries into the stun.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. No other changes to enemies, rooms or attacks.
