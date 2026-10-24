# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/57-studio-to-game-director.md
next_seq: 60
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/60-game-director-to-<recipient>.md
- decisions/D-009-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-combat-monotony/57-studio-to-game-director.md
---
kind: handoff
goal: G-001
seq: 57
from: studio
to: game-director
stage: Review
outcome: routed
---
# 57: studio → game-director — Review G-001: is combat still monotonous? (second playtest and QA results)

## Task

Judge with `review-outcome` whether the Goal's intent is met on build 0.6.1: does combat play as varied and engaging rather than monotonous? Name the next issues. If the Goal is not met, say what the next pass should address, or whether a direction, priority or scope change is needed (new enemy type, healing, input, or any other change to D-001 or the pillars). Such a change is an Owner-level question; frame it as an escalation instead of deciding it.

## Context

Goal G-001, from the Owner: "戦闘が単調なので改善したい" ("combat is monotonous; I want to improve it"). Success condition (goal.md): different situations call for noticeably different play (positioning, timing, attack and dash) and the player can tell why. The change stays inside D-001 and the pillars.

History in short:

- A first playtest (02) found that melee enemies share one answer. Diagnose passes ran twice (04, 31).
- Design and Build followed (D-004 to D-007). Build 0.6.1 was verified by QA at 30 and 60 FPS (50).
- A second, fresh playtest (53, scripted at 60 FPS) reported that rooms still feel alike, that cautious play stalls, and that room 3 has simultaneous volleys.
- "Rooms feel alike" would be a third Diagnose pass without progress. The loop limit sends it to your review instead.

## Findings

From the second playtest (53), for you to weigh. Read the report itself:

- Rooms still feel alike.
- Cautious play stalls.
- Room 3 simultaneous volleys. The tester read them as readable, with no shot from nowhere and no count above 5, so the room 3 reopen triggers were not met (D-007).
- Three hits called unfair or unexplained.
- The same message for every lunger led the tester to waste dashes.
- Playtest limits: reactions were scripted, not live play, and four runs were truncated.

From QA (56) on the three hit moments:

- Not a defect, and the expected behavior is defined.
- Item 1 (room 2) and item 2 (room 5): the swipe landed after the wind-up had ended, because the grub was about 2 tiles away and out of the 1.5 reach during the whole wind-up. It hit during the lunge, which the design allows: a non-lethal swipe on a lunging grub does not cancel it.
- Item 3 (room 2, "no cue"): a cue was printed 0.48 s before the hit. The swipe at 5.0 s killed the other runner.
- Item 4: the message "a grub rears back" is the same for all variants, as documented. Whether the text view should name the variant is an experience question, and it is with `game-designer` (58).
- QA did not isolate the 30 vs 60 FPS course difference (a script timing effect, not a build defect under criterion 16). The player view at 30 FPS was not run.

Other state: tests pass (59). Visual criteria V1–V11 need a graphical build and are proposed as a new Goal at Close. V12 stays open until one exists.

## Decisions already made

- D-001: one attack button plus dash. No new input buttons without Owner approval.
- D-002 / D-003: contact-edge graze accepted; exact reach and lunge band.
- D-004: rooms 4–5 cue gap 0.6 s; the brute's wind-up is not cancelled by a swipe; room 2 spitter deferred.
- D-005: a blocked contact consumes the shot and spends the lunge's hit.
- D-006: walker limit in rooms 3–5 is 3–7 hearts.
- D-007: room 3 simultaneous cues accepted; criterion 11 reworded.

## Constraints

- Stay inside the vision pillars and D-001. A change to the core concept, a pillar or an Owner-made Decision goes to the Owner, not to you.
- Experience Goal: judge from the playtests and QA results in the Load list. Do not rely on any implementation explanation.
- Playtest evidence is scripted and limited, so say how much it supports your verdict.
- New issues become proposed Goals, not scope growth.

## Open questions

- Is the Goal met? Judge it against the success condition above, not the numeric criteria.
- If not met, which concrete next step: another Diagnose with specific findings, a Decide on a direction change, or an Owner escalation? Say why, given that two Diagnose passes did not remove the "rooms feel alike" report.
- A parallel Design step (58) is looking at manual wording on late swipes and the per-variant cue message. Note whether either belongs in your verdict.

## Expected output

A Review verdict (`outcome: goal-met` or `goal-not-met`) in a handoff addressed to `studio`, with reasoning, the next issues, and any Decision you record (templates/decision.md). If an Owner-level question arises, write the Escalation (templates/escalation.md) in `owner_language` (ja) instead, using `prepare-owner-escalation`.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md, studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, design/combat.md, repo/manual.md, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/53-playtester-to-studio.md, goals/G-001-combat-monotony/02-playtester-to-studio.md, goals/G-001-combat-monotony/31-game-designer-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/56-qa-to-studio.md
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

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE studio/skills/prepare-owner-escalation.md
---
name: prepare-owner-escalation
description: Frame an Owner-level question as concrete options with consequences, a Studio recommendation, reasoning, and what happens next under each option.
---
# Skill: Prepare Owner escalation

Typical roles: game-director, technical-director.

## When to use

An escalation trigger in `studio/orchestration.md` fires.

## Inputs

The question, the evidence so far, the options, the vision and Decisions involved.

## Method

1. State the question in one sentence the Owner can answer without reading anything else.
2. Name the trigger: why this is the Owner's decision and not the Studio's.
3. Give 2–3 options. For each: what it means for the game, cost, risk, reversibility, and the
   route the Studio will take if it is chosen.
4. Recommend one option and give the reasons, including what evidence would change the
   recommendation.
5. List what the Studio will do meanwhile (independent work that continues).
6. Write it in the project's `owner_language`, using `studio/templates/escalation.md`.

## Output

An Escalation file addressed to `owner`.

## Do not

Return a bare question. Do not hide the recommendation, and do not present it as already decided.
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

- Observe: done (scripted play, rooms 1–3 + practice room; 02). FPS divergence (qa): done (16, 20); the contact-edge graze is accepted (D-002, D-003). Spitter fire times: build conforms to its spec (36). The three hits the second playtest called unfair or unexplained: done (56), all match the design and the build, no defect (late swipes land in the lunge, out of reach during the wind-up; the "no cue" hit had a cue printed). Not covered by QA: player view at 30 FPS, the late-swipe boundary at 30 FPS.
- Diagnose: two passes done (04, 31). Melee enemies share one answer (S1, the core of the Goal); rooms 4–5 spitter crossfire was unfair (S4). The second playtest (53, scripted, 60 FPS) still reports rooms feeling alike, stalling cautious play, and room 3 simultaneous volleys. A third pass without progress goes to `game-director` review (loop limit), so these go to Review.
- Decide: skipped. All options so far are inside D-001 and the pillars. Tentative again (game-director) if a later step finds the need for a new enemy type, healing, new input, or a scope or priority change.
- Design: complete (35, 38, 44, 46; D-004 to D-007). Criterion 11d reworded (54): build 0.6 satisfies it. Open (18d, 58): manual wording on late swipes (a swipe cancels only during the warning, out of reach early in the wind-up) and whether the text-view cue message should name the variant. Non-blocking for Review.
- Plan: skipped (approach local, reuses the enemy update loop). Returns if the same criterion fails verification twice.
- Build: 0.6.1 done (48). A build change returns only if 58 proposes a message change.
- Verify (QA): pass on build 0.6.1 at 30 and 60 FPS (50). Visual V1–V11 need a graphical build, a proposed new Goal at Close; V12 open until one exists.
- Play: second pass done (53). Room 3 reopen triggers not met: the tester read the volleys as readable, no shot from nowhere, no count above 5. Playtest limits: scripted reactions, not live play; four runs truncated.
- Review: open (`game-director`, 57), experience Goal. The Goal is not yet met.

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
| 11 | Decide (if Design implies direction or scope change) | game-director | make-decision | tentative | — |
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
| 18d | Design (manual wording on late swipes; variant cue message; non-blocking) | game-designer | write-design-spec | open | 58-studio-to-game-designer.md |
| 19 | Review | game-director | review-outcome | open | 57-studio-to-game-director.md |
| 20 | Next | studio | — | planned | — |

## Route changes

After 18c (56): not a defect; the late-swipe hits and the "no cue" hit match the design (a cue was printed). Opened Review (57) with playtest 53 and QA 56, since "rooms feel alike" would be a third Diagnose pass. In parallel, non-blocking Design 18d (58): manual wording on late swipes and the per-variant cue message.

## Next action

Run two steps, in parallel: `game-director` with 57-studio-to-game-director.md (Review, result addressed to `studio`) and `game-designer` with 58-studio-to-game-designer.md (result addressed to `studio`). Then Route with both results. If 58 proposes a build change, route it to Build (`gameplay-engineer`) and Verify (`qa`), and tell Review whether the verdict still stands. If Review says goal-met, Close. If goal-not-met, apply the return rule (Diagnose again with Review's findings, or an Owner escalation if it finds an Owner-level question).

## Outcome

(open)
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

<<<FILE goals/G-001-combat-monotony/02-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: studio
stage: Observe
outcome: done
---
# 02: playtester → studio — Observation report on combat (rooms 1, 2, 3 and the practice room)

## Task

Report the player-visible experience of combat. Intended for `game-designer` (Diagnose) via the Studio's Route operation.

## Context

The Owner asked for a first-hand player observation of combat. I played as the profile describes: an action player who likes dodging and spacing and dislikes memorizing combos. I had no expectations to check.

## Findings

### Method (what I actually did)

- I did **not** play live. I played through input automation: reaction-rule scripts from the manual, run with `python3 play.py --view player`. I read the room drawings and the event log.
- Four sessions: room 1, room 2, room 3, and the practice room with one spitter.
- I could not see the feel of real-time play: animation, sound, hit feedback. I only saw half-second snapshots plus hit events.
- **Not played:** rooms 4 and 5, and any session where I deliberately timed inputs by hand.
- I tried one rule set per room, one attempt each. This is a thin sample.
- In the practice room my script was flawed. The "move toward" rule only triggered within 8 tiles, and the spitter was 9 away. I mostly stood still and only sidestepped shots. That session shows spitter shots, not a fair fight.

### Session summary

| Session | Enemies | Result | Time |
|---|---|---|---|
| Room 1 | 3 grubs | Killed 2, went down with 1 left | 4.7 s |
| Room 2 | 4 grubs | Killed 2, went down with 2 left | 5.6 s |
| Room 3 | 3 spitters | Killed 1, went down with 2 left | 14.5 s |
| Practice | 1 spitter | Never reached it, went down | 10.1 s |

I won none of the four. Each time I lost all 3 hearts.

### Concrete moments

**Grubs, room 1**
- 0.9 s: swipe, "grub hit". The grub survived.
- 1.37 s: "YOU ARE HIT by a grub." 1.68 s: swipe, grub defeated.
- 2.38 s: swipe, "grub hit". 2.63 s: hit again. 2.98 s: defeated.
- 3.0–4.3 s: one grub left. I walked toward it for about 1.3 s with nothing happening.
- 4.27 s: swipe, grub hit. 4.68 s: it hit me and I went down before my second swipe.
- Each grub took two swipes, and nearly every grub landed a hit on me. I felt I was trading hits, not avoiding them. I never dodged a grub and had no clear window to do so.

**Grubs, room 2**
- It felt like room 1 with one more grub.
- 1.35–3.3 s: swipe, get hit, swipe, kill, then repeat.
- 3.3–5.3 s: more walking toward slow-closing grubs, then another trade at 5.3 s. A hit at 5.63 s ended the run.
- My loop here was walk toward, swipe, swipe, take a hit.
- I saw no difference in how grubs behaved between rooms 1 and 2. They just walk straight at me.

**Spitters, room 3**
- This was the only session with real tension and decisions.
- Each spitter fires every 2 s, so a volley comes from several spitters at once (three shots at 2.0 s). The screen filled with `*` quickly.
- I dashed about 9 times in 15 s ("you dash right/down/left/up"), mostly sideways or down, away from shots.
- I got one spitter down (swipes at 1.78 s, 3.53 s, 3.98 s) early.
- After 4 s I never got near the others. They sit in the corners at the far edge, and I spent the rest of the session dodging. I had no moment to attack.
- I was hit at 9.5 s, 12.7 s and 14.5 s. Some hits came right after a dash (dash at 12.1 s, hit at 12.7 s). The dash did not feel like a reliable safe move, and I could not tell where shots would be.
- Dodging was engaging for the first ~8 s. After that it felt like an endless chore, because there was no way to make progress.

**Practice room, spitter at distance 9**
- Shots are slow and travel a long way. They pile up on screen, with up to 4–5 in flight.
- Moving "aside" did not reliably avoid them. I was hit at 8.35 s, 9.2 s and 10.1 s.
- Because the spitter keeps firing every 2 s from the far side, closing the distance means crossing a lane of shots.

### Issues and impact

| Issue | Impact |
|---|---|
| Grub fights are a repeated loop: walk in, swipe twice, trade a hit. I never needed to dodge or space them. | **High.** It was the main feel of rooms 1 and 2, and it was boring. |
| Rooms 1 and 2 felt the same apart from enemy count. Nothing new appeared. | **High** |
| Idle walking toward the last enemy, with nothing to do (room 1, 3.0–4.3 s). | **Medium** |
| Spitters stay far away, so combat turns into dodging with no way to counter-attack. | **High**, in room 3 |
| Shots fill the screen, and I could not read a safe path. Dashing sometimes still led into hits. | **Medium–high** |
| I always lost all 3 hearts and saw no healing or recovery. Runs ended in 5–15 s. | **Medium** |

I only ever used swipe and dash. My script never tried a different approach. Whether other approaches work better is unknown.

### Positives

- Spitter volleys were visually clear (`*`), and the hit events were easy to follow.
- Room 3 gave a taste of the dodging and spacing this player wants, for a short time.
- Runs are short, which suits the profile.

### What I wanted to do but couldn't

- Dodge or space a grub, such as step out of its path and strike. I saw no cue for when a grub would hit.
- Reach and attack the spitters without crossing their shots.
- Find any variation in my own options. I only had swipe and dash, and I used them the same way each time.

## Decisions already made

None.

## Constraints

I did not read code or design documents, and I make no claims about internals.

## Open questions

- Is the grub fight as repetitive when I play by hand, with deliberate timing, instead of by reaction rules?
- What do rooms 4 and 5 add? I did not play them.
- Does the dash give any protection, such as invulnerability? From the log alone I could not tell.

## Expected output

Route to `game-designer` (Diagnose) via the Studio's Route operation.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-combat-monotony/31-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 31
from: game-designer
to: studio
stage: Route
outcome: done
---
# 31: game-designer → studio — Second Diagnose: why combat still felt repetitive after build 0.5, with ranked options

## Task

Route this diagnosis. I recommend **no Decide step**. All options below are changes to variant parameters, one per-variant rule flag, per-room spitter timing and room contents. All use existing systems and stay inside D-001 and the pillars. The next step is Design (write-design-spec) for the options marked "do", then Build and QA. Two small side items for QA are listed at the end.

## Context

Goal G-001: the Owner finds combat monotonous. Diagnose 04 led to design 14/22, build 0.5 and QA criteria 1–17 passing. Handoff 27 is a fresh playtester report on rooms 1–5. This is the second Diagnose, so the focus is what 0.5 did and did not fix. I read 27 against `design/combat.md`. I ran no `play` or `bots` this step, because the evidence needed is a hand-timed human session, which scripts cannot give. My claims about timing come from the spec numbers.

## Findings

### 1. What 0.5 fixed and what it left (against 04)

| Symptom in 04 | Status after 0.5 (from 27) |
|---|---|
| Grubs trivial, no telegraph | **Fixed.** Warnings are consistently readable, and cancel and stagger on swipe "felt good". Ignoring the cue now costs hearts (room 1, timed script: three hits in under 3 s). |
| Spitter volleys unreadable | **Partly fixed.** A single aim line and glow are readable. In rooms 4–5, several threats at once are not (symptom 4 below). |
| Dash never needed | **Not fixed** for melee. The dash is still optional there. |
| Rooms 1–2 interchangeable | **Not fixed in play.** Contents differ, but the answer is the same ("sidestep on the warning, then swipe or ignore"). |

The 0.5 changes made threats readable, which was needed for pillar 3. They did not make enemies ask for different answers. Readability turned the grub into "see flash, move, hit".

### 2. Symptoms, causes, and design cause versus script artifact

**S1. Melee enemies share one answer (most important for the Goal).**
- **Design cause (supported by `combat.md`):** grub, runner and brute are one behavior (wind-up, lunge, recovery, same 1.2-tile lane, same 2.4-tile lunge, same cancel rule). The parameter sets change *how long you have* but not *what you do*. The wind-up cancel works the same on all three, and sidestepping the same 1.2-tile lane works the same on all three.
- **Runner: probably partly a script artifact.** The runner's wind-up is 0.35 s. The lane is 0.6 tile either side, so a player needs a sideways move of just over 0.6 tile, about 0.15 s at 4 tiles/s. A script with a fixed 0.15 s reaction finishes at about 0.30 s, just under 0.35 s. A human with 0.25 s reaction plus 0.15 s of movement needs about 0.40 s, which is **over** 0.35 s. For a human the runner is likely a real test, unless the player swipes it in the wind-up, which is a different answer from the standard grub. The playtester's finding "the runner's short warning never tested the player" is therefore not safe to use. It needs a human check.
- **Brute: design cause plus artifact.** The brute asks for the same dodge as the others, only slower, and dodging costs nothing. The playtester dodged for 20+ s and never fought it. The room does not clear until it dies (rule: a room ends when all enemies are defeated), so a human has a reason the scripted player did not apply. A human who tries to clear room 2 will end up fighting it. What the design lacks is a *different way* to fight it. The same swipe-cancel works, so "fight the brute" is "dodge, then swipe", as for any grub. The playtester's open question ("is the brute meant to be attacked?") shows the player was not told by the game that it must die.
- **Attention drop by the second grub (room 1):** a design cause shared with the rest of S1. Three identical grubs in one room mean three repeats of the same loop. It is also helped by the script's perfect play: a human who is hit once will have more variation.

**S2. The dash was never needed against melee. Low priority; mostly a consequence of S1.**
- Cause: a 1.2-tile lane is cleared by a 1-tile sidestep, which is cheaper than a dash (0.6 s cooldown). That is by design and the dash does its job against shots. I do not recommend forcing the dash into melee. For example, widening a lane to need a dash would break the visual spec ("lane geometry identical"), and would make the cue harder to read. Instead, the dash's job is to be the answer in crossfire (S4). The dash can also close a gap on a recovering enemy (dash toward, queued swipe), which is a valid use that the scripts never tried.
- Answer to the playtester's question: no, the dash is not only for spitters, but only the spitter rooms currently make it better than a sidestep.

**S3. A single spitter loop is repetitive and drawn out. Mostly a script artifact.**
- The scripts chose to dodge on every cue and to approach slowly. Crossing 15 tiles takes about 3.75 s at 4 tiles/s, and the build 0.5 walker in QA's bots takes hearts for charging. In 04, charging was free, so this has changed. A human who rushes the last spitter finishes in a few seconds. A scripted dodge-and-approach loop is long by choice.
- Real design residue: a stationary spitter that fires every 2.4 s at one fixed pattern has no variation. This is acceptable for one spitter and not the first thing to fix.

**S4. Rooms 4–5: crossfire felt unfair (second most important, and the only real threat). Most important to *fairness*.**
- Observed: deaths at 15.75 s (room 4) and 11.1 s (room 5), all from shots, with hits from shots already in flight while lined up for another warning. Stepping out of one line put the player into another.
- Causes (from `combat.md`, to be confirmed in a trace):
  1. **Cue gap is only 0.2 s.** With two spitters, the first shots are at 1.8 s and 2.6 s and each repeats every 2.4 s. Each cue lasts 0.6 s, so cue windows are 1.2–1.8, 2.0–2.6, 3.6–4.2, 4.4–5.0 s. After one cue ends, the next begins 0.2 s later and **locks onto the player's position at that moment**, which is where the player stands after sidestepping the first. A good dodge of line 1 is therefore the aim point of line 2. The playtester's "stepping aside put me in another line" is the same thing. The player has no time to reposition before the next lock.
  2. **Shots live long.** A shot at 3 tiles/s crosses the 16-tile room in about 5 s (its lifetime limit). With two spitters firing every 1.2 s combined, 3–4 shots are in the air most of the time. Slow shots linger, so the playtester dodged a line only to meet a shot already in flight.
  3. Rooms 4–5 also contain grubs (a lunge under fire). In room 5 the brute adds a third source.
- **Discrepancy to flag (for QA, not blocking):** 27 says the spitters are in "opposite corners" and "fire in sync". Per the room table, they are at (15,0) and (15,8): the **same side** (two east corners). Per the spec, they are 0.8 s apart, not in sync. In room 3 a 5.8 s double fire was reported. The cap delay can bring two shots closer together, so this could be real, or a misreading of the printed picture. The conclusions above hold either way, but a trace of room 4 would settle which one it is.
- Not a defect on its face: criterion 13 requires cue-ignoring to cost 3–6 hearts across rooms 3–5, so the room is meant to bite. The problem is that a **cue-reading** player also dies. The scripted dodger bot clears 3/3, so the scripts that read cues in 27 (0.15 s fixed reaction, but diverted by overlapping lines) are not the bot's policy. This is the single clearest place where "hard" turns into "unfair".

### 3. Options

All stay inside D-001 and the pillars (readable threats, short runs).

**Option 1: Breathing room in spitter rooms 4–5 (addresses S4, helps S2).** *Do.*
- Change: for rooms 4–5 only, space the two spitters' cues so there is a **gap of at least 0.6 s** between one cue ending and the next starting (for example, a first-shot offset of 1.2 s instead of 0.8 s for the second spitter, with the 2.4 s interval unchanged: cue windows 1.2–1.8, 2.4–3.0, 3.6–4.2…). Optionally also lower the shots-in-flight cap to 2 in those rooms. Room 3 stays exactly as spec'd, so criterion 11 does not change.
- Why: the player gets time to take the sidestep and reposition before the next lock, so each line is a separate decision. The dash then becomes the way to cross a lane for a counter-attack rather than a panic button. This preserves "spitter danger forces movement".
- Cost: low. It is a per-room parameter (stagger, cap) on the existing spitter timing rule, with no new code path beyond a per-room value.
- Risk: criterion 13 (walker 3–6 hearts lost, dodger at most half) may move. The walker is already at the 60 FPS upper limit (6). If the walker drops below 3 total, that is a tuning matter for me, not a build defect, and a re-check of the numbers is part of the spec. Keep the interval unchanged, so run length is unaffected.
- Fit: strengthens pillar 3 (readable threats) and the Positives (spitter danger).

**Option 2: Make the melee variants ask for different answers (addresses S1, S2). *Do.***
- Change: add one per-variant flag to the existing grub rule, "can a swipe in the wind-up cancel the lunge", and use it for the **brute**:
  - **Brute (`G`)**: a swipe during its wind-up still damages it but does **not** cancel the lunge. The answer is "sidestep (or dash through), then punish in its 1.2 s recovery". Four swipes need more than one window, so the player must dodge, hit, and dodge again.
  - **Standard and runner**: unchanged (cancel works), so the runner remains "commit to the swipe or step out quickly" and the standard grub is "either".
- Why: three enemies would then want three different things (swipe-cancel quickly, either, dodge-and-punish). The brute becomes a different fight and gives a reason to learn the cue (swiping into its wind-up now costs a heart). It reuses the existing rule and parameter table, and the cue visuals are unchanged (the lane and tint are the same for all variants).
- Cost: low. It is a flag in the existing wind-up cancel check, plus the manual line (brute swipe does not stop the lunge) and a spec/criterion for it (criterion 6 and 8 need a brute case).
- Risk: it makes the brute harder, which could hurt room 5 (already deadly, deaths at 11 s). The brute's lunge is also dodgeable, so it stays fair. Check that a cue-reading player stays safe. A player who has learned "a swipe cancels" and swipes the brute in the wind-up gets hit, and this is a learning moment that should be signalled: the manual and the message ("a brute rears back, heavy") need a short line. That text is not mine to style; art-director can add presentation.

**Option 3: Give the brute a reason to be fought, in room 2 (addresses S1; also S4's single-source problem).** *Do, after 1 and 2 if the team wants a smaller first slice.*
- Change: in room 2, replace the Standard grub at (14,0) with a spitter at (14,0) (existing enemy). Room 2 becomes "runners and a brute under one spitter".
- Why: stalling and dodging the brute for 20 s now costs hearts from shots, so dodging forever is no longer free, and room 2 differs in *kind* from room 1 (no more "same fight, more enemies"). It mixes the two existing enemy classes earlier, as the player profile (comfortable with dodging and spacing) suggests.
- Cost: low (room data).
- Risk: criterion 14 (grub rooms: walker loses at least 1 heart, dodger loses at most 1 and clears both) must be rechecked with a spitter in room 2, and the rooms 1–2 sentence in the spec changes. It brings room 2 closer to 4. Not for a first slice if 1 and 2 already fix the feel.

**Needs a Decide step (named only, not chosen, not recommended now):**
- A **new enemy type** (for example a melee enemy with a genuinely different behavior, like a charger or a shielded enemy), a healing or recovery system, any new input, or a change to run length or the number of rooms. Each would need the `game-director`. I raise one only if a human playtest after Options 1–2 still reports that the melee fights feel the same. At present the evidence is scripted play, so it is premature.

**Ranking:** 1 first (the only real threat and the least fair), 2 second (the main monotony cause), 3 optional third. 1 and 2 are independent and can be built together.

### 4. The most important symptoms for the Goal

1. **S1 (melee shares one answer)** is the Goal's core: it directly produces "monotonous", and rooms 1–2 reading as the same fight.
2. **S4 (crossfire in rooms 4–5)** is the most important *problem*: the only real danger, and the one that feels unfair. A fix here protects the positives. It is also late in a run, where a player decides whether to continue.
3. S2 follows from S1. S3 is mostly a scripted-play artifact.

### 5. What the evidence cannot settle (hand-timed human session needed)

- **Runner:** with a human reaction of 0.2–0.3 s, does the 0.35 s wind-up actually test the player (my estimate says yes) and do they choose swipe or sidestep? A human needs to play room 2 at least twice and say what they did against the runner.
- **Brute:** does a human who must clear room 2 fight the brute at all, and what do they do? Do they notice the room will not clear while it lives? Kill at least one brute (the playtester never did).
- **Rooms 4–5:** is the crossfire unfair for a human, or only for a scripted player who reacts at a fixed 0.15 s? Hand-timed play in rooms 4–5, at least two attempts each, noting cause of each hit (a shot in flight, a new lock, or a line misread). Also whether the two spitters really fire together.
- **Rooms 2 and 3 endings:** the playtester's output was cut off, so the end of those sessions is unknown. Do not treat the 20+ s brute dodging as a finding about clear times.
- **Dash:** whether a human uses it on purpose against shots once Option 1 is in. Experience signal: at least once in a room, not only in panic.

## Decisions already made

- D-001: attack and dash only; no new input. All options comply.
- D-002: per-frame contact sampling and the contact-edge graze stay. Not touched here.
- D-003 (step 30, band wording): not touched.
- Step 9b and the room 2 possible defect (handoff 29) are separate and not diagnosed here.

## Constraints

- Pillars: one-button combat, short runs (15–20 min), readable threats. Play correctly at 30 and 60 FPS. Reuse existing systems.
- Option 1 keeps the 2.4 s interval, so run length is unaffected. Option 2 and 3 are content and rule-flag changes. No run-length change.
- The visual spec says lane geometry is identical for all variants. Option 2 keeps this. Any option that changes lane width per variant would need `art-director` and a spec change, and I do not propose one.

## Open questions

- None that need a Decide step.
- For the Studio: whether to take Options 1 and 2 as one Design step (my recommendation) or 1 first. If a human playtest of the hand-timed kind can run **before** the Design step, it would settle the runner and brute questions above and could change the priority of Option 2. It is not blocking, because Option 1 is justified by the spec numbers alone.

## Expected output

Route to Design for `game-designer` (write-design-spec) for Options 1 and 2, with Option 3 as optional. The spec updates `design/combat.md`: per-room spitter stagger and cap for rooms 4–5, the brute wind-up flag, manual text, and any rewritten criteria (6, 8, 13, 14 if room 2 changes), plus new player-observable criteria (for example: a cue-reading player in rooms 4–5 can name which line to avoid; a brute swipe in its wind-up does not cancel the lunge). Then Build, then QA at 30 and 60 FPS, then a **hand-timed** playtest of rooms 2, 4 and 5 (briefed on the unknowns in Findings 5).

Two side items for QA, not blocking: (a) a trace of room 4 and of room 3 around 5.8 s to confirm spitter fire times and shots in flight against the spec (0.8 s apart, at most 3 in flight), given 27's "in sync" report; (b) handoff 29, the room 2 defect, already routed.

## Sender assessment

Confidence: high that S1 is a design cause (one shared behavior and answer, and the 0.5 changes tuned timing, not the answer). Medium on S4's causes: they come from the spec numbers and the playtester's account, and the "in sync" and "opposite corners" statements conflict with the spec, so a trace is wanted. Medium-low on the runner and brute conclusions: they rest on scripted play and on my reaction-time arithmetic. I ran no `play` or `bots` this step, so I did not verify any build behavior.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/31-game-designer-to-studio.md
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
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
