# Simulated repository notes — lantern-depths (build 0.6)

Implementation facts only — never load this for a Playtester.

Facts carried over and still true:
- Enemies share one controller. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: a hit enemy enters a 0.2 s Flinch that interrupts anything, including Attack, then returns to Chase. Not described in `design/combat.md`.
- The player's attack is a short arc hitbox. Enemies take damage on overlap. No blocking or facing.
- Player invulnerability is one on/off flag. The dash sets it and starts a 0.25 s timer. Getting hit sets it and starts a timer ending 0.8 s after the hit. Each timer clears the flag when it ends, so a dash within 0.8 s of a hit loses protection mid-dash. This code was not touched. Other player numbers (attack damage 1, recovery 0.35 s; dash 4 tiles in 0.25 s, cooldown 0.6 s, buffered attack at dash end; hit stun 0.3 s; speed, reach, hitbox) are also untouched.
- Movement is simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- The game loop uses variable delta; 30 and 60 FPS are supported.

Changes (described, not built or run; assumptions from the register are unverified against real code):
- Delta is capped at 0.05 s per update, including the first update after unpausing. State timers use delta, carry leftovers into the next state, and stop while paused.
- Room data holds waves (spawn list of type and slot), next-wave condition (K, T), Grub speed, Spitter interval and charge switch. Spawn timings (fade-in 0.8 s, first Spitter shot 1.0 s after fade-in, spawn wait at 4 tiles up to 2.0 s) are shared constants.
- Slots (six, coordinates in room data, actual values unknown):
  - Door: door side.
  - Far: back middle.
  - L: left side.
  - R: right side.
  - FL: far-left corner.
  - FR: far-right corner.
  - No slot exists for a near (door-side) corner. Corner slots are only FL and FR.
- Room table (waves; K/T for wave 2; Grub speed; Spitter interval; charge switch):
  - R1: [Grub L, Grub R], [Grub Far]; K=1 T=10; 2.0; –; off.
  - R2: [Charger Far], [Grub L, Grub R, Charger Far]; K=0 T=15; 2.0; –; on.
  - R3: [Spitter Far, Grub L], [Spitter farther of FL/FR, Grub R]; K=1 T=12; 2.2; 2.0; off.
  - R4: [Spitter FL, Charger Far, Grub L], [Spitter FR, Charger R]; K=1 T=12; 2.2; 1.8; on.
  - R5: [Spitter Far, Grub L, Grub R], [Spitter farther of FL/FR, Charger L, Charger R]; K=1 T=12; 2.4; 1.6; on.
- Grub Chase speed per room (2.0, 2.0, 2.2, 2.2, 2.4) applies to both `grub` and `grub_charger` walking. It is not used for Charge (8.0).
- Spawner: wave 1 at room start. Wave N+1 spawns when living enemies ≤ K or T seconds after the last enemy of wave N finished fading in (after any wait), whichever is first. Living enemies include fading-in enemies and exclude those waiting at a slot. K and T are checked only once every enemy in wave N has started fading in; this start point is logged and set in one place. For waves without waiting enemies it is the spawn decision.
- Slot waiting: per slot, all slots of a wave start waiting together at the spawn decision; player-to-slot center distance under 4 tiles waits up to 2.0 s. A slot that finished waiting does not wait again. The player is not pushed out of a slot.
- Far corner choice (FL or FR), in order: use the player position at the spawn decision (before waiting); compute center-to-center distance from the player to the FL slot and to the FR slot; the larger distance wins; on exactly equal distances FL is used; only FL and FR are candidates; the choice is not redone while waiting. Does not apply when FL or FR is named as a fixed slot for another enemy in the same wave. The chosen corner (FL or FR) is written to the log with the wave arrival.
- Charge switch: one place in the spawner replaces `grub_charger` with `grub` when off. No visuals are added in that case.
- Spawning state for all enemies: 0.8 s, no movement, no action, no damage to the player, no damage or flinch from the player. Then Chase.
- Spitter projectile: 4.0 tiles/s, 1 heart, straight to the player's position at firing, vanishes on walls, passes through enemies. Flinch unchanged.
- `grub_charger`: Grub data (HP 2, room Grub speed) plus charge numbers, same controller, states Spawning, Chase, Windup 0.7 s, Charge, Recovery 0.8 s. Charge goes at 8.0 tiles/s in a direction fixed at Windup start, to 7.0 tiles or a wall; leftover distance converts to time carried into Recovery.
- Windup entry conditions: ≥1.5 s since Spawning ended; ≥2.5 s since the previous Recovery ended (the moment it returned to Chase, not the end of Charge; the 0.8 s Recovery is excluded; a charger that has never been through Recovery counts as satisfied; flinch does not reset); player distance 3.0–6.0 center to center; no other living `grub_charger` in Windup or Charge (derived by scanning enemies, no stored token). Earliest repeat: Charge end + 0.8 + 2.5 = +3.3 s. Update order for simultaneous eligibility is the existing enemy order.
- Contact resolution during Charge only, in one function: per-update swept overlap, first overlap per charge is the contact; already overlapping at charge start counts on the first Charge update. The invulnerability query reads the flag as seen this update. Invulnerable gives "slipped through" (no damage), otherwise the existing damage routine applies 1 heart once and the result is "hit". The result stays for the rest of the charge; it resets to unresolved at Windup and Charge start. The visuals read it.
- Damage routine change: Spawning enemies ignore hits. A `grub_charger` in Windup, Charge or Recovery loses HP only, with no Flinch, knockback or state/direction/timer change. All other cases flinch 0.2 s. HP 0 kills immediately in any state.
- Visuals (stage 0 art, no reduced fallback): fade-in with a blue ring; ember ridge overlay on charge-type Grubs only; floor lane drawn below characters and projectiles, self-lit, clipped to 7 tiles or the wall using the charge collision test, width from the enemy contact width value; body squash/stretch is render-only; afterimages every 0.5 tiles; one new particle type (afterimage, dust, steam, sparks); white hit flash 0.1 s; crack overlay at HP 1; pale ring at the player for 0.15 s on "slipped through". No audio.
- Dev build only: room select 1–5, per-room charge switch, 30/60 FPS toggle, and a state transition log (including the wave all-fading-in moment, each `grub_charger`'s Recovery end time, and the corner chosen by the far-corner rule). No new player inputs.

Open assumptions (unconfirmed): contact shape and size of enemies; slot coordinates; whether other enemy timers (bite interval) use delta; room end condition coupling to wave spawning; lane/projectile/lantern color similarity.
