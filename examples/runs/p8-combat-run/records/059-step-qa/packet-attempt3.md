# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/62-studio-to-qa.md
next_seq: 64
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/64-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/62-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 62
from: studio
to: qa
stage: Observe
outcome: routed
---
# 62: studio → qa — Close the 30 FPS coverage gaps on the current build (player view, late-swipe boundary)

## Task

On the current build, run the player view at 30 FPS for rooms 1–5 and check the late-swipe boundary at 30 FPS against the design. Report whether anything differs from 60 FPS or from `design/combat.md`.

## Context

Goal G-001 (combat feels monotonous). An earlier QA pass left two items not covered: the player view at 30 FPS, and the late-swipe boundary at 30 FPS. They need closing before the next Review.

## Findings

Not applicable. Do not change the build.

## Decisions already made

- D-002 and D-003: the contact-edge graze is an accepted limitation.
- D-004: a brute's wind-up is not cancelled by a swipe.
- D-005, D-006, D-007: accepted as recorded.

## Constraints

- The project must play correctly at both 30 and 60 FPS.
- Verify from the design and the build, not from any explanation.
- Do not change code or documents other than your report.

## Open questions

None.

## Expected output

A QA report (templates/handoff.md), addressed to `studio`, from `qa`, with `outcome: pass`, `fail` or `done`:

1. **Player view at 30 FPS, rooms 1–5.** Do the warnings, cue lines and hit messages match the rules in `design/combat.md` and `repo/manual.md`? Note any difference from the same scripts at 60 FPS.
2. **Late-swipe boundary at 30 FPS.** Check these cases for a grub and a runner:
   - a swipe in reach while the wind-up is still running cancels it;
   - a swipe landing just after the lunge has begun does not cancel it;
   - a swipe that is out of reach (the grub starts about 2 tiles away) does not cancel it.
   Compare with 60 FPS and say whether the boundary differs by more than one frame at 30 FPS.
3. A defect report with reproduction steps and acceptance criteria for anything that fails.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, the build (`repo/`; `run_play`, `run_trace`, `run_tests`)
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/56-qa-to-studio.md
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

<<<FILE studio/skills/reproduce-defect.md
---
name: reproduce-defect
description: Reproduce a reported problem reliably and turn it into a precise defect report with acceptance criteria for the fix.
---
# Skill: Reproduce defect

Typical roles: qa. Any Role whose responsibility covers confirming a defect may use it.

## When to use

A problem is reported but has not been reproduced first-hand, or its conditions are unclear.

## Inputs

The report, how to run the build, the design documents that define expected behavior, the
project's supported platforms and settings.

## Method

1. Reproduce exactly as reported. Then vary one condition at a time (timing, input device, frame
   rate, platform, state) to find the minimal reliable steps and the boundary where it stops.
2. Name the source of "expected": cite the design document or Decision. If no source defines the
   expected behavior, it is a spec gap, not a defect — say so and hand back to `game-designer`.
3. Rate severity from the player's view (blocks progress / hurts the experience / cosmetic) and
   frequency.
4. Write acceptance criteria for the fix: observable checks, including the conditions you varied.

## Output

Defect report: steps, expected (with source), actual, conditions and boundary, severity, frequency,
acceptance criteria, evidence (logs, recordings, notes).

## Do not

Guess at code-level causes as fact; label any hypothesis as one. Do not fix the defect.
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

<<<FILE decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-003: A miss of exactly the reach is inside the contact band; measured lunge band recorded (follow-up to D-002)

## Decision

This is a follow-up to D-002. D-002 stays in force and is not edited. It is refined as follows.

1. **Exactly the reach is inside the band.** A path whose lateral miss is exactly the reach (0.400 for shots, 0.600 for lunges) belongs to the accepted band. Hit or miss is accepted at either frame rate, and 30 and 60 FPS may differ. It is not a guaranteed miss. The `distance <= reach` check in the build stays, so no Build change is needed.
2. **The band has no gap and no overlap.** It is the lateral miss more than reach − tolerance and up to and including the reach: more than 0.39 up to 0.40 for shots, more than 0.57 up to 0.60 for lunges. At reach − tolerance or less: hit at both rates. More than the reach: miss at both rates. Criterion 17 and the contact sampling rule in `design/combat.md` are reworded to this. No number changes, so criteria already verified in handoffs 20 and 24 remain valid.
3. **Measured lunge band (QA, handoff 24, derived and probed).** A lunge hit is guaranteed up to a lateral miss of about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. Probes: 0.570 hit and 0.610 miss at both rates; the rates disagreed only at 0.590 (0.580 and 0.599 agreed, because the frame phase differs between positions). **Limit:** five probes, not a full scan. There is no evidence of a band wider than 0.03 tile, which is the threshold at which QA must report back. The shot band figure (about 0.003 tile) is likewise derived.

## Rationale

- Exactly the reach cannot be made a guaranteed miss without changing `<=` to `<`. That is a Build change to a verified build, and then a re-Verify, for a case a player cannot produce or see (a difference of 0.000 tile). D-002 already rejected changing contact for no player-observable gain.
- Putting the reach inside the band matches the band definition QA read ("reach − 0.01 to reach") and makes criterion 17 unambiguous without changing what was verified.
- Recording the measured band keeps D-002's estimate ("derived, not yet run") honest. The figures are well inside the 0.03 tolerance, and the sidestep margins (0.3 tile or more, 1.2-tile lane) are far larger.

## Alternatives considered

- Guaranteed miss at exactly the reach (`<` instead of `<=`): the cleaner rule on paper, but a Build change plus re-Verify of every hit-time criterion, with no visible benefit. Not chosen.
- Leave the wording ambiguous: QA already had to make a judgment call. Not chosen.
- Run a full scan of the lunge band before recording: not needed. The decision does not depend on the exact width as long as it stays within 0.03 tile.

## Revisit when

- QA or a playtest finds a lunge band wider than 0.03 tile (report to `game-designer`).
- A graphical build uses different hitboxes or a different contact test (as in D-002); criterion 17 must then be re-verified and the band rewritten.
- A playtest reports "I dodged it and it still hit me" or the reverse, and the cause is the edge band.
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

<<<FILE goals/G-001-combat-monotony/56-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 56
from: qa
to: studio
stage: Triage
outcome: done
---
# 56: qa → studio — Three "unfair" hits (rooms 2 and 5) and the wording point: no build defect; one manual wording gap for Design

## Task

Reproduce the playtester's three hit moments (handoff 53) and check the "A grub rears back" wording. Verdict: **items 1–3 reproduce and match the design documents and the build. Item 4 matches the documents. No defect and no "expected behavior undefined" case.** One low-severity manual wording gap goes to Design, and there is one player-experience observation (item 4).

`python3 -m unittest discover -s tests`: **59 tests, OK** (build 0.6).

## Context

Goal G-001. The scripts from handoff 55 were run through the player view and trace at 60 FPS (room 2) and the trace at 30 FPS (rooms 2 and 5). The room 5 trace at 60 FPS was also run. I also ran a practice-room script for the late-swipe boundary. As in step 32, the swipes landed after the wind-up ended. The cases differ from step 32 in two ways:

- Item 1 and item 2: the swipe was out of reach during the whole wind-up (see below).
- Item 3 is not a swipe case at all.

## Findings

### Item 1: room 2, late swipe at a rearing grub. Reproduced at 60 FPS. Matches (not a defect).

60 FPS trace and player view:

| Time (s) | Event |
|---|---|
| 3.550 | grub `windup:0.500`; player (10.47,4.00), grub (11.34,2.23) |
| 4.00 | last printed cue line: "0.05 s to the lunge" |
| 4.050 | grub `lunge` begins |
| 4.150 | player view: "you swipe: grub hit" (trace row 4.167): grub hp 2→1, phase still `lunge` |
| 4.250 | `hurt` by the grub, hearts 3→2; grub goes to `recovery` |

- **Where the "0.05 s" came from.** The player view prints a picture at every half second and at events. The last cue line before the hit was at 4.00 s, with 0.05 s left. The swipe was at 4.15 s, which is **0.10 s after the lunge began** (4.05 s). It was not in the last 0.05 s of the wind-up.
- **Reach.** During the wind-up the grub was about 1.97 tiles from the player (10.47,4.00 to 11.34,2.23). The swipe reach is 1.5 tiles, and the rule `see g within 1.4 then attack` could not fire. The swipe became possible only once the lunge had brought the grub within reach.
- **Governing lines.** `design/combat.md` says a swipe that damages a grub in wind-up cancels it. A grub hit but not killed during Lunge continues its phase unchanged. A lunge that reaches a hurtable player deals 1 damage.
- **Is "in range, landed, needs more than one swipe" the explanation?** Partly. The swipe did land, and the grub had 2 HP (2→1). But the number of swipes is not the reason. A single non-lethal swipe during the wind-up cancels a 2 HP grub. The reason is timing: the swipe came after the wind-up ended.
- **Boundary check (practice room, 60 FPS).** Script: `room empty`, `spawn grub 9.3 4`, `player 8 4`, `0.45 attack`.
  - The wind-up started at 0.017 and the swipe landed at 0.467 with about 0.05 s of wind-up left.
  - The result was `stagger:0.383`, grub hp 1, no lunge, and a new wind-up at 0.867.
  - So a swipe with 0.05 s left does cancel a standard grub, when the grub is in reach.
- **Contact.** The hit was a centre-lane contact: grub (10.63,3.67) against player (10.20,4.00), distance about 0.54. It is not in the D-002/D-003 band (0.57–0.60).
- **30 FPS room 2.** The same script gave a different course. The grub's wind-up started at 3.567, the lunge at 4.067 and the swipe at 4.233 (hp 2→1, lunge continues). The lunge ended in `recovery` at 4.367 with hearts still 3, so there was no hit. The player stood at (9.87,4.00) at 4.233, against (10.13,4.00) at 4.067, and the grub ended its lunge at (10.34,4.42), which is about 0.7 tile from the player.
- **Likely cause of the 60/30 difference (hypothesis, not confirmed in code).** The reaction rules act on a 0.15 s grid, so the player's position differs between rates. The documents say bot or script timing differences are not a build defect (criterion 16d/16e). I did not test that the same decision from the same position gives the same outcome at both rates.

**Verdict: matches. Not the same as step 32 in detail, but the same class: the swipe landed in the lunge, not the wind-up.** Neither case is the D-002 graze.

### Item 2: room 5, swipe at a rearing grub. Reproduced at 60 FPS (8.35 / 8.95 / 9.03 s). Matches.

| Time (s) | Event |
|---|---|
| 8.350 | grub `windup:0.500`; player (7.33,0.00), grub (6.57,1.85) |
| 8.850 | `lunge` begins |
| 8.950 | `attack` hit: grub hp 2→1, phase `lunge` |
| 9.033 | `hurt` by the grub, hearts 1→0, `down`; grub goes to `recovery:0.800` |

- **Timing and reach.** The playtester's 8.93 s swipe is 0.10 s after the lunge began (8.85 s). The grub was 2.0 tiles away during the wind-up, outside the 1.5 reach, and the player was against the top wall (y=0), where "move aside" had no room. The grub had 2 HP, so one swipe could not kill it.
- **The "two swipes" thought.** The player thought the grub needed two swipes. A swipe in wind-up would have cancelled it, but the swipe landed in the lunge.
- **Blocked-contact rule (D-005).** At 8.95 s the player's last hit was at 6.433 s, so the hurt window had ended at 7.233 s. The player was hurtable and the lunge was not blocked. D-005 does not apply to the 9.03 s hit.
- **Contact.** The lunge reached the player at distance about 0.56 and a small lateral miss. It is a centre hit, not in the band.
- **D-005 evidence from the same trace (60 FPS, 7.0–7.4 s).**
  - A grub lunged at 7.000 while the player was inside a hurt window (`hurt_left` 0.233, hurt at 6.433).
  - At 7.200 (`hurt_left` 0.033) the grub was at (7.66,0.33), about 0.39 from the player, so contact was made while the player was protected.
  - The window ended at 7.233 with the grub still in `lunge` and within 0.6 of the player (7.80,0.10 then 7.87,0.00 on the player). No damage followed. Hearts stayed at 1 through 7.4, and the grub went to `recovery`.
  - This matches "a blocked contact spends the lunge's hit; the lunge is not cancelled" (criterion 21b).
  - Another case at 30 FPS (13.6–13.9 s, grub in recovery at 13.900 with the player at about 0.5 tile and `hurt_left` 0.100, then no hit when the window ended) is consistent but less conclusive.
- **30 FPS room 5.** The exact moment did not recur at the same time, but the same pattern did. The grub's wind-up started at 14.300 and its lunge at 14.800. A swipe at 14.933 hit it (hp 2→1) in the lunge, and the hit followed at 15.000 (hearts 1→0).

**Verdict: matches. Not a defect.**

### Item 3: room 2, hit at about 5.4 s with no cue seen. Reproduced at 60 FPS. A cue was printed, so the design requirement is met.

| Time (s) | Event |
|---|---|
| 4.267 | first runner `windup` |
| 4.617 | that runner's lunge |
| 4.917 | **second runner** `windup:0.350` at (8.09,4.73); the first runner is in `recovery` |
| 5.000 | the swipe that killed "a runner" killed the **first** runner (the recovering one at (10.61,4.10)), not the winding-up one |
| 5.267 | second runner's `lunge` |
| 5.400 | `hurt` by the second runner (shown as "by a grub"), hearts 2→1 |

- **The printed cue.** The player view printed `4.917 a grub rears back`, a picture with `~`, and `cue: r at (8.1,4.7) flashes orange-red, lunge line toward (+0.93,-0.37), 2.4 tiles (0.35 s to the lunge)`. It printed the cue again at 5.00 with "0.27 s to the lunge", and the same picture shows "you swipe: runner defeated".
- **Why it looked like no cue.** The cue came **before** the swipe at 5.000, not after it. The swipe killed the other runner. The next lunge, from the second runner, was the one that hit at 5.400. The text view removes the line when the lunge starts, so the 5.40 picture has no `~`, which is the documented behavior.
- **Warning duration.** The cue was visible 0.48 s before the hit, from 4.917 to 5.400. The runner's wind-up is 0.35 s, which is the documented minimum.
- **Why the player was hit.** The player was hurt-stunned until 4.617 and had moved only about 0.2 tile across the lane (y 4.0→3.8) by 5.017. Lateral miss at the hit was about 0.41 tile, which is a true hit and not in the band. I did not investigate why the reaction script moved so little (hypothesis only: an attack rule acted at 5.0).
- **One-at-a-time.** The second runner began its wind-up only when the first was in recovery, so the "one at a time" rule held.
- **30 FPS.** The sequence differed because of the earlier divergence. A runner's `windup` is logged at 4.400, its lunge at 4.767 and the hit at 4.900. A second runner's `windup` at 4.900 led to a lunge at 5.267, but the player had killed that runner (5.300) before it hit. Every hit in the 30 FPS trace is preceded by a `windup` event for the same enemy. I did not run the player view at 30 FPS, so the printed lines are confirmed at 60 FPS only.

**Verdict: matches. There was a cue and it was printed. Not a defect.**

### Item 4: wording "A grub rears back" for all variants. Matches the documents.

- `design/combat.md` says: "Text view: message 'a grub rears back' when it starts (all variants, unchanged in step 35)."
- `repo/manual.md` says: "**A grub rears back** (message `a grub rears back`)", followed by the `cue:` line that "names the grub". It gives warning times per variant but does not give a per-variant message.
- The build matches. The runner's cue at 4.267 s printed `a grub rears back` and `cue: r ...`. The brute's message differs only for the swipe ("the brute shrugs off the swipe").
- The variant-specific look is a graphical build matter (visual spec: silhouette, size, cadence). The text view relies on `cue: r|g|G`.

**Verdict: matches. No mismatch.** The playtester wasted dashes by reacting to the message alone (handoff 53, "Same message for every lunger"). That is an experience point for `game-designer`, not a defect. I do not decide whether the message should name the variant.

## Decisions already made

D-005 (blocked contact consumes the shot and spends the lunge's hit) applies only as stated for item 2 (consistent). D-002/D-003 (contact band): none of the contacts above lie in the band.

## Constraints

- The build was not changed. All results come from the run results in this step: tests, player view and trace at 60 FPS, trace at 30 FPS, and one practice-room script.
- Experience judgments (monotony, fun) are not assessed here.

## Open questions

For `game-designer` (low priority, wording only, no rule change needed):

1. Does the manual say clearly enough that a swipe cancels a lunge **only during the warning**, and not once the lunge has started? Current text: "step 1 tile to the side or dash to avoid the lunge, or swipe a grub or runner (within 1.5 tiles) to cancel it". It does not say "during the warning" there. The line "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s" is the only place the limit appears. It also does not say that a swipe out of reach during the warning (a grub starts winding up at about 2 tiles, beyond the 1.5 reach) can't cancel anything, which is how both of this playtester's late swipes happened. Same gap as step 32.
2. How many swipes does a grub take? The manual says "2 swipes", which is clear. A non-lethal swipe in wind-up cancels the lunge, so a player does not need two swipes to cancel. If the designer wants the manual to say this, it is wording.
3. Experience point from item 4: whether a text-view player should be able to tell the variant from the message (the player reacted to "rears back" alone and dashed at a distant runner). Out of QA scope.

Not covered:

- Player view at 30 FPS.
- The late-swipe boundary at 30 FPS.
- A swipe exactly at the end of the wind-up (0.5 s boundary): only the 0.45 s case was run.
- The 60 vs 30 FPS divergence in item 1 was explained as script timing but not isolated.

## Expected output

Studio: close items 1–4 of this request as not-a-defect. Send the wording question above to `game-designer` (low priority). No fix is requested from `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/55-studio-to-qa.md
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
Ran 59 tests in 0.188s

OK
```

### Round 1: @run/play/room1-30 — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 30
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see g within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 1 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.033  a grub rears back
   [2.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |        ~       |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |        ~       |
   |     g P~    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.03 s to the lunge)
  2.633  you swipe: grub hit
  2.767  YOU ARE HIT by a grub — hearts 2/3
   [2.77 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      gPg   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.800  a grub rears back
   [2.80 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      gPg   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (5.8,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      gPg   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (5.8,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.30 s to the lunge)
  3.167  you swipe: grub defeated
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P    g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.533  you swipe: grub hit
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       Pg  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.033  you swipe: grub defeated
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P   g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P  g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P  g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.567  a grub rears back
   [5.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P~g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [6.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |       ~~g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.07 s to the lunge)
  6.167  you swipe: grub hit
  6.300  YOU ARE HIT by a grub — hearts 1/3
   [6.30 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.667  you swipe: grub defeated
  6.700  room cleared
   [7.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 7.70 s: hearts 1/3, enemies left 0
```

### Round 1: @run/play/room2-30 — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 30
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see r within 3 then face
when see G within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 2 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  r             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               G|
   | r              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |              g |
   |   r            |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               G|
   |  r             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |   r            |
   |                |
   |        P       |
   |                |
   |                |
   |  r           G |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |    r           |
   |                |
   |        P       |
   |                |
   |                |
   |   r          G |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |     r          |
   |                |
   |        P       |
   |                |
   |    r         G |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |                |
   |      r         |
   |        P       |
   |                |
   |    r        G  |
   |                |
   |                |
   +----------------+
  3.000  a grub rears back
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r~        |
   |       ~P       |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,3.1) flashes orange-red, lunge line toward (+0.89,+0.45), 2.4 tiles (0.35 s to the lunge)
  3.433  you swipe: runner defeated
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |        P       |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
  3.867  a grub rears back
   [3.87 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |       ~P       |
   |      r~        |
   |             G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.3,4.9) flashes orange-red, lunge line toward (+0.85,-0.53), 2.4 tiles (0.35 s to the lunge)
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |       ~P       |
   |      r~        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (6.3,4.9) flashes orange-red, lunge line toward (+0.85,-0.53), 2.4 tiles (0.22 s to the lunge)
  4.300  you swipe: runner defeated
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
  5.267  a grub rears back
   [5.27 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         ~g     |
   |        P~      |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: g at (9.6,2.9) flashes orange-red, lunge line toward (-0.83,+0.56), 2.4 tiles (0.50 s to the lunge)
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        P~g     |
   |        ~~      |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.6,2.9) flashes orange-red, lunge line toward (-0.83,+0.56), 2.4 tiles (0.27 s to the lunge)
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |        P       |
   |                |
   |                |
   |        g       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |        g       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |        g       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |        g  G    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |        g       |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.167  a grub rears back
   [9.17 s] hearts 3/3
   +----------------+
   |        P       |
   |        ~       |
   |        g       |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (7.8,2.0) flashes orange-red, lunge line toward (+0.08,-1.00), 2.4 tiles (0.50 s to the lunge)
   [9.50 s] hearts 3/3
   +----------------+
   |       P~       |
   |        ~       |
   |        g       |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (7.8,2.0) flashes orange-red, lunge line toward (+0.08,-1.00), 2.4 tiles (0.17 s to the lunge)
   [10.00 s] hearts 3/3
   +----------------+
   |     P  g       |
   |                |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 3/3
   +----------------+
   |   P    g       |
   |                |
   |                |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.00 s] hearts 3/3
   +----------------+
   | P      g       |
   |                |
   |                |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.50 s] hearts 3/3
   +----------------+
   |P      g        |
   |                |
   |                |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 3/3
   +----------------+
   |P      g        |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 3/3
   +----------------+
   |P     g         |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.00 s] hearts 3/3
   +----------------+
   |P     g         |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.50 s] hearts 3/3
   +----------------+
   |P    g          |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.00 s] hearts 3/3
   +----------------+
   |P    g          |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.50 s] hearts 3/3
   +----------------+
   |P   g           |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.00 s] hearts 3/3
   +----------------+
   |P   g           |
   |                |
   |      G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.50 s] hearts 3/3
   +----------------+
   |P  g            |
   |                |
   |      G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.00 s] hearts 3/3
   +----------------+
   |P  g            |
   |                |
   |      G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.50 s] hearts 3/3
   +----------------+
   |P g             |
   |                |
   |     G          |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.867  a grub rears back
   [16.87 s] hearts 3/3
   +----------------+
   |P~g             |
   |     G          |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (2.0,0.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [17.00 s] hearts 3/3
   +----------------+
   |~~g             |
   |P    G          |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (2.0,0.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.37 s to the lunge)
   [17.50 s] hearts 3/3
   +----------------+
   | g              |
   |     G          |
   |                |
   |P               |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [18.00 s] hearts 3/3
   +----------------+
   |g               |
   |                |
   |    G           |
   |                |
   |                |
   |P               |
   |                |
   |                |
   |                |
   +----------------+
   [18.50 s] hearts 3/3
   +----------------+
   |g               |
   |                |
   |    G           |
   |                |
   |                |
   |                |
   |                |
   |P               |
   |                |
   +----------------+
   [19.00 s] hearts 3/3
   +----------------+
   |                |
   |g               |
   |    G           |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [19.50 s] hearts 3/3
   +----------------+
   |                |
   |g               |
   |    G           |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [20.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |g               |
   |   G            |
   |                |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [20.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |g               |
   |   G            |
   |                |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [21.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |g  G            |
   |                |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [21.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |g               |
   |   G            |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [22.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |g  G            |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [22.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |g G             |
   |                |
   |                |
   |                |
   |P               |
   +----------------+
   [23.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |  G             |
   |g               |
   |                |
   |                |
   |P               |
   +----------------+
   [23.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |g G             |
   |                |
   |                |
   |P               |
   +----------------+
   [24.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |  G             |
   |g               |
   |                |
   |P               |
   +----------------+
 24.500  a grub rears back
   [24.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |  G             |
   |g               |
   |~               |
   |P               |
   +----------------+
   cue: g at (0.0,6.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
   [25.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |g G             |
   |                |
   |P               |
   +----------------+
 25.100  you swipe: grub hit
 25.200  YOU ARE HIT by a grub — hearts 2/3
   [25.20 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   |                |
   |P               |
   +----------------+
   [25.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   |                |
   |P               |
   +----------------+
 25.600  you swipe: grub defeated
 25.967  a grub rears back
   [25.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | ~              |
   |P~              |
   +----------------+
   cue: G at (1.2,6.3) flashes orange-red, lunge line toward (-0.48,+0.87), 2.4 tiles (0.70 s to the lunge)
   [26.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | ~              |
   |P~              |
   +----------------+
   cue: G at (1.2,6.3) flashes orange-red, lunge line toward (-0.48,+0.87), 2.4 tiles (0.67 s to the lunge)
   [26.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | ~              |
   |~P              |
   +----------------+
   cue: G at (1.2,6.3) flashes orange-red, lunge line toward (-0.48,+0.87), 2.4 tiles (0.17 s to the lunge)
 26.733  you swipe: brute hit
 26.833  YOU ARE HIT by a grub — hearts 1/3
   [26.83 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | P              |
   +----------------+
   [27.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | P              |
   +----------------+
 27.233  you swipe: brute hit
   [27.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | P              |
   +----------------+
 27.733  you swipe: brute hit
   [28.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | P              |
   +----------------+
 28.067  a grub rears back
   [28.07 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | G              |
   | P              |
   +----------------+
   cue: G at (0.6,7.4) flashes orange-red, lunge line toward (+0.13,+0.99), 2.4 tiles (0.70 s to the lunge)
 28.100  you swipe: brute defeated
 28.133  room cleared
   [28.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | P              |
   +----------------+
   [29.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | P              |
   +----------------+
end at 29.13 s: hearts 1/3, enemies left 0
```

### Round 1: @run/play/room3-30 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 30
end 12
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when see s within 1.4 then attack
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
   |     ~~~P       |
   |       ~~~      |
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
   |       ~~       |
   |  s*    P~      |
   |         ~      |
   |          ~~    |
   |           ~~   |
   |            ~   |
   |             ~  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.70,-0.72) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |       ~~       |
   |  s     ~~      |
   |    *    ~      |
   |        P ~~    |
   |           ~~   |
   |            ~   |
   |             ~  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.70,-0.72) (0.10 s to the shot)
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
   |   ~~~        * |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |           ~~~  |
   |     *  P~~~    |
   |       ~~~      |
   |     ~~~        |
   |   ~~~       *  |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.45) (0.40 s to the shot)
  3.400  a spitter spits
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s     P       |
   |                |
   |       *        |
   |                |
   |            *   |
   |                |
   |  s           s |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *  *    |
   |                |
   |    *           |
   |  s           s |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |          *     |
   |                |
   |     *   *      |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |         *      |
   |                |
   |                |
   |      *    *    |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s     *       |
   |                |
   |                |
   |        *       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
  5.633  YOU ARE HIT by a shot — hearts 2/3
   [5.63 s] hearts 2/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
  5.800  a spitter takes aim
  5.800  a spitter takes aim
  5.800  a spitter takes aim
   [5.80 s] hearts 2/3
   +----------------+
   |     ~~~P~~     |
   |  s~~~ ~~~      |
   |      ~  ~~     |
   |     ~~   ~~    |
   |    ~~   * ~~   |
   |   ~~       ~   |
   |  ~~         *  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.98,-0.18) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.67,-0.74) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.62,-0.78) (0.60 s to the shot)
   [6.00 s] hearts 2/3
   +----------------+
   |     ~~~P~~     |
   |  s~~~ ~~~      |
   |      ~  ~~     |
   |     ~~  *~~    |
   |    ~~     ~~   |
   |   ~~       ~   |
   |  ~~         ~  |
   |  s          *s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.98,-0.18) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.67,-0.74) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.62,-0.78) (0.40 s to the shot)
  6.400  a spitter spits
  6.400  a spitter spits
  6.400  a spitter spits
   [6.50 s] hearts 2/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |          *     |
   |                |
   |                |
   |                |
   |  s           s*|
   |                |
   +----------------+
   [7.00 s] hearts 2/3
   +----------------+
   |        P       |
   |  s *           |
   |            *   |
   |                |
   |                |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |     *  P       |
   |  s          *  |
   |                |
   |                |
   |    *       *   |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.00 s] hearts 2/3
   +----------------+
   |       *        |
   |  s     P     * |
   |                |
   |     *     *    |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |        *       |
   |  s    P        |
   |      *   *     |
   |                |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   |          *     |
   |  s    * *      |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
   +----------------+
   |        *       |
   |  s             |
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |  s           s |
   |                |
   +----------------+
 10.000  a spitter takes aim
 10.000  a spitter takes aim
 10.000  a spitter takes aim
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |  ~~            |
   |   ~~           |
   |    ~~          |
   |     ~~         |
   |      ~~        |
   |  s~~~~P~~~~~~s |
   |~~~~~  ~~ ~~~~~~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.64,+0.76) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.05) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.06) (0.60 s to the shot)
   [10.50 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |  ~~            |
   |   ~~           |
   |    ~~          |
   |     ~~P        |
   |      ~~        |
   |  s~~~~~~~~~~~s |
   |~~~~~  ~~ ~~~~~~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 83%, aim line toward (+0.64,+0.76) (0.10 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-1.00,+0.05) (0.10 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 83%, aim line toward (+1.00,+0.06) (0.10 s to the shot)
 10.600  a spitter spits
 10.600  a spitter spits
 10.600  a spitter spits
   [11.00 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |       P        |
   |                |
   |                |
   |                |
   |  s*         *s |
   |                |
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |                |
   |  s    P        |
   |                |
   |    *           |
   |                |
   |                |
   |                |
   |  s  *     *  s |
   |                |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |       P        |
   |  s             |
   |                |
   |                |
   |     *          |
   |                |
   |                |
   |  s   *   *   s |
   |                |
   +----------------+
end at 12.00 s: hearts 2/3, enemies left 3
```

### Round 1: @run/play/room4-30 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 30
end 15
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see r within 1.4 then attack
when see s within 1.4 then attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 4 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | r      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   |  r     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   r    P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   | g          ~~~ |
   |           ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g         ~~   |
   |        P~~     |
   |   r   ~~~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |        P       |
   |  g             |
   |                |
   |    r           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |        P      s|
   |  g      ~   *  |
   |         ~~     |
   |     r    ~~    |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.66,-0.75) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |        P      s|
   |  g      ~   *  |
   |         ~~     |
   |     r    ~~    |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.66,-0.75) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |   g            |
   |        P   *   |
   |     r          |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |      r   *     |
   |        P       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |   g       ~~~  |
   |      r   *~    |
   |         ~~     |
   |       ~P       |
   |      ~~        |
   |    ~~~       * |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.82,+0.57) (0.60 s to the shot)
  3.733  a grub rears back
   [3.73 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |      r~  *~    |
   |       ~ ~~     |
   |       P~       |
   |      ~~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: r at (6.4,3.2) flashes orange-red, lunge line toward (+0.56,+0.83), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 22%, aim line toward (-0.82,+0.57) (0.47 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |      r~ *~~    |
   |       ~ ~~     |
   |       ~~P      |
   |      ~~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: r at (6.4,3.2) flashes orange-red, lunge line toward (+0.56,+0.83), 2.4 tiles (0.08 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.82,+0.57) (0.20 s to the shot)
  4.200  a spitter spits
  4.233  you swipe: runner defeated
   [4.50 s] hearts 3/3
   +----------------+
   |               s|
   |              * |
   |    g           |
   |                |
   |        *       |
   |       P    *   |
   |                |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |     g          |
   |           *    |
   |                |
   |       * P      |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |          * *   |
   |     g          |
   |                |
   |           P    |
   |     *          |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |               s|
   |         *      |
   |                |
   |      g   *     |
   |                |
   |             P  |
   |    *           |
   |                |
   |               s|
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        *      s|
   |                |
   |                |
   |      g         |
   |         *      |
   |               P|
   |                |
   |   *            |
   |               s|
   +----------------+
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |               s|
   |               ~|
   |               ~|
   |      g        ~|
   |        *      ~|
   |               P|
   |               ~|
   |               ~|
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |               s|
   |               ~|
   |               ~|
   |       g       ~|
   |               ~|
   |        *     P~|
   |               ~|
   |               ~|
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (+0.00,+1.00) (0.40 s to the shot)
  7.400  a spitter spits
   [7.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |       g        |
   |                |
   |            P   |
   |       *        |
   |                |
   |               s|
   +----------------+
  8.000  a spitter takes aim
   [8.00 s] hearts 3/3
   +----------------+
   |  ~~~          s|
   |    ~~          |
   |     ~~~       *|
   |       g~       |
   |        ~~~     |
   |          P~    |
   |           ~~~  |
   |      *      ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.83,-0.55) (0.60 s to the shot)
   [8.50 s] hearts 3/3
   +----------------+
   |  ~~~          s|
   |    ~~          |
   |     ~~~        |
   |       ~g P    *|
   |        ~~~     |
   |          ~~    |
   |           ~~~  |
   |    *        ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-0.83,-0.55) (0.10 s to the shot)
  8.600  a spitter spits
   [9.00 s] hearts 3/3
   +----------------+
   |               s|
   |          P     |
   |                |
   |        g       |
   |                |
   |               *|
   |                |
   |              * |
   |   *           s|
   +----------------+
  9.200  a spitter takes aim
   [9.20 s] hearts 3/3
   +----------------+
   |~~~~~~~~~~P~~~~s|
   |                |
   |                |
   |        g       |
   |                |
   |               *|
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [9.50 s] hearts 3/3
   +----------------+
   |~~~~~~~~~P~~~~~s|
   |                |
   |                |
   |         g      |
   |                |
   |                |
   |             * *|
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
  9.800  a spitter spits
   [10.00 s] hearts 3/3
   +----------------+
   |       P      *s|
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   [10.50 s] hearts 3/3
   +----------------+
   |     P       * s|
   |                |
   |        g       |
   |                |
   |                |
   |          *     |
   |                |
   |                |
   |               s|
   +----------------+
 10.600  a spitter takes aim
   [10.60 s] hearts 3/3
   +----------------+
   |    ~P       * s|
   |     ~~         |
   |       ~g       |
   |        ~~      |
   |         ~~     |
   |          *~~   |
   |            ~~  |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.79,-0.61) (0.60 s to the shot)
   [11.00 s] hearts 3/3
   +----------------+
   |    ~~     *   s|
   |     ~~         |
   |     P ~g       |
   |        ~~      |
   |         *~     |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 67%, aim line toward (-0.79,-0.61) (0.20 s to the shot)
 11.200  a spitter spits
   [11.50 s] hearts 3/3
   +----------------+
   |          *    s|
   |                |
   |       g        |
   |        *       |
   |     P          |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   [12.00 s] hearts 3/3
   +----------------+
   |        *      s|
   |                |
   |      *g        |
   |                |
   |                |
   |                |
   |     P       *  |
   |                |
   |               s|
   +----------------+
   [12.50 s] hearts 3/3
   +----------------+
   |       *       s|
   |     *          |
   |                |
   |       g        |
   |                |
   |                |
   |            *   |
   |                |
   |     P         s|
   +----------------+
   [13.00 s] hearts 3/3
   +----------------+
   |     *         s|
   |    *           |
   |                |
   |      g         |
   |                |
   |           *    |
   |                |
   |                |
   |     P         s|
   +----------------+
   [13.50 s] hearts 3/3
   +----------------+
   |   **          s|
   |                |
   |                |
   |                |
   |      g  *      |
   |                |
   |                |
   |                |
   |     P         s|
   +----------------+
 13.600  a spitter takes aim
   [13.60 s] hearts 3/3
   +----------------+
   |    *         ~s|
   |             ~~ |
   |            ~~  |
   |           ~~   |
   |      g  *~     |
   |        ~~      |
   |       ~~       |
   |     ~~         |
   |    ~P         s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.79,+0.61) (0.60 s to the shot)
   [14.00 s] hearts 3/3
   +----------------+
   |  *           ~s|
   |             ~~ |
   |            ~~  |
   |        *  ~~   |
   |      g  ~~     |
   |        ~~      |
   |       ~~       |
   |     ~~         |
   |    ~~P        s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.79,+0.61) (0.20 s to the shot)
 14.200  a spitter spits
   [14.50 s] hearts 3/3
   +----------------+
   | *             s|
   |              * |
   |       *        |
   |                |
   |                |
   |      g         |
   |                |
   |                |
   |        P      s|
   +----------------+
 14.800  a spitter takes aim
   [14.80 s] hearts 3/3
   +----------------+
   |               s|
   |      *      *  |
   |                |
   |                |
   |                |
   |      g         |
   |                |
   |                |
   |~~~~~~~~~P~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [15.00 s] hearts 3/3
   +----------------+
   |               s|
   |      *         |
   |             *  |
   |                |
   |                |
   |       g        |
   |                |
   |                |
   |~~~~~~~~~P~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-1.00,+0.00) (0.40 s to the shot)
end at 15.00 s: hearts 3/3, enemies left 3
```

### Round 1: @run/play/room5-30 — `python3 play.py --view player {script}`

Script:

```text
room 5
fps 30
end 15
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 5 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   | g              |
   |                |
   |    G          s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |  g         ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |  g        ~~   |
   |        P~~     |
   |       ~~~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |        P       |
   |   g            |
   |                |
   |                |
   |  g             |
   |                |
   |     G          |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |        P      s|
   |   g     ~   *  |
   |         ~~     |
   |          ~~    |
   |           ~~   |
   |  g         ~~  |
   |             ~~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.66,-0.75) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |        P      s|
   |   g     ~   *  |
   |         ~~     |
   |          ~~    |
   |           ~~   |
   |  g         ~~  |
   |             ~~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.66,-0.75) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |    g           |
   |        P   *   |
   |                |
   |                |
   |   g            |
   |     G          |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g           |
   |          *     |
   |        P       |
   |   g            |
   |     G          |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |          *~    |
   |         ~~     |
   |   g   ~P       |
   |      G~        |
   |    ~~~       * |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.82,+0.57) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |     g     ~~~  |
   |         *~~    |
   |        P~~     |
   |    g  ~~       |
   |      G~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.82,+0.57) (0.20 s to the shot)
  4.200  a spitter spits
  4.333  YOU ARE HIT by a shot — hearts 2/3
   [4.33 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |     g          |
   |                |
   |        P       |
   |    g       *   |
   |      G         |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |               s|
   |              * |
   |     g          |
   |                |
   |        P       |
   |    g       *   |
   |      G         |
   |                |
   |               s|
   +----------------+
  4.800  a spitter takes aim
   [4.80 s] hearts 2/3
   +----------------+
   | ~~~           s|
   |   ~~        *  |
   |     g~         |
   |      ~~~       |
   |    g   P~ *    |
   |      G  ~~~    |
   |           ~~   |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.85,-0.52) (0.60 s to the shot)
  5.000  a grub rears back
   [5.00 s] hearts 2/3
   +----------------+
   | ~~~           s|
   |   ~~        *  |
   |     ~g         |
   |      ~~~  *    |
   |     g  ~~      |
   |      G~P~~~    |
   |           ~~   |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: G at (6.3,5.4) flashes orange-red, lunge line toward (+0.89,-0.45), 2.4 tiles (0.70 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.85,-0.52) (0.40 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |          * *   |
   |      g P       |
   |     g  ~       |
   |      G~~       |
   |                |
   |                |
   |               s|
   +----------------+
   cue: G at (6.3,5.4) flashes orange-red, lunge line toward (+0.89,-0.45), 2.4 tiles (0.20 s to the lunge)
   [6.00 s] hearts 2/3
   +----------------+
   |               s|
   |         *      |
   |       gP       |
   |          *     |
   |      g G       |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  6.033  a grub rears back
   [6.03 s] hearts 2/3
   +----------------+
   |               s|
   |         *      |
   |       g        |
   |        P~*     |
   |      g G       |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: g at (6.5,2.5) flashes orange-red, lunge line toward (+1.00,+0.05), 2.4 tiles (0.50 s to the lunge)
  6.167  you swipe: brute hit
   [6.50 s] hearts 2/3
   +----------------+
   |        *      s|
   |                |
   |       g        |
   |        P~      |
   |      g G*      |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
   cue: g at (6.5,2.5) flashes orange-red, lunge line toward (+1.00,+0.05), 2.4 tiles (0.03 s to the lunge)
  6.600  you swipe: grub hit
  6.833  a grub rears back
   [6.83 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |       ~Pg      |
   |      g~G       |
   |        *       |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: g at (6.3,3.7) flashes orange-red, lunge line toward (+0.97,-0.26), 2.4 tiles (0.50 s to the lunge)
  7.000  a spitter takes aim
   [7.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |          ~~~   |
   |       ~Pg      |
   |     ~g~G       |
   |   ~~~  *  *    |
   | ~~~            |
   |~               |
   |               s|
   +----------------+
   cue: g at (6.3,3.7) flashes orange-red, lunge line toward (+0.97,-0.26), 2.4 tiles (0.33 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.91,+0.41) (0.60 s to the shot)
  7.033  you swipe: grub hit, brute hit
  7.233  a grub rears back
   [7.23 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |          ~~~   |
   |       P~g      |
   |     ~g~G       |
   |   ~~~ *  *     |
   | ~~~            |
   |~               |
   |               s|
   +----------------+
   cue: G at (8.4,4.3) flashes orange-red, lunge line toward (-0.68,-0.73), 2.4 tiles (0.70 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 39%, aim line toward (-0.91,+0.41) (0.37 s to the shot)
  7.433  you swipe: grub defeated
   [7.50 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |          ~~~   |
   |       P~g      |
   |     ~~~G       |
   |   ~~~    *     |
   | ~~~   *        |
   |~               |
   |               s|
   +----------------+
   cue: G at (8.4,4.3) flashes orange-red, lunge line toward (-0.68,-0.73), 2.4 tiles (0.43 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 83%, aim line toward (-0.91,+0.41) (0.10 s to the shot)
  7.600  a spitter spits
  7.867  the brute shrugs off the swipe
  7.867  you swipe: brute hit
  8.000  YOU ARE HIT by a grub — hearts 1/3
   [8.00 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |         g      |
   |       PG       |
   |                |
   |                |
   |      *         |
   |               s|
   +----------------+
  8.033  a grub rears back
   [8.03 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |        ~g      |
   |       PG       |
   |                |
   |                |
   |     *          |
   |               s|
   +----------------+
   cue: g at (8.6,2.8) flashes orange-red, lunge line toward (-0.73,+0.68), 2.4 tiles (0.50 s to the lunge)
  8.400  a spitter takes aim
   [8.40 s] hearts 1/3
   +----------------+
   |~~             s|
   | ~~~         *  |
   |   ~~~          |
   |     ~~~~g      |
   |       PG       |
   |         ~~     |
   |           ~~   |
   |     *      ~~~ |
   |              ~s|
   +----------------+
   cue: g at (8.6,2.8) flashes orange-red, lunge line toward (-0.73,+0.68), 2.4 tiles (0.13 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.88,-0.48) (0.60 s to the shot)
  8.433  you swipe: brute defeated
   [8.50 s] hearts 1/3
   +----------------+
   |~~             s|
   | ~~~        *   |
   |   ~~~          |
   |     ~~~~g      |
   |       P~       |
   |         ~~     |
   |           ~~   |
   |    *       ~~~ |
   |              ~s|
   +----------------+
   cue: g at (8.6,2.8) flashes orange-red, lunge line toward (-0.73,+0.68), 2.4 tiles (0.03 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.88,-0.48) (0.50 s to the shot)
  8.933  you swipe: grub defeated
  9.000  a spitter spits
   [9.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |   *           s|
   +----------------+
   [9.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |          *     |
   |                |
   |       P        |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  9.600  a spitter takes aim
   [9.60 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |          ~~~   |
   |         *~     |
   |       P~       |
   |     ~~         |
   |   ~~~          |
   | ~~~         *  |
   |~~             s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.88,+0.47) (0.60 s to the shot)
   [10.00 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |          ~~~   |
   |        *~~     |
   |       ~~       |
   |     ~~         |
   |   ~~~ P        |
   | ~~~        *   |
   |~~             s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.88,+0.47) (0.20 s to the shot)
 10.200  a spitter spits
   [10.50 s] hearts 1/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |       *        |
   |                |
   |           *    |
   |                |
   |       P       s|
   +----------------+
   [11.00 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |      *         |
   |          *     |
   |                |
   |                |
   |       P       s|
   +----------------+
   [11.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |                |
   |        *       |
   |    *           |
   |                |
   |                |
   |       P       s|
   +----------------+
   [12.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |          *     |
   |       *        |
   |   *            |
   |                |
   |                |
   |       P       s|
   +----------------+
   [12.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |      *  *      |
   |                |
   |                |
   |  *             |
   |                |
   |       P       s|
   +----------------+
 12.600  a spitter takes aim
   [12.60 s] hearts 1/3
   +----------------+
   |               s|
   |              ~ |
   |             ~  |
   |     *   *  ~~  |
   |           ~~   |
   |          ~~    |
   |         ~~     |
   |        ~~      |
   |       P~      s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.69,+0.73) (0.60 s to the shot)
   [13.00 s] hearts 1/3
   +----------------+
   |               s|
   |              ~ |
   |    *        ~  |
   |            ~~  |
   |       *   ~~   |
   |          ~~    |
   |         ~~     |
   |        ~~      |
   |       ~~P     s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.69,+0.73) (0.20 s to the shot)
 13.200  a spitter spits
   [13.50 s] hearts 1/3
   +----------------+
   |               s|
   |   *          * |
   |                |
   |                |
   |                |
   |      *         |
   |                |
   |                |
   |           P   s|
   +----------------+
 14.000  a spitter takes aim
   [14.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |             *  |
   |                |
   |                |
   |     *          |
   |                |
   |                |
   |~~~~~~~~~~~~~P~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [14.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |            *   |
   |                |
   |                |
   |    *        P  |
   |                |
   |~~~~~~~~~~~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-1.00,+0.00) (0.10 s to the shot)
 14.600  a spitter spits
   [15.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |           * P  |
   |                |
   |                |
   |  *             |
   |              *s|
   +----------------+
end at 15.00 s: hearts 1/3, enemies left 2
```

### Round 1: @run/trace/grub-inreach-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 9.3 4
player 8 4
0.40 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.433 frame=13 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,stagger:0.367) | stagger {'enemy': 'grub'}; attack {'hits': [('grub', 'hit')]}
t=0.833 frame=25 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.333 frame=40 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.433 frame=43 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=60 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.233 stun_left=0.000 | grub(8.50,4.00,hp=1,recovery:0.233) | end
```

### Round 1: @run/trace/grub-late-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 9.3 4
player 8 4
0.60 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.633 frame=19 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | attack {'hits': [('grub', 'hit')]}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.433 frame=43 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.467 frame=44 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.967 frame=59 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.000 frame=60 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.23,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.000 frame=60 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.23,4.00,hp=1,recovery:0.800) | end
```

### Round 1: @run/trace/grub-outofreach-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 10 4
player 8 4
0.30 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.333 frame=10 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.200) | attack {'hits': []}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.733 frame=22 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.40,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.533 frame=46 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.40,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.567 frame=47 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.40,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.000 frame=60 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.40,4.00,hp=2,windup:0.067) | end
```

### Round 1: @run/trace/runner-inreach-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn runner 9.3 4
player 8 4
0.20 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.233 frame=7 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('runner', 'defeated')]}; cleared
t=1.233 frame=37 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/trace/runner-late-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn runner 9.3 4
player 8 4
0.43 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.400 frame=12 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,lunge:-0.017) | lunge {'enemy': 'runner'}
t=0.467 frame=14 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('runner', 'defeated')]}; cleared
t=1.467 frame=44 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/trace/runner-outofreach-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn runner 10 4
player 8 4
0.20 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.233 frame=7 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,windup:0.150) | attack {'hits': []}
t=0.400 frame=12 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,lunge:-0.017) | lunge {'enemy': 'runner'}
t=0.600 frame=18 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(8.40,4.00,hp=1,recovery:0.600) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.233 frame=37 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 | runner(8.40,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=1.400 frame=42 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.40,4.00,hp=1,windup:0.183) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.600 frame=48 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.40,4.00,hp=1,lunge:-0.017) | lunge {'enemy': 'runner'}
t=1.633 frame=49 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(8.13,4.00,hp=1,recovery:0.600) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.000 frame=60 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.433 stun_left=0.000 | runner(8.13,4.00,hp=1,recovery:0.233) | end
```

### Round 2: @run/play/room1-60 — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 60
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see g within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 1 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.017  a grub rears back
   [2.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |        ~       |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |        ~       |
   |     g  P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.02 s to the lunge)
  2.600  you swipe: grub hit
  2.700  YOU ARE HIT by a grub — hearts 2/3
   [2.70 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.883  a grub rears back
   [2.88 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |      g~P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (5.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |      g~P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (5.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.38 s to the lunge)
  3.050  you swipe: grub defeated
  3.467  you swipe: grub hit
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.567  YOU ARE HIT by a grub — hearts 1/3
   [3.57 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.917  you swipe: grub defeated
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.150  a grub rears back
   [5.15 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.9,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.9,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.15 s to the lunge)
  5.733  you swipe: grub hit
  5.833  YOU ARE HIT by a grub — hearts 0/3
  5.833  you went down
   [5.83 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 6.83 s: hearts 0/3, enemies left 1
```

### Round 2: @run/play/room2-60 — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 60
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see r within 3 then face
when see G within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 2 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  r             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               G|
   | r              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |              g |
   |   r            |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               G|
   |  r             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |   r            |
   |                |
   |        P       |
   |                |
   |                |
   |  r           G |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |    r           |
   |                |
   |        P       |
   |                |
   |                |
   |   r          G |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |     r          |
   |                |
   |        P       |
   |                |
   |    r         G |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |                |
   |      r         |
   |        P       |
   |                |
   |    r        G  |
   |                |
   |                |
   +----------------+
  2.967  a grub rears back
   [2.97 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r~        |
   |       ~P       |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,3.1) flashes orange-red, lunge line toward (+0.89,+0.45), 2.4 tiles (0.35 s to the lunge)
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r~        |
   |       ~P       |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,3.1) flashes orange-red, lunge line toward (+0.89,+0.45), 2.4 tiles (0.32 s to the lunge)
  3.383  you swipe: runner defeated
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |        P       |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
  3.967  a grub rears back
   [3.97 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |        ~       |
   |       ~P       |
   |      r~        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (6.4,4.7) flashes orange-red, lunge line toward (+0.80,-0.59), 2.4 tiles (0.35 s to the lunge)
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |        ~       |
   |       ~P       |
   |      r~        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (6.4,4.7) flashes orange-red, lunge line toward (+0.80,-0.59), 2.4 tiles (0.32 s to the lunge)
  4.383  you swipe: runner defeated
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
  5.067  a grub rears back
   [5.07 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        ~~g     |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: g at (9.7,2.7) flashes orange-red, lunge line toward (-0.86,+0.50), 2.4 tiles (0.50 s to the lunge)
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        ~~g     |
   |        ~       |
   |        P  G    |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.7,2.7) flashes orange-red, lunge line toward (-0.86,+0.50), 2.4 tiles (0.07 s to the lunge)
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |                |
   |           G    |
   |        P       |
   |                |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |                |
   |           G    |
   |                |
   |        P       |
   +----------------+
   [7.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |                |
   |           G    |
   |                |
   |        P       |
   +----------------+
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |          G     |
   |                |
   |        P       |
   +----------------+
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |          G     |
   |                |
   |        P       |
   +----------------+
   [8.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |          G     |
   |        P       |
   +----------------+
  8.833  a grub rears back
   [8.83 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |        ~ G     |
   |        P       |
   +----------------+
   cue: g at (7.8,6.0) flashes orange-red, lunge line toward (+0.09,+1.00), 2.4 tiles (0.50 s to the lunge)
   [9.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        g       |
   |        ~G      |
   |        P       |
   +----------------+
   cue: g at (7.8,6.0) flashes orange-red, lunge line toward (+0.09,+1.00), 2.4 tiles (0.33 s to the lunge)
  9.417  you swipe: grub hit
   [9.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        gG      |
   |        P       |
   +----------------+
  9.533  YOU ARE HIT by a grub — hearts 2/3
   [9.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |        P       |
   +----------------+
  9.550  a grub rears back
   [9.55 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |       ~P       |
   +----------------+
   cue: G at (9.2,7.0) flashes orange-red, lunge line toward (-0.85,+0.53), 2.4 tiles (0.70 s to the lunge)
  9.867  you swipe: grub defeated
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |       ~P       |
   +----------------+
   cue: G at (9.2,7.0) flashes orange-red, lunge line toward (-0.85,+0.53), 2.4 tiles (0.25 s to the lunge)
 10.317  you swipe: brute hit
 10.417  YOU ARE HIT by a grub — hearts 1/3
   [10.42 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [10.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
 10.767  you swipe: brute hit
   [11.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
 11.217  you swipe: brute hit
   [11.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
 11.633  a grub rears back
   [11.63 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       ~P       |
   +----------------+
   cue: G at (8.0,7.7) flashes orange-red, lunge line toward (-0.85,+0.53), 2.4 tiles (0.70 s to the lunge)
 11.667  you swipe: brute defeated
 11.683  room cleared
   [12.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [12.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
end at 12.68 s: hearts 1/3, enemies left 0
```

### Round 2: @run/play/room3-60 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 60
end 12
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when see s within 1.4 then attack
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
   |     ~~~P       |
   |       ~~~      |
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
   |       ~~       |
   |  s*    P~      |
   |         ~      |
   |          ~~    |
   |           ~~   |
   |            ~   |
   |             ~  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.70,-0.72) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |       ~~       |
   |  s     ~~      |
   |    *    ~      |
   |        P ~~    |
   |           ~~   |
   |            ~   |
   |             ~  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.70,-0.72) (0.10 s to the shot)
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
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |           ~~~  |
   |     *  P~~~    |
   |       ~~~      |
   |     ~~~        |
   |   ~~~       *  |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.45) (0.40 s to the shot)
  3.400  a spitter spits
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s     P       |
   |                |
   |       *        |
   |                |
   |            *   |
   |                |
   |  s           s |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |        *  *    |
   |                |
   |    *           |
   |  s           s |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |          *     |
   |                |
   |         *      |
   |     *          |
   |  s           s |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |         *      |
   |                |
   |                |
   |      *    *    |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s     *       |
   |                |
   |                |
   |        *       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
  5.667  YOU ARE HIT by a shot — hearts 2/3
   [5.67 s] hearts 2/3
   +----------------+
   |       P        |
   |  s             |
   |                |
   |                |
   |        *       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
  5.800  a spitter takes aim
  5.800  a spitter takes aim
  5.800  a spitter takes aim
   [5.80 s] hearts 2/3
   +----------------+
   |     ~~P~~~     |
   |  s~~~~~~~      |
   |      ~  ~~     |
   |     ~    ~~    |
   |    ~~  *  ~~   |
   |   ~~       ~   |
   |  ~~         *  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.98,-0.18) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.68,-0.73) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.62,-0.79) (0.60 s to the shot)
   [6.00 s] hearts 2/3
   +----------------+
   |     ~~P~~~     |
   |  s~~~~~~~      |
   |      ~  ~~     |
   |     ~   *~~    |
   |    ~~     ~~   |
   |   ~~       ~   |
   |  ~~         ~  |
   |  s          *s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.98,-0.18) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.68,-0.73) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.62,-0.79) (0.40 s to the shot)
  6.400  a spitter spits
  6.400  a spitter spits
  6.400  a spitter spits
   [6.50 s] hearts 2/3
   +----------------+
   |       P        |
   |  s             |
   |                |
   |          *     |
   |                |
   |                |
   |                |
   |  s           s*|
   |                |
   +----------------+
   [7.00 s] hearts 2/3
   +----------------+
   |       P        |
   |  s *           |
   |            *   |
   |                |
   |                |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |     * P        |
   |  s          *  |
   |                |
   |                |
   |    *           |
   |            *   |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.00 s] hearts 2/3
   +----------------+
   |       *        |
   |  s    P      * |
   |                |
   |     *     *    |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |        *       |
   |  s    P        |
   |      *   *     |
   |                |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   |          *     |
   |  s    * *      |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
   +----------------+
   |        *       |
   |  s             |
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |  s           s |
   |                |
   +----------------+
  9.800  a spitter takes aim
  9.800  a spitter takes aim
  9.800  a spitter takes aim
   [9.80 s] hearts 2/3
   +----------------+
   |       *        |
   |  s             |
   |   ~            |
   |    ~           |
   |    ~~          |
   |     ~~         |
   |~~~~~~~~~~~~~~~~|
   |  s~~~~P~~~~~~s |
   |        ~~      |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.67,+0.74) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.07) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+1.00,-0.09) (0.60 s to the shot)
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |   ~            |
   |    ~           |
   |    ~~          |
   |     ~~         |
   |~~~~~~~P~~~~~~~~|
   |  s~~~~~~~~~~~s |
   |        ~~      |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.67,+0.74) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-1.00,-0.07) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+1.00,-0.09) (0.40 s to the shot)
 10.400  a spitter spits
 10.400  a spitter spits
 10.400  a spitter spits
   [10.50 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [11.00 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |   *   P        |
   |                |
   |                |
   |                |
   |                |
   |  s *       * s |
   |                |
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |       P        |
   |  s             |
   |                |
   |    *           |
   |                |
   |                |
   |                |
   |  s  *     *  s |
   |                |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |       P        |
   |  s             |
   |                |
   |                |
   |                |
   |     *          |
   |                |
   |  s    * *    s |
   |                |
   +----------------+
end at 12.00 s: hearts 2/3, enemies left 3
```

### Round 2: @run/play/room4-60 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
end 15
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see r within 1.4 then attack
when see s within 1.4 then attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 4 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | r      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   |  r     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   r    P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   | g          ~~~ |
   |           ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g         ~~   |
   |        P~~     |
   |   r   ~~~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |        P       |
   |  g             |
   |                |
   |    r           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |        P      s|
   |  g      ~   *  |
   |         ~~     |
   |     r    ~~    |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.66,-0.75) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |        P      s|
   |  g      ~   *  |
   |         ~~     |
   |     r    ~~    |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.66,-0.75) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |   g            |
   |        P   *   |
   |     r          |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |      r    *    |
   |        P       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |   g       ~~~  |
   |      r   *~    |
   |         ~~     |
   |       ~P       |
   |      ~~        |
   |    ~~~       * |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.82,+0.57) (0.60 s to the shot)
  3.717  a grub rears back
   [3.72 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |      r~  *~    |
   |       ~ ~~     |
   |       ~P       |
   |      ~~      * |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: r at (6.4,3.2) flashes orange-red, lunge line toward (+0.58,+0.82), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 19%, aim line toward (-0.82,+0.57) (0.48 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |      r~ *~~    |
   |       ~ ~~     |
   |      P~~       |
   |      ~~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: r at (6.4,3.2) flashes orange-red, lunge line toward (+0.58,+0.82), 2.4 tiles (0.07 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.82,+0.57) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 3/3
   +----------------+
   |               s|
   |              * |
   |    g           |
   |                |
   |        *       |
   |    P   r   *   |
   |                |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |    g      *    |
   |                |
   |  P    *r       |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |          * *   |
   |   g            |
   |                |
   |P      r        |
   |     *          |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |               s|
   |         *      |
   |                |
   |   g       *    |
   |                |
   |P     r         |
   |    *           |
   |                |
   |               s|
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        *      s|
   |                |
   |                |
   |                |
   |   g     *      |
   |P    r          |
   |                |
   |   *            |
   |               s|
   +----------------+
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |              ~s|
   |          ~~~~  |
   |       ~~~~     |
   |    ~~~~        |
   | ~g~~    *      |
   |P~   r          |
   |                |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.95,+0.30) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |          ~~~~  |
   |       ~~~~     |
   |    ~~~~        |
   |P~g~~           |
   |~~   r  *       |
   |                |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.95,+0.30) (0.40 s to the shot)
  7.150  a grub rears back
   [7.15 s] hearts 3/3
   +----------------+
   |              ~s|
   |          ~~~~  |
   |       ~~~~     |
   |P   ~~~~        |
   | ~g~~           |
   |~~  r   *       |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (2.0,3.7) flashes orange-red, lunge line toward (-0.98,-0.17), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 58%, aim line toward (-0.95,+0.30) (0.25 s to the shot)
  7.400  a spitter spits
   [7.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |~               |
   | ~g             |
   |P   r           |
   |       *        |
   |                |
   |               s|
   +----------------+
   cue: g at (2.0,3.7) flashes orange-red, lunge line toward (-0.98,-0.17), 2.4 tiles (0.15 s to the lunge)
  8.000  a spitter takes aim
   [8.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |g               |
   |                |
   |   r            |
   |      *         |
   |P~~~~~~~~~      |
   |         ~~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.08) (0.60 s to the shot)
  8.333  a grub rears back
   [8.33 s] hearts 3/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |g               |
   |                |
   |   r            |
   |  ~             |
   |~P~~~*~~~~      |
   |         ~~~~~~s|
   +----------------+
   cue: r at (2.6,5.3) flashes orange-red, lunge line toward (-0.66,+0.76), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 56%, aim line toward (-1.00,-0.08) (0.27 s to the shot)
   [8.50 s] hearts 3/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |g               |
   |                |
   |   r            |
   |  ~             |
   |~~P~*~~~~~      |
   |         ~~~~~~s|
   +----------------+
   cue: r at (2.6,5.3) flashes orange-red, lunge line toward (-0.66,+0.76), 2.4 tiles (0.18 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-1.00,-0.08) (0.10 s to the shot)
  8.600  a spitter spits
  8.683  you swipe: runner defeated
   [9.00 s] hearts 3/3
   +----------------+
   |               s|
   |          *     |
   |                |
   |                |
   |g               |
   |                |
   |                |
   |   P            |
   |   *          *s|
   +----------------+
  9.200  a spitter takes aim
   [9.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |          *~~   |
   |         ~~~    |
   |g       ~~      |
   |      ~~~       |
   |     ~~         |
   |   ~P           |
   | ~~~         * s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.85,+0.53) (0.60 s to the shot)
   [9.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |         * ~~   |
   |         ~~~    |
   | g      ~~      |
   |      ~~~       |
   |    P~~         |
   |   ~~           |
   | ~~~        *  s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.85,+0.53) (0.30 s to the shot)
  9.800  a spitter spits
   [10.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |        *       |
   |                |
   | g  P           |
   |                |
   |                |
   |                |
   |           *   s|
   +----------------+
   [10.50 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |    P           |
   |      *         |
   |  g             |
   |                |
   |                |
   |                |
   |         *     s|
   +----------------+
   [11.00 s] hearts 3/3
   +----------------+
   |    P          s|
   |                |
   |            *   |
   |  g  *          |
   |                |
   |                |
   |                |
   |        *       |
   |               s|
   +----------------+
   [11.50 s] hearts 3/3
   +----------------+
   |    P          s|
   |                |
   |                |
   |  g        *    |
   |   *            |
   |                |
   |                |
   |      *         |
   |               s|
   +----------------+
   [12.00 s] hearts 3/3
   +----------------+
   |    P          s|
   |                |
   |                |
   |  g             |
   |  *      *      |
   |                |
   |                |
   |     *          |
   |               s|
   +----------------+
 12.400  a spitter takes aim
   [12.40 s] hearts 3/3
   +----------------+
   |~~~~P~~~~~~~~~~s|
   |                |
   |   g            |
   |                |
   |        *       |
   |                |
   |                |
   |    *           |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [12.50 s] hearts 3/3
   +----------------+
   |~~~~~P~~~~~~~~~s|
   |                |
   |   g            |
   |                |
   |        *       |
   |                |
   |                |
   |   *            |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-1.00,+0.00) (0.50 s to the shot)
 13.000  a spitter spits
   [13.00 s] hearts 3/3
   +----------------+
   |       P       s|
   |                |
   |   g            |
   |                |
   |                |
   |       *        |
   |                |
   |  *             |
   |               s|
   +----------------+
   [13.50 s] hearts 3/3
   +----------------+
   |         P   * s|
   |                |
   |    g           |
   |                |
   |                |
   |                |
   |      *         |
   |*               |
   |               s|
   +----------------+
 13.600  a spitter takes aim
   [13.60 s] hearts 3/3
   +----------------+
   |         P   * s|
   |         ~~     |
   |    g     ~~    |
   |           ~~   |
   |            ~   |
   |            ~~  |
   |     *       ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.60,-0.80) (0.60 s to the shot)
   [14.00 s] hearts 3/3
   +----------------+
   |         ~  *  s|
   |         ~~     |
   |    g    P~~    |
   |           ~~   |
   |            ~   |
   |            ~~  |
   |             ~~ |
   |    *         ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 67%, aim line toward (-0.60,-0.80) (0.20 s to the shot)
 14.200  a spitter spits
   [14.50 s] hearts 3/3
   +----------------+
   |          *    s|
   |                |
   |     g          |
   |                |
   |         P      |
   |                |
   |                |
   |   *          * |
   |               s|
   +----------------+
 14.800  a spitter takes aim
   [14.80 s] hearts 3/3
   +----------------+
   |          *   ~s|
   |             ~~ |
   |     g      ~~  |
   |           ~~   |
   |          ~~    |
   |        ~P      |
   |       ~~       |
   |      ~~      * |
   |    ~~         s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.78,+0.62) (0.60 s to the shot)
   [15.00 s] hearts 3/3
   +----------------+
   |         *    ~s|
   |             ~~ |
   |     g      ~~  |
   |           ~~   |
   |          ~~    |
   |        P~      |
   |       ~~     * |
   |      ~~        |
   |    ~~         s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.78,+0.62) (0.40 s to the shot)
end at 15.00 s: hearts 3/3, enemies left 3
```

### Round 2: @run/play/room5-60 — `python3 play.py --view player {script}`

Script:

```text
room 5
fps 60
end 15
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 5 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   | g              |
   |                |
   |    G          s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |  g         ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |  g        ~~   |
   |        P~~     |
   |       ~~~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |        P       |
   |   g            |
   |                |
   |                |
   |  g             |
   |                |
   |     G          |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |        P      s|
   |   g     ~   *  |
   |         ~~     |
   |          ~~    |
   |           ~~   |
   |  g         ~~  |
   |             ~~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.66,-0.75) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |        P      s|
   |   g     ~   *  |
   |         ~~     |
   |          ~~    |
   |           ~~   |
   |  g         ~~  |
   |             ~~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.66,-0.75) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |    g           |
   |        P   *   |
   |                |
   |                |
   |   g            |
   |     G          |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g           |
   |           *    |
   |        P       |
   |   g            |
   |     G          |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |          *~    |
   |         ~~     |
   |   g   ~P       |
   |      G~        |
   |    ~~~       * |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.82,+0.57) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |     g     ~~~  |
   |         *~~    |
   |        P~~     |
   |    g  ~~       |
   |      G~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.82,+0.57) (0.20 s to the shot)
  4.200  a spitter spits
  4.350  YOU ARE HIT by a shot — hearts 2/3
   [4.35 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |     g          |
   |                |
   |        P       |
   |    g       *   |
   |      G         |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |               s|
   |              * |
   |     g          |
   |                |
   |        P       |
   |    g       *   |
   |      G         |
   |                |
   |               s|
   +----------------+
  4.800  a spitter takes aim
   [4.80 s] hearts 2/3
   +----------------+
   |~~             s|
   |  ~~         *  |
   |   ~~g          |
   |     ~~~        |
   |    g  ~P~ *    |
   |         ~~     |
   |      G    ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.49) (0.60 s to the shot)
   [5.00 s] hearts 2/3
   +----------------+
   |~~             s|
   |  ~~         *  |
   |   ~~~g         |
   |     ~~~P  *    |
   |     g ~~~      |
   |      G  ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.87,-0.49) (0.40 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |        P       |
   |      g   * *   |
   |                |
   |     g          |
   |      G         |
   |                |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 2/3
   +----------------+
   |        P      s|
   |         *      |
   |      g         |
   |           *    |
   |     g          |
   |       G        |
   |                |
   |             *  |
   |               s|
   +----------------+
  6.217  a grub rears back
   [6.22 s] hearts 2/3
   +----------------+
   |       P~      s|
   |       ~ *      |
   |       g        |
   |          *     |
   |     g          |
   |       G        |
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: g at (6.5,1.9) flashes orange-red, lunge line toward (+0.45,-0.89), 2.4 tiles (0.50 s to the lunge)
  6.383  you swipe: grub hit
   [6.50 s] hearts 2/3
   +----------------+
   |        *      s|
   |       P        |
   |       g        |
   |      g         |
   |       G *      |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
  6.800  a grub rears back
   [6.80 s] hearts 2/3
   +----------------+
   |        ~      s|
   |       P~       |
   |       g        |
   |      g         |
   |       G *      |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: g at (6.5,1.9) flashes orange-red, lunge line toward (+0.64,-0.77), 2.4 tiles (0.50 s to the lunge)
  7.000  a spitter takes aim
   [7.00 s] hearts 2/3
   +----------------+
   |        ~  ~~~~s|
   |  ~~~~~~P~~~    |
   |~~~    g        |
   |      g         |
   |       G        |
   |        *       |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: g at (6.5,1.9) flashes orange-red, lunge line toward (+0.64,-0.77), 2.4 tiles (0.30 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.99,+0.12) (0.60 s to the shot)
   [7.50 s] hearts 2/3
   +----------------+
   |           ~~~~s|
   |  ~~~~~~g~~~    |
   |~~~             |
   |      g P       |
   |       G        |
   |         *      |
   |       *        |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 83%, aim line toward (-0.99,+0.12) (0.10 s to the shot)
  7.583  you swipe: brute hit
  7.600  a grub rears back
  7.600  a spitter spits
   [7.60 s] hearts 2/3
   +----------------+
   |        g      s|
   |                |
   |                |
   |      g~P~      |
   |       G        |
   |         *      |
   |       *        |
   |                |
   |               s|
   +----------------+
   cue: g at (6.5,2.8) flashes orange-red, lunge line toward (+0.98,+0.20), 2.4 tiles (0.50 s to the lunge)
   [8.00 s] hearts 2/3
   +----------------+
   |        g     *s|
   |                |
   |                |
   |      g~P~      |
   |       G*       |
   |                |
   |      *         |
   |                |
   |               s|
   +----------------+
   cue: g at (6.5,2.8) flashes orange-red, lunge line toward (+0.98,+0.20), 2.4 tiles (0.10 s to the lunge)
  8.033  you swipe: grub hit, brute hit
  8.050  a grub rears back
   [8.05 s] hearts 2/3
   +----------------+
   |        g     *s|
   |                |
   |        ~~      |
   |      gP~       |
   |       G*       |
   |                |
   |                |
   |     *          |
   |               s|
   +----------------+
   cue: G at (7.2,3.7) flashes orange-red, lunge line toward (+0.59,-0.81), 2.4 tiles (0.70 s to the lunge)
   [8.50 s] hearts 2/3
   +----------------+
   |        g   *  s|
   |                |
   |        ~~      |
   |       gP       |
   |       G        |
   |                |
   |                |
   |    *           |
   |               s|
   +----------------+
   cue: G at (7.2,3.7) flashes orange-red, lunge line toward (+0.59,-0.81), 2.4 tiles (0.25 s to the lunge)
  8.517  the brute shrugs off the swipe
  8.517  you swipe: grub defeated, brute hit
  8.783  YOU ARE HIT by a grub — hearts 1/3
   [8.78 s] hearts 1/3
   +----------------+
   |        g  *   s|
   |                |
   |                |
   |      *GP       |
   |                |
   |                |
   |                |
   |                |
   |    *          s|
   +----------------+
   [9.00 s] hearts 1/3
   +----------------+
   |           *   s|
   |        g       |
   |                |
   |      *GP       |
   |                |
   |                |
   |                |
   |                |
   |   *           s|
   +----------------+
  9.117  you swipe: brute defeated
  9.200  a spitter takes aim
   [9.20 s] hearts 1/3
   +----------------+
   |  ~~           s|
   |   ~~~  g *     |
   |     *~         |
   |       ~P       |
   |        ~~~     |
   |          ~~    |
   |           ~~   |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.84,-0.54) (0.60 s to the shot)
   [9.50 s] hearts 1/3
   +----------------+
   |  ~~           s|
   |   ~~~  g*      |
   |    *~~         |
   |       P~       |
   |        ~~~     |
   |          ~~    |
   |           ~~   |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 50%, aim line toward (-0.84,-0.54) (0.30 s to the shot)
  9.800  a spitter spits
   [10.00 s] hearts 1/3
   +----------------+
   |               s|
   |   *    g       |
   |                |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
 10.400  a spitter takes aim
   [10.40 s] hearts 1/3
   +----------------+
   |             ~~s|
   |       *  ~~~~  |
   |      ~g~~~     |
   |   P~~~         |
   |~~~             |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.96,+0.27) (0.60 s to the shot)
   [10.50 s] hearts 1/3
   +----------------+
   |             ~~s|
   |      *   ~~~~  |
   |      ~g~~~     |
   |   ~~~~         |
   |~~~P            |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-0.96,+0.27) (0.50 s to the shot)
 11.000  a spitter spits
   [11.00 s] hearts 1/3
   +----------------+
   |               s|
   |     *          |
   |       g        |
   |                |
   |                |
   |                |
   |   P        *   |
   |                |
   |               s|
   +----------------+
   [11.50 s] hearts 1/3
   +----------------+
   |              *s|
   |   *            |
   |      g         |
   |                |
   |                |
   |           *    |
   |                |
   |                |
   |   P           s|
   +----------------+
   [12.00 s] hearts 1/3
   +----------------+
   |               s|
   |            *   |
   |  *             |
   |      g         |
   |         *      |
   |                |
   |                |
   |                |
   |   P           s|
   +----------------+
   [12.50 s] hearts 1/3
   +----------------+
   |               s|
   |           *    |
   |*               |
   |      g         |
   |        *       |
   |                |
   |                |
   |                |
   |   P           s|
   +----------------+
 12.600  a spitter takes aim
   [12.60 s] hearts 1/3
   +----------------+
   |               s|
   |          *     |
   |                |
   |      g *       |
   |                |
   |                |
   |                |
   |                |
   |~~~P~~~~~~~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [13.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |         *      |
   |       *        |
   |      g         |
   |                |
   |                |
   |                |
   |~~~~~P~~~~~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
 13.200  a spitter spits
   [13.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |      * *       |
   |                |
   |      g         |
   |                |
   |                |
   |                |
   |       P      *s|
   +----------------+
   [14.00 s] hearts 1/3
   +----------------+
   |               s|
   |    *           |
   |      *         |
   |                |
   |                |
   |      g         |
   |                |
   |                |
   |         P   * s|
   +----------------+
   [14.50 s] hearts 1/3
   +----------------+
   |   *           s|
   |                |
   |                |
   |     *          |
   |                |
   |      g         |
   |                |
   |          P     |
   |           *   s|
   +----------------+
 14.800  a spitter takes aim
   [14.80 s] hearts 1/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |    *       ~~  |
   |           ~~   |
   |       g   ~    |
   |          ~     |
   |         P~     |
   |        ~~*    s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.63,+0.78) (0.60 s to the shot)
   [15.00 s] hearts 1/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |   *        ~~  |
   |           ~~   |
   |       g   ~    |
   |          ~     |
   |         P~     |
   |        ~~*    s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.63,+0.78) (0.40 s to the shot)
end at 15.00 s: hearts 1/3, enemies left 3
```

### Round 2: @run/trace/grub-inreach-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 9.3 4
player 8 4
0.40 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.417 frame=25 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,stagger:0.383) | stagger {'enemy': 'grub'}; attack {'hits': [('grub', 'hit')]}
t=0.817 frame=49 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.317 frame=79 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.417 frame=85 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=120 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.217 stun_left=0.000 | grub(8.50,4.00,hp=1,recovery:0.217) | end
```

### Round 2: @run/trace/grub-late-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 9.3 4
player 8 4
0.60 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.617 frame=37 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | attack {'hits': [('grub', 'hit')]}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.417 frame=85 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.433 frame=86 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.933 frame=116 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.950 frame=117 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.37,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.000 frame=120 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.750 stun_left=0.250 | grub(8.37,4.00,hp=1,recovery:0.750) | end
```

### Round 2: @run/trace/grub-outofreach-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
player 8 4
0.30 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.317 frame=19 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.200) | attack {'hits': []}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.700 frame=42 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.53,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.500 frame=90 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.53,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.517 frame=91 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.53,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.000 frame=120 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.53,4.00,hp=2,windup:0.017) | end
```

### Round 2: @run/trace/runner-inreach-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn runner 9.3 4
player 8 4
0.20 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.217 frame=13 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('runner', 'defeated')]}; cleared
t=1.217 frame=73 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/trace/runner-late-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn runner 9.3 4
player 8 4
0.43 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.367 frame=22 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.30,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'runner'}
t=0.450 frame=27 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('runner', 'defeated')]}; cleared
t=1.450 frame=87 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/trace/runner-outofreach-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn runner 10 4
player 8 4
0.20 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.217 frame=13 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,windup:0.150) | attack {'hits': []}
t=0.367 frame=22 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(10.00,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'runner'}
t=0.550 frame=33 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(8.53,4.00,hp=1,recovery:0.600) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.167 frame=70 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.183 stun_left=0.000 | runner(8.53,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=1.350 frame=81 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.53,4.00,hp=1,windup:0.167) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.517 frame=91 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.53,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'runner'}
t=1.533 frame=92 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(8.40,4.00,hp=1,recovery:0.600) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.000 frame=120 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | runner(8.40,4.00,hp=1,recovery:0.133) | end
```

### Round 2: @run/trace/grub-edge50-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 9.3 4
player 8 4
0.50 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,stagger:0.367) | stagger {'enemy': 'grub'}; attack {'hits': [('grub', 'hit')]}
t=0.933 frame=28 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.433 frame=43 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.533 frame=46 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=60 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | grub(8.50,4.00,hp=1,recovery:0.333) | end
```

### Round 2: @run/trace/grub-edge52-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 9.3 4
player 8 4
0.52 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.567 frame=17 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.03,4.00,hp=1,lunge:0.000) | attack {'hits': [('grub', 'hit')]}
t=0.633 frame=19 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.433 frame=43 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.467 frame=44 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.967 frame=59 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.000 frame=60 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.23,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.000 frame=60 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.23,4.00,hp=1,recovery:0.800) | end
```

### Round 2: @run/trace/grub-edge50-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 9.3 4
player 8 4
0.50 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,stagger:0.383) | stagger {'enemy': 'grub'}; attack {'hits': [('grub', 'hit')]}
t=0.917 frame=55 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.417 frame=85 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.517 frame=91 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=120 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.317 stun_left=0.000 | grub(8.50,4.00,hp=1,recovery:0.317) | end
```

### Round 2: @run/trace/grub-edge52-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 9.3 4
player 8 4
0.52 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.30,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.550 frame=33 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.03,4.00,hp=1,lunge:0.000) | attack {'hits': [('grub', 'hit')]}
t=0.617 frame=37 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.50,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.417 frame=85 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.433 frame=86 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=1.933 frame=116 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.50,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.950 frame=117 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.37,4.00,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.000 frame=120 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.750 stun_left=0.250 | grub(8.37,4.00,hp=1,recovery:0.750) | end
```

### Round 2: @run/trace/room1-reaction-30 — `python3 play.py --view trace {script}`

Script:

```text
room 1
fps 30
end 4
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see g within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=1 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.00,4.00,hp=2,approach:0.000) grub(15.00,4.00,hp=2,approach:0.000) grub(8.00,0.00,hp=2,approach:0.000) | setup
t=2.033 frame=61 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.03,4.00,hp=2,approach:0.000) grub(12.97,4.00,hp=2,approach:0.000) grub(8.00,2.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.533 frame=76 pos=(7.47,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.53,4.00,hp=2,approach:0.000) grub(12.47,4.00,hp=2,approach:0.000) grub(8.00,2.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.667 frame=80 pos=(7.47,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.67,4.00,hp=2,approach:0.000) grub(12.33,4.00,hp=2,approach:0.000) grub(8.00,3.07,hp=1,lunge:0.000) | attack {'hits': [('grub', 'hit')]}
t=2.767 frame=83 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.77,4.00,hp=2,approach:0.000) grub(12.23,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.800 frame=84 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 | grub(5.77,4.00,hp=2,windup:0.500) grub(12.20,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.767) | windup {'enemy': 'grub'}
t=2.833 frame=85 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | grub(5.77,4.00,hp=2,windup:0.467) grub(12.17,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.733) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=2.867 frame=86 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | grub(5.77,4.00,hp=2,windup:0.433) grub(12.13,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.700) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=2.900 frame=87 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | grub(5.77,4.00,hp=2,windup:0.400) grub(12.10,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.667) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}
t=3.033 frame=91 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.033 | grub(5.77,4.00,hp=2,windup:0.267) grub(11.97,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.533) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=3.067 frame=92 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.500 stun_left=0.000 | grub(5.77,4.00,hp=2,windup:0.233) grub(11.93,4.00,hp=2,approach:0.000) grub(8.00,3.87,hp=1,recovery:0.500) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}
t=3.200 frame=96 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 | grub(5.77,4.00,hp=2,windup:0.100) grub(11.80,4.00,hp=2,approach:0.000) | attack {'hits': [('grub', 'defeated')]}
t=3.300 frame=99 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.267 stun_left=0.000 | grub(5.77,4.00,hp=2,lunge:0.000) grub(11.70,4.00,hp=2,approach:0.000) | lunge {'enemy': 'grub'}
t=3.400 frame=102 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 | grub(6.57,4.00,hp=2,lunge:0.000) grub(11.60,4.00,hp=2,approach:0.000) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=3.567 frame=107 pos=(7.47,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.90,4.00,hp=1,lunge:0.000) grub(11.43,4.00,hp=2,approach:0.000) | attack {'hits': [('grub', 'hit')]}; invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.733 frame=112 pos=(7.47,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.17,4.00,hp=1,recovery:0.667) grub(11.27,4.00,hp=2,approach:0.000) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=3.900 frame=117 pos=(7.47,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.17,4.00,hp=1,recovery:0.500) grub(11.10,4.00,hp=2,approach:0.000) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=4.000 frame=120 pos=(7.47,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.17,4.00,hp=1,recovery:0.400) grub(11.00,4.00,hp=2,approach:0.000) | end
```

### Round 2: @run/trace/room1-reaction-60 — `python3 play.py --view trace {script}`

Script:

```text
room 1
fps 60
end 4
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see g within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=1 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.00,4.00,hp=2,approach:0.000) grub(15.00,4.00,hp=2,approach:0.000) grub(8.00,0.00,hp=2,approach:0.000) | setup
t=2.017 frame=121 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.02,4.00,hp=2,approach:0.000) grub(12.98,4.00,hp=2,approach:0.000) grub(8.00,2.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.517 frame=151 pos=(7.87,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.52,4.00,hp=2,approach:0.000) grub(12.48,4.00,hp=2,approach:0.000) grub(8.00,2.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.617 frame=157 pos=(7.87,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.62,4.00,hp=2,approach:0.000) grub(12.38,4.00,hp=2,approach:0.000) grub(8.00,2.80,hp=1,lunge:0.000) | attack {'hits': [('grub', 'hit')]}
t=2.700 frame=162 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.70,4.00,hp=2,approach:0.000) grub(12.30,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.767 frame=166 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | grub(5.77,4.00,hp=2,approach:0.000) grub(12.23,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.733) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=2.817 frame=169 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.683 stun_left=0.183 | grub(5.82,4.00,hp=2,approach:0.000) grub(12.18,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.683) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}
t=2.883 frame=173 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | grub(5.87,4.00,hp=2,windup:0.500) grub(12.12,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.617) | windup {'enemy': 'grub'}
t=2.900 frame=174 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.600 stun_left=0.100 | grub(5.87,4.00,hp=2,windup:0.483) grub(12.10,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.600) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=2.917 frame=175 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.583 stun_left=0.083 | grub(5.87,4.00,hp=2,windup:0.467) grub(12.08,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.583) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=2.967 frame=178 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.033 | grub(5.87,4.00,hp=2,windup:0.417) grub(12.03,4.00,hp=2,approach:0.000) grub(8.00,3.47,hp=1,recovery:0.533) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}
t=3.067 frame=184 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.433 stun_left=0.000 | grub(5.87,4.00,hp=2,windup:0.317) grub(11.93,4.00,hp=2,approach:0.000) | attack {'hits': [('grub', 'defeated')]}
t=3.383 frame=203 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.117 stun_left=0.000 | grub(5.87,4.00,hp=2,lunge:0.000) grub(11.62,4.00,hp=2,approach:0.000) | lunge {'enemy': 'grub'}
t=3.483 frame=209 pos=(7.87,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.017 stun_left=0.000 | grub(6.67,4.00,hp=1,lunge:0.000) grub(11.52,4.00,hp=2,approach:0.000) | attack {'hits': [('grub', 'hit')]}
t=3.500 frame=210 pos=(7.87,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.80,4.00,hp=1,lunge:0.000) grub(11.50,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.567 frame=214 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.33,4.00,hp=1,recovery:0.800) grub(11.43,4.00,hp=2,approach:0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.633 frame=218 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | grub(7.33,4.00,hp=1,recovery:0.733) grub(11.37,4.00,hp=2,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=3.717 frame=223 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.650 stun_left=0.150 | grub(7.33,4.00,hp=1,recovery:0.650) grub(11.28,4.00,hp=2,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}
t=3.783 frame=227 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.583 stun_left=0.083 | grub(7.33,4.00,hp=1,recovery:0.583) grub(11.22,4.00,hp=2,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=3.867 frame=232 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.500 stun_left=0.000 | grub(7.33,4.00,hp=1,recovery:0.500) grub(11.13,4.00,hp=2,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}
t=3.933 frame=236 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.433 stun_left=0.000 | grub(11.07,4.00,hp=2,approach:0.000) | attack {'hits': [('grub', 'defeated')]}
t=4.000 frame=240 pos=(7.87,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 | grub(11.00,4.00,hp=2,approach:0.000) | end
```
>>>END
