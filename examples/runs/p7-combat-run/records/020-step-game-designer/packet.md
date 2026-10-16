# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/21-studio-to-game-designer.md
next_seq: 22
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/22-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-002-<name>.md
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

<<<FILE goals/G-001-combat-monotony/21-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 21
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 21: studio → game-designer — Rule on the frame-rate-dependent graze, the shot cap, the walker margin and the doc contradictions

## Task

Answer four spec questions raised by QA's verification of build 0.5, in a ruling written for the Studio. The main one: is a frame-rate-dependent hit/miss at the contact edge acceptable in the text build? If not, state the rule precisely enough that `gameplay-engineer` can build it and QA can verify it.

## Context

Goal G-001 (combat feels monotonous). Build 0.5 implements your cues, variants and rooms (criteria 1–16). QA verified it independently (handoff 20). Criteria 1–15 and 16a–d pass. For 16e, the walker's 30/60 FPS differences are caused by bot decision timing, which is not a build defect (the exact cause is a float tie at the bot's 2.5 threshold in room 1). QA did find one scripted case where the game itself gives different outcomes at 30 and 60 FPS with identical input. QA does not decide whether that is acceptable, so it is yours. The Timing rule in the spec only guarantees "no tunnelling". The answer decides whether 16e passes as ruled (the verdict becomes pass) or the Build reopens. This is the first failure of criterion 16, so no technical-director re-plan is triggered.

## Findings

All facts below are QA's, from runs it made in step 20. Figures marked "derived" were calculated, not run.

### 1. Frame-rate-dependent graze (the main question)

- Shot reach is 0.4 tile. Contact is a distance check once per frame. A shot moves 0.1 tile per frame at 30 FPS and 0.05 at 60 FPS.
- Reproduction (`python3 play.py --view trace`, run at `fps 30` and at `fps 60`):

```text
room empty
fps 30            # and 60
spawn spitter 1.04 3.70
1.3 move up
1.4 stop
end 5
```

| Spitter position | 30 FPS | 60 FPS |
|---|---|---|
| (1.04, 3.70) | no hit, 3 hearts at 5 s | hit at 4.100 s, 2 hearts |
| (1.00, 3.70) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.73) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.76) | hit at 4.100 s | hit at 4.117 s |

- Cause: the first shot is locked on the player at (8, 4.0) at the cue start (1.2 s). The player then stands at (8, 3.6). The shot line passes the player at a perpendicular distance of about 0.3996, which is 0.0004 inside the reach. A hit needs a sampled frame within about ±0.017 tile of the closest approach. That window is narrower than the frame step at both rates, so which rate catches it depends on the phase.
- Size (derived): only a lateral miss within about 0.003 tile of the 0.4 reach is affected (the shot's step is 0.1 tile at 30 FPS and 0.05 at 60 FPS). Clearly closer always hits and clearly farther never does, at both rates. Grub lunges (reach 0.6, step up to 0.27 tile at 30 FPS) probably have a wider band, about 0.015 tile at 30 FPS. Grubs were not tested. QA rates severity low. The effect is a hit or a miss only and does not change timing.
- 16e says a build defect is "same decision, same time, same positions, different outcome". Read literally, this matches. QA did not decide.

### 2. Shot cap: limit on cue starts, or on shots in flight?

Criterion 11 says "never more than 3 in flight". In the practice-room trace `cap-four-spitters-60` (four spitters, no real room has this), the cap is checked only when a cue starts. Three spitters start cues at 4.6 s, and each check sees 2 shots in flight. At 5.2 s all three fire while the shots from 2.6 s and 3.4 s are still in flight, so 5 shots are in flight (QA's count; the trace shows hits at 5.3 s and 6.1 s). Room 3 (three spitters) stays ≤ 3 in the test. Which does the spec mean?

### 3. Walker margin in rooms 3–5 at 60 FPS

The walker at 60 FPS loses 2+2+2 = 6 hearts in rooms 3–5, the top of criterion 13's range (3–6). At 30 FPS it loses 0+1+3 = 4 and clears 2. One more heart lost would break 13. The dodger loses 0 and the camper clears 0, at both rates. Keep the margin as it is, or retune? (A tuning change is a Build.)

### 4. Contradictions between design/combat.md and design/combat-cues-visual-spec.md (QA reported them; no ruling yet)

- **Lunge line.** `combat.md` says a thin orange-red line for the lunge path. The visual spec draws a lane 1.2 tiles wide.
- **Spitter glow.** `combat.md` and the text view start the glow at 0%. The visual spec requires a floor of at least 30%.
- **Grub cue behaviour.** `combat.md` says the grub flashes for the whole wind-up. The visual spec says a steady tint with a slight pulse (no strobe, ≤ 3 Hz), and the lane stays at full strength until the lunge starts and fades during it. The text view removes the line when the lunge starts.
- **Text marks.** `combat.md` leaves the `r` / `G` marks open for the graphical build. The visual spec uses silhouette and size, which answers that open question.

These matter for a future graphical build, not for the text build. The visual points V1–V11 are already planned as a proposed new Goal at Close. State which document governs each point, or what the visual spec's author (`art-director`) must reconcile. Do not rule on visual style.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Your rulings on criteria 13–16 and five spec defaults (handoff 14). Change them only if you say why.

## Constraints

- Stay within D-001, the vision pillars (one-button combat, short runs, readable threats) and the project constraints (30 and 60 FPS must both play correctly; small team, reuse existing systems).
- If a ruling would need a new enemy type, a healing system, a new input, or a scope change, hand back instead of ruling (it goes to `game-director`).
- Do not edit the game. A rule that you add must be checkable by QA at both frame rates, with player-observable acceptance criteria.
- If you accept the graze (question 1), record it as a known, accepted limitation of the text build and say what, if anything, must be re-checked in a graphical build.

## Open questions

1. Is the graze in Finding 1 acceptable? If yes, state it as accepted and name the sampling rule. If no, state the required behaviour (for example a swept contact test between frames, with the tolerance allowed between 30 and 60 FPS) and whether it also applies to grub lunges.
2. Is the cap a limit on cue starts (as built) or on shots in flight?
3. Keep or retune the walker margin at 60 FPS (criterion 13)?
4. Which document governs each contradiction in Finding 4?

## Expected output

A short ruling written into `design/combat.md` where it changes the spec, plus a handoff with `outcome: done`, addressed to `studio`. For each question give the ruling and, where the build must change, the acceptance criteria. Say clearly whether the build must change (Build for `gameplay-engineer`) or not (QA closes the open 30 FPS gaps and the verdict becomes pass).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, goals/G-001-combat-monotony/14-game-designer-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/20-qa-to-studio.md
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
# Combat design (build 0.5, specified in G-001 step 07, rulings in step 14)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). The player kit is unchanged from 0.4.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub flashes saturated orange-red and a thin orange-red line shows the lunge path (length equal to the lunge distance).
   - Text view: message "a grub rears back" when it starts.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge).
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
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + 0.8 s × k. After that each spitter fires every 2.4 s after its previous shot. With three spitters, shots are 0.8 s apart.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cap.** At most 3 shots in flight in the room. A spitter that would start a cue while 3 shots are in flight waits 0.2 s and checks again.
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
11. **Stagger.** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame. Never more than 3 shots in flight.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above.
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change is required.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
16. **Frame-rate independence (ruled in step 14).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference. The walker only has to satisfy 13 and 14 at each rate.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. The check: with `log on`, run walker room 3 at both rates and compare decision times and states. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11 fails at one rate. That must be fixed before 16 can pass.

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

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether the text view's `r` / `G` marks suit the graphical build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled.

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

<<<FILE goals/G-001-combat-monotony/14-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 14
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 14: game-designer → studio — Criteria 14 and 16 ruled, five spec gaps confirmed; no build or bot change needed

## Task

Route the updated `design/combat.md` to QA for final verification of criteria 1–16 against build 0.5. Add the checks below to QA's list, including the walker 30/60 comparison already in progress (handoff 13).

## Context

G-001 (combat monotony). Handoff 11 asked for rulings on criterion 14 (walker misses rooms 1–2), criterion 16 (walker differs between rates) and the five defaults the engineer used.

## Findings

### What changed in `design/combat.md`

- **Criterion 14 changed.** Old: the walker loses at least 1 heart in rooms 1–2 and clears both. New, at each rate: the walker loses at least 1 heart in rooms 1–2 summed (no clear required); the dodger loses at most 1 and clears both. Observed: walker 5 lost at 30 FPS and 5 at 60 FPS; dodger 0 lost, both cleared. Met.
  - The reason is structural. A wind-up always comes before contact, so a player who ignores the cue and stands still takes one lunge per grub. Room 1 has three grubs and 3 hearts, so a bot that never adapts cannot clear it. That is the cost "ignoring the cue costs hearts" asks for. Making the walker survive would need either a cue-reading walker (it would stop being the "ignores cues" proxy) or a gentler room 1 (a balance change, not needed to meet the intent).
  - Player-observable behavior protected: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. A human can learn the cue from the first hit; the bot cannot. I added this as an experience signal.
- **Criterion 16 changed.** It now has parts a–e:
  - 1–12 hold at both rates.
  - 13–15 are evaluated separately at each rate.
  - The dodger agrees across rates (same cleared set, hearts lost per room within 1).
  - The walker only has to meet 13 and 14 at each rate; its per-room numbers need not match. The reason is the 0.15 s decision grid (4.5 frames at 30 FPS, 9 at 60), which makes its sidestep timing sensitive to frame rounding.
  - A build defect is not excused: it is present if the same decision at the same game time (±1 frame) and the same state gives a different outcome, or if any of 1–11 fails at one rate.
- **Criterion 13** keeps its numbers but is stated to hold at each rate separately, with its protected behavior spelled out. Observed: walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (top of the range), dodger 0 lost and 3/3, camper 0/3.
- **Criterion 6** now also says a swipe that kills a grub in wind-up kills it with no stagger and no lunge.
- **The five defaults, all confirmed** (written into the spec):
  1. A grub exactly on the player: wind-up aims right. Confirmed and added to the Grub rules and edge cases.
  2. Spitter cap wait of 0.2 s from the moment the cue would start. Confirmed. I also wrote down what the code does: the delay carries forward, so the spitter's next shot is 2.4 s after its actual shot. The criterion 11 first-shot times are not affected.
  3. Spitter index counts only spitters, in spawn order, also in the practice room. Confirmed. A defeated spitter does not renumber the others.
  4. A grub hit but not killed during lunge or recovery continues its phase. Confirmed, extended to Approach and Stagger (a hit during stagger does not extend it). Only a hit during wind-up changes the phase.
  5. No stagger if the swipe kills the grub. Confirmed.

### Does anything need to change in the build or the bots?

No. All five defaults match the spec as now written. Bot thresholds (0.15 s grid, walker 2.5 and 1.1 tiles, dodger rules) stay as they are. The criteria were changed to fit the build and the bots, not the other way round.

### What QA's final verification should check

1. Criteria 1–12 at both 30 and 60 FPS with practice-room scripts, including the new part of 6 (swipe that kills a grub in wind-up: dies, no stagger, no lunge).
2. Criteria 13, 14 and 15 with `bots camper,walker,dodger` and `rooms 1-5` at `fps 30` and at `fps 60` separately. Expected from handoff 11: 13 met at both (walker total 4 and 6), 14 met at both (walker lost 5 in rooms 1–2), 15 met at both. If walker totals in rooms 3–5 fall outside 3–6 on QA's run, report it; that is a tuning question for the designer, not a build defect.
3. Criterion 16 c: dodger agreement between rates, per room (cleared set equal, hearts lost within 1).
4. Criterion 16 e: the walker comparison from handoff 13 (`log on`, `bots walker`, `rooms 3`, both rates). Decide whether the differences come from decision times landing on different frames, or from a build defect, using the rule in criterion 16 e. Only a defect is a failure.
5. Edge cases newly written: grub at distance 0 aims right (cue shown); a spitter delayed by the cap shifts its later shots by the same delay; a defeated spitter does not renumber the others.
6. Check that `repo/manual.md` still matches the spec: marks `r` and `G`, the `~` line, the messages, wind-up lengths 0.5 / 0.35 / 0.7 s and the 0.4 s stagger. No spec change affects the manual.

## Decisions already made

- D-001: one attack button plus dash; no new input. Unchanged.
- Studio: Decide and Plan skipped. I did not write a Decision (no direction, scope, input or enemy-type change).

## Constraints

- Everything in the spec stays within the vision pillars and D-001, reuses existing systems, and holds at 30 and 60 FPS.
- No scope change, new enemy type, healing system or input was needed, so no Decide step is required.

## Open questions

1. If a human playtest later finds room 1 too punishing for a first-time player, the fix is a room change (for example a lone first grub). It needs a new spec step and is not requested now.
2. Art cue review (flash, line, glow) is still with the art-director.

## Expected output

QA's verification report on criteria 1–16, including the walker 30/60 finding. If QA finds a build defect, route it to gameplay-engineer. If the walker's rooms 3–5 totals leave the 3–6 range, route it back to the game-designer.

## Sender assessment

- I did not run `play` or `bots`; the rulings use the observed numbers in handoffs 10 and 11 and the code in `game.py` and `bots.py`.
- Confidence: high that criterion 14 as ruled is met and that the five defaults match the code. Medium on criterion 16 e: the sensitivity explanation is consistent with the code, but QA's logged comparison must confirm it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/11-studio-to-game-designer.md
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

<<<FILE goals/G-001-combat-monotony/20-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 20
from: qa
to: studio
stage: Verify
outcome: question
---
# 20: qa → studio — Build 0.5 (sha 29993eac7bb0) verified against 1–16 and V12; one open item for the designer: a frame-rate-dependent graze at the contact edge

## Task

Report the independent verification of build 0.5 against combat criteria 1–16 and V12, and settle 16e from the new `log on` output.

## Context

All evidence is from runs made in this step (tests, bots with and without `log`, play/trace scripts). No run rounds are left. Anything not run is marked "not run". The verdict is not `pass` yet. Criteria 1–15 and 16a–d pass. For 16e, the walker's differences are explained by bot timing. But a frame-rate-dependent graze at the contact edge exists in the build, shown by a scripted reproduction. The spec does not say whether that is acceptable, so it goes to `game-designer` through the Studio. No criterion has failed for a second time.

## Findings

### A. Per-criterion result

| # | Result | Evidence |
|---|---|---|
| 1 Telegraph | pass, 30 and 60 | Trace `c1-stand`: windup at frame 1 (0.033 s at 30, 0.017 s at 60). The lunge starts exactly 0.5 s later (0.533 / 0.517). The first hit lands at 0.667 / 0.633, so cue to hit is 0.633 s / 0.617 s, which is ≥ 0.5 s. The test suite checks the gap at both rates. |
| 2 Sidestep | pass, 30 and 60 | Trace `c2-side`: the player moves up from 0.1 s to 0.35 s (1.07 tiles at 30, 1.0 at 60). Hearts stay 3 through the first lunge. Later damage in that trace comes from a second lunge the script does not dodge. |
| 3 Dash | pass, 30 and 60 | Trace `c3-dash-late` (dash at 0.65 s, inside the window): 3 hearts at both rates, `dash` and `dash_end` logged, no `ignored`. The tests dash at offsets 0, 0.25, 0.5 and 0.6 s after the cue at both rates. |
| 4 Standing still | pass, 30 and 60 | `c1-stand` loses 2 hearts in 3 s at both rates. The test suite checks it at both rates. |
| 5 Safe window | pass at 60 (test). 30 FPS not run. | `test_recovery_is_safe` and `test_grub_walking_alone_does_not_hurt` run at 60 only. In `game.py`, grub damage happens only in the lunge phase, so I expect the same result at 30, but I did not observe it. Hurt-invulnerability (0.8 s) equals recovery (0.8 s), so trace `c1-stand` cannot isolate it. |
| 6 Cancel | pass | Trace `c6-kill-windup` at 30 and 60: the runner is defeated in wind-up, the room clears, with no stagger event and no lunge. Swipe during wind-up gives stagger and no lunge (tests, both rates). The two-swipe kill is a 60 FPS test only. |
| 7 One at a time | pass, 30 and 60 | Test: the maximum number of grubs in wind-up or lunge is 1 at both rates. |
| 8 Variants | pass | Swipes to defeat 2 / 1 / 4 (60 FPS test; not run at 30). Marks `r` and `G` are drawn (test) and listed in `manual.md`. |
| 9 Aim cue | pass, 30 and 60 | Room 3 test: aim to spit is 0.6 s ±1 frame. The shot follows the locked line (y stays 4.0 in the spitter test). |
| 10 Dodge | pass, 30 and 60 | Spitter sidestep test. |
| 11 Stagger | pass, 30 and 60 | Room 3 test: first shots at 1.8 / 2.6 / 3.4 s ±1 frame, and at most 3 shots in flight over 12 s. See finding C for a 4-spitter observation. |
| 12 Rooms | pass | `ROOMS` in `game.py` matches the table for all 5 rooms (I read it). The test checks rooms 2, 4 and the brute in room 5. |
| 13 | pass at each rate | See table B. |
| 14 | pass at each rate | See table B. |
| 15 Dash used | pass at each rate | Dodger dashes in rooms 3/4/5: 8/7/11 at 30 FPS, 10/8/14 at 60 FPS. |
| 16a | pass, with the gaps listed for 5, 6 and 8 | |
| 16b | pass | See table B. |
| 16c | pass | The dodger is identical at both rates: 0 hearts lost in every room and 5/5 cleared. |
| 16d | acknowledged | The walker differs between rates (per room, 30 FPS: 3✗ 2✓ 0✓ 1✓ 3✗; 60 FPS: 3✗ 2✓ 2✓ 2✓ 2✓). |
| 16e | walker differences: bot timing. Graze: open (see D and E). | |
| V12 | not assessable | There is no graphical build. The text-view reference timings hold at both rates: wind-up to lunge is exactly 0.5 s, and aim to spit is 0.6 s ±1 frame. The cue appears on frame 1 at both rates. |

### B. Criteria 13/14/15 numbers

The bots ran with `log off`, from `bots.py`, at each rate separately.

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker lost, rooms 3–5 (need 3–6) | 0+1+3 = 4 | 2+2+2 = 6 (top of range) |
| Walker cleared, rooms 3–5 (need ≥ 2) | 2 | 3 |
| Dodger lost / cleared, rooms 3–5 (need ≤ half the walker's loss; 3/3) | 0 / 3 | 0 / 3 |
| Camper cleared, rooms 3–5 (must be < walker) | 0 | 0 |
| Walker lost, rooms 1–2 (need ≥ 1) | 3+2 = 5 | 3+2 = 5 |
| Dodger lost / cleared, rooms 1–2 (need ≤ 1; both cleared) | 0 / 2 | 0 / 2 |

The walker at 60 FPS sits at exactly 6, the limit of the range. A change of one heart would break 13. This is a tuning note for the designer, not a failure.

### C. Other observations

Neither of these fails a criterion as written.

1. **Shot cap exceeded with four spitters (practice room).** Trace `cap-four-spitters-60` has four spitters. Cues start for three spitters at 4.6 s, and each cap check sees only 2 shots in flight. At 5.2 s all three fire, while the shots from 2.6 s and 3.4 s are still in flight. By my count that is 5 shots in flight; the trace shows the hits at 5.3 s and 6.1 s. The spec text checks the cap only when a cue starts, so this may be intended. Criterion 11 says "never more than 3 in flight", and the 3-spitter room 3 stayed ≤ 3 in the test. No real room has 4 spitters. Question for the designer: is the cap a limit on cue starts or on shots in flight?
2. **Hit-stun can last one frame longer than 0.3 s.** Several `skipped decision` lines show "0.000 s of stun left" while the bot was still skipped. Examples: 60 FPS camper room 1 at frame 180; 30 FPS camper room 3 at frame 126. I infer that a tiny floating-point residue keeps `stun_left` above 0 for one extra frame. It is within ±1 frame. It shifts one bot decision, and it is a plain float effect, not tied to one frame rate.
3. **Criterion 6 and 8:** the two-swipe and variant-swipe tests run at 60 FPS only.
4. **Not run:** the "spitter index not renumbered after a defeat" edge case. No test or trace covers it.
5. **Edge cases that were run:** grub at distance 0 (trace `edge-dist0`) aims right (+1,0) and shows the cue and line. The cap delay carries forward (trace `cap-four-spitters-60`: shots at 5.2 s instead of 4.2 s, then +2.4 s).
6. **Manual check:** `manual.md` lists the marks `r` and `G`, the `~` line, both messages, warnings of 0.5 / 0.35 / 0.7 s and the 0.4 s stagger. It matches the spec.

### D. 16e — walker, room 3, 30 vs 60 FPS (`log on`)

**Room 1 at 0.30 s (the first walker difference): fully explained by the log.**
- The walker swings when `distance < 2.5`. At 0.30 s the player is at (8.0, 2.8) and the grub at (8.0, 0.3) at both rates, so the true distance is exactly 2.5.
- The logged exact values are 2.5000000000000004 at 30 FPS and 2.4999999999999964 at 60 FPS.
- So 30 FPS evaluates "not < 2.5" and walks (it swings first at 0.47 s). 60 FPS evaluates "< 2.5" and swings at 0.30 s.
- The cause is floating-point residue at an exact threshold tie in the bot. The game and the real geometry are the same. This confirms the hypothesis in handoff 16.

**Room 3: positions diverge long before any damage.**
- Decisions up to 1.05 s are the same action ("walk to spitter"). The decision grid is the same at both rates. The 30 FPS decisions land 0–1 frame later (for example 0.17 vs 0.15 s), so the player keeps its old heading up to 0.033 s longer.
- Already at 1.20 s the player is at (4.267, 2.933) at 30 FPS and (3.8, 3.4) at 60 FPS.
- The aim cue is locked on the player's position at its start, so the first shots differ in direction. From the logs: v = (2.28, 1.95) at 30 FPS and v = (1.8, 2.4) at 60 FPS. At 1.80 s the players are 0.47 tile apart.
- At 60 FPS the walker, at (3.8, 2.2) at 2.10 s, walks left into the shot. The hit at 2.25 s is at distance ≈ 0.37 (player (3.2, 2.2), shot (2.84, 2.12)), and ≈ 0.47 one frame earlier. That is a clear hit, not a graze.
- At 30 FPS the walker, at (2.933, 3.067) at 2.10 s, is somewhere else, so there is no contact.

**Conclusion:** I found no pair of decisions at the same game time (±1 frame) from the same positions that gave different outcomes. The walker difference comes from bot decision timing, plus the different positions that follow from it. The walker's room 3 difference is not a build defect. The logs are cut at 20000 characters (up to about 9.3 s at 30 FPS). They cover the first divergence and the whole of room 3 at 60 FPS, but not every later decision.

### E. Frame-rate-dependent graze at the contact edge (exists)

**Reproduction.** Shot reach is 0.4. Scripts, run at `fps 30` and `fps 60`, with `python3 play.py --view trace`:

```text
room empty
fps 30            # and 60
spawn spitter 1.04 3.70
1.3 move up
1.4 stop
end 5
```

| Spitter position | 30 FPS | 60 FPS |
|---|---|---|
| (1.04, 3.70) | **no hit**, 3 hearts at 5 s | **hit at 4.100 s**, 2 hearts |
| (1.00, 3.70) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.73) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.76) | hit at 4.100 s | hit at 4.117 s |

**What happens.** The first shot (spit at 1.8 s) is locked on the player at (8, 4.0), as of the cue start at 1.2 s. The player then stands at (8, 3.6). The shot line passes at a perpendicular distance of about 0.3996 from the player, which is 0.0004 inside the reach of 0.4. Contact is a distance check once per frame (a shot moves 0.1 tile per frame at 30 FPS and 0.05 at 60 FPS). The hit needs a sampled frame within about ±0.017 tile of the closest approach. That window is narrower than the frame step at both rates, so which rate catches it depends on the phase.

**Reading the 16e rule.** The scripted input, the player position and the shot line are identical at both rates, and the outcome differs. This is not a walker-timing effect. 16e defines a build defect as "same decision, same time, same positions, different outcome". Read literally, this matches. But the Timing rule in the spec only guarantees "no tunnelling", and the spec does not say what collision sampling is allowed to do at the reach edge. I do not decide whether it is acceptable.

**Size (derived by my arithmetic, not run).**
- The effect only exists when the lateral miss is within about 0.003 tile of the 0.4 reach. Misses of 0.4 or more never hit, and misses more than about 0.003 inside always hit at both rates.
- Grub lunges use reach 0.6 and a step up to 0.27 tile at 30 FPS. The same logic gives a wider band, about 0.015 tile at 30 FPS. I did not test grubs for this.
- Severity: low. Frequency: only when a player's lateral miss falls in that very narrow band. The effect is a hit or a miss and does not change timing.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Designer's rulings on 13–16 and the five spec defaults (handoff 14). They were applied as written.

## Constraints

- This verification used only the spec, the criteria and the build.
- The game was not edited.
- Supported frame rates are 30 and 60 FPS.

## Open questions

For `game-designer`, through the Studio:

1. Is the frame-rate-dependent graze (finding E) acceptable for the text build? If yes, 16e passes as ruled and the verdict becomes `pass`. If not, `gameplay-engineer` must change the contact test (for example a swept test between frames) and QA re-verifies. This would be the first failure of 16, so no `technical-director` re-plan is triggered.
2. Is the shot cap a limit on starting cues (as built) or a hard limit on shots in flight (finding C1)?
3. The walker at 60 FPS in rooms 3–5 totals exactly 6 hearts, the upper limit of criterion 13. Does the designer want to keep that margin?
4. Contradictions between `design/combat.md` and `design/combat-cues-visual-spec.md` (reported only, no ruling):
   - **Lunge line.** `combat.md` says a "thin" orange-red line for the lunge path. The visual spec draws a lane 1.2 tiles wide.
   - **Spitter glow.** `combat.md` and the text view show the glow starting at 0%. The visual spec requires a floor of at least 30%.
   - **Grub cue behaviour.** `combat.md` says the grub "flashes" for the whole wind-up. The visual spec says a steady tint with a slight pulse, no strobe, at 3 Hz or less. The lane in the visual spec stays at full strength until the lunge starts and fades during it. The text view removes the line when the lunge starts.
   - **Text marks.** `combat.md` leaves the `r` / `G` marks open for the graphical build. The visual spec uses silhouette and size instead, which answers the open question.

## Expected output

The Studio routes finding E and open questions 1–3 to `game-designer`. After the ruling:
- If E is accepted, QA's verdict is `pass`, and the gaps on criteria 5, 6, 8 at 30 FPS can be closed with one more test run.
- If E is not accepted, the Studio routes to `gameplay-engineer` with the reproduction above.

V12 stays open until a graphical build exists.

## Regression check

- **Existing tests:** `python3 -m unittest discover -s tests` ran 34 tests, all OK. This includes the replaced walker test (13 and 14 at each rate), the dodger agreement test and the two new log tests.
- **Log on vs off:** the visible results are identical for the camper in all rooms at both rates, and for the walker in rooms 1, 2 and 3 (room 3 from the separate runs) at both rates. The `all30-log` and `all60-log` outputs were cut at 20000 characters (walker rooms 3–5 and the dodger are not in the visible part). The unit test `test_bot_log_adds_state_and_changes_no_result` covers every bot, rooms 1 and 3 and both rates, and passes.
- **Bots unchanged:** the `log off` numbers equal the table in handoff 16 and the walker/dodger figures in handoff 14 (walker 4 lost / 2 cleared at 30 FPS and 6 lost / 3 cleared at 60 FPS in rooms 3–5, dodger 0 lost).
- **Log format:** every decision line has frame, grid time, frame time, player position, hearts, stun, nearest enemy with the exact distance, and shots in flight. Heart-loss lines and skipped-decision lines appear as described in `README.md`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, repo/README.md, repo/bots.py, repo/tests/test_game.py, repo/game.py, repo/play.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/19-studio-to-qa.md
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
