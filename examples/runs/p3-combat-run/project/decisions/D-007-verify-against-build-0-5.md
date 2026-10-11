---
kind: decision
id: D-007
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-007: Verify the hit-stun input change against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated

## Decision

The Owner chose Option A of Escalation 27 in substance. The build description that reflects the Build 3c change (handoff 20) already exists as `sim/build-0.5.md`. QA re-verifies the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md`. `sim/build-0.4.md` is an outdated version and is no longer the build under verification.

Owner's words (from Escalation 27): "A の内容はもう用意されています。ハンドオフ20の変更を反映したビルドは sim/build-0.5.md にあります（sim/build-0.4.md は古い版です）。0.5 で QA に再検証させてください。"

Limits:
- No change to the acceptance criteria (handoff 23, criteria 1–6) or to D-003.
- Options B and C are not used. QA verifies from the build description and does not rely on the engineer's account.
- The Owner added no further conditions.

## Rationale

The only blocker was that the build description lacked the hit-stun statements. The Owner supplied a description that has them, so the independent verification QA's Role requires can proceed without reducing its scope or independence.

## Alternatives considered

- Option B (use Handoff 20 as a substitute build record): lowers QA independence. Not needed now.
- Option C (carry criteria 2 and 5 forward and start Phase 1): leaves D-003 unverified under Phase 1. Not needed now.

## Revisit when

If `sim/build-0.5.md` also turns out not to state the hit-stun behavior, QA hands back `question` a fourth time for the same input. Do not route to a Role again; escalate to the Owner for that input (loop limit).
