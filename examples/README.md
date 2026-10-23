# Examples

Two sample Project Contexts used to dry-run the Studio. Neither game exists: builds and code are
simulated by files under each project's `sim/` (a player-observable description of each build, and
for `lantern-depths` a stand-in for reading the repository). `sim/` is dry-run scaffolding, not part
of the Project Context layout.

| Project | Genre and audience | Goals |
|---|---|---|
| `lantern-depths` | Top-down action roguelite; one-button combat | G-001 reproducible bug (short route, QA failure loop). G-002 monotonous combat (full expansion, Owner escalation and resume, spec question handed back, blind re-playtest). |
| `tidepool-garden` | Calm touch puzzle for children 7–10 | G-001 children stall at the first puzzle (left in progress here: Intake and the first Step/Route were run by fresh executors with no prior context; the Studio added the Art Director in parallel). Completed in `runs/p4-tidepool-run`. |

How the dry-runs were produced and what they revealed: `docs/phase1.md`.

## Phase 2: isolated re-runs

`fixtures/` holds frozen Project Context states; `runs/` holds Goals re-run from them by
`scripts/studio_run.py`, one fresh executor per operation. Each run directory has the produced
`project/` and a `records/` entry per operation (packet, manifest, raw output, session id).

| Run | What it shows |
|---|---|
| `runs/bug-claude` | The bug Goal end to end: QA → Engineer → QA, a Designer ruling on frame tolerance, no Director/Art Director/Playtester. |
| `runs/combat-claude` | The combat Goal end to end, including an Owner escalation and resume, an engineer spec hand-back, the Art Director joining only when needed, and a blind re-playtest. |
| `runs/resume-claude` | Owner decision on a frozen escalation → fresh Resume → a fresh Designer consuming the Owner Decision. |
| `runs/bug-codex` | The same fixture on Codex: Intake output produced, retry stopped by a usage limit. |
| `runs/bug-codex2` | The bug Goal on Codex only, completed to Close (35 operations): Owner escalations for missing reproduction details and for unmeasurable criteria, fresh resumes, and a recovery re-route (`route --since`). |

Results and findings: `docs/phase2.md`.

## Phase 3: continuous runs

| Run | What it shows |
|---|---|
| `runs/p3-bug-run` | The bug Goal finished by a single `run` (7 operations), no person in between. |
| `runs/p3-escalation-run` | `run` stops at once on an open escalation; after `decide`, it continues through parallel steps until its budget. |
| `runs/p3-combat-run` | The combat Goal under `run`: two genuine Owner escalations, parallel steps joined by one Route, a context request, policy rejections, and the runner fixes made along the way (see `docs/phase3.md`). |

## Phase 4: Goal log

| Run | What it shows |
|---|---|
| `runs/p4-tidepool-run` | tidepool-garden G-001 resumed from its Phase 1 state (`fixtures/tidepool-garden`) and finished by `run`: the Phase 1 *Route changes* history kept as the first Goal log entry, one log entry per Studio operation, `goal.md` holding only the current state, Route output flat across 19 Routes, spec gaps sent back to Design, a blind Playtester, and Close. `records/014-route` predates the runner's handling of an executor that cannot start (no `record.json`). |

Results and findings: `docs/phase4.md`.

## Phase 5: playable build

| Run | What it shows |
|---|---|
| `runs/p5-bug-run` | The bug Goal on `fixtures/lantern-depths-real`, one `intake` and one `run` (7 operations): QA reproduces with real traces at 30 and 60 FPS, the engineer fixes `repo/game.py` and adds tests it runs in the sandbox, QA verifies independently with 13 more runs, Close. The final build passes an oracle that never entered a packet (`tests/test_phase5.py`). Each Step's `runs-round*.json` holds the scripts and outputs. |

Results and findings: `docs/phase5.md`.

## Phase 6: experience Goal on the playable build

| Run | What it shows |
|---|---|
| `runs/p6-combat-run` | The combat Goal on `fixtures/lantern-depths-combat`, stopped before Close (78 operations, 120 executors). Live Playtesters played the real build from the player view only; the Director chose to rework the existing enemies (D-002); many Design/Build/Verify rounds on display details followed. `measurement.json` holds the held-out bots' measurement (criteria S1–S3 not met). Six Owner questions, all about `manual.md`, which no Role could write. |

Results and findings: `docs/phase6.md`.

## Phase 7: reactive play

| Run | What it shows |
|---|---|
| `runs/p7-combat-run` | The combat Goal again, from the updated `fixtures/lantern-depths-combat` (reaction rules, manual in the build), stopped at build 0.6.1 after two Reviews judged a narrow gap (59 operations, 101 executors, no Owner questions). Playtesters reacted from the player view and reached every room; the held-out measurement in `measurement.json` meets S1–S3. |

Results and findings: `docs/phase7.md`.


## Phase 8: EDIT blocks

| Run | What it shows |
|---|---|
| `runs/p8-combat-run` | A copy of `runs/p7-combat-run` continued with EDIT blocks (records from 065 on) until the Goal closed: Review pass 4 judged it met (97 operations, 167 executors in all, 66 of them in Phase 8, no Owner questions). Engineers wrote 52 EDIT blocks against 8 whole build files, and their output per attempt fell by about 80%. The held-out measurement in `measurement.json` meets S1–S3. The Outcome in `goal.md` still ends with a stray `>>>REPLACE` line, from the marker slip the runner now rejects. |

Results and findings: `docs/phase8.md`.

## Phase 9: the answer's shape at the end of a Step packet

| Run | What it shows |
|---|---|
| `runs/p9-answer-shape-replay` | The three recorded QA packets whose final answers dropped the Handoff's sections, re-sent twice as they were and twice with the Phase 9 ending (12 executors). As they were, 3 of 6 answers dropped sections; with the ending, 0 of 6 (one-sided Fisher p ≈ 0.09). The ending used there predates the recipient sentence added afterwards. `replay.py` re-runs it. |

Results and findings: `docs/phase9.md`.

## Phase 10: a second Goal on the same project

| Run | What it shows |
|---|---|
| `runs/p10-boss-run` | G-002 ("最後に手応えのあるボス戦がほしい") on the project as G-001 closed it, started on Codex and continued on Claude after the Codex engineer kept handing back unfinished work. Stopped inside Build at 78 executors (budget 100), before Close. Room 5 became a single boss; the held-out measurement in `measurement.json` meets S1–S3 and the pre-registered B1–B2. Shows the earlier Decisions carried into the new Goal, two Owner questions (one about scope, one about hardware the project never needed), and 25 operations of planning before Build. |

Results and findings: `docs/phase10.md`.

## Phase 11: `partial` and the build check

| Run | What it shows |
|---|---|
| `runs/p11-boss-run` | A copy of `runs/p10-boss-run` continued on Codex with the Phase 11 runner (records from 062 on). Engineers handed back `partial` twice and then `done`, so Build finished in 4 steps; every build-writing step got a passing `## Build check`. QA failed twice, partly on a real finding (the boss bot may use state the player cannot see) and partly because a Load entry named a directory and was silently dropped. Stopped at the third Owner question, 104 executors in all. The measurement in `measurement.json` meets S1–S3 and B1–B2. |

Results and findings: `docs/phase11.md`.

## Phase 12: Steps ask for files; Close refreshes the Current state

| Run | What it shows |
|---|---|
| `runs/p12-boss-run` | A copy of `runs/p11-boss-run` continued on Codex after the third Owner question was answered with what exists (records from 077 on). Steps asked for files with `@need` four times, no new Owner question came, and every build check passed; stopped inside Build again for budget (131 executors in all). The measurement in `measurement.json` meets S1–S3 and B1–B2. |
| `runs/p12-close-run` | The Phase 5 bug Goal run again from `fixtures/lantern-depths-real` on Claude to reach Close (9 operations, 16 executors): the closing Route rewrote only `project.md`'s Current state, a failing build check sent the fix back, and QA asked for a test source with `@need`. |

Results and findings: `docs/phase12.md`.

## Phase 13: a budget per Goal

| Run | What it shows |
|---|---|
| `runs/p13-boss-run` | A copy of `runs/p12-boss-run` continued on Codex under the budget rule (records from 092 on). Already past the default budget, the Studio added only a game-director scope step, cut the remaining work (D-025) and twice asked the Owner about cost with an itemized estimate. The Owner extended the budget once (D-026) and then stopped the Goal (D-027): the Resume closed it as `abandoned`, with an Outcome stating what was and was not done, and refreshed only `project.md`'s Current state. The measurement in `measurement.json` meets S1–S3 and B1–B2. |

Results and findings: `docs/phase13.md`.
