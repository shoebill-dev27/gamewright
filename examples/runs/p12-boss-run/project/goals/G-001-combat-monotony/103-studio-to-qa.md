---
kind: handoff
goal: G-001
seq: 103
from: studio
to: qa
stage: Verify (manual line, marker grep, suite)
outcome: routed
---
# 103: studio → qa — Verify the manual fix, search for stray edit markers, run the suite

## Task

Verify a small wording-only change and check the repository for leftover edit markers. This is a narrow check, not a full re-verification of W1–W8.

## Context

Goal G-001 (combat feels monotonous). A previous QA report found a stray edit marker line in the Warnings section of `repo/manual.md`. The manual was edited to remove it, and a wording correction was made to `design/combat-step94.md`. No code, test or parameter was changed in this round.

## Findings

Nothing from the senders is passed on; verify from the criteria and the files.

## Decisions already made

- D-011: variant names appear in wind-up and hit messages (accepted).
- D-013: one wording-only round, then Close.

## Constraints

- Verify from the files and the build. Run the project's commands (`run_tests`; `run_trace` only if used for V4).
- Do not widen into a full 30/60 FPS re-verification. Items already reported as unshown stay unshown.

## Open questions

None.

## Acceptance criteria

- **V1.** `repo/manual.md` contains no line starting with `>>>`, `<<<` or `=======`, and no occurrence of `REPLACE_PLACEHOLDER` or `SEARCH`.
- **V2.** In the Warnings section of `repo/manual.md`, the hit-message bullet (shot-hit direction wording) and the stagger sentence are two separate, well-formed bullets. The stagger bullet reads: "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted."
- **V3.** The same marker search (V1 patterns) over `repo/game.py`, `repo/tests/test_game.py`, `repo/bots.py`, `repo/play.py` and `design/combat-step94.md` finds nothing. (`=======` is legitimate only if it is part of ordinary text, which you should state if you find it.)
- **V4.** The test suite (`python3 -m unittest discover -s tests`) passes. The previous result was 69 tests OK.
- **V5.** In `design/combat-step94.md`, W1 for the spitter at (15,7) is labelled `from the south-east`, and the bullet is internally consistent (reversed travel vector about (0.92, 0.39), ratio 0.43 above 0.4142). The W5 brute case states a 0.7 s wind-up. If you can do it cheaply, check with `run_trace` that the build reports south-east for that case; if not, say it was not checked.

## Expected output

A verification report with pass/fail per criterion V1–V5 and any defect found. Address the result to `studio`. Say plainly what you did not check.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: repo/manual.md, repo/game.py, repo/tests/test_game.py, repo/bots.py, repo/play.py, design/combat-step94.md, project.md#current-state
- Decisions: decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: none (composed by the Studio from permitted information only)
