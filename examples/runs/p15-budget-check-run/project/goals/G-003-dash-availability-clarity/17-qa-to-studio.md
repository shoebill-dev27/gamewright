---
kind: handoff
goal: G-003
seq: 17
from: qa
to: studio
stage: Verify (re-verification against the D-029 spec)
outcome: question
---
# 17: qa → studio — Dash availability re-verification: no failure found in what I could run; verdict is NOT pass (unverified items and one spec gap)

## Task

Decide how to close the unverified items listed below and route the one spec gap (public-driver periodic picture timing) to `game-designer`. Verdict for G-003: **not pass**. No criterion I could check failed. Several criteria were not observed by me and are not counted as pass.

## Context

Goal G-003: the Owner finds it unclear when dash can be used again. This is the re-verification after the D-029 rulings and the fix Build (handoff 15). All evidence comes from the current build in `repo/`, checked against `design/dash-availability.md`. Two run rounds were used: tests, play, trace, and one bots attempt that failed on script syntax. The "before" build does not exist, so no before/after comparison was made.

## Findings

### Results per criterion

**Passed, with evidence**

| Criterion | Result | Evidence |
|---|---|---|
| Full test run | **PASS**: `python3 -m unittest discover -s tests` → `Ran 180 tests … OK`, exit 0. | Test run. The inventory lists `tests/test_dash_refusal.py` (F 08), run as 8 tests: 5 in `RefusalSourcesTest`, 1 in `GridTest`, 1 in `TimingTest`, with ids 076–082. |
| P1–P5, 60 FPS (script P) | **PASS** | Run P60. Pictures before 0.6 s end `dash: ready`. 0.600 `you dash right — usable again in 0.9 s`. 0.700 `dash not ready — 0.8 s left (dashing)`. The 1.00 s picture ends `dash: 0.5 s`. 1.000 `… 0.5 s left`. 1.400 `… 0.1 s left`. |
| P1–P5, 30 FPS | **PASS** | Run P30. The same text and numbers appear. |
| P6, 60 FPS | **PASS** | P60: `dash ready` at 1.450, followed by a picture ending `dash: ready`. The 1.50 picture shows ready. 1.500 `you dash right`. |
| P6, 30 FPS (0.90 s) | **PASS** | P30: `dash ready` at 1.500, followed by a picture ending `dash: ready`. The 1.50 picture shows ready. The press at 1.5 prints `you dash right`. |
| P7 / Q1 / Q2, 30 FPS | **PASS** | P30pre (dash at 0.6, presses at 1.46 and 1.5): 1.467 `dash not ready — 0.1 s left`, 1.500 `dash ready`, then accepted at 1.500. That is 0.900 s start-to-start, one frame earlier is refused. T30 trace: `dash_end` t=0.867, `dash_ready` t=1.500, so `dash_ready` is dash_end + 0.633, which is +1 frame and within ±1 frame (QA 10 saw the same). |
| 60 FPS press at 1.433 / 1.450 (also P7, Q1) | **PASS** | E60: 1.433 `dash not ready — 0.1 s left`, 1.450 `dash ready`, then `you dash left` at 1.450. T60 trace: `dash_end` 0.850, `dash_ready` 1.450 (+0.600 exactly). |
| P10 (reading rule), as far as observed | **PASS** (observed only) | In P30, P60, E60, P13leg and EVp, every refusal shows a time and every acceptance follows `dash ready`, with no case of "ready" shown before a refusal. Rounding was checked against trace waits in T13leg and EVt: wait 0.55 → `0.6`, 0.40 → `0.4`, 0.6167 → `0.7`, 0.4667 → `0.5`. |
| P13 legacy route, dash action | **PASS** | P13leg (`when nothing within 20 then dash right` plus `when text "not ready" then move up`): every refusal prints `dash not ready — <R> s left`, with ` (dashing)` while active and no suffix during cooldown. The `P` row climbs 4→3→2→1→0 after refusals, so the text rule fires. T13leg trace confirms the `ignored` refusals. No `(nothing happens)` appears. |
| P13 public driver, dash action | **PASS** | P13pub: the same lines appear with the driver's usual event picture after each message. `P` moves up after refusals, so the text rule fires. |
| P13, different action type (`dash toward`), both routes | **PASS** | P13legAside (legacy) and P13pubAside (`mode room`) both print `dash not ready — 0.7 s left (dashing)` and the cooldown refusals at 0.150, 0.300, 0.450 and 0.600. Legacy has no extra picture and the driver prints one. This separates route from action type. |
| Q12 as reduced by D-029 | **PASS** (the reduced check only) | R5leg: the first line is exactly `note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`, and every picture carries the dash field. |
| Event identity, player view vs trace view (after-only) | **PASS** on the scripts compared | E60 vs T60 and EVp vs EVt: the sequence of dash, `dash_end`, refusal (with wait) and `dash_ready` events, and their times, agree between views. Trace lines are stamped post-step, one frame after the player-view time. The only difference is the display-only `quiet: True` on non-dash `ignored` events, as in EVt `attack recovering`. Refused dashes from rules carry no `quiet` (T13leg). This compares two scripts, not the whole game. |
| P12 scripted (no dodger bot) | **PASS** for these runs only | EVp (legacy room 3, 30 FPS): every live picture has the field, and `dash ready` follows each dash (3.033→3.933, 6.700→7.600, 7.833→8.733, 10.267→11.167). R5pub (`mode room`, room 5, 30 FPS): every picture has the field, with `dash ready` at 1.500 and 2.400 after dashes at 0.6 and 1.5. R5leg (legacy room 5, 60 FPS): ready at 1.450 and 2.350. |
| Q9 (partial) | Observed | Field present in legacy `room empty`, room 3 and room 5; `mode room` `room empty` and room 5 (boss). The legacy room-5 note line is kept. |

**Observations (reported, not judged)**

- P30edge used `1.467` as a script time. At 30 FPS frame 44 is t=1.46667, which is before 1.467, so that press ran on frame 45 at 1.500 together with the 1.5 press. That script therefore did not test "one frame earlier". P30pre (1.46) did.
- In `mode room`, the periodic pictures after an event picture follow the 0.5 s cadence from the last picture. In P13pubAside they appear at 1.350, 1.850, 2.350 and 2.850 after the `dash ready` picture at 0.850. In the legacy route they stay on the fixed grid; test `GridTest` covers legacy only. `public-driver.md` says "Default player scheduling retains the existing half-second cadence after event pictures", but spec 3.5 and Q8(b) say "the fixed 0.5 s grid including after dash event pictures". See Open questions.
- In the public driver a rule produces one refusal message and one picture per rule action, about 6 per second (P13pub). This is accepted under D-029.

### Not verified (not counted as pass)

| Item | Why | What it needs |
|---|---|---|
| Q5 (room-entry reset, `mode run`) | Run Q5a had no usable result. It was one trace run with a 15 s limit, and the output was truncated. Its summary shows only room 1 cleared at run time 4.35 s. The second run (dash at k − 0.25 with a queued swipe) was not made. | A trace run of the second script with `dash_ready` and entry lines readable. This needs a bounded output (short limit, or a smaller view). |
| Q7 (bot-run consistency) | The bots attempt failed on script syntax (B1: `script line 1: cannot read 'dodger room 3 fps 60'`, so there was no run and no `bots.py` header). Dodger traces for rooms 3 and 4 over 60 s and a `room 5` run were not produced. | `bots.py` script lines are `bots …`, `rooms …`, `fps …`, `limit …`, `hearts …`, `mode …`, `log on` (from the usage text). Plus trace-view dodger runs, which only the generated `public_script` can provide. |
| P12 via the public replay scripts (dodger) | Not run. The scripts come from `tests.test_split_c.public_script`, and my means cannot generate them. Only scripted rooms 3 and 5 were run. | A step able to produce `run30.txt` and `run60.txt` (see `repo/public-driver.md`) and read both views. |
| P8, P9, P11 | No script of mine had a no-dash hit, a hit-stun press, or a wind-up near the player at the right time. In R5pub the room-5 hit at 3.933 shows `dash: 0.3 s` and the run ended before the stun ended. In EVp wind-ups occurred with dashes working, but P11 was not isolated. Unit tests exist (`test_hit_stun_refusal_reason`, `test_no_dash_ready_without_a_dash`, `test_state_matches_press`) and passed. I did not read them. | Short scripts: a hit with no dash; a dash then a hit then a press at +0.3 s; a grub wind-up scripted near the player. |
| P13, attack-refusal half (both routes) | No run of a held attack rule (for example `when nothing within 20 then attack`) on either route. Only the unit test `test_rule_attack_that_does_nothing_stays_quiet_on_legacy` covers it (legacy only, and I did not read it). Public driver: unobserved. | Two short play runs, one per route. |
| Q3, Q4, Q6, Q10, Q11 | Not run by me. Unit tests for Q3, Q4 and Q11 exist (`test_a_hit_does_not_change_the_cooldown`, `test_attack_recovery_does_not_block_a_dash`, `test_text_rule_on_dash_ready`). The pause test (`test_pause_freezes_dash_and_queued_attack`) is in the suite; I did not read it. | Short scripts, or accept the tests. |
| Q9 gaps | Legacy rooms 1, 2 and 4, and `mode room`/`mode run` rooms 1–4, plus clear and terminal screens without the field, were not observed. `test_terminal_picture_has_no_field` exists. | Optional player-view scripts. |
| Q8 (a) recorded numbers and (b) | (a): only the suite's own printouts exist (dodger room results and dash counts at 30 and 60 FPS, e.g. room 1 clear 6.63 s at 30 and 9.62 s at 60). I did not compare them with an earlier handoff, because no earlier numbers are in this packet. (b): the legacy grid and event order held in the runs. The public driver is the spec gap. Hence Q8 is unverifiable beyond the suite. | Recorded numbers from earlier handoffs, or an explicit acceptance of the suite alone. |
| Q12 remainder (L1 comparison) | No baseline (D-024). | Cannot be done. |
| Before/after of timing (27 and 51 frames) | The "before" build is gone, so the claim that timing is unchanged cannot be shown. Only the frame-quantized values were checked: 51 frames at 60 and 27 at 30 (`test_start_to_start_frames_unchanged` passes). | Cannot be done. |
| Real keyboard or gamepad | Not covered. Only scripted text runs were used. | — |

### What my means cannot show

I ran scripts through `play.py` and the test suite only. I cannot see human clarity, real input devices, a baseline, or runs that need the generated replay scripts. I did not read the test bodies, only their names in the inventory.

## Decisions already made

- D-028: the dash indicator is shown on the legacy route too (including room 5). The behavior observed matches.
- D-029: 30 FPS tolerance (0.90 s, ready at 1.500 for a dash at 0.6 s), public-driver pictures after dash messages, rule-driven refusals print, and evidence without a baseline for Q8 and Q12. The observed results agree with items 1–3.

## Constraints

- Dash rules and timing must stay unchanged. Both 30 and 60 FPS apply.
- QA does not fix, widen scope or decide intended behavior. The grid question below is a spec question.

## Open questions

1. **Source ids (from handoff 15).** Public `summary:` blocks show `source_id: 3951a3656940`, and the test run prints `3951a3656940` (evidence and D022 lines, `SPLIT_C`). The `bots.py` run (B1) failed before any header was printed, so I have no bots id to report. No id is printed by the legacy `play.py` runs. Earlier files cite `b62005468da6` and `aa28af2ce710`; neither appears in this round. I cannot tell whether the ids are the same kind, because I saw only one value.
2. **For `game-designer` (spec gap).** In the public driver the periodic pictures re-start their 0.5 s cadence after each event picture (1.350, 1.850, … after the `dash ready` picture at 0.850). Spec 3.5 and Q8(b) say the fixed grid, including after dash event pictures. `public-driver.md` says the cadence is retained after event pictures. Which text governs for the public driver? Whether this behavior predates the Goal cannot be shown.

## Expected output

The Studio:

1. Routes open question 2 to `game-designer`.
2. Decides whether to give QA one more round for the unverified items. The most valuable are Q5, Q7 and P12 via the replay scripts, which need generated scripts or a repo-side runner; the short P8/P9/P11 and attack-rule scripts are cheap. Or it accepts the listed items as unverifiable.
3. Keeps the Q8 and Q12 remainders and the no-baseline timing claim as explicit unverifiable items in the Review. Not a pass.

Reproduction commands for the checks above (no failure to reproduce):

```text
python3 -m unittest discover -s tests
python3 play.py --view player P30pre.txt   # room empty, fps 30, 0.6 dash right, 1.46 dash left, 1.5 dash left, end 3
python3 play.py --view player E60.txt      # room empty, fps 60, 0.6 dash right, 1.433 dash left, 1.45 dash left, end 3
python3 play.py --view trace  T60.txt      # same script as E60
python3 play.py --view player P13leg.txt   # room empty, fps 60, when nothing within 20 then dash right, when text "not ready" then move up, end 3
python3 play.py --view player P13pub.txt   # mode room, room empty, fps 60, limit 3, driver-limit 4, same two rules
python3 play.py --view player P13pubAside.txt   # mode room, room empty, fps 60, limit 3, driver-limit 4, spawn grub 10 4, when see g within 3 then dash toward
python3 play.py --view player R5pub.txt    # mode room, room 5, fps 30, limit 4, driver-limit 5, 0.6 dash right, 1.5 dash left
```

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/public-driver.md, repo/play.py, repo/tests/test_dash_refusal.py, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/15-studio-to-qa.md
