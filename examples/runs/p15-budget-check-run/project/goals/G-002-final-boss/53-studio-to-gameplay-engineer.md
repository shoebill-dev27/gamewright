---
kind: handoff
goal: G-002
seq: 53
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 53: studio → gameplay-engineer — Complete D-022 observation and final validation

## Task

Complete the remaining D-022 observation implementation, acceptance coverage, and documentation. Execute the full suite against the completed saved sources and record their source id; return the Build report to Studio before Split C.

## Context

52 delivered partial implementation. Its runtime Build check ran `python3 -m unittest discover -s tests` successfully: 140 tests, exit 0. This verifies that saved intermediate build only; remaining D-022 work is not complete.

50 and 52 are two consecutive partial returns for this continuation. Continue with the same Role because no input or design question remains. If the same work returns partial a third time, Studio will route to Technical Director for splitting or replanning.

## Findings

52 delivered:
- One leading note for legacy room 5 player output.
- Opt-in shot IDs, firing events, and removal events.
- Shot numbering carried across room entry and reset on retry.
- Diagnostic shot tracking and active-shot trace metadata.
- Controlled shot and note probes, plus related manual documentation.

Remaining work:
1. Implement parser dispatch and validation for `view-every` and numeric `trace-every`.
2. Implement bounded periodic output while preserving event output, simulation behavior, and default output.
3. Reset observation scheduling on retry as specified.
4. Implement one final summary covering every attempt and the D-022 fields: outcomes, clocks, room times, boss entry hearts, hits, attacks, pauses, driver elapsed time excluding pauses, and processing time.
5. Complete L1 output/result equivalence coverage, public spitter/boss shared-sequence coverage, and O1–O6 coverage, including controlled 1200-second executions separately at 30 and 60 FPS.
6. Update interval and summary documentation and stale integration-gap descriptions.
7. Execute and inspect the full suite, including `tests/test_play_run_controls.py`, against the completed saved sources and record their source id.

Use the approved spec and D-022 for exact behavior. Historical unpersisted proposals described in 52 are not the current baseline.

## Decisions already made

- D-017: boss combat, continuous run, clocks, terminal priority, retry, and presentation contract.
- D-019: retained regressions and subsequent measurement and Designer judgment.
- D-021: current text build and Studio verification authorized; no real-device supply or verification requirement for this Goal.
- D-022: supplement behavior is settled; no pending design clarification.

## Constraints

Preserve rooms 1–4, shared combat rules, and legacy behavior except the approved note. Preserve existing tests. Exercise acceptance cases independently at 30 and 60 FPS.

Do not start Split C until this implementation is complete and its full suite is green. Split C remains a later Build step for pause/retry normal-run measurement and dodger rooms 1–4 regression fixation. Independent QA follows the completed Build work.

No purchases, outsourcing, or additional expenditure. Do not change approved scope or resolve new spec ambiguities through implementation.

## Open questions

None currently. If a new spec ambiguity or unworkable plan is discovered, identify it precisely and hand back under the Role contract.

## Expected output

Return a handoff addressed to `studio` with:
- Delivered files and completed acceptance cases.
- Documentation updates.
- Actual full-suite command, result, and final executed source id.
- Separate 30/60 FPS long-observation execution evidence.
- Any remaining work or concrete blocker.

Distinguish automated Build evidence from independent verification. Do not claim completion based solely on the intermediate 140-test result. Studio will route Split C after completion, then independent QA.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/play.py
- Project: repo/session.py
- Project: repo/source_id.py
- Project: repo/run_driver.py
- Project: repo/game.py
- Project: repo/bots.py
- Project: repo/tests/test_d022_shots_and_note.py
- Project: repo/tests/test_play_run_controls.py
- Project: repo/tests/test_run_driver.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_boss_contract_details.py
- Project: repo/tests/test_bots_boss.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/52-gameplay-engineer-to-studio.md
