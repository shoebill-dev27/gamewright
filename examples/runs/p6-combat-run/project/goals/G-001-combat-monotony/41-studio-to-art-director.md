---
kind: handoff
goal: G-001
seq: 41
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 41: studio → art-director — re-judge the combat visuals (V-1, V-2, V-6, displaced cell) from QA's captures of build 0.5

## Task

Do a visual review of the current rendering against `design/combat-visuals.md` (V-1…V-8) and D-006, using the captures QA made. Give a pass/fail per criterion, and name what you could not observe.

## Context

G-001 (combat feels monotonous) is in Verify. Your earlier review (32) failed V-1 (a grub hidden under the player) and found F3 (an enemy drawn over the swipe arc). Build then changed the rendering: an enemy on the player's tile is drawn on a free adjacent tile, never hidden (D-006, AC-18), and the enemy glyph stays visible over the arc. QA (39) re-ran the build at 30 and 60 FPS. AC-17 and AC-18 pass, and the timings are unchanged from the baseline. The gameplay-engineer or QA do not need to be consulted for this review.

## Findings

QA's captures, in `goals/G-001-combat-monotony/39-qa-to-studio.md`:

- Section 2: a grub on the player's tile in wind-up, strike, recovery, and down (`PG`, `Pg`, `xg`); a damaged grub (`Pw`/`PW`); a spitter on the tile (`Ps` idle, `PS` charging) at 30 and 60 FPS; two overlapping enemies (`sPg`, `SPg`, `SPG`, `sxg`); three overlapping grubs (`G` left, `g` right, `g` above).
- Section 4: the swipe hit with the arc over the neighbouring tiles and the enemy glyph visible in its own cell; a swipe that hits nothing.
- Section 5: the table of which capture covers which request.

More captures, in `40-qa-to-studio.md`: a practice-room run with a grub and a spitter on the player's tile, 30 and 60 FPS.

Known gaps in the captures:

- No `--color` capture was obtainable with the project commands. QA's reading of the code is lantern yellow for the player, orange for alert enemies, red for shots; this was not verified. V-6 (color) may remain unobserved.
- Not observed: a swipe while an enemy is drawn beside the player (arc and displaced glyph in one cell).
- Not checked by QA: whether the displaced glyph prefers the side the enemy last came from. All captures place a single grub on the side it came from. Readability of the placement is yours to judge.
- F2 is cosmetic and stays so unless you disagree.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; the practice room is listed in the On screen section of the manual.
- D-001: no new inputs.

## Constraints

- Judge only what the captures and the repository's read-only files show. Do not edit the build or `manual.md`.
- You may read `repo/play.py` to judge V-6 if no color capture exists, but mark the result as "from code, not observed".
- A fail must name the criterion and the capture where it shows, so it can go to Build.

## Open questions

1. V-1, V-2, V-6 and the displaced cell: pass, fail, or not observable?
2. Is the missing swipe-plus-displaced-glyph capture needed, or is it safe to leave to Play?
3. Is a `--color` capture needed? If yes, say exactly what is needed, so the Studio can ask the Owner.

## Expected output

A visual-review report as a Handoff, `from: art-director`, addressed to `studio`, with `outcome: pass`, `fail` or `question`, and per-criterion results for V-1…V-8 that are in scope for the current build. List the gaps that remain.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/combat-visuals.md; design/combat.md (AC-18 only); project.md#art-direction; repo/play.py (read-only, V-6 only); goals/G-001-combat-monotony/40-qa-to-studio.md (captures only)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/39-qa-to-studio.md
