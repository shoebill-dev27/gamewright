---
kind: handoff
goal: G-001
seq: 39
from: qa
to: studio
stage: Verify
outcome: pass
---
# 39: qa → studio — rendering change (build 0.5) verified: AC-17 and AC-18 pass at 30 and 60 FPS, C1/C7/C3 unchanged, one capture not obtainable

## Task

Verify the current build against AC-17 and AC-18 and D-006's display ruling, and confirm that nothing else changed. AC-15 is not judged: its manual text part is waiting on the Owner.

## Context

This is the follow-up to handoff 37 and the baseline handoff 29. I did not edit the build or `manual.md`. All evidence is from `run_tests`, `run_play` and `run_trace` output of this step (round 1 of the runs). Cuts are marked `[cut: …]`; every event line in a cut section is kept in order.

## Findings

### Verdict: `pass` for the scope of handoff 37

- AC-18 passes at 30 and 60 FPS.
- AC-17 passes for the 30/60 comparison of the scripts I re-ran. The other criteria within AC-1…14 were not re-run and rest on the suite (see section 2).
- C1, C7 and C3 are unchanged from the baseline in timings, hearts and hit results.
- AC-15 is not judged. `ManualTest` is reported as **not run**.
- The `--color` capture could not be made (section 5).

### 1. run_tests

- Command: `python3 -m unittest discover -s tests`. Exit 1. 40 tests ran: **38 passed, 0 failed, 2 errors**.
- The two errors are both `ManualTest` (`test_manual_lists_glyphs_and_lines`, `test_on_screen_section_lists_x_and_the_practice_room`), `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`.
- This is the known `manual.md` layout matter, as the task said. Both are counted as **not run**, and I count them against no AC.
- The suite grew from 34 to 40 tests since handoff 29. No other test errors or fails.

### 2. AC-18 (no hidden enemy) and AC-17 (frame rate)

**AC-18, grub on the player's tile.** Script C1: `room empty`, `fps N`, `player 8 4`, `spawn grub 12 4`, `end 8`. Run at `fps 30` and `fps 60`. The player view, both frame rates, shows a grub glyph in a cell different from `P` in every draw where a living grub exists, from 0.00 s to 5.50 s. After the down at 5.0 s it is `xg`.

- **"(on you)" lines, 30 FPS:**
  - 3.600 "the grub is open (on you)": draw `Pg` (lowercase `g` visible). Same at the 4.00 s draw.
  - 4.500 "a grub rears back (on you)": draw `PG` (uppercase `G` visible).
- **"(on you)" lines, 60 FPS:**
  - 3.583 "the grub is open (on you)": `Pg`.
  - 4.483 "a grub rears back (on you)": `PG`.
- **Strike draws on the tile:** 30 FPS 5.00 s `PG`. 60 FPS 4.50 s `PG`, and the down draw at 5.00 s is `xg`.
- **"(on you)" with a damaged grub (C2, `1.6 attack`, `end 5`):** 30 FPS 4.867 and 60 FPS 4.883 "the grub is open (on you)" show `Pw`. The wind-up draws before show `PW`.

Raw excerpt (C1, 30 FPS):

```text
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 4.00 s, identical]
  4.500  a grub rears back (on you)
   [4.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 5.00 s, `PG`]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
   [5.03 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
```

Raw excerpt (C1, 60 FPS):

```text
  3.583  the grub is open (on you)
   [3.58 s] hearts 1/3
   |        Pg      |
  4.483  a grub rears back (on you)
   [4.48 s] hearts 1/3
   |        PG      |
  5.000  YOU ARE HIT by a grub — hearts 0/3
  5.000  you went down
   [5.00 s] hearts 0/3
   |        xg      |
```

(The map rows are shortened to the player row; the other rows are empty, as in the full capture.)

**AC-18, spitter on the tile.** Script: `room empty`, `fps N`, `player 8 4`, `spawn spitter 8.2 4`, `end 4`. At both frame rates every draw shows `P` with a spitter in the neighbouring cell on the right: `Ps` while idle, **`PS` during the charge** (1.00 s and 1.50 s, and 3.50 s and 4.00 s), `Ps` again after the spit.

```text
  1.000  spitter (center) charges
   [1.00 s] hearts 3/3
   |        PS      |
  1.800  spitter (center) spits
   [1.80 s] hearts 3/3
   |        Ps      |
  1.833  YOU ARE HIT by a shot — hearts 2/3
```

60 FPS: the same draws; charge 1.000, spit 1.800, hit 1.817.

**Two enemies overlapping the player.** Script: `room empty`, `fps N`, `player 8 4`, `spawn grub 8.2 4`, `spawn spitter 8.1 4`, `end 4`. The two enemies are drawn in different cells on opposite sides of `P`, in every draw and in every state:

- Idle: `sPg`.
- Spitter charging, grub idle: `SPg`.
- Spitter charging and grub winding up: `SPG`.
- Down: `sxg`.

```text
  0.033  a grub rears back (right)
   [0.03 s] hearts 3/3
   |       sPG      |
  1.000  spitter (center) charges
   [1.00 s] hearts 2/3
   |       SPg      |
  1.583  a grub rears back (on you)
   [1.60 s] hearts 2/3
   |       SPG      |
  3.667  YOU ARE HIT by a grub — hearts 0/3
  3.667  you went down
   [3.67 s] hearts 0/3
   |       sxg      |
```

60 FPS: the same draws (`sPG` at 0.017, `SPg` at 1.00, `SPG` at 1.57, `sxg` after the down at 3.633).

**Three overlapping grubs (room 1 after several bites, C7).** At 3.57 s (30 FPS) three grubs have their true cell on the player's cell. The draw shows three grub glyphs in three distinct cells beside `P`: `G` left, `g` right, `g` above. After the down it is `gxg` with a `g` above. No grub is hidden, and the wind-up `G` is on the side named in the line ("rears back (left)").

```text
  3.567  a grub rears back (left)
   [3.57 s] hearts 1/3
   |        G       |
   |       GPg      |
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
   |        g       |
   |       GPg      |
```

**AC-17 timings and 30/60 comparison.** Timestamps for the three scripts:

| Event | 30 FPS | 60 FPS | Difference |
|---|---|---|---|
| C1 first wind-up | 1.400 | 1.383 | 0.017 |
| C1 first hit | 1.967 | 1.933 | 0.034 |
| C1 open | 2.050 | 2.033 | 0.017 |
| C1 second wind-up | 2.950 | 2.933 | 0.017 |
| C1 second hit | 3.467 | 3.450 | 0.017 |
| C1 down | 5.033 | 5.000 | 0.033 |
| C7 down | 4.967 | 4.950 | 0.017 |
| C7 run over | 6.967 | 6.950 | 0.017 |
| C3 swipe hit | 2.500 | 2.500 | 0 |
| C3 third hit | 3.500 | 3.483 | 0.017 |
| C3 down | 5.033 | 5.000 | 0.033 |

All differences are at most 0.034 s (limit 0.07 s). Event sequences are the same at both rates. AC-18's own clause "no change to timings, hearts or positions" holds (section 3). The grub wind-up to strike interval is 0.500 s and the recovery interval is 0.900 s at both rates (trace C1: 1.400→1.900, 2.067→2.967 at 30 FPS; 1.383→1.883, 2.033→2.933 at 60 FPS).

**Scope of AC-17.** AC-17 also names AC-1…AC-14. This round I re-ran only the scripts C1, C2, C3, C7, the spitter, miss and overlap scripts, at both frame rates. The 38 passing suite tests still cover the rest. The independent observations of handoff 29 for AC-3, AC-9, AC-10 and AC-12 were not repeated, and nothing in this round contradicts them.

### 3. Repeats of C1, C7, C3 compared with the earlier results (handoff 29)

I compared the event lines and the trace events. Every timestamp, heart count and hit result equals the baseline.

**C1 (30 FPS), event lines:** 1.400 rears back; 1.967 hit 2/3; 2.050 open; 2.950 rears back; 3.467 hit 1/3; 3.600 open (on you); 4.500 rears back (on you); 5.033 hit 0/3 and "you went down"; `end at 7.03 s: hearts 0/3, enemies left 1`. All the same as baseline. C1 60 FPS: 1.383, 1.933, 2.033, 2.933, 3.450, 3.583, 4.483, 5.000, `end at 7.00 s`. Same as baseline.

C1 trace lines (30 FPS):

```text
t=1.400 frame=42 ... hearts=3 ... | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.967 frame=59 ... hearts=2 ... | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 ... hearts=2 ... | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=3.600 frame=108 ... hearts=1 ... | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=5.033 frame=151 room=empty phase=down ... hearts=0 ... | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
```

The 1.400, 1.967 and 2.067 lines are identical to the baseline trace lines in handoff 29. The positions agree too (grub x 9.25, 8.81, 8.25, 8.00).

**C7 (room 1, no input, `15 attack`, `end 20`), 30 FPS:**

- Event lines match the baseline line for line: 1.400 above, 1.900 left, 1.967 hit 2/3, 2.050, 2.550, 2.900, 2.950, 3.467 hit 1/3, 3.550, 3.567, 3.600 (on you), 4.217, 4.450, 4.500, 4.967 hit 0/3 and down, 6.967 run over, 15.000 "a new run begins" and "room 1 begins", second run through 19.967 down.
- 60 FPS: down at 4.950, run over 6.950, new run 15.000, second run down 19.950. Same as baseline.
- Trace: `run_over {'rooms': 0, 'complete': False}` at t=6.967 (30 FPS) and t=6.950 (60 FPS). `run_start; room_loaded {'room': '1'}` at t=15.033 and t=15.017 with hearts=3. Same as baseline.

**C3 (`2.5 attack`, `end 6`), 30 FPS:** 1.400 rears back, 1.967 hit, 2.050 open, 2.500 "you swipe: grub hit (1 left)", 2.950 rears back, 3.500 hit 1/3, 3.600 open, 4.500 rears back, 5.033 hit 0/3 and down. 60 FPS: 2.500, 2.933, 3.483, 3.583, 4.483, 5.000. Same as baseline.

C3 trace at the swipe (30 FPS) and baseline-equal:

```text
t=2.533 frame=76 ... | grub#0(8.42,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
```

C3 trace at 60 FPS: `t=2.517 ... grub#0(8.33,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}`.

C2 (`1.6 attack` in the wind-up) also matches the baseline: 1.600 hit and "the grub is open (right)", next wind-up 2.667 (30 FPS) / 2.683 (60 FPS), first hit 3.233 at both rates.

**The only differences from the baseline are in the draws**, and are the intended ones: where the baseline showed only `P` for an enemy on the player's tile, the new draws show the glyph beside `P`.

### 4. The hit draw with the swipe arc

The enemy glyph is visible over the arc. The arc `)` is drawn on the tiles above and below, and the hit enemy's own cell shows the enemy glyph, not the arc.

C3, 30 FPS, 2.500 swipe:

```text
  2.500  you swipe: grub hit (1 left)
   [2.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
```

- C3 60 FPS 2.52 s and C2 at 1.63 s (30 FPS) / 1.62 s (60 FPS) show the same `)` / `Pw` / `)`.
- The damaged glyph `w` is visible under the arc.
- A swipe that hits nothing draws the arc in all three cells: `)` / `P)` / `)` (miss script, 0.53 s at 30 FPS and 0.52 s at 60 FPS).

Not observed: a swipe while an enemy is on the player's tile and drawn beside `P` (the arc and the displaced glyph in the same cell). No script of mine covered it.

### 5. Captures for the art director

Verbatim where shown above. "Source" names the script.

| Requested | Result | Where |
|---|---|---|
| Grub on the player's tile in wind-up | captured | C1 30 FPS 4.50 s `PG`; 60 FPS 4.48 s `PG`; C7 3.57 s `GPg` |
| Strike draw | captured | C1 30 FPS 5.00 s `PG`; 60 FPS 4.50 s `PG` (strike starts at 5.000 / 4.983 in the trace) |
| Recovery draw | captured | C1 3.60 s `Pg` (30 FPS), 3.58 s (60 FPS); C2 4.87 s `Pw` |
| Spitter on the tile | captured | section 2, `Ps` idle, `PS` charging |
| Swipe after a miss | captured | miss script, section 4 |
| 60 FPS charge-start draw | captured | spitter on the tile, 60 FPS, 1.000 s `PS` and 3.500 s `PS` |
| One `--color` capture | **not captured** | see below |

**Color.** The project commands as given (`run_play: python3 play.py --view player {script}`) have no place for `--color`, and no output of mine contains ANSI codes. The only input of a run is the script, so I could not add the flag. The captures above are plain text. Handoff 29's reading of the code (lantern yellow for the player, orange for alert enemies, red for shots) is unchanged and not verified here. The studio should arrange a color run (for example a run command with `--color`) or leave color to the art director's own check.

### 6. Not verifiable, or not done

- **ManualTest** (2 tests): not run, because `manual.md` is missing from the workspace. Counted against no AC. AC-15's manual part is not judged.
- **`--color` capture:** not obtainable with the given commands.
- **Swipe while an enemy sits on the player's tile** (arc and displaced glyph together): not observed.
- **AC-14 and the suite-only items from handoff 29** (room clear, "(too soon)", "(down)" in the player view, the 2-swipe spitter kill): not re-run. They rest on the passing suite.
- **Pause:** still not verifiable (no script line for it).
- **Bots (`run_bots`):** not run. The handoff did not ask for balance numbers, and the simulation was meant to be unchanged. C1/C7/C3 equality supports that.
- **Where the displaced glyph sits:** in the captures it appears on the right when the grub sits at or slightly right of the player, and left/above for the extra grubs, as the D-006 order says. I did not check the "side it last came from" preference separately, because the captures all place a single grub on the side it came from. The art director may judge readability (an open point in the spec).

## Decisions already made

- D-006: enemies may overlap but are never hidden. Observed true at 30 and 60 FPS for grub, spitter, damaged grub, a down player and two or three enemies.
- D-001: no new inputs. None seen.

## Constraints

- All checks were run at 30 and 60 FPS through `run_tests`, `run_play` and `run_trace`. I did not edit the build or `manual.md`.

## Open questions

1. **For the studio:** provide a way to capture `--color` output, or decide the art director's color check is done outside QA.
2. **For the Owner or studio:** the `manual.md` layout, so `ManualTest` can run and AC-15 can be judged.

## Expected output

The studio can accept the rendering change for AC-17 (as listed in section 2) and AC-18. The art director can use the captures in section 5 for the visual re-check. No defect is routed to `gameplay-engineer`.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md, manual.md
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
