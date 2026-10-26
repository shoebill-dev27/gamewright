---
kind: handoff
goal: G-001
seq: 6
from: game-designer
to: studio
stage: Design
outcome: done
---
# 06: game-designer → studio — check 14 versus the threat-mark definition: resolved by adding reach marks (D-002)

## Task

Route this answer to `gameplay-engineer` (if Build is still open) or otherwise to `qa`. Verify must use the new wording of check 14 and of spec section 9.7.

## Context

G-001, handoff 04. Technical Director's planning found that check 14 as written could not hold with correct rules: a creature that is visible but not adjacent has no threat mark, and if the player steps next to it, it strikes in that same turn's creature phase.

## Findings

**Build's interim reading does not stand as the final meaning. The spec is amended so that check 14 holds without exceptions.**

- Reasoning: pillar 1 says every threat that can hurt the player next turn is visible and readable before it does. A step beside a moth, a hound or a shade at r = 2 is a legal next-turn action that leads to damage. Allowing "unless the player's own move ended adjacent" would let unmarked damage in. The rules are fine. Only the display and the wording of check 14 were wrong.
- Fix, in D-002: a **reach mark** is added. For each of the four neighbour tiles the player could step onto, the screen shows which visible creatures would hurt the player at their next action if the player ended the turn there. The threat mark is unchanged: it covers the player's current tile. Both use the same rules and, for the Build, the same planner, evaluated with a hypothetical player position.
- No change to creature behaviour, numbers, content or scope. The pillars are untouched, and the check count and numbering are unchanged (30 checks).
- Changed wording:
  - Spec 9.7 is rewritten (threat marks, reach marks, E after dimming, always showing creatures adjacent to the player or to a neighbour tile, nothing unmarked can hurt).
  - Section 11 gains two edge-case lines.
  - Check 14 is rewritten. It now requires that the damaging creature was visible in the previous output and carried a mark on the tile where the player ended the turn, and it requires the test log to name the case (threat or reach). Hand-made scenarios are added to the check.
  - Check 29 now also requires visible reach marks, distinct from threat marks.
- **What Build must change**:
  1. Compute marks with the E after this turn's dimming (current E minus 1, or minus 2 near the Gloom). At E = 20 a Wait beside a shade must already show a threat mark, because the creature phase sees r = 2. This is a spec detail Build may not have had.
  2. Add reach marks to `view()` for the four neighbours, from `planAction` with a hypothetical player position. Brazier tiles and stairs tiles get none, because the flare stuns the visible creatures and stairs skip the creature phase. Walls and creature-occupied tiles get none.
  3. Always show a creature orthogonally adjacent to the player or to a neighbour tile, even if the line of sight is blocked.
  4. Show the reach marks in both the text (e.g. `Danger: N (m), E (h)`) and the page, from the same `view` data. The text format is Build's to define in `manual.md`.
  5. Replace the check-14 test assertion with the strict form above.
- Not decided here and left to Build: the exact text format and glyphs of the reach marks.
- What I could not check: I have no running build. Whether the reach marks clutter the screen is for the Play step.

## Decisions already made

- D-001: shared code is plain classic-script modules.
- D-002 (new): threat marks plus reach marks on the four neighbour tiles, marks computed with E after dimming. Check 14 is strict.

## Constraints

- Do not change creature rules or numbers to fit the marks. The marks follow the rules.
- Keep the numbering and count of checks.

## Open questions

None.

## Expected output

For `gameplay-engineer`: implement the five changes above, update the check-14 test and the sampled-states test (marks equal what the planner does), and note the final text format in `manual.md` and the Handoff to `qa`. For `qa`, if Build is closed: verify the build against the new check 14 and 29, and send any gap back to `gameplay-engineer`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/game-spec.md, design/acceptance-criteria.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/06-game-designer-to-studio.md
