---
kind: handoff
goal: G-001
seq: 37
from: studio
to: playtester
stage: Play
outcome: routed
---
# 37: studio → playtester — Play the first puzzle as a child would

## Task

Play the first puzzle (level 1) of the current build as a player from the profile below, from the moment the level starts until it is solved. Report what you observe as a player: what you do, when, and what you notice. Report observable experience only.

## Context

This is a playtest session on the newest build of a touch puzzle game for children. You have no history of the build and need none. Your report goes back to the Studio.

## Findings

Nothing to report from the sender. Run the build as follows:

- Build: `sim/build-0.6.md`. This is a dry-run project with no device. "Running the build" means reading that file as the player-visible description of the game, and playing through it step by step as the player would.
- Part to play: level 1 only, from the first moment after it loads, to the solved state.
- Player profile: children aged 7–10, some still early readers, often playing beside a parent. Sessions of 5–15 minutes. They quickly lose interest when nothing responds to their touch. Play as such a child would, not as a developer. Do not rely on reading text, and do not use outside knowledge of how the game is meant to work.
- Play focus: the first puzzle from start to finish. Note moments where you hesitate, what you try, what responds, and what you would do next as the child.

## Decisions already made

None.

## Constraints

- Touch only; judge only what a player can see and do.
- Report observations, not fixes or design changes. You have no authority over the game.
- If part of the build description is unclear or you cannot tell what a player would see, say so instead of guessing.
- Levels 2 and later are out of scope.

## Open questions

None.

## Expected output

An observation report (per `playtest-session`): the sequence of what you did and noticed, any hesitation or pause and where it occurred, what responded to your touch and how clearly, and anything confusing, frustrating or delightful. Address it to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.6.md
- Decisions: none
- Previous handoff: none
