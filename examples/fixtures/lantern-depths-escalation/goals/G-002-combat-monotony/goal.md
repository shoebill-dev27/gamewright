---
kind: goal
id: G-002
project: lantern-depths
status: blocked-on-owner
created: 2026-10-10
---
# G-002: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success: in a playtest of the 5-room slice, the player has to make different decisions across rooms
(where to stand, when to dash, which enemy first) instead of repeating one pattern, and the Game
Director judges the monotony addressed on that evidence. Out of scope: new biomes,
meta-progression, run length.

## Unknowns

All stages of route pattern 2 are open: the monotony has not been observed or diagnosed, a
direction choice is likely (D-001 limits some options), new behavior will need a spec and a plan,
and it is an experience Goal (Play, Review).

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 02-playtester-to-game-designer.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done (escalated) | 03-game-designer-to-game-director.md |
| 4 | Decide | owner | — | open | 04-game-director-to-owner.md |
| 5 | Design | game-designer | write-design-spec | planned | — |
| 6 | Plan | technical-director | technical-plan | planned | — |
| 7 | Build | gameplay-engineer | implement-change | planned | — |
| 8 | Verify | qa | verify-change | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |

## Route changes

- After step 3: Option B would change Owner Decision D-001 while the evidence leaves A and B both
  viable → escalation triggers → step 4 (Owner); all later steps paused.

## Next action

Waiting for the Owner on 04-game-director-to-owner.md.

## Outcome

—
