---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — Play the combat and report what you experience

## Task

Play the game as a player, concentrating on combat, and report what you observe and experience. Cover several combat encounters across the rooms available, not only the first one.

## Context

The studio wants a first-hand, player-side account of how combat plays. Your report goes to the game designer for analysis.

## Findings

None. This Handoff deliberately carries no information about the implementation.

## Decisions already made

None.

## Constraints

- Observe only what a player can see and feel. Use the player view (`run_play`), not the trace or the source.
- Play with the controls and script format in `manual.md`.
- Play as the player profile describes: an action player, comfortable with dodging and spacing.
- Report what you experienced, not what you think should change in the code. Suggestions as a player are welcome, but mark them as such.

## Open questions

None.

## Expected output

An observation report from your `playtest-session`: what you did, what happened, how the fights felt over time (including anything that changed or stayed the same between encounters), moments of tension or boredom, and anything unclear or surprising. If you find behavior that looks plainly broken, record it as a separate item. The report goes to `game-designer` for the Diagnose step.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in `repo/` (run with `python3 play.py --view player {script}`)
- Decisions: none
- Previous handoff: none
