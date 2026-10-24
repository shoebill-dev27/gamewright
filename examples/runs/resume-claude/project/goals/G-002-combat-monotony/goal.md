---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-10
---
# G-002: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success: in a playtest of the 5-room slice, the player has to make different decisions across rooms
(where to stand, when to dash, which enemy first) instead of repeating one pattern, and the Game
Director judges the monotony addressed on that evidence. Out of scope: new biomes,
meta-progression, run length. Also out of scope, per the Owner (D-002): any new input, including
hold-to-charge on the attack button.

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
| 4 | Decide | owner | — | done (D-002: Option A) | 04-game-director-to-owner.md |
| 5 | Design | game-designer | write-design-spec | done (spec: design/enemy-depth.md) | 05-studio-to-game-designer.md; result 06-game-designer-to-technical-director.md |
| 6 | Plan | technical-director | technical-plan | open | 06-game-designer-to-technical-director.md |
| 6b | Design (visual) | art-director | write-design-spec | tentative (needed if the plan finds the visual spec in enemy-depth.md section 7 blocks Build or Verify, e.g. marker look, non-colour cue) | — |
| 7 | Build | gameplay-engineer | implement-change | planned | — |
| 8 | Verify | qa | verify-change | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |

## Route changes

- After step 3: Option B would change Owner Decision D-001 while the evidence leaves A and B both
  viable → escalation triggers → step 4 (Owner); all later steps paused.
- After step 4: the Owner chose Option A (D-002), so the route continues as the escalation
  described for A. No D-001 replacement and no Decide step for B. The Owner added one condition
  (no hold-to-charge in this Goal), carried into the Design handoff. Steps 5–10 are confirmed
  `planned`; step 5 is now open.
- After step 5: the spec fits the plan (no direction conflict, no escalation trigger, no D-001 or
  pillar 3 conflict reported). Plan stays `planned` → open, since the work is cross-system and
  needs sequencing. Added tentative step 6b (art-director visual spec): the spec lists art
  follow-ups (section 7) that it does not decide, and the Technical Director's plan will say
  whether they gate Build or Verify. If they do not, drop 6b as skipped; the art work can then
  follow later as a proposed new issue.

## Next action

technical-director starts step 6 (Plan) from `06-game-designer-to-technical-director.md`. Then the
Studio routes again: confirm or drop 6b, and send the plan to gameplay-engineer (step 7) unless the
plan hands back a question.

## Outcome

—
