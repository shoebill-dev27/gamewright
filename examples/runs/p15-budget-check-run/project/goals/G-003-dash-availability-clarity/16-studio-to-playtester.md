---
kind: handoff
goal: G-003
seq: 16
from: studio
to: playtester
stage: Play
outcome: routed
---
# 16: studio → playtester — Play the build as a player and report what you can tell

## Task

Play the current build as a player would, using only what the game shows you and the player manual, and report your observable experience. Address the result to `studio`.

## Context

Lantern Depths is a short-session top-down action roguelite played here through a text view and input scripts. Players are action players who like short, intense runs, are comfortable with dodging and spacing, dislike memorizing combo lists, and mostly use a gamepad.

## Findings

Nothing from implementation is given. To run the build, work in `repo/`. The manual `repo/manual.md` explains the controls, the script format and how to choose the frame rate. Play with `python3 play.py --view player {script}`, where `{script}` is an input script you write. Do not use the trace view or read source code, tests or design documents.

Play focus: pay attention to how you use movement and dash during fights, and what you can tell about your options at each moment. Play mainly at 60 FPS, and run at least one short session at 30 FPS.

## Decisions already made

None.

## Constraints

- Report only what a player could observe. Do not guess at causes or at how the game is built.
- Use only player-visible material: the game's output and `repo/manual.md`.
- Say plainly what you could not observe with the means you have.

## Open questions

None.

## Expected output

An observation report to `studio` (kind handoff, `to: studio`): what you did, with the scripts you used, what the game showed, where you were unsure what you could do or when, and where you had to guess or try something just to find out. Quote the game's text where it matters.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
- Previous handoff: none
