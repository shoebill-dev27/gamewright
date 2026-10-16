# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/41-studio-to-qa.md
next_seq: 43
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/43-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/41-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 41
from: studio
to: qa
stage: Verify
outcome: routed
---
# 41: studio → qa — Verify build 0.6 against criteria 1–21 at 30 and 60 FPS

## Task

Verify build 0.6 (`repo/`, sha 5eb065e08fef) independently, with `verify-change`. Check every acceptance criterion in the Design handoffs (35, 38) at both 30 and 60 FPS, including regressions in criteria 1–17 that passed for 0.5. Pay particular attention to the new and changed criteria: 18–21 and changed 3, 6, 8, 11, 13–16.

## Context

G-001 (combat monotony). Build 0.5 passed criteria 1–17 (handoff 24). Playtesting (27) and Diagnose (31) found that melee enemies share one answer and that the spitter crossfire in rooms 4–5 is unfair. Design (35, 38; D-004, D-005) specified build 0.6 to address both. Visual criteria V1–V11 wait for a graphical build and are out of scope here.

## Findings

Behavior the build should now show (from the spec; verify against the criteria text, not this summary):

- **Rooms 4–5, spitters.** The first spitter shots come at about 1.8 s and 3.0 s. A spitter cue never starts while another spitter's cue is running, or less than 0.6 s after the last shot in the room. Room 3 and practice rooms keep the 0.8 s offset and do not use the gap rule (room 3 first shots at 1.8, 2.6 and 3.4 s).
- **Brute.** A swipe that damages but does not kill a brute in wind-up does not cancel the wind-up; the lunge still comes. The grub and the runner are still cancelled. A kill in wind-up produces no lunge. The text view should show a message that the brute shrugs off the swipe (the trace shows a `shrug` event). Check that the player view (`run_play`) prints it; if it does not, report that as a defect of the player view.
- **Blocked contact (D-005).** A shot touching a player who is invulnerable (dashing, hit-stun or the hurt window) is consumed and does no damage, now or later. A lunge contact during invulnerability spends that lunge's hit: no damage for the rest of that lunge, the lunge is not shortened, and the next lunge damages normally.
- **Manual.** `repo/manual.md` (version 0.6) should describe the above in player terms and match the build.

How to exercise (project commands in `project.md`: `run_tests`, `run_play`, `run_trace`, `run_bots`):

- Practice room with a brute near the player and two swipes during its wind-up, at both frame rates.
- Rooms 4 and 5 for 15 s or more with a surviving player, at both rates: first shot times, gaps, overlaps.
- Room 3 for 15 s or more with a surviving player, in a real room trace (requested in the Design handoff 38): check for cap delay and simultaneous cue starts.
- A practice room with one spitter and a grub, for the hurt-window and dash scripts of criteria 20 and 21.
- `run_bots` for criteria 13–16: report the measured figures per room and rate, and your own verdict against the criteria as written. A figure over a limit is reported as a fail of that criterion; the question of whether the limit itself is right is being routed to Design in parallel, so do not adjust a limit yourself.

## Decisions already made

- D-001: one-button combat; no new input.
- D-002, D-003: per-frame contact sampling is kept; the contact-edge graze and the exact-reach rule are accepted.
- D-004: rooms 4–5 get a 0.6 s cue gap; the brute's wind-up is not cancelled by a swipe; the room 2 spitter is deferred.
- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Verify from the spec, the criteria and the build; do not rely on any explanation of why it should work.
- Do not change files other than your report.

## Open questions

- Does the player view print the brute's shrug message?
- What does a real-room trace of room 3 (15 s or more, surviving player) show for cap delay and simultaneous cue starts?

## Expected output

A verification report with a pass/fail verdict per criterion and per frame rate, the measured bot figures, reproduction steps for any failure, and answers to the open questions. Address it to `studio` (a fresh Play step follows and must be composed from permitted information only). Use `kind: handoff`, `from: qa`, `to: studio`, `outcome: pass | fail | question`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/38-game-designer-to-studio.md
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

<<<FILE decisions/D-002-contact-edge-graze-accepted.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-002: Per-frame contact sampling is kept; the contact-edge graze is an accepted limitation of the text build

## Decision

Contact (shot reach 0.4 tile, grub lunge reach 0.6 tile) stays a distance check once per frame after that frame's movement, with no swept test. At 30 and 60 FPS the hit or miss may differ only when the path's lateral miss lies in a narrow band just inside the reach: 0.39–0.40 tile for shots, 0.57–0.60 tile for lunges. Outside the band both rates must agree and follow the geometry. The band changes hit or miss only, never timing. The limitation is recorded in `design/combat.md` (Contact sampling rule, criterion 17, 16e).

## Rationale

- The band is tiny: about 0.003 tile for shots (QA, derived) and about 0.015 tile for lunges at 30 FPS (derived, not yet run). The player-sized sidestep margins are 0.3 tile or more, and the lane is 1.2 tiles wide. A player cannot see or aim at a difference of 0.003 tile.
- Both outcomes are "fair": the shot always visibly passes within about 0.4 tile of the player.
- A swept test would be a build change for no player-observable gain, against the project constraint of a small team that reuses existing systems.
- The damage a change could cause is larger than the effect: a new contact test would shift every hit time in the verified build 0.5.

## Alternatives considered

- Swept (continuous) contact test with a tolerance between 30 and 60 FPS: removes the band but changes a verified build, and has a cost with no visible benefit. Not chosen.
- Fixed sub-step contact at 120 Hz at both rates: same objection, and it only narrows the band.
- Widening the reach slightly so the case never sits in the band: moves the band, does not remove it, and changes tuning for every cue-based criterion.

## Revisit when

- A graphical build uses different hitboxes or a different contact test (re-verify criterion 17 at 30 and 60 FPS).
- A playtest reports "I dodged it and it still hit me" or the reverse, and the cause is the edge band.
- A lunge band wider than 0.03 tile is measured (QA's close-out run).
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

<<<FILE goals/G-001-combat-monotony/38-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 38
from: game-designer
to: studio
stage: Build
outcome: done
---
# 38: game-designer → studio — Rulings on blocked contact and simultaneous cue starts; complete change list for Build 0.6

## Task

Route the Build step for 0.6. The spec in `design/combat.md` (marked "step 38") is complete for Build: the step 35 items plus two rulings on QA's open items (handoff 36). No further design step is needed first.

## Context

G-001 (combat monotony). Step 35 specified the cue gap in rooms 4–5, the brute that is not cancelled by a swipe, and the manual wording (D-004). QA (handoff 36) found build 0.5 conforming to the 0.5 spec and reported two undefined behaviors. Both are ruled here. No scope or pillar change, no new input, no new enemy, no healing. Contact sampling (D-002, D-003) is unchanged.

## Findings

**Ruling 1 (QA item 1): a shot that touches an invulnerable player is consumed (D-005).**
- Rule: a shot with contact (distance <= 0.4, unchanged) on a player who cannot be hurt (dash, 0.3 s hit-stun, or hurt window until 0.8 s after the hit) disappears on that frame with no damage. It does not pass through and does not wait for the window to end.
- Lunges: a lunge has one hit; a contact on a protected player spends it. No damage from that lunge for the rest of it, even if the protection ends while the grub is still in reach. The lunge is not cancelled or shortened (existing rule). The next lunge damages normally.
- Why: QA saw damage land exactly at the end of the hurt window (4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS), 0.15–0.2 s after the shot visibly reached the player. That is a hidden hit, against "every threat is visible before it can hurt". The mechanism is QA's hypothesis, not confirmed in code; the rule holds regardless.
- Difficulty: only the chained hit on an already hurt player disappears, so rooms 4–5 get somewhat easier in that case. The intended cost (a still player takes each shot that arrives after the window) stays. Tuning values (offset, interval) are the lever if the rooms get too easy.
- Dash: a shot or lunge the dash overlaps cannot hit after the dash ends, so the dash is a more robust answer. It is not made necessary.
- Observable criterion for QA: criteria 20 (shots: hurt window, dash, normal hit, room 4 still-player trace, cap slots, band unchanged) and 21 (lunges: dash, hurt window, lunge not cancelled, next lunge normal). Numbers are in `design/combat.md`.

**Ruling 2 (QA item 2): a simultaneous cue start is accepted in room 3 and practice rooms; the gap rule is not extended (D-005).**
- Reasons: reproduced only in a practice replica with a surviving player, not in a real room; room 3's verified first shots (1.8, 2.6, 3.4 s) are unaffected either way; two simultaneous cues are two readable lines each answered by a sidestep or a dash; rooms 4–5 are covered by the rule.
- Criteria 11 and 18 do not change for room 3 and practice rooms. Criterion 18d must use room 4 or 5 (the practice room does not use the rule), or QA says d was not run. Revisit if a real-room trace of room 3 shows a problem.

**Bot expectations (questions 3 and 4).**
- Criterion 13 (walker 3–6 hearts, ≥2 of 3 cleared; dodger ≤ half, 3/3; camper fewer than walker): numbers kept. Two opposite effects on the walker in rooms 4–5: the brute lunge it used to cancel (step 35, more hearts) and the consumed shots (step 38, fewer hearts). Net unknown, and the walker's lower limit of 3 is now also at risk. Measured on 0.6; values outside limits are reported to `game-designer` as tuning, not as a build defect.
- Criterion 14 (grub rooms): numbers kept. Rooms 1–2 have no spitters; the lunge ruling can only lower hearts. The step 35 rule for the dodger's brute policy stands (sidestep or dash on the cue, swipe only in recovery); the Build step checks `bots.py`.
- Criterion 15 (dodger dashes ≥1 in rooms 3–5): numbers kept; the dash is safer, not required; a missing dash is reported, nothing is forced.
- Inconsistencies fixed in the spec: "two shots arriving together" now says the second is consumed; "dash invulnerability stops the damage" and "hurt invulnerability" now cover spent lunges; criterion 3 notes no later damage; criterion 16a/16e include 20 and 21 (and the band note); cap and edge-case notes added. Criteria 6, 11, 18 and 19 are unchanged in substance (11 and 18 only gain a note). Manual wording from step 35 is not made inconsistent; two lines are added below.

## Decisions already made

- D-001 (attack and dash only), D-002 and D-003 (contact sampling and exact reach; unchanged), D-004 (cue gap rule and offset in rooms 4–5, brute flag, Option 3 deferred; unchanged), D-005 (this step: consumed shots, spent lunge, simultaneous start accepted outside rooms 4–5).

## Constraints

- Correct at 30 and 60 FPS, all durations on accumulated time. Do not change contact detection (`distance <= reach` per frame after movement). Only the consequence after a detected contact changes.
- Room 3 criterion 11 stays (1.8, 2.6, 3.4 s ±1 frame). No new input, enemy, healing, room content or message beyond those listed.
- A spec step only: nothing was built or run. The bot numbers for 13–15 on 0.6 are unknown.

## Open questions

- Is a real-room cap delay reproducible in room 3, and is a simultaneous start a problem there? Needs a real-room trace of 15 s or more with a surviving player (a reaction-rule script as in the manual example). QA can do it in Verify.
- Do the walker's hearts in rooms 4–5 stay inside criterion 13 on 0.6 (the two effects pull in opposite directions)? Answered by the bots on 0.6.
- Is the "hidden hit" mechanism in 0.5 really an unconsumed shot, or something else with the same effect? Build confirms in code; criterion 20a confirms the result.

## Expected output

**Build 0.6** implements the full set below, then QA verifies it, then the bots run, then the hand-timed playtest.

Complete change list for Build 0.6:
1. (Step 35) Spitter offset per room: 0.8 s default (rooms 1–3, practice rooms), 1.2 s in rooms 4–5 (first shots 1.8 and 3.0 s in those rooms).
2. (Step 35) Cue gap rule in rooms 4–5 only: a spitter starts a cue only if no other spitter's cue is running, the last shot in the room was at least 0.6 s ago (1 ms tolerance), and the cap allows it; else wait 0.2 s and check again. A cancelled cue is not a shot. Room 3 and practice rooms do not use it.
3. (Step 35) Brute (`G`) wind-up is not cancelled by a swipe: the swipe deals 1 damage, shows "the brute shrugs off the swipe", the cue and timer continue, the lunge happens at 0.7 s. Kill in wind-up: no lunge, no message. Flag per variant: standard yes, runner yes, brute no.
4. (Step 35) Dodger bot policy against the brute: sidestep or dash on the cue, swipe in recovery only (check `bots.py`).
5. **(Step 38) Shot consumed on any contact:** a shot that makes contact with a player who is dashing, in hit-stun, or in hurt invulnerability is removed on that frame with no damage.
6. **(Step 38) Lunge hit spent:** a lunge that makes contact with a protected player deals no damage for the rest of that lunge; the lunge is not cancelled or shortened; the next lunge is normal.
7. (Step 38) No change to the cue gap rule for room 3, practice rooms, or to contact detection.
8. Manual (`repo/manual.md`), besides the step 35 lines: (a) "A shot that reaches you while you are dashing or still flashing after a hit is stopped and does no damage." (b) "A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection ends during that lunge." Also update the version number; the sentence "A swipe that interrupts a grub's warning staggers it for 0.4 s" needs the step 35 exception for the brute, as in the step 35 handoff.

New and changed criteria for QA: new 20 (a–f) and 21 (a–d); amended 3, 13, 14, 15, 16 (a and e), 11 and 18 (notes only). Existing 18 and 19 from step 35 stay. Scripts for 20–21 are practice-room scripts at `fps 30` and `fps 60`; the derived arrival time of the spitter at (15,4) to a player at (8,4) is about 4.0 s, to be taken from the trace.

For `art-director` (deferred with the other visual criteria until a graphical build exists): (1) step 35 brute hit reaction and the outdated "0.8 s apart" sentence; (2) step 38: a consumed shot should visibly end at the player (small flash or puff), not read as passing through. Nothing in the visual spec is blocked.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-game-designer.md
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
......................................................
----------------------------------------------------------------------
Ran 54 tests in 0.181s

OK
```

### Round 1: @run/play/brute30 — `python3 play.py --view player {script}`

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
Lantern Depths 0.5 — room empty — 30 FPS
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

### Round 1: @run/play/brute60 — `python3 play.py --view player {script}`

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
Lantern Depths 0.5 — room empty — 60 FPS
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

### Round 1: @run/trace/brute30 — `python3 play.py --view trace {script}`

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
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,windup:0.700) | windup {'enemy': 'brute'}
t=0.133 frame=4 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=3,windup:0.600) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,windup:0.200) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.733 frame=22 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'brute'}
t=0.800 frame=24 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(8.47,4.00,hp=2,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.600 frame=48 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=2,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.033 frame=61 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=2,windup:0.700) | windup {'enemy': 'brute'}
t=2.733 frame=82 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'brute'}
t=2.767 frame=83 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(8.20,4.00,hp=2,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.567 frame=107 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.20,4.00,hp=2,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=120 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.20,4.00,hp=2,windup:0.700) | windup {'enemy': 'brute'}
t=4.000 frame=120 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.20,4.00,hp=2,windup:0.700) | end
```

### Round 1: @run/trace/brute60 — `python3 play.py --view trace {script}`

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
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,windup:0.700) | windup {'enemy': 'brute'}
t=0.117 frame=7 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=3,windup:0.600) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,windup:0.200) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.717 frame=43 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,lunge:-0.000) | lunge {'enemy': 'brute'}
t=0.783 frame=47 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(8.47,4.00,hp=2,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.583 frame=95 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=2,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.000 frame=120 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=2,windup:0.700) | windup {'enemy': 'brute'}
t=2.700 frame=162 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=2,lunge:-0.000) | lunge {'enemy': 'brute'}
t=2.717 frame=163 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(8.33,4.00,hp=2,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.517 frame=211 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.33,4.00,hp=2,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.933 frame=236 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.33,4.00,hp=2,windup:0.700) | windup {'enemy': 'brute'}
t=4.000 frame=240 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.33,4.00,hp=2,windup:0.633) | end
```

### Round 1: @run/trace/room3-30 — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 30
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=3 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=3.400,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=1.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.200,cue=False) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.600,cue=False) | spit
t=2.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.200,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | aim
t=2.600 frame=78 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.600,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | spit
t=2.800 frame=84 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.200,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.400 frame=102 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.900 frame=117 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(2.00,1.00,hp=2,fire_in=0.700,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.100,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.900,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.000 frame=120 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=1.000,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.400 frame=132 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.200,cue=True) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | aim
t=4.600 frame=138 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.100 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.400,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.700 frame=141 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(2.00,1.00,hp=2,fire_in=2.300,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.300,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.100,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=5.000 frame=150 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.500 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.000,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | spit
t=5.500 frame=165 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(2.00,1.00,hp=2,fire_in=1.500,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=6.300 frame=189 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.500,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.500 frame=195 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.500,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | end
```

### Round 1: @run/trace/room3-60 — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 60
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=3 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=3.400,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=1.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.200,cue=False) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.600,cue=False) | spit
t=2.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.200,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | aim
t=2.600 frame=156 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.600,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | spit
t=2.800 frame=168 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.200,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.400 frame=204 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.900 frame=234 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(2.00,1.00,hp=2,fire_in=0.700,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.100,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.900,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.000 frame=240 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=1.000,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.400 frame=264 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.200,cue=True) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | aim
t=4.600 frame=276 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.100 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.400,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.700 frame=282 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(2.00,1.00,hp=2,fire_in=2.300,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.300,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.100,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=5.000 frame=300 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.500 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.000,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | spit
t=5.500 frame=330 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(2.00,1.00,hp=2,fire_in=1.500,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=6.300 frame=378 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.500,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.500 frame=390 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.500,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | end
```

### Round 1: @run/trace/room4-30 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 30
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=4 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(1.00,4.00,hp=1,approach:0.000) grub(0.00,1.00,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.92,4.00,hp=1,approach:0.000) grub(1.12,1.42,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.88,4.00,hp=1,approach:0.000) grub(1.69,1.63,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.84,4.00,hp=1,approach:0.000) grub(2.25,1.84,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=90 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.80,4.00,hp=1,approach:0.000) grub(2.81,2.05,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.167 frame=95 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.350) grub(2.97,2.11,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.033,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.233,cue=False) | windup {'enemy': 'runner'}
t=3.533 frame=106 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,lunge:-0.017) grub(3.31,2.24,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.867,cue=False) | lunge {'enemy': 'runner'}
t=3.600 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.55,4.00,hp=1,lunge:-0.017) grub(3.37,2.26,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=3.733 frame=112 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.61,4.00,hp=1,recovery:0.600) grub(3.50,2.31,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.467,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.667,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=4.200 frame=126 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | runner(7.61,4.00,hp=1,recovery:0.133) grub(3.93,2.47,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.367 frame=131 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.350) grub(4.09,2.53,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.233,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.033,cue=False) | windup {'enemy': 'runner'}
t=4.533 frame=136 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.183) grub(4.24,2.59,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.067,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.867,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.733 frame=142 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.61,4.00,hp=1,lunge:-0.017) grub(4.43,2.66,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.867,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | lunge {'enemy': 'runner'}
t=4.767 frame=143 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.88,4.00,hp=1,recovery:0.600) grub(4.46,2.67,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.833,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.800 frame=144 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 | runner(7.88,4.00,hp=1,recovery:0.567) grub(4.49,2.69,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=5.400 frame=162 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 | runner(7.88,4.00,hp=1,windup:0.350) grub(5.06,2.90,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | windup {'enemy': 'runner'}; spit
t=5.567 frame=167 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.88,4.00,hp=1,windup:0.183) grub(5.21,2.95,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.033,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.233,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.767 frame=173 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.88,4.00,hp=1,lunge:-0.017) grub(5.40,3.02,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.833,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.033,cue=False) | lunge {'enemy': 'runner'}
t=5.800 frame=174 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(8.15,4.00,hp=1,recovery:0.600) grub(5.43,3.04,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.000,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=6.600 frame=198 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.15,4.00,hp=1,recovery:0.600) grub(5.43,3.04,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.000,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.800 frame=204 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.15,4.00,hp=1,recovery:0.600) grub(5.43,3.04,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.000,cue=False) | end
```

### Round 1: @run/trace/room4-60 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 60
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=4 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(1.00,4.00,hp=1,approach:0.000) grub(0.00,1.00,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.92,4.00,hp=1,approach:0.000) grub(1.12,1.42,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.88,4.00,hp=1,approach:0.000) grub(1.69,1.63,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=144 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.84,4.00,hp=1,approach:0.000) grub(2.25,1.84,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=180 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.80,4.00,hp=1,approach:0.000) grub(2.81,2.05,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.150 frame=189 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.350) grub(2.95,2.11,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.250,cue=False) | windup {'enemy': 'runner'}
t=3.500 frame=210 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,lunge:0.000) grub(3.28,2.23,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.900,cue=False) | lunge {'enemy': 'runner'}
t=3.600 frame=216 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.81,4.00,hp=1,lunge:0.000) grub(3.37,2.26,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=3.683 frame=221 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.48,4.00,hp=1,recovery:0.600) grub(3.45,2.29,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.517,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.717,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=4.200 frame=252 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.283 stun_left=0.000 | runner(7.48,4.00,hp=1,recovery:0.083) grub(3.93,2.47,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.300 frame=258 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.183 stun_left=0.000 | runner(7.48,4.00,hp=1,windup:0.350) grub(4.03,2.51,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.300,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.100,cue=False) | windup {'enemy': 'runner'}
t=4.483 frame=269 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.48,4.00,hp=1,windup:0.167) grub(4.20,2.57,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.117,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.917,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.650 frame=279 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.48,4.00,hp=1,lunge:0.000) grub(4.35,2.63,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.950,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | lunge {'enemy': 'runner'}
t=4.667 frame=280 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.61,4.00,hp=1,recovery:0.600) grub(4.37,2.64,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.933,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.800 frame=288 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | runner(7.61,4.00,hp=1,recovery:0.467) grub(4.49,2.69,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=5.283 frame=317 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.183 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.350) grub(4.95,2.86,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.317,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.117,cue=True) | windup {'enemy': 'runner'}
t=5.400 frame=324 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.067 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.233) grub(5.06,2.90,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=5.467 frame=328 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.167) grub(5.12,2.92,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.133,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.333,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.550 frame=333 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.61,4.00,hp=1,windup:0.083) grub(5.20,2.95,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.250,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=6.350 frame=381 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.083) grub(5.20,2.95,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.250,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.550 frame=393 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.61,4.00,hp=1,windup:0.083) grub(5.20,2.95,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.250,cue=False) | end
```

### Round 1: @run/trace/room5-30 — `python3 play.py --view trace {script}`

Script:

```text
room 5
fps 30
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=5 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2,approach:0.000) grub(0.00,6.00,hp=2,approach:0.000) brute(4.00,8.00,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.10,1.47,hp=2,approach:0.000) grub(1.16,5.71,hp=2,approach:0.000) brute(4.59,7.41,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.65,1.71,hp=2,approach:0.000) grub(1.75,5.56,hp=2,approach:0.000) brute(4.89,7.11,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.21,1.95,hp=2,approach:0.000) grub(2.33,5.42,hp=2,approach:0.000) brute(5.19,6.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=90 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.76,2.18,hp=2,approach:0.000) grub(2.91,5.27,hp=2,approach:0.000) brute(5.48,6.52,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.31,2.42,hp=2,approach:0.000) grub(3.49,5.13,hp=2,approach:0.000) brute(5.78,6.22,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.200 frame=126 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.86,2.65,hp=2,approach:0.000) grub(4.07,4.98,hp=2,approach:0.000) brute(6.08,5.92,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.333 frame=130 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(4.98,2.71,hp=2,approach:0.000) grub(4.20,4.95,hp=2,approach:0.000) brute(6.14,5.86,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.067,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.800 frame=144 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | grub(5.41,2.89,hp=2,approach:0.000) grub(4.66,4.84,hp=2,approach:0.000) brute(6.38,5.62,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=5.133 frame=154 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.72,3.02,hp=2,approach:0.000) grub(4.98,4.75,hp=2,approach:0.000) brute(6.54,5.46,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.467,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.267,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.267 frame=158 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.84,3.07,hp=2,approach:0.000) grub(5.11,4.72,hp=2,approach:0.000) brute(6.59,5.41,hp=4,windup:0.700) spitter(15.00,0.00,hp=2,fire_in=1.333,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.133,cue=True) | windup {'enemy': 'brute'}
t=5.400 frame=162 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.96,3.13,hp=2,approach:0.000) grub(5.24,4.69,hp=2,approach:0.000) brute(6.59,5.41,hp=4,windup:0.567) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=5.533 frame=166 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.09,3.18,hp=2,approach:0.000) grub(5.37,4.66,hp=2,approach:0.000) brute(6.59,5.41,hp=4,windup:0.433) spitter(15.00,0.00,hp=2,fire_in=1.067,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.267,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=5.967 frame=179 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 | grub(6.48,3.35,hp=2,approach:0.000) grub(5.79,4.55,hp=2,approach:0.000) brute(6.59,5.41,hp=4,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.633,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.833,cue=False) | lunge {'enemy': 'brute'}
t=6.000 frame=180 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | grub(6.51,3.36,hp=2,approach:0.000) grub(5.82,4.54,hp=2,approach:0.000) brute(6.78,5.22,hp=4,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=6.300 frame=189 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 | grub(6.76,3.47,hp=2,windup:0.500) grub(6.11,4.47,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:1.167) spitter(15.00,0.00,hp=2,fire_in=0.300,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.500,cue=False) | windup {'enemy': 'grub'}
t=6.333 frame=190 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.76,3.47,hp=2,windup:0.467) grub(6.14,4.46,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:1.133) spitter(15.00,0.00,hp=2,fire_in=0.267,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.467,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.600 frame=198 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.76,3.47,hp=2,windup:0.200) grub(6.40,4.40,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.867) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=6.733 frame=202 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.76,3.47,hp=2,windup:0.067) grub(6.53,4.37,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.733) spitter(15.00,0.00,hp=2,fire_in=2.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.067,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=7.533 frame=226 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.76,3.47,hp=2,windup:0.067) grub(6.53,4.37,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.733) spitter(15.00,0.00,hp=2,fire_in=2.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.067,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.733 frame=232 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.76,3.47,hp=2,windup:0.067) grub(6.53,4.37,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.733) spitter(15.00,0.00,hp=2,fire_in=2.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.067,cue=False) | end
```

### Round 1: @run/trace/room5-60 — `python3 play.py --view trace {script}`

Script:

```text
room 5
fps 60
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2,approach:0.000) grub(0.00,6.00,hp=2,approach:0.000) brute(4.00,8.00,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.10,1.47,hp=2,approach:0.000) grub(1.16,5.71,hp=2,approach:0.000) brute(4.59,7.41,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.65,1.71,hp=2,approach:0.000) grub(1.75,5.56,hp=2,approach:0.000) brute(4.89,7.11,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=144 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.21,1.95,hp=2,approach:0.000) grub(2.33,5.42,hp=2,approach:0.000) brute(5.19,6.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=180 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.76,2.18,hp=2,approach:0.000) grub(2.91,5.27,hp=2,approach:0.000) brute(5.48,6.52,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.31,2.42,hp=2,approach:0.000) grub(3.49,5.13,hp=2,approach:0.000) brute(5.78,6.22,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.200 frame=252 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.86,2.65,hp=2,approach:0.000) grub(4.07,4.98,hp=2,approach:0.000) brute(6.08,5.92,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.350 frame=261 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.00,2.71,hp=2,approach:0.000) grub(4.22,4.94,hp=2,approach:0.000) brute(6.15,5.85,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.050,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.800 frame=288 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 | grub(5.41,2.89,hp=2,approach:0.000) grub(4.66,4.84,hp=2,approach:0.000) brute(6.38,5.62,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=5.150 frame=309 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.73,3.03,hp=2,approach:0.000) grub(5.00,4.75,hp=2,approach:0.000) brute(6.55,5.45,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.450,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.250,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.250 frame=315 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.83,3.07,hp=2,approach:0.000) grub(5.09,4.73,hp=2,approach:0.000) brute(6.59,5.41,hp=4,windup:0.700) spitter(15.00,0.00,hp=2,fire_in=1.350,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.150,cue=True) | windup {'enemy': 'brute'}
t=5.400 frame=324 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.96,3.13,hp=2,approach:0.000) grub(5.24,4.69,hp=2,approach:0.000) brute(6.59,5.41,hp=4,windup:0.550) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=5.550 frame=333 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.10,3.19,hp=2,approach:0.000) grub(5.38,4.65,hp=2,approach:0.000) brute(6.59,5.41,hp=4,windup:0.400) spitter(15.00,0.00,hp=2,fire_in=1.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.250,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=5.950 frame=357 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.400 stun_left=0.000 | grub(6.47,3.34,hp=2,approach:0.000) grub(5.77,4.56,hp=2,approach:0.000) brute(6.59,5.41,hp=4,lunge:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.650,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.850,cue=False) | lunge {'enemy': 'brute'}
t=6.000 frame=360 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 | grub(6.51,3.36,hp=2,approach:0.000) grub(5.82,4.54,hp=2,approach:0.000) brute(6.87,5.13,hp=4,lunge:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=6.267 frame=376 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.083 stun_left=0.000 | grub(6.74,3.46,hp=2,windup:0.500) grub(6.08,4.48,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:1.183) spitter(15.00,0.00,hp=2,fire_in=0.333,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.533,cue=False) | windup {'enemy': 'grub'}
t=6.350 frame=381 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.74,3.46,hp=2,windup:0.417) grub(6.16,4.46,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:1.100) spitter(15.00,0.00,hp=2,fire_in=0.250,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.450,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.600 frame=396 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.74,3.46,hp=2,windup:0.167) grub(6.40,4.40,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.850) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=6.750 frame=405 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.74,3.46,hp=2,windup:0.017) grub(6.55,4.36,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.700) spitter(15.00,0.00,hp=2,fire_in=2.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.050,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=7.550 frame=453 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.74,3.46,hp=2,windup:0.017) grub(6.55,4.36,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.700) spitter(15.00,0.00,hp=2,fire_in=2.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.050,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.750 frame=465 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.74,3.46,hp=2,windup:0.017) grub(6.55,4.36,hp=2,approach:0.000) brute(8.29,3.71,hp=4,recovery:0.700) spitter(15.00,0.00,hp=2,fire_in=2.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.050,cue=False) | end
```

### Round 1: @run/bots/fps30 — `python3 bots.py {script}`

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

### Round 1: @run/bots/fps60 — `python3 bots.py {script}`

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

### Round 2: @run/trace/room3s-30 — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 30
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=3 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=3.400,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=1.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.200,cue=False) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.600,cue=False) | spit
t=2.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.200,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | aim
t=2.600 frame=78 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.600,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | spit
t=2.800 frame=84 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.200,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.400 frame=102 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}; spit
t=3.633 frame=109 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.767,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.367,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.167,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.800 frame=204 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim; aim; aim
t=7.400 frame=222 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit; spit; spit
t=8.767 frame=263 pos=(8.00,0.53) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.033,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.033,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.033,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=9.000 frame=270 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.000 frame=330 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim; aim; aim
t=11.600 frame=348 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit; spit; spit
t=13.200 frame=396 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=13.433 frame=403 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.767,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.767,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.767,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=15.000 frame=450 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | end
```

### Round 2: @run/trace/room3s-60 — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 60
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=3 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=3.400,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=1.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.200,cue=False) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.600,cue=False) | spit
t=2.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.200,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | aim
t=2.600 frame=156 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.600,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | spit
t=2.800 frame=168 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.200,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.383 frame=203 pos=(8.00,3.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.817,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.617,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.017,cue=True) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=3.400 frame=204 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.617 frame=217 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.783,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.383,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.183,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.800 frame=408 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim; aim; aim
t=7.400 frame=444 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit; spit; spit
t=8.767 frame=526 pos=(8.00,0.27) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.033,cue=False) spitter(14.00,7.00,hp=2,fire_in=1.033,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.033,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=9.000 frame=540 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.000 frame=660 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(14.00,7.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim; aim; aim
t=11.600 frame=696 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(14.00,7.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit; spit; spit
t=13.183 frame=791 pos=(8.00,3.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.817,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.817,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.817,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=13.417 frame=805 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.783,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.783,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.783,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=15.000 frame=900 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(14.00,7.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | end
```

### Round 2: @run/trace/room4s-30 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 30
when text "rears back" then dash aside
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=4 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(1.00,4.00,hp=1,approach:0.000) grub(0.00,1.00,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.92,4.00,hp=1,approach:0.000) grub(1.12,1.42,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.88,4.00,hp=1,approach:0.000) grub(1.69,1.63,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.84,4.00,hp=1,approach:0.000) grub(2.25,1.84,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=90 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.80,4.00,hp=1,approach:0.000) grub(2.81,2.05,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.167 frame=95 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.350) grub(2.97,2.11,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.033,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.233,cue=False) | windup {'enemy': 'runner'}
t=3.200 frame=96 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.317) grub(3.00,2.12,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.000,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.200,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=3.433 frame=103 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.083) grub(3.22,2.09,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.967,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.533 frame=106 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,lunge:-0.017) grub(3.32,2.05,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.867,cue=False) | lunge {'enemy': 'runner'}
t=3.600 frame=108 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.55,4.00,hp=1,lunge:-0.017) grub(3.38,2.02,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.200 frame=126 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.41,4.00,hp=1,recovery:0.233) grub(3.93,1.78,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=5.733 frame=172 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,windup:0.350) grub(5.33,1.17,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.867,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | windup {'enemy': 'runner'}
t=5.767 frame=173 pos=(7.47,0.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,windup:0.317) grub(5.36,1.15,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.833,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=6.000 frame=180 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,windup:0.083) grub(5.35,0.97,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.100 frame=183 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,lunge:-0.017) grub(5.27,0.91,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | lunge {'enemy': 'runner'}
t=6.400 frame=192 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.600) grub(5.05,0.76,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | windup {'enemy': 'grub'}
t=6.433 frame=193 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.567) grub(5.05,0.76,hp=2,windup:0.467) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.800 frame=204 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.200) grub(5.05,0.76,hp=2,windup:0.100) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=6.900 frame=207 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.100) grub(5.05,0.76,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.500,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | lunge {'enemy': 'grub'}
t=7.000 frame=210 pos=(4.00,0.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.96,0.00,hp=1,approach:0.000) grub(4.40,0.29,hp=2,recovery:0.800) spitter(15.00,0.00,hp=2,fire_in=0.400,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=7.067 frame=212 pos=(4.00,0.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | runner(7.85,0.00,hp=1,approach:0.000) grub(4.40,0.29,hp=2,recovery:0.733) spitter(15.00,0.00,hp=2,fire_in=0.333,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=7.233 frame=217 pos=(4.00,0.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.567 stun_left=0.067 | runner(7.59,0.00,hp=1,approach:0.000) grub(4.40,0.29,hp=2,recovery:0.567) spitter(15.00,0.00,hp=2,fire_in=0.167,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=7.400 frame=222 pos=(4.00,0.53) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.400 stun_left=0.000 | runner(7.32,0.01,hp=1,approach:0.000) grub(4.40,0.29,hp=2,recovery:0.400) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | dash {'direction': 'down'}; spit
t=7.633 frame=229 pos=(4.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 | runner(7.03,0.23,hp=1,approach:0.000) grub(4.40,0.29,hp=2,recovery:0.167) spitter(15.00,0.00,hp=2,fire_in=2.167,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | dash_end
t=7.800 frame=234 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.86,0.44,hp=1,approach:0.000) grub(4.40,0.29,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.000,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=8.000 frame=240 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.66,0.69,hp=1,approach:0.000) grub(4.38,0.49,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=8.600 frame=258 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.06,1.44,hp=1,approach:0.000) grub(4.32,1.09,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=9.200 frame=276 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.46,2.18,hp=1,approach:0.000) grub(4.25,1.68,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=9.467 frame=284 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.48,hp=1,windup:0.350) grub(4.22,1.95,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.333,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.533,cue=False) | windup {'enemy': 'runner'}
t=9.500 frame=285 pos=(4.53,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.48,hp=1,windup:0.317) grub(4.23,1.98,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.300,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.500,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=9.733 frame=292 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.48,hp=1,windup:0.083) grub(4.40,2.13,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.067,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.267,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=9.800 frame=294 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.48,hp=1,windup:0.017) grub(4.45,2.16,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=9.833 frame=295 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.48,hp=1,lunge:-0.017) grub(4.48,2.18,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.367,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.167,cue=False) | lunge {'enemy': 'runner'}
t=10.767 frame=323 pos=(7.47,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | runner(3.77,4.34,hp=1,approach:0.000) grub(5.31,2.61,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.433,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=10.833 frame=325 pos=(6.40,4.00) hearts=2 invulnerable=True dash_left=0.150 hurt_left=0.000 stun_left=0.000 | runner(3.88,4.33,hp=1,approach:0.000) grub(5.34,2.63,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=1.367,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | windup {'enemy': 'grub'}
t=10.867 frame=326 pos=(5.87,4.00) hearts=2 invulnerable=True dash_left=0.117 hurt_left=0.000 stun_left=0.000 | runner(3.93,4.32,hp=1,approach:0.000) grub(5.34,2.63,hp=2,windup:0.467) spitter(15.00,0.00,hp=2,fire_in=1.333,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=11.000 frame=330 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,approach:0.000) grub(5.34,2.63,hp=2,windup:0.333) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.333 frame=340 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,approach:0.000) grub(5.34,2.63,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.867,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | lunge {'enemy': 'grub'}
t=11.667 frame=350 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,windup:0.350) grub(6.81,4.53,hp=2,recovery:0.767) spitter(15.00,0.00,hp=2,fire_in=0.733,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | windup {'enemy': 'runner'}
t=11.700 frame=351 pos=(4.53,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,windup:0.317) grub(6.81,4.53,hp=2,recovery:0.733) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=11.733 frame=352 pos=(5.07,4.00) hearts=2 invulnerable=True dash_left=0.183 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,windup:0.283) grub(6.81,4.53,hp=2,recovery:0.700) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=11.933 frame=358 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,windup:0.083) grub(6.81,4.53,hp=2,recovery:0.500) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.967 frame=359 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,windup:0.050) grub(6.81,4.53,hp=2,recovery:0.467) spitter(15.00,0.00,hp=2,fire_in=0.633,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.033 frame=361 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.04,4.29,hp=1,lunge:-0.017) grub(6.81,4.53,hp=2,recovery:0.400) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | lunge {'enemy': 'runner'}
t=12.133 frame=364 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.94,3.50,hp=1,lunge:-0.017) grub(6.81,4.53,hp=2,recovery:0.300) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.300 frame=369 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.78,2.17,hp=1,lunge:-0.017) grub(6.81,4.53,hp=2,recovery:0.133) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.400 frame=372 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.75,1.91,hp=1,recovery:0.533) grub(6.81,4.53,hp=2,recovery:0.033) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=12.467 frame=374 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.75,1.91,hp=1,recovery:0.467) grub(6.81,4.53,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=0.533,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | windup {'enemy': 'grub'}
t=12.500 frame=375 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.75,1.91,hp=1,recovery:0.433) grub(6.81,4.53,hp=2,windup:0.467) spitter(15.00,0.00,hp=2,fire_in=0.500,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.967 frame=389 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.79,1.93,hp=1,approach:0.000) grub(6.81,4.53,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.033,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | lunge {'enemy': 'grub'}
t=13.000 frame=390 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.84,1.95,hp=1,approach:0.000) grub(7.05,4.42,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=13.067 frame=392 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(3.94,2.00,hp=1,approach:0.000) grub(7.54,4.20,hp=2,recovery:0.800) spitter(15.00,0.00,hp=2,fire_in=2.333,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=13.600 frame=408 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.267 stun_left=0.000 | runner(4.70,2.38,hp=1,approach:0.000) grub(7.54,4.20,hp=2,recovery:0.267) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=13.867 frame=416 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.09,2.57,hp=1,approach:0.000) grub(7.54,4.20,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.533,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.333,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=13.900 frame=417 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.13,2.59,hp=1,approach:0.000) grub(7.54,4.20,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=1.500,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.300,cue=True) | windup {'enemy': 'grub'}
t=13.933 frame=418 pos=(8.00,3.47) hearts=1 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | runner(5.18,2.61,hp=1,approach:0.000) grub(7.54,4.20,hp=2,windup:0.467) spitter(15.00,0.00,hp=2,fire_in=1.467,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.267,cue=True) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=14.167 frame=425 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.51,2.47,hp=1,approach:0.000) grub(7.54,4.20,hp=2,windup:0.233) spitter(15.00,0.00,hp=2,fire_in=1.233,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.033,cue=True) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=14.200 frame=426 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.55,2.43,hp=1,approach:0.000) grub(7.54,4.20,hp=2,windup:0.200) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=14.400 frame=432 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.78,2.20,hp=1,approach:0.000) grub(7.54,4.20,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=1.000,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.200,cue=False) | lunge {'enemy': 'grub'}
t=14.800 frame=444 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.23,1.75,hp=1,approach:0.000) grub(9.74,3.23,hp=2,recovery:0.700) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=15.000 frame=450 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.46,1.53,hp=1,approach:0.000) grub(9.74,3.23,hp=2,recovery:0.500) spitter(15.00,0.00,hp=2,fire_in=0.400,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.600,cue=False) | end
```

### Round 2: @run/trace/room4s-60 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 60
when text "rears back" then dash aside
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=4 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(1.00,4.00,hp=1,approach:0.000) grub(0.00,1.00,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.92,4.00,hp=1,approach:0.000) grub(1.12,1.42,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.88,4.00,hp=1,approach:0.000) grub(1.69,1.63,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=144 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.84,4.00,hp=1,approach:0.000) grub(2.25,1.84,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=180 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.80,4.00,hp=1,approach:0.000) grub(2.81,2.05,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.150 frame=189 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.350) grub(2.95,2.11,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.250,cue=False) | windup {'enemy': 'runner'}
t=3.167 frame=190 pos=(8.00,3.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.333) grub(2.97,2.11,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.033,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.233,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=3.400 frame=204 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,windup:0.100) grub(3.19,2.09,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.000,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.500 frame=210 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.01,4.00,hp=1,lunge:0.000) grub(3.28,2.05,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.900,cue=False) | lunge {'enemy': 'runner'}
t=3.600 frame=216 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.81,4.00,hp=1,lunge:0.000) grub(3.38,2.01,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.200 frame=252 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.41,4.00,hp=1,recovery:0.200) grub(3.93,1.77,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=5.683 frame=341 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,windup:0.350) grub(5.29,1.18,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.917,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.717,cue=False) | windup {'enemy': 'runner'}
t=5.700 frame=342 pos=(7.73,0.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,windup:0.333) grub(5.30,1.17,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.900,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=5.933 frame=356 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,windup:0.100) grub(5.34,1.00,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.033 frame=362 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.21,1.98,hp=1,lunge:0.000) grub(5.26,0.94,hp=2,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | lunge {'enemy': 'runner'}
t=6.333 frame=380 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.600) grub(5.03,0.77,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | windup {'enemy': 'grub'}
t=6.350 frame=381 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.583) grub(5.03,0.77,hp=2,windup:0.483) spitter(15.00,0.00,hp=2,fire_in=0.650,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.800 frame=408 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.133) grub(5.03,0.77,hp=2,windup:0.033) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=6.833 frame=410 pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.96,0.00,hp=1,recovery:0.100) grub(5.03,0.77,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.567,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | lunge {'enemy': 'grub'}
t=6.933 frame=416 pos=(4.00,0.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(7.96,0.00,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,recovery:0.800) spitter(15.00,0.00,hp=2,fire_in=0.467,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=7.067 frame=424 pos=(4.00,0.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | runner(7.75,0.00,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,recovery:0.667) spitter(15.00,0.00,hp=2,fire_in=0.333,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=7.217 frame=433 pos=(4.00,0.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.517 stun_left=0.017 | runner(7.51,0.00,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,recovery:0.517) spitter(15.00,0.00,hp=2,fire_in=0.183,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.783,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=7.367 frame=442 pos=(4.00,0.27) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.367 stun_left=0.000 | runner(7.27,0.00,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,recovery:0.367) spitter(15.00,0.00,hp=2,fire_in=0.033,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | dash {'direction': 'down'}
t=7.400 frame=444 pos=(4.00,0.80) hearts=2 invulnerable=True dash_left=0.200 hurt_left=0.333 stun_left=0.000 | runner(7.21,0.01,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,recovery:0.333) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=7.600 frame=456 pos=(4.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | runner(6.96,0.20,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,recovery:0.133) spitter(15.00,0.00,hp=2,fire_in=2.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | dash_end
t=7.733 frame=464 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.83,0.37,hp=1,approach:-0.000) grub(4.39,0.29,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.067,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=8.000 frame=480 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(6.57,0.71,hp=1,approach:-0.000) grub(4.36,0.56,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=8.600 frame=516 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.98,1.46,hp=1,approach:-0.000) grub(4.30,1.15,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=9.200 frame=552 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.39,2.22,hp=1,approach:-0.000) grub(4.24,1.75,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=9.383 frame=563 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.43,hp=1,windup:0.350) grub(4.22,1.93,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.417,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.617,cue=False) | windup {'enemy': 'runner'}
t=9.400 frame=564 pos=(4.27,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.43,hp=1,windup:0.333) grub(4.22,1.95,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.400,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.600,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=9.633 frame=578 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.43,hp=1,windup:0.100) grub(4.37,2.11,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.167,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.367,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=9.733 frame=584 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.22,2.43,hp=1,lunge:0.000) grub(4.46,2.16,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.067,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.267,cue=False) | lunge {'enemy': 'runner'}
t=9.800 frame=588 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.90,2.85,hp=1,lunge:0.000) grub(4.51,2.19,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=10.767 frame=646 pos=(7.73,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | runner(3.96,4.31,hp=1,approach:-0.000) grub(5.37,2.64,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.433,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=10.833 frame=650 pos=(6.67,4.00) hearts=2 invulnerable=True dash_left=0.167 hurt_left=0.000 stun_left=0.000 | runner(4.07,4.30,hp=1,approach:-0.000) grub(5.41,2.67,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=1.367,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | windup {'enemy': 'grub'}
t=10.850 frame=651 pos=(6.40,4.00) hearts=2 invulnerable=True dash_left=0.150 hurt_left=0.000 stun_left=0.000 | runner(4.09,4.29,hp=1,approach:-0.000) grub(5.41,2.67,hp=2,windup:0.483) spitter(15.00,0.00,hp=2,fire_in=1.350,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=11.000 frame=660 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,approach:-0.000) grub(5.41,2.67,hp=2,windup:0.333) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.333 frame=680 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,approach:-0.000) grub(5.41,2.67,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.867,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | lunge {'enemy': 'grub'}
t=11.650 frame=699 pos=(4.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,windup:0.350) grub(7.06,4.41,hp=2,recovery:0.783) spitter(15.00,0.00,hp=2,fire_in=0.750,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | windup {'enemy': 'runner'}
t=11.667 frame=700 pos=(4.27,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,windup:0.333) grub(7.06,4.41,hp=2,recovery:0.767) spitter(15.00,0.00,hp=2,fire_in=0.733,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=11.700 frame=702 pos=(4.80,4.00) hearts=2 invulnerable=True dash_left=0.200 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,windup:0.300) grub(7.06,4.41,hp=2,recovery:0.733) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=11.900 frame=714 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,windup:0.100) grub(7.06,4.41,hp=2,recovery:0.533) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.967 frame=718 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,windup:0.033) grub(7.06,4.41,hp=2,recovery:0.467) spitter(15.00,0.00,hp=2,fire_in=0.633,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.000 frame=720 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.25,4.25,hp=1,lunge:0.000) grub(7.06,4.41,hp=2,recovery:0.433) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | lunge {'enemy': 'runner'}
t=12.117 frame=727 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.60,3.58,hp=1,lunge:0.000) grub(7.06,4.41,hp=2,recovery:0.317) spitter(15.00,0.00,hp=2,fire_in=0.683,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.683,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.267 frame=736 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.76,2.72,hp=1,lunge:0.000) grub(7.06,4.41,hp=2,recovery:0.167) spitter(15.00,0.00,hp=2,fire_in=0.733,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.400 frame=744 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.58,2.53,hp=1,recovery:0.500) grub(7.06,4.41,hp=2,recovery:0.033) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=12.417 frame=745 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.58,2.53,hp=1,recovery:0.483) grub(7.06,4.41,hp=2,recovery:0.017) spitter(15.00,0.00,hp=2,fire_in=0.583,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.783,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.450 frame=747 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.58,2.53,hp=1,recovery:0.450) grub(7.06,4.41,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=0.550,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | windup {'enemy': 'grub'}
t=12.467 frame=748 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.58,2.53,hp=1,recovery:0.433) grub(7.06,4.41,hp=2,windup:0.483) spitter(15.00,0.00,hp=2,fire_in=0.533,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.950 frame=777 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.65,2.55,hp=1,approach:-0.000) grub(7.06,4.41,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.050,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | lunge {'enemy': 'grub'}
t=13.000 frame=780 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.73,2.57,hp=1,approach:-0.000) grub(7.42,4.25,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=13.017 frame=781 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(2.76,2.58,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,recovery:0.800) spitter(15.00,0.00,hp=2,fire_in=2.383,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.783,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=13.600 frame=816 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.217 stun_left=0.000 | runner(3.66,2.82,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,recovery:0.217) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=13.817 frame=829 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(3.99,2.92,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.583,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.383,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=13.833 frame=830 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.02,2.92,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,windup:0.500) spitter(15.00,0.00,hp=2,fire_in=1.567,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.367,cue=True) | windup {'enemy': 'grub'}
t=13.850 frame=831 pos=(8.00,3.73) hearts=1 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | runner(4.04,2.93,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,windup:0.483) spitter(15.00,0.00,hp=2,fire_in=1.550,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.350,cue=True) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=14.083 frame=845 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.39,2.82,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,windup:0.250) spitter(15.00,0.00,hp=2,fire_in=1.317,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.117,cue=True) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=14.200 frame=852 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.54,2.71,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,windup:0.133) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=14.333 frame=860 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(4.71,2.58,hp=1,approach:-0.000) grub(7.55,4.20,hp=2,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=1.067,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.267,cue=False) | lunge {'enemy': 'grub'}
t=14.800 frame=888 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(5.29,2.12,hp=1,approach:-0.000) grub(9.74,3.23,hp=2,recovery:0.633) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue
[output cut at 20000 characters]
```

### Round 2: @run/trace/room5s-30 — `python3 play.py --view trace {script}`

Script:

```text
room 5
fps 30
when text "rears back" then dash aside
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=5 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2,approach:0.000) grub(0.00,6.00,hp=2,approach:0.000) brute(4.00,8.00,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.10,1.47,hp=2,approach:0.000) grub(1.16,5.71,hp=2,approach:0.000) brute(4.59,7.41,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.65,1.71,hp=2,approach:0.000) grub(1.75,5.56,hp=2,approach:0.000) brute(4.89,7.11,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.21,1.95,hp=2,approach:0.000) grub(2.33,5.42,hp=2,approach:0.000) brute(5.19,6.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=90 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.76,2.18,hp=2,approach:0.000) grub(2.91,5.27,hp=2,approach:0.000) brute(5.48,6.52,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.31,2.42,hp=2,approach:0.000) grub(3.49,5.13,hp=2,approach:0.000) brute(5.78,6.22,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=3.833 frame=115 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(4.52,2.51,hp=2,approach:0.000) grub(3.72,5.07,hp=2,approach:0.000) brute(5.90,6.10,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.367,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.567,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=4.067 frame=122 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.74,2.44,hp=2,approach:0.000) grub(3.89,4.92,hp=2,approach:0.000) brute(5.96,5.95,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.133,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.333,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=4.200 frame=126 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.85,2.36,hp=2,approach:0.000) grub(3.98,4.82,hp=2,approach:0.000) brute(5.99,5.86,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=6.200 frame=186 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.42,1.18,hp=2,windup:0.500) grub(5.26,3.28,hp=2,approach:0.000) brute(6.45,4.54,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | windup {'enemy': 'grub'}
t=6.233 frame=187 pos=(8.00,0.53) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(6.42,1.18,hp=2,windup:0.467) grub(5.29,3.26,hp=2,approach:0.000) brute(6.46,4.52,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=6.367 frame=191 pos=(8.00,2.67) hearts=3 invulnerable=True dash_left=0.083 hurt_left=0.000 stun_left=0.000 | grub(6.42,1.18,hp=2,windup:0.333) grub(5.40,3.20,hp=2,approach:0.000) brute(6.50,4.44,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.633,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.467 frame=194 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.42,1.18,hp=2,windup:0.233) grub(5.50,3.22,hp=2,approach:0.000) brute(6.57,4.41,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.733,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.533 frame=196 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.42,1.18,hp=2,windup:0.167) grub(5.56,3.24,hp=2,approach:0.000) brute(6.61,4.40,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.700 frame=201 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.42,1.18,hp=2,lunge:0.000) grub(5.72,3.29,hp=2,approach:0.000) brute(6.72,4.36,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}; lunge {'enemy': 'grub'}
t=6.733 frame=202 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.63,1.02,hp=2,lunge:0.000) grub(5.76,3.30,hp=2,approach:0.000) brute(6.74,4.36,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.667,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=6.800 frame=204 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | grub(7.06,0.70,hp=2,lunge:0.000) grub(5.82,3.32,hp=2,approach:0.000) brute(6.79,4.34,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=7.000 frame=210 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.033 | grub(8.34,0.00,hp=2,recovery:0.800) grub(6.01,3.38,hp=2,approach:0.000) brute(6.90,4.31,hp=4,windup:0.700) spitter(15.00,0.00,hp=2,fire_in=0.400,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | windup {'enemy': 'brute'}
t=7.033 frame=211 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.500 stun_left=0.000 | grub(8.34,0.00,hp=2,recovery:0.767) grub(6.04,3.39,hp=2,approach:0.000) brute(6.90,4.31,hp=4,windup:0.667) spitter(15.00,0.00,hp=2,fire_in=0.367,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=7.400 frame=222 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | grub(8.34,0.00,hp=2,recovery:0.400) grub(6.39,3.50,hp=2,approach:0.000) brute(6.90,4.31,hp=4,windup:0.300) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=7.533 frame=226 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.34,0.00,hp=2,recovery:0.267) grub(6.52,3.54,hp=2,approach:0.000) brute(6.90,4.31,hp=4,windup:0.167) spitter(15.00,0.00,hp=2,fire_in=2.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.700 frame=231 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.34,0.00,hp=2,recovery:0.100) grub(6.68,3.59,hp=2,approach:0.000) brute(6.90,4.31,hp=4,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=2.100,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | lunge {'enemy': 'brute'}
t=7.800 frame=234 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.34,0.00,hp=2,approach:0.000) grub(6.77,3.62,hp=2,approach:0.000) brute(7.67,4.09,hp=4,recovery:1.200) spitter(15.00,0.00,hp=2,fire_in=2.000,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=7.833 frame=235 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 | grub(8.34,0.03,hp=2,approach:0.000) grub(6.77,3.62,hp=2,windup:0.500) brute(7.67,4.09,hp=4,recovery:1.167) spitter(15.00,0.00,hp=2,fire_in=1.967,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | windup {'enemy': 'grub'}
t=7.867 frame=236 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | grub(8.34,0.07,hp=2,approach:0.000) grub(6.77,3.62,hp=2,windup:0.467) brute(7.67,4.09,hp=4,recovery:1.133) spitter(15.00,0.00,hp=2,fire_in=1.933,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=8.000 frame=240 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.600 stun_left=0.100 | grub(8.33,0.20,hp=2,approach:0.000) grub(6.77,3.62,hp=2,windup:0.333) brute(7.67,4.09,hp=4,recovery:1.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=8.333 frame=250 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.267 stun_left=0.000 | grub(8.30,0.53,hp=2,approach:0.000) grub(6.77,3.62,hp=2,lunge:0.000) brute(7.67,4.09,hp=4,recovery:0.667) spitter(15.00,0.00,hp=2,fire_in=1.467,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.267,cue=True) | lunge {'enemy': 'grub'}
t=8.600 frame=258 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.27,0.80,hp=2,approach:0.000) grub(8.81,4.25,hp=2,lunge:0.000) brute(7.67,4.09,hp=4,recovery:0.400) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}; spit
t=9.033 frame=271 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.24,1.23,hp=2,approach:0.000) grub(9.06,4.33,hp=2,recovery:0.400) brute(7.67,4.09,hp=4,windup:0.700) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.967,cue=False) | windup {'enemy': 'brute'}
t=9.067 frame=272 pos=(8.00,3.47) hearts=1 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(8.23,1.26,hp=2,approach:0.000) grub(9.06,4.33,hp=2,recovery:0.367) brute(7.67,4.09,hp=4,windup:0.667) spitter(15.00,0.00,hp=2,fire_in=0.733,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.933,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=9.200 frame=276 pos=(8.00,1.33) hearts=1 invulnerable=True dash_left=0.083 hurt_left=0.000 stun_left=0.000 | grub(8.21,1.36,hp=2,approach:0.000) grub(9.06,4.33,hp=2,recovery:0.233) brute(7.67,4.09,hp=4,windup:0.533) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=9.300 frame=279 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.19,1.26,hp=2,approach:0.000) grub(9.06,4.33,hp=2,recovery:0.133) brute(7.67,4.09,hp=4,windup:0.433) spitter(15.00,0.00,hp=2,fire_in=0.500,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.700,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=9.733 frame=292 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.12,0.83,hp=2,approach:0.000) grub(8.99,4.04,hp=2,approach:0.000) brute(7.67,4.09,hp=4,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=0.067,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.267,cue=False) | lunge {'enemy': 'brute'}
t=9.800 frame=294 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.11,0.77,hp=2,approach:0.000) grub(8.98,3.98,hp=2,approach:0.000) brute(8.18,3.95,hp=4,lunge:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=10.067 frame=302 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.54,hp=2,windup:0.500) grub(8.91,3.72,hp=2,approach:0.000) brute(9.98,3.44,hp=4,recovery:1.167) spitter(15.00,0.00,hp=2,fire_in=2.133,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.933,cue=False) | windup {'enemy': 'grub'}
t=10.100 frame=303 pos=(7.47,0.00) hearts=1 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.54,hp=2,windup:0.467) grub(8.90,3.69,hp=2,approach:0.000) brute(9.98,3.44,hp=4,recovery:1.133) spitter(15.00,0.00,hp=2,fire_in=2.100,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.900,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=10.333 frame=310 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.54,hp=2,windup:0.233) grub(8.74,3.52,hp=2,approach:0.000) brute(9.98,3.44,hp=4,recovery:0.900) spitter(15.00,0.00,hp=2,fire_in=1.867,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=10.567 frame=317 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.54,hp=2,lunge:0.000) grub(8.56,3.38,hp=2,approach:0.000) brute(9.98,3.44,hp=4,recovery:0.667) spitter(15.00,0.00,hp=2,fire_in=1.633,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | lunge {'enemy': 'grub'}
t=12.400 frame=372 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.99,0.00,hp=2,approach:0.000) grub(7.08,2.29,hp=2,approach:0.000) brute(9.27,3.03,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=12.667 frame=380 pos=(4.53,0.00) hearts=1 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(6.73,0.00,hp=2,approach:0.000) grub(6.87,2.13,hp=2,approach:0.000) brute(9.11,2.94,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.333,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=12.700 frame=381 pos=(5.07,0.00) hearts=1 invulnerable=True dash_left=0.183 hurt_left=0.000 stun_left=0.000 | grub(6.73,0.00,hp=2,windup:0.500) grub(6.85,2.10,hp=2,approach:0.000) brute(9.09,2.92,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.300,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | windup {'enemy': 'grub'}
t=12.733 frame=382 pos=(5.60,0.00) hearts=1 invulnerable=True dash_left=0.150 hurt_left=0.000 stun_left=0.000 | grub(6.73,0.00,hp=2,windup:0.467) grub(6.83,2.07,hp=2,approach:0.000) brute(9.07,2.91,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.267,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.900 frame=387 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.73,0.00,hp=2,windup:0.300) grub(6.86,1.92,hp=2,approach:0.000) brute(9.01,2.81,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.100,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=13.000 frame=390 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.73,0.00,hp=2,windup:0.200) grub(6.91,1.83,hp=2,approach:0.000) brute(8.99,2.74,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=13.200 frame=396 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.73,0.00,hp=2,lunge:0.000) grub(7.01,1.66,hp=2,approach:0.000) brute(8.94,2.61,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | lunge {'enemy': 'grub'}
t=13.500 frame=405 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.33,0.00,hp=2,recovery:0.800) grub(7.15,1.43,hp=2,windup:0.500) brute(8.87,2.42,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.900,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | windup {'enemy': 'grub'}
t=13.533 frame=406 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.33,0.00,hp=2,recovery:0.767) grub(7.15,1.43,hp=2,windup:0.467) brute(8.86,2.39,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.867,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.667,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=13.600 frame=408 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.33,0.00,hp=2,recovery:0.700) grub(7.15,1.43,hp=2,windup:0.400) brute(8.85,2.35,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=14.000 frame=420 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.33,0.00,hp=2,recovery:0.300) grub(7.15,1.43,hp=2,lunge:0.000) brute(8.75,2.09,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.200,cue=True) | lunge {'enemy': 'grub'}
t=14.133 frame=424 pos=(8.00,0.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(4.33,0.00,hp=2,recovery:0.167) grub(7.69,0.51,hp=2,recovery:0.800) brute(8.72,2.00,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.067,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=14.933 frame=448 pos=(8.00,0.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.33,0.00,hp=2,recovery:0.167) grub(7.69,0.51,hp=2,recovery:0.800) brute(8.72,2.00,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.067,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=15.000 frame=450 pos=(8.00,0.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.33,0.00,hp=2,recovery:0.167) grub(7.69,0.51,hp=2,recovery:0.800) brute(8.72,2.00,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.267,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.067,cue=True) | end
```

### Round 2: @run/trace/room5s-60 — `python3 play.py --view trace {script}`

Script:

```text
room 5
fps 60
when text "rears back" then dash aside
when see * coming within 2 then dash aside
end 15
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2,approach:0.000) grub(0.00,6.00,hp=2,approach:0.000) brute(4.00,8.00,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.10,1.47,hp=2,approach:0.000) grub(1.16,5.71,hp=2,approach:0.000) brute(4.59,7.41,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.65,1.71,hp=2,approach:0.000) grub(1.75,5.56,hp=2,approach:0.000) brute(4.89,7.11,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=144 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.21,1.95,hp=2,approach:0.000) grub(2.33,5.42,hp=2,approach:0.000) brute(5.19,6.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=180 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.76,2.18,hp=2,approach:0.000) grub(2.91,5.27,hp=2,approach:0.000) brute(5.48,6.52,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.31,2.42,hp=2,approach:0.000) grub(3.49,5.13,hp=2,approach:0.000) brute(5.78,6.22,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=3.833 frame=230 pos=(8.00,3.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(4.52,2.51,hp=2,approach:0.000) grub(3.72,5.07,hp=2,approach:0.000) brute(5.90,6.10,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.367,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.567,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=4.067 frame=244 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.74,2.46,hp=2,approach:0.000) grub(3.90,4.93,hp=2,approach:0.000) brute(5.97,5.96,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.133,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.333,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=4.200 frame=252 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.85,2.38,hp=2,approach:0.000) grub(3.99,4.83,hp=2,approach:0.000) brute(6.00,5.87,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=6.167 frame=370 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,windup:0.500) grub(5.24,3.32,hp=2,approach:0.000) brute(6.44,4.57,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.633,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | windup {'enemy': 'grub'}
t=6.183 frame=371 pos=(8.00,0.27) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,windup:0.483) grub(5.26,3.30,hp=2,approach:0.000) brute(6.45,4.55,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.617,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.617,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=6.300 frame=378 pos=(8.00,2.13) hearts=3 invulnerable=True dash_left=0.117 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,windup:0.367) grub(5.35,3.24,hp=2,approach:0.000) brute(6.48,4.48,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.417 frame=385 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,windup:0.250) grub(5.47,3.24,hp=2,approach:0.000) brute(6.55,4.43,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.783,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.783,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.450 frame=387 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,windup:0.217) grub(5.50,3.25,hp=2,approach:0.000) brute(6.57,4.43,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.750,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.600 frame=396 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,windup:0.067) grub(5.64,3.29,hp=2,approach:0.000) brute(6.67,4.40,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=6.667 frame=400 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.40,1.21,hp=2,lunge:0.000) grub(5.70,3.31,hp=2,approach:0.000) brute(6.71,4.38,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.733,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | lunge {'enemy': 'grub'}
t=6.750 frame=405 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.94,0.80,hp=2,lunge:0.000) grub(5.78,3.33,hp=2,approach:0.000) brute(6.77,4.37,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.650,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=6.800 frame=408 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.750 stun_left=0.250 | grub(7.26,0.56,hp=2,lunge:0.000) grub(5.83,3.35,hp=2,approach:0.000) brute(6.80,4.36,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=6.967 frame=418 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.583 stun_left=0.083 | grub(8.32,0.00,hp=2,recovery:0.800) grub(5.99,3.39,hp=2,approach:0.000) brute(6.90,4.33,hp=4,windup:0.700) spitter(15.00,0.00,hp=2,fire_in=0.433,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | windup {'enemy': 'brute'}
t=6.983 frame=419 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.567 stun_left=0.067 | grub(8.32,0.00,hp=2,recovery:0.783) grub(6.01,3.40,hp=2,approach:0.000) brute(6.90,4.33,hp=4,windup:0.683) spitter(15.00,0.00,hp=2,fire_in=0.417,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.617,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=7.400 frame=444 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.150 stun_left=0.000 | grub(8.32,0.00,hp=2,recovery:0.367) grub(6.41,3.52,hp=2,approach:0.000) brute(6.90,4.33,hp=4,windup:0.267) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=7.550 frame=453 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.32,0.00,hp=2,recovery:0.217) grub(6.55,3.56,hp=2,approach:0.000) brute(6.90,4.33,hp=4,windup:0.117) spitter(15.00,0.00,hp=2,fire_in=2.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.667 frame=460 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.32,0.00,hp=2,recovery:0.100) grub(6.66,3.60,hp=2,approach:0.000) brute(6.90,4.33,hp=4,lunge:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.133,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | lunge {'enemy': 'brute'}
t=7.750 frame=465 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.32,0.00,hp=2,recovery:0.017) grub(6.74,3.62,hp=2,approach:0.000) brute(7.54,4.14,hp=4,recovery:1.200) spitter(15.00,0.00,hp=2,fire_in=2.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=7.767 frame=466 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.783 stun_left=0.283 | grub(8.32,0.00,hp=2,approach:-0.000) grub(6.74,3.62,hp=2,windup:0.500) brute(7.54,4.14,hp=4,recovery:1.183) spitter(15.00,0.00,hp=2,fire_in=2.033,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.633,cue=False) | windup {'enemy': 'grub'}
t=7.783 frame=467 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 | grub(8.32,0.02,hp=2,approach:-0.000) grub(6.74,3.62,hp=2,windup:0.483) brute(7.54,4.14,hp=4,recovery:1.167) spitter(15.00,0.00,hp=2,fire_in=2.017,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.617,cue=False) | ignored {'action': 'dash', 'reason': 'stunned', 'quiet': True}
t=8.000 frame=480 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.550 stun_left=0.050 | grub(8.30,0.23,hp=2,approach:-0.000) grub(6.74,3.62,hp=2,windup:0.267) brute(7.54,4.14,hp=4,recovery:0.950) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=8.267 frame=496 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.283 stun_left=0.000 | grub(8.28,0.50,hp=2,approach:-0.000) grub(6.74,3.62,hp=2,lunge:0.000) brute(7.54,4.14,hp=4,recovery:0.683) spitter(15.00,0.00,hp=2,fire_in=1.533,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.333,cue=True) | lunge {'enemy': 'grub'}
t=8.550 frame=513 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.26,0.78,hp=2,approach:-0.000) grub(8.91,4.27,hp=2,lunge:0.000) brute(7.54,4.14,hp=4,recovery:0.400) spitter(15.00,0.00,hp=2,fire_in=1.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.050,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=8.600 frame=516 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.25,0.83,hp=2,approach:-0.000) grub(9.04,4.31,hp=2,recovery:0.767) brute(7.54,4.14,hp=4,recovery:0.350) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=8.967 frame=538 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.22,1.20,hp=2,approach:-0.000) grub(9.04,4.31,hp=2,recovery:0.400) brute(7.54,4.14,hp=4,windup:0.700) spitter(15.00,0.00,hp=2,fire_in=0.833,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.033,cue=False) | windup {'enemy': 'brute'}
t=8.983 frame=539 pos=(8.00,3.73) hearts=1 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(8.22,1.21,hp=2,approach:-0.000) grub(9.04,4.31,hp=2,recovery:0.383) brute(7.54,4.14,hp=4,windup:0.683) spitter(15.00,0.00,hp=2,fire_in=0.817,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.017,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=9.200 frame=552 pos=(8.00,0.27) hearts=1 invulnerable=True dash_left=0.017 hurt_left=0.000 stun_left=0.000 | grub(8.19,1.28,hp=2,approach:-0.000) grub(9.04,4.31,hp=2,recovery:0.167) brute(7.54,4.14,hp=4,windup:0.467) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=9.217 frame=553 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.19,1.26,hp=2,approach:-0.000) grub(9.04,4.31,hp=2,recovery:0.150) brute(7.54,4.14,hp=4,windup:0.450) spitter(15.00,0.00,hp=2,fire_in=0.583,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.783,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=9.667 frame=580 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.12,0.82,hp=2,approach:-0.000) grub(8.97,4.02,hp=2,approach:-0.000) brute(7.54,4.14,hp=4,lunge:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.133,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.333,cue=False) | lunge {'enemy': 'brute'}
t=9.800 frame=588 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.10,0.69,hp=2,approach:-0.000) grub(8.94,3.89,hp=2,approach:-0.000) brute(8.57,3.83,hp=4,lunge:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=9.983 frame=599 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.53,hp=2,windup:0.500) grub(8.90,3.71,hp=2,approach:-0.000) brute(9.84,3.45,hp=4,recovery:1.183) spitter(15.00,0.00,hp=2,fire_in=2.217,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.017,cue=False) | windup {'enemy': 'grub'}
t=10.000 frame=600 pos=(7.73,0.00) hearts=1 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.53,hp=2,windup:0.483) grub(8.89,3.70,hp=2,approach:-0.000) brute(9.84,3.45,hp=4,recovery:1.167) spitter(15.00,0.00,hp=2,fire_in=2.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.000,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=10.233 frame=614 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.53,hp=2,windup:0.250) grub(8.74,3.52,hp=2,approach:-0.000) brute(9.84,3.45,hp=4,recovery:0.933) spitter(15.00,0.00,hp=2,fire_in=1.967,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=10.483 frame=629 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.53,hp=2,lunge:0.000) grub(8.54,3.37,hp=2,approach:-0.000) brute(9.84,3.45,hp=4,recovery:0.683) spitter(15.00,0.00,hp=2,fire_in=1.717,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.717,cue=False) | lunge {'enemy': 'grub'}
t=12.400 frame=744 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.91,0.00,hp=2,approach:-0.000) grub(7.00,2.23,hp=2,approach:-0.000) brute(9.10,3.01,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | aim
t=12.667 frame=760 pos=(4.27,0.00) hearts=1 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(6.65,0.00,hp=2,approach:-0.000) grub(6.79,2.07,hp=2,approach:-0.000) brute(8.94,2.92,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.333,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=12.700 frame=762 pos=(4.80,0.00) hearts=1 invulnerable=True dash_left=0.200 hurt_left=0.000 stun_left=0.000 | grub(6.63,0.00,hp=2,windup:0.500) grub(6.77,2.05,hp=2,approach:-0.000) brute(8.92,2.90,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.300,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | windup {'enemy': 'grub'}
t=12.717 frame=763 pos=(5.07,0.00) hearts=1 invulnerable=True dash_left=0.183 hurt_left=0.000 stun_left=0.000 | grub(6.63,0.00,hp=2,windup:0.483) grub(6.76,2.03,hp=2,approach:-0.000) brute(8.91,2.90,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.283,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.683,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=12.900 frame=774 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.63,0.00,hp=2,windup:0.300) grub(6.75,1.86,hp=2,approach:-0.000) brute(8.84,2.79,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.100,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=13.000 frame=780 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.63,0.00,hp=2,windup:0.200) grub(6.81,1.78,hp=2,approach:-0.000) brute(8.82,2.73,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=13.200 frame=792 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.63,0.00,hp=2,lunge:0.000) grub(6.92,1.61,hp=2,approach:-0.000) brute(8.78,2.59,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=2.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | lunge {'enemy': 'grub'}
t=13.500 frame=810 pos=(8.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,recovery:0.800) grub(7.08,1.38,hp=2,windup:0.500) brute(8.72,2.39,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.900,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | windup {'enemy': 'grub'}
t=13.517 frame=811 pos=(7.73,0.00) hearts=1 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,recovery:0.783) grub(7.08,1.38,hp=2,windup:0.483) brute(8.71,2.38,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.883,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.683,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=13.600 frame=816 pos=(6.40,0.00) hearts=1 invulnerable=True dash_left=0.150 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,recovery:0.700) grub(7.08,1.38,hp=2,windup:0.400) brute(8.68,2.33,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=13.750 frame=825 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,recovery:0.550) grub(7.08,1.38,hp=2,windup:0.250) brute(8.59,2.28,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.650,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.450,cue=True) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=14.000 frame=840 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,recovery:0.300) grub(7.08,1.38,hp=2,lunge:0.000) brute(8.43,2.20,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.200,cue=True) | lunge {'enemy': 'grub'}
t=14.200 frame=852 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,recovery:0.100) grub(7.97,0.05,hp=2,lunge:0.000) brute(8.31,2.14,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=14.317 frame=859 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,windup:0.500) grub(8.41,0.00,hp=2,recovery:0.783) brute(8.24,2.10,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.083,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.283,cue=False) | windup {'enemy': 'grub'}
t=14.333 frame=860 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,windup:0.483) grub(8.41,0.00,hp=2,recovery:0.767) brute(8.22,2.10,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=1.067,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.267,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'quiet': True}
t=14.800 frame=888 pos=(4.00,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.23,0.00,hp=2,windup:0.017) grub(8.41,0.00,hp=2,recovery:0.300) brute(7.93,1.95,hp=4,approach:-0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.0
[output cut at 20000 characters]
```

### Round 2: @run/trace/c20a-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn spitter 15 4
spawn grub 3 4
player 8 4
end 7
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.800,cue=False) grub(3.00,4.00,hp=2,approach:0.000) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) grub(4.20,4.00,hp=2,approach:0.000) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) grub(4.80,4.00,hp=2,approach:0.000) | spit
t=3.033 frame=91 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.167,cue=False) grub(6.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=3.533 frame=106 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.667,cue=False) grub(6.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=3.600 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) grub(6.53,4.00,hp=2,lunge:0.000) | aim
t=3.733 frame=112 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=0.467,cue=True) grub(7.60,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=4.200 frame=126 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) grub(7.60,4.00,hp=2,recovery:0.333) | spit
t=4.533 frame=136 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.067,cue=False) grub(7.60,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.567 frame=137 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.033,cue=False) grub(7.60,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=5.067 frame=152 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.533,cue=False) grub(7.60,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=5.100 frame=153 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=1.500,cue=False) grub(7.87,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=5.900 frame=177 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.700,cue=False) grub(7.87,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.933 frame=178 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.667,cue=False) grub(7.87,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=6.000 frame=180 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) grub(7.87,4.00,hp=2,windup:0.433) | aim
t=6.400 frame=192 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=0.200,cue=True) grub(7.87,4.00,hp=2,windup:0.033) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=7.000 frame=210 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.200,cue=True) grub(7.87,4.00,hp=2,windup:0.033) | end
```

### Round 2: @run/trace/c20a-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 4
spawn grub 3 4
player 8 4
end 7
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.800,cue=False) grub(3.00,4.00,hp=2,approach:0.000) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) grub(4.20,4.00,hp=2,approach:0.000) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) grub(4.80,4.00,hp=2,approach:0.000) | spit
t=3.017 frame=181 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.183,cue=False) grub(6.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=3.517 frame=211 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.683,cue=False) grub(6.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=3.600 frame=216 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) grub(6.67,4.00,hp=2,lunge:0.000) | aim
t=3.700 frame=222 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=0.500,cue=True) grub(7.47,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=4.200 frame=252 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) grub(7.47,4.00,hp=2,recovery:0.300) | spit
t=4.500 frame=270 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.100,cue=False) grub(7.47,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.517 frame=271 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.083,cue=False) grub(7.47,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=5.017 frame=301 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.583,cue=False) grub(7.47,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=5.033 frame=302 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=1.567,cue=False) grub(7.60,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=5.833 frame=350 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.767,cue=False) grub(7.60,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.850 frame=351 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.750,cue=False) grub(7.60,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=6.000 frame=360 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) grub(7.60,4.00,hp=2,windup:0.350) | aim
t=6.350 frame=381 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.250,cue=True) grub(7.60,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=6.367 frame=382 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=0.233,cue=True) grub(7.73,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=7.000 frame=420 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.233,cue=True) grub(7.73,4.00,hp=2,recovery:0.800) | end
```

### Round 2: @run/trace/c20b-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn spitter 15 4
player 8 4
3.85 dash right
end 7
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.900 frame=117 pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.300,cue=True) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=4.133 frame=124 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.067,cue=True) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=4.200 frame=126 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) | spit
t=5.067 frame=152 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=1.533,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=5.867 frame=176 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.733,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.000 frame=180 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) | aim
t=6.600 frame=198 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) | spit
t=7.000 frame=210 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.000,cue=False) | end
```

### Round 2: @run/trace/c20b-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 4
player 8 4
3.85 dash right
end 7
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=108 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.867 frame=232 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.333,cue=True) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=4.100 frame=246 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.100,cue=True) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=4.200 frame=252 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) | spit
t=5.050 frame=303 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,4.00,hp=2,fire_in=1.550,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=5.850 frame=351 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.750,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.000 frame=360 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=0.600,cue=True) | aim
t=6.600 frame=396 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.400,cue=False) | spit
t=7.000 frame=420 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,4.00,hp=2,fire_in=2.000,cue=False) | end
```

### Round 2: @run/trace/c21std-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 1.9 4
player 0.5 4
0.5 dash left
end 3.5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.90,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.90,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(0.00,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(1.90,4.00,hp=2,lunge:0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}; lunge {'enemy': 'grub'}
t=0.767 frame=23 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.03,4.00,hp=2,lunge:0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.667 frame=50 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.167 frame=65 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.200 frame=66 pos=(0.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(0.27,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.000 frame=90 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.27,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.033 frame=91 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.27,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=3.500 frame=105 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.27,4.00,hp=2,windup:0.033) | end
```

### Round 2: @run/trace/c21std-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 1.9 4
player 0.5 4
0.5 dash left
end 3.5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.90,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.90,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(0.23,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(1.90,4.00,hp=2,lunge:0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}; lunge {'enemy': 'grub'}
t=0.750 frame=45 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.03,4.00,hp=2,lunge:0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.633 frame=98 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.133 frame=128 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.150 frame=129 pos=(0.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(0.13,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.950 frame=177 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.13,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.967 frame=178 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.13,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=3.467 frame=208 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(0.13,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=3.483 frame=209 pos=(0.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(0.00,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.500 frame=210 pos=(0.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.783 stun_left=0.283 | grub(0.00,4.00,hp=2,recovery:0.783) | end
```

### Round 2: @run/trace/c21brute-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn brute 1.9 4
player 0.5 4
0.1 attack
0.7 dash left
end 4
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=4,approach:0.000) | setup
t=0.033 frame=1 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=4,windup:0.700) | windup {'enemy': 'brute'}
t=0.133 frame=4 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=3,windup:0.600) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.733 frame=22 pos=(0.00,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=3,lunge:0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}; lunge {'enemy': 'brute'}
t=0.967 frame=29 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.03,4.00,hp=3,lunge:0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.267 frame=68 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.00,4.00,hp=3,windup:0.700) | windup {'enemy': 'brute'}
t=2.967 frame=89 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.00,4.00,hp=3,lunge:0.000) | lunge {'enemy': 'brute'}
t=3.000 frame=90 pos=(0.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(0.27,4.00,hp=3,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.800 frame=114 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.27,4.00,hp=3,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=120 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.27,4.00,hp=3,recovery:0.200) | end
```

### Round 2: @run/trace/c21brute-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn brute 1.9 4
player 0.5 4
0.1 attack
0.7 dash left
end 4
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=4,approach:0.000) | setup
t=0.017 frame=1 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=4,windup:0.700) | windup {'enemy': 'brute'}
t=0.117 frame=7 pos=(0.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=3,windup:0.600) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.717 frame=43 pos=(0.23,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | brute(1.90,4.00,hp=3,lunge:-0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}; lunge {'enemy': 'brute'}
t=0.950 frame=57 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.03,4.00,hp=3,lunge:-0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.233 frame=134 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.00,4.00,hp=3,windup:0.700) | windup {'enemy': 'brute'}
t=2.933 frame=176 pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.00,4.00,hp=3,lunge:-0.000) | lunge {'enemy': 'brute'}
t=2.950 frame=177 pos=(0.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(0.13,4.00,hp=3,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.750 frame=225 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.13,4.00,hp=3,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=240 pos=(0.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(0.13,4.00,hp=3,recovery:0.150) | end
```

### Round 2: @run/trace/c19c-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn brute 9 4
player 8 4
0.1 attack
0.5 attack
1.2 attack
2.3 attack
end 4
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,windup:0.700) | windup {'enemy': 'brute'}
t=0.133 frame=4 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=3,windup:0.600) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,windup:0.200) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.733 frame=22 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'brute'}
t=0.800 frame=24 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(8.47,4.00,hp=2,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.233 frame=37 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 | brute(8.47,4.00,hp=1,recovery:0.767) | attack {'hits': [('brute', 'hit')]}
t=1.600 frame=48 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=1,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.033 frame=61 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=1,windup:0.700) | windup {'enemy': 'brute'}
t=2.333 frame=70 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('brute', 'defeated')]}; cleared
t=3.333 frame=100 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/trace/c19c-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn brute 9 4
player 8 4
0.1 attack
0.5 attack
1.2 attack
2.3 attack
end 4
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=4,windup:0.700) | windup {'enemy': 'brute'}
t=0.117 frame=7 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=3,windup:0.600) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,windup:0.200) | shrug {'enemy': 'brute'}; attack {'hits': [('brute', 'hit')]}
t=0.717 frame=43 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(9.00,4.00,hp=2,lunge:-0.000) | lunge {'enemy': 'brute'}
t=0.783 frame=47 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | brute(8.47,4.00,hp=2,recovery:1.200) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.217 frame=73 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 | brute(8.47,4.00,hp=1,recovery:0.767) | attack {'hits': [('brute', 'hit')]}
t=1.583 frame=95 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=1,recovery:0.400) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.000 frame=120 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(8.47,4.00,hp=1,windup:0.700) | windup {'enemy': 'brute'}
t=2.317 frame=139 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('brute', 'defeated')]}; cleared
t=3.317 frame=199 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```
>>>END
