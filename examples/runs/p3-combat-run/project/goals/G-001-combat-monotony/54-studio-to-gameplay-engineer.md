---
kind: handoff
goal: G-001
seq: 54
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 54: studio → gameplay-engineer — Wording-only update of the Phase 1 build description (7 items)

## Task

Update the wording of the Phase 1 build description (`sim/build-0.7.md`) exactly as listed under Findings, and state the result in your Handoff. This is a wording-only change: no rule, timing, value, input or visual behavior changes. Address your result to `studio`.

## Context

G-001, Phase 1 (encounter escalation). Both re-checks of `sim/build-0.7.md` passed (QA, Art Director). The Game Designer then closed the remaining wording items (handoff 53) and changed no rule. The playtester will read the build description, so it must say the same thing as the amended spec (`design/g001-combat-escalation.md`, 3.3 and 3.4). The playtest waits for this update.

## Findings

Seven wording items from the Game Designer (handoff 53), all in the build description:

1. In "Choice of arrival point", replace "handled one after another in a fixed order" with: "handled one after another in the order they are listed in the room's arrival data (rows in room order, and within a row in the order the row gives)."
2. Replace "Spitters appear about 1.5 tiles along the wall from a corner." with: "In rooms 1 and 2 the Spitter appears on the east edge at mid-height (the other two east points are alternatives). In rooms 3 to 5 each Spitter appears about 1.5 tiles along its wall from a corner."
3. Name the covered corners: room 3, Spitter at the north edge near the north-east corner; room 4 wave 1, north edge near the north-west corner; room 4 wave 2, south edge near the south-east corner; room 5, one Spitter at the south edge near the south-west corner and one at the north edge near the north-east corner. Keep the sentence that a player standing in the covered corner makes the Spitter appear at the far end of that wall.
4. In "The arrival ring", change "Rooms 3 (wave 2) and 5 (wave 1, west edge) have rings at the same moment." so that it names rooms 3 (wave 2), 4 (wave 1, west edge) and 5 (wave 1, west edge).
5. In the sampling bullet, extend the caveat to: "... a very fast move across a 5-tile boundary, or an enemy moving across a 1.5-tile occupancy boundary, in that gap can change the point at one frame rate and not the other."
6. In "Test output", state that each ring start line and each appearance line carries the scheduled time (the frame time may also be given), as the Spitter shot line already carries the scheduled shot time.
7. Heading: the heading "Simulated build 0.3.3" is the same as in 0.6. Relabel it so it identifies the build this change produces (the label must match that build's file name).

Optional wording items QA and the Art Director raised earlier (the word "solid" for the ring's solid stage, and "linear in game time" for the ring brightness ramp): apply them only if handoff 50 or 51 gives the exact wording. If it does not, do not invent one; list them as "not done" in your Handoff.

Wording only. If any item cannot be done without changing behavior, or contradicts the spec, do not apply it: hand back `question` naming the item.

## Decisions already made

- D-008: Phase 1 spawn and wave rules (deterministic from ordered candidate lists).
- D-009: criteria 1 and 2 are judged at the playtest from counts; no rule change.
- D-001, D-003: unchanged.

## Constraints

- No change to any rule, timing, data value, wave, spawn point, dash, hit-stun, invulnerability, input or ring look (dot `#FFC14D`, 40% ramp, overlap cap stay as in 0.7).
- No Phase 2 content.
- The build description must keep behaving identically at 30 and 60 FPS; state in your Handoff that nothing but wording changed.
- Dry run: there is no code to run; state the change exactly (which sentence, what it says now), as in earlier Builds.

## Open questions

None. Report anything in the build description that still contradicts spec 3.3 or 3.4 and was not in the list above, without fixing it.

## Expected output

A Handoff addressed to `studio`: for each of items 1 to 7 the exact new wording and where it sits, the optional items done or not done, and a statement that no behavior changed. The Studio then routes the playtest (a fresh Handoff for the Playtester). QA does not re-verify unless you report that behavior changed.

## Sender assessment

Studio routing note: the items are copied from the Game Designer's list in handoff 53, which is the authority for their content. The Studio did not read `sim/build-0.7.md` and did not check that the quoted sentences exist as written; report any that differ.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: sim/build-0.7.md; design/g001-combat-escalation.md (3.2a, 3.3, 3.4); sim/repo-notes.md
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/53-game-designer-to-studio.md (also, for the optional items only: goals/G-001-combat-monotony/50-qa-to-studio.md and goals/G-001-combat-monotony/51-art-director-to-studio.md)
