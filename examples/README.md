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
