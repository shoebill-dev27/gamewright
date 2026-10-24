---
kind: handoff
goal: G-001
seq: 37
from: studio
to: qa
stage: Verify
outcome: routed
---
# 37: studio → qa — verify the rendering change (build 0.5) except the manual check

## Task

Verify the current build against AC-17 and AC-18 in `design/combat.md` (and the D-006 display ruling), and confirm that nothing else changed. Do not judge AC-15 (manual text): it is waiting on the Owner, so report `ManualTest` as not run, not as a failure.

## Context

G-001 (combat feels monotonous). The enemy rework is built. The last Build step changed only how the player view draws enemies: an enemy standing on the player's tile must never be hidden (AC-18, D-006), and enemy glyphs must be visible over the swipe arc. The simulation (`game.py`) is meant to be unchanged, so the timings, hearts and hit results from earlier verification should be identical. The previous QA pass (29) repeated scripts C1, C7 and C3 and captured raw output; those are the baseline.

## Findings

None to hand over. Work from the acceptance criteria and the build.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; the practice room is listed in the manual's On screen section.
- D-001: no new inputs.

## Constraints

- Play correctly at 30 and 60 FPS: run each check at both.
- Run through the project's commands (`run_tests`, `run_play`, `run_trace`, `run_bots`).
- `manual.md` may be missing from your workspace. If so, the two `ManualTest` errors are an environment matter. Do not count them against any AC.

## Open questions

None.

## Expected output

A pass/fail report per criterion, with exact scripts and the raw output you rely on. Cover:
1. AC-17 and AC-18 (grub and spitter on the player's tile, wind-up and strike draws, a down player, two enemies overlapping).
2. Repeats of C1, C7, C3 at 30 and 60 FPS compared with the earlier results: timings, hearts and hit results should be unchanged.
3. The hit draw with the swipe arc: the enemy glyph is visible over the arc.
4. Raw captures for the art director's visual re-check: grub on the player's tile in wind-up, strike and recovery draws, a spitter on the tile, a swipe after a miss, the 60 FPS charge-start draw, and one `--color` capture.
5. Anything not verifiable.

Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, manual.md, repo/ (build; run commands in project.md)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
