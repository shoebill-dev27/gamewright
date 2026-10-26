---
kind: handoff
goal: G-002
seq: 12
from: studio
to: qa
stage: Verify
outcome: routed
---
# 12: studio → qa — second verification of the entity pictures, with real screenshots

## Task

Verify the current build against the acceptance criteria 31 to 49 in `design/entity-pictures.md`. Re-check criterion 44 first (the reach letters need a dark backing). Use real screenshots of the browser page wherever a criterion is visual.

## Context

Goal G-002 gives each kind of thing on the floor grid its own picture on the browser page. Your first verification (08) failed criterion 44, passed 45 and 48 with limits, and could not check the rest without a viewer. The build was changed after that. D-005 sets a larger tile, dark chips behind badges and reach letters, a player outline, and shade and Gloom contrast. The Art Director reviews the same build visually in parallel; you do not depend on that review.

## Findings

Nothing from the implementer is passed on. Verify from the spec, the criteria and the build.

## Decisions already made

- D-003: flat dark-cave pictures; marks are always drawn over pictures.
- D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast.

## Constraints

- Run the build only through the project's run commands (`node --test`, `node play.js {script}`, and the page `repo/index.html`).
- In your earlier pass, the `shot` call failed because of how keys were passed. Use one key name per press in each `shot` call.
- Do not change files in `repo/`.
- If a criterion cannot be checked with your means, say so plainly. Do not mark it pass by inference.
- Also check that the page layout (board plus side panel) fits a 1280 px wide window. If it does not, report the measured widths.

## Open questions

None.

## Expected output

A pass/fail report per criterion 31 to 49, with evidence (screenshot or run output) and any limit stated. Address the result to `studio`. A failing criterion goes in the report with steps to reproduce.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, design/acceptance-criteria.md, repo/manual.md, repo/index.html, the build in repo/
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/08-qa-to-studio.md
