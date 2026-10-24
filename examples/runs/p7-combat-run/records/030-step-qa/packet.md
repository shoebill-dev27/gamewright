# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/29-studio-to-qa.md
next_seq: 32
runs: tests, play, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/32-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/29-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 29
from: studio
to: qa
stage: Observe
outcome: routed
---
# 29: studio → qa — Reproduce a possible defect: grub hit right after a lunge-cancelling swipe (room 2)

## Task

Try to reproduce the reported behavior in room 2 and decide whether it is a defect, a rules-conforming case (for example a second grub), or not reproducible. Address the result to `studio`.

## Context

Goal G-001 (combat feels monotonous). A fresh playtester played the current build through input scripts with the player view. In room 2 (2 runners, 1 grub, 2 brutes) they reported:

- a grub began rearing back at about 5.37 s;
- the player swiped and the output said "grub hit" at about 5.9 s;
- the player was hit by a grub at about 6.017 s, about 0.1 s after the swipe.

The manual says a swipe within 1.5 tiles of a rearing enemy cancels its lunge. The playtester could not tell whether the hit came from a different grub or whether the cancel failed, and is unsure it is a defect. Impact judged low. The room 2 start count they saw was probably 1 grub; they noted a second `G` later, which may be a brute, not a grub.

## Findings

Observations only. The playtester's run used a reaction-rule script (sidestep on "rears back", swipe things within about 1.4 tiles, approach). The exact script was not preserved, so reconstruct comparable play with the trace view. The playtester's report is in the previous handoff.

## Decisions already made

- D-002: per-frame contact sampling is kept; the contact-edge graze is an accepted limitation, so check that this case is not just that graze. A lunge-band note for D-002 is with the game-designer in a separate step.

## Constraints

- Verify from the design documents, the manual and the build, not from any explanation of how it should work.
- Check at both 30 and 60 FPS. Use `run_play`, `run_trace` and `run_tests` from `project.md`.
- Report only: do not change the build.

## Open questions

- In the trace, which enemy dealt the 6.017 s hit, and was its lunge cancelled, staggered or already in flight when the swipe landed (distance at swipe time versus the 1.5-tile rule)?
- Is the outcome consistent with the documented rules (design/combat.md, repo/manual.md, D-002)? If the documents are silent or conflict, say so; do not rule on intent.

## Expected output

A defect report with exact reproduction steps and acceptance criteria if it is a defect; otherwise a clear "not a defect / not reproducible" with the trace evidence and, if the documents are unclear, the question for the game-designer. Severity and reproducibility are yours. Address it to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/ (run_play, run_trace, run_tests)
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/27-playtester-to-studio.md
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
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

<<<FILE goals/G-001-combat-monotony/27-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 27
from: playtester
to: studio
stage: Play
outcome: done
---
# 27: playtester → studio — Observation report: combat across rooms 1–5

## Task

Report what I experienced playing combat in the build, with attention to how the rooms and enemies compare.

## Context

This follows handoff 25. I played with the player view only. I did not read source, tests or design documents, and I did not use the trace view.

## Findings

### Method (what I actually did)

- I played only through input scripts run with `python3 play.py --view player`. No live play and no gamepad. The comments about the gamepad profile are therefore my inference, not observed.
- Timed-input script, room 1: wait, swipe and dash at fixed times, regardless of what was on screen.
- Reaction-rule scripts, rooms 1–5:
  - Sidestep on "rears back".
  - Dash aside on "rears back" and on incoming shots.
  - Swipe whatever got within about 1.4 tiles.
  - Walk toward spitters and grubs, or away from brutes.
- Reaction rules react in about 0.15 s every time. That is steadier than a human, so my results probably flatter dodging and hide human-reaction problems.
- **Not seen:**
  - Rooms 2 and 3 output was cut off (room 2 at about 29.5 s, room 3 at about 25 s). I don't know how those sessions ended.
  - I did not see a brute die. I never fully engaged one.
  - I did not see room 3 cleared.
  - I did not try the practice room.
  - I did not try rooms 2–5 with timed scripts.
  - Each reaction script ran once per room (room 1 had three), so single outcomes are anecdotes.

### Session summary

| Room | Enemies at start | Approach | Result I saw |
|---|---|---|---|
| 1 | 3 grubs | Timed script, no reactions | Down at 4.6 s. Three grub lunges hit me. I stood in the lines and swiped one grub. |
| 1 | 3 grubs | Sidestep on "rears back", swipe, approach | Cleared at 4.4 s with 3/3 hearts. |
| 1 | 3 grubs | Dash aside on "rears back", swipe, approach | Cleared at 5.1 s with 3/3 hearts. |
| 2 | 2 runners, 1 grub, 2 brutes (likely; I saw `r`, `r`, `g`, `G`, `G`, then a second `G` later) | Sidestep, swipe close things, approach | Both runners dead by about 5.4 s (one swipe each). The grub took two swipes and cost me one heart (2/3). Then I only dodged brutes for the rest of what I saw (until about 29 s). I did not engage them. |
| 3 | 3 spitters in corners | Dash aside on shots and aim lines, approach spitters | Two spitters killed. One point-blank hit at 5.8 s (2/3). The third spitter kept firing for the rest of the visible 25 s, and I mostly dodged. |
| 4 | 1 runner, 1 grub, 2 spitters | Sidestep, swipe, approach spitters | Runner and grub dead by 2.9 s with no damage. Then I went down at 15.75 s to shots, never having reached a spitter. |
| 5 | 2 grubs, 1 brute, 2 spitters | Same style | Down at 11.1 s, all three hits from shots. I killed 2 grubs, and the brute was still alive. |

### Concrete moments

- **Room 1, timed script.** I felt punished for being passive. The grubs came at me, flashed, and hit me three times in under 3 s. The warning picture and `cue:` line were clear. I simply had not reacted.
- **Room 1, reactive scripts.** Once I stepped aside or dashed on the warning, the room was trivial. Every grub got swiped to death with nothing coming at me. It felt like "see flash, move, hit". Attention dropped by the second grub.
- **Dash versus sidestep in room 1.** I could not tell them apart in practice. Both dodged every lunge, so the dash felt like an optional extra. I never needed it there. A swipe during the warning also cancelled the lunge and staggered the grub.
- **Room 2 runners.** The runners (fast, 1 swipe, short warning) came in pairs and died quickly. They felt like faster grubs, but my swipe-when-close answer was the same.
- **Room 2, odd moment.**
  - A grub began rearing back at 5.37 s.
  - I swiped it ("grub hit") at 5.9 s.
  - I was still hit by a grub at 6.017 s, about 0.1 s later. The manual says a swipe within 1.5 tiles cancels the lunge.
  - I can't tell whether the lunge came from a different grub or my swipe didn't cancel it. I'm flagging it as a possible defect for QA and am not sure.
- **Room 2 brutes.** They were slow with a long warning (0.7 s). Dodging them was easy and boring. They trailed me across the room for 20+ seconds, pausing, rearing and lunging into empty space, and nothing about it made me change how I played.
- **Room 3 spitters.**
  - The aim lines and growing glow were readable. I could see where a shot would go well ahead of time.
  - The sessions were dominated by the same loop: aim line appears, move or dash aside, shot flies past, repeat about every 2.4 s from a spitter I wasn't reaching.
  - I was hit once when two spitters fired at the same instant (5.8 s) and I was close to one of them.
  - Once I was down to one spitter, it felt repetitive and drawn out.
- **Rooms 4 and 5, crossfire.**
  - Two spitters in opposite corners fire in sync, so aim lines fan out across most of the room.
  - Slow shots linger and cross. I was hit by shots already in flight (e.g. 6.9 s in room 4, 8.7 s in room 5) while I was lined up for a different warning.
  - Stepping aside from one line sometimes put me in another. This was the first time anything truly threatened me, and it also felt the least fair.
  - The lines are still visible, but with several at once I could not tell which to avoid.
- **Room 5 mix.** Grubs got killed quickly, and the brute and the spitters carried the danger. The spitters killed me while the brute stayed in the background.

### Issues and impact

1. **Melee enemies (grub, runner, brute) all want the same reaction: sidestep the warning, then swipe or ignore.**
   - Different rooms and enemy types did not make me play differently.
   - The runner's short warning was never a real test, because I always had time.
   - The brute asked for patience, not a different approach.
   - Impact: high on monotony. Rooms 1 and 2 felt interchangeable apart from enemy count.
2. **The dash was never needed.** A one-tile sidestep always sufficed against lunges. Impact: medium.
3. **Spitters are the only thing that changed how I moved.** I had to keep moving, approach, and weigh several lines. Impact: positive for variety, but the solution is again "keep moving". With multiple spitters the room turned into attrition.
4. **Spitter rooms (3–5) end in repetition or an unreadable crossfire.** Impact: medium–high.
5. **Possible defect, room 2 (~5.9–6.0 s):** I was hit by a grub right after a swipe that should have cancelled its lunge. Impact: low; I'm unsure.

### Positives

- Warnings were consistently readable: the message, the `~` line, the `cue:` countdown and the glow. Nothing hurt me without a warning I could see.
- Combat is short and quick. Room 1 cleared in about 4–5 s, which suits short runs.
- Cancelling a lunge by swiping, and the stagger on a swipe, felt good when it worked.
- Spitter rooms had real danger and made me move (a plus for an action player).

### Open player questions

- Is the brute meant to be attacked at all, rather than dodged? I could not find a reason to fight it.
- Is the dash only meant for spitters? I used it in room 1 and room 3, and it only felt necessary against shots.

## Decisions already made

None.

## Constraints

Observations only. No numbers or implementation guesses proposed.

## Open questions

None for the studio beyond the above. The cut-off outputs for rooms 2 and 3 mean I could not report how those sessions ended, and a fresh round with hand-varied timing in rooms 2–5 would add information.

## Expected output

This report. The experience issues (1–4) go to `game-designer`. The possible defect (5) goes to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/25-studio-to-playtester.md
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
