---
kind: handoff
goal: G-002
seq: 10
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 10: studio → gameplay-engineer — fix criterion 44 and apply D-005 (picture and mark legibility)

## Task

Edit `repo/src/page.js` and `repo/src/pictures.js` to apply Decision D-005 in full. This includes the dark backing behind the reach letters, which fixes the QA failure on criterion 44. Run `node --test` and report to `studio`.

## Context

Goal G-002 (a picture for each kind of thing on the floor grid). The first build (sha ed0ad983accb, 69/69 tests) went through two parallel checks:

- QA (08): criterion 44 **fails**. `design/entity-pictures.md` section 5 requires a dark backing behind the reach letter, and `page.js` draws the letters (`#ffd070`, 10 px) with none. QA could not check the other visual criteria because it had no viewer.
- Art Director (09): judged from the code only and accepted **D-005**. It requires TILE 28, explicit badge fonts, dark chips behind the threat `!` badge, the stun/stagger badge and the reach letters, a night outline on the player, a lighter shade violet and a thicker Gloom ring. It also checked the remembered wall/floor contrast (item 7). The details and exact values are in D-005. It is the authority for this step.

This is the first failure of criterion 44, so it goes back to Build, not to Plan.

## Findings

Points from the two reports that the engineer needs:

- QA R2: the threat `!` badge is centered on the creature tile's top edge (`cr.y - 0.55` tiles, 16 px font). Half of it lies on the tile above and is clipped in row 0. D-005 items 2 and 3 address this.
- QA R1 / Art Director: the player body is the same blue as `<`, and the player flame is the same gold as the lit-brazier flame. D-005 item 5 (outline, `grow` flame parameter) addresses this.
- The Art Director could not read the board width (`v.w`). The board at TILE 28 plus the 360 px panel must fit a 1280 px window. If it does not, use TILE 26 (D-005's fallback) and say which TILE you used.
- The Art Director expects reach marks inside a Gloom area or hound line to possibly merge with the 3 px red border. Do not change this now. Screenshots will decide.

## Decisions already made

- D-002: threat marks plus reach marks. Their meaning and tile sets do not change.
- D-003: flat dark-cave style, marks always drawn over pictures.
- D-004: pictures drawn by code, pure `scene.js` mapping.
- D-005: tile size, badge fonts, dark chips, player outline, shade violet, Gloom ring.

## Constraints

- Do not touch `scene.js`, the rules, `textview.js`, `script.js`, `play.js` or the mark logic. `scene.js` must stay pure and must not read `threat` or `reach`.
- No rule, content, dependency, network or asset change. The palette stays at 12 colors at most, with no red or orange main fill. The page must still open from the file system.
- The text player output must stay byte-identical. The golden hashes in `repo/tests/golden/hashes.json` must not change. Do not regenerate them to make a test pass.
- The existing tests (the picture tests, the marks tests for criteria 42 to 46 and the golden test) must pass. Adjust a picture test only where D-005 deliberately changes the value it checks (for example the TILE size), and say which one you changed and why.
- If D-005 conflicts with the spec or with a tested criterion, stop and hand back with the conflict. Do not decide the look yourself.

## Open questions

None for the engineer. The Studio sends the results of the screenshots to the Art Director and QA later.

## Expected output

Build notes in the handoff template, addressed to `studio` (`to: studio`), so that the next Verify steps get fresh Handoffs. They list:

- the files changed, and how each D-005 item (1 to 7) was applied, or why one was not applied;
- which TILE was used (28 or 26) and why;
- the `node --test` result with counts, with the golden test unchanged;
- anything the Art Director or QA should look at in screenshots.

The notes are not a verification verdict.

## Sender assessment

Studio routing note: this step is the first return to Build for criterion 44. The next step is Verify in parallel, with screenshots (QA and Art Director). Budget is tight: 13 planned in total, 10 used after this Route.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, repo/src/scene.js, repo/index.html, repo/tests/pictures.test.js, repo/tests/golden.test.js, repo/tests/golden/hashes.json, project.md#constraints
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/09-art-director-to-studio.md (also read goals/G-002-entity-pictures/08-qa-to-studio.md for the criterion 44 failure)
