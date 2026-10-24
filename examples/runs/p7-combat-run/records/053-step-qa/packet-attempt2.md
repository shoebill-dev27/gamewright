# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/55-studio-to-qa.md
next_seq: 56
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/56-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/55-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 55
from: studio
to: qa
stage: Observe
outcome: routed
---
# 55: studio → qa — Reproduce three player-reported unfair-feeling hits (late swipe vs lunge; hit with no visible cue)

## Task

Using the build in `repo/`, try to reproduce the three moments below, then decide for each whether the build matches the design documents and manual (not a defect) or contradicts them (defect, with a precise report and acceptance criteria). Also check one wording point (item 4).

## Context

Goal G-001 (combat feels monotonous). A fresh playtester played rooms 2–5 at 60 FPS through the player view with hand-written reaction scripts. They reported three hits that felt unfair or unexplained. An earlier, similar case (a room 2 grub hit after a swipe) was ruled not a defect in step 32; your report should say whether these differ from that case. Experience judgments (monotony, fun) are out of your scope; report only whether behavior matches the documents.

## Findings

Reported by the playtester (observations only, times in seconds of play):

1. **Room 2, late swipe at a rearing grub (about 4.0–4.25 s).** A grub reared back with a 0.5 s warning. The player swiped at the last moment (about 0.05 s left) and was hit anyway at 4.25 s. The manual says a swipe within 1.5 tiles cancels the lunge. Question: should a swipe this late have stopped it? Is "was in range, swipe landed, grub needs more than one swipe" the explanation?
2. **Room 5, swipe at a rearing grub (about 8.35–9.03 s).** A grub reared back (0.5 s warning). The player swiped once at 8.93 s (a hit) and the grub's lunge hit the player at 9.03 s, taking the last heart. The player thought the grub needed two swipes. Question: does the build behave as the documents say, including blocked-contact and lunge rules (see D-005)?
3. **Room 2, hit at about 5.4 s with no cue seen.** A runner was swiped and killed at about 5.0 s, then a grub hit the player at 5.4 s. The player saw no "rears back" line before it. Question: was there a cue (and was it printed in the player view), or did a hit land without the warning the design requires?
4. **Wording.** The line "A grub rears back" was reported as printed for runners and brutes too, distinguishable only from the `cue:` line ("r", "g", "G"). Check what the design documents and manual say the message should be for each enemy; report any mismatch.

Scripts used (play with `python3 play.py --view player {script}`, then `--view trace` to explain; reproduce at 60 FPS and 30 FPS):

Room 2 cautious (items 1 and 3), with `end 16`:
```
room 2
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see r within 3 then move away
```

Room 5 cautious (item 2), with `end 16`:
```
room 5
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when text "takes aim" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see g within 3 then move away
```

If the exact moments do not recur from these scripts, write your own input script that puts the player in the same situation (a swipe in the last 0.1 s of a grub's wind-up) and report what you ran.

## Decisions already made

D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit. D-002/D-003: contact-edge sampling and exact-reach rules. Other Decisions in the Load list apply as written.

## Constraints

- Verify against the design documents, manual and Decisions; where they are silent or contradict each other, report the gap as "expected behavior undefined" (goes to Design), do not invent a rule.
- Do not change the build.
- Run `python3 -m unittest discover -s tests` first and report the result.

## Open questions

- Is the hit at about 5.4 s in room 2 preceded by a printed cue? (item 3)
- Does the manual state clearly enough to a player whether a late swipe cancels a lunge, and how many swipes a grub takes? If not, say so; that is a wording question for Design, not a build defect.

## Expected output

A report in the handoff template: for each of items 1–4, reproduced yes/no, what happened (times, hearts, enemy state), the governing document line, and the verdict (matches / defect with severity and acceptance criteria / undefined). Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, the build in repo/ (run commands in project.md)
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/53-playtester-to-studio.md (observations only); similar earlier case: goals/G-001-combat-monotony/32-qa-to-studio.md
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

<<<FILE design/combat-cues-visual-spec.md
# Combat cue visual spec (build 0.5 cues, for the graphical build)

Owner: art-director. Source: G-001 step 15. Basis: the text view and `design/combat.md`. I did not see a rendered build. Timings and rules are unchanged and belong to the game-designer.

## Principles

- Threat cues are saturated orange-red and **self-lit**. They do not depend on the lantern, so a cue reads in full darkness.
- The lantern is warm, pale and low-saturation (amber to cream). Threat cues are more saturated and shifted toward red, and they are the brightest saturated thing on screen.
- **Color is never the only signal.** Every cue also differs in shape or motion, so it holds up for color-blind players and under lantern tint.
- Reuse existing assets: one orange-red palette entry, one additive glow sprite, one line/quad sprite. All variants are parameter changes (scale, rate), not new assets.

## Grub lunge cue (Standard, Runner, Brute)

1. **Lane, not a hairline.** The lunge path is drawn as a band along the locked direction, 2.4 tiles long. Its width equals the actual danger zone, 1.2 tiles (0.6 either side). It is a translucent orange-red fill with a brighter hazard edge.
   - Reason: the design text says "thin line" but the danger is 1.2 tiles wide. A hairline makes a 1-tile sidestep look sufficient when it may not be.
   - Players should be able to see that stepping 1 tile sideways takes them clear of the band.
2. **Onset.** The grub flash and the lane appear at full contrast on the first frame of wind-up, with no fade-in. This matters for the Runner, whose wind-up is 0.35 s, about 10 frames at 30 FPS.
3. **Duration visibility.** The lane fills from the grub outward, or its fill brightens, so that it is complete exactly when the lunge starts. The player can judge the time left without reading text.
4. **Grub body.** The grub holds a steady orange-red tint with a slight pulse, and rears back by squashing away from the lunge direction. Do not strobe. Keep flashing at or below 3 Hz.
5. **End of cue.** The lane stays at full strength until the lunge starts, then fades during the lunge. The flash and tint stop when recovery begins, and the grub returns to its neutral cool color. A grub that is neutral and not tinted means "safe to swipe".
6. **Stagger.** A cancelled wind-up (swipe) removes the lane immediately and shows a hit reaction, so a cancelled lunge is not mistaken for a pending one.

### Variants

Differentiate by silhouette and size first, then by cue cadence. Do not use a different hue.

| Variant | Body | Lane | Cue cadence |
|---|---|---|---|
| Runner `r` | smallest, lean | full 1.2 width | fast pulse, ends in 0.35 s |
| Standard `g` | medium | full 1.2 width | medium pulse, 0.5 s |
| Brute `G` | largest, heavy | full 1.2 width | slow pulse, 0.7 s |

The lane geometry is identical, so lane width never depends on variant. All three share the lunge distance.

## Spitter aim cue

1. **Glow.** An orange-red additive glow on the spitter ramps from a **floor of at least 30% to 100%** over the 0.6 s. The text view shows 0% at the start. Do not render 0% as invisible. The cue must be noticeable on the first frame.
2. **Aim line.** A **thin** orange-red line, visually narrower than the grub lane. It runs from the spitter along the locked direction to the room edge. It is visible from the first frame of the cue at full line brightness. Only the glow ramps.
3. **End of cue.** At the shot the line disappears (it does not linger), the glow drops to neutral, and a projectile starts. The line must not be readable as a stationary shot.
4. **Distance.** The spitter glow and the line are self-lit. They must be visible when the spitter is outside the lantern radius, including in the far corners of the 16-by-9 room.
5. **Killed during cue.** The line and the glow disappear at once (the shot is cancelled).

## Shot `*`

- A compact **round** orange-red core with a short bright trail, brighter than the line, always moving.
- It must differ from the aim line by shape (a round object vs a straight line) and by motion.
- It must be readable against the lantern light and against a lane or line behind it. Give the core a light outline or a hot white center so it does not merge with a same-colored lane.

## Telling cues apart on one screen

| Thing | Shape | Motion/time signal |
|---|---|---|
| Grub lunge | wide band, short (2.4 tiles) | fills up, then the grub moves |
| Spitter aim | thin line, long (to edge) | glow ramps, then the line vanishes |
| Shot | round core with trail | moves at 3 tiles/s |
| Lantern | soft round warm pool, low saturation | static around the player |

At most one grub cue is active at once (rule). Spitter cues are normally 0.8 s apart and last 0.6 s, so they rarely overlap. They can overlap after a cap delay, and then the two aim lines must still be readable. They are identical in style, and the glow plus the line origin tell them apart.

## Player-observable acceptance criteria

V1. In a dark room with the player far from a grub, the player can see the cue (flash plus lane) without the lantern reaching it.
V2. A first-time player can state where the lunge will go and how wide it is, and can tell a 1-tile sidestep clears it.
V3. The cue is visible from the very first frame of the wind-up, including the Runner's 0.35 s, at both 30 and 60 FPS.
V4. The player can tell, without text, how much time is left before the lunge or the shot.
V5. A Runner, Standard grub and Brute are told apart by silhouette alone, in grayscale.
V6. A grub lane and a spitter aim line are told apart in grayscale (wide band vs thin line).
V7. The aim line, the shot and the lane never merge. A shot passing over a lane is still seen.
V8. A recovering or staggered grub looks clearly neutral (no tint). A player can tell when it is safe to swipe.
V9. No cue flashes faster than 3 Hz.
V10. A cancelled or killed enemy's cue disappears at once.
V11. The orange-red threat color is never confused with the warm lantern light. A threat inside the lantern radius is still clearly redder and more saturated than the lit floor.
V12. Cue timing in the graphical build matches the text-view timings at 30 and 60 FPS, within one frame.
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

<<<FILE goals/G-001-combat-monotony/53-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 53
from: playtester
to: studio
stage: Play
outcome: done
---
# 53: playtester → studio — Observation report: combat in rooms 2–5

## Task

Report what I experienced playing the combat of rooms 2, 3, 4 and 5 as a player, with the scripts I used and the moments I describe.

## Context

This follows handoff 51, a fresh playtest of the build in `repo/`. I played with the player view only, with no trace view, bots or tests, and I did not read the source. I was told nothing about what changed.

I played as the profile: an action player who likes dodging and spacing, wants short intense runs and uses a gamepad.

## Findings

### Method

- I could not play live. I played by input automation with reaction rules, using `python3 play.py --view player {script}` at 60 FPS.
- The rules were reaction-time style: step aside from a shot coming at me, dash or step aside on "rears back" or "takes aim", swipe whatever is within about 1.4 tiles, and move toward or away from enemies.
- I did not use frame-perfect inputs. My feel notes come from reading the printed room pictures and cue lines, not from controller feel.
- Several runs were cut off by the output limit, so I only saw the first 20–24 s of the round 1 runs:
  - room 2 aggressive, up to about 24 s;
  - room 3 cautious, up to about 22 s;
  - room 4 aggressive, up to about 19.5 s;
  - room 5 aggressive, up to about 21 s.
- I never saw how those four runs ended.
- Runs seen in full:
  - room 2 cautious, 16 s;
  - room 3 aggressive, which cleared the room in 10.4 s;
  - room 4 cautious, 16 s;
  - room 5 cautious, where I went down at 9.0 s.
- I tried an aggressive and a cautious approach in every room.
- I did not try slow, deliberate play with long waits in any room.

### Scripts played

Round 1:
- room 2 aggressive:
  ```
  room 2
  when see * coming within 1.5 then move aside
  when text "rears back" then dash aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see g within 4 then move toward
  ```
- room 3 cautious:
  ```
  room 3
  when see * coming within 1.5 then move aside
  when text "rears back" then dash aside
  when see r within 1.4 then attack
  when see G within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 3 then move away
  when see g within 3 then face
  ```
- room 4 aggressive and room 5 aggressive used the same script:
  ```
  room N
  when see * coming within 1.5 then move aside
  when text "rears back" then dash aside
  when text "takes aim" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 1.4 then attack
  when see s within 1.4 then attack
  when nothing within 2 then move toward
  ```

Round 2, all with `end 16`:
- room 2 cautious:
  ```
  room 2
  end 16
  when see * coming within 1.5 then move aside
  when text "rears back" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 1.4 then attack
  when see G within 3 then move away
  when see r within 3 then move away
  ```
- room 3 aggressive:
  ```
  room 3
  end 16
  when see * coming within 1.5 then move aside
  when text "takes aim" then move aside
  when see s within 1.4 then attack
  when see s within 12 then move toward
  ```
- room 4 cautious:
  ```
  room 4
  end 16
  when see * coming within 1.5 then move aside
  when text "rears back" then move aside
  when text "takes aim" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see s within 1.4 then attack
  when see g within 3 then move away
  when see r within 3 then move away
  ```
- room 5 cautious:
  ```
  room 5
  end 16
  when see * coming within 1.5 then move aside
  when text "rears back" then move aside
  when text "takes aim" then move aside
  when see r within 1.4 then attack
  when see g within 1.4 then attack
  when see G within 1.4 then attack
  when see G within 3 then move away
  when see g within 3 then move away
  ```

### Session summary

| Run | Result I saw |
|---|---|
| Room 2 aggressive | 3/3 hearts until 11.6 s. Hit once by the brute's lunge, then 2/3 until the output cut at about 24 s. Runners and a grub killed, room not cleared. |
| Room 2 cautious | Hit by a grub at 4.25 s and 5.4 s, so 1/3. Stalled for 10 s, kiting the brute along the left wall. Ended at 16 s with the brute alive. |
| Room 3 cautious | Hit by shots at 3.9 s and 4.7 s, so 1/3. Then a long standoff with shots filling the room, no kills, until the cut at about 22 s. |
| Room 3 aggressive | Cleared at 9.4 s with 2/3 hearts. One hit by a shot. All three spitters killed. |
| Room 4 aggressive | 3/3 hearts until the cut at about 19.5 s. Two grubs/runners hit or killed, spitters untouched. |
| Room 4 cautious | Hit by a shot at 4.8 s and by a grub at 14.7 s, so 1/3. Two kills, ended at 16 s with enemies left. |
| Room 5 aggressive | Hit once by a shot at 4.35 s. Then 2/3 through about 21 s. Two grubs and one spitter killed, brute still alive. |
| Room 5 cautious | Went down at 9.0 s. Hit by shots at 4.3 s and 6.4 s, then by a grub lunge. |

### Concrete moments

- **Room 3 opening, 1.2 s.** "A spitter takes aim" printed, and a big `~` line crossed the whole room through me. It was very readable: I knew where the shot would go and how long I had (0.6 s). I felt in control.
- **Room 3 cautious, about 9.6 s onward.** All three spitters took aim at the same instant, three times in a row (9.6 s, 13.8 s, 17.4 s and again at 19.8 s). Lines crossed the screen and I could only slide along a wall and wait. My attention dropped. It felt like waiting out a pattern, and I never had a way to fight back.
- **Room 3 aggressive, 1.2–9.4 s.** I charged the spitters and swiped them as I reached them. This felt completely different from the cautious run: quick, tense, over in about 10 s. It was the most fun combat of the session. I took one hit at 2.1 s when I walked into a shot that was already flying.
- **Rooms 4 and 5, spitters.** The spitters alternated about every 0.6–0.8 s and it was always the same rhythm: aim, glow, spit, then the other one. Stepping aside worked every time I reacted on the cue. The shots I took (4.35 s in room 5 aggressive, 4.27 s and 6.43 s in room 5 cautious, 4.78 s in room 4 cautious) were ones where I was already standing in the line. I could see them coming, so these were fair hits.
- **Grubs and runners.** "A grub rears back" printed for every grub, runner and brute alike. I could only tell them apart from the `cue:` line, which says "r", "g" or "G". Because I dashed on the message alone, I often dashed away from a runner that was far off and wasted a dash. Dashing "aside" on every cue left me dashing about every second in room 2 (about 12 dashes in 24 s) and landing few swipes.
- **Room 2 cautious, 4.0–4.25 s.** A grub reared back with a 0.5 s warning. I swiped at the last moment (0.05 s left) and was hit anyway. The swipe did not stop it. This felt unfair, though the pictures show I was close, so I may have mistimed it. The manual says a swipe within 1.5 tiles cancels, and this one did not.
- **Room 2 cautious, 5.0–5.4 s.** I swiped a runner and killed it, then was hit by a grub at 5.4 s with no new warning that I saw. It was probably another lunge that started right after, but I did not see its cue in the print. This one felt like damage I could not see coming. I am not certain.
- **Room 2 aggressive, 10.9–11.6 s.** The brute reared back with a 0.7 s warning and I stood in the line for the whole time. I got hit at 0.08 s left. The warning was long and obvious, so this was my own mistake. Brutes on their own are slow and easy to step away from.
- **Room 2 cautious, 6–16 s.** I backed away from the brute along the left wall and nothing happened for 10 s. The brute crept after me without attacking. Boring.
- **Room 5 cautious, 8.35–9.03 s.** A grub reared back at 0.5 s warning. I swiped it once (hit) at 8.93 s, and the grub lunged and hit me at 9.03 s, taking my last heart. I think I stayed in the lunge line because the grub needed two swipes. This felt harsh: I did the "right" thing (swipe to cancel) and still went down. I could not tell whether the swipe was supposed to have stopped it.
- **Room 5 aggressive, 6.2–8.0 s.** Grubs and the brute were near each other. I got a good hit streak: "grub hit, brute hit", then "grub defeated, brute hit". It felt busy and fun for a moment. I also dashed to avoid a brute lunge at 7.35 s and it worked. The brute's lunge cue came while I was swiping grubs, and I had to choose between the two. That was the one moment in rooms 4–5 where I had to decide something.
- **Nothing looked broken.** No crash, no stuck state and no shot from nowhere. Every hit I took had a visible cue before it, except possibly the 5.4 s hit in room 2 noted above.

### Issues with impact

1. **Rooms feel alike, high impact.** Almost every threat is the same move: see a cue, step or dash sideways, swipe afterwards. Grub, runner and brute differ in warning time (0.5 s, 0.35 s, 0.7 s) and in swipes needed, but I answered all of them the same way. Spitters in rooms 3, 4 and 5 are the same too. By room 4 I felt I had already seen it all. "I never needed to think about which enemy it was."
2. **The fighting-style difference is only visible in room 3, medium impact.** In room 3 charging and kiting felt very different. In rooms 2, 4 and 5 both approaches ended up as the same cue-dodging loop. The cautious runs mostly burned time and lost hearts, and the aggressive ones did not feel riskier.
3. **Cautious play stalls, medium-high impact.** In room 2 cautious (10 s of nothing) and room 3 cautious (several simultaneous volleys with no way to progress), I spent a lot of time waiting. Kiting a brute along a wall was dull.
4. **Simultaneous spitters in room 3, medium impact.** Three lines at once across the whole room were readable but left me with only one answer: slide along a wall.
5. **Dash was nearly free, medium impact.** Dashing on each cue avoided nearly all damage, so threat felt low in room 5 aggressive and room 4 aggressive (3/3 at the cut). Hits came almost only when I did not react.
6. **Same message for every lunger, low-medium impact.** "A grub rears back" is printed for runners and brutes too. I could not tell from the message which one was about to hit me.
7. **Swipe versus lunge timing, medium impact.** The two hits where I swiped a rearing grub and was hit anyway (room 2 cautious at 4.25 s, room 5 cautious at 9.03 s) felt unfair, because I could not tell whether swiping that late would work.

### Positives

- Spitter telegraphs are very readable: the line, the brightening and the 0.6 s countdown. I never felt cheated by a shot.
- Grub and brute warnings are clear, and the brute's long warning makes it feel heavy.
- Room 3 aggressive was the best moment: fast, tense and clean.
- Room 5's mix of grubs, brute and spitters at 6–8 s was the most interesting crowd.
- Runs are short, which fits the profile.

## Decisions already made

None.

## Constraints

- I used the player view only, with no trace view, bots or tests.
- I did not read source code.
- This report contains only what I saw and did, with no guesses at implementation and no code changes proposed.
- Four round 1 runs were truncated in the output, so I report nothing about how they ended.

## Open questions

- Does a swipe at a rearing grub cancel it when done very late (under about 0.1 s)? Twice I swiped and was hit anyway, and I could not tell why.
- What caused the grub hit at 5.4 s in room 2 cautious? I saw no cue before it.
- I did not try slow, waiting-style play or other dash timings in any room, and I did not play room 1.

## Expected output

This report goes to `studio`, for routing. Experience issues belong with `game-designer`. The possible unfair-hit moments might go to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/51-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-combat-monotony/32-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 32
from: qa
to: studio
stage: Triage
outcome: done
---
# 32: qa → studio — Room 2 "grub hit right after a swipe": not a build defect (swipe landed during the lunge); manual wording is misleading

## Task

Report whether the playtester's room 2 observation (handoff 27, item 5) is a defect, a rules-conforming case, or not reproducible. Verdict: **not a build defect. It reproduces, and it conforms to design/combat.md.** One low-severity documentation wording issue is noted for routing.

## Context

Goal G-001. The playtester reported:

- a grub rearing back at about 5.37 s;
- "grub hit" from their swipe at about 5.9 s;
- a grub hit on the player at about 6.017 s.

They asked whether the swipe failed to cancel the lunge or a second grub hit them. The exact script was not preserved. I reconstructed a comparable reaction-rule script (sidestep on "rears back", swipe things within 1.4, approach) and ran `run_trace` at 60 and 30 FPS in room 2. `run_tests` passed (34 tests, OK).

## Findings

### Timeline check against the playtester's numbers

Wind-up for a standard grub is 0.5 s, so a wind-up starting at 5.37 s turns into a lunge at about 5.87 s. The swipe at 5.9 s therefore landed about 0.03 s after the lunge began, not during the wind-up. The grub is then in flight, and the hit at 6.017 s is the lunge reaching the player, about 0.1 s later. The playtester's timeline fits one grub whose swipe came too late to cancel. I derived this from the numbers and could not check it against the original run.

### Trace evidence, 30 FPS (same pattern reproduced)

| Time (s) | Event |
|---|---|
| 2.633 | grub `windup:0.500` |
| 3.133 | grub `lunge` begins |
| 3.300 | `attack {'hits': [('grub','hit')]}`: grub hp 2→1, phase still `lunge` (grub at about (11.95,3.25), player (11.60,4.13), distance about 0.95, within the 1.5 reach) |
| 3.367 | `hurt {'source':'grub','hearts':2}`, 0.067 s after the swipe; the grub goes to `recovery:0.800` |

The sequence is the same as the playtester's: "grub hit", then hurt about 0.07–0.1 s later. It is the same grub, there is no second grub, and the lunge was already in flight when the swipe landed.

The same pattern appears for a brute at 30 FPS: swipe hit during `lunge` at 4.567, hurt at 4.633, source labelled `grub` (the brute is a brute grub). A runner lunge also hit at 5.933 on the same frame the swipe defeated a brute.

### Trace evidence, 60 FPS

- 4.033: grub `windup:0.500`. The player was at (12.93,5.27) and the grub at (12.79,3.60), so the distance was about 1.68, **outside the 1.5 swipe reach**. The swipes at 4.033–4.483 hit or killed the brute. The attacks at 4.183 and 4.333 were ignored as `recovering`.
- 4.533: lunge. 4.650: the player is hit, and the grub stops early at contact and goes to `recovery`.
- Here the swipe never reached the winding-up grub, so this is not a failed cancel.
- 5.033: a swipe hits the grub in recovery (hp 2→1), phase unchanged.
- 5.467: the grub winds up again. 5.500: a swipe kills it during wind-up with no stagger and no lunge, which matches the "kill in wind-up" rule.

### Not the D-002 graze

The lunge contacts were not edge cases. The grub stopped about 0.5 tile (60 FPS: (12.83,4.53) vs player (12.87,5.07), distance about 0.54) from a stationary player in the lane's center. That is far from the 0.57–0.60 band, and the hit came from the player standing in the lane, not from a near-reach path.

### Expected vs actual

- Expected (design/combat.md, Grub rules): "A swipe that damages a grub in wind-up cancels the wind-up." Also: a grub hit but not killed during Lunge "continues its phase unchanged", and a lunge that reaches the player deals 1 damage unless the player is invulnerable.
- Actual: the swipe landed in the lunge, the lunge continued, and the hit followed. This conforms.
- Documentation conflict (low): `repo/manual.md` says "step 1 tile to the side, dash, or swipe it (within 1.5 tiles) to cancel the lunge." It does not say the swipe only works during the warning, and "cancel the lunge" can read as covering a lunge already moving. combat.md is clear and says a lunge in flight is not cancelled. The manual's own warning duration (0.5 s) hints at the limit but does not state it. This is a manual wording gap, not a build defect. Fixing it is a manual change, and I do not decide intended player-facing wording.

### Classification, severity, reproducibility

- Defect: none found. Rules-conforming, with the documents agreeing on the build's behavior.
- Reproducibility: the pattern reproduced at 30 FPS (grub and brute) and the timing arithmetic fits the playtester's report. At 60 FPS my script did not produce the same sequence, because the swipe never reached the winding-up grub. I did not run a controlled 60 FPS case of a swipe landing just after lunge start.
- Severity of the manual wording issue: low (it can mislead a player about when the swipe cancels). Frequency: any swipe that lands after the wind-up ends.

### Not covered

- The exact original script and its trace are unavailable, so the match is by arithmetic and a comparable reproduction.
- I did not observe a non-lethal swipe during wind-up (the "cancel plus 0.4 s stagger" case) in these traces. The tests passed, but I did not inspect which tests cover it.
- I did not check at code level how the 1.5 reach is measured. The distances above come from trace positions.
- No unit or script was changed. The build was not modified.

## Decisions already made

- D-002: per-frame contact sampling kept, graze accepted. This case is not the graze (see above).

## Constraints

Report only, verified from design/combat.md, repo/manual.md, D-002 and the build (trace, tests). The build is unchanged.

## Open questions

- For `game-designer`: should the manual say explicitly that a swipe only cancels a lunge during the wind-up, and that a lunge already moving is not cancelled (the grub stays hittable and the lunge still hurts unless the player dashes or sidesteps)? This is wording, not a rule change. The combat.md rule is unambiguous, so no ruling on intent is needed. Whether to reword the manual is the designer's call.
- Related and optional, for the same designer: nothing else is raised by this case.

## Expected output

Studio decides routing: close handoff 27 item 5 as not-a-defect, and send the manual wording question above to `game-designer` (low priority). No fix is requested from `gameplay-engineer`.

If the studio wants more evidence, a controlled practice-room script (`room empty`, `spawn grub`, `player`, swipe at 0.45 s vs 0.55 s after the cue) at fps 30 and 60 would show the two sides of the 0.5 s boundary. I did not run it, since the verdict does not depend on it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/29-studio-to-qa.md
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

### Round 1: @run/play/room2 — `python3 play.py --view player {script}`

Script:

```text
room 2
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see r within 3 then move away
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
   |         P      |
   |                |
   |    r        G  |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r         |
   |           P    |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |       r        |
   |          P     |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
  3.550  a grub rears back
   [3.55 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |       r   ~    |
   |          P~    |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
   cue: g at (11.3,2.2) flashes orange-red, lunge line toward (-0.44,+0.90), 2.4 tiles (0.50 s to the lunge)
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |        r  ~    |
   |          P~    |
   |       r        |
   |             G  |
   |                |
   |                |
   +----------------+
   cue: g at (11.3,2.2) flashes orange-red, lunge line toward (-0.44,+0.90), 2.4 tiles (0.05 s to the lunge)
  4.150  you swipe: grub hit
  4.250  YOU ARE HIT by a grub — hearts 2/3
   [4.25 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        r Pg    |
   |       r        |
   |            G   |
   |                |
   |                |
   +----------------+
  4.267  a grub rears back
   [4.27 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        r~Pg    |
   |       r        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (8.3,3.5) flashes orange-red, lunge line toward (+0.97,+0.25), 2.4 tiles (0.35 s to the lunge)
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        r~Pg    |
   |       r        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (8.3,3.5) flashes orange-red, lunge line toward (+0.97,+0.25), 2.4 tiles (0.12 s to the lunge)
  4.600  you swipe: grub defeated
  4.917  a grub rears back
   [4.92 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~Pr    |
   |        r~  G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.1,4.7) flashes orange-red, lunge line toward (+0.93,-0.37), 2.4 tiles (0.35 s to the lunge)
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~Pr    |
   |        r~  G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.1,4.7) flashes orange-red, lunge line toward (+0.93,-0.37), 2.4 tiles (0.27 s to the lunge)
  5.000  you swipe: runner defeated
  5.400  YOU ARE HIT by a grub — hearts 1/3
   [5.40 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
  5.767  you swipe: runner defeated
   [6.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P           |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |  P             |
   |          G     |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |          G     |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |          G     |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |         G      |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |         G      |
   |                |
   |                |
   |                |
   +----------------+
   [10.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |         G      |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P       G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P       G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P       G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P      G        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P      G        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P      G        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P     G         |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P     G         |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P    G          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P    G          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P    G          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P   G           |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 16.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/trace/room2 — `python3 play.py --view trace {script}`

Script:

```text
room 2
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see r within 3 then move away
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=2 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(2.00,1.00,hp=1,approach:0.000) runner(1.00,8.00,hp=1,approach:0.000) brute(15.00,7.00,hp=4,approach:0.000) grub(14.00,0.00,hp=2,approach:0.000) | setup
t=3.550 frame=213 pos=(10.47,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.20,3.22,hp=1,approach:0.000) runner(6.05,5.45,hp=1,approach:0.000) brute(12.79,5.89,hp=4,approach:0.000) grub(11.34,2.23,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=4.050 frame=243 pos=(9.93,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(7.97,3.43,hp=1,approach:0.000) runner(6.81,5.18,hp=1,approach:0.000) brute(12.51,5.68,hp=4,approach:0.000) grub(11.34,2.23,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=4.167 frame=250 pos=(10.07,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.15,3.48,hp=1,approach:0.000) runner(6.98,5.12,hp=1,approach:0.000) brute(12.44,5.64,hp=4,approach:0.000) grub(10.93,3.07,hp=1,lunge:0.000) | attack {'hits': [('grub', 'hit')]}
t=4.250 frame=255 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(8.28,3.51,hp=1,approach:0.000) runner(7.11,5.07,hp=1,approach:0.000) brute(12.39,5.60,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=4.267 frame=256 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.783 stun_left=0.283 | runner(8.28,3.51,hp=1,windup:0.350) runner(7.13,5.06,hp=1,approach:0.000) brute(12.38,5.60,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.783) | windup {'enemy': 'runner'}
t=4.283 frame=257 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 | runner(8.28,3.51,hp=1,windup:0.333) runner(7.16,5.05,hp=1,approach:0.000) brute(12.37,5.59,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.767) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.300 frame=258 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.750 stun_left=0.250 | runner(8.28,3.51,hp=1,windup:0.317) runner(7.19,5.05,hp=1,approach:0.000) brute(12.37,5.58,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.750) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.317 frame=259 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | runner(8.28,3.51,hp=1,windup:0.300) runner(7.21,5.04,hp=1,approach:0.000) brute(12.36,5.58,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.733) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=4.383 frame=263 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | runner(8.28,3.51,hp=1,windup:0.233) runner(7.31,5.00,hp=1,approach:0.000) brute(12.32,5.55,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.667) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.450 frame=267 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.600 stun_left=0.100 | runner(8.28,3.51,hp=1,windup:0.167) runner(7.41,4.97,hp=1,approach:0.000) brute(12.28,5.52,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.600) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.467 frame=268 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.583 stun_left=0.083 | runner(8.28,3.51,hp=1,windup:0.150) runner(7.44,4.96,hp=1,approach:0.000) brute(12.27,5.51,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.583) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=4.533 frame=272 pos=(10.20,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.517 stun_left=0.017 | runner(8.28,3.51,hp=1,windup:0.083) runner(7.54,4.92,hp=1,approach:0.000) brute(12.23,5.49,hp=4,approach:0.000) grub(10.63,3.67,hp=1,recovery:0.517) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.617 frame=277 pos=(10.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.433 stun_left=0.000 | runner(8.28,3.51,hp=1,lunge:0.000) runner(7.66,4.88,hp=1,approach:0.000) brute(12.19,5.45,hp=4,approach:0.000) | attack {'hits': [('grub', 'defeated')]}; lunge {'enemy': 'runner'}
t=4.717 frame=283 pos=(10.27,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 | runner(9.06,3.71,hp=1,lunge:0.000) runner(7.81,4.83,hp=1,approach:0.000) brute(12.13,5.41,hp=4,approach:0.000) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=4.867 frame=292 pos=(10.07,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.183 stun_left=0.000 | runner(10.22,4.01,hp=1,lunge:0.000) runner(8.04,4.74,hp=1,approach:0.000) brute(12.04,5.35,hp=4,approach:0.000) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=4.917 frame=295 pos=(9.93,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | runner(10.61,4.10,hp=1,recovery:0.600) runner(8.09,4.73,hp=1,windup:0.350) brute(12.01,5.33,hp=4,approach:0.000) | windup {'enemy': 'runner'}
t=5.017 frame=301 pos=(9.80,3.80) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 | runner(8.09,4.73,hp=1,windup:0.250) brute(11.96,5.29,hp=4,approach:0.000) | attack {'hits': [('runner', 'defeated')]}
t=5.050 frame=303 pos=(9.73,3.80) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.09,4.73,hp=1,windup:0.217) brute(11.94,5.28,hp=4,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.267 frame=316 pos=(9.40,3.80) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.09,4.73,hp=1,lunge:0.000) brute(11.81,5.20,hp=4,approach:0.000) | lunge {'enemy': 'runner'}
t=5.333 frame=320 pos=(9.60,3.80) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(8.59,4.53,hp=1,lunge:0.000) brute(11.77,5.17,hp=4,approach:0.000) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=5.400 frame=324 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | runner(9.08,4.33,hp=1,recovery:0.600) brute(11.73,5.15,hp=4,approach:0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=5.433 frame=326 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 | runner(9.08,4.33,hp=1,recovery:0.567) brute(11.71,5.14,hp=4,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=5.483 frame=329 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 | runner(9.08,4.33,hp=1,recovery:0.517) brute(11.68,5.12,hp=4,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=5.500 frame=330 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | runner(9.08,4.33,hp=1,recovery:0.500) brute(11.67,5.12,hp=4,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=5.583 frame=335 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | runner(9.08,4.33,hp=1,recovery:0.417) brute(11.62,5.09,hp=4,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=5.633 frame=338 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.567 stun_left=0.067 | runner(9.08,4.33,hp=1,recovery:0.367) brute(11.59,5.07,hp=4,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'stop', 'reason': 'stunned', 'quiet': True}; ignored {'action': 'attack', 'reason': 'stunned', 'quiet': True}
t=5.650 frame=339 pos=(9.33,3.80) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.550 stun_left=0.050 | runner(9.08,4.33,hp=1,recovery:0.350) brute(11.58,5.06,hp=4,approach:0.000) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=5.783 frame=347 pos=(9.33,3.60) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.417 stun_left=0.000 | brute(11.50,5.02,hp=4,approach:0.000) | attack {'hits': [('runner', 'defeated')]}
t=6.200 frame=372 pos=(7.67,3.60) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(11.23,4.89,hp=4,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=16.000 frame=960 pos=(0.00,3.60) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | brute(4.43,4.07,hp=4,approach:0.000) | end
```

### Round 1: @run/trace/room5 — `python3 play.py --view trace {script}`

Script:

```text
room 5
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when text "takes aim" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see g within 3 then move away
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2,approach:0.000) grub(0.00,6.00,hp=2,approach:0.000) brute(4.00,8.00,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=3.000,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.10,1.47,hp=2,approach:0.000) grub(1.16,5.71,hp=2,approach:0.000) brute(4.59,7.41,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=1.800 frame=108 pos=(8.00,1.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.69,1.59,hp=2,approach:0.000) grub(1.71,5.47,hp=2,approach:0.000) brute(4.84,7.07,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=2.400 frame=144 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.27,1.47,hp=2,approach:0.000) grub(2.18,5.10,hp=2,approach:0.000) brute(5.03,6.69,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=3.000 frame=180 pos=(8.00,2.40) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.86,1.45,hp=2,approach:0.000) grub(2.68,4.77,hp=2,approach:0.000) brute(5.23,6.32,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.33,4.47) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.39,1.72,hp=2,approach:0.000) grub(3.27,4.65,hp=2,approach:0.000) brute(5.53,6.04,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.800,cue=False) | aim
t=4.200 frame=252 pos=(8.33,3.93) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.92,2.01,hp=2,approach:0.000) grub(3.86,4.57,hp=2,approach:0.000) brute(5.87,5.79,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | spit
t=4.267 frame=256 pos=(8.47,4.07) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(4.97,2.05,hp=2,approach:0.000) grub(3.93,4.56,hp=2,approach:0.000) brute(5.91,5.76,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.333,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.133,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.400 frame=264 pos=(8.47,4.07) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | grub(5.09,2.12,hp=2,approach:0.000) grub(4.06,4.54,hp=2,approach:0.000) brute(5.98,5.71,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.000,cue=False) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.550 frame=273 pos=(8.47,4.07) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.517 stun_left=0.017 | grub(5.22,2.19,hp=2,approach:0.000) grub(4.21,4.53,hp=2,approach:0.000) brute(6.07,5.65,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.850,cue=False) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=4.800 frame=288 pos=(8.93,4.07) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.267 stun_left=0.000 | grub(5.44,2.31,hp=2,approach:0.000) grub(4.46,4.50,hp=2,approach:0.000) brute(6.22,5.56,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.800,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.600,cue=True) | aim
t=5.067 frame=304 pos=(8.93,3.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.69,2.40,hp=2,approach:0.000) grub(4.72,4.44,hp=2,approach:0.000) brute(6.37,5.45,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.533,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.333,cue=True) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.400 frame=324 pos=(8.93,1.67) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.02,2.38,hp=2,approach:0.000) grub(5.01,4.29,hp=2,approach:0.000) brute(6.52,5.27,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=2.400,cue=False) | spit
t=6.433 frame=386 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.80,1.74,hp=2,approach:0.000) grub(5.70,3.53,hp=2,approach:0.000) brute(6.80,4.61,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.367,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=6.500 frame=390 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 | grub(6.83,1.70,hp=2,windup:0.500) grub(5.74,3.47,hp=2,approach:0.000) brute(6.81,4.56,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.700,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.300,cue=False) | windup {'enemy': 'grub'}
t=6.517 frame=391 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 | grub(6.83,1.70,hp=2,windup:0.483) grub(5.75,3.46,hp=2,approach:0.000) brute(6.82,4.55,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.683,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.283,cue=False) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=6.583 frame=395 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.650 stun_left=0.150 | grub(6.83,1.70,hp=2,windup:0.417) grub(5.78,3.40,hp=2,approach:0.000) brute(6.83,4.50,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.617,cue=False) spitter(15.00,8.00,hp=2,fire_in=1.217,cue=False) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=6.600 frame=396 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.633 stun_left=0.133 | grub(6.83,1.70,hp=2,windup:0.400) grub(5.79,3.39,hp=2,approach:0.000) brute(6.83,4.49,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.600,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.200,cue=False) | aim
t=6.617 frame=397 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | grub(6.83,1.70,hp=2,windup:0.383) grub(5.80,3.38,hp=2,approach:0.000) brute(6.83,4.48,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.583,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.183,cue=False) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=6.733 frame=404 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.500 stun_left=0.000 | grub(6.83,1.70,hp=2,windup:0.267) grub(5.86,3.28,hp=2,approach:0.000) brute(6.85,4.40,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.467,cue=True) spitter(15.00,8.00,hp=2,fire_in=1.067,cue=False) | ignored {'action': 'move', 'reason': 'stunned', 'quiet': True}
t=7.000 frame=420 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.233 stun_left=0.000 | grub(6.83,1.70,hp=2,lunge:0.000) grub(6.00,3.05,hp=2,approach:0.000) brute(6.89,4.22,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.200,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | lunge {'enemy': 'grub'}
t=7.100 frame=426 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | grub(7.25,1.01,hp=1,lunge:0.000) grub(6.05,2.96,hp=2,approach:0.000) brute(6.91,4.15,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.100,cue=True) spitter(15.00,8.00,hp=2,fire_in=0.700,cue=False) | attack {'hits': [('grub', 'hit')]}
t=7.200 frame=432 pos=(7.87,0.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 | grub(7.66,0.33,hp=1,lunge:0.000) grub(6.10,2.88,hp=2,approach:0.000) brute(6.92,4.08,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.400,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | spit
t=7.233 frame=434 pos=(7.87,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.80,0.10,hp=1,lunge:0.000) grub(6.12,2.85,hp=2,approach:0.000) brute(6.93,4.06,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.367,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.250 frame=435 pos=(7.87,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.87,0.00,hp=1,lunge:0.000) grub(6.13,2.84,hp=2,approach:0.000) brute(6.93,4.05,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.350,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=7.400 frame=444 pos=(7.60,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.08,0.00,hp=1,recovery:0.700) grub(6.20,2.71,hp=2,approach:0.000) brute(6.95,3.95,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.200,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.800,cue=False) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=7.550 frame=453 pos=(7.33,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.27,2.57,hp=2,approach:0.000) brute(6.97,3.84,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=2.050,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | attack {'hits': [('grub', 'defeated')]}
t=8.350 frame=501 pos=(7.33,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.57,1.85,hp=2,windup:0.500) brute(7.02,3.28,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=1.250,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | windup {'enemy': 'grub'}
t=8.850 frame=531 pos=(7.40,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.57,1.85,hp=2,lunge:0.000) brute(7.06,2.94,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.750,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.750,cue=False) | lunge {'enemy': 'grub'}
t=8.950 frame=537 pos=(7.40,0.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.87,1.11,hp=1,lunge:0.000) brute(7.07,2.87,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.650,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.650,cue=False) | attack {'hits': [('grub', 'hit')]}
t=9.033 frame=542 pos=(7.40,0.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.13,0.49,hp=1,recovery:0.800) brute(7.07,2.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=9.833 frame=590 pos=(7.40,0.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.13,0.49,hp=1,recovery:0.800) brute(7.07,2.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=10.033 frame=602 pos=(7.40,0.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.13,0.49,hp=1,recovery:0.800) brute(7.07,2.81,hp=4,approach:0.000) spitter(15.00,0.00,hp=2,fire_in=0.767,cue=False) spitter(15.00,8.00,hp=2,fire_in=0.767,cue=False) | end
```
>>>END
