# Simulated repository notes — lantern-depths (build 0.4)

Implemented change identifier: `0.3-G001-15`.
Current build description: `sim/build-0.4.md`.
`sim/build-0.3.md` describes the previous build.

Implementation facts only — never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Movement: simple steering; walls stop movement.
- Game loop uses variable delta time; 30 and 60 FPS supported. Desktop keyboard and gamepad are supported.
- Tests: none for invulnerability or enemies.

## Player invulnerability

- The writable shared invulnerability flag is removed. `dashProtectionActive` and `hitProtectionActive` are independently maintained. Effective invulnerability is their logical OR.
- An accepted dash starts dash protection only. It does not modify hit protection or its expiration.
- Dash protection follows the existing dash continuation state and ends in the existing dash termination processing. No separate dash-protection timer is added.
- A successful damaging hit starts hit protection until 0.8 s after that hit.
- Hit-protection expiration clears only hit protection. Dash termination clears only dash protection.
- Input loss ends after the existing 0.3 s duration without clearing hit protection.
- All previous invulnerability reads use the OR result. The old shared writes at dash start, dash end, damage application and hit-timer expiration are replaced by the corresponding source-specific operations. Any cached derived value is not directly overwritten by individual timers.

## Contact and projectile damage

Grub contact and Spitter projectile hits both enter the same player-damage gate:

1. Contact or projectile impact is established.
2. Effective invulnerability is checked before heart loss or input loss.
3. If either protection is active, player-damage processing returns without changing hearts, input loss, hit protection or its expiration.
4. Otherwise, the hit removes one heart, applies 0.3 s of input loss and starts 0.8 s of hit protection.

Neither hit source retains a bypass that directly manipulates the removed shared flag. Non-damage impact behavior, including existing projectile disappearance, is unchanged.

Blocked hits neither start hit protection nor extend either protection. Consequently, expiration of one source cannot cancel the other, and hits after both sources have ended can cause normal damage.

## Preserved behavior

- Dash distance remains four tiles and duration remains 0.25 s.
- Dash cooldown remains 0.6 s with its existing origin.
- An attack queued during a dash activates once at dash termination.
- Existing variable-delta-time and timer mechanisms are reused; no fixed-frame replacement is introduced.
- Existing event scheduling is unchanged. The damage-gate order does not establish priority between coincident dash transitions and hits.
- Enemy AI, Flinch, movement, walls, attack damage and recovery are unchanged.
- No new input buttons or save-format changes are defined.

## Limits of available implementation detail

- The cooldown origin is not specified in the supplied repository description and cannot be identified as dash start or dash end.
- At 30 FPS, the 0.25 s dash duration is not an integer number of frame intervals. Exact timer-update ordering, movement integration at the final interval and the observable termination frame are unspecified. No rounding tolerance or new timing policy is introduced.
- Exact collision geometry, enemy speeds, room coordinates, projectile trajectories and firing phases are unavailable. Frame-by-frame collision trials, numerical initial heart counts and valid-trial totals cannot be reconstructed from these inputs.
- The specified scenario times are exercise targets, not measured event logs. No independent QA result or executed test record is available.
- Input buffering during input loss, coincident-event priority, and unspecified save/restore or dash-interruption behavior remain undefined by this change.
