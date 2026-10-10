# Enemy telegraphs and new enemies

Written in G-002 (step 5) under D-002. Extends `design/combat.md`; build 0.4.

## Intent

Make each room ask the player a different question — where to stand, when to dash, which enemy
first — through enemy behavior, keeping one-button combat (D-001, D-002).

## Telegraph rule

- Every ranged or charging enemy attack is preceded by a telegraph: the enemy glows threat-orange
  and holds a wind-up pose for the telegraph duration.
- Durations: Spitter 0.5 s, Charger 0.5 s, Shieldbearer 0.6 s.
- The Grub keeps its contact bite without a telegraph; it is the baseline pressure enemy.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Unchanged. |
| Spitter | 2 | Unchanged, except each shot is preceded by a 0.5 s telegraph. |
| Charger (new) | 3 | Approaches to within 5 tiles. Telegraphs 0.5 s; the lunge direction is locked at the start of the telegraph. Lunges 6 tiles in 0.3 s; 1 damage on contact during the lunge. Then 1.0 s recovery in place: no movement, no attack. |
| Shieldbearer (new) | 4 | Walks toward the player at 60% of Grub speed, turning to face the player at 90°/s. Its shield blocks player attacks arriving within its front 120° arc (block spark, no damage). Attack: telegraph 0.6 s, then a 1-tile shield bash forward, 1 damage. |

## Rooms (build 0.4)

| Room | Enemies | Question it asks |
|---|---|---|
| 1 | 4 Grubs | spacing (baseline) |
| 2 | 2 Grubs, 2 Spitters | keep moving while attacking |
| 3 | 2 Chargers, 1 Grub | read the telegraph; dash through or aside |
| 4 | 2 Shieldbearers, 2 Grubs | flank; choose a target order |
| 5 | 1 Shieldbearer, 2 Chargers, 1 Spitter | combine everything |

## Acceptance criteria — verification (QA)

- **V1** Each telegraph lasts its specified duration (±1 frame) at 30 and 60 FPS; the attack starts
  immediately after.
- **V2** The Charger's lunge direction is locked at telegraph start; player movement during the
  telegraph does not change it.
- **V3** Charger lunge: 6 tiles in 0.3 s; 1 damage on contact during the lunge only; then 1.0 s with
  no movement or attack.
- **V4** Player attacks arriving within a Shieldbearer's front 120° arc deal no damage and show the
  block spark; attacks from outside the arc deal damage.
- **V5** Shieldbearer turn rate is 90°/s.
- **V6** Dash invulnerability protects against lunges and bashes (G-001 behavior intact).
- **V7** Room compositions match the table.

## Acceptance criteria — experience (Review only; never given to the Playtester)

- **E1** In rooms 3–5 the player uses the dash to avoid attacks, not only to travel.
- **E2** The player describes rooms as asking for different things.
- **E3** No single strategy (e.g., back into a corner and swipe) clears every room.

## Open questions

None known.

## Edge cases (added in G-002 step 8)

- **Hits during a telegraph or attack** deal damage but do not interrupt it (D-003). Enemies flinch
  for 0.2 s only when hit outside a telegraph or attack. (The flinch existed in build 0.3 but was
  undocumented; it is now part of this spec.)
- **Charger lunge into a wall:** the lunge stops at the wall; the 1.0 s recovery starts there.
- **V8** Hitting an enemy during its telegraph deals damage and does not delay or cancel the attack;
  hitting it outside a telegraph or attack makes it flinch for 0.2 s.
- **V9** A Charger lunging at a wall stops at the wall and recovers for 1.0 s.
