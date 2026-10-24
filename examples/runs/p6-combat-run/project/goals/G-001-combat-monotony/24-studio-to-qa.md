---
kind: handoff
goal: G-001
seq: 24
from: studio
to: qa
stage: Verify
outcome: routed
---
# 24: studio → qa — verify Build 0.5 against the combat spec (AC-1…AC-17)

## Task

Verify the current build in `repo/` against the acceptance criteria in `design/combat.md` (AC-1…AC-17) and the run and room rules in D-003. Check for regressions, including at both 30 and 60 FPS. Report pass/fail per criterion.

## Context

Goal G-001 (combat feels monotonous). Option A (D-002) reworks existing enemy behavior, built as one change set (D-004). Build 0.5 is ready for independent verification. This Handoff is composed by the Studio and contains no implementer reasoning. Verify from the spec and the build.

## Findings

- Build: `repo/`, run through the project's run commands: `run_tests`, `run_play`, `run_trace`, `run_bots` (see `project.md` front matter). Controls and script format are in `manual.md`.
- `run_tests` layout: `ManualTest` reads `manual.md` from the directory above `repo/`. Run the tests in a layout where `manual.md` sits next to `repo/`, as in the project directory. Report the `ManualTest` result separately. The Owner placed `manual.md` (D-005); one earlier test run in a layout without it errored with FileNotFoundError, so that test has no valid result yet.
- Known scope limit: the pause behavior (F11 in the plan) is not implemented. Mark it "not verifiable", not as a failure.
- AC-8 (the doubled spit line when two spitters print identical text) and AC-15 (`manual.md` content) are in scope.
- Visuals (colors, glyph readability; `design/combat-visuals.md`) are reviewed in parallel by the art-director. Check only what the acceptance criteria in `combat.md` state about them.

## Decisions already made

- D-002: Option A, rework existing enemy behavior first.
- D-003: room mix is across rooms; zero hearts ends the run; a room clear heals one heart.
- D-004: one sequential change set on the existing simulation.
- D-005: the Owner placed the draft `manual.md` unchanged.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Do not edit the build. Report failures with a script that reproduces them.

## Open questions

- If `manual.md` cannot be placed next to `repo/` in your workspace, say so exactly. Do not mark `ManualTest` pass or fail. Report it as blocked on the Owner.

## Expected output

A pass/fail report per criterion (AC-1…AC-17) plus the `run_tests` totals, regressions found, and items not verifiable, each with reproduction scripts for failures. Address the result to `studio`. The result is used to compose the playtester's Handoff without implementation history.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: project.md, design/combat.md, manual.md, repo/ (build), repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: none (composed by the Studio; earlier handoffs contain the implementer's self-assessment)
