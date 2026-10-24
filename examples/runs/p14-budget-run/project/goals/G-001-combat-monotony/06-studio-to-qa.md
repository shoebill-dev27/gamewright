---
kind: handoff
goal: G-001
seq: 6
from: studio
to: qa
stage: Observe
outcome: routed
---
# 06: studio → qa — Reproduce the 30 vs 60 FPS difference in bot results and check dash invulnerability

## Task

Reproduce and report whether the build behaves differently at 30 and 60 FPS, using the balance bots, and check that the dash invulnerability in the build matches `design/combat.md`.

## Context

Goal G-001 is about improving combat variety. Before combat is changed, the team needs to know whether the current build plays correctly at both 30 and 60 FPS, which is a project constraint. A team member observed a discrepancy when running the bots. No change to the build is wanted in this step.

## Findings

Reported observation (not yet reproduced or explained), from `run_bots` over rooms 1–5 at both rates:

- The dodger bot (uses dashes), room 3: at 60 FPS it failed (19.7 s, 13 dashes, 3 hearts lost). At 30 FPS it cleared (9.5 s, 0 hearts lost, 4 dashes).
- The dodger bot, room 4: 21.8 s at 60 FPS and 17.8 s at 30 FPS.
- The walker and camper bots gave the same results at both rates.

It is not known whether the difference comes from the build or from how the bot works.

## Decisions already made

None.

## Constraints

- Must play correctly at both 30 and 60 FPS (project.md#constraints).
- Do not change the build or the bots. Report only.
- `run_bots` takes a script argument; see `repo/README.md`, `repo/manual.md` and `repo/bots.py` for the correct format and how to set the frame rate. Earlier attempts with a wrong script format produced no output.
- Also use `run_trace` and `run_tests`. Report reproducibility, the conditions needed to reproduce it, and severity.

## Open questions

- Is the difference reproducible, and is it deterministic (same result on repeated runs)?
- Does the simulation itself (enemy timing, shot timing, damage, dash duration, cooldown) differ between 30 and 60 FPS, or only the bot's decisions?
- Does the dash make the player invulnerable for its full duration in the build, as `design/combat.md` says, at both rates?

## Expected output

A defect report (or a report that nothing reproduces) with reproduction steps, observed vs expected behavior and acceptance criteria if a defect is confirmed. If it cannot be determined whether the build or the bot is at fault, say so and state what was ruled out. Write the outgoing Handoff addressed to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, repo/README.md, repo/manual.md, repo/bots.py, repo/play.py, repo/game.py, repo/tests/test_game.py
- Decisions: none
- Previous handoff: none
