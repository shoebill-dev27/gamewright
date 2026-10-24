---
kind: handoff
goal: G-002
seq: 55
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 55: studio → gameplay-engineer — Split C: normal-run control measurements and retained dodger regression

## Task

Complete Split C: measure normal runs with pause and retry through the public driver control syntax, separately at 30 and 60 FPS, and fix retained dodger rooms 1–4 regression coverage. Return completed Build evidence and independent-verification instructions to Studio.

## Context

54 completed D-022. Its appended runtime check ran the saved sources successfully: 149 tests, source `120ca2671495`. Controlled 1200-second observations succeeded for player and trace at both FPS, with periodic counts 121 and 241 respectively. Those survival probes used raised hearts and do not establish normal reachability.

Split C is the remaining planned Build work before independent QA. No design clarification or Owner approval is pending.

## Findings

40 supplies historical measurements at source `5145454ab956`:

- Normal dodger run: victory at 86.967 seconds (30 FPS) and 103.533 seconds (60 FPS), no hurts, boss entry 3 hearts, four 1-second transitions, no pause or retry.
- Independent dodger rooms 1–4: all clear, no hearts lost at either FPS.
- Room times at 30 FPS: 6.6 / 20.7 / 15.6 / 18.3 seconds; attacks 8 in room 3 and 7 in room 4; dashes 3 / 10 / 6 / 7.
- Room times at 60 FPS: 9.6 / 25.1 / 15.0 / 17.0 seconds; attacks 8 in room 3 and 7 in room 4; dashes 5 / 14 / 6 / 8.

40 did not prove equality with the pre-boss bot policy. Treat its rounded figures as historical comparison data, not an exact unrounded baseline or proof of pre-change identity.

The public driver accepts `mode run`, `control <driver-seconds> pause|resume|retry`, attempt-specific inputs, separate game and driver limits, and final per-attempt summaries. A bots.py pause/retry run alone does not exercise this parser/control path.

## Decisions already made

- D-017 and the approved specification define progression, pause, retry, clocks and terminal priority.
- D-019 retains independent rooms 1–4 regressions and requires subsequent Designer judgment after independent QA and Play.
- D-021 authorizes text/script execution and Studio verification; real devices and additional expenditure are outside this Goal.
- D-022 defines observation controls, lifecycle metadata and summaries.

## Constraints

Preserve rooms 1–4, shared combat rules and the existing independent-room bot policy. Do not introduce difficulty gates, alter HP or add waiting to match the Vision duration.

Measure each normal-run attempt from its own session clocks. Do not sum independent room times as continuous-run evidence. Use normal initial hearts and actual regular-enemy defeats for reachability; identify any controlled state probes separately.

Do not claim independent QA or experience success. Do not route directly to QA: address the result to Studio. No purchases or outsourcing.

## Open questions

No specification question is pending. Report a concrete ambiguity or unworkable technical plan rather than deciding outside the engineering contract.

## Expected output

Return a handoff to `studio` containing:

1. Reproducible public-driver scripts or complete input-generation instructions for both FPS. Exercise finite pause/resume and terminal retry with explicit inputs for the next attempt. Cover retry from victory and death; controlled terminal probes may supplement but cannot replace normal-run reachability.
2. Actual per-attempt results: clear/death/unfinished, visited rooms, room and run times, transitions, first boss-entry hearts, hurts and sources, attacks and boss hits where observed, dashes, pause count/duration, retry count, driver time, elapsed time excluding pauses, terminal waiting and processing time. Distinguish measured fields from unavailable fields. Identify build/source, policy, limits and trial counts.
3. Evidence that pause excludes frozen time from game clocks, retry starts a fresh room-1 attempt, and old future inputs do not replay. Reference existing contract coverage where appropriate; use the public syntax in the integration measurements.
4. Retained dodger independent rooms 1–4 results at both FPS and meaningful regression coverage. Compare against 40 at its reported precision, preserve D-019's FPS comparison, and distinguish historical comparison from a new fixed baseline. Do not invent missing pre-change measurements.
5. Inspect actual boss decision logs at both FPS to support the approved observable-information policy and report the historical time/dash difference without inventing a timing threshold or treating bot victory as difficulty acceptance.
6. Necessary documentation updates and the full-suite command/result on final saved sources, with final executed source id. Separate executed evidence from proposed or unpersisted results.
7. A concise acceptance-criteria and exercise guide for independent QA, keeping engineering reasoning and confidence in `## Sender assessment`. List any unfinished work explicitly.

Studio will check completion and route independent QA, then limited Art Verify, fresh Play, Designer measurement judgment and Game Director Review. Preserve the known 1.5–1.7-minute bot-run observation for later judgment; it does not settle the human experience or Vision question.

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
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/54-gameplay-engineer-to-studio.md
