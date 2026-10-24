---
kind: decision
id: D-014
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-014: One rule for cells, sides, "on you" and the hit-line word

## Decision

All of these come from true positions by one rule, written in `design/combat.md` ("Cells, sides and 'on you'") and used by the draw, the text lines, the `on you:` line, the hit line and the knockback:

1. **Cell at .5:** `cell(v) = floor(v + 0.5 + 0.005)`. An exact .5 (or within 0.005 below it) goes to the larger index (right, down). No banker's rounding, no raw float compare. The player is drawn in `cell(player)`.
2. **On you:** the enemy is within 0.5 tile of the player by true position (the body-hit radius, same test as the swipe). Not cell equality, and not the 0.05 tile used before for the text and knockback.
3. **Position word of an enemy not on you:** the side of `P` on which its glyph is drawn (cell offset; if it shares the player's cell but is farther than 0.5 tile, the side of its true offset). An on-you enemy reads "on you" in every line, has an entry in the `on you:` line, and is drawn in a free straight neighbour cell inside the room.
4. **Hit-line word for a grub:** the position word fixed at the instant its Strike began (the end of Wind-up), not the lunge position at the damage tick. For a still player this equals its "rears back" word and the place of its `G` in the Wind-up start draw.
5. **Knockback of an on-you grub:** toward the side it is drawn on, ending 1.0 tile from the player's true position on that side. The display side may only be an in-room cell, so a grub on a player at the edge (player 14.5) is drawn and knocked left.
6. Criteria: AC-17, AC-28 reworded; AC-29, AC-30 new in `design/combat.md`; V-10, V-12, V-14, V-16 reworded and V-18 new in `design/combat-visuals.md`.

Limits: no timing, damage, hit test, cap or spacing value changes. The spitter hit line keeps its wording (position when the shot lands). Colors and glyphs are untouched. It does not decide the manual text.

## Rationale

- QA found the same cause three times: the display and the text lines took a position from different places (rounding at a boundary, cell equality versus distance, lunge tick). The picture and the text must never contradict (pillar 3), so one definition feeds all of them.
- Round-half-to-larger with a small tolerance gives the same cell for a resting position at 30 and 60 FPS, because the tolerance is far larger than float noise and far smaller than a frame of movement.
- "On you" at 0.5 tile matches the swipe's body-hit radius. The playtest promise (A3) is that a grub "on you" can always be hit; a cell-based definition could call a grub 0.9 tile behind "on you" and then let the swipe miss it.
- The strike-start position is a fact fixed by the Wind-up: the grub stands still during it and the player saw it. The lunge position at the damage tick depends on which frame the damage lands in, so it cannot be the same at both rates.
- Reusing the display side for the knockback (D-013) keeps its promise that the grub steps out where it was shown, including the edge case that failed (player 14.5).

## Alternatives considered

- **Relative rounding (round the offset, ties away from the player):** rejected. At the room edge it can place a glyph outside the room (player 14.5, grub 15.0) or in the player's own cell.
- **Round half to even / leave to the build:** rejected. That is the cause of D-A.
- **"On you" = same drawn cell:** rejected. It makes the word depend on the player's absolute rounding, and a grub that a swipe can miss would be called "on you".
- **"On you" = 0.05 tile (the old text/knockback value):** rejected. A grub 0.2 tile away would show a side word and be drawn displaced, with no hint in the text, which was the original confusion D-012 fixed.
- **Hit word from the damage tick (as built):** rejected, it differs between 30 and 60 FPS. **Hit word from the last draw the player saw:** rejected, draws are every 0.5 s plus events, so that position depends on timing as well.
- **Freeze the drawn cell of a striking grub at its Strike-start cell:** rejected for now. It is a display lie of up to 1 tile for 0.15 s and a new rule; the art-director can reopen it at Verify if a lunged draw reads badly.
- **Knock an on-you grub straight away from the true offset:** rejected for offsets of 0.05–0.5 tile. It could land on the side opposite the drawn glyph (D-013).

## Revisit when

- A playtest or the art-director's review shows that a draw taken during the Strike, with the grub in a nearer cell than the hit line names, confuses players.
- Overlap or movement rules change (Option B), or the view gets two cells per tile.
- The tolerance of 0.005 tile ever lets two different resting positions share a cell at one rate and not the other.
