---
kind: handoff
goal: G-001
seq: 11
from: studio
to: qa
stage: Verify
outcome: routed
---
# 11: studio → qa — verify the first playable against AC-1..AC-15

## Task

Verify the current build in `repo/` against acceptance criteria AC-1..AC-15 in `design/first-playable.md`, by playing input scripts and checking the player-visible output. Give a pass/fail verdict per criterion and an overall verdict, with severity for any failure.

## Context

Goal G-001: the Owner asked for a first playable version of Lamplight Keeper (a short, turn-based lighthouse puzzle game). The build is a standard-library Python 3 program in `repo/`, played through input scripts. The build is complete for this Goal's scope; the project's own test suite is green (31 tests). Tests are not a substitute for your own verification.

## Findings

None to hand over. Verify from the spec, the acceptance criteria and the build, not from any account of how the build works.

## Decisions already made

- D-001 (`decisions/D-001-beam-and-ship-rules.md`): three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Treat as the intended behavior.
- The first screen of a night draws `~` under the starting aim (spec amended). Treat the spec as it stands in `design/first-playable.md`.

## Constraints

- Run the build only through the project's commands: `python3 play.py {script}` (player view), `python3 play.py --trace {script}` (adds internal state), `python3 -m unittest discover -s tests`.
- Player-facing behavior must be derivable from `repo/manual.md` alone; note any place where a player following the manual would be misled or stuck (relevant to AC-15).
- Deterministic: the same script must always give the same night; check repeat runs.
- Do not edit the build, the design or the Decisions. Report defects; do not fix them.
- Anything the spec leaves undefined: report it as undefined, do not decide it.

## Open questions

- None for this step. Design questions that are not defects (mid-night arrivals, whether a wreck always loses the night) are reserved for the later Review; mention them only if you observe concrete player-facing trouble.

## Expected output

A verification report in your outgoing Handoff: a pass/fail verdict for each of AC-1..AC-15 with the script or evidence used, regressions or other defects found with severity and reproduction scripts, and an overall `pass` or `fail`. Address the result to `studio` (the Playtester step that follows must be composed without verification history).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/first-playable.md; repo/manual.md; repo/play.py; repo/lamplight.py; repo/tests/test_game.py; project.md#constraints
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: none (the incoming implementation handoff holds the implementer's reasoning, which QA does not receive)
