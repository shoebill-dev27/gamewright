---
kind: handoff
goal: G-001
seq: 1
from: studio
to: qa
stage: Observe
outcome: routed
---
# 01: studio → qa — Reproduce "damage taken while dashing" and write a defect report

## Task

Reproduce the reported defect: the player sometimes takes damage while dashing. Find the precise conditions that trigger it and write a defect report with acceptance criteria, following `reproduce-defect`.

## Context

Goal G-001. The Owner reported this in Japanese (verbatim):

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

Translation: "I sometimes take damage even while dashing. It's reproducible, so please fix it."

The Owner gave no reproduction steps. Nothing has been investigated so far. The project is a small headless build in `repo/`, played through input scripts. `run_play` shows what the player sees, `run_trace` shows simulation state, and `run_tests` runs the existing tests (see `project.md` front matter and `manual.md`).

## Findings

None yet. This is the first step.

## Decisions already made

- D-001: combat uses one attack button plus dash. No new input buttons.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate.
- Judge the defect against the intended behavior in `design/combat.md` (damage and invulnerability rules). Report exactly what the document says about dash and damage, and quote it.
- Do not propose or implement a fix, and do not speculate about code causes. The root cause is the engineer's decision. You may record trace observations as evidence.
- Do not change the design. If the documents do not define the intended behavior for the conditions you find, say so plainly.

## Open questions

- Under what exact conditions is damage taken during a dash (which enemy or attack, which moment of the dash, positions, frame rate)?
- Does `design/combat.md` define the intended behavior for those conditions?

## Expected output

A defect report (using `reproduce-defect`) that includes:
- the input script(s) that reproduce it, and how often it reproduces;
- the observed behavior, with player-view and trace evidence;
- the expected behavior, quoting the design document;
- severity and reproducibility;
- acceptance criteria that are player-observable and stated for both 30 and 60 FPS.

Put the report in the Findings of your outgoing Handoff (templates/handoff.md) and set `to` as follows:
- Reproduced and the intended behavior is specified: `to: gameplay-engineer`, `outcome: done`.
- Reproduced but the design documents leave the intended behavior undefined: `to: game-designer`, `outcome: done`, with the gap stated in Open questions.
- Cannot reproduce, or the Owner must supply details only they have: `to: studio`, `outcome: question`, stating exactly what is missing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md (Vision, Constraints, Current state), design/combat.md, manual.md, repo/README.md, the build in `repo/` (run with `run_play` and `run_trace`)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none
