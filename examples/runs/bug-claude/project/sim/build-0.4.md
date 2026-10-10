# Simulated build 0.4 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

## Dash and being hit (changed in 0.4)

Behavior is the same at 30 FPS and 60 FPS, apart from the frame-sized timing differences noted below.

- Taking a hit still costs 1 heart, locks out input for 0.3 s, and then leaves you unhurtable until 0.8 s after the hit.
- A dash still covers 4 tiles in 0.25 s, has a 0.6 s cooldown, and an attack pressed during the dash still fires when the dash ends.
- You cannot be hurt at any moment from the start of a dash to its end. This holds whether the dash begins with no recent hit or any time after a hit, once input returns (about 0.3 s after the hit). A Grub touching you or a Spitter projectile reaching you during the dash does nothing, for both enemy types.
- If a dash starts shortly after a hit (for example 0.6–0.75 s after it), you stay unhurtable through the whole dash, even though the 0.8 s post-hit period runs out partway through. Protection then ends when the dash ends.
- If a dash starts early after a hit (for example about 0.3 s or 0.5 s after) and ends before the 0.8 s mark, you remain unhurtable for the rest of the 0.8 s post-hit period after the dash. The dash ending does not make you vulnerable early.
- Once both the dash and the 0.8 s post-hit period are over, the next contact hurts normally.
- Edge timing: protection ends on the first frame at or after its end time. At 30 FPS that can be up to about 33 ms late, and at 60 FPS up to about 17 ms late. So a contact landing within one frame of an end time can go either way depending on frame rate. This is not visible in normal play.
- A hit taken without dashing behaves as before: 1 heart, 0.3 s of input lock, unhurtable until 0.8 s after the hit.
- The fix has not been run or tested in this simulation; the description follows the change as specified.
