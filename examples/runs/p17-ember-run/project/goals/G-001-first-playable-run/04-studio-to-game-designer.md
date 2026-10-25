---
kind: handoff
goal: G-001
seq: 4
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 04: studio → game-designer — resolve check 14 versus the threat-mark definition

## Task

Decide whether acceptance check 14 and the spec's threat-mark definition (section 9.7) conflict, and fix whichever is wrong. Amend `design/game-spec.md` and/or `design/acceptance-criteria.md` so check 14 is verifiable with correct rules.

## Context

G-001 (first complete playable run in the browser). Design and Plan are done; Build is running now in parallel (handoff 03) and does not wait for this answer. Verify must not start until this is settled. The Technical Director found, while planning, that a threat mark means "can hurt the player at its next action", so a creature that is visible but not adjacent has no mark. If the player steps next to it, it attacks in that same turn's creature phase. The damage then comes from a creature that was visible but not marked in the previous output. The same holds for an adjacent step toward a shade at r = 2. Read literally, check 14 ("no damage from a creature that was not shown and marked before it hit") would fail with correct rules.

## Findings

Technical Director's proposed interim reading, used by Build: every damaging creature was visible in the previous frame, and it was threat-marked there unless the player's own move ended adjacent to it (or inside its reach). The check-14 test logs both cases. One alternative the TD named: mark "would strike if you step adjacent" tiles, so the danger is readable before the step (this bears on pillar 1, "every threat that can hurt the player next turn is visible and readable before it does"). Choosing between them is a rules and player-facing decision and belongs to you.

## Decisions already made

- D-001: shared code is plain classic-script modules (not relevant to the content, listed for completeness).
- No Decision exists on threat marking.

## Constraints

- Stay inside the vision and its pillars, and inside Goal scope. Do not add content beyond what one five-floor run needs.
- If the fix would change a pillar or the Goal's scope, say so and hand back with the question instead of deciding.
- Stay in design terms; do not prescribe code structure.
- Keep the numbered checks stable (same count and numbering) so Build and QA references hold.

## Open questions

- Is the interim reading acceptable as the intended meaning of check 14, or should the spec change (for example, mark tiles that would be struck if the player stepped there)?

## Expected output

Updated spec and/or acceptance criteria in `design/`, with the reasoning and the exact new wording of check 14 and of section 9.7 if changed. Write a Handoff addressed to `studio` (outcome `done`, or `question` if a Decision is out of your authority) that states in Findings whether Build's interim reading stands or what must change. The Studio will route it to `gameplay-engineer` (if Build is still open) or `qa`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, design/game-spec.md, design/acceptance-criteria.md
- Decisions: none
- Previous handoff: goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md (Findings 10.1 only)
