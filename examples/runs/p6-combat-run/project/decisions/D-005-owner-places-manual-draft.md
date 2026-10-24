---
kind: decision
id: D-005
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-005: The Owner places the draft `manual.md` (Option A)

## Decision

For Escalation 21, the Owner chose **Option A**. The Draft `manual.md` from `goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md` ("Draft `manual.md`") was placed unchanged at the project root as `manual.md`.

Owner's own words (2026-10-15):

> A。18 の Draft manual.md を変更せずにプロジェクト直下の manual.md として置きました（Owner の代理として Studio の推奨案を採用）。

Conditions and limits:
- The file is the draft verbatim, with no edits. Whether it passes `ManualTest` (`REPO.parent / "manual.md"`) is still untested; the gameplay-engineer confirms this with `run_tests` (expected 34/34).
- The response says the Studio's recommendation was adopted on the Owner's behalf. The Studio treats this as the Owner's choice of A, as recorded in the Escalation.
- This is a one-time placement. It does not give the gameplay-engineer write access to `manual.md`. If later changes to `manual.md` are needed, they are a new question.

## Rationale

The draft was already checked against the implementation by reading, and placing it is quick and reversible. It unblocks AC-15 and V-5 without a change to the execution environment.

## Alternatives considered

- **B, give the gameplay-engineer write access:** matches D-004 item 5 but needs an environment change. Not chosen.
- **C, verify without `manual.md`:** AC-15, V-5 and `ManualTest` would stay unverified and the problem would return later. Not chosen.

## Revisit when

`run_tests` shows `ManualTest` failing on the placed draft, or QA/art-director find that the manual contradicts the build. Then `manual.md` needs another edit, which needs a write path (B) or another Owner action.
