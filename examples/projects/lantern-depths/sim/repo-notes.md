# Simulated repository notes — lantern-depths

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data
  (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it
  is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on
  overlap. There is no concept of blocking or facing yet.
- Player invulnerability: time-based "invulnerable until t" (fixed in G-001).
- Movement: simple steering; walls stop movement.
- Tests: unit tests for player invulnerability; none for enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.
