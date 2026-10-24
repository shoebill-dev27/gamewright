# Fixtures

Pristine Project Contexts for re-running Goals with the isolated runner (`scripts/studio_run.py`).
A fixture is a frozen Project Context state that a run starts from; runs never modify it.

| Fixture | State |
|---|---|
| `lantern-depths` | Build 0.3 of `examples/projects/lantern-depths`, before its G-001 and G-002: only D-001, the original combat design, the build with the dash defect, and pre-fix repository notes. |
| `lantern-depths-escalation` | The same project with Phase 1 G-002 frozen at its open Owner escalation (handoffs 01–04, no D-002): used to test Owner decision → fresh Resume. |
| `lantern-depths-real` | The same Project Context with a playable build in `repo/` (a headless Python combat simulation with tests) instead of `sim/`: the dash-invulnerability defect is real code. Declares `run_tests`, `run_play` (player view) and `run_trace` (internal state); `manual.md` is the player-facing script format. Carries the design and implementation canaries. |
| `lantern-depths-combat` | Build 0.4 of the playable project, before its combat Goal (`runs/p6-combat-run` started from its version at commit 6b57441; since Phase 7 the manual ships inside the build as `repo/manual.md`, `play.py` takes reaction rules, and grubs and shots are a little slower): the dash defect fixed, rooms and enemy speeds set so that the simple pattern (hold, face, swipe; step aside from shots) wins every room and dashing does not pay, as the project describes itself. Adds the team's balance bots (`repo/bots.py`, `run_bots`). |
| `tidepool-garden` | `examples/projects/tidepool-garden` as Phase 1 left it: G-001 run by hand through its first Route (steps 2 and 2b open, a Phase 1-style *Route changes* history, no Goal log), plus the dry-run Build convention and `sim/repo-notes.md`. No canaries. |

The `lantern-depths` fixtures carry canary strings in HTML comments (`ZX-...`). Tests assert that a canary reaches
an executor only through a file that executor's packet lists — e.g., the design canary never
reaches a Playtester and the implementation canary never reaches QA except via a written Handoff.
