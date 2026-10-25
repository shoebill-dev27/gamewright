---
kind: handoff
goal: G-001
seq: 3
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 03: studio → gameplay-engineer — build the first playable from the design spec

## Task

Build Lamplight Keeper's first playable in `repo/` exactly as specified in `design/first-playable.md`: `play.py`, the game code, the three nights, tests, and `repo/manual.md`. Define the script format yourself and document it in the manual.

## Context

Goal G-001: the Owner asked (ja) "このコンセプトで、遊べる最初の版を作ってほしい". Design is done; the spec was written without a build and its solutions were only hand-simulated. `repo/` holds only a README. Plan was skipped as the scope is small and standard-library only.

## Findings

Spec summary (the spec is authoritative; read it in full):
- 7×7 board, lighthouse at (3,3), coast in row 6 made of harbor and rock tiles. All ships are on the board at turn 0.
- Beam aims: LEFT, UP (lights nothing), RIGHT. Commands `L`, `R`, `H`, clamped at the ends; changing sides takes two turns.
- Only row 3 can be lit. A lit ship does not advance; it slides one tile away from the lighthouse (pinned at the map edge, not wrecked). An unlit ship moves one tile south.
- Harbor docks a ship; a rock or the lighthouse wrecks it; any wreck loses the night. Turn limit 10 (dawn) loses with ships still at sea.
- Required screen content: grid, row/column numbers, ship list, forecast line, `~` for lit tiles, dock/wreck reports with position (spec §2, §6).
- Three nights with intended winning solutions (win on turn 7): Night 1 `L H H H R H H`; Night 2 `H L R R L H H`; Night 3 `L L R R L H H`. The spec also has failure scripts that must lose as stated.
- Acceptance criteria AC-1..AC-15 are in spec §9. They cover: first screen, aim changes, lit tiles, ship movement, edge pinning, dock/wreck reports, the solutions and failure scripts, dawn loss, same-turn dock and wreck, determinism, invalid commands and short scripts, commands after the end, and deriving positions from screen plus manual.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit.

## Constraints

- Python 3, standard library only; text output; deterministic; played through input scripts only (no live input).
- Commands to support: `python3 play.py {script}`, `python3 play.py --trace {script}` (adds internal state), `python3 -m unittest discover -s tests` (run from `repo/`).
- `repo/manual.md` ships with the build and is all a player is told. It must give the rules (spec §3–§4), the symbols (§2) and the script format, and must let a player derive ship positions (AC-15). It must not reveal solutions.
- Add no mechanics beyond the spec. If the spec is ambiguous, contradictory or missing a case, stop and hand back to `game-designer` (via `studio`); do not decide it yourself.
- Tests should cover the spec's solutions and failure scripts, and the AC items that can be tested automatically.

## Open questions

None for you. The designer's questions (mid-night arrivals, wreck always losing) are for `game-director` at Review.

## Expected output

The built `repo/` with passing tests, and build notes in your outgoing Handoff: files created, script format, how to run, test results, any spec deviations or ambiguities, and anything you could not check. Address the result to `studio` (the next step is QA, which must receive a Handoff composed from permitted information only).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/first-playable.md; project.md#constraints; repo/README.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/02-game-designer-to-studio.md
