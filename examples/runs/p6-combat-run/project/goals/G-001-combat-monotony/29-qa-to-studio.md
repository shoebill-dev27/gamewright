---
kind: handoff
goal: G-001
seq: 29
from: qa
to: studio
stage: Verify
outcome: question
---
# 29: qa → studio — second verification round of Build 0.5: no failing criterion, but ManualTest still has no test result, AC-14 is suite-only, and one telegraph-readability gap needs a design ruling

## Task

Report the second verification round of Build 0.5 against `design/combat.md` (AC-1…AC-17) at 30 and 60 FPS. The round covered the manual check, independent runs for the criteria that were suite-only, and raw captures.

## Context

Handoff 28 asked for A (ManualTest and AC-15), B (independent runs) and C (raw captures). I did not edit the build or `manual.md`. All evidence below comes from `run_tests`, `run_play` and `run_trace` output in this step's run results.

## Findings

### Verdict: `question`

No criterion was observed failing. I cannot give `pass` for three reasons:

1. **ManualTest has no valid result.** I could not build the scratch layout, so I only did a static check (section A).
2. **AC-14 is still suite-only.** I did not run a full room clear myself.
3. **A spec gap affects telegraph readability.** When a grub stands on the player's tile, the player view shows no threat glyph (finding F1). The spec is silent on overlap, so this goes to `game-designer`.

Pause (F11) stays not verifiable.

### run_tests totals

- Command: `python3 -m unittest discover -s tests`. Exit 1. 34 tests ran: **33 passed, 0 failed, 1 error**.
- The error is `ManualTest.test_manual_lists_glyphs_and_lines`: `FileNotFoundError: /manual.md`. The run happened with the repo at `/work`, so the test looked in `/`.
- **ManualTest: no test run, no pass/fail mark.**
- **Why the scratch layout was blocked:** `ManualTest` needs `manual.md` in the directory above `repo/`. My allowed writes are this handoff and `@run` blocks, and no `@run` block was allowed to carry `repo/` files or a file in the parent of `repo/`. I cannot create a `manual.md` beside the repo copy, and I did not write into the project's own paths. Fixing this needs a layout where `manual.md` sits beside `repo/` (for example, a QA workspace that allows writing the parent directory).

### A. Static check of the manual (not a test run)

Method: I read the glyph table in `repo/play.py`, the phrases `ManualTest` requires, and `manual.md`, and compared them by eye.

- **Glyphs.** The test looks for each `` `char` `` in the manual. Build glyphs are `P x * ) ( ^ v g G w W s S z Z`. All appear backticked in the manual's On screen table: `P`, `x`, `g`, `G`, `w`, `W`, `s`, `S`, `z`, `Z`, `*`, and `` `)` `(` `^` `v` ``. No difference found.
- **Phrases.** All twelve required phrases appear in `manual.md`. No difference found:
  - "room empty", "rears back", "is open", "charges", "spits", "run over", "press attack to start again"
  - "(miss)", "(too soon)", "(stunned)", "(down)", "room cleared"
- **Result:** the static check found no missing or differing item. This supports AC-15 but is not a test result.
- **Where the practice room is described.** The practice room (`room empty`) appears in the Script table and in "Rooms and runs". The `x` marker is in the On screen table. The practice room is **not** in the On screen section.
  - AC-15 reads "`x` and the practice room are in the manual". By that wording, AC-15 is met.
  - The body text of the spec's Practice room (Q4) section says both must be listed in `manual.md#on-screen`. Taken literally, that is not met for the practice room.
  - I judge AC-15 as met, and I flag the difference between AC wording and body text as a spec question for the game-designer. I did not change anything.

### B. Independent runs, per criterion

"Observed" means I read it in this round's player-view or trace output. "Suite" means a repo test I did not re-derive. Earlier-round observations are marked "round 1".

| AC | Result | Evidence |
|---|---|---|
| AC-1 grub telegraph | pass, observed (and round 1) | Idle player, grub at distance 4: "a grub rears back (right)" and `G` at 1.400 (30 FPS) / 1.383 (60 FPS). First heart lost at 1.967 / 1.933, so about 0.55 s of warning. No heart lost during Approach or Recovery. **See F1** for later bites. |
| AC-2 grub timing | pass, observed (round 1 traces) | Windup→strike 0.500 at both frame rates. Strike→recover 0.167 at 30 FPS and 0.150 at 60 FPS. Recover→next windup 0.900. |
| AC-3 grub dodge | pass, observed | Dash left at 1.500 during the wind-up (1.400–1.900). Hearts stayed 3/3 to the end (3.5 s) at both frame rates. The grub showed `G` at 2.00 with the player 4 tiles away, then "the grub is open" at 2.050 / 2.033. This is one dash timing per frame rate, so the suite's offsets 0 / 0.25 / 0.45 remain suite evidence. |
| AC-4 grub counter | pass, observed | Swipe at 2.500 in Recovery: "grub hit (1 left)" and `w` glyph. Next hit on the player at 3.500 (30 FPS) vs 1.967 before = 1.533 s. At 60 FPS 3.483 vs 1.933 = 1.550 s. |
| AC-5 interrupt | pass, observed | Swipe at 1.600 during the wind-up: "grub hit (1 left)", then "the grub is open (right)" at the same time. Trace at 1.633 (30 FPS): grub `hp=1, recovery, 0.567`, event `recover {'cause': 'interrupted'}` and `knockback`. 60 FPS: `recovery, 0.583` at 1.617. No heart lost from that strike. The next bite is a fresh wind-up at 2.667 / 2.683, with the first hit on the player at 3.233 at both frame rates. |
| AC-6 attack limit | pass (round 1 observed, suite) | Not re-run this round. |
| AC-7 spitter stagger | pass, observed | Room 4 player view at both frame rates: charges at 1.000 (top right) and 1.800 (bottom right), repeats at 3.500 and 4.300. |
| AC-8 spitter telegraph | pass, observed | "spitter (top right) charges" at 1.000 with `S`, and the spit at 1.800 (0.8 s later). Two different lines at 1.800: "spitter (top right) spits" and "spitter (bottom right) charges". No identical duplicate lines at one timestamp (rooms 3, 4, and the single-spitter runs). |
| AC-9 projectile dodge | pass, observed | Spitter at 13,4 (charge 1.000, spit 1.800). **Still player:** "YOU ARE HIT by a shot — hearts 2/3" at 3.367 (30 FPS) / 3.333 (60 FPS). **Move up** 2.0–2.5: hearts 3/3 to the end, the shot passed below. **Dash right** at 3.1: hearts 3/3 to the end, the shot continued past. |
| AC-10 spitter approach | pass for the cancel, observed. The 2-swipe kill is suite only | Cancel: swipe at 1.200 during the charge gives "spitter hit (1 left)" and "spitter (center) is staggered", with no spit at 1.8. The next charge starts at 2.200 (1.0 s after the hit) and spits at 3.000. Same at both frame rates. In room 3 I walked to the top-left spitter and swiped at 2.500: "spitter hit (1 left)", `z` glyph. My first swipe at 2.05 was "(stunned)" because I had walked into a shot at 2.033, so I did not observe the second swipe defeating it. The 2-swipe kill is suite only (`test_walk_up_and_defeat_a_spitter`). |
| AC-11 hit feedback | partial: observed for "hit (1 left)", "(miss)", "(stunned)" and the glyph change. "(too soon)" and "(down)" are suite only | Observed: "you swipe: grub hit (1 left)" with `g`→`w`, "you swipe: spitter hit (1 left)" with `s`→`z`, "you swipe: (miss)" at 0.500 in the multi-hit script, "you swipe: (stunned)" at 2.067 in room 3. No "(nothing happens)" seen. The `G`/`W`/`Z` alert glyphs are distinct from the harmless ones. |
| AC-12 multi-hit | pass, observed | Two grubs inside the cone: two lines at 0.000, "you swipe: grub hit (1 left)" ×2, and the draw shows both as `w`. Same at both frame rates. |
| AC-13 zero hearts | pass, observed (extends round 1) | Room 1, no input: "YOU ARE HIT … 0/3" and "you went down" at 4.967 (30 FPS) / 4.950 (60 FPS). `x` replaces `P`. Trace shows all grubs `approach` (none committed) and `shots=0` after the down. "run over — rooms cleared: 0" and "press attack to start again" at 6.967 / 6.950 (2.000 s after down). An attack at 15.000 printed "a new run begins" and "room 1 begins" with hearts 3/3 and three grubs at their start positions. Room 4 also showed the shots disappear at the down. The "(down)" reason for an attack while down is suite only. |
| AC-14 room clear | pass, suite only | I did not run a full clear (no scripted kill of a whole room, no clear while a strike was due). Suite: `test_room_clear`, `test_clearing_room_5_completes_the_run`. |
| AC-15 practice room and manual | pass by the AC wording, static check only; ManualTest not run | See section A. |
| AC-16 room mix | pass, observed | Room 3 trace setup row: 3 spitters at (2,1), (14,7), (2,7); first charge 1.000 / 1.800 / 2.600. Round 1: room 5 setup row 3 grubs + 2 spitters. Suite: `test_layouts`. |
| AC-17 frame rate | pass for what I observed; the suite-only parts stay suite | The same scripts at 30 and 60 FPS give the same event sequences. Timestamp differences are at most 0.034 s: windup 1.400/1.383, first hit 1.967/1.933, down 5.033/5.000, run over 6.967/6.950. Spits, charges and the dash landing match exactly (dash left 4 tiles: `P` from column 8 to 4 at both). The Strike ≥4 frames at 30 FPS check is suite only. |

### Findings that are not criterion failures

- **F1 (spec gap, for game-designer): the threat glyph is hidden when a grub is on the player's tile.**
  - After a few bites the grub ends up at the player's position (`side: on you`). The player is drawn last, so only `P` shows.
  - Evidence, idle 30 FPS: at 4.500 the line "a grub rears back (on you)" prints, and the draw at 4.50 shows only `P`. The hit lands at 5.033. Room 1 shows the same at 3.57–4.50.
  - The Conventions define a telegraph as at least one on-map change plus a text line. In that situation the on-map change is missing, and pillar 3 says every threat is visible before it hurts.
  - AC-1 itself (first bite from distance 4) is met. The spec is silent on whether enemies may overlap the player. Needed: a ruling (keep distance, or draw the threat). Not marked a failure.
- **F2 (cosmetic): out-of-order timestamps in the player view.** At 30 FPS in room 4 with a dash, "2.600 spitter (bottom right) spits" prints before "2.583 the grub is open (left)", and "3.500 … charges" before "3.483 a grub rears back (left)". Nothing in the spec is affected.
- **Run-over timing.** In a practice room (grub only) the session ends after the down without a run-over screen, as designed (`end at 7.03 s`).

### Answer on color

- With the `run_play` command as given (no `--color`, output not a terminal), the player view is **plain text**. None of the captures contain ANSI codes or markup.
- From `play.py`: color is added only with `--color` or when stdout is a terminal. Then each glyph is wrapped like `ESC[38;5;229mPESC[0m` (lantern yellow for the player), with `ESC[1;38;5;202m` for alert enemies and `ESC[1;38;5;196m` for shots. I did not capture a colored run, so this is from reading the code. The glyphs carry every state without color.

### Captures

All output is verbatim from this step's runs. Cuts are marked `[cut: …]`. Where I cut draws, every text line (events) is kept in order. Draws are kept at the events named in each heading. Each capture is shown at 30 FPS and 60 FPS.

#### C1. Practice room, one grub, idle player (`room empty`, `player 8 4`, `spawn grub 12 4`, `end 8`) — 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 0.50 s and 1.00 s; grub walking left, player unchanged]
  1.400  a grub rears back (right)
   [1.40 s] hearts 3/3
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
[cut: draw at 1.50 s, identical to the 1.40 s draw]
  1.967  YOU ARE HIT by a grub — hearts 2/3
   [1.97 s] hearts 2/3
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
[cut: draw at 2.00 s, identical]
  2.050  the grub is open (right)
   [2.07 s] hearts 2/3
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
[cut: draw at 2.50 s, identical to the 2.07 s draw]
  2.950  a grub rears back (right)
[cut: draws at 2.97 s, 3.00 s: only `P` in the room]
  3.467  YOU ARE HIT by a grub — hearts 1/3
[cut: draws at 3.47 s, 3.50 s]
  3.600  the grub is open (on you)
[cut: draws at 3.60 s, 4.00 s: only `P`]
  4.500  a grub rears back (on you)
   [4.50 s] hearts 1/3
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
[cut: draw at 5.00 s]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
   [5.03 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 5.50, 6.00, 6.50, 7.00 s, all with `x` alone]
end at 7.03 s: hearts 0/3, enemies left 1
```

60 FPS (same script):

```text
Lantern Depths 0.5 — room empty — 60 FPS
[cut: draws at 0.00, 0.50, 1.00 s; same as 30 FPS]
  1.383  a grub rears back (right)
   [1.38 s] hearts 3/3
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
[cut: draw at 1.50 s, identical]
  1.933  YOU ARE HIT by a grub — hearts 2/3
   [1.93 s] hearts 2/3
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
[cut: draw at 2.00 s (only `P`)]
  2.033  the grub is open (right)
[cut: draws at 2.03, 2.50 s]
  2.933  a grub rears back (right)
[cut: draws at 2.93, 3.00 s]
  3.450  YOU ARE HIT by a grub — hearts 1/3
[cut: draws at 3.45, 3.50 s]
  3.583  the grub is open (on you)
[cut: draws at 3.58, 4.00 s]
  4.483  a grub rears back (on you)
   [4.48 s] hearts 1/3
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
[cut: draw at 4.50 s]
  5.000  YOU ARE HIT by a grub — hearts 0/3
  5.000  you went down
   [5.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 5.50, 6.00, 6.50, 7.00 s]
end at 7.00 s: hearts 0/3, enemies left 1
```

Trace for timing (30 FPS, selected lines; full trace was run):

```text
t=1.400 frame=42 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.900 frame=57 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=1.967 frame=59 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
```

#### C2. Same, `1.6 attack` during the wind-up (`end 5`) — 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
[cut: draws at 0.00, 0.50, 1.00 s; as in C1]
  1.400  a grub rears back (right)
   [1.40 s] hearts 3/3
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
[cut: draw at 1.50 s, identical]
  1.600  you swipe: grub hit (1 left)
  1.600  the grub is open (right)
   [1.63 s] hearts 3/3
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
[cut: draws at 2.00, 2.50 s: `P w`]
  2.667  a grub rears back (right)
   [2.67 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 3.00 s, identical]
  3.233  YOU ARE HIT by a grub — hearts 2/3
  3.317  the grub is open (right)
[cut: draws at 3.23, 3.33, 3.50, 4.00 s]
  4.217  a grub rears back (right)
[cut: draws at 4.23, 4.50 s]
  4.733  YOU ARE HIT by a grub — hearts 1/3
  4.867  the grub is open (on you)
[cut: draws at 4.73, 4.87, 5.00 s]
end at 5.00 s: hearts 1/3, enemies left 1
```

Trace line at the swipe (30 FPS): 

```text
t=1.633 frame=49 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.42,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0}
```

60 FPS (same script):

```text
Lantern Depths 0.5 — room empty — 60 FPS
[cut: draws at 0.00, 0.50, 1.00 s]
  1.383  a grub rears back (right)
[cut: draws at 1.38, 1.50 s: `PG`]
  1.600  you swipe: grub hit (1 left)
  1.600  the grub is open (right)
   [1.62 s] hearts 3/3
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
[cut: draws at 2.00, 2.50 s]
  2.683  a grub rears back (right)
[cut: draws at 2.68, 3.00 s: `PW`]
  3.233  YOU ARE HIT by a grub — hearts 2/3
  3.333  the grub is open (right)
[cut: draws at 3.23, 3.33, 3.50, 4.00 s]
  4.233  a grub rears back (right)
[cut: draws at 4.23, 4.50 s]
  4.750  YOU ARE HIT by a grub — hearts 1/3
  4.883  the grub is open (on you)
[cut: draws at 4.75, 4.88, 5.00 s]
end at 5.00 s: hearts 1/3, enemies left 1
```

Trace line at the swipe (60 FPS):

```text
t=1.617 frame=97 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.33,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0}
```

#### C3. Same, `2.5 attack` during the recovery (`end 6`) — 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
[cut: draws at 0.00 to 1.50 s, as in C1; wind-up line follows]
  1.400  a grub rears back (right)
  1.967  YOU ARE HIT by a grub — hearts 2/3
  2.050  the grub is open (right)
[cut: draws at 1.40, 1.50, 1.97, 2.00, 2.07 s, as in C1]
  2.500  you swipe: grub hit (1 left)
   [2.53 s] hearts 2/3
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
  2.950  a grub rears back (right)
   [2.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 3.00 s, identical]
  3.500  YOU ARE HIT by a grub — hearts 1/3
  3.600  the grub is open (right)
[cut: draws at 3.50, 3.60, 4.00 s]
  4.500  a grub rears back (right)
[cut: draws at 4.50, 5.00 s]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
[cut: draws at 5.03, 5.50, 6.00 s: `x`]
end at 6.00 s: hearts 0/3, enemies left 1
```

60 FPS: swipe at 2.500 "you swipe: grub hit (1 left)" (draw [2.52 s] identical to the one above), then 2.933 "a grub rears back (right)", 3.483 "YOU ARE HIT … 1/3", 3.583 "the grub is open (right)", 4.483 "a grub rears back (right)", 5.000 "YOU ARE HIT … 0/3" / "you went down", `end at 6.00 s`. Lines kept as printed; draws cut.

#### C4. Room 4, `0.5 move left`, `end 8` — 30 FPS (draws only at key events)

```text
Lantern Depths 0.5 — room 4 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | g      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
[cut: draw at 0.50 s]
  1.000  spitter (top right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |  g             |
   |                |
   |   g  P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.300  a grub rears back (left)
   [1.30 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |  g             |
   |                |
   |    GP          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
[cut: draw at 1.50 s]
  1.733  a grub rears back (above)
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
  1.833  YOU ARE HIT by a grub — hearts 2/3
  1.950  the grub is open (right)
  2.383  the grub is open (above)
  2.600  spitter (bottom right) spits
  2.850  a grub rears back (right)
  3.283  a grub rears back (above)
  3.367  YOU ARE HIT by a grub — hearts 1/3
  3.500  spitter (top right) charges
  3.500  the grub is open (on you)
  3.933  the grub is open (on you)
  4.300  spitter (top right) spits
  4.300  spitter (bottom right) charges
  4.400  a grub rears back (on you)
  4.833  a grub rears back (on you)
[cut: draws for 1.73 to 4.83 s; all text lines above kept, in order]
  4.933  YOU ARE HIT by a grub — hearts 0/3
  4.933  you went down
   [4.93 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |   x            |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
[cut: draws at 5.00, 5.50, 6.00, 6.50 s, all like the 4.93 s draw]
  6.933  run over — rooms cleared: 0
  6.933  press attack to start again
end at 6.93 s: hearts 0/3, enemies left 4
```

60 FPS (same script), text lines as printed: 1.000 "spitter (top right) charges"; 1.300 "a grub rears back (left)"; 1.733 "a grub rears back (above)"; 1.800 "spitter (top right) spits" and "spitter (bottom right) charges"; 1.817 "YOU ARE HIT by a grub — hearts 2/3"; 1.950 "the grub is open (right)"; 2.383 "the grub is open (above)"; 2.600 "spitter (bottom right) spits"; 2.850 "a grub rears back (right)"; 3.283 "a grub rears back (above)"; 3.367 "YOU ARE HIT by a grub — hearts 1/3"; 3.500 "spitter (top right) charges" and "the grub is open (on you)"; 3.933 "the grub is open (on you)"; 4.300 "spitter (top right) spits" and "spitter (bottom right) charges"; 4.400 "a grub rears back (on you)"; 4.833 "a grub rears back (on you)"; 4.917 "YOU ARE HIT by a grub — hearts 0/3" and "you went down" (draw [4.92 s] has `x` at column 4 and shots gone); 6.917 "run over — rooms cleared: 0" and "press attack to start again"; `end at 6.92 s: hearts 0/3, enemies left 4`. Draws cut.

#### C5. Room 4, `0.5 dash left`, `end 8` — 30 FPS

```text
Lantern Depths 0.5 — room 4 — 30 FPS
[cut: draws at 0.00, 0.50 s, as in C4]
  0.500  you dash left
  0.900  a grub rears back (left)
   [0.90 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |  g             |
   |                |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.000  spitter (top right) charges
  1.467  YOU ARE HIT by a grub — hearts 2/3
  1.550  the grub is open (left)
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
  1.933  a grub rears back (left)
  2.450  a grub rears back (left)
  2.500  YOU ARE HIT by a grub — hearts 1/3
  2.600  spitter (bottom right) spits
  2.583  the grub is open (left)
  3.100  the grub is open (on you)
  3.500  spitter (top right) charges
  3.483  a grub rears back (left)
[cut: draws between 1.00 and 3.50 s; text lines kept in printed order]
  4.000  YOU ARE HIT by a grub — hearts 0/3
  4.000  you went down
[cut: draws at 4.00 to 5.50 s]
  6.000  run over — rooms cleared: 0
  6.000  press attack to start again
end at 6.00 s: hearts 0/3, enemies left 4
```

60 FPS lines: 0.500 "you dash left"; 0.883 "a grub rears back (left)"; 1.000 charge; 1.433 "YOU ARE HIT … 2/3"; 1.533 open; 1.800 spit + charge; 1.917 rears back; 2.433 rears back; 2.467 "YOU ARE HIT … 1/3"; 2.567 open; 2.600 "spitter (bottom right) spits"; 3.083 "the grub is open (on you)"; 3.467 rears back; 3.500 "spitter (top right) charges"; 3.983 "YOU ARE HIT … 0/3" / "you went down"; 5.983 "run over — rooms cleared: 0" / "press attack to start again"; `end at 5.98 s`.

#### C6. Room 3, walk up to a spitter and attack twice (`0 move up`, `0.75 move left`, `2.0 stop`, `2.05 attack`, `2.5 attack`, `end 3.5`) — 30 FPS

```text
Lantern Depths 0.5 — room 3 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
[cut: draw at 0.50 s]
  1.000  spitter (top left) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  S    P        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
[cut: draw at 1.50 s]
  1.800  spitter (top left) spits
  1.800  spitter (bottom right) charges
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |  s P           |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           S |
   |                |
   +----------------+
[cut: draw at 2.00 s]
  2.033  YOU ARE HIT by a shot — hearts 2/3
   [2.03 s] hearts 2/3
   +----------------+
   |                |
   |  sP            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           S |
   |                |
   +----------------+
  2.067  you swipe: (stunned)
[cut: draw at 2.50 s, identical to the 2.03 s draw]
  2.500  you swipe: spitter hit (1 left)
   [2.53 s] hearts 2/3
   +----------------+
   |  (             |
   |  zP            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           S |
   |                |
   +----------------+
  2.600  spitter (bottom right) spits
  2.600  spitter (bottom left) charges
[cut: draws at 2.60, 3.00 s]
  3.400  spitter (bottom left) spits
  3.500  spitter (top left) charges
[cut: draws at 3.40, 3.50 s; at 3.50 s the hit spitter shows `Z`]
end at 3.50 s: hearts 2/3, enemies left 3
```

60 FPS (same script): the same sequence: 1.000 charge, 1.800 spit + "spitter (bottom right) charges", 2.017 "YOU ARE HIT by a shot — hearts 2/3", 2.050 "you swipe: (stunned)", 2.500 "you swipe: spitter hit (1 left)" (draw [2.52 s] shows `(` above and below the `zP` row), 2.600 spit + "spitter (bottom left) charges", 3.400 spit, 3.500 "spitter (top left) charges", `end at 3.50 s: hearts 2/3, enemies left 3`.

#### C7. Room 1, no input, then `15 attack` after the run-over screen (`end 20`) — 30 FPS

```text
Lantern Depths 0.5 — room 1 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 0.50, 1.00 s]
  1.400  a grub rears back (above)
  1.900  a grub rears back (left)
  1.967  YOU ARE HIT by a grub — hearts 2/3
  2.050  the grub is open (above)
  2.550  the grub is open (left)
  2.900  a grub rears back (right)
  2.950  a grub rears back (above)
  3.467  YOU ARE HIT by a grub — hearts 1/3
  3.550  the grub is open (right)
  3.567  a grub rears back (left)
  3.600  the grub is open (on you)
  4.217  the grub is open (on you)
  4.450  a grub rears back (right)
  4.500  a grub rears back (on you)
[cut: draws between 1.40 and 4.50 s; text lines kept]
  4.967  YOU ARE HIT by a grub — hearts 0/3
  4.967  you went down
   [4.97 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 5.00, 5.50, 6.00, 6.50 s, all `x` alone]
  6.967  run over — rooms cleared: 0
  6.967  press attack to start again
 15.000  a new run begins
 15.000  room 1 begins
   [15.03 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: second run, identical to the first from 15.50 s; lines kept:]
 16.400  a grub rears back (above)
 16.900  a grub rears back (left)
 16.967  YOU ARE HIT by a grub — hearts 2/3
 17.050  the grub is open (above)
 17.550  the grub is open (left)
 17.900  a grub rears back (right)
 17.950  a grub rears back (above)
 18.467  YOU ARE HIT by a grub — hearts 1/3
 18.550  the grub is open (right)
 18.567  a grub rears back (left)
 18.600  the grub is open (on you)
 19.217  the grub is open (on you)
 19.450  a grub rears back (right)
 19.500  a grub rears back (on you)
 19.967  YOU ARE HIT by a grub — hearts 0/3
 19.967  you went down
[cut: draws in this second run]
end at 20.00 s: hearts 0/3, enemies left 3
```

60 FPS: down at 4.950 ("YOU ARE HIT by a grub — hearts 0/3", "you went down"), "6.950  run over — rooms cleared: 0", "6.950  press attack to start again", " 15.000  a new run begins", " 15.000  room 1 begins" (draw [15.02 s] same as the start layout, hearts 3/3), second run down at 19.950, `end at 20.00 s: hearts 0/3, enemies left 3`. The full trace (60 FPS) shows `run_over {'rooms': 0, 'complete': False}` at t=6.950 and `run_start; room_loaded {'room': '1'}` at t=15.017 with hearts=3.

#### C8. Independent checks (AC-3, AC-9, AC-10, AC-12)

AC-3, grub dash during wind-up (`spawn grub 12 4`, `1.5 dash left`, `end 3.5`), 30 FPS:

```text
  1.400  a grub rears back (right)
   [1.40 s] hearts 3/3
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
[cut: draw at 1.50 s]
  1.500  you dash left
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P    G      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.050  the grub is open (right)
[cut: draws at 2.07 to 3.50 s: `P   g`]
end at 3.50 s: hearts 3/3, enemies left 1
```

60 FPS: wind-up 1.383, "1.500 you dash left", draw [2.00 s] `|    P   G       |`, "2.033 the grub is open (right)", `end at 3.50 s: hearts 3/3, enemies left 1`.

AC-9 still / side-step / dash through (spitter at 13,4, player 8,4, `end 4.2`). Text lines at 30 FPS; 60 FPS differs only as noted.

```text
-- still --
  1.000  spitter (right) charges
  1.800  spitter (right) spits
  3.367  YOU ARE HIT by a shot — hearts 2/3
  3.500  spitter (right) charges
end at 4.20 s: hearts 2/3, enemies left 1
(60 FPS: hit at 3.333)
-- move up 2.0, stop 2.5 --
  1.000  spitter (right) charges
  1.800  spitter (right) spits
  3.500  spitter (right) charges
end at 4.20 s: hearts 3/3, enemies left 1
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |           * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
-- dash right 3.1 --
  1.000  spitter (right) charges
  1.800  spitter (right) spits
  3.100  you dash right
  3.500  spitter (right) charges
end at 4.20 s: hearts 3/3, enemies left 1
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        *   PS  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
```

The 60 FPS runs print the same lines and draws (still: hit at 3.333; side-step and dash: hearts 3/3 at the end).

AC-10 hit during the charge (`spawn spitter 9.2 4`, `1.2 attack`, `end 3.0`), 30 FPS:

```text
  1.000  spitter (center) charges
  1.200  you swipe: spitter hit (1 left)
  1.200  spitter (center) is staggered
   [1.23 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pz      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 1.50, 2.00 s: `Pz`]
  2.200  spitter (center) charges
   [2.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PZ      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 2.50 s]
  3.000  spitter (center) spits
[cut: draw at 3.00 s]
end at 3.00 s: hearts 3/3, enemies left 1
```

60 FPS: identical lines (1.000, 1.200 ×2, 2.200, 3.000), draw [1.22 s] same as above, `end at 3.00 s: hearts 3/3, enemies left 1`. The spit at 3.000 hit nothing because the player stayed at hearts 3/3 (the shot flies away from the adjacent spitter; I did not trace where it went).

AC-12 multi-hit (`spawn grub 9.2 4`, `spawn grub 9 3.2`, `0 attack`, `0.5 attack`, `end 1.5`), 30 FPS:

```text
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: grub hit (1 left)
  0.000  you swipe: grub hit (1 left)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         w      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 0.50 s]
  0.500  you swipe: (miss)
[cut: draw at 0.53 s]
  0.700  a grub rears back (right)
  0.733  a grub rears back (right)
  1.267  YOU ARE HIT by a grub — hearts 2/3
  1.350  the grub is open (right)
  1.383  the grub is open (right)
[cut: draws at 0.70 to 1.50 s]
end at 1.50 s: hearts 2/3, enemies left 2
```

60 FPS: the same lines at 0.000 (two hit lines), 0.500 "(miss)", 0.683 and 0.717 "a grub rears back (right)", 1.233 hit, 1.333 and 1.367 "the grub is open (right)", `end at 1.50 s: hearts 2/3, enemies left 2`.

## Decisions already made

- D-001: attack, dash and pause are the only inputs. No new input seen.
- D-002: Option A. D-003: room mix across rooms, zero hearts ends the run (confirmed in C7), +1 heart on clear (not observed this round). D-004: one change set. D-005: `manual.md` not edited.

## Constraints

- I verified at 30 and 60 FPS where noted. I did not edit the build or `manual.md`.
- Suite evidence and own observation are labeled separately in the table.

## Open questions

1. **For the Owner or Studio (ManualTest):** run `python3 -m unittest discover -s tests` in a layout with `manual.md` beside a `repo/` copy. A QA workspace that allows writing the parent of `repo/`, or an Owner-placed `manual.md` in the QA workspace, would do it. Until then ManualTest has no pass/fail. The static check found no difference.
2. **For game-designer (F1):** may a grub stand on the player's tile? If yes, how must the telegraph read there? Today the only signal is the text line while the map shows `P`.
3. **For game-designer (AC-15 wording):** must the practice room be listed in the On screen section (Q4 body text), or is the Script and Rooms-and-runs mention enough (AC-15 wording)?
4. **Not covered, if a further round is allowed:** a full room clear observed by me (heal, projectiles removed, 1.5 s, next room, clearing swipe on a strike tick, "run complete"), and the "(too soon)" and "(down)" lines in the player view. These remain suite-only.

## Expected output

The studio decides on the `manual.md` layout (question 1) and routes F1 and the AC-15 wording to the game-designer. If ManualTest then passes and the studio accepts AC-14 as suite evidence, the verdict can become `pass`. No defect is routed to `gameplay-engineer` unless the designer's ruling on F1 requires a build change.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: project.md, design/combat.md, manual.md
- Decisions: decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/28-studio-to-qa.md
