# Simulated repository notes — lantern-depths (build 0.4)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Player invulnerability (changed in 0.4): no longer a single on/off flag. The player tracks two independent sources: dash invulnerability (ends 0.25 s after dash start) and post-hit invulnerability (ends 0.8 s after the hit). The player is invulnerable while either source is active. One source expiring does not clear the other. The logic is in the shared player invulnerability path, so Grub bites and Spitter projectiles use the same code.
- Unchanged: dash 4 tiles over 0.25 s, dash cooldown 0.6 s, queued attack during dash, hit-stun 0.3 s, damage 1 heart, input set (D-001). Enemy behavior untouched.
- Expiry is checked per frame, so end times resolve to the first frame at or after the end time (up to about one frame late).
- Movement: simple steering; walls stop movement.
- Tests: none for invulnerability or enemies. The change has not been run or verified by tests; a unit test for "hit, dash at 0.6 s, invulnerable through 0.85 s" at both frame rates is still missing.
- Game loop uses variable delta time; 30 and 60 FPS supported.
