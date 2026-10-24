---
kind: handoff
goal: G-001
seq: 87
from: studio
to: art-director
stage: Verify (visuals: V-17 from QA captures; dash-draw wording)
outcome: routed
---
# 87: studio → art-director — Read the V-17 captures and rule on the dash-draw wording

## Task

Read the QA captures in Appendix A of `83-qa-to-studio.md` for V-17 (the on-you entry and displaced glyph are gone after a defeat and after a dash off the tile). Give the visual verdict, and rule on the dash-draw question below.

## Context

G-001, Option A. In 80 you passed V-9…V-14, V-16 and V-18 and left V-17 open until QA could capture the defeat and dash-off cases. QA has now run them at 30 and 60 FPS and found the draws correct in all cases (83, outcome pass):

- On the draw that prints "grub defeated", the map, the "on you:" line and the displaced glyph are all gone.
- The first draw after a dash off the tile has no "on you:" line and no displaced glyph.
- The same holds when the grub is in Recovery on the tile.
- Colour and the reverse-video cell cannot be checked in a text view.

## Findings

QA observation 1 (a wording tension, not a failure):

- `design/combat-visuals.md` ("When the enemy leaves or dies") says the on-you line updates "in the same draw as … the player's dash".
- Principle 4 lists no draw at the dash. V-16 forbids draw events that are not listed.
- So the first draw after a dash comes up to 0.5 s later. QA measured 0.2 s in `dashA` and 0.4 s in `dashB`.
- No draw shows a stale entry, so V-17 as written holds.

QA observation 2: the `dashA` draw at 0.50 s shows the player mid-dash, more than half a tile from the grub, with `G` alone in its own cell. QA reads it as a valid "after" draw.

## Decisions already made

- D-012, D-014: the on-you line and cell rules.
- D-015: lunge draws with the Strike-start hit word, and the spit shot at spawn, are accepted.

## Constraints

- A new draw event at the dash would change V-16, which is a spec change. Do not add one on your own. If you think it is needed, say so and hand it to the Studio for the `game-designer`, and for the `game-director` if scope would change.
- Do not rewrite the criteria to match the build. Colour (V-6) and the reverse-video cell are recorded as not checked unless you can check them from a colour capture.

## Open questions

1. Does V-17 pass visually at both frame rates, from the captures?
2. Is the delay until the first draw after the dash acceptable for the "readable threats" pillar? Accept it and fix the wording, or ask for a spec change?

## Expected output

A handoff to `studio` with `stage: Verify`:

- outcome `pass` if V-17 passes and the delay is acceptable, `fail` if V-17 fails, `question` if you are blocked;
- if you accept the delay, a short ruling, recorded as a Decision if it constrains later work, plus a one-sentence correction to the "in the same draw as … the player's dash" wording in `design/combat-visuals.md`;
- a note on whether any other criterion needs a second look.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md, studio/skills/make-decision.md
- Project: design/combat-visuals.md, design/combat-visuals-verify-rulings.md, project.md#art-direction
- Decisions: decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md, decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
- Previous handoff: goals/G-001-combat-monotony/83-qa-to-studio.md
