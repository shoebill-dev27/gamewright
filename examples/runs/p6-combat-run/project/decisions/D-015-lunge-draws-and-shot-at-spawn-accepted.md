---
kind: decision
id: D-015
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-015: Accept lunge draws with the Strike-start hit word, and accept the spit shot sharing the spitter's cell at spawn

## Decision

1. **Lunge draws.** The draw made at the moment of a grub hit may show the grub already lunged into a cell nearer than the one named in the hit line. This is accepted. The hit line names the position fixed at Strike start (D-014), which is the position the player was shown in the telegraph. The hit line is excluded from V-18's word-versus-picture comparison, and its own check is V-14. The same event may fall in different cells at 30 and 60 FPS in this draw only, because the draw happens at a different point of a 0.15 s lunge. Resting positions, "rears back" lines, "is open" lines and the `on you:` line stay under V-16 and V-18 unchanged.
2. **Shot at spawn.** In the draw made at "spitter (...) spits", the projectile starts in the spitter's own cell, and the spitter glyph (already lowercase `s`, Recovery) is drawn there. No `*` is visible in that one draw. This is accepted. The `*` is required from the first draw after spawn until removal. No cell is added and no glyph changes.
3. Wording is in `design/combat-visuals-verify-rulings.md`. No rule, number, input, timing or build change is needed.

## Rationale

- The lunge draw is a moving state, not a resting one. The cell shown is on the line from the telegraphed cell to the player, so the glyph moves toward the player and never to a side the player was not shown. The hit line repeats the word the player already read in "rears back" and saw as the `G`. Pillar 3 holds, because the threat was visible before it could hurt. A one-cell difference during 0.15 s does not mislead.
- Freezing the drawn cell of a striking grub was rejected in D-014 as a display lie of up to 1 tile. Nothing in the captures changes that.
- The shot at spawn is never the first warning. The spitter glyph is `S` for the whole 0.8 s charge, the charge line prints at its start, and the "spits" line prints at the spawn. The draw one frame later (0.2 s at 3 tiles/s) shows the `*` clear of the spitter. Showing the `*` in the spawn draw would mean giving up the spitter glyph or adding a second mark per cell. That costs more than it gains.

## Alternatives considered

- **Draw the strike at the Strike-start cell until the hit:** rejected, see D-014.
- **Make the hit line use the lunged cell's word:** rejected. It differs between 30 and 60 FPS, which is the defect D-014 removed.
- **Print `*` over the spitter at spawn:** rejected. It hides the state change `S` to `s`, which is the cue that the shot has left.
- **Offset the spawn `*` by one cell toward the target:** rejected. It is a position the shot does not have, and it breaks word-matches-picture for any line naming the spitter.

## Revisit when

- A playtest shows a tester misreading which grub hit them because of a lunged draw, or a tester says a shot "came from nowhere".
- A color or two-cells-per-tile view makes a second mark on the spitter's cell possible.
- Spitters or shots change speed or range (Option B), so the first draw after spawn could come after the hit.
