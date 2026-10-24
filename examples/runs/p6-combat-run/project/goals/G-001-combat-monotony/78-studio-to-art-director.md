---
kind: handoff
goal: G-001
seq: 78
from: studio
to: art-director
stage: Verify (visuals, from QA's verbatim captures)
outcome: routed
---
# 78: studio → art-director — Visual review of V-9…V-18 from QA's verbatim captures (build cf0f0ee63752)

## Task

Review what the player sees in the D-014 rebuild against V-1…V-18 in `design/combat-visuals.md` and the art direction. Use the verbatim player-view captures in Appendices A and B of `77-qa-to-studio.md` (30 and 60 FPS) as your material. Address the result to `studio`.

## Context

G-001 (combat feels monotonous), Option A. Verify 13f (77, QA) found no failing criterion in the rebuild at 30 and 60 FPS. Report 71 was a question because you could not run the build, and V-15 failed there on the document. The visual review was deferred to these captures. Do not hand back "no live view" again: the captures are the live material for this round. For anything the text view cannot show (colour, the reverse-video cell, V-6), say "not assessable from captures" per item and continue.

## Findings

- QA's captures cover the six setups from 71: grub on the player's tile then attack; grub on the tile plus one to its right; left/right grubs with one striking first; a spit shot hit; room 2 with four grubs to the down screen; the two misses. Appendix B has the edge case (player 14.5, grub on the player's tile, knockback) and the left-neighbour case.
- QA reports V-9, V-10, V-11, V-12, V-13, V-14, V-16 and V-18 as observed passing at both rates. V-15 is not checkable because the manual text is not placed yet (Owner step). V-6 is not assessable in a text view. V-17 was not re-observed.
- Two QA observations need your judgement (77 §5):
  1. **Lunge draws and the hit-line word.** In room 2 the draw made at the moment of a hit shows the lunged grub. At 30 FPS 4.300 the `G` is right of `P` while the line says "(top right)". At 60 FPS 4.283 the `G` is drawn top right. At 3.300 / 3.283 `G` is left of `P` while the line says "(top left)". D-014 and V-14 allow it (the hit line names the Wind-up position; draws during the Strike are not compared). Decide whether this reads acceptably to a player, and whether the same event drawn in different cells at the two rates matters.
  3. **Shot at spawn.** In the draw at "spitter (right) spits" (1.800 / 4.300) no `*` is visible because the spitter glyph covers it. The first `*` shows in the next draw. The glyph table says the projectile is visible from spawn. Decide whether the spec is met or needs a change.
- Not seen by QA in play: `z/Z` glyphs, defeat and dash-off draws (V-17), colour.

## Decisions already made

- D-001 (one-button combat), D-011, D-012, D-013, D-014 (cells, sides, "on you", hit-line word).

## Constraints

- You decide visual readability and consistency within the art direction. You do not change numbers, inputs or the rules of D-014. If a change is needed, hand it back as a design question or a spec change within visuals.
- Do not edit the repo or `manual.md`.

## Open questions

- Items 1 and 3 above (accept, or specify a change).
- Any V-item that you find failing from the captures: cite the capture and time.

## Expected output

A handoff to `studio` (outcome `pass` or `fail`, or `question` only for input that is truly missing and that captures cannot supply). Give a per-item verdict for V-9…V-18 and the two observations, and mark what is not assessable.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, design/combat-visuals.md, design/combat.md, manual.md
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/77-qa-to-studio.md (Appendices A and B are the captures)
