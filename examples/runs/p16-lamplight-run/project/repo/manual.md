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
