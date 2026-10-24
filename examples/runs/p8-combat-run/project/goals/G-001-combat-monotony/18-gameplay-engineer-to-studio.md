---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 18: gameplay-engineer → studio — Bot log now carries decision-time state; walker 30/60 test replaced by tests of criteria 13/14 per rate and dodger agreement

## Task

Report the tooling and test change from handoff 17, for routing to QA. No simulation or bot decision changed.

## Context

G-001, build 0.5. QA (handoff 16) could not close criterion 16e because `log on` printed action names and times only. The designer ruled (handoff 14) that the walker only has to meet 13 and 14 at each rate and the dodger must agree across rates (16c).

## Findings

### Files changed

- `repo/bots.py`: log only. `Brain` gained log-only fields `grid` and `shadow`, a `skip` method, and `note` now appends ` | <state>`. New helpers `_state` and `_hurt_lines`. `play_room` calls `brain.skip` while the player is stunned, and records state around `game.step()` only when `log` is on. Bot functions, thresholds (2.5, 1.1), `REACTION = 0.15`, the grid logic in `due`, and `game.py` are untouched. Added imports `SHOT_LIFE`, `SHOT_REACH`.
- `repo/tests/test_game.py`: the walker `expectedFailure` test is replaced by `test_walker_meets_criteria_13_and_14_at_each_rate` (the dodger test, unchanged, already covers 16c). Added `test_bot_log_adds_state_and_changes_no_result` and `test_walker_logs_the_exact_distance_it_compared`. Other tests are unchanged.
- `repo/README.md`: describes the new log.
- `game.py`, `play.py`, `design/combat.md`: not changed.

### Log format (`log on`)

- Decision line: `<time> s  <action> | frame N, grid G s, frame time T s, player (x, y), hearts H, stunned no|yes (S s left), nearest <kind> at (x, y) distance D (exact <repr>), shots in flight: (x, y) v (vx, vy); …|none`. The part before ` | ` is identical to the old line. `distance` is the same `math.hypot` expression the bot compares, printed to 9 decimals and as the full float repr.
- Skipped line: `<time> s  skipped decision | frame, grid, frame time, reason: player stunned (S s of stun left)`, once per grid time swallowed by the stun.
- Heart-loss line: `<time> s  HEART LOST | frame N, source grub|shot, player (x, y), grub <kind> at (x, y) | shot at (x, y) v (vx, vy); hearts now H`.

### Run results

- `run_tests`: `python3 -m unittest discover -s tests` → Ran 34 tests, OK. This was with the final `bots.py` and `test_game.py`. A temporary comparison harness (original bots.py kept as a copy plus a comparison test; not delivered) also ran 37 tests OK. That harness is not part of the repo.
- Criterion 4, log off: before and after output were compared byte for byte with the temporary harness, for `bots walker,dodger,camper`, `rooms 1-5`, at 30 and 60 FPS. Both are identical. With `log on`, removing the new ` | …` parts and the new HEART LOST and skipped lines gives exactly the old log (863 lines at 30 FPS, 968 at 60 FPS).

Output before and after (identical), hearts lost per room 1/2/3/4/5:

| Bot, rate | Per room | Totals |
|---|---|---|
| walker 30 | 3✗ 2✓ 0✓ 1✓ 3✗ | cleared 3/5, lost 9, dashes 0 |
| walker 60 | 3✗ 2✓ 2✓ 2✓ 2✓ | cleared 4/5, lost 11, dashes 0 |
| dodger 30 | 0✓ ×5 | cleared 5/5, lost 0, dashes 35 (rooms 3/4/5: 8/7/11) |
| dodger 60 | 0✓ ×5 | cleared 5/5, lost 0, dashes 48 (rooms 3/4/5: 10/8/14) |
| camper 30 | 3✗ 2✓ 3✗ 3✗ 3✗ | cleared 1/5, lost 14, dashes 0 |
| camper 60 | 3✗ 3✗ 3✗ 3✗ 3✗ | cleared 0/5, lost 15, dashes 0 |

Camper recorded output (before = after):

```text
30 FPS
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 2: cleared in 10.2 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.2 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
camper  total: cleared 1/5, hearts lost 14, dashes 0
60 FPS
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.1 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
camper  total: cleared 0/5, hearts lost 15, dashes 0
```

### Sample of the new lines (walker)

Room 1, 0.15–0.50 s:

```text
30 FPS
  0.17 s  walk to grub | frame 5, grid 0.150 s, frame time 0.166667 s, player (8.000000, 3.333333), hearts 3, stunned no, nearest grub at (8.000000, 0.166667) distance 3.166666667 (exact 3.166666666666667), shots in flight: none
  0.30 s  walk to grub | frame 9, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.5000000000000004), shots in flight: none
  0.47 s  face and swing at grub | frame 14, grid 0.450 s, frame time 0.466667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
60 FPS
  0.15 s  walk to grub | frame 9, grid 0.150 s, frame time 0.150000 s, player (8.000000, 3.400000), hearts 3, stunned no, nearest grub at (8.000000, 0.150000) distance 3.250000000 (exact 3.2499999999999982), shots in flight: none
  0.30 s  face and swing at grub | frame 18, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.4999999999999964), shots in flight: none
  0.45 s  face and swing at grub | frame 27, grid 0.450 s, frame time 0.450000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.450000) distance 2.350000000 (exact 2.349999999999996), shots in flight: none
```

Room 3, 1.80–2.60 s:

```text
30 FPS
  1.80 s  sidestep shot in flight | frame 54, grid 1.800 s, frame time 1.800000 s, player (2.933333, 1.866667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.273664878 (exact 1.273664878302845), shots in flight: (2.076083, 1.064895) v (2.282502, 1.946840)
  1.97 s  sidestep shot in flight | frame 59, grid 1.950 s, frame time 1.966667 s, player (2.933333, 2.533333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.795054936 (exact 1.7950549357114955), shots in flight: (2.456500, 1.389368) v (2.282502, 1.946840)
  2.10 s  walk to spitter | frame 63, grid 2.100 s, frame time 2.100000 s, player (2.933333, 3.066667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.267646847 (exact 2.267646846892655), shots in flight: (2.760834, 1.648947) v (2.282502, 1.946840)
  2.27 s  sidestep shot in flight | frame 68, grid 2.250 s, frame time 2.266667 s, player (2.933333, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.682590595 (exact 1.682590595216522), shots in flight: (3.141251, 1.973420) v (2.282502, 1.946840)
  2.40 s  walk to spitter | frame 72, grid 2.400 s, frame time 2.400000 s, player (2.933333, 2.933333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.146832292 (exact 2.1468322917472777), shots in flight: (3.445585, 2.232999) v (2.282502, 1.946840)
  2.57 s  walk to spitter | frame 77, grid 2.550 s, frame time 2.566667 s, player (2.933333, 2.266667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.573389829 (exact 1.5733898294941195), shots in flight: (3.826001, 2.557472) v (2.282502, 1.946840)
60 FPS
  1.80 s  sidestep shot in flight | frame 108, grid 1.800 s, frame time 1.800000 s, player (2.600000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.341640786 (exact 1.3416407864998732), shots in flight: (2.030000, 1.040000) v (1.800000, 2.400000)
  1.95 s  sidestep shot in flight | frame 117, grid 1.950 s, frame time 1.950000 s, player (3.200000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: (2.300000, 1.400000) v (1.800000, 2.400000)
  2.10 s  walk to spitter | frame 126, grid 2.100 s, frame time 2.100000 s, player (3.800000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.163330765 (exact 2.1633307652784017), shots in flight: (2.570000, 1.760000) v (1.800000, 2.400000)
  2.25 s  HEART LOST | frame 135, source shot, player (3.200000, 2.200000), shot at (2.840000, 2.120000) v (1.800000, 2.400000); hearts now 2
  2.25 s  skipped decision | frame 135, grid 2.250 s, frame time 2.250000 s, reason: player stunned (0.300 s of stun left)
  2.40 s  skipped decision | frame 144, grid 2.400 s, frame time 2.400000 s, reason: player stunned (0.150 s of stun left)
  2.55 s  skipped decision | frame 153, grid 2.550 s, frame time 2.550000 s, reason: player stunned (0.000 s of stun left)
  2.57 s  walk to spitter | frame 154, grid 2.550 s, frame time 2.566667 s, player (3.200000, 2.200000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: none
```

### Observations for QA (stated without judgment)

- Room 1, 0.30 s: the exact distance the walker compared is 2.5000000000000004 at 30 FPS (not `< 2.5`, so it walks) and 2.4999999999999964 at 60 FPS (`< 2.5`, so it swings). This matches the floating-point tie hypothesis in handoff 16. Both decisions are on grid time 0.300 at frame time 0.300000.
- Room 3: the states at the same grid time already differ before the 2.10–2.25 s hit. At grid 1.800 s the player is at (2.933, 1.867) at 30 FPS and (2.600, 2.200) at 60 FPS. The shot velocities differ too: (2.283, 1.947) at 30 FPS and (1.800, 2.400) at 60 FPS, because the aim direction was locked at the start of the cue from different player positions. The logged data therefore contains no pair of decisions with the same state at the same game time in this window.
- The 60 FPS hit is logged at frame 135 (2.25 s) with the player at (3.200, 2.200) and the shot at (2.840, 2.120): centre distance about 0.369, inside the 0.4 reach. The 30 FPS player's positions in this window are different, so the log does not show a graze at the contact edge for this case. Whether any frame-rate-dependent graze exists is not shown by this data.

## Decisions already made

- D-001: one attack button plus dash; no new input. Unchanged.
- Designer's rulings (handoff 14) applied as written.

## Constraints

- No change to simulation, bot decisions, thresholds, the 0.15 s grid, or player-visible output. Log off is byte-identical to before.

## Open questions

None for the engineer. Whether any frame-rate-dependent contact-edge graze is acceptable is for the game-designer after QA reads the log; the log above did not show a graze case.

## Expected output

QA runs `bots walker`, `rooms 3`, `log on` at `fps 30` and `fps 60`, compares decisions and states by the 16e rule, and reports. Also QA's verification of 1–16 continues as planned in handoff 14.

## Sender assessment

- Behavior preservation: confirmed by the byte comparison of log-off output and by stripping the new log parts (both described above), for all three bots, rooms 1–5, both rates. The added `skip` uses a shadow clock so it never changes `Brain.next`. `_hurt_lines` only reads state; `shots_before` and `struck_before` are copies taken before `step`.
- The heart-loss shot position is found by comparing the shot list before and after the step. A shot that hits in the frame it is fired would be reported as "shot position not found"; no such case appeared in the logs checked.
- The new walker test passes at both rates with the existing numbers (30 FPS: rooms 3–5 lost 4, cleared 2/3; 60 FPS: lost 6, cleared 3/3; rooms 1–2 lost 5 at both rates). The 60 FPS walker sits at the top of the criterion 13 limit (6).
- Confidence: high that nothing behavioral changed; medium on the 16e conclusion, which QA must draw.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md (criteria 13–16), repo/bots.py, repo/game.py, repo/tests/test_game.py, repo/README.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
