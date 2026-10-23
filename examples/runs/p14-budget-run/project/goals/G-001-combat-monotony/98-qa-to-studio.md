---
kind: handoff
goal: G-001
seq: 98
from: qa
to: studio
stage: Verify (report for routing to Review pass 4 or back to Build)
outcome: fail
---
# 98: qa → studio — Verification of W1–W8 on build sha 0f2c1f134c79: NOT a pass (manual defect, several criteria not fully shown)

## Task

Report the pass/fail result per criterion W1–W8 at 30 and 60 FPS, the suite and bots results, and regressions. Route to Build if the manual defect below is confirmed. Otherwise decide whether the unshown items are accepted as known gaps.

## Context

Verification of the wording-only change from `design/combat-step94.md` (handoff 97). This round had one set of runs: tests, bots and play views. The results hold play-view runs only. No `--view trace` run is in the results, and no previous build or baseline output was available. Zero rounds are left, so unshown items stay unshown. I did not modify any code.

## Findings

**Verdict: fail.** W1 and W5 pass. The player-visible manual shows a defect. W2, W3, W4, W6, W7 and W8 are only partly shown or not shown.

### Suite and bots
- Suite: `python3 -m unittest discover -s tests` ran 69 tests, OK, exit 0.
- Bots ran at 60 FPS only. No 30 FPS bot run was possible in this packet.
  - Walker: rooms 3–5 summed 6 hearts lost and 2 cleared. Rooms 1–2: 5 hearts lost.
  - Dodger: 5/5 cleared, 0 hearts lost, dashes in every room (rooms 3, 4 and 5: 6, 8 and 14).
  - Camper: 0/5 cleared.
  - Against the combat.md limits (criteria 13, 14, 15): walker 6 hearts, within 3–6; walker clears 2 of rooms 3–5; dodger at most half the walker's hearts and clears 3/3; camper clears fewer than the walker; rooms 1–2 walker loses at least 1, dodger loses at most 1 and clears both; dodger uses at least 1 dash in each of rooms 3–5. All hold at 60 FPS.
  - The bots classify hits as "shot", so the unchanged prefix `YOU ARE HIT by a shot` still parses.
  - There is no baseline in the packet, so "bots as before" (W7) is not shown. These are the current values only.

### W1 Direction words (spitter and player in the practice room, player at (8,4), both rates)

| Spitter at | Hit line seen, 30 FPS | Hit line seen, 60 FPS | Expected | Result |
|---|---|---|---|---|
| (15,4) | 4.000 `YOU ARE HIT by a shot from the east — hearts 2/3` | 3.983, same text | east | pass |
| (8,0) | 2.967 `…from the north…` | 3.000, same | north | pass |
| (1,4) | 4.000 `…from the west…` | 4.000, same | west | pass |
| (8,8) | 3.000 `…from the south…` | 3.000, same | south | pass |
| (15,0) | 4.333 `…from the north-east…` | 4.350, same | north-east (ratio 0.57) | pass |
| (15,7) | 4.200 `…from the south-east…` | 4.200, same | formula | pass |

- For (15,7) the cue is (-0.92,-0.39). The reversed vector is (0.92,0.39), ratio 0.42 > 0.4142, so the formula gives south-east, and the trace shows south-east.
- Every line begins `YOU ARE HIT by a shot from the `. W1: **pass at 30 and 60 FPS.**
- Spec ambiguity: the (15,7) bullet is self-contradictory. It labels the case `from the east` and then says the diagonal is expected. I judged against the formula, as the bullet itself tells QA to do (see Open questions).

### W2 Real rooms
- Room 4, 60 FPS: one shot hit, at 5.550, `from the south-east`.
  - It came from the spitter at (15,8), which has cue direction (-0.87,-0.50). Reversed, that is south-east, so it is consistent.
  - The shot was fired at 3.0 s. Arrival is 3.0 + 2.55 = 5.55 s (derived).
- Room 5, 60 FPS: three shot hits. Matching each hit to the spitter by fire time (derived) gives:
  - 4.350 `north-east`, from the (15,0) spitter fired at 1.8 s, cue (-0.87,+0.50).
  - 5.550 `south-east`, from the (15,8) spitter fired at 3.0 s.
  - 6.750 `north-east`, from the (15,0) spitter fired at 4.2 s.
  - All three are consistent with the reversed cue direction.
- **Pass at 60 FPS in rooms 4 and 5.**
- At 30 FPS the room 4 run ended with 0 shot hits (the player was downed by runners at 5.8 s). Room 5 was not run at 30 FPS. **W2 at 30 FPS is not shown.**

### W3 Prefix kept
- Suite is green. Bots parse `shot` hits.
- `text "rears back"` rule at 60 FPS, grub at (10,4): the rule fired (player stepped up at about 0.5 s) and there was no damage. This shows `rears back` still matches.
- `text "by a shot"` rule: the hit line was shown at 3.983, but the player did not move up afterwards (`P` stayed on row y=4 to 5.5 s). The action fell inside the 0.3 s hit-stun, or the rule did not fire. The run cannot tell which, so it does not show the match.
- `text "YOU ARE HIT by"` and `text "takes aim"` were not run.
- **W3 is partly shown, not passed.** There is no before/after comparison either.

### W4 Absorbed shots
- Dash case at 30 and 60 FPS: dash right at 3.8 s into the shot (first shot fired at 1.8 s, arriving about 4.0 s).
  - No hit message, hearts stayed 3/3 at the end (4.17 s and 4.15 s), and no `*` remains on the frame at 4.00 s.
  - **Pass for the dash case at both rates.** The run ended 0.1–0.15 s after contact, so "no damage afterwards" is not shown.
- Hurt-window case: not run. **W4 is partly shown.**

### W5 Late swipe

| Case | Rate | Swipe | Late-swipe line | Hit |
|---|---|---|---|---|
| Grub at (10,4) | 30 | 0.6 | `0.600 the grub's lunge had already started, the swipe was too late to stop it`, before `0.600 you swipe: grub hit` | 0.733 `YOU ARE HIT by a grub` |
| Grub at (10,4) | 60 | 0.6 | same | 0.700 |
| Brute at (10,4) | 60 | 0.8 | `the brute's lunge…`, 0.800 | 0.900 |
| Brute at (10,4) | 30 | 0.8 | same | 0.933 |

- In all four, the late-swipe line comes before the hit line and the swipe result shows "hit", not "killed". The lunge completed and the hit landed.
- The remaining grub HP is not visible in the player view (it was not checked in a trace view).
- **W5: pass at 30 and 60 FPS** for line, wording and ordering. "Loses 1 HP" rests on the `hit` message only.

### W6 No line elsewhere
- Grub wind-up swipe (swipe at 0.3, player at 8.8) at 30 and 60 FPS: `you swipe: grub hit`, no late line, and the cue is cancelled. The grub rears back again later. Pass.
- Brute wind-up swipe, 60 FPS only: `the brute shrugs off the swipe`, no late line. Pass at 60.
- Grub recovery swipe (at 1.3 s), 60 FPS only: `you swipe: grub hit`, no late line. Pass at 60.
- Not run: approach, stagger, kill in the lunge, and brute wind-up and recovery at 30 FPS. **W6 is partly shown.**

### W7 No behavior change
- No trace view was run and there is no baseline, so a comparison with the previous build cannot be made.
- Observed values match the spec's numbers, but this is not a comparison with the previous build:
  - first shots at 1.8 s and 3.0 s in rooms 4 and 5;
  - 2.4 s fire interval;
  - cue at 0.6 s before the shot;
  - grub wind-up 0.5 s and brute 0.7 s;
  - shot arrival about 2.2 s after the shot at 7 tiles.
- **W7 is not shown.**

### W8 Frame-rate independence
- Same wording at both rates for W1 and W5, and for the W6 grub wind-up case.
- Not shown for W2, W6 (several items) and W3, because those were not run at both rates. **W8 is partly shown.**

### Defect: `repo/manual.md` (as given in this packet) contains stray text
- In the "Warnings" section, the bullet that starts `Being hit shows … by a shot from the <direction> (…)` is followed by the line `>>>REPLACE_PLACEHOLDER A swipe that interrupts the warning of a`. The next line continues `grub or runner staggers it for 0.4 s; …`.
- A leftover edit marker is in the player-facing text, and the hit-message bullet and the stagger sentence are merged. The intended manual wording from step 94 is otherwise present, including the late-swipe sentence and the hit wording.
- I saw only the packet's copy and did not open the repo file. Severity: low to medium (player-facing documentation, no gameplay effect). Fix: remove the marker and restore a separate bullet "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted."
- This is not a W1–W8 gameplay failure. The manual text was part of the Build task in `combat-step94.md`, so it blocks a pass.

### Known gaps from handoff 97
- R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe in room 3 were not tried and stay known gaps.
- The 30 FPS grub cancel was seen in the practice room only (W6 above), not in room 3. The 30 FPS recovery swipe was not seen.

## Decisions already made

- D-005: blocked contact consumes the shot and spends the lunge's hit. Only the dash case was observed, with no message and no damage.
- D-011: variant names in messages. Confirmed in all W5 lines and the cue lines.
- D-013: wording-only round, then Close, with a pre-commitment. This report does not meet the "pass" condition for that, so nothing here supports goal-met yet.

## Constraints

- No production code was changed.
- No QA rounds are left.
- Findings are limited to what is shown above. Derived figures (arrival times, matching a hit to a spitter by fire time) are marked as derived.

## Open questions

1. To `game-designer`: the W1 bullet for the spitter at (15,7) says `from the east` and then says the diagonal is expected. The formula and the build give `south-east`. Please correct the criterion text. I judged by the formula.
2. To the Studio: the manual stray marker, if confirmed in the repo, needs a Build fix. Do you want a re-verify of the manual line only?
3. To the Studio: are the unshown items (W2 at 30 FPS, W3 other substrings, W4 hurt window and post-dash, W6 approach, stagger, kill and 30 FPS cases, W7 trace comparison, bots at 30 FPS) accepted as known gaps like those in D-013 item 5, or do they need another QA round?

## Expected output

The Studio reads this report. If the manual defect is confirmed, it routes to Build for a manual-only fix. Otherwise it decides on Review pass 4 and the gap acceptance in Open questions 2 and 3. A criterion that fails goes back to Build with this report.

## Load

- Role: Studio routing (Review or Build, chosen by the Studio)
- Skills: studio/skills/verify-change.md
- Project: design/combat-step94.md, design/combat.md, repo/manual.md, the build in `repo/`
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/97-studio-to-qa.md
