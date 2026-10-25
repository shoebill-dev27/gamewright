# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-first-playable/11-studio-to-qa.md
next_seq: 12
runs: tests, play, trace (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py {script}
run_trace: python3 play.py --trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable/12-qa-to-<recipient>.md
- @run/<tests|play|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-001-first-playable/11-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 11
from: studio
to: qa
stage: Verify
outcome: routed
---
# 11: studio → qa — verify the first playable against AC-1..AC-15

## Task

Verify the current build in `repo/` against acceptance criteria AC-1..AC-15 in `design/first-playable.md`, by playing input scripts and checking the player-visible output. Give a pass/fail verdict per criterion and an overall verdict, with severity for any failure.

## Context

Goal G-001: the Owner asked for a first playable version of Lamplight Keeper (a short, turn-based lighthouse puzzle game). The build is a standard-library Python 3 program in `repo/`, played through input scripts. The build is complete for this Goal's scope; the project's own test suite is green (31 tests). Tests are not a substitute for your own verification.

## Findings

None to hand over. Verify from the spec, the acceptance criteria and the build, not from any account of how the build works.

## Decisions already made

- D-001 (`decisions/D-001-beam-and-ship-rules.md`): three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Treat as the intended behavior.
- The first screen of a night draws `~` under the starting aim (spec amended). Treat the spec as it stands in `design/first-playable.md`.

## Constraints

- Run the build only through the project's commands: `python3 play.py {script}` (player view), `python3 play.py --trace {script}` (adds internal state), `python3 -m unittest discover -s tests`.
- Player-facing behavior must be derivable from `repo/manual.md` alone; note any place where a player following the manual would be misled or stuck (relevant to AC-15).
- Deterministic: the same script must always give the same night; check repeat runs.
- Do not edit the build, the design or the Decisions. Report defects; do not fix them.
- Anything the spec leaves undefined: report it as undefined, do not decide it.

## Open questions

- None for this step. Design questions that are not defects (mid-night arrivals, whether a wreck always loses the night) are reserved for the later Review; mention them only if you observe concrete player-facing trouble.

## Expected output

A verification report in your outgoing Handoff: a pass/fail verdict for each of AC-1..AC-15 with the script or evidence used, regressions or other defects found with severity and reproduction scripts, and an overall `pass` or `fail`. Address the result to `studio` (the Playtester step that follows must be composed without verification history).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/first-playable.md; repo/manual.md; repo/play.py; repo/lamplight.py; repo/tests/test_game.py; project.md#constraints
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: none (the incoming implementation handoff holds the implementer's reasoning, which QA does not receive)
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

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
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

<<<FILE repo/play.py
"""Lamplight Keeper - play an input script.

Usage: python3 play.py [--trace] SCRIPT
"""
import sys

from lamplight import run_script


def main(argv):
    args = argv[1:]
    trace = False
    if args and args[0] == "--trace":
        trace = True
        args = args[1:]
    if len(args) != 1:
        sys.stderr.write("usage: python3 play.py [--trace] SCRIPT\n")
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.stderr.write("cannot read script: %s\n" % e)
        return 2
    out, code = run_script(text, trace)
    sys.stdout.write(out)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
>>>END

<<<FILE repo/lamplight.py
"""Lamplight Keeper - first playable game logic (standard library only)."""

GRID = 7
LIGHTHOUSE = (3, 3)
BEAM_ROW = 3
TURN_LIMIT = 10
AIMS = ("LEFT", "UP", "RIGHT")
# Order of commands in the forecast line: L, H, R.
COMMANDS = ("L", "H", "R")

NIGHTS = {
    1: {"name": "First light", "aim": "UP",
        "ships": {1: (1, 2)}, "coast": "H######"},
    2: {"name": "Both sides", "aim": "UP",
        "ships": {1: (2, 2), 2: (0, 4)}, "coast": "#H###H#"},
    3: {"name": "Keep it dark", "aim": "RIGHT",
        "ships": {1: (2, 1), 2: (1, 2), 3: (0, 5)}, "coast": "H#H###H"},
}


def fmt(pos):
    return "(%d,%d)" % pos


def next_aim(aim, cmd):
    i = AIMS.index(aim)
    if cmd == "L":
        i = max(0, i - 1)
    elif cmd == "R":
        i = min(len(AIMS) - 1, i + 1)
    return AIMS[i]


def lit_tiles(aim):
    if aim == "LEFT":
        return {(BEAM_ROW, c) for c in range(0, 3)}
    if aim == "RIGHT":
        return {(BEAM_ROW, c) for c in range(4, 7)}
    return set()


class Game:
    def __init__(self, night):
        cfg = NIGHTS[night]
        self.night = night
        self.name = cfg["name"]
        self.coast = cfg["coast"]
        self.aim = cfg["aim"]
        self.ships = dict(cfg["ships"])   # ships at sea: number -> (row, col)
        self.docked = []
        self.wrecked = {}                 # number -> (row, col)
        self.turn = 1
        self.started = False
        self.over = False
        self.status = "playing"           # playing | won | lost | dawn

    def tile(self, r, c):
        if (r, c) == LIGHTHOUSE:
            return "T"
        if r == GRID - 1:
            return self.coast[c]
        return "."

    def lit(self):
        return lit_tiles(self.aim)

    def display_lit(self):
        # Every screen, including the first, draws the tiles lit by the current aim.
        return self.lit()

    def board_lines(self):
        lit = self.display_lit()
        grid = []
        for r in range(GRID):
            row = []
            for c in range(GRID):
                row.append("~" if (r, c) in lit else self.tile(r, c))
            grid.append(row)
        for n in sorted(self.ships, reverse=True):  # lower number drawn last
            r, c = self.ships[n]
            grid[r][c] = str(n)
        lines = ["  " + "".join(str(c) for c in range(GRID))]
        for r in range(GRID):
            lines.append("%d %s" % (r, "".join(grid[r])))
        return lines

    def ship_lines(self):
        lines = []
        everyone = set(self.ships) | set(self.docked) | set(self.wrecked)
        for n in sorted(everyone):
            if n in self.ships:
                lines.append("  Ship %d: %s" % (n, fmt(self.ships[n])))
            elif n in self.docked:
                lines.append("  Ship %d: docked" % n)
            else:
                lines.append("  Ship %d: wrecked at %s" % (n, fmt(self.wrecked[n])))
        return lines

    def forecast(self):
        return "Forecast: " + ", ".join(
            "%s -> %s" % (c, next_aim(self.aim, c)) for c in COMMANDS)

    def header(self):
        return '=== Night %d "%s" | Turn %d of %d | Beam: %s ===' % (
            self.night, self.name, self.turn, TURN_LIMIT, self.aim)

    def screen(self):
        out = [self.header()]
        out += self.board_lines()
        out.append("Ships:")
        out += self.ship_lines()
        out.append(self.forecast())
        return out

    def trace_line(self):
        return "[trace] turn=%d aim=%s lit=%s ships=%s docked=%s wrecked=%s status=%s" % (
            self.turn, self.aim, sorted(self.lit()),
            {n: self.ships[n] for n in sorted(self.ships)},
            sorted(self.docked),
            {n: self.wrecked[n] for n in sorted(self.wrecked)}, self.status)

    def step(self, cmd):
        """Play one turn with a valid command; return event lines."""
        assert not self.over and cmd in COMMANDS
        self.started = True
        self.aim = next_aim(self.aim, cmd)
        lit = self.lit()
        events = []
        moves = {}
        for n in sorted(self.ships):
            old = self.ships[n]
            r, c = old
            if old in lit:
                if self.aim == "LEFT":
                    nc, word = c - 1, "west"
                else:
                    nc, word = c + 1, "east"
                if 0 <= nc < GRID:
                    new = (r, nc)
                    desc = "lit, slid %s %s -> %s" % (word, fmt(old), fmt(new))
                else:
                    new = old
                    desc = "lit but pinned at the map edge, stays at %s" % fmt(old)
            else:
                new = (r + 1, c)
                desc = "moved south %s -> %s" % (fmt(old), fmt(new))
            moves[n] = (new, desc)
        for n in sorted(moves):
            new, desc = moves[n]
            ch = self.tile(*new)
            if ch == "H":
                del self.ships[n]
                self.docked.append(n)
                desc += ": DOCKED at %s" % fmt(new)
            elif ch in ("#", "T"):
                del self.ships[n]
                self.wrecked[n] = new
                desc += ": WRECKED at %s" % fmt(new)
            else:
                self.ships[n] = new
            events.append("  Ship %d %s." % (n, desc))
        if self.wrecked:
            self.status, self.over = "lost", True
        elif not self.ships:
            self.status, self.over = "won", True
        elif self.turn >= TURN_LIMIT:
            self.status, self.over = "dawn", True
        else:
            self.turn += 1
        return events

    def result(self):
        if self.status == "won":
            return "NIGHT WON on turn %d." % self.turn
        if self.status == "lost":
            return "NIGHT LOST on turn %d: %s." % (self.turn, "; ".join(
                "ship %d wrecked at %s" % (n, fmt(self.wrecked[n]))
                for n in sorted(self.wrecked)))
        if self.status == "dawn":
            return "DAWN: ships still at sea (NIGHT LOST at turn %d): %s." % (
                self.turn, ", ".join("ship %d at %s" % (n, fmt(self.ships[n]))
                                     for n in sorted(self.ships)))
        return ""


def parse_script(text):
    """Return (night or None, commands, error or None)."""
    tokens = []
    for line in text.splitlines():
        tokens += line.split("#", 1)[0].split()
    if len(tokens) < 2 or tokens[0] != "night" or tokens[1] not in ("1", "2", "3"):
        return None, [], "Script must start with 'night N' where N is 1, 2 or 3."
    return int(tokens[1]), tokens[2:], None


def run_script(text, trace=False):
    """Play a script; return (output text, exit code)."""
    night, cmds, err = parse_script(text)
    if err:
        return "ERROR: " + err + "\n", 2
    g = Game(night)
    out = g.screen()
    if trace:
        out.append(g.trace_line())
    for tok in cmds:
        if g.over:
            out.append("Ignored (the night is over): %s" % tok)
            continue
        if tok not in COMMANDS:
            out.append("> Unrecognized command '%s': ignored. Turn %d is unchanged "
                       "(use L, R or H)." % (tok, g.turn))
            continue
        out.append("> Turn %d command: %s" % (g.turn, tok))
        out += g.step(tok)
        if g.over:
            out.append("=== Night %d \"%s\" | Turn %d of %d | Beam: %s ===" % (
                g.night, g.name, g.turn, TURN_LIMIT, g.aim))
            out += g.board_lines()
            out.append("Ships:")
            out += g.ship_lines()
            out.append(g.result())
        else:
            out += g.screen()
        if trace:
            out.append(g.trace_line())
    if not g.over:
        out.append("SCRIPT ENDED: the night is unfinished at turn %d of %d." % (
            g.turn, TURN_LIMIT))
    return "\n".join(out) + "\n", 0
>>>END

<<<FILE repo/tests/test_game.py
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from lamplight import Game, run_script, next_aim  # noqa: E402


def play(night, cmds, trace=False):
    return run_script("night %d\n%s\n" % (night, cmds), trace)[0]


def positions(night, cmds):
    g = Game(night)
    seq = []
    for c in cmds.split():
        g.step(c)
        seq.append(dict(g.ships))
    return g, seq


class StartScreens(unittest.TestCase):
    def test_night1(self):
        out = play(1, "")
        self.assertIn('=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===', out)
        self.assertIn("  0123456\n0 .......\n1 ..1....\n2 .......\n3 ...T...\n"
                      "4 .......\n5 .......\n6 H######\n", out)
        self.assertIn("  Ship 1: (1,2)", out)
        self.assertIn("Forecast: L -> LEFT, H -> UP, R -> RIGHT", out)

    def test_night2(self):
        out = play(2, "")
        self.assertIn("0 ....2..\n1 .......\n2 ..1....\n3 ...T...\n"
                      "4 .......\n5 .......\n6 #H###H#\n", out)

    def test_night3_ships_and_coast(self):
        out = play(3, "")
        self.assertIn("Beam: RIGHT", out)
        self.assertIn("0 .....3.", out)
        self.assertIn("1 ..2....", out)
        self.assertIn("2 .1.....", out)
        self.assertIn("6 H#H###H", out)
        self.assertIn("3 ...T~~~", out)

    def test_first_screen_lit_matches_aim(self):
        self.assertNotIn("~", play(1, ""))
        self.assertNotIn("~", play(2, ""))
        out = play(3, "")
        first = out.split("Forecast:")[0]
        self.assertEqual(first.count("~"), 3)
        self.assertIn("Forecast: L -> UP, H -> RIGHT, R -> RIGHT", out)


class Aim(unittest.TestCase):
    def test_transitions(self):
        self.assertEqual(next_aim("UP", "L"), "LEFT")
        self.assertEqual(next_aim("UP", "R"), "RIGHT")
        self.assertEqual(next_aim("LEFT", "L"), "LEFT")
        self.assertEqual(next_aim("RIGHT", "R"), "RIGHT")
        self.assertEqual(next_aim("LEFT", "R"), "UP")
        self.assertEqual(next_aim("RIGHT", "L"), "UP")
        for a in ("LEFT", "UP", "RIGHT"):
            self.assertEqual(next_aim(a, "H"), a)

    def test_switch_takes_two_turns(self):
        g = Game(1)
        g.step("L")
        g.step("R")
        self.assertEqual(g.aim, "UP")
        g.step("R")
        self.assertEqual(g.aim, "RIGHT")


class Display(unittest.TestCase):
    def test_lit_tiles(self):
        out = play(1, "L")
        self.assertIn("3 ~~~T~~~"[:0] + "3 ~~~T...", out.split("Beam: LEFT")[1])
        out = play(2, "R R")
        self.assertIn("3 ...T~~~", out)
        self.assertNotIn("~", play(1, "H H"))

    def test_ship_on_lit_tile_shows_digit(self):
        out = play(1, "L H")  # turn 3 screen: ship at (3,2) under LEFT
        self.assertIn("3 ~~1T...", out.split("Turn 3 of 10")[1])


class Solutions(unittest.TestCase):
    def check(self, night, cmds, table):
        g, seq = positions(night, cmds)
        self.assertEqual(seq, table)
        self.assertEqual(g.status, "won")
        self.assertEqual(g.turn, 7)
        self.assertIn("NIGHT WON on turn 7.", play(night, cmds))

    def test_night1(self):
        self.check(1, "L H H H R H H",
                   [{1: (2, 2)}, {1: (3, 2)}, {1: (3, 1)}, {1: (3, 0)},
                    {1: (4, 0)}, {1: (5, 0)}, {}])

    def test_night2(self):
        self.check(2, "H L R R L H H",
                   [{1: (3, 2), 2: (1, 4)}, {1: (3, 1), 2: (2, 4)},
                    {1: (4, 1), 2: (3, 4)}, {1: (5, 1), 2: (3, 5)},
                    {2: (4, 5)}, {2: (5, 5)}, {}])

    def test_night3(self):
        self.check(3, "L L R R L H H",
                   [{1: (3, 1), 2: (2, 2), 3: (1, 5)},
                    {1: (3, 0), 2: (3, 2), 3: (2, 5)},
                    {1: (4, 0), 2: (4, 2), 3: (3, 5)},
                    {1: (5, 0), 2: (5, 2), 3: (3, 6)},
                    {3: (4, 6)}, {3: (5, 6)}, {}])

    def test_night1_early_turn(self):
        self.assertIn("NIGHT WON on turn 7.", play(1, "H L H H R H H"))


class Failures(unittest.TestCase):
    def test_n1_all_hold(self):
        out = play(1, "H H H H H")
        self.assertIn("NIGHT LOST on turn 5: ship 1 wrecked at (6,2).", out)
        self.assertIn("WRECKED at (6,2)", out)

    def test_n1_released_early(self):
        self.assertIn("NIGHT LOST on turn 6: ship 1 wrecked at (6,1).",
                      play(1, "L H H R H H"))

    def test_n1_dawn(self):
        out = play(1, "L" + " H" * 9)
        self.assertIn("DAWN: ships still at sea", out)
        self.assertIn("ship 1 at (3,0)", out)
        g, _ = positions(1, "L" + " H" * 9)
        self.assertEqual((g.status, g.turn), ("dawn", 10))

    def test_n2_all_hold(self):
        self.assertIn("NIGHT LOST on turn 4: ship 1 wrecked at (6,2).",
                      play(2, "H H H H"))

    def test_n3_all_hold(self):
        self.assertIn("NIGHT LOST on turn 4: ship 1 wrecked at (6,1).",
                      play(3, "H H H H"))
        g, _ = positions(3, "H H H H")
        self.assertEqual(g.ships[3], (3, 6))

    def test_n3_same_turn(self):
        out = play(3, "L L H R H H")
        self.assertIn("NIGHT LOST on turn 6:", out)
        self.assertIn("Ship 1 moved south (5,0) -> (6,0): DOCKED at (6,0)", out)
        self.assertIn("ship 2 wrecked at (6,1)", out)
        self.assertIn("ship 3 wrecked at (6,5)", out)

    def test_last_ship_docks_on_turn_10(self):
        out = play(1, "L H H H H H H R H H")
        self.assertIn("NIGHT WON on turn 10.", out)

    def test_pinned_reported(self):
        out = play(1, "L H H H H")
        self.assertIn("pinned at the map edge, stays at (3,0)", out)
        self.assertNotIn("WRECKED", out)

    def test_pinned_right_edge(self):
        # Night 3 solution prefix, then R again: ship 3 slides to (3,6) on turn 4
        # and is pinned there on turn 5 (RIGHT stays RIGHT); ships 1 and 2 dock.
        g, seq = positions(3, "L L R R R")
        self.assertEqual(g.status, "playing")
        self.assertEqual(g.ships, {3: (3, 6)})
        self.assertIn("pinned at the map edge, stays at (3,6)",
                      play(3, "L L R R R"))


class Input(unittest.TestCase):
    def test_deterministic(self):
        s = "night 2\nH L R R L H H\n"
        self.assertEqual(run_script(s), run_script(s))
        self.assertEqual(run_script(s, True), run_script(s, True))

    def test_invalid_command_does_not_advance(self):
        out = play(1, "X L")
        self.assertIn("Unrecognized command 'X': ignored. Turn 1 is unchanged", out)
        self.assertIn("> Turn 1 command: L", out)

    def test_lowercase_is_invalid(self):
        self.assertIn("Unrecognized command 'l'", play(1, "l"))

    def test_unfinished(self):
        self.assertIn("SCRIPT ENDED: the night is unfinished at turn 3 of 10.",
                      play(1, "L H"))

    def test_ignored_after_end(self):
        out = play(1, "H H H H H H L")
        self.assertIn("Ignored (the night is over): H", out)
        self.assertIn("Ignored (the night is over): L", out)

    def test_bad_header(self):
        out, code = run_script("L H H")
        self.assertEqual(code, 2)
        self.assertIn("ERROR", out)
        self.assertEqual(run_script("night 4 L")[1], 2)

    def test_comments_and_lines(self):
        a = play(1, "L H H H R H H")
        b = run_script("night 1  # first\nL H H\nH R # x\nH H\n")[0]
        self.assertEqual(a, b)

    def test_trace_adds_state(self):
        out = play(1, "L", trace=True)
        self.assertIn("[trace] turn=2 aim=LEFT", out)
        self.assertNotIn("[trace]", play(1, "L"))

    def test_forecast_follows_aim(self):
        out = play(1, "L")
        self.assertIn("Forecast: L -> LEFT, H -> LEFT, R -> UP", out)

    def test_lower_number_drawn(self):
        g = Game(1)
        g.ships = {2: (0, 0), 1: (0, 0)}
        self.assertEqual(g.board_lines()[1][2], "1")


if __name__ == "__main__":
    unittest.main()
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

- Write the outgoing Handoff as goals/G-001-first-playable/12-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
