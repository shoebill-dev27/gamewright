# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-playable/05-studio-to-game-designer.md
next_seq: 6
runs: play (up to 3 rounds)
run_play: python3 play.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable/06-game-designer-to-<recipient>.md
- design/<name>
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

<<<FILE goals/G-001-first-playable/05-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — settle the first-screen display of Night 3

## Task

Decide whether the first screen of Night 3 shows `~` on (3,4)-(3,6) (the starting aim is RIGHT), and amend `design/first-playable.md` so that §8, §2, AC-1 and AC-3 no longer contradict each other.

## Context

Goal G-001: first playable of Lamplight Keeper. The engineer built the game from your spec (`repo/`). One contradiction came up during Build:
- Night 3 starts with aim RIGHT. §8 draws its first screen with no `~` (`3 ...T...`).
- AC-3 and §2 say that under RIGHT the tiles (3,4)-(3,6) show `~`.
- AC-1 says the first screen shows the board "exactly as in §8".

It changes no ship movement (lit status is judged after the first command), only what the first Night 3 screen looks like.

## Findings

Engineer's options (see handoff 04):
- (a) Draw `~` under the starting aim. This matches AC-3 and every later screen. The §8 drawing is then layout only. The engineer proposes this and has provisionally built it.
- (b) Draw the first screen with no `~` until a command has been given. This matches the §8 drawing literally, but the lit state would disagree with the aim shown in the header, so say how the first-screen lit state should be shown.

Studio note: the question is yours (player-facing behavior). Pick the option that best serves pillar 2 (readable ahead); (a) looks consistent with it, but the choice is yours.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Not reopened.

## Constraints

- Change only what resolves this contradiction; no new mechanics, no changes to the other nights' behavior.
- Do not change the code. The engineer applies your answer in the next Build step.
- Stay within the vision and D-001. If the answer would need a direction choice, say so and hand back.
- Do not take up the two Review questions (mid-night arrivals, wrecks always losing the night): they remain for `game-director`.

## Open questions

- Option (a) or (b) for the first screen of Night 3? State the final wording of AC-1 / §8 so QA can check it.

## Expected output

Amend `design/first-playable.md` in place and write a handoff to `studio` with the decision stated in one sentence and the exact amended sections. The Studio then routes to `gameplay-engineer` to apply it, fix the failing tests and rebuild.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/first-playable.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/04-gameplay-engineer-to-studio.md
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

<<<FILE goals/G-001-first-playable/04-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 4
from: gameplay-engineer
to: studio
stage: Routing (spec question to game-designer; QA after it is resolved)
outcome: question
---
# 04: gameplay-engineer → studio — first playable built; one spec contradiction to settle before QA

## Task

Route the open spec question below to `game-designer`. When it is answered, route the build to `qa` (against AC-1..AC-15). Nothing is delivered to QA yet.

## Context

Goal G-001: build Lamplight Keeper's first playable from `design/first-playable.md` (handoff 03). The build is written in `repo/`. All of it is unblocked except one small display question; applying either answer is a one-line change.

## Findings

**Files created (all in `repo/`):**
- `play.py`: entry point.
- `lamplight.py`: game logic, the night data and the script parser.
- `tests/test_game.py`: unit tests.
- `manual.md`: rules, symbols, script format. It has no solutions.
- `README.md`: updated.

**Script format** (defined in `manual.md`):
- Whitespace-separated words. The first two are `night N` (N = 1, 2 or 3).
- Then commands `L`, `R`, `H` (capitals only), one per turn.
- `#` starts a comment to the end of the line.
- Choices of mine inside the spec's "build's to define": a non-command word is reported and skipped; capital letters are required, so `l` counts as unrecognized; a missing `night N` header gives an error and exit code 2.

**How to run** (from `repo/`):
- `python3 play.py SCRIPT`
- `python3 play.py --trace SCRIPT`: adds a `[trace]` line (turn, aim, lit tiles, ship positions, docked, wrecked, status) after every screen.
- `python3 -m unittest discover -s tests`

**Output shape:**
- Each turn shows the header, the board with row and column numbers, the ship list, and the forecast line.
- After a command, the turn's event lines follow, each with positions (slid west or east, moved south, pinned, DOCKED or WRECKED at a position).
- At the end of the night it prints the final board and ship list, then `NIGHT WON on turn N.`, `NIGHT LOST on turn N: ship X wrecked at (r,c).` or `DAWN: ships still at sea ...`.
- Ignored and unrecognized commands, and an unfinished script, are each reported on their own line.

**Tests:** they cover the first screens of all three nights, the aim transitions, `~` display, the three solutions with the position tables, all failure scripts (including dawn and the same-turn dock and wreck), a dock on turn 10 winning, pinning at both edges, determinism, invalid and short scripts, commands after the end, header errors and the trace output. Results are in the Build check below. I could not run anything myself.

**Spec contradiction (blocking the delivery to QA):**
- Night 3 starts with aim RIGHT. §8 draws its first screen with no `~` (`3 ...T...`). AC-3 and §2 say that under RIGHT, (3,4)-(3,6) show `~`, and AC-1 says the first screen shows the board "exactly as in §8".
- It does not change any ship's movement, because lit status is judged after the first command. It only changes the first Night 3 screen.
- Options:
  - (a) Draw `~` under the starting aim. This matches AC-3 and the screen of every later turn. The §8 drawing is then layout only.
  - (b) Draw the first screen with no `~` until a command has been given. This matches the §8 drawing literally, but the lit state would then disagree with the aim shown in the header.
- Cost of either is one constant, `DRAW_LIT_ON_FIRST_SCREEN` in `repo/lamplight.py`. It is currently `True` (option a) so the build runs, but this is provisional until the designer decides. The tests do not depend on it.
- Proposed default: (a), with the designer amending the §8 drawing or AC-1 wording.

**Not checked:** the E-1..E-5 signals (playtest only), and whether the manual alone is enough to derive positions (AC-15), which QA must judge. I did not check how the output looks to a first-time player.

**Other deviations:** none. No mechanics were added.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Implemented as written.

## Constraints

- Python 3 standard library only, text output, deterministic, input scripts only.
- QA must receive this handoff without the Sender assessment, and the manual is all a player is told.
- Do not apply the open-question answer in the code without the designer's decision (the current value is provisional).

## Open questions

- For `game-designer`: should the first screen of Night 3 draw `~` on (3,4)-(3,6), since the starting aim is RIGHT (option a, proposed), or not (option b)? If (a), amend the §8 Night 3 drawing or AC-1. If (b), say how the first-screen lit state should be shown.
- Non-blocking, for `game-director` at Review: the designer's questions on mid-night arrivals and on wrecks always losing the night.

## Expected output

Studio routing (done in Route after seq 4): the display question went to `game-designer` (05). Then `gameplay-engineer` applies the answer, fixes the failing tests reported in the Build check (4 failures, e.g. forecast order `L, R, H` in the build against `L, H, R` in the tests) and reports a green `run_tests`. Only then does the build go to `qa`, with that Build handoff minus Sender assessment.

## Sender assessment

- All three solutions and every failure script in §8 were re-derived by hand against the implemented rules while writing the tests, and they agree with the spec's tables. This is not a substitute for the runtime result.
- Confidence is high on rule logic, medium on the tests until the Build check is read, since I never executed the code.
- The risk is a typo in the test expectations (for example the exact screen strings), not in the rules.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 1 (0.0 s).

```text
\n4 .......\n5 .......\n6 H######\nShips:\n  Ship 1: (1,2)\nForecast: L -> LEFT, R -> RIGHT, H -> UP\n> Turn 1 command: L\n  Ship 1 moved south (1,2) -> (2,2).\n=== Night 1 "First light" | Turn 2 of 10 | Beam: LEFT ===\n  0123456\n0 .......\n1 .......\n2 ..1....\n3 ~~~T...\n4 .......\n5 .......\n6 H######\nShips:\n  Ship 1: (2,2)\nForecast: L -> LEFT, R -> UP, H -> LEFT\nSCRIPT ENDED: the night is unfinished at turn 2 of 10.\n'

======================================================================
FAIL: test_night1 (test_game.StartScreens)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 30, in test_night1
    self.assertIn("Forecast: L -> LEFT, H -> UP, R -> RIGHT", out)
AssertionError: 'Forecast: L -> LEFT, H -> UP, R -> RIGHT' not found in '=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===\n  0123456\n0 .......\n1 ..1....\n2 .......\n3 ...T...\n4 .......\n5 .......\n6 H######\nShips:\n  Ship 1: (1,2)\nForecast: L -> LEFT, R -> RIGHT, H -> UP\nSCRIPT ENDED: the night is unfinished at turn 1 of 10.\n'

======================================================================
FAIL: test_night3_ships_and_coast (test_game.StartScreens)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 44, in test_night3_ships_and_coast
    self.assertIn("Forecast: L -> UP, H -> RIGHT, R -> RIGHT", out)
AssertionError: 'Forecast: L -> UP, H -> RIGHT, R -> RIGHT' not found in '=== Night 3 "Keep it dark" | Turn 1 of 10 | Beam: RIGHT ===\n  0123456\n0 .....3.\n1 ..2....\n2 .1.....\n3 ...T~~~\n4 .......\n5 .......\n6 H#H###H\nShips:\n  Ship 1: (2,1)\n  Ship 2: (1,2)\n  Ship 3: (0,5)\nForecast: L -> UP, R -> RIGHT, H -> RIGHT\nSCRIPT ENDED: the night is unfinished at turn 1 of 10.\n'

----------------------------------------------------------------------
Ran 30 tests in 0.004s

FAILED (failures=4)
```

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/first-playable.md; repo/manual.md; repo/play.py; repo/lamplight.py; repo/tests/test_game.py
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/03-studio-to-gameplay-engineer.md
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

- Write the outgoing Handoff as goals/G-001-first-playable/06-game-designer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
