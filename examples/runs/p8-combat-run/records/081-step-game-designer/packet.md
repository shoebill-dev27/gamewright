# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/78-studio-to-game-designer.md
next_seq: 80
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/80-game-designer-to-<recipient>.md
- design/<name>
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

<<<FILE goals/G-001-combat-monotony/78-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 78
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 78: studio → game-designer — Bring `combat.md` in line with the step 68 and step 72 specs; fix a stray line in D-007 (documents only)

## Task

Remove the document conflicts QA found, so the next verification has one consistent reference. Edit documents only. Do not change any rule, parameter or player-facing behavior.

## Context

Goal G-001 (combat monotony). Verify 24 (QA report 76, section 6, item 2) found that the build follows `design/combat-step68.md` (D-011) and `design/combat-step72.md` (D-012), but older documents still say otherwise. A QA re-verify follows once a test fix (handoff 77, in parallel) is done, and it will use these documents.

## Findings

Conflicts reported by QA 76:
1. `design/combat.md` still has the old room 3 row (a spitter at (14,7), no grub), the old room 3 purpose, criterion 12, and criterion 11 ("rooms 1–5 never more than 3"). Per D-007 and `combat-step72.md` the room 3 contents are spitters (2,1), (10,6), (2,7) and a grub (15,0), and the in-flight bound is the one D-007 states.
2. `design/combat.md` still says the wind-up message is "a grub rears back (all variants)". `combat-step68.md` and D-011 govern: messages name the variant, and the build prints `a grub/runner/brute rears back` and `YOU ARE HIT by a grub/runner/brute`.
3. `design/combat-cues-visual-spec.md` says spitter cues are "normally 0.8 s apart". That holds only in room 3 and is already noted for the art director. Fix the wording or add a pointer.
4. `decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md` ends with a stray `</parameter>` line, which looks like a formatting leftover. Remove only that line.

## Decisions already made

- D-007, D-011, D-012 (the governing texts). The documents are brought to them, not the other way round.

## Constraints

- Change no numbers or rules. Where a document would need a rule decision to resolve a conflict, do not decide it: report it in the result and hand back with `outcome: question`.
- Do not edit `combat-step68.md` or `combat-step72.md`, or the content of any Decision beyond the stray line in item 4.
- Prefer a short pointer ("see `combat-step72.md`") where copying content would risk new drift.

## Open questions

None.

## Expected output

Address the result to `studio`, `outcome: done`. List each document edited and what changed in Findings. The next step after this and handoff 77 is a QA re-verify (fresh context).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-step68.md, design/combat-step72.md, design/combat-cues-visual-spec.md, project.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/76-qa-to-studio.md
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

<<<FILE design/combat-step68.md
# Combat design addendum, step 68 (stale sentences, manual wording, variant messages)

Status: wording and message strings only. No rule, parameter, timing or room change. Where this file differs from `design/combat.md`, `design/combat-step59.md` or `repo/manual.md`, this file governs. Decisions: D-007 (unchanged), D-011 (accepts and completes D-008).

## 1. Stale sentences, superseded (room 3 in-flight bound)

`design/combat-step-46-room3-cap.md` (amended criterion 11, D-007) governs the cap. These sentences are superseded and must be folded out the next time the files are edited:

- `combat.md`, Cap paragraph: "In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3". Replacement: in rooms 4–5 the count stays at 3 or fewer; in room 3 up to 5 is accepted after a cap delay (2 plus the living spitters).
- `combat.md`, criterion 11: "In rooms 1–5 never more than 3 shots in flight". Replacement: criterion 11 as amended in the step 46 note (a–e).
- `repo/manual.md`, spitter paragraph: "and no more than 3 are in the air at once". Replacement (exact text): "A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once."

## 2. Manual wording for late swipes (step 59, point 1, unchanged rules)

Replace the sentence in the grub warning bullet "or swipe a grub or runner (within 1.5 tiles) to cancel it" with this exact text:

"or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. One swipe is enough to cancel a grub or a runner. A brute is never cancelled."

This covers every point of the step 59 acceptance list.

## 3. Runner cancel vs kill

No separate runner cancel rule is intended. A runner has 1 hp, so a swipe in reach kills it. A late swipe on a runner in reach is therefore a kill, not a cancel, and QA cannot and need not distinguish them. Criterion 6 for the runner reads: an in-reach swipe during wind-up kills it with no lunge.

## 4. Variant messages (D-011; supersedes the message table in step 59 point 2)

| Variant | Mark | Wind-up message | Hit message |
|---|---|---|---|
| Standard grub | `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner grub | `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute grub | `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | n/a | unchanged | `YOU ARE HIT by a shot` (unchanged) |

Rules:
- All three wind-up messages contain `rears back`. Rules keyed on `text "rears back"` match all variants. Rules keyed on `a grub rears back` or `by a grub` match only the standard grub after the change.
- The hit message keeps its current hearts suffix. Only the noun changes.
- Applies in the player view and any other text view that prints these strings. The `cue:` line, `~` line, all timings, the swipe, kill and shrug messages, and spitter messages are unchanged.
- Graphical presentation is not affected.
- Tests and bots that match the old strings are updated by the Build.

Acceptance (verification), at 30 and 60 FPS, practice room, one case per variant:
- V-a. Each wind-up prints its message once, at the same moment as today (±1 frame).
- V-b. A hit by each variant prints the matching hit message on the frame of contact, with unchanged hearts text.
- V-c. All other output is byte-identical to 0.6.1 in the same scripts, apart from these words.
- V-d. `text "rears back"` reacts to all three variants.
- V-e. Criteria 1–11 and 17–21 of `combat.md` hold. No bot result changes.

Experience signal (Review and playtest, not for the Playtester's handoff): a text-view player can say from the message line which kind of grub is attacking or hit them.

## Open questions

- Whether the variant name changes behaviour or only moves a wasted dash is for the next playtest.
- Build timing: only after Review 65, stating the build number if a playtest follows (D-009 item 5).
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

<<<FILE goals/G-001-combat-monotony/76-qa-to-studio.md
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
