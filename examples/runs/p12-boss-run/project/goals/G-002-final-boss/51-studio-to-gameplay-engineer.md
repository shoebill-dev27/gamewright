---
kind: handoff
goal: G-002
seq: 51
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 51: studio → gameplay-engineer — continue D-022 with complete source inputs

## Task

Complete the D-022 supplements, acceptance tests, and manual update. Run the full suite, including the pause/retry tests from 46, and report results against the final source id.

## Context

50 returned partial because the packet omitted repo/play.py, repo/session.py, and repo/source_id.py. No repository changes or execution results were delivered in that step. Supply the complete current versions of these files with the other inputs below; this is a continuation of the same Build work, not a new design question.

D-021 authorizes implementation and Studio verification using the current text build. Real-device supply, external staffing, spending, and matching a specified sha are not prerequisites.

## Findings

Outstanding work:
- Implement the D-022 legacy room 5 leading note while preserving other legacy behavior and output.
- Implement per-attempt shot IDs and removal events.
- Implement the specified observation intervals and final per-attempt summary.
- Add acceptance coverage and update the manual.
- Execute the full suite, including tests/test_play_run_controls.py, against the final sources and record their source id.

The approved design and D-022 are authoritative for exact behavior and acceptance conditions. 50 contains the dependency report, not a verified implementation.

Split C remains a separate subsequent Build step: pause/retry-inclusive normal-run measurements and dodger regression fixtures for rooms 1–4.

## Decisions already made

- D-017: boss combat and continuous-run contract.
- D-019: applicable regressions and subsequent measurement/Designer judgment.
- D-021: current text build and independent Studio QA/Play are authorized.
- D-022: V1 supplements are specified; no further design clarification is currently pending.

## Constraints

- Preserve rooms 1–4, shared combat rules, and legacy timing/results/output except the specified note.
- Preserve existing tests without weakening or editing them.
- Exercise acceptance cases separately at 30 and 60 FPS.
- Report execution results only against the final source id; distinguish historical results.
- Do not start Split C before the full suite is green.
- Use supplied current source files; do not infer missing implementations.
- No additional spending, real-device procurement, or new combat inputs.

## Open questions

None about the specification. The operation packet must include complete current repo/play.py, repo/session.py, and repo/source_id.py, as well as the other listed inputs. If another concrete dependency is missing, identify it precisely and report completed work separately.

## Expected output

Return a handoff addressed to studio with outcome done when this continuation is complete, or partial with precise remaining work. Include changed files, acceptance coverage, exact run commands and results, final source id, and any unresolved failures. Do not claim independent verification.

Studio will route Split C after this work completes, then independent QA, limited Art Verify, independent Play, Designer measurement judgment, and Director Review. Do not begin those Roles' work.

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
- Previous handoff: goals/G-002-final-boss/50-gameplay-engineer-to-studio.md
