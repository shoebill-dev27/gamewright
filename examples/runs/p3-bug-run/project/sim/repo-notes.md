# Simulated repository notes — lantern-depths (build 0.4)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Player invulnerability (changed in this build): the single shared on/off flag and its two "switch off" timer callbacks are removed. Two independent sources are combined:
  - Dash source: invulnerable while the dash state is active, read directly from the dash state.
  - Post-hit source: on a hit, `hitInvulnUntil = hitTime + 0.8 s` using accumulated game time (sum of delta time); active while `gameTime < hitInvulnUntil`.
  - `isInvulnerable = isDashing || gameTime < hitInvulnUntil`. The damage check reads `isInvulnerable` when damage would apply. Nothing writes a flag, so one source ending cannot cancel the other.
  - No per-frame countdowns; frame-rate independent apart from up to one frame of quantization at the end of the 0.8 s window.
  - Damage on the exact frame a dash starts or ends depends on the order of the dash-state update and the damage check within a frame; the check reads the dash state at check time.
- Unchanged: enemy controller, hit-stun (0.3 s), dash movement (4 tiles over 0.25 s), dash cooldown (0.6 s), attack queuing during a dash.
- Movement: simple steering; walls stop movement.
- Tests: unit tests added for invulnerability, stepping the simulation at fixed delta times of 1/30 s and 1/60 s: hit at t=0 then dash at 0.3, 0.4, 0.55, 0.7, 0.79 s (no damage during the dash); dash with no prior hit (no damage); dash ending before 0.8 s (damage blocked until 0.8 s after the hit, applies after); dash and hit in the same frame. No tests for enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.
