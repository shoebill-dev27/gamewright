---
kind: handoff
goal: G-002
seq: 54
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 54: gameplay-engineer → studio — D-022 observation implementation delivered

## Task

Inspect the appended final-source Build check. Route Split C only if the full suite is green, then route independent verification.

## Context

53 requested completion of D-022 observation controls, summaries, acceptance coverage and documentation after the intermediate 140-test build. The packet supplied a successful run of an unpersisted proposal; that result is distinguished from this saved delivery.

## Findings

Delivered files:

- `repo/play.py`: dispatches `view-every` to the public parser.
- `repo/run_driver.py`: validates numeric observation intervals, retains `trace-every frame`, bounds periodic output without thinning events, resets schedules on retry, and prints one final summary for both views.
- `repo/tests/test_d022_observation.py`: nine acceptance tests, independently exercised at 30 and 60 FPS where applicable.
- `repo/manual.md`, `repo/README.md`, `repo/public-driver.md`: interval syntax, summary fields, output bounds and remaining integration work.

Player-observable changes follow D-022: optional slower periodic pictures, unchanged immediate event messages, execution-time validation errors, and one final public summary. Default player cadence is retained. Default trace records retain their existing shape. Legacy output is unchanged beyond the previously delivered note.

Summaries cover every attempt: clear/death/unfinished outcome, run time, visited room times, first boss-entry hearts, hurts, attacks, pause count and duration, driver time, driver elapsed excluding pauses, processing seconds and source id. Execution stop remains separate from combat result.

Acceptance coverage includes L1 note/output/event/result/time equivalence and the unchanged 60-second cap, public boss/spitter shared shot numbering, O1 bounded periodic output, O2 event/result equivalence, O3 default/explicit half-second equivalence, O4 one summary at clear/death/limit with retry/pause accounting, O5 invalid intervals, and O6 controlled 1200-second executions.

Historical evidence supplied in this packet:

`python3 -m unittest discover -s tests`: 149 tests, exit 0, 2.299 seconds, proposal source `b337ca3e09cf`.

Separate controlled long observations in that run:

| FPS | View | Run seconds | Periodic output |
|---|---|---|---|
| 30 | player | 1200 | 121 / 121 |
| 30 | trace | 1200 | 241 / 241 |
| 60 | player | 1200 | 121 / 121 |
| 60 | trace | 1200 | 241 / 241 |

That source is not claimed as this delivery's source. This delivery strengthens numeric-trace equivalence and malformed-interval coverage and retains default trace record shape. The runtime's appended Build check is the authoritative full-suite result for these saved sources. The long-observation test prints the final executed source id separately for each FPS/view pair, along with actual time and periodic counts. The full discovery command includes `tests/test_play_run_controls.py`.

These are automated Build probes, not independent verification or continuous reachability evidence. Long observations deliberately raise hearts to survive 1200 seconds in normal-run mode; they do not demonstrate normal survival, progression or completion. No new bot measurement is claimed.

Implementation and documentation are complete for this continuation. Split C measurements and independent verification remain later work. Any failure in the appended final-source check must be resolved before Split C.

## Decisions already made

- D-017: combat, progression, clocks, pause, retry and presentation.
- D-019: retained regressions, measurement and subsequent Designer judgment.
- D-021: text/script Build and Studio verification authorized.
- D-022: legacy note, developer shot lifecycle metadata and long observation controls.

## Constraints

Preserve rooms 1–4, shared combat rules and existing tests. Evaluate 30 and 60 FPS separately. Do not equate controlled survival with normal-run reachability. No purchases, outsourcing or additional expenditure. Independent QA, limited Art Verify and Play remain required.

## Open questions

None.

## Expected output

Studio inspects the appended full-suite result and final executed source id. If green, route Split C for normal-run pause/retry measurements and retained dodger rooms 1–4 regression fixation. Then route independent QA and subsequent verification and judgment steps. If the final-source suite fails, route the concrete failure for correction before Split C.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (2.4 s).

```text
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=120ca2671495
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=120ca2671495
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=120ca2671495
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=120ca2671495
.....................................................................................................................................................
----------------------------------------------------------------------
Ran 149 tests in 2.287s

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
- Project: repo/run_driver.py
- Project: repo/session.py
- Project: repo/game.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/tests/test_d022_observation.py
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
- Previous handoff: goals/G-002-final-boss/53-studio-to-gameplay-engineer.md
