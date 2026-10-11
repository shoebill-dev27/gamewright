---
kind: handoff
goal: G-001
seq: 52
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 52: studio → game-designer — Close the spec wording items from the Phase 1 re-verify and write a neutral playtest record sheet

## Task

(1) Settle the spec and wording items that QA's narrow re-verify of `sim/build-0.7.md` raised (list under Findings), changing the spec only where you decide a rule is needed. (2) Write a neutral playtest record sheet for the Phase 1 playtest: the positions to hold and the records to take, with no thresholds, expected results or implementation detail. Address the result to `studio`.

## Context

G-001, Phase 1 (encounter escalation, D-002, D-008, D-009). Both parallel re-checks of `sim/build-0.7.md` passed:

- QA (handoff 50): criteria 3, 4 (first-shot basis), 5 and 10 (c), (d), (g) pass at 30 and 60 FPS, on a build description and not a counted run; no regression against 0.5. Criteria 1 and 2 (Phase 1 part) are recorded "deferred to playtest" (D-009). Phase 1 stands as "verified, with criteria 1 and 2 open".
- Art Director (handoff 51): the arrival ring dot colour and statements S0–S3 pass on the described look. Nothing further for the Designer there.

The next step is the Phase 1 playtest. The playtester is not told what changed or what to expect, so the playtest record sheet has to come from you first.

## Findings

QA items for the Designer (none fails a criterion):

1. **Spec 3.3 wording.** The build states, and spec 3.2a/3.3 only imply: (a) same-start enemies are handled in a fixed order, and a ring started by an earlier one counts as occupying its point when the next is chosen; (b) enemies that have not yet started their ring do not count as occupancy; (c) the point is read on the first logic frame at or after the scheduled start. Decide whether to add these to 3.3 word for word, and whether "table order" is the intended fixed order (the build says "a fixed order" only).
2. **Spitter position, rooms 1–2.** Spec 3.4 puts the rooms 1–2 Spitter at E2 (mid-height), with E1 and E3 as alternatives. The build says generally that Spitters appear about 1.5 tiles along the wall from a corner. Confirm which statement is intended for rooms 1–2 and for rooms 3–5, and whether the room 3 Spitter corner (the build says "north edge near a corner") must be named in the spec.
3. **Overlap examples.** The build names room 3 wave 2 and room 5 wave 1 (west edge) only. Room 4 wave 1 also has two Grubs on the west edge at once. Say whether the spec needs the room 4 case named.
4. **Sampling caveat.** The build names only a fast move across the 5-tile boundary; the spec's margin rule also covers the 1.5-tile occupancy threshold. Confirm that the margin rule is the whole rule.
5. **Appearance log basis.** The criterion 4 no-tolerance check needs the scheduled appearance time as well as the scheduled shot time. State what the log must carry, if you hold that rule; wording of the build's log description would go to Build.
6. Carried unchanged for the playtest (spec 3.8 and 6a): the existing values (speeds, hearts, room size, hitboxes) are not available from the build; `SPAWN_FALLBACK` counts per room, arrival gaps of "simul." Grubs and real-time run length must be recorded by the playtest.

Studio note: a pending question for you, not an escalation. If the playtest is also a description with no counted attempts, criteria 1 and 2 stay "not judged". Say in your answer whether the record sheet is written so a tester can give counts where they exist and says "not available" otherwise, so Review is never offered an uncounted pass.

## Decisions already made

- D-001: one-button combat; no new input.
- D-003: input in hit-stun ignored.
- D-008: Phase 1 spawn and wave rules.
- D-009: criteria 1 and 2 judged at the playtest from counts; thresholds unchanged; no rule change.

## Constraints

- No new input, no change to verified dash, hit-stun or invulnerability behavior, correct at 30 and 60 FPS, no RNG in spawn choice.
- Do not change thresholds or the marker look (Art Director's; passed). A rule change needs a Decision if it constrains work beyond this step. If a change alters scope, a pillar or an Owner Decision, hand back to `studio`.
- The record sheet is given to a Playtester who works from the build and the player profile only. It must contain: five positions for rooms 4 and 5 (five attempts each: hits taken, death yes or no, as in spec 6a), the per-room "dash in combat and why" record for rooms 1–5, the neutral items P1 ("For each arrival, say when you first noticed it and what drew your attention to it") and P2 ("When more than one arrival was on the floor at the same time, say how many you saw and where each one was"), the records of 3.8 and `SPAWN_FALLBACK` counts per room, arrival gaps, and real-time run length and per-room clear time. It must not contain thresholds, pass or fail wording, which stance is expected to win, or any description of what changed.
- The A3 signal (do testers dodge a ring as if it were an attack) must be observable from the free-play notes without naming it as a hypothesis.

## Open questions

- Is a rule or only wording needed for items 1–5? If a build wording change follows, list it exactly for a narrow Build; if none, say so.
- Do the five positions need to be defined in room-relative terms (like the spawn data) so the tester can hold them without knowing the spawn points?

## Expected output

An update to `design/g001-combat-escalation.md` only where you decide it is needed (record a Decision if required), plus, in this handoff's reply (`53-game-designer-to-studio.md`, addressed to `studio`): your answers to items 1–5; the playtest record sheet as a self-contained block the Studio can paste into the playtester's Handoff; and an exact list of build wording items for Build, or "none". Do not address it to the playtester or the engineer; the Studio composes those.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md (sections 3.2–3.4, 3.8, 6, 6a, criteria 1–5 and 10); sim/build-0.7.md; project.md#player-profile
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/50-qa-to-studio.md
