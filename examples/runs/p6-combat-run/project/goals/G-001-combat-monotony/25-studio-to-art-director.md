---
kind: handoff
goal: G-001
seq: 25
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 25: studio → art-director — visual review of Build 0.5 against V-1…V-8

## Task

Review what the player sees in the current build against your visual spec (`design/combat-visuals.md`, V-1…V-8) and the project's art direction. Report pass/fail per item and any readability problems.

## Context

Goal G-001. The Option A change set (D-002, D-004) changed enemy telegraphs, colors and the player-facing text output. QA verifies behavior in parallel (24); you review readability and consistency only.

## Findings

- Run the build with `run_play` (player view, what the player sees) on the scripts described in `manual.md`. Use `run_trace` to see which state is on screen at a given moment. The player view is text-based and headless.
- V-5 (manual) and V-6 (color) are in your scope.
- The `manual.md` placed by the Owner is the player-facing text to review for V-5.
- The pause behavior is not implemented. Skip it.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: rework existing enemy behavior first.
- D-005: the Owner placed the draft `manual.md` unchanged.

## Constraints

- Art direction: dark caves, warm light against cold blue-black; threats in saturated orange/red so they read against the dark.
- Small team: prefer fixes that reuse existing systems.
- Threats must be visible before they can hurt the player (pillar 3).

## Open questions

- If the headless text view cannot show an item (for example real color), say which V items you could check only from the spec and `manual.md`.

## Expected output

A pass/fail report per V item with specific fixes for failures. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, design/combat-visuals.md, design/combat.md, manual.md, repo/ (build)
- Decisions: decisions/D-002-combat-response-scope.md
- Previous handoff: none (composed by the Studio)
