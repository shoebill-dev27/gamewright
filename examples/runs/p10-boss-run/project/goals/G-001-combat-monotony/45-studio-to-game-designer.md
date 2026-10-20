---
kind: handoff
goal: G-001
seq: 45
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 45: studio → game-designer — Room 3: in-flight shot cap vs criterion 11 after cap delays (D-005 revisit)

## Task

Rule on the room 3 finding from QA's verification of build 0.6: when the shot cap delays several cues together, three spitters start cues at the same moment and shoot together. Up to 5 shots may be in the air, which contradicts criterion 11 ("rooms 1–5 never more than 3 in flight"). Decide whether this is accepted (reword criterion 11) or the rule changes. If the build must change, give a complete change list with player-observable acceptance criteria.

## Context

G-001 (combat monotony). Build 0.6 was verified by QA (43): FAIL, three items.
- F1, criterion 13 at 60 FPS (walker 7 hearts vs limit 6): already ruled in 44 and D-006 (limit 3–7, at least 2 rooms cleared). No further Design needed. QA will judge the figures against the amended limits at re-verify.
- F2, the player view does not print the brute shrug message (criterion 19a), and F3, the banner says 0.5 instead of 0.6: build defects for `gameplay-engineer`. They are independent of this question, but the Build waits for your ruling so the enemy code changes only once.
- The room 3 finding (this handoff).

## Findings

From QA (43), room 3 in a real room, 15 s, a scripted dasher who took no damage (reaction script `when see * coming within 2 then dash aside`), identical at 30 and 60 FPS:
- First shots at 1.8, 2.6, 3.4, as specified. Cue gap 0.8 s.
- The second cues are due at 3.6, 4.4 and 5.2, but none starts until 6.8. The cap delays them by 3.2 s, 2.8 s and 1.6 s.
- At 6.8 all three spitters start cues together and all three shoot together at 7.4. The pattern repeats at 11.0 (cues) and 11.6 (shots).
- QA's derivation: with 2 shots in flight at the cue-start check, up to 5 shots are in the air at 7.4. This is derived from timings, not observed, because the trace does not list shots. A player-view check of `*` at 7.5 s would settle the count.
- QA also noted a spec tension: the cap is checked only at cue start (D-005 area), while criterion 11 says never more than 3 in flight in rooms 1–5. They look contradictory when several cues are delayed together. The bound "2 + living spitters" (5 in room 3) does hold.
- It is unknown whether a human can answer three simultaneous lines. The scripted dasher was not hit.

Related QA facts for your ruling:
- Rooms 4–5 cap delay behaves per criterion 18: after the delay the cues are separated by 0.6 s with no overlap, at both rates. Do not break this.
- Simultaneous cue starts outside rooms 4–5 were accepted in D-005. This finding shows that room 3 reaches a fully simultaneous start through the cap delay, not only at spawn.

Not run by QA and still to be covered at re-verify (list so you can state anything undefined): criteria 2, 6, 10, 17 (a–d), 19f, isolated runner dash in 3, runner's one-swipe death in 8, rooms 1–2 contents in 12, 18c with a killed spitter, 20e, 20f, 21b, 16e decision logs, and an observed in-flight shot count.

## Decisions already made

- D-001: one-button combat; no new input.
- D-004: rooms 4–5 rule-based 0.6 s cue gap; brute not cancelled by a swipe; room 2 spitter deferred.
- D-005: blocked contact consumes the shot and spends the lunge; simultaneous cue starts outside rooms 4–5 accepted. QA's finding is the revisit trigger for the room 3 part.
- D-006: walker limit in rooms 3–5 is 3–7 hearts with at least 2 rooms cleared; no parameter change.

## Constraints

- Stay inside D-001 and the pillars, especially "readable threats": every threat is visible before it can hurt.
- Behavior at 30 and 60 FPS must stay equivalent; no new input, enemy type, healing or room content.
- Prefer a rule change that reuses the existing enemy update loop; the team is small.
- Do not break criterion 18 (rooms 4–5) or the criterion 13/14/15 bot figures without saying which criteria need re-verification. If you change the cap or cue timing, say what that does to rooms 3–5 and the bot expectations.
- If your ruling would change a Decision (D-004, D-005, D-006) or scope, say so and hand to `game-director` instead of deciding.

## Open questions

- Accept the room 3 behavior (reword criterion 11 to the actual bound, with the reason) or change the rule? Options you may weigh: accept as built; re-check the cap at shot release; stagger delayed cues by a fixed gap as in rooms 4–5; a lower cap for room 3.
- If accepted, is a hand-timed playtest of room 3 the check, and what outcome would reopen it?
- Record a Decision if the ruling constrains later work (D-005 follow-up).

## Expected output

An updated spec (`design/combat.md` or a step file named in your findings) with player-observable acceptance criteria, and a handoff addressed to `studio`. State explicitly the build change list, or "no build change" for this item. Studio then opens a single Build for this ruling plus F2 and F3, and after it an independent QA re-verify covering the "not run" list.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md, project.md#constraints, project.md#vision
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Previous handoff: goals/G-001-combat-monotony/43-qa-to-studio.md
