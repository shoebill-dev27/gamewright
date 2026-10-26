---
kind: handoff
goal: G-002
seq: 13
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 13: studio → art-director — final visual review of the pictures after D-005 was applied

## Task

Review what the player sees on the browser page, using real screenshots, against your spec `design/entity-pictures.md` (criteria 31 to 46) and D-005. Give a visual verdict per criterion, and say whether the pictures read clearly and fit the cave and ember mood.

## Context

Goal G-002 gives each kind of thing on the floor grid its own picture. Your first review (09) could not confirm the visuals without screenshots, and you issued D-005. The build now follows D-005: tile 28 px, dark chips behind badges and reach letters, a player outline, brighter shade violet, and a ringed Gloom disc. QA verifies the criteria in parallel; the Studio combines both results.

## Findings

Points that the build's author left for your eye (not verdicts):

- Does the board plus the 360 px side panel fit a 1280 px window? If not, say whether tile 26 is your fallback (one constant, `TILE` in `repo/src/page.js`).
- Reach letters on salve, lit brazier and stairs tiles, and with 2 or 3 letters: does the dark backing cover the dashed border?
- Reach tile inside a Gloom area or hound line: do the 2 px dashes and the 3 px red border merge?
- The threat chip sits at the top-left of a creature tile. Does it hide a key feature (shade head, moth antenna)? Check row 0 and next to other marked tiles.
- Stunned and staggered chips on the wash.
- Player on `<`, on a lit brazier and on plain floor: does the outline separate it?
- Shade and Gloom against the floor; remembered wall against remembered floor; flame steps at r = 6 and r = 2 with the outline; whether the dim palette factor 0.55 needs 0.65.

## Decisions already made

- D-003 (style, layering), D-004 (pictures drawn by code), D-005 (your tile size and chips).

## Constraints

- You decide visual matters within the vision (`art-director` authority). If a change is needed, name the exact constants or items; a small change is for the next Build, not for you to edit.
- Do not edit files in `repo/`. If a screenshot cannot be taken with your means, say so plainly and state which verdicts remain unverified.
- Rules, balance and the text player are out of scope.

## Open questions

None.

## Expected output

A visual-review report with a verdict per criterion 31 to 46, a list of required changes if any, and whether the Goal's visual intent is met. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/entity-pictures.md, repo/index.html, repo/src/page.js, repo/src/pictures.js, repo/manual.md, the build in repo/
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/09-art-director-to-studio.md
