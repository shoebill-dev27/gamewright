---
kind: handoff
goal: G-001
seq: 83
from: studio
to: playtester
stage: Play
outcome: routed
---
# 83: studio → playtester — Play the current build as a player and report your experience of combat

## Task

Play rooms 1–5 of the build as a player and report what you experience, especially in combat.

## Context

Lantern Depths is a short-session top-down action roguelite prototype. This is a fresh session: you have no history of earlier sessions and need none.

## Findings

Build: `repo/`, sha 1ac4d04d0e75. A play session is an input script; `repo/manual.md` describes the controls, the script format and the reaction rules. Run a script with `python3 play.py --view player {script}` from `repo/` (the player view shows what a player sees). Do not use the trace view or read the source, tests or design documents: stay with what a player can observe.

Player profile: action players who want short, intense runs. They are comfortable with dodging and spacing, are not interested in memorizing combo lists, and mostly play with a gamepad.

Play focus: pay attention to combat. Play every room at least once. Time your inputs by hand from what the player view shows, rather than replaying one fixed script, and try more than one way of handling a room. Note which situations feel alike and which feel different, and whether you can tell why something hurt you.

## Decisions already made

None.

## Constraints

- Observable experience only: no causes, no design opinions presented as fact, no code or balance numbers.
- No new input buttons exist: attack, dash and pause only.

## Open questions

None.

## Expected output

An observation report in the usual playtest format (what you did, what you saw and felt, moments of boredom or engagement, anything confusing, anything that looked broken). Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
- Decisions: none
- Previous handoff: none
