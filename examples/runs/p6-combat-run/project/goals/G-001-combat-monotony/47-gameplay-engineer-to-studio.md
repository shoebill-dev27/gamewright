---
kind: handoff
goal: G-001
seq: 47
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 47: gameplay-engineer → studio — `ManualTest` phrase check now ignores line wraps (test change only)

## Task

Report the test change from 46 (D-009) and ask the Studio to arrange the AC-15 rerun with the unchanged `manual.md`.

## Context

G-001. The Owner's run (D-008) gave 39/40; the one failure was `'run over' not found`, because `manual.md` hard-wraps `run` / `over`. The designer ruled (45, D-009) that the manual is correct and the test is too literal.

## Findings

Changed only `ManualTest.test_manual_lists_glyphs_and_lines` in `repo/tests/test_game.py`. The designer's snippet fitted the code as written, so it was applied unchanged.

Exact diff:

```diff
     def test_manual_lists_glyphs_and_lines(self):  # AC-15, V-5
         text = MANUAL.read_text(encoding="utf-8")
+        flat = " ".join(text.split())  # a hard-wrapped Markdown line must not hide a phrase
         for key, (char, _) in play.GLYPHS.items():
             self.assertIn(f"`{char}`", text, key)
         for phrase in ("room empty", "rears back", "is open", "charges", "spits",
                        "run over", "press attack to start again", "(miss)", "(too soon)",
                        "(stunned)", "(down)", "room cleared"):
-            self.assertIn(phrase, text, phrase)
+            self.assertIn(phrase, flat, phrase)
```

- The glyph loop still checks `text`.
- The phrase list is unchanged.
- `test_on_screen_section_lists_x_and_the_practice_room` is untouched.

**Suite result in my workspace: not run.** I did not execute `python3 -m unittest discover -s tests` for this step, and I have no evidence that `manual.md` exists beside `repo/` in my workspace. So I report no pass and no `ManualTest` result. This is not a pass. Without `manual.md`, `ManualTest` would error on reading it, not pass.

**Confirmation:** nothing else was changed. `manual.md`, `design/combat.md`, `game.py`, `play.py`, `bots.py`, the other tests and the README are unchanged. The suite entry point is the same.

## Decisions already made

D-009 (phrase check ignores line wraps, `manual.md` unchanged), D-008, D-007, D-005, D-001.

## Constraints

- No Role edits `manual.md`.
- AC-15 passes only on 40/40 with the unchanged `manual.md` beside `repo/`.

## Open questions

None.

## Expected output

The Studio arranges the AC-15 rerun: the Owner (or their stand-in, as in D-008) runs `python3 -m unittest discover -s tests` with the unchanged `manual.md` beside `repo/`, or places it in QA's workspace so QA can run it. Expected result: 40/40. If another phrase fails, the designer rules on that failure (45, D-009 "Revisit when").

## Sender assessment

Root cause is in the test, not the code: `assertIn("run over", text)` cannot match across the newline plus indent that `manual.md` has between `run` and `over`. Collapsing whitespace with `" ".join(text.split())` fixes exactly that, and from the designer's reading no other phrase is missing. The change is small and low-risk, but I have not verified it by running the suite. Confidence is high from reading the code, and no verification is claimed.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: repo/tests/test_game.py; design/combat.md (AC-15 only)
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md; decisions/D-008-manualtest-run-by-owner-one-failure.md
- Previous handoff: goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
