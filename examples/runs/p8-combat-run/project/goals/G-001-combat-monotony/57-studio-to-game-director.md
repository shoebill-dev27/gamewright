---
kind: handoff
goal: G-001
seq: 57
from: studio
to: game-director
stage: Review
outcome: routed
---
# 57: studio → game-director — Review G-001: is combat still monotonous? (second playtest and QA results)

## Task

Judge with `review-outcome` whether the Goal's intent is met on build 0.6.1: does combat play as varied and engaging rather than monotonous? Name the next issues. If the Goal is not met, say what the next pass should address, or whether a direction, priority or scope change is needed (new enemy type, healing, input, or any other change to D-001 or the pillars). Such a change is an Owner-level question; frame it as an escalation instead of deciding it.

## Context

Goal G-001, from the Owner: "戦闘が単調なので改善したい" ("combat is monotonous; I want to improve it"). Success condition (goal.md): different situations call for noticeably different play (positioning, timing, attack and dash) and the player can tell why. The change stays inside D-001 and the pillars.

History in short:

- A first playtest (02) found that melee enemies share one answer. Diagnose passes ran twice (04, 31).
- Design and Build followed (D-004 to D-007). Build 0.6.1 was verified by QA at 30 and 60 FPS (50).
- A second, fresh playtest (53, scripted at 60 FPS) reported that rooms still feel alike, that cautious play stalls, and that room 3 has simultaneous volleys.
- "Rooms feel alike" would be a third Diagnose pass without progress. The loop limit sends it to your review instead.

## Findings

From the second playtest (53), for you to weigh. Read the report itself:

- Rooms still feel alike.
- Cautious play stalls.
- Room 3 simultaneous volleys. The tester read them as readable, with no shot from nowhere and no count above 5, so the room 3 reopen triggers were not met (D-007).
- Three hits called unfair or unexplained.
- The same message for every lunger led the tester to waste dashes.
- Playtest limits: reactions were scripted, not live play, and four runs were truncated.

From QA (56) on the three hit moments:

- Not a defect, and the expected behavior is defined.
- Item 1 (room 2) and item 2 (room 5): the swipe landed after the wind-up had ended, because the grub was about 2 tiles away and out of the 1.5 reach during the whole wind-up. It hit during the lunge, which the design allows: a non-lethal swipe on a lunging grub does not cancel it.
- Item 3 (room 2, "no cue"): a cue was printed 0.48 s before the hit. The swipe at 5.0 s killed the other runner.
- Item 4: the message "a grub rears back" is the same for all variants, as documented. Whether the text view should name the variant is an experience question, and it is with `game-designer` (58).
- QA did not isolate the 30 vs 60 FPS course difference (a script timing effect, not a build defect under criterion 16). The player view at 30 FPS was not run.

Other state: tests pass (59). Visual criteria V1–V11 need a graphical build and are proposed as a new Goal at Close. V12 stays open until one exists.

## Decisions already made

- D-001: one attack button plus dash. No new input buttons without Owner approval.
- D-002 / D-003: contact-edge graze accepted; exact reach and lunge band.
- D-004: rooms 4–5 cue gap 0.6 s; the brute's wind-up is not cancelled by a swipe; room 2 spitter deferred.
- D-005: a blocked contact consumes the shot and spends the lunge's hit.
- D-006: walker limit in rooms 3–5 is 3–7 hearts.
- D-007: room 3 simultaneous cues accepted; criterion 11 reworded.

## Constraints

- Stay inside the vision pillars and D-001. A change to the core concept, a pillar or an Owner-made Decision goes to the Owner, not to you.
- Experience Goal: judge from the playtests and QA results in the Load list. Do not rely on any implementation explanation.
- Playtest evidence is scripted and limited, so say how much it supports your verdict.
- New issues become proposed Goals, not scope growth.

## Open questions

- Is the Goal met? Judge it against the success condition above, not the numeric criteria.
- If not met, which concrete next step: another Diagnose with specific findings, a Decide on a direction change, or an Owner escalation? Say why, given that two Diagnose passes did not remove the "rooms feel alike" report.
- A parallel Design step (58) is looking at manual wording on late swipes and the per-variant cue message. Note whether either belongs in your verdict.

## Expected output

A Review verdict (`outcome: goal-met` or `goal-not-met`) in a handoff addressed to `studio`, with reasoning, the next issues, and any Decision you record (templates/decision.md). If an Owner-level question arises, write the Escalation (templates/escalation.md) in `owner_language` (ja) instead, using `prepare-owner-escalation`.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md, studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, design/combat.md, repo/manual.md, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/53-playtester-to-studio.md, goals/G-001-combat-monotony/02-playtester-to-studio.md, goals/G-001-combat-monotony/31-game-designer-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/56-qa-to-studio.md
