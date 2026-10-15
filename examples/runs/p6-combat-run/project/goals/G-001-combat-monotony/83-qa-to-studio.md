---
kind: handoff
goal: G-001
seq: 83
from: qa
to: studio
stage: Verify (V-17 defeat and dash-off draws, verbatim captures)
outcome: pass
---
# 83: qa → studio — V-17: both cases pass at 30 and 60 FPS; verbatim captures for the art-director

## Task

Report whether the build draws what V-17 requires in two cases, at 30 and 60 FPS:
1. A grub on the player's tile is defeated.
2. The player dashes off a tile with a grub on it.

Both cases could be set up with input scripts. Appendix A has the verbatim captures for the art-director.

## Context

G-001, Option A. Handoff 82 asked for the V-17 draws that the captures in 77 did not cover. I verified from the spec, the criteria and the build only, using `run_play` (`python3 play.py --view player {script}`). The results are the six runs of round 1. I did not change the repo, `manual.md` or the tests.

## Findings

### Verdict

| Case | 30 FPS | 60 FPS |
|---|---|---|
| 1. On-you grub defeated: the "grub defeated" draw has no entry and no displaced glyph | pass | pass |
| 2. Dash off the tile: the first draw after the dash has no entry and no displaced glyph | pass | pass |
| Colour, reverse-video cell | not assessable (text view) | not assessable |

No criterion failure was noticed in these runs.

### Case 1: on-you grub defeated

Script `defeat` (run at `fps 30` and `fps 60`):

```text
fps 30
room empty
player 8 4
spawn grub 8 4
0.2 attack
1.6 attack
end 2.6
```

- The first swipe at 0.2 s hits the grub (1 left). The grub is shown right of `P`, with the entry `on you: … (shown right)`.
- The grub then winds up, hits the player once (1.333 / 1.317), and goes to Recovery.
- At 1.450 the line reads "the grub is open (on you)". The 1.47/1.45 and 1.50 draws both carry `on you: w open (shown right)` with `Pw`. This is the draw just before the defeat.
- The grub stays in Recovery from 1.45 s until about 2.35 s, so it is stationary at the second swipe (1.6). It is still on you then; I did not run a trace to confirm its true position.
- The second swipe at 1.600 prints "grub defeated". "room cleared" follows one tick later (1.633 at 30 FPS, 1.617 at 60).
- **The draw that prints "grub defeated"** is [1.63 s] at 30 FPS and [1.62 s] at 60 FPS. It shows only `P)` and the arc. It has:
  - no `w` anywhere on the map,
  - no `on you:` line,
  - no displaced glyph.
- The next draw ([2.00 s]) and the final draw ([2.50 s]) show `P` alone, with no `on you:` line.
- Both rates are identical in text apart from the draw times (1.63 / 1.62).
- V-17: pass.
- The lines also agree with V-10 and V-18. The "(on you)" lines in this run all have an entry in the same draw. The defeat line carries no position word, as specified.

Limit: this was the last enemy, so "room cleared" printed too. A defeat with another enemy still on the tile was not run.

### Case 2: dash off the tile

Script `dashA` (grub winding up when the player dashes; `fps 30` and `fps 60`):

```text
fps 30
room empty
player 8 4
spawn grub 8 4
0.3 dash up
end 1.5
```

- The draw before the dash is [0.03 s] / [0.02 s]. It shows `PG` and `on you: G biting soon (shown right)`.
- "you dash up" prints at 0.300. **No draw is made at the dash itself**, because dash is not an event in principle 4.
- **The first draw after the dash** is [0.50 s]. It shows `P` at row 1 (mid-dash) and `G` alone at row 4 below, with no `on you:` line and no displaced glyph. It is identical at both rates.
- The grub finishes its strike toward where the player stood. The player takes no heart damage (hearts 3/3).
- "the grub is open (below)" prints at 0.683 / 0.667. The draw at [0.70 s] / [0.67 s] shows `P` at row 0 and `g` at row 3, and the word "below" matches the picture.
- V-17: pass at both rates.

Script `dashB` (grub in Recovery on the tile after a first hit, then dash; `fps 30` and `fps 60`):

```text
fps 30
room empty
player 8 4
spawn grub 8 4
0.2 attack
1.6 dash left
end 2.6
```

- The draw just before the dash is [1.50 s], with `Pw` and `on you: w open (shown right)`.
- "you dash left" prints at 1.600, again with no draw at that moment.
- **The first draw after the dash** is [2.00 s]. It shows `P` at column 4 and `w` alone at column 8, with no `on you:` line and no displaced glyph. The grub is in its own cell, no longer beside `P`.
- The draw at [2.50 s] is the same.
- No hit line, so no heart is lost (the player is invulnerable during the dash). The results are identical at both rates.
- V-17: pass at both rates.

### Observations (not failures)

1. **No draw at the dash.**
   - `combat-visuals.md` ("When the enemy leaves or dies") says the on-you line updates "in the same draw as … the player's dash". Principle 4 lists no dash draw, so the first draw after the dash is up to 0.5 s later: 0.2 s after the dash starts in `dashA`, and 0.4 s in `dashB`.
   - No draw shows a stale entry, so V-17 as written holds.
   - If the art-director wants the clearing to be visible at the moment of the dash, that would be a new draw event, which V-16 forbids without a spec change. This is for the art-director and game-designer to decide.
2. **`dashA` mid-dash draw.** The 0.50 s draw shows the player mid-dash (row 1), not at the dash end. It is still a valid "after" draw: the player is more than 0.5 tile from the grub, and the grub's `G` sits in its own cell.
3. Not run this round: the test suite. 77 stands (71 passed, 2 `ManualTest` errors from the missing `manual.md`, which is an environment matter for the Owner's AC-15 run). No other criterion was re-checked beyond what these runs showed.

### Scripts to re-run

Put each script in a file and run `python3 play.py --view player <file>`.

- Defeat: `fps 30` or `fps 60` as above, with the `defeat` lines.
- Dash with grub winding up: `dashA`, same lines with `fps 30` or `fps 60`.
- Dash with grub open: `dashB`, same lines with `fps 30` or `fps 60`.

## Decisions already made

- D-011, D-012, D-013, D-014, D-015 (applied as written).

## Constraints

- No change to the repo, `manual.md` or the tests. Colour and the reverse-video cell are not claimed either way.

## Open questions

1. **To the art-director:** read Appendix A. Does the lack of a draw at the dash (observation 1) read acceptably?
2. **To the Owner:** the suite run with `manual.md` (AC-15) and the V-15 text, as in 77.

## Expected output

The Studio forwards Appendix A to the art-director. With the Owner steps from 77, V-17 is now covered at both rates.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-visuals.md, design/combat-visuals-verify-rulings.md, design/combat.md, manual.md, repo/
- Decisions: decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md, decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
- Previous handoff: goals/G-001-combat-monotony/82-studio-to-qa.md

---

# Appendix A — verbatim captures (`python3 play.py --view player`)

For `defeat` and `dashB` the output is the full run from the first hit onward. The earlier part (0 to 1.45 s) is the same as A1 in handoff 77 and is cut here. `dashA` is complete.

## A1. Case 1, `defeat`, 30 FPS (from the "open" line before the defeat to the end)

```text
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.600  grub defeated
  1.633  room cleared
   [1.63 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.60 s: hearts 2/3, enemies left 0
```

## A2. Case 1, `defeat`, 60 FPS

```text
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.600  grub defeated
  1.617  room cleared
   [1.62 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.60 s: hearts 2/3, enemies left 0
```

## A3. Case 2, `dashA`, 30 FPS (complete)

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
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
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown right)
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
  0.300  you dash up
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        P       |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (below)
   [0.70 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 3/3, enemies left 1
```

## A4. Case 2, `dashA`, 60 FPS (complete)

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
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
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown right)
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
  0.300  you dash up
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        P       |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (below)
   [0.67 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 3/3, enemies left 1
```

## A5. Case 2, `dashB`, 30 FPS (from the "open" line before the dash to the end)

```text
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.600  you dash left
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.60 s: hearts 2/3, enemies left 1
```

## A6. Case 2, `dashB`, 60 FPS

```text
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.600  you dash left
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.60 s: hearts 2/3, enemies left 1
```
