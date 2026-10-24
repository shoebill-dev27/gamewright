---
kind: handoff
goal: G-001
seq: 51
from: studio
to: playtester
stage: Play
outcome: routed
---
# 51: studio → playtester — Play the combat of rooms 2–5 as a player and report what you experience

## Task

Play the build in `repo/` as a player would, rooms 2 to 5, and report your observable experience of the combat: what you did, what happened, what you felt, and where it was unclear, unfair, repetitive or engaging. Write the report addressed to `studio`.

## Context

This is a fresh playtest session of a short-session top-down action roguelite. You are not told what changed or what to expect. Judge only from what you see and feel.

## Findings

How to play (from `repo/`, using only the player view):

- Run a play script with `python3 play.py --view player {script}`; the script format, controls and reaction rules are in `repo/manual.md`.
- Use the player view only. Do not use the trace view, the bots or the tests.
- Play by hand-timed reactions, as a human would: react to what is on screen, with realistic reaction time rather than frame-perfect inputs.
- Play rooms 2, 3, 4 and 5. In each, try more than one approach (for example, fighting aggressively and playing cautiously, and in some rooms taking your time) and note whether different approaches feel different.
- Pay attention to combat: how threats announce themselves, how you decide what to do, and whether situations feel different from one another.

Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad.

## Decisions already made

None.

## Constraints

- Attack, dash and pause are the only inputs.
- Report observations only (what you saw, did and felt); do not guess at implementation or propose code changes.
- Report anything that looks broken (crash, stuck state, shot from nowhere, damage you could not see coming) with the script you used.

## Open questions

None.

## Expected output

An observation report (per the `playtest-session` skill), written as a Handoff addressed to `studio`, with the scripts you played and the moments you describe.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/ (run through `python3 play.py --view player {script}`)
- Decisions: none
- Previous handoff: none
