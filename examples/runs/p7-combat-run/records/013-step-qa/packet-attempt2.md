# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/13-studio-to-qa.md
next_seq: 16
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/16-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/13-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 13
from: studio
to: qa
stage: Observe
outcome: routed
---
# 13: studio → qa — Reproduce the walker bot's different results at 30 and 60 FPS in rooms 3–5

## Task

Determine whether the walker bot's differing results at 30 and 60 FPS in rooms 3–5 come from the build (the simulation behaves differently at the two rates) or from the bot's own behavior. Write a defect report with reproduction steps if it is a build defect.

## Context

G-001 (combat monotony). The project must play correctly at 30 and 60 FPS. A previous QA pass (`goals/G-001-combat-monotony/08-qa-to-studio.md`) found the simulation matching within one frame in traced cases. Since then the build was updated (0.5: new enemy behavior, bots decide on a 0.15 s accumulated-time grid).

## Findings

Reported observation (`python3 bots.py {script}`, bots `camper,walker,dodger`, `rooms 1-5`, `fps 30` and `fps 60`), walker hearts lost per room 1/2/3/4/5:

- 30 FPS: 3✗ 2✓ 0✓ 1✓ 3✗ (✓ cleared, ✗ not cleared)
- 60 FPS: 3✗ 2✓ 2✓ 2✓ 2✓

The dodger bot agrees at both rates (0 hearts lost, all cleared). The `bots` option `log on` in a script prints each bot decision under the room line (see `repo/README.md`).

## Decisions already made

- D-001: one attack button plus dash; no new input.

## Constraints

- Intended behavior is defined by `design/combat.md` and `repo/manual.md`. A difference caused only by a bot's decision timing is not a build defect, but say so with evidence.
- Do not fix code. Report only.

## Open questions

1. Is the divergence reproducible and deterministic?
2. Is it caused by the build simulation (enemy timers, movement, collision, damage at different frame rates) or by the walker's decisions? Identify the first point where the two runs differ, using `log on` and `run_trace`.

## Expected output

A report: reproduction commands, the first divergence point and its cause, severity, and, if it is a build defect, acceptance criteria for a fix. Address the result to `studio`. Full verification of criteria 1–16 follows in a later step.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, repo/README.md, repo/bots.py, repo/game.py, repo/play.py, repo/tests/test_game.py, project.md#constraints, the build (repo/; run_bots, run_trace and run_play in project.md)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/08-qa-to-studio.md
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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.5.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual; it changes with the build.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  behave the same at 30 and 60 FPS up to frame rounding. Only the dodger reads the new cues.
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  log on                      print each bot's decisions (time, what it did) under its room line

Each bot starts every room with full hearts. Bots decide at most once every 0.15 s of game time
(accumulated seconds, on a fixed time grid), so a bot behaves the same at 30 and 60 FPS apart from
frame rounding. The walker and camper do not read the new cues; the dodger does.
"""

import math
import sys

from game import (
    ATTACK_REACH,
    DIRECTIONS,
    GRUB_REACH,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    ROOMS,
    SHOT_SPEED,
    Game,
)

REACTION = 0.15  # seconds between a bot's decisions, like play.py's rule reaction time
LUNGE_LEN = LUNGE_SPEED * LUNGE_TIME


class Brain:
    """The bot's reaction clock (accumulated seconds) and decision log."""

    def __init__(self, log=None):
        self.next, self.log = 0.0, log

    def due(self, t):
        if t < self.next - 1e-9:
            return False
        while self.next <= t + 1e-9:
            self.next += REACTION
        return True

    def note(self, t, text):
        if self.log is not None:
            self.log.append(f"{t:6.2f} s  {text}")


def _toward(dx, dy):
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def _nearest(game):
    live = [e for e in game.enemies if e.hp > 0]
    return min(live, key=lambda e: math.hypot(e.x - game.x, e.y - game.y), default=None)


def _face_and_swing(game, enemy):
    game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    game.press("stop")
    if math.hypot(enemy.x - game.x, enemy.y - game.y) <= ATTACK_REACH and game.recovery <= 0:
        game.press("attack")


def _incoming(game):
    """A shot in flight that will reach the player within 0.7 s, if any (ignores cues)."""
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        ahead = ((game.x - x) * vx + (game.y - y) * vy) / speed
        beside = abs((game.x - x) * vy - (game.y - y) * vx) / speed
        if 0 < ahead < 0.7 * speed and beside < 0.7:
            return vx, vy
    return None


def _sidestep(game, shot):
    vx, vy = shot
    if abs(vx) >= abs(vy):
        return "down" if game.y < 4 else "up"
    return "right" if game.x < 8 else "left"


def _dangers(game):
    """Lines the player can see: wind-up paths, lunges, spitter aim lines, shots in flight.

    Each is (x, y, ux, uy, length, wait, speed, kind): origin, unit direction, length of the
    dangerous stretch, seconds until it starts moving, and how fast it moves along the line.
    """
    out = []
    for e in game.enemies:
        if e.hp <= 0:
            continue
        if e.is_grub and e.phase == "windup":
            out.append((e.x, e.y, e.aim[0], e.aim[1], LUNGE_LEN + GRUB_REACH, e.phase_left, LUNGE_SPEED, "lunge"))
        elif e.is_grub and e.phase == "lunge":
            out.append((e.x, e.y, e.aim[0], e.aim[1], e.lunge_left * LUNGE_SPEED + GRUB_REACH, 0.0, LUNGE_SPEED, "lunge"))
        elif not e.is_grub and e.cueing and e.aim:
            out.append((e.x, e.y, e.aim[0], e.aim[1], 40.0, e.fire_in, SHOT_SPEED, "aim"))
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        out.append((x, y, vx / speed, vy / speed, 40.0, 0.0, speed, "shot"))
    return out


def _threat(game):
    """The most urgent line the player stands in: (eta, ox, oy, ux, uy, beside, kind)."""
    best = None
    for ox, oy, ux, uy, length, wait, speed, kind in _dangers(game):
        rx, ry = game.x - ox, game.y - oy
        ahead = rx * ux + ry * uy
        beside = rx * -uy + ry * ux
        if ahead < -0.3 or ahead > length or abs(beside) > 0.9:
            continue
        eta = wait + max(0.0, ahead - 0.5) / speed
        if best is None or eta < best[0]:
            best = (eta, ox, oy, ux, uy, beside, kind)
    return best


def _axis(vx, vy):
    if abs(vx) >= abs(vy):
        return "right" if vx > 0 else "left"
    return "down" if vy > 0 else "up"


def _escape(game, threat):
    """The direction across the line, away from the side the player is on, with room to go."""
    _, _, _, ux, uy, beside, _ = threat
    px, py = -uy, ux
    sign = 1 if beside >= 0 else -1
    direction = None
    for _ in range(2):
        direction = _axis(sign * px, sign * py)
        dx, dy = DIRECTIONS[direction]
        x, y = game.x + dx * 1.5, game.y + dy * 1.5
        if 0 <= x <= ROOM_W - 1 and 0 <= y <= ROOM_H - 1:
            return direction
        sign = -sign
    return direction


def camper(game, note):
    """Holds the starting spot: turns to the nearest enemy and swings when it is in reach."""
    enemy = _nearest(game)
    if enemy:
        _face_and_swing(game, enemy)


def walker(game, note):
    """Lets a nearby grub come and swings, walks up to anything further away, steps aside from
    shots already in flight. Never dashes and does not read the wind-up or aim cues."""
    enemy = _nearest(game)
    if not enemy:
        return
    shot = _incoming(game)
    distance = math.hypot(enemy.x - game.x, enemy.y - game.y)
    coming = enemy.is_grub and distance < 2.5
    if shot:
        note("sidestep shot in flight")
        game.press("move", _sidestep(game, shot))
    elif distance > 1.1 and not coming:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


def dodger(game, note):
    """Reads the cues: swipes a wind-up that is in reach (it cancels), otherwise dashes across a
    line when the hit is under 0.4 s away, steps across it earlier if the dash is not ready,
    holds still while a lunge plays out, and walks in to swipe the rest."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    for e in game.enemies:
        if (
            e.hp > 0
            and e.is_grub
            and e.phase == "windup"
            and math.hypot(e.x - game.x, e.y - game.y) <= 1.4
            and game.recovery <= 0
        ):
            note(f"swipe {e.kind} wind-up")
            _face_and_swing(game, e)
            return
    threat = _threat(game)
    if threat and threat[0] <= 1.0:
        eta, kind = threat[0], threat[6]
        direction = _escape(game, threat)
        if ready and eta <= 0.4:
            note(f"dash {direction} from {kind} (hit in {eta:.2f} s)")
            game.press("dash", direction)
            return
        if not ready:
            note(f"step {direction} from {kind} (hit in {eta:.2f} s, dash not ready)")
            game.press("move", direction)
            return
        note(f"hold, dash ready, {kind} in {eta:.2f} s")
        game.press("stop")
        return
    if any(e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in game.enemies):
        note("hold while a grub lunges")
        game.press("stop")
        return
    enemy = _nearest(game)
    if not enemy:
        return
    if math.hypot(enemy.x - game.x, enemy.y - game.y) > 1.1:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


BOTS = {"camper": camper, "walker": walker, "dodger": dodger}


def play_room(bot, room, fps, limit, log=None):
    game = Game(fps=fps, room=room)
    brain = Brain([] if log else None)
    while game.t < limit - 1e-9 and not game.cleared and game.hearts > 0:
        if game.stun_left <= 0 and brain.due(game.t):
            bot(game, lambda text: brain.note(game.t, text))
        game.step()
    counts = {}
    sources = {}
    for _, kind, details in game.events:
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "hurt":
            sources[details["source"]] = sources.get(details["source"], 0) + 1
    return {
        "cleared": game.cleared,
        "seconds": round(game.t, 2),
        "hearts_lost": HEARTS - game.hearts,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "log": False,
    }
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, value = line.partition(" ")
        value = value.replace(" ", "")
        try:
            if key == "bots":
                setup["bots"] = value.split(",")
                assert all(b in BOTS for b in setup["bots"])
            elif key == "rooms":
                if "-" in value:
                    first, last = value.split("-")
                    value = ",".join(str(n) for n in range(int(first), int(last) + 1))
                setup["rooms"] = value.split(",")
                assert all(r in ROOMS for r in setup["rooms"])
            elif key == "fps":
                setup["fps"] = int(value)
            elif key == "limit":
                setup["limit"] = float(value)
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | log on"
            )
    return setup


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {HEARTS} hearts each")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"])
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}"
            )
            for entry in r["log"]:
                print("          " + entry)
            total["cleared"] += r["cleared"]
            total["hearts_lost"] += r["hearts_lost"]
            total["dashes"] += r["dashes"]
        print(
            f"{name:7} total: cleared {total['cleared']}/{len(setup['rooms'])}, hearts lost "
            f"{total['hearts_lost']}, dashes {total['dashes']}"
        )


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.5: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. All durations are in seconds and run
on accumulated time, never on frame counts.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

# Grubs: one type, parameter sets only (design/combat.md).
GRUB_REACH = 0.6
WINDUP_RANGE = 2.0  # a grub starts its wind-up when the player is this close
LUNGE_SPEED, LUNGE_TIME = 8.0, 0.3  # 2.4 tiles
STAGGER = 0.4  # after a swipe cancels a wind-up
GRUBS = {
    "grub": {"mark": "g", "hp": 2, "speed": 1.0, "windup": 0.5, "recovery": 0.8},
    "runner": {"mark": "r", "hp": 1, "speed": 1.6, "windup": 0.35, "recovery": 0.6},
    "brute": {"mark": "G", "hp": 4, "speed": 0.7, "windup": 0.7, "recovery": 1.2},
}

SPITTER_HP = 2
SPIT_INTERVAL = 2.4
SPIT_FIRST, SPIT_STAGGER = 1.8, 0.8  # first shot of the k-th spitter: 1.8 s + 0.8 s * k
AIM_CUE = 0.6
SHOT_SPEED, SHOT_REACH, SHOT_LIFE = 3.0, 0.4, 5.0
SHOT_CAP, CAP_WAIT = 3, 0.2

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)],
    "3": [("spitter", 2, 1), ("spitter", 14, 7), ("spitter", 2, 7)],
    "4": [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [
        ("grub", 1, 1),
        ("grub", 0, 6),
        ("brute", 4, 8),
        ("spitter", 15, 0),
        ("spitter", 15, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}


class Enemy:
    def __init__(self, kind, x, y, index=0):
        if kind not in GRUBS and kind != "spitter":
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "spitter":
            self.hp = SPITTER_HP
            self.fire_in = SPIT_FIRST + SPIT_STAGGER * index  # seconds to the next shot
            self.cueing = False
        else:
            spec = GRUBS[kind]
            self.hp = spec["hp"]
            self.phase = "approach"  # approach | windup | lunge | recovery | stagger
            self.phase_left = 0.0
            self.lunge_left = 0.0
            self.struck = False

    @property
    def is_grub(self):
        return self.kind in GRUBS

    @property
    def mark(self):
        return GRUBS[self.kind]["mark"] if self.is_grub else "s"


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.queued_attack = False
        self.enemies = []
        self.shots = []  # [x, y, vx, vy, age]
        self.events = []  # (time, kind, details)
        self.cleared = False
        for spec in ROOMS[room]:
            self.spawn(*spec)

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        index = sum(1 for e in self.enemies if e.kind == "spitter")
        self.enemies.append(Enemy(kind, x, y, index))

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    # --- Input -------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.hearts <= 0:
            return
        if self.stun_left > 0:
            self.log("ignored", action=action, reason="stunned")
            return
        if action == "move":
            self.heading = self.facing = DIRECTIONS[direction]
        elif action == "stop":
            self.heading = (0, 0)
        elif action == "attack":
            if self.dash_left > 0:
                self.queued_attack = True
            elif self.recovery > 0:
                self.log("ignored", action=action, reason="recovering")
            else:
                self._attack()
        elif self.dash_left > 0 or self.dash_cooldown > 0:
            self.log("ignored", action=action, reason="dash not ready")
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation --------------------------------------------------------------------------

    def step(self):
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= 1e-9:
                self.hurt_left = 0.0
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= 1e-9:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        self._update_enemies(dt)
        self._update_shots(dt)
        if not self.cleared and self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.cleared = True
            self.log("cleared")

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        fx, fy = self.facing
        hit = []
        for enemy in self.enemies:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if (
                enemy.hp > 0
                and math.hypot(dx, dy) <= ATTACK_REACH
                and dx * fx + dy * fy > 0
            ):
                enemy.hp -= 1
                hit.append(enemy)
        for enemy in hit:
            if enemy.hp > 0 and enemy.is_grub and enemy.phase == "windup":
                enemy.phase, enemy.phase_left, enemy.aim = "stagger", STAGGER, None
                self.log("stagger", enemy=enemy.kind)
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        if self.hearts <= 0:  # the player is down: everything stops
            return
        busy = any(
            e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in self.enemies
        )
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            if enemy.is_grub:
                busy = self._update_grub(enemy, dt, busy)
            else:
                self._update_spitter(enemy, dt)

    def _update_grub(self, e, dt, busy):
        """One grub for one frame; returns whether some grub is now in wind-up or lunge."""
        spec = GRUBS[e.kind]
        dx, dy = self.x - e.x, self.y - e.y
        dist = math.hypot(dx, dy)
        if e.phase == "approach":
            if dist <= WINDUP_RANGE + EPS and not busy:
                e.phase, e.phase_left = "windup", spec["windup"]
                # Aim locked now. Grub exactly on the player: the spec is silent; face right.
                e.aim = (dx / dist, dy / dist) if dist > 0 else (1.0, 0.0)
                self.log("windup", enemy=e.kind)
                return True
            stop = GRUB_REACH * 0.9
            if dist > stop:
                step = min(spec["speed"] * dt, dist - stop)
                e.x += dx / dist * step
                e.y += dy / dist * step
        elif e.phase == "windup":
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase, e.lunge_left, e.struck = "lunge", LUNGE_TIME, False
                self.log("lunge", enemy=e.kind)
            return True
        elif e.phase == "lunge":
            span = min(dt, e.lunge_left)
            e.x, e.y = self._clamp(
                e.x + e.aim[0] * LUNGE_SPEED * span, e.y + e.aim[1] * LUNGE_SPEED * span
            )
            e.lunge_left -= span
            close = math.hypot(self.x - e.x, self.y - e.y) <= GRUB_REACH
            if close and not e.struck and not self.invulnerable:
                e.struck = True
                self._hurt("grub")
                e.lunge_left = 0.0  # contact ends the lunge
            if e.lunge_left <= EPS:
                e.phase, e.phase_left, e.aim = "recovery", spec["recovery"], None
                return False
            return True
        else:  # recovery or stagger
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase = "approach"
        return busy

    def _update_spitter(self, e, dt):
        e.fire_in -= dt
        if not e.cueing:
            if e.fire_in <= AIM_CUE + EPS:
                if len(self.shots) >= SHOT_CAP:
                    e.fire_in += CAP_WAIT  # wait and check again
                    return
                e.cueing = True
                dx, dy = self.x - e.x, self.y - e.y
                dist = math.hypot(dx, dy)
                e.aim = (dx / dist, dy / dist) if dist > 0 else None
                if e.aim:
                    self.log("aim")
        elif e.fire_in <= EPS:
            e.cueing = False
            e.fire_in += SPIT_INTERVAL
            if e.aim:
                self.shots.append(
                    [e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED, 0.0]
                )
                self.log("spit")
            e.aim = None

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            if shot[4] >= SHOT_LIFE - EPS:
                continue
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and not self.invulnerable and self.hearts > 0:
                self._hurt("shot")
                continue
            kept.append(shot)
        self.shots = kept

    def _hurt(self, source):
        if self.invulnerable or self.hearts <= 0:
            return
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self.log("down")

    def _set_invulnerable(self, value, why):
        if self.invulnerable != value:
            self.invulnerable = value
            self.log("invulnerable", value=value, why=why)

    def _move(self, direction, distance):
        self.x, self.y = self._clamp(
            self.x + direction[0] * distance, self.y + direction[1] * distance
        )

    @staticmethod
    def _clamp(x, y):
        return min(max(x, 0.0), ROOM_W - 1.0), min(max(y, 0.0), ROOM_H - 1.0)


def _name(direction):
    return next(k for k, v in DIRECTIONS.items() if v == direction)
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format, including reaction rules, is described in manual.md.
"""

import argparse
import math
import re
import sys

from game import (
    AIM_CUE,
    DIRECTIONS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    Game,
)

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots
REACTION = 0.15  # a rule acts at most this often, like a player's reaction time
AFTER_END = 1.0  # seconds shown after the room is cleared or the player goes down


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs, rules = [], []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "when":
                rules.append(Rule(line))
            elif words[0] == "room":
                setup["room"] = words[1]
            elif words[0] == "fps":
                setup["fps"] = int(words[1])
            elif words[0] == "end":
                setup["end"] = float(words[1])
            elif words[0] == "spawn":
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
            elif words[0] == "player":
                setup["player"] = (float(words[1]), float(words[2]))
            else:
                inputs.append(
                    (float(words[0]), words[1], words[2] if len(words) > 2 else None)
                )
        except (IndexError, ValueError) as error:
            hint = f" ({error})" if str(error) else ""
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}{hint}")
    return setup, sorted(inputs, key=lambda i: i[0]), rules


class Rule:
    """`when <condition> then <action>`, judged only from the frame as drawn and the messages shown."""

    def __init__(self, line):
        match = re.fullmatch(r"when (.+?) then (.+)", line)
        if not match:
            raise ValueError("a rule reads: when <condition> then <action>")
        self.condition, self.action = match.group(1).split(), match.group(2).split()
        c, a = self.condition, self.action
        quoted = re.fullmatch(r'text "(.+)"', match.group(1))
        if quoted:
            self.condition = ["text", quoted.group(1).lower()]
        elif not (
            (c[0] == "see" and len(c) == 4 and len(c[1]) == 1 and c[2] == "within")
            or (c[0] == "see" and len(c) == 5 and len(c[1]) == 1 and c[2:4] == ["coming", "within"])
            or (c[0] == "nothing" and len(c) == 3 and c[1] == "within")
            or (c[0] == "hearts" and len(c) == 3 and c[1] == "<=")
        ):
            raise ValueError(
                "conditions: see <mark> [coming] within <n>, nothing within <n>, text \"<words>\", hearts <= <n>"
            )
        if c[0] in ("see", "nothing", "hearts"):
            float(c[-1])
        targets = list(DIRECTIONS) + ["away", "toward", "aside"]
        if not (
            a in (["attack"], ["stop"], ["face"], ["dash"])
            or (len(a) == 2 and a[0] in ("move", "dash") and a[1] in targets)
        ):
            raise ValueError(
                "actions: attack, stop, face, move <dir|away|toward|aside>, dash [<dir|away|toward|aside>]"
            )
        self.last = -math.inf

    def matches(self, view):
        """The cell the rule reacts to (or True), if the condition holds in this view."""
        c = self.condition
        if c[0] == "text":
            return any(c[1] in m.lower() for m in view.messages) and (view.nearest() or True)
        if c[0] == "hearts":
            return view.hearts <= float(c[2]) and (view.nearest() or True)
        if c[0] == "nothing":
            return view.nearest(within=float(c[2])) is None
        return view.nearest(mark=c[1], within=float(c[-1]), coming=c[2] == "coming")

    def act(self, game, target):
        a = self.action
        toward = _toward(target, (game.x, game.y)) if isinstance(target, tuple) else None
        away = {"left": "right", "right": "left", "up": "down", "down": "up"}.get(toward)
        # Aside: across the line to the target, toward the roomier half of the room.
        if toward in ("left", "right"):
            aside = "down" if game.y < (ROOM_H - 1) / 2 else "up"
        else:
            aside = "right" if game.x < (ROOM_W - 1) / 2 else "left"
        if a == ["attack"]:
            if toward:  # turn to it and swing, as one input
                game.press("move", toward)
                game.press("stop")
            game.press("attack")
        elif a == ["stop"]:
            game.press("stop")
        elif a == ["face"]:
            if toward:
                game.press("move", toward)
                game.press("stop")
        elif a == ["dash"]:
            game.press("dash")
        else:
            direction = {"toward": toward, "away": away, "aside": aside if toward else None}.get(a[1], a[1])
            if direction:
                game.press(a[0], direction)


def _toward(cell, position):
    dx, dy = cell[0] - position[0], cell[1] - position[1]
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


class View:
    """What the player can see right now: what is on screen and where, the hearts, the messages."""

    def __init__(self, game, messages, before=()):
        self.sprites, self.hearts, self.messages = sprites(game), game.hearts, messages
        self.before = before  # the previous frame's sprites, to see what is moving
        self.me = next(((x, y) for mark, x, y in self.sprites if mark == "P"), None)

    def closing(self, mark, x, y):
        """Whether this sprite came closer since the last frame (the eye follows the nearest match)."""
        earlier = [(math.dist((x, y), (bx, by)), (bx, by)) for m, bx, by in self.before if m == mark]
        if not earlier:
            return False
        jump, (bx, by) = min(earlier)
        return jump < 0.5 and math.dist((x, y), self.me) < math.dist((bx, by), self.me) - 1e-9

    def nearest(self, mark=None, within=math.inf, coming=False):
        if self.me is None:
            return None
        seen = [
            (math.dist((x, y), self.me), (x, y))
            for m, x, y in self.sprites
            if m not in "Px"
            and (mark is None or m == mark)
            and (not coming or self.closing(m, x, y))
        ]
        seen = [place for d, place in sorted(seen) if d <= within + 1e-9]
        return seen[0] if seen else None


def react(game, rules, messages, before):
    view = View(game, messages, before)
    if view.me is None:
        return
    for rule in rules:  # the first rule that holds and is not still waiting acts
        target = rule.matches(view)
        if not target or game.t - rule.last < REACTION - 1e-9:
            continue
        rule.last = game.t
        before = len(game.events)
        rule.act(game, target)
        for _, kind, details in game.events[before:]:
            if kind == "ignored":
                details["quiet"] = True  # a held button, not news
        return


def play(setup, inputs, view, rules=()):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    default = (inputs[-1][0] + 3 if inputs else 5) if not rules else MAX_SECONDS
    end = min(setup["end"] if setup["end"] is not None else default, MAX_SECONDS)
    out = Player(game) if view == "player" else Trace(game)
    out.start()
    pending, seen, messages, over, before = list(inputs), 0, [], None, []
    while game.t < end - 1e-9 and (over is None or game.t < over - 1e-9):
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        if rules:
            react(game, rules, messages, before)
            before = sprites(game)
        game.step()
        out.frame()
        new = game.events[seen:]
        seen = len(game.events)
        messages = [m for m in (Player.describe(k, d) for _, k, d in new) if m]
        if over is None and (game.cleared or game.hearts <= 0):
            over = game.t + AFTER_END
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.5 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, show = self.game, False
        for when, kind, details in g.events[self.seen :]:
            text = self.describe(kind, details)
            if text:
                print(f"{when:7.3f}  {text}")
            show = show or kind in ("hurt", "windup", "aim")
        self.seen = len(g.events)
        if show or g.t >= self.next_snapshot - 1e-9:
            self.snapshot()
            if g.t >= self.next_snapshot - 1e-9:
                self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    @staticmethod
    def describe(kind, details):
        if kind == "attack":
            hits = details["hits"]
            return "you swipe: " + (
                ", ".join(f"{enemy} {result}" for enemy, result in hits)
                if hits
                else "miss"
            )
        if kind == "dash":
            return f"you dash {details['direction']}"
        if kind == "hurt":
            return f"YOU ARE HIT by a {details['source']} — hearts {details['hearts']}/{HEARTS}"
        if kind == "down":
            return "you went down"
        if kind == "windup":
            return "a grub rears back"
        if kind == "aim":
            return "a spitter takes aim"
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored" and not details.get("quiet"):
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in draw(g):
            print("   |" + row + "|")
        print("   +" + "-" * ROOM_W + "+")
        for text in cue_lines(g):
            print("   " + text)


def sprites(g):
    """Everything on screen as (mark, x, y), drawn in this order (later ones on top)."""
    shown = [("*", s[0], s[1]) for s in g.shots]
    shown += [(e.mark, e.x, e.y) for e in g.enemies if e.hp > 0]
    return shown + [("P" if g.hearts > 0 else "x", g.x, g.y)]


def _line_cells(g):
    """Points of the thin orange-red lines: lunge paths during a wind-up, aim lines during a cue."""
    cells = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        if e.is_grub and e.phase == "windup":
            length = LUNGE_SPEED * LUNGE_TIME
        elif not e.is_grub and e.cueing:
            length = ROOM_W + ROOM_H
        else:
            continue
        for i in range(1, int(length / 0.25) + 1):
            cells.append((e.x + e.aim[0] * 0.25 * i, e.y + e.aim[1] * 0.25 * i))
    return cells


def cue_lines(g):
    """Text description of the flash, glow and lines (orange-red) shown under the room."""
    out = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        where = f"at ({e.x:.1f},{e.y:.1f})"
        line = f"line toward ({e.aim[0]:+.2f},{e.aim[1]:+.2f})"
        if e.is_grub and e.phase == "windup":
            out.append(
                f"cue: {e.mark} {where} flashes orange-red, lunge {line}, "
                f"{LUNGE_SPEED * LUNGE_TIME:.1f} tiles ({e.phase_left:.2f} s to the lunge)"
            )
        elif not e.is_grub and e.cueing:
            bright = min(1.0, max(0.0, (AIM_CUE - e.fire_in) / AIM_CUE))
            out.append(
                f"cue: s {where} glows orange-red, brightness {bright:.0%}, aim {line} "
                f"({e.fire_in:.2f} s to the shot)"
            )
    return out


def draw(g):
    """The room as the player sees it, one string per row ('~' is an orange-red line)."""
    grid = [[" "] * ROOM_W for _ in range(ROOM_H)]
    for x, y in _line_cells(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = "~"
    for mark, x, y in sprites(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = mark
    return ["".join(row) for row in grid]


class Trace:
    """Simulation state for developers: one line per frame in which anything happened."""

    def __init__(self, game):
        self.game, self.seen = game, 0

    def start(self):
        g = self.game
        print(f"trace: fps={g.fps} room={g.room} dt={g.dt:.5f}")
        self.line([("setup", {})])

    def frame(self):
        g = self.game
        new = [(kind, details) for _, kind, details in g.events[self.seen :]]
        self.seen = len(g.events)
        if new:
            self.line(new)

    def finish(self):
        self.line([("end", {})])

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp},"
            + (f"{e.phase}:{e.phase_left:.3f}" if e.is_grub else f"fire_in={e.fire_in:.3f},cue={e.cueing}")
            + ")"
            for e in g.enemies
            if e.hp > 0
        )
        happened = "; ".join(
            kind + (f" {details}" if details else "") for kind, details in events
        )
        print(f"{state} | {enemies} | {happened}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["player", "trace"], default="player")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs, rules = read_script(f.read())
    play(setup, inputs, args.view, rules)


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/tests/test_game.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, ROOMS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


def has_event(kind):
    return lambda g: any(k == kind for _, k, _ in g.events)


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def busy_grubs(game):
    return sum(1 for e in game.enemies if e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge"))


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 0.4)  # the swipe cancels the grub's start; recovery passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_lunge_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_grub_walking_alone_does_not_hurt(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_spitter_fires_every_2_4_seconds_from_1_8(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.25)
        spits = times(game, "spit")
        self.assertEqual(len(spits), 2)
        self.assertAlmostEqual(spits[0], 1.8, places=6)
        self.assertAlmostEqual(spits[1], 4.2, places=6)


class GrubTest(unittest.TestCase):
    def cue(self, fps, x=10.0, kind="grub"):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, x, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_telegraph_comes_at_least_half_a_second_before_the_hit(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.5, 4)
            run(game, 2.0)
            gap = times(game, "hurt")[0] - times(game, "windup")[0]
            self.assertGreaterEqual(gap, 0.5 - 1.0 / fps - 1e-9, fps)

    def test_a_sidestep_avoids_the_lunge(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            run(game, 1.1)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_dash_from_cue_into_the_lunge_takes_no_damage(self):
        for fps in (30, 60):
            for offset in (0.0, 0.25, 0.5, 0.6):
                game = self.cue(fps)
                run(game, offset)
                game.press("dash", "up")
                run(game, 1.0)
                self.assertEqual(game.hearts, HEARTS, (fps, offset))
                self.assertFalse(any(k == "ignored" for _, k, _ in game.events), (fps, offset))

    def test_standing_still_is_punished(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 10, 4)
            run(game, 3.0)
            self.assertLessEqual(game.hearts, HEARTS - 1, fps)

    def test_recovery_is_safe(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_a_swipe_during_windup_stops_the_lunge(self):
        for fps in (30, 60):
            game = self.cue(fps, x=9.2)
            game.press("attack")
            self.assertEqual(game.enemies[0].phase, "stagger")
            run(game, 0.8)
            self.assertFalse(any(k == "lunge" for _, k, _ in game.events), fps)
            self.assertEqual(game.hearts, HEARTS)

    def test_only_one_grub_winds_up_or_lunges(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for x, y in ((9.5, 4), (8, 5.5), (6.5, 4)):
                game.spawn("grub", x, y)
            most = 0
            for _ in range(3 * fps):
                game.step()
                most = max(most, busy_grubs(game))
            self.assertEqual(most, 1, fps)

    def test_variants_swipes_to_defeat(self):
        for kind, swipes in (("grub", 2), ("runner", 1), ("brute", 4)):
            game = Game(room="empty")
            game.spawn(kind, 9.2, 4)
            for done in range(swipes):
                self.assertGreater(game.enemies[0].hp, 0, (kind, done))
                game.press("attack")
                run(game, 0.4)
            self.assertEqual(game.enemies[0].hp, 0, kind)

    def test_wind_up_lengths_differ_by_variant(self):
        windups = {}
        for kind in ("grub", "runner", "brute"):
            game = Game(room="empty")
            game.spawn(kind, 10, 4)
            run(game, 2.0)
            windups[kind] = times(game, "lunge")[0] - times(game, "windup")[0]
        self.assertAlmostEqual(windups["grub"], 0.5, delta=0.02)
        self.assertAlmostEqual(windups["runner"], 0.35, delta=0.02)
        self.assertAlmostEqual(windups["brute"], 0.7, delta=0.02)

    def test_rooms_match_the_spec(self):
        self.assertEqual(
            ROOMS["2"], [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)]
        )
        self.assertEqual(
            ROOMS["4"], [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)]
        )
        self.assertEqual(ROOMS["5"][2], ("brute", 4, 8))


class SpitterTest(unittest.TestCase):
    def test_room_3_first_shots_are_staggered_and_cued_0_6_s_before(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            most = 0
            for _ in range(12 * fps):
                game.step()
                most = max(most, len(game.shots))
            tol = 1.0 / fps + 1e-9
            spits, aims = times(game, "spit"), times(game, "aim")
            for got, want in zip(spits, (1.8, 2.6, 3.4)):
                self.assertAlmostEqual(got, want, delta=tol, msg=fps)
            for aim, spit in zip(aims, spits):
                self.assertAlmostEqual(spit - aim, 0.6, delta=tol, msg=fps)
            self.assertLessEqual(most, 3, fps)

    def test_shot_follows_the_locked_line_and_a_sidestep_dodges_it(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 1, 4)
            self.assertTrue(step_until(game, has_event("aim")))
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            self.assertTrue(step_until(game, has_event("spit")))
            self.assertAlmostEqual(game.shots[0][3], 0.0, places=9)  # still along y = 4
            run(game, 4.0)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_standing_player_is_hit_by_the_shot(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 4)
        run(game, 5.0)
        self.assertEqual(game.hearts, HEARTS - 1)


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(2, 4)
            game.press("dash", "right")
            run(game, 0.5)
            self.assertAlmostEqual(game.x, 2 + DASH_DISTANCE, places=6)

    def test_attack_during_dash_fires_when_it_ends(self):
        game = Game(room="empty")
        game.place_player(2, 4)
        game.press("dash", "right")
        run(game, 0.1)
        game.press("attack")
        self.assertFalse(any(kind == "attack" for _, kind, _ in game.events))
        run(game, 0.2)
        self.assertTrue(any(kind == "attack" for _, kind, _ in game.events))

    def test_dash_has_a_cooldown(self):
        game = Game(room="empty")
        game.press("dash", "left")
        run(game, 0.5)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "ignored")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(4, 4)
            game.spawn("grub", 4.5, 4)
            game.spawn("grub", 4.5, 5)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 0.32)  # hit-stun passes, still hurt-invulnerable
            game.press("dash", "right")
            run(game, 1.5)
            hurt = times(game, "hurt")
            ended = next(t for t, kind, _ in game.events if kind == "dash_end")
            self.assertTrue(all(t >= ended for t in hurt[1:]), (fps, hurt, ended))
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        import bots

        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_dodger_agrees_at_30_and_60_fps(self):
        import bots

        for room in ("1", "2", "3", "4", "5"):
            a = bots.play_room(bots.BOTS["dodger"], room, 30, 60)
            b = bots.play_room(bots.BOTS["dodger"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))

    @unittest.expectedFailure
    def test_walker_agrees_at_30_and_60_fps(self):
        # KNOWN, UNEXPLAINED (G-001 step 10): the walker differs between rates in rooms 3-5
        # (room 3: 0 hearts lost at 30 FPS, 2 at 60 FPS; room 5: not cleared at 30, cleared at
        # 60). Not diagnosed; may be bot sensitivity to frame rounding of the 0.15 s decision
        # grid, may be a build defect. Remove expectedFailure once resolved.
        import bots

        for room in ("1", "2", "3", "4", "5"):
            a = bots.play_room(bots.BOTS["walker"], room, 30, 60)
            b = bots.play_room(bots.BOTS["walker"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))


class ReactionTest(unittest.TestCase):
    def session(self, script):
        import contextlib
        import io

        import play

        setup, inputs, rules = play.read_script(script)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            play.play(setup, inputs, "player", rules)
        return out.getvalue()

    def test_rules_react_to_what_is_on_screen(self):
        out = self.session("room empty\nspawn grub 9.2 4\nwhen see g within 1.4 then attack\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("YOU ARE HIT", out)

    def test_cues_show_in_the_player_view(self):
        out = self.session("room empty\nspawn grub 10 4\nspawn spitter 1 1\nend 2.5\n")
        self.assertIn("a grub rears back", out)
        self.assertIn("a spitter takes aim", out)
        self.assertIn("~", out)
        self.assertIn("cue: g", out)
        self.assertIn("cue: s", out)

    def test_marks_r_and_G_are_drawn(self):
        out = self.session("room 2\nend 0.2\n")
        self.assertIn("r", out)
        self.assertIn("G", out)

    def test_a_rule_acts_at_most_every_reaction_time(self):
        import play

        rule = play.Rule("when see g within 20 then attack")
        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        fired = 0
        for _ in range(60):  # one second at 60 FPS
            before = rule.last
            play.react(game, [rule], [], [])
            fired += rule.last != before
            game.step()
        self.assertEqual(fired, 7)  # 0.0, 0.15, ... 0.9

    def test_rules_ignore_what_is_not_drawn(self):
        import play

        game = Game(room="empty")  # nothing on screen
        view = play.View(game, [])
        self.assertIsNone(view.nearest())
        self.assertTrue(play.Rule("when nothing within 3 then stop").matches(view))

    def test_rules_and_timed_inputs_mix(self):
        out = self.session("room empty\n0.1 dash right\nwhen see g within 1.4 then attack\nend 1\n")
        self.assertIn("you dash right", out)

    def test_a_bad_rule_says_how_rules_read(self):
        import play

        with self.assertRaises(ValueError) as caught:
            play.Rule("when grub close then hit")
        self.assertIn("conditions:", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE goals/G-001-combat-monotony/08-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 8
from: qa
to: studio
stage: Observe
outcome: done
---
# 08: qa → studio — 30 vs 60 FPS dodger discrepancy reproduced; build timing consistent, cause not isolated

## Task

Report on the 30 vs 60 FPS discrepancy in the balance-bot results and on dash invulnerability in the build (0.4). Studio decides the next routing.

## Context

Goal G-001 (combat monotony). The project constraint is "must play correctly at both 30 and 60 FPS". Studio handoff 06 reported that the dodger bot failed room 3 at 60 FPS and cleared it at 30 FPS. No build or bot change was made in this step; this is report only.

## Findings

### 1. Reproduction (bot results)

Script (`run_bots`, one script per rate, first line optional):

```text
bots camper,walker,dodger
rooms 1-5
fps 60        # second run: fps 30
```

Build at the time of the run: `repo/` 0.4 (the combat.md changes are SPEC for the next build and are not in this build).

| Bot / room | 60 FPS | 30 FPS |
|---|---|---|
| dodger room 3 | NOT cleared (19.7 s), 3 hearts lost (shot 3), attacks 3, dashes 13 | cleared 9.5 s, 0 hearts lost, attacks 6, dashes 4 |
| dodger room 4 | cleared 21.8 s, 2 lost (shot), dashes 9 | cleared 17.8 s, 2 lost (shot), dashes 6 |
| dodger room 5 | cleared 17.7 s, 1 lost, dashes 8 | cleared 17.8 s, 1 lost, dashes 8 |
| dodger rooms 1, 2 | 5.1 s and 7.1 s, 0 lost | 5.0 s and 7.0 s, 0 lost |
| dodger total | cleared 4/5, 6 hearts lost, 30 dashes | cleared 5/5, 3 hearts lost, 18 dashes |
| walker | 5/5 cleared, 1 heart lost in total (room 3, shot) | identical outcomes |
| camper | 2/5 cleared, 9 hearts lost | identical outcomes |

- **Reproduced**: yes, the 06 observation is exactly as reported.
- **Deterministic**: yes. Two identical 60 FPS runs gave byte-identical output. The game is headless and deterministic.
- **Where it stops**: only the dodger differs materially, in rooms 3 and 4. Rooms 1, 2, 5 and the walker and camper agree. Their clear times differ by at most 0.1 s, which is one frame of quantization.
- **Bots test**: `python3 -m unittest discover -s tests` passes (14 tests).

### 2. Does the simulation itself differ between 30 and 60 FPS? (traces)

Not in anything I could measure. Traces were taken in the practice room (`room empty`, `spawn`, `player`) at both rates:

- **Spitter timing**: the shot is fired at t=2.000 and t=4.000 at both rates.
- **Shot damage**: with no dash, the player is hit at t=4.250 at 60 FPS, losing 1 heart. Shot travel time is the same.
- **Dash distance**: 4.00 tiles at both rates (the test suite also checks this).
- **Dash duration**: the dash ends at t=0.250 at 60 FPS (frame 15) and t=0.267 at 30 FPS (frame 8). This is frame rounding of up to one frame.
- **Hit-stun and hurt-invulnerability**: a hit gives stun 0.300 s and invulnerability 0.800 s at both rates. The second grub hit comes 0.8 s after the first (t=0.250 → 1.050 at 60 FPS, 0.267 → 1.067 at 30 FPS).
- **Not directly traced**: grub walk speed and cooldown are computed from `dt` in the same way at both rates. I did not test them separately beyond the bot room runs.

So the simulation constants and event times agree within one frame. The measured discrepancy sits in the dodger bot's results.

### 3. Dash invulnerability vs `design/combat.md` ("invulnerable for the full dash duration")

The build matches at both rates in the cases I traced.

- **Dash into a grub** (`player 0 4`, grub at 0.5, 4, `0.0 dash left`): invulnerable from the dash press until the dash-timer-ended frame. The first hit lands at t=0.250 (60 FPS) and t=0.267 (30 FPS), in the same simulation step in which the dash ends. No hit occurs while the dash is active.
- **Dash through a shot**: in the practice room, a shot due to reach the player at about t=4.25 was crossed by a dash started at 4.1 s. The dash covered 4.1–4.35 s at 60 FPS and 4.133–4.367 s at 30 FPS. No hurt event occurred at either rate. The control run without the dash was hit at t=4.250.
- **Invulnerability handoff**: the trace shows invulnerability dropping on "dash timer ended" and being re-set by "hurt" in the same step. This is consistent with the spec and with the existing test.
- **Not tested**: a dash started while hurt-invulnerable (the existing test `test_a_dash_right_after_a_hit_keeps_both_protections` covers it at both rates and passes), and dash against a lunging grub (not in this build).

### 4. Defect assessment

- **Build defect confirmed?** No. I found no build behaviour that differs between 30 and 60 FPS beyond ±1 frame rounding.
- **Bot issue?** Likely, but not isolated. This is a hypothesis, not a finding: the dodger acts every frame, with no reaction delay, and dashes whenever a shot is detected and the dash is ready. Dashes are 4 tiles long. A one-frame difference in when a shot is first detected, or in where the dash ends, may be enough to shift later decisions in a chaotic way (13 dashes at 60 FPS vs 4 at 30 FPS in room 3). Note that `play.py` limits rules to one action per 0.15 s but `bots.py` does not.
- **Ruled out**: non-determinism; differing spit timing, dash distance, hit-stun and hurt-invulnerability timing; dash invulnerability missing at either rate in the traced cases.
- **Not ruled out**: an unnoticed 30/60 difference in a case I did not trace, for example shot reach and position checks while the player is dashing past a shot at different frame offsets. I did not examine this. I could not produce a per-frame bot decision log because `bots.py` only prints summaries and I may not change it.
- **Cannot yet say** whether the dodger's room 3 result "should" be the 30 FPS or the 60 FPS result. Neither rate is defined as correct by the spec.

### 5. Severity and frequency

- **Severity**: medium for the project's evaluation. The discrepancy affects bot-based balance verification, not the player, as far as measured. If the cause turns out to be the build, it would be a constraint violation.
- **Frequency**: always reproduced at the given scripts (deterministic).

### 6. Effect on the 07 spec's acceptance criteria

`design/combat.md` criteria 13–16 depend on the dodger behaving the same at both rates, and the existing bots do not react to the new cues. They stay conditional. Criteria 1–12 cannot be run against build 0.4 at all (grub wind-up, aim cue, new rooms and variants are not in the build).

## Decisions already made

None.

## Constraints

- No change to the build or bots was made.
- Must play correctly at both 30 and 60 FPS (project.md#constraints).

## Open questions

- Is the room 3 / room 4 dodger split purely a bot-sensitivity effect? To settle it, either update the dodger with a frame-rate-independent reaction (an accumulated-time reaction delay like `play.py`'s 0.15 s) and re-run, or log the dodger's per-frame decisions, e.g. via a `gameplay-engineer` change to `bots.py`.
- Suggested check for that next run: a reaction-rule script in `play.py` (for example `when see * coming within 2 then dash aside` plus the walker-like rules) in room 3 at 30 and 60 FPS. If it gives the same outcome at both rates, the build is not the cause.
- Which of the two results should count as the dodger baseline for criterion 13? Studio / `game-designer` to say once the bot is fixed.

## Expected output

This report. Proposed next step by Studio:

- Route to `gameplay-engineer` to make the dodger bot frame-rate independent (accumulated-time reaction delay) and to add reaction to the new cues. Do not change the build for this.
- Afterwards, QA re-runs the bots at 30 and 60 FPS (`bots camper,walker,dodger`, `rooms 1-5`, both rates), and verifies criteria 13–16.

If a defect is later confirmed in the build, acceptance criteria for the fix:
1. The same bot script gives equal pass/fail per room at 30 and 60 FPS, with hearts lost within ±1 and clear time within ±0.5 s.
2. Traces of dash into a grub and through a shot show no hurt event during the dash at either rate.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, repo/bots.py, repo/game.py, repo/play.py
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/06-studio-to-qa.md
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
### Round 1: @run/bots/walker30 — `python3 bots.py {script}`

Script:

```text
bots walker
rooms 1-5
fps 30
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
walker  room 1: NOT cleared (4.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
            0.00 s  walk to grub
            0.17 s  walk to grub
            0.30 s  walk to grub
            0.47 s  face and swing at grub
            0.60 s  face and swing at grub
            0.77 s  face and swing at grub
            0.90 s  face and swing at grub
            1.07 s  face and swing at grub
            1.43 s  face and swing at grub
            1.50 s  walk to grub
            1.67 s  walk to grub
            1.80 s  face and swing at grub
            1.97 s  face and swing at grub
            2.10 s  face and swing at grub
            2.27 s  face and swing at grub
            2.40 s  face and swing at grub
            2.57 s  face and swing at grub
            2.70 s  face and swing at grub
            2.87 s  face and swing at grub
            3.33 s  face and swing at grub
            3.47 s  walk to grub
            3.60 s  walk to grub
            3.77 s  walk to grub
            3.90 s  walk to grub
            4.07 s  face and swing at grub
            4.20 s  face and swing at grub
            4.37 s  face and swing at grub
            4.50 s  face and swing at grub
            4.67 s  face and swing at grub
            4.80 s  face and swing at grub
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
            0.00 s  walk to runner
            0.17 s  walk to runner
            0.30 s  walk to runner
            0.47 s  walk to runner
            0.60 s  walk to runner
            0.77 s  walk to runner
            0.90 s  face and swing at runner
            1.07 s  face and swing at runner
            1.20 s  face and swing at runner
            1.37 s  face and swing at runner
            1.50 s  face and swing at runner
            1.67 s  face and swing at runner
            1.80 s  walk to runner
            1.97 s  face and swing at runner
            2.10 s  face and swing at runner
            2.27 s  face and swing at runner
            2.40 s  face and swing at runner
            2.57 s  face and swing at runner
            2.70 s  face and swing at runner
            2.87 s  walk to grub
            3.00 s  walk to grub
            3.17 s  walk to grub
            3.30 s  walk to grub
            3.47 s  walk to grub
            3.60 s  walk to grub
            3.77 s  walk to grub
            3.90 s  walk to grub
            4.07 s  face and swing at grub
            4.20 s  face and swing at grub
            4.37 s  face and swing at grub
            4.50 s  face and swing at grub
            4.67 s  face and swing at grub
            4.80 s  face and swing at grub
            5.27 s  face and swing at grub
            5.40 s  walk to brute
            5.57 s  face and swing at brute
            5.70 s  face and swing at brute
            5.87 s  face and swing at brute
            6.00 s  face and swing at brute
            6.17 s  face and swing at brute
            6.30 s  face and swing at brute
            6.47 s  face and swing at brute
            6.60 s  face and swing at brute
            6.77 s  face and swing at brute
            6.90 s  face and swing at brute
            7.07 s  face and swing at brute
            7.47 s  face and swing at brute
            7.50 s  face and swing at brute
            7.67 s  face and swing at brute
            7.80 s  face and swing at brute
            7.97 s  face and swing at brute
            8.10 s  face and swing at brute
            8.27 s  face and swing at brute
            8.40 s  face and swing at brute
walker  room 3: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
            0.00 s  walk to spitter
            0.17 s  walk to spitter
            0.30 s  walk to spitter
            0.47 s  walk to spitter
            0.60 s  walk to spitter
            0.77 s  walk to spitter
            0.90 s  walk to spitter
            1.07 s  walk to spitter
            1.20 s  walk to spitter
            1.37 s  walk to spitter
            1.50 s  walk to spitter
            1.67 s  walk to spitter
            1.80 s  sidestep shot in flight
            1.97 s  sidestep shot in flight
            2.10 s  walk to spitter
            2.27 s  sidestep shot in flight
            2.40 s  walk to spitter
            2.57 s  walk to spitter
            2.70 s  walk to spitter
            2.87 s  face and swing at spitter
            3.00 s  face and swing at spitter
            3.17 s  face and swing at spitter
            3.30 s  face and swing at spitter
            3.47 s  walk to spitter
            3.60 s  walk to spitter
            3.77 s  walk to spitter
            3.90 s  sidestep shot in flight
            4.07 s  sidestep shot in flight
            4.20 s  walk to spitter
            4.37 s  walk to spitter
            4.50 s  walk to spitter
            4.67 s  walk to spitter
            4.80 s  walk to spitter
            4.97 s  walk to spitter
            5.10 s  face and swing at spitter
            5.27 s  face and swing at spitter
            5.40 s  face and swing at spitter
            5.57 s  face and swing at spitter
            5.70 s  walk to spitter
            5.87 s  walk to spitter
            6.00 s  walk to spitter
            6.17 s  walk to spitter
            6.30 s  walk to spitter
            6.47 s  walk to spitter
            6.60 s  walk to spitter
            6.77 s  walk to spitter
            6.90 s  walk to spitter
            7.07 s  walk to spitter
            7.20 s  walk to spitter
            7.37 s  walk to spitter
            7.50 s  sidestep shot in flight
            7.67 s  walk to spitter
            7.80 s  walk to spitter
            7.97 s  walk to spitter
            8.10 s  walk to spitter
            8.27 s  walk to spitter
            8.40 s  walk to spitter
            8.57 s  walk to spitter
            8.70 s  face and swing at spitter
            8.87 s  face and swing at spitter
            9.00 s  sidestep shot in flight
            9.17 s  sidestep shot in flight
            9.30 s  walk to spitter
            9.47 s  walk to spitter
            9.60 s  face and swing at spitter
walker  room 4: cleared in 10.5 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0
            0.00 s  walk to runner
            0.17 s  walk to runner
            0.30 s  walk to runner
            0.47 s  walk to runner
            0.60 s  walk to runner
            0.77 s  walk to runner
            0.90 s  face and swing at runner
            1.07 s  face and swing at runner
            1.20 s  face and swing at runner
            1.37 s  face and swing at runner
            1.50 s  walk to grub
            1.67 s  walk to grub
            1.80 s  walk to grub
            1.97 s  face and swing at grub
            2.10 s  face and swing at grub
            2.27 s  face and swing at grub
            2.40 s  face and swing at grub
            2.57 s  face and swing at grub
            2.70 s  face and swing at grub
            3.07 s  face and swing at grub
            3.17 s  walk to spitter
            3.30 s  walk to spitter
            3.47 s  walk to spitter
            3.60 s  walk to spitter
            3.77 s  walk to spitter
            3.90 s  walk to spitter
            4.07 s  sidestep shot in flight
            4.20 s  walk to spitter
            4.37 s  walk to spitter
            4.50 s  walk to spitter
            4.67 s  walk to spitter
            4.80 s  walk to spitter
            4.97 s  walk to spitter
            5.10 s  walk to spitter
            5.27 s  walk to spitter
            5.40 s  walk to spitter
            5.57 s  walk to spitter
            5.70 s  walk to spitter
            5.87 s  walk to spitter
            6.00 s  walk to spitter
            6.17 s  walk to spitter
            6.30 s  walk to spitter
            6.47 s  walk to spitter
            6.60 s  walk to spitter
            6.77 s  walk to spitter
            6.90 s  face and swing at spitter
            7.07 s  face and swing at spitter
            7.20 s  face and swing at spitter
            7.37 s  face and swing at spitter
            7.50 s  walk to spitter
            7.67 s  walk to spitter
            7.80 s  walk to spitter
            7.97 s  walk to spitter
            8.10 s  walk to spitter
            8.27 s  sidestep shot in flight
            8.40 s  walk to spitter
            8.57 s  walk to spitter
            8.70 s  walk to spitter
            8.87 s  walk to spitter
            9.00 s  walk to spitter
            9.17 s  walk to spitter
            9.30 s  walk to spitter
            9.47 s  face and swing at spitter
            9.60 s  face and swing at spitter
            9.77 s  face and swing at spitter
            9.90 s  sidestep shot in flight
           10.07 s  sidestep shot in flight
           10.20 s  walk to spitter
           10.37 s  walk to spitter
           10.50 s  face and swing at spitter
walker  room 5: NOT cleared (10.2 s); hearts lost 3 (hit by: grub 2, shot 1); attacks 9, dashes 0
            0.00 s  walk to brute
            0.17 s  walk to brute
            0.30 s  walk to brute
            0.47 s  walk to brute
            0.60 s  walk to brute
            0.77 s  walk to brute
            0.90 s  face and swing at brute
            1.07 s  face and swing at brute
            1.20 s  face and swing at brute
            1.37 s  face and swing at brute
            1.50 s  face and swing at brute
            1.67 s  face and swing at brute
            1.80 s  face and swing at brute
            1.97 s  face and swing at brute
            2.10 s  face and swing at brute
            2.27 s  face and swing at brute
            2.40 s  face and swing at brute
            2.87 s  face and swing at brute
            3.00 s  face and swing at brute
            3.17 s  face and swing at brute
            3.30 s  face and swing at brute
            3.47 s  face and swing at brute
            3.60 s  face and swing at brute
            3.77 s  face and swing at brute
            3.90 s  face and swing at grub
            4.07 s  face and swing at grub
            4.20 s  face and swing at grub
            4.37 s  face and swing at grub
            4.50 s  face and swing at grub
            4.67 s  sidestep shot in flight
            4.80 s  sidestep shot in flight
            4.97 s  face and swing at grub
            5.10 s  face and swing at grub
            5.27 s  face and swing at grub
            5.40 s  face and swing at grub
            5.57 s  face and swing at grub
            6.00 s  face and swing at grub
            6.17 s  face and swing at grub
            6.30 s  face and swing at grub
            6.47 s  face and swing at grub
            6.60 s  walk to spitter
            6.77 s  sidestep shot in flight
            6.90 s  walk to spitter
            7.07 s  walk to spitter
            7.20 s  walk to spitter
            7.37 s  walk to spitter
            7.50 s  walk to spitter
            7.67 s  walk to spitter
            7.80 s  walk to spitter
            7.97 s  walk to spitter
            8.10 s  walk to spitter
            8.27 s  walk to spitter
            8.40 s  walk to spitter
            8.57 s  walk to spitter
            8.70 s  walk to spitter
            8.87 s  walk to spitter
            9.00 s  walk to spitter
            9.17 s  walk to spitter
            9.30 s  walk to spitter
            9.47 s  walk to spitter
            9.60 s  face and swing at spitter
            9.77 s  face and swing at spitter
            9.90 s  sidestep shot in flight
           10.07 s  walk to spitter
walker  total: cleared 3/5, hearts lost 9, dashes 0
```

### Round 1: @run/bots/walker60 — `python3 bots.py {script}`

Script:

```text
bots walker
rooms 1-5
fps 60
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
            0.00 s  walk to grub
            0.15 s  walk to grub
            0.30 s  face and swing at grub
            0.45 s  face and swing at grub
            0.60 s  face and swing at grub
            0.75 s  face and swing at grub
            0.90 s  face and swing at grub
            1.05 s  face and swing at grub
            1.20 s  face and swing at grub
            1.35 s  face and swing at grub
            1.82 s  face and swing at grub
            1.95 s  face and swing at grub
            2.10 s  face and swing at grub
            2.25 s  face and swing at grub
            2.40 s  walk to grub
            2.55 s  face and swing at grub
            2.70 s  face and swing at grub
            2.85 s  face and swing at grub
            3.00 s  face and swing at grub
            3.15 s  face and swing at grub
            3.60 s  face and swing at grub
            3.75 s  face and swing at grub
            3.90 s  face and swing at grub
            4.05 s  face and swing at grub
            4.20 s  walk to grub
            4.35 s  walk to grub
            4.50 s  face and swing at grub
            4.65 s  face and swing at grub
            4.80 s  face and swing at grub
            4.95 s  face and swing at grub
            5.10 s  face and swing at grub
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
            0.00 s  walk to runner
            0.15 s  walk to runner
            0.30 s  walk to runner
            0.45 s  walk to runner
            0.60 s  walk to runner
            0.75 s  walk to runner
            0.90 s  face and swing at runner
            1.05 s  face and swing at runner
            1.20 s  face and swing at runner
            1.35 s  face and swing at runner
            1.50 s  face and swing at runner
            1.65 s  face and swing at runner
            1.80 s  walk to runner
            1.95 s  walk to runner
            2.10 s  face and swing at runner
            2.25 s  face and swing at runner
            2.40 s  face and swing at runner
            2.55 s  face and swing at runner
            2.70 s  walk to grub
            2.85 s  walk to grub
            3.00 s  walk to grub
            3.15 s  walk to grub
            3.30 s  walk to grub
            3.45 s  walk to grub
            3.60 s  walk to grub
            3.75 s  walk to grub
            3.90 s  walk to grub
            4.05 s  face and swing at grub
            4.20 s  face and swing at grub
            4.35 s  face and swing at grub
            4.50 s  face and swing at grub
            4.65 s  face and swing at grub
            5.07 s  face and swing at grub
            5.10 s  walk to brute
            5.25 s  walk to brute
            5.40 s  face and swing at brute
            5.55 s  face and swing at brute
            5.70 s  face and swing at brute
            5.85 s  face and swing at brute
            6.00 s  face and swing at brute
            6.15 s  face and swing at brute
            6.30 s  face and swing at brute
            6.45 s  face and swing at brute
            6.60 s  face and swing at brute
            7.07 s  face and swing at brute
            7.20 s  face and swing at brute
            7.35 s  face and swing at brute
            7.50 s  face and swing at brute
            7.65 s  face and swing at brute
            7.80 s  face and swing at brute
            7.95 s  face and swing at brute
            8.10 s  face and swing at brute
            8.25 s  face and swing at brute
            8.40 s  face and swing at brute
walker  room 3: cleared in 9.5 s; hearts lost 2 (hit by: shot 2); attacks 6, dashes 0
            0.00 s  walk to spitter
            0.15 s  walk to spitter
            0.30 s  walk to spitter
            0.45 s  walk to spitter
            0.60 s  walk to spitter
            0.75 s  walk to spitter
            0.90 s  walk to spitter
            1.05 s  walk to spitter
            1.20 s  walk to spitter
            1.35 s  walk to spitter
            1.50 s  walk to spitter
            1.65 s  walk to spitter
            1.80 s  sidestep shot in flight
            1.95 s  sidestep shot in flight
            2.10 s  walk to spitter
            2.57 s  walk to spitter
            2.70 s  walk to spitter
            2.85 s  face and swing at spitter
            3.00 s  face and swing at spitter
            3.15 s  face and swing at spitter
            3.30 s  face and swing at spitter
            3.45 s  walk to spitter
            3.60 s  walk to spitter
            3.75 s  walk to spitter
            3.90 s  walk to spitter
            4.05 s  sidestep shot in flight
            4.20 s  walk to spitter
            4.35 s  walk to spitter
            4.50 s  walk to spitter
            4.65 s  walk to spitter
            4.80 s  walk to spitter
            4.95 s  face and swing at spitter
            5.10 s  face and swing at spitter
            5.25 s  face and swing at spitter
            5.40 s  face and swing at spitter
            5.55 s  walk to spitter
            5.70 s  walk to spitter
            5.85 s  walk to spitter
            6.00 s  walk to spitter
            6.15 s  walk to spitter
            6.30 s  walk to spitter
            6.45 s  walk to spitter
            6.60 s  walk to spitter
            6.75 s  walk to spitter
            6.90 s  sidestep shot in flight
            7.28 s  walk to spitter
            7.35 s  walk to spitter
            7.50 s  walk to spitter
            7.65 s  walk to spitter
            7.80 s  walk to spitter
            7.95 s  sidestep shot in flight
            8.10 s  walk to spitter
            8.25 s  walk to spitter
            8.40 s  walk to spitter
            8.55 s  walk to spitter
            8.70 s  walk to spitter
            8.85 s  walk to spitter
            9.00 s  face and swing at spitter
            9.15 s  face and swing at spitter
            9.30 s  face and swing at spitter
            9.45 s  face and swing at spitter
walker  room 4: cleared in 11.9 s; hearts lost 2 (hit by: grub 1, shot 1); attacks 7, dashes 0
            0.00 s  walk to runner
            0.15 s  walk to runner
            0.30 s  walk to runner
            0.45 s  walk to runner
            0.60 s  walk to runner
            0.75 s  walk to runner
            0.90 s  face and swing at runner
            1.05 s  face and swing at runner
            1.20 s  face and swing at runner
            1.35 s  face and swing at runner
            1.50 s  walk to grub
            1.65 s  walk to grub
            1.80 s  walk to grub
            1.95 s  face and swing at grub
            2.10 s  face and swing at grub
            2.25 s  face and swing at grub
            2.40 s  face and swing at grub
            2.55 s  face and swing at grub
            2.70 s  face and swing at grub
            3.05 s  face and swing at grub
            3.15 s  face and swing at grub
            3.30 s  walk to spitter
            3.45 s  walk to spitter
            3.60 s  walk to spitter
            3.75 s  walk to spitter
            3.90 s  walk to spitter
            4.05 s  walk to spitter
            4.20 s  sidestep shot in flight
            4.35 s  walk to spitter
            4.50 s  walk to spitter
            4.65 s  walk to spitter
            4.80 s  walk to spitter
            4.95 s  walk to spitter
            5.10 s  walk to spitter
            5.25 s  walk to spitter
            5.40 s  walk to spitter
            5.55 s  walk to spitter
            5.70 s  walk to spitter
            5.85 s  walk to spitter
            6.00 s  walk to spitter
            6.15 s  walk to spitter
            6.30 s  walk to spitter
            6.45 s  walk to spitter
            6.60 s  walk to spitter
            6.75 s  walk to spitter
            6.90 s  walk to spitter
            7.05 s  face and swing at spitter
            7.20 s  face and swing at spitter
            7.35 s  face and swing at spitter
            7.50 s  sidestep shot in flight
            7.65 s  sidestep shot in flight
            7.80 s  walk to spitter
            8.22 s  walk to spitter
            8.25 s  walk to spitter
            8.40 s  walk to spitter
            8.55 s  face and swing at spitter
            8.70 s  walk to spitter
            8.85 s  walk to spitter
            9.00 s  sidestep shot in flight
            9.15 s  sidestep shot in flight
            9.30 s  sidestep shot in flight
            9.45 s  walk to spitter
            9.60 s  walk to spitter
            9.75 s  walk to spitter
            9.90 s  walk to spitter
           10.05 s  walk to spitter
           10.20 s  walk to spitter
           10.35 s  walk to spitter
           10.50 s  walk to spitter
           10.65 s  walk to spitter
           10.80 s  walk to spitter
           10.95 s  walk to spitter
           11.10 s  walk to spitter
           11.25 s  walk to spitter
           11.40 s  face and swing at spitter
           11.55 s  face and swing at spitter
           11.70 s  face and swing at spitter
           11.85 s  face and swing at spitter
walker  room 5: cleared in 12.9 s; hearts lost 2 (hit by: grub 2); attacks 12, dashes 0
            0.00 s  walk to brute
            0.15 s  walk to brute
            0.30 s  walk to brute
            0.45 s  walk to brute
            0.60 s  walk to brute
            0.75 s  walk to brute
            0.90 s  face and swing at brute
            1.05 s  face and swing at brute
            1.20 s  face and swing at brute
            1.35 s  face and swing at brute
            1.50 s  face and swing at brute
            1.65 s  face and swing at brute
            1.80 s  face and swing at brute
            1.95 s  face and swing at brute
            2.10 s  face and swing at brute
            2.25 s  face and swing at brute
            2.40 s  face and swing at brute
            2.82 s  face and swing at brute
            2.85 s  face and swing at brute
            3.00 s  face and swing at brute
            3.15 s  face and swing at brute
            3.30 s  face and swing at brute
            3.45 s  face and swing at brute
            3.60 s  face and swing at brute
            3.75 s  face and swing at brute
            3.90 s  face and swing at grub
            4.05 s  face and swing at grub
            4.20 s  face and swing at grub
            4.35 s  face and swing at grub
            4.50 s  face and swing at grub
            4.65 s  sidestep shot in flight
            4.80 s  sidestep shot in flight
            4.95 s  face and swing at grub
            5.10 s  face and swing at grub
            5.25 s  face and swing at grub
            5.40 s  face and swing at grub
            5.55 s  face and swing at grub
            5.98 s  face and swing at grub
            6.00 s  face and swing at grub
            6.15 s  face and swing at grub
            6.30 s  face and swing at grub
            6.45 s  face and swing at grub
            6.60 s  walk to spitter
            6.75 s  sidestep shot in flight
            6.90 s  walk to spitter
            7.05 s  walk to spitter
            7.20 s  walk to spitter
            7.35 s  walk to spitter
            7.50 s  walk to spitter
            7.65 s  walk to spitter
            7.80 s  walk to spitter
            7.95 s  walk to spitter
            8.10 s  walk to spitter
            8.25 s  walk to spitter
            8.40 s  walk to spitter
            8.55 s  walk to spitter
            8.70 s  walk to spitter
            8.85 s  walk to spitter
            9.00 s  walk to spitter
            9.15 s  walk to spitter
            9.30 s  walk to spitter
            9.45 s  walk to spitter
            9.60 s  face and swing at spitter
            9.75 s  face and swing at spitter
            9.90 s  sidestep shot in flight
           10.05 s  sidestep shot in flight
           10.20 s  sidestep shot in flight
           10.35 s  walk to spitter
           10.50 s  walk to spitter
           10.65 s  walk to spitter
           10.80 s  face and swing at spitter
           10.95 s  walk to spitter
           11.10 s  walk to spitter
           11.25 s  walk to spitter
           11.40 s  walk to spitter
           11.55 s  walk to spitter
           11.70 s  walk to spitter
           11.85 s  walk to spitter
           12.00 s  walk to spitter
           12.15 s  walk to spitter
           12.30 s  walk to spitter
           12.45 s  face and swing at spitter
           12.60 s  face and swing at spitter
           12.75 s  face and swing at spitter
           12.90 s  face and swing at spitter
walker  total: cleared 4/5, hearts lost 11, dashes 0
```

### Round 1: @run/bots/all30 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 1-5
fps 30
```

Exit: 0 (0.0 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 2: cleared in 10.2 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.2 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
camper  total: cleared 1/5, hearts lost 14, dashes 0
walker  room 1: NOT cleared (4.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
walker  room 3: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker  room 4: cleared in 10.5 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0
walker  room 5: NOT cleared (10.2 s); hearts lost 3 (hit by: grub 2, shot 1); attacks 9, dashes 0
walker  total: cleared 3/5, hearts lost 9, dashes 0
dodger  room 1: cleared in 6.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 3
dodger  room 2: cleared in 13.2 s; hearts lost 0 (hit by: none); attacks 8, dashes 6
dodger  room 3: cleared in 19.7 s; hearts lost 0 (hit by: none); attacks 6, dashes 8
dodger  room 4: cleared in 19.1 s; hearts lost 0 (hit by: none); attacks 7, dashes 7
dodger  room 5: cleared in 24.9 s; hearts lost 0 (hit by: none); attacks 12, dashes 11
dodger  total: cleared 5/5, hearts lost 0, dashes 35
```

### Round 1: @run/bots/all60 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 1-5
fps 60
```

Exit: 0 (0.1 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.1 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
camper  total: cleared 0/5, hearts lost 15, dashes 0
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
walker  room 3: cleared in 9.5 s; hearts lost 2 (hit by: shot 2); attacks 6, dashes 0
walker  room 4: cleared in 11.9 s; hearts lost 2 (hit by: grub 1, shot 1); attacks 7, dashes 0
walker  room 5: cleared in 12.9 s; hearts lost 2 (hit by: grub 2); attacks 12, dashes 0
walker  total: cleared 4/5, hearts lost 11, dashes 0
dodger  room 1: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 5
dodger  room 2: cleared in 19.5 s; hearts lost 0 (hit by: none); attacks 8, dashes 11
dodger  room 3: cleared in 22.1 s; hearts lost 0 (hit by: none); attacks 6, dashes 10
dodger  room 4: cleared in 17.0 s; hearts lost 0 (hit by: none); attacks 7, dashes 8
dodger  room 5: cleared in 27.2 s; hearts lost 0 (hit by: none); attacks 12, dashes 14
dodger  total: cleared 5/5, hearts lost 0, dashes 48
```
>>>END
