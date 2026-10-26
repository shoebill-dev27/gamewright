---
kind: handoff
goal: G-002
seq: 6
from: studio
to: qa
stage: Verify
outcome: routed
---
# 06: studio → qa — verify the entity pictures build against criteria 31 to 49

## Task

Verify the built change against the acceptance criteria 31 to 49 in `design/entity-pictures.md`, and check for regressions in criteria 1 to 30. Report pass/fail per criterion. Mark a criterion "not checkable with my means" rather than pass when it needs a viewer you do not have.

## Context

Goal G-002: each kind of thing on the floor grid of the browser page gets its own picture (player and ember, creatures, braziers, items, terrain), with the threat and reach marks (D-002) and the ember-light visibility still readable. The change is in `repo/` (sha ed0ad983accb). It touches the browser page only; the text player (`node play.js`) must be byte-for-byte unchanged in output. No rule, balance or content change.

## Findings

Facts about the build, for exercising it (not a claim that it works):

- New modules: `repo/src/scene.js` (maps the view model to picture requests; pure) and `repo/src/pictures.js` (canvas drawing; 14 pictures, 11-color palette). Changed: `repo/index.html` (two script tags), `repo/src/page.js` (draw order, inventory icons, threat border), `repo/manual.md` (one paragraph).
- Not touched: `game.js`, `light.js`, `floorgen.js`, `rng.js`, `view.js`, `textview.js`, `play.js`, `script.js`.
- New tests: `tests/scene.test.js`, `pictures.test.js`, `marks.test.js`, `golden.test.js` (+ `tests/golden/hashes.json`, sha256 and byte counts of text-player output recorded before the change), helper `tests/pic-helpers.js`.
- The runtime's check of `node --test` on this build: exit 0, 69 tests, 69 pass.
- Tile size is 22 px; pictures are drawn inset in each tile.
- Intended draw order (D-003): terrain picture, item/brazier/stairs picture, area tint, reach mark, creatures and player, then threat border and badge.

## Decisions already made

- D-002: threat marks plus reach marks. D-003: flat dark-cave pictures, marks always over pictures. D-004: pictures drawn by code, pure scene mapping.

## Constraints

- Judge from the spec and the build, not from this note's wording.
- Many criteria (look, legibility, brightness steps, no console error on opening, clicking, inventory icons) need the page to be shown. If you have no browser or screenshot means, say so plainly per criterion; do not infer a pass from code reading alone.
- Do not change the repository.

## Open questions

- Is the golden test an adequate check of criterion 48? It compares hashes, so a failure shows no diff. Confirm the criterion is met or state what is missing.
- Can any visual criterion be checked with your means (for example by running the page's drawing code with a fake canvas)? State which, and how.

## Expected output

A verification report with pass, fail or not-checkable for each of criteria 31 to 49 and a regression statement for 1 to 30, with how you exercised each. Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, repo/manual.md, repo/index.html, repo/src/page.js, repo/src/scene.js, repo/src/pictures.js, repo/tests/golden.test.js, repo/tests/golden/hashes.json, build (`node --test`, `node play.js {script}`)
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
- Previous handoff: none (composed fresh; the Build handoff holds an implementation self-assessment QA does not receive)
