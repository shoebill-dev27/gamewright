# Combat design (build 0.3, frame-rate rule added for G-001)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

## Protection expiry and frame rate (G-001, criterion 6; D-002)

Intent: the player should never be hurt at a moment the rules say they are safe, and the game
should behave the same at 30 and 60 FPS in every way the player can notice.

Applies to both protection end times: the end of a dash (0.25 s after it starts) and the 0.8 s
post-hit mark. It applies equally to Grub contact and Spitter projectiles.

Rule:
- **Never early.** A contact at any moment before a protection end time never hurts, at either
  frame rate.
- **Late by at most one frame.** Protection may continue past its end time by less than one frame
  at the running frame rate: under 34 ms at 30 FPS, under 17 ms at 60 FPS. The error always favors
  the player.
- **Not late beyond that.** A contact more than one frame after the end time hurts normally, at
  both frame rates.
- A contact inside that single trailing frame may be harmless at one frame rate and hurt at the
  other. This is accepted and is not a difference under "same results at 30 and 60 FPS".

All other rules (damage, hit-stun, dash distance, duration, cooldown, queued attack) must give the
same results at 30 and 60 FPS with no tolerance.

Acceptance criterion for QA (criterion 6), at both 30 and 60 FPS, for the dash end and the 0.8 s
mark, for Grub and Spitter:
1. Contact at or before the end time: no damage.
2. Contact later than the end time plus one frame (34 ms at 30 FPS, 17 ms at 60 FPS): 1 heart of
   damage.
3. Contact between those two moments: either result passes.
4. No other difference between the two frame rates in damage, dash or hit-stun results.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

## Rooms

5 rooms, 3–6 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
