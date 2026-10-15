---
kind: decision
id: D-013
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-013: A grub on the player's tile is knocked back toward the side it is drawn on

## Decision

1. The first hit (HP 2→1) knocks a grub back 1 tile over 0.2 s. If its true position is 0.05 tile or more from the player's, the direction is straight away from the player. If it is on the player's tile, the direction is its display side from D-006 (the side it last approached or struck from, otherwise right, left, above, below), so it ends in the cell where it was already drawn.
2. If that side has less than 1 tile of clear room, the next side in the order right, left, above, below that has 1 clear tile is used. A knockback away from the player toward an edge is clamped at the edge, as a dash is.
3. A grub knocked back from distance 0 ends about 1.0 tile away, inside the 1.5-tile zone, and keeps its engagement slot. No state or timer changes.
4. Q2: the swipe result line is unchanged for an on-tile grub ("you swipe: grub hit (1 left)"). The position is read from the `on you:` line.
5. Acceptance: AC-28 in `design/combat.md`. V-17 in `design/combat-visuals.md` is unchanged and still applies.

## Rationale

- The display side is already stored and already what the player sees (D-006, D-012). The grub steps out to the cell it was shown in, so nothing jumps to a side the player was not told about.
- It is defined in every case, needs no new input, and reuses what exists (D-001, small team).
- The `on you:` line and the picture stay consistent after the hit: the entry goes away when the grub lands.
- Keeping the slot is the honest result of a 1-tile knockback from distance 0. It does not weaken the cap or the turns rule, and the grub that was on the player is still the nearest one to be countered.

## Alternatives considered

- **Along the player's facing:** rejected. Always defined, but the grub can jump to the side opposite its drawn cell, and a player who dashed or turned sees it land where nothing pointed. It also pushes the grub into the player's facing line, where its next bite becomes easier to stay in front of by accident.
- **Fixed direction (right, falling back to left):** rejected. Arbitrary to the player, and it contradicts the displayed side.
- **No knockback at distance 0:** rejected. It breaks "the first hit knocks back" for the case A3 makes common, and the grub would stay on the player and stay hard to read.
- **Knock it far enough to free a slot (1.5 tiles or more):** rejected. It would reward an on-you grub with a free escape from the cap, which changes the cap's tuned play, and needs a new distance.
- **Push the other way when blocked, instead of clamping:** adopted only for the on-tile case. For a grub that is not on the tile, clamping matches the dash and needs no new rule.

## Revisit when

- The retest shows testers misreading where the grub lands, or an on-tile grub that stays near the player too long, so the slot it keeps feels like a wall.
- The overlap display rule (D-006) or the `on you:` line (D-012) changes.
- Option B opens movement or collision changes for grubs.
