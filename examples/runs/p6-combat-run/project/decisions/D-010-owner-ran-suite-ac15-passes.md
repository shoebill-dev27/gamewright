---
kind: decision
id: D-010
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-010: The Owner ran `run_tests` for the AC-15 rerun (Option A); 40/40 passes

## Decision

The Owner chose Option A of Escalation 48. The Owner ran `python3 -m unittest discover -s tests` in `repo/` with the unchanged `manual.md` beside it, and reported: Ran 40 tests, OK (40 of 40 passed, 0 failures).

AC-15 is therefore treated as passing. Together with 7g (39) and 7h (44), all Verify steps are done and Play (stage 8) opens. Limit: the run is the Owner's, not QA's. It was made in a sandbox on the Owner's behalf, against `manual.md` unchanged (D-009), and the result is the raw test output.

Owner's own words (2026-10-15): "A。manual.md は変更せず repo/ の隣に置いた環境で python3 -m unittest discover を実行しました（Owner の代理、サンドボックス内）。結果: Ran 40 tests — OK（40件中40件成功、失敗0）。"

No conditions were added by the Owner.

## Rationale

The test output itself is objective. It is the same procedure as D-008, and it clears the only open Verify item. Another QA round would have lacked the same input (`manual.md`, see 29, 40, 47).

## Alternatives considered

- Option B (the Owner places `manual.md` in QA's workspace, QA reruns): higher independence, but it was unclear whether the Owner could place the file there. It was not needed once A returned 40/40.

## Revisit when

The suite or `manual.md` changes after this run, so that AC-15 must be re-verified. Or a later build fails `ManualTest`. In that case the designer rules (D-009 "Revisit when").
