---
kind: handoff
goal: G-002
seq: 44
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 44: gameplay-engineer → studio — Split A: contract detail tests added; 130 tests OK at source id 7670da50793b

## Task

Studio chooses the next Build or QA step. Split A (43) is done for the items listed below. B and C remain.

## Context

G-002 Build. 43 asked for a baseline check, then contract tests for B3, B6, B7, B9, B10, T1–T4, C2 and C3, written against the real internals of `game.py`, `session.py` and `play.py`. This step added one file, `repo/tests/test_boss_contract_details.py` (18 tests). No production code was changed. Because `source_id` hashes `tests/*.py`, adding the file changed the id from `5145454ab956` to `7670da50793b`.

## Findings

### Execution

- Run 1, `tests` (`python3 -m unittest discover -s tests`), with the new file present: **Ran 130 tests, OK**, source id **7670da50793b**. The id came from a `bots` run in the same round, which executed the same file set.
- 130 = 112 + 18. I did not run a separate baseline on the file set without the new file. "112 at `5145454ab956`" is therefore not re-confirmed in this step. It rests on the 40 report and on the count arithmetic.
- No test failed, so no test or implementation was corrected. I found no implementation defect and no conflict with the spec.
- Internal names were taken from the code: `phase`, `phase_left`, `aim`, `attack_name`, `struck`, `spent`, `hurt_left`, `invulnerable`, the events `boss_contact` (`blocked`), `boss_recovery`, `boss_pursuit`, `cleared`, `down`, and the session events `run_won`, `run_dead`, `retry`. Session state, `stop_reason` and `control("pause"|"resume"|"retry")` were also used. These are fixtures, so they do not show reachability in a normal run.

### Per-item table (all executed at 7670da50793b, 30 and 60 FPS)

| Item | Tests added | Result | Coverage notes |
|---|---|---|---|
| B3 | `B3ChargeMovementTest.test_open_charge_moves_2_4_tiles_in_0_3_s`, `…test_wall_clamps_without_moving_recovery_start` | OK | 2.4 tiles in 0.3 s. At the wall: x=15, recovery starts on the same frame, 1.2 s left. |
| B6 | `B6DashContactTest.test_dash_through_charge_is_spent_and_harmless_afterwards`, `…test_dash_through_shot_consumes_it_and_no_later_damage` | OK | Charge: `spent`, not `struck`, one blocked `boss_contact`, 0 hearts lost. Shot: consumed, no damage afterwards. |
| B7 | `B7ProtectionExpiryTest.test_charge_touched_in_protection_cannot_hit_when_it_ends` | OK | Charge spent while protected: no damage when protection ends. A fresh charge then hits (hearts 2). Shot consumption in protection is covered by the existing `test_boss.py` and `ShotContactTest`, not duplicated. |
| B9 | `B9RecoveryTest.test_recovery_contact_is_harmless`, `…test_recovery_lengths` | OK | Harmless in both recoveries. 1.2 s and 1.4 s measured from `boss_recovery` to `boss_pursuit`. The "4 swipes" opportunity is covered by the existing `test_four_swipes_fit_in_recovery`. |
| B10 | `B10ContactBandTest.test_charge_inside_and_outside_the_band`, `…test_shot_inside_and_outside_the_band` | OK | Charge: 0.5 and 0.57 hit, 0.61 and 0.8 miss, 0.6 hit or miss. Shot: 0.3 and 0.39 hit, 0.41 and 0.7 miss, 0.4 hit or miss. Both FPS tested separately. |
| T1 | `TerminalTest.test_t1_clear_removes_shots_and_refuses_chasing_damage` | OK | At the clear, shots are empty. 2 s later frame and hearts are unchanged and input is refused. One `cleared` event. |
| T2 | `test_t2_same_frame_death_wins_over_victory`, `test_t2_survivor_wins_only` | OK | A lethal swipe and a lethal shot in one frame give dead only (one `run_dead`, no `run_won`, not cleared). With one more heart: won only. |
| T3 | `test_t3_terminal_state_is_frozen` | OK | After 2 s of steps and inputs, run time, room time, frame, hearts and state are unchanged, and `press` returns False. |
| T4 | `test_t4_retry_from_win_and_death_equals_a_new_run` | OK | Attempt 2, times 0, room 1, 3 hearts. Game and enemy `__dict__`s equal a fresh `RunSession`. The queued attack does not reappear and there are no attack or hurt events in the first second. |
| C2 | `C2PauseTest.test_pause_in_warning_freezes_and_resume_continues`, `…test_pause_freezes_protection_timer` | OK | Pause in a boss warning: clocks, frame and `phase_left` are unchanged after 2 s. After resume it continues. `hurt_left` and `invulnerable` are frozen. |
| C3 | `C3LimitTest.test_limit_in_combat_is_unfinished_with_no_result`, `…test_same_frame_death_or_victory_is_recorded_beside_the_limit` | OK | The limit in combat gives the unfinished `stop_reason`, state combat, no outcome. Same-frame death or victory is recorded together with the limit. |
| Shared combat regression | None added | Existing tests ran | Existing G-001 tests, including CueGap, ShotContact, LungeContact, Brute and the dodger agreement test, were in the 130 OK. I added nothing new for them. |

### Not covered in A (stated plainly)

- B5 (sidestep within 0.4 s) has the existing `test_one_tile_sidestep_during_each_warning`. B1, B2, B4 and B8 are covered by the existing `test_boss.py` and `test_boss_contract.py`. I did not re-audit them against §7.
- C2 pause was tested only in a boss warning and with the protection timer. Dash, a queued attack and the room-clear display are covered by the existing `test_session.py`. I added no combined "pause during dash contact" fixture.
- T4 was tested at session level. Discarding future-timed old inputs lives in the driver (`drive`) and is not newly tested here.
- B6/B7 were tested from the charge side with a close-range fixture, not a full dash into a full short-shot cycle.
- The README still says "112 tests". I did not edit it.

## Decisions already made

- D-017: two attacks, boundary recovery, death priority, terminal retry, clock and display contract.
- D-019: old aggregates retired, shared regressions, boss-adapted bot comparison, Designer judgment after measurement.
- D-021: Build on the current repo and Studio-internal text verification. No real device or sha check needed.

## Constraints

- Rooms 1–4, shared combat rules and the independent 1–4 bot policy are preserved. No new input, checkpoint, HP padding or tuning toward 15–20 minutes.
- The 130 OK holds only for source id 7670da50793b. Any later code or test change needs a rerun and a new id.
- A bot taking no hits is not evidence that the boss can be hit and avoided. The contact tests above (B6, B7, B10) serve that purpose, together with the existing B5.

## Open questions

None for the Designer. No spec gap or contradiction was found.

## Expected output

For Studio, remaining items:

- **Split B:** V1 supplements (legacy route boss display, bullet IDs and removal reasons, long observation). Extend `bots.play_run` with pause and retry: `pause_at`, `pause_seconds`, `retries`, using `RunSession.control` and resetting reaction memory on a new generation. Add tests for it. `RunSession.control` returns True or False and logs `pause`, `resume`, `retry`, `control_rejected`, as now confirmed.
- **Split C:** a normal-run measurement with pause and retry at both FPS. Add loose regression tests for the dodger in rooms 1–4: clear, 0 hearts lost, hearts lost differing by at most 1 across FPS, and dash ≥ 1 in rooms 3–4. The timings and dash counts from 40 are diagnostic reference values only.
- Optional: update the README test count and source id once the file set is final. Run the baseline without the new file if Studio needs "112 at 5145454ab956" re-confirmed.
- Next is Studio's choice between the remaining Build (B, C) and QA. Because of the unfinished items, this is still not a complete package for independent QA.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/tests/test_boss_contract_details.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/43-studio-to-gameplay-engineer.md
