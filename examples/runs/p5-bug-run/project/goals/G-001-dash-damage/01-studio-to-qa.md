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

Reproduce the Owner's reported defect and write a precise defect report with acceptance criteria, using the `reproduce-defect` skill.

## Context

Goal G-001. The Owner reported (verbatim): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 (Translation: "I sometimes take damage even while dashing. It's reproducible, so please fix it.") No reproduction steps were given. Intended behavior is expected to be in `design/combat.md` (damage and invulnerability rules), but the Studio has not read it; you must check it.

## Findings

Nothing yet. This is the first step.

## Decisions already made

D-001: combat is one attack button plus dash. Not directly affected, but no new buttons may be added.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate, and report the result for both.
- Use the input-script workflow in `manual.md`: `run_play` for the player view, `run_trace` for simulation state, `run_tests` for the existing tests.
- Do not diagnose the root cause in code or fix anything; that belongs to the engineer.

## Open questions

- Under what exact conditions (enemy type, timing within the dash, position, frame rate) does damage occur during a dash?
- What do the design documents say the player's state should be at that moment (invulnerable or not, for which part of the dash)? Quote the relevant text.
- Is the observed behavior a contradiction of the documents, or are the documents silent, ambiguous or contradictory about this case?
- If the defect cannot be reproduced with the information available, say exactly what is missing.

## Expected output

A defect report: minimal reproduction script(s), observed vs. expected behavior (with the design reference), frame-rate dependence, severity, and player-observable acceptance criteria for the fix, including a regression check at 30 and 60 FPS. Write it as the outgoing Handoff.
- If the intended behavior is documented and violated: set `to` to `gameplay-engineer`, `outcome: done`.
- If the intended behavior is undefined, ambiguous or contradictory: set `to` to `game-designer`, `outcome: question`, naming the gap.
- If the defect cannot be reproduced: `outcome: question`, and state what is needed; the Studio will decide on an Owner escalation.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, project.md#current-state, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none
