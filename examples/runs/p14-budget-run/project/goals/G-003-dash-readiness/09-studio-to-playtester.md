---
kind: handoff
goal: G-003
seq: 9
from: studio
to: playtester
stage: Play
outcome: routed
---
# 09: studio → playtester — play the build and report what you can observe

## Task

Play the current build as a player would and report what you observe, from the game's own display and the player manual only. Pay particular attention to dash: whether you can tell when you may use it, and what the game shows you when you try.

## Context

You are evaluating the game as a player of the project's target profile. You are given no information about the build's history and no expected result. Report only what you experience.

## Findings

Not applicable (no implementation information is passed to a Playtester).

How to obtain and run the build:

- The build is in `repo/` (read `repo/manual.md` for controls, the play script format and reaction rules).
- Run from `repo/`: `python3 play.py --view player {script}`, where `{script}` is an input script you write in the format the manual describes.
- Play at least two different runs or sessions, including some fighting in the early rooms. If the manual offers a frame-rate option, play at both 30 and 60 FPS.
- Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad. Input is attack and dash only.

## Decisions already made

None.

## Constraints

- Use only what a player sees: the player view and `repo/manual.md`. Do not read source code, tests, design documents or other handoffs.
- Do not use the trace view.
- Report observations, not fixes or design opinions beyond how it felt to play.
- Say plainly what your means cannot show (for example gamepad feel, since the build is played through scripts).

## Open questions

None.

## Expected output

An observation report: what you did, what the game showed you, where you were unsure or had to guess, and any problem you noticed, with the script or the moments where it happened so someone can reproduce it. Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
- Previous handoff: none
