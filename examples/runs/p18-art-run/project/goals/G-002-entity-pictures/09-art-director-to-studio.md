---
kind: handoff
goal: G-002
seq: 9
from: art-director
to: studio
stage: Route
outcome: partial
---
# 09: art-director → studio — visual review of the entity pictures: changes required (D-005), screenshots still needed

## Task

Route D-005 to the gameplay-engineer to apply. Then get screenshots of the page, and send them back to me for the final visual verdict.

## Context

Goal G-002. Handoff 07 asked for a visual review of the 14 pictures and the marks, and for answers to two open questions. This step could not see the page. It judged from the drawing code (`pictures.js`, `scene.js`, `page.js`) and the palette arithmetic only. A verdict is called "met" only for what the code proves. Everything visual is **unverified**, and the predictions below are code-based.

## Findings

**Basis.** The pictures are authored on 16x16 and drawn with inset 4 px at TILE 22, so the picture is 14 px and one design unit is 0.875 px. Marks are drawn after the pictures, in D-003 order.

**Answer to Q1: do the 14 pictures read at 14 px?**
- Not reliably. The silhouettes are fine, but several details fall under 1 px. Raise `TILE` to 28 (picture 20 px, unit 1.25 px) and do not simplify the silhouettes. D-005 item 1 has the details and a fallback of 26.

**Answer to Q2: is the dark backing for the reach letter required?**
- Yes. D-005 item 4 gives the exact backing.
- The letter is bold 10 px `#ffd070` at the tile center, over a 30% orange tint.
- At the center the pictures hold the salve's pale cross, the lit brazier's gold flame and the stair bars, all near the letter's color.

**Per picture** (readability at 14 px, predicted from the code; every visual verdict is unverified until seen):

| Picture | Verdict | Notes |
|---|---|---|
| Player | unverified, change required | Cloak is `blue`, the same as stairs-up, and the gold flame overlaps the lit brazier's gold flame (player on `<` or on a lit brazier, criterion 35). Add the night outline (D-005 item 5). The staff is 0.9 px wide, which is fine at 28. |
| Moth | unverified, likely readable | Wide pale X-wings are a strong silhouette. The 1-unit antennae are sub-pixel at 22, fine at 28. |
| Shade | unverified, change required | `violet` on the floor is low contrast (luminance about 86 against 44). Eyes are 1.3x1.75 px at 22. Lighten the violet (D-005 item 6). |
| Hound | unverified, likely readable | Body is wide and the legs are visible. The ember eye is 0.9 px at 22. Fine at 28. |
| Hound crouching | unverified, likely readable | The body is about 3 px lower than the standing one, so the pose difference exists at 22 and grows at 28. |
| Gloom | unverified, change required | `night` disc on a near-black floor, held only by a 0.9 px ring at 22. Thicken the ring to 1.5 units (D-005 item 6). Eyes are 1.75 px, fine. |
| Wall, floor | unverified | Intended low contrast. Full tone: wall `#54493c`, floor `#332b22`, a quiet and plausible difference. In dim tone the wall is about `#2c2926` against the floor at about `#1a1816`, only about 18 levels apart. Watch this in the screenshot (D-005 item 7). |
| Stairs up, down | unverified, likely readable | Blue ascending and green descending bars. The gaps between bars are 0.9 px at 22 and may blur into a wedge. Shape and color both differ, so it is acceptable. |
| Salve, oil flask | unverified, likely readable | Green square with a cross against a blue round flask with a gold stopper. Their luminances are close (about 146 and 154), but the shapes differ (greyscale test, criterion 33). The oil highlight (1 unit) is nearly invisible at 22. |
| Unlit, lit brazier | unverified, likely readable | The same bowl. The lit one adds a gold and pale flame, so shape and light both differ. |
| Flame steps | unverified | Heights grow about 1.2 px per step at 22, so adjacent steps may not be told apart. Large, medium and small (6-5, 4-3, 2) are very likely distinguishable, which the spec accepts as a fallback. |
| Remembered tone (all) | unverified | Math: gold dims to about `#776c4b`, green to about `#425a46`, still readable on the dim floor. Visible floor against remembered floor is about 25 levels apart, so check 39 is probably met but needs a look. |

**Per mark:**

| Mark | Verdict | Notes |
|---|---|---|
| Threat border, 3 px (creature, hound line, Gloom area) | unverified, likely readable | The 4 px picture inset leaves 1 px free of the border, so the border does not touch the pictures. Adjacent area tiles form a red grid (6 px lines with 1 px gap), which still reads as an area. |
| Area tint 35% (hound line, Gloom 3x3) | unverified, likely readable | Drawn under the creature and player pictures, which is correct. |
| Threat `!` badge on creatures | **not readable as built, change required** | Centered on the top tile edge at the 16 px base font (`TILE-6`). Half of it lies on the neighbor tile, and its lower half sits on the red border (red on red) and on the creature's head. In row 0 it is cut off. See D-005 items 2 and 3. |
| Reach mark (tint, dashed border, letters) | **not readable on some tiles, change required** | The dashed border is fine. The letters need the backing (Q2). Also, in D-002 and edge case 8 a reach tile can lie inside a Gloom area or hound line. Then the 2 px orange dashes sit over the inner 2 px of the 3 px red border and leave 1 px of red outside. Unverified. If the screenshot shows the two marks merging, QA reports it and I will specify an offset. |
| Stun/stagger wash and badge | unverified, change required | The `z`/`~` is `#cfe6ff` over the pale-blue wash, so light on light. Use the dark chip (D-005 item 3). The wash has no red, which is right. |

**Q2 and the open questions are answered above. Nothing here changes a rule, a mark's meaning, or a mark's tile set** (criterion 45 stays valid). The engineer must re-run the marks and golden tests after the edit.

**Criteria status for the visual ones** (31 to 46 that need eyes): 32, 34, 37 to 41, 44 and 46 stay **unverified**. 42 and 44 are expected to fail as built (badge and reach letter), per the table. Nothing is marked met. 47 to 49 are not my part.

## Decisions already made

- D-003 (style, layering) and D-004 (code-drawn pictures) followed.
- **D-005 (new, accepted)**: TILE 28, explicit badge fonts, dark chips for badges and reach letters, player outline, lighter shade violet and thicker Gloom ring.

## Constraints

- Visual direction only. No rule, content, dependency, network or asset change. Palette stays at 11 colors (12 allowed); no red or orange main fill is added.
- The page must open from the file system. `scene.js` must stay pure and must not read `threat` or `reach`.

## Open questions

1. For QA and the screenshots: the board width at 28 px depends on `v.w`, which I could not read. If the board plus the 360 px panel does not fit a 1280 px window, use TILE 26. Report which one was used.
2. Do the reach border and the red border merge on a tile that has both (see the mark table)? A screenshot decides.
3. Do remembered wall and remembered floor merge? A screenshot decides (D-005 item 7).

## Expected output

1. The Studio routes D-005 to **gameplay-engineer**. The engineer edits `repo/src/page.js` (TILE, fonts, chips, backing) and `repo/src/pictures.js` (player outline with a `grow` flame parameter, `violet`, Gloom ring), and runs `node --test`. The engineer should not touch `scene.js` or mark logic.
2. Then run **shot** screenshots of `index.html` with scripts that show: r=6 and r=2 (criterion 36); a remembered area; each of the four creatures; a hound crouch line and a Gloom 3x3 area; reach marks on an item tile, on a lit brazier tile and on a stairs tile; a stunned creature; the player on `<`, on a lit brazier and on a plain floor; the inventory with items; and a reach tile inside a threat area. Add a greyscale view if possible.
3. Send the screenshots back to **art-director** for the final visual verdict, covering criteria 31 to 46 (visual part).

## Load

- Role: none, because the recipient is the Studio (routing). The next Role is gameplay-engineer, then art-director.
- Skills: none
- Project: design/entity-pictures.md, repo/src/pictures.js, repo/src/scene.js, repo/src/page.js, repo/index.html
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/07-studio-to-art-director.md
