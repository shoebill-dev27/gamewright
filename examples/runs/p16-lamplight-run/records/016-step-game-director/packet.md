# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-first-playable/15-studio-to-game-director.md
next_seq: 16
runs: play (up to 3 rounds)
run_play: python3 play.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable/16-game-director-to-<recipient>.md
- decisions/D-002-<name>.md
- @run/<play>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-001-first-playable/15-studio-to-game-director.md
---
kind: handoff
goal: G-001
seq: 15
from: studio
to: game-director
stage: Review
outcome: routed
---
# 15: studio → game-director — Review the first playable against the pillars and E-1..E-5

## Task

Judge whether G-001's intent is met, using the playtest observations and the QA result below. Give a verdict (`goal-met` or `goal-not-met`), answer the designer's two open questions (mid-night arrivals; whether a wreck always loses), and name the next issues. Address the result to `studio`.

## Context

Goal G-001: "このコンセプトで、遊べる最初の版を作ってほしい". Design, Build and Verify are done. QA passed the build against AC-1..AC-15 with no defects (12-qa-to-studio.md); `run_tests` is green (31 tests). A Playtester then played nights 1–3 from the manual and the build only (14-playtester-to-studio.md, attached as the previous handoff).

**Budget:** 14 of 15 operations were used before this Route, so this Route uses the last. Review is the one remaining planned step. Studio rules for a used budget: no stages may be added except a `game-director` scope cut or an `owner` cost escalation. If you judge the goal not met, do not request another Diagnose or Build chain on your own. Decide what is the minimum needed for the Owner's request. Either cut scope (the rest becomes proposed Goals), or say that an Owner decision on budget is needed. The Studio will then route accordingly.

## Findings

Playtester observation report (from 14; read it in full for detail):

- **Played:** Night 1 won on turn 7 (also lost by doing nothing, turn 5); Night 2 won on turn 7; Night 3 won on turn 7 (also lost by doing nothing, turn 4). All by input scripts.
- **Pillars:**
  - Reading ahead worked. Predictions matched outcomes every time, and nothing was random.
  - The forecast line, the lit `~` tiles and the per-turn messages made every move explainable.
  - Win and loss messages are plain, and the wreck message names the position.
  - Each night adds one idea: slide, two sides, keep one ship dark.
- **Difficulty and depth:**
  - Night 1 reads as a tutorial.
  - Night 2 is a gentle step up (the beam swing passes through UP).
  - Night 3 is the first with a real trade-off (lighting the wrong ship at the wrong time ruins it), and the best of the three.
  - Rated medium impact: all wins took 7 of 10 turns, nights 1–2 were over quickly, and only one winning line per night was seen. The playtester cannot say whether other or shorter solutions exist.
- **Low-impact friction:**
  - The final screen prints twice with the same turn number (for example "Turn 7 of 10" twice), which briefly suggested a new turn had begun. This is a defect candidate or a presentation issue; you decide which.
  - No hint on a first attempt: an unfinished script gives no sense of progress.
  - Script play removes live feedback; this is a known constraint of the project.
- **Not observed:**
  - DAWN (loss by running out of turns).
  - Pinned ships at column 0 or 6.
  - Overlapping ships.
  - Unrecognized words and a missing `night N` start.
  - A failing Night 2.
  - Real-time pacing and long-session feel (not observable by this method).
- **Player questions:**
  - Is there a reason to win in fewer turns, since the result only says "won on turn N"?
  - Do later nights exist beyond these three?

QA result: pass against AC-1..AC-15, no defects, 31 tests green (see 12-qa-to-studio.md).

## Decisions already made

- D-001: Lit ships slide along the beam row; the beam has three aims.
- Night 3's first screen was settled in Design (the first screen draws `~` under the starting aim); the spec is amended.

## Constraints

- Verdict scope: whether this is a "first version" that shows the core loop (a small set of nights, not a full game), and whether the three pillars hold qualitatively. Numbers and balancing beyond a first playable set are out of scope for G-001.
- You hold direction and scope. Anything that would change a pillar or an existing Decision is an Owner escalation, not yours to decide.
- The playtest is by scripts only; do not treat what it could not observe as a failure by itself.
- Record a Decision only if it constrains work beyond this step.

## Open questions

- The designer's two non-blocking questions, left for Review: (1) mid-night arrivals (ships appearing after turn 1); (2) whether a wreck always loses the night. Answer both, or say they become next issues.
- Is the short, mostly-gentle difficulty (medium finding) acceptable for a first playable, or does it make the Goal not met?
- Is the duplicate final screen a defect to fix now or a next-issue item?

## Expected output

A Review result (templates/handoff.md) addressed to `studio` with `outcome: goal-met` or `goal-not-met`: the verdict against the pillars and E-1..E-5, answers to the open questions, and next issues as proposed new Goals (not scope growth). If goal-not-met, state the minimal remaining work and whether it fits the used budget. The Studio then Closes the Goal or escalates the budget question to the Owner.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md (vision, pillars, player profile); design/first-playable.md; repo/manual.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/14-playtester-to-studio.md (also read goals/G-001-first-playable/12-qa-to-studio.md for the QA result)
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

<<<FILE project.md
---
kind: project
id: lamplight-keeper
name: Lamplight Keeper (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py {script}
run_trace: python3 play.py --trace {script}
---
# Project: Lamplight Keeper (new concept)

## Vision

A short, turn-based puzzle game. The player keeps a lighthouse on a rocky coast for one night at
a time. Ships come in from the dark sea, one tile per turn, heading for the harbor; the lamp's
beam turns them aside, and every turn the player chooses where it points. Bring ships to the
harbor; let none hit the rocks.

Pillars:

1. **One clear choice per turn.** Turn the beam left, turn it right, or hold. Nothing else.
2. **Reading ahead is the fun.** Where each ship will be in a few turns, and what the beam will do
   to it, can be worked out from what is on screen. Luck does not decide a night.
3. **A night is short.** One night takes a few minutes; it is lost or won in that time.

## Player profile

Puzzle players who like short, thinky sessions with readable rules (in the spirit of small
turn-based puzzle games). They want to plan, not to react fast.

## Current state

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.

## Constraints

- The build is a Python 3 program using the standard library only, in `repo/`.
- It is played through input scripts, with no live input: `run_play` (`python3 play.py {script}`)
  plays a script and prints what the player sees, `run_trace` adds the internal state, and
  `run_tests` runs the build's tests. The script format is the build's to define, in
  `repo/manual.md`, which ships with the build and is all a player is told.
- Text output only (a grid of characters per turn); no graphics yet.
- Deterministic: the same script always gives the same night.

## Design index

None yet.
>>>END

<<<FILE design/first-playable.md
---
kind: design
id: first-playable
goal: G-001
status: proposed
author: game-designer
---
# Design: Lamplight Keeper — first playable

## 1. Intent

The player keeps a lighthouse for one short night. Each turn they make one choice (beam left, beam right, hold) and bring every ship into the harbor. Every ship's path can be worked out from the screen and the rules, with no randomness, so a night is solved by reading ahead rather than by reflex. A night takes about 7 turns, well under a few minutes.

## 2. The board

- The sea is a grid of **7 columns × 7 rows**. Both are numbered from 0. Row 0 is the top (the dark open sea); row 6 is the bottom (the coast). Column 0 is the left. A position is written (row, col).
- The **lighthouse** is at (3,3) in every night. Its row, row 3, is the **beam row**.
- Row 6 (the coast) holds only **harbor** and **rock** tiles. Each night defines it.
- Every other tile is **sea**, except the lighthouse tile. The three nights have no other rocks (see §8).

| Element | Symbol | Notes |
|---|---|---|
| Sea (dark) | `.` | Ships may be here. |
| Sea lit by the beam | `~` | Only tiles in row 3 can be lit. |
| Rock | `#` | A ship that enters it is wrecked. |
| Harbor | `H` | A ship that enters it is docked (safe, removed from play). |
| Lighthouse | `T` | Always (3,3). Treated like a rock: a ship that enters it is wrecked. |
| Ship | `1`–`9` | The digit is the ship's number. A ship's symbol is drawn over `.` or `~`. |

If two ships share a tile, the board draws the lower number. The ship list (§6) names both. Ships never collide or interact (see §7).

## 3. The beam

The beam has an **aim**, one of three values: `LEFT`, `UP`, `RIGHT`. Each night defines its starting aim.

- **LEFT** lights every tile in row 3 with column < 3, i.e. (3,0), (3,1), (3,2). It lights the whole stretch to the map edge. Rocks do not block it, and ships do not block it.
- **RIGHT** lights (3,4), (3,5), (3,6).
- **UP** lights nothing. The beam points over the open sea and affects no ship.
- The lighthouse tile (3,3) is never lit.

Player commands, exactly one per turn:

| Command | Effect on aim |
|---|---|
| `L` (turn left) | RIGHT → UP, UP → LEFT, LEFT → LEFT (stays; the beam stops at its left end). |
| `R` (turn right) | LEFT → UP, UP → RIGHT, RIGHT → RIGHT. |
| `H` (hold) | Aim unchanged. |

Going from LEFT to RIGHT, or the reverse, therefore takes two turns and passes through UP. This is the main thing the player plans around.

## 4. A turn, in order

Turn numbers start at 1. Each turn goes as follows:

1. **Show.** The screen shows the board and the information in §6.
2. **Command.** The player gives `L`, `R` or `H`, and the aim changes as in §3. The lit tiles are those of the **new** aim.
3. **Move.** Every ship still at sea moves at once, judged by where it stood at the start of the move.
   - If its tile is **lit**, it does not advance. It slides **one tile along row 3 away from the lighthouse**: west (column − 1) under LEFT, east (column + 1) under RIGHT.
   - If its tile is **not lit**, it moves **one tile south** (row + 1).
   - A lit ship at column 0 under LEFT, or at column 6 under RIGHT, cannot slide off the map. It stays where it is (pinned).
4. **Resolve.** Each ship's new tile decides its fate:
   - Harbor → **docked**: the ship is removed and counts as safe.
   - Rock or lighthouse → **wrecked**.
   - Sea → the ship stays at sea.
5. **Report.** The screen lists what happened to each ship that moved: slid west or east, moved south, was pinned, docked, or was wrecked, with the position.
6. **End check.** The whole turn is resolved first, so ships that dock and ships that wreck on the same turn are all reported.
   - If any ship was wrecked → the night is **lost** at once.
   - Otherwise, if all ships are docked → the night is **won**.
   - Otherwise, if this was turn 10 → the night is **lost at dawn** (ships still at sea).
   - Otherwise the next turn begins.

## 5. Parameters

| Parameter | Value |
|---|---|
| Grid | 7 × 7 |
| Lighthouse | (3,3) |
| Ship speed | 1 tile per turn (south, or 1 tile sideways when lit) |
| Turn limit (dawn) | 10 turns, then the night ends |
| Commands | `L`, `R`, `H` |
| Beam aims | LEFT, UP, RIGHT (3) |
| Beam range | The full beam row on the lit side |
| Ships per night | 1 to 3 in the first nights; 9 at most overall |

A ship's trajectory is fully predictable. Ships are all on the board at turn 0 and nothing enters mid-night. A ship in row 3 moves exactly as §4 says. A ship in any other row moves south one tile per turn, because only row 3 can be lit.

## 6. What the player sees (required content)

Every turn, before the command, the screen shows:

1. A header with the night number, the current turn out of the limit, and the current beam aim.
2. The board, with row and column numbers so any position can be read as (row, col). Lit tiles are drawn `~`.
3. A **ship list** with one line per ship still at sea: number and position. Docked ships are listed as docked.
4. A **forecast line** giving the aim each command would produce from the current aim, e.g. `L -> LEFT, H -> UP, R -> RIGHT`.

After a command, the screen shows the event report of §4 step 5. When the night ends it shows a clear result: **NIGHT WON**, **NIGHT LOST** (naming the wrecked ships and where), or **DAWN: ships still at sea** (naming them). The exact layout belongs to the build and `repo/manual.md`. The symbols, the content above and the rules above do not change.

## 7. Edge cases

| Case | Rule |
|---|---|
| Two ships on one tile | Allowed. They never interact. The board shows the lower number; the ship list shows both. |
| Ship moves south from (2,3) | It enters the lighthouse tile (3,3) and is wrecked. (No ship may start at (3,3).) |
| Ship slides into a rock in row 3 | Wrecked (no night here has rocks in row 3, but the rule holds). |
| Lit ship at the map edge | Pinned; it stays put and is not wrecked. It can stay pinned until dawn. |
| Beam turns UP while a ship is mid-slide | The ship is unlit and moves south from its current tile that turn. |
| Ship starts in row 3 | It is judged like any ship: lit or not at its first move. |
| Ship reaches row 6 | Row 6 is only harbor or rock, so it docks or wrecks at once. |
| Wreck and dock on the same turn | Both are reported; the night is lost. |
| Last ship docks on turn 10 | Docking is resolved before the dawn check, so the night is **won**. |
| Command is not `L`, `R` or `H` | The build reports it and the night state does not change (the turn does not advance). |
| Script ends before the night ends | The build reports an unfinished night. |
| Commands after the night ends | Ignored, and reported as ignored. |

## 8. The nights

Each night has a starting aim, ships (start position and number) and a coast row. All other tiles are sea. In every night T stands at (3,3), the turn limit is 10, and ships and aim begin as shown. The drawings are first screens: tiles lit by the starting aim are drawn `~`, exactly as on every later screen (§2, §3). Nights 1 and 2 start with UP, so their first screens show no `~`. Commands are written turn by turn (the script syntax is defined in `repo/manual.md`).

### Night 1 — "First light" (teaches: slide a ship until it clears the rock, then let it go)

Start aim: UP. Ship 1 at (1,2). Coast row 6: `H######` (harbor only at (6,0)).

```
  0123456
0 .......
1 ..1....
2 .......
3 ...T...
4 .......
5 .......
6 H######
```

**Solution (won on turn 7):** `L H H H R H H`

| Turn | Command | Aim | Ship 1 |
|---|---|---|---|
| 1 | L | LEFT | (1,2) → (2,2) |
| 2 | H | LEFT | → (3,2) |
| 3 | H | LEFT | lit; slides to (3,1) |
| 4 | H | LEFT | lit; slides to (3,0) |
| 5 | R | UP | unlit; → (4,0) |
| 6 | H | UP | → (5,0) |
| 7 | H | UP | → (6,0), docked. **NIGHT WON** |

(`L` may also be given on turn 2 or 3 instead of turn 1; the ship is only judged when it reaches row 3.)

**Check scripts:**
- `H H H H H` ends in a loss on turn 5. Ship 1 goes (2,2), (3,2), (4,2), (5,2), (6,2) and is wrecked on a rock.
- `L H H R H H` ends in a loss on turn 6. Ship 1 slides only to (3,1), then goes (4,1), (5,1), (6,1) and is wrecked.
- `L` then `H` on every turn ends in **DAWN** at turn 10. Ship 1 slides to (3,0) on turn 4 and is pinned from turn 5 on.

### Night 2 — "Both sides" (teaches: the beam takes two turns to change sides, so plan the order)

Start aim: UP. Ship 1 at (2,2), ship 2 at (0,4). Coast row 6: `#H###H#` (harbor at (6,1) and (6,5)).

```
  0123456
0 ....2..
1 .......
2 ..1....
3 ...T...
4 .......
5 .......
6 #H###H#
```

**Solution (won on turn 7):** `H L R R L H H`

| Turn | Command | Aim | Ship 1 | Ship 2 |
|---|---|---|---|---|
| 1 | H | UP | → (3,2) | → (1,4) |
| 2 | L | LEFT | lit; slides to (3,1) | → (2,4) |
| 3 | R | UP | unlit; → (4,1) | → (3,4) |
| 4 | R | RIGHT | → (5,1) | lit; slides to (3,5) |
| 5 | L | UP | → (6,1), docked | unlit; → (4,5) |
| 6 | H | UP | (done) | → (5,5) |
| 7 | H | UP | (done) | → (6,5), docked. **NIGHT WON** |

**Check script:** `H H H H` ends in a loss on turn 4. Ship 1 goes (3,2), (4,2), (5,2) and is wrecked at (6,2).

### Night 3 — "Keep it dark" (teaches: lighting a ship you want to leave alone ruins it)

Start aim: RIGHT. Ship 1 at (2,1), ship 2 at (1,2), ship 3 at (0,5). Coast row 6: `H#H###H` (harbor at (6,0), (6,2), (6,6)).

```
  0123456
0 .....3.
1 ..2....
2 .1.....
3 ...T~~~
4 .......
5 .......
6 H#H###H
```

The starting aim is RIGHT, so (3,4), (3,5) and (3,6) are drawn `~` on the first screen. No ship stands there at turn 0, and lit status is judged only after the first command, so this changes no ship movement.

Ship 2 sits straight above a harbor and needs no beam. It must pass row 3 while the beam is UP.

**Solution (won on turn 7):** `L L R R L H H`

| Turn | Command | Aim | Ship 1 | Ship 2 | Ship 3 |
|---|---|---|---|---|---|
| 1 | L | UP | → (3,1) | → (2,2) | → (1,5) |
| 2 | L | LEFT | lit; slides to (3,0) | → (3,2) | → (2,5) |
| 3 | R | UP | unlit; → (4,0) | unlit; → (4,2) | → (3,5) |
| 4 | R | RIGHT | → (5,0) | → (5,2) | lit; slides to (3,6) |
| 5 | L | UP | → (6,0), docked | → (6,2), docked | unlit; → (4,6) |
| 6 | H | UP | (done) | (done) | → (5,6) |
| 7 | H | UP | (done) | (done) | → (6,6), docked. **NIGHT WON** |

**Check scripts:**
- `H H H H` ends in a loss on turn 4. Ship 1 goes (3,1), (4,1), (5,1), (6,1) and is wrecked. Ship 3 slides to (3,6) on the same turn.
- `L L H R H H` ends in a loss on turn 6.
  - Ship 1 is pinned at (3,0) on turn 3, then drops and docks at (6,0) on turn 6.
  - Ship 2 is lit on turn 3 and slides to (3,1), so it is wrecked at (6,1) on turn 6.
  - Ship 3 is not lit on turn 4, so it drops down column 5 and is wrecked at (6,5) on turn 6.

## 9. Acceptance criteria — verification (QA, by playing scripts)

- **AC-1 Start screen.** Each of Nights 1–3 can be started. Its first screen shows the 7×7 board exactly as in §8: coast row, ships, lighthouse at (3,3), row and column numbers, header, ship list and forecast line. The starting aim is as stated. The tiles lit by the starting aim are drawn `~` on the first screen, as AC-3 requires for every screen: Night 1 and Night 2 (UP) show no `~`, and Night 3 (RIGHT) shows `~` on (3,4)-(3,6). The header aim and the drawn lit tiles always agree.
- **AC-2 Commands.** The three commands behave as in §3: from UP, `L` gives LEFT and `R` gives RIGHT. From LEFT, `L` stays LEFT. From RIGHT, `R` stays RIGHT. `H` never changes the aim. Going LEFT to RIGHT takes two commands.
- **AC-3 Beam display.** Under LEFT the sea tiles (3,0)–(3,2) show `~`. Under RIGHT, (3,4)–(3,6) show `~`. Under UP no tile shows `~`. A ship on a lit tile still shows its digit.
- **AC-4 Unlit ships.** A ship not on a lit tile moves exactly one tile south per turn.
- **AC-5 Lit ships.** A lit ship does not move south. It slides one tile away from the lighthouse (west under LEFT, east under RIGHT) and stays in row 3.
- **AC-6 Edge.** A lit ship at column 0 under LEFT, or column 6 under RIGHT, stays where it is and is not wrecked.
- **AC-7 Fates.** Entering a harbor docks the ship. Entering a rock or the lighthouse wrecks it. Both outcomes are reported with the position.
- **AC-8 Winning.** The solution scripts of Nights 1, 2 and 3 each end in **NIGHT WON** on turn 7, with the ship positions in the tables.
- **AC-9 Losing.** Each failure script in §8 ends as stated: night, turn, which ships are wrecked and where.
- **AC-10 Dawn.** At the end of turn 10, ships still at sea mean the night is lost at dawn. This is checked by the Night 1 script `L` then `H` on every turn.
- **AC-11 Same-turn events.** When a ship docks and another is wrecked on the same turn, both are reported and the night is lost (the Night 3 script `L L H R H H`).
- **AC-12 Determinism.** The same script on the same night gives byte-identical output on every run.
- **AC-13 Invalid and unfinished input.** An unrecognized command is reported and leaves the state unchanged, and the turn counter does not advance. A script that ends early is reported as unfinished.
- **AC-14 Night end.** After a night ends, further commands are ignored and reported as ignored.
- **AC-15 Predictability.** From the first screen of any night, using only the rules in `repo/manual.md`, the position of every ship after each turn of the solution table can be derived. Each screen's forecast line gives the correct aim for each of `L`, `H`, `R`.

## 10. Acceptance criteria — experience signals (playtest and Review)

These are for the playtest and Review. They are not for QA verdicts.

- **E-1** A new player can say, before playing Night 1, which tile the ship will slide to if the beam is held for one turn and for two.
- **E-2** In Night 2, a player who gets stuck can say why: the beam cannot change sides in one turn. They do not blame luck.
- **E-3** After losing Night 3 by lighting the wrong ship, the player can explain what they did wrong and can name the turn at which they should have turned the beam off.
- **E-4** A first-time player finishes any night in under 5 minutes of reading and deciding.
- **E-5** Players describe the game as planning ahead, not as reacting.

## 11. Not in this spec (scope)

- No mid-night arrivals, no random events, no speed differences between ships, no extra rocks in the sea, no scoring beyond won/lost, no graphics.
- Script syntax, night selection and file layout are the build's to define in `repo/manual.md`.

## 12. Open questions

- **Non-blocking, for `game-director`:** Do you want ships to appear from the top mid-night in later nights, as the vision's "ships come in from the dark sea" might suggest? This first playable puts every ship on the board at turn 0 for readability. Adding arrivals would be a scope question I do not hold.
- **Non-blocking, for `game-director`:** Should a wreck lose the night at once (as specified), or should later nights allow losing some ships? This spec follows the vision: "let none hit the rocks".
>>>END

<<<FILE repo/manual.md
# Lamplight Keeper - Manual

You keep a lighthouse for one short night. Every turn you give one command
and turn the beam. Bring every ship into the harbor. None may hit the rocks.
Nothing is random: every ship's path can be worked out from the screen and
the rules below.

## Running

Run these from the `repo/` directory.

    python3 play.py SCRIPT            play a script and print what you see
    python3 play.py --trace SCRIPT    the same, plus a `[trace]` line after each screen

## Script format

A script is a plain text file of words separated by spaces or line breaks.

- The first word pair chooses the night: `night 1`, `night 2` or `night 3`.
- After it come commands, one word each, played in order, one per turn:
  `L`, `R` or `H` (capital letters only).
- Everything from `#` to the end of a line is a comment.

Example:

    night 1
    H H L   # three turns

What the script does:
- A word that is not `L`, `R` or `H` is reported as unrecognized and skipped. The turn does
  not advance and nothing changes.
- If the script ends before the night does, the output says the night is unfinished.
- Commands after the night has ended are ignored; each one is reported as ignored.
- A script without a valid `night N` start prints an error.

## The screen

    === Night 1 "First light" | Turn 1 of 10 | Beam: UP ===
      0123456
    0 .......
    ...
    6 H######
    Ships:
      Ship 1: (1,2)
    Forecast: L -> LEFT, H -> UP, R -> RIGHT

- The header gives the night, the turn (out of 10) and the current beam aim.
- The board is 7 columns by 7 rows. Rows are numbered down the left, columns
  across the top, both from 0. A position is written (row,col). Row 0 is the
  top (open sea); row 6 is the bottom (the coast).
- The ship list shows where each ship is, or `docked`, or where it was wrecked.
- The forecast line shows the beam aim each command would give from the current aim,
  always in the order `L`, `H`, `R` (for example `L -> LEFT, H -> UP, R -> RIGHT`).
- Tiles lit by the current beam aim are drawn `~` on every screen, including the first
  (Night 3 starts with the beam RIGHT, so its first screen shows `~` on (3,4)-(3,6)).

| Symbol | Meaning |
|---|---|
| `.` | Sea (dark) |
| `~` | Sea lit by the beam (only row 3 can be lit) |
| `#` | Rock. A ship that enters it is wrecked. |
| `H` | Harbor. A ship that enters it is docked (safe, removed from play). |
| `T` | The lighthouse, always at (3,3). A ship that enters it is wrecked. |
| `1`-`9` | A ship, drawn over `.` or `~`. If two ships share a tile, the lower number is drawn; the ship list names both. Ships never interact. |

The coast (row 6) holds only harbors and rocks. The lighthouse is in row 3,
the **beam row**.

## The beam

The beam has one of three aims:

- **LEFT** lights (3,0), (3,1) and (3,2) - the whole row to the left edge.
- **RIGHT** lights (3,4), (3,5) and (3,6).
- **UP** lights nothing.

Rocks and ships do not block the beam. The lighthouse tile (3,3) is never lit.

Commands, one per turn:

| Command | Effect |
|---|---|
| `L` | RIGHT becomes UP, UP becomes LEFT, LEFT stays LEFT |
| `R` | LEFT becomes UP, UP becomes RIGHT, RIGHT stays RIGHT |
| `H` | The aim does not change |

So going from LEFT to RIGHT (or back) takes two turns and passes through UP.

## A turn

1. The screen is shown.
2. You give a command. The aim changes; the lit tiles are those of the **new** aim.
3. Every ship still at sea moves at once, judged by the tile it stood on:
   - On a **lit** tile: it does not advance. It slides one tile along row 3
     away from the lighthouse: west (column - 1) under LEFT, east (column + 1)
     under RIGHT. A lit ship at column 0 under LEFT, or column 6 under RIGHT,
     cannot leave the map: it stays where it is (pinned), and is not wrecked.
   - On a **dark** tile: it moves one tile south (row + 1).
4. Each ship's new tile decides its fate: harbor means docked; rock or
   lighthouse means wrecked; sea means it stays at sea.
5. The screen reports what happened to each ship, with positions.
6. End of the turn:
   - If any ship was wrecked, the night is **lost** at once (all of that turn's
     events are still reported, including docks).
   - Otherwise, if every ship is docked, the night is **won**. This counts
     on turn 10 too.
   - Otherwise, if this was turn 10, **DAWN**: the night is lost with ships
     still at sea.
   - Otherwise the next turn begins.

All ships are on the board from the start; none arrive later. A ship on
any row other than row 3 simply moves south one tile per turn, because only
row 3 can be lit. A ship on row 3 is judged like any other: lit or not after
your command.

## Working out a ship's path

Take the ship's position from the ship list. For each turn, apply your command to the aim (or read it
off the forecast line), check whether the ship's tile is in the lit set, and
move it as above. Two turns of `H` under LEFT with a ship at (3,2), for
example, give (3,1) then (3,0), where it stays pinned until the beam moves away.

## Results

- `NIGHT WON on turn N.`
- `NIGHT LOST on turn N: ship X wrecked at (row,col).`
- `DAWN: ships still at sea ...`, naming the ships and where they are.
>>>END

<<<FILE decisions/D-001-beam-and-ship-rules.md
---
kind: decision
id: D-001
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-25
supersedes: none
---
# D-001: Lit ships slide along the beam row; the beam has three aims

## Decision

- The beam has three aims: LEFT, UP (lights nothing) and RIGHT. The commands `L`, `R` and `H` turn it one step or hold it, clamped at the ends.
- Only the lighthouse's row (row 3) can be lit.
- A ship on a lit tile does not advance south. It slides one tile along the row away from the lighthouse each turn it stays lit.
- A ship not on a lit tile moves one tile south.
- A wreck loses the night at once. A night has a 10-turn limit (dawn).

## Rationale

- The slide gives the player real control over how far a ship is pushed (one tile per held turn) and keeps everything predictable.
- UP as a neutral aim makes switching sides cost two turns, which gives planning depth with only three commands (Pillar 1).
- Every ship's path can be derived from the board and the rules (Pillar 2).
- Short nights of about 7 turns keep to Pillar 3.

## Alternatives considered

- **Beam pushes a ship back along its heading.** Ships would leave the map or stall, which is not "turned aside".
- **Two aims only (LEFT, RIGHT).** `L` and `R` would be redundant with `H` when already at an end, and switching sides would cost nothing, which loses the planning depth.
- **Diagonal rays from a lighthouse at the bottom.** Harder to read ahead from a character grid.
- **Ship-ship collisions as a loss.** This is a new mechanic beyond the vision, so ships pass through each other.

## Revisit when

- Playtests show the nights are too easy or too hard to read.
- Later nights need rocks in the beam row or mid-night arrivals (a scope question for `game-director`).
>>>END

<<<FILE goals/G-001-first-playable/14-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 14
from: playtester
to: studio
stage: Play
outcome: done
---
# 14: playtester → studio — observation report on the Lamplight Keeper first playable (nights 1–3)

## Task

Review the playtest observation report in Findings and route it. Experience issues go to `game-designer`, defects to `qa`.

## Context

I played the first playable as a new player, using only `repo/manual.md` and the screen output. The profile was a puzzle player who likes short, thinky sessions with readable rules and wants to plan rather than react. I did not read source, tests or design documents, and I did not use `--trace`.

## Findings

### Method

- I played with input scripts, run as `python3 play.py {script}`. There was no live play.
- I had three run rounds and used all of them. The output arrived as run results, and everything below comes from those outputs and the manual.
- I cannot observe real-time pacing or my own attention over time. Where I describe feel, it is inferred from the screens and the number of turns.

### Scripts tried, in order

Round 1:
1. Night 1, `H H H`. The ship drifted straight down and the script ended at turn 4. The output said the night was unfinished.

Round 2:
2. Night 1, `H H L H R H H`. **Won on turn 7.**
3. Night 1, ten times `H`. **Lost on turn 5.** The ship sank to (6,2), which is a rock. Five more `H` were reported as "Ignored (the night is over)".
4. Night 2, `H`. I only looked at the opening. The script ended at turn 2.
5. Night 3, `H`. I only looked at the opening. The script ended at turn 2.

Round 3:
6. Night 2, `H L R R L H H`. **Won on turn 7.**
7. Night 3, `L L R R L H H`. **Won on turn 7.**
8. Night 3, six times `H`. **Lost on turn 4.** Ship 1 sank onto a rock at (6,1), while ship 3 slid east to (3,6).

### What happened and how it felt, by night

**Night 1 "First light" (one ship)**
- The first screen showed the ship at (1,2) and the harbor at the far left of the coast (6,0). The rest of the coast is rock.
- Doing nothing wrecks the ship on a rock, so the puzzle is to steer the ship sideways to column 0.
- The rule that a lit ship slides away from the lighthouse made sense once I read the manual. Planning was easy: the ship arrives at row 3, you light it, and it slides west.
- The solution came on the first real attempt. It worked as the manual predicts, and I could work out the whole path before running it. That is pleasing for a thinky player, but it is a very small puzzle with almost nothing to weigh. It reads as a tutorial.
- The "do nothing" run showed clearly why the ship dies. The wreck message gave the position, so the cause was readable.

**Night 2 "Both sides" (two ships)**
- Harbors sit at columns 1 and 5, with rock at column 0, columns 2–4 and column 6. Ship 1 at (2,2) must go one tile west, and ship 2 at (0,4) one tile east.
- The new idea is that the beam can only point one way at a time, so the two ships must reach row 3 at different times and the beam has to swing between sides. The swing passes through UP.
- My solution used `L R R L` around the middle turns. I could plan it on paper from the opening screen, and the result matched my plan.
- It felt like a real step up from night 1, but still gentle.
- I did not run a failing script for night 2, so I have not seen how it loses.

**Night 3 "Keep it dark" (three ships)**
- It starts with the beam already RIGHT, so (3,4)–(3,6) are lit on the first screen.
- Harbors are at columns 0, 2 and 6, with rock at column 1. Ship 1 starts at column 1 and needs a west slide. Ship 2 at column 2 must pass through row 3 while it is dark. Ship 3 needs an east slide.
- The title and the lit start made me think about when a ship is lit, and that is the interesting part: lighting the wrong ship at the wrong time ruins it.
- The forecast line was useful here (`L -> UP, H -> RIGHT, R -> RIGHT`). It showed that pressing `L` from RIGHT only gets to UP.
- My win script came out of working through the three ships' timings. It felt like the best of the three nights.
- The "do nothing" run lost at turn 4, earlier than night 1's, and the loss was easy to read.

### Clear
- The forecast line, the lit `~` tiles and the per-turn "moved south / lit, slid west" messages made every move explainable. I never had to guess why something happened.
- A win or loss is stated plainly: "NIGHT WON on turn N" or "NIGHT LOST on turn N: ship X wrecked at (row,col)".
- Nothing is random. My predictions matched the outcome every time.

### Confusing or friction (all low impact)
- **Duplicate final screen (low).** After the last move the screen is printed again with the same turn number, for example "Turn 7 of 10" twice. It was briefly unclear whether a new turn had begun.
- **No hint on first attempts (low).** A first script such as `H H H` ends as "unfinished" with no sense of whether you were doing well. You have to read the manual's note about row 3 and the harbors to know where to aim.
- **Scripts instead of live play (low).** Writing the whole sequence blind at first, before seeing the effect of each command, is more like planning on paper. That suits a planner, but it removes the feedback of live play.
- **Short nights (medium).** Winning took 7 of the 10 turns on all three nights. Nights 1 and 2 felt over quickly and did not make me think hard; night 3 was the first with real decisions. I saw only one winning line per night and cannot say whether others exist.

### Positives
- The rules are readable, and the planning worked as promised.
- Night 3 is the first night with a real trade-off.
- Each night adds one idea to the last: slide, two sides, keep one ship dark.

### Not observed
- **DAWN:** no loss by running out of turns.
- **Pinned ships:** a ship stuck at column 0 or 6 under the beam.
- **Overlapping ships:** two ships sharing a tile.
- **Unrecognized words:** the "skipped" behaviour for a bad command.
- **Error cases:** a script with no `night N` start.
- **Night 2 failing:** no failing script for this night.
- **Other solutions:** I tried one winning script per night. I cannot say whether any night has a shorter or alternative solution.
- **Feel:** real-time pacing and long-session feel are not observable with this method.

### Open player questions
- Is there a reason to win in fewer turns, since the result only says "won on turn N"?
- Do later nights exist beyond these three?

## Decisions already made

None.

## Constraints

- This is observable experience only, with no prescribed fixes.
- Nothing in the build or project was edited.

## Open questions

None for the sender. The Studio decides where to route the experience observations (`game-designer`) and the duplicate-final-screen note (`qa` if treated as a defect).

## Expected output

Studio routes this report: experience observations to `game-designer`, any defect candidates to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile; repo/manual.md
- Decisions: none
- Previous handoff: goals/G-001-first-playable/13-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-first-playable/12-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 12
from: qa
to: studio
stage: Verify
outcome: pass
---
# 12: qa → studio — verification of the first playable against AC-1..AC-15: pass

## Task

Route the verified first playable onward to the Playtester step. This report is the verification record. The Playtester handoff should carry the build and the experience signals (E-1..E-5), not this verification history.

## Context

Goal G-001: first playable of Lamplight Keeper. QA verified `repo/` against AC-1..AC-15 in `design/first-playable.md`, using the spec, `repo/manual.md` and observed play output. No implementer reasoning was used. All run rounds were used. Scripts played: n3-same-turn-invalid, n2-solution-extra, n3-solution, n1-dawn, n1-solution, n2-all-hold, n3-all-hold. The unit suite also ran: 31 tests, OK. The suite is not counted as verification evidence on its own.

## Findings

**Overall verdict: pass.** No defects were found: no regressions, no spec mismatches, no severity-bearing failures.

### Per-criterion results

| AC | Result | Evidence |
|---|---|---|
| AC-1 Start screen | pass | First screens of Night 1 (n1-solution), Night 2 (n2-all-hold) and Night 3 (n3-solution) match §8 exactly: coast rows, ships, `T` at (3,3), row and column numbers, header, ship list, forecast line. Night 1 and 2 show UP with no `~`. Night 3 shows RIGHT with `~` on (3,4)-(3,6) and forecast `L -> UP, H -> RIGHT, R -> RIGHT`. |
| AC-2 Commands | pass (partly by code reading) | Observed in play: UP+L→LEFT, UP+R→RIGHT, LEFT+R→UP, RIGHT+L→UP, H never changes the aim. LEFT to RIGHT took two commands in the Night 2 solution (R, then R). The clamps (LEFT+L stays LEFT, RIGHT+R stays RIGHT) were not played as a command. They show in the forecast lines (`L -> LEFT` under LEFT, `R -> RIGHT` under RIGHT) and in `next_aim` (index clamp). |
| AC-3 Beam display | pass | LEFT shows `~~~T...`, RIGHT shows `...T~~~`, UP shows no `~`. A ship on a lit tile shows its digit (`~~1T...`, `1~~T...`, `...T~2~`). The header aim always matches the drawn tiles. |
| AC-4 Unlit ships | pass | Every unlit ship moved exactly one tile south in all plays. |
| AC-5 Lit ships | pass | Lit ships slid west under LEFT and east under RIGHT, staying in row 3 (e.g. (3,2)→(3,1)→(3,0); (3,4)→(3,5); (3,5)→(3,6)). |
| AC-6 Edge | pass (right edge by code reading) | Left edge: ship pinned at (3,0) under LEFT and not wrecked (n1-dawn turns 5-10, n3-same-turn turn 3). The right-edge pin was not reached in the played scripts. The code path is symmetric (`nc` outside 0..6 keeps the position). |
| AC-7 Fates | pass (lighthouse wreck by code reading) | Harbor: `DOCKED at (6,0)`, `(6,1)`, `(6,5)`, `(6,6)`, `(6,2)`. Rock: `WRECKED at (6,2)`, `(6,1)`, `(6,5)`. All are reported with positions. No night script can send a ship into the lighthouse, because ships start off column 3 and only slide away from it. The `T` branch is the same code as the rock branch. |
| AC-8 Winning | pass | Solution scripts for Nights 1, 2 and 3 each ended `NIGHT WON on turn 7.` with every ship position matching the §8 tables, turn by turn. |
| AC-9 Losing | pass (two Night 1 scripts derived) | Played: Night 2 `H H H H` (lost turn 4, ship 1 at (6,2)). Night 3 `H H H H` (lost turn 4, ship 1 at (6,1); ship 3 slid to (3,6) the same turn). Night 3 `L L H R H H` (lost turn 6, ships 2 at (6,1) and 3 at (6,5); ship 1 docked). The Night 1 scripts `H H H H H` and `L H H R H H` were not played in the rounds. Tracing them through the code gives the §8 results: wrecked at (6,2) on turn 5 and at (6,1) on turn 6. The unit tests assert both. |
| AC-10 Dawn | pass | `L` then `H`×9: at turn 10 the output was `DAWN: ships still at sea (NIGHT LOST at turn 10): ship 1 at (3,0).` Ship 1 was pinned from turn 5. |
| AC-11 Same-turn events | pass | Night 3 `L L H R H H` turn 6 reported ship 1 DOCKED, ship 2 WRECKED and ship 3 WRECKED. The night was lost and both wrecks were named in the result line. |
| AC-12 Determinism | pass (by inspection) | The code has no randomness, clock or unordered iteration (ships are iterated sorted). No script was played twice in the rounds, so byte-identical repeat output was not directly observed. The unit test `test_deterministic` compares two runs. |
| AC-13 Invalid and unfinished input | pass (unfinished by code reading) | Script `L L H X R H H Z`: `Unrecognized command 'X': ignored. Turn 4 is unchanged`, and the next line was `> Turn 4 command: R`, so the turn did not advance and the state was unchanged. No script ended early in the rounds. The code appends `SCRIPT ENDED: the night is unfinished at turn N of 10.` whenever the night is not over. |
| AC-14 Night end | pass | `Ignored (the night is over): Z` after the Night 3 loss. `Ignored (the night is over): H` after the Night 2 win. |
| AC-15 Predictability | pass | The manual's rules (aim change, lit set of the new aim, slide or south, fate by tile) reproduce every ship position in the played solution tables. The forecast line was correct on every observed screen (UP: `LEFT, UP, RIGHT`; LEFT: `LEFT, LEFT, UP`; RIGHT: `UP, RIGHT, RIGHT`), always in the order L, H, R. No place was found where a player following the manual would be misled or stuck. |

### Evidence limits

- This step could not play more scripts. Not played in the rounds: Night 1 failure scripts, an early-ending script, a same-script repeat, a right-edge pin, and `L` at LEFT or `R` at RIGHT as actual commands. Each is marked above as verified by code reading, with the unit tests agreeing. The Studio may add these plays in a later round if it wants direct play evidence.
- `--trace` was not run, and no criterion needs it.
- The manual does not say whether `night` is case-sensitive. The build rejects anything other than the lowercase `night N`. This is minor and not a failure of any AC.

### Spec gaps, design questions, regressions

- No spec gaps affected any verdict.
- No concrete player-facing trouble was observed in mid-night arrivals or in wreck-loses-night, so nothing is raised for Review.
- Regressions: none seen. The unit suite (31 tests) is green.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Treated as intended behavior.
- The first screen of a night draws `~` under the starting aim (spec amended). Treated as intended behavior.

## Constraints

- QA did not edit the build, the design or the Decisions.
- The build was run only through the project's commands.
- The Playtester step must be composed without this verification history. Pass it the manual, the build and E-1..E-5 only.

## Open questions

None.

## Expected output

Studio routes to the Playtester step (experience signals E-1..E-5), composing that handoff without the contents of this report. No fix work is needed, so there is nothing for `gameplay-engineer` or `game-designer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/first-playable.md; repo/manual.md; project.md#constraints
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/11-studio-to-qa.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable/16-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
