# Simulated build 0.3.1 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

Dash and hit protection (same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs):

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned with no input for the first 0.3 s. After 0.8 s damage can land again.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after the dash ends. You stay protected until 0.8 s after the hit, then damage can land again.
- Dash started between 0.55 s and just under 0.8 s after a hit: no damage during the dash. Protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later. Damage cannot land partway through the dash.
- Dash started at 0.8 s or later after a hit: the hit protection has ended; the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- Compared with 0.3, a hit followed quickly by a dash now gives more safe time, since the dash ending no longer ends the hit protection early.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection; at 30 FPS versus 60 FPS this can differ by one frame.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. An attack pressed during a dash still fires when the dash ends. A dash pressed during hit-stun behaves as it did in 0.3.
- No other changes to enemies, rooms or attacks.
