---
kind: decision
id: D-008
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-008: The Owner ran `run_tests` for AC-15 (Option A); one `ManualTest` failure goes to the designer

## Decision

The Owner chose Option A of escalation 42. They ran the full test suite in a sandbox where `manual.md` sits next to `repo/`, as a stand-in for the Owner, and reported the result. AC-15 is **not** accepted on a static check (Option B is rejected). It stays open until the failing test is resolved.

Owner's own words (2026-10-15):

> A。manual.md を repo/ の隣に置いた環境で python3 -m unittest discover を実行しました（Owner の代理、サンドボックス内）。結果: 40件中39件成功、1件失敗。失敗: test_manual_lists_glyphs_and_lines (test_game.ManualTest) — AssertionError: 'run over' not found in manual.md の本文（tests/test_game.py 631行目 self.assertIn(phrase, text, phrase)）。ほかの39件は成功。

Conditions added by the Owner: none.

Facts this Decision records:
- 39 of 40 tests pass, including `test_on_screen_section_lists_x_and_the_practice_room`.
- `test_manual_lists_glyphs_and_lines` fails: the phrase `run over` is not in the text of `manual.md` (`tests/test_game.py` line 631).
- The QA static checks in 29 and 40 did not detect this, because that test could not run in the QA workspace.

Limits: this Decision only settles how AC-15 is verified and what the result was. It does not say whether `manual.md` or the test is wrong. That ruling belongs to `game-designer` (player-facing behavior and spec wording). `manual.md` stays Owner-managed (D-005, D-007): no Role edits it.

## Rationale

The Owner took the option that gives a real test result rather than relying on the paragraph comparison. The result showed what the static check missed, which is why Option A was recommended.

## Alternatives considered

- Option B (accept AC-15 on QA's static check): not chosen by the Owner. The result shows it would have accepted a failing check.

## Revisit when

- The designer's ruling on the `run over` phrase requires a change to a vision pillar, to D-001, or to D-003.
- The `ManualTest` result in the Owner's environment and in QA's workspace keeps differing after the fix.
