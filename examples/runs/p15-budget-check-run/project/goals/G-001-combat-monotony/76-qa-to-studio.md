---
kind: handoff
goal: G-001
seq: 76
from: qa
to: studio
stage: Verify
outcome: fail
---
# 76: qa → studio — Verification of the current build (D-011 messages and manual, D-012 room 3) at 30 and 60 FPS: FAIL on one red test; no build-behavior defect found; three checks not run

## Task

Report the verification of `repo/` (build 0.6 with D-011 and D-012) against `design/combat-step68.md` (V-a to V-e), `design/combat-step72.md` (R3-1 to R3-10) and the regression list, at 30 and 60 FPS.

## Context

Goal G-001 (combat monotony). Handoff 75 asked for a verdict per criterion for the D-011 message and manual changes and the D-012 room 3 layout change. The last verified state was 0.6.1 (QA 50 and 64). I used three run rounds: the whole test suite and the bots at both rates; player-view traces of the practice room (one per variant, both rates); and room 3 traces (still player, a no-grub replica, a last-spitter replica, a reactive dasher), both rates. No 0.6.1 output was in the packet, so nothing is compared with the earlier build byte for byte.

## Findings

### 1. `run_tests` (whole suite): FAIL, 1 of 64

```
FAIL: test_wind_up_and_hit_messages_name_the_variant (test_game.VariantMessageTest)
AssertionError: 3 != 1 : (30, 'grub')     (assertion on out.count("a grub rears back"), test_game.py line 763)
```

- 63 tests pass. This includes the room 3 contents test, the room 3 clear test (spitters and grub all needed), the manual-wording test, the `text "rears back"` test for all three variants, and the cue, cap, blocked-contact and brute tests.
- Classification: a defect in the test, not in the build. The test runs 3 s with a still player and asserts the wind-up message appears once. A still player is hit, the grub recovers, walks up and rears back again. My direct trace shows this: the runner rears back at 0.033 s and again at 1.167 s at 30 FPS. Derived for the grub at 30 FPS: wind-ups at about 0.03, 1.5 and 2.8 s, which gives the 3 the test counted. The derivation is not separately traced.
- The assertion stops at the first failure, so the runner and brute cases and the 60 FPS cases of this test never ran. I covered them by direct traces (section 3).
- Severity: low, since the build is not affected. The suite is red, so I cannot pass.

### 2. `run_bots` (rooms 1–5, limit 60 s, 3 hearts each)

| Bot / room | 30 FPS | 60 FPS |
|---|---|---|
| walker 1 | not cleared, lost 3 | not cleared, lost 3 |
| walker 2 | cleared 8.4 s, lost 2 | cleared 8.4 s, lost 2 |
| walker 3 (new layout) | cleared 8.9 s, lost 1 (grub 1), 8 attacks | cleared 9.2 s, lost 1 (grub 1), 8 attacks |
| walker 4 | cleared 9.9 s, lost 1 | not cleared, lost 3 |
| walker 5 | not cleared, lost 3 | cleared 12.9 s, lost 2 |
| dodger 1 / 2 / 3 / 4 / 5 | all cleared, 0 lost; 6.6 / 20.7 / 15.6 / 18.3 / 24.2 s; dashes 3 / 10 / 6 / 7 / 11 | all cleared, 0 lost; 9.6 / 25.1 / 15.0 / 17.0 / 28.8 s; dashes 5 / 14 / 6 / 8 / 14 |
| camper (clears) | 1/5 (room 2 only) | 0/5 |
| camper room 3 | not cleared (6.3 s), lost 3, 0 attacks | same |

Criteria against the numbers:
- **13** (rooms 3–5 summed):
  - 30 FPS: walker lost 1+1+3 = 5 (limit 3–6) and cleared 2 (limit ≥2). Dodger lost 0 (limit ≤2.5) and cleared 3/3. Camper cleared 0 of 3 rooms, fewer than the walker's 2. **Pass.**
  - 60 FPS: walker lost 1+3+2 = 6, exactly the upper limit and not above it, and cleared 2 (rooms 3 and 5). Dodger lost 0 and cleared 3/3. Camper cleared 0. **Pass, with the walker at both limits.**
  - The in-repo test comment records 7 hearts for the 60 FPS walker earlier on 0.6. It is 6 now, so the room 3 change did not push it over. The walker's loss in room 3 is 1 heart, all from the grub, at both rates.
- **14** (rooms 1–2): walker lost 5 at both rates (limit ≥1). Dodger lost 0 and cleared 2/2 (limit ≤1). **Pass.**
- **15**: dodger dashes in rooms 3 / 4 / 5 are 6 / 7 / 11 at 30 FPS and 6 / 8 / 14 at 60 FPS, all ≥1. **Pass.**
- **16c**: the dodger clears the same rooms at both rates, with hearts lost per room identical (0). **Pass.** The walker's per-room differences are allowed by 16d.
- Observation, with no limit in any design document: dodger clear times differ between rates, for example room 1 at 6.6 s vs 9.6 s and room 5 at 24.2 s vs 28.8 s. The documents define no clear-time limit, so no comparison is possible.
- Nothing is outside a limit, so no tuning question arises from the bots.

### 3. D-011 criteria (`design/combat-step68.md`)

Evidence: practice room, one enemy at (9.5, 4), player at the start, 1.2 s, both rates.

| Variant | Wind-up message, 30 / 60 FPS | Hit message and time, 30 / 60 FPS |
|---|---|---|
| grub | `a grub rears back` 0.033 / 0.017 s | `YOU ARE HIT by a grub — hearts 2/3` 0.667 / 0.633 s |
| runner | `a runner rears back` 0.033 / 0.017 s | `YOU ARE HIT by a runner — hearts 2/3` 0.533 / 0.483 s |
| brute | `a brute rears back` 0.033 / 0.017 s | `YOU ARE HIT by a brute — hearts 2/3` 0.867 / 0.833 s |

- The `cue:` line at the first picture reads 0.50 / 0.35 / 0.70 s to the lunge, and the wind-up lengths match the parameter table.
- **V-a: pass.** One message per wind-up, on the first frame in range. It is printed again only when the enemy winds up a second time. A comparison against 0.6.1 timing was not possible (no baseline).
- **V-b: pass.** The hit message names the matching variant at the contact frame. The hearts suffix is unchanged. The shot message is unchanged (`by a shot — hearts 2/3`, seen in the room 3 traces and covered by the test).
- **V-c: NOT VERIFIED.** "Byte-identical to 0.6.1" needs a 0.6.1 baseline, and the packet has none. This is a verification gap, not a failure. The `cue:` line, `~` line, swipe and shrug messages looked as specified.
- **V-d: pass.** `test_rears_back_rule_matches_all_variants` passes. In room 3 live, `when text "rears back" then dash aside` fired on `a grub rears back` (dash at 5.667 s at 30 FPS, 5.650 s at 60 FPS).
- **V-e: partial.** The 63 passing tests cover criteria 1–11 and 17–21 in the practice room at both rates. "No bot result changes" cannot be compared, because room 3 changed in the same build and there is no 0.6.1 bot output.
- **Manual text: pass.** `repo/manual.md` carries the exact replacement text for the late-swipe bullet (including "A brute is never cancelled.") and for the spitter paragraph ("so in room 3 up to 5 can be in the air at once."). It also lists all three wind-up messages and all four hit messages. The test for it passes.

### 4. D-012 criteria (`design/combat-step72.md`)

- **R3-1 contents: pass.** `game.py` ROOMS["3"] is spitters (2,1), (10,6), (2,7) and grub (15,0), and the contents test passes. The picture at 0.00 s shows the same. Rooms 1, 2, 4, 5 match the `combat.md` table (room 1 grubs (3,4), (15,4), (8,0); room 2 runners (2,1), (1,8), brute (15,7), grub (14,0); room 4 runner (1,4), grub (0,1), spitters (15,0), (15,8); room 5 grubs (1,1), (0,6), brute (4,8), spitters (15,0), (15,8)).
- **R3-2 schedule: pass.**
  - Still player: aims at 1.200, 2.000, 2.800 s and spits at 1.800, 2.600, 3.400 s at both rates (cue 0.600 s before each shot).
  - The cue and spit times of the still-player room 3 trace and the no-grub replica (three spitters, player at (8,4)) are the same up to the end of the trace. Spits fall at 1.8, 2.6, 3.4, 4.2, 5.0, 6.2 s and aims at 1.2, 2.0, 2.8, 3.6, 4.4, 5.6, 6.0 s, identical at both rates. The 6.0 s aim of the second spitter and the hits at 3.4, 5.5 and 6.3 s match too.
- **R3-3 grub after the lessons: pass.** For a still player at (8,4), the grub's first `a grub rears back` is at **6.100 s at 30 FPS and 6.083 s at 60 FPS**, against the 4.0 s minimum. The grub was at (9.7, 3.0), about 1.97 tiles from the player. No retune is needed under D-012 item 4.
- **R3-4 grub criteria in room 3: pass on the evidence I have, with a gap.**
  - Observed in room 3 live with the reactive player:
    - The cue read 0.50 s to the lunge at its first picture.
    - A swipe during the wind-up cancelled it. At 30 FPS the swipe at 7.533 s was followed by a new wind-up at 7.967 s, and no lunge came between them.
    - Two swipes killed the grub: 7.533 and 10.433 s at 30 FPS; 7.117 and 7.483 s at 60 FPS.
    - A dash on the cue (`dash aside` at 5.667 s) was followed by no grub hit.
  - The room 3 trace never showed a 1-tile sidestep, a dash late in the lunge, or a recovery swipe. Those are covered only by the practice-room tests (GrubTest) at both rates, which use the same code path. I did not run them as separate room 3 scripts.
- **R3-5 spitter criteria with the grub alive: pass.** In the still-player trace, every cue is 0.6 s before its shot. The dodge and contact-edge tests pass. In the reactive 60 FPS run the player took no damage in 20 s. The 30 FPS reactive run took one shot hit at 8.7 s. That is the scripted player's reaction timing and not a build question: its rules act every 0.15 s, and I did not trace the divergence between the rates further.
- **R3-6 D-007 bound: pass.**
  - Cue start times with and without the grub are equal up to the player's death at 6.3 s, as in R3-2. The grub's first lunge would have come at about 6.6 s.
  - In the reactive traces all three spitters start cues together after a cap delay: 6.000 s (spits at 6.600 s) at both rates, then again around 8.8–9.4 s at 30 FPS, 10.0–10.6 s at 60 FPS, and later. This is the accepted D-007 behavior and not a defect.
  - Derived in-flight counts by the step 46 method (visible `*` plus spits in the last 0.3 s):
    - 30 FPS: 4 at 7.00 s; 2 visible + 3 spits = 5 at 13.50 s.
    - 60 FPS: 5 visible at 11.00 s; 2 visible + 3 spits = 5 at 14.00 s.
    - The maximum is 5, never above 5.
  - The script is my own (it has the grub and extra rules), not the QA 43 script of criterion 11d. The method is the same.
- **R3-7 room end: pass.** The room clear test (spitters alone or grub alone does not clear; all four does) passes. In the 60 FPS reactive run the grub was killed at 7.483 s while three spitters were alive, and the session ended at 20 s with "enemies left 3" and no `room cleared`.
- **R3-8 last spitter close: PARTIAL.**
  - Geometry: pair distances are (2,1)–(10,6) = 9.43, (10,6)–(2,7) = 8.06 and (2,1)–(2,7) = 6.00 tiles, so the maximum is 9.43, within 9.5. **Pass.**
  - The "within 6 s of the previous kill" run, with a scripted kill of the grub and two spitters followed by a walk to the last spitter, was **not run**. The derived value is about 3 s (9.43 tiles at 4 tiles/s is about 2.4 s, plus two swipes). My single-spitter replica (a walk of about 7 tiles and two swipes) shows only that the walk and two swipes take about 1.35 s from the last arrival. That is not the specified measurement.
- **R3-9 messages: pass.** `a grub rears back` appears in room 3 live and `YOU ARE HIT by a grub` in the practice room. The `text "rears back"` rule reacts (see V-d).
- **R3-10 frame-rate independence: pass for what ran.** R3-2 and R3-3 differ by 0.000–0.017 s between rates (at most one 60 FPS frame, within ±1 frame). The tests cover criteria 1–12 and 17–21 at both rates.

### 5. Regression checks

- Rooms 1, 2, 4, 5: contents unchanged (R3-1). The bots clear them as in section 2, and the dodger loses 0 hearts in all of them at both rates.
- Criteria 1–11, 17–21: covered by the passing tests at 30 and 60 FPS. Criterion 11 (cap) in room 3 is covered in R3-6.
- Criteria 13–16: section 2.
- Room 3 in-flight bound: R3-6.
- Not re-run as separate traces: the criteria 17 and 20 edge cases and the room 4 and 5 gap traces. They rely on the unit tests, which pass.

### 6. Defects, conflicts, undefined behavior

1. **Defect (test, severity low, Build):** `test_wind_up_and_hit_messages_name_the_variant` expects one wind-up message in 3 s from a still player, but a variant re-winds up after recovering. The suite is red because of it. Expected source: V-a says "each wind-up prints its message once". It does not say "once in 3 s". Acceptance for the fix is a green suite that still checks, for every variant at both rates, one message per wind-up and a matching hit message.
2. **Document conflicts** (`design/combat-step72.md` governs, as the handoff says):
   - `combat.md` still has the old room 3 row (spitter at (14,7), no grub), the old room 3 purpose, criterion 12 and criterion 11 ("rooms 1–5 never more than 3").
   - `combat.md` still says the wind-up message is "a grub rears back (all variants)". `combat-step68.md` governs and the build follows it.
   - `combat-cues-visual-spec.md` says spitter cues are "normally 0.8 s apart". That is true only in room 3 and is already noted for the art director.
   - `decisions/D-007` ends with a stray `</parameter>` line, which looks like a formatting leftover.
3. **Not verified (gaps, not failures):**
   - V-c, byte-identical output to 0.6.1: no baseline in the packet.
   - V-e, "no bot result changes": no 0.6.1 bot output, and room 3 changed in the same build.
   - R3-8, the timed run to the last spitter.
   - R3-4, a direct room 3 sidestep, late dash and recovery swipe.
4. **Observations, no defect:**
   - A still player in room 3 dies at 6.3 s to three spitter shots (hits at 3.4, 5.5, 6.3 s), before the grub's first lunge. The grub only matters to a player who survives the first 6 s.
   - The D-007 simultaneous cue start now occurs at 6.0 s in the reactive run (6.8 s in QA 43). This is the same accepted cap-delay case, and the count never exceeded 5.
   - No undefined expected behavior was found, so nothing goes to Design.

## Decisions already made

- D-012 (room 3 layout), D-011 (variant messages), D-007 (room 3 bound and simultaneous cues), D-005 (blocked contact), D-001 (one-button combat). I applied them as written and changed none.

## Constraints

- Both 30 and 60 FPS were checked wherever a run was made.
- I verified from the specs, criteria and build, not from the implementer's explanations. I did not modify production code or tests.
- Bot numbers are reported without proposed values. None is outside a limit.

## Open questions

1. Can the Studio supply a 0.6.1 baseline (play output for the V-c scripts and bot output) so V-c and the "no bot result changes" part of V-e can be judged? Otherwise Studio decides whether to accept them as unverified.
2. Should the 60 FPS walker sitting at both limits (6 hearts lost, 2 rooms cleared) be watched? Any further layout change risks it. It is not a defect now.

## Expected output

**Verdict: fail** for this verification round. The reason is the red suite (a test defect), not any observed build behavior. Routing:
- Defect 1 goes to `gameplay-engineer` (Build): fix the test, which is test tooling.
- The re-verify should then close the gaps: a timed R3-8 run in room 3, direct room 3 sidestep, late-dash and recovery-swipe scripts for R3-4, and V-c / V-e if a baseline exists.
- No spec gap goes to `game-designer`, and no criterion has failed twice.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step72.md, design/combat-step68.md, design/combat.md, design/combat-step-46-room3-cap.md, design/combat-cues-visual-spec.md, repo/manual.md, repo/README.md, repo/game.py, repo/bots.py, repo/tests/test_game.py, project.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/75-studio-to-qa.md
