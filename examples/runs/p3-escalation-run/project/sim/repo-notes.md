# Simulated repository notes — lantern-depths (build 0.3)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data
  (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it
  is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on
  overlap. There is no concept of blocking or facing yet.
- Player invulnerability: one on/off flag. The dash switches it on and starts a 0.25 s timer;
  getting hit switches it on and starts a timer that ends 0.8 s after the hit. Each timer switches
  the flag off when it ends.
- Movement: simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.

<!-- dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
if a Role writes it into a Handoff. -->
