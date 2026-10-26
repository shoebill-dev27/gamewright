---
kind: handoff
goal: G-002
seq: 16
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 16: studio → game-director — G-002 is over budget: cut the remaining work to what the Owner request needs

## Task

Decide the scope of what is left in G-002. Name what must still be done for "それぞれに絵をつけてほしい" to count as met, and what is skipped or handed to the Owner as a look-and-confirm item. If the cost cannot be cut inside the Goal, prepare an Owner escalation about the cost.

## Context

G-002 asks for a picture for each kind of thing on the floor grid. Design (spec `design/entity-pictures.md`, criteria 31 to 49), Plan, Build, Verify, a Build fix (D-005) and a second Verify have all run. The budget was 13 operations and 16 are used. Under the budget rule the Studio may add only this scope step or an Owner step, plus steps already planned.

## Findings

From QA (14) and the Art Director (15), both from the same tool limits:

- No criterion was seen to fail. 69 of 69 tests pass (golden hashes included). The page loads with no console errors.
- Seen on the page and fine: wall, floor, unlit brazier (small and grey but readable), player (outline works on plain floor), `<`, moth at a distance, remembered versus visible wall, ember flame at r = 6. The look fits the cave-and-ember mood.
- Never seen on the page, because `shot` takes keys only (random seed, no URL hash, no scenario): threat marks, reach marks, criterion 44 (the earlier fail, re-check order unfulfilled), hound, shade, Gloom, stunned creatures, the flame at r = 2, items in slots, the lit brazier, and the layout at 1280 px (computed fit about 1130 to 1190 px, not measured).
- QA's options for seeing them: (a) a QA-only fixture page under a new path; (b) extend `shot` to pass a URL hash or viewport; (c) the Owner looks. The Art Director recommends holding the Goal, since the marks carry pillar 1. Neither role can change the tools.
- Art Director's one suggested change: `dim()` factor 0.55 to 0.65 in `repo/src/pictures.js`, because remembered floor is nearly black. Optional, with a fallback of 0.60. It touches no rule or mark.
- Play (the playtester) stays tentative: the page cannot be shown to a playtester with the available means.

## Decisions already made

- D-003 (flat dark-cave style, marks over pictures), D-004 (pictures drawn by code), D-005 (tile 28 px, chips, outline).

## Constraints

- Add no stages beyond what you decide here; the Studio can only open Roles' steps that you name. Only the Owner changes the budget.
- Rules, balance and the text player are out of scope. Do not reinterpret the Goal; if the cost must change, escalate.
- Be plain about what the available means cannot show; do not claim a verified result that no one saw.

## Open questions

1. Is the Goal accepted on the partial evidence, with the unseen scenes (marks, creatures, 1280 px) handed to the Owner as a look-and-confirm item at Close?
2. Is the `dim()` change worth one more Build (and then an unverified result), or is it dropped as a proposed follow-up Goal?
3. If more verification is needed, is it an Owner decision about cost (for example, extra budget or a `shot` extension)? Then write the Escalation.

## Expected output

A Decision (`decisions/D-006-...md`) or an Escalation, addressed to `studio`, that states which remaining steps are kept (named by Role) and which are `skipped`. Give the Owner-facing look-and-confirm list if you choose that path.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md#vision, project.md#constraints, design/entity-pictures.md, goals/G-002-entity-pictures/goal.md
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/14-qa-to-studio.md, goals/G-002-entity-pictures/15-art-director-to-studio.md
