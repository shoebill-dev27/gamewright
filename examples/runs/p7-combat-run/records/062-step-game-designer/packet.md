# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/66-studio-to-game-designer.md
next_seq: 68
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/68-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-011-<name>.md
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

<<<FILE goals/G-001-combat-monotony/66-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 66
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 66: studio → game-designer — Room 3 shots in flight vs D-007; is D-008 ready to build?

## Task

Answer two small Design questions in writing: (1) QA's room 3 shots-in-flight conflict, checking it against D-007 and the room 3 cap spec; (2) whether the variant-named wind-up message (D-008) is specified well enough to build, given a new playtest finding. This is non-blocking for the Review running in parallel (65).

## Context

Goal G-001 (combat monotony). Build 0.6.1 is unchanged. QA (64) found no defect in a 30 FPS pass of rooms 1–5, and raised one spec question. A variant-aware playtest (63) reported a clarity issue with the message line.

## Findings

**1. QA's room 3 question (from 64):**
- In room 3 reaction runs (same at 30 and 60 FPS), all three spitters started a cue together at about 5.8 s and again at about 10 s (9.8 s at 60 FPS), then fired together 0.6 s later. QA saw at least 4 `*` on screen at 7.0–8.0 s and could not say if the count was 4 or 5 (pictures only, no trace).
- QA reads criterion 11 as "never more than 3 shots in flight in rooms 1–5" and the cap section as allowing up to 2 plus the number of living spitters, which is 5 for room 3. QA asks whether simultaneous starts after a cap delay are still accepted (D-005) and which bound applies.
- The Studio's project record has D-007, "simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 is reworded to the real in-flight bound". QA did not load D-007 or `design/combat-step-46-room3-cap.md`. Check whether the conflict QA describes is already resolved there. If it is, say so and name the exact wording; if the spec text still contradicts itself, fix it.
- Reproduction script, from QA:
  ```text
  room 3
  fps 30
  end 12
  when see * coming within 1.5 then move aside
  when text "takes aim" then move aside
  when see s within 1.4 then attack
  ```

**2. Other QA notes (64, open questions 2 and 3):**
- Manual wording on late swipes (59) is specified but not applied to `repo/manual.md`. Confirm 59 still stands.
- For a 1-hp runner, a swipe in reach kills it, so "cancel" cannot be told from "kill". State in the spec, if useful, that no separate runner cancel rule is intended.

**3. Playtest finding (63), clarity only:**
- Brute and runner wind-ups print "a grub rears back" and hits print "YOU ARE HIT by a grub". Only the `cue:` line names the enemy. The tester was confused for a moment and said a player without the cue line would not know. The playtester gives this medium impact.
- D-008 proposes naming the variant in the text-view message and makes no swipe-timing change. Decide whether D-008 is complete (message strings for grub, runner, brute, hit message, and which views it applies to) and whether it stays inside the "readable threats" pillar and D-001. If it is ready, say so in a form the engineer can build from, with player-observable acceptance criteria.

## Decisions already made

- D-005: blocked contact consumes the shot; simultaneous cue starts outside rooms 4–5 accepted.
- D-007: simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 reworded.
- D-008 (proposed): variant-named wind-up message; no swipe-timing change.
- D-009: next pass was a variant-aware playtest; the Director is judging it in 65.

## Constraints

- No new input buttons; no changes to enemy timings, room layouts or hearts from this step. Message wording only for item 3.
- Do not reopen D-004 to D-007 unless the spec text truly contradicts itself.
- Do not design new content to fix monotony here; that question belongs to the Director's Review (65).
- If D-008 needs a Decision to become `accepted`, record it yourself if it is within your authority (player-facing wording), or hand back with the question if it is not.

## Open questions

1. Is QA's room 3 conflict already resolved by D-007? If not, which bound applies, and what is the exact criterion wording?
2. Is D-008 ready to build, and what is its acceptance criterion?

## Expected output

A handoff addressed to `studio` with the answers and any spec or Decision file changes named in Findings. If anything is ready to build, say exactly what (manual text from 59, D-008 message) so the Studio can open a Build after Review. No Build is requested yet.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-step-46-room3-cap.md, design/combat-step59.md, design/combat-cues-visual-spec.md, project.md#constraints, repo/manual.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-009-review-next-pass-variant-aware-playtest.md
- Previous handoff: goals/G-001-combat-monotony/64-qa-to-studio.md (also goals/G-001-combat-monotony/63-playtester-to-studio.md for the clarity finding only)
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
runs: play, bots
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
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

<<<FILE design/combat-step-46-room3-cap.md
# Combat design note: room 3 shots in flight after cap delays (step 46, build 0.6)

Status: amends criterion 11 of `design/combat.md` and the "Cap" paragraph. Where this note and `combat.md` differ on criterion 11 or the cap, this note governs. No rule, parameter or room changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-007 (follow-up to D-005 item 4). Step 54 reworded criterion 11d only (how the count is read in the text view); the bound is unchanged.

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
- d. **Observation of the count (reworded in step 54).** In `play --view player`, run the QA 43 room 3 script (real room 3, `when see * coming within 2 then dash aside`, 15 s) at 30 and 60 FPS. The player view prints a picture every 0.5 s, so the count is taken at the printed pictures at **7.5 s and 12.0 s**, not at 11.7 s (no picture is printed there). The count at a picture is:
  - **shots in flight = the `*` marks visible in that picture + the number of `a spitter spits` events in the 0.3 s up to and including the picture time.**
  - The second term exists because a shot within one cell of its spitter is drawn as `s`, not `*`, so it is not visible as a mark for its first moments (3.0 tiles/s, about 0.1–0.3 s). Spit events are in the printed messages; they are not a new build output.
  - Expected: 3 to 5 at 7.5 s (QA 50: 2 visible + 3 spits at 7.400 = 5) and 3 at 12.0 s (QA 50: 3 visible, the spits at 11.600 are 0.4 s old and already drawn as `*`, so the spit term adds 0). A derived count within 3 to 5 in room 3 is a pass; 4 or 5 needs no report. A count above 5 in room 3, or above 3 in rooms 4–5, is a build defect. A literal `*` count below 3 is not a verdict by itself; QA records the visible marks, the spit events counted, and the derived total for both rates.
  - A derived count is an accepted method for 11d. It is a derivation from printed text, and QA states it as such.
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

**None for this item.** The enemy code does not change. The Build for this handoff is F2 and F3 only (see handoff 46). Step 54: no trace field or other build change is needed for 11d.

## Re-verification needed because of this ruling

- Criterion 11 against the amended wording (a–e above). For 11d, QA's step 50 figures already give 5 at 7.5 s and 3 at 12.0 s at both rates; no new run is needed unless the build changes.
- Nothing else. No parameter, rule or room changed, so the criterion 13, 14, 15 and 18 figures are unaffected.

## Undefined or not observed

- The count of 5 shots is derived from timings and printed events, not observed as 5 marks. This is the accepted method (11d).
- The assumption that a freshly fired shot stays hidden under `s` for at most 0.3 s is derived from speed and cell size. If a spit event older than 0.3 s is still hidden, QA records it and the window is widened by a spec step.
- Whether a human can answer the burst is derived from geometry, not observed. The playtest settles it.
- Criteria 2, 6, 10, 17 (a–d), 19f, the isolated runner dash in 3, the runner's one-swipe death in 8, rooms 1–2 contents in 12, 18c with a killed spitter, 20e, 20f, 21b and the 16e decision logs are not affected by this ruling and stay on the re-verify list.

## Experience signal (playtest and Review)

A player in room 3 who sees several cues at once can say which lines are coming and moves out of them. They do not describe a burst of shots as unfair or hidden.
>>>END

<<<FILE design/combat-step59.md
# Combat design addendum, step 59 (wording of late swipes; cue message per variant)

Status: wording only for point 1 (no rule or parameter change, no build change). Point 2 is a proposed player-facing change, not built, see D-008. Where this file and `design/combat.md` differ, this file governs for the two points below. `combat.md` itself is unchanged in step 59 because its rules already say what the manual must say.

## Intent

A text-view player can tell, from what is printed, (a) when a swipe can still cancel a lunge and (b) which kind of grub is about to lunge. No new information that makes threats harder to read, and no dependence on graphics.

## Point 1: swipe timing wording (no rule change)

Rules already in `combat.md` (unchanged):
- A swipe that damages a standard grub or runner in wind-up cancels it. Stagger 0.4 s. One non-lethal swipe is enough, even on a 2 HP grub.
- A swipe during the lunge, recovery or stagger changes no phase. A lunge that reaches a hurtable player in its path still deals 1 damage.
- The brute is never cancelled by a swipe (D-004).
- Swipe reach 1.5 tiles. A grub starts its wind-up when the player is within 2.0 tiles, so at the start of a wind-up the target may be 1.5–2.0 tiles away and out of reach. A swipe cancels only if the grub is within 1.5 tiles at the moment the swipe lands, which the player can reach by stepping in during the warning (4 tiles/s).

Conclusion: wording is enough. Playtest 53 and QA 56 show both "unfair" swipes landed 0.10 s after the lunge began with the grub out of reach during the whole warning. A swipe-timing rule change (a grace period after the lunge starts, or a larger reach) would make the lunge cancellable after its warning and weaken "step aside or dash" as the answer, and the evidence does not show a rule problem. No rule change is proposed.

Manual wording (exact text, for `repo/manual.md`) is in handoff 59.

Acceptance (verification): the manual says all of: swipe cancels only during the warning; a grub starts rearing back about 2 tiles away, beyond the 1.5-tile reach, so step in to within 1.5 tiles during the warning; a swipe landing after the lunge has begun does not cancel it; one swipe is enough to cancel a grub or runner; the brute is never cancelled.

Experience signal (playtest and Review): a player who swipes a rearing grub from too far, or too late, and is hit can say why ("it was already lunging" or "it was too far") without calling the hit unexplained.

## Point 2: cue message per variant (proposed build change, see D-008)

Proposed text-view start-of-warning messages:

| Variant | Mark | Message |
|---|---|---|
| Standard grub | `g` | `a grub rears back` (unchanged) |
| Runner grub | `r` | `a runner rears back` |
| Brute grub | `G` | `a brute rears back` |

Rules:
- All three contain the words `rears back`, so existing reaction rules `text "rears back"` still match all variants. A rule `text "a grub rears back"` matches only the standard grub after the change.
- Only the message text changes. Timing, the `~` line, the `cue:` line, one-at-a-time, cancel flags and every parameter stay the same.
- No distance, hit points or timing are added to the message. The `cue:` line stays the place for those.
- The message is a text-build presentation. The graphical build keeps its silhouette, size and cadence (visual spec) and is unaffected.
- The spitter and brute-swipe messages are unchanged.

Acceptance criteria (verification, for QA if built), at 30 and 60 FPS, practice room:
- V-a. A runner's wind-up prints `a runner rears back`, a standard grub's prints `a grub rears back`, a brute's prints `a brute rears back`, each at the same moment as the current message (±1 frame) and once per wind-up.
- V-b. The `cue:` line, `~` line, wind-up time, lunge time and every other output line are byte-identical to the current build in the same scripts, apart from the message words.
- V-c. A script with `when text "rears back" then ...` reacts to all three variants as before.
- V-d. Criteria 1–11 and 17–21 of `combat.md` still hold. No bot result changes. If the bots key on the old message text, the Build step updates them (test tooling).

Experience signal (not for the Playtester's handoff): a text-view player can say, from the message alone, that a runner is the fast, short-warning one and a brute the slow one, and does not report wasted dashes at a distant runner because it "said grub".

Worth doing now: low cost and low risk, but not required by the Goal. Recommendation: build it with the next build that is opened anyway. Do not hold or reopen Review 57 for it. Any change to `play.py` and the tests is a Build step with Verify.

## Open questions

- Whether naming the variant helps the player or only moves the wasted dash to another cue is for the next playtest. Dashing at a distant threat is a reaction-script choice (a rule keyed on a message ignores distance), not a message defect.
- Whether the brute's `a brute rears back` plus its shrug message is enough signal for a human is already open from step 35.
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE decisions/D-008-cue-message-names-variant-proposed.md
---
kind: decision
id: D-008
status: proposed
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-008: Text-view wind-up message names the variant (proposed build change); no swipe-timing rule change

## Decision

1. **Swipe timing stays a wording matter.** No rule or parameter change. The manual says that a swipe cancels a grub or runner only during its warning, that a grub starts rearing back about 2 tiles away (beyond the 1.5-tile reach), and that a swipe after the lunge began does not cancel it.
2. **Name the variant in the message** (proposed, not built): `a grub rears back`, `a runner rears back`, `a brute rears back`. All keep the words `rears back`. Nothing else in the output changes. Details and acceptance criteria are in `design/combat-step59.md`.
3. **Routing advice:** not urgent, not part of Review 57. Build it with the next opened build and Verify it. `game-director` need not weigh in unless they think the change moves the Goal.

## Rationale

- The graphical build already tells variants apart before the cue (silhouette, size, cadence). The text view has only the message and the `cue:` line. Naming the variant gives the text-view player the same early information and costs no new pillar-breaking information.
- It does not conflict with the "one answer for melee enemies" diagnosis (S1, 04, 31). The answer to runner and standard grub is the same, and the variant name only says how long the warning is. The brute's different answer comes from the cancel flag (D-004), and its name makes that flag easier to learn.
- Compatibility: the substring `rears back` keeps existing reaction scripts working.
- Wording is enough for the swipe, because both reported hits were swipes after the lunge began with the target out of reach during the warning (QA 56). A grace window or larger reach would let a swipe cancel a started lunge, which weakens "step aside or dash" and is not backed by a defect.

## Alternatives considered

- **Keep one message for all variants** (current, `combat.md` step 35): the `cue:` line already names the variant. Not chosen because the playtester reacts to the message line, and a reaction-rule player has to parse the `cue:` line to tell the variant.
- **Put distance and time left in the message** (for example "a runner rears back, 0.35 s"): the numbers make the message long, repeat the `cue:` line, and risk making the text view easier than the graphical build. Not chosen.
- **A swipe grace period of about 0.1 s after the lunge starts, or a bigger reach during wind-up:** would turn the two "unfair" hits into cancels, but needs a rule change that QA did not find a defect for, and it weakens the sidestep/dash answer. Not chosen; reopen if a human playtest still reports unexplained late swipes after the manual is clear.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after variant naming.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text message irrelevant.
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

<<<FILE goals/G-001-combat-monotony/64-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 64
from: qa
to: studio
stage: Observe
outcome: done
---
# 64: qa → studio — 30 FPS coverage closed: player view (rooms 1–5) and late-swipe boundary match the design and 60 FPS; no defect; one spec conflict on shots in flight (room 3) for Design

## Task

Close the two gaps left by handoff 56: the player view at 30 FPS for rooms 1–5, and the late-swipe boundary at 30 FPS for a grub and a runner. Report any difference from 60 FPS or from `design/combat.md`.

## Context

Goal G-001. The build was not changed. Evidence comes from this step's runs only:
- `python3 -m unittest discover -s tests`: 59 tests, OK.
- Player view at 30 and 60 FPS for rooms 1–5. They are reaction scripts, as in handoff 55. Rooms 3–5 ran 12–15 s.
- Practice-room traces at 30 and 60 FPS for the grub and runner, in reach and out of reach.
- Grub swipes at 0.40, 0.50, 0.52 and 0.60 s, and a room 1 reaction trace at both rates.

## Findings

### 1. Player view at 30 FPS, rooms 1–5: matches the design, the manual and 60 FPS in everything the rules fix

**Warnings and cue lines**
- Every grub, runner and brute wind-up printed `a grub rears back` and a picture with `~`. A `cue:` line named the enemy (`g`, `r`, `G`) and gave the lane direction, 2.4 tiles, and the seconds left.
  - Standard grub: starts at "0.50 s", e.g. room 1, 2.033 s.
  - Runner: "0.35 s", e.g. room 2, 3.000 s.
  - Brute: "0.70 s", e.g. room 2, 25.967 s, and room 5, 5.000 s.
- The countdown falls consistently between prints, e.g. 0.50 → 0.03 s in room 1. The 60 FPS runs show the same values within one frame.
- The line disappears when the lunge starts. The manual and `combat.md` accept this.
- Spitters: `a spitter takes aim` → `a spitter spits` is 0.6 s apart at both rates. Brightness rises 0% → 33% → 50% → 83% in the `cue:` lines. The text view starts at 0%, as ruled in step 22.

**Spitter timing**
- Room 3, first shots: 1.8, 2.6 and 3.4 s at both rates.
- Rooms 4 and 5, first shots: 1.8 and 3.0 s at both rates.
- Cue gap in rooms 4–5 at 30 FPS:
  - Room 4: shots at 1.8, 3.0, 4.2, … with the next cue starting 0.6 s after each. Cues are 2.4 → 3.0, 3.6 → 4.2, 6.8 → 7.4, 8.0 → 8.6, and so on.
  - Room 5: 7.000 → 7.600, then 8.400 → 9.000. The gap is 0.8 s, which is at least 0.6 s.
  - No cue windows overlap.
- Cap delay in room 5 at 60 FPS: the cue due at 6.0 s was delayed to 7.0 s. This is allowed.

**Hit messages**
- `YOU ARE HIT by a grub — hearts n/3` and `… by a shot …` appear on the frame of contact.
- Shot hits: room 3 at 5.633 (30 FPS) against 5.667 (60 FPS), and room 5 at 4.333 against 4.350. That is within one frame.

**Brute**
- Room 5, a swipe during the wind-up:
  - 30 FPS: 7.867, a swipe 0.07 s before the lunge. It printed `the brute shrugs off the swipe`, the cue stayed, and the hit followed at 8.000.
  - 60 FPS: 8.517, same behaviour, with the hit at 8.783.
- Room 2, 30 FPS: swipes during the lunge (26.733) and recovery (27.233, 27.733) printed only `you swipe: brute hit`, with no shrug message. The fourth hit, at 28.100, printed `brute defeated` with no shrug message, even though the brute was already winding up (cue at 28.067). That matches criterion 19c: a killing swipe in wind-up shows no message and there is no lunge.

**One at a time and cancel**
- Room 5, 30 FPS: a swipe at 7.033 cancelled the winding-up grub. Its cue vanished and the next wind-up was the brute's, at 7.233.
- Room 1, 30 FPS: a second grub began its wind-up (2.800) only while the first was in recovery.

**Blocked contact (D-005) seen unprompted at 30 FPS**
- Room 1 reaction trace: the player was hit at 2.767, so the window ran to 3.567.
- The grub's lunge touched the player at about 3.467 (grub at 7.11, player at 7.47) while protected.
- At 3.567 the window ended with the grub still lunging, 0.43 tile from the player. Hearts stayed at 2, and the grub went into recovery at 3.733.
- This matches criterion 21b: the lunge's hit is spent.
- At 60 FPS the same room gave a hit at 3.567 instead. That timeline differs: the player was at 7.87, and first contact came after the window had ended, which is a legitimate hit.

**Differences between 30 and 60 FPS in the reaction scripts**
- Final outcomes differ:
  - Room 1: cleared at 1 heart (30 FPS) against down at 5.83 s (60 FPS).
  - Room 2: cleared at 28.1 s (30 FPS) against 11.7 s (60 FPS), both with 1 heart.
  - Room 5: 1 heart at 15 s with 2 enemies left (30 FPS) against 3 left (60 FPS).
  - Rooms 3 and 4: the same hearts at 12 s and 15 s.
- The reaction rules act on a 0.15 s grid, so positions diverge early. Examples are the room 2 grub that was avoided for many seconds at 30 FPS, and the different paths in room 1.
- I did not isolate a case of the same decision from the same state at the same time giving a different result. By criterion 16d/16e this is bot-timing sensitivity, not a finding. I make no claim beyond that.

**Verdict for item 1: matches. No difference in warnings, cue lines or messages between 30 and 60 FPS beyond one-frame timing.**

### 2. Late-swipe boundary at 30 FPS: matches the design, and differs from 60 FPS by less than one 30-FPS frame

Practice room, grub at 9.3 or 10, player at 8,4. A scripted input fires on the first frame after its timestamp at both rates (0.50 → frame 16 at 30 FPS and frame 31 at 60 FPS). Within a frame, the swipe is resolved before the grub's wind-up timer expires.

**Standard grub**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe mid-wind-up (0.40) | swipe at 0.433: stagger 0.367, hp 2→1, no lunge, new wind-up at 0.833 | swipe at 0.417: stagger 0.383, no lunge, new wind-up at 0.817 |
| In reach, swipe on the frame the lunge starts (0.50) | swipe at 0.533, frame 16: **cancelled** (stagger 0.367) | swipe at 0.517, frame 31: **cancelled** (stagger 0.383) |
| In reach, swipe one frame after the lunge starts (0.52) | lunge 0.533, swipe 0.567: hp 2→1, lunge continues, hit at 0.633 (hearts 3→2) | lunge 0.517, swipe 0.550: same, hit at 0.617 |
| In reach, swipe 0.60 (late) | swipe 0.633 with the hit in the same row; not cancelled | swipe 0.617 with the hit in the same row; not cancelled |
| Out of reach (grub starts 2 tiles away), swipe 0.30 | `hits: []` at 0.333; wind-up unchanged (0.200 left); lunge at 0.533; hit at 0.733 | `hits: []` at 0.317; lunge at 0.517; hit at 0.700 |

- At both rates the last swipe that cancels is the one landing on the frame the lunge begins. A swipe one frame later does not cancel.
- Lunge start is 0.533 s at 30 FPS and 0.517 s at 60 FPS. The difference is 0.017 s, half a 30-FPS frame. The cancel limit therefore differs by under one frame at 30 FPS.
- The 60 FPS probes bracket the boundary between frames 31 and 33. I did not probe frame 32.
- Lunge hit times differ by one to two frames (0.733 against 0.700, 0.633 against 0.617), which is frame sampling.

**Runner**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe 0.20, mid-wind-up | `runner defeated` at 0.233; no lunge; cleared | `runner defeated` at 0.217; same |
| In reach, swipe 0.43, after the lunge began | lunge 0.400, swipe 0.467: runner defeated before contact; hearts 3 | lunge 0.367, swipe 0.450: same; hearts 3 |
| Out of reach (2 tiles), swipe 0.20 | `hits: []`; wind-up continues; lunge 0.400; hit 0.600 (hearts 3→2) | `hits: []`; lunge 0.367; hit 0.550 |

- The runner's out-of-reach swipe does not cancel at either rate.
- The runner has 1 hp, so an in-reach swipe always kills it. The "a late swipe does not cancel the lunge" case is not separable from a kill for a runner. It showed as a kill at both rates, with the lunge ending before contact. The spec cannot tell "cancel" from "kill" for a runner, and I report it as observed behaviour only.
- After the first hit, the second runner lunge fell at 1.600 s (30 FPS) against 1.517 s (60 FPS), a 0.083 s gap. It comes from the earlier contact-frame difference of 0.05 s plus frame quantization. Both rates took two hits.

**Verdict for item 2: matches. At 30 FPS the cancel boundary sits at the frame the lunge starts, as at 60 FPS, and differs by less than one 30-FPS frame.**

### 3. Defects: none

I found nothing that is wrong against `design/combat.md` or `repo/manual.md`. One conflict inside the spec, found while reading the room 3 views, is below. It is not a build defect.

### Spec gap for `game-designer` (not a defect, low to medium priority): room 3 shots in flight, and simultaneous cue starts in a real room

**What the room 3 reaction runs show (same at 30 and 60 FPS)**
- All three spitters started a cue at the same moment twice: 5.800 (at both rates) and 10.000 (30 FPS) or 9.800 (60 FPS). In both cases all three then fired together 0.6 s later.
- Their checks run on the same 0.2 s grid after cap delays. The first start at 5.8 s followed the hit by a shot at 5.633 / 5.667 s, which freed a cap slot. This is my reading of the pattern and is not confirmed in code.
- This is the "real-room trace in room 3 with a surviving player past 7 s" asked for in `combat.md` open questions and D-005 (revisit).
- In both runs the player (a reaction script with "move aside") took no hit from the simultaneous volleys. Hearts stayed at 2 from 5.8 s to 12 s. The lines did cross at the player's row (30 FPS, 10.0 s). So this case did not show unanswerable shots.
- At least 4 `*` are visible in flight at 7.0, 7.5 and 8.0 s at both rates. Up to 5 would be expected: two earlier shots plus the three fired at 6.4 s. Criterion 11 says "in rooms 1–5 never more than 3 shots in flight". The cap section says real rooms stay at 3 or fewer, citing a QA observation, and also says the count at a check can reach 2 + the number of living spitters. For three spitters that is 5.
- I counted `*` from the pictures only. I did not run a trace for the exact count, and shots in the same cell as a spitter can be hidden. I cannot say whether the number is exactly 4 or 5.

**Question for Design:** is the simultaneous start in room 3 still accepted (D-005), and is "never more than 3 in flight in rooms 1–5" still the rule in room 3? The two statements conflict when a cap delay releases all three spitters at once.

**Reproduction:**
```text
room 3
fps 30
end 12
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when see s within 1.4 then attack
```
Run it at `fps 30` and `fps 60` and look at the cue starts at 5.8 s and the stars at 7.0–8.0 s.

**Acceptance criterion if Design wants a change:** in a trace of room 3 with a moving player over 12 s, the shot count never exceeds the number the spec states, at both frame rates.

## Decisions already made

- D-002/D-003: contact-edge graze. No contact in these runs was in the band. The lunge contacts were at lateral miss 0 against 0.6.
- D-004: the brute is not cancelled by a swipe. Confirmed at both rates (see item 1).
- D-005: a lunge's hit is spent when it touches a protected player. Seen at 30 FPS (room 1) and consistent with the room 5 observations in handoff 56. The simultaneous-start acceptance is raised again above because the revisit trigger has now been traced.

## Constraints

- The build and documents were not changed.
- Not run:
  - A frame-32 probe at 60 FPS.
  - A brute late-swipe boundary pair, beyond the room 2 and 5 views.
  - Dash cases at 30 FPS.
  - A trace of room 3 for the exact in-flight count.
  - A human playtest.
  - Isolating the 30/60 FPS reaction-script divergences.
- Experience judgments (monotony, fun) are not assessed here.

## Open questions

For `game-designer`:
1. The room 3 shot-count conflict and the simultaneous-start acceptance (above).
2. The manual wording from handoff 56 is still open. It should say a swipe cancels a lunge only during the warning, and not when the grub is out of reach. This step again showed an out-of-reach swipe that did nothing (2 tiles, `hits: []`, at both rates) and the cancel limit at the lunge start.
3. For a 1-hp runner, "cancel" and "kill" cannot be told apart by a swipe in reach. If the design means a separate runner cancel rule, it does not show up in play.

## Expected output

Studio: record the two 30 FPS gaps as closed and matching. Route the room 3 in-flight-count and simultaneous-start question to `game-designer`. No change is requested from `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, the build in repo/
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/62-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/63-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 63
from: playtester
to: studio
stage: Play
outcome: done
---
# 63: playtester → studio — Observation report: combat of the current build, rooms 1–5

## Task

Report what I experienced playing rooms 1–5 of the current build through the player view, with separate reaction rules per enemy mark.

## Context

Reply to handoff 61. I played only through input scripts with reaction rules, using `python3 play.py --view player`. I did not read source, design documents or tests, and I did not use the trace view or the bots. I played as the profile describes: an action player who dodges and spaces, with no combo memorizing.

## Findings

### Method

All play was scripted reaction rules, not live play. Six sessions in two rounds. I cannot feel the pad or the timing. Reaction rules act at most every 0.15 s, so "my" dodges are an approximation of a player.

| Session | Style | Result |
|---|---|---|
| room 1, 60 FPS, "fast" | Chase every grub, swipe at 1.4 tiles, step aside on "rears back" | Cleared in 6.6 s, 3/3 hearts. |
| room 2, 60 FPS, "slow" | Wait, face enemies, swipe at 1.4 tiles, step aside on every warning | Output cut at ~27 s. Room not finished. Hearts 2/3. |
| room 3, 30 FPS | Dash on warnings, walk toward enemies | Output cut at ~26 s. Room not finished. Hearts 3/3. |
| room 2, 60 FPS, "fast" | Rush the runners and grubs, back off the brute only inside 1.6 tiles | Went down at 11.4 s. |
| room 4, 60 FPS, "my style" | Chase, dash on grub warnings, step aside on spitter aim | Cleared in 15.2 s, 2/3 hearts. |
| room 5, 60 FPS, "slow" | Keep distance from the brute, step aside on every warning | Output cut at ~19.5 s. Alive at 1/3 hearts with both spitters still up. |

Rules per mark:
- **Grub `g`:** I moved aside when it reared back and swiped when it was within 1.4 tiles. Its warning is 0.5 s and a swipe cancels it, so the answer was "step out or hit it first".
- **Runner `r`:** Same as the grub. The 0.35 s warning left little time to step aside, so swiping early or moving at the first warning mattered more.
- **Brute `G`:** I stepped away or aside and did not swipe it into its warning. The manual says a swipe will not cancel it. In the fast run I did not give the brute its own dodge rule, which is my mistake and explains that death.
- **Spitter `s`:** I moved aside or dashed across the aim line (a different answer, because the shot is a slow travelling projectile), and closed in to swipe it.

I made the rules differ for the reason above. In the fast room 2 and room 1 runs I also let "move toward" override spacing.

### Room 1 → room 2 → rooms 3–5

**Room 1 (three grubs).**
- Every grub asked the same thing: step aside, or swipe it to cancel.
- Cancelling worked every time I tried (0.6 s, 1.05 s, 2.08 s, 2.53 s, and so on). The fast run took 6.6 s with no damage.
- It was easy and quick. It was also all one move; there was nothing to adapt to.

**Room 2 (two runners, a grub, a brute).**
- The runners were over quickly (one swipe each, 3.4 s and 4.3 s in the slow run, 1.3 s and 2.1 s in the fast run).
- The brute changed the pace. It is slow and has a long warning, and its swipe-cancel does not work.
- In the slow run the brute fell into a loop from about 8 s to 27 s: it rears back, I step aside, it lunges, it follows me, it rears back again. I counted six or seven of these. I never got to hit it in the gap after a lunge, because my rules did not do that.
- That stretch felt repetitive, though it may partly be the scripting.
- In the fast run, the brute killed me after three hits (7.4 s, 9.4 s, 11.4 s). I stood next to it each time and my rules did not react to its warning.

**Room 3 (three spitters, no melee).**
- Everything was "read the line, move across it".
- The spitters take aim in turn, and the aim lines are long diagonals or straight lines across the room.
- I was never hit in the 26 s I saw. Early on I killed two spitters, but the third stayed in the far corner, and for about 20 s the same pattern repeated: aim, dash, shot lands behind me, again.
- This was the most repetitive stretch of everything I played. Attention dropped, though it stayed safe.

**Room 4 (grub, runner, two spitters).**
- This was the first room that mixed asks: a melee dodge and an aim line at once.
- I was hit once by a shot at 7.45 s while moving aside, in a crowd of several projectiles.
- It felt better than rooms 1 and 3. The grub and runner lunges, the spitter lines and my own movement overlapped, and I had to choose which to answer first.

**Room 5 (two grubs, a brute, two spitters).**
- This was the busiest room, and the only one where my attention stayed high all the way through.
- I took a shot at 6.8 s while walking through an aim line, then took a hit that I think came from the brute's lunge at 9.7 s (see the unexplained hit below), and was at 1/3 hearts by 9.7 s.
- I did kill the brute (11.45 s) and the grubs. The room did not clear in the part I saw; the output was cut while the spitters were still firing and I was still dodging.

### Repeated vs. different

- **Repeated:** the "rears back → step aside → swipe in the gap" loop in room 1, and the slow room 2 brute dance. The spitter-only room 3 felt the same from about 6 s on.
- **Felt different:** the brute (first time my swipe could not stop the warning), spitters (the first enemy that fights from range, with a line to read), and rooms 4–5 (several asks at once). Rooms 3 → 4 → 5 differ mostly in how many things overlap, not in what each thing asks.

### Did anything hurt me that I couldn't explain?

- **Brute lunge at 9.72 s in room 5.** The only message was "YOU ARE HIT by a grub". The brute's hit is reported as "a grub", and its warning also says "a grub rears back". A runner's and a brute's warnings read the same way in the message line. Only the `cue:` line (`r` / `G`) says which enemy it is. That was confusing for a moment, and a player without the cue line would not know.
- **Grub hit at 5.82 s in room 2 (slow run).** My swipe landed at 5.72 s ("grub hit") with 0.13 s left on the warning, but did not cancel it, and the lunge arrived. This was explainable (a grub needs 2 swipes, and the first one only wounded it), but easy to misjudge.
- **Spitter shots in rooms 4 and 5.** The two hits I took came from walking across lines in a field of several shots. I could tell where they came from in the printed rooms. In live play with this many `*` on screen I would expect some hits to feel unfair.

### Impact

| Issue | Impact |
|---|---|
| Room 3 spitter standoff repeats the same dodge for 20+ s | High on feel (boredom) |
| Brute loop in room 2 (dodge, wait, dodge) | Medium on feel |
| Brute and runner warnings read "a grub rears back" | Medium on clarity |
| Rooms 4–5 shot clutter | Medium |
| Room 1 offers only one kind of ask | Low to medium, as a first room it is fine |

### Positives

- Warnings were always shown before damage; I always knew roughly where danger would land.
- Room 4 and room 5 were clearly different from the single-ask rooms, and engaging.
- The brute's no-flinch rule makes it distinct from the grubs.
- The runner is a quick, readable one-swipe threat.

### Limits of my evidence

- All play was scripted reaction rules; I did not hold a pad or react in real time. Rule choices (for example, "move toward" in the fast runs) decided several outcomes.
- Outputs for room 2 (slow), room 3 and room 5 were cut by the output limit, at about 27 s, 26 s and 19.5 s. I did not see how they ended.
- I did not play room 1 slow or in my own style, or rooms 3, 4 and 5 as a fast-clear run. Room 4 was my favourite style only and room 5 only slow. The 30 FPS run was room 3 only; I made no comparison against 60 FPS.
- I saw no difference I could attribute to frame rate.
- I did not play the practice room.

## Decisions already made

None.

## Constraints

Player view only; no source, design or tests read.

## Open questions

None for the studio. I cannot say, from scripts, whether the room 3 and brute loops would feel as flat to a human player; a live check would help.

## Expected output

Studio reads this and routes experience issues to game-designer, and the "a grub rears back" wording on brute and runner to whoever owns clarity or defects.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build (`repo/`)
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/61-studio-to-playtester.md
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
