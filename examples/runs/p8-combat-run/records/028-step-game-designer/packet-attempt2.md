# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/26-studio-to-game-designer.md
next_seq: 30
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/30-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-003-<name>.md
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

<<<FILE goals/G-001-combat-monotony/26-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 26
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 26: studio → game-designer — Two non-blocking spec rulings from QA's close-out verification

## Task

Rule on two small points QA raised, and record them where the governing documents say. Neither blocks the playtest, which runs in parallel.

## Context

G-001 (combat monotony). QA verified build 0.5 against criteria 1–17 at 30 and 60 FPS and passed it (handoff 24). The build is unchanged. Two notes concern the contact-edge graze accepted in D-002.

## Findings

From QA's handoff 24, section D:

1. **Shot at exactly the reach (0.40).** A shot whose lateral miss is nominally exactly 0.400 hit at 30 FPS and missed at 60 FPS. At 30 FPS a frame lands exactly on the closest approach and the code treats `distance <= 0.4` as a hit. Criterion 17b says "0.40 or more: no hit at both rates", while the band definition ("reach − 0.01 to reach", 0.39 to 0.40) includes 0.40. QA did not count it as a failure because the spec is ambiguous at exactly the reach; the clean case at 0.407 misses at both rates. Question: is a miss of exactly the reach inside the band (either result accepted) or a guaranteed miss? A guaranteed miss would need `<=` changed to `<`, which is a Build change.
2. **Lunge band width.** QA derived that a lunge hit is guaranteed up to a lateral miss of about 0.585 at 30 FPS, so the band is about 0.015 tile (about 0.004 at 60 FPS). Five probes only; 0.570 hit and 0.610 missed at both rates; the rates disagreed only at 0.590. This was not a full scan. There is no evidence of a band wider than 0.03 tile. QA suggests recording the measured figures in D-002 with the scan limitation stated.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the graze is an accepted limitation.

## Constraints

- Prefer the ruling that leaves the build unchanged. If you conclude the build must change (`<` instead of `<=`), say so and hand back to `studio`; do not decide the Build route.
- Stay within D-001 and the pillars. The numeric ranges in the other criteria are not reopened.
- Keep the edit to wording clarifications, so criteria already verified remain valid.

## Open questions

The two questions above.

## Expected output

- Update `design/combat.md` criterion 17 (and the band definition) so it is unambiguous at exactly the reach; record the measured lunge band and its limits in D-002 (edit that Decision in place, or add a short follow-up Decision if you judge it warranted).
- A handoff to `studio` with your rulings and whether a Build or re-Verify is needed (expected: neither).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/24-qa-to-studio.md
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
# Combat design (build 0.5, specified in G-001 step 07, rulings in steps 14 and 22)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). The player kit is unchanged from 0.4. No build change results from step 22.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002)

- Contact is a distance check made once per frame, after that frame's movement. Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- The accepted band is the lateral miss within these tolerances of the reach:
  - Shots: from reach − 0.01 to reach (0.39 to 0.40 tile). QA derived about 0.003 tile.
  - Lunges: from reach − 0.03 to reach (0.57 to 0.60 tile). QA derived about 0.015 tile at 30 FPS; not yet run.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss smaller than reach − tolerance always hits (if the player is not invulnerable), and a lateral miss of reach or more never hits.
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

Contact edge (new, step 22):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of 0.40 tile or more: no hit at both rates.
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of 0.60 tile or more: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. Between those values (the band) a difference between 30 and 60 FPS is accepted and is not a build defect. In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

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
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11 or 17 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss within the stated tolerance of the reach) is NOT a build defect. QA's step 20 result stands: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted. 16e therefore passes.

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
- Path passing the player at almost exactly the reach (step 22): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
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

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
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

<<<FILE goals/G-001-combat-monotony/24-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 24
from: qa
to: studio
stage: Verify
outcome: pass
---
# 24: qa → studio — Build 0.5 verified against criteria 1–17: pass; V12 stays open; two small notes for the designer (shot tie at exactly 0.40, lunge band)

## Task

Report the close-out verification of build 0.5 against `design/combat.md` criteria 1–17 (plus V12 for the text build), and give the verdict. The next step is a playtest, composed without implementation history.

## Context

G-001 (combat monotony). The build is unchanged since handoff 20. Handoff 23 asked for these checks: 5, 6 and 8 at 30 FPS, the "no renumber" edge case, criterion 17 with known misses, criterion 11 in its new wording, and the unit tests. All evidence below comes from runs made in this step (tests, bots, play/trace scripts). Anything not re-run is marked as carried over. The build and the spec were not changed.

## Findings

### A. Per-criterion result

| # | Result | Evidence |
|---|---|---|
| 1 Telegraph | pass, 30 and 60 | Not re-traced this step. The suite checks the gap ≥ 0.5 s − 1 frame at both rates (34 tests OK). Handoff 20 trace `c1-stand` showed the lunge exactly 0.5 s after the cue. |
| 2 Sidestep | pass, 30 and 60 | Suite (both rates). `c5-30` this step: the player steps up 1.07 tiles during the wind-up and takes no damage from the lunge. |
| 3 Dash | pass, 30 and 60 | Suite (offsets 0, 0.25, 0.5 and 0.6 s, both rates). |
| 4 Standing still | pass, 30 and 60 | Suite (both rates). |
| 5 Safe window | **pass at 30 (new)** and 60 | Trace `c5-30`: the lunge ends at 0.833 s at (7.60, 4.00). The player walks back to (8.00, 3.73), 0.48 tile from the grub and inside the 0.6 reach, during the recovery from about 1.1 s. Hearts stay 3 until the end at 1.5 s, and a swipe at 1.3 s hits the grub (hp 1). The player was never hurt before this, so hurt-invulnerability cannot explain the result. |
| 6 Cancel | **pass at 30 (new)** and 60 | `c6-two-swipes-30`: the grub (hp 2) is hit to hp 1, then defeated by the second swipe at 0.433 s, and the room clears. `c6-cancel-30`: the swipe in wind-up at 0.133 s gives stagger and no lunge by 0.9 s. The stagger lasts exactly 0.4 s, and the wind-up then restarts at 0.533 s. A kill in wind-up with no stagger and no lunge: runner, handoff 20 `c6-kill-windup` at 30 and 60, carried over, plus `c8-runner-30` this step (defeated, cleared, no stagger event). |
| 7 One at a time | pass, 30 and 60 | Suite (maximum 1 grub in wind-up or lunge, both rates). |
| 8 Variants | **pass at 30 (new)** and 60 | `c8-runner-30`: 1 swipe. `c8-brute-30`: 4 swipes (hp 4→3→2→1→defeated at 1.233 s). Standard grub: 2 swipes (see 6). Marks `r` and `G` are in the suite and listed in `manual.md`. |
| 9 Aim cue | pass, 30 and 60 | `room3-30` and `room3-60`: aim at 1.200 s, spit at 1.800 s (0.600 s at both rates). The shots go along the locked line (hit traces in 17). |
| 10 Dodge | pass, 30 and 60 | Suite. `b-miss` traces: the 1-tile-class sidestep gives no hit at either rate. |
| 11 Stagger and cap | **pass, 30 and 60** | See section B. |
| 12 Rooms | pass | Suite compares rooms 2, 4 and the brute in room 5. Handoff 20 read all five rooms against the table; `game.py` is unchanged. |
| 13 | pass at each rate | See section C. |
| 14 | pass at each rate | See section C. |
| 15 Dash used | pass at each rate | Dodger dashes in rooms 3/4/5: 8/7/11 at 30 FPS and 10/8/14 at 60 FPS. |
| 16a | pass | The gaps from handoff 20 (5, 6, 8 at 30 FPS) are closed. 17 is covered below. |
| 16b | pass | Section C. |
| 16c | pass | The dodger is identical at both rates: 0 hearts lost in every room, 5/5 cleared. |
| 16d | acknowledged | Walker per room, 30 FPS: 3✗ 2✓ 0✓ 1✓ 3✗. At 60 FPS: 3✗ 2✓ 2✓ 2✓ 2✓. The same figures as in handoff 20. |
| 16e | pass | No new finding. The walker differences are bot timing (handoff 20, section D). The contact-edge differences found in 17 are inside the accepted band. |
| 17 Contact edge | **pass**, with two notes (section D) | Shot misses of about 0.39 hit at both rates and about 0.41 miss at both. Lunge misses of 0.570 hit at both rates and 0.610 miss at both. Differences between rates appear only at lateral misses of 0.40 (shot) and 0.59 (lunge). |
| Edge: no renumber | **pass, 30 and 60** | Section E. |
| V12 | open | There is no graphical build. The text-build timings hold at both rates (wind-up to lunge exactly 0.5 s, aim to spit 0.6 s). V12 stays open until a graphical build exists. |

### B. Criterion 11 in its new wording

- **Room 3, first shots.** `room3-30` and `room3-60` both spit at 1.800, 2.600 and 3.400 s. The cues start 0.6 s earlier, at 1.2, 2.0 and 2.8 s.
- **Room 3, cap.** The suite counts the shots in flight over 12 s at both rates. The maximum is at most 3, and the suite passed.
- **Four-spitter practice room** (`four-30` and `four-60`): spitters at (0,0), (0,3), (0,5), (0,8), player at (15,4). The results at 30 and 60 are the same, down to the printed messages and times.
  - The first three spitters cue at 1.2, 2.0 and 2.8 s with fewer than 3 shots in flight. They spit at 1.8, 2.6 and 3.4 s.
  - The fourth spitter's cue (due at 3.6 s) and the repeat cues of the others are blocked. At those checks the three earlier shots are in flight.
  - The 1.8 s shot leaves at its 5 s life limit. Only then, at 6.8 s, do all four cues start together, with 2 shots in flight at each check.
  - All four spit at 7.4 s. By my count that is the 2 older shots plus 4 new ones, so at most 6 in flight. That equals 2 + 4 living spitters, which is the limit. I derived this from the traces, the 2 older shots are still visible at 6.5 s and 7.0 s, and I did not count it directly.
  - The player view shows "YOU ARE HIT" at 7.467 s and 8.267 s at both rates, so the shots really are in flight.
  - Result: a cue starts only when fewer than 3 shots are in flight, the maximum stays within 2 + living spitters, and the cap delay carries forward. All of this matches the spec.
- **Manual wording.** `manual.md` says "no more than 3 are in the air at once". This is true in rooms 1–5, which are the only rooms a player meets. The count can be higher only in a practice room with four or more spitters, which is a script feature. I do not consider the sentence misleading for a player. If the Studio wants it exact, "in the five rooms" would remove the gap. I did not edit the manual.

### C. Bots and regression (bots run at 30 and 60 FPS, `log` off)

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker lost, rooms 3–5 (need 3–6) | 0+1+3 = 4 | 2+2+2 = 6 (top of range) |
| Walker cleared, rooms 3–5 (need ≥ 2) | 2 | 3 |
| Dodger lost / cleared, rooms 3–5 (need ≤ half the walker's loss; 3/3) | 0 / 3 | 0 / 3 |
| Camper cleared, rooms 3–5 (must be < walker) | 0 | 0 |
| Walker lost, rooms 1–2 (need ≥ 1) | 3+2 = 5 | 3+2 = 5 |
| Dodger lost / cleared, rooms 1–2 (need ≤ 1; both cleared) | 0 / 2 | 0 / 2 |

- These figures are identical to handoff 20. The walker at 60 FPS stays at exactly the limit of 6. Per the step 22 ruling, a result of 7 would be a tuning question and not a defect.
- Camper room 2: cleared at 30 FPS (2 hearts lost), not cleared at 60 FPS (3 lost). No criterion covers the camper in rooms 1–2. I note it only as an observation.
- `python3 -m unittest discover -s tests`: 34 tests, OK.
- Nothing else regressed. All figures equal the earlier handoffs.

### D. Criterion 17: contact edge

Reproduction: `room empty`, one spitter or grub, the player locked on at (8, 4.0) and then moved to a final position, as in handoff 20. The lateral miss is the perpendicular distance of the player's final position from the locked line. I calculated it from the positions printed in the traces.

**Shots (reach 0.4)**

| Spitter at | Final player y | Lateral miss | 30 FPS | 60 FPS |
|---|---|---|---|---|
| (1.0, 2.4) | 3.60 | 0.390 (0.3899) | hit at 4.133 s | hit at 4.133 s |
| (5.0, 6.5) | 3.47 | 0.407 | no hit | no hit |
| (1.04, 3.70) | 3.60 | 0.3996 (band) | no hit | hit at 4.100 s |
| (1.0, 4.0) | 3.60 | nominal 0.400 | hit at 4.100 s | no hit |

- 17a passes (0.390 is a hit at both rates). 17b passes (0.407 is a miss at both rates).
- The difference at 0.3996 is inside the accepted band. Only hit or miss differs. The aim and spit times are identical (1.2 s and 1.8 s).
- **Note 1, shot at exactly 0.40 (for the designer).** The row with a nominal 0.400 miss hit at 30 FPS and not at 60 FPS.
  - At 30 FPS a frame lands exactly on the closest approach (x = 8.0), and the code treats `distance <= 0.4` as a hit. The actual miss is 0.4 within float noise, and I cannot read the float value from the trace.
  - 17b says "0.40 or more: no hit at both rates". The band definition says "from reach − 0.01 to reach (0.39 to 0.40)", which includes 0.40.
  - I did not count this row as a 17b failure, because the spec is ambiguous at exactly the reach and the clean case at 0.407 passes. I treat it as a spec question: is a miss of exactly the reach inside the band (differences accepted) or a guaranteed miss? If it is a guaranteed miss, `<=` would need to become `<`, which is a Build change.

**Lunges (reach 0.6), grub standing near, player at (8.0, 3.2) at lunge time**

| Lateral miss | 30 FPS | 60 FPS |
|---|---|---|
| 0.570 | hit at 0.667 s | hit at 0.650 s |
| 0.580 | hit at 0.667 s | hit at 0.650 s |
| 0.590 | **no hit** | hit at 0.667 s |
| 0.599 | hit at 0.667 s | hit at 0.650 s |
| 0.610 | no hit | no hit |

- 17c passes: 0.570 hits at both rates, and 0.610 misses at both rates.
- In the hit cases the lunge starts at 0.533 s (30) and 0.517 s (60). The hit comes 0.133 s later at both rates, so timing, cue and message are the same. Only the hit itself differs, at 0.590.
- **Note 2, lunge band width (for the designer).** My calculation is that a lunge hit is guaranteed up to a lateral miss of 0.585 at 30 FPS, which makes the band about 0.015 tile and not more than 0.03. That is the derivation: a frame step of 0.267 tile needs the sampled point within 0.133 tile along the line. At 60 FPS the same calculation gives about 0.004 tile.
  - Measured with five probes only: the 30 FPS disagreement appeared only at 0.590, and no probe at 0.570 or below missed. The 0.599 probe hit again at 30 FPS because the frame phase differs between positions. I did not scan the whole range.
  - There is no evidence that the band is wider than 0.03 tile, so I do not report this as a spec failure. The designer may want to record "about 0.015 at 30 FPS, 0.004 at 60 FPS" in D-002 as measured, with the scan limitation stated.

### E. Edge case: a defeated spitter does not renumber the others

Script `renum-30` and `renum-60`: three spitters in spawn order, with the first one (1,1) killed by two swipes before 0.5 s.

- The next two spitters keep their own timers: aim at 2.000 s and spit at 2.600 s for the second spitter (k = 1), then aim at 2.800 s and spit at 3.400 s for the third (k = 2).
- Renumbering would have moved the shots to 1.8 s and 2.6 s. That did not happen.
- The second spitter fires again with its cue at 4.400 s, as it should (2.6 + 2.4 = 5.0 s).
- The results are identical at 30 and 60 FPS.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the graze is an accepted limitation. Notes 1 and 2 above concern the revisit condition in D-002 and the band numbers.

## Constraints

- The build and the spec were not changed.
- Verified from the spec, the criteria and the build, at 30 and 60 FPS.
- V12 is not assessable in the text build.

## Open questions

For `game-designer`, via the Studio. These are not blocking, and the verdict does not depend on them:

1. A shot whose lateral miss is exactly the reach (0.40): inside the band (either result accepted) or a guaranteed miss? See Note 1.
2. Please record the measured lunge band for D-002 (about 0.015 tile at 30 FPS, derived and probed at five points; not a full scan). See Note 2.

## Expected output

- Verdict: **pass**. Criteria 1–17 hold at 30 and 60 FPS with the figures above, and V12 is open until a graphical build exists. There is no failing criterion.
- The Studio can route to the playtest. The Playtester gets no implementation history, and the walker margin and the notes above are not needed by the Playtester.
- Notes 1 and 2 go to `game-designer` when convenient.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/23-studio-to-qa.md
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

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- decisions/D-002-contact-edge-graze-accepted.md: not on the write list
