# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/33-studio-to-game-designer.md
next_seq: 35
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/35-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-004-<name>.md
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

<<<FILE goals/G-001-combat-monotony/33-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 33
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 33: studio → game-designer — Specify Options 1 and 2 from your second Diagnose, plus manual wording

## Task

Write the design spec (`write-design-spec`) for the changes your Diagnose (handoff 31) recommended as "do": Option 1 (breathing room in spitter rooms 4–5) and Option 2 (the brute's wind-up swipe does not cancel its lunge). Decide yourself whether Option 3 (room 2 spitter) belongs in this slice. Also settle the manual wording items below.

## Context

G-001 (combat monotony). Build 0.5 passed QA (criteria 1–17). The fresh playtest (27) still found monotony: melee enemies share one answer and rooms 4–5 crossfire feels unfair. Your Diagnose (31) ranked the options; the Studio found no Decide needed because all options stay inside D-001 and the pillars. A parallel QA step (handoff 34) is tracing spitter fire times in rooms 3–4, because the playtest said "in sync" and "opposite corners", which conflicts with the spec. That result arrives after this step.

## Findings

- From 31: S1 (melee share one answer) is the core cause of "monotonous". S4 (rooms 4–5 crossfire) is the most important problem: the next cue locks 0.2 s after the previous one ends, at the position the player dodged to. Options 1 and 2 are independent and can be built together.
- From 32 (QA, room 2): the "grub hit right after a swipe" was not a defect. The swipe landed after the 0.5 s wind-up had ended, so the lunge continued, which conforms to `design/combat.md`. `repo/manual.md` says "swipe it (within 1.5 tiles) to cancel the lunge" without saying this works only during the warning. QA asks whether the manual should say so; this is a wording question, not a rule change.
- Known manual item: "no more than 3 in the air" is true in rooms 1–5 only.
- Runner and brute behavior for a human, and the real crossfire experience, are unconfirmed by scripted evidence; a hand-timed playtest will follow the Build.

## Decisions already made

- D-001: attack and dash only; no new input.
- D-002, D-003: per-frame contact sampling, graze accepted, exactly the reach is inside the band.

## Constraints

- Stay inside D-001 and the pillars (one-button combat, short runs 15–20 min, readable threats); reuse existing systems; correct at 30 and 60 FPS.
- Keep lane geometry identical across variants (visual spec); if a change needs presentation work, name it for the `art-director` rather than styling it.
- Make Option 1 robust whether or not the spitters currently fire together: state the required gap between cue windows as a rule in the spec, with player-observable criteria, and do not depend on the "in sync" claim.
- Every new or changed criterion must be checkable by scripts or bots at 30 and 60 FPS. Say which existing criteria change (for example 6, 8, 13, 14) and re-derive the affected bot expectations, flagging any you cannot verify without running the bots.
- Wording of `repo/manual.md` is player-facing text that ships with the build: give the exact lines to add or change (swipe cancels only during the warning; the brute rule if Option 2 is taken; the "3 in the air" scope). The Build step will apply them.

## Open questions

- Include Option 3 in this slice or defer it? Your call; say why.
- Does the Option 2 change need any signal to the player beyond the manual (for example a cue-text line)? If it does, name it as an item for the `art-director`.
- If you find the changes need a new enemy type, healing, new input, or a scope or priority change, stop and hand back to the Studio for a Decide step.

## Expected output

Update `design/combat.md` (and the visual spec only if needed), then write a handoff addressed to `studio`: the rulings, the changed and new criteria, the exact manual wording, whether Build is needed (expected yes), what QA must verify, and anything the Playtester should be asked to focus on without revealing the expected result. Record a Decision only if a real alternative was rejected.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Previous handoff: goals/G-001-combat-monotony/31-game-designer-to-studio.md (also read goals/G-001-combat-monotony/32-qa-to-studio.md for the manual wording question)
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
# Combat design (build 0.5, specified in G-001 step 07, rulings in steps 14, 22 and 30)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). The player kit is unchanged from 0.4. No build change results from steps 22 or 30.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

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
   - Text view: message "a grub rears back" when it starts.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above.
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- A swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up changes its phase, and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery.
- Hurt-invulnerability (0.8 s) also stops the damage the same way.
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) |
|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + 0.8 s × k. After that each spitter fires every 2.4 s after its previous shot. With three spitters, shots are 0.8 s apart.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles.

| Room | Contents (changes from 0.4 in bold) | Purpose |
|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) (unchanged) | Teach the lunge cue against one grub at a time |
| 2 | **Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0)** | Different from room 1: fast fragile ones plus a slow tough one, from four corners |
| 3 | Spitters at (2,1), (14,7), (2,7) (unchanged), with the new stagger and cue | Learn the aim cue |
| 4 | **Runner (1,4)**, Standard (0,1), Spitters (15,0), (15,8) | Grub lunges under fire |
| 5 | Standard (1,1), Standard (0,6), **Brute (4,8)**, Spitters (15,0), (15,8) | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored".
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel.** Two swipes kill a standard grub. A swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four. Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame. In rooms 1–5 never more than 3 shots in flight. In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above.
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin: walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for the current build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change is required.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12 and 17 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11 or 17 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. QA's step 20 result stands: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted. 16e therefore passes.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots now decide on a 0.15 s time grid and the dodger reads cues; no further bot change is needed for 13–16 as written.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now.
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue.
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |

For `art-director`: nothing in the visual spec must change. Only its sentence that "the design text says thin line" is out of date after this step, and the V1–V11 points need no rework. V12 stays open until a graphical build exists. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003).

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
# Lantern Depths — how to play build 0.5

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
  4 swipes, long warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side, dash, or swipe it
  (within 1.5 tiles) to cancel the lunge. The warning lasts 0.5 s for a grub, 0.35 s for a runner,
  0.7 s for a brute. After a lunge the grub is harmless for a while: that is the time to swipe it.
  Only one grub rears back or lunges at a time.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second, and no more than 3 are in the air at once.
- Being hit shows `YOU ARE HIT by a grub` or `by a shot`. A swipe that interrupts a grub's warning
  staggers it for 0.4 s.
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
