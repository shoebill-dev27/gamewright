---
kind: handoff
goal: G-001
seq: 46
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 46: studio → gameplay-engineer — make the `ManualTest` phrase check ignore line wraps (test change only)

## Task

In `repo/tests/test_game.py`, change only `ManualTest.test_manual_lists_glyphs_and_lines` so the phrase check ignores hard line wraps in `manual.md`. Do not change `manual.md`, the phrase list, the glyph check, any other test, or any game code.

## Context

G-001 (combat feels monotonous). The combat rework is built and verified except AC-15. The Owner ran the suite (D-008) and got 39 of 40 passing. The one failure is `'run over' not found` at `tests/test_game.py` line 631. The designer's ruling (45, D-009) is that `manual.md` is correct: it quotes the run-over lines with the right wording, but a hard line wrap splits `run` and `over`. The test is too literal. The manual stays unchanged.

## Findings

The designer specified the change (45):

```python
text = MANUAL.read_text(encoding="utf-8")
flat = " ".join(text.split())   # a hard-wrapped Markdown line must not hide a phrase
for key, (char, _) in play.GLYPHS.items():
    self.assertIn(f"`{char}`", text, key)
for phrase in (...same list, unchanged...):
    self.assertIn(phrase, flat, phrase)
```

- Only the phrase loop uses the whitespace-collapsed `flat`. The glyph loop keeps `text`.
- Leave `test_on_screen_section_lists_x_and_the_practice_room` alone; its strings are on single lines.
- If the designer's snippet does not fit the actual code (names, structure), apply the same idea with the smallest edit. If something is ambiguous or a different phrase turns out to be missing, stop and hand back as `question`. Do not rule on manual wording yourself.

## Decisions already made

- D-009: the `ManualTest` phrase check ignores line wraps; `manual.md` stays unchanged.
- D-007, D-008: the manual paragraph was placed by the Owner; no Role edits `manual.md`.
- D-001: no new inputs.

## Constraints

- Edit only the one test method.
- Do not edit `manual.md`, `design/combat.md` or any game code.
- The change must keep working at the same suite entry point: `python3 -m unittest discover -s tests`.

## Open questions

None.

## Expected output

A short build note in a Handoff to `studio` (outcome `done`, or `question` if blocked):

- The exact diff of the test method.
- The suite result in your workspace, saying plainly whether `ManualTest` actually ran against the Owner's `manual.md` or could not find it. A skipped or unreadable `manual.md` is not a pass.
- Confirmation that you changed nothing else.

The Studio then arranges the AC-15 rerun with the unchanged `manual.md` (expected 40/40).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: repo/tests/test_game.py; design/combat.md (AC-15 only); repo/README.md
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md; decisions/D-008-manualtest-run-by-owner-one-failure.md
- Previous handoff: goals/G-001-combat-monotony/45-game-designer-to-studio.md
