---
kind: handoff
goal: G-002
seq: 7
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 07: studio → art-director — visual review of the built entity pictures

## Task

Review what the player sees on the browser page against your spec `design/entity-pictures.md` and D-003. Judge readability and consistency: can each kind of thing be told apart at a glance, do the pictures fit the cave and ember mood, and do the threat and reach marks and the light levels stay readable over the pictures. Answer the two open questions below.

## Context

Goal G-002 (pictures for each kind of thing on the floor grid). Design and Plan are done, and the engineer has built the pictures per D-004 (code-drawn, 16x16 design grid, inset 4 px so 14 px in a 22 px tile). QA verifies the testable criteria in parallel. Nobody has yet seen the page. Tests only prove the mapping, palette size and text output.

## Findings

Facts about the build:

- 14 pictures (13 entities, the hound with 2 poses), 11-color palette (spec allows at most 12), no red or orange main fills.
- Marks as drawn: threat tile/area = red tint `rgba(255,40,40,0.35)` plus 3 px `#ff3030` border; creature threat = same border plus red `!` badge above the center; reach = `rgba(255,170,0,0.30)` tint, 2 px dashed `#ffb000` border, bold 10 px `#ffd070` creature letters at the tile center, with no dark backing; stunned/staggered = `rgba(150,200,255,0.45)` pale-blue wash plus badge `z` or `~` at top-left, no red.
- Remembered tiles use the dimmed tone and visible tiles the full tone. The flame has five growing steps for light radius 2 to 6.
- `TILE` is one constant in `repo/src/page.js` (22; also used for click mapping), so raising it (for example to 28) is a one-line change.

## Decisions already made

- D-003: flat dark-cave pictures, marks always drawn over pictures. D-004: pictures drawn by code.

## Constraints

- Your authority is visual direction within the vision. No rule or content change; no assets other than code-drawn pictures; no dependencies or network use; the page must open from the file system.
- If you have no means to see the page (no browser or screenshot), say so. You may then judge only from the drawing code and the palette. Mark any visual verdict you cannot give as unverified, not as met.

## Open questions

1. Do the 14 pictures read at 14 px? If not, should `TILE` be raised or the pictures simplified? State which pictures and what you would change.
2. Spec section 5 asks for a dark backing behind the reach-mark creature letter. It was not added. Is it required, and if so what exactly?

## Expected output

A visual-review report: per picture and per mark, readable / not readable / unverified, with required changes if any, and answers to the open questions. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/entity-pictures.md, repo/src/pictures.js, repo/src/scene.js, repo/src/page.js, repo/index.html
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
- Previous handoff: goals/G-002-entity-pictures/05-gameplay-engineer-to-studio.md
