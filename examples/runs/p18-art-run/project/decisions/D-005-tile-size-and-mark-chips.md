---
kind: decision
id: D-005
status: accepted
decided_by: art-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast

## Decision

All of this is visual direction. No rule, mark meaning, mark position (which tiles) or text output changes.

1. **Tile size.** `TILE` goes from 22 to 28 in `repo/src/page.js`. The picture inset stays 4 px, because `pictures.js` takes `max(round(0.1*size), BORDER+1)`, which is 4 at 28. The picture is then 20 px, so one design unit is 1.25 px instead of 0.875 px. The 3 px threat border keeps 1 px of gap to the picture. If the board plus the 360 px panel is too wide for the Owner's screen, 26 is acceptable (unit 1.125 px). The panel already wraps below the board via flex-wrap. The click mapping uses `TILE`, so it follows.
2. **Fonts.** `render()` sets the base font to `TILE-6` px bold (22 px at 28). That is far too big for the `!` badge. Set explicit fonts: the `!` and the `z`/`~` badges use bold 10 px, the reach letters bold 10 px.
3. **Badges on a dark chip, inside the tile.** The threat `!` is no longer centered on the top tile edge (that put half of it on the tile above and red on red against the border).
   - It is drawn after the creature picture, as a chip in the top-left corner inside the 3 px border: rect at (x*TILE+3, y*TILE+3), 8 px wide, 11 px tall, fill `#150f22` at alpha 0.9, `!` in `#ff4040` centered in it.
   - The stunned/staggered badge uses the same chip position and shape, with `z` or `~` in `#cfe6ff`.
   - A stunned or staggered creature is not a threat, so the two badges do not co-occur. If they could, the threat chip wins and the state chip goes bottom-left.
   - The wash keeps `rgba(150,200,255,0.45)` over the inner area, and still no red on it.
4. **Reach letters get the dark backing (spec section 5 is required).**
   - After the orange tint and dashed border, and before the letters, fill a rect centered on the tile: height 12 px, width = letter count * 6 + 4 px, capped at TILE-6. Fill `#150f22` at alpha 0.85.
   - Letters stay bold 10 px `#ffd070`. With 3 or more letters, use 9 px and a width of letter count * 5.5 + 4.
   - The backing must not cover the dashed border, which lies in the outer 3 px.
5. **Player outline.** The player's blue cloak sits on blue stairs-up, and the player's gold flame sits on the lit brazier's gold flame.
   - Before the player shapes, draw the same head, cloak and flame polygons in `night` grown by 1 design unit on every side. The flame takes a `grow` parameter on `h` and `w`.
   - This is the player picture only. It adds no color.
6. **Shade and Gloom contrast.** The shade (`violet #5b4d80`, luminance about 86 against a floor of about 44) and the Gloom ring (1 unit thick) are the weakest against the floor.
   - Change `violet` to `#7566a8` (12th palette slot not needed, same slot).
   - Reduce the Gloom's inner `night` disc from radius 6 to 5.5, so the ring is 1.5 units.
7. **Dim palette.** Keep the 0.55 factor for now. If a screenshot shows remembered wall and remembered floor merging, raise the factor from 0.55 to 0.65 in `dim()`.

## Rationale

- At 14 px, one design unit is 0.875 px. Sub-pixel features are the moth antennae (1 unit), the hound eye (1x1), the oil-flask highlight (1x3), the staff, and the gaps between stair bars. At 20 px they are 1.25 px and survive. Simplifying all of them would lose the ember-eye cue that the spec asks for.
- The reach letter sits at the tile center, where the salve's pale cross, the lit brazier's gold flame and the stair bars all have colors close to `#ffd070`. Without a backing the letter can vanish on exactly those tiles, which breaks pillar 1 (D-002) and check 44.
- The old `!` placement came from the pre-picture page. Over pictures it lands on the creature's head and on the neighbor tile.

## Alternatives considered

- Simplify the pictures and keep 22 px: loses detail the spec asks for and still leaves 3 px of margin per side. Rejected.
- Backing the letters with a light fill: clashes with the dark mood. Rejected.
- Tile 32: the board would be about 1090 px wide for a 34-column map, too wide with the panel. Held back.

## Revisit when

A screenshot at 28 px shows any picture still unreadable, the board does not fit, or marks are lost on a picture.
