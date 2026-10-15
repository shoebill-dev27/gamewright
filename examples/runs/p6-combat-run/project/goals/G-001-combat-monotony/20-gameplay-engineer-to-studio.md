---
kind: handoff
goal: G-001
seq: 20
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 20: gameplay-engineer → studio — `manual.md` (T8) still cannot be written; escalate

## Task

Escalate to the Owner (or give a step write access to `manual.md`). This step could not write `manual.md`, so T8 is still open and nothing can go to QA yet.

## Context

G-001, Build of Option A (build 0.5). Handoff 19 asked this step to place the draft from handoff 18 at the project root as `manual.md` and then confirm `run_tests`. The write list for this step contains only this handoff, `repo/<path>`, and `@run` blocks. `manual.md` at the project root is not on it. The test (`ManualTest`) reads `REPO.parent / "manual.md"`, which is the project root. A file under `repo/` would not satisfy it. Handoff 19 told this step not to work around a missing write permission, so I did not place the file anywhere else, and I did not run the tests. Without `manual.md` they would fail the same way as in handoff 18.

## Findings

**`manual.md` could not be written.** It does not exist at the project root. This is the second time the same input has been handed back for this reason, so the Studio should escalate to the Owner.

What I could do without the file, by reading the draft against `repo/play.py` and `repo/tests/test_game.py`:

1. **Glyphs.** Every `GLYPHS` character is in the draft as a backticked entry: `P`, `x`, `g`, `G`, `w`, `W`, `s`, `S`, `z`, `Z`, `*`, `)`, `(`, `^`, `v`. This is what `ManualTest` checks.
2. **Phrases.** Each of the test's phrases appears in the draft: "room empty", "rears back", "is open", "charges", "spits", "run over", "press attack to start again", "(miss)", "(too soon)", "(stunned)", "(down)", "room cleared". I checked this by reading, not by running the test.
3. **Behavior.** I found nothing in the draft that contradicts the built game. The "(dash not ready)" wording, the heal, the 1.5 s of free input and the practice-room rules match `LINES` and the spec. The draft's "the grub is open" is a prefix of the built line "the grub is open ({side})", which is fine.
4. **Wording changes.** None were needed. The draft can be placed unchanged.
5. **Player-facing rule.** The draft names no internal states, plan IDs or acceptance-criterion numbers.

Not done: `run_tests` was not run, so the 34-test result is unconfirmed. The expected result is 34 of 34 once the draft is at the project root, but that has not been shown.

## Decisions already made

D-001…D-004 hold. D-004 item 5 assigns the manual to the gameplay-engineer in this change set. That needs write access to `manual.md`.

## Constraints

- Place the draft from handoff 18, section "Draft `manual.md`", unchanged at the project root.
- No code changes are needed.

## Open questions

- Who writes `manual.md`? Options:
  - (a) The Owner places the draft from handoff 18 at the project root by hand.
  - (b) The Studio re-runs the gameplay-engineer with `manual.md` on the write list.
- After either option, run `python3 -m unittest discover -s tests` and confirm 34 of 34 pass before composing the QA handoff.

## Expected output

Once `manual.md` exists and `run_tests` passes, the Studio composes the verification Handoff for QA without the Sender assessment.

## Sender assessment

- High confidence the draft passes `ManualTest`, from reading the test against the draft. This is not tested.
- AC-15 and V-5 stay unverifiable until the file exists.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-visuals.md, design/combat.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/19-studio-to-gameplay-engineer.md
