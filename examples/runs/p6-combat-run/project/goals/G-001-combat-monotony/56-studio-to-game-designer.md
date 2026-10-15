---
kind: handoff
goal: G-001
seq: 56
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 56: studio → game-designer — Update the spec with A1, A2, A3, A5 and draft the manual changes

## Task

Specify the cheap fixes from your diagnosis (53) in `design/combat.md`: A1 wind-up spacing, A2 shorter stun, A3 body-hit rule, and the A5 gaps (dash and facing; the distance-0 swipe rule if A3 is not taken). Give each player-observable acceptance criteria that hold at 30 and 60 FPS. Also draft the group B manual changes.

## Context

G-001 (combat monotony), Option A (D-002). Your diagnosis (53) put the harshness of rooms 1–2 down to rules and tuning that your authority covers. The second playtest (54) agrees: in room 2, four grubs arrived together, reared back about 0.3 s apart, ended up in a ring around the player and bit in turns; the player was down in about 6 s and one swipe hit one of three adjacent grubs. Grubs on the player's tile were also hard to read (see handoff 57 for the display side). QA is checking the dash distance, facing and swipe cases in parallel (55); its results arrive after this step and may add defects, so settle the unspecified cases by rule, not by what the build happens to do.

Studio decision on routing: D1 (facing change) and D2 (room 1 composition) are not routed to the director now, as you recommended.

## Findings

Points to cover beyond 53:

- Check A1 against the room 2 ring: with four grubs, does spacing plus A3 let a player escape or counter, or should some limit on grubs adjacent to the player also be considered? Decide within your authority.
- A4 (cone width) stays held back. State what result of a retest would bring it in.
- Manual draft (group B): the interrupt, the knockback, the dash distance, the hit stun, and clearer wording for a swipe that is too far. Draft it as text in your outgoing Handoff for the Owner to place (D-005, D-007 pattern); do not edit `manual.md`. Keep the phrases that `ManualTest` checks (D-009).
- A guideline for the retest: say what a skilled player should be able to do in room 1 and room 2, qualitatively, so the next Play and Review have something to judge against. Numeric thresholds only as acceptance criteria.

## Decisions already made

- D-001: one attack button plus dash; no new input without the Owner.
- D-002: Option A first; staggered arrival (part of B) deferred.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.

## Constraints

- All timings in seconds; hold at 30 and 60 FPS.
- Reuse existing systems (small team).
- Record a Decision (`make-decision`) for the A1–A3 package, since it constrains the build and Verify, including the alternatives you rejected (A4, D1, D2) and when to revisit.
- If you conclude the cheap fixes cannot work without a facing mechanic or a room composition change, hand back to `studio` with the reason; that goes to `game-director`.

## Open questions

- Does A1 alone handle the ring of grubs in room 2, or is a second rule needed?
- What should the dash do to facing?

## Expected output

An updated `design/combat.md` (new acceptance criteria numbered after AC-18), a Decision, the manual draft and a retest guideline. Outgoing Handoff addressed to `studio` (it routes to Build, and to the Owner if the manual changes).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md, design/combat-visuals.md, manual.md, project.md#constraints, goals/G-001-combat-monotony/54-playtester-to-studio.md (the second playtest report)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md
- Previous handoff: goals/G-001-combat-monotony/53-game-designer-to-studio.md
