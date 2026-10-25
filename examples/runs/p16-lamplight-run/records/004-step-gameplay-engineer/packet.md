# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-first-playable/03-studio-to-gameplay-engineer.md
next_seq: 4
runs: tests, trace (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable/04-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-001-first-playable/03-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 3
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 03: studio → gameplay-engineer — build the first playable from the design spec

## Task

Build Lamplight Keeper's first playable in `repo/` exactly as specified in `design/first-playable.md`: `play.py`, the game code, the three nights, tests, and `repo/manual.md`. Define the script format yourself and document it in the manual.

## Context

Goal G-001: the Owner asked (ja) "このコンセプトで、遊べる最初の版を作ってほしい". Design is done; the spec was written without a build and its solutions were only hand-simulated. `repo/` holds only a README. Plan was skipped as the scope is small and standard-library only.

## Findings

Spec summary (the spec is authoritative; read it in full):
- 7×7 board, lighthouse at (3,3), coast in row 6 made of harbor and rock tiles. All ships are on the board at turn 0.
- Beam aims: LEFT, UP (lights nothing), RIGHT. Commands `L`, `R`, `H`, clamped at the ends; changing sides takes two turns.
- Only row 3 can be lit. A lit ship does not advance; it slides one tile away from the lighthouse (pinned at the map edge, not wrecked). An unlit ship moves one tile south.
- Harbor docks a ship; a rock or the lighthouse wrecks it; any wreck loses the night. Turn limit 10 (dawn) loses with ships still at sea.
- Required screen content: grid, row/column numbers, ship list, forecast line, `~` for lit tiles, dock/wreck reports with position (spec §2, §6).
- Three nights with intended winning solutions (win on turn 7): Night 1 `L H H H R H H`; Night 2 `H L R R L H H`; Night 3 `L L R R L H H`. The spec also has failure scripts that must lose as stated.
- Acceptance criteria AC-1..AC-15 are in spec §9. They cover: first screen, aim changes, lit tiles, ship movement, edge pinning, dock/wreck reports, the solutions and failure scripts, dawn loss, same-turn dock and wreck, determinism, invalid commands and short scripts, commands after the end, and deriving positions from screen plus manual.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit.

## Constraints

- Python 3, standard library only; text output; deterministic; played through input scripts only (no live input).
- Commands to support: `python3 play.py {script}`, `python3 play.py --trace {script}` (adds internal state), `python3 -m unittest discover -s tests` (run from `repo/`).
- `repo/manual.md` ships with the build and is all a player is told. It must give the rules (spec §3–§4), the symbols (§2) and the script format, and must let a player derive ship positions (AC-15). It must not reveal solutions.
- Add no mechanics beyond the spec. If the spec is ambiguous, contradictory or missing a case, stop and hand back to `game-designer` (via `studio`); do not decide it yourself.
- Tests should cover the spec's solutions and failure scripts, and the AC items that can be tested automatically.

## Open questions

None for you. The designer's questions (mid-night arrivals, wreck always losing) are for `game-director` at Review.

## Expected output

The built `repo/` with passing tests, and build notes in your outgoing Handoff: files created, script format, how to run, test results, any spec deviations or ambiguities, and anything you could not check. Address the result to `studio` (the next step is QA, which must receive a Handoff composed from permitted information only).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/first-playable.md; project.md#constraints; repo/README.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/02-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).
- The change is not finished but nothing is missing → `outcome: partial`, saying what is done and
  what remains (not `question`).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
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

Each night has a starting aim, ships (start position and number) and a coast row. All other tiles are sea. In every night T stands at (3,3), the turn limit is 10, and ships and aim begin as shown. Commands are written turn by turn (the script syntax is defined in `repo/manual.md`).

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
3 ...T...
4 .......
5 .......
6 H#H###H
```

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

- **AC-1 Start screen.** Each of Nights 1–3 can be started. Its first screen shows the 7×7 board exactly as in §8: coast row, ships, lighthouse at (3,3), row and column numbers, header, ship list and forecast line. The starting aim is as stated.
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

<<<FILE project.md#constraints
## Constraints

- The build is a Python 3 program using the standard library only, in `repo/`.
- It is played through input scripts, with no live input: `run_play` (`python3 play.py {script}`)
  plays a script and prints what the player sees, `run_trace` adds the internal state, and
  `run_tests` runs the build's tests. The script format is the build's to define, in
  `repo/manual.md`, which ships with the build and is all a player is told.
- Text output only (a grid of characters per turn); no graphics yet.
- Deterministic: the same script always gives the same night.
>>>END

<<<FILE repo/README.md
# Lamplight Keeper build

Empty: the first playable build goes here (see `../project.md`, Constraints).
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

<<<FILE goals/G-001-first-playable/02-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 2
from: game-designer
to: studio
stage: Routing (Plan or Build next)
outcome: done
---
# 02: game-designer → studio — first-playable design spec is ready for routing

## Task

Route the work to Plan or Build. The design spec `design/first-playable.md` is finished and needs an engineer to build it and QA to verify it.

## Context

Goal G-001: the Owner asked (ja) "このコンセプトで、遊べる最初の版を作ってほしい". Handoff 01 asked the game-designer for a player-observable spec of the first playable. This is that spec. `repo/` holds only a README; no build exists yet.

## Findings

**Design index (for the Owner's `project.md`; I did not edit it):**
- `design/first-playable.md`: rules, parameters, edge cases, three nights with solutions, acceptance criteria.
- `decisions/D-001-beam-and-ship-rules.md`: the beam and ship-movement rules.

**Rules in short**
- The board is 7×7. The lighthouse is at (3,3). The coast is row 6, made of harbor and rock tiles.
- Ships are all on the board at turn 0.
- The beam has three aims: LEFT, UP (lights nothing) and RIGHT. Commands are `L`, `R` and `H`, clamped at the ends. Changing sides takes two turns.
- Only row 3 can be lit. A lit ship does not advance; it slides one tile away from the lighthouse. An unlit ship moves one tile south. A lit ship at the map edge stays put.
- Harbor docks a ship. A rock or the lighthouse wrecks it. Any wreck loses the night. The turn limit is 10 (dawn).

**The three nights** (each with a solution that wins on turn 7, plus check scripts that lose)
- Night 1 "First light": 1 ship, solution `L H H H R H H`.
- Night 2 "Both sides": 2 ships, solution `H L R R L H H`.
- Night 3 "Keep it dark": 3 ships, solution `L L R R L H H`.

**Acceptance criteria (verification, AC-1 to AC-15; the full text is in the spec §9)**
- AC-1: the first screen of each night matches the layout.
- AC-2: `L`, `R` and `H` change the aim as specified, and switching sides takes two turns.
- AC-3: lit tiles are drawn `~` correctly.
- AC-4: an unlit ship moves one tile south per turn.
- AC-5: a lit ship slides one tile away from the lighthouse and stays in row 3.
- AC-6: a lit ship at the map edge is pinned, not wrecked.
- AC-7: dock and wreck are reported with the position.
- AC-8: the three solutions win on turn 7 with the tabled positions.
- AC-9: the failure scripts lose as stated.
- AC-10: dawn at turn 10 loses with ships still at sea.
- AC-11: a dock and a wreck on the same turn are both reported, and the night is lost.
- AC-12: the same script gives identical output every run.
- AC-13: an invalid command is reported without advancing the turn, and a script that ends early is reported.
- AC-14: commands after the night ends are ignored and reported.
- AC-15: ship positions can be derived from the screen and the manual, including a correct forecast line.

**Experience signals (E-1 to E-5, playtest and Review only):**
- E-1: a new player can predict how far a held beam pushes the ship in Night 1.
- E-2: a stuck player in Night 2 can name the cause, not luck.
- E-3: after losing Night 3, the player can explain the mistake.
- E-4: a night takes under 5 minutes to decide.
- E-5: players describe the game as planning, not reacting.

**Limits of what I could do:** I had no build, so I could not run `play.py`. I simulated every solution and failure script by hand, turn by turn, in the spec's tables. QA should confirm them against the build.

## Decisions already made

- D-001 (accepted, game-designer): three beam aims, lit ships slide along the beam row, a wreck loses the night at once, and there is a 10-turn limit.

## Constraints

- Python 3 standard library only, text output, deterministic, played through input scripts with no live input.
- The script format and `repo/manual.md` are the build's to define. The manual must tell the player the rules in §3–§4 and the symbols in §2.
- Do not add mechanics beyond the spec. Row and column numbers, the ship list and the forecast line are required screen content (spec §6).

## Open questions

- For `game-director`, non-blocking: do you want mid-night ship arrivals in later nights? This version places every ship on the board at turn 0. Adding arrivals would be a scope question.
- For `game-director`, non-blocking: should a wreck always lose the night at once? The spec follows the vision's "let none hit the rocks".

## Expected output

Route to Build (an engineer builds `repo/` and `repo/manual.md` from `design/first-playable.md`), then QA against AC-1 to AC-15. Plan looks unnecessary: the scope is small, standard-library only, and has no cross-system risk.

## Sender assessment

- The spec is complete for a first playable. All three solutions were hand-simulated and are consistent with the rules.
- Confidence is high on rule consistency and medium on balance, since nothing has been played yet. The experience signals are for the playtest.
- If the engineer finds an ambiguity, it should come back as a spec question to the game-designer.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/first-playable.md; project.md#constraints
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/01-studio-to-game-designer.md
>>>END

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/README.md
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

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable/04-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
