---
kind: handoff
goal: G-001
seq: 8
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 08: studio → game-designer — rule the flare stun timing and the hound bite at lunge distance 1

## Task

Answer two spec questions the Build raised, amending `design/game-spec.md` and `design/acceptance-criteria.md` only if the answer differs from what is built.

## Context

G-001: first playable five-floor run. The Build (handoff 05) chose readings where the spec was silent or ambiguous. Two are left for you; the check-14 question was answered in handoff 06 / D-002. Build is continuing in parallel (handoff 07) with the built readings, and Verify waits for both.

## Findings

1. **Flare stun.** Stun is 2 and is decremented in the lighting turn's own creature phase. Effect: the creature shows as "stunned" in only one frame, but skips 2 actions. Question: does "next 2 turns" include the lighting turn's creature phase (reading A, built) or start after it (reading B, a one-line change to `STUN_TURNS`/the decrement)?
2. **Hound bite at lunge distance 1.** A hound that springs while the player is directly adjacent in the line bites for 3 (the hound hunts statelessly at path distance ≤ 6). Question: is that correct (built), or should "cannot move" mean no damage?

Note: a built reading that agrees with the spec text and the pillars costs nothing to ratify. Changing it costs a Build return. Change one only if it contradicts the spec or a pillar (readable threats, a decision every turn), and say which.

## Decisions already made

- D-002: threat marks plus reach marks; check 14 strict. Marks follow the planner, so the answers must be expressible as planner rules.

## Constraints

- Within the vision and Goal scope; no change to numbers beyond what the answers need.
- Keep the 30 checks and their numbering.

## Open questions

The two above.

## Expected output

A Handoff to `studio` (outcome `done`): for each question, the ruling and its reason; if a ruling differs from the built reading, the exact rule and the check(s) amended so that Build and QA can apply it. Amend the design files in place if needed.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md
- Decisions: decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/05-gameplay-engineer-to-qa.md
