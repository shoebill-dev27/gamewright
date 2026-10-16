# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/19-studio-to-qa.md
next_seq: 20
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/20-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/19-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 19
from: studio
to: qa
stage: Verify
outcome: routed
---
# 19: studio → qa — Verify build 0.5 against criteria 1–16 and V12; settle 16e from the new log

## Task

Verify the current build (`repo/`, sha 29993eac7bb0) independently against the combat acceptance criteria 1–16 and the timing item V12 of the visual spec. Specifically close criterion 16e (frame-rate behavior of the walker bot) using the richer `log on` output.

## Context

Goal G-001 ("戦闘が単調なので改善したい", combat feels monotonous). Build 0.5 added combat variety. The designer ruled criteria 13–16 and confirmed five spec defaults. QA's earlier check found the walker bot's 30 and 60 FPS runs differ, with no build defect shown, but 16e could not be proven because the log had no positions. A tooling step has since made the bot log carry decision-time state. Per the designer's ruling, the walker only has to meet 13 and 14 at each frame rate, and the dodger must agree across rates (16c).

## Findings

Facts about what changed since your last report (no judgment attached; verify them yourself):

- `repo/bots.py` changed in its logging only. Bot decisions are meant to be unchanged.
- `repo/tests/test_game.py`: the walker `expectedFailure` test was replaced by a test of criteria 13 and 14 at each rate. Two tests were added for the log. `repo/README.md` describes the new log.
- `repo/game.py`, `repo/play.py` and `design/combat.md` are not meant to have changed.
- `log on` now adds, after each decision line, ` | frame, grid time, frame time, player position, hearts, stun state, nearest enemy position and exact distance, shots in flight`. It also adds heart-loss lines and skipped-decision lines (while the player is stunned). See `repo/README.md` for the format.
- Commands (from the project): tests `python3 -m unittest discover -s tests`; bots `python3 bots.py {script}`; player view `python3 play.py --view player {script}`; trace `python3 play.py --view trace {script}`. Run from `repo/`. The script syntax is in `repo/manual.md`; the log switch and frame-rate options are in `repo/README.md`.

Scope of the verification:

1. Criteria 1–16 in `design/combat.md`, including the designer's rulings for 13–16 (see handoff 14).
2. 16e: run the walker bot in room 3 with `log on` at 30 and 60 FPS. Compare decisions and states by the 16e rule as ruled. State whether any frame-rate-dependent graze at the contact edge exists. Also report whether the first walker difference in room 1 at 0.30 s is explained by the exact distance values in the log.
3. Regression check: bot results with `log on` versus log off, and the existing tests.
4. V12 only (timing of the cues), from the art review (handoff 15). V1–V11 concern a future graphical build and are out of scope. Report, but do not rule on, any contradiction between `design/combat.md` and `design/combat-cues-visual-spec.md`.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Designer's rulings on criteria 13–16 and the five spec defaults (handoff 14, Findings).

## Constraints

- Judge from the spec, the acceptance criteria and the build only.
- Supported frame rates: 30 and 60 FPS.
- Do not edit the game. Report failures with a reproduction.
- If one criterion fails for the second time, the Studio re-plans via `technical-director`; report precisely which criterion and how.

## Open questions

- Does 16e hold, or does the log show a frame-rate-dependent graze at the contact edge? If it does, state it as a finding. The designer decides whether it is acceptable.

## Expected output

A pass/fail report per criterion (1–16, V12) with reproduction steps for any failure, and a clear 16e conclusion. Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-cues-visual-spec.md (V12), repo/manual.md, repo/README.md, repo/bots.py, repo/tests/test_game.py, repo/game.py, repo/play.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none. Read these only in the sections named, ignoring any `## Sender assessment`:
  - goals/G-001-combat-monotony/14-game-designer-to-studio.md#findings (the criteria rulings and checklist items 1–6)
  - goals/G-001-combat-monotony/15-art-director-to-studio.md#findings (V12 only)
  - goals/G-001-combat-monotony/16-qa-to-studio.md#findings (your earlier divergence report)
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

<<<FILE design/combat-cues-visual-spec.md
# Combat cue visual spec (build 0.5 cues, for the graphical build)

Owner: art-director. Source: G-001 step 15. Basis: the text view and `design/combat.md`. I did not see a rendered build. Timings and rules are unchanged and belong to the game-designer.

## Principles

- Threat cues are saturated orange-red and **self-lit**. They do not depend on the lantern, so a cue reads in full darkness.
- The lantern is warm, pale and low-saturation (amber to cream). Threat cues are more saturated and shifted toward red, and they are the brightest saturated thing on screen.
- **Color is never the only signal.** Every cue also differs in shape or motion, so it holds up for color-blind players and under lantern tint.
- Reuse existing assets: one orange-red palette entry, one additive glow sprite, one line/quad sprite. All variants are parameter changes (scale, rate), not new assets.

## Grub lunge cue (Standard, Runner, Brute)

1. **Lane, not a hairline.** The lunge path is drawn as a band along the locked direction, 2.4 tiles long. Its width equals the actual danger zone, 1.2 tiles (0.6 either side). It is a translucent orange-red fill with a brighter hazard edge.
   - Reason: the design text says "thin line" but the danger is 1.2 tiles wide. A hairline makes a 1-tile sidestep look sufficient when it may not be.
   - Players should be able to see that stepping 1 tile sideways takes them clear of the band.
2. **Onset.** The grub flash and the lane appear at full contrast on the first frame of wind-up, with no fade-in. This matters for the Runner, whose wind-up is 0.35 s, about 10 frames at 30 FPS.
3. **Duration visibility.** The lane fills from the grub outward, or its fill brightens, so that it is complete exactly when the lunge starts. The player can judge the time left without reading text.
4. **Grub body.** The grub holds a steady orange-red tint with a slight pulse, and rears back by squashing away from the lunge direction. Do not strobe. Keep flashing at or below 3 Hz.
5. **End of cue.** The lane stays at full strength until the lunge starts, then fades during the lunge. The flash and tint stop when recovery begins, and the grub returns to its neutral cool color. A grub that is neutral and not tinted means "safe to swipe".
6. **Stagger.** A cancelled wind-up (swipe) removes the lane immediately and shows a hit reaction, so a cancelled lunge is not mistaken for a pending one.

### Variants

Differentiate by silhouette and size first, then by cue cadence. Do not use a different hue.

| Variant | Body | Lane | Cue cadence |
|---|---|---|---|
| Runner `r` | smallest, lean | full 1.2 width | fast pulse, ends in 0.35 s |
| Standard `g` | medium | full 1.2 width | medium pulse, 0.5 s |
| Brute `G` | largest, heavy | full 1.2 width | slow pulse, 0.7 s |

The lane geometry is identical, so lane width never depends on variant. All three share the lunge distance.

## Spitter aim cue

1. **Glow.** An orange-red additive glow on the spitter ramps from a **floor of at least 30% to 100%** over the 0.6 s. The text view shows 0% at the start. Do not render 0% as invisible. The cue must be noticeable on the first frame.
2. **Aim line.** A **thin** orange-red line, visually narrower than the grub lane. It runs from the spitter along the locked direction to the room edge. It is visible from the first frame of the cue at full line brightness. Only the glow ramps.
3. **End of cue.** At the shot the line disappears (it does not linger), the glow drops to neutral, and a projectile starts. The line must not be readable as a stationary shot.
4. **Distance.** The spitter glow and the line are self-lit. They must be visible when the spitter is outside the lantern radius, including in the far corners of the 16-by-9 room.
5. **Killed during cue.** The line and the glow disappear at once (the shot is cancelled).

## Shot `*`

- A compact **round** orange-red core with a short bright trail, brighter than the line, always moving.
- It must differ from the aim line by shape (a round object vs a straight line) and by motion.
- It must be readable against the lantern light and against a lane or line behind it. Give the core a light outline or a hot white center so it does not merge with a same-colored lane.

## Telling cues apart on one screen

| Thing | Shape | Motion/time signal |
|---|---|---|
| Grub lunge | wide band, short (2.4 tiles) | fills up, then the grub moves |
| Spitter aim | thin line, long (to edge) | glow ramps, then the line vanishes |
| Shot | round core with trail | moves at 3 tiles/s |
| Lantern | soft round warm pool, low saturation | static around the player |

At most one grub cue is active at once (rule). Spitter cues are normally 0.8 s apart and last 0.6 s, so they rarely overlap. They can overlap after a cap delay, and then the two aim lines must still be readable. They are identical in style, and the glow plus the line origin tell them apart.

## Player-observable acceptance criteria

V1. In a dark room with the player far from a grub, the player can see the cue (flash plus lane) without the lantern reaching it.
V2. A first-time player can state where the lunge will go and how wide it is, and can tell a 1-tile sidestep clears it.
V3. The cue is visible from the very first frame of the wind-up, including the Runner's 0.35 s, at both 30 and 60 FPS.
V4. The player can tell, without text, how much time is left before the lunge or the shot.
V5. A Runner, Standard grub and Brute are told apart by silhouette alone, in grayscale.
V6. A grub lane and a spitter aim line are told apart in grayscale (wide band vs thin line).
V7. The aim line, the shot and the lane never merge. A shot passing over a lane is still seen.
V8. A recovering or staggered grub looks clearly neutral (no tint). A player can tell when it is safe to swipe.
V9. No cue flashes faster than 3 Hz.
V10. A cancelled or killed enemy's cue disappears at once.
V11. The orange-red threat color is never confused with the warm lantern light. A threat inside the lantern radius is still clearly redder and more saturated than the lit floor.
V12. Cue timing in the graphical build matches the text-view timings at 30 and 60 FPS, within one frame.
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
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  log on                      print each bot's decisions under its room line: time, what it did,
                              and the state it decided from (after " | "); skipped decisions and
                              every heart lost are logged too

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
    SHOT_LIFE,
    SHOT_REACH,
    SHOT_SPEED,
    Game,
)

REACTION = 0.15  # seconds between a bot's decisions, like play.py's rule reaction time
LUNGE_LEN = LUNGE_SPEED * LUNGE_TIME


class Brain:
    """The bot's reaction clock (accumulated seconds) and decision log."""

    def __init__(self, log=None):
        self.next, self.log = 0.0, log
        self.grid = 0.0  # log only: the last grid time passed by the last decision
        self.shadow = 0.0  # log only: a copy of the clock that also runs while the player is stunned

    def due(self, t):
        if t < self.next - 1e-9:
            return False
        while self.next <= t + 1e-9:
            self.grid = self.next
            self.next += REACTION
        self.shadow = self.next
        return True

    def note(self, game, text):
        if self.log is not None:
            self.log.append(f"{game.t:6.2f} s  {text} | {_state(game, self.grid)}")

    def skip(self, game):
        """Log a grid decision that is skipped because the player is stunned (once per grid time)."""
        t = game.t
        if self.log is None or t < self.shadow - 1e-9:
            return
        grid = self.shadow
        while self.shadow <= t + 1e-9:
            grid = self.shadow
            self.shadow += REACTION
        self.log.append(
            f"{t:6.2f} s  skipped decision | frame {game.frame}, grid {grid:.3f} s, "
            f"frame time {t:.6f} s, reason: player stunned ({game.stun_left:.3f} s of stun left)"
        )


def _state(game, grid):
    """The state a decision is made from, as one line of text (log only)."""
    enemy = _nearest(game)
    if enemy:
        distance = math.hypot(enemy.x - game.x, enemy.y - game.y)  # same expression the bots compare
        near = (
            f"nearest {enemy.kind} at ({enemy.x:.6f}, {enemy.y:.6f}) "
            f"distance {distance:.9f} (exact {distance!r})"
        )
    else:
        near = "nearest none"
    shots = (
        "; ".join(f"({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in game.shots)
        or "none"
    )
    stun = f"yes ({game.stun_left:.3f} s left)" if game.stun_left > 0 else "no"
    return (
        f"frame {game.frame}, grid {grid:.3f} s, frame time {game.t:.6f} s, "
        f"player ({game.x:.6f}, {game.y:.6f}), hearts {game.hearts}, stunned {stun}, "
        f"{near}, shots in flight: {shots}"
    )


def _hurt_lines(game, first_event, shots_before, struck_before):
    """Log lines for the hearts lost in the frame just played (log only; reads, never changes)."""
    out = []
    for when, kind, details in game.events[first_event:]:
        if kind != "hurt":
            continue
        source = details["source"]
        if source == "grub":
            hit = [e for e in game.enemies if e.is_grub and e.struck and not struck_before.get(id(e))]
            there = (
                ", ".join(f"grub {e.kind} at ({e.x:.6f}, {e.y:.6f})" for e in hit)
                or "grub position not found"
            )
        else:
            gone = [
                s
                for s in shots_before
                if not any(s is k for k in game.shots)
                and s[4] < SHOT_LIFE - 1e-9
                and -1 <= s[0] <= ROOM_W
                and -1 <= s[1] <= ROOM_H
                and math.hypot(s[0] - game.x, s[1] - game.y) <= SHOT_REACH
            ]
            there = (
                ", ".join(
                    f"shot at ({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in gone
                )
                or "shot position not found (fired in this frame)"
            )
        out.append(
            f"{when:6.2f} s  HEART LOST | frame {game.frame}, source {source}, "
            f"player ({game.x:.6f}, {game.y:.6f}), {there}; hearts now {details['hearts']}"
        )
    return out


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
        if game.stun_left <= 0:
            if brain.due(game.t):
                bot(game, lambda text: brain.note(game, text))
        else:
            brain.skip(game)  # log only: a grid decision that the stun swallows
        if brain.log is not None:
            first_event = len(game.events)
            shots_before = list(game.shots)
            struck_before = {id(e): e.struck for e in game.enemies if e.is_grub}
        game.step()
        if brain.log is not None:
            brain.log.extend(_hurt_lines(game, first_event, shots_before, struck_before))
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

    def test_walker_meets_criteria_13_and_14_at_each_rate(self):
        # Criterion 16d: the walker's per-room numbers may differ between rates (its 0.15 s
        # decision grid lands on different frames); it only has to meet 13 and 14 at each rate.
        import bots

        for fps in (30, 60):
            result = {
                name: {room: bots.play_room(bot, room, fps, 60) for room in "12345"}
                for name, bot in bots.BOTS.items()
            }

            def lost(name, rooms):
                return sum(result[name][r]["hearts_lost"] for r in rooms)

            def cleared(name, rooms):
                return sum(result[name][r]["cleared"] for r in rooms)

            # 13: rooms 3-5 summed.
            walker_lost = lost("walker", "345")
            self.assertTrue(3 <= walker_lost <= 6, (fps, walker_lost))
            self.assertGreaterEqual(cleared("walker", "345"), 2, fps)
            self.assertLessEqual(lost("dodger", "345"), walker_lost / 2, fps)
            self.assertEqual(cleared("dodger", "345"), 3, fps)
            self.assertLess(cleared("camper", "345"), cleared("walker", "345"), fps)
            # 14: rooms 1-2 summed; the walker need not clear them.
            self.assertGreaterEqual(lost("walker", "12"), 1, fps)
            self.assertLessEqual(lost("dodger", "12"), 1, fps)
            self.assertEqual(cleared("dodger", "12"), 2, fps)

    def test_bot_log_adds_state_and_changes_no_result(self):
        import bots

        for name, bot in bots.BOTS.items():
            for room in ("1", "3"):
                for fps in (30, 60):
                    quiet = bots.play_room(bot, room, fps, 60)
                    loud = bots.play_room(bot, room, fps, 60, log=True)
                    for key in ("cleared", "seconds", "hearts_lost", "hits_by", "attacks", "dashes"):
                        self.assertEqual(quiet[key], loud[key], (name, room, fps, key))
                    self.assertEqual(quiet["log"], [])
                    hurt = [line for line in loud["log"] if "HEART LOST" in line]
                    self.assertEqual(len(hurt), loud["hearts_lost"], (name, room, fps))
                    for line in loud["log"]:
                        if "HEART LOST" in line:
                            self.assertIn("source", line)
                        elif "skipped decision" in line:
                            self.assertIn("reason: player stunned", line)
                        else:
                            for part in ("frame ", "grid ", "player (", "hearts ", "stunned ", "nearest ", "shots in flight"):
                                self.assertIn(part, line, (name, room, fps, line))

    def test_walker_logs_the_exact_distance_it_compared(self):
        import bots

        result = bots.play_room(bots.BOTS["walker"], "1", 60, 60, log=True)
        self.assertTrue(any("(exact " in line for line in result["log"]))


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

<<<FILE goals/G-001-combat-monotony/14-game-designer-to-studio.md#findings
## Findings

### What changed in `design/combat.md`

- **Criterion 14 changed.** Old: the walker loses at least 1 heart in rooms 1–2 and clears both. New, at each rate: the walker loses at least 1 heart in rooms 1–2 summed (no clear required); the dodger loses at most 1 and clears both. Observed: walker 5 lost at 30 FPS and 5 at 60 FPS; dodger 0 lost, both cleared. Met.
  - The reason is structural. A wind-up always comes before contact, so a player who ignores the cue and stands still takes one lunge per grub. Room 1 has three grubs and 3 hearts, so a bot that never adapts cannot clear it. That is the cost "ignoring the cue costs hearts" asks for. Making the walker survive would need either a cue-reading walker (it would stop being the "ignores cues" proxy) or a gentler room 1 (a balance change, not needed to meet the intent).
  - Player-observable behavior protected: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. A human can learn the cue from the first hit; the bot cannot. I added this as an experience signal.
- **Criterion 16 changed.** It now has parts a–e:
  - 1–12 hold at both rates.
  - 13–15 are evaluated separately at each rate.
  - The dodger agrees across rates (same cleared set, hearts lost per room within 1).
  - The walker only has to meet 13 and 14 at each rate; its per-room numbers need not match. The reason is the 0.15 s decision grid (4.5 frames at 30 FPS, 9 at 60), which makes its sidestep timing sensitive to frame rounding.
  - A build defect is not excused: it is present if the same decision at the same game time (±1 frame) and the same state gives a different outcome, or if any of 1–11 fails at one rate.
- **Criterion 13** keeps its numbers but is stated to hold at each rate separately, with its protected behavior spelled out. Observed: walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (top of the range), dodger 0 lost and 3/3, camper 0/3.
- **Criterion 6** now also says a swipe that kills a grub in wind-up kills it with no stagger and no lunge.
- **The five defaults, all confirmed** (written into the spec):
  1. A grub exactly on the player: wind-up aims right. Confirmed and added to the Grub rules and edge cases.
  2. Spitter cap wait of 0.2 s from the moment the cue would start. Confirmed. I also wrote down what the code does: the delay carries forward, so the spitter's next shot is 2.4 s after its actual shot. The criterion 11 first-shot times are not affected.
  3. Spitter index counts only spitters, in spawn order, also in the practice room. Confirmed. A defeated spitter does not renumber the others.
  4. A grub hit but not killed during lunge or recovery continues its phase. Confirmed, extended to Approach and Stagger (a hit during stagger does not extend it). Only a hit during wind-up changes the phase.
  5. No stagger if the swipe kills the grub. Confirmed.

### Does anything need to change in the build or the bots?

No. All five defaults match the spec as now written. Bot thresholds (0.15 s grid, walker 2.5 and 1.1 tiles, dodger rules) stay as they are. The criteria were changed to fit the build and the bots, not the other way round.

### What QA's final verification should check

1. Criteria 1–12 at both 30 and 60 FPS with practice-room scripts, including the new part of 6 (swipe that kills a grub in wind-up: dies, no stagger, no lunge).
2. Criteria 13, 14 and 15 with `bots camper,walker,dodger` and `rooms 1-5` at `fps 30` and at `fps 60` separately. Expected from handoff 11: 13 met at both (walker total 4 and 6), 14 met at both (walker lost 5 in rooms 1–2), 15 met at both. If walker totals in rooms 3–5 fall outside 3–6 on QA's run, report it; that is a tuning question for the designer, not a build defect.
3. Criterion 16 c: dodger agreement between rates, per room (cleared set equal, hearts lost within 1).
4. Criterion 16 e: the walker comparison from handoff 13 (`log on`, `bots walker`, `rooms 3`, both rates). Decide whether the differences come from decision times landing on different frames, or from a build defect, using the rule in criterion 16 e. Only a defect is a failure.
5. Edge cases newly written: grub at distance 0 aims right (cue shown); a spitter delayed by the cap shifts its later shots by the same delay; a defeated spitter does not renumber the others.
6. Check that `repo/manual.md` still matches the spec: marks `r` and `G`, the `~` line, the messages, wind-up lengths 0.5 / 0.35 / 0.7 s and the 0.4 s stagger. No spec change affects the manual.
>>>END

<<<FILE goals/G-001-combat-monotony/15-art-director-to-studio.md#findings
## Findings

**Basis and limits.** I reviewed the cue descriptions in handoff 12, `design/combat.md` and `repo/manual.md`. I did not run `play.py`. The build is text-only, so color, brightness and look are not verifiable yet. This is a design-level verdict for the cue forms, and graphical acceptance is still open.

**Verdict by question**

1. **Are the cue forms readable and consistent with the art direction?** Yes, with conditions.
   - Saturated orange-red against a dark cave fits the art direction. The forms (flash, lane, aim line, glow ramp) are appropriate and reuse simple assets.
   - The same hue is used for the grub cue, the aim line and the shot, so shape and motion must carry the differences (see problems 3 and 4).
2. **What the graphical implementation must satisfy.** See `design/combat-cues-visual-spec.md`, criteria V1–V12.

**Problems found, with where they occur**

1. **The grub lane must show its true width.** The combat design calls it a "thin line" but also says the danger is 0.6 tiles either side (1.2 wide). A hairline would make the sidestep requirement unreadable. Requirement: draw the lane at 1.2 tiles wide. This is a visual fix, with no rule change.
2. **The spitter glow starts at 0% brightness.** The text cue shows `brightness 0%` at the start, so the glow carries no information on the first frame. Requirement: a glow floor of at least 30%, and the aim line at full brightness from the first frame. The ramp then conveys time left.
3. **Grub lane vs spitter aim line vs shot.** All three are orange-red and the text view draws the lane and aim line with the same `~`. In the text view the `cue:` line resolves this, but a graphical build needs different shapes: a wide short band for the grub, a thin long line for the spitter, and a round moving core for the shot. The line must disappear when the shot fires.
4. **Threat color vs lantern.** The lantern is also warm. The threat cues must be self-lit, more saturated and redder than the lantern, and not dimmed by distance from the lantern. Spitters in the far corners of the room must still show their cue (rooms 3–5).
5. **Short Runner cue (0.35 s).** About 10 frames at 30 FPS, with no room for a fade-in. The cue must appear at full contrast on the first frame. Variants must differ by silhouette and cadence, not by hue.
6. **No "safe" state is specified.** The recovery and stagger windows are where the player is meant to swipe. The grub should clearly return to a neutral untinted look so the player knows it is safe.
7. **Flash rate.** Keep pulses at or below 3 Hz. Do not strobe, including for the Runner.

**Does any of this need a rule or timing change?** No. All seven points are visual. I do not ask the game-designer to change timings. The 0.35 s minimum wind-up remains workable if V3 is met. If playtesting shows Runner cues are still missed in graphics, the escalation is a wind-up change within the allowed 0.35–0.7 s range, which is the game-designer's call.

**Also noted.** The open question in `design/combat.md` about whether the `r` / `G` text marks suit the graphical build is answered: the graphical build should use silhouette and size instead (spec table). The text marks stay for the text view.
>>>END

<<<FILE goals/G-001-combat-monotony/16-qa-to-studio.md#findings
## Findings

### 1. Reproduction

Commands (script files, one per rate):

```text
bots walker
rooms 1-5
fps 30        # second script: fps 60
log on
```

Command: `python3 bots.py {script}`. Results match the report exactly, hearts lost in rooms 1/2/3/4/5:

| Rate | Walker per room | Cleared |
|---|---|---|
| 30 FPS | 3✗ 2✓ 0✓ 1✓ 3✗ | 3/5, 9 lost |
| 60 FPS | 3✗ 2✓ 2✓ 2✓ 2✓ | 4/5, 11 lost |

- **Deterministic:** the game is headless and fixed-step, and the bot output was identical across the separate runs with and without `log on`. The dodger agrees at both rates: 0 lost, 5/5 cleared (dashes 35 at 30 FPS, 48 at 60 FPS).
- The camper also differs between rates (room 2: cleared at 30, not cleared at 60). 16c–e do not cover the camper. It shares the same decision grid, so the same explanation applies.

### 2. Where the runs first differ

**The decision grid is the same at both rates.** The bot's clock advances in exact 0.15 s steps (`Brain.due`), and a decision is made on the first frame at or after each grid time.
- At 60 FPS decisions fall on 0.00, 0.15, 0.30…
- At 30 FPS they fall on the next frame boundary: 0.00, 0.17, 0.30, 0.47, 0.60, 0.77…, a delay of 0 to 1 frame (0.033 s).
- This is the "up to frame rounding" behaviour described in the README.

**Room 1, the earliest and clearest divergence, at 0.30 s.**
- At 0.30 s the 60 FPS walker logs "face and swing at grub". The 30 FPS walker logs "walk to grub" and does not swing until 0.47 s.
- The walker picks "swing" when the nearest grub is closer than 2.5 tiles (`coming = distance < 2.5`).
- By arithmetic: the nearest grub is the one at (8,0), 4 tiles away. At 0.30 s the player has closed 1.2 tiles and the grub 0.3 tiles, so the distance is 4 − 1.5 = 2.5 tiles. That is exactly the threshold.
- **Hypothesis, not verified:** floating-point accumulation over 9 steps at 30 FPS versus 18 steps at 60 FPS lands on opposite sides of 2.5. If so, the cause is the bot's hard threshold at an exact tie, and not game behaviour.
- Everything later in room 1 follows from that one decision: 4 attacks at 60 FPS versus 5 at 30 FPS, and 5.2 s versus 4.9 s. The final result, 3 hearts lost and not cleared, is the same at both rates.

**Room 3 (spitters): the same action sequence, then different damage.**
- Up to 2.10 s the two logs contain the same actions: 12× walk to spitter, sidestep shot at 1.80, sidestep shot at 1.95 (60) or 1.97 (30), walk at 2.10. The only differences are the grid rounding.
- At 60 FPS there are no decisions at 2.25 and 2.40. The bot skips decisions while the player is stunned, so a shot hit the player between 2.10 and 2.25 s (stun 0.3 s; the next decision is at 2.57 s). Room 3 ends with 2 hearts lost, both from shots.
- At 30 FPS the walker logs "sidestep shot in flight" at 2.27 s. It was not hit, and room 3 ends with 0 hearts lost.
- From there the rooms play out differently. After a hit the player is stunned, so its position and timing are shifted for the rest of the room.

**Rooms 4 and 5:** the divergence follows the same pattern, with different shot and grub hits at different moments.
- Room 4: 30 FPS had 1 heart lost (grub); 60 FPS had 2 (grub, shot).
- Room 5: 30 FPS had 3 lost (grub 2, shot 1) and was not cleared; 60 FPS had 2 lost (grub 2) and was cleared.
- After the first difference, the shot-hit and grub-hit sequences are different. I did not trace the first difference in these rooms separately.

### 3. Build checks (all consistent with a bot-timing cause so far)

- `python3 -m unittest discover -s tests` is part of the existing suite. It includes timing, dash, sidestep and spitter-stagger tests at both rates, and the walker test is marked `expectedFailure`. I did not re-run it in this step (it was run in earlier steps); I rely on its existing assertions only as context.
- The simulation advances all durations on accumulated time. In the code I read, the grub walk, wind-up, lunge, the spit timer and the shot motion all scale with `dt`.
- No result in the logs shows a behaviour that cannot be explained by a one-frame shift in a decision or by a threshold.

### 4. What is not proven

- **Room 3 and the shot hit:** the logs give action names and times only. They do not give player positions or shot positions. I could not show the "same decision at the same game time (±1 frame) from the same positions gives a different outcome" test of 16e, either way.
- **Hypothesis (labelled as such):** the 60 FPS hit and the 30 FPS miss can be a sampling effect. Contact is a distance check each frame (reach 0.4) against a shot moving 0.1 tile per frame at 30 FPS and 0.05 at 60 FPS, with the player moving 0.13 or 0.07 tile per frame. A pass that only grazes the 0.4 reach for a fraction of a frame can be caught at one rate and missed at the other. That would make the simulation not a fault in itself, but it does mean a graze result depends on the frame rate. I did not check whether this is what happened.
- I did not check criteria 1–11 in this step, so 16a is untested here.

### 5. Verdict on the question

- Reproducible and deterministic: yes.
- First divergence point: room 1, 0.30 s, a bot threshold at an exact tie (distance 2.5), the first differing decision; room 3, between 2.10 and 2.25 s, a shot hit at 60 FPS and not at 30 FPS.
- Cause: bot decision timing is the best-supported cause (room 1 is concrete). **No build defect is demonstrated.** A build cause for room 3 cannot be excluded without positions.
- Severity if the cause is the bot only: low. It affects the balance-proxy numbers and not a player. Frequency: always, with these scripts.
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
### Round 1: @run/tests/suite — `python3 -m unittest discover -s tests`

Exit: 0 (0.2 s). Output:

```text
..................................
----------------------------------------------------------------------
Ran 34 tests in 0.147s

OK
```

### Round 1: @run/bots/all30-off — `python3 bots.py {script}`

Script:

```text
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

### Round 1: @run/bots/all60-off — `python3 bots.py {script}`

Script:

```text
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

### Round 1: @run/bots/all30-log — `python3 bots.py {script}`

Script:

```text
fps 30
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
            2.73 s  HEART LOST | frame 82, source grub, player (8.000000, 4.000000), grub grub at (8.000000, 3.600000); hearts now 2
            2.87 s  skipped decision | frame 86, grid 2.850 s, frame time 2.866667 s, reason: player stunned (0.167 s of stun left)
            3.00 s  skipped decision | frame 90, grid 3.000 s, frame time 3.000000 s, reason: player stunned (0.033 s of stun left)
            3.73 s  HEART LOST | frame 112, source grub, player (8.000000, 4.000000), grub grub at (7.600000, 4.000000); hearts now 1
            3.77 s  skipped decision | frame 113, grid 3.750 s, frame time 3.766667 s, reason: player stunned (0.267 s of stun left)
            3.90 s  skipped decision | frame 117, grid 3.900 s, frame time 3.900000 s, reason: player stunned (0.133 s of stun left)
            5.73 s  HEART LOST | frame 172, source grub, player (8.000000, 4.000000), grub grub at (8.400000, 4.000000); hearts now 0
camper  room 2: cleared in 10.2 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
            5.97 s  HEART LOST | frame 179, source grub, player (8.000000, 4.000000), grub grub at (8.314323, 3.790451); hearts now 2
            6.00 s  skipped decision | frame 180, grid 6.000 s, frame time 6.000000 s, reason: player stunned (0.267 s of stun left)
            6.17 s  skipped decision | frame 185, grid 6.150 s, frame time 6.166667 s, reason: player stunned (0.100 s of stun left)
            8.97 s  HEART LOST | frame 269, source grub, player (8.000000, 4.000000), grub brute at (8.360709, 4.154590); hearts now 1
            9.00 s  skipped decision | frame 270, grid 9.000 s, frame time 9.000000 s, reason: player stunned (0.267 s of stun left)
            9.17 s  skipped decision | frame 275, grid 9.150 s, frame time 9.166667 s, reason: player stunned (0.100 s of stun left)
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
            3.90 s  HEART LOST | frame 117, source shot, player (8.000000, 4.000000), shot at (7.724334, 3.862167) v (2.683282, 1.341641); hearts now 2
            3.90 s  skipped decision | frame 117, grid 3.900 s, frame time 3.900000 s, reason: player stunned (0.300 s of stun left)
            4.07 s  skipped decision | frame 122, grid 4.050 s, frame time 4.066667 s, reason: player stunned (0.133 s of stun left)
            4.20 s  skipped decision | frame 126, grid 4.200 s, frame time 4.200000 s, reason: player stunned (0.000 s of stun left)
            4.70 s  HEART LOST | frame 141, source shot, player (8.000000, 4.000000), shot at (8.275666, 4.137833) v (-2.683282, -1.341641); hearts now 1
            4.80 s  skipped decision | frame 144, grid 4.800 s, frame time 4.800000 s, reason: player stunned (0.200 s of stun left)
            4.97 s  skipped decision | frame 149, grid 4.950 s, frame time 4.966667 s, reason: player stunned (0.033 s of stun left)
            5.50 s  HEART LOST | frame 165, source shot, player (8.000000, 4.000000), shot at (7.724334, 4.137833) v (2.683282, -1.341641); hearts now 0
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
            4.33 s  HEART LOST | frame 130, source shot, player (8.000000, 4.000000), shot at (8.314528, 3.820270) v (-2.604729, 1.488417); hearts now 2
            4.37 s  skipped decision | frame 131, grid 4.350 s, frame time 4.366667 s, reason: player stunned (0.267 s of stun left)
            4.50 s  skipped decision | frame 135, grid 4.500 s, frame time 4.500000 s, reason: player stunned (0.133 s of stun left)
            5.13 s  HEART LOST | frame 154, source shot, player (8.000000, 4.000000), shot at (8.314528, 4.179730) v (-2.604729, -1.488417); hearts now 1
            5.27 s  skipped decision | frame 158, grid 5.250 s, frame time 5.266667 s, reason: player stunned (0.167 s of stun left)
            5.40 s  skipped decision | frame 162, grid 5.400 s, frame time 5.400000 s, reason: player stunned (0.033 s of stun left)
            6.73 s  HEART LOST | frame 202, source shot, player (8.000000, 4.000000), shot at (8.314528, 3.820270) v (-2.604729, 1.488417); hearts now 0
camper  room 5: NOT cleared (6.2 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
            4.33 s  HEART LOST | frame 130, source shot, player (8.000000, 4.000000), shot at (8.314528, 3.820270) v (-2.604729, 1.488417); hearts now 2
            4.37 s  skipped decision | frame 131, grid 4.350 s, frame time 4.366667 s, reason: player stunned (0.267 s of stun left)
            4.50 s  skipped decision | frame 135, grid 4.500 s, frame time 4.500000 s, reason: player stunned (0.133 s of stun left)
            5.13 s  HEART LOST | frame 154, source shot, player (8.000000, 4.000000), shot at (8.314528, 4.179730) v (-2.604729, -1.488417); hearts now 1
            5.27 s  skipped decision | frame 158, grid 5.250 s, frame time 5.266667 s, reason: player stunned (0.167 s of stun left)
            5.40 s  skipped decision | frame 162, grid 5.400 s, frame time 5.400000 s, reason: player stunned (0.033 s of stun left)
            6.17 s  HEART LOST | frame 185, source grub, player (8.000000, 4.000000), grub brute at (7.721739, 4.278261); hearts now 0
camper  total: cleared 1/5, hearts lost 14, dashes 0
walker  room 1: NOT cleared (4.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
            0.00 s  walk to grub | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest grub at (8.000000, 0.000000) distance 4.000000000 (exact 4.0), shots in flight: none
            0.17 s  walk to grub | frame 5, grid 0.150 s, frame time 0.166667 s, player (8.000000, 3.333333), hearts 3, stunned no, nearest grub at (8.000000, 0.166667) distance 3.166666667 (exact 3.166666666666667), shots in flight: none
            0.30 s  walk to grub | frame 9, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.5000000000000004), shots in flight: none
            0.47 s  face and swing at grub | frame 14, grid 0.450 s, frame time 0.466667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            0.60 s  face and swing at grub | frame 18, grid 0.600 s, frame time 0.600000 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            0.77 s  face and swing at grub | frame 23, grid 0.750 s, frame time 0.766667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            0.90 s  face and swing at grub | frame 27, grid 0.900 s, frame time 0.900000 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            1.07 s  face and swing at grub | frame 32, grid 1.050 s, frame time 1.066667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 1.466667) distance 0.666666667 (exact 0.6666666666666672), shots in flight: none
            1.10 s  HEART LOST | frame 33, source grub, player (8.000000, 2.133333), grub grub at (8.000000, 1.733333); hearts now 2
            1.20 s  skipped decision | frame 36, grid 1.200 s, frame time 1.200000 s, reason: player stunned (0.200 s of stun left)
            1.37 s  skipped decision | frame 41, grid 1.350 s, frame time 1.366667 s, reason: player stunned (0.033 s of stun left)
            1.43 s  face and swing at grub | frame 43, grid 1.350 s, frame time 1.433333 s, player (8.000000, 2.133333), hearts 2, stunned no, nearest grub at (8.000000, 1.733333) distance 0.400000000 (exact 0.4000000000000006), shots in flight: none
            1.50 s  walk to grub | frame 45, grid 1.500 s, frame time 1.500000 s, player (8.000000, 2.133333), hearts 2, stunned no, nearest grub at (4.417261, 3.531738) distance 3.845979201 (exact 3.8459792005106057), shots in flight: none
            1.67 s  walk to grub | frame 50, grid 1.650 s, frame time 1.666667 s, player (7.333333, 2.133333), hearts 2, stunned no, nearest grub at (4.569694, 3.464449) distance 3.067502526 (exact 3.0675025256704145), shots in flight: none
            1.80 s  face and swing at grub | frame 54, grid 1.800 s, frame time 1.800000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (4.686468, 3.400191) distance 2.464132366 (exact 2.4641323661562193), shots in flight: none
            1.97 s  face and swing at grub | frame 59, grid 1.950 s, frame time 1.966667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (4.829421, 3.314505) distance 2.297465699 (exact 2.297465699489551), shots in flight: none
            2.10 s  face and swing at grub | frame 63, grid 2.100 s, frame time 2.100000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (4.943783, 3.245955) distance 2.164132366 (exact 2.164132366156217), shots in flight: none
            2.27 s  face and swing at grub | frame 68, grid 2.250 s, frame time 2.266667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.40 s  face and swing at grub | frame 72, grid 2.400 s, frame time 2.400000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.57 s  face and swing at grub | frame 77, grid 2.550 s, frame time 2.566667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.70 s  face and swing at grub | frame 81, grid 2.700 s, frame time 2.700000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.87 s  face and swing at grub | frame 86, grid 2.850 s, frame time 2.866667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.544186, 2.886072) distance 1.464132366 (exact 1.4641323661562147), shots in flight: none
            3.00 s  HEART LOST | frame 90, source grub, player (6.800000, 2.133333), grub grub at (6.459086, 2.337678); hearts now 1
            3.00 s  skipped decision | frame 90, grid 3.000 s, frame time 3.000000 s, reason: player stunned (0.300 s of stun left)
            3.17 s  skipped decision | frame 95, grid 3.150 s, frame time 3.166667 s, reason: player stunned (0.133 s of stun left)
            3.30 s  skipped decision | frame 99, grid 3.300 s, frame time 3.300000 s, reason: player stunned (0.000 s of stun left)
            3.33 s  face and swing at grub | frame 100, grid 3.300 s, frame time 3.333333 s, player (6.800000, 2.133333), hearts 1, stunned no, nearest grub at (6.459086, 2.337678) distance 0.397465699 (exact 0.3974656994895464), shots in flight: none
            3.47 s  walk to grub | frame 104, grid 3.450 s, frame time 3.466667 s, player (6.800000, 2.133333), hearts 1, stunned no, nearest grub at (11.626085, 3.220944) distance 4.947120155 (exact 4.9471201549117545), shots in flight: none
            3.60 s  walk to grub | frame 108, grid 3.600 s, frame time 3.600000 s, player (7.333333, 2.133333), hearts 1, stunned no, nearest grub at (11.496511, 3.189526) distance 4.295065590 (exact 4.295065590215387), shots in flight: none
            3.77 s  walk to grub | frame 113, grid 3.750 s, frame time 3.766667 s, player (8.000000, 2.133333), hearts 1, stunned no, nearest grub at (11.336101, 3.144341) distance 3.485930257 (exact 3.485930256555839), shots in flight: none
            3.90 s  walk to grub | frame 117, grid 3.900 s, frame time 3.900000 s, player (8.533333, 2.133333), hearts 1, stunned no, nearest grub at (11.209798, 3.101668) distance 2.846249365 (exact 2.8462493648299154), shots in flight: none
            4.07 s  face and swing at grub | frame 122, grid 4.050 s, frame time 4.066667 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (11.056727, 3.035944) distance 2.064495181 (exact 2.064495180648655), shots in flight: none
            4.20 s  face and swing at grub | frame 126, grid 4.200 s, frame time 4.200000 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.37 s  face and swing at grub | frame 131, grid 4.350 s, frame time 4.366667 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.50 s  face and swing at grub | frame 135, grid 4.500 s, frame time 4.500000 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.67 s  face and swing at grub | frame 140, grid 4.650 s, frame time 4.666667 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.80 s  face and swing at grub | frame 144, grid 4.800 s, frame time 4.800000 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.037451, 2.540443) distance 0.931161847 (exact 0.9311618473153187), shots in flight: none
            4.87 s  HEART LOST | frame 146, source grub, player (9.200000, 2.133333), grub grub at (9.557791, 2.307267); hearts now 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
            0.00 s  walk to runner | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest runner at (2.000000, 1.000000) distance 6.708203932 (exact 6.708203932499369), shots in flight: none
            0.17 s  walk to runner | frame 5, grid 0.150 s, frame time 0.166667 s, player (7.333333, 4.000000), hearts 3, stunned no, nearest runner at (2.234947, 1.126081) distance 5.852602390 (exact 5.852602389764123), shots in flight: none
            0.30 s  walk to runner | frame 9, grid 0.300 s, frame time 0.300000 s, player (6.800000, 4.000000), hearts 3, stunned no, nearest runner at (2.417539, 1.236363) distance 5.181086117 (exact 5.181086117451613), shots in flight: none
            0.47 s  walk to runner | frame 14, grid 0.450 s, frame time 0.466667 s, player (6.133333, 4.000000), hearts 3, stunned no, nearest runner at (2.636345, 1.388672) distance 4.364397460 (exact 4.364397460138426), shots in flight: none
            0.60 s  walk to runner | frame 18, grid 0.600 s, frame time 0.600000 s, player (5.600000, 4.000000), hearts 3, stunned no, nearest runner at (2.800640, 1.524659) distance 3.736807884 (exact 3.736807883951396), shots in flight: none
            0.77 s  walk to runner | frame 23, grid 0.750 s, frame time 0.766667 s, player (4.933333, 4.000000), hearts 3, stunned no, nearest runner at (2.985441, 1.716595) distance 3.001370135 (exact 3.0013701346750254), shots in flight: none
            0.90 s  face and swing at runner | frame 27, grid 0.900 s, frame time 0.900000 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (3.136575, 1.866918) distance 2.405730079 (exact 2.4057300794780985), shots in flight: none
            1.07 s  face and swing at runner | frame 32, grid 1.050 s, frame time 1.066667 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (3.335739, 2.044244) distance 2.139063413 (exact 2.139063412811432), shots in flight: none
            1.20 s  face and swing at runner | frame 36, grid 1.200 s, frame time 1.200000 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (3.455238, 2.150640) distance 1.979063413 (exact 1.9790634128114317), shots in flight: none
            1.37 s  face and swing at runner | frame 41, grid 1.350 s, frame time 1.366667 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (3.455238, 2.150640) distance 1.979063413 (exact 1.9790634128114317), shots in flight: none
            1.50 s  face and swing at runner | frame 45, grid 1.500 s, frame time 1.500000 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (3.455238, 2.150640) distance 1.979063413 (exact 1.9790634128114317), shots in flight: none
            1.67 s  face and swing at runner | frame 50, grid 1.650 s, frame time 1.666667 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (4.052731, 2.682620) distance 1.179063413 (exact 1.179063412811432), shots in flight: none
            1.80 s  walk to runner | frame 54, grid 1.800 s, frame time 1.800000 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest runner at (2.989975, 5.955202) distance 3.157443451 (exact 3.1574434505419253), shots in flight: none
            1.97 s  face and swing at runner | frame 59, grid 1.950 s, frame time 1.966667 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest runner at (3.172358, 5.761073) distance 2.398034744 (exact 2.3980347443994), shots in flight: none
            2.10 s  face and swing at runner | frame 63, grid 2.100 s, frame time 2.100000 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest runner at (3.329017, 5.616267) distance 2.184701411 (exact 2.1847014110660665), shots in flight: none
            2.27 s  face and swing at runner | frame 68, grid 2.250 s, frame time 2.266667 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest runner at (3.485677, 5.471460) distance 1.971368078 (exact 1.9713680777327331), shots in flight: none
            2.40 s  face and swing at runner | frame 72, grid 2.400 s, frame time 2.400000 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest runner at (3.485677, 5.471460) distance 1.971368078 (exact 1.9713680777327331), shots in flight: none
            2.57 s  face and swing at runner | frame 77, grid 2.550 s, frame time 2.566667 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest runner at (3.485677, 5.471460) distance 1.971368078 (exact 1.9713680777327331), shots in flight: none
            2.70 s  face and swing at runner | frame 81, grid 2.700 s, frame time 2.700000 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest runner at (3.877325, 5.109444) distance 1.438034744 (exact 1.4380347443993995), shots in flight: none
            2.87 s  walk to grub | frame 86, grid 2.850 s, frame time 2.866667 s, player (4.933333, 4.133333), hearts 3, stunned no, nearest grub at (11.384281, 1.160980) distance 7.102788630 (exact 7.1027886303680186), shots in flight: none
            3.00 s  walk to grub | frame 90, grid 3.000 s, frame time 3.000000 s, player (5.466667, 4.133333), hearts 3, stunned no, nearest grub at (11.264376, 1.219282) distance 6.488847053 (exact 6.4888470525162205), shots in flight: none
            3.17 s  walk to grub | frame 95, grid 3.150 s, frame time 3.166667 s, player (6.133333, 4.133333), hearts 3, stunned no, nearest grub at (11.117783, 1.298542) distance 5.734177075 (exact 5.734177074791192), shots in flight: none
            3.30 s  walk to grub | frame 99, grid 3.300 s, frame time 3.300000 s, player (6.666667, 4.133333), hearts 3, stunned no, nearest grub at (11.003979, 1.367987) distance 5.143872081 (exact 5.143872080728375), shots in flight: none
            3.47 s  walk to grub | frame 104, grid 3.450 s, frame time 3.466667 s, player (7.333333, 4.133333), hearts 3, stunned no, nearest grub at (10.867741, 1.463915) distance 4.429201921 (exact 4.429201921291835), sho
[output cut at 20000 characters]
```

### Round 1: @run/bots/all60-log — `python3 bots.py {script}`

Script:

```text
fps 60
log on
```

Exit: 0 (0.1 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
            2.70 s  HEART LOST | frame 162, source grub, player (8.000000, 4.000000), grub grub at (8.000000, 3.466667); hearts now 2
            2.70 s  skipped decision | frame 162, grid 2.700 s, frame time 2.700000 s, reason: player stunned (0.300 s of stun left)
            2.85 s  skipped decision | frame 171, grid 2.850 s, frame time 2.850000 s, reason: player stunned (0.150 s of stun left)
            3.00 s  skipped decision | frame 180, grid 3.000 s, frame time 3.000000 s, reason: player stunned (0.000 s of stun left)
            3.70 s  HEART LOST | frame 222, source grub, player (8.000000, 4.000000), grub grub at (7.466667, 4.000000); hearts now 1
            3.75 s  skipped decision | frame 225, grid 3.750 s, frame time 3.750000 s, reason: player stunned (0.250 s of stun left)
            3.90 s  skipped decision | frame 234, grid 3.900 s, frame time 3.900000 s, reason: player stunned (0.100 s of stun left)
            5.70 s  HEART LOST | frame 342, source grub, player (8.000000, 4.000000), grub grub at (8.533333, 4.000000); hearts now 0
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
            4.35 s  HEART LOST | frame 261, source grub, player (8.000000, 4.000000), grub runner at (7.552342, 4.255805); hearts now 2
            4.35 s  skipped decision | frame 261, grid 4.350 s, frame time 4.350000 s, reason: player stunned (0.300 s of stun left)
            4.50 s  skipped decision | frame 270, grid 4.500 s, frame time 4.500000 s, reason: player stunned (0.150 s of stun left)
            4.65 s  skipped decision | frame 279, grid 4.650 s, frame time 4.650000 s, reason: player stunned (0.000 s of stun left)
            5.92 s  HEART LOST | frame 355, source grub, player (8.000000, 4.000000), grub grub at (8.439131, 3.707246); hearts now 1
            6.00 s  skipped decision | frame 360, grid 6.000 s, frame time 6.000000 s, reason: player stunned (0.217 s of stun left)
            6.15 s  skipped decision | frame 369, grid 6.150 s, frame time 6.150000 s, reason: player stunned (0.067 s of stun left)
            8.93 s  HEART LOST | frame 536, source grub, player (8.000000, 4.000000), grub brute at (8.483262, 4.207112); hearts now 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
            3.90 s  HEART LOST | frame 234, source shot, player (8.000000, 4.000000), shot at (7.679613, 3.839806) v (2.683282, 1.341641); hearts now 2
            3.90 s  skipped decision | frame 234, grid 3.900 s, frame time 3.900000 s, reason: player stunned (0.300 s of stun left)
            4.05 s  skipped decision | frame 243, grid 4.050 s, frame time 4.050000 s, reason: player stunned (0.150 s of stun left)
            4.20 s  skipped decision | frame 252, grid 4.200 s, frame time 4.200000 s, reason: player stunned (0.000 s of stun left)
            4.70 s  HEART LOST | frame 282, source shot, player (8.000000, 4.000000), shot at (8.320387, 4.160194) v (-2.683282, -1.341641); hearts now 1
            4.80 s  skipped decision | frame 288, grid 4.800 s, frame time 4.800000 s, reason: player stunned (0.200 s of stun left)
            4.95 s  skipped decision | frame 297, grid 4.950 s, frame time 4.950000 s, reason: player stunned (0.050 s of stun left)
            5.50 s  HEART LOST | frame 330, source shot, player (8.000000, 4.000000), shot at (7.679613, 4.160194) v (2.683282, -1.341641); hearts now 0
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
            4.35 s  HEART LOST | frame 261, source shot, player (8.000000, 4.000000), shot at (8.314528, 3.820270) v (-2.604729, 1.488417); hearts now 2
            4.35 s  skipped decision | frame 261, grid 4.350 s, frame time 4.350000 s, reason: player stunned (0.300 s of stun left)
            4.50 s  skipped decision | frame 270, grid 4.500 s, frame time 4.500000 s, reason: player stunned (0.150 s of stun left)
            4.65 s  skipped decision | frame 279, grid 4.650 s, frame time 4.650000 s, reason: player stunned (0.000 s of stun left)
            5.15 s  HEART LOST | frame 309, source shot, player (8.000000, 4.000000), shot at (8.314528, 4.179730) v (-2.604729, -1.488417); hearts now 1
            5.25 s  skipped decision | frame 315, grid 5.250 s, frame time 5.250000 s, reason: player stunned (0.200 s of stun left)
            5.40 s  skipped decision | frame 324, grid 5.400 s, frame time 5.400000 s, reason: player stunned (0.050 s of stun left)
            6.75 s  HEART LOST | frame 405, source shot, player (8.000000, 4.000000), shot at (8.314528, 3.820270) v (-2.604729, 1.488417); hearts now 0
camper  room 5: NOT cleared (6.1 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
            4.35 s  HEART LOST | frame 261, source shot, player (8.000000, 4.000000), shot at (8.314528, 3.820270) v (-2.604729, 1.488417); hearts now 2
            4.35 s  skipped decision | frame 261, grid 4.350 s, frame time 4.350000 s, reason: player stunned (0.300 s of stun left)
            4.50 s  skipped decision | frame 270, grid 4.500 s, frame time 4.500000 s, reason: player stunned (0.150 s of stun left)
            4.65 s  skipped decision | frame 279, grid 4.650 s, frame time 4.650000 s, reason: player stunned (0.000 s of stun left)
            5.15 s  HEART LOST | frame 309, source shot, player (8.000000, 4.000000), shot at (8.314528, 4.179730) v (-2.604729, -1.488417); hearts now 1
            5.25 s  skipped decision | frame 315, grid 5.250 s, frame time 5.250000 s, reason: player stunned (0.200 s of stun left)
            5.40 s  skipped decision | frame 324, grid 5.400 s, frame time 5.400000 s, reason: player stunned (0.050 s of stun left)
            6.13 s  HEART LOST | frame 368, source grub, player (8.000000, 4.000000), grub brute at (7.627458, 4.372542); hearts now 0
camper  total: cleared 0/5, hearts lost 15, dashes 0
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
            0.00 s  walk to grub | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest grub at (8.000000, 0.000000) distance 4.000000000 (exact 4.0), shots in flight: none
            0.15 s  walk to grub | frame 9, grid 0.150 s, frame time 0.150000 s, player (8.000000, 3.400000), hearts 3, stunned no, nearest grub at (8.000000, 0.150000) distance 3.250000000 (exact 3.2499999999999982), shots in flight: none
            0.30 s  face and swing at grub | frame 18, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.4999999999999964), shots in flight: none
            0.45 s  face and swing at grub | frame 27, grid 0.450 s, frame time 0.450000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.450000) distance 2.350000000 (exact 2.349999999999996), shots in flight: none
            0.60 s  face and swing at grub | frame 36, grid 0.600 s, frame time 0.600000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.600000) distance 2.200000000 (exact 2.199999999999996), shots in flight: none
            0.75 s  face and swing at grub | frame 45, grid 0.750 s, frame time 0.750000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.750000) distance 2.050000000 (exact 2.0499999999999954), shots in flight: none
            0.90 s  face and swing at grub | frame 54, grid 0.900 s, frame time 0.900000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.800000) distance 2.000000000 (exact 1.9999999999999956), shots in flight: none
            1.05 s  face and swing at grub | frame 63, grid 1.050 s, frame time 1.050000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.800000) distance 2.000000000 (exact 1.9999999999999956), shots in flight: none
            1.20 s  face and swing at grub | frame 72, grid 1.200 s, frame time 1.200000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.800000) distance 2.000000000 (exact 1.9999999999999956), shots in flight: none
            1.35 s  face and swing at grub | frame 81, grid 1.350 s, frame time 1.350000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 1.066667) distance 1.733333333 (exact 1.7333333333333287), shots in flight: none
            1.50 s  HEART LOST | frame 90, source grub, player (8.000000, 2.800000), grub grub at (8.000000, 2.266667); hearts now 2
            1.50 s  skipped decision | frame 90, grid 1.500 s, frame time 1.500000 s, reason: player stunned (0.300 s of stun left)
            1.65 s  skipped decision | frame 99, grid 1.650 s, frame time 1.650000 s, reason: player stunned (0.150 s of stun left)
            1.80 s  skipped decision | frame 108, grid 1.800 s, frame time 1.800000 s, reason: player stunned (0.000 s of stun left)
            1.82 s  face and swing at grub | frame 109, grid 1.800 s, frame time 1.816667 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            1.95 s  face and swing at grub | frame 117, grid 1.950 s, frame time 1.950000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            2.10 s  face and swing at grub | frame 126, grid 2.100 s, frame time 2.100000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            2.25 s  face and swing at grub | frame 135, grid 2.250 s, frame time 2.250000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            2.40 s  walk to grub | frame 144, grid 2.400 s, frame time 2.400000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (5.335539, 3.458223) distance 2.744560270 (exact 2.7445602699534217), shots in flight: none
            2.55 s  face and swing at grub | frame 153, grid 2.550 s, frame time 2.550000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.479779, 3.417169) distance 2.016964246 (exact 2.016964245671973), shots in flight: none
            2.70 s  face and swing at grub | frame 162, grid 2.700 s, frame time 2.700000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.511514, 3.406969) distance 1.983630912 (exact 1.9836309123386402), shots in flight: none
            2.85 s  face and swing at grub | frame 171, grid 2.850 s, frame time 2.850000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.511514, 3.406969) distance 1.983630912 (exact 1.9836309123386402), shots in flight: none
            3.00 s  face and swing at grub | frame 180, grid 3.000 s, frame time 3.000000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.511514, 3.406969) distance 1.983630912 (exact 1.9836309123386402), shots in flight: none
            3.15 s  face and swing at grub | frame 189, grid 3.150 s, frame time 3.150000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.892328, 3.284573) distance 1.583630912 (exact 1.5836309123386392), shots in flight: none
            3.28 s  HEART LOST | frame 197, source grub, player (7.400000, 2.800000), grub grub at (6.907832, 2.958185); hearts now 1
            3.30 s  skipped decision | frame 198, grid 3.300 s, frame time 3.300000 s, reason: player stunned (0.283 s of stun left)
            3.45 s  skipped decision | frame 207, grid 3.450 s, frame time 3.450000 s, reason: player stunned (0.133 s of stun left)
            3.60 s  face and swing at grub | frame 216, grid 3.600 s, frame time 3.600000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            3.75 s  face and swing at grub | frame 225, grid 3.750 s, frame time 3.750000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            3.90 s  face and swing at grub | frame 234, grid 3.900 s, frame time 3.900000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            4.05 s  face and swing at grub | frame 243, grid 4.050 s, frame time 4.050000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            4.20 s  walk to grub | frame 252, grid 4.200 s, frame time 4.200000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (10.854408, 3.334326) distance 3.495488595 (exact 3.4954885948648555), shots in flight: none
            4.35 s  walk to grub | frame 261, grid 4.350 s, frame time 4.350000 s, player (8.000000, 2.800000), hearts 1, stunned no, nearest grub at (10.706585, 3.308902) distance 2.754012647 (exact 2.7540126472547657), shots in flight: none
            4.50 s  face and swing at grub | frame 270, grid 4.500 s, frame time 4.500000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.559989, 3.277217) distance 2.017248561 (exact 2.0172485605352772), shots in flight: none
            4.65 s  face and swing at grub | frame 279, grid 4.650 s, frame time 4.650000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.527601, 3.269332) distance 1.983915227 (exact 1.9839152272019436), shots in flight: none
            4.80 s  face and swing at grub | frame 288, grid 4.800 s, frame time 4.800000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.527601, 3.269332) distance 1.983915227 (exact 1.9839152272019436), shots in flight: none
            4.95 s  face and swing at grub | frame 297, grid 4.950 s, frame time 4.950000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.527601, 3.269332) distance 1.983915227 (exact 1.9839152272019436), shots in flight: none
            5.10 s  face and swing at grub | frame 306, grid 5.100 s, frame time 5.100000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.138956, 3.174704) distance 1.583915227 (exact 1.5839152272019446), shots in flight: none
            5.23 s  HEART LOST | frame 314, source grub, player (8.600000, 2.800000), grub grub at (9.102566, 2.922365); hearts now 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
            0.00 s  walk to runner | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest runner at (2.000000, 1.000000) distance 6.708203932 (exact 6.708203932499369), shots in flight: none
            0.15 s  walk to runner | frame 9, grid 0.150 s, frame time 0.150000 s, player (7.400000, 4.000000), hearts 3, stunned no, nearest runner at (2.212027, 1.112407) distance 5.937445889 (exact 5.937445888950024), shots in flight: none
            0.30 s  walk to runner | frame 18, grid 0.300 s, frame time 0.300000 s, player (6.800000, 4.000000), hearts 3, stunned no, nearest runner at (2.418170, 1.235248) distance 5.181146882 (exact 5.18114688228216), shots in flight: none
            0.45 s  walk to runner | frame 27, grid 0.450 s, frame time 0.450000 s, player (6.200000, 4.000000), hearts 3, stunned no, nearest runner at (2.616166, 1.370799) distance 4.444835989 (exact 4.444835988563267), shots in flight: none
            0.60 s  walk to runner | frame 36, grid 0.600 s, frame time 0.600000 s, player (5.600000, 4.000000), hearts 3, stunned no, nearest runner at (2.802436, 1.522001) distance 3.737223999 (exact 3.737223998524535), shots in flight: none
            0.75 s  walk to runner | frame 45, grid 0.750 s, frame time 0.750000 s, player (5.000000, 4.000000), hearts 3, stunned no, nearest runner at (2.971099, 1.692520) distance 3.072605258 (exact 3.0726052578574956), shots in flight: none
            0.90 s  face and swing at runner | frame 54, grid 0.900 s, frame time 0.900000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (3.143622, 1.858997) distance 2.412639109 (exact 2.412639108515722), shots in flight: none
            1.05 s  face and swing at runner | frame 63, grid 1.050 s, frame time 1.050000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (3.328288, 2.012290) distance 2.172639109 (exact 2.1726391085157237), shots in flight: none
            1.20 s  face and swing at runner | frame 72, grid 1.200 s, frame time 1.200000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (3.471916, 2.131518) distance 1.985972442 (exact 1.9859724418490576), shots in flight: none
            1.35 s  face and swing at runner | frame 81, grid 1.350 s, frame time 1.350000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (3.471916, 2.131518) distance 1.985972442 (exact 1.9859724418490576), shots in flight: none
            1.50 s  face and swing at runner | frame 90, grid 1.500 s, frame time 1.500000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (3.471916, 2.131518) distance 1.985972442 (exact 1.9859724418490576), shots in flight: none
            1.65 s  face and swing at runner | frame 99, grid 1.650 s, frame time 1.650000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (4.190059, 2.727657) distance 1.052639109 (exact 1.052639108515725), shots in flight: none
            1.80 s  walk to runner | frame 108, grid 1.800 s, frame time 1.800000 s, player (5.000000, 3.400000), hearts 3, stunned no, nearest runner at (2.994884, 5.960205) distance 3.251944079 (exact 3.251944078882153), shots in flight: none
            1.95 s  walk to runner | frame 117, grid 1.950 s, frame time 1.950000 s, player (5.000000, 4.000000), hearts 3, stunned no, nearest runner at (3.155980, 5.782570) distance 2.564754211 (exact 2.5647542106490664), shots in flight: none
            2.10 s  face and swing at runner | frame 126, grid 2.100 s, frame time 2.100000 s, player (4.400000, 4.000000), hearts 3, stunned no, nearest runner at (3.294685, 5.620858) distance 1.961861867 (exact 1.9618618665857057), shots in flight: none
            2.25 s  face and swing at runner | frame 135, grid 2.250 s, frame time 2.250000 s, player (4.400000, 4.000000), hearts 3, stunned no, nearest runner at (3.294685, 5.620858) distance 1.961861867 (exact 1.9618618665857057), shots in flight: none
            2.40 s  face and swing at runner | frame 144, grid 2.400 s, frame time 2.400000 s, player (4.400000, 4.000000), hearts 3, stunned no, nearest runner at (3.294685, 5.620858) distance 1.961861867 (exact 1.9618618665857057), shots in flight: none
            2.55 s  face and swing at runner | frame 153, grid 2.550 s, frame time 2.550000 s, player (4.400000, 4.000000), hearts 3, stunned no, nearest runner at (3.745406, 4.959911) distance 1.161861867 (exact 1.1618618665857046), shots in flight: none
            2.70 s  walk to grub | frame 162, grid 2.700 s, frame time 2.700000 s, player (4.400000, 4.000000), hearts 3, stunned no, nearest grub at (11.522934, 1.061153) distance 7.705388426 (exact 7.705388426206925), shots in flight: none
            2.85 s  walk to grub | frame 171, grid 2.850 s, frame time 2.850000 s, player (5.000000, 4.000000), hearts 3, stunned no, nearest grub at (11.385301, 1.120778) distance 7.004426184 (exact 7.004426183644148), shots
[output cut at 20000 characters]
```

### Round 1: @run/bots/walker-r3-30 — `python3 bots.py {script}`

Script:

```text
bots walker
rooms 3
fps 30
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
walker  room 3: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
            0.00 s  walk to spitter | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.708203932 (exact 6.708203932499369), shots in flight: none
            0.17 s  walk to spitter | frame 5, grid 0.150 s, frame time 0.166667 s, player (7.333333, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.119186584 (exact 6.119186583561938), shots in flight: none
            0.30 s  walk to spitter | frame 9, grid 0.300 s, frame time 0.300000 s, player (6.800000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 5.660388679 (exact 5.660388679233959), shots in flight: none
            0.47 s  walk to spitter | frame 14, grid 0.450 s, frame time 0.466667 s, player (6.133333, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 5.107293260 (exact 5.10729326007861), shots in flight: none
            0.60 s  walk to spitter | frame 18, grid 0.600 s, frame time 0.600000 s, player (5.600000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 4.686149806 (exact 4.6861498055439865), shots in flight: none
            0.77 s  walk to spitter | frame 23, grid 0.750 s, frame time 0.766667 s, player (4.933333, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 4.195765061 (exact 4.195765060682543), shots in flight: none
            0.90 s  walk to spitter | frame 27, grid 0.900 s, frame time 0.900000 s, player (4.933333, 3.466667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 3.832608627 (exact 3.832608627147942), shots in flight: none
            1.07 s  walk to spitter | frame 32, grid 1.050 s, frame time 1.066667 s, player (4.266667, 3.466667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 3.349958540 (exact 3.3499585403736223), shots in flight: none
            1.20 s  walk to spitter | frame 36, grid 1.200 s, frame time 1.200000 s, player (4.266667, 2.933333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.979187063 (exact 2.9791870628672354), shots in flight: none
            1.37 s  walk to spitter | frame 41, grid 1.350 s, frame time 1.366667 s, player (3.600000, 2.933333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.509537363 (exact 2.509537363295821), shots in flight: none
            1.50 s  walk to spitter | frame 45, grid 1.500 s, frame time 1.500000 s, player (3.600000, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.126029163 (exact 2.126029162546921), shots in flight: none
            1.67 s  walk to spitter | frame 50, grid 1.650 s, frame time 1.666667 s, player (2.933333, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.682590595 (exact 1.682590595216522), shots in flight: none
            1.80 s  sidestep shot in flight | frame 54, grid 1.800 s, frame time 1.800000 s, player (2.933333, 1.866667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.273664878 (exact 1.273664878302845), shots in flight: (2.076083, 1.064895) v (2.282502, 1.946840)
            1.97 s  sidestep shot in flight | frame 59, grid 1.950 s, frame time 1.966667 s, player (2.933333, 2.533333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.795054936 (exact 1.7950549357114955), shots in flight: (2.456500, 1.389368) v (2.282502, 1.946840)
            2.10 s  walk to spitter | frame 63, grid 2.100 s, frame time 2.100000 s, player (2.933333, 3.066667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.267646847 (exact 2.267646846892655), shots in flight: (2.760834, 1.648947) v (2.282502, 1.946840)
            2.27 s  sidestep shot in flight | frame 68, grid 2.250 s, frame time 2.266667 s, player (2.933333, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.682590595 (exact 1.682590595216522), shots in flight: (3.141251, 1.973420) v (2.282502, 1.946840)
            2.40 s  walk to spitter | frame 72, grid 2.400 s, frame time 2.400000 s, player (2.933333, 2.933333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.146832292 (exact 2.1468322917472777), shots in flight: (3.445585, 2.232999) v (2.282502, 1.946840)
            2.57 s  walk to spitter | frame 77, grid 2.550 s, frame time 2.566667 s, player (2.933333, 2.266667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.573389829 (exact 1.5733898294941195), shots in flight: (3.826001, 2.557472) v (2.282502, 1.946840)
            2.70 s  walk to spitter | frame 81, grid 2.700 s, frame time 2.700000 s, player (2.933333, 1.733333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.186966254 (exact 1.186966254317648), shots in flight: (4.130335, 2.817050) v (2.282502, 1.946840); (13.627536, 6.854156) v (-2.793480, -1.093833)
            2.87 s  face and swing at spitter | frame 86, grid 2.850 s, frame time 2.866667 s, player (2.266667, 1.733333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.780313327 (exact 0.7803133273813049), shots in flight: (4.510752, 3.141524) v (2.282502, 1.946840); (13.161956, 6.671850) v (-2.793480, -1.093833)
            3.00 s  face and swing at spitter | frame 90, grid 3.000 s, frame time 3.000000 s, player (2.266667, 1.733333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.780313327 (exact 0.7803133273813049), shots in flight: (4.815086, 3.401102) v (2.282502, 1.946840); (12.789492, 6.526006) v (-2.793480, -1.093833)
            3.17 s  face and swing at spitter | frame 95, grid 3.150 s, frame time 3.166667 s, player (2.266667, 1.733333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.780313327 (exact 0.7803133273813049), shots in flight: (5.195503, 3.725576) v (2.282502, 1.946840); (12.323912, 6.343700) v (-2.793480, -1.093833)
            3.30 s  face and swing at spitter | frame 99, grid 3.300 s, frame time 3.300000 s, player (2.266667, 1.733333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.780313327 (exact 0.7803133273813049), shots in flight: (5.499836, 3.985154) v (2.282502, 1.946840); (11.951448, 6.197856) v (-2.793480, -1.093833)
            3.47 s  walk to spitter | frame 104, grid 3.450 s, frame time 3.466667 s, player (2.266667, 1.733333), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 5.273413400 (exact 5.273413400150691), shots in flight: (5.880253, 4.309628) v (2.282502, 1.946840); (11.485868, 6.015551) v (-2.793480, -1.093833); (2.030225, 6.701526) v (0.302252, -2.984735)
            3.60 s  walk to spitter | frame 108, grid 3.600 s, frame time 3.600000 s, player (2.266667, 2.266667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 4.740839119 (exact 4.740839119349605), shots in flight: (6.184587, 4.569206) v (2.282502, 1.946840); (11.113404, 5.869706) v (-2.793480, -1.093833); (2.070525, 6.303562) v (0.302252, -2.984735)
            3.77 s  walk to spitter | frame 113, grid 3.750 s, frame time 3.766667 s, player (2.266667, 2.933333), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 4.075400457 (exact 4.075400457487445), shots in flight: (6.565004, 4.893680) v (2.282502, 1.946840); (10.647824, 5.687401) v (-2.793480, -1.093833); (2.120901, 5.806106) v (0.302252, -2.984735)
            3.90 s  sidestep shot in flight | frame 117, grid 3.900 s, frame time 3.900000 s, player (2.266667, 3.466667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.543381938 (exact 3.5433819375782156), shots in flight: (6.869337, 5.153258) v (2.282502, 1.946840); (10.275360, 5.541557) v (-2.793480, -1.093833); (2.161201, 5.408141) v (0.302252, -2.984735)
            4.07 s  sidestep shot in flight | frame 122, grid 4.050 s, frame time 4.066667 s, player (2.933333, 3.466667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.654525353 (exact 3.654525352977529), shots in flight: (7.249754, 5.477732) v (2.282502, 1.946840); (9.809780, 5.359251) v (-2.793480, -1.093833); (2.211576, 4.910685) v (0.302252, -2.984735)
            4.20 s  walk to spitter | frame 126, grid 4.200 s, frame time 4.200000 s, player (3.466667, 3.466667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.825644463 (exact 3.825644462774281), shots in flight: (7.554088, 5.737310) v (2.282502, 1.946840); (9.437316, 5.213407) v (-2.793480, -1.093833); (2.251876, 4.512721) v (0.302252, -2.984735)
            4.37 s  walk to spitter | frame 131, grid 4.350 s, frame time 4.366667 s, player (3.466667, 4.133333), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.220075914 (exact 3.22007591352888), shots in flight: (7.934505, 6.061784) v (2.282502, 1.946840); (8.971736, 5.031101) v (-2.793480, -1.093833); (2.302252, 4.015265) v (0.302252, -2.984735)
            4.50 s  walk to spitter | frame 135, grid 4.500 s, frame time 4.500000 s, player (3.466667, 4.666667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 2.756003548 (exact 2.756003547812577), shots in flight: (8.238838, 6.321362) v (2.282502, 1.946840); (8.599272, 4.885257) v (-2.793480, -1.093833); (2.342552, 3.617300) v (0.302252, -2.984735)
            4.67 s  walk to spitter | frame 140, grid 4.650 s, frame time 4.666667 s, player (3.466667, 5.333333), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 2.220110107 (exact 2.2201101073795506), shots in flight: (8.619255, 6.645835) v (2.282502, 1.946840); (8.133692, 4.702952) v (-2.793480, -1.093833); (2.392927, 3.119844) v (0.302252, -2.984735)
            4.80 s  walk to spitter | frame 144, grid 4.800 s, frame time 4.800000 s, player (3.466667, 5.866667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.853525170 (exact 1.8535251699276996), shots in flight: (8.923589, 6.905414) v (2.282502, 1.946840); (7.761228, 4.557107) v (-2.793480, -1.093833); (2.433227, 2.721880) v (0.302252, -2.984735)
            4.97 s  walk to spitter | frame 149, grid 4.950 s, frame time 4.966667 s, player (2.800000, 5.866667), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.387243470 (exact 1.387243469778976), shots in flight: (9.304006, 7.229887) v (2.282502, 1.946840); (7.295648, 4.374802) v (-2.793480, -1.093833); (2.483603, 2.224424) v (0.302252, -2.984735)
            5.10 s  face and swing at spitter | frame 153, grid 5.100 s, frame time 5.100000 s, player (2.800000, 6.400000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.000000000 (exact 0.9999999999999861), shots in flight: (9.608340, 7.489466) v (2.282502, 1.946840); (6.923184, 4.228958) v (-2.793480, -1.093833); (2.523903, 1.826459) v (0.302252, -2.984735)
            5.27 s  face and swing at spitter | frame 158, grid 5.250 s, frame time 5.266667 s, player (2.800000, 6.400000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.000000000 (exact 0.9999999999999861), shots in flight: (9.988756, 7.813939) v (2.282502, 1.946840); (6.457604, 4.046652) v (-2.793480, -1.093833); (2.574278, 1.329003) v (0.302252, -2.984735)
            5.40 s  face and swing at spitter | frame 162, grid 5.400 s, frame time 5.400000 s, player (2.800000, 6.400000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.000000000 (exact 0.9999999999999861), shots in flight: (10.293090, 8.073518) v (2.282502, 1.946840); (6.085140, 3.900808) v (-2.793480, -1.093833); (2.614578, 0.931039) v (0.302252, -2.984735)
            5.57 s  face and swing at spitter | frame 167, grid 5.550 s, frame time 5.566667 s, player (2.800000, 6.400000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.000000000 (exact 0.9999999999999861), shots in flight: (10.673507, 8.397991) v (2.282502, 1.946840); (5.619560, 3.718502) v (-2.793480, -1.093833); (2.664954, 0.433583) v (0.302252, -2.984735)
            5.70 s  walk to spitter | frame 171, grid 5.700 s, frame time 5.700000 s, player (2.800000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 11.216059914 (exact 11.216059914247973), shots in flight: (10.977841, 8.657570) v (2.282502, 1.946840); (5.247096, 3.572658) v (-2.793480, -1.093833); (2.705254, 0.035618) v (0.302252, -2.984735)
            5.87 s  walk to spitter | frame 176, grid 5.850 s, frame time 5.866667 s, player (3.466667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 10.550408102 (exact 10.550408101638125), shots in flight: (11.358258, 8.982043) v (2.282502, 1.946840); (4.781516, 3.390353) v (-2.793480, -1.093833); (2.755629, -0.461838) v (0.302252, -2.984735)
            6.00 s  walk to spitter | frame 180, grid 6.000 s, frame time 6.000000 s, player (4.000000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 10.017983829 (exact 10.017983829094566), shots in flight: (4.409052, 3.244508) v (-2.793480, -1.093833); (2.795929, -0.859803) v (0.302252, -2.984735)
            6.17 s  walk to spitter | frame 185, grid 6.150 s, frame time 6.166667 s, player (4.666667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 9.352599163 (exact 9.352599163393633), shots in flight: (3.943472, 3.062203) v (-2.793480, -1.093833)
            6.30 s  walk to spitter | frame 189, grid 6.300 s, frame time 6.300000 s, player (5.200000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 8.820430828 (exact 8.820430828479985), shots in flight: (3.571008, 2.916359) v (-2.793480, -1.093833)
            6.47 s  walk to spitter | frame 194, grid 6.450 s, frame time 6.466667 s, player (5.866667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 8.155434453 (exact 8.155434452627967), shots in flight: (3.105428, 2.734053) v (-2.793480, -1.093833)
            6.60 s  walk to spitter | frame 198, grid 6.600 s, frame time 6.600000 s, player (6.400000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 7.623647421 (exact 7.623647421018371), shots in flight: (2.732964, 2.588209) v (-2.793480, -1.093833); (13.900180, 6.994011) v (-2.994615, -0.179677)
            6.77 s  walk to spitter | frame 203, grid 6.750 s, frame time 6.766667 s, player (7.066667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 6.959246447 (exact 6.959246447073932), shots in flight: (2.267384, 2.405903) v (-2.793480, -1.093833); (13.401077, 6.964065) v (-2.994615, -0.179677)
            6.90 s  walk to spitter | frame 207, grid 6.900 s, frame time 6.900000 s, player (7.600000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 6.428063472 (exact 6.428063471995279), shots in flight: (1.894920, 2.260059) v (-2.793480, -1.093833); (13.001795, 6.940108) v (-2.994615, -0.179677)
            7.07 s  walk to spitter | frame 212, grid 7.050 s, frame time 7.066667 s, player (8.266667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 5.764643190 (exact 5.764643190268684), shots in flight: (1.429340, 2.077754) v (-2.793480, -1.093833); (12.502693, 6.910162) v (-2.994615, -0.179677)
            7.20 s  walk to spitter | frame 216, grid 7.200 s, frame time 7.200000 s, player (8.800000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 5.234500931 (exact 5.234500931320962), shots in flight: (1.056876, 1.931909) v (-2.793480, -1.093833); (12.103411, 6.886205) v (-2.994615, -0.179677)
            7.37 s  walk to spitter | frame 221, grid 7.350 s, frame time 7.366667 s, player (9.466667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 4.572866837 (exact 4.572866837238009), shots in flight: (0.591296, 1.749604) v (-2.793480, -1.093833); (11.604308, 6.856259) v (-2.994615, -0.179677)
            7.50 s  sidestep shot in flight | frame 225, grid 7.500 s, frame time 7.500000 s, player (10.000000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 4.044749683 (exact 4.044749683231343), shots in flight: (0.218832, 1.603760) v (-2.793480, -1.093833); (11.205026, 6.832302) v (-2.994615, -0.179677)
            7.67 s  walk to spitter | frame 230, grid 7.650 s, frame time 7.666667 s, player (10.000000, 5.733333), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 4.195765061 (exact 4.195765060682556), shots in flight: (10.705924, 6.802355) v (-2.994615, -0.179677)
            7.80 s  walk to spitter | frame 234, grid 7.800 s, frame time 7.800000 s, player (10.533333, 5.733333), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 3.690829476 (exact 3.690829476177716), shots in flight: (10.306642, 6.778399) v (-2.994615, -0.179677)
            7.97 s  walk to spitter | frame 239, grid 7.950 s, frame time 7.966667 s, player (11.200000, 5.733333), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 3.073181486 (exact 3.073181485764304), shots in flight: (9.807540, 6.748452) v (-2.994615, -0.179677)
            8.10 s  walk to spitter | frame 243, grid 8.100 s, frame time 8.100000 s, player (11.733333, 5.733333), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 2.596578946 (exact 2.596578945886735), shots in flight: (9.408258, 6.724495) v (-2.994615, -0.179677)
            8.27 s  walk to spitter | frame 248, grid 8.250 s, frame time 8.266667 s, player (12.400000, 5.733333), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 2.040697049 (exact 2.040697048668538), shots in flight: (8.909155, 6.694549) v (-2.994615, -0.179677)
            8.40 s  walk to spitter | frame 252, grid 8.400 s, frame time 8.400000 s, player (12.933333, 5.733333), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 1.655965646 (exact 1.6559656464499033), shots in flight: (8.509873, 6.670592) v (-2.994615, -0.179677)
            8.57 s  walk to spitter | frame 257, grid 8.550 s, frame time 8.566667 s, player (12.933333, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 1.223837317 (exact 1.2238373167123995), shots in flight: (8.010771, 6.640646) v (-2.994615, -0.179677)
            8.70 s  face and swing at spitter | frame 261, grid 8.700 s, frame time 8.700000 s, player (13.466667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.802772972 (exact 0.8027729719194937), shots in flight: (7.611489, 6.616689) v (-2.994615, -0.179677)
            8.87 s  face and swing at spitter | frame 266, grid 8.850 s, frame time 8.866667 s, player (13.466667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.802772972 (exact 0.8027729719194937), shots in flight: (7.112387, 6.586743) v (-2.994615, -0.179677)
            9.00 s  sidestep shot in flight | frame 270, grid 9.000 s, frame time 9.000000 s, player (13.466667, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.802772972 (exact 0.8027729719194937), shots in flight: (6.713105, 6.562786) v (-2.994615, -0.179677); (13.935586, 6.923509) v (-1.932407, -2.294734)
            9.17 s  sidestep shot in flight | frame 275, grid 9.150 s, frame time 9.166667 s, player (12.800000, 6.400000), hearts 3, stunned no, nearest spitter at (14.000000, 7.000000) distance 1.341640786 (exact 1.3416407864998858), shots in flight: (6.214002, 6.532840) v (-2.994615, -0.179677); (13.613519, 6.541053) v (-1.932407, -2.294734)
            9.30 s  walk to spitter | frame 2
[output cut at 20000 characters]
```

### Round 1: @run/bots/walker-r3-60 — `python3 bots.py {script}`

Script:

```text
bots walker
rooms 3
fps 60
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
walker  room 3: cleared in 9.5 s; hearts lost 2 (hit by: shot 2); attacks 6, dashes 0
            0.00 s  walk to spitter | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.708203932 (exact 6.708203932499369), shots in flight: none
            0.15 s  walk to spitter | frame 9, grid 0.150 s, frame time 0.150000 s, player (7.400000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.177378085 (exact 6.177378084592202), shots in flight: none
            0.30 s  walk to spitter | frame 18, grid 0.300 s, frame time 0.300000 s, player (6.800000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 5.660388679 (exact 5.660388679233966), shots in flight: none
            0.45 s  walk to spitter | frame 27, grid 0.450 s, frame time 0.450000 s, player (6.200000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 5.161395160 (exact 5.161395160225581), shots in flight: none
            0.60 s  walk to spitter | frame 36, grid 0.600 s, frame time 0.600000 s, player (5.600000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 4.686149806 (exact 4.686149805543999), shots in flight: none
            0.75 s  walk to spitter | frame 45, grid 0.750 s, frame time 0.750000 s, player (5.000000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 4.242640687 (exact 4.242640687119293), shots in flight: none
            0.90 s  walk to spitter | frame 54, grid 0.900 s, frame time 0.900000 s, player (4.400000, 4.000000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 3.841874542 (exact 3.8418745424597174), shots in flight: none
            1.05 s  walk to spitter | frame 63, grid 1.050 s, frame time 1.050000 s, player (4.400000, 3.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 3.394112550 (exact 3.3941125496954356), shots in flight: none
            1.20 s  walk to spitter | frame 72, grid 1.200 s, frame time 1.200000 s, player (3.800000, 3.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 3.000000000 (exact 3.0000000000000067), shots in flight: none
            1.35 s  walk to spitter | frame 81, grid 1.350 s, frame time 1.350000 s, player (3.800000, 2.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.545584412 (exact 2.545584412271578), shots in flight: none
            1.50 s  walk to spitter | frame 90, grid 1.500 s, frame time 1.500000 s, player (3.200000, 2.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.163330765 (exact 2.163330765278397), shots in flight: none
            1.65 s  walk to spitter | frame 99, grid 1.650 s, frame time 1.650000 s, player (3.200000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: none
            1.80 s  sidestep shot in flight | frame 108, grid 1.800 s, frame time 1.800000 s, player (2.600000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.341640786 (exact 1.3416407864998732), shots in flight: (2.030000, 1.040000) v (1.800000, 2.400000)
            1.95 s  sidestep shot in flight | frame 117, grid 1.950 s, frame time 1.950000 s, player (3.200000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: (2.300000, 1.400000) v (1.800000, 2.400000)
            2.10 s  walk to spitter | frame 126, grid 2.100 s, frame time 2.100000 s, player (3.800000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.163330765 (exact 2.1633307652784017), shots in flight: (2.570000, 1.760000) v (1.800000, 2.400000)
            2.25 s  HEART LOST | frame 135, source shot, player (3.200000, 2.200000), shot at (2.840000, 2.120000) v (1.800000, 2.400000); hearts now 2
            2.25 s  skipped decision | frame 135, grid 2.250 s, frame time 2.250000 s, reason: player stunned (0.300 s of stun left)
            2.40 s  skipped decision | frame 144, grid 2.400 s, frame time 2.400000 s, reason: player stunned (0.150 s of stun left)
            2.55 s  skipped decision | frame 153, grid 2.550 s, frame time 2.550000 s, reason: player stunned (0.000 s of stun left)
            2.57 s  walk to spitter | frame 154, grid 2.550 s, frame time 2.566667 s, player (3.200000, 2.200000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: none
            2.70 s  walk to spitter | frame 162, grid 2.700 s, frame time 2.700000 s, player (2.666667, 2.200000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.372750685 (exact 1.3727506854649334), shots in flight: (13.681166, 6.855622) v (-2.732863, -1.237523)
            2.85 s  face and swing at spitter | frame 171, grid 2.850 s, frame time 2.850000 s, player (2.666667, 1.600000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.896908270 (exact 0.8969082698049176), shots in flight: (13.271237, 6.669994) v (-2.732863, -1.237523)
            3.00 s  face and swing at spitter | frame 180, grid 3.000 s, frame time 3.000000 s, player (2.666667, 1.600000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.896908270 (exact 0.8969082698049176), shots in flight: (12.861307, 6.484366) v (-2.732863, -1.237523)
            3.15 s  face and swing at spitter | frame 189, grid 3.150 s, frame time 3.150000 s, player (2.666667, 1.600000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.896908270 (exact 0.8969082698049176), shots in flight: (12.451378, 6.298737) v (-2.732863, -1.237523)
            3.30 s  face and swing at spitter | frame 198, grid 3.300 s, frame time 3.300000 s, player (2.666667, 1.600000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 0.896908270 (exact 0.8969082698049176), shots in flight: (12.041449, 6.113109) v (-2.732863, -1.237523)
            3.45 s  walk to spitter | frame 207, grid 3.450 s, frame time 3.450000 s, player (2.666667, 1.600000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 5.440996641 (exact 5.440996640730861), shots in flight: (11.631519, 5.927480) v (-2.732863, -1.237523); (2.025433, 6.801624) v (0.381493, -2.975645)
            3.60 s  walk to spitter | frame 216, grid 3.600 s, frame time 3.600000 s, player (2.666667, 2.200000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 4.846075159 (exact 4.846075158769674), shots in flight: (11.221590, 5.741852) v (-2.732863, -1.237523); (2.082657, 6.355277) v (0.381493, -2.975645)
            3.75 s  walk to spitter | frame 225, grid 3.750 s, frame time 3.750000 s, player (2.666667, 2.800000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 4.252580916 (exact 4.252580915684555), shots in flight: (10.811660, 5.556224) v (-2.732863, -1.237523); (2.139881, 5.908930) v (0.381493, -2.975645)
            3.90 s  walk to spitter | frame 234, grid 3.900 s, frame time 3.900000 s, player (2.666667, 3.400000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.661208058 (exact 3.6612080580655983), shots in flight: (10.401731, 5.370595) v (-2.732863, -1.237523); (2.197105, 5.462583) v (0.381493, -2.975645)
            4.05 s  sidestep shot in flight | frame 243, grid 4.050 s, frame time 4.050000 s, player (2.666667, 4.000000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.073181486 (exact 3.073181485764298), shots in flight: (9.991802, 5.184967) v (-2.732863, -1.237523); (2.254329, 5.016237) v (0.381493, -2.975645)
            4.20 s  walk to spitter | frame 252, grid 4.200 s, frame time 4.200000 s, player (3.266667, 4.000000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 3.256446598 (exact 3.2564465978186217), shots in flight: (9.581872, 4.999338) v (-2.732863, -1.237523); (2.311553, 4.569890) v (0.381493, -2.975645)
            4.35 s  walk to spitter | frame 261, grid 4.350 s, frame time 4.350000 s, player (3.266667, 4.600000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 2.713750992 (exact 2.7137509916063567), shots in flight: (9.171943, 4.813710) v (-2.732863, -1.237523); (2.368777, 4.123543) v (0.381493, -2.975645)
            4.50 s  walk to spitter | frame 270, grid 4.500 s, frame time 4.500000 s, player (3.266667, 5.200000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 2.201009869 (exact 2.201009869229234), shots in flight: (8.762013, 4.628082) v (-2.732863, -1.237523); (2.426000, 3.677196) v (0.381493, -2.975645)
            4.65 s  walk to spitter | frame 279, grid 4.650 s, frame time 4.650000 s, player (3.266667, 5.800000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.744833644 (exact 1.7448336437736665), shots in flight: (8.352084, 4.442453) v (-2.732863, -1.237523); (2.483224, 3.230850) v (0.381493, -2.975645)
            4.80 s  walk to spitter | frame 288, grid 4.800 s, frame time 4.800000 s, player (2.666667, 5.800000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 1.372750685 (exact 1.3727506854649438), shots in flight: (7.942155, 4.256825) v (-2.732863, -1.237523); (2.540448, 2.784503) v (0.381493, -2.975645)
            4.95 s  face and swing at spitter | frame 297, grid 4.950 s, frame time 4.950000 s, player (2.666667, 6.400000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 0.896908270 (exact 0.8969082698049272), shots in flight: (7.532225, 4.071196) v (-2.732863, -1.237523); (2.597672, 2.338156) v (0.381493, -2.975645)
            5.10 s  face and swing at spitter | frame 306, grid 5.100 s, frame time 5.100000 s, player (2.666667, 6.400000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 0.896908270 (exact 0.8969082698049272), shots in flight: (7.122296, 3.885568) v (-2.732863, -1.237523); (2.654896, 1.891809) v (0.381493, -2.975645); (13.657128, 6.929722) v (-2.938900, -0.602383)
            5.25 s  face and swing at spitter | frame 315, grid 5.250 s, frame time 5.250000 s, player (2.666667, 6.400000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 0.896908270 (exact 0.8969082698049272), shots in flight: (6.712367, 3.699940) v (-2.732863, -1.237523); (2.712120, 1.445463) v (0.381493, -2.975645); (13.216293, 6.839364) v (-2.938900, -0.602383)
            5.40 s  face and swing at spitter | frame 324, grid 5.400 s, frame time 5.400000 s, player (2.666667, 6.400000), hearts 2, stunned no, nearest spitter at (2.000000, 7.000000) distance 0.896908270 (exact 0.8969082698049272), shots in flight: (6.302437, 3.514311) v (-2.732863, -1.237523); (2.769344, 0.999116) v (0.381493, -2.975645); (12.775458, 6.749007) v (-2.938900, -0.602383)
            5.55 s  walk to spitter | frame 333, grid 5.550 s, frame time 5.550000 s, player (2.666667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 11.349204573 (exact 11.349204573204425), shots in flight: (5.892508, 3.328683) v (-2.732863, -1.237523); (2.826568, 0.552769) v (0.381493, -2.975645); (12.334623, 6.658649) v (-2.938900, -0.602383)
            5.70 s  walk to spitter | frame 342, grid 5.700 s, frame time 5.700000 s, player (3.266667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 10.750090439 (exact 10.750090438896047), shots in flight: (5.482578, 3.143054) v (-2.732863, -1.237523); (2.883792, 0.106422) v (0.381493, -2.975645); (11.893788, 6.568292) v (-2.938900, -0.602383)
            5.85 s  walk to spitter | frame 351, grid 5.850 s, frame time 5.850000 s, player (3.866667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 10.151080950 (exact 10.151080949556267), shots in flight: (5.072649, 2.957426) v (-2.732863, -1.237523); (2.941016, -0.339924) v (0.381493, -2.975645); (11.452953, 6.477934) v (-2.938900, -0.602383)
            6.00 s  walk to spitter | frame 360, grid 6.000 s, frame time 6.000000 s, player (4.466667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 9.552195792 (exact 9.552195791777104), shots in flight: (4.662720, 2.771798) v (-2.732863, -1.237523); (2.998240, -0.786271) v (0.381493, -2.975645); (11.012118, 6.387577) v (-2.938900, -0.602383)
            6.15 s  walk to spitter | frame 369, grid 6.150 s, frame time 6.150000 s, player (5.066667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 8.953459915 (exact 8.953459914717007), shots in flight: (4.252790, 2.586169) v (-2.732863, -1.237523); (10.571283, 6.297220) v (-2.938900, -0.602383)
            6.30 s  walk to spitter | frame 378, grid 6.300 s, frame time 6.300000 s, player (5.666667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 8.354905412 (exact 8.354905412058494), shots in flight: (3.842861, 2.400541) v (-2.732863, -1.237523); (10.130448, 6.206862) v (-2.938900, -0.602383)
            6.45 s  walk to spitter | frame 387, grid 6.450 s, frame time 6.450000 s, player (6.266667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 7.756574272 (exact 7.7565742724765006), shots in flight: (3.432932, 2.214912) v (-2.732863, -1.237523); (9.689613, 6.116505) v (-2.938900, -0.602383)
            6.60 s  walk to spitter | frame 396, grid 6.600 s, frame time 6.600000 s, player (6.866667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 7.158522504 (exact 7.158522504291259), shots in flight: (3.023002, 2.029284) v (-2.732863, -1.237523); (9.248778, 6.026147) v (-2.938900, -0.602383)
            6.75 s  walk to spitter | frame 405, grid 6.750 s, frame time 6.750000 s, player (7.466667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 6.560826506 (exact 6.5608265061990805), shots in flight: (2.613073, 1.843656) v (-2.732863, -1.237523); (8.807943, 5.935790) v (-2.938900, -0.602383)
            6.90 s  sidestep shot in flight | frame 414, grid 6.900 s, frame time 6.900000 s, player (8.066667, 6.400000), hearts 2, stunned no, nearest spitter at (14.000000, 7.000000) distance 5.963593249 (exact 5.963593249413013), shots in flight: (2.203143, 1.658027) v (-2.732863, -1.237523); (8.367108, 5.845432) v (-2.938900, -0.602383)
            6.97 s  HEART LOST | frame 418, source shot, player (8.066667, 6.133333), shot at (8.171181, 5.805273) v (-2.938900, -0.602383); hearts now 1
            7.05 s  skipped decision | frame 423, grid 7.050 s, frame time 7.050000 s, reason: player stunned (0.217 s of stun left)
            7.20 s  skipped decision | frame 432, grid 7.200 s, frame time 7.200000 s, reason: player stunned (0.067 s of stun left)
            7.28 s  walk to spitter | frame 437, grid 7.200 s, frame time 7.283333 s, player (8.066667, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 5.996295152 (exact 5.9962951524716965), shots in flight: (1.155546, 1.183643) v (-2.732863, -1.237523)
            7.35 s  walk to spitter | frame 441, grid 7.350 s, frame time 7.350000 s, player (8.333333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 5.732558087 (exact 5.732558087121512), shots in flight: (0.973355, 1.101142) v (-2.732863, -1.237523)
            7.50 s  walk to spitter | frame 450, grid 7.500 s, frame time 7.500000 s, player (8.933333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 5.140255074 (exact 5.140255073653667), shots in flight: (0.563426, 0.915514) v (-2.732863, -1.237523); (13.651560, 6.966990) v (-2.986627, -0.282944)
            7.65 s  walk to spitter | frame 459, grid 7.650 s, frame time 7.650000 s, player (9.533333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 4.549969475 (exact 4.549969474867088), shots in flight: (13.203566, 6.924548) v (-2.986627, -0.282944)
            7.80 s  walk to spitter | frame 468, grid 7.800 s, frame time 7.800000 s, player (10.133333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 3.962602960 (exact 3.9626029604569637), shots in flight: (12.755572, 6.882107) v (-2.986627, -0.282944)
            7.95 s  sidestep shot in flight | frame 477, grid 7.950 s, frame time 7.950000 s, player (10.733333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 3.379677828 (exact 3.379677828169765), shots in flight: (12.307578, 6.839665) v (-2.986627, -0.282944)
            8.10 s  walk to spitter | frame 486, grid 8.100 s, frame time 8.100000 s, player (10.733333, 5.533333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 3.580813067 (exact 3.580813067198887), shots in flight: (11.859584, 6.797224) v (-2.986627, -0.282944)
            8.25 s  walk to spitter | frame 495, grid 8.250 s, frame time 8.250000 s, player (11.333333, 5.533333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 3.043389923 (exact 3.043389922803567), shots in flight: (11.411590, 6.754782) v (-2.986627, -0.282944)
            8.40 s  walk to spitter | frame 504, grid 8.400 s, frame time 8.400000 s, player (11.933333, 5.533333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 2.534210374 (exact 2.5342103744997764), shots in flight: (10.963596, 6.712341) v (-2.986627, -0.282944)
            8.55 s  walk to spitter | frame 513, grid 8.550 s, frame time 8.550000 s, player (12.533333, 5.533333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 2.074179891 (exact 2.0741798914805547), shots in flight: (10.515601, 6.669899) v (-2.986627, -0.282944)
            8.70 s  walk to spitter | frame 522, grid 8.700 s, frame time 8.700000 s, player (13.133333, 5.533333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 1.703590979 (exact 1.7035909785574324), shots in flight: (10.067607, 6.627458) v (-2.986627, -0.282944)
            8.85 s  walk to spitter | frame 531, grid 8.850 s, frame time 8.850000 s, player (13.133333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 1.225651754 (exact 1.2256517540567007), shots in flight: (9.619613, 6.585016) v (-2.986627, -0.282944)
            9.00 s  face and swing at spitter | frame 540, grid 9.000 s, frame time 9.000000 s, player (13.733333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.906764701 (exact 0.9067647005823761), shots in flight: (9.171619, 6.542574) v (-2.986627, -0.282944)
            9.15 s  face and swing at spitter | frame 549, grid 9.150 s, frame time 9.150000 s, player (13.733333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.906764701 (exact 0.9067647005823761), shots in flight: (8.723625, 6.500133) v (-2.986627, -0.282944)
            9.30 s  face and swing at spitter | frame 558, grid 9.300 s, frame time 9.300000 s, player (13.733333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.906764701 (exact 0.9067647005823761), shots in flight: (8.275631, 6.457691) v (-2.986627, -0.282944)
            9.45 s  face and swing at spitter | frame 567, grid 9.450 s, frame time 9.450000 s, player (13.733333, 6.133333), hearts 1, stunned no, nearest spitter at (14.000000, 7.000000) distance 0.906764701 (exact 0.9067647005823761), shots in flight: (7.827637, 6.415250) v (-2.986627, -0.282944)
walker  total: cleared 1/1, hearts lost 2, dashes 0
```

### Round 1: @run/bots/walker-r1-30 — `python3 bots.py {script}`

Script:

```text
bots walker
rooms 1
fps 30
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
walker  room 1: NOT cleared (4.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
            0.00 s  walk to grub | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest grub at (8.000000, 0.000000) distance 4.000000000 (exact 4.0), shots in flight: none
            0.17 s  walk to grub | frame 5, grid 0.150 s, frame time 0.166667 s, player (8.000000, 3.333333), hearts 3, stunned no, nearest grub at (8.000000, 0.166667) distance 3.166666667 (exact 3.166666666666667), shots in flight: none
            0.30 s  walk to grub | frame 9, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.5000000000000004), shots in flight: none
            0.47 s  face and swing at grub | frame 14, grid 0.450 s, frame time 0.466667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            0.60 s  face and swing at grub | frame 18, grid 0.600 s, frame time 0.600000 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            0.77 s  face and swing at grub | frame 23, grid 0.750 s, frame time 0.766667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            0.90 s  face and swing at grub | frame 27, grid 0.900 s, frame time 0.900000 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
            1.07 s  face and swing at grub | frame 32, grid 1.050 s, frame time 1.066667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 1.466667) distance 0.666666667 (exact 0.6666666666666672), shots in flight: none
            1.10 s  HEART LOST | frame 33, source grub, player (8.000000, 2.133333), grub grub at (8.000000, 1.733333); hearts now 2
            1.20 s  skipped decision | frame 36, grid 1.200 s, frame time 1.200000 s, reason: player stunned (0.200 s of stun left)
            1.37 s  skipped decision | frame 41, grid 1.350 s, frame time 1.366667 s, reason: player stunned (0.033 s of stun left)
            1.43 s  face and swing at grub | frame 43, grid 1.350 s, frame time 1.433333 s, player (8.000000, 2.133333), hearts 2, stunned no, nearest grub at (8.000000, 1.733333) distance 0.400000000 (exact 0.4000000000000006), shots in flight: none
            1.50 s  walk to grub | frame 45, grid 1.500 s, frame time 1.500000 s, player (8.000000, 2.133333), hearts 2, stunned no, nearest grub at (4.417261, 3.531738) distance 3.845979201 (exact 3.8459792005106057), shots in flight: none
            1.67 s  walk to grub | frame 50, grid 1.650 s, frame time 1.666667 s, player (7.333333, 2.133333), hearts 2, stunned no, nearest grub at (4.569694, 3.464449) distance 3.067502526 (exact 3.0675025256704145), shots in flight: none
            1.80 s  face and swing at grub | frame 54, grid 1.800 s, frame time 1.800000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (4.686468, 3.400191) distance 2.464132366 (exact 2.4641323661562193), shots in flight: none
            1.97 s  face and swing at grub | frame 59, grid 1.950 s, frame time 1.966667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (4.829421, 3.314505) distance 2.297465699 (exact 2.297465699489551), shots in flight: none
            2.10 s  face and swing at grub | frame 63, grid 2.100 s, frame time 2.100000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (4.943783, 3.245955) distance 2.164132366 (exact 2.164132366156217), shots in flight: none
            2.27 s  face and swing at grub | frame 68, grid 2.250 s, frame time 2.266667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.40 s  face and swing at grub | frame 72, grid 2.400 s, frame time 2.400000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.57 s  face and swing at grub | frame 77, grid 2.550 s, frame time 2.566667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.70 s  face and swing at grub | frame 81, grid 2.700 s, frame time 2.700000 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.086736, 3.160269) distance 1.997465699 (exact 1.9974656994895488), shots in flight: none
            2.87 s  face and swing at grub | frame 86, grid 2.850 s, frame time 2.866667 s, player (6.800000, 2.133333), hearts 2, stunned no, nearest grub at (5.544186, 2.886072) distance 1.464132366 (exact 1.4641323661562147), shots in flight: none
            3.00 s  HEART LOST | frame 90, source grub, player (6.800000, 2.133333), grub grub at (6.459086, 2.337678); hearts now 1
            3.00 s  skipped decision | frame 90, grid 3.000 s, frame time 3.000000 s, reason: player stunned (0.300 s of stun left)
            3.17 s  skipped decision | frame 95, grid 3.150 s, frame time 3.166667 s, reason: player stunned (0.133 s of stun left)
            3.30 s  skipped decision | frame 99, grid 3.300 s, frame time 3.300000 s, reason: player stunned (0.000 s of stun left)
            3.33 s  face and swing at grub | frame 100, grid 3.300 s, frame time 3.333333 s, player (6.800000, 2.133333), hearts 1, stunned no, nearest grub at (6.459086, 2.337678) distance 0.397465699 (exact 0.3974656994895464), shots in flight: none
            3.47 s  walk to grub | frame 104, grid 3.450 s, frame time 3.466667 s, player (6.800000, 2.133333), hearts 1, stunned no, nearest grub at (11.626085, 3.220944) distance 4.947120155 (exact 4.9471201549117545), shots in flight: none
            3.60 s  walk to grub | frame 108, grid 3.600 s, frame time 3.600000 s, player (7.333333, 2.133333), hearts 1, stunned no, nearest grub at (11.496511, 3.189526) distance 4.295065590 (exact 4.295065590215387), shots in flight: none
            3.77 s  walk to grub | frame 113, grid 3.750 s, frame time 3.766667 s, player (8.000000, 2.133333), hearts 1, stunned no, nearest grub at (11.336101, 3.144341) distance 3.485930257 (exact 3.485930256555839), shots in flight: none
            3.90 s  walk to grub | frame 117, grid 3.900 s, frame time 3.900000 s, player (8.533333, 2.133333), hearts 1, stunned no, nearest grub at (11.209798, 3.101668) distance 2.846249365 (exact 2.8462493648299154), shots in flight: none
            4.07 s  face and swing at grub | frame 122, grid 4.050 s, frame time 4.066667 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (11.056727, 3.035944) distance 2.064495181 (exact 2.064495180648655), shots in flight: none
            4.20 s  face and swing at grub | frame 126, grid 4.200 s, frame time 4.200000 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.37 s  face and swing at grub | frame 131, grid 4.350 s, frame time 4.366667 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.50 s  face and swing at grub | frame 135, grid 4.500 s, frame time 4.500000 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.67 s  face and swing at grub | frame 140, grid 4.650 s, frame time 4.666667 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.996769, 3.006797) distance 1.997828514 (exact 1.9978285139819874), shots in flight: none
            4.80 s  face and swing at grub | frame 144, grid 4.800 s, frame time 4.800000 s, player (9.200000, 2.133333), hearts 1, stunned no, nearest grub at (10.037451, 2.540443) distance 0.931161847 (exact 0.9311618473153187), shots in flight: none
            4.87 s  HEART LOST | frame 146, source grub, player (9.200000, 2.133333), grub grub at (9.557791, 2.307267); hearts now 0
walker  total: cleared 0/1, hearts lost 3, dashes 0
```

### Round 1: @run/bots/walker-r1-60 — `python3 bots.py {script}`

Script:

```text
bots walker
rooms 1
fps 60
log on
```

Exit: 0 (0.0 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
            0.00 s  walk to grub | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest grub at (8.000000, 0.000000) distance 4.000000000 (exact 4.0), shots in flight: none
            0.15 s  walk to grub | frame 9, grid 0.150 s, frame time 0.150000 s, player (8.000000, 3.400000), hearts 3, stunned no, nearest grub at (8.000000, 0.150000) distance 3.250000000 (exact 3.2499999999999982), shots in flight: none
            0.30 s  face and swing at grub | frame 18, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.4999999999999964), shots in flight: none
            0.45 s  face and swing at grub | frame 27, grid 0.450 s, frame time 0.450000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.450000) distance 2.350000000 (exact 2.349999999999996), shots in flight: none
            0.60 s  face and swing at grub | frame 36, grid 0.600 s, frame time 0.600000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.600000) distance 2.200000000 (exact 2.199999999999996), shots in flight: none
            0.75 s  face and swing at grub | frame 45, grid 0.750 s, frame time 0.750000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.750000) distance 2.050000000 (exact 2.0499999999999954), shots in flight: none
            0.90 s  face and swing at grub | frame 54, grid 0.900 s, frame time 0.900000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.800000) distance 2.000000000 (exact 1.9999999999999956), shots in flight: none
            1.05 s  face and swing at grub | frame 63, grid 1.050 s, frame time 1.050000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.800000) distance 2.000000000 (exact 1.9999999999999956), shots in flight: none
            1.20 s  face and swing at grub | frame 72, grid 1.200 s, frame time 1.200000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.800000) distance 2.000000000 (exact 1.9999999999999956), shots in flight: none
            1.35 s  face and swing at grub | frame 81, grid 1.350 s, frame time 1.350000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 1.066667) distance 1.733333333 (exact 1.7333333333333287), shots in flight: none
            1.50 s  HEART LOST | frame 90, source grub, player (8.000000, 2.800000), grub grub at (8.000000, 2.266667); hearts now 2
            1.50 s  skipped decision | frame 90, grid 1.500 s, frame time 1.500000 s, reason: player stunned (0.300 s of stun left)
            1.65 s  skipped decision | frame 99, grid 1.650 s, frame time 1.650000 s, reason: player stunned (0.150 s of stun left)
            1.80 s  skipped decision | frame 108, grid 1.800 s, frame time 1.800000 s, reason: player stunned (0.000 s of stun left)
            1.82 s  face and swing at grub | frame 109, grid 1.800 s, frame time 1.816667 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            1.95 s  face and swing at grub | frame 117, grid 1.950 s, frame time 1.950000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            2.10 s  face and swing at grub | frame 126, grid 2.100 s, frame time 2.100000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            2.25 s  face and swing at grub | frame 135, grid 2.250 s, frame time 2.250000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (8.000000, 2.266667) distance 0.533333333 (exact 0.5333333333333288), shots in flight: none
            2.40 s  walk to grub | frame 144, grid 2.400 s, frame time 2.400000 s, player (8.000000, 2.800000), hearts 2, stunned no, nearest grub at (5.335539, 3.458223) distance 2.744560270 (exact 2.7445602699534217), shots in flight: none
            2.55 s  face and swing at grub | frame 153, grid 2.550 s, frame time 2.550000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.479779, 3.417169) distance 2.016964246 (exact 2.016964245671973), shots in flight: none
            2.70 s  face and swing at grub | frame 162, grid 2.700 s, frame time 2.700000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.511514, 3.406969) distance 1.983630912 (exact 1.9836309123386402), shots in flight: none
            2.85 s  face and swing at grub | frame 171, grid 2.850 s, frame time 2.850000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.511514, 3.406969) distance 1.983630912 (exact 1.9836309123386402), shots in flight: none
            3.00 s  face and swing at grub | frame 180, grid 3.000 s, frame time 3.000000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.511514, 3.406969) distance 1.983630912 (exact 1.9836309123386402), shots in flight: none
            3.15 s  face and swing at grub | frame 189, grid 3.150 s, frame time 3.150000 s, player (7.400000, 2.800000), hearts 2, stunned no, nearest grub at (5.892328, 3.284573) distance 1.583630912 (exact 1.5836309123386392), shots in flight: none
            3.28 s  HEART LOST | frame 197, source grub, player (7.400000, 2.800000), grub grub at (6.907832, 2.958185); hearts now 1
            3.30 s  skipped decision | frame 198, grid 3.300 s, frame time 3.300000 s, reason: player stunned (0.283 s of stun left)
            3.45 s  skipped decision | frame 207, grid 3.450 s, frame time 3.450000 s, reason: player stunned (0.133 s of stun left)
            3.60 s  face and swing at grub | frame 216, grid 3.600 s, frame time 3.600000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            3.75 s  face and swing at grub | frame 225, grid 3.750 s, frame time 3.750000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            3.90 s  face and swing at grub | frame 234, grid 3.900 s, frame time 3.900000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            4.05 s  face and swing at grub | frame 243, grid 4.050 s, frame time 4.050000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (6.907832, 2.958185) distance 0.516964246 (exact 0.5169642456719702), shots in flight: none
            4.20 s  walk to grub | frame 252, grid 4.200 s, frame time 4.200000 s, player (7.400000, 2.800000), hearts 1, stunned no, nearest grub at (10.854408, 3.334326) distance 3.495488595 (exact 3.4954885948648555), shots in flight: none
            4.35 s  walk to grub | frame 261, grid 4.350 s, frame time 4.350000 s, player (8.000000, 2.800000), hearts 1, stunned no, nearest grub at (10.706585, 3.308902) distance 2.754012647 (exact 2.7540126472547657), shots in flight: none
            4.50 s  face and swing at grub | frame 270, grid 4.500 s, frame time 4.500000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.559989, 3.277217) distance 2.017248561 (exact 2.0172485605352772), shots in flight: none
            4.65 s  face and swing at grub | frame 279, grid 4.650 s, frame time 4.650000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.527601, 3.269332) distance 1.983915227 (exact 1.9839152272019436), shots in flight: none
            4.80 s  face and swing at grub | frame 288, grid 4.800 s, frame time 4.800000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.527601, 3.269332) distance 1.983915227 (exact 1.9839152272019436), shots in flight: none
            4.95 s  face and swing at grub | frame 297, grid 4.950 s, frame time 4.950000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.527601, 3.269332) distance 1.983915227 (exact 1.9839152272019436), shots in flight: none
            5.10 s  face and swing at grub | frame 306, grid 5.100 s, frame time 5.100000 s, player (8.600000, 2.800000), hearts 1, stunned no, nearest grub at (10.138956, 3.174704) distance 1.583915227 (exact 1.5839152272019446), shots in flight: none
            5.23 s  HEART LOST | frame 314, source grub, player (8.600000, 2.800000), grub grub at (9.102566, 2.922365); hearts now 0
walker  total: cleared 0/1, hearts lost 3, dashes 0
```

### Round 2: @run/trace/c1-stand-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 9.5 4
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.50,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.50,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.50,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.667 frame=20 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.43,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.467 frame=44 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.43,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.500 frame=45 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.43,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.000 frame=60 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.43,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.033 frame=61 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.17,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.833 frame=85 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.17,4.00,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.867 frame=86 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.17,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=3.000 frame=90 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.17,4.00,hp=2,windup:0.367) | end
```

### Round 2: @run/trace/c1-stand-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 9.5 4
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.50,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.50,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.50,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.633 frame=38 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.57,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.433 frame=86 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.57,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.450 frame=87 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.57,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=1.950 frame=117 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.57,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.967 frame=118 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.43,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.767 frame=166 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.43,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.783 frame=167 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.43,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=3.000 frame=180 pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.43,4.00,hp=2,windup:0.283) | end
```

### Round 2: @run/trace/c2-side-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 10 4
0.1 move up
0.35 stop
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(8.00,2.93) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.667 frame=50 pos=(8.00,2.93) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.60,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.167 frame=65 pos=(8.00,2.93) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.60,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.267 frame=68 pos=(8.00,2.93) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.88,3.25,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.000 frame=90 pos=(8.00,2.93) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.067 stun_left=0.000 | grub(7.88,3.25,hp=2,recovery:0.067) | end
```

### Round 2: @run/trace/c2-side-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
0.1 move up
0.35 stop
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,3.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=1.633 frame=98 pos=(8.00,3.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.60,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=2.133 frame=128 pos=(8.00,3.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.60,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=2.200 frame=132 pos=(8.00,3.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.80,3.50,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.000 frame=180 pos=(8.00,3.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.80,3.50,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.000 frame=180 pos=(8.00,3.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.80,3.50,hp=2,approach:-0.000) | end
```

### Round 2: @run/trace/c3-dash-late-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 10 4
0.65 dash up
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.533 frame=16 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.700 frame=21 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(8.67,4.00,hp=2,lunge:0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=0.933 frame=28 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.60,4.00,hp=2,recovery:0.700) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.000 frame=90 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.74,2.64,hp=2,approach:0.000) | end
```

### Round 2: @run/trace/c3-dash-late-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
0.65 dash up
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.667 frame=40 pos=(8.00,3.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(8.80,4.00,hp=2,lunge:0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=0.900 frame=54 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.60,4.00,hp=2,recovery:0.717) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.000 frame=180 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.74,2.62,hp=2,approach:-0.000) | end
```

### Round 2: @run/trace/c6-kill-windup-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn runner 9.2 4
0.1 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.20,4.00,hp=1,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.20,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.133 frame=4 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('runner', 'defeated')]}; cleared
t=1.133 frame=34 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/trace/c6-kill-windup-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn runner 9.2 4
0.1 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.20,4.00,hp=1,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | runner(9.20,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.117 frame=7 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': [('runner', 'defeated')]}; cleared
t=1.117 frame=67 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/play/edge-dist0 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn grub 8 4
end 1.5
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
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
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~~     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~~     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.533  YOU ARE HIT by a grub — hearts 2/3
   [0.53 s] hearts 2/3
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
   [1.00 s] hearts 2/3
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
  1.350  a grub rears back
   [1.35 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.1,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.1,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
end at 1.50 s: hearts 2/3, enemies left 1
```

### Round 2: @run/trace/graze-370-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn spitter 1 3.70
1.3 move up
1.4 stop
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=54 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=108 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=0.600,cue=True) | aim
t=4.100 frame=123 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(1.00,3.70,hp=2,fire_in=0.100,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.200 frame=126 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | spitter(1.00,3.70,hp=2,fire_in=2.400,cue=False) | spit
t=4.900 frame=147 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=1.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.000 frame=150 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=1.600,cue=False) | end
```

### Round 2: @run/trace/graze-370-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 1 3.70
1.3 move up
1.4 stop
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=108 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=0.600,cue=True) | aim
t=4.117 frame=247 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(1.00,3.70,hp=2,fire_in=0.083,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.200 frame=252 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 | spitter(1.00,3.70,hp=2,fire_in=2.400,cue=False) | spit
t=4.917 frame=295 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=1.683,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.000 frame=300 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.70,hp=2,fire_in=1.600,cue=False) | end
```

### Round 2: @run/trace/graze-373-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn spitter 1 3.73
1.3 move up
1.4 stop
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=54 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=108 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=0.600,cue=True) | aim
t=4.100 frame=123 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(1.00,3.73,hp=2,fire_in=0.100,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.200 frame=126 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | spitter(1.00,3.73,hp=2,fire_in=2.400,cue=False) | spit
t=4.900 frame=147 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=1.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.000 frame=150 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=1.600,cue=False) | end
```

### Round 2: @run/trace/graze-373-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 1 3.73
1.3 move up
1.4 stop
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=108 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=0.600,cue=True) | aim
t=4.117 frame=247 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(1.00,3.73,hp=2,fire_in=0.083,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.200 frame=252 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 | spitter(1.00,3.73,hp=2,fire_in=2.400,cue=False) | spit
t=4.917 frame=295 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=1.683,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.000 frame=300 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.73,hp=2,fire_in=1.600,cue=False) | end
```

### Round 2: @run/trace/graze-376-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn spitter 1 3.76
1.3 move up
1.4 stop
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=54 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=108 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=0.600,cue=True) | aim
t=4.100 frame=123 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(1.00,3.76,hp=2,fire_in=0.100,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.200 frame=126 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 | spitter(1.00,3.76,hp=2,fire_in=2.400,cue=False) | spit
t=4.900 frame=147 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=1.700,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.000 frame=150 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=1.600,cue=False) | end
```

### Round 2: @run/trace/graze-376-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 1 3.76
1.3 move up
1.4 stop
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=1.800,cue=False) | setup
t=1.200 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=0.600,cue=True) | aim
t=1.800 frame=108 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=2.400,cue=False) | spit
t=3.600 frame=216 pos=(8.00,3.60) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=0.600,cue=True) | aim
t=4.117 frame=247 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(1.00,3.76,hp=2,fire_in=0.083,cue=True) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.200 frame=252 pos=(8.00,3.60) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 | spitter(1.00,3.76,hp=2,fire_in=2.400,cue=False) | spit
t=4.917 frame=295 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=1.683,cue=False) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.000 frame=300 pos=(8.00,3.60) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(1.00,3.76,hp=2,fire_in=1.600,cue=False) | end
```
>>>END
