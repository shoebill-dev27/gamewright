---
kind: handoff
goal: G-001
seq: 70
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 70: studio → game-designer — Room 3 variety: give the room a second kind of ask, inside D-001

## Task

Specify room content options for room 3 (spitters only) so the room stops reading as one repeated ask. Pick one inside your authority and write it as a spec with player-observable acceptance criteria. Use existing enemies and systems only.

## Context

Goal G-001 (combat feels monotonous). Review pass 2 found the Goal not met by a narrow gap and recorded D-010: no Owner escalation, because the remaining issue is design content inside D-001. Playtests 53 and 63 both found room 3 the most repetitive stretch: about 20 s of "aim, dash, shot lands behind me, again", with attention dropping. Part of the long standoff came from the tester killing two spitters and leaving the third in a far corner. Rooms 4–5, where several asks overlap, held attention well. Your step 68 already settled that the room 3 in-flight bound is D-007 (up to 2 plus the number of living spitters). That question is closed; do not reopen it.

## Findings

What the Director asked for (D-010, Review 67, issue 1):
- Room 3 should offer a second kind of ask, or avoid a long standoff against one cornered spitter.
- It must not break criterion 11 or the room 3 cue timing that teaches the aim cue.
- If your change touches the room 3 cap or the cue rule, state it clearly so one room 3 change is built and verified once. Otherwise leave D-004 to D-007 alone.
- Room 1 is a teaching room; leave it unchanged.
- Timeline: Build 22a (the D-011 messages and manual wording) runs in parallel. It does not touch room 3. Your room 3 change would be a later build.

## Decisions already made

- D-001: one-button combat. Attack and dash only; no new input.
- D-004 to D-007: stand. D-007 (room 3 in-flight bound, simultaneous cue starts after a cap delay accepted) is unchanged.
- D-010: Review pass 2; no Owner escalation; room 3 variety goes to Design.
- D-011 (accepted): variant-named messages, in Build 22a.

## Constraints

- Existing enemy types only (grub, runner, brute, spitter) and existing systems. A new enemy type, healing, a new input, or longer runs is outside this step. If you conclude it is needed, hand back to `studio` with a question that routes to `game-director`; do not specify it.
- Prefer changes that reuse existing systems (small team). Readable threats pillar: every threat visible before it can hurt.
- Must play correctly at 30 and 60 FPS.
- Acceptance criteria must be player-observable and checkable by QA from the spec and the build.
- Numeric tuning of room contents is yours; record a Decision if it constrains later work or rejects a real alternative.

## Open questions

1. Which room 3 option do you pick, and what are its player-observable acceptance criteria, including how a cornered lone spitter stops dragging the room out?
2. Does your option leave the cap and cue rule (D-005, D-007) as built, or change them?

## Expected output

A design note (new file under `design/`, for example `design/combat-step70.md`) and a handoff to `studio` with outcome `done`, listing the option chosen, the alternatives rejected, the acceptance criteria and whether a Build is needed. Address the result to `studio`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-step-46-room3-cap.md, design/combat-step68.md, design/combat-step59.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
- Previous handoff: goals/G-001-combat-monotony/68-game-designer-to-studio.md
