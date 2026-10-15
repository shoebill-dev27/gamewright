---
kind: decision
id: D-012
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-012: Mark an enemy on the player's tile with an `on you:` line, and name the attacker's position in hit lines

## Decision

1. D-006 stands. An enemy sharing the player's tile is still drawn in the nearest free cell beside the player, and it is still never hidden.
2. When any enemy is on the player's tile, an `on you:` line under the hearts line names each one (glyph, state, and the cell it is drawn in). The line is absent when nobody is on the tile. In a color view the displaced glyph's cell is also reverse-video as a reinforcement.
3. Hit lines name the attacker and its position at the moment of the hit ("YOU ARE HIT by a grub (left)"). Position words are shared with the telegraph lines. A distance is added only where two enemies of the same type would otherwise get identical words.
4. Details and acceptance criteria are `design/combat-visuals.md` (V-9 to V-17).

## Rationale

- Two playtesters in two sessions could not tell which side a bite would come from or which grub hit them (G-001, handoff 57). Pillar 3 asks that threats be readable.
- A one-cell-per-tile text view has no room for a second mark on the same tile, so the clarity has to come from a text line. Principle 1 already allows state to be carried in text.
- It changes only display. No rule, timing or parameter changes. It reuses the existing glyphs, the "(on you)" wording and the position words, so the praised lines stay as they are.
- It does not depend on the designer's pending swipe rule. The line reports position and state, not what a swipe will hit.

## Alternatives considered

- **Change the glyph on overlap (a separate "overlap" glyph or marker character):** rejected. It drops the enemy's case-coded state, which is the reading players praised, and D-006 rejected a similar idea.
- **Replace `P` while an enemy is on the tile:** rejected in D-006. The player would vanish from the map.
- **Rely on reverse-video or color only:** rejected. Principle 1 forbids meaning that depends on color alone, and it cannot be verified from the text view.
- **Make the map wider (two cells per tile) to show the overlap side by side:** rejected for now. It reflows the room and the tests, and it is not a small change for a small team.
- **Only add "(on you)" to hit lines:** rejected. It does not help when the enemy is beside the player in the picture, which was the reported confusion.

## Revisit when

- A playtest after the build shows the player still misreads the drawn side, or the `on you:` line is not read.
- Overlap becomes frequent enough (Option B, movement changes, or the designer's swipe rule) that the line is on screen most of the time and adds noise.
- The view moves beyond text and glyphs, so a real overlap marker on the tile becomes possible.
