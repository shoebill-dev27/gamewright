---
kind: handoff
goal: G-001
seq: 43
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 43: studio → game-designer — rule on the `run over` phrase that `ManualTest` expects in `manual.md`

## Task

Decide why `test_manual_lists_glyphs_and_lines` fails and what the correct fix is. Either the player-facing `manual.md` should mention `run over` and does not, or the test's expectation is stale or wrong against the spec. Write the ruling so that the next step can act without guessing.

## Context

Goal G-001 (combat feels monotonous) is in Verify. Everything behavioral passed in 39. The only open item for AC-15 (the manual describes what the player sees, including the practice room) is a `ManualTest` check. QA could not run `ManualTest` in its workspace, because the test reads `REPO.parent / "manual.md"` and that file is absent there. The Owner then ran the whole suite in an environment where `manual.md` sits next to `repo/` (escalation 42, D-008). Result: 39 of 40 pass. The failing test is `test_manual_lists_glyphs_and_lines` (`test_game.ManualTest`). Failure: `AssertionError: 'run over' not found in manual.md` at `tests/test_game.py` line 631 (`self.assertIn(phrase, text, phrase)`). The other `ManualTest` test, `test_on_screen_section_lists_x_and_the_practice_room`, passes. QA's earlier static check found the practice-room paragraph identical to D-007 and the practice-room behavior matching the build (40), but it could not cover this test.

## Findings

- Failing check: the test iterates over a list of phrases and asserts that each appears in the text of `manual.md`. `run over` is the first (or only) phrase reported missing. The assertion stops at the first missing phrase, so other phrases in the same list may also be missing. Read the test to see the full list.
- `run over` is the line the build shows when a run ends (D-003: zero hearts ends the run). Check in `repo/game.py` / `repo/play.py` what is actually printed, and whether `manual.md` describes the run end in other words.
- `manual.md` is player-facing and Owner-managed (D-005, D-007). You may not edit it. If it needs new text, write the exact proposed wording in your Handoff and the Studio will ask the Owner to place it, as was done for the practice-room paragraph.
- `design/combat.md` AC-15 was reworded in 33. Check whether its wording covers the run-end line, and whether the test checks more than AC-15 requires.

## Decisions already made

- D-003: room mix is across rooms; zero hearts ends the run; room clear heals one heart.
- D-005, D-007: the Owner places `manual.md` text. Roles do not edit it.
- D-006: enemies may overlap the player but are never hidden; the practice room is listed in the On screen section.
- D-008: the Owner ran the suite (39/40); AC-15 is not accepted on a static check; the `run over` question goes to you.
- D-001: no new input buttons.

## Constraints

- Do not edit `manual.md`. Do not edit the code or tests; that is Build.
- Stay inside the approved direction (D-002 Option A) and the existing Decisions. If the ruling would change D-001, D-003 or a vision pillar, hand back with that as an open question instead of ruling.
- Prefer the smallest change that makes the manual, the build and the test agree (small team, reuse existing systems).
- Player-visible text should stay consistent with what `run_play` actually shows.

## Open questions

1. Is `run over` text that the player sees in the build? If yes, should `manual.md` mention it (and is it mentioned in other words)?
2. Does the test check anything beyond what the spec (AC-15) requires? Is any other phrase in that list also missing from `manual.md`?
3. Which fix is right: (a) `manual.md` gets new wording (give the exact text, for the Owner to place), (b) the test's phrase list is corrected (give the exact change, for the Engineer), (c) the build's displayed wording is changed (describe it, for the Engineer), or (d) a combination?

## Expected output

A ruling in this Handoff's Findings (if you change `design/combat.md`, name the section), with:
- the full list of phrases the test expects and which of them are missing from `manual.md`;
- the chosen fix (a–d) with exact wording or test/code change;
- the acceptance check QA should run afterwards (expected: the full `run_tests` result 40/40 in an environment where `manual.md` is beside `repo/`, plus what the Owner or QA must provide for that).

Address the result to `studio`. Set `outcome: done`, or `question` if you need a decision you do not hold.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md (AC-15 and the run-end rules); manual.md; repo/tests/test_game.py (class `ManualTest`, around line 631); repo/game.py and repo/play.py (what the player sees at run end)
- Decisions: decisions/D-003-run-end-and-room-rules.md, decisions/D-005-owner-places-manual-draft.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-007-practice-room-paragraph-placed-by-owner.md, decisions/D-008-manualtest-run-by-owner-one-failure.md
- Previous handoff: goals/G-001-combat-monotony/42-studio-to-owner.md
