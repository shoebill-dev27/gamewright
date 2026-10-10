# Fixtures

Pristine Project Contexts for re-running Goals with the isolated runner (`scripts/studio_run.py`).
A fixture is a frozen Project Context state that a run starts from; runs never modify it.

| Fixture | State |
|---|---|
| `lantern-depths` | Build 0.3 of `examples/projects/lantern-depths`, before its G-001 and G-002: only D-001, the original combat design, the build with the dash defect, and pre-fix repository notes. |
| `lantern-depths-escalation` | The same project with Phase 1 G-002 frozen at its open Owner escalation (handoffs 01–04, no D-002): used to test Owner decision → fresh Resume. |

Each fixture carries canary strings in HTML comments (`ZX-...`). Tests assert that a canary reaches
an executor only through a file that executor's packet lists — e.g., the design canary never
reaches a Playtester and the implementation canary never reaches QA except via a written Handoff.
