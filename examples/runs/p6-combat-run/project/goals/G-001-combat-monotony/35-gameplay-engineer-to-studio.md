---
kind: handoff
goal: G-001
seq: 35
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 35: gameplay-engineer → studio — F1/AC-18 and F3 built with tests; `manual.md` paragraph NOT placed (path not writable; Owner action needed)

## Task

Route the `manual.md` edit to the Owner, then open Verify (QA, art director) for the rendering change.

## Context

Handoff 34: Build 0.5, render fix for enemies on the player's tile (F1, AC-18, D-006), enemy-over-arc priority (F3), and the practice-room paragraph in `manual.md#on-screen` (AC-15).

## Findings

### Done: rendering only (`repo/play.py`); `game.py` is untouched

- No rules, timing, hit-test, trace or input change. The display offset lives in the `Player` view class.
- **Displaced cell, as built.** A living enemy whose drawn cell equals the player's cell is drawn in a free in-room cell beside the player. The order tried is:
  1. the side it was last seen on, in a different cell from the player's. This is tracked once per simulation frame, so it covers the side it approached or struck from, as a unit step right, left, above or below;
  2. then right, left, above, below;
  3. if all four are taken or off-room, the free cell nearest the player (ties: top row first, then left);
  4. an enemy that has never been seen in another cell (for example a `spawn` on the player) has no side history, so it starts at right, left, above, below.
- Cells already holding another enemy, or `P`, count as taken, so two overlapping enemies get different cells. Enemies not on the player's cell keep their true cell.
- It applies in every state, to grubs and spitters, damaged glyphs and the immediate event draws. Text lines are unchanged, including "(on you)". `x` stays on the player's own cell when down.
- A displaced enemy is not moved in the simulation. A swipe still hits by true position, so the arc can point away from the drawn glyph, as D-006 states.
- **F3.** The arc now fills only empty tiles. Enemy glyphs, displaced ones included, and `P`/`x` are drawn on top. The `w` is visible in the hit draw at 30 and 60 FPS, and `)` still shows on the empty reach tiles.
- Shots are drawn before enemies, so an enemy glyph wins a cell shared with `*`. This is a side effect and is not in the spec. The previous code also drew enemies after shots.
- **F2 (out-of-order timestamps at 30 FPS): not touched.**

### Tests (`repo/tests/test_game.py`)

- New `VisibilityTest`, run at 30 and 60 FPS:
  - AC-18 grub case: practice room, grub at distance 4, run to 5.5 s. Every draw has exactly one grub glyph. `P` or `x` is visible. Each "a grub rears back" line is followed by a draw with `G`/`W`. Each "the grub is open (on you)" line is followed by a draw with `g`/`w`. The test also asserts that the "(on you)" wind-up case actually occurs.
  - AC-18 spitter case: `player 8 4`, `spawn spitter 8.2 4`. In every draw `P` and `s`/`S` are in neighbouring cells, and `S` appears.
  - Two overlapping grubs take different cells, and a down player keeps `x` with the enemy beside it.
  - F3: the hit draw shows `w` and `)`, both for a grub beside the player and for one on the player's cell.
- New `ManualTest.test_on_screen_section_lists_x_and_the_practice_room` checks that the On screen section contains `x` and the exact paragraph text.
- `run_tests` result, round 1 on these files: Ran 40 tests, FAILED (errors=2). The only 2 errors are both `ManualTest` tests (`test_manual_lists_glyphs_and_lines`, `test_on_screen_section_lists_x_and_the_practice_room`), `FileNotFoundError: '/manual.md'`. All other 38 tests passed, including the new `VisibilityTest`. I made no changes to the code after that run, only to this note.
- **`manual.md` location when I ran `run_tests`:** it was absent. The workspace root was `/work`, so the test looked for `REPO.parent / "manual.md"` = `/manual.md`. It would pass if `manual.md` sits one level above the directory that holds `tests/`, `play.py` and `game.py`.
- I did not run the trace or the bots with these files. The change is in the player view only, and `game.py` is unchanged, so AC-1…AC-4 timings and hearts cannot change. QA should confirm this with the C1/C7 trace repeats.

### Blocked: `manual.md` paragraph (AC-15, ruling 2)

- **Exactly what blocked me:** the packet's "You may write" list contains only the handoff path and `repo/<path>`. `manual.md` is outside that list, so I could not write it.
- **Not completed:** the paragraph is not in `manual.md`, so AC-15 does not hold yet. The new `ManualTest` test fails until the paragraph is placed.
- **Needed from the Owner (D-005):** in `manual.md`, section `## On screen`, after the mark table and before the "With color on…" paragraph (or directly after it; the section must contain it), insert this paragraph with no changes to the wording:

  > The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

- Nothing else in `manual.md` changes. The glyph table and the required phrases stay.
- **For the Owner when running `run_tests`:** `manual.md` must sit beside `repo/` for both `ManualTest` tests to run.
- This is the third round in which `manual.md` could not be written. Per handoff 34 it goes to the Owner and not to a Role again.

## Decisions already made

D-001 (no inputs), D-002 (Option A), D-004 (one change set), D-005 (Owner places `manual.md`), D-006 (overlap display, practice-room listing).

## Constraints

Rendering only; 30/60 FPS; no rules, timing or input change.

## Open questions

1. **Owner:** place the `manual.md` paragraph (above), with `manual.md` beside `repo/`.
2. For the art director's readability check: the order of the displaced cell is above. Known edge case: a displaced glyph on the side it last came from can sit where the swipe arc would otherwise appear, so the arc then shows one tile fewer. This is by the F3 rule.

## Expected output

After the Owner places `manual.md`, QA verifies AC-15 (both `ManualTest` tests green), AC-17, AC-18 and the C1/C7/C3 repeats at 30 and 60 FPS. The art director then does the visual re-check (V-1, F1, F3, and V-6 with a `--color` capture, still open).

## Sender assessment

Confidence is good in the renderer and tests: 38 of 40 tests passed in the run, and the 2 failures are only the missing `manual.md`. The weakest point is the side-history rule. It is a per-frame cell approximation, not the exact side of the strike lunge. If the art director finds a displaced glyph misleading, change `track()`/`free_cell()` in `play.py` only.

## Load

- Role: studio/roles/qa.md (after the Owner step)
- Skills: none
- Project: design/combat.md, design/combat-visuals.md, manual.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/34-studio-to-gameplay-engineer.md
