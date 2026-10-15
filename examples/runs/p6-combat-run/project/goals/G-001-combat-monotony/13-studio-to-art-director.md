---
kind: handoff
goal: G-001
seq: 13
from: studio
to: art-director
stage: Design
outcome: routed
---
# 13: studio → art-director — Review the visuals of the Option A spec before Build

## Task

Review what the player will see under the Option A spec (glyphs, colors, states, telegraphs, swipe arc, run-over screen) for readability and consistency with the art direction, and give the visual rulings Build needs.

## Context

G-001: the Owner finds combat monotonous. The game-designer specified a rework of the grub and spitter behavior (D-002, Option A) in `design/combat.md`. The new behavior depends on telegraphs the player can read: the grub Wind-up (0.5 s), the spitter Charge (0.8 s), damaged states, the swipe arc, the downed marker and the run-over screen. Pillar 3 requires every threat to be visible before it can hurt the player. The game is a headless build shown as text; "what the player sees" is the `run_play` view.

## Findings

From the designer's hand-off: glyph and color choices in the spec need art-director review (threat colors saturated orange/red against the dark cave). The rooms 4–5 playtest (08) found that spitters read as scenery and their shots were never reacted to.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: Option A, reuse existing enemy behavior.

## Constraints

- Art direction in `project.md#art-direction`; small team, reuse existing systems.
- Do not change rules, timings or parameters; those belong to the game-designer. If a visual problem needs a rule change, say so as an open question.
- No new inputs.

## Open questions

- Is each telegraphed state (Wind-up, Charge, Recovery) distinguishable from the idle and harmless states in `run_play`?
- Do the threat glyphs/colors read against the dark, and are damaged states and the downed marker clear?

## Expected output

A short visual review with concrete rulings (what to keep, what to change), written in Findings of the outgoing Handoff, and edits to the visual parts of `design/combat.md` only if needed. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md, studio/skills/write-design-spec.md
- Project: project.md#art-direction, project.md#vision, design/combat.md, manual.md, goals/G-001-combat-monotony/08-playtester-to-game-designer.md
- Decisions: decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/10-game-designer-to-studio.md
