---
kind: handoff
goal: G-001
seq: 13
from: studio
to: qa
stage: Observe
outcome: routed
---
# 13: studio → qa — Reproduce the walker bot's different results at 30 and 60 FPS in rooms 3–5

## Task

Determine whether the walker bot's differing results at 30 and 60 FPS in rooms 3–5 come from the build (the simulation behaves differently at the two rates) or from the bot's own behavior. Write a defect report with reproduction steps if it is a build defect.

## Context

G-001 (combat monotony). The project must play correctly at 30 and 60 FPS. A previous QA pass (`goals/G-001-combat-monotony/08-qa-to-studio.md`) found the simulation matching within one frame in traced cases. Since then the build was updated (0.5: new enemy behavior, bots decide on a 0.15 s accumulated-time grid).

## Findings

Reported observation (`python3 bots.py {script}`, bots `camper,walker,dodger`, `rooms 1-5`, `fps 30` and `fps 60`), walker hearts lost per room 1/2/3/4/5:

- 30 FPS: 3✗ 2✓ 0✓ 1✓ 3✗ (✓ cleared, ✗ not cleared)
- 60 FPS: 3✗ 2✓ 2✓ 2✓ 2✓

The dodger bot agrees at both rates (0 hearts lost, all cleared). The `bots` option `log on` in a script prints each bot decision under the room line (see `repo/README.md`).

## Decisions already made

- D-001: one attack button plus dash; no new input.

## Constraints

- Intended behavior is defined by `design/combat.md` and `repo/manual.md`. A difference caused only by a bot's decision timing is not a build defect, but say so with evidence.
- Do not fix code. Report only.

## Open questions

1. Is the divergence reproducible and deterministic?
2. Is it caused by the build simulation (enemy timers, movement, collision, damage at different frame rates) or by the walker's decisions? Identify the first point where the two runs differ, using `log on` and `run_trace`.

## Expected output

A report: reproduction commands, the first divergence point and its cause, severity, and, if it is a build defect, acceptance criteria for a fix. Address the result to `studio`. Full verification of criteria 1–16 follows in a later step.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, repo/README.md, repo/bots.py, repo/game.py, repo/play.py, repo/tests/test_game.py, project.md#constraints, the build (repo/; run_bots, run_trace and run_play in project.md)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/08-qa-to-studio.md
