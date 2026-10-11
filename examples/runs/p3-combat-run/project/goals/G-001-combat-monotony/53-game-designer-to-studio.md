---
kind: handoff
goal: G-001
seq: 53
from: game-designer
to: studio
stage: Playtest
outcome: done
---
# 53: game-designer → studio — Wording items 1–5 settled (no rule change); neutral playtest record sheet for Phase 1; exact build wording list

## Task

Route the playtest record sheet below to the Playtester, route the build wording list to a narrow Build, and note that `design/g001-combat-escalation.md` was amended in wording only.

## Context

G-001 Phase 1. Both re-checks of `sim/build-0.7.md` passed (handoffs 50, 51). Criteria 1 and 2 (Phase 1) are open until the playtest (D-009). This handoff answers the QA items in handoff 52 and supplies the record sheet.

## Findings

### Answers to items 1–5

No rule changes. No new Decision is needed (D-010 not written): nothing constrains work beyond this step, and thresholds, marker look, scope and pillars are untouched. The spec was amended in wording only.

1. **Spec 3.3 wording.** Added word for word to 3.3: (a) same-start enemies are handled in a fixed order, and a marker started by an earlier one counts as an active marker when the next is chosen; (b) enemies whose marker has not started do not count as occupying; (c) position and occupancy are read on the same logic frame, the first at or after the scheduled start. "Table order" is the intended fixed order: the rows of the 3.2a candidate table from top to bottom, and within a row the order the row gives. The build says only "a fixed order" (see the build wording list).
2. **Spitter position.** Rooms 1–2: point E2 (E wall, mid-height), with E1 and E3 as alternatives. Rooms 3–5: the corner-covering rule, 1.5 tiles along the wall from the covered corner, with the far end of the same wall as the second point. The build's general "1.5 tiles from a corner" sentence is true only for rooms 3–5. The covered corners are: room 3 NE (N wall); room 4 wave 1 NW, wave 2 SE; room 5 SW and NE. The spec already names them (3.4); I added that the build description should name them too, because "north edge near a corner" does not.
3. **Overlap examples.** The spec needs no room 4 example: it has no overlap list, and the general rule covers every case. The build's example list is incomplete, so I list the room 4 wave 1 west-edge Grubs as wording for the build.
4. **Sampling caveat.** Confirmed: the margin rule in criterion 5 is the whole rule, and it covers both the 5-tile distance and the 1.5-tile occupancy distance. The build's caveat names only the 5-tile case (see the wording list).
5. **Appearance log basis.** I hold this rule (3.3, "Log basis"). The log must carry the **scheduled** timestamp on each ring start and each appearance line (it may also carry the frame time it was noticed), and the scheduled shot time on each Spitter shot line. The no-tolerance check compares scheduled shot time with scheduled appearance time. Item 6 (existing values, `SPAWN_FALLBACK` counts, "simul." arrival gaps, real run length) is carried into the record sheet below.

### Open questions answered

- **Rule or only wording for items 1–5?** Only wording. Nothing in the build changes behavior.
- **Are the five positions defined room-relative?** Yes. The sheet defines them from what the tester sees (corners of the walkable floor, centre of the room), so the tester needs no spawn points.
- **Studio note (counts):** the sheet is written so a tester gives a count where one exists and writes "not available" otherwise. A position with fewer than 5 attempts is reported with the attempts it has and is not turned into a pass. Review is never offered an uncounted pass. If the playtest is also a description with no counted attempts, criteria 1 and 2 stay "not judged" (spec 6a).
- **A3 signal:** observable from the free-play notes through prompts F2 and F3 below. They ask what the tester did between first noticing an arrival and the enemy appearing, and where they were relative to it. The hypothesis is not named.

### Exact build wording items (for a narrow Build, `sim/build-0.7.md`; wording only, no behavior change)

1. In "Choice of arrival point", replace "handled one after another in a fixed order" with: "handled one after another in the order they are listed in the room's arrival data (rows in room order, and within a row in the order the row gives)."
2. Replace "Spitters appear about 1.5 tiles along the wall from a corner." with: "In rooms 1 and 2 the Spitter appears on the east edge at mid-height (the other two east points are alternatives). In rooms 3 to 5 each Spitter appears about 1.5 tiles along its wall from a corner."
3. Name the covered corners: room 3, Spitter at the north edge near the north-east corner; room 4 wave 1, north edge near the north-west corner; room 4 wave 2, south edge near the south-east corner; room 5, one Spitter at the south edge near the south-west corner and one at the north edge near the north-east corner. Keep the sentence that a player standing in the covered corner makes the Spitter appear at the far end of that wall.
4. In "The arrival ring", change "Rooms 3 (wave 2) and 5 (wave 1, west edge) have rings at the same moment." to name rooms 3 (wave 2), 4 (wave 1, west edge) and 5 (wave 1, west edge).
5. In the sampling bullet, extend the caveat: "... a very fast move across a 5-tile boundary, or an enemy moving across a 1.5-tile occupancy boundary, in that gap can change the point at one frame rate and not the other."
6. In "Test output", state that each ring start line and each appearance line carries the scheduled time (the frame time may also be given), as the Spitter shot line already carries the scheduled shot time.
7. Heading: "Simulated build 0.3.3" matches the heading of 0.6. Relabel it so it identifies 0.7 (QA labeling note).

The ring look and the word "solid" go to the Art Director as QA routed them; nothing for the Designer.

## Decisions already made

D-001, D-003, D-008, D-009. Nothing here changes a decision.

## Constraints

No threshold change, no marker look change, no new input, no RNG, no change to verified dash, hit-stun or invulnerability behavior.

## Open questions

None for the Designer. For the Studio: if the playtest also yields no counted attempts, decide whether the dry run accepts "not judged" for criteria 1 and 2 (spec 6a).

## Expected output

Studio pastes the block below into the playtester's Handoff, unchanged, and sends the build wording list to Build.

### PLAYTEST RECORD SHEET (paste as is)

You play the build and fill in this sheet. Report what happened, in your own words where asked. Where a number exists, give the number. Where you cannot give it, write "not available". Do not estimate a number you did not count.

**Part A. Held positions, rooms 4 and 5**

Positions (defined from what you see on the floor):
- NW corner: the north-west corner of the walkable floor of the room, standing within 1 tile of both walls.
- NE corner, SW corner, SE corner: the same for the other three corners.
- Centre: the middle of the room, equally far from all four walls as best you can judge.

How to hold a position: begin each attempt at the start of the room, move to the position before the first arrival appears or as soon as you can, and stay there. You may turn to face the nearest arrival or enemy and swipe. Do not walk off the position and do not dash. An attempt ends when every enemy in the room is dead or you die.

Do 5 attempts per position in room 4 and 5 attempts per position in room 5 (50 attempts in all). If you cannot do all of them, do as many as you can and say which are missing.

For each attempt record:
- Room, position, attempt number (1 to 5)
- Hits taken (a number)
- Died: yes or no
- If you could not hold the position for the whole attempt, say so.

**Part B. Free play, rooms 1 to 5**

Play each room normally, with no position restriction. For each room record:
- F1. Did you dash in combat? yes or no. How many times? Why, in your words, each time.
- F2. For each arrival, say when you first noticed it and what drew your attention to it. (P1)
- F3. When more than one arrival was on the floor at the same time, say how many you saw and where each one was. (P2)
- F4. For each arrival, say where you were, whether you moved before the enemy appeared, and where to. Also describe what you did in that time, step by step.
- F5. Did you leave the spot you were standing on during the room? How often, and what made you move, in your words?
- Hits taken in the room and whether you died.

**Part C. Records and measurements**

- The number of `SPAWN_FALLBACK` lines in the log, per room (rooms 1 to 5). Write "not available" if you have no log.
- For each pair of enemies that arrived "at the same time", the time between the two enemies appearing, in seconds, and how you obtained it.
- Real elapsed time for a full run (rooms 1 to 5), and the clear time of each room, from when you gained control to when the last enemy died. Use a clock, not a guess.
- Values you can measure or read from the build: Grub speed, player speed, projectile speed and range, player hearts, room size (width by height, in tiles), and the Grub, player and Spitter hitbox sizes. Give how you measured each. Write "not available" for any you could not measure.
- Anything that surprised you, or any damage that seemed to come from nowhere, in your words.

### END OF RECORD SHEET

## Sender assessment

Confidence is high that no rule change is needed. The sheet has no thresholds, no expected results, no pass or fail words, no stance named, and no description of changes. I used "arrival" wording from P1 and P2. F4 is the A3 signal.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/g001-combat-escalation.md (3.3, 3.4, 6a, criteria 1, 2, 4, 5, 10); sim/build-0.7.md
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-game-designer.md
