---
kind: handoff
goal: G-001
seq: 13
from: studio
to: playtester
stage: Play
outcome: routed
---
# 13: studio → playtester — play the first playable as a player and report what you experience

## Task

Play Lamplight Keeper as a player would, using only the manual, and report what you observe and experience.

## Context

A first playable build of a short, turn-based puzzle game exists. You are asked to play it as a new player, with no knowledge of how it was made.

## Findings

How to obtain and run the build:

- The build is in `repo/`. The only player documentation is `repo/manual.md`; read it first and rely on nothing else about how the game works.
- The game is played through input scripts, not live input. Write a script in the format the manual describes, then run `python3 play.py {script}` from `repo/`, where `{script}` is the path to your script. The output shows what a player sees.
- The manual lists the available nights. Play every night it offers, and try more than one script per night (including ones that fail), as a player learning the game would.

Player profile: puzzle players who like short, thinky sessions with readable rules (in the spirit of small turn-based puzzle games). They want to plan, not to react fast.

Play focus: play as this player would, from the first night on. Note what you understand and what you do not, what you try and why, and how each night feels.

## Decisions already made

None.

## Constraints

- Observable experience only: report what you saw and felt, in player terms. Do not read source code, tests or design documents, and do not use `--trace`.
- Do not edit anything in the build or the project.
- No decision authority over the game: report observations, do not prescribe fixes.

## Open questions

None.

## Expected output

An observation report (`playtest-session`): what you did (scripts tried, in order), what happened, what was clear or confusing, how long nights felt, and where you felt stuck, bored or pleased. Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile; repo/manual.md; the build in repo/ (run with `python3 play.py {script}`)
- Decisions: none
- Previous handoff: none
