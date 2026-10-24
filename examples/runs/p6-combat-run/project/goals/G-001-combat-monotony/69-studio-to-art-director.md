---
kind: handoff
goal: G-001
seq: 69
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 69: studio → art-director — Visual review of the changed combat view (V-9…V-17)

## Task

Review what the player sees in the current build against `design/combat-visuals.md` (V-9…V-17, earlier V items as regression) and the project's art direction. Judge readability and consistency, and report pass/fail per V item.

## Context

Goal G-001, "Combat feels monotonous", Option A (D-002). The change set altered the player view: an `on you:` line under the hearts line when an enemy shares the player's tile, a reverse-video cell for the displaced enemy glyph in color mode, hit lines that name the attacker's position or the spitter's spot, and `(miss)` lines with a cause. Your own spec (D-012, V-9…V-17) defines what the view should show. A QA verification of behavior runs in parallel; you review only what the player sees.

## Findings

How to look (from `project.md`; run in `repo/`):

- `python3 play.py --view player {script}` shows what a player sees. Script format is in `manual.md`.
- Useful setups: an enemy on the player's tile (`room empty`, `player 8 4`, `spawn grub 8 4`, then an attack); a room with several grubs; a spitter shot hitting the player; a swipe that misses too far away and one that misses with the enemy not in front.
- Check the color view as well as the plain view, in particular the reverse-video cell and whether it reads against the dark background and keeps the threat colors (saturated orange/red).

Points earlier rounds could not see: the reverse-video cell in color mode, and the `on you:` line in a live frame. Report what you saw first-hand versus what you inferred from code.

## Decisions already made

- D-001: no new inputs.
- D-006: enemies may overlap the player but are never hidden.
- D-012: `on you:` line for displaced enemies; attacker position in hit lines.

## Constraints

- Art direction in `project.md`: warm light against cold blue-black; threats in saturated orange/red.
- You review and specify; do not edit the repo. Changes you want go back as findings.
- Wording placed in `manual.md` is Owner-placed (D-005, D-007); report if V-15 text is missing there, but do not edit it.

## Open questions

None.

## Expected output

A visual review with per-item pass/fail (V-9…V-17, regressions), what was seen first-hand versus inferred, and any specified fixes. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, design/combat-visuals.md, manual.md, repo/
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/60-art-director-to-studio.md
