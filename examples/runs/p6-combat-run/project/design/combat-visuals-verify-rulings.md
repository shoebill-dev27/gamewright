# Combat visuals: rulings at Verify (G-001, build cf0f0ee63752)

Status: art-director rulings on `design/combat-visuals.md`, made from QA's verbatim captures (77, Appendices A and B). It changes no rule, number, input or timing and needs no build change. Where it differs from the wording in `combat-visuals.md`, this file applies. D-015 is the decision.

## 1. Draws made during a Strike (replaces the "Not checked" bullet on lunged draws)

- The draw made at the moment of a grub hit, and any other draw made inside the 0.15 s Strike, may show the grub in a cell nearer to `P` than the one named in the hit line. This reads acceptably and is intended.
- The hit line names the Strike-start position (D-014). The lunged glyph is on the path from that position toward the player and never on a side the player had not been shown.
- The same event may be drawn in different cells at 30 and 60 FPS in such a draw (room 2, 4.300 against 4.283). That is not a V-16 failure.
- Hit lines are excluded from the word comparison in V-18. V-14 is their check.

## 2. V-18 wording (replaces the V-18 sentence)

- **V-18** In every draw, the side word of every text line that names an enemy, except hit lines ("YOU ARE HIT by ..."), equals the side or corner of `P` on which that enemy's glyph is drawn in the same draw (for lines printed at that moment). The hit line's word is checked by V-14 and does not depend on the draw. An enemy exactly on a half-tile boundary is drawn in the same cell at 30 and 60 FPS (for instance a grub resting at x 13.5 with the player at x 14.5 is always drawn left of `P`).

## 3. Projectile visibility (replaces "Visible from spawn to removal" in the glyph table)

- `*`: visible from the first draw after the shot is spawned until removal. In the draw made at the spawn itself, the `*` shares the spitter's cell and the spitter glyph is shown there (lowercase `s`, Recovery). The "spits" line and the `s` mark the spawn. This is intended.
- The projectile still has to be saturated orange/red and the brightest mark on the map once visible. V-6 is unaffected.

## 4. Minor, not criteria

- When the `on you:` line appears or disappears, the room frame moves down or up by one line. This is acceptable in the text view. Revisit it if the view is ever drawn in place.
- The `on you:` line is not indented like the other lines. It is cosmetic.
