---
kind: handoff
goal: G-002
seq: 56
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 56: gameplay-engineer → studio — Split C delivery and independent-verification guide

## Task

Inspect the appended saved-source Build check before routing independent QA. Preserve the measurement evidence for subsequent limited Art Verify, fresh Play, Designer judgment and Game Director Review.

## Context

55 requested public-driver normal-run pause/retry measurements, retained independent dodger regressions and actual boss decision-log inspection. D-022 was previously executed at source `120ca2671495` with 149 tests.

## Findings

### Delivery and evidence provenance

Delivered `repo/tests/test_split_c.py`, README status updates and public-driver reproduction instructions. No combat, room data, bot policy, HP, input syntax or difficulty parameter changes are submitted. Player-observable behavior remains the approved D-017/D-022 behavior; this change adds engineering coverage and documentation.

The supplied run results contain two proposal executions:

- Round 1: source `187d2b2be59b`, 152 tests, one failure: the public replay's first attempt died rather than cleared. Its failed integration result is not completion evidence.
- Round 2: source `eff43c2d918c`, 152 tests, all successful in 2.886 seconds. The measurements below belong to that executed proposal.
- The final files written here are identified by the runtime's appended `## Build check`. Do not assign `eff43c2d918c` to these saved files without the appended source identification. The saved-source suite includes all three Split C tests and prints its actual source IDs and measurements. If that execution fails, return the concrete failure to engineering before QA.

### Reproduction

From `repo`, generate each FPS script separately:

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
python3 play.py --view trace run30.txt
python3 play.py --view player run60.txt
```

Both generated scripts support both views. Generation records the existing dodger's button presses through `_Proxy.press`; replay passes the resulting text through `play.read_script` and the public driver. No live bot, state injection, raised hearts or automatic enemy defeats occur during replay. The observer in the integration test reads paused state only.

Settings: build `0.6-g002-public-32`, dodger boss policy v1, reaction interval 0.15 seconds, ordinary initial position/facing and 3 hearts, game limit 1200 seconds per attempt, driver limit 141 seconds. Each FPS execution contains three attempts; reported trial count is one per FPS.

The first clear display pauses at driver time 7–9 seconds at 30 FPS or 10–12 at 60 FPS. Retry controls occur at driver times 120 and 140. Attempt 2 explicitly receives `0 stop`; attempt 3 receives `0 move up`, `0.1 stop`, `0.1 attack`. Attempt 1 also contains an old future `1100 dash left`.

### Public integration measurements

All times below are seconds, rounded to three decimals. Elapsed excludes pause but includes terminal waiting.

| FPS | Attempt | Outcome | Visited rooms | Run time | Driver time | Elapsed | Pause count/time | Terminal wait |
|---|---|---|---|---:|---:|---:|---|---:|
| 30 | 1 | clear | 1–5 | 86.967 | 120.000 | 118.000 | 1 / 2.000 | 31.033 |
| 60 | 1 | clear | 1–5 | 103.533 | 120.000 | 118.000 | 1 / 2.000 | 14.467 |
| 30 | 2 | death | 1 | 5.100 | 20.000 | 20.000 | 0 / 0 | 14.900 |
| 60 | 2 | death | 1 | 5.033 | 20.000 | 20.000 | 0 / 0 | 14.967 |
| 30 | 3 | unfinished | 1 | 1.000 | 1.000 | 1.000 | 0 / 0 | 0 |
| 60 | 3 | unfinished | 1 | 1.000 | 1.000 | 1.000 | 0 / 0 | 0 |

Execution ends at the driver limit, independently of the final unfinished combat outcome. Two retries occur per execution: victory→attempt 2 and death→attempt 3. Retry counts before attempts are 0, 1 and 2.

| FPS | Attempt-1 room times, rooms 1 / 2 / 3 / 4 / 5 | Transitions |
|---|---|---|
| 30 | 6.633 / 20.733 / 15.633 / 18.333 / 21.633 | four × 1.000 |
| 60 | 9.617 / 25.067 / 15.017 / 16.967 / 32.867 | four × 1.000 |

Attempt 1 at either FPS: first boss entry 3 hearts, zero hurts and no hurt sources, 41 successful attack starts, 12 boss hits. Dashes: 34 at 30 FPS and 45 at 60 FPS.

Attempt 2 at either FPS: three hurts, all source `grub`, hearts 2→1→0; zero attacks, boss hits or dashes; no boss entry or transitions. Room-1 time equals the attempt run time.

Attempt 3 at either FPS: zero hurts, one attack start, zero boss hits/dashes, no boss entry or transitions. It remains in room 1 with 3 hearts.

Total simulated driver duration is 141 seconds at each FPS. Measured processing time for the whole three-attempt execution was 0.129023 seconds at 30 FPS and 0.327988 seconds at 60 FPS. Per-attempt processing times are unavailable; these figures are headless processing, not human play time.

These are same-attempt session clocks, not sums of independent-room measurements.

### Pause, retry and input evidence

During the finite two-second pause, every sampled tuple of run time, room time, combat frame, clear-display frame count and session state is identical. The state is `room_clear`. All four transition durations remain exactly one run second; paused driver time does not enter either game clock.

After each retry, the observed entry is room 1, run time 0, room time 0 and 3 hearts. Subsequent attempt-specific inputs execute. No dash event occurs in attempts 2 or 3.

The `1100 dash left` sentinel is beyond this integration run's subsequent attempt durations; its nonappearance alone is not a complete pending-input-discard proof. `DriverDiscardTest.test_old_future_timed_input_is_discarded_on_retry` supplies the complementary controlled public-parser check. Fresh complete combat-state equality from both terminal outcomes is covered by session and boss-contract tests. Warning, protection, dash/queued-attack and boundary freeze cases remain in their dedicated contract tests.

### Retained independent rooms 1–4

One trial per room/FPS, ordinary 3 hearts, limit 60 seconds, unchanged dodger. Every result is clear with end hearts 3, loss 0 and no hurt sources.

| FPS | Room | Seconds | Attacks | Dashes |
|---|---|---:|---:|---:|
| 30 | 1 | 6.63 | 6 | 3 |
| 30 | 2 | 20.73 | 8 | 10 |
| 30 | 3 | 15.63 | 8 | 6 |
| 30 | 4 | 18.33 | 7 | 7 |
| 60 | 1 | 9.62 | 6 | 5 |
| 60 | 2 | 25.07 | 8 | 14 |
| 60 | 3 | 15.02 | 8 | 6 |
| 60 | 4 | 16.97 | 7 | 8 |

The retained regression test fixes clear outcome, zero loss, attack and dash counts, and times at the historical one-decimal precision. It also retains D-019's separate cross-FPS requirement: same clear result and per-room hearts-lost difference at most one. Rooms 3 and 4 each use at least one dash.

All historical times/dashes from 40 match at its reported precision. This establishes a new executable regression reference; it does not establish exact unrounded historical identity or equality with the unavailable pre-boss bot policy. Existing criterion-14 walker/dodger coverage is retained. No retired rooms-3–5 aggregate gate is restored.

### Boss logs and FPS comparison

Independent room 5, limit 120 seconds, one trial for each FPS/start-hearts pair:

| FPS | Start hearts | Outcome | Seconds | Loss | Attacks | Dashes | Decision lines |
|---|---:|---|---:|---:|---:|---:|---:|
| 30 | 3 | clear | 21.63 | 0 | 12 | 8 | 145 |
| 30 | 2 | clear | 21.63 | 0 | 12 | 8 | 145 |
| 60 | 3 | clear | 32.87 | 0 | 12 | 12 | 220 |
| 60 | 2 | clear | 32.87 | 0 | 12 | 12 | 220 |

Each hearts-matched pair has the same clear outcome and zero loss difference. Actual log samples show:

- Both FPS: approach from (8,4) toward B at (12,4), then hold on the charge warning and dash up at 0.900 seconds.
- At that dash, player x is 9.866667 at 30 FPS and 9.800000 at 60 FPS; reported charge ETA is 0.39 versus 0.38 seconds.
- The first short-shot dodge is down at 3.166667 seconds at 30 FPS and up at 3.150000 seconds at 60 FPS. The respective player positions are (9.866667,3.6) and (9.8,3.6).
- Both logs show holding off the locked attack line and returning to face/swipe at 2.400 seconds. Shot positions and velocities appear after emission.

Complete logs can be reproduced with `python3 bots.py SCRIPT`, using:

```text
bots dodger
rooms 5
fps 30
hearts 3,2
limit 120
log on
```

Repeat with `fps 60`.

#### Sender assessment

Engineering assessment, to strip before independent QA/Play: source inspection supports the approved observable-information policy: the boss branches use displayed B position, phase, attack name, locked direction/countdown and visible projectiles. Logs support avoidance followed by return to attack; samples alone do not prove the absence of every hidden-state dependency.

The first short-shot escape already differs between FPS, alongside different sampled positions and decision times. Later paths therefore cannot be treated as identical-input geometry probes. The measured historical boss difference remains approximately 11.24 seconds and four dashes; no new timing threshold is proposed and no contact-band explanation is asserted. Dedicated phase/contact contract tests, rather than bot duration, establish mechanics.

Round 2's successful proposal evidence supports completion, but only the appended saved-source check establishes this delivery's execution result. The earlier failed replay is explicitly preserved above; its precise cause is not established by the supplied results.

Normal bot completion remains 86.967/103.533 seconds, approximately 1.5–1.7 minutes, substantially below the 15–20-minute Vision. Pause and terminal waiting must not inflate combat duration. No HP increases, waiting or difficulty gates were added. Bot victory is neither difficulty acceptance nor evidence of the human experience.

### Independent QA acceptance and exercise guide

1. Run `python3 -m unittest discover -s tests` on saved sources and record the printed source ID. Independently generate and execute both public scripts in player and trace views.
2. Check R1/C1: actual regular-enemy defeats and entries 1→5, B alone in room 5, room clocks resetting, four one-second transitions, and first boss-entry hearts.
3. Check C2/T4: finite pause freezes both clocks and clear countdown; victory and natural death each accept retry into fresh room 1. Compare complete fresh state and exercise pending old inputs using the dedicated controlled discard test.
4. Check per-attempt summaries against event logs, including attack/boss-hit/dash/hurt counts, pause accounting, terminal waiting and final driver-limit outcome.
5. Independently exercise retained criteria 14/15/16c and boss comparisons at 3 and 2 starting hearts. Inspect full boss decision logs against visible information. Use B1–B10/T1–T4/C1–C3 and D-022 tests as reproducible controlled fixtures, not normal reachability substitutes.
6. Check V1 in player output and D-022 lifecycle/observation behavior against trace. V2 real keyboard/gamepad operation remains unverified under D-021.

No independent QA, Art Verify, Play or experience verdict is claimed. No engineering implementation work remains conditional on a green appended Build check; a saved-source failure must be corrected before routing.

## Decisions already made

- D-017: boss, progression, terminal priority, pause/retry and clocks.
- D-019: retained independent regressions, FPS comparisons and later Designer judgment.
- D-021: Studio text/script execution; no real-device provision or extra expenditure.
- D-022: public observation controls, summaries and shot lifecycle metadata.

## Constraints

Preserve rooms 1–4, shared combat and existing independent-room bot policy. Keep both FPS separate. Do not substitute controlled fixtures or independent-room time sums for normal reachability. Do not force duration with HP or waiting. No purchases or outsourcing. Strip engineering assessment and design-side experience expectations before Play routing.

## Open questions

None requiring specification clarification. Saved-source execution status is supplied by the appended Build check.

## Expected output

Studio checks the appended full-suite result and executed source ID. If green, route independent QA with the exercise guide and saved files, followed by limited Art Verify and fresh Play. Route the measurements and independent findings to Designer for D-019 judgment before Game Director Review, preserving the Vision-duration discrepancy. If the saved-source check fails, return the failure to gameplay-engineer.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (3.0 s).

```text
2-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.33148257399443537, "source_id": "04fa2b1c168a"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "04fa2b1c168a", "trial_count_per_room_fps": 1}
........................................................................................................................................................
----------------------------------------------------------------------
Ran 152 tests in 2.903s

OK
```

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/session.py
- Project: repo/game.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_play_run_controls.py
- Project: repo/tests/test_run_driver.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_boss_contract_details.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Project: goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/54-gameplay-engineer-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/55-studio-to-gameplay-engineer.md
