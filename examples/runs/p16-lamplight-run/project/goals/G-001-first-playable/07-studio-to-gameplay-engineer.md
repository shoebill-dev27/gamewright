---
kind: handoff
goal: G-001
seq: 7
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 07: studio → gameplay-engineer — Apply the Night 3 first-screen answer, make tests agree with the spec, deliver a green build

## Task

Rebuild the first playable so it matches the amended `design/first-playable.md` (option a: the first screen of every night draws `~` on the tiles lit by the starting aim), and make `run_tests` (`python3 -m unittest discover -s tests`) pass.

## Context

Goal G-001: first playable of Lamplight Keeper. The first Build pass (handoff 04) produced a build whose `run_tests` had 4 failures. It also exposed a spec contradiction about the first Night 3 screen. The game-designer resolved it (handoff 06) and amended §8 and AC-1. QA needs a green build next.

## Findings

From the Design answer (handoff 06):
- The first screen of every night draws `~` on the tiles lit by the starting aim. Nights 1 and 2 start UP and show no `~`. Night 3 starts RIGHT: its first screen must read `3 ...T~~~` with header `Beam: RIGHT`. The header aim and the drawn lit tiles must always agree.
- No ship movement or mechanic changes. No ship stands on (3,4)-(3,6) at turn 0, and lit status is judged after the first command.
- Spec §2, AC-3 and the amended §8 and AC-1 now agree with each other.
- Forecast order: the spec does not fix it. §6 gives `L -> LEFT, H -> UP, R -> RIGHT` only as an example, and AC-15 requires only the correct aim for each of `L`, `H`, `R`. The build prints `L, R, H`, and 4 tests expect `L, H, R`. Either order complies. You decide (implementation detail). Make the build, the tests and `repo/manual.md` agree with each other. If you find a case that needs one fixed order in the spec, hand back to the designer and do not decide it yourself.
- The "provisional" status of `DRAW_LIT_ON_FIRST_SCREEN` is gone: option (a) is final. Remove the constant or fix it as True, with no remaining toggle.
- The other failures from the Build check (handoff 04) must also be fixed. Where a test disagrees with the spec, the spec wins. If the spec is ambiguous, contradictory or missing a case, stop and hand back; do not decide.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Not reopened.

## Constraints

- Python 3 standard library only; deterministic; text output only; all changes inside `repo/`.
- No mechanics changes and no change to the behavior of Nights 1 and 2.
- `repo/manual.md` is all a player is told: keep it accurate for what you build, including the forecast order.
- Do not edit the design documents or Decisions.
- Do not expand scope (no new nights, no new mechanics).

## Open questions

- None for you. The two Review questions (mid-night arrivals, wrecks always losing the night) stay with `game-director`.

## Expected output

- The changed build and tests, with a short build note: what changed, the forecast order chosen, and the result of `run_tests`, which should be green.
- Address the result to `studio`: it composes the next Handoffs (QA first, then the Playtester) from permitted information only. Put your reasoning and self-test verdicts in `## Sender assessment`.
- If a test or the build cannot be reconciled with the spec, hand back (`outcome: question`) naming the exact conflict.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/first-playable.md; repo/lamplight.py; repo/tests/test_game.py; repo/manual.md; repo/play.py; goals/G-001-first-playable/04-gameplay-engineer-to-studio.md (failing tests and Build check)
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/06-game-designer-to-studio.md
