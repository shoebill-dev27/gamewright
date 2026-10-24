# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/91-studio-to-game-director.md
next_seq: 92
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/92-game-director-to-<recipient>.md
- decisions/D-013-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/91-studio-to-game-director.md
---
kind: handoff
goal: G-001
seq: 91
from: studio
to: game-director
stage: Review
outcome: routed
---
# 91: studio → game-director — Review pass 3: is combat still monotonous after builds 22a, 23 and 25a?

## Task

Judge with `review-outcome` whether the Goal's intent is now met, and name the next issues. This is Review pass 3; passes 1 and 2 both returned goal-not-met with a narrow gap.

## Context

Goal G-001 (Owner request: 戦闘が単調なので改善したい). Success condition: a player experiences combat as varied and engaging, different situations call for noticeably different play, and the player can tell why. Everything stays inside the pillars: one-button combat (D-001), short runs, readable threats.

Since Review pass 2 (67, D-010):
- Build 22a: variant-named wind-up and hit messages and manual wording (D-011).
- Build 23: room 3 gets one standard grub at (15,0) and its second spitter moves to (10,6) (D-012).
- Build 25a: test-only fix. The suite is 64/64 and bot results are unchanged.
- Docs were aligned in 25b and 26c.

Evidence to weigh:
- QA 76, 82, 86 and 90: no build defect. Criteria pass at 30 and 60 FPS except for the known gaps below.
- Playtest 88 (fresh, reaction rules, not live) reports:
  - grub encounters feel identical across rooms;
  - spitter rooms are mostly dodging;
  - the brute tail in room 5 is empty;
  - two of three room 4 shot hits could not be traced;
  - "swipe landed, still hit" was unexplained.
- Earlier playtests (27, 53, 63): rooms 4–5 varied and tense; runner and brute distinct.

## Findings

QA 90 on the two readability points from playtest 88:
- **A. Room 4 hits.** No defect. Dash invulnerability matches the design (0.25 s, no damage in any dash). The player's three hits were not reproduced because the script was lost. Readability failure: `YOU ARE HIT by a shot` names no source, and the shot is consumed at the hit, so no later frame shows which shot hit.
- **B. Swipe landed, still hit.** Matches the design: a swipe cancels only during wind-up (`combat.md`, manual). Reproduced at 30 FPS in room 4. Readability failure: no player-view line says the lunge had already begun or why the swipe did not cancel it. Only the brute has a "shrugs off" line.

Known gaps still unshown (QA has made its last bounded try; no further QA round is planned):
- R3-8 at 60 FPS (passes at 30 FPS);
- the room 3 pure 1-tile sidestep;
- 30 FPS cancel and recovery swipe in room 3.

Visual criteria V1–V11 need a graphical build and are planned as a new Goal at Close. V12 is open. The stray last line of D-007 could not be removed by any step and is an Owner item at Close.

## Decisions already made

- D-001: one attack button plus dash.
- D-002, D-003: contact-edge graze accepted.
- D-004 to D-007: cue gap, blocked contact, walker limit, room 3 in-flight bound.
- D-009: next pass was a variant-aware playtest; escalate to the Owner only if the melee still reads as one fight.
- D-010: Review pass 2 result.
- D-011: variant-named messages accepted.
- D-012: room 3 change.

## Constraints

- No new input buttons (Owner approval needed, D-001), no change to run length, no new biomes or unrelated content.
- Small team: prefer changes that reuse existing systems.
- Must play correctly at 30 and 60 FPS.
- Escalate to the Owner only for an escalation trigger. Record a Decision if your verdict constrains later work.

## Open questions

1. Is the Goal met, or is the remaining gap (grub sameness, dodge-heavy spitter rooms, empty brute tail) small enough to call met?
2. Should the two readability gaps (A: shot source in the hit message; B: a line explaining a late swipe) become a Design step for `game-designer` under the "readable threats" pillar? Or do they belong in a later Goal?
3. Do you accept the unshown items as known gaps? Does the loop limit on Diagnose (two passes done, no new cause in Review 67) still bar a third Diagnose?
4. Does the melee still read as one fight? If so, D-009's Owner escalation condition fires.

## Expected output

A Review verdict handoff, with `outcome` goal-met or goal-not-met, addressed to `studio`. State the next issues, and name any Decision or Escalation you propose.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/combat-step72.md, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/88-playtester-to-studio.md, goals/G-001-combat-monotony/86-qa-to-studio.md, goals/G-001-combat-monotony/67-game-director-to-studio.md
- Decisions: decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/90-qa-to-studio.md
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
runs: play, bots
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/review-outcome.md
---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
>>>END

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE design/combat.md
# Combat design (specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38; builds 0.5 and 0.6)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Build 0.6 implements the step 35 and step 38 parts (verified by QA, handoff 82); build 0.5 behaved as described without them.** The player kit is unchanged from 0.4.

**Step 80 (documents only, no rule or number changed):** the room 3 row and purpose, criterion 11 (in-flight bound), criterion 12, the Cap paragraph's real-room sentence and the wind-up message wording were brought in line with `combat-step68.md` (D-011), `combat-step72.md` (D-012) and D-007. Where they differ, those notes and decisions govern.

**Step 87 (documents only, no rule or number changed):** the wording items from QA report 82 section 4 (cue gap rule for room 3, two step 38 references to the room 3 simultaneous-start case, title and header build references) were corrected.

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
   - Text view: a message naming the variant when it starts: `a grub rears back`, `a runner rears back` or `a brute rears back` (D-011). The strings, and the matching hit messages `YOU ARE HIT by a grub/runner/brute`, are in `combat-step68.md`, which governs.
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
  - Room 3 and practice rooms do not use this rule. Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007).
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. The reopen triggers are those of D-007 (revisit of D-005 item 4).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In rooms 4–5 the count stays at 3 or fewer. In room 3 up to 5 is accepted after a cap delay (2 plus the living spitters, D-007; see `combat-step-46-room3-cap.md`). A practice room with four or more spitters can also go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
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
| 3 | Spitters at (2,1), (10,6), (2,7), in that order, and a standard grub at (15,0) (D-012; see `combat-step72.md`) | 0.8 s / none | Learn the aim cue first, then answer an aim line and a lunge lane together |
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
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). The in-flight bound is criterion 11 as amended in `combat-step-46-room3-cap.md` (a–e) and D-007: shots in flight never exceed 2 plus the living spitters (at most 3 in rooms 4–5, up to 5 in room 3 after a cap delay). In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

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

12. **Rooms differ.** The contents match the table above (room 3 as in `combat-step72.md`, R3-1).
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
- Step 38: a real-room trace of room 3 past 7 s — closed. QA 43 showed simultaneous starts occur there after a cap delay; accepted in D-007, whose reopen triggers apply.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-step72.md
# Combat design note, step 72: room 3 gets a second ask (a standard grub) and a tighter spitter layout

Status: room content only (room 3 table row). No rule, parameter, cap, cue, timing or input change. Where this note and `design/combat.md` differ on the room 3 row, criterion 12 or the room 3 purpose, this note governs. Fold into `combat.md` the next time it is edited. Decision: D-012. D-001, D-004 to D-007 and D-011 are untouched.

## Intent

Room 3 still teaches the aim cue first, with the verified schedule (first shots 1.8, 2.6, 3.4 s). After that it asks a second, different question: a lunge lane on top of aim lines. The player must move toward and through the room instead of repeating "aim, dash, shot lands behind me". The last spitter is never far from the others, and a hunting grub keeps the player moving, so the room does not become a long standoff against one spitter in a far corner.

## Diagnosis (design terms)

1. One ask. Room 3 has only the aim-line ask, answered the same way each time (sidestep or dash). With nothing else to answer, attention drops after the third or fourth repeat (playtests 53 and 63).
2. A standoff has no pressure to end it. Spitters are stationary, HP 2, and fire every 2.4 s. A player who kills two and leaves the third far away loses nothing by dodging for a long time. The east spitter at (14,7) is 12 tiles from the west spitter at (2,7), so reaching it is a long walk. Shots take about 4 s to cross, so each dodge is slow and the whole thing reads as a wait.
3. Rooms 4–5 held attention because several different asks overlap. Room 3 is the only room with a single ask.

## Options considered

| Option | Second ask | Pressure on a lone spitter | Touches cap or cue rule? | Verdict |
|---|---|---|---|---|
| A. Add one standard grub, far from the player's start, and move the third spitter closer | Lunge lane (step aside or dash) | The grub hunts the player, so staying still costs hearts. The spitters are closer together. | No | **Chosen** |
| B. Add one runner instead | Fast short lane (0.35 s warning) | Same | No | Rejected: the 0.35 s warning on top of 0.6 s aim cues in the teaching room is a harsh jump. Rooms 2 and 4 already cover the runner. |
| C. Add a brute | "Step aside, then punish" | Strong | No | Rejected: HP 4 and a 1.2 s recovery add a long fight to a room that is meant to teach. The brute stays in rooms 2 and 5. |
| D. Replace one spitter with a grub (two spitters plus grub) | Same as A | Strong | Yes. It changes the 1.8/2.6/3.4 s schedule and the in-flight bound. | Rejected: breaks criterion 11a and forces the D-007 verification to be redone. |
| E. Gap rule 0.2 s in room 3 (D-007 prepared fallback) | None | None | Yes | Rejected: fixes a different problem and changes a verified room. |
| F. New mechanics (reinforcements arriving later, a spitter that speeds up when alone, healing) | n/a | n/a | n/a | Outside this step: a new system or new enemy behavior. Not specified. |

## Chosen option: A

### Room 3 contents (replaces the room 3 row)

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 3 | Spitters at (2,1), (10,6), (2,7), in that room-table order (k = 0, 1, 2). Standard grub at (15,0). | 0.8 s / none (unchanged) | Learn the aim cue first, then answer an aim line and a lunge lane together |

Changes against the old row:
- The second spitter moves from (14,7) to (10,6). The order of the spitter list is the same, so k = 0, 1, 2 and the first-shot times are unchanged.
- One standard grub is added at (15,0), in the far corner away from the spitters and from the usual start.

All other room 3 parameters are unchanged: spitter interval 2.4 s, offset 0.8 s, cap 3, no gap rule, the D-007 bound (up to 2 plus the living spitters, so at most 5), and the grub parameters of the standard variant (HP 2, walk 1.0, wind-up 0.5 s, lunge 8.0 for 0.3 s, recovery 0.8 s, swipe cancels wind-up).

### Why these choices

- **Standard grub, not runner or brute.** Its answer is "either" (sidestep, dash or cancel). It is the gentlest lunge, so it is the right second ask for a room that is still teaching. It does not need new text; D-011 names it `a grub rears back`.
- **The grub walks at 1.0 tile/s from the far corner.** The distance gives the delay with no new system: it should not reach 2.0 tiles of the player, and so not start its first wind-up, until well after the third spitter's first cue. Criterion R3-3 checks this and tells QA what to do if the geometry says otherwise.
- **Spitter (10,6).** The largest distance between any two spitters becomes 9.4 tiles (between (2,1) and (10,6)), against 12.4 before. A player at 4 tiles/s covers that in about 2.4 s, or sooner with a dash. Spitter position affects only where the shot starts, not any cue time.
- **The grub pressures a stationary or kiting player.** A player who stands off and dodges shots is hunted by the grub, which asks for a lane answer or a kill. The room does not end until the grub is dead too, and it is a 2 HP target that can be swiped in recovery.
- **The one-at-a-time rule is untouched.** It applies among grubs. With one grub it changes nothing in room 3. Spitters are not gated by the grub and the grub is not gated by spitters.

### Edge cases

- **Grub wind-up while a spitter cue is running (or the reverse).** Allowed. They are two separate cues: a thin line and a 1.2-tile lane. A dash clears both. A sidestep must clear both. Readable threats holds because each cue is visible for its full duration. This is the same overlap that rooms 4–5 already have, except there the gap rule spaces the spitter cues from each other, which does not matter for a grub.
- **Cap and in-flight bound.** The grub does not count as a shot and does not delay a cue. D-007 stands: shots in flight never exceed 2 plus the living spitters.
- **Blocked contact (D-005).** Unchanged. A lunge that touches a protected player is spent. A shot that touches a protected player is consumed.
- **Grub killed early.** Room 3 continues with the spitters only. The standoff risk then returns for the last spitter, but the layout keeps it close (see R3-8).
- **All spitters killed first.** The grub fights as a single standard grub, as in room 1.
- **Player dies or room cleared.** Existing handling.
- **Player start position.** I could not check the start position in this packet. R3-3 is written so QA measures it from a trace.

## Acceptance criteria

### Verifiable (QA, `play` and `bots`; every check at both 30 and 60 FPS)

- **R3-1. Contents.** Room 3 contains exactly three spitters at (2,1), (10,6), (2,7) and one standard grub at (15,0). Room 3 contains no other enemy. Rooms 1, 2, 4, 5 are unchanged (criterion 12).
- **R3-2. Teaching schedule intact.** With a still player, the first spitter shots are at 1.8, 2.6 and 3.4 s ±1 frame, each cue 0.6 s ±1 frame before its shot (criteria 9, 11a). The grub changes none of these.
- **R3-3. The grub comes after the lessons.** With a player standing still at the room's start position, the grub's first wind-up message (`a grub rears back`) appears no earlier than 4.0 s after the room starts. Expected from geometry: the grub has to cover several tiles at 1.0 tile/s before it is within 2.0 tiles (derived, not measured). If QA's trace shows an earlier start, QA reports the measured time and the start position to `game-designer`, who moves the grub (tuning, no new spec step).
- **R3-4. The grub obeys the existing grub criteria in room 3.** The cue is at least 0.5 s before the hit (1); a 1-tile sidestep within 0.4 s of the cue avoids it (2); a dash from the cue until 0.1 s before the lunge ends avoids it and the player takes no damage after the dash (3, 21); a swipe in reach during the wind-up cancels it (6); two swipes kill it (6, 8); the recovery is safe (5).
- **R3-5. Spitter criteria hold with the grub alive.** Criteria 9 and 10 (cue and dodge) and 17 hold for shots fired in room 3.
- **R3-6. The D-007 bound is unchanged.** Criterion 11 as amended (step 46 note a–e) holds: the derived count of shots in flight in room 3 is 3 to 5 after a cap delay, and above 5 is a defect. No cue start is delayed or advanced by the grub: cue start times with the grub are equal to the times without it, ±1 frame, for the same still-player script until the grub's first lunge.
- **R3-7. Room end.** Room 3 is cleared only when the three spitters and the grub are all defeated. Killing the last spitter with the grub alive does not clear the room, and the reverse.
- **R3-8. The last spitter is close.** The distance between any two spitters in room 3 is at most 9.5 tiles. In a scripted run that kills the grub and two spitters, a player that then walks straight to the last spitter (dashing when a cue is on) and swipes it clears the room within 6 s of the previous kill (derived: about 2.4 s of walking plus two swipes, so about 3 s). This checks that the layout allows a quick finish. It does not force the player to take it.
- **R3-9. Messages.** The grub's wind-up and hit use whatever messages the build has (`a grub rears back`, `YOU ARE HIT by a grub`), whether or not Build 22a (D-011) is in. A rule `text "rears back"` reacts to it.
- **R3-10. Frame-rate independence (16).** Criteria 1–12 and 17–21 hold at both rates in room 3. No new tolerance is introduced.

Bots (criteria 13–15): the walker faces one more lunge in room 3, so the sum of its hearts lost in rooms 3–5 is expected to rise. At 60 FPS it was already at the upper limit of 6 (criterion 13). The limit may be exceeded, and the clear count may fall below 2. The dodger should be unaffected or have slightly more use for the dash. These are **expected effects, not verified**. QA measures them on the Build and reports values outside the limits to `game-designer` as a tuning question, not a build defect, as in steps 22, 35 and 38. If the bots key on room 3 contents, the Build updates them (test tooling).

### Experience signals (playtest and Review, not for the Playtester's handoff)

- In room 3 the player describes two kinds of threat: "the lines from the spitters" and "the grub that comes for me", and answers each differently.
- The first minute of room 3 is still described as learning the aim line, with the grub appearing as a new thing after that, not as a surprise during the first cues.
- The room is not described as "the same thing again" for most of its length, and no stretch of about 10 s consists of dodging one far-off spitter.
- A player who hears or sees a lunge cue during a shot cue can say which one to answer first, or that one move answered both.
- Nobody reports a shot or lunge that "came out of nowhere".

## Changed design documents

This note (new). `combat.md` is not edited here. The room 3 row, criterion 12 and the room 3 purpose line are governed by this note until folded in. D-012 records the choice.

## Open questions

1. The player start position in room 3 was not available to me. R3-3 is the guard; QA reports the measured grub arrival time.
2. Whether a human still produces a long single-spitter standoff cannot be known from scripts. A live or hand-timed playtest of room 3 is the check (D-010 item 5). If a standoff persists, the next levers are a runner in place of the standard grub (Option B) or a second grub, then a larger room change. A new enemy or new behavior would go to `game-director`.
3. Whether the grub on top of aim cues is too much for a room that teaches. If the playtest says so, move the grub later (further away) before changing anything else.
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-16
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player playing the current build's combat experiences it as varied and engaging instead of monotonous. Different situations call for noticeably different play (positioning, timing, use of attack and dash), and the player can tell why. The improvement stays inside the vision pillars: one-button combat (attack + dash only, D-001), short runs, readable threats. Numeric thresholds belong to Design; the final verdict belongs to Review.

Out of scope: new input buttons (needs Owner approval per D-001), changing run length, new biomes or content unrelated to combat variety, and any change to the core concept. Not a defect report: nothing in the request says combat is broken.

## Unknowns

- Observe: done (02; QA 16, 20, 32, 36, 56, 64). Contact-edge graze accepted (D-002, D-003). 30 FPS player view and late-swipe boundary match the design (64). Playtest 88's room 4 hits and "swipe landed, still hit" were checked by QA 90: no defect; the player's three hits were not reproduced. Two readability gaps remain: a shot hit names no source, and no line says why a late swipe did not cancel the lunge.
- Diagnose: two passes done (04, 31); a third is barred by the loop limit. Review 67 found no new cause.
- Decide: skipped. Review pass 2 (67, D-010) found the D-009 escalation condition not met. Row 11 (Owner escalation) stays tentative: only if Review pass 3 says the melee still reads as one fight.
- Design: D-004 to D-007 stand. Room 3 in-flight question settled by D-007 (68); D-011 accepted (variant-named wind-up and hit messages, supersedes D-008). Room 3 variety specified by D-012 (72): one standard grub at (15,0), second spitter to (10,6); cap and cue rule unchanged. Open for the playtest: whether a long single-spitter standoff remains. Wording fixes done (87). The stray last line of D-007 could not be removed by any step (outside the designer's writable paths): an Owner item at Close.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: 0.6.1 done (48). Build 22a done (71): D-011 messages and manual wording. Build 23 done (74): room 3 data change per D-012. Build 25a done (79): test-only fix, suite 64/64 OK, bots unchanged. Docs aligned in 25b (80, 87).
- Verify (QA): pass on 0.6.1 at 30 and 60 FPS (50, 64). Re-verify 26 (82): suite 64/64, no defect. Round 26b (86): no defect; R3-8 passes at 30 FPS only; the room 3 sidestep, 30 FPS cancel and recovery cases are not shown. Round 27b (90) did not run room 3: R3-8 at 60 FPS, the room 3 sidestep and the 30 FPS cancel/recovery swipe stay unshown. They go to Review as known gaps; no further QA try. Visual V1–V11 need a graphical build, a proposed new Goal at Close; V12 open.
- Play: four scripted passes done (27, 53, 63, 88). Rooms 4–5 varied and tense; runner and brute distinct. Pass 4 (88, reaction rules, not live): grub encounters identical in all rooms; two of three room 4 shot hits untraceable; swipe-and-still-hit unexplained; spitter rooms mostly dodging; brute tail in room 5 empty.
- Review: pass 1 (60) and pass 2 (67) done, both goal-not-met; the gap is narrow. Pass 3 is open (91).

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md (report: 02-playtester-to-studio.md) |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-studio-to-game-designer.md (result: 04-game-designer-to-studio.md) |
| 3 | Decide | game-director | make-decision | skipped (no real choice; see Unknowns) | — |
| 4a | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md (result: 07-game-designer-to-studio.md) |
| 4b | Observe (FPS divergence) | qa | reproduce-defect | done | 06-studio-to-qa.md (result: 08-qa-to-studio.md) |
| 5 | Plan | technical-director | technical-plan | skipped (approach local; see Unknowns) | — |
| 6 | Build | gameplay-engineer | implement-change | done | 09-studio-to-gameplay-engineer.md (result: 10-gameplay-engineer-to-studio.md) |
| 7a | Design (criterion 14, spec gaps) | game-designer | write-design-spec | done | 11-studio-to-game-designer.md (result: 14-game-designer-to-studio.md) |
| 7b | Verify (visual) | art-director | visual-review | done | 12-studio-to-art-director.md (result: 15-art-director-to-studio.md) |
| 7c | Observe (walker 30/60 divergence) | qa | reproduce-defect | done | 13-studio-to-qa.md (result: 16-qa-to-studio.md) |
| 7d | Build (bot log data, walker test) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md (result: 18-gameplay-engineer-to-studio.md) |
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | done (question: graze) | 19-studio-to-qa.md (result: 20-qa-to-studio.md) |
| 8b | Design (graze, cap, margin, doc conflicts) | game-designer | write-design-spec | done | 21-studio-to-game-designer.md (result: 22-game-designer-to-studio.md) |
| 8c | Build (contact test / cap) | gameplay-engineer | implement-change | skipped (graze and cap accepted as built) | — |
| 8d | Verify (criteria 1–17; close 30 FPS gaps) | qa | verify-change | done (pass) | 23-studio-to-qa.md (result: 24-qa-to-studio.md) |
| 9a | Play | playtester | playtest-session | done | 25-studio-to-playtester.md (report: 27-playtester-to-studio.md) |
| 9b | Design (QA notes: exact-reach miss, lunge band) | game-designer | write-design-spec | done | 26-studio-to-game-designer.md (result: 30-game-designer-to-studio.md) |
| 10a | Diagnose (playtest issues 1–4) | game-designer | diagnose-experience | done | 28-studio-to-game-designer.md (result: 31-game-designer-to-studio.md) |
| 10b | Observe (room 2 grub hit after swipe) | qa | reproduce-defect | done (not a defect) | 29-studio-to-qa.md (result: 32-qa-to-studio.md) |
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | tentative (only if Review pass 3 says so) | — |
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | done | 33-studio-to-game-designer.md (result: 35-game-designer-to-studio.md) |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | done (no defect) | 34-studio-to-qa.md (result: 36-qa-to-studio.md) |
| 12c | Design (invulnerable contact, room 3 cue overlap) | game-designer | write-design-spec | done | 37-studio-to-game-designer.md (result: 38-game-designer-to-studio.md) |
| 13 | Build (build 0.6 per Design 35 and 38) | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md (result: 40-gameplay-engineer-to-studio.md) |
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | done (fail: F2, F3, 13@60, room 3) | 41-studio-to-qa.md (result: 43-qa-to-studio.md) |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | done (D-006, no build change) | 42-studio-to-game-designer.md (result: 44-game-designer-to-studio.md) |
| 15 | Design (room 3 cap vs criterion 11) | game-designer | write-design-spec | done (D-007, accepted as built) | 45-studio-to-game-designer.md (result: 46-game-designer-to-studio.md) |
| 16 | Build (F2, F3 only) | gameplay-engineer | implement-change | done | 47-studio-to-gameplay-engineer.md (result: 48-gameplay-engineer-to-studio.md) |
| 17 | Verify (re-verify, incl. "not run" list, criterion 11 a–e) | qa | verify-change | done (pass) | 49-studio-to-qa.md (result: 50-qa-to-studio.md) |
| 18a | Play (fresh, hand-timed rooms 2–5) | playtester | playtest-session | done | 51-studio-to-playtester.md (report: 53-playtester-to-studio.md) |
| 18b | Design (criterion 11d wording, non-blocking) | game-designer | write-design-spec | done (no build change) | 52-studio-to-game-designer.md (result: 54-game-designer-to-studio.md) |
| 18c | Observe (late swipe vs lunge; hit with no cue; message wording) | qa | reproduce-defect | done (not a defect) | 55-studio-to-qa.md (result: 56-qa-to-studio.md) |
| 18d | Design (manual wording on late swipes; variant cue message) | game-designer | write-design-spec | done (D-008 proposed, later D-011) | 58-studio-to-game-designer.md (result: 59-game-designer-to-studio.md) |
| 19 | Review (pass 1) | game-director | review-outcome | done (goal-not-met; D-009) | 57-studio-to-game-director.md (result: 60-game-director-to-studio.md) |
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | done | 61-studio-to-playtester.md (report: 63-playtester-to-studio.md) |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | done (no defect) | 62-studio-to-qa.md (result: 64-qa-to-studio.md) |
| 21a | Review (pass 2) | game-director | review-outcome | done (goal-not-met; D-010) | 65-studio-to-game-director.md (result: 67-game-director-to-studio.md) |
| 21b | Design (room 3 in-flight vs D-007; D-008 readiness) | game-designer | write-design-spec | done (D-007 stands; D-011 accepted) | 66-studio-to-game-designer.md (result: 68-game-designer-to-studio.md) |
| 22a | Build (D-011 messages, manual wording) | gameplay-engineer | implement-change | done | 69-studio-to-gameplay-engineer.md (result: 71-gameplay-engineer-to-studio.md) |
| 22b | Design (room 3 variety, existing enemies) | game-designer | write-design-spec | done (D-012) | 70-studio-to-game-designer.md (result: 72-game-designer-to-studio.md) |
| 23 | Build (room 3 change, D-012) | gameplay-engineer | implement-change | done | 73-studio-to-gameplay-engineer.md (result: 74-gameplay-engineer-to-studio.md) |
| 24 | Verify (22a + 23; V-a..e, R3-1..10; 30 and 60 FPS) | qa | verify-change | done (fail: red test only) | 75-studio-to-qa.md (result: 76-qa-to-studio.md) |
| 25a | Build (fix test, test code only) | gameplay-engineer | implement-change | done | 77-studio-to-gameplay-engineer.md (result: 79-gameplay-engineer-to-studio.md) |
| 25b | Design (doc conflicts, documents only) | game-designer | write-design-spec | done (D-007 stray line left) | 78-studio-to-game-designer.md (result: 80-game-designer-to-studio.md) |
| 26 | Verify (re-verify; close R3-8, R3-4 gaps) | qa | verify-change | done (no defect; 5 items unjudged) | 81-studio-to-qa.md (result: 82-qa-to-studio.md) |
| 26b | Verify (R3-8 timed run, R3-4 in room 3) | qa | verify-change | done (no defect; 60 FPS items unshown) | 84-studio-to-qa.md (result: 86-qa-to-studio.md) |
| 26c | Design (doc wording, D-007 stray line) | game-designer | write-design-spec | done (wording fixed; D-007 line is an Owner item) | 85-studio-to-game-designer.md (result: 87-game-designer-to-studio.md) |
| 27 | Play (fresh, new build, reaction rules) | playtester | playtest-session | done | 83-studio-to-playtester.md (report: 88-playtester-to-studio.md) |
| 27b | Observe (room 4 hits, swipe-and-still-hit; last bounded 60 FPS items) | qa | reproduce-defect | done (no defect; 2 readability gaps) | 89-studio-to-qa.md (result: 90-qa-to-studio.md) |
| 28 | Review (pass 3) | game-director | review-outcome | open | 91-studio-to-game-director.md |
| 29 | Next | studio | — | planned | — |

## Route changes

After QA 27b (90): no defect. The player's room 4 hits were not reproduced, and dash invulnerability matches the design. Two readability gaps (shot hit names no source; no line explains a late swipe) are given to Review rather than a new Design step. The room 3 timed items stay unshown and go to Review as known gaps. Review pass 3 opened (91).

## Next action

Run `game-director` with 91-studio-to-game-director.md (result addressed to `studio`). Then Route: goal-met goes to Close; goal-not-met goes to Diagnose or Design as the Review directs (the readability gaps are the likely Design input), and to the Owner only if the melee still reads as one fight (D-009). At Close, propose the visual criteria V1–V12 (graphical build) as a new Goal and list the D-007 stray line as an Owner item.

## Outcome

(open)
>>>END

<<<FILE goals/G-001-combat-monotony/88-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 88
from: playtester
to: studio
stage: Play
outcome: done
---
# 88: playtester → studio — Observation report: rooms 1–5, combat experience

## Task

Report what I experienced playing rooms 1–5, with attention to combat. This is a player-view observation report only.

## Context

This answers handoff 83. The build was sha 1ac4d04d0e75, played with `python3 play.py --view player`. I did not read source, tests or design documents.

## Findings

### Method (what I actually did)

- I did **not** play live with hand-timed inputs. The session is a script, and I could only play by writing **reaction rules** (react to what is on screen, with a 0.15 s reaction delay) and reading the printed frames afterwards.
- I made one run per room, rooms 1–5, and revised the rules between rounds. I never replayed an identical script.
- Rules I used:
  - Room 1: dash aside on every "rears back", swipe when close.
  - Room 2: dash aside only on a brute, swipe on other rear-backs.
  - Rooms 3–5: step aside on "takes aim", dash aside on "rears back", dash aside from nearby shots, swipe when close, otherwise walk toward the enemy.
- Different handling styles were tried only partly. Dash-everything was room 1. Swipe-to-cancel was tried on grubs and runners in room 2. Mixed handling was rooms 3–5.
- **Not observed:**
  - The middle of the room 5 session (roughly 10.5 s to 52 s) was cut from my output. I only saw its start and its last ~8 s.
  - I did not use the practice room.
  - I could not feel timing or controller feel. Everything below comes from printed frames and message lines.

### Session summary

| Room | Enemies at start | Result | Time | Hearts left |
|---|---|---|---|---|
| 1 | 3 grubs | cleared | 7.2 s | 3/3 |
| 2 | 2 runners, grub, brute | cleared | 9.8 s | 1/3 |
| 3 | 3 spitters, grub | cleared | 10.9 s | 2/3 |
| 4 | 2 spitters, grub, runner | I went down | 8.55 s | 0/3 |
| 5 | 2 spitters, 2 grubs, brute | not cleared | 60 s limit | 1/3 (brute left) |

### Concrete moments

**Room 1: very repetitive.**
- Each of the three grubs did the same thing. It crept toward me, stopped about 2 tiles away and reared back with a `~` line and a `cue:` line. I dashed aside, then swiped twice and it died.
- I was never touched, and I never needed to think after the first grub.
- Beats 2 and 3 looked identical to beat 1 on screen. The only differences were the direction and the distance.
- Reading the warning was easy, which is good. But three beats of "rears back → dash → two swipes" felt like one fight repeated.

**Room 2: the first room that felt different.**
- Runner:
  - The warning (0.35 s) was much shorter. At 1.72 s I swiped when it reared back, but it was too far away and the swipe missed.
  - The runner then lunged and hit me (3→2 hearts).
  - The second runner died to a swipe at 3.0 s without hurting me.
- Grub:
  - At 5.42 s a grub reared back about 2 tiles away. My first swipe missed (out of reach).
  - My second swipe at 5.92 s hit but did not stop the lunge, and I was hit at 5.95 s (2→1 hearts).
  - The message order made it look like I "hit it and still got hit". It was not clear to me why the swipe didn't stop it.
- Brute:
  - It felt different. It was slow, with a long warning and a long fight (4 swipes).
  - A swipe during its warning still said "shrugs off the swipe", which I understood, and dashing aside worked.
  - I finished the room at 1/3.
- This room had the most varied feel (runner, grub and brute each played differently).

**Room 3: spitters.**
- The aim cues were clear: a brightness percentage and seconds left, with a wide `~` band across the room. I mostly avoided them by stepping or dashing. Stepping aside worked about as well as dashing.
- The combat became crowded. Around 4.5–6.5 s there were 4–5 shots drifting around the screen, and I spent that stretch only dodging, not attacking. That stretch felt busy but passive.
- I was hurt only by a grub, once. I swiped a rearing grub at 8.12 s and was hit at 8.25 s anyway, the same "I hit it, it still hit me" confusion as in room 2.

**Room 4: the one I lost.**
- I was hit three times by shots and died at 8.55 s.
- Hit at 3.45 s: I had dashed left at 2.65 s and was still hit. The picture after the hit shows a shot far from me, so I **couldn't tell which shot hurt me or why my dodge didn't work**.
- Hit at 5.38 s: I was swiping a runner while standing inside the second spitter's glowing line at 97% brightness. That one I could explain: I stayed in the line.
- Hit at 8.55 s: I had dashed down at 7.65 s and was hit about a second later. Again I couldn't tell where that shot came from.
- Two spitters alternating across the room, plus a runner and a grub, kept me moving and left almost no time to attack. Frustrating, but it was the most tense room.

**Room 5: partial.**
- Early: the spitters alternated just like room 4. I took one shot hit (3→2), then a brute hit (2→1).
- The brute hit: I swiped it while it was rearing back ("shrugs off the swipe") and I didn't leave the lunge line. It hit me at 7.05 s. I understood why, but I'd been drawn into swiping a thing the cue had told me not to.
- At the end (about 52–60 s) only a brute was left. It rears back, I dash aside, it then stands a few tiles away and nothing happens for seconds. Nobody attacks. That was partly my rules (I only attacked within 1.5 tiles), but it was a long, empty tail.
- The session ended at the 60 s cap with the brute still alive and 1/3 hearts.

### Which situations felt alike, which different

- **Alike:**
  - Every grub encounter felt the same: warning, dodge, two swipes. This held in all five rooms.
  - Spitter rooms (3, 4, 5) all felt like "step out of the line, step out of the line".
- **Different:**
  - The runner (short warning, hard to answer by swiping) and the brute (slow, long fight) each felt distinct.
  - The spitter rooms felt different from the grub rooms. Inside them, though, the individual dodge felt repetitive.

### Could I tell why something hurt me?

- **Usually yes**, for grubs, runners and brutes. A hurt always followed a visible warning, and in most cases I could see I was standing in the line.
- **Mixed** in the grub "I swiped and still got hit" cases: it was not obvious from the frames why the swipe didn't cancel.
- **No**, for two of the three shot hits in room 4. I couldn't tell which shot hit me, because the frame showed none near me.

## Issues with impact

1. **Grub encounters feel identical (high impact in room 1, medium elsewhere).** Warning → dodge → swipes, over and over. Attention dropped after the first grub.
2. **Shot hits in room 4 were unclear (high impact).** I died without being able to tell which shot hit me or why.
3. **Swipe-and-still-hit (medium).** Swiping a rearing grub, and the brute once, then still being hit.
4. **Spitter rooms are mostly dodging (medium).** I had little time to attack, and the screen got cluttered with shots.
5. **Brute tail in room 5 (low–medium).** Long periods of standoff with little happening. Part of this is my script's limits.

## Positives

- Warnings were readable (`~` lines and `cue:` text), and nothing hurt me without one.
- The brute and the runner each felt distinct from the grub.
- Room 4 was the most tense.
- Rooms 1–3 were quick (7–11 s), which fits short runs.

## Open player questions

- What exactly makes a swipe cancel a rear-back, and when does it not? I couldn't read it from play.
- In room 4, which spitter's shot was I hit by each time?
- Is there anything to do in a fight besides "dodge, then swipe"?

## Decisions already made

None.

## Constraints

Observations only. No design opinions or numbers are presented as fact.

## Open questions

None.

## Expected output

Routing is the Studio's decision. The experience issues above (repetition, unclear shot hits) are the kind that go to `game-designer`; the "swipe landed but I was still hit" cases may be worth `qa` if they look broken.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/83-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-combat-monotony/86-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 86
from: qa
to: studio
stage: Verify
outcome: done
---
# 86: qa → studio — Room 3 timed checks R3-8 and R3-4 on build 1ac4d04d0e75: no defect; R3-8 passes at 30 FPS only, so the verdict is not a full pass

## Task

Report the two room 3 checks left unrun by report 82 (R3-8, and the room 3 part of R3-4). Both were run at 30 and 60 FPS and judged against `design/combat-step72.md`.

## Context

Goal G-001. Report 82 found the suite green (64/64) and no defect. I used two trace rounds of the build, with no code or document changed. Round 1 was a still-player trace of room 3. Round 2 was an approach trace plus a reaction-rule playthrough that kills everything. Both rounds ran at 30 and 60 FPS. I used no further round.

## Findings

### Verdict

- **No failing criterion and no build defect found.**
- **Not a full pass.** R3-8 passes at 30 FPS but is not shown at 60 FPS. R3-4 is only partly observed in room 3 itself. Details are below, and the Studio decides how to close them.

### Scripts (rerunnable; `python3 play.py --view trace {script}`)

- **still** (`room 3`, `fps 30|60`, `end 14`): a player who does nothing.
- **approach** (`room 3`, `fps 30|60`, `0 move right`, `end 5`): the player walks to the east wall (15,4).
- **rules** (`room 3`, `fps 30|60`, no `end`), reaction rules in this order:
  ```text
  when see * coming within 2 then dash aside
  when see g within 1.4 then attack
  when see g within 20 then move toward
  when see s within 1.4 then attack
  when see s within 20 then move toward
  ```

### Measured geometry

- The player starts at (8, 4).
- Without moving, the grub walks in from (15,0). It is within 2 tiles of the player at 6.083 s at 60 FPS and 6.100 s at 30 FPS.

### R3-8 (timed finish of the last spitter)

- **Geometry:** the largest spitter distance is 9.43 tiles, within 9.5. This is unchanged from report 82. Pass.
- **30 FPS timed run (rules script): pass.**
  - Spitter (10,6) died at 1.067 s and the grub at 8.467 s.
  - Spitter (2,1) died at 11.567 s.
  - The last spitter, (2,7), died at 13.933 s, which cleared the room.
  - From the previous kill to the clear: **2.37 s**, against the limit of 6 s. This is consistent with the derived ~3 s.
  - The kill order differs from the handoff's grub-first order. The run killed the grub and two spitters before the last spitter, as R3-8 requires. A reaction script walks "toward" the nearest enemy, not in a straight line, so this is a looser walk than R3-8 describes.
- **60 FPS timed run (rules script): not shown.**
  - Kills were spitter (10,6) at 0.983 s, spitter (2,7) at 4.950 s, and the grub at 10.867 s.
  - The last spitter, (2,1), was not reached. The rules kept dashing the player away ("dash aside" to the right, 4.9 to 8.6 tiles away from it), and shots killed the player at 15.683 s.
  - That is 4.8 s after the previous kill, which is not a measurement against the 6 s limit. It is a limit of the reaction script, not of the layout, so I do not call it a failure.
  - A deterministic walk-and-swipe script (timed from this trace) is still needed for 60 FPS.
- **Result:** R3-8 passes at 30 FPS. At 60 FPS it is **unverified** (geometry only).

### R3-4 (the grub's criteria in room 3)

| Case | 30 FPS | 60 FPS |
|---|---|---|
| Cue ≥0.5 s before the hit | wind-up 2.567 s, lunge 3.067 s, hit 3.267 s (approach): pass | wind-up 2.550 s, lunge 3.050 s, hit 3.233 s: pass |
| Swipe cancels the wind-up | not seen in this round (report 76 saw it) | wind-up 7.633 s, swipe 7.683 s: stagger, grub hp 2→1, no lunge: pass |
| Dash during or around the cue and lunge | dash at 6.5 s, 0.1 s before the lunge (6.3–6.6 s) ends: hearts stayed 3, but I cannot say the lunge would have reached the player | dash at 10.283 s, 0.033 s before the lunge: hearts stayed 2 through the lunge: pass. Dash at 8.333 s during a wind-up, ending off the lane: hearts stayed 3 |
| Recovery is safe, and a swipe in recovery works | not observed | grub in recovery after 10.617 s: no damage, swipe at 10.867 s killed the hp-1 grub: pass |
| Sidestep within 0.4 s of the cue (a pure 1-tile sidestep) | **not observed** in room 3 | **not observed** in room 3 |
| Two swipes kill it | report 76 saw it; not repeated here | the grub took one swipe at 7.683 s (hp 1) and another at 10.867 s (killed): pass |

- **Blocked lunge (criterion 21), seen in room 3 at 60 FPS (approach).**
  - Wind-up 4.050 s, shot hit at 4.250 s, lunge from 4.550 s while the player was in the hurt window (until 5.050 s).
  - Hearts stayed 1, so the lunge did no damage.
  - At 30 FPS the same pattern shows the shot hit at 4.233 s and hearts staying 1 through the lunge at 4.600 s.
- **Result:** R3-4 holds wherever it was observed in room 3.
  - The pure sidestep in room 3 and the 30 FPS cancel and recovery swipe are not observed here.
  - Report 82 covers those cases in the practice room, where they pass at both rates (`GrubTest`, `LungeContactTest`).
  - They stay **unverified in room 3 itself**.

### Other room 3 criteria seen in the still-player traces (both rates)

- **R3-2:** the first shots are at 1.800, 2.600 and 3.400 s. Each cue starts 0.6 s before (1.200, 2.000, 2.800 s). Pass.
- **R3-3:** the first wind-up is at 6.083 s (60 FPS) and 6.100 s (30 FPS), at least 4.0 s. Pass.
- **R3-6:** cue starts match the no-grub schedule above, and the grub's first lunge comes after them. The shots in flight never exceeded 3. A direct run without the grub was not made.
- **R3-7:** the room cleared only after all four enemies were dead (30 FPS, 13.933 s).
- **R3-9:** `a grub rears back` appears as the `windup` event (see the traces), so `text "rears back"` matches.

### Design observation (not a defect)

A player who stands still at the start (8,4) loses all 3 hearts to spitter shots at 3.4, 5.5 and 6.3 s, before the grub's first lunge at about 6.6 s. The grub only matters for a moving player. This is for the playtest (D-012 open question 3).

## Decisions already made

D-007, D-011 and D-012 applied as written. None changed.

## Constraints

Checked at 30 and 60 FPS. No code or document changed. Verified from the specs, criteria and traces. Criteria I could not judge are reported as unverified, not passed.

## Open questions

1. Close R3-8 at 60 FPS and the room 3 sidestep/cancel cases by accepting them as unverified, or route one more QA round? A further round needs deterministic timed scripts built from the traces above.
2. The Studio must still route the stray `</parameter>` line at the end of D-007 and the four wording items from report 82 (section 4). Nothing in this round changes them.

## Expected output

The Studio decides routing. There is no failure, so nothing goes to `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, repo/manual.md, repo/bots.py, repo/tests/test_game.py, design/combat-step72.md, design/combat-step-46-room3-cap.md, design/combat.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/84-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/67-game-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 67
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 67: game-director → studio — Review pass 2 on build 0.6.1: goal not met yet, but the gap is narrow and inside D-001. No Owner escalation. Build the D-008 message and manual text now; Design gets a room 3 content question.

## Task

Route the Review result. Verdict: **goal-not-met**, moderate confidence. The remaining gap is design content inside D-001 and the pillars. The Owner escalation named in D-009 is **not** needed. Decision D-010 records this.

## Context

Goal G-001. Success condition: different situations call for noticeably different play (positioning, timing, attack, dash), and the player can tell why. Pass 1 (60, D-009) asked for a variant-aware playtest. It is done (63, build 0.6.1, scripted, six sessions, rooms 1–5), and QA (64) closed the 30 FPS gaps with no defect. I ran no `play` or `bots` this step.

## Findings

### Verdict

**Goal-not-met, with a much smaller gap than at pass 1.** The main suspicion in D-009 is mostly cleared: the differences the build was changed to create do show up when the player plays them separately. Two things keep me from calling the Goal met: one room is still flat for a long stretch, and the "can tell why" half is only partly met in the text view.

### Evidence that the intent is met

- **Enemies ask different things.**
  - Grub and runner: "step aside or swipe first". For the runner, the 0.35 s warning makes acting early matter more.
  - Brute: "step aside; a swipe will not stop it". The tester called it the first time a swipe cannot stop the warning.
  - Spitter: "cross or dash the aim line, or close in".
- **Rooms 4–5 hold attention.** Several asks overlap, the tester had to choose which to answer first, and attention stayed high through room 5. This is the strongest evidence for the Goal.
- **Readable threats.** Warnings always came before damage. QA 64 confirms the warnings, cue lines and messages match the design at 30 and 60 FPS, with no defect.
- **Cost of ignoring cues.** The fast run in room 2 lost to the brute because the script had no brute rule. That is the design working as intended, and it is not evidence of failure.

### Evidence that it is not met yet

- **Room 3 (spitters only).** The tester called it the most repetitive stretch: about 20 s of "aim, dash, shot lands behind me, again", with attention dropping. The single ask is the content gap. Only the tester's own choice of killing two spitters and leaving the third in a far corner made the standoff last that long, so part of it is script behaviour. It matches the cautious-play standoff in 53, and I treat it as real but not severe.
- **Room 1** offers one kind of ask. The tester rated this low impact, and it is a teaching room. I do not act on it.
- **Rooms 3 → 4 → 5** differ mostly in how many things overlap, not in what each thing asks (the tester's summary). Variety comes from overlap more than from distinct asks. That is acceptable under D-001, since depth is meant to come from positioning and enemy behaviour. It means variety outside rooms 4–5 is thin.
- **"Can tell why" is partly unmet.** The message line reads "a grub rears back" and "hit by a grub" for runner and brute, and only the `cue:` line names the enemy. The tester was confused by a brute hit that read as a grub hit. This is a clarity gap that D-008 already proposes to fix.

### D-009 escalation condition: not triggered

The condition was that the melee enemies still read as one answer, with runner, standard grub and brute not told apart, or the brute only kited.
- The brute **was** told apart from the grub and runner.
- The runner and the standard grub share an answer, but they differ in time pressure. That was designed (D-008 says so).
- The brute loop in the slow room 2 run (about 8–27 s, six or seven dodges, never punished in the recovery) was partly caused by the tester's rules. The tester said so, and their rules never hit the brute in its recovery window. This is the D-004 trigger "human dodges the brute without fighting it". It is not confirmed on scripted evidence, so Option 3 (a spitter in room 2) stays deferred.

So there is no Owner question. A new melee behaviour or enemy type, healing, or an input change is not needed on this evidence.

### Confidence and limits

- Confidence in "not met, narrow gap": moderate. Confidence that no Owner decision is needed now: fairly high.
- All play was scripted. The tester could not feel the pad, reaction rules ran on a 0.15 s grid, and three outputs were cut at about 19–27 s. The 30 FPS run was room 3 only, with no frame-rate difference seen (QA 64 covers it).
- A human check would add what scripts cannot: whether room 3 and the brute loop feel flat to a person, whether a person understands the brute's no-flinch rule without the manual, and whether the shot clutter in rooms 4–5 feels unfair (the tester expected some hits would). I recommend one short live check after Build 21, as the closing evidence, not as a new Diagnose.

## Next issues

1. **Room 3 has a single ask** (inside G-001, Design). Ask `game-designer` for room-content options inside D-001, using existing enemies only. Room 3 should offer a second kind of ask, or avoid a long standoff against one cornered spitter, without breaking criterion 11 or the room 3 cue timing that teaches the aim cue. This is design content. It is not an Owner choice.
2. **Variant names in the wind-up message and the manual late-swipe text** (clarity, "can tell why"). Build now, see below.
3. **Room 3 in-flight count vs D-007 (66, non-blocking).** I do not decide it here. The tester read room 3 volleys as readable and took no hit in the 26 s seen. QA's conflict is about which stated rule governs, and that is the Design call. If Design changes the room 3 cap or the cue rule, bundle it with issue 1 so one room 3 change is built and checked once.
4. **Brute loop and the "dodge without fighting" trigger (D-004).** Not confirmed. Watch it in the human check. Option 3 stays the first lever.
5. **Proposed new Goal at Close:** visual criteria V1–V11 need a graphical build, and V12 stays open.

I do not ask for another Diagnose. There is no new cause. The remaining questions are about content and wording, and a human check.

## Answer to question 3: build D-008 and the manual text now

Build 21 should carry the D-008 variant-named message (`a grub`, `a runner`, `a brute rears back`) and the manual late-swipe wording from 59. Reasons:
- D-009 item 5 kept the message out of the playtested build to keep the comparison fair. That playtest is done, so the reason to wait is gone.
- Clarity is half of the success condition ("the player can tell why"), and the tester hit it directly.
- The change is small, reuses the existing message system, and keeps the substring `rears back`, so reaction scripts still work. `game-designer` stays the owner of the wording and acceptance criteria (`design/combat-step59.md`).
- The message change should not wait for the room 3 Design answer. They can be built together if Design is ready in time. If not, ship the message and manual text first and Verify them, and do the room 3 change in a later build. The next playtest must state which build it used.

Treat D-008 as ready to build. Because D-008 is `proposed` and written by the Designer, the Studio should mark it accepted once Build 21 is routed (D-010 records that I do not object).

## Decisions already made

- D-001: one-button combat. Respected; nothing here needs a new input.
- D-004 to D-007: stand. D-007 is touched only by QA's non-blocking question (66), which is Design's call.
- D-008 (proposed): now cleared to build (see D-010).
- D-009: its escalation condition was checked and is not triggered. The "revisit when" items "cannot tell runner, standard grub and brute apart" and "stalls against the brute" are not reached on this evidence.
- New: **D-010** (this step).

## Constraints

- Stay inside D-001 and the pillars. A new enemy type, healing, or an input needs the Owner, and nothing here needs it.
- New issues become proposed Goals unless they serve "the player can tell why" or the room 3 variety gap named above.
- Evidence stays scripted until a human check is done. Weigh the next report that way.

## Open questions

For `studio` (routing):
1. Route Design for room 3 (issue 1), together with the existing 66 question.
2. Route Build 21 (message and manual text), then Verify (QA).
3. After Build 21, one playtest of the new build, ideally a live player or a hand-timed run, with room 3, the brute in room 2, and the brute hit message as checks. Then Review pass 3. If the melee reads as one fight in that pass, escalate per D-009; otherwise the Goal can be met or partially-met with the reasons stated.

## Expected output

The Studio routes Design (room 3), Build 21 and Verify, then a final playtest and Review pass 3. No Owner escalation is drafted: the trigger is not met.

## Sender assessment

Verdict confidence is moderate because the evidence is scripted. I weighed the playtester's own admissions that the room 2 brute loop and the fast-run deaths came from their rules. I counted the room 3 standoff as real because the same standoff was reported in 53, in a different script. I did not run the build.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, goals/G-001-combat-monotony/goal.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
- Previous handoff: goals/G-001-combat-monotony/65-studio-to-game-director.md
>>>END

<<<FILE decisions/D-009-review-next-pass-variant-aware-playtest.md
---
kind: decision
id: D-009
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-009: After build 0.6.1 the next pass is a variant-aware playtest, not a third Diagnose; no Owner escalation yet

## Decision

1. G-001 is **not met** on build 0.6.1 (handoff 60). The "rooms feel alike" report in playtest 53 is not accepted as a settled design finding, because the scripts used one answer for every lunger and one run had no brute rule at all.
2. The next pass is a fresh playtest of the unchanged build 0.6.1. The player writes separate rules per enemy mark, plays rooms 1–5 including a slow run, and keeps the output short enough not to be truncated. The brief does not describe the design. No third Diagnose is run on the existing scripted evidence.
3. No direction change now. D-001, the pillars, D-004 to D-007 stand. Option 3 (a spitter in room 2) stays deferred but is the first lever if the stall is confirmed.
4. **Owner escalation condition.** If the variant-aware playtest still reports that the melee enemies ask for one answer (runner, standard grub and brute not told apart in play, or the brute only kited), the next Review does not send the Goal to Diagnose. The game-director prepares an Owner escalation (in Japanese) on adding a genuinely different melee behavior or enemy type, healing, or another change that touches D-001 or the pillars. Room content changes such as Option 3 do not need the Owner.
5. The manual wording on late swipes and a per-variant cue message (step 58) are accepted as in scope, as "the player can tell why". Their detail is the designer's. The playtested build must be stated, and a message change should not be mixed into the same pass without saying so.

## Rationale

- A third Diagnose on the same scripted evidence would repeat 04 and 31 without new information. The loop limit exists for this.
- The cheapest explanation that fits the evidence is that the test did not exercise the intended differences: uniform rules per cue, no brute rule in room 2 aggressive, and a "move away" rule that produced the 10 s stall. That has to be ruled out before changing direction.
- Escalating now would ask the Owner to approve new content on evidence that may be an artifact of the test method.
- The one run with a brute-specific choice (room 5 aggressive) was called interesting, and room 3 showed distinct styles. So the direction is plausible and not shown to have failed.

## Alternatives considered

- **Third Diagnose:** no new evidence; rejected.
- **Escalate now for a new enemy type or healing:** premature, and a cost to the Owner on weak evidence; rejected.
- **Declare goal met or partially-met and close:** the tester's report says rooms feel alike and cautious play stalls, and the deciding case is untested; rejected.
- **Take Option 3 (room 2 spitter) now:** would change room 2 before knowing whether the brute rule works for a human, and would make the next result impossible to attribute (this was the reason for deferring it in D-004); rejected for now.
- **Bundle the cue message change with the playtest build:** would confound the result; not chosen.

## Revisit when

- The variant-aware playtest report arrives (next Review).
- The tester still stalls against the brute or kites it with no reason to fight: take Option 3 or a room change.
- The tester cannot tell runner, standard grub and brute apart in play: apply item 4 (Owner escalation).
- Step 58 changes the cue message, so the playtested build changes: state the build and re-check that the comparison is fair.
- A graphical build exists: re-judge variant readability, since silhouettes replace the text message.
>>>END

<<<FILE decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
---
kind: decision
id: D-010
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-010: Review pass 2 — goal not met yet, no Owner escalation; build the variant message and manual text now; room 3 variety goes to Design

## Decision

1. G-001 is **not met** on build 0.6.1, with moderate confidence. The gap is narrow: room 3 offers a single ask and repeats for about 20 s, and the text-view messages for runner and brute read "a grub". Rooms 4–5 and the brute and spitter asks are varied and engaging in the variant-aware playtest (63).
2. The D-009 Owner-escalation condition is **not triggered**. The brute was told apart from the grub and runner. The slow room 2 brute loop is partly caused by the test scripts, so the D-004 "dodges without fighting" trigger is not confirmed. No Owner decision is needed; nothing touches D-001 or the pillars.
3. **Build now (Build 21):** the D-008 variant-named wind-up message, and the manual late-swipe wording from step 59. D-008 may be treated as accepted when Build 21 is routed. The playtest that needed a stable build is complete, so D-009 item 5's reason to wait has ended. The next playtest must state its build.
4. **Design (room content, inside D-001):** `game-designer` is asked for options to give room 3 a second kind of ask or to avoid the long single-spitter standoff, using existing enemies. It must keep criterion 11 and the aim-cue timing that room 3 teaches. It may combine this with the open room 3 in-flight question (66). Option 3 (a spitter in room 2) stays deferred.
5. No third Diagnose. After Build 21 and the Design answer, one more playtest (live or hand-timed if possible) feeds Review pass 3.

## Rationale

- The variant-aware playtest tested the differences the build was changed to create, and they were found: rooms 4–5 held attention, and the brute and spitters each asked something new. That removes the main reason to suspect the melee redesign failed.
- Variety outside rooms 4–5 is thin, but adding a second ask to one room is cheap content, inside D-001, and does not need the Owner.
- "The player can tell why" is half the success condition and the tester hit the unclear message directly. The fix reuses the message system and keeps `rears back`, so scripts keep working.
- All evidence is scripted. A human check is the proportionate next evidence, not more analysis.

## Alternatives considered

- **Declare the goal met:** room 3 and the message clarity gap are real, and no human has played. Rejected.
- **Escalate to the Owner now:** the condition in D-009 is not met and the cheaper content fix is untried. Rejected.
- **Take Option 3 (room 2 spitter) now:** the brute stall is not confirmed, and it would change room 2 without evidence. Rejected for now.
- **Third Diagnose:** no new cause. Rejected (loop limit).
- **Wait on the message change until after the room 3 change:** needless delay. Build 21 may carry the message and manual text alone.

## Revisit when

- The next playtest still shows the melee reading as one fight, or the brute only kited: apply D-009 item 4 (Owner escalation).
- A human still reports a flat room 3 after the Design change: consider a larger room change or Option 3.
- The new message still leaves the player unable to tell what hit them: reopen the text-view clarity question.
- A graphical build exists: re-judge variant readability.
>>>END

<<<FILE decisions/D-011-variant-named-messages-accepted.md
---
kind: decision
id: D-011
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: D-008
---
# D-011: Text-view wind-up and hit messages name the variant (accepted); swipe timing stays a wording matter

## Decision

1. The wind-up messages are `a grub rears back`, `a runner rears back` and `a brute rears back`. The hit messages are `YOU ARE HIT by a grub`, `by a runner` and `by a brute`. The shot message stays `by a shot`. The strings and acceptance criteria V-a to V-e are in `design/combat-step68.md`.
2. This completes D-008, which left the hit message out. Playtest 63 showed the hit message was the other half of the confusion.
3. No swipe-timing rule change. The late-swipe manual wording from step 59 is specified in `design/combat-step68.md` and is ready to build.
4. The change is player-facing wording within the designer's authority. It adds no input (D-001), no timing change and no new information beyond the existing `cue:` line, so it stays inside the "readable threats" pillar.
5. Build only after Review 65. It must not be mixed silently into a playtest pass of 0.6.1 (D-009 item 5): hold it until after any further 0.6.1 playtest, or state the new build number in that brief.

## Rationale

- A text-view player sees the message line first. A brute or runner reported as "a grub" hides which answer applies, and playtest 63 rated this medium impact on clarity.
- Naming the variant gives the text view the early information the graphical build gets from silhouette and size. It changes no timing or hit points.
- The shared words `rears back` keep existing reaction rules working.
- Wording alone explains the two reported late-swipe hits (QA 56). A grace period or larger reach would let a swipe cancel a started lunge and weaken "step aside or dash".

## Alternatives considered

- Keep one message for all variants: leaves the playtest confusion, and reaction-script players must parse the `cue:` line.
- Put distance and time left in the message: duplicates the `cue:` line and may make the text view easier than the graphical build.
- Wind-up renames only: leaves a brute hit labelled "a grub".
- A swipe grace period or a larger wind-up reach: needs a rule change with no defect behind it.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after the rename.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text messages irrelevant.
>>>END

<<<FILE decisions/D-012-room3-standard-grub-and-closer-spitter.md
---
kind: decision
id: D-012
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-012: Room 3 gets one standard grub at (15,0) and its second spitter moves to (10,6); cap and cue rule unchanged

## Decision

1. Room 3 contents become: spitters at (2,1), (10,6), (2,7) in that order, plus one standard grub at (15,0). Nothing else in room 3 or elsewhere changes.
2. D-004 to D-007 and D-011 stand. The cap, the cue rule, the 0.8 s offset and the 1.8/2.6/3.4 s first-shot schedule are unchanged. The D-007 in-flight bound (up to 2 plus the living spitters) is unchanged.
3. The room 3 purpose line becomes "learn the aim cue first, then answer an aim line and a lunge lane together".
4. If the grub's first wind-up in a still-player trace is earlier than 4.0 s, the grub's position is retuned by the designer without a new spec step.
5. Spec and criteria: `design/combat-step72.md` (R3-1 to R3-10).

## Rationale

- Room 3 has a single ask. A grub gives a second, different ask using an existing enemy and existing systems, inside D-001.
- The grub walks in from the far corner, so its first lunge comes after the spitter cues are taught, with no new spawn system.
- It also pressures a player who stands off to dodge a lone spitter, and the spitters are now closer together, so the last one is a short walk away.
- It touches no spitter timing, so the cue rule and cap need no change and one room 3 change is built and verified once.

## Alternatives considered

- **A runner instead of the standard grub:** the 0.35 s warning on top of 0.6 s aim cues is too harsh for the teaching room, and runners are already in rooms 2 and 4. Not chosen.
- **A brute:** adds a long fight to a teaching room. Not chosen.
- **Replacing a spitter with a grub:** changes the verified 1.8/2.6/3.4 s schedule and the in-flight bound. Not chosen.
- **The 0.2 s cue gap in room 3 (D-007 fallback):** does not give a second ask, and changes a verified room. Not chosen.
- **Reinforcements, a lone-spitter speed-up, healing, or any new enemy:** new systems or enemies, outside this step. Not specified.

## Revisit when

- A playtest still shows a long single-spitter standoff or a flat room 3: try a runner in place of the grub, then a second grub, then a larger room change (D-010 revisit).
- A playtest shows the grub overloads the room while the cue is being taught: move the grub later.
- The bots measured on the Build leave criterion 13 or 15 outside its limits for a reason that is design, not bot policy.
- Any change to the cap, the spitter interval or the room 3 schedule (also a D-007 reopen).
>>>END

<<<FILE goals/G-001-combat-monotony/90-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 90
from: qa
to: studio
stage: Verify
outcome: done
---
# 90: qa → studio — Room 4 shot hits and "swiped, still hit" on build 1ac4d04d0e75: no defect; two readability gaps; room 3 timed items (C) stay unverified

## Task

Judge two player-reported experiences (A: room 4 hits, B: "swipe landed, still hit") and make a last attempt at the open room 3 timed items (C). Everything was run at 30 and 60 FPS where noted.

## Context

Goal G-001. Report 88 is the playtest. I used one run round (three trace/play runs of room 4, with reaction rules like the player's). No code or document was changed. I spent the round on A and B, so C was not run (see below).

## Findings

### Verdicts

| Item | Verdict |
|---|---|
| A. Room 4 hits | **No defect found.** The player's three hits were **not reproduced** (script not kept, so my rules differ). Dash invulnerability matches the design. **Readability failure (confirmed in the player view):** a shot hit gives no source and the shot disappears at the hit. |
| B. Swipe landed, still hit | **Matches design.** Reproduced at 30 FPS in room 4. **Readability failure:** no line says why the lunge was not cancelled. |
| C. Room 3 timed items | **Unverified** (no run this round). Goes to Review as a known gap. |

### Scripts (rerunnable; `python3 play.py --view trace|player {script}`)

Room 4, run at `fps 60` and `fps 30` (trace) and `fps 60` (player view):

```text
room 4
fps 60
when text "takes aim" then move aside
when text "rears back" then dash aside
when see * coming within 2 then dash aside
when see g within 1.4 then attack
when see r within 1.4 then attack
when see g within 20 then move toward
when see r within 20 then move toward
when see s within 20 then move toward
```

This follows the player's stated rules, but it is not the player's exact script. Its output was partly cut (the 60 FPS trace between about 14 and 19 s). Anything I say about those parts is not claimed.

### Item A

**What I could not reproduce.** The player's hits at 3.45, 5.38 and 8.55 s did not occur in my runs.
- 60 FPS: no hit in the visible part before about 14 s.
- 30 FPS: the first hit was at 6.300 s.

I tried the player's rules as written, at both rates. Because the exact script was lost, the three specific hits are open, not disproved.

**What the runs do show.**

1. **Dash window is correct.**
   - Every dash in the traces shows `dash_left=0.233` at the first frame (60 FPS) or 0.217 (30 FPS), `invulnerable=True`, and `invulnerable False` at `dash_end` about 0.25 s later.
   - No damage was taken during any dash (design: 0.25 s, `combat.md` Player kit).
   - A hit 0.8 s after a dash is therefore not a defect by itself.

2. **A hit after a wasted dash (30 FPS, 6.300 s, source: grub).**
   - The dash was at 5.467 s and ended at 5.700 s.
   - The grub began its wind-up at 5.667 s, lunged at 6.167 s and hit at 6.300 s, 0.6 s after the dash ended.
   - The dash came too early for that lunge. The cue was shown for the full 0.5 s.

3. **Shot hits in my runs were point-blank.**
   - The 30 FPS hits at 9.800 s and 13.000 s, and the 60 FPS hits at 23.200 s and 25.800 s, happened on the same frame as "a spitter spits".
   - In each, my rules had walked the player next to the spitter: the 30 FPS hits had the player at (15.00, 0.00) and (14.60, 0.00) next to the spitter at (15, 0), and the 60 FPS hits had it at about (14.9, 8.0) next to (15, 8).
   - My rule set has no swipe-at-spitter rule, so this is an artifact of my script, not a finding.
   - The aim line and the `cue:` line were shown for the full 0.6 s before each of these. Pass for readability of the cue.

4. **The hit message gives no source (player view, 60 FPS).**
   - The line is `YOU ARE HIT by a shot — hearts 1/3` at 23.200 s and the same at 25.800 s.
   - It does not say which spitter fired.
   - The frame after the hit shows no shot at the player. In the 23.20 s and 25.80 s frames the `*` marks seen are other shots, far away.
   - By the design, a shot that makes contact is consumed and disappears (`combat.md`, Shot and Blocked contact). So a post-hit frame can never show the shot that hit.
   - Shots take about 1–4 s to cross, so several `*` are on screen, and none of them is marked as the one that hit.

**Hypothesis, not confirmed.** The player's hits at 3.45 s and 8.55 s were 0.8 s and about 0.65 s after the player's dashes ended. Both are consistent with shots already in flight when the dash ended. For example, the first room 4 shot is fired at 1.8 s from the far corner and takes about 3 s to reach the middle of the room, so it can arrive at about 3.4–4 s. A 0.25 s dash only protects the player for the dash itself. I could not match these to a particular shot without the original script.

**Verdict A.** No defect; dash invulnerability matches the design. The player's hits could not be reproduced. The inability to tell which shot hit is a **readability failure** (the build matches the design; the player view does not show the cause).

### Item B

**Reproduced (30 FPS, room 4, trace).**
- The grub's wind-up began at 5.667 s and its lunge at 6.167 s.
- A swipe at 6.267 s hit it (`grub hp 2→1`, `attack hits [('grub','hit')]`), and the player was hit at 6.300 s (hearts 3→2).
- The swipe landed 0.1 s after the lunge began and did not cancel it. The lunge continued and the grub went to recovery at hp 1.
- This matches the late-swipe rule in `combat.md` (a swipe cancels only during wind-up) and the manual ("A swipe that lands after the lunge has begun does not cancel it").
- Cancel does work in wind-up (seen in report 86 at 60 FPS, 7.683 s).

**Reports from the player (derived, not reproduced).**
- Room 2 (swipe 5.92 s, hit 5.95 s): the cue began about 5.42 s (the first swipe at 5.42 s was out of reach), and a 0.5 s wind-up ends at about 5.92 s. The swipe came at or just after the lunge start, and the hit followed one frame later. This is consistent with the boundary.
- Room 3 (swipe 8.12 s, hit 8.25 s): the hit is 0.13 s after the swipe, inside the 0.3 s lunge. This is consistent with a swipe after the lunge started.
- Room 5 brute: by design (`the brute shrugs off the swipe`).

**Messages.** In the player view the order reads as a swipe result ("you swipe: …") followed by "YOU ARE HIT by a grub". In the output I could see, no line says that the lunge had already started or that the swipe was too late. The `cue:` line and the `~` lane also stop at the lunge start (the design allows this). Only the brute has a "shrugs off" line. I did not see the full player-view output of the 6.267 s case, so this is based on the visible player-view lines and the design text.

**Verdict B.** Matches design. **Readability failure:** the player view has no line that says why the swipe did not stop the lunge.

### Item C (unverified)

I did not run any room 3 script this round. I used the round on room 4, and room 3 needs a new deterministic script. Nothing here is a failure.

| C item | Status |
|---|---|
| R3-8 at 60 FPS | **Unverified.** The 30 FPS result stands (2.37 s against 6 s, report 86). At 60 FPS the report 86 rules script was shut off by "dash aside" dashing away from the last spitter. |
| Pure 1-tile sidestep in room 3 | **Unverified in room 3.** Passes in the practice room (report 82, criterion 2). |
| 30 FPS cancel and recovery swipe in room 3 | **Unverified in room 3.** Cancel was seen at 60 FPS, and at 30 FPS only in report 76. |

For whoever picks this up in Review, an untested starting point for R3-8 at 60 FPS is the report 86 rules with a narrower dash trigger and a swipe rule for spitters (`when see * coming within 1.5 then dash aside`, `when see g within 1.4 then attack`, `when see s within 1.4 then attack`, then the two `move toward` rules). It has not been run.

## Decisions already made

D-002, D-003, D-007, D-011, D-012 applied as written. None reopened.

## Constraints

No code or document changed. Claims are limited to what the traces show. The run output was partly cut, and the player's script was not available.

## Open questions

1. **For `game-designer` or Review (readability, not defects):**
   - (a) Should the hit message or post-hit frame identify the source of a shot (which spitter, or where it came from)? Today `YOU ARE HIT by a shot` carries no source and the shot vanishes at the hit.
   - (b) Should the text view say why a swipe did not cancel a lunge that has already begun (for example when a swipe hits a grub in its lunge)?
2. **Review:** record C as a known gap (R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe).
3. **Review:** the player's exact room 4 hits (3.45 s and 8.55 s) are not reproduced; a hand-timed playtest of room 4 is the check if this matters.

## Expected output

Studio routes. Nothing goes to `gameplay-engineer`. Readability items 1(a) and 1(b) go to `game-designer` or Review, and the open gaps to Review.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md, studio/skills/verify-change.md
- Project: project.md, repo/manual.md, design/combat.md, design/combat-step72.md, design/combat-cues-visual-spec.md, goals/G-001-combat-monotony/86-qa-to-studio.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/89-studio-to-qa.md
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
