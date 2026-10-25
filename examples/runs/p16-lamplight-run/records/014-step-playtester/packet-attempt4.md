# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-first-playable/13-studio-to-playtester.md
next_seq: 14
runs: play (0 rounds left; results in @run-results)
run_play: python3 play.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable/14-playtester-to-<recipient>.md
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

<<<FILE goals/G-001-first-playable/13-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 13
from: studio
to: playtester
stage: Play
outcome: routed
---
# 13: studio → playtester — play the first playable as a player and report what you experience

## Task

Play Lamplight Keeper as a player would, using only the manual, and report what you observe and experience.

## Context

A first playable build of a short, turn-based puzzle game exists. You are asked to play it as a new player, with no knowledge of how it was made.

## Findings

How to obtain and run the build:

- The build is in `repo/`. The only player documentation is `repo/manual.md`; read it first and rely on nothing else about how the game works.
- The game is played through input scripts, not live input. Write a script in the format the manual describes, then run `python3 play.py {script}` from `repo/`, where `{script}` is the path to your script. The output shows what a player sees.
- The manual lists the available nights. Play every night it offers, and try more than one script per night (including ones that fail), as a player learning the game would.

Player profile: puzzle players who like short, thinky sessions with readable rules (in the spirit of small turn-based puzzle games). They want to plan, not to react fast.

Play focus: play as this player would, from the first night on. Note what you understand and what you do not, what you try and why, and how each night feels.

## Decisions already made

None.

## Constraints

- Observable experience only: report what you saw and felt, in player terms. Do not read source code, tests or design documents, and do not use `--trace`.
- Do not edit anything in the build or the project.
- No decision authority over the game: report observations, do not prescribe fixes.

## Open questions

None.

## Expected output

An observation report (`playtest-session`): what you did (scripts tried, in order), what happened, what was clear or confusing, how long nights felt, and where you felt stuck, bored or pleased. Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile; repo/manual.md; the build in repo/ (run with `python3 play.py {script}`)
- Decisions: none
- Previous handoff: none
>>>END

<<<FILE studio/roles/playtester.md
---
kind: role
id: playtester
receives_from: studio
load_only: studio/roles/playtester.md, studio/skills/playtest-session.md, project.md#player-profile, @player_visible
strip_sections: Sender assessment
runs: play
---
# Role: Playtester

## Responsibility

Evaluates the game as a player: what is fun, boring, confusing or frustrating, based only on what a
player can observe.

## Decides

Nothing about the game. Owns the honesty and accuracy of its observations.

## Must not

- Read source code, diffs, implementation notes, or design intent before playing.
- Propose code-level fixes or judge against the design document instead of the experience.
- Report observations it did not actually make.

## Independence

Works from the build and a player profile only, in a fresh executor context without implementation
history. Is not told what changed or what result is expected, so that it cannot confirm a
hypothesis it was handed.

## Works from

A Handoff composed by the Studio (never one written by a Role that knows the implementation):

- How to obtain and run the build, and which part to play.
- The player profile from the Project Context.
- Optionally a play focus that does not reveal the expected result (e.g., "pay attention to
  combat", not "check whether combat is less monotonous now").

## Produces

- An observation report: concrete moments, what the player did and felt, friction, quotes in
  player language, how strongly each issue affected the experience, and the method used to play.

## Hands back / escalates when

Sets `to` per the route; the Studio's Route operation confirms or changes it. Experience issues go
to `game-designer`, defects to `qa`.

## Typical skills

playtest-session
>>>END

<<<FILE studio/skills/playtest-session.md
---
name: playtest-session
description: Play a build as a player and report the observable experience — fun, friction, confusion, boredom — without reference to implementation.
---
# Skill: Playtest session

Typical roles: playtester.

## When to use

To observe how the game plays or feels, before diagnosis or after a change.

## Inputs

How to obtain and run the build, what to play, the player profile, optionally a neutral play focus.

## Method

1. Adopt the player profile. Play as that player would, not as a tester hunting edge cases.
2. Log concrete moments: what you tried, what happened, what you felt, and when your attention
   dropped or spiked.
3. Note friction, confusion, boredom and delight in player language ("I never needed to dodge").
4. Rate how much each issue affected the experience. Separate observations from hypotheses.
5. State the method you actually used to play (live play, input automation, recorded sessions,
   human playtest notes). If you could not observe something, say so.

## Output

Observation report: method, session summary, concrete moments, issues with impact, positives,
open player questions.

## Do not

Read source code or design intent first. Invent observations. Prescribe code-level fixes.
>>>END

<<<FILE project.md#player-profile
## Player profile

Puzzle players who like short, thinky sessions with readable rules (in the spirit of small
turn-based puzzle games). They want to plan, not to react fast.
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

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/manual.md
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

<<<FILE @run-results
### Round 1: @run/play/night1-explore — `python3 play.py {script}`

Script:

```text
night 1
H H H
```

Exit: 0 (0.0 s). Output:

```text
=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===
  0123456
0 .......
1 ..1....
2 .......
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (1,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (1,2) -> (2,2).
=== Night 1 "First light" | Turn 2 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 ..1....
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (2,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 2 command: H
  Ship 1 moved south (2,2) -> (3,2).
=== Night 1 "First light" | Turn 3 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ..1T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (3,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 3 command: H
  Ship 1 moved south (3,2) -> (4,2).
=== Night 1 "First light" | Turn 4 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 ..1....
5 .......
6 H######
Ships:
  Ship 1: (4,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
SCRIPT ENDED: the night is unfinished at turn 4 of 10.
```

### Round 2: @run/play/night1-win — `python3 play.py {script}`

Script:

```text
night 1
H H L H R H H   # slide the ship west with the beam, then let it sink to the harbor
```

Exit: 0 (0.0 s). Output:

```text
=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===
  0123456
0 .......
1 ..1....
2 .......
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (1,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (1,2) -> (2,2).
=== Night 1 "First light" | Turn 2 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 ..1....
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (2,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 2 command: H
  Ship 1 moved south (2,2) -> (3,2).
=== Night 1 "First light" | Turn 3 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ..1T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (3,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 3 command: L
  Ship 1 lit, slid west (3,2) -> (3,1).
=== Night 1 "First light" | Turn 4 of 10 | Beam: LEFT ===
  0123456
0 .......
1 .......
2 .......
3 ~1~T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (3,1)
Forecast: L -> LEFT, H -> LEFT, R -> UP
> Turn 4 command: H
  Ship 1 lit, slid west (3,1) -> (3,0).
=== Night 1 "First light" | Turn 5 of 10 | Beam: LEFT ===
  0123456
0 .......
1 .......
2 .......
3 1~~T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (3,0)
Forecast: L -> LEFT, H -> LEFT, R -> UP
> Turn 5 command: R
  Ship 1 moved south (3,0) -> (4,0).
=== Night 1 "First light" | Turn 6 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 1......
5 .......
6 H######
Ships:
  Ship 1: (4,0)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 6 command: H
  Ship 1 moved south (4,0) -> (5,0).
=== Night 1 "First light" | Turn 7 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 1......
6 H######
Ships:
  Ship 1: (5,0)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 7 command: H
  Ship 1 moved south (5,0) -> (6,0): DOCKED at (6,0).
=== Night 1 "First light" | Turn 7 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: docked
NIGHT WON on turn 7.
```

### Round 2: @run/play/night1-fail — `python3 play.py {script}`

Script:

```text
night 1
H H H H H H H H H H   # do nothing, see what happens
```

Exit: 0 (0.0 s). Output:

```text
=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===
  0123456
0 .......
1 ..1....
2 .......
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (1,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (1,2) -> (2,2).
=== Night 1 "First light" | Turn 2 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 ..1....
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (2,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 2 command: H
  Ship 1 moved south (2,2) -> (3,2).
=== Night 1 "First light" | Turn 3 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ..1T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: (3,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 3 command: H
  Ship 1 moved south (3,2) -> (4,2).
=== Night 1 "First light" | Turn 4 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 ..1....
5 .......
6 H######
Ships:
  Ship 1: (4,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 4 command: H
  Ship 1 moved south (4,2) -> (5,2).
=== Night 1 "First light" | Turn 5 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 ..1....
6 H######
Ships:
  Ship 1: (5,2)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 5 command: H
  Ship 1 moved south (5,2) -> (6,2): WRECKED at (6,2).
=== Night 1 "First light" | Turn 5 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 .......
6 H######
Ships:
  Ship 1: wrecked at (6,2)
NIGHT LOST on turn 5: ship 1 wrecked at (6,2).
Ignored (the night is over): H
Ignored (the night is over): H
Ignored (the night is over): H
Ignored (the night is over): H
Ignored (the night is over): H
```

### Round 2: @run/play/night2-look — `python3 play.py {script}`

Script:

```text
night 2
H
```

Exit: 0 (0.0 s). Output:

```text
=== Night 2 "Both sides" | Turn 1 of 10 | Beam: UP ===
  0123456
0 ....2..
1 .......
2 ..1....
3 ...T...
4 .......
5 .......
6 #H###H#
Ships:
  Ship 1: (2,2)
  Ship 2: (0,4)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (2,2) -> (3,2).
  Ship 2 moved south (0,4) -> (1,4).
=== Night 2 "Both sides" | Turn 2 of 10 | Beam: UP ===
  0123456
0 .......
1 ....2..
2 .......
3 ..1T...
4 .......
5 .......
6 #H###H#
Ships:
  Ship 1: (3,2)
  Ship 2: (1,4)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
SCRIPT ENDED: the night is unfinished at turn 2 of 10.
```

### Round 2: @run/play/night3-look — `python3 play.py {script}`

Script:

```text
night 3
H
```

Exit: 0 (0.0 s). Output:

```text
=== Night 3 "Keep it dark" | Turn 1 of 10 | Beam: RIGHT ===
  0123456
0 .....3.
1 ..2....
2 .1.....
3 ...T~~~
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (2,1)
  Ship 2: (1,2)
  Ship 3: (0,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (2,1) -> (3,1).
  Ship 2 moved south (1,2) -> (2,2).
  Ship 3 moved south (0,5) -> (1,5).
=== Night 3 "Keep it dark" | Turn 2 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .....3.
2 ..2....
3 .1.T~~~
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (3,1)
  Ship 2: (2,2)
  Ship 3: (1,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
SCRIPT ENDED: the night is unfinished at turn 2 of 10.
```

### Round 3: @run/play/night2-win — `python3 play.py {script}`

Script:

```text
night 2
H L R R L H H   # ship 1 slides west to column 1, ship 2 slides east to column 5, then both sink to harbors
```

Exit: 0 (0.0 s). Output:

```text
=== Night 2 "Both sides" | Turn 1 of 10 | Beam: UP ===
  0123456
0 ....2..
1 .......
2 ..1....
3 ...T...
4 .......
5 .......
6 #H###H#
Ships:
  Ship 1: (2,2)
  Ship 2: (0,4)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (2,2) -> (3,2).
  Ship 2 moved south (0,4) -> (1,4).
=== Night 2 "Both sides" | Turn 2 of 10 | Beam: UP ===
  0123456
0 .......
1 ....2..
2 .......
3 ..1T...
4 .......
5 .......
6 #H###H#
Ships:
  Ship 1: (3,2)
  Ship 2: (1,4)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 2 command: L
  Ship 1 lit, slid west (3,2) -> (3,1).
  Ship 2 moved south (1,4) -> (2,4).
=== Night 2 "Both sides" | Turn 3 of 10 | Beam: LEFT ===
  0123456
0 .......
1 .......
2 ....2..
3 ~1~T...
4 .......
5 .......
6 #H###H#
Ships:
  Ship 1: (3,1)
  Ship 2: (2,4)
Forecast: L -> LEFT, H -> LEFT, R -> UP
> Turn 3 command: R
  Ship 1 moved south (3,1) -> (4,1).
  Ship 2 moved south (2,4) -> (3,4).
=== Night 2 "Both sides" | Turn 4 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T2..
4 .1.....
5 .......
6 #H###H#
Ships:
  Ship 1: (4,1)
  Ship 2: (3,4)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 4 command: R
  Ship 1 moved south (4,1) -> (5,1).
  Ship 2 lit, slid east (3,4) -> (3,5).
=== Night 2 "Both sides" | Turn 5 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .......
2 .......
3 ...T~2~
4 .......
5 .1.....
6 #H###H#
Ships:
  Ship 1: (5,1)
  Ship 2: (3,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 5 command: L
  Ship 1 moved south (5,1) -> (6,1): DOCKED at (6,1).
  Ship 2 moved south (3,5) -> (4,5).
=== Night 2 "Both sides" | Turn 6 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .....2.
5 .......
6 #H###H#
Ships:
  Ship 1: docked
  Ship 2: (4,5)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 6 command: H
  Ship 2 moved south (4,5) -> (5,5).
=== Night 2 "Both sides" | Turn 7 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 .....2.
6 #H###H#
Ships:
  Ship 1: docked
  Ship 2: (5,5)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 7 command: H
  Ship 2 moved south (5,5) -> (6,5): DOCKED at (6,5).
=== Night 2 "Both sides" | Turn 7 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 .......
6 #H###H#
Ships:
  Ship 1: docked
  Ship 2: docked
NIGHT WON on turn 7.
```

### Round 3: @run/play/night3-win — `python3 play.py {script}`

Script:

```text
night 3
L L R R L H H   # swing the beam left to push ship 1, keep ship 2 dark, then right for ship 3
```

Exit: 0 (0.0 s). Output:

```text
=== Night 3 "Keep it dark" | Turn 1 of 10 | Beam: RIGHT ===
  0123456
0 .....3.
1 ..2....
2 .1.....
3 ...T~~~
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (2,1)
  Ship 2: (1,2)
  Ship 3: (0,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 1 command: L
  Ship 1 moved south (2,1) -> (3,1).
  Ship 2 moved south (1,2) -> (2,2).
  Ship 3 moved south (0,5) -> (1,5).
=== Night 3 "Keep it dark" | Turn 2 of 10 | Beam: UP ===
  0123456
0 .......
1 .....3.
2 ..2....
3 .1.T...
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (3,1)
  Ship 2: (2,2)
  Ship 3: (1,5)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 2 command: L
  Ship 1 lit, slid west (3,1) -> (3,0).
  Ship 2 moved south (2,2) -> (3,2).
  Ship 3 moved south (1,5) -> (2,5).
=== Night 3 "Keep it dark" | Turn 3 of 10 | Beam: LEFT ===
  0123456
0 .......
1 .......
2 .....3.
3 1~2T...
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (3,0)
  Ship 2: (3,2)
  Ship 3: (2,5)
Forecast: L -> LEFT, H -> LEFT, R -> UP
> Turn 3 command: R
  Ship 1 moved south (3,0) -> (4,0).
  Ship 2 moved south (3,2) -> (4,2).
  Ship 3 moved south (2,5) -> (3,5).
=== Night 3 "Keep it dark" | Turn 4 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T.3.
4 1.2....
5 .......
6 H#H###H
Ships:
  Ship 1: (4,0)
  Ship 2: (4,2)
  Ship 3: (3,5)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 4 command: R
  Ship 1 moved south (4,0) -> (5,0).
  Ship 2 moved south (4,2) -> (5,2).
  Ship 3 lit, slid east (3,5) -> (3,6).
=== Night 3 "Keep it dark" | Turn 5 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .......
2 .......
3 ...T~~3
4 .......
5 1.2....
6 H#H###H
Ships:
  Ship 1: (5,0)
  Ship 2: (5,2)
  Ship 3: (3,6)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 5 command: L
  Ship 1 moved south (5,0) -> (6,0): DOCKED at (6,0).
  Ship 2 moved south (5,2) -> (6,2): DOCKED at (6,2).
  Ship 3 moved south (3,6) -> (4,6).
=== Night 3 "Keep it dark" | Turn 6 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 ......3
5 .......
6 H#H###H
Ships:
  Ship 1: docked
  Ship 2: docked
  Ship 3: (4,6)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 6 command: H
  Ship 3 moved south (4,6) -> (5,6).
=== Night 3 "Keep it dark" | Turn 7 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 ......3
6 H#H###H
Ships:
  Ship 1: docked
  Ship 2: docked
  Ship 3: (5,6)
Forecast: L -> LEFT, H -> UP, R -> RIGHT
> Turn 7 command: H
  Ship 3 moved south (5,6) -> (6,6): DOCKED at (6,6).
=== Night 3 "Keep it dark" | Turn 7 of 10 | Beam: UP ===
  0123456
0 .......
1 .......
2 .......
3 ...T...
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: docked
  Ship 2: docked
  Ship 3: docked
NIGHT WON on turn 7.
```

### Round 3: @run/play/night3-fail — `python3 play.py {script}`

Script:

```text
night 3
H H H H H H   # leave the beam alone, see what happens
```

Exit: 0 (0.0 s). Output:

```text
=== Night 3 "Keep it dark" | Turn 1 of 10 | Beam: RIGHT ===
  0123456
0 .....3.
1 ..2....
2 .1.....
3 ...T~~~
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (2,1)
  Ship 2: (1,2)
  Ship 3: (0,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 1 command: H
  Ship 1 moved south (2,1) -> (3,1).
  Ship 2 moved south (1,2) -> (2,2).
  Ship 3 moved south (0,5) -> (1,5).
=== Night 3 "Keep it dark" | Turn 2 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .....3.
2 ..2....
3 .1.T~~~
4 .......
5 .......
6 H#H###H
Ships:
  Ship 1: (3,1)
  Ship 2: (2,2)
  Ship 3: (1,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 2 command: H
  Ship 1 moved south (3,1) -> (4,1).
  Ship 2 moved south (2,2) -> (3,2).
  Ship 3 moved south (1,5) -> (2,5).
=== Night 3 "Keep it dark" | Turn 3 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .......
2 .....3.
3 ..2T~~~
4 .1.....
5 .......
6 H#H###H
Ships:
  Ship 1: (4,1)
  Ship 2: (3,2)
  Ship 3: (2,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 3 command: H
  Ship 1 moved south (4,1) -> (5,1).
  Ship 2 moved south (3,2) -> (4,2).
  Ship 3 moved south (2,5) -> (3,5).
=== Night 3 "Keep it dark" | Turn 4 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .......
2 .......
3 ...T~3~
4 ..2....
5 .1.....
6 H#H###H
Ships:
  Ship 1: (5,1)
  Ship 2: (4,2)
  Ship 3: (3,5)
Forecast: L -> UP, H -> RIGHT, R -> RIGHT
> Turn 4 command: H
  Ship 1 moved south (5,1) -> (6,1): WRECKED at (6,1).
  Ship 2 moved south (4,2) -> (5,2).
  Ship 3 lit, slid east (3,5) -> (3,6).
=== Night 3 "Keep it dark" | Turn 4 of 10 | Beam: RIGHT ===
  0123456
0 .......
1 .......
2 .......
3 ...T~~3
4 .......
5 ..2....
6 H#H###H
Ships:
  Ship 1: wrecked at (6,1)
  Ship 2: (5,2)
  Ship 3: (3,6)
NIGHT LOST on turn 4: ship 1 wrecked at (6,1).
Ignored (the night is over): H
Ignored (the night is over): H
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable/14-playtester-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
