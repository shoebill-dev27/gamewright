---
kind: handoff
goal: G-001
seq: 4
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 04: studio → gameplay-engineer — Fix the failing regression test / remaining damage during the dash at 30 FPS

## Task

Your fix from handoff 03 did not pass the runtime's test run. Find out why `test_dash_begun_late_in_hurt_window_is_invulnerable_throughout` fails at 30 FPS, fix the cause, and run the whole suite until it is green at 30 and 60 FPS. Use `implement-change`.

## Context

Goal G-001: the player takes damage during a dash (QA's defect report is `02-qa-to-gameplay-engineer.md`, with the acceptance criteria). You replaced `_set_invulnerable` with `_refresh_invulnerable`, which derives the flag from `dash_left` and `hurt_left`, and added `DashInvulnerabilityTest`. The runtime then ran `python3 -m unittest discover -s tests` on your build: exit 1, 10 tests run, 1 failure:

```text
FAIL: test_dash_begun_late_in_hurt_window_is_invulnerable_throughout (test_game.DashInvulnerabilityTest)
  File "/work/tests/test_game.py", line 93, in test_dash_begun_late_in_hurt_window_is_invulnerable_throughout
    self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")
AssertionError: 1 != 2 : fps 30 t=0.9666666666666667
```

The failing case is fps 30. The test expects hearts to stay at 2, but they are 1, so the player took one more hit at t≈0.967 s (hearts only dropped because a shot or contact landed).

## Findings

Nothing beyond the failure above. Whether the cause is the fix (the player is still vulnerable at some frame of the dash at 30 FPS, e.g. a frame-ordering or timer-boundary case) or the test (setup, shot placement, which frame is checked) is for you to determine; root cause is your call. The test also skipped the dash's final frame by design; check that the skip is justified by `design/combat.md` and not hiding a real gap.

## Decisions already made

- D-001: one attack button plus dash. No inputs were added.

## Constraints

- Do not change `design/combat.md` or the dash's design values (duration, cooldown, distance, invulnerability length). If the spec turns out ambiguous or missing a case, hand back instead of deciding.
- Must play correctly at both 30 and 60 FPS.
- Do not weaken the test to make it pass unless you show the assertion was wrong against the spec.
- Run the tests yourself this time (`run_tests`) and report the actual result. Also run scripts A and B from 03 with `run_trace` at 30 and 60 FPS.

## Open questions

None.

## Expected output

A fixed build and green test suite, and a handoff addressed to `qa` for Verify (stage Verify, acceptance criteria from 02, how to exercise, actual test and trace results). Put your root-cause reasoning in `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, project.md#constraints, repo/game.py, repo/tests/test_game.py, goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/03-gameplay-engineer-to-qa.md
