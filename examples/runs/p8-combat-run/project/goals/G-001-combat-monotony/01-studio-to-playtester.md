---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — Play the game's combat and report your experience

## Task

Play the current build as a player, with a focus on combat, across the available rooms and both enemy types. Report what you observe and experience as a player.

## Context

The Owner asked for a first-hand player observation of the game's combat. Nothing is known about expected results; report only what you experience.

## Findings

None. This Handoff deliberately carries no implementation information.

## Decisions already made

None.

## Constraints

- Play only through the player-visible view (`run_play`) and the player-facing manual (`repo/manual.md`). Use only the controls the manual describes.
- Play with a gamepad-style mindset: the player profile is an action player who likes dodging and spacing, and dislikes memorizing combo lists.
- Report observable experience only (what you saw, did, felt, and when). Do not speculate about code or internals.

## Open questions

None.

## Expected output

An observation report (per the `playtest-session` skill), covering: what you did over the session, how combat felt over time, moments of engagement or boredom, what you did repeatedly, and what, if anything, you wanted to do but couldn't. Cover several rooms and attempts if possible. The report goes to `game-designer` (Diagnose) via the Studio's Route operation; address it to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/ (run with `python3 play.py --view player {script}`)
- Decisions: none
- Previous handoff: none
