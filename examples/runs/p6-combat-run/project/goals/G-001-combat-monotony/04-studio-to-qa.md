---
kind: handoff
goal: G-001
seq: 4
from: studio
to: qa
stage: Observe
outcome: routed
---
# 04: studio → qa — Check two points of build behavior against design/combat.md

## Task

Run the current build and check the two points below against `design/combat.md`. Report for each whether the build matches the spec, contradicts it, or shows behavior the spec does not define.

## Context

Goal G-001 is about combat feeling monotonous. While reviewing scripted play of rooms 1–3, two points came up that may be defects, so they are checked independently here. This step only observes and reports. It does not change the game.

## Findings

Nothing is established yet. The points to check:

1. **Room composition.** `design/combat.md` describes rooms as a mix of Grubs and Spitters with 3–6 enemies. For each of rooms 1–5 (and the practice room, if it exists), record which enemy types and how many enemies appear at start, and whether that matches the spec.
2. **Behavior after the player's hearts reach zero, and after a room is cleared.** Record what the player sees and what the simulation does (is there a game-over, restart or end state; do enemies keep acting; can the player still give input). Compare with what `design/combat.md` says. If the spec says nothing, report it as undefined behavior, not as a defect.

## Decisions already made

None.

## Constraints

- Use the project's run commands: `python3 play.py --view player {script}` (what the player sees), `python3 play.py --view trace {script}` (simulation state), `python3 bots.py {script}`, and `python3 -m unittest discover -s tests`. Script format is in `manual.md`. Run them from `repo/`.
- Do not modify the build or the design documents.
- Report in the same terms the player would see; use the trace view for exact state.
- Separate three kinds of result: matches the spec, contradicts the spec (defect), spec undefined (not a defect).

## Open questions

None.

## Expected output

A report following `reproduce-defect`: for each point, the exact steps or scripts used, the observed behavior, the spec reference, and the verdict. For each confirmed defect, give a reproduction and player-observable acceptance criteria, plus a severity. Address the report to `game-designer`, who owns the spec and any wording or missing rule that follows from it. A defect that needs a fix goes through the Studio's routing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#current-state, project.md#constraints, design/combat.md, manual.md, repo/ (build; run with the commands above)
- Decisions: none
- Previous handoff: none
