---
kind: handoff
goal: G-002
seq: 15
from: art-director
to: studio
stage: Verify
outcome: partial
---
# 15: art-director → studio — final visual review: only the plain-floor view could be seen; most verdicts stay unverified

## Task

Record this visual review. Decide whether another look is worth the cost (see Open questions). Pass the one suggested small change (dim factor) to the next Build, if the Studio agrees.

## Context

Goal G-002 (pictures for each thing on the floor grid). Handoff 13 asked for a verdict per criterion 31 to 46 from real screenshots. The `shot` tool gave one usable screenshot (round 2 of the first run). Round 1 failed because the key script `dddd` is not a valid key name; keys must be space-separated (`d d d d`). The usable screenshot is floor 1, turn 2, seed unknown, after `d d d d s s`. Each run yields one image taken after the last key. The page picks a random seed on load, and the tool cannot set a `#seed` hash. So I cannot reproduce or aim at a hound, the Gloom, a stunned creature, marks or two flame radii. I did not use the last run: it would give one more random frame and no way to reach those scenes.

## Findings

**What the screenshot shows (verified by sight).** Console errors: none (`console_errors: []`). The board is 28 columns by 16 rows at 28 px, so 784 x 448 px. The viewport was 1000 px wide, so the side panel wrapped below the board, as designed by the flex-wrap.

**Fit in 1280 px (arithmetic, not seen).** 12 margin + 786 board with border + 16 gap + 360 panel = about 1174 px, which is under 1280. TILE 28 should fit side by side, and the fallback 26 is not needed. This is not seen in a 1280 window.

**Per criterion (31 to 46):**

| # | Verdict | Evidence |
|---|---|---|
| 31 | unverified (partial) | Seen with their own picture: wall, floor, `<`, unlit brazier, the player. Not seen: moth, shade, hound, Gloom, lit brazier, salve, oil, `>`. |
| 32 | unverified | No creature on screen. Greyscale not available. |
| 33 | unverified | Only `<` and the unlit brazier were seen. |
| 34 | **pass** (wall vs floor; player vs floor) | Wall is light-grey brick, floor is dark brown speckle, clear at a glance. The player stands out from the plain floor. Item and creature standing-out unverified. |
| 35 | unverified (partial) | The player reads clearly on plain floor: pale head, blue cloak, gold flame with a dark outline. Not seen on `<` or on a lit brazier. |
| 36 | unverified | Only r=6 was seen (flame large and clear, with a pale core). No r=2 frame. |
| 37 | unverified | The inventory was empty in this frame (`[1] empty` and so on, with no picture, as required). Item pictures in the slots were not seen. |
| 38 | partial | Remembered brick wall at the left of the board keeps its shape and is clearly dimmer (pass). Remembered floor tiles (lower middle and left) are nearly black, and the speckle is not visible. This is only borderline "same shape, dimmer". No creature on a remembered tile, and unseen tiles are blank (pass). |
| 39 | unverified | The visible-floor edge against remembered floor looks clear in this frame (visible floor is brown, remembered is near-black). No frame at r=2. |
| 40 | unverified | Needs frames across an E threshold. |
| 41 | **pass** (as far as one frame shows) | Near-black background. The warmest, brightest spot is the player's flame. No lit brazier seen. |
| 42 | unverified | No threat border or chip seen. |
| 43 | unverified | No hound line or Gloom area seen. |
| 44 | unverified | No reach mark seen. |
| 45 | not mine | Tile-set equality is QA's check. |
| 46 | unverified | No stunned or staggered creature, no crouching hound seen. |

**Readability notes from the one frame:**
- `<` (blue rising bars) is clear and reads as steps at 28 px.
- Unlit brazier (grey bowl) is small but recognisable, and distinct from the floor.
- Player outline works on floor. Not tested on `<` or a lit brazier, where it matters most.
- D-005 item 7 (dim factor): remembered wall and remembered floor do not merge; the wall is clearly visible against the floor. The remembered floor, though, is close to black, and the speckle is lost. I suggest 0.65 (see Required changes).

**Open points from handoff 13 that this frame cannot answer:** reach letters on salve, lit brazier and stairs tiles; reach next to the Gloom area or hound line (dash versus red border merging); threat chip hiding the shade head or moth antenna, including row 0; stunned chips; flame at r=2; Shade and Gloom against floor; the player on `<` and on a lit brazier. All stay **unverified**.

**Visual intent met?** Not confirmed. What was seen fits the cave and ember mood (dark cave, one warm light, quiet terrain) and the pictures drawn so far read clearly. Nothing seen contradicts D-005. The marks, which carry pillar 1, were not seen at all, so I do not call the Goal's visual intent met.

**Required changes.** None are demanded by what was seen. One small change is recommended:
1. `repo/src/pictures.js`, `dim()`: change the factor `0.55` (the final `* 0.55`) to `0.65`. Reason: remembered floor is almost black. Check that visible floor is still clearly brighter than remembered floor (criterion 39). This changes no mark or rule. If QA finds the visible/remembered gap too small after the change, go back to 0.60.

## Decisions already made

- D-003 (style, layering), D-004 (pictures drawn by code), D-005 (TILE 28, chips, outline, violet, Gloom ring) all stand. No new decision.

## Constraints

- No edits to `repo/`. Visual matters only; rules, balance and the text player are out of scope.
- Only what a screenshot shows counts as verified. Nothing above is a pass from code reading alone.

## Open questions

1. How can the missing scenes be seen? With the available `shot` tool the seed is random, so scenes cannot be aimed at. Options for the Studio: (a) a Build step adds a way to start from a fixed seed or scenario from the page (for example honouring `#seed`, which `page.js` already supports, if the tool can open `index.html#<seed>`; this needs a tool that passes a URL hash, which the run line `screenshots of index.html` does not show); (b) QA, who can run the Node text player with a seed, picks a seed and a script that reach each scene, and the page is then opened with that seed; (c) the Owner looks at the page himself or herself for the marks and the creatures. I cannot decide which of these the means allow. Say plainly: with the means in this step, criteria 32, 33, 35 (on `<` and a lit brazier), 36 (r=2), 37, 40 and 42 to 44, 46 cannot be shown.
2. Does the Studio accept the Goal on the partial evidence, or hold G-002 until the mark scenes are seen? My recommendation: hold, because the marks are pillar 1 and the D-005 chips and backings were never seen working.

## Expected output

The Studio records this partial review. It then either (a) routes the dim-factor change to the gameplay-engineer and arranges a way to see the marked scenes (open question 1), then returns to art-director for a short final verdict on criteria 35, 36, 42 to 44 and 46, or (b) hands the open scenes to the Owner as a look-and-confirm item.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, the build in repo/
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/13-studio-to-art-director.md
