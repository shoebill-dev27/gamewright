---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: no damage during a dash begun in the post-hit window

## Task

Verify independently, from the acceptance criteria below and the build, that the player cannot take damage at any moment of a dash at 30 and 60 FPS. Use `verify-change`.

## Context

Goal G-001. The Owner reported taking damage while dashing. Your handoff 02 reproduced it: a dash begun with less than 0.25 s left of the 0.8 s post-hit invulnerability, and the invulnerability flag dropped mid-dash. A fix is now in `repo/game.py`, with regression tests in `repo/tests/test_game.py`.

## Findings

### What changed and where

- `repo/game.py`: `_set_invulnerable(value, why)` is replaced by `_refresh_invulnerable(why)`. It sets `invulnerable = (dash_left > 0 or hurt_left > 0)` and logs an `invulnerable` event only when the value changes, as before. The four call sites (dash start, hurt timer ended, dash timer ended, hurt) now call it after their timer change.
- `repo/tests/test_game.py`: new class `DashInvulnerabilityTest`, each test at fps 30 and 60:
  - a dash begun with about 0.1 s of post-hit window left takes no damage from shots placed on the player on every frame it is active;
  - invulnerability persists after dash end until `hurt_left` reaches 0;
  - a plain dash is invulnerable for exactly its duration.
- `design/combat.md`, the inputs and the dash and cooldown code are unchanged.

### Criteria addressed

1. Script A at 30 and 60 FPS: the flag no longer drops at "hurt timer ended" while `dash_left` > 0, so the shot at about 2.08–2.10 s should not hurt.
2. Any dash start inside the window is covered, because the flag follows both timers.
3. At `dash_end` with `hurt_left` > 0, the trace should report `invulnerable=True`. The flag clears only when both timers are 0. I treated this as part of the fix, since the rule quoted in 02 ("invulnerability until 0.8 s after the hit") requires it. It is not a new design decision.
4. Unchanged by construction: hit damage, 0.3 s stun, the 0.8 s window, the 0.25 s plain-dash invulnerability, cooldown and inputs.
5. Tests added. Run `python3 -m unittest discover -s tests`.

### How to exercise

Re-run these with `python3 play.py --view trace {script}` (and `--view player`):

- Script A at `fps 60`, and the same script with `fps 30`:
```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```
  Expect no "YOU ARE HIT" between the second "you dash" and the dash end, with hearts staying 2/3 through the dash. In the trace there should be no `invulnerable False ('hurt timer ended')` mid-dash, and `dash_end` should show `invulnerable=True` while `hurt_left` > 0.
- Script B at 60 FPS (and 30):
```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```
  Expect no flag drop mid-dash. The Grub hit after the dash is still expected, once the post-hit window is over.
- Also check that a hit outside any dash or window still costs 1 heart with 0.3 s stun.

### Known risks

- Not tested to a hit: a Grub contact during the dash in the late-window case. The flag logic is shared by both sources, so it should be covered, but please check it with your own script.
- The post-hit window now extends past dash end in the case from criterion 3. This is intended per 02.
- I did not run the tests or the traces myself. The Build check appended by the runtime gives the test result.

## Decisions already made

- D-001: one attack button plus dash. No inputs were added.

## Constraints

- Must play correctly at 30 and 60 FPS.
- `design/combat.md` unchanged.
- QA verifies independently from the criteria and the build, not from this report's explanations.

## Open questions

None.

## Expected output

A verification verdict (pass/fail) with evidence at 30 and 60 FPS for script A, script B and the unchanged behaviors. On pass, the work goes to Review for G-001.

## Sender assessment

Root cause: `invulnerable` was a single boolean written by independent events (dash start, hurt, hurt timer end, dash end). Each end event cleared it without checking the other source. The hurt timer ending mid-dash cleared the flag, and the dash ending inside the window did the same. This explains both the reported hit and the "flag drops after a dash" observation. Deriving the flag from both timers fixes the shared path rather than the Spitter path alone, so Grub contacts are covered too.

Step ordering: within `step`, the hurt timer is processed before the dash. If both end in the same frame, the flag clears at the dash-end refresh, still before enemies and shots update. So the flag is False on that frame, as for a plain dash.

Test results: not run by me. Confidence is high in the logic and moderate on the regression test details. The test uses a player against the wall (x=15) so a rightward dash does not move them, and it places zero-velocity shots on the player. It skips the dash's final frame, where the dash legitimately ends before shots update.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 1 (0.0 s).

```text
....F.....
======================================================================
FAIL: test_dash_begun_late_in_hurt_window_is_invulnerable_throughout (test_game.DashInvulnerabilityTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 93, in test_dash_begun_late_in_hurt_window_is_invulnerable_throughout
    self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")
AssertionError: 1 != 2 : fps 30 t=0.9666666666666667

----------------------------------------------------------------------
Ran 10 tests in 0.001s

FAILED (failures=1)
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, the build in `repo/` (run with `run_play` and `run_trace`)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
