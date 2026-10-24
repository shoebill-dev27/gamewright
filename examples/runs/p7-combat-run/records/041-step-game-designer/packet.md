# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/42-studio-to-game-designer.md
next_seq: 44
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/44-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-006-<name>.md
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

<<<FILE goals/G-001-combat-monotony/42-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 42
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 42: studio → game-designer — Tuning question on criterion 13 (walker bot, 60 FPS, rooms 3–5)

## Task

Rule on criterion 13 with `write-design-spec`: build 0.6's walker bot loses more hearts in rooms 3–5 at 60 FPS than the criterion allows. Decide whether the limit, the criterion's wording or a room or enemy parameter should change, and write the result as a spec amendment with player-observable acceptance criteria.

## Context

G-001 (combat monotony). The engineer finished build 0.6 per Design 35 and 38 (D-004, D-005) and found no spec gap. All criteria it checked hold except one bot figure: the walker bot (a deliberately naive player that walks toward enemies and swipes) loses 7 hearts in rooms 3–5 at 60 FPS (4 at 30 FPS), against criterion 13's limit of 6. Other criterion 13 limits hold: the walker clears 2 of 3 rooms at both rates, the dodger loses 0 and clears 3 of 3, the camper clears fewer rooms than the walker. Build 0.6 is going to QA for Verify in parallel (41); QA will report its own measured figures.

## Findings

Engineer's bot figures for 0.6 (hearts lost; `run_bots`, limit 60), for your reference. QA will re-measure.

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker room 3 | 0 lost, cleared | 2 lost (shots), cleared |
| Walker room 4 | 1 lost (grub), cleared | 3 lost (grub 1, shot 2), not cleared |
| Walker room 5 | 3 lost (grub 2, shot 1), not cleared | 2 lost (grub), cleared |
| Walker rooms 3–5 | 4 lost, 2 of 3 cleared | 7 lost, 2 of 3 cleared |
| Dodger rooms 1–5 | 0 lost, 5/5 cleared | 0 lost, 5/5 cleared |

- The 0.5 values in the spec were: walker rooms 3–5 4 lost and 2 cleared at 30 FPS, 6 lost and 3 cleared at 60 FPS. So the 30 FPS figure is unchanged and the 60 FPS figure moved from 6 to 7 hearts with one fewer room cleared.
- The engineer reports the walker is sensitive to its 0.15 s decision grid, and per-room totals moved in opposite directions between 0.5 and 0.6.
- The 30/60 difference comes from bot timing, not from a rule difference; criterion 16 (rates agree for the dodger) holds.
- Hearts lost by the walker in rooms 1–2 are 5 (criterion 14 wants at least 1), which is unchanged in intent.

## Decisions already made

- D-001: one-button combat; no new input.
- D-004: rooms 4–5 cue gap 0.6 s; brute not cancelled; room 2 spitter deferred.
- D-005: blocked contact consumes the shot and spends the lunge hit.
- Design 35 and 38 are the approved spec for 0.6; the engineer built it as written.

## Constraints

- Must play correctly at both 30 and 60 FPS; the pillars apply (readable threats, short runs, one-button combat).
- Prefer changes that reuse existing systems; no new enemy, healing, input or room content.
- Do not undo D-004 or D-005. If the answer needs a change that contradicts them or a scope or priority change, hand back for Decide (`game-director`).
- The purpose of criterion 13 is a gradient: the naive player is punished more than the dodger, but not walled out. Keep that purpose, state whether 7 at 60 FPS breaks it, and give the reason.

## Open questions

- Is 7 hearts for the walker at 60 FPS a breach of intent, or is the limit of 6 too tight for a grid-sensitive bot? If the limit changes, what should it be, and should it be expressed as a range across both rates?
- If a parameter should change instead, which one, and what must QA re-verify afterwards?
- Does the answer depend on QA's independent figures? If so, say which figure would change your ruling.

## Expected output

An amendment to the spec (in `design/combat.md` or a design note you name) and a handoff to `studio` (`kind: handoff`, `from: game-designer`, `to: studio`) stating the ruling, the changed criteria and, if a build change is needed, the exact change list. Record a Decision if the ruling constrains later work.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/diagnose-experience.md
- Project: design/combat.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/40-gameplay-engineer-to-studio.md
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

<<<FILE studio/skills/diagnose-experience.md
---
name: diagnose-experience
description: Turn experience observations into likely causes and solution options in design terms, with trade-offs, without choosing a direction that is not yours.
---
# Skill: Diagnose experience

Typical roles: game-designer, game-director.

## When to use

Observations show an experience problem whose cause is not understood.

## Inputs

Observation reports, the project vision and player profile, relevant design documents, Decisions.

## Method

1. Cluster observations into symptoms. Keep the evidence attached to each.
2. For each symptom, name candidate causes in design terms (rules, systems, parameters, feedback,
   pacing, readability). Prefer causes that explain several symptoms.
3. Generate 2–3 genuinely different solution options. For each: what it changes, which symptoms it
   addresses, cost, risk, and fit with the vision and Decisions.
4. Mark any option that would change a pillar, a Decision, scope or risk significantly — those are
   not yours to choose.
5. State what the evidence cannot settle.

## Output

Diagnosis: symptoms with evidence, causes, options with trade-offs and vision fit, unknowns, and
your recommendation if one is defensible.

## Do not

Pick a direction outside your authority. Do not present a single option as if it were the only one.
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

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE goals/G-001-combat-monotony/40-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 40
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 40: gameplay-engineer → studio — Build 0.6 done: cue gap, brute no-cancel, consumed shots, spent lunges

## Task

Compose an independent Verify handoff for `qa` for build 0.6 (`repo/`). Route the walker figure below (7 hearts in rooms 3–5 at 60 FPS, over criterion 13's limit of 6) to `game-designer` as a tuning question. It is not a build defect.

## Context

G-001 (combat monotony). Build 0.6 implements the complete change list from handoffs 38 and 39 (D-004, D-005). No spec gap was found, so there are no questions. Contact detection is unchanged: still `distance <= reach` per frame after movement.

## Findings

What changed, per item (files `repo/game.py`, `repo/bots.py`, `repo/tests/test_game.py`, `repo/manual.md`, `repo/README.md`):

1. **Spitter offset per room.** `ROOM_SPIT_STAGGER = {"4": 1.2, "5": 1.2}`; every other room and the practice room use 0.8 s. The offset is applied when an enemy is spawned, so first shots in rooms 4–5 are at 1.8 s and 3.0 s. Room 3 stays at 1.8, 2.6 and 3.4 s.
2. **Cue gap rule, rooms 4–5 only.** `Game._gap_blocks` is checked in `_update_spitter` together with the cap. A cue is blocked if another living spitter has a cue running, or if the last shot in the room (`Game.last_shot`) was less than 0.6 s ago. The comparison uses a 1 ms tolerance. A blocked check waits 0.2 s, the same mechanism as the cap delay. A cancelled cue (spitter killed) never sets `last_shot`. Room 3 and practice rooms do not use the rule (`GAP_ROOMS = ("4", "5")`).
3. **Brute wind-up not cancelled.** A `cancels` flag per variant in `GRUBS`: grub and runner true, brute false. A swipe that damages but does not kill a brute in wind-up logs a `shrug` event, and the phase, timer and aim are untouched. Several swipes each log one. A kill in wind-up logs no `shrug` and no lunge. The text view shows "the brute shrugs off the swipe" for `shrug`. I did not re-read `play.py` in this step, so I could not confirm that it prints this message. `play.py` is not among the files I may write. The trace shows the `shrug` event. QA must check that the player view prints the message, and if it does not, this is a gap in `play.py` to hand back.
4. **Dodger bot.** `bots.py` previously swiped any wind-up in reach, including the brute's. It now swipes a wind-up only when `GRUBS[kind]["cancels"]` is true. Against the brute it sidesteps or dashes on the cue and swipes in recovery. A test (`test_dodger_never_swipes_a_brute_in_wind_up`) checks the log in room 2.
5. **Shot consumed on any contact.** In `_update_shots`, a contact with `hearts > 0` now always removes the shot. `_hurt` is called only when the player is not invulnerable. This covers dash, hit-stun and the hurt window.
6. **Lunge hit spent.** Each grub has a `spent` flag, reset at the start of each lunge. A contact while `self.invulnerable` sets `spent` with no damage, and the lunge is not cancelled or shortened. After that, no damage for the rest of that lunge. The next lunge damages normally, and a lunge whose first contact comes after the protection ended hits.
7. **No change** to the gap rule for room 3 or practice rooms, nor to contact detection.
8. **Manual.** Version 0.6. It adds the brute no-flinch lines and the gap-room sentence, and amends the stagger sentence with the brute exception. It adds the two blocked-contact lines (a) and (b) in the exact wording of handoff 39. `README.md` is updated to 0.6 and the dodger's brute policy.

**Code finding (late damage in 0.5).** Confirmed by reading the 0.5 code. `_update_shots` only checked `close and not self.invulnerable`. A shot that touched a player who was dashing or in the hurt window was kept and flew on. A shot aimed at the player stays within 0.4 tile for about 0.27 s of flight (0.8 tile at 3.0 tiles/s). So it could still be within reach when the hurt window ended and hit then. This fits QA's observed hits at the end of the window (4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS). I did not re-run 0.5 traces to confirm those exact times. In 0.6 the shot is consumed on first contact, and the test `test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end` covers it at both rates.

**Tests.** `python3 -m unittest discover -s tests`: 54 tests, OK, in the last run (run round 2). New tests cover items 2, 3, 5 and 6 at 30 and 60 FPS:
- `BruteTest`: one swipe, two swipes, a kill in wind-up, dash plus swipe, and a swipe in recovery.
- `CueGapTest`: first shots 1.8 / 3.0 in rooms 4–5 with gap and overlap checks over 15 s; the 0.8 s offset kept elsewhere; forced simultaneous first shots; a cancelled cue; a cap delay with the player far west.
- `ShotContactTest`: hurt window, dash ending inside the old line, normal hit, a miss above the reach, a hit after the window, and two shots together.
- `LungeContactTest`: dash against the wall for a grub and a brute, a window ending mid-lunge, a first contact after the window, and the next lunge hurting.
- Existing tests adjusted for the new rules: the swipe-cancel test now covers grub and runner, with runner hp set to 2 because the swipe would kill it. The variants swipe test swipes the brute in recovery. In the bots test I removed the walker's upper bound of 6 hearts (see figures), and added a dodger dash check for criterion 15 in rooms 3–5.

**Bot figures on 0.6** (hearts lost; `run_bots`, `limit 60`):

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker room 1 | 3 lost, not cleared | 3 lost, not cleared |
| Walker room 2 | 2 lost, cleared 8.4 s | 2 lost, cleared 8.4 s |
| Walker room 3 | 0 lost, cleared 9.6 s | 2 lost (shots), cleared 9.5 s |
| Walker room 4 | 1 lost (grub), cleared 9.9 s | 3 lost (grub 1, shot 2), NOT cleared 11.1 s |
| Walker room 5 | 3 lost (grub 2, shot 1), NOT cleared 10.2 s | 2 lost (grub), cleared 12.9 s |
| Walker rooms 3–5 | **4 lost, 2 of 3 cleared** | **7 lost, 2 of 3 cleared** |
| Walker rooms 1–2 | 5 lost | 5 lost |
| Dodger (all rooms) | 0 lost, 5/5 cleared | 0 lost, 5/5 cleared |
| Dodger dashes, rooms 3 / 4 / 5 | 8 / 7 / 11 | 10 / 8 / 14 |
| Camper rooms 3–5 | 0 cleared | 0 cleared |

- Dodger clear times at 30 FPS, rooms 1–5: 6.6 / 20.7 / 19.7 / 18.3 / 24.2 s. At 60 FPS: 9.6 / 25.1 / 22.1 / 17.0 / 28.8 s.
- Camper room 2 is cleared at 30 FPS (2 lost) and not at 60 FPS.
- Criterion 13: the 60 FPS walker loses **7** hearts in rooms 3–5, over the limit of 6. The 30 FPS walker is at 4. The other 13 limits hold: the walker clears 2 of 3 at both rates, the dodger loses 0 and clears 3/3, and the camper clears fewer rooms than the walker. This is the tuning question already foreseen in steps 22, 35 and 38. I did not tune.
- Criterion 14: the walker loses 5 in rooms 1–2 (limit: at least 1), and the dodger loses 0 and clears both rooms.
- Criterion 15: the dodger uses at least 7 dashes in each of rooms 3–5 at both rates.
- Criterion 16c: the dodger's rooms agree between rates (cleared sets equal, 0 hearts lost).
- The 0.5 values I have for comparison are those in the spec (walker rooms 3–5: 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS). I do not have the per-room 0.5 figures from handoffs 13–16 in this packet.

**How to exercise it (for QA):**
- Practice room with `spawn brute 9 4`, a swipe at 0.1 s and another at 0.5 s: the lunge comes at about 0.717 s, and the swipes show `shrug`. In the trace the brute is at hp 3 and then 2, the lunge hits, and the hurt window runs to the end.
- Rooms 4 and 5, 15 s or more at both rates, for the gap, overlap and first shots at 1.8 / 3.0.
- A practice room with one spitter and a grub, for the hurt-window and dash scripts of criteria 20 and 21.

**Known risks:**
- Bot figures for 13–15 are outside or at the limit as listed above. Bots are deterministic, but the walker is sensitive to its 0.15 s grid.
- The simultaneous first-shot test uses the room data with the spitter `fire_in` forced equal, as allowed by criterion 18d for rooms 4–5.
- The `play.py` message for `shrug` is unchecked (see item 3).

## Decisions already made

D-001 to D-005 are respected: no new input, enemy, healing or room content, contact detection untouched, and the gap rule not extended to room 3 or the practice room.

## Constraints

None changed. Visual criteria and art-director items remain deferred.

## Open questions

- For `game-designer`: the 60 FPS walker loses 7 hearts in rooms 3–5, over criterion 13's limit of 6. The figures above are the evidence. This is a tuning or limits question, and the build is unchanged for it.
- For QA: whether `play.py` prints "the brute shrugs off the swipe" for the `shrug` event (item 3), and the real-room trace of room 3 requested in handoff 38.

## Expected output

The Studio composes the Verify handoff for `qa` from the changes and criteria above. It must not include the Sender assessment.

## Sender assessment

Confidence is high that the rules match the spec: the tests cover every listed item at both rates and pass. Medium confidence on bot behavior, since the walker is grid-sensitive and its totals moved in opposite directions per room. I read the 0.5 mechanism in the code rather than reproducing it on a 0.5 trace. The `play.py` message path is the one thing I could not check.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, project.md#constraints
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/39-studio-to-gameplay-engineer.md
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
