---
kind: handoff
goal: G-001
seq: 60
from: art-director
to: studio
stage: Build
outcome: done
---
# 60: art-director → studio — Visual spec for "on you" and "which grub hit you" (V-9 to V-17)

## Task

Route the visual spec in `design/combat-visuals.md` (new items V-9 to V-17) to Build with the designer's spec change from 56, then to Verify. The display must show when a grub is on the player's tile and which grub dealt a hit.

## Context

G-001 (combat monotony), Option A. Two playtesters in two sessions reported the same two confusions (from 57 and the report in 54):
- A grub on the player's tile ("the grub is open (on you)") is drawn beside the player (D-006), and the player could not tell which side the bite would come from or where to swing.
- "YOU ARE HIT by a grub" does not say which grub when several are around. Rooms 1 and 2 often have two to four close together.

The capital and lowercase marks and the "rears back (left)" lines were praised. They are kept unchanged.

## Findings

What the spec adds (all display and text; no rule, timing or parameter changed):

1. **`on you:` line** under the hearts, present only while an enemy shares the player's tile. It lists each such enemy with its glyph, a state word (`walking`, `biting soon`, `open`, `charging`, `idle`) and the cell it is drawn in, for example `on you: G biting soon (shown right)`. It answers the first open question: the displaced glyph is marked by text, and a reverse-video cell reinforces it in a color view. No glyph changes.
2. **Position in hit lines**: `YOU ARE HIT by a grub (left)`, `... (on you)`, or `... by a spit shot from spitter (top right)`. It answers the second open question. It uses the same position words as the existing lines. A distance in tiles is added only when two enemies of the same type would get identical words.
3. **Same position words for the "is open" line**: "the grub is open (left)", "(on you)".
4. **Order and timing**: no new draws beyond the existing principle 4; the on-you line and the hit position come from the state of the draw that prints them. They hold at 30 and 60 FPS.
5. **D-012** records the choice. D-006 is not reversed.

The spec's wording makes no claim about which enemies a swipe hits, so it stays valid whatever swipe rule 56 settles. Only the swipe result lines depend on that rule, and this spec leaves them unchanged.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; display offset only. Stands.
- D-012: `on you:` line and attacker position in hit lines (new, art-director).

## Constraints

- Visual and text changes only. If Build finds that naming the attacker needs a rule or timing change, hand back to `game-designer`.
- `manual.md` is not written by the art-director or by Build. The Owner places manual text (D-005, D-007 pattern); the Studio routes the V-15 text (`manual.md#on-screen`, `manual.md#what-you-hear-and-read`) to the Owner (62). (Corrected by the Studio at Route; the original said Build updates `manual.md`.)
- Art direction: orange/red only for telegraphed glyphs and projectiles. The on-you line text and the hit lines are lantern-colored, not orange/red. Only the glyph letter inside the on-you line uses its glyph color.

## Open questions

- **For Build:** Does the hit event know which grub dealt the damage, and where it was when the hit landed? V-13 and V-14 need that. If it is only known in the trace and not in the player-view event, say so; it is a Build question, not a rule change.
- **For Build:** Can the player view print one extra line under the hearts and give a displaced cell inverse video? If a plain view cannot, the line alone still meets V-9 to V-11.
- **For `game-designer` (informational):** the swipe rule in 56 should be reflected in the swipe result lines only. If a swipe that hits an on-tile grub should print "(on you)" in its line, the designer should say so; the visual spec does not require it.
- **For `qa`:** The possibly short bite warning at 11.90 s to 11.97 s in report 54 is not a visual issue. The new hit lines will help trace which grub it was.

## Expected output

- Build: implement V-9 to V-17 in the player view with the designer's spec. `manual.md` is placed by the Owner, not by Build.
- Verify (`qa`): check V-9 to V-17 by scripted sessions in the practice room, for example `player 8 4` with `spawn grub 8 4`, and a grub on the left and right with only one striking, at both `fps 30` and `fps 60`.
- Review: the experience signals at the end of the "Experience signals" section in `design/combat-visuals.md`. A visual review of the built view is still needed for the real colors.

## Sender assessment

I am fairly confident in the text-line approach. It is cheap, testable from the plain view and independent of the swipe rule. The least certain parts are whether a single `on you:` line stays readable with three or more enemies on the tile, and whether the hit event can name the attacker. Both are listed as open and are cheap to settle in Build.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-visuals.md, design/combat.md, manual.md, the build `repo/`
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/57-studio-to-art-director.md
