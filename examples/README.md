# Examples

Two sample Project Contexts used to dry-run the Studio. Neither game exists: builds and code are
simulated by files under each project's `sim/` (a player-observable description of each build, and
for `lantern-depths` a stand-in for reading the repository). `sim/` is dry-run scaffolding, not part
of the Project Context layout.

| Project | Genre and audience | Goals |
|---|---|---|
| `lantern-depths` | Top-down action roguelite; one-button combat | G-001 reproducible bug (short route, QA failure loop). G-002 monotonous combat (full expansion, Owner escalation and resume, spec question handed back, blind re-playtest). |
| `tidepool-garden` | Calm touch puzzle for children 7–10 | G-001 children stall at the first puzzle (in progress: Intake and the first Step/Route were run by fresh executors with no prior context; the Studio added the Art Director in parallel). |

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
| `runs/bug-codex2` | The bug Goal on Codex only: 25 operations including an Owner escalation for missing reproduction details and a fresh resume; stopped two operations before Close by Codex's weekly usage limit. |

Results and findings: `docs/phase2.md`.
