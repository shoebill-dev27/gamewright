---
kind: handoff
goal: G-001
seq: 76
from: studio
to: qa
stage: Verify
outcome: routed
---
# 76: studio → qa — Verify the D-014 rebuild at 30 and 60 FPS and capture the player view for the art-director

## Task

Verify the rebuilt `repo/` (sha cf0f0ee63752) against the acceptance criteria below, at both 30 and 60 FPS. Report pass/fail per criterion. Also capture the player view verbatim for the visual review (see Expected output).

## Context

G-001 (combat feels monotonous), Option A. Your report 70 failed AC-17, AC-22 (suite), AC-28(b) at 30 FPS, V-10, V-14 and V-16, and V-15 (the manual text, an Owner step). The game-designer ruled three spec gaps in 73 (D-014). The gameplay-engineer then rebuilt: cell rule at .5, one meaning of "on you", the side word of an enemy not on you, the hit-line word fixed at Strike start, knockback of an on-you grub, and a fix to the hit-stun test.

This is the first failure of each item from 70, so a failure now is also a first failure. A second failure of the same criterion goes to the technical-director.

## Findings

Facts about the change (not a verdict):

- Changed files: `repo/game.py`, `repo/play.py`, `repo/tests/test_game.py`. `repo/bots.py`, `manual.md` and the design documents are unchanged.
- The test suite in `repo/tests/` was edited, including two tests (`CellRuleTest.test_line_words_match_the_next_draw`, `KnockbackTest.test_edge_grub_is_shown_and_knocked_left`) and `CrowdTest.test_hit_stun_is_short`. Judge whether these tests match the spec, not only whether they pass.
- The build environment of the last engineer run had no `manual.md`, so the two `ManualTest` tests could not be run there. Run the suite with `manual.md` available beside `repo/` if your environment allows it. If it does not, report that and the rest of the suite result. AC-15 is also being run by the Owner (route step 13e-O).
- Scripts to exercise (run each at `fps 30` and `fps 60`, in the player view and the trace view):
  - AC-28(b): `player 14.5 4`, `spawn grub 14.5 4`, `0.2 attack`, `end 2`.
  - AC-29: `player 14.5 4`, `spawn grub 13.5 4`.
  - Knockback of a grub close to the player: `spawn grub 8.2 4` and `spawn grub 8 4`.
  - AC-30: `room 2` with a still player for 6 s.
  - V-14: grubs at 9.25 and 6.75, only the right one striking.
  - Also AC-28(c), the AC-30(a) draw-by-draw check, and spitter views.
- Items unobserved in 70 §6 are still to be observed where possible: AC-1, 3, 9, 10, 12, 28(c); real-room clear, heal and next room, and "run complete" (AC-13, 14); spitter player-view runs; V-6, V-7, V-8.
- AC-21 (the margin): re-measure it. AC-2, 4, 5, 7, 11, 19, 21, 23–27, AC-28 a/d/e, V-9, V-11 and V-17 passed in 70 and should be re-checked for regressions.

## Decisions already made

- D-001: one attack button plus dash.
- D-011: grubs take turns, crowd two deep, hit-stun 0.15 s, body hit, dash sets facing.
- D-012: `on you:` line for displaced enemies; the attacker's position in hit lines.
- D-013: knockback of a grub on the player's tile.
- D-014: one rule for cells, sides, "on you" and the hit-line word.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Verify from the spec, the acceptance criteria and the build only. You have not been given, and should not seek, the engineer's explanation of why it works.
- Do not change the repo, `manual.md` or the design documents. Report problems; do not fix them.
- V-15 (manual text) depends on the Owner placing the text. Judge it only if it is in place; otherwise report it as not checkable.

## Open questions

- Where the spec leaves expected behavior undefined, say so precisely (that goes to the game-designer).

## Expected output

A QA report addressed to `studio` (`77-qa-to-studio.md` is the next free number if no other artifact intervenes), with:

1. A pass/fail/not-observed table by criterion, with both frame rates, covering at least: AC-17, AC-22, AC-28(a, b, c), AC-29, AC-30, V-10, V-12, V-14, V-16, V-18, V-15 (if checkable), the AC-15 `ManualTest` result (or why it could not be run), and the items unobserved in 70.
2. A regression check of the items that passed in 70.
3. Verbatim player-view captures at 30 and 60 FPS of the six setups listed in `goals/G-001-combat-monotony/71-art-director-to-studio.md`, so the art-director can review from them without running the build.
4. For each failure: the exact script, the frame rate, observed versus expected output, and whether it is a first or second failure of that criterion.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py, goals/G-001-combat-monotony/71-art-director-to-studio.md, goals/G-001-combat-monotony/73-game-designer-to-studio.md
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/70-qa-to-studio.md
