# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/49-studio-to-qa.md
next_seq: 50
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/50-qa-to-<recipient>.md
- @run/<tests|play|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/49-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 49
from: studio
to: qa
stage: Verify
outcome: routed
---
# 49: studio → qa — Re-verify the current build (repo/) at 30 and 60 FPS

## Task

Independently verify the current build in `repo/` against the acceptance criteria in `design/combat.md` and the amendments in `design/combat-step-44-walker-limit.md` and `design/combat-step-46-room3-cap.md`. Cover every item below, at both 30 and 60 FPS where timing is involved. Report pass/fail per criterion.

## Context

G-001 (combat feels monotonous). Your earlier verification (43) of the previous build failed on F2 (player view omitted the brute's shrug message, criterion 19a) and F3 (the banner showed the wrong build number). Design has since ruled on the other open items: criterion 13 (walker limit in rooms 3–5) is judged against D-006, and criterion 11 is reworded by D-007 and `design/combat-step-46-room3-cap.md`. A new build is ready for you. Judge it only from the spec, the criteria and what you observe by running it.

## Findings

Nothing from the implementer is passed to you. Start by running `python3 -m unittest discover -s tests` and report failures as they are; some tests are new and have not been run before. Then:

1. Re-check F2 and F3 with the scripts and acceptance criteria from your report 43 (criterion 19a, including no message when a swipe kills; and the banner shows the current build version).
2. Cover the items marked "not run" in 43: criteria 2, 6, 10, 17 a–d, 19f; the isolated runner dash in criterion 3; the runner's one-swipe death in criterion 8; the rooms 1–2 contents in criterion 12; criterion 18c with a killed spitter; 20e, 20f, 21b; the 16e decision logs.
3. Criterion 11 a–e as amended in `design/combat-step-46-room3-cap.md`, including the room 3 `*` count of 3–5 at 7.5 s and 11.7 s at both frame rates.
4. Criterion 13 (walker limit, rooms 3–5) against D-006 (3–7 hearts, at least 2 rooms cleared) using `run_bots`.
5. Regression check: rooms 1–5 at 30 and 60 FPS, anything else in the criteria that the above does not touch.

Visual items (V1–V11) need a graphical build and are out of scope here.

## Decisions already made

- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit.
- D-006: criterion 13 walker limit is 3–7 hearts with at least 2 rooms cleared.
- D-007: simultaneous cue starts in room 3 after a cap delay are accepted; criterion 11 is the in-flight bound.
- D-004 and D-001 stand (no new input beyond attack, dash, pause).

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No new input buttons.
- Do not rule on design questions: if a rule is undefined or contradictory, report `question` with the case rather than inventing the expectation.

## Open questions

None.

## Expected output

A verification report with a pass/fail per criterion (and the list of anything still not run, with the reason), reproduction scripts for each failure, and the severity of each. Address the result to `studio`. A fail on the same criterion a second time goes to the Technical Director (loop limit), so state clearly which criteria failed in 43 and fail again here.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/ (run commands in project.md)
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/43-qa-to-studio.md
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.5, specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Until 0.6 exists, build 0.5 behaves as described without the step 35 and step 38 parts.** The player kit is unchanged from 0.4.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: message "a grub rears back" when it starts (all variants, unchanged in step 35).
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their gap stays at the old 0.2 s between consecutive cues in the room.
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. Reopen if a real-room trace in room 3 shows simultaneous starts that a player cannot answer (see D-005).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (14,7), (2,7), with the stagger and cue | 0.8 s / none | Learn the aim cue |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). In rooms 1–5 never more than 3 shots in flight. In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above.
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 with a surviving player past 7 s, to see if simultaneous cue starts occur there (D-005 revisit).

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-step-44-walker-limit.md
# Combat design note: criterion 13 walker limit (step 44, build 0.6)

Status: amends criterion 13 of `design/combat.md`. Where this note and `combat.md` differ on criterion 13, this note governs. No other criterion, rule or parameter changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-006.

## Question

The walker bot on build 0.6 loses 7 hearts in rooms 3–5 at 60 FPS (4 at 30 FPS). Criterion 13 allowed at most 6. All other criterion 13 limits hold.

## Ruling

7 hearts is not a breach of intent. The limit of 6 was too tight, and it was never derived. Step 22 recorded 6 as "exactly the upper limit" of the 0.5 observation, so it was a snapshot of one bot result.

The purpose of criterion 13 is a gradient: ignoring the aim cue is costly but not hopeless. The 0.6 evidence shows both halves:

- **Costly.** The walker loses 4 (30 FPS) and 7 (60 FPS) hearts. The dodger loses 0 and clears 3/3, and uses 7 or more dashes per room. The camper clears 0 of 3. The gap between ignoring and reading the cue is larger than in 0.5.
- **Not hopeless.** The walker still clears 2 of 3 rooms at both rates. It is not walled out.

Why the hearts ceiling was the wrong tool:

- Each room has 3 hearts. A room the walker clears must have been survived, so it costs at most 2 hearts.
- A walker that clears 2 of 3 rooms therefore loses at most 3 + 2 + 2 = 7 hearts in rooms 3–5. The clear count is what carries "not hopeless". A hearts ceiling below 7 only forbids particular distributions of the same outcome. For example, 3+2+2 at 60 FPS is forbidden, while 3+2+1 is allowed. That says nothing about the gradient.
- The walker decides on a 0.15 s grid. The engineer saw per-room totals move in opposite directions between 0.5 and 0.6. A one-frame difference in a sidestep decides whether a shot hits (criterion 16d). Tuning rooms to move a bot's total by one heart would fit the room to the bot's grid phase, not to any player-visible behavior.

I did not change a room or enemy parameter, for these reasons:

- Both D-004 and D-005 expected this movement. The brute no longer being cancelled raises the walker's losses; consumed shots lower them. The net is what the rules produce.
- Any parameter change would force QA to re-verify criteria 11, 13, 14, 15, 18, 20 and 21 for no player-visible gain.
- D-004 and D-005 stay as they are.

## Amended criterion 13 (replaces the numbers in `combat.md`)

**13. Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate (30 FPS and 60 FPS) separately, in rooms 3–5 summed:

- a. The walker clears at least 2 of the 3 rooms. This is the "not walled out" gate.
- b. The walker loses at least 3 and at most 7 hearts. The lower limit is the "costly" gate. 7 is the largest total consistent with 13a (3 hearts per room, at most 2 lost in a cleared room), so the upper limit is a consistency check and not an independent gate.
- c. The dodger loses at most half of the walker's total and clears 3/3.
- d. The camper clears fewer of rooms 3–5 than the walker.
- e. Per-room walker figures are not criteria. The 30 and 60 FPS totals need not match (16d). The two rates are checked separately and not as a range.
- f. Measured values: 0.6 walker 4 lost / 2 cleared at 30 FPS, 7 lost / 2 cleared at 60 FPS. Dodger 0 lost / 3 cleared at both. Camper 0 cleared at both (engineer's figures; QA re-measures).

Reporting rule: QA reports to `game-designer` any measured value that fails 13a–13d. A walker total anywhere in 3–7 with at least 2 rooms cleared is a pass and needs no report, even if it differs from the figures above.

Criteria 14, 15 and 16 are unchanged. Criterion 16c (dodger agrees between rates) and 16d (walker need not) still apply.

## Which figures would change this ruling

The ruling depends on the gradient, not on the exact engineer figures. These QA results would reopen it:

1. The walker clears fewer than 2 of 3 rooms at either rate. That means walled out, and the response would be a room or enemy parameter change, or Director input if it touches D-004 or D-005.
2. The walker loses fewer than 3 hearts at either rate. That means ignoring the cue is not punished enough. The 30 FPS margin is only 1 heart (4 against 3).
3. The dodger loses more than half the walker's total, or fails to clear 3/3.
4. The camper clears as many rooms as the walker or more.
5. QA finds a difference between rates that comes from a rule and not from bot timing (16e). That is a build defect and not a tuning question.

A QA 60 FPS walker figure of 6 or 7 with 2 rooms cleared changes nothing.

## What QA re-verifies

Only criterion 13 against the amended limits, using `run_bots` on the unchanged 0.6 build at both rates. QA also confirms that the walker's 30/60 FPS differences come from the 0.15 s decision grid (16e). Nothing else needs re-verification, because no rule or parameter changed.

## Experience signal (playtest and Review)

A player who ignores the aim cues in rooms 3–5 is hurt often and may fail a room. They can still finish the three rooms without being locked out, and a player who reads the cues does clearly better. If the hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5, reopen this note and D-004/D-005 tuning values. Do not rely on the bot figure alone.
>>>END

<<<FILE design/combat-step-46-room3-cap.md
# Combat design note: room 3 shots in flight after cap delays (step 46, build 0.6)

Status: amends criterion 11 of `design/combat.md` and the "Cap" paragraph. Where this note and `combat.md` differ on criterion 11 or the cap, this note governs. No rule, parameter or room changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-007 (follow-up to D-005 item 4).

## Question

QA (43): in a real room 3 with a surviving, dashing player, the shot cap delays all three second cues. At 6.8 s all three spitters start cues together and shoot together at 7.4 s (and again at 11.0 s / 11.6 s). Up to 5 shots may be in the air, while criterion 11 says "rooms 1–5 never more than 3 in flight". Is that accepted, or does the rule change?

## Ruling

**Accepted. No rule change, no build change.** Criterion 11 was worded too strongly. It contradicted the cap rule in `combat.md`, which says the cap is a limit on cue starts, checked once, and not rechecked at the shot. The contradiction is in the criterion text, so the criterion is changed.

Why accepting is right:

- **The cue is the telegraph, and the cue always ends in a shot.** Refusing or dropping a shot whose cue is already showing would make cues lie. This is the reason given for the cap design in step 22 and it still holds.
- **Three simultaneous cues are readable.** Each spitter shows its own full-brightness line for the full 0.6 s. The three lines are locked on the same point, the player's position at 6.8 s, and meet only there. A player who moves about 1 tile off that point, away from all three lines, clears all three. A dash clears any line it crosses. Shots travel at 3.0 tiles/s, so even when fired together they arrive at different times, spread by their different distances (a 12-tile path takes 4 s). The player never has to answer three arrivals at one instant. This is derived from geometry, not observed with a human.
- **The case is narrow.** It needs a player who keeps all shots alive in the air for several seconds, usually by never killing a spitter (HP 2, stationary, swipeable at any time). It is not the normal way to play room 3. It was seen with a scripted dasher that is not hit.
- **A fix would change a verified room.** The only consistent fix is to extend the cue gap rule to room 3 with a 0.2 s minimum gap (see "Prepared fallback"). It would alter room 3 behavior after any cap delay, and criteria 13, 15, 16 and 18 would need re-measuring. That cost is not justified by an unconfirmed player problem.

The other options were considered and not taken:

- Re-checking the cap at shot release: shots would be dropped or delayed after the cue showed them. That breaks "the cue ends in the shot" and makes cues lie.
- A lower cap for room 3: it makes room 3 delays longer and more frequent, and moves it away from the room that teaches the cue.
- Staggering delayed cues by a fixed gap: this is the prepared fallback, not taken now.

## Amended criterion 11 (replaces the "never more than 3" sentence in `combat.md`)

**11. Stagger and cap.**

- a. Room 3: the first shots are at 1.8, 2.6 and 3.4 s ±1 frame. Rooms 4 and 5: the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). Unchanged.
- b. **Cue starts.** A spitter may start a cue only if fewer than 3 shots are in flight at that moment, at both rates, in every room and in a practice room. Otherwise it waits 0.2 s and checks again.
- c. **Shots in flight.** The number of shots in flight never exceeds 2 plus the number of living spitters, at both rates:
  - Rooms 4 and 5: never more than 3, because cue windows never overlap (criterion 18a).
  - Room 3: up to 5 is accepted, when the cap delays several cues together (up to 2 already in flight at the check, plus one shot from each of three spitters).
  - Practice room with four or more spitters: up to 2 plus the number of living spitters, as before.
- d. **Observation of the count (new).** In `play --view player`, run the QA 43 room 3 script (real room 3, `when see * coming within 2 then dash aside`, 15 s) at 30 and 60 FPS. Count the `*` marks in the room at 7.5 s and at 11.7 s. The expected value is 3 to 5. A count above 5, or a count above 3 in rooms 4–5, is a build defect. A count of 4 or 5 in room 3 is a pass and needs no report. QA records the figures.
- e. Cue timing (criterion 9) holds at every cue, including the simultaneous ones: each cue is 0.6 s ±1 frame before its own shot and each shot goes along its own locked line.

## Hand-timed playtest of room 3

The hand-timed playtest is the check of whether a human can answer the burst. It follows the Build and re-verify, together with the other playtest items already open. The tester plays room 3 and, as one variant, avoids killing the spitters for about 12 s so that a cap delay occurs.

Outcomes that reopen this ruling:

1. The tester is hit by 2 or 3 of the 3 shots of a simultaneous volley, in at least half of the volleys they see, even though they saw the cues.
2. The tester says a shot "came out of nowhere" or cannot say which line to leave in a simultaneous volley.
3. A real-room trace of room 3 shows a count above 5, or a simultaneous start in room 3 at a time before any cap delay.

If none occurs, this ruling stands.

## Prepared fallback (not specified for the build now)

If the playtest reopens this: extend the cue gap rule of rooms 4–5 to room 3 with a minimum gap of **0.2 s** (a spitter starts a cue only if no other cue is running and the last shot in the room was at least 0.2 s ago, with the 1 ms tolerance). The mechanism is the same as in rooms 4–5, with a per-room gap parameter. This reproduces the verified first-shot schedule exactly (cues 1.2–1.8, 2.0–2.6, 2.8–3.4 s) and removes simultaneous starts after a cap delay. It also makes the in-flight bound 3 in room 3. Criteria 11, 13, 15, 16 and 18 would be re-verified for rooms 3–5. This needs its own spec step and a Decision that supersedes D-005 item 4.

## Build change list

**None for this item.** The enemy code does not change. The Build for this handoff is F2 and F3 only (see handoff 46).

## Re-verification needed because of this ruling

- Criterion 11 against the amended wording (a–e above), including the `*` count at 7.5 s and 11.7 s.
- Nothing else. No parameter, rule or room changed, so the criterion 13, 14, 15 and 18 figures are unaffected.

## Undefined or not observed

- The count of 5 shots is derived from timings, not observed. Step d settles it.
- Whether a human can answer the burst is derived from geometry, not observed. The playtest settles it.
- Criteria 2, 6, 10, 17 (a–d), 19f, the isolated runner dash in 3, the runner's one-swipe death in 8, rooms 1–2 contents in 12, 18c with a killed spitter, 20e, 20f, 21b and the 16e decision logs are not affected by this ruling and stay on the re-verify list.

## Experience signal (playtest and Review)

A player in room 3 who sees several cues at once can say which lines are coming and moves out of them. They do not describe a burst of shots as unfair or hidden.
>>>END

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.6

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit or warning.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing.

## Script

One instruction per line; `#` starts a comment.

| Line | Meaning |
|---|---|
| `room 1` … `room 5` | Which room to play (default 1). `room empty` is the practice room. |
| `fps 30` or `fps 60` | Frame rate (default 60). |
| `end 12` | Stop the session at 12 seconds (default: 3 s after the last input; at most 60). |
| `<seconds> move left\|right\|up\|down` | Start moving at that time. |
| `<seconds> stop` | Stop moving. |
| `<seconds> attack` | Swipe. |
| `<seconds> dash [left\|right\|up\|down]` | Dash. |
| `spawn grub\|runner\|brute\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |
| `when <condition> then <action>` | A reaction rule (below). |

## Reactions

Instead of (or as well as) timed inputs, you can play by reacting to what is on screen. Each frame
the rules are checked from the top; the first one whose condition holds acts. A rule acts at most
every 0.15 s, like a player's reaction time, so the next rule down can act meanwhile. A session
with rules runs until the room is cleared or you go down (at most 60 s), unless `end` says
otherwise.

| Condition | Holds when |
|---|---|
| `see <mark> within <n>` | that mark (`g`, `r`, `G`, `s`, `*`, …) is on screen within n tiles of you |
| `see <mark> coming within <n>` | the same, and it has moved closer since the last frame |
| `nothing within <n>` | no enemy or shot is on screen within n tiles |
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"`) |
| `hearts <= <n>` | you have n hearts or fewer |

| Action | Does |
|---|---|
| `attack` | turn to what the condition saw (if anything) and swipe |
| `face` | turn to it without moving |
| `move <dir>`, `move toward`, `move away`, `move aside`, `stop` | move (`aside` steps across its line, toward the open side of the room) |
| `dash`, `dash <dir>`, `dash toward`, `dash away`, `dash aside` | dash |

Example:

```text
room 2
when see * coming within 1.5 then move aside
when see r within 1.4 then attack
when see g within 3 then face
```

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `r` runner grub, `G` brute grub, `s` spitter, `*` projectile, `~` an orange-red
line (see warnings below). Hearts are shown above the room.

- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow,
  4 swipes, long warning, and it does not flinch: a swipe does not interrupt its warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the
  lunge, or swipe a grub or runner (within 1.5 tiles) to cancel it. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second, and no more than 3 are in the air at once. In rooms 4 and 5 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub` or `by a shot`. A swipe that interrupts the warning of a
  grub or runner staggers it for 0.4 s; a brute is not interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.
>>>END

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual; it changes with the build.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  behave the same at 30 and 60 FPS up to frame rounding. Only the dodger reads the new cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
>>>END

<<<FILE decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
---
kind: decision
id: D-004
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-004: Rooms 4–5 get a rule-based 0.6 s cue gap; the brute's wind-up is not cancelled by a swipe; the room 2 spitter is deferred

## Decision

1. **Cue gap as a rule (rooms 4 and 5 only).** A spitter may start a cue only when no other spitter's cue is running and the last shot in the room was at least 0.6 s ago (plus the existing cap). The first-shot offset in these rooms is 1.2 s (shots at 1.8 s and 3.0 s, then alternating every 1.2 s), which meets the rule exactly. The interval stays 2.4 s, the cap stays 3, and room 3 is unchanged.
2. **Brute is not cancelled by a swipe in wind-up.** A per-variant flag "swipe cancels wind-up": standard yes, runner yes, brute no. A swipe still damages the brute, shows "the brute shrugs off the swipe", and the lunge goes ahead. The lane geometry is the same for all variants.
3. **Option 3 (a spitter in room 2) is deferred** out of this slice.

## Rationale

- The crossfire problem (31, S4) is that a cue locks 0.2 s after the previous one ends, at the place the player dodged to. The playtest said the spitters fired "in sync", which the room table and the spec do not support. A rule on cue windows is correct either way, and a fixed offset alone would not be: a cap delay can push two cues together and the offset would not stop it. The offset is chosen so that the rule normally never has to delay anything, which keeps the verified first-shot timing style.
- The melee enemies share one answer (31, S1). A per-variant flag reuses the existing wind-up rule, keeps lane geometry and cue visuals identical (visual spec), needs no new input (D-001) and no new enemy. The brute is the best carrier: it is slow, has the longest warning and the longest recovery, so "step aside, then punish" is readable and fair.
- Option 3 would change criterion 14 and the room 2 identity at the same moment as the brute rule. Both aim at the brute dodging for 20 s, and it is not known whether the brute rule is enough. Doing both together would also make the next playtest unable to say which change worked.

## Alternatives considered

- **Only change the offset, no rule:** simpler, but not robust against a cap delay or against the unconfirmed "in sync" claim. Not chosen.
- **Lower the shot cap to 2 in rooms 4–5:** shortens the number of lines in the air, but delays cues unpredictably and makes the cue timing differ from room 3 in a way the player cannot read. Not chosen; the longer spacing already reduces shots in the air through the existing cap.
- **Gap rule in room 3 too:** room 3 teaches the cue and is verified; criterion 11 would change for no reported problem. Not chosen.
- **A new melee enemy, or widening a lane for the brute so that a dash is needed:** needs a Decide step or breaks the "identical lane geometry" rule of the visual spec. Not chosen.
- **Brute swipe cancels only with the second swipe, or cancels with a longer stagger:** a more complex rule for the player to learn, with no extra answer. Not chosen.
- **Take Option 3 in this slice:** deferred (see Rationale).

## Revisit when

- The hand-timed playtest after Build shows the crossfire in rooms 4–5 is still unfair, or the gap makes it trivial (then the gap and offset are tuning values).
- The playtest shows a human still dodges the brute without ever fighting it in room 2 (then take Option 3 or a room change in a new spec step).
- The bots show the 13/14/15 expectations cannot be met on 0.6 and the cause is the design, not bot policy.
- A graphical build changes cue presentation in a way that makes the "no flinch" signal unreadable.
>>>END

<<<FILE decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-005: A contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted

## Decision

1. **Shots are consumed by any contact.** A shot that makes contact (distance <= 0.4 tile, unchanged detection) with a player who cannot be hurt (dash, hit-stun, or hurt invulnerability up to 0.8 s after a hit) disappears on that frame and deals no damage. It does not pass through and does not wait for the window to end.
2. **A lunge has one hit, and a blocked contact spends it.** A lunge that makes contact (distance <= 0.6 tile) with a protected player deals no damage for the rest of that lunge, even if the protection ends while the grub is still in reach. The lunge is not cancelled or shortened (existing rule), and the next lunge after the recovery damages normally.
3. **Contact sampling is unchanged** (D-002, D-003). Only the consequence of a detected contact changes.
4. **The cue gap rule (D-004) is not extended** to room 3 or practice rooms. A simultaneous cue start there after a cap delay is accepted. Criteria 11 and 18 are unchanged for them.

## Rationale

- The spec said a shot "disappears on contact with the player", so consuming it is the reading closest to the existing text. QA (handoff 36) saw damage land exactly when the hurt window ended (0.15–0.2 s after the shot visibly reached the player), and chained hits at the end of each window. That breaks the pillar "every threat is visible before it can hurt": the player sees the shot touch them, nothing happens, and damage arrives later with no visible cause.
- Consuming makes the dash a clean answer: a shot or lunge that the dash overlaps is finished and cannot hit on the frame after the dash ends. The playtest reported the dash unused; one of the reasons it is unattractive can be that overlap with a threat is risky at the dash's end. This does not make the dash required, so criterion 15 stays a report-only risk.
- Difficulty: rooms 4–5 get easier only in the case of chained hits on a player who is already hurt, which is the unintended behavior. The intended difficulty (a still player is hit by each shot aimed at them that arrives after the window) stays. If the rooms become too easy, the levers are the offset, interval and cap, which are tuning values.
- Lunges: the same rule for the same reason, at a smaller scale (a lunge lasts 0.3 s, the window 0.8 s, so the case is rare but possible when a shot hit just before a lunge).
- Room 3 and practice rooms: the simultaneous start was reproduced only in a practice replica; room 3 is the room that teaches the cue and its verified timing would not change; two simultaneous lines are two readable cues that a sidestep or dash answers. The cost of extending the rule (a changed verified criterion in room 3, code for rooms that the playtest did not flag) outweighs a hypothetical gain.
- Both rulings stay inside D-001 (no new input), the pillars, and the Goal's scope: no new enemy, no healing, no new room content.

## Alternatives considered

- **Pass through (the shot continues and may hit later at a different place):** keeps the shot alive in the air for up to 5 s behind the player and can hit the player when they step back, with the same "hidden hit" problem; harder to read. Not chosen.
- **Stay and hit when the window ends (the apparent 0.5 behavior):** hidden, delayed damage; makes the hurt window a delay rather than protection, chains hits (the 0.8 s window equals the hit spacing in room 3), and weakens the dash. Not chosen.
- **Consume on hurt window but pass through during a dash (so the dash "avoids" but does not "eat"):** a more complex rule with two behaviors for the same thing. Not chosen.
- **A lunge that stops at the first contact with a protected player:** contradicts the existing "the grub finishes the lunge" rule and changes recovery timing in criteria 3 and 5. Not chosen.
- **Extend the gap rule to room 3 and practice rooms (or a smaller start-tie rule):** see Rationale. Not chosen now.
- **Change contact sampling (swept test):** rejected in D-002.

## Revisit when

- The hand-timed playtest after Build finds rooms 4–5 too easy or the dash still unused (then tuning values, or a new spec step; not a silent revert).
- A real-room trace of room 3 (or a playtest) shows simultaneous cue starts that a player cannot answer (then extend a gap or start-tie rule).
- QA's criterion 20 shows the 0.6 build cannot meet the rule for a technical reason (then `technical-director`).
- A graphical build uses a different hitbox or contact test (as in D-002).
>>>END

<<<FILE decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
---
kind: decision
id: D-006
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-006: Criterion 13's walker limit in rooms 3–5 is 3–7 hearts, with at least 2 rooms cleared; no room or enemy parameter changes

## Decision

1. The walker's hearts-lost limit in rooms 3–5 (each rate separately) changes from 3–6 to 3–7. The "clears at least 2 of 3" gate is the primary check that the player is not walled out.
2. The upper limit of 7 is the structural maximum for a walker that clears 2 rooms (3 hearts per room, at most 2 lost in a cleared room). It is kept as a consistency check, not an independent tuning target.
3. Bot results are balance proxies. Per-room walker numbers, and a 30/60 FPS difference in the walker's totals, are not criteria.
4. No room, enemy, cap, offset or interval parameter changes. D-004 and D-005 stand. Build 0.6 is unchanged.
5. The full amended wording is in `design/combat-step-44-walker-limit.md`.

## Rationale

- The limit of 6 was the 0.5 observation recorded as a limit, not a derived bound. The purpose (costly but not hopeless) is met at 7: the dodger loses 0 and clears 3/3, the camper clears 0, and the walker still clears 2 of 3 at both rates.
- A hearts ceiling below the structural maximum only forbids certain distributions of the same outcome. The walker's grid sensitivity moves single hearts between rooms without any player-visible cause. Tuning rooms against it would fit the bot, not the player.
- D-004 and D-005 predicted opposite pressures on the walker (brute no longer cancelled: more losses; consumed shots: fewer). The net result is a consequence of those rulings and is accepted.
- A parameter change would reopen verification of criteria 11, 13, 14, 15, 18, 20 and 21 with no player-visible gain.

## Alternatives considered

- **Keep 6 and change a parameter** (for example a longer brute recovery, or fewer shots in room 4): it fits the grid phase of one bot, forces a wide QA re-verify, and risks undoing D-004 or D-005. Not chosen.
- **Change the walker bot's decision grid:** it changes test tooling to hit a number, hides the real sensitivity, and is not a design answer. Not chosen.
- **Drop the hearts upper limit entirely:** equivalent in practice. Keeping 7 keeps the old criterion shape and a visible check that a walker that clears 2 rooms is within the structural bound. Not chosen, but acceptable if QA prefers.
- **Express the limit as one range across both rates:** weaker, because a rate-specific failure could be hidden. The rates stay separate. Not chosen.

## Revisit when

- QA's independent figures show the walker clearing fewer than 2 of 3 rooms at either rate, a total below 3, the dodger over half the walker's total, or the camper clearing as many rooms as the walker.
- The hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5.
- Any later change to rooms 3–5, the brute, the spitter schedule or the cap moves the bot figures. Re-measure; do not assume 7 still holds.
>>>END

<<<FILE decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
---
kind: decision
id: D-007
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-007: Simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 is reworded to the real in-flight bound

## Decision

1. This is the revisit of D-005 item 4 for room 3, triggered by a real-room trace (QA, handoff 43). Outcome: **accepted as built**. D-005 items 1–4 stand unchanged, and D-004 and D-006 are not touched.
2. The cap stays a limit on cue starts (fewer than 3 shots in flight at the check). It is not rechecked at shot release.
3. Criterion 11 is reworded. Shots in flight never exceed 2 plus the living spitters. That is at most 3 in rooms 4–5 (cue windows never overlap) and up to 5 in room 3 after a cap delay. The sentence "rooms 1–5 never more than 3" is withdrawn.
4. No build change, no parameter change. The reword and the new observation check are in `design/combat-step-46-room3-cap.md`.
5. Reopen triggers are in the same note: a human hit by most of a simultaneous volley, a shot reported as "out of nowhere", or a real-room count above 5. The prepared fallback is a 0.2 s cue gap in room 3.

## Rationale

- The cue is the telegraph. Dropping or refusing a shot whose cue is already showing would make cues lie.
- Three simultaneous cues give three readable lines locked on one point. Moving about 1 tile off that point clears all three, and a dash clears any line it crosses. Shots take up to about 4 s to cross the room, so the arrivals are spread out.
- The case needs a player who keeps spitters alive and shots in the air for several seconds. It was seen only with a scripted dasher, and whether a human can answer it is not observed.
- The only consistent fix changes room 3, the room that teaches the cue, and forces re-measuring of criteria 13, 15, 16 and 18, for an unconfirmed problem.
- The conflict was in the criterion text, not in the rule. D-005 and step 22 already described the 2 plus living spitters bound.

## Alternatives considered

- **Re-check the cap at shot release:** drops or delays shots after the cue showed them, so cues lie. Not chosen.
- **Lower cap for room 3 (for example 2):** more and longer delays, and the cue timing in room 3 drifts from what the player learned. D-004 already declined this for rooms 4–5. Not chosen.
- **Fixed cue gap of 0.2 s in room 3 (the rooms 4–5 mechanism):** keeps first-shot timing and caps the count at 3, but is a change to a verified room and to D-005 item 4. Kept as the prepared fallback, not taken now.
- **Keep criterion 11 as "never more than 3":** it would make the build fail against a rule the spec has stated since step 22. Not chosen.

## Revisit when

- The hand-timed playtest of room 3 shows a human cannot answer a simultaneous volley (hit by most of it, or "came out of nowhere").
- QA's `*` count at 7.5 s or 11.7 s is above 5, or above 3 in rooms 4–5.
- A real-room trace shows simultaneous starts in room 3 before any cap delay.
- Any change to the cap, the spitter interval or the room 3 schedule.
</parameter>
>>>END

<<<FILE goals/G-001-combat-monotony/43-qa-to-studio.md
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
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.2 s). Output:

```text
...........................................................
----------------------------------------------------------------------
Ran 59 tests in 0.186s

OK
```

### Round 1: @run/bots/b30 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 1-5
fps 30
```

Exit: 0 (0.0 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 2: cleared in 10.2 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 2, dashes 0
camper  total: cleared 1/5, hearts lost 14, dashes 0
walker  room 1: NOT cleared (4.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
walker  room 3: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker  room 4: cleared in 9.9 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0
walker  room 5: NOT cleared (10.2 s); hearts lost 3 (hit by: grub 2, shot 1); attacks 9, dashes 0
walker  total: cleared 3/5, hearts lost 9, dashes 0
dodger  room 1: cleared in 6.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 3
dodger  room 2: cleared in 20.7 s; hearts lost 0 (hit by: none); attacks 8, dashes 10
dodger  room 3: cleared in 19.7 s; hearts lost 0 (hit by: none); attacks 6, dashes 8
dodger  room 4: cleared in 18.3 s; hearts lost 0 (hit by: none); attacks 7, dashes 7
dodger  room 5: cleared in 24.2 s; hearts lost 0 (hit by: none); attacks 12, dashes 11
dodger  total: cleared 5/5, hearts lost 0, dashes 39
```

### Round 1: @run/bots/b60 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 1-5
fps 60
```

Exit: 0 (0.1 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 2, dashes 0
camper  total: cleared 0/5, hearts lost 15, dashes 0
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
walker  room 3: cleared in 9.5 s; hearts lost 2 (hit by: shot 2); attacks 6, dashes 0
walker  room 4: NOT cleared (11.1 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 5, dashes 0
walker  room 5: cleared in 12.9 s; hearts lost 2 (hit by: grub 2); attacks 12, dashes 0
walker  total: cleared 3/5, hearts lost 12, dashes 0
dodger  room 1: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 5
dodger  room 2: cleared in 25.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 14
dodger  room 3: cleared in 22.1 s; hearts lost 0 (hit by: none); attacks 6, dashes 10
dodger  room 4: cleared in 17.0 s; hearts lost 0 (hit by: none); attacks 7, dashes 8
dodger  room 5: cleared in 28.8 s; hearts lost 0 (hit by: none); attacks 12, dashes 14
dodger  total: cleared 5/5, hearts lost 0, dashes 51
```

### Round 1: @run/play/f2_30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn brute 9 4
player 8 4
0.1 attack
0.5 attack
end 4
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  0.100  the brute shrugs off the swipe
  0.100  you swipe: brute hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.23 s to the lunge)
  0.500  the brute shrugs off the swipe
  0.500  you swipe: brute hit
  0.800  YOU ARE HIT by a grub — hearts 2/3
   [0.80 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.033  a grub rears back
   [2.03 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.23 s to the lunge)
  2.767  YOU ARE HIT by a grub — hearts 1/3
   [2.77 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.000  a grub rears back
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.2,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
end at 4.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/f2_60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn brute 9 4
player 8 4
0.1 attack
0.5 attack
end 4
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  0.100  the brute shrugs off the swipe
  0.100  you swipe: brute hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.22 s to the lunge)
  0.500  the brute shrugs off the swipe
  0.500  you swipe: brute hit
  0.783  YOU ARE HIT by a grub — hearts 2/3
   [0.78 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.000  a grub rears back
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.20 s to the lunge)
  2.717  YOU ARE HIT by a grub — hearts 1/3
   [2.72 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.933  a grub rears back
   [3.93 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.3,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.3,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.63 s to the lunge)
end at 4.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/f2kill_30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn brute 9 4
player 8 4
0.1 attack
1.0 attack
1.3 attack
2.3 attack
end 4
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  0.100  the brute shrugs off the swipe
  0.100  you swipe: brute hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.23 s to the lunge)
  0.800  YOU ARE HIT by a grub — hearts 2/3
   [0.80 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  (nothing happens)
  1.300  you swipe: brute hit
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.033  a grub rears back
   [2.03 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  2.300  the brute shrugs off the swipe
  2.300  you swipe: brute hit
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.23 s to the lunge)
  2.767  YOU ARE HIT by a grub — hearts 1/3
   [2.77 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.000  a grub rears back
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.2,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
end at 4.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/f2kill_60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn brute 9 4
player 8 4
0.1 attack
1.0 attack
1.3 attack
2.3 attack
end 4
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  0.100  the brute shrugs off the swipe
  0.100  you swipe: brute hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.22 s to the lunge)
  0.783  YOU ARE HIT by a grub — hearts 2/3
   [0.78 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  (nothing happens)
  1.300  you swipe: brute hit
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.000  a grub rears back
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  2.300  the brute shrugs off the swipe
  2.300  you swipe: brute hit
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.20 s to the lunge)
  2.717  YOU ARE HIT by a grub — hearts 1/3
   [2.72 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.933  a grub rears back
   [3.93 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.3,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.3,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.63 s to the lunge)
end at 4.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/r3_30 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 30
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 3 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.89,+0.45) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.89,+0.45) (0.30 s to the shot)
  1.800  a spitter spits
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3
   +----------------+
   |~~              |
   | ~s*            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.45) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |~~              |
   | ~s~            |
   |   ~*~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.89,-0.45) (0.10 s to the shot)
  2.600  a spitter spits
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |     *     ~~~  |
   |         ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~          |
   |  s~         *s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |           ~~~  |
   |     *   ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~       *  |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.45) (0.40 s to the shot)
  3.367  you dash up
  3.400  a spitter spits
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |        P       |
   |       *        |
   |                |
   |                |
   |           *    |
   |  s           s |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *       |
   |          *     |
   |    *           |
   |  s           s |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |         *      |
   |     *   *      |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |       *        |
   |      *    *    |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |      *         |
   |        *       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |     *          |
   |         *      |
   |                |
   |                |
   |                |
   |  s          *s |
   |                |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |   *            |
   |          *     |
   |                |
   |                |
   |                |
   |  s           s*|
   |                |
   +----------------+
  6.800  a spitter takes aim
  6.800  a spitter takes aim
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |     ~~~P~~~    |
   |  s*~~ ~~~      |
   |      ~~ ~~*    |
   |     ~~   ~~    |
   |    ~~     ~~   |
   |   ~~       ~~  |
   |  ~~         ~~ |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.99,-0.16) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.65,-0.76) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.65,-0.76) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |     ~~~P~~~    |
   |  s~~~ ~~~      |
   |      ~~ ~~ *   |
   |     ~~   ~~    |
   |    ~~     ~~   |
   |   ~~       ~~  |
   |  ~~         ~~ |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.99,-0.16) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.65,-0.76) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.65,-0.76) (0.40 s to the shot)
  7.400  a spitter spits
  7.400  a spitter spits
  7.400  a spitter spits
   [7.50 s] hearts 3/3
   +----------------+
   | *      P       |
   |  s          *  |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s *         * |
   |                |
   |                |
   |                |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [8.50 s] hearts 3/3
   +----------------+
   |     *  P       |
   |  s             |
   |                |
   |                |
   |    *       *   |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  8.733  you dash down
   [9.00 s] hearts 3/3
   +----------------+
   |       *        |
   |  s             |
   |                |
   |     *     *    |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [9.50 s] hearts 3/3
   +----------------+
   |        *       |
   |  s             |
   |      *   *     |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [10.00 s] hearts 3/3
   +----------------+
   |          *     |
   |  s    * *      |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [10.50 s] hearts 3/3
   +----------------+
   |        *       |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
 11.000  a spitter takes aim
 11.000  a spitter takes aim
 11.000  a spitter takes aim
   [11.00 s] hearts 3/3
   +----------------+
   |~~             ~|
   | ~s~         ~~~|
   |   ~~~     ~~~  |
   |     ~~~ ~~~    |
   |       ~P~      |
   |     ~~~ ~~~    |
   |   ~~~     ~~~  |
   |  s~         ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.89,+0.45) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.45) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [11.50 s] hearts 3/3
   +----------------+
   |~~             ~|
   | ~s~         ~~~|
   |   ~~~     ~~~  |
   |     ~~~ ~~~    |
   |       ~P~      |
   |     ~~~ ~~~    |
   |   ~~~     ~~~  |
   |  s~         ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 83%, aim line toward (+0.89,+0.45) (0.10 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.89,-0.45) (0.10 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 83%, aim line toward (+0.89,-0.45) (0.10 s to the shot)
 11.600  a spitter spits
 11.600  a spitter spits
 11.600  a spitter spits
   [12.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |        P       |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [12.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |                |
   |        P       |
   |                |
   |     *     *    |
   |  s           s |
   |                |
   +----------------+
   [13.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |      *         |
   |        P       |
   |      *   *     |
   |                |
   |  s           s |
   |                |
   +----------------+
 13.167  you dash up
   [13.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |       * *      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [14.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |       * *      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [14.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |      *   *     |
   |                |
   |          *     |
   |                |
   |  s           s |
   |                |
   +----------------+
   [15.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |     *     *    |
   |                |
   |                |
   |                |
   |           *    |
   |  s           s |
   |                |
   +----------------+
end at 15.00 s: hearts 3/3, enemies left 3
```

### Round 1: @run/play/r3_60 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 60
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 3 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.89,+0.45) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.89,+0.45) (0.30 s to the shot)
  1.800  a spitter spits
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3
   +----------------+
   |~~              |
   | ~s*            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.45) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |~~              |
   | ~s~            |
   |   ~*~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.89,-0.45) (0.10 s to the shot)
  2.600  a spitter spits
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |     *     ~~~  |
   |         ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~          |
   |  s~         *s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |           ~~~  |
   |     *   ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~       *  |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.45) (0.40 s to the shot)
  3.367  you dash up
  3.400  a spitter spits
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |        P       |
   |       *        |
   |                |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *       |
   |          *     |
   |    *           |
   |  s           s |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |         *      |
   |         *      |
   |     *          |
   |  s           s |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *       |
   |      *    *    |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |      *         |
   |        *       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |     *          |
   |         *      |
   |                |
   |                |
   |                |
   |  s          *s |
   |                |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |   *            |
   |          *     |
   |                |
   |                |
   |                |
   |  s           s*|
   |                |
   +----------------+
  6.800  a spitter takes aim
  6.800  a spitter takes aim
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |     ~~~P~~~    |
   |  s*~~ ~~~      |
   |      ~~ ~~*    |
   |     ~~   ~~    |
   |    ~~     ~~   |
   |   ~~       ~~  |
   |  ~~         ~~ |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.99,-0.16) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.65,-0.76) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.65,-0.76) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |     ~~~P~~~    |
   |  s~~~ ~~~      |
   |      ~~ ~~ *   |
   |     ~~   ~~    |
   |    ~~     ~~   |
   |   ~~       ~~  |
   |  ~~         ~~ |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.99,-0.16) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.65,-0.76) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.65,-0.76) (0.40 s to the shot)
  7.400  a spitter spits
  7.400  a spitter spits
  7.400  a spitter spits
   [7.50 s] hearts 3/3
   +----------------+
   | *      P       |
   |  s          *  |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s *         * |
   |                |
   |                |
   |                |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [8.50 s] hearts 3/3
   +----------------+
   |     *  P       |
   |  s             |
   |                |
   |                |
   |    *       *   |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  8.750  you dash down
   [9.00 s] hearts 3/3
   +----------------+
   |       *        |
   |  s             |
   |                |
   |     *     *    |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [9.50 s] hearts 3/3
   +----------------+
   |        *       |
   |  s             |
   |      *   *     |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [10.00 s] hearts 3/3
   +----------------+
   |          *     |
   |  s    * *      |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [10.50 s] hearts 3/3
   +----------------+
   |        *       |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
 11.000  a spitter takes aim
 11.000  a spitter takes aim
 11.000  a spitter takes aim
   [11.00 s] hearts 3/3
   +----------------+
   |~~             ~|
   | ~s~         ~~~|
   |   ~~~     ~~~  |
   |     ~~~ ~~~    |
   |       ~P~      |
   |     ~~~ ~~~    |
   |   ~~~     ~~~  |
   |  s~         ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.89,+0.45) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.45) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [11.50 s] hearts 3/3
   +----------------+
   |~~             ~|
   | ~s~         ~~~|
   |   ~~~     ~~~  |
   |     ~~~ ~~~    |
   |       ~P~      |
   |     ~~~ ~~~    |
   |   ~~~     ~~~  |
   |  s~         ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 83%, aim line toward (+0.89,+0.45) (0.10 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.89,-0.45) (0.10 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 83%, aim line toward (+0.89,-0.45) (0.10 s to the shot)
 11.600  a spitter spits
 11.600  a spitter spits
 11.600  a spitter spits
   [12.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |        P       |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [12.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |    *           |
   |                |
   |        P       |
   |                |
   |    *       *   |
   |  s           s |
   |                |
   +----------------+
   [13.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |      *         |
   |        P       |
   |      *   *     |
   |                |
   |  s           s |
   |                |
   +----------------+
 13.167  you dash up
   [13.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |       * *      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [14.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [14.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |      *   *     |
   |                |
   |          *     |
   |                |
   |  s           s |
   |                |
   +----------------+
   [15.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |     *     *    |
   |                |
   |                |
   |                |
   |           *    |
   |  s           s |
   |                |
   +----------------+
end at 15.00 s: hearts 3/3, enemies left 3
```
>>>END
