---
kind: handoff
goal: G-001
seq: 46
from: game-designer
to: studio
stage: Build
outcome: done
---
# 46: game-designer → studio — Room 3 ruling: accepted as built, criterion 11 reworded, no enemy change

## Task

Open one Build for `gameplay-engineer` with F2 and F3 only. The room 3 item (D-005 revisit) needs no build change. After the Build, open an independent QA re-verify that covers the "not run" list plus the new criterion 11 observation.

## Context

G-001. QA (43) failed build 0.6 on three items. F1 was ruled in 44 and D-006. This handoff rules the room 3 finding: with a surviving dashing player, the shot cap delays three cues together, all three spitters start cues at 6.8 s and shoot at 7.4 s, and up to 5 shots may be in the air against criterion 11's "never more than 3".

## Findings

- **Ruling: accepted as built.** The cap stays a limit on cue starts. It is not rechecked at shot release. The contradiction was in criterion 11's text, not in the rule, so the criterion is reworded: shots in flight never exceed 2 plus living spitters. That is at most 3 in rooms 4–5 (cue windows never overlap) and up to 5 in room 3 after a cap delay.
- **Reasons:** the cue is the telegraph and must always end in a shot. The three simultaneous lines are locked on one point, are all visible for 0.6 s, and one move of about 1 tile away from that point or a dash clears them all. Shots arrive spread over time (3.0 tiles/s over up to about 12 tiles). The case needs a player who keeps spitters alive. A fix would change the verified room 3 and force re-measuring of criteria 13, 15, 16 and 18.
- **Not observed:** the count of 5 is derived from timings. Whether a human can answer the burst is derived from geometry. Both are settled by the checks below.
- Full text: `design/combat-step-46-room3-cap.md` (governs criterion 11 and the cap paragraph over `design/combat.md`; fold in at the next edit). Decision: D-007. D-005 items 1–4, D-004 and D-006 are unchanged, so no hand-off to `game-director` is needed.

### Build change list

1. **Enemy code: none.** No rule, parameter, room or bot change from this ruling. Rooms 3–5 timing stays as 0.6, so the criteria 13, 14, 15, 18, 20 and 21 figures need no re-measuring because of this item.
2. **F2 (player view, criterion 19a).** Print "the brute shrugs off the swipe" at the moment of each swipe that damages but does not kill a brute in wind-up, at both rates. Acceptance: with the QA 43 script (brute at (9,4), player at (8,4), swipes at 0.1 and 0.5, `--view player`), both swipes print the message. A kill in wind-up prints no message. A swipe at a standard grub or runner is unchanged. Timings unchanged at 30 and 60 FPS.
3. **F3 (banner).** The player-view banner shows 0.6. Acceptance: every player-view output starts `Lantern Depths 0.6 — room …`, and nothing else changes.

### Acceptance for the re-verify of this ruling (criterion 11, amended)

- a. First shots: room 3 at 1.8, 2.6, 3.4 s ±1 frame; rooms 4–5 at 1.8, 3.0 s ±1 frame (as before).
- b. A cue starts only with fewer than 3 shots in flight, at both rates.
- c. In `play --view player`, run the QA 43 room 3 script (real room 3, `when see * coming within 2 then dash aside`, 15 s) at 30 and 60 FPS. Count `*` at 7.5 s and 11.7 s. Expected 3 to 5. A count above 5 is a build defect. 4 or 5 is a pass.
- d. In rooms 4–5 the count never exceeds 3 (traces or `*` counts).
- e. Each cue, including simultaneous ones, is 0.6 s ±1 frame before its own shot.

### Hand-timed playtest

Room 3, including a variant where the tester avoids killing the spitters for about 12 s so that a cap delay occurs. Reopen if the tester is hit by most of a simultaneous volley, says a shot "came out of nowhere", or a real-room count exceeds 5. The prepared fallback is a 0.2 s cue gap in room 3 (own spec step, supersedes D-005 item 4).

## Decisions already made

- D-001, D-004, D-005, D-006 as before.
- D-007 (new): room 3 simultaneous cues accepted; criterion 11 reworded; reopen triggers recorded.

## Constraints

- F2 and F3 must keep all timings unchanged at 30 and 60 FPS.
- The Build must not change the enemy update loop, the cap, the offsets or the cue gap rule.

## Open questions

None for Design. Still to be covered at re-verify (from 43): criteria 2, 6, 10, 17 (a–d), 19f, the isolated runner dash in 3, the runner's one-swipe death in 8, rooms 1–2 contents in 12, 18c with a killed spitter, 20e, 20f, 21b and the 16e decision logs (`log on`, to confirm walker differences between rates come from bot timing). Criterion 13 is judged against the limits in D-006 (walker 3–7 hearts, at least 2 rooms cleared).

## Expected output

Studio opens one Build (F2 and F3, with the acceptance above), then an independent QA re-verify covering the list above and criterion 11 a–e. The playtest of room 3 follows.

## Sender assessment

Confidence is medium-high that accepting is right. The geometry argument is derived, not observed. The risk is a human who cannot handle the volley, and the playtest and the `*` count cover it. The 0.2 s gap fallback is ready and cheap if needed.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/43-qa-to-studio.md
