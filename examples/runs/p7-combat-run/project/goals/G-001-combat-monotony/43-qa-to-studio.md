---
kind: handoff
goal: G-001
seq: 43
from: qa
to: studio
stage: Route
outcome: fail
---
# 43: qa → studio — Verify of build 0.6 (criteria 1–21, 30 and 60 FPS): FAIL

## Task

Route the failures below to `gameplay-engineer`. Send the criterion 13 numbers to `game-designer` as a tuning question, which was already planned. Send the room 3 finding to `game-designer` as well, because D-005 says to revisit it. After the fixes, QA re-verifies. The items listed under "Not run" below must be covered then.

## Context

Verification of build 0.6 (`repo/`, sha 5eb065e08fef) against Design handoffs 35 and 38. Evidence comes from the executed runs: the unit tests, player-view and trace scripts at 30 and 60 FPS, and the bots. All times are game seconds. "30" and "60" mean the frame rate. Visual criteria V1–V11 are out of scope.

## Findings

### Verdict

**FAIL.** Three failures: criterion 13 (60 FPS), the missing brute shrug message in the player view (a defect of the player view, criterion 19a), and the version banner. Criterion 16 fails through 16b, because criterion 13 does not hold at 60 FPS. Criteria 18, 19 (trace behavior), 20 a–d and 21 a, c, d are met on the evidence listed. Several criteria were not run this round (list below), so no full pass can be claimed.

### Unit tests

`python3 -m unittest discover -s tests`: 54 tests, OK. Used as a regression signal only.

### Per criterion

| # | 30 FPS | 60 FPS | Evidence |
|---|---|---|---|
| 1 Telegraph | pass | pass | Standard grub: cue 0.033 → lunge 0.533 (30); cue 0.017 → lunge 0.517 (60). The hit in the second lunge lands 0.533 s (30) and 0.517 s (60) after the cue (c21std). |
| 3 Dash | pass (standard grub, brute) | pass (standard grub, brute) | A dash during the lunge gives 3/3 hearts after the dash ends (c21std, c21brute). Runner: not run in isolation. |
| 4 Standing still | pass | pass | brute30/60, c20a: the standing player loses hearts. |
| 5 Safe window | pass (brute) | pass (brute) | Brute recovery 1.6–2.0 with the brute 0.47 tile away and the player hurtable: no damage. Standard grub: the recovery overlaps the hurt window in my scripts, so it is not isolated. |
| 7 One at a time | pass (read) | pass (read) | Rooms 4 and 5 traces: never two grubs in wind-up or lunge together. Not a dedicated test. |
| 8 Variants | partial | partial | Brute takes exactly 4 swipes: 1+1 in wind-up, 1 in recovery, 1 kill (c19c). Runner's one-swipe death: not run. |
| 9 Cue timing | pass | pass | Every cue is 0.6 s before its shot in all spitter traces. The locked line was not observed. |
| 11 Stagger, cap | partial | partial | Room 3 first shots 1.8, 2.6, 3.4. Rooms 4 and 5 first shots 1.8, 3.0. All at both rates. **Shots in flight are not visible in the trace, so "never more than 3" was not observed. See the room 3 finding below.** |
| 12 Rooms | pass (rooms 3–5) | pass (rooms 3–5) | Contents match the table. Rooms 1–2 not viewed. |
| 18 Cue gap (rooms 4–5) | pass | pass | See below. |
| 19 Brute | pass in trace; **fail in player view** | pass in trace; **fail in player view** | See below. |
| 20 Consumed shot | a, b, c, d pass | a, b, c, d pass | See below. e, f not run. |
| 21 Spent lunge | a, c, d pass | a, c, d pass | See below. b not run. |
| 13 Spitter rooms (bots) | **PASS** | **FAIL** | Walker loses 7 hearts in rooms 3–5 at 60 FPS (limit 6). |
| 14 Grub rooms (bots) | pass | pass | |
| 15 Dash used (bots) | pass | pass | |
| 16 Frame-rate independence | **fail** | | 16b fails because of 13 at 60. 16c passes. 16e is not resolved (see below). |

**Criterion 18 (cue gap in rooms 4–5).**
- Rooms 4 and 5, still player: cues at 1.2, 2.4, 3.6, 4.8 and shots at 1.8, 3.0, 4.2, 5.4. The gap from shot to next cue is exactly 0.6 s and cue windows never overlap, at both rates.
- Cap delay, `dash aside` script, 15 s, rooms 4 and 5, both rates. The 3 shots in flight block both cues. Both spitters then become due together at 6.8 s.
  - A starts its cue at 6.8 and shoots at 7.4.
  - B starts its cue at 8.0 (gap 0.6 s) and shoots at 8.6.
  - A starts again at 9.2 (gap 0.6 s) and shoots at 9.8.
  - Later in the same traces the pattern repeats: a cue at 12.4, shot at 13.0, B cue at 13.6, shot at 14.2 (and A cue at 14.8 at 60 FPS).
  - All gaps are 0.6 s with no overlap.
- This is a naturally forced simultaneous schedule, so 18c (cap delay) and 18d (equivalent) are covered at both rates. The first shots were not forced to the same time.
- Not run: 18c with one spitter killed.

**Criterion 19 (brute not cancelled).**
- Wind-up swipes: practice room, brute at (9,4), player at (8,4), swipes at 0.1 and 0.5.
  - a: hp 4→3, a `shrug` event at 0.133 (30) and 0.117 (60). The cue stays (still shown at 0.5 s). The lunge comes 0.700 s after the cue (0.033→0.733 at 30, 0.017→0.717 at 60). 1 heart is lost.
  - b: two swipes give hp 2 and two `shrug` events, with one lunge.
- c: a kill in wind-up (c19c, hp 1, swipe at 2.3) gives `defeated`, no lunge, no shrug event.
- d: swipe at 0.1 plus dash at 0.7 (c21brute): no damage from that lunge, and hp stays 3 (the swipe damage is kept). The dash and lunge start on the same frame, so this is not a late dash.
- e: a recovery swipe at 1.2 gives hp 2→1, phase unchanged.
- f: not run this round (standard grub and runner still cancelled; criterion 6).

**Criterion 20 (consumed shot).**
- a, hurt window (c20a, spitter at (15,4), player at (8,4)). The grub hurts the player at 3.733 (30) / 3.700 (60). The window runs to 4.533 / 4.500. The first shot arrives at about 4.0, inside the window. **No hit at the window end** and hearts stay 2 until the next grub hit (5.1 / 5.033). Before 0.6 there was a hit at 4.533 / 4.483. The shot's disappearance frame was not observed, because the trace does not show shots.
- b, dash (c20b): the player dashes right into the shot line at 3.9 (30) / 3.867 (60) and ends the dash at x=12 on the old line. The first shot does no damage then or later. The only later hit is the second shot at 5.067 (30) / 5.05 (60), exactly its arrival time.
- c, normal hit: the same scripts give a hit at 6.4 (c20a) and 5.067 (c20b), on the arrival frame.
- d, room 4 still-player trace:
  - The shot arriving about 4.35 is consumed in the window at both rates.
  - 60 FPS: the next shot hits at 5.550, exactly its arrival time, and not at the window end (5.467).
  - 30 FPS: the window of the hit at 4.767 ends at 5.567, which is the same frame in which the shot's contact falls. The trace shows no shot hit at 5.567. The next damage is the runner at 5.8. The shot was consumed at the window-end frame. The spec accepts ±1 frame at this boundary. Hearts lost are identical at both rates; only the death time differs (5.8 vs 5.55). Reported as an observation, not as a fail.
- e (cap slots) and f (band) not run.

**Criterion 21 (spent lunge).**
- a, standard grub (c21std): the dash at 0.5 puts the player at x=0 against the edge. At the dash end (0.767 at 30, 0.75 at 60) the grub is at x=0.03 and still lunging. No damage. Hearts stay 3.
- c: the lunge is not shortened. The recovery is 0.8 s, and the next wind-up is at 1.667 (30) / 1.633 (60).
- d: the second lunge hits at 2.2 (30) / 2.15 (60).
- Brute: the same result (c21brute). Recovery 1.2 s and the next lunge hits at 3.0 / 2.95.
- b (hurt window ends inside a lunge) was not run.

### Failures and defects (reproduction)

**F1. Criterion 13 fails at 60 FPS.** `run_bots` with `bots camper,walker,dodger`, `rooms 1-5`, `fps 60`: the walker loses 2+3+2 = 7 hearts in rooms 3–5 (limit at most 6). Per the criterion text this is a fail. The limit question is routed to Design in parallel, and I did not adjust it. Severity: medium, a tuning question.

**F2. The player view does not print the brute shrug message (criterion 19a).**
- Reproduction: the script below, `python3 play.py --view player`.
  ```
  room empty
  fps 30
  spawn brute 9 4
  player 8 4
  0.1 attack
  0.5 attack
  end 4
  ```
- Expected (design 35, criterion 19a, handoff 41): the text "the brute shrugs off the swipe" at the moment of each swipe that damages but does not kill the brute in wind-up.
- Actual: only `0.100  you swipe: brute hit` and `0.500  you swipe: brute hit`. The same happens at 60 FPS. The trace view does contain `shrug {'enemy': 'brute'}` events, so the simulation is right and the player view omits the message.
- Severity: medium. The manual promises the message, and it is the only in-game signal of the brute rule.
- Acceptance for the fix: both swipes print the message at both rates. A kill in wind-up prints no message. A swipe at a standard grub or runner is unchanged.

**F3. The version banner says 0.5.** Every player-view output starts `Lantern Depths 0.5 — room …`, but the manual and README say build 0.6. Low severity. Acceptance: the banner shows 0.6.

### Bot figures (hearts lost / cleared)

| Bot, room | 30 FPS | 60 FPS |
|---|---|---|
| walker 1 | 3 / no | 3 / no |
| walker 2 | 2 / yes | 2 / yes |
| walker 3 | 0 / yes | 2 / yes |
| walker 4 | 1 / yes | 3 / no |
| walker 5 | 3 / no | 2 / yes |
| walker rooms 3–5 | 4 lost, 2 cleared | **7 lost**, 2 cleared |
| dodger rooms 1–5 | 0 lost, 5/5 | 0 lost, 5/5 |
| dodger dashes, rooms 1–5 | 3, 10, 8, 7, 11 | 5, 14, 10, 8, 14 |
| camper rooms 3–5 | 0 cleared, 9 lost | 0 cleared, 9 lost |
| camper rooms 1–2 | 1 of 2 cleared | 0 of 2 cleared |

- **13:** 30 passes (walker 4 hearts, 2 cleared; dodger 0 and 3/3; camper 0 < walker 2). 60 fails (7 > 6).
- **14:** pass at both rates. Walker rooms 1–2 lose 5 (at least 1). The dodger loses 0 and clears both. The brute policy of the dodger holds.
- **15:** pass at both rates. The dodger dashes in each of rooms 3–5 (30: 8, 7, 11; 60: 10, 8, 14).
- **16c:** pass. The dodger has the same cleared set and 0 vs 0 hearts.
- **16d/16e:** the walker differs between rates in rooms 3, 4 and 5. QA did not run decision logs (`log on`), so it is not confirmed whether the differences come from bot timing or from a build defect. This stays open for re-verification.

### Open questions, answered

**1. Does the player view print the brute shrug message?** No. See F2.

**2. Room 3 in a real room, 15 s, surviving player** (reaction script: `when see * coming within 2 then dash aside`, both rates; the player took no damage in 15 s):
- First shots at 1.8, 2.6, 3.4 as specified. The cue gap stays 0.8 s.
- **A cap delay occurs.** The second cues are due at 3.6, 4.4 and 5.2 but none starts until 6.8. The delay is 3.2 s, 2.8 s and 1.6 s.
- **Three cues start at the same moment** (6.8 s, all three spitters `aim; aim; aim`) and all three shoot together at 7.4. The same repeats at 11.0 (cues) and 11.6 (shots). Identical at 30 and 60 FPS.
- With the cap counted at each check (2 shots in flight when the three cues start), my derivation from the timings is that up to 5 shots are in the air at 7.4. This is derived, not observed, because the trace does not list shots. If so, the statement "room 3 stays at 3 or fewer" and criterion 11 ("rooms 1–5 never more than 3") would not hold in this run, although the 2 + living spitters bound (5) does. **Design should rule on whether this is accepted (D-005 revisit trigger).** A player-view check of `*` at 7.5 s would settle the count.
- The scripted dasher was not hit in 15 s. I cannot say from a trace whether a human can answer three simultaneous lines.

### Spec gap (for Design, not a fail)

Criterion 11 ("never more than 3 in flight in rooms 1–5") and the cap rule (the cap is checked at cue start only) look contradictory in room 3 when several cues are delayed together. See the finding above.

### Not run this round (must be covered at re-verify)

- Criteria 2, 6 (standard grub and runner cancel), 10, 17 (all of a–d), 19f, and the isolated runner dash in 3.
- Runner's one-swipe death in 8, and rooms 1–2 contents in 12.
- 18c with a killed spitter.
- 20e, 20f and 21b.
- 16e decision logs.
- The in-flight shot count.

## Decisions already made

D-001 to D-005 as in handoff 41. No limit or criterion was changed by QA.

## Constraints

- Production code was not touched.
- A fix to F2 or F3 must keep timings unchanged at both rates.

## Open questions

- Design: is the three-simultaneous-cue start and the possible 5 shots in the air in room 3 accepted (D-005 revisit)?
- Design: the criterion 13 limit at 60 FPS, with the numbers above.

## Expected output

Studio routes F2 and F3 to `gameplay-engineer`. Studio routes F1 and the room 3 finding to `game-designer`. Then Studio asks QA for a re-verify that covers the "Not run" list.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/41-studio-to-qa.md
