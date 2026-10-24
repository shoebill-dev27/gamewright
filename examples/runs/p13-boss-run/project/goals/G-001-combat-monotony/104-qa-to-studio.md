---
kind: handoff
goal: G-001
seq: 104
from: qa
to: studio
stage: Verify (manual line, marker grep, suite)
outcome: pass
---
# 104: qa → studio — Verification report: manual fix, marker search, suite

## Task

Report the pass/fail result for V1–V5 of handoff 103. Studio decides the next step. By D-013 item 4 that is a paper-check Review pass 4.

## Context

Goal G-001 (combat feels monotonous). A previous QA report found a stray edit marker in the Warnings section of `repo/manual.md`. Handoff 103 asked for a narrow wording-only check, not a full re-verification of W1–W8. No code, test or parameter changed in this round. I read the files as given in the packet. I used the test result from the `tests` run. I used the `play` run (`--view player`, 60 FPS) for the south-east case, not `run_trace`.

## Findings

Verdict: **pass**. All five criteria pass. I found no defects.

- **V1: pass.** I read `repo/manual.md` in full.
  - No line starts with `>>>`, `<<<` or `=======`. Every line starts with text, `#`, `-`, `|`, a code fence or indentation.
  - `REPLACE_PLACEHOLDER` and `SEARCH` do not occur.
- **V2: pass.** In the Warnings section the hit-message bullet and the stagger sentence are separate bullets.
  - The hit-message bullet begins `Being hit shows ...` and ends `... the same line the cue: line and ~ showed before the shot).`. Its parentheses and backticks are balanced.
  - The next bullet reads "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted." The text is identical to the required sentence. It is only wrapped across two source lines.
  - The following two bullets (dash-stopped shot, lunge while protected) are also separate and well-formed.
- **V3: pass.** I read `repo/game.py`, `repo/tests/test_game.py`, `repo/bots.py`, `repo/play.py` and `design/combat-step94.md`.
  - No line starts with `>>>`, `<<<` or `=======`.
  - `REPLACE_PLACEHOLDER` and `SEARCH` do not occur.
  - Nothing needed an "ordinary text" exception, because `=======` does not appear at all.
- **V4: pass.** `python3 -m unittest discover -s tests` ran 69 tests, OK, exit 0. That matches the previous 69 OK.
- **V5: pass.**
  - In `design/combat-step94.md`, W1 for the spitter at (15,7) is labelled `from the south-east`. The bullet is consistent: travel vector about (-0.92,-0.39), reversed (0.92,0.39), ratio 3/7 = 0.43, above 0.4142, so the diagonal applies.
  - The W5 brute case says "for the brute, after its 0.7 s wind-up".
  - Build check: a `play --view player` run (`room empty`, `spawn spitter 15 7`, `player 8 4`, 60 FPS, `end 7`) printed `YOU ARE HIT by a shot from the south-east — hearts 2/3` at 4.200 s and again at 6.600 s. The `cue:` line gave aim (-0.92,-0.39), which matches the design. I did not use `run_trace`.

## Decisions already made

- D-011: variant names appear in wind-up and hit messages (accepted). The shot-hit message now carries the source side, per step 94.
- D-013: one wording-only round, then Close. Review pass 4 is a paper check if QA passes with the suite green and bots unchanged.

## Constraints

I did not modify any code, test, manual or design file. I did not widen into a full 30/60 FPS re-verification.

## Open questions

None.

## Expected output

Studio routes to Review pass 4 as a paper check, per D-013 item 4.

What I did not check:
- I did not run `run_bots`. The bots-unchanged part of W7 is not newly verified. `bots.py` was unchanged in this round, and the suite, which includes the bot tests, is green.
- The south-east wording was observed live at 60 FPS only. The 30 FPS case and the other W1 placements (east, north, west, south, north-east) are covered only by `ShotSourceTest.test_direction_words_at_both_rates` in the passing suite, not by my own play runs.
- I did not re-run W2–W4, W6 or W8, and did not re-verify the 30/60 FPS items already reported as unshown (R3-8 at 60 FPS, room 3 pure 1-tile sidestep, 30 FPS cancel and recovery swipe in room 3).
- I did not run `grep` or any tool for V1 and V3. These are read-throughs of the provided file contents.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: repo/manual.md, repo/game.py, repo/tests/test_game.py, repo/bots.py, repo/play.py, design/combat-step94.md, project.md#current-state
- Decisions: decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/103-studio-to-qa.md
