---
kind: project
id: lamplight-keeper
name: Lamplight Keeper (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py {script}
run_trace: python3 play.py --trace {script}
---
# Project: Lamplight Keeper (new concept)

## Vision

A short, turn-based puzzle game. The player keeps a lighthouse on a rocky coast for one night at
a time. Ships come in from the dark sea, one tile per turn, heading for the harbor; the lamp's
beam turns them aside, and every turn the player chooses where it points. Bring ships to the
harbor; let none hit the rocks.

Pillars:

1. **One clear choice per turn.** Turn the beam left, turn it right, or hold. Nothing else.
2. **Reading ahead is the fun.** Where each ship will be in a few turns, and what the beam will do
   to it, can be worked out from what is on screen. Luck does not decide a night.
3. **A night is short.** One night takes a few minutes; it is lost or won in that time.

## Player profile

Puzzle players who like short, thinky sessions with readable rules (in the spirit of small
turn-based puzzle games). They want to plan, not to react fast.

## Current state

First playable exists (G-001 closed, goal met). `repo/` holds a standard-library Python 3 build
(`lamplight.py`, `play.py`, `manual.md`, `tests/`). Three nights are playable by input script:
Night 1 teaches the slide, Night 2 two sides, Night 3 keeping one ship dark. Each turn offers
L / R / H; wins took at most 7 turns, cap 10. Deterministic. Spec: `design/first-playable.md`;
Decision: D-001 (three aims, lit ships slide along the beam row, a wreck loses the night).
Run: `python3 play.py {script}` (`--trace` adds state); tests: `python3 -m unittest discover -s tests`
(31 pass). QA passed AC-1..AC-15; a script-only playtest won nights 1-3.
Known issues: the final screen prints twice (low); nights 1-2 are short and gentle; DAWN, pinned or
overlapping ships, bad commands, a failing Night 2 and a wrong-ship Night 3 loss are unobserved;
real-time length is unmeasured. Proposed next Goals: depth of nights, final-screen tidy-up,
observation gaps, mid-night arrivals, manual wording.

## Constraints

- The build is a Python 3 program using the standard library only, in `repo/`.
- It is played through input scripts, with no live input: `run_play` (`python3 play.py {script}`)
  plays a script and prints what the player sees, `run_trace` adds the internal state, and
  `run_tests` runs the build's tests. The script format is the build's to define, in
  `repo/manual.md`, which ships with the build and is all a player is told.
- Text output only (a grid of characters per turn); no graphics yet.
- Deterministic: the same script always gives the same night.

## Design index

None yet.
