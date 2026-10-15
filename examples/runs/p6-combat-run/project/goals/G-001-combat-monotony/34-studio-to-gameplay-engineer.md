---
kind: handoff
goal: G-001
seq: 34
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 34: studio → gameplay-engineer — render fix for enemies on the player's tile and under the swipe arc; add the practice-room text to manual.md

## Task

Implement two rendering-only changes in the player view of Build 0.5, with tests, and place one paragraph in `manual.md`. Address the build notes to `studio`.

## Context

Goal G-001 (combat feels monotonous), Option A (D-002), Build 0.5. Verify found no failing AC, but the art director's visual review (32) failed V-1: in "a grub rears back (on you)" draws, the committed grub is hidden under `P`. The game-designer ruled on this (33, D-006) and added AC-18 to `design/combat.md`. The art director also found F3 (the swipe arc hides the hit enemy). The designer also reworded AC-15.

## Findings

### Change 1 — F1: no living enemy is hidden under `P` (spec: D-006, AC-18)

- Gameplay stays unchanged: enemies and the player still have no collision (the dash passes through enemies). Hit tests, damage radius, timings and the swipe use true positions. Only the drawing changes.
- If a living enemy's cell equals the player's cell, draw its glyph in the nearest free in-room cell beside the player. Try first the side it last approached or struck from, then right, left, above, below. Two overlapping enemies take different cells.
- It applies in all states, including the "open (on you)" counter window, to grubs and spitters, and to the immediate event draws (wind-up, charge, swipe).
- Text lines stay as they are, including "(on you)". `x` is still drawn on the player's own cell when down.
- AC-18 (full text in `design/combat.md`):
  - Practice room, idle player, grub at distance 4, run to 5.5 s at 30 and 60 FPS: every draw with a living grub shows it in a cell other than `P`'s. Each "a grub rears back" line (including "(on you)") has `G`/`W` visible in that draw, and each "the grub is open (on you)" has `g`/`w` visible.
  - `player 8 4`, `spawn spitter 8.2 4`: `P` and `s` are in neighbouring cells, and `S` is beside `P` during its Charge.
  - Timings, hearts and trace positions stay within the AC-1…AC-4 tolerances. AC-17 now includes AC-18.

### Change 2 — F3: enemy glyphs draw over the swipe arc (art director, 32)

- In the draw right after "you swipe: grub hit (1 left)", the arc `)` was drawn over the grub's tile and the `w` was not visible (30 FPS draw [2.53] in QA's capture C3; the 60 FPS draw is identical).
- Cell priority rule: enemy glyphs draw over the arc, and the arc fills only empty tiles. A committed (uppercase) enemy always wins its cell. The hit-confirming glyph change (`g`→`w` etc.) must be visible in the same draw as the hit line.
- This is a drawing-only change. Acceptance: repeating the C3 script shows the damaged glyph (`w`) in the hit draw at 30 and 60 FPS, and the arc `)` still shows on the empty tiles of the reach.

### Change 3 — `manual.md` (AC-15, designer ruling 2)

`x` and the practice room must both be listed in the `manual.md#on-screen` section. Add this paragraph in the On screen section, after the mark table, with the wording unchanged (the designer's text in 33):

> The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

- `manual.md` is the Owner's draft (D-005). Change only this paragraph. The glyph table and the phrases the tests require ("room empty", "(miss)" and the others) must stay.
- Keep `ManualTest` valid: in the earlier rounds the engineer's and QA's workspaces lacked `manual.md` beside `repo/`. State in your notes where `manual.md` stood when you ran `run_tests`.

### Not in this change

- F2 (out-of-order timestamps in the player view at 30 FPS): the art director rules it cosmetic and the designer did not rule on it. Do not change it unless it falls out of the work without risk. If you touch it, say so.
- No change to rules, timings, parameters or inputs (D-001).

## Decisions already made

- D-001: no new inputs. D-002: Option A. D-004: one sequential change set on the existing simulation. D-005: the Owner places `manual.md`. D-006: enemies may overlap the player but are never hidden; the practice room is listed in the On screen section.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Prefer reuse of the existing renderer; small team.
- Stop and hand back with a `question` if the spec is ambiguous, contradicts itself, or misses a case (for example, no free cell beside the player). Do not decide it yourself.

## Open questions

- If you cannot write `manual.md` (as happened twice before), say exactly what blocked you and which parts you did complete. The Studio will not route this to a Role a third time with nothing new; it goes to the Owner.
- Name the as-built choice of the displaced cell (the order tried, edge cases) in your notes, for the art director's readability check.

## Expected output

Code change plus tests for AC-18 and F3, the `manual.md` paragraph, and the `run_tests` result (all tests, including `ManualTest`, with the `manual.md` location). Build notes address the result to `studio`. The Studio then opens Verify: QA (AC-15, AC-17, AC-18, C1/C7/C3 repeats at 30 and 60 FPS) and the art director for the visual re-check.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-visuals.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-001-one-button-combat.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/33-game-designer-to-studio.md (also for F3: goals/G-001-combat-monotony/32-art-director-to-studio.md)
