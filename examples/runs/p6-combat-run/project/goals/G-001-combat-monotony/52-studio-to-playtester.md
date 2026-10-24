---
kind: handoff
goal: G-001
seq: 52
from: studio
to: playtester
stage: Play
outcome: routed
---
# 52: studio → playtester — Play the parts of the game that have not been seen yet

## Task

Play the build as a first-time player and report what you experience, paying attention to combat. Cover the parts that no earlier session has seen: the later rooms and any enemies other than the first room's. Use the manual to find out how far you can get and how to reach those parts.

## Context

A player of the profile below tried the game before; they reached only the start of the first room. This session looks at the rest. Nothing else about earlier sessions is passed on to you.

## Findings

Not applicable (no implementation information is included, by design).

## Decisions already made

None.

## Constraints

- Use only the player view (`python3 play.py --view player {script}`) and `manual.md`. Do not read source code, tests, design documents or other Studio files. Do not use the trace view or the bots.
- A play session is an input script as described in `manual.md`. Play in many short runs and adjust between runs. If you can play live and react to the screen, do that.
- Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad.
- If you cannot reach a part of the game with the manual's means, say so and report what you could reach.

## Open questions

None.

## Expected output

An observation report in the Findings of your outgoing handoff (`templates/handoff.md`), as a player, from observable experience only. Say how you played (live or by script) and which rooms, enemies and situations you actually saw, and which you did not. Cover: how the fights felt and whether they differed from each other; whether your choices (positioning, timing, dash, attack) mattered; anything unclear, unreadable or unfair; anything broken; positives. Address the result to `studio` (`54-playtester-to-studio.md`).

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
- Decisions: none
- Previous handoff: none
