---
kind: handoff
goal: G-001
seq: 68
from: studio
to: qa
stage: Verify
outcome: routed
---
# 68: studio → qa — Verify the combat response change set (AC-1…AC-28, V-9…V-17) at 30 and 60 FPS

## Task

Verify the current build in `repo/` against the acceptance criteria in `design/combat.md` (AC-1…AC-28) and the player-visible criteria in `design/combat-visuals.md` (V-9…V-17, with earlier V items as regression). Run each check at both 30 and 60 FPS where the criterion depends on timing. Report pass/fail per criterion, plus regressions.

## Context

Goal G-001, "Combat feels monotonous". The Owner chose to rework existing enemy behavior first (D-002, Option A). A change set has just been built on the existing simulation: grub turn-taking and spacing between Wind-ups, a cap on grubs engaged near the player, shorter hit-stun, a body hit, dash facing, miss causes, a hit in Strike cancelling the strike, knockback of a grub on the player's tile, an `on you:` line, and attacker position in hit lines. The previous verification round (AC-1…AC-27 earlier set) passed or was settled by the Owner's suite runs (D-008, D-010). This round covers the new and changed criteria and checks the old ones for regressions.

## Findings

Nothing to forward from the implementation beyond how to exercise it. Verify from the spec, the criteria and the build.

How to exercise (from `project.md`; the project directory is the one containing `manual.md` and `repo/`):

- Tests: `python3 -m unittest discover -s tests` (run in `repo/`). The manual tests read `manual.md` at the project root, one level above `repo/`. Run the whole suite with it in place and report the counts and any failure by name.
- Player view: `python3 play.py --view player {script}`; trace view: `python3 play.py --view trace {script}`. Script format is in `manual.md`.
- Balance bots: `python3 bots.py {script}`. Run at both frame rates for reference data on room 1 and room 2 (clear time, hearts lost, actions used); report the numbers without judging balance.

Items left unobserved by earlier rounds, to check first-hand against the spec:

- The `(miss)` text with its cause, in the player view.
- Knockback of a grub standing on the player's tile in open floor (AC-28), and near a wall.
- A hit in Strike at 30 FPS (the earlier open point D-58-1; the spec rule is in `design/combat.md`).
- Engagement cap and Wind-up spacing in room 2 with the player standing still, at both frame rates.

Also read `manual.md` against V-15 and the AC-15 wording. The Owner may not yet have placed all draft text there (open Owner step); report what is and is not present, and whether any missing text is needed by a criterion. Do not edit `manual.md`.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-009: the manual phrase check ignores line wraps.
- D-010: AC-15 passed on the Owner's suite run (40/40) for the earlier build.
- D-011: grubs take turns, crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line for an enemy on the player's tile; hit lines name the attacker position.
- D-013: a grub on the player's tile is knocked back toward the side it is drawn on.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Do not edit the repo or `manual.md`. If something cannot be run in your environment, report exactly what is needed (for example the Owner running the suite, as in D-008) instead of guessing.
- A criterion failing for the second time goes to re-planning (orchestration, loop limits). Say in the report which criteria failed before, if the earlier reports show it.

## Open questions

None. If a criterion is undefined or ambiguous, say so and name it.

## Expected output

A verification report with per-criterion pass/fail (AC-1…AC-28, V-9…V-17, regressions), suite counts, bot numbers at both frame rates, and an explicit list of what you could not observe. Address the result to `studio` (the Studio composes the next step from it).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/ (build: run commands in project.md)
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-010-owner-ran-suite-ac15-passes.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: none (composed fresh without the implementer's assessment)
