---
kind: handoff
goal: G-001
seq: 5
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 05: gameplay-engineer → qa — Verify fix: no damage during a dash begun in the post-hit window (test corrected, suite green)

## Task

Verify independently, from the acceptance criteria below and the build, that the player cannot take damage at any moment of a dash at 30 and 60 FPS. Use `verify-change`.

## Context

Goal G-001. The Owner reported taking damage while dashing. QA's defect report (02, in the Load list) reproduced it: a dash begun with less than 0.25 s left of the 0.8 s post-hit invulnerability, where the invulnerability dropped mid-dash. A fix is in `repo/game.py`. The runtime's test run on the build is green. Judge the build by running it, not by this note.

## Findings

### What changed and where

- `repo/game.py`: invulnerability now follows both the dash timer and the post-hit timer.
- `repo/tests/test_game.py`: a regression test for the late-window dash exists and was adjusted in the last pass (no assertion weakened).
- `design/combat.md`, inputs, dash and cooldown values: unchanged.

### Acceptance criteria (full text in 02)

1. Script A at 30 and 60 FPS: no hit during or at the dash; hearts stay 2/3.
2. A dash started anywhere in the post-hit window is invulnerable for its full duration.
3. Invulnerability persists after the dash ends until the post-hit window ends.
4. Unchanged behaviors: hit damage (1 heart), 0.3 s stun, 0.8 s post-hit window, 0.25 s plain-dash invulnerability, cooldown, inputs.
5. Test suite passes; a regression test exists covering both frame rates.

### How to exercise

Run `python3 play.py --view trace {script}` and `--view player {script}` for these, each at `fps 60` and `fps 30`:

Script A:
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
Script B:
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

Also cover, with your own scripts:
- The criterion 3 case: a dash that ends while the post-hit window is still running, with a threat arriving after the dash ends.
- A Grub contact arriving during a dash begun late in the post-hit window.
- A hit outside any dash or window (1 heart, 0.3 s stun).
- The exact frame at which a dash ends with a shot or contact already overlapping the player. `design/combat.md` says "invulnerable for the full dash duration" and may not define that instant; report what you observe, and if the expected behavior is undefined say so.

Run the suite: `python3 -m unittest discover -s tests`.

## Decisions already made

- D-001: one attack button plus dash. No inputs were added.

## Constraints

- Must play correctly at 30 and 60 FPS.
- `design/combat.md` is unchanged and is the reference for intended behavior.
- Verify from the criteria and the build.

## Open questions

None blocking.

## Expected output

A verification verdict (pass/fail) with evidence at 30 and 60 FPS for script A, script B, the criterion 3 case and the unchanged behaviors. Address the result to `studio`. On pass, the Goal goes to Close (Review is not part of this defect Goal); on fail, the return rules apply.

## Sender assessment

Root cause of the failing test: a test artifact, not a game defect. `_update_shots` keeps a shot that touches an invulnerable player (it neither hurts nor consumes it). The test's zero-velocity shots therefore accumulated on the player. In `step`, the dash-end refresh clears `invulnerable` before `_update_shots`, so on the final dash frame the accumulated shots hit. Failure reported at fps 30 t=0.9667: the frame where `dash_left` reaches 0. The assertion in question was `hearts == hearts_before` after that step. The earlier `if game.dash_left > 0: assertTrue(invulnerable)` check proves the flag was True on every earlier frame, so the fix held for every frame in which the dash was still active after the step.

The skip of the final frame (no new shot placed there) is justified by the spec only partly: the spec's "full dash duration" is satisfied by the flag being True throughout the active dash, but it does not define a hit evaluated at the exact end instant. I treat the end frame as outside the dash (unchanged behavior), report it as a known risk rather than deciding it, and did not change the assertion.

Confidence: high that the code fix is correct (suite green, traces A at both rates show no mid-dash drop). Moderate on the untested paths: script B and Grub contact in the late window were not run by me.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (0.0 s).

```text
..........
----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, the build in `repo/` (run with `run_play` and `run_trace`)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
