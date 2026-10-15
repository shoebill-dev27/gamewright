---
kind: handoff
goal: G-001
seq: 38
from: studio
to: qa
stage: Verify
outcome: routed
---
# 38: studio → qa — Verify AC-15 (practice-room paragraph in `manual.md`) and run `ManualTest`

## Task

Verify AC-15 against the build and `manual.md`. Read the `## On screen` section of `manual.md` and check that it contains the practice-room paragraph below, word for word. Then run `run_tests` and report the result of the two `ManualTest` tests in particular.

## Context

Goal G-001 (combat feels monotonous) is in Verify. In earlier rounds `ManualTest` had no valid result: the QA and engineer workspaces lacked `manual.md`. The Owner has now added the paragraph (D-007). A separate Verify step (37) covers the other acceptance criteria and does not cover AC-15. Do not repeat that work except where AC-15 needs it.

## Findings

Nothing to report from earlier work for this check. The Owner states they appended the following paragraph at the end of `## On screen`:

> The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

This is the Owner's statement; verify it independently.

## Decisions already made

- D-005: the Owner places `manual.md` content. Roles do not edit it. Report problems, do not fix them.
- D-006: the practice room is listed in the On screen section; enemies may overlap the player but are never hidden.
- D-007: the Owner placed the paragraph above (Option A).

## Constraints

- `manual.md` must sit beside `repo/` in your workspace, because `ManualTest` reads it there. If it is missing, report that as a blocker. Do not call it a test failure.
- Do not edit `manual.md` or the build.
- Use the project's run commands: `run_tests`, and `run_play` / `run_trace` with your own input scripts.

## Open questions

- Is the paragraph present in `## On screen`, word for word and inside that section?
- Do the two `ManualTest` tests pass with `manual.md` placed?
- Does the behavior the paragraph describes match the build? Check with scripts: the practice room is not part of a run, enemies appear only where `spawn` places them, nothing heals, there is no next room, the session ends shortly after you go down, and an enemy on the player's tile is drawn on a free adjacent tile.

## Expected output

A pass/fail report on AC-15, covering the paragraph check, the `ManualTest` results, and the behavior checks, with raw command output as evidence. Address the result to `studio`. If anything cannot be run, say what is missing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: manual.md; design/combat.md (AC-15, AC-18); project.md#current-state; repo (build; use `run_tests`, `run_play`, `run_trace`)
- Decisions: decisions/D-005-owner-places-manual-draft.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-007-practice-room-paragraph-placed-by-owner.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
