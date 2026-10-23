---
kind: handoff
goal: G-001
seq: 25
from: studio
to: playtester
stage: Play
outcome: routed
---
# 25: studio → playtester — Play the build as a player and report what you experience in combat

## Task

Play the build in `repo/` as a player would and report your observable experience of the combat: what you did, what you felt, what stood out. Address the report to `studio`.

## Context

This is a playable vertical-slice prototype of a short-session top-down action roguelite. The player descends through lantern-lit caves, one room at a time. Combat uses an attack and a dash. You have no other background, and none is needed.

## Findings

Nothing to report from the sender. This Handoff carries no information about the implementation.

How to obtain and run the build:

- The build is in `repo/`. Read `repo/manual.md` first. It is the player-facing manual: controls, the input-script format and the reaction rules.
- A play session is an input script. Run it from `repo/` with `python3 play.py --view player {script}`. Use the player view only.
- The build has 5 rooms. Play all of them, in order, and also try rooms again with different approaches.
- Play by hand: write your own scripts and vary the timing of your moves (waiting, approaching, dashing, attacking at different moments). Do not rely only on scripts that ship with the repository.

Player profile (the player you represent): action players who want short, intense runs. Comfortable with dodging and spacing; not interested in memorizing combo lists. Mostly play with a gamepad.

Play focus: pay attention to combat across the whole build, including how the rooms and the enemies compare with each other.

## Decisions already made

None.

## Constraints

- Judge from what a player can observe only. Do not read source code, tests, design documents or bot output, and do not use the trace view.
- Do not propose or assume specific numbers; describe experience.
- No new input buttons exist: attack, dash and pause only.

## Open questions

None.

## Expected output

An observation report written for `studio`: what you played (rooms, approaches), what happened, what felt engaging or repetitive, whether different situations made you play differently, whether threats were readable before they could hurt you, and anything that looked broken (a defect, which would go to QA). Observations only; no implementation guesses.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
- Decisions: none
- Previous handoff: none
