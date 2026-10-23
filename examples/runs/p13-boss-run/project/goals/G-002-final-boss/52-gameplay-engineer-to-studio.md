---
kind: handoff
goal: G-002
seq: 52
from: gameplay-engineer
to: studio
stage: Build
outcome: partial
---
# 52: gameplay-engineer → studio — shot lifecycle and legacy note delivered; observation work remains

## Task

Continue D-022 implementation with observation intervals, per-attempt summaries, remaining acceptance coverage, and final-source execution. Keep Split C deferred until the full suite is green.

## Context

51 supplied the missing source files. The packet also included unpersisted proposals and a historical run of those proposals: 142 tests, four failures. Those proposals are not the current repository baseline and are not delivered wholesale here.

## Findings

Delivered changes:

- `repo/play.py`: exactly one leading note for legacy room 5 player output.
- `repo/game.py`: opt-in public shot IDs, firing events, and removal events for lifetime, edge, hit, absorbed, and terminal cleared. Legacy logging retains its existing behavior.
- `repo/session.py`: integer shot sequence persists across room entry and resets on retry.
- `repo/run_driver.py`: diagnostic sessions enable shot tracking; trace active-shot records include ID, source, and indexed state.
- `repo/tests/test_d022_shots_and_note.py`: new controlled probes at both FPS for note scope, short-shot removal reasons and unchanged recovery timing, cross-room numbering, terminal clearing, retry numbering, legacy event isolation, and hidden player IDs.
- `repo/manual.md`: documents the note and shot event contract.

Existing tests were not edited. The unpersisted `test_v1_supplements.py` proposal is not added.

The integer counter avoids storing a session-bound allocator method in Game state, which caused the two historical fresh-state equality failures. The new dash fixture moves toward the projectile to exercise actual contact; the historical fixture dashed away and observed lifetime expiry.

Player-observable scope is limited to the approved legacy note. Public trace and session logs gain developer shot metadata; combat parameters and player message wording are unchanged.

Remaining work:

1. Implement parser dispatch and validation for `view-every` and numeric `trace-every`.
2. Implement bounded periodic output without thinning event output or changing simulation.
3. Reset observation scheduling appropriately on retry and preserve default output behavior.
4. Implement one final summary covering every attempt, outcomes, clocks, room times, boss entry hearts, hits, attacks, pauses, driver elapsed time excluding pauses, and processing time.
5. Complete L1 output/result equivalence coverage, public spitter/boss shared-sequence coverage, and O1–O6 coverage, including controlled 1200-second executions separately at 30 and 60 FPS.
6. Update interval/summary documentation and stale integration-gap descriptions.
7. Execute and inspect the full suite, including `tests/test_play_run_controls.py`, against the completed final sources and record their source id.

No execution was requested in this response. The runtime Build check should report the result of:
`python3 -m unittest discover -s tests`
against these saved changes. No new passing result, final source id, trace execution, or bot execution is claimed here. The packet's four failures are historical results from different proposed sources.

## Decisions already made

- D-017: boss combat, run progression, clocks, terminal priority, retry, and presentation.
- D-019: retained regressions and subsequent measurement and Designer judgment.
- D-021: current text build and Studio verification authorized.
- D-022: exact supplement behavior; no pending design clarification.

## Constraints

Preserve rooms 1–4, shared combat rules, legacy behavior except the note, and existing tests. Exercise acceptance cases independently at 30 and 60 FPS. Report results against the executed source id. Do not start Split C before the full suite is green. Independent QA remains required.

## Open questions

None. Remaining work is implementation and validation, not a missing dependency or design decision.

## Expected output

Route a continuation to gameplay-engineer. Deliver the remaining D-022 observation implementation, complete acceptance coverage and documentation, and full-suite results with the final source id. Return the completed Build report to Studio before Split C or independent verification.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (0.3 s).

```text
............................................................................................................................................
----------------------------------------------------------------------
Ran 140 tests in 0.223s

OK
```

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
- Previous handoff: goals/G-002-final-boss/51-studio-to-gameplay-engineer.md
