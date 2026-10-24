---
kind: handoff
goal: G-001
seq: 77
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 77: studio → gameplay-engineer — Fix the red test `test_wind_up_and_hit_messages_name_the_variant` (test only)

## Task

Fix the test defect QA found in `repo/tests/test_game.py` so the whole suite is green at 30 and 60 FPS. Change test code only; do not change game behavior in `repo/game.py`, `repo/bots.py` or `repo/manual.md`.

## Context

Goal G-001 (combat monotony). Verify 24 (QA report 76) ran the 22a build (D-011 variant messages and manual text) and the 23 build (D-012 room 3 layout). 63 of 64 tests pass and no build-behavior defect was found. The one failure:

```
FAIL: test_wind_up_and_hit_messages_name_the_variant (test_game.VariantMessageTest)
AssertionError: 3 != 1 : (30, 'grub')   (out.count("a grub rears back"), test_game.py line 763)
```

## Findings

From QA 76 (defect 1, severity low):
- The test runs 3 s with a still player and asserts the wind-up message appears once. A still player is hit, the variant recovers, walks up and winds up again, so more than one message in 3 s is correct. QA's trace shows the runner winding up at 0.033 s and again at 1.167 s at 30 FPS. For the grub QA derived wind-ups at about 0.03, 1.5 and 2.8 s at 30 FPS (not separately traced).
- The assertion stops at the first failure, so the runner and brute cases and the 60 FPS cases of this test never ran. Expect further failures of the same kind once the grub case is fixed.
- The spec (`design/combat-step68.md`, V-a) says each wind-up prints its message once, on the first frame in range. It does not say "once in 3 s".

## Decisions already made

- D-011: variant-named wind-up and hit messages (accepted). The build behaves as specified; only the test's expectation is wrong.
- D-012: room 3 layout. Not to be touched.

## Constraints

- Test code only. If you find that the build behavior differs from V-a or V-b, stop and report it instead of changing game code.
- Acceptance criteria for the fix:
  1. The whole suite is green (`run_tests`).
  2. For every variant (grub, runner, brute) and at both 30 and 60 FPS, the test still checks that (a) a wind-up message names the matching variant, (b) one message is printed per wind-up and not per frame, and (c) the hit message names the matching variant and keeps the hearts suffix. Counting messages per wind-up (for example, comparing the count with the number of wind-ups seen in the trace, or limiting the window to the first wind-up) satisfies (b).
  3. The test does not rely on a window in which a second wind-up can occur unless it counts that wind-up.
- Must play correctly at both 30 and 60 FPS (project constraint).
- Run `run_bots` for rooms 1–5 after the change and state that the output is unchanged from what QA 76 reported (section 2 of that report). It should be, since no game code changes.

## Open questions

None.

## Expected output

Address the result to `studio`. Report: the test change, the full `run_tests` result, and the bot check. The next step is a QA re-verify in a fresh context, so keep implementation reasoning in `## Sender assessment`, which is removed before QA receives it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: repo/tests/test_game.py, repo/game.py, repo/bots.py, repo/README.md, design/combat-step68.md, project.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/76-qa-to-studio.md
