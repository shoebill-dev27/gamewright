---
kind: handoff
goal: G-001
seq: 50
from: qa
to: studio
stage: Route
outcome: pass
---
# 50: qa → studio — Re-verify of build 0.6 (repo/) at 30 and 60 FPS: PASS on everything exercised, with a short list of items not fully run

## Task

Route the result. No criterion failed in this round. No failure repeats a failure from 43, so nothing goes to the Technical Director. Decide whether the "not fully run" items below need a follow-up QA step or can be left to the hand-timed playtest. There is one non-blocking wording question for `game-designer` (criterion 11d, see Open questions).

## Context

Re-verification of build 0.6 against `design/combat.md`, `design/combat-step-44-walker-limit.md` (D-006) and `design/combat-step-46-room3-cap.md` (D-007). The evidence comes from executed runs only: unit tests, player-view and trace scripts at 30 and 60 FPS, and the bots. Times are game seconds. Visual criteria V1–V11 are out of scope. All run rounds are used (0 left), so anything not covered below could not be run.

Failures in 43: criterion 13 at 60 FPS (F1), the brute shrug message missing from the player view (F2, criterion 19a), the wrong version banner (F3), and criterion 16b as a consequence of F1. All four now pass (see below).

## Findings

### Verdict

**PASS** for every criterion exercised in this round, at both 30 and 60 FPS. Several items could only be partly covered, and they are listed explicitly under "Not run or only partly run". A reader must not take this as "every sub-item of every criterion was independently re-run".

### Unit tests

`python3 -m unittest discover -s tests`: 59 tests, OK (43 had 54, so 5 are new). They passed and I used them only as a regression signal.

### Re-check of the 43 failures

| 43 finding | Result | Evidence |
|---|---|---|
| F2: brute shrug message (19a) | **pass** at 30 and 60 | Script: `room empty`, `spawn brute 9 4`, `player 8 4`, swipes at 0.1 and 0.5. Each wind-up swipe prints `the brute shrugs off the swipe` at the swipe time (0.100 and 0.500), before `you swipe: brute hit`. The cue stays (0.23 s / 0.22 s to the lunge at 0.5). The lunge hit comes at 0.800 (30) / 0.783 (60), 1 heart lost. No message on a recovery swipe (1.3 s: `you swipe: brute hit` only). No message when a swipe kills in wind-up (swipe at 2.3 gives `brute defeated`, room cleared, no lunge). A swipe at a standard grub or runner is unchanged (`you swipe: grub hit`, `grub defeated`, `runner defeated`; no shrug). A swipe during hit-stun prints `(nothing happens)`. |
| F3: banner build number | **pass** | Every player-view output starts `Lantern Depths 0.6 — …`. |
| F1 / 16b: criterion 13 at 60 FPS | **pass** under D-006 | See criterion 13 below. |

### Per criterion

| # | 30 FPS | 60 FPS | Evidence |
|---|---|---|---|
| 1 Telegraph | pass | pass | Cue 0.033 → lunge 0.533 (30); cue 0.017 → lunge 0.517 (60). The cue line says 0.50 s to the lunge. Also seen in the h21b traces (windup 3.900 → lunge 4.400 at 30; 3.883 → 4.383 at 60). |
| 2 Sidestep | pass | pass | Grub at (9,4), player at (8,4); `0.1 move down`, `0.35 stop` (1 tile). Hearts stay 3/3 through the whole lunge and the recovery (s2). |
| 3 Dash | pass (standard, brute, runner as stated) | pass | Standard grub and brute: see 43 (c21), and 21a below. Runner: dash right at 0.3 and at 0.4 (lunge starts 0.383), hearts stay 3/3. The control without a dash is hit at 0.467 (30) / 0.433 (60). Limit: both runner scripts dash away from the lunge direction, so the no-damage result is partly displacement. A dash into the runner's lunge line was not run. |
| 4 Standing still | pass | pass | Control runner hit at 0.467 / 0.433; brute hits at 0.800 / 0.783 and 2.767 / 2.717 (f2). |
| 5 Safe window | pass | pass | Standard grub (c5std): sidestep the lunge (y=5), then walk to (6.8, 4.4) at 1.0–1.5, about 0.45 tile from the recovering grub, with no hurt window active. Hearts 3/3 at 1.6. Brute: see 43. |
| 6 Cancel | pass | pass | Standard grub, swipes at 0.1 and 0.6 (c6): the first swipe in wind-up stops the lunge (hearts 3/3 at 0.5, the grub rears again at 0.533 / 0.517, which is the 0.4 s stagger). The second swipe kills it in wind-up: `grub defeated`, `room cleared`, no lunge, no stagger. Runner: one swipe kills it in wind-up, no lunge (rswipe). The runner's non-lethal cancel cannot be observed (HP 1, any damaging swipe kills it). |
| 7 One at a time | pass (read) | pass (read) | Room 4 and 5 traces and bot logs: no two grubs in wind-up or lunge together. No dedicated three-grub script this round (carried from 43). |
| 8 Variants | pass | pass | Runner dies to one swipe (rswipe, at 0.100 at both rates). Brute needs exactly 4 (swipes at 0.1, 0.5, 1.3, 2.3 → `brute defeated`). Marks `r` and `G` appear in the views; the manual lists them. |
| 9 Cue timing | pass | pass | Room 3 cues 1.2/2.0/2.8 → shots 1.8/2.6/3.4; simultaneous cues 6.8 → 7.4 and 11.0 → 11.6, each 0.6 s. The d10 shot flew along the locked line (y=4) while the player had moved to y≈5. Each simultaneous cue has its own distinct aim line. |
| 10 Dodge | pass | pass | d10: spitter (15,4), player (8,4), `1.3 move down`, `1.55 stop` (1 tile). The first shot (1.8) passes on row 4, hearts 3/3 through 5.0 at both rates. |
| 11 Stagger and cap (amended) | pass | pass | See the criterion 11 section below. |
| 12 Rooms | pass | pass | Room 1: grubs at (3,4), (15,4), (8,0). Room 2: runners (2,1), (1,8), brute (15,7), standard (14,0). Room 3 spitters at (2,1), (14,7), (2,7). Rooms 4 and 5 as in 43 and as in the traces (room 4 runner (1,4), grub (0,1), spitters (15,0), (15,8)). |
| 13 Spitter rooms (D-006) | pass | pass | See below. |
| 14 Grub rooms | pass | pass | See below. |
| 15 Dash used | pass | pass | See below. |
| 16 Frame-rate independence | pass (16a–d); 16e partly confirmed | | See below. |
| 17 Contact edge | a, b, c pass; d partly | a, b, c pass; d partly | See below. |
| 18 Cue gap rooms 4–5 | pass (a, b, c); d not run | pass (a, b, c); d not run | See below. |
| 19 Brute | a, b, c, e, f pass; d carried from 43 | same | See F2 above. d: carried from 43, not re-run. |
| 20 Consumed shot | a, b, f pass; c, d carried; e partly | a, b, f pass; c, d carried; e partly | See below. |
| 21 Spent lunge | a, b, c, d pass | a, b, c, d pass | See below. |

**Criterion 11 (amended, step 46).**
- a: Room 3 first shots at 1.8, 2.6 and 3.4 at both rates (n11a). Room 4 first shots at 1.8 and 3.0 at both rates (t18c). Room 5: carried from 43.
- b: In the real room 3 with the reaction script, the second cues (due 3.6, 4.4, 5.2) are delayed by the cap to 6.8, and all three start together. This is the same at 30 and 60 FPS and is accepted by D-007. At 6.5 s three shots are in the air and one leaves the room before 6.8, so each check sees 2, which is fewer than 3.
- c: Rooms 4 and 5: every bot log line I read (0–9 s per run, both rates) lists at most 3 shots in flight. Cue windows never overlap (criterion 18a), so 3 is the derived maximum. Room 3: at most 5 (derived, below), which is the accepted bound.
- d (count of `*` at 7.5 and 11.7): **the literal count is not readable from the player view.** See Open questions.
  - 7.5 s, both rates: 2 visible `*` (two older shots far from the spitters). The 3 shots fired at 7.4 are 0.3 tile from their spitters and share the spitter's cell, which is drawn as `s`. The three `a spitter spits` events at 7.400 give a derived total of 2 + 3 = **5**, which is at the accepted bound, not above.
  - 11.7 s: the player view prints no picture at 11.7. The 11.5 picture has 0 `*` marks, and the three spits come at 11.600, so the count at 11.7 is a derived **3**. The 12.0 picture shows 3 marks at both rates.
  - Nothing above 5 and nothing above 3 in rooms 4–5 was seen.
- e: Cue timing 0.6 s per cue holds for the simultaneous cues (6.8 → 7.4 and 11.0 → 11.6), each along its own locked line.

**Criterion 13 (D-006: walker 3–7 hearts and at least 2 rooms cleared in rooms 3–5; dodger at most half of the walker's total and 3/3; camper clears fewer than the walker).**

| | 30 FPS | 60 FPS |
|---|---|---|
| walker room 3 / 4 / 5 | 0 lost cleared / 1 lost cleared / 3 lost not cleared | 2 lost cleared / 3 lost not cleared / 2 lost cleared |
| walker total | 4 lost, 2 of 3 cleared | **7 lost**, 2 of 3 cleared |
| dodger | 0 lost, 3 of 3 | 0 lost, 3 of 3 |
| camper | 0 of 3 cleared | 0 of 3 cleared |

Pass at both rates. The 60 FPS walker figure of 7 is the upper limit; the 30 FPS total of 4 is one above the lower limit of 3. This matches the engineer's figures in the step 44 note. Per the reporting rule, no number is outside 13a–13d, so nothing is reported to `game-designer`.

**Criterion 14.** Walker in rooms 1–2: 5 lost at both rates (room 1: 3 lost, not cleared; room 2: 2 lost, cleared). Dodger: 0 lost and both rooms cleared at both rates. Pass.

**Criterion 15.** Dodger dashes in rooms 3, 4, 5: 30 FPS 8, 7, 11; 60 FPS 10, 8, 14. Pass.

**Criterion 16.**
- 16b: 13, 14 and 15 hold at each rate.
- 16c: the dodger has the same cleared set (5/5) and 0 hearts lost at both rates.
- 16d: the walker differs between rates, as allowed.
- 16e: partly confirmed. I read the logs (`log on`) for the walker in room 3 from 0 s to about 9.5 s at both rates, and about 9 s of rooms 4 and 5. The walker's decisions run on the 0.15 s grid. A decision happens on the first frame at or after the grid time, so at 30 FPS it lands up to one frame later than at 60 FPS (for example grid 0.150: frame time 0.1667 at 30, 0.150 at 60; the walker is at x 7.333 vs 7.400). Positions therefore differ from the first second, and with them the cue-start aim lines and the shot geometry in room 3. Each heart lost that I read has a different position or decision timing behind it, such as the room 3 hits at 2.25 and 6.97 at 60 FPS, and the room 4 shot hit at 7.90 at 60 FPS. I found no case where the same decision at the same game time (±1 frame) from the same positions had a different outcome, and no rule-caused difference. The logs are cut at 20000 characters, so the later parts of rooms 4 and 5 (past about 9 s) were not read. See "Not run or only partly run".

**Criterion 17 (contact edge), scripts like those of handoff 20 (spitter at (15,4), player at (8,4) with a sidestep of known length).**
- a (shot, lateral miss 0.39 or less): miss about 0.27 (30) / 0.20 (60): hit at both, at 4.033 / 4.017 (t17a2).
- b (more than 0.40): miss about 0.67 (30) / 0.60 (60): no hit at either rate, hearts 3 through 4.6 (t17c). Note: at 0.33–0.40 (t17a, t17b) the rates disagree only at about 0.40, inside the band: 30 FPS with y=4.40 gives no hit, 60 FPS with y=4.40 hits at 4.117, and 60 FPS with y=4.33 hits at 4.050. This is in the accepted band, and the only difference is the hit itself.
- c (lunge): lateral miss 0.533 gives a hit at both rates (0.633 / 0.617); lateral miss 0.667 gives no hit at both rates (l17hit, l17miss). One case on each side of the band.
- d: for shots, the rates differ at the 0.40 reach, which is accepted (see b). I did not scan the lunge band width, so I cannot say the lunge band is within 0.03 tile. I saw no evidence that it is wider.

**Criterion 18 (cue gap in rooms 4–5, 15 s traces at both rates).**
- a, b: Still player: cues 1.2, 2.4, 3.6, 4.8 and shots 1.8, 3.0, 4.2, 5.4: the gap from a shot to the next cue is exactly 0.6 s, and cue windows never overlap. The dash script t18c in room 4 (cap delay) gives A cue 1.2 / B cue 2.4 / A cue 3.6 / B cue 5.0 (the cap delayed it by 0.2 s) / A cue 6.2 / B cue 7.4. Gaps are 0.6 s or longer at both rates.
- c with one spitter killed (k18c, room 4): spitter A killed at 2.033 (30) / 2.017 (60). The remaining spitter B cues at 2.4 (gap 0.6 from A's shot at 1.8), then at 4.8 and 7.2 (shots every 2.4 s). Gap rule respected at both rates. A spitter killed during its own cue (the cancelled-cue case) was not run.
- d: not run. The Build step provides no forced simultaneous-first-shot test, and the practice room does not use the rule.
- e: criterion 9 and the cap hold in rooms 4–5 in these traces.

**Criterion 20 (consumed shot).**
- a: Hurt window (h21b scripts): a shot hurts the player at 3.833 and the window ends at 4.633. There is no damage at the window end, hearts stay 2 until the end of the run at both rates.
- b: Dash (e20): dash right at 3.9 into the first shot. The `*` is gone by the 4.0 picture, and hearts are 3/3 at 4.07 / 4.05. The dash ends on the old line. Not repeated this round for a second shot after the dash.
- c: Normal hit unchanged: a shot reaching the unprotected player hits on arrival (b21a/b21c: `YOU ARE HIT by a shot` at 3.833). The "shot arriving at least a frame after the window ends hits" half is carried from 43.
- d (room 4 still-player 15 s): carried from 43. Not re-run.
- e (cap slots): partly. The `*` disappears at the dash contact (e20 at 4.0), but the player view prints every 0.5 s and the trace does not list shots, so the frame of the in-flight count drop was not observed.
- f (band): f20b: the player crosses the first shot's line with a lateral miss of about 0.48–0.53 (above 0.40). The shot is not consumed: the `*` is still visible and moving left at 4.0, 4.5 and 5.0. No damage at either rate.

**Criterion 21 (spent lunge).**
- a (dash): carried from 43 (c21std, c21brute). Not re-run.
- b (hurt window ends inside the lunge): h21b with the grub at x 2.59, 2.60 and 2.61, at both rates. The shot hurts at 3.833. The grub lunge starts at 4.4 (30) / 4.383–4.367 (60). Contact begins before the window ends at 4.633, and the grub is still lunging at 4.633 (x 8.32–8.58, player at 8.45, within 0.6). Hearts stay 2 to 5.0: no lunge damage. A lunge whose first contact comes after the window ends hits: b21a hits at 4.667 (30) / 4.633 (60), b21c at 4.800 / 4.750.
- c, d: carried from 43 (recovery 0.8 s; the second lunge hits normally).

### Observations (not failures)

1. The text view draws a shot that is within one cell of a spitter as `s` (shots just fired at 7.4 and 11.6 are not visible as `*` until about 0.2 s later). It does not break a criterion. It does make the room 3 `*` count at 7.5 s unreadable (see criterion 11d). Severity: low, presentation only (`art-director` owns presentation of the shot).
2. The 60 FPS walker total of 7 hearts sits at the D-006 limit, and the 30 FPS total of 4 sits near the lower limit of 3. A later change to rooms 3–5 will move these (D-006 says to re-measure).

### Not run or only partly run

- 3: a dash into the runner's lunge line (the runner scripts dash away from the lunge).
- 7: a dedicated script with three close grubs.
- 17d: the lunge band width scan.
- 18c: a spitter killed while its cue is running. 18d: not run (no forcing test exists).
- 19d, 20c (second half), 20d, 21a, 21c, 21d: carried from 43, not re-run on this build.
- 20e: the frame of the in-flight drop (`*` gone) was not observed; the view and the trace do not list it.
- 16e: the logs are cut at 20000 characters (a tool limit). The parts of rooms 4 and 5 beyond about 9 s were not read. To read them, use shorter bot scripts (for example `limit 6`, or `rooms 4` with a second script for the tail).
- Reason for all of the above: the runs were limited to the rounds available (0 left), and the tool output limit.

## Decisions already made

D-004, D-005, D-006, D-007 stand and were applied as written. D-006 limits were used for criterion 13; D-007 for criterion 11. No criterion or limit was changed by QA.

## Constraints

- Production code was not touched.
- Visual criteria V1–V11 are out of scope (no graphical build).

## Open questions

1. For `game-designer`, non-blocking: criterion 11d says "count the `*` marks at 7.5 s and at 11.7 s, expected 3 to 5". In the text view the literal count at 7.5 s is 2 (the 3 shots fired at 7.4 are drawn as `s`), and no picture is printed at 11.7 s. I judged it from the three spit events plus the visible marks (derived 5 at 7.5, 3 at 11.7; 3 marks seen at 12.0). A count of 2 is outside the stated expected range but the rule only names counts above 5 (or above 3 in rooms 4–5) as defects, so I did not invent a verdict from the literal number. Please say whether the derived counts are acceptable, or give a time at which the marks can be counted (for example 7.7 s or 12.0 s) or a trace field for shots in flight.

## Expected output

Studio decides the next step: either close this verify (no failing criterion), or ask QA for a small follow-up covering the "not run or only partly run" list (needs rounds and shorter bot logs for 16e). The playtest items in D-004 to D-007 remain open for the hand-timed playtest.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/49-studio-to-qa.md
