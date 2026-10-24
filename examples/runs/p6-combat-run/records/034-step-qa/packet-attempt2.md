# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/28-studio-to-qa.md
next_seq: 29
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/29-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/28-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 28
from: studio
to: qa
stage: Verify
outcome: routed
---
# 28: studio → qa — second verification round: manual check, independent runs, raw captures

## Task

Verify Build 0.5 again against `design/combat.md` (AC-1…AC-17) at 30 and 60 FPS, covering the three gaps below, and report to `studio`. Do not edit the build or `manual.md`.

## Context

Goal G-001 is "combat feels monotonous" (Owner, Japanese: 戦闘が単調なので改善したい). Your first round (26) found no failing criterion, but left gaps:

1. `ManualTest` errored with `FileNotFoundError` because your workspace had no `manual.md` beside `repo/`. That is a layout problem, not a build result. The Owner has already placed the draft `manual.md` (D-005, unchanged) in the project directory.
2. Several criteria rest on the repo's own test suite only.
3. A separate visual review (art director) of the player view could not run because no build output was available to that reviewer. It can only proceed from output you capture.

## Findings

Nothing new from the Studio. The work for this round:

### A. ManualTest and AC-15

- `ManualTest` looks for `manual.md` in the directory above `repo/`.
  - If you can run commands in a scratch location, build a layout there: a directory holding the project's `manual.md` (unchanged) next to a copy of `repo/`. Run `run_tests` from the copy. Do not write into the project's own paths.
  - If no such layout is possible, compare statically: read the glyph table in `repo/play.py` and the phrases `ManualTest` requires in `repo/tests/test_game.py` against `manual.md`. Report it as "static check, not a test run".
  - Mark `ManualTest` pass or fail only if the test itself ran. A static check can support AC-15 but must be labeled as one.
- Check AC-15 again for where the practice room is described. A reviewer noted that `manual.md` mentions the practice room under "Script" and "Rooms and runs" and not in its on-screen section. Compare with the AC-15 wording and judge it yourself.
- If `manual.md` and the glyph table or required phrases disagree, report the exact missing or differing item. Do not fix it.

### B. Independent runs for the criteria that had only suite evidence

Exercise these with your own scripts and label each as observed:

- AC-3, AC-5, AC-9, AC-10, AC-11, AC-12, AC-14.
- AC-13: the run-over text and the restart by attack in the player view. Let the script run at least 2.0 s past going down, then give an attack.
- Pause (F11) stays "not verifiable".

### C. Raw captures

Include in your report a "Captures" section with verbatim output (not summaries) from `run_play` (player view), and `run_trace` where it helps you read timing. Run each script at `fps 30` and `fps 60`. You may cut long stretches of identical frames, but mark each cut and keep every draw around events. Suggested exercises, using the script format in `manual.md`:

- Practice room, one grub: `room empty`, `player 8 4`, `spawn grub 4 4`, a long enough `end`.
  - An idle player until the first bite.
  - The same with an `attack` timed (from the trace) during the grub's wind-up.
  - The same with an `attack` timed during its recovery.
- Room 4 with `end 8`: one run with a `move` away, one with a `dash`.
- Room 3: walk up to a spitter and `attack` twice.
- Room 1 with no inputs and a long `end` (20), to reach the down state and the run-over screen. Or an idle player against a practice-room grub until three hearts are lost. Then an `attack` after the run-over screen appears.

Also state a plain fact: does the player view output any color (ANSI codes or markup), or plain text only? If it does, include a short sample.

## Decisions already made

- D-001: attack, dash and pause are the only inputs.
- D-002: rework existing enemy behavior first (Option A).
- D-003: room mix is across rooms; zero hearts ends the run; a room clear heals one heart.
- D-004: one sequential change set on the existing simulation.
- D-005: the Owner placed the draft `manual.md`; it is not edited in this Goal's steps.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Verify from the spec, acceptance criteria and build output, not from any explanation of why it should work.
- Keep suite evidence and your own observations clearly separate.
- You may find that more than one round of runs is needed. Use your allowed rounds to complete A, B and C.

## Open questions

1. Can `ManualTest` get a valid result by running it in a layout with `manual.md` beside the repo copy? If not, say exactly what blocked it.
2. Does the player view emit color?

## Expected output

A report addressed to `studio` (set `to: studio`), containing:

- An overall verdict: `pass`, `fail` or `question`, with the reason.
- The `run_tests` totals, with `ManualTest` reported separately and its method named (test run or static check).
- A table for the criteria in B (and AC-15, AC-17 if now judgeable), each marked observed or suite.
- The "Captures" section from C and the answer on color.
- For any failure: a defect report with reproduction steps and the failing criterion.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, manual.md, repo/ (build), repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/26-qa-to-studio.md
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

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `manual.md` — controls and the play script format (player-facing).
>>>END

<<<FILE design/combat.md
# Combat design (build 0.5 target — Option A, G-001)

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text.

## Experience intent

Every enemy does something the player can read, answer and profit from. A grub is a threat with a beat: it approaches, winds up, strikes, then is open to a counter. A spitter is a threat on a rhythm that the player can dodge or break by walking up and hitting it. The player's attack visibly changes the enemy. Fights are decided by spacing and timing with attack and dash only (D-001, pillars 1 and 3).

## Conventions

- All timings are in seconds and must hold at 30 and 60 FPS (section "30 / 60 FPS").
- Distances are in tiles. The room is 16×9 (x 0–15, y 0–8).
- "Telegraph" means a change the player can see in the player view, at least one on-map change plus one text line. Threat colors are saturated orange/red.
- Values marked **[tune]** are starting values the designer expects to adjust after a live playtest of the Option A build.

## Player kit

- **Attack** (one button): a swipe in the facing direction.
  - Damage 1. Recovery 0.35 s.
  - Reach 1.5 tiles, in a 90° cone centred on the facing direction.
  - It hits every enemy inside the cone. Hitting two enemies with one swipe is intended and rewards positioning.
  - Rulings in "Attack feedback" below.
- **Dash**: 4 tiles over 0.25 s, invulnerable for the full dash. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends. The dash passes through enemies and projectiles without harm.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- **Hearts**: 3 maximum.
- **Moving while attacking**: allowed. Movement continues during the 0.35 s recovery. (Not yet observed; this is the spec rule, to be verified.)

## Enemies

### Grub (HP 2)

States: **Approach → Wind-up → Strike → Recovery → Approach**.

| State | Duration | Rules |
|---|---|---|
| Approach | until in range | Walks at the player at 2.0 tiles/s (as observed). Harmless. |
| Wind-up | 0.5 s **[tune]** | Starts when the grub is within 1.25 tiles of the player. The grub stops, and its glyph and color change (see "Feedback"). A text line "a grub rears back" prints. It deals no damage. |
| Strike | 0.15 s | A short lunge of up to 1 tile toward where the player stood when the wind-up ended. It damages the player once (1 heart) if the player is within 1.0 tile of the grub at any moment of the strike and is not invulnerable. |
| Recovery | 0.9 s **[tune]** | The grub stands still, "open". No damage. Its normal glyph returns. |

- Cycle with a player standing still: 0.5 + 0.15 + 0.9 = about 1.55 s per bite (was about 0.8 s).
- **Attack limit:** at most 2 grubs may be in Wind-up or Strike at the same time. A third grub that reaches range keeps approaching/circling at 2.0 tiles/s until a slot frees. This keeps big groups readable.
- **Player hits on a grub:**
  - First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s and shows the damaged state.
  - A hit during Wind-up cancels the wind-up. The grub goes straight into a 0.6 s Recovery and does not strike.
  - Second hit: the grub is defeated.
- Grubs never damage the player outside Strike, so the dash and spacing are the answers: step back, or dash through the wind-up, then counter in Recovery.

### Spitter (HP 2)

States: **Idle → Charge → Fire → Recovery → Idle**.

| State | Duration | Rules |
|---|---|---|
| Idle | until its next volley time | Stationary. Harmless. |
| Charge | 0.8 s **[tune]** | A visible charge-up: glyph and color change, and a text line "spitter (top right) charges". The aim point is locked when the charge ends. |
| Fire | instant | Fires one projectile toward the locked aim point: the player's position at the end of the charge. |
| Recovery | 0.6 s | Stationary, harmless, normal glyph. |

- **Volley interval:** one volley (Charge start to next Charge start) every 2.5 s **[tune]**.
- **Staggering:** spitters never fire together. In a room, spitter k (k = 0, 1, 2 in spawn-list order) starts its first Charge at 1.0 + 0.8·k s after the room starts, then repeats every 2.5 s.
- **Projectile:** speed 3.0 tiles/s **[tune]**; flies in a straight line to the locked aim point and continues until it leaves the room or hits the player. It damages the player for 1 heart on contact (unless invulnerable or dashing). It is saturated orange/red and visible for the whole flight.
- **Dodge:** because the aim point is fixed at the end of the charge, moving off the locked line, or dashing through it, avoids the projectile. A dash through a projectile is safe.
- **Approachable (ruling):** yes. Spitters stay stationary (moving spitters belong to deferred Option B), but a player can walk up and swipe at one at any time. A hit during Charge cancels the charge and staggers the spitter for 1.0 s, after which its next Charge starts. A hit in any state shows the damaged state. The second hit defeats it.
- Spitters have no melee attack. A player standing next to one is hit only by its projectiles.

### Group behavior

- A grub is never threatened by friendly projectiles. Projectiles only affect the player.
- Enemies do not block projectiles.

## Attack feedback (applies to all enemies)

- **Swipe is always visible.** Every swipe, hit or miss, draws a short arc on the map for 0.15 s in the facing direction.
- **Damaged state.** After 1 hit an enemy shows a distinct glyph/color, and the hit line states its remaining HP: "you swipe: grub hit (1 left)". A defeat prints "grub defeated".
- **Multi-hit.** A swipe that hits two enemies prints one hit line per enemy.
- **"(nothing happens)" ruling (Q6).** It is intended that a swipe sometimes does nothing, but never silently. It must say why:
  - "(miss)": the swipe landed but no enemy was in reach.
  - "(too soon)": the 0.35 s recovery after the previous swipe has not finished.
  - "(stunned)": hit-stun, the first 0.3 s after taking a hit.
  - "(down)": the player is at zero hearts.
- The glyph and color for each state (full, wind-up/charge, damaged) is chosen in Build and documented in the manual. Wind-up and charge are saturated orange/red. The three states must be distinguishable in the player view.

## Player down, game over and room clear

### Zero hearts (Q2)

- At 0 hearts the player is **down**. The marker `x` replaces `P`.
- Immediately: all enemies stop acting (no new Wind-up, Charge or Fire), and enemy projectiles in flight are removed. A line prints: "you went down".
- Input while down does nothing, but it is never silent. An attack prints "(down)". Move and dash do nothing.
- After 2.0 s down, the screen shows "run over — rooms cleared: N" and the run ends.
- A new run starts at room 1 with 3 hearts when the attack button is pressed after the run-over screen is shown. (Pause remains available.) A scripted session ends at the run-over screen.
- This rule changes no input and does not change run length (15–20 min). See D-003.

### Room cleared (Q3)

- A room is cleared when its last enemy is defeated. The check runs after the player's attacks and before enemy damage in each tick, so a swipe that defeats the last enemy cancels any strike or projectile hit due on that tick.
- On clear, all projectiles are removed, "room cleared" prints, and the player is healed 1 heart (not above 3) **[tune]**.
- Hearts otherwise carry over between rooms.
- Input stays active for 1.5 s (the player can walk and swipe; nothing can hurt them), then the next room loads with the player at the start position x 8, y 4. Clearing room 5 prints "run complete" and ends the run like the run-over screen.
- **Cleared while down:** impossible. Once the player is down, enemies stop acting and the room cannot clear (see tick order above); down takes priority.
- Rooms do not restart in place. A clear is never undone.

### Practice room (Q4)

- `room empty` starts with no enemies and is not part of a run. `spawn` and `player` lines place things.
- "Room cleared" prints when the last spawned enemy is defeated. There is no heal and no room transition; the session continues to its `end` time.
- If the player goes down, the same down rules apply except that the session ends after the 2.0 s instead of showing a run-over screen.
- The `x` marker and the practice room must be listed in `manual.md#on-screen` (change requested, see handoff 10).

## Rooms (Q1)

- 5 rooms, 3–6 enemies each. **Mixed Grubs and Spitters applies across the set of rooms, not per room.**
- Layouts (unchanged from build 0.4): room 1 = 3 grubs; room 2 = 4 grubs; room 3 = 3 spitters; room 4 = 2 grubs + 2 spitters; room 5 = 3 grubs + 2 spitters.
- Per-room mixing, moving spitters and staggered grub arrival are Option B and stay deferred (D-002).
- A room ends when all enemies are defeated.

## Edge cases

- **Simultaneous hits on the player (grub strike and projectile in the same tick):** one heart is lost, and the 0.8 s invulnerability covers the other.
- **Player hit during an attack's recovery:** the recovery continues after the stun; the swipe shows "(stunned)" if pressed during stun.
- **Dash during stun:** ignored with "(stunned)".
- **Enemy defeated mid-state:** it stops acting at once. A defeated grub does not strike.
- **Two grubs wanting the same slot:** the nearer grub takes the free attack slot.
- **Player dashes through a grub in Wind-up:** the grub still completes its Wind-up, Strike (at the old spot or toward the player's current position, as built) and Recovery; its strike misses if the player is more than 1.0 tile away.
- **Spitter Charge canceled by a hit:** the projectile is not fired.
- **Pause:** all timers freeze.

## 30 / 60 FPS (Q5)

- Every timer above runs on elapsed seconds, not frame counts.
- Tolerance: an event's trace timestamp may differ from its spec time by at most 0.04 s at 30 FPS and 0.02 s at 60 FPS.
- The Strike damage window (0.15 s) must cover at least 4 frames at 30 FPS.
- Dash distance (4 tiles) may differ between 30 and 60 FPS by at most 0.25 tiles.
- Running the same script at `fps 30` and `fps 60` gives the same sequence of events, with timestamps within 0.07 s of each other.

## Acceptance criteria

### Verification (QA; trace view and player view; each at `fps 30` and `fps 60`)

- **AC-1 Grub telegraph:** in the practice room, a grub starting at distance 4 on an idle player produces "a grub rears back" and a changed glyph at least 0.45 s before the first heart is lost. No heart is lost during Approach or Recovery.
- **AC-2 Grub timing:** wind-up 0.5 s, strike 0.15 s, recovery 0.9 s, each within tolerance.
- **AC-3 Grub dodge:** a player who dashes away at any time in the wind-up loses no heart on that strike.
- **AC-4 Grub counter:** a swipe during Recovery hits and the grub shows a damaged state; the next bite then arrives no sooner than 1.5 s after the previous one for a still player.
- **AC-5 Interrupt:** a swipe that hits a winding-up grub cancels its strike (no heart lost) and puts it in a 0.6 s Recovery.
- **AC-6 Attack limit:** in room 5, no more than 2 grubs are in Wind-up/Strike at any time (from the trace).
- **AC-7 Spitter stagger:** in rooms 4 and 5, the two spitters never start a Charge or fire in the same 0.5 s. The first Charge starts at 1.0 s and 1.8 s, and each spitter repeats every 2.5 s.
- **AC-8 Spitter telegraph:** "spitter (position) charges" and a changed glyph appear 0.8 s before each shot. The spit line names its spitter; there are no identical duplicate lines at one timestamp.
- **AC-9 Projectile dodge:** a player who has moved at least 1 tile off the locked line (or dashes through it) before the projectile arrives takes no damage. A player who stays still on that line is hit for 1 heart.
- **AC-10 Spitter approach:** a player can walk to a spitter in room 3 and defeat it with 2 swipes, and a hit during Charge cancels that shot.
- **AC-11 Hit feedback:** each swipe prints exactly one outcome per enemy hit ("hit (1 left)", "defeated") or one reason ("miss", "too soon", "stunned", "down"). "(nothing happens)" never appears without a reason. A damaged enemy has a distinct glyph/color from a full-HP one.
- **AC-12 Multi-hit:** one swipe with two grubs inside the cone prints two hit lines.
- **AC-13 Zero hearts:** after the third hit, "you went down" prints, `x` replaces `P`, enemies stop, projectiles vanish, and attack prints "(down)". After 2.0 s the run-over screen shows. Pressing attack there starts room 1 with 3 hearts.
- **AC-14 Room clear:** "room cleared" prints on the last defeat, projectiles vanish, hearts +1 (max 3), and the next room loads after 1.5 s. A clearing swipe at the same tick as a would-be strike results in no damage. Clearing room 5 prints "run complete".
- **AC-15 Practice room:** `room empty` works as described and `x` and the practice room are in the manual.
- **AC-16 Room mix:** the trace setup rows match the layouts above.
- **AC-17 Frame rate:** AC-1…AC-14 pass at both frame rates, and the 30/60 comparison above holds.

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A playtester can say, unprompted, what a grub is about to do before it bites, and describes a reason to move or dash.
- A playtester reacts to a projectile at least once (moves, dashes or approaches a spitter) and can tell the two spitters apart.
- Rooms 4 and 5 are described as different from each other and from rooms 1–3 by what the player does, not only by enemy count.
- The playtester can tell from the screen how many hits an enemy needs.
- Grubs are neither trivial nor unfair: the playtester takes some damage in rooms 4–5 but can explain how it happened. (If grubs read as trivial, or the dash seems unnecessary, retune within D-001.)

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director.
- Whether the run has any progression after "run over" is outside this spec.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE manual.md
# Lantern Depths — how to play build 0.5

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears. The room is drawn every half second, and also at the moment of every swipe,
hit, wind-up, charge, shot and other key event.

## Controls

- **Move** in four directions; you keep moving until you stop or turn. You can move while you swipe.
- **Attack**: a short swipe in the direction you face. It reaches a little more than one tile in a
  wide cone and hits every enemy inside it. After a swipe you must wait a moment before the next.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing, and
  you can dash through enemies and shots. It needs a moment to recharge.

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
| `spawn grub\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

Hearts are shown above the room. Capital letters mean danger now; small letters mean harmless.

| Mark | Meaning |
|---|---|
| `P` | you |
| `x` | you, down (out of hearts) |
| `g` | grub, harmless right now (walking, or open to a counter) |
| `G` | grub about to bite or biting. Dash or step away. |
| `w` | grub that has been hit once, harmless right now |
| `W` | grub that has been hit once, about to bite or biting |
| `s` | spitter, harmless right now |
| `S` | spitter charging a shot. The shot goes where you stand when the charge ends. |
| `z` | spitter that has been hit once, harmless right now |
| `Z` | spitter that has been hit once, charging a shot |
| `*` | spit shot in flight |
| `)` `(` `^` `v` | your swipe, drawn on the tiles it reaches (right, left, up, down) |

With color on, committed enemies and shots are orange or red, harmless enemies are muted, and you and
your swipe are lantern yellow. The letters carry the meaning without color.

## What you hear and read

- "a grub rears back (left)": that grub is about to bite. Step away or dash.
- "the grub is open": the grub has finished biting; strike now.
- "spitter (top right) charges": that spitter is aiming. Leave the line or dash through it.
- "spitter (top right) spits" / "is staggered": it fired / you hit it mid-charge and it lost its shot.
- "you swipe: grub hit (1 left)", "grub defeated": your swipe result, one line per enemy hit.
- A swipe that does nothing says why: "(miss)" nothing in reach, "(too soon)" you are still
  recovering from the last swipe, "(stunned)" you were just hit, "(down)" you are out of hearts.
- A dash on cooldown says "(dash not ready)".

## Rooms and runs

- Hearts carry from room to room. Clearing a room ("room cleared") heals one heart, up to three.
  You can move and swipe for a moment, then the next room begins.
- Clearing room 5 ends the run with "run complete".
- At zero hearts you are down: enemies stop and shots vanish. A moment later the screen reads "run
  over — rooms cleared: N" and "press attack to start again". Attack starts a new run from room 1
  with full hearts.
- The practice room (`room empty`) is not a run: nothing heals, there is no next room, and the
  session ends a moment after you go down.
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py [--color] --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format is described in the project's manual.md. Color is only added with --color or
when the output is a terminal; the glyphs carry every state without it.
"""

import argparse
import sys

from game import ATTACK_REACH, HEARTS, ROOM_H, ROOM_W, Game

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots

RESET = "\033[0m"
LANTERN = "\033[38;5;229m"  # warm yellow-white: player and swipe arc
GRAY_BLUE = "\033[38;5;67m"  # downed player
MUTED = "\033[38;5;245m"  # harmless enemy
MUTED_TINT = "\033[38;5;137m"  # harmless, damaged enemy
ALERT = "\033[1;38;5;202m"  # saturated orange/red: telegraphed enemies
SHOT = "\033[1;38;5;196m"  # projectile

# One cell per tile: (character, color). Uppercase = committed to hurting; lowercase = harmless.
GLYPHS = {
    "player": ("P", LANTERN),
    "down": ("x", GRAY_BLUE),
    "shot": ("*", SHOT),
    "arc_right": (")", LANTERN),
    "arc_left": ("(", LANTERN),
    "arc_up": ("^", LANTERN),
    "arc_down": ("v", LANTERN),
    "grub": ("g", MUTED),
    "grub_alert": ("G", ALERT),
    "grub_hurt": ("w", MUTED_TINT),
    "grub_hurt_alert": ("W", ALERT),
    "spitter": ("s", MUTED),
    "spitter_alert": ("S", ALERT),
    "spitter_hurt": ("z", MUTED_TINT),
    "spitter_hurt_alert": ("Z", ALERT),
}
ARC_KEYS = {(1, 0): "arc_right", (-1, 0): "arc_left", (0, -1): "arc_up", (0, 1): "arc_down"}

# Every player-visible line.
LINES = {
    "windup": "a grub rears back ({side})",
    "recover": "the grub is open ({side})",
    "charge": "spitter{num} ({spot}) charges",
    "spit": "spitter{num} ({spot}) spits",
    "stagger": "spitter{num} ({spot}) is staggered",
    "hit": "you swipe: {kind} hit ({left} left)",
    "defeated": "{kind} defeated",
    "miss": "you swipe: (miss)",
    "ignored_attack": "you swipe: ({reason})",
    "ignored_dash": "you dash: ({reason})",
    "ignored_other": "you cannot move: ({reason})",
    "dash": "you dash {direction}",
    "hurt": "YOU ARE HIT by a {source} — hearts {hearts}/{max}",
    "down": "you went down",
    "cleared": "room cleared",
    "heal": "you catch your breath — hearts {hearts}/{max}",
    "run_complete": "run complete",
    "room_loaded": "room {room} begins",
    "run_start": "a new run begins",
    "run_over": "run over — rooms cleared: {rooms}",
    "run_over_complete": "run complete — rooms cleared: {rooms}",
    "restart": "press attack to start again",
}

# Events that get their own draw of the room at the moment they happen.
SNAPSHOT_EVENTS = {
    "hurt", "attack", "windup", "charge", "spit", "recover", "down",
    "cleared", "room_loaded", "run_start",
}


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "room":
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
        except (IndexError, ValueError):
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}")
    return setup, sorted(inputs, key=lambda i: i[0])


def play(setup, inputs, view, color=False):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    end = setup["end"] if setup["end"] is not None else (inputs[-1][0] + 3 if inputs else 5)
    end = min(end, MAX_SECONDS)
    out = Player(game, color) if view == "player" else Trace(game)
    out.start()
    pending = list(inputs)
    while game.t < end - 1e-9:
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        game.step()
        out.frame()
        if game.finished or (game.phase == "over" and not pending):
            break
    out.finish()


def describe(kind, d):
    """The lines a player sees for one event (a list; empty when the event is silent)."""
    if kind == "attack":
        lines = []
        for enemy, result, left, _ in d["hits"]:
            if result == "hit":
                lines.append(LINES["hit"].format(kind=enemy, left=left))
            else:
                lines.append(LINES["defeated"].format(kind=enemy))
        return lines or [LINES["miss"]]
    if kind == "ignored":
        key = {"attack": "ignored_attack", "dash": "ignored_dash"}.get(
            d["action"], "ignored_other"
        )
        return [LINES[key].format(reason=d["reason"])]
    if kind == "dash":
        return [LINES["dash"].format(direction=d["direction"])]
    if kind == "hurt":
        return [LINES["hurt"].format(source=d["source"], hearts=d["hearts"], max=HEARTS)]
    if kind == "windup" or kind == "recover":
        return [LINES[kind].format(side=d["side"])]
    if kind in ("charge", "spit", "stagger"):
        num = f" {d['n']}" if d["dup"] else ""
        return [LINES[kind].format(num=num, spot=d["spot"])]
    if kind == "heal":
        return [LINES["heal"].format(hearts=d["hearts"], max=HEARTS)] if d["gained"] else []
    if kind == "room_loaded":
        return [LINES["room_loaded"].format(room=d["room"])]
    if kind == "run_over":
        key = "run_over_complete" if d["complete"] else "run_over"
        return [LINES[key].format(rooms=d["rooms"]), LINES["restart"]]
    if kind in ("down", "cleared", "run_complete", "run_start"):
        return [LINES[kind]]
    return []


def arc_tiles(game):
    fx, fy = game.arc_dir
    tiles = []
    for row in range(ROOM_H):
        for col in range(ROOM_W):
            dx, dy = col - game.x, row - game.y
            along = dx * fx + dy * fy
            across = dx * fy - dy * fx
            if along > 0 and abs(across) <= along and (dx * dx + dy * dy) ** 0.5 <= ATTACK_REACH:
                tiles.append((col, row))
    return tiles


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game, color=False):
        self.game, self.color = game, color
        self.seen, self.next_snapshot = 0, 0.0

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.5 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, snap = self.game, False
        for when, kind, details in g.events[self.seen :]:
            for text in describe(kind, details):
                print(f"{when:7.3f}  {text}")
            snap = snap or kind in SNAPSHOT_EVENTS
        self.seen = len(g.events)
        due = g.t >= self.next_snapshot - 1e-9
        if g.phase != "over" and (snap or due):
            self.snapshot()
        if due:
            self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    def paint(self, key):
        char, color = GLYPHS[key]
        return f"{color}{char}{RESET}" if self.color else char

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(x, y, key):
            col, row = int(round(x)), int(round(y))
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = self.paint(key)

        if g.arc_left > 0:
            for col, row in arc_tiles(g):
                put(col, row, ARC_KEYS[g.arc_dir])
        for shot in g.shots:
            put(shot[0], shot[1], "shot")
        for enemy in g.enemies:
            if enemy.alive:
                key = enemy.kind
                if enemy.hp < enemy.max_hp:
                    key += "_hurt"
                if enemy.committed:
                    key += "_alert"
                put(enemy.x, enemy.y, key)
        put(g.x, g.y, "player" if g.hearts > 0 else "down")
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in grid:
            print("   |" + "".join(row) + "|")
        print("   +" + "-" * ROOM_W + "+")


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

    def remaining(self, e):
        g = self.game
        if e.kind == "grub":
            return e.timer if e.state in ("windup", "strike", "recovery") else 0.0
        if e.state in ("charge", "recovery"):
            return max(0.0, e.until - g.t)
        return max(0.0, e.next_charge - g.t) if e.next_charge != float("inf") else 0.0

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} room={g.room} phase={g.phase} "
            f"pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f} shots={len(g.shots)}"
        )
        enemies = " ".join(
            f"{e.kind}#{e.index}({e.x:.2f},{e.y:.2f},hp={e.hp},{e.state},{self.remaining(e):.3f})"
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
    parser.add_argument("--color", action="store_true")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs = read_script(f.read())
    play(setup, inputs, args.view, color=args.color or sys.stdout.isatty())


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/tests/test_game.py
import contextlib
import io
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
import play  # noqa: E402
from game import DASH_DISTANCE, HEARTS, ROOMS, START, Game  # noqa: E402

FPS = (30, 60)
REPO = Path(__file__).resolve().parent.parent
MANUAL = REPO.parent / "manual.md"


def tol(fps):
    return 0.04 if fps == 30 else 0.02


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def run_to(game, t):
    while game.t < t - 1e-9:
        game.step()


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def run_until(game, kind, limit=10.0):
    count = len(times(game, kind))
    while game.t < limit:
        game.step()
        if len(times(game, kind)) > count:
            return
    raise AssertionError(f"no {kind} event within {limit} s")


def capture(script, view="player"):
    setup, inputs = play.read_script(script)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        play.play(setup, inputs, view)
    return buf.getvalue()


def timed_lines(text):
    found = []
    for line in text.splitlines():
        m = re.match(r"\s*(\d+\.\d+)  (.+)$", line)
        if m:
            found.append((float(m.group(1)), m.group(2)))
    return found


def drive(game, out, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()
        out.frame()


def down(game):
    for _ in range(HEARTS):
        game.invulnerable = False
        game._hurt("test")


def grub_game(fps, gx=12.0):
    game = Game(fps=fps, room="empty")
    game.place_player(8, 4)
    game.spawn("grub", gx, 4)
    return game


class GrubTest(unittest.TestCase):
    def test_telegraph_and_timing(self):  # AC-1, AC-2, AC-4 (cycle)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = grub_game(fps)
                run(game, 4.0)
                d = tol(fps)
                w, s, r = times(game, "windup")[0], times(game, "strike")[0], times(game, "recover")[0]
                self.assertAlmostEqual(s - w, 0.5, delta=d)
                self.assertAlmostEqual(r - s, 0.15, delta=d)
                self.assertAlmostEqual(times(game, "windup")[1] - r, 0.9, delta=d)
                hurts = times(game, "hurt")
                self.assertGreaterEqual(hurts[0] - w, 0.45)
                self.assertTrue(s - 1e-9 <= hurts[0] <= r + 1.0 / fps)
                self.assertGreaterEqual(hurts[1] - hurts[0], 1.5 - d)

    def test_dash_away_during_windup_avoids_the_strike(self):  # AC-3
        for fps in FPS:
            for offset in (0.0, 0.25, 0.45):
                with self.subTest(fps=fps, offset=offset):
                    game = grub_game(fps)
                    run_until(game, "windup")
                    run(game, offset)
                    game.press("dash", "left")
                    run(game, 1.0)
                    self.assertEqual(game.hearts, HEARTS)

    def test_swipe_in_recovery_hits_and_next_bite_is_late(self):  # AC-4
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "recover")
                run(game, 0.2)
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, 1)
                run(game, 3.0)
                hurts = times(game, "hurt")
                self.assertGreaterEqual(hurts[1] - hurts[0], 1.5 - tol(fps))

    def test_swipe_interrupts_windup(self):  # AC-5
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "windup")
                run(game, 0.2)
                game.press("attack")
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                self.assertEqual(grub.state, "recovery")
                self.assertAlmostEqual(grub.timer, 0.6, delta=0.01)
                self.assertTrue(
                    any(d.get("cause") == "interrupted" for _, k, d in game.events if k == "recover")
                )
                self.assertTrue(times(game, "knockback"))
                run(game, 0.9)
                self.assertEqual(game.hearts, HEARTS)

    def test_at_most_two_grubs_attack_at_once(self):  # AC-6
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                for x, y in ((9.2, 4), (6.8, 4), (8, 5.2), (8, 2.8), (9.0, 4.9)):
                    game.spawn("grub", x, y)
                peak = 0
                for _ in range(round(8 * fps)):
                    game.step()
                    busy = sum(1 for e in game.enemies if e.alive and e.state in ("windup", "strike"))
                    peak = max(peak, busy)
                    self.assertLessEqual(busy, 2)
                self.assertEqual(peak, 2)

    def test_strike_covers_at_least_four_frames_at_30_fps(self):
        for offset in (0.0, 0.01, 0.02, 0.03, 0.04):
            with self.subTest(offset=offset):
                game = grub_game(30, 12.0 + offset)
                calls = [0]
                original = game._lunge

                def counting(enemy, use):
                    if use > 1e-6:
                        calls[0] += 1
                    return original(enemy, use)

                game._lunge = counting
                run(game, 2.3)
                self.assertGreaterEqual(calls[0], 4)


class SpitterTest(unittest.TestCase):
    def room_spitters(self, room, fps):
        game = Game(fps=fps, room="empty")
        game.place_player(8, 4)
        for kind, x, y in ROOMS[room]:
            if kind == "spitter":
                game.spawn(kind, x, y)
        return game

    def test_volleys_are_staggered_and_regular(self):  # AC-7
        for room in "345":
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    game = self.room_spitters(room, fps)
                    run(game, 4.9)
                    d = tol(fps)
                    charges = [(t, k["who"]) for t, kind, k in game.events if kind == "charge"]
                    for who in {w for _, w in charges}:
                        mine = [t for t, w in charges if w == who]
                        self.assertAlmostEqual(mine[0], 1.0 + 0.8 * who, delta=d)
                        for a, b in zip(mine, mine[1:]):
                            self.assertAlmostEqual(b - a, 2.5, delta=d)
                    starts = sorted(t for t, _ in charges)
                    fires = sorted(times(game, "spit"))
                    for seq in (starts, fires):
                        self.assertTrue(all(b - a >= 0.5 for a, b in zip(seq, seq[1:])))
                    for t, kind, k in game.events:
                        if kind == "spit":
                            start = [c for c, w in charges if w == k["who"] and abs(c + 0.8 - t) < 1e-6]
                            self.assertTrue(start)

    def test_charge_lines_and_spit_lines_name_the_spitter(self):  # AC-8
        for room, end in (("3", 3.8), ("4", 3.0), ("5", 3.0)):
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    text = capture(f"room {room}\nfps {fps}\nend {end}\n")
                    lines = timed_lines(text)
                    for stamp, count in Counter(lines).items():
                        self.assertEqual(count, 1, stamp)
                    spits = [(t, s) for t, s in lines if "spits" in s]
                    charges = [(t, s) for t, s in lines if "charges" in s]
                    self.assertTrue(spits)
                    game = Game(fps=fps, room=room)
                    run(game, end)
                    self.assertEqual(len(spits), len(times(game, "spit")))
                    for t, s in spits:
                        label = s.replace("spits", "charges")
                        self.assertTrue(
                            any(label == c and abs(t - 0.8 - ct) < 0.01 for ct, c in charges), s
                        )

    def test_two_spitters_in_one_spot_get_numbers(self):
        text = capture(
            "room empty\nfps 60\nspawn spitter 15 0\nspawn spitter 14 0\nplayer 8 4\nend 3\n"
        )
        lines = timed_lines(text)
        self.assertIn("spitter 1 (top right) spits", [s for _, s in lines])
        for stamp, count in Counter(lines).items():
            self.assertEqual(count, 1, stamp)

    def test_projectile_dodge(self):  # AC-9
        def spit_game(fps):
            game = Game(fps=fps, room="empty")
            game.place_player(8, 4)
            game.spawn("spitter", 13, 4)
            return game

        for fps in FPS:
            with self.subTest(fps=fps, case="still"):
                game = spit_game(fps)
                run_to(game, 5.0)
                self.assertEqual(game.hearts, HEARTS - 1)
            with self.subTest(fps=fps, case="sidestep"):
                game = spit_game(fps)
                run_to(game, 2.0)
                game.press("move", "up")
                run_to(game, 2.5)
                game.press("stop")
                run_to(game, 5.0)
                self.assertEqual(game.hearts, HEARTS)
            with self.subTest(fps=fps, case="dash through"):
                game = spit_game(fps)
                run_to(game, 3.1)
                game.press("dash", "right")
                run_to(game, 4.0)
                self.assertEqual(game.hearts, HEARTS)

    def test_walk_up_and_defeat_a_spitter(self):  # AC-10
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("spitter", 9.2, 4)
                game.press("attack")
                run(game, 0.4)
                game.press("attack")
                run(game, 0.1)
                self.assertTrue(game.cleared)
                run(game, 5.0)
                self.assertFalse(times(game, "spit"))

    def test_hit_during_charge_cancels_the_shot(self):  # AC-10
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("spitter", 9.2, 4)
                run_to(game, 1.2)
                game.press("attack")
                self.assertEqual(game.enemies[0].state, "stagger")
                run_to(game, 2.9)
                self.assertFalse(times(game, "spit"))
                self.assertAlmostEqual(times(game, "charge")[1], 2.2, delta=tol(fps))


class FeedbackTest(unittest.TestCase):
    def test_every_swipe_outcome_has_a_line(self):  # AC-11
        text = capture("room empty\nfps 60\nplayer 8 4\n0 attack\n0.1 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: (miss)", lines)
        self.assertIn("you swipe: (too soon)", lines)
        text = capture("room empty\nfps 60\nspawn grub 9.2 4\nplayer 8 4\n0 attack\n0.5 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: grub hit (1 left)", lines)

    def test_reasons_stunned_and_down(self):  # AC-11
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run_until(game, "hurt")
        game.press("attack")
        self.assertEqual(game.events[-1][2]["reason"], "stunned")
        game = Game(room="1")
        down(game)
        game.press("attack")
        self.assertEqual(game.events[-1][2]["reason"], "down")

    def test_no_bare_nothing_happens(self):
        self.assertNotIn("nothing happens", (REPO / "play.py").read_text(encoding="utf-8"))

    def test_damaged_glyph_differs_from_full(self):  # V-1, V-4
        for kind in ("grub", "spitter"):
            chars = {play.GLYPHS[k][0] for k in (kind, kind + "_alert", kind + "_hurt", kind + "_hurt_alert")}
            self.assertEqual(len(chars), 4)
        self.assertEqual(play.GLYPHS["grub"][0], "g")
        self.assertEqual(play.GLYPHS["grub_alert"][0], "G")

    def test_grub_glyph_telegraph_before_first_hit(self):  # AC-1, V-3
        for fps in FPS:
            text = capture(f"room empty\nfps {fps}\nspawn grub 12 4\nplayer 8 4\nend 3\n")
            rows = text.splitlines()
            first_hit = next(i for i, r in enumerate(rows) if "YOU ARE HIT" in r)
            before = rows[:first_hit]
            self.assertTrue(any("a grub rears back (right)" in r for r in before))
            self.assertTrue(any(re.match(r"\s+\|.*G.*\|$", r) for r in before))

    def test_swipe_has_its_own_draw_with_arc(self):  # V-2
        for fps in FPS:
            text = capture(f"room empty\nfps {fps}\nplayer 8 4\n0.2 attack\nend 0.4\n")
            self.assertIn(")", "".join(r for r in text.splitlines() if r.startswith("   |")))

    def test_multi_hit(self):  # AC-12
        text = capture(
            "room empty\nfps 60\nspawn grub 9.2 4\nspawn grub 9 3.2\nplayer 8 4\n0 attack\nend 1\n"
        )
        lines = [s for _, s in timed_lines(text)]
        self.assertEqual(lines.count("you swipe: grub hit (1 left)"), 2)

    def test_moving_during_swipe_recovery(self):
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("attack")
        game.press("move", "right")
        run(game, 0.2)
        self.assertGreater(game.x, 8.5)


class RunFlowTest(unittest.TestCase):
    def test_zero_hearts(self):  # AC-13
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="1")
                game.shots.append([5.0, 5.0, 1.0, 0.0])
                down(game)
                self.assertEqual(game.hearts, 0)
                self.assertEqual(game.shots, [])
                self.assertTrue(all(not e.committed for e in game.enemies))
                self.assertTrue(times(game, "down"))
                game.press("attack")
                self.assertEqual(game.events[-1][2]["reason"], "down")
                run(game, 1.9)
                self.assertEqual(game.phase, "down")
                run(game, 0.2)
                self.assertEqual(game.phase, "over")
                self.assertTrue(times(game, "run_over"))
                game.press("attack")
                self.assertEqual((game.hearts, game.room, game.phase), (HEARTS, "1", "playing"))

    def test_down_screen_in_the_player_view(self):  # AC-13, V-8
        game = Game(room="1")
        out = play.Player(game)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out.start()
            down(game)
            drive(game, out, 2.2)
        text = buf.getvalue()
        self.assertIn("you went down", text)
        self.assertRegex(text, r"\|.*x.*\|")
        self.assertIn("run over — rooms cleared: 0", text)
        self.assertIn("press attack to start again", text)

    def test_practice_room_session_ends_after_down(self):
        game = Game(room="empty")
        down(game)
        run(game, 2.1)
        self.assertTrue(game.finished)

    def test_room_clear(self):  # AC-14
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="1")
                for e in game.enemies[1:]:
                    e.hp, e.state = 0, "dead"
                last = game.enemies[0]
                last.hp, last.x, last.y = 1, 9.0, 4.0
                game.hearts = 2
                game.shots.append([8.0, 4.0, 0.0, 0.0])
                game.press("attack")
                game.step()
                self.assertTrue(game.cleared)
                self.assertEqual(game.hearts, HEARTS)
                self.assertEqual(game.shots, [])
                self.assertFalse(times(game, "hurt"))
                run(game, 1.45)
                self.assertEqual(game.room, "1")
                run(game, 0.1)
                self.assertEqual(game.room, "2")
                self.assertEqual(len(game.enemies), 4)
                self.assertEqual((game.x, game.y), START)

    def test_clearing_room_5_completes_the_run(self):  # AC-14
        game = Game(room="5")
        for e in game.enemies[1:]:
            e.hp, e.state = 0, "dead"
        last = game.enemies[0]
        last.hp, last.x, last.y = 1, 9.0, 4.0
        game.press("attack")
        game.step()
        self.assertTrue(times(game, "run_complete"))
        run(game, 1.6)
        self.assertEqual(game.phase, "over")
        self.assertTrue(game.events[-1][2]["complete"])

    def test_layouts(self):  # AC-16
        expected = {"1": (3, 0), "2": (4, 0), "3": (0, 3), "4": (2, 2), "5": (3, 2)}
        for room, (grubs, spitters) in expected.items():
            row = capture(f"room {room}\nend 0.1\n", view="trace").splitlines()[1]
            found = re.findall(r"(grub|spitter)#", row)
            self.assertEqual((found.count("grub"), found.count("spitter")), (grubs, spitters))


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in FPS:
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
        self.assertEqual(game.events[-1][2]["reason"], "dash not ready")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(4, 4)
                game.spawn("grub", 4.5, 4)
                run_until(game, "hurt")
                hit = times(game, "hurt")[0]
                run(game, 0.32)  # the hit-stun (0.3 s) has passed
                game.press("dash", "right")
                self.assertTrue(times(game, "dash"))
                run(game, 0.3)
                self.assertTrue(times(game, "dash_end"))
                self.assertTrue(game.invulnerable)
                run_to(game, hit + 0.95)
                self.assertFalse(game.invulnerable)
                hurts = times(game, "hurt")
                self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurts, hurts[1:])))


class FrameRateTest(unittest.TestCase):
    def session(self, fps):
        game = Game(fps=fps, room="empty")
        game.spawn("grub", 12, 4)
        game.spawn("spitter", 15, 0)
        game.place_player(8, 4)
        pending = [
            (2.3, "attack", None),
            (2.6, "move", "down"),
            (2.9, "stop", None),
            (3.3, "dash", "left"),
        ]
        while game.t < 6.0 - 1e-9:
            while pending and pending[0][0] <= game.t + 1e-9:
                _, action, direction = pending.pop(0)
                game.press(action, direction)
            game.step()
        return game

    def test_same_events_within_0_07_s(self):  # AC-17
        a, b = self.session(30), self.session(60)
        kinds = {k for _, k, _ in a.events} | {k for _, k, _ in b.events}
        for kind in kinds:
            ta, tb = times(a, kind), times(b, kind)
            self.assertEqual(len(ta), len(tb), kind)
            for x, y in zip(ta, tb):
                self.assertLessEqual(abs(x - y), 0.07, (kind, x, y))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_room_5_runs_at_both_frame_rates(self):
        for fps in FPS:
            result = bots.play_room(bots.BOTS["dodger"], "5", fps, 30)
            self.assertIn("hearts_lost", result)


class ManualTest(unittest.TestCase):
    # manual.md sits next to repo/ in the project directory; it is written in the final step of the Build.
    def test_manual_lists_glyphs_and_lines(self):  # AC-15, V-5
        text = MANUAL.read_text(encoding="utf-8")
        for key, (char, _) in play.GLYPHS.items():
            self.assertIn(f"`{char}`", text, key)
        for phrase in ("room empty", "rears back", "is open", "charges", "spits",
                       "run over", "press attack to start again", "(miss)", "(too soon)",
                       "(stunned)", "(down)", "room cleared"):
            self.assertIn(phrase, text, phrase)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE decisions/D-003-run-end-and-room-rules.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-003: Room mix is across rooms; zero hearts ends the run; room clear heals one heart

## Decision

1. **Room mix:** "mixed Grubs and Spitters" applies across the set of five rooms, not to every room. Rooms 1–3 stay single-type. Per-room mixing belongs to Option B (deferred in D-002).
2. **Zero hearts:** enemies stop and projectiles vanish. After 2.0 s the run ends with a "run over" screen. Attack starts a new run at room 1. No new input is added.
3. **Room clear:** hearts carry over, +1 heart (max 3) on clear, 1.5 s of free input, then the next room. A room cannot clear while the player is down.
4. **Practice room and downed marker** are documented behavior (see `design/combat.md`).
5. The spec in `design/combat.md` is the source of truth for the timings.

## Rationale

- Rooms 1–3 are single-type by design as teaching rooms, and mixing them is Option B, which D-002 defers until Option A is playtested.
- A run-end rule is needed because the build soft-locks at zero hearts. It reuses the attack button, so D-001 holds, and it keeps runs short (pillar 2).
- Hearts carry over because 3 hearts without a heal would make the later rooms too punishing with the longer fights telegraphs allow. +1 on clear is a tuning value to review after a live playtest.

## Alternatives considered

- **Mixed enemies in every room:** rejected for now; it is Option B and would change layout before A's effect is known.
- **Restart the current room on zero hearts:** rejected; it makes death cheap in a roguelite and hides the cost of mistakes.
- **Hearts reset to 3 each room:** rejected; it removes any cost of earlier mistakes.
- **A separate restart button:** not allowed without Owner approval (D-001).

## Revisit when

- A live playtest shows runs ending too fast or too slow relative to the 15–20 minute target.
- The Director or Owner defines run progression or meta-structure.
- Option B is opened (room mix).
>>>END

<<<FILE goals/G-001-combat-monotony/26-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 26
from: qa
to: studio
stage: Verify
outcome: question
---
# 26: qa → studio — Build 0.5 verification: no failures found, but not complete (ManualTest blocked on the Owner; pause not verifiable)

## Task

Report the verification of Build 0.5 against AC-1…AC-17, with the `run_tests` totals, regressions, and items not verifiable.

## Context

Handoff 24 asked for independent verification of `repo/` against `design/combat.md`, at 30 and 60 FPS. One round of runs was used (tests, 2 traces, 1 player-view play). Two rounds remain, but the main gap needs an Owner action, so no further runs were requested.

## Findings

### Verdict: no failures found, but not a `pass`

I cannot give `pass` because two criteria are not fully judged:

- **AC-15** is unresolved because `ManualTest` has no valid result (see "Blocked").
- **AC-17** depends on the same layout fix for its "AC-1…AC-14" part, and I observed only part of it myself.

Pause (F11) is out of scope and marked not verifiable.

### run_tests totals

- Command: `python3 -m unittest discover -s tests`. Exit 1. 34 tests ran: **33 passed, 0 failed, 1 error**.
- The one error is `ManualTest.test_manual_lists_glyphs_and_lines`: `FileNotFoundError: /manual.md`.
- **The error comes from the workspace layout, not from the build.** The tests ran from `/work`, so `repo/` resolved to `/work` and the test looked for `manual.md` in `/`.
- **ManualTest result: no valid result (blocked on the Owner).** I do not mark it pass or fail.

### Blocked: manual.md placement

I cannot write `manual.md` next to `repo/` in my workspace. My allowed write paths contain only the handoff file and `@run` blocks, and none lets me write `repo/` or its parent.

- **Needed:** `manual.md` (the Owner's draft per D-005, unchanged) placed in the directory above `repo/`, then `run_tests` rerun.
- **Reading check only, not a test result:** I read `manual.md` as provided in the packet.
  - It lists the marks `P x g G w W s S z Z * ) ( ^ v`.
  - It mentions the practice room (`room empty`) and the `x` marker.
  - It includes the phrases the test requires: "rears back", "is open", "charges", "spits", "run over", "press attack to start again", "(miss)", "(too soon)", "(stunned)", "(down)", "room cleared".
  - I cannot see `play.GLYPHS`, so I cannot confirm the manual covers every glyph the build defines. That is exactly what the test checks.

### Per-criterion results

"Observed" means I read the evidence directly in the traces or player view from this run. "Suite" means a repo test that passed at both `fps 30` and `fps 60` (the tests loop over both). The suite is the implementer's side's test code, so I label it separately from my own observation.

| AC | Result | Evidence |
|---|---|---|
| AC-1 grub telegraph | pass | Observed, 30 FPS trace (`grub 12 4`, player 8 4): windup at 1.400, first heart lost at 1.967, so 0.567 s of warning (≥0.45). On the second bite, windup at 2.967 and hurt at 3.467 give 0.50 s. Hearts were lost only during Strike. Observed, player view, room 4: "a grub rears back (left)" with `G` before "YOU ARE HIT". Suite: `test_telegraph_and_timing`, `test_grub_glyph_telegraph_before_first_hit`. |
| AC-2 grub timing | pass | Observed, 30 FPS: windup→strike 0.500; strike→recover 0.167 (spec 0.15, tolerance 0.04); recover→next windup 0.900. Observed, 60 FPS room 5: strike 2.717 → recover 2.867 = 0.150. Suite: `test_telegraph_and_timing`. |
| AC-3 grub dodge | pass (suite only) | `test_dash_away_during_windup_avoids_the_strike` at offsets 0 / 0.25 / 0.45 s, both FPS. Not observed independently. |
| AC-4 grub counter | pass (suite + partial observation) | Observed: bites by a still player came 1.5 s apart (hurt 1.967 → 3.467 at 30 FPS). Suite: `test_swipe_in_recovery_hits_and_next_bite_is_late`. The "swipe in Recovery shows a damaged state" part is suite only. |
| AC-5 interrupt | pass (suite only) | `test_swipe_interrupts_windup`: HP 1, state recovery, timer 0.6, no heart lost, cause "interrupted". |
| AC-6 attack limit | pass | Observed, 60 FPS room 5: in every sampled row at most 2 grubs were in windup/strike (e.g. 3.683, 3.833, 4.000). Suite: `test_at_most_two_grubs_attack_at_once` checks every frame and reaches a peak of exactly 2. |
| AC-7 spitter stagger | pass | Observed, 60 FPS room 5: first charges at 1.000 and 1.800; repeats at 3.500 and 4.300 (2.5 s period). Spits at 1.800, 2.600, 4.300, never within 0.5 s of each other. Observed, 30 FPS room 4 player view: charges at 1.000 / 1.800 / 3.500 / 4.300. Suite: `test_volleys_are_staggered_and_regular` for rooms 3, 4, 5. |
| AC-8 spitter telegraph and spit line | pass | Observed, room 4 player view: "spitter (top right) charges" at 1.000 with `S`, and its spit at 1.800 (0.8 s later). At 1.800 two different lines print: "spitter (top right) spits" and "spitter (bottom right) charges". No identical duplicate lines at one timestamp. Suite: `test_charge_lines_and_spit_lines_name_the_spitter`, plus `test_two_spitters_in_one_spot_get_numbers` (two spitters at the same position are numbered). |
| AC-9 projectile dodge | pass (suite only) | `test_projectile_dodge` covers a still player (hit for 1 heart), a sidestep, and a dash through, both FPS. |
| AC-10 spitter approach | pass (suite only) | `test_walk_up_and_defeat_a_spitter` (2 swipes defeat it) and `test_hit_during_charge_cancels_the_shot` (no spit, next charge at 2.2 s). |
| AC-11 hit feedback | pass (suite only) | Suite: miss, too soon, hit (1 left), stunned, down; no "nothing happens" string in `play.py`; the four glyph variants differ. Observed (partial): the `g`/`G` glyphs differ in the player view. |
| AC-12 multi-hit | pass (suite only) | `test_multi_hit` gives two "grub hit (1 left)" lines from one swipe. |
| AC-13 zero hearts | pass | Observed, room 4 player view (30 FPS): "YOU ARE HIT … 0/3" and "you went down" at 5.067; `x` replaces `P`; enemies reset to harmless glyphs; shots gone. Observed, room 5 trace (60 FPS): down at 4.533, shots=0, enemies idle/approach, `run_over` at 6.533 = exactly 2.0 s. Suite: `test_zero_hearts` (attack prints "(down)", the 1.9 s / 2.1 s boundary, attack restarts room 1 with 3 hearts) and `test_down_screen_in_the_player_view`. The run-over text and the restart by attack were not seen in my own player-view run (the script ended first). |
| AC-14 room clear | pass (suite only) | `test_room_clear`: clearing swipe on the same tick as a would-be strike leaves no hurt event, hearts 2→3, shots cleared, next room at 1.5 s with 4 enemies, start position. `test_clearing_room_5_completes_the_run` covers "run complete". |
| AC-15 practice room and manual | **blocked** | Practice room behavior was exercised in all `room empty` runs and works as described, including the same down rules (suite: `test_practice_room_session_ends_after_down`). The manual content check is the blocked `ManualTest`. |
| AC-16 room mix | pass | Observed: room 5 trace setup row = 3 grubs + 2 spitters at the expected positions. Suite: `test_layouts` for rooms 1–5. |
| AC-17 frame rate | partial | Observed at both frame rates: grub timing within tolerance (30 FPS and 60 FPS traces), and spitter timestamps match the spec at both. Suite: `test_same_events_within_0_07_s` (30 vs 60 FPS event kinds and counts equal, timestamps within 0.07 s), the dash distance test, and the Strike ≥4 frames at 30 FPS test, all passing. The comparison needs a rerun once `ManualTest` has a valid result; nothing observed contradicts it. |

### Regressions checked

- Dash: covers 4 tiles at both frame rates, has a cooldown ("dash not ready"), and an attack during a dash fires when it ends. All pass.
- Invulnerability: a dash right after a hit keeps both protections; hurt events were ≥0.8 s apart (observed 0.8 s in room 4). Pass.
- Moving while attacking works (suite).
- Balance bots finish room 1, and the dodger bot runs room 5 at both frame rates (suite). Not independently exercised through `run_bots` this round.
- No regression found.

### Observations (not failures; the spec is silent)

- In the 30 FPS grub trace the grub ends up at the player's position (`side: on you`, grub at 8.00,4.00) after a few bites on a still player. The spec does not say whether enemies may overlap the player. Flagged for the game-designer, not a defect.
- With the spec's Recovery of 0.9 s and wind-up of 0.5 s, a still player is bitten every 1.5 s. The 3 hearts were lost in about 3.5 s in room 4 and about 4.5 s in room 5 with no player input. This is an experience-tuning matter for the playtest (the spec marks these values [tune]).

### Not verifiable

- **Pause (F11):** not implemented, a known scope limit. Not verifiable, not a failure.
- **Run-over screen and restart by attack in my own player-view run:** the script ended before 2.0 s after going down. Covered only by the suite.

## Decisions already made

- D-001: one attack button plus dash. No new inputs were seen in the manual or script format.
- D-002: Option A.
- D-003: room mix across rooms, zero hearts ends the run, +1 heart per room clear. Consistent with what I observed.
- D-004: one sequential change set.
- D-005: the Owner placed the draft `manual.md` unchanged.

## Constraints

- Verified at both 30 and 60 FPS as described above.
- I did not edit the build.

## Open questions

1. **Blocked on the Owner:** place `manual.md` in the directory above `repo/` (D-005) and rerun `run_tests`. Until then `ManualTest` and the AC-15 manual check have no valid result. I mark neither pass nor fail.
2. After that rerun, the studio can decide whether to route to the playtester or to request a second QA round. A second QA round would add independent scripts for the "suite only" rows (AC-3, 5, 9, 10, 11, 12, 14). No failure has been found, so there is nothing to return to `gameplay-engineer`.

## Expected output

The studio takes this report, resolves the `manual.md` placement with the Owner, and reruns `run_tests`. If `ManualTest` then passes and the studio accepts the suite-only evidence, the verdict becomes `pass` and the playtester's Handoff can be composed without implementation history. If it fails, the failure goes to `gameplay-engineer` (with the missing glyph or phrase from the test output).

Reproduction for the blocker: run `python3 -m unittest discover -s tests` in a layout without `manual.md` next to `repo/`. It yields the `FileNotFoundError` above.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: project.md, design/combat.md, manual.md
- Decisions: decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/24-studio-to-qa.md
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
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 1 (0.1 s). Output:

```text
.....................E............
======================================================================
ERROR: test_manual_lists_glyphs_and_lines (test_game.ManualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 528, in test_manual_lists_glyphs_and_lines
    text = MANUAL.read_text(encoding="utf-8")
  File "/usr/lib/python3.10/pathlib.py", line 1134, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
  File "/usr/lib/python3.10/pathlib.py", line 1119, in open
    return self._accessor.open(self, mode, buffering, encoding, errors,
FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'

----------------------------------------------------------------------
Ran 34 tests in 0.051s

FAILED (errors=1)
```

### Round 1: @run/play/idle30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn grub 12 4
end 8
```

Exit: 0 (0.0 s). Output:

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
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [1.50 s] hearts 3/3
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
   [2.00 s] hearts 2/3
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
  2.950  a grub rears back (right)
   [2.97 s] hearts 2/3
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
   [3.00 s] hearts 2/3
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
  3.467  YOU ARE HIT by a grub — hearts 1/3
   [3.47 s] hearts 1/3
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
   [3.50 s] hearts 1/3
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
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
   [5.00 s] hearts 1/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
   [7.00 s] hearts 0/3
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
end at 7.03 s: hearts 0/3, enemies left 1
```

### Round 1: @run/play/idle60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
end 8
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
   |        P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [1.50 s] hearts 3/3
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
  2.033  the grub is open (right)
   [2.03 s] hearts 2/3
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
  2.933  a grub rears back (right)
   [2.93 s] hearts 2/3
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
   [3.00 s] hearts 2/3
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
  3.450  YOU ARE HIT by a grub — hearts 1/3
   [3.45 s] hearts 1/3
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
   [3.50 s] hearts 1/3
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
  3.583  the grub is open (on you)
   [3.58 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
   [7.00 s] hearts 0/3
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
end at 7.00 s: hearts 0/3, enemies left 1
```

### Round 1: @run/trace/idle30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn grub 12 4
end 8
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(12.00,4.00,hp=2,approach,0.000) | setup
t=1.400 frame=42 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.900 frame=57 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=1.967 frame=59 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=2.767 frame=83 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.183) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.967 frame=89 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=2,windup,0.483) | windup {'who': 0, 'side': 'right'}
t=3.467 frame=104 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.22,4.00,hp=2,strike,0.133) | strike {'who': 0}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.600 frame=108 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=4.267 frame=128 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.500 frame=135 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=5.000 frame=150 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=5.033 frame=151 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.833 frame=175 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.033 frame=211 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | session_end
t=7.033 frame=211 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | end
```

### Round 1: @run/trace/idle60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
end 8
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(12.00,4.00,hp=2,approach,0.000) | setup
t=1.383 frame=83 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.883 frame=113 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=1.933 frame=116 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.92,4.00,hp=2,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.033 frame=122 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=2.733 frame=164 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.933 frame=176 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=3.433 frame=206 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=3.450 frame=207 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.22,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.583 frame=215 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=4.250 frame=255 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.483 frame=269 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=4.983 frame=299 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=5.000 frame=300 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.800 frame=348 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.000 frame=420 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | session_end
t=7.000 frame=420 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | end
```

### Round 1: @run/play/windup30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn grub 12 4
1.6 attack
end 5
```

Exit: 0 (0.0 s). Output:

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
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [1.50 s] hearts 3/3
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
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P w     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P w     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [3.00 s] hearts 3/3
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
  3.233  YOU ARE HIT by a grub — hearts 2/3
   [3.23 s] hearts 2/3
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
  3.317  the grub is open (right)
   [3.33 s] hearts 2/3
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
   [3.50 s] hearts 2/3
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
   [4.00 s] hearts 2/3
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
  4.217  a grub rears back (right)
   [4.23 s] hearts 2/3
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
   [4.50 s] hearts 2/3
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
  4.733  YOU ARE HIT by a grub — hearts 1/3
   [4.73 s] hearts 1/3
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
  4.867  the grub is open (on you)
   [4.87 s] hearts 1/3
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
   [5.00 s] hearts 1/3
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
end at 5.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/windup60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
1.6 attack
end 5
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
   |        P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [1.50 s] hearts 3/3
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
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P w     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P w     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.683  a grub rears back (right)
   [2.68 s] hearts 3/3
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
   [3.00 s] hearts 3/3
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
  3.233  YOU ARE HIT by a grub — hearts 2/3
   [3.23 s] hearts 2/3
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
  3.333  the grub is open (right)
   [3.33 s] hearts 2/3
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
   [3.50 s] hearts 2/3
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
   [4.00 s] hearts 2/3
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
  4.233  a grub rears back (right)
   [4.23 s] hearts 2/3
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
   [4.50 s] hearts 2/3
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
  4.750  YOU ARE HIT by a grub — hearts 1/3
   [4.75 s] hearts 1/3
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
  4.883  the grub is open (on you)
   [4.88 s] hearts 1/3
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
   [5.00 s] hearts 1/3
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
end at 5.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/trace/windup30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn grub 12 4
1.6 attack
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(12.00,4.00,hp=2,approach,0.000) | setup
t=1.400 frame=42 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.633 frame=49 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.42,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0}
t=2.667 frame=80 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=3.167 frame=95 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=3.233 frame=97 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.81,4.00,hp=1,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.333 frame=100 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=4.033 frame=121 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.183) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.233 frame=127 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,windup,0.483) | windup {'who': 0, 'side': 'right'}
t=4.733 frame=142 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.22,4.00,hp=1,strike,0.133) | strike {'who': 0}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.867 frame=146 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=5.000 frame=150 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.033 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.767) | end
```

### Round 1: @run/trace/windup60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
1.6 attack
end 5
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(12.00,4.00,hp=2,approach,0.000) | setup
t=1.383 frame=83 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.617 frame=97 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.33,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0}
t=2.683 frame=161 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=3.183 frame=191 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=3.233 frame=194 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.92,4.00,hp=1,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.333 frame=200 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=4.033 frame=242 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.233 frame=254 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=4.733 frame=284 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=4.750 frame=285 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.22,4.00,hp=1,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.883 frame=293 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=5.000 frame=300 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.550 stun_left=0.050 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.783) | end
```

### Round 1: @run/play/recovery30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn grub 12 4
2.5 attack
end 6
```

Exit: 0 (0.0 s). Output:

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
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [1.50 s] hearts 3/3
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
   [2.00 s] hearts 2/3
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
   [3.00 s] hearts 2/3
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
  3.500  YOU ARE HIT by a grub — hearts 1/3
   [3.50 s] hearts 1/3
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
  3.600  the grub is open (right)
   [3.60 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
  4.500  a grub rears back (right)
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
   [5.00 s] hearts 1/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
end at 6.00 s: hearts 0/3, enemies left 1
```

### Round 1: @run/play/recovery60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
2.5 attack
end 6
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
   |        P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
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
   [1.50 s] hearts 3/3
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
  2.033  the grub is open (right)
   [2.03 s] hearts 2/3
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
  2.500  you swipe: grub hit (1 left)
   [2.52 s] hearts 2/3
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
  2.933  a grub rears back (right)
   [2.93 s] hearts 2/3
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
   [3.00 s] hearts 2/3
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
  3.483  YOU ARE HIT by a grub — hearts 1/3
   [3.48 s] hearts 1/3
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
   [3.50 s] hearts 1/3
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
  3.583  the grub is open (right)
   [3.58 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
  4.483  a grub rears back (right)
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
end at 6.00 s: hearts 0/3, enemies left 1
```

### Round 1: @run/trace/recovery30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn grub 12 4
2.5 attack
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(12.00,4.00,hp=2,approach,0.000) | setup
t=1.400 frame=42 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.900 frame=57 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=1.967 frame=59 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=2.533 frame=76 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.233 stun_left=0.000 shots=0 | grub#0(8.42,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
t=2.767 frame=83 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,recovery,0.183) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.967 frame=89 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,windup,0.483) | windup {'who': 0, 'side': 'right'}
t=3.467 frame=104 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.14,4.00,hp=1,strike,0.133) | strike {'who': 0}
t=3.500 frame=105 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.92,4.00,hp=1,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.600 frame=108 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=4.300 frame=129 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.500 frame=135 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=5.000 frame=150 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=5.033 frame=151 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.19,4.00,hp=1,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.833 frame=175 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.19,4.00,hp=1,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.000 frame=180 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.19,4.00,hp=1,approach,0.000) | end
```

### Round 1: @run/trace/recovery60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
2.5 attack
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(12.00,4.00,hp=2,approach,0.000) | setup
t=1.383 frame=83 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.883 frame=113 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=1.933 frame=116 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.92,4.00,hp=2,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.033 frame=122 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=2.517 frame=151 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.217 stun_left=0.000 shots=0 | grub#0(8.33,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
t=2.733 frame=164 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.933 frame=176 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=3.433 frame=206 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=3.483 frame=209 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.92,4.00,hp=1,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.583 frame=215 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=4.283 frame=257 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.483 frame=269 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=4.983 frame=299 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.25,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=5.000 frame=300 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.22,4.00,hp=1,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.800 frame=348 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.22,4.00,hp=1,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.000 frame=360 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.22,4.00,hp=1,approach,0.000) | end
```

### Round 1: @run/play/room4move30 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 30
0.5 move left
end 8
```

Exit: 0 (0.0 s). Output:

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
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |  g     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
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
   [1.50 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |   g            |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.733  a grub rears back (above)
   [1.73 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |                |
   |   G            |
   |   PG           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
   [1.80 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |   PG           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  1.833  YOU ARE HIT by a grub — hearts 2/3
   [1.83 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  1.950  the grub is open (right)
   [1.97 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |   G            |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.383  the grub is open (above)
   [2.40 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.600  spitter (bottom right) spits
   [2.60 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.850  a grub rears back (right)
   [2.87 s] hearts 2/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   [3.00 s] hearts 2/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
  3.283  a grub rears back (above)
   [3.30 s] hearts 2/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.367  YOU ARE HIT by a grub — hearts 1/3
   [3.37 s] hearts 1/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.500  spitter (top right) charges
  3.500  the grub is open (on you)
   [3.50 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |          *     |
   |                |
   |   P            |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
  3.933  the grub is open (on you)
   [3.93 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |         *      |
   |                |
   |   P            |
   |                |
   |                |
   |           *    |
   |               s|
   +----------------+
   [4.00 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |         *      |
   |                |
   |   P            |
   |                |
   |                |
   |           *    |
   |               s|
   +----------------+
  4.300  spitter (top right) spits
  4.300  spitter (bottom right) charges
   [4.30 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |        *       |
   |                |
   |   P            |
   |                |
   |          *     |
   |                |
   |               S|
   +----------------+
  4.400  a grub rears back (on you)
   [4.40 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |        *       |
   |                |
   |   P            |
   |                |
   |          *     |
   |                |
   |               S|
   +----------------+
   [4.50 s] hearts 1/3
   +----------------+
   |              *s|
   |                |
   |                |
   |       *        |
   |   P            |
   |                |
   |          *     |
   |                |
   |               S|
   +----------------+
  4.833  a grub rears back (on you)
   [4.83 s] hearts 1/3
   +----------------+
   |             * s|
   |                |
   |                |
   |      *         |
   |   P            |
   |                |
   |         *      |
   |                |
   |               S|
   +----------------+
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
   [5.00 s] hearts 0/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
  6.933  run over — rooms cleared: 0
  6.933  press attack to start again
end at 6.93 s: hearts 0/3, enemies left 4
```

### Round 1: @run/play/room4move60 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
0.5 move left
end 8
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 4 — 60 FPS
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
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |  g     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
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
   [1.50 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |   g            |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.733  a grub rears back (above)
   [1.73 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |                |
   |   G            |
   |   PG           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
   [1.80 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |   PG           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  1.817  YOU ARE HIT by a grub — hearts 2/3
   [1.82 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  1.950  the grub is open (right)
   [1.95 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |   G            |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.383  the grub is open (above)
   [2.38 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.600  spitter (bottom right) spits
   [2.60 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.850  a grub rears back (right)
   [2.85 s] hearts 2/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   [3.00 s] hearts 2/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
  3.283  a grub rears back (above)
   [3.28 s] hearts 2/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.367  YOU ARE HIT by a grub — hearts 1/3
   [3.37 s] hearts 1/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |                |
   |   P            |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.500  spitter (top right) charges
  3.500  the grub is open (on you)
   [3.50 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |          *     |
   |                |
   |   P            |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
  3.933  the grub is open (on you)
   [3.93 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |         *      |
   |                |
   |   P            |
   |                |
   |                |
   |           *    |
   |               s|
   +----------------+
   [4.00 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |         *      |
   |                |
   |   P            |
   |                |
   |                |
   |           *    |
   |               s|
   +----------------+
  4.300  spitter (top right) spits
  4.300  spitter (bottom right) charges
   [4.30 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |        *       |
   |                |
   |   P            |
   |                |
   |          *     |
   |                |
   |               S|
   +----------------+
  4.400  a grub rears back (on you)
   [4.40 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |        *       |
   |                |
   |   P            |
   |                |
   |          *     |
   |                |
   |               S|
   +----------------+
   [4.50 s] hearts 1/3
   +----------------+
   |              *s|
   |                |
   |                |
   |       *        |
   |   P            |
   |                |
   |          *     |
   |                |
   |               S|
   +----------------+
  4.833  a grub rears back (on you)
   [4.83 s] hearts 1/3
   +----------------+
   |             * s|
   |                |
   |                |
   |      *         |
   |   P            |
   |                |
   |         *      |
   |                |
   |               S|
   +----------------+
  4.917  YOU ARE HIT by a grub — hearts 0/3
  4.917  you went down
   [4.92 s] hearts 0/3
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
   [5.00 s] hearts 0/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
  6.917  run over — rooms cleared: 0
  6.917  press attack to start again
end at 6.92 s: hearts 0/3, enemies left 4
```

### Round 1: @run/play/room4dash30 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 30
0.5 dash left
end 8
```

Exit: 0 (0.0 s). Output:

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
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |  g     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
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
   [1.00 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |  g             |
   |                |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.467  YOU ARE HIT by a grub — hearts 2/3
   [1.47 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |  g             |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |  g             |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.550  the grub is open (left)
   [1.57 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |   g            |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
   [1.80 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   g            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  1.933  a grub rears back (left)
   [1.93 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.450  a grub rears back (left)
   [2.47 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.500  YOU ARE HIT by a grub — hearts 1/3
   [2.50 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.600  spitter (bottom right) spits
  2.583  the grub is open (left)
   [2.60 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
  3.100  the grub is open (on you)
   [3.10 s] hearts 1/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.500  spitter (top right) charges
  3.483  a grub rears back (left)
   [3.50 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |          *     |
   |                |
   |    P           |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
  4.000  YOU ARE HIT by a grub — hearts 0/3
  4.000  you went down
   [4.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  6.000  run over — rooms cleared: 0
  6.000  press attack to start again
end at 6.00 s: hearts 0/3, enemies left 4
```

### Round 1: @run/play/room4dash60 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
0.5 dash left
end 8
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 4 — 60 FPS
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
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |  g     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  0.500  you dash left
  0.883  a grub rears back (left)
   [0.88 s] hearts 3/3
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
   [1.00 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |  g             |
   |                |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.433  YOU ARE HIT by a grub — hearts 2/3
   [1.43 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |  g             |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |  g             |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.533  the grub is open (left)
   [1.53 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |   g            |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
   [1.80 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   g            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  1.917  a grub rears back (left)
   [1.92 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.433  a grub rears back (left)
   [2.43 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.467  YOU ARE HIT by a grub — hearts 1/3
   [2.47 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |   G            |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.50 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |   GP           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.567  the grub is open (left)
   [2.57 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.600  spitter (bottom right) spits
   [2.60 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
  3.083  the grub is open (on you)
   [3.08 s] hearts 1/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
  3.467  a grub rears back (left)
   [3.47 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |          *     |
   |                |
   |    P           |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.500  spitter (top right) charges
   [3.50 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |          *     |
   |                |
   |    P           |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
  3.983  YOU ARE HIT by a grub — hearts 0/3
  3.983  you went down
   [3.98 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [4.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |    x           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  5.983  run over — rooms cleared: 0
  5.983  press attack to start again
end at 5.98 s: hearts 0/3, enemies left 4
```

### Round 1: @run/trace/room3setup — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 60
end 0.1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=3 dt=0.01667
t=0.000 frame=0 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,idle,1.000) spitter#1(14.00,7.00,hp=2,idle,1.800) spitter#2(2.00,7.00,hp=2,idle,2.600) | setup
t=0.100 frame=6 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,idle,0.900) spitter#1(14.00,7.00,hp=2,idle,1.700) spitter#2(2.00,7.00,hp=2,idle,2.500) | end
```

### Round 1: @run/play/room1over30 — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 30
15 attack
end 20
```

Exit: 0 (0.0 s). Output:

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
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.400  a grub rears back (above)
   [1.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.900  a grub rears back (left)
   [1.90 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.967  YOU ARE HIT by a grub — hearts 2/3
   [1.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.050  the grub is open (above)
   [2.07 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GP  g    |
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
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.550  the grub is open (left)
   [2.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.900  a grub rears back (right)
   [2.90 s] hearts 2/3
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
  2.950  a grub rears back (above)
   [2.97 s] hearts 2/3
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
   [3.00 s] hearts 2/3
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
  3.467  YOU ARE HIT by a grub — hearts 1/3
   [3.47 s] hearts 1/3
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
   [3.50 s] hearts 1/3
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
  3.550  the grub is open (right)
  3.567  a grub rears back (left)
   [3.57 s] hearts 1/3
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
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
  4.217  the grub is open (on you)
   [4.23 s] hearts 1/3
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
  4.450  a grub rears back (right)
   [4.47 s] hearts 1/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
   [15.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.400  a grub rears back (above)
   [16.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.900  a grub rears back (left)
   [16.90 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.967  YOU ARE HIT by a grub — hearts 2/3
   [16.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 17.050  the grub is open (above)
   [17.07 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 17.550  the grub is open (left)
   [17.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 17.900  a grub rears back (right)
   [17.90 s] hearts 2/3
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
 17.950  a grub rears back (above)
   [17.97 s] hearts 2/3
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
   [18.00 s] hearts 2/3
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
 18.467  YOU ARE HIT by a grub — hearts 1/3
   [18.47 s] hearts 1/3
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
   [18.50 s] hearts 1/3
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
 18.550  the grub is open (right)
 18.567  a grub rears back (left)
   [18.57 s] hearts 1/3
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
 18.600  the grub is open (on you)
   [18.60 s] hearts 1/3
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
   [19.00 s] hearts 1/3
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
 19.217  the grub is open (on you)
   [19.23 s] hearts 1/3
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
 19.450  a grub rears back (right)
   [19.47 s] hearts 1/3
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
 19.500  a grub rears back (on you)
   [19.50 s] hearts 1/3
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
 19.967  YOU ARE HIT by a grub — hearts 0/3
 19.967  you went down
   [19.97 s] hearts 0/3
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
   [20.00 s] hearts 0/3
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
end at 20.00 s: hearts 0/3, enemies left 3
```

### Round 1: @run/play/room1over60 — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 60
15 attack
end 20
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 1 — 60 FPS
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
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.383  a grub rears back (above)
   [1.38 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.883  a grub rears back (left)
   [1.88 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.933  YOU ARE HIT by a grub — hearts 2/3
   [1.93 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
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
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.033  the grub is open (above)
   [2.03 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GP  g    |
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
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.533  the grub is open (left)
   [2.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.883  a grub rears back (right)
   [2.88 s] hearts 2/3
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
  2.933  a grub rears back (above)
   [2.93 s] hearts 2/3
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
   [3.00 s] hearts 2/3
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
  3.433  YOU ARE HIT by a grub — hearts 1/3
   [3.43 s] hearts 1/3
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
   [3.50 s] hearts 1/3
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
  3.533  the grub is open (right)
  3.533  a grub rears back (left)
   [3.53 s] hearts 1/3
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
  3.583  the grub is open (on you)
   [3.58 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
  4.183  the grub is open (on you)
   [4.18 s] hearts 1/3
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
  4.433  a grub rears back (right)
   [4.43 s] hearts 1/3
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
  4.950  YOU ARE HIT by a grub — hearts 0/3
  4.950  you went down
   [4.95 s] hearts 0/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
  6.950  run over — rooms cleared: 0
  6.950  press attack to start again
 15.000  a new run begins
 15.000  room 1 begins
   [15.02 s] hearts 3/3
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
   [15.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.383  a grub rears back (above)
   [16.38 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.883  a grub rears back (left)
   [16.88 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.933  YOU ARE HIT by a grub — hearts 2/3
   [16.93 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 17.033  the grub is open (above)
   [17.03 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 17.533  the grub is open (left)
   [17.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 17.883  a grub rears back (right)
   [17.88 s] hearts 2/3
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
 17.933  a grub rears back (above)
   [17.93 s] hearts 2/3
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
   [18.00 s] hearts 2/3
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
 18.433  YOU ARE HIT by a grub — hearts 1/3
   [18.43 s] hearts 1/3
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
   [18.50 s] hearts 1/3
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
 18.533  the grub is open (right)
 18.533  a grub rears back (left)
   [18.53 s] hearts 1/3
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
 18.583  the grub is open (on you)
   [18.58 s] hearts 1/3
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
   [19.00 s] hearts 1/3
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
 19.183  the grub is open (on you)
   [19.18 s] hearts 1/3
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
 19.433  a grub rears back (right)
   [19.43 s] hearts 1/3
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
 19.483  a grub rears back (on you)
   [19.48 s] hearts 1/3
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
   [19.50 s] hearts 1/3
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
 19.950  YOU ARE HIT by a grub — hearts 0/3
 19.950  you went down
   [19.95 s] hearts 0/3
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
   [20.00 s] hearts 0/3
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
end at 20.00 s: hearts 0/3, enemies left 3
```

### Round 1: @run/trace/room1over60 — `python3 play.py --view trace {script}`

Script:

```text
room 1
fps 60
15 attack
end 20
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=1 dt=0.01667
t=0.000 frame=0 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.00,4.00,hp=2,approach,0.000) grub#1(15.00,4.00,hp=2,approach,0.000) grub#2(8.00,0.00,hp=2,approach,0.000) | setup
t=1.383 frame=83 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(5.77,4.00,hp=2,approach,0.000) grub#1(12.23,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=1.883 frame=113 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.500) grub#1(11.23,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,strike,0.150) | strike {'who': 2}; windup {'who': 0, 'side': 'left'}
t=1.933 frame=116 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.450) grub#1(11.13,4.00,hp=2,approach,0.000) grub#2(8.00,3.08,hp=2,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.033 frame=122 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.350) grub#1(10.93,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 2, 'side': 'above'}
t=2.383 frame=143 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,strike,0.150) grub#1(10.23,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.550) | strike {'who': 0}
t=2.533 frame=152 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.900) grub#1(9.93,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.400) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=2.733 frame=164 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.700) grub#1(9.53,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.883 frame=173 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.550) grub#1(9.25,4.00,hp=2,windup,0.500) grub#2(8.00,3.75,hp=2,recovery,0.050) | windup {'who': 1, 'side': 'right'}
t=2.933 frame=176 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.500) grub#1(9.25,4.00,hp=2,windup,0.450) grub#2(8.00,3.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=3.383 frame=203 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.050) grub#1(9.25,4.00,hp=2,strike,0.150) grub#2(8.00,3.75,hp=2,windup,0.050) | strike {'who': 1}
t=3.433 frame=206 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(8.92,4.00,hp=2,strike,0.100) grub#2(8.00,3.75,hp=2,strike,0.150) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}; strike {'who': 2}
t=3.533 frame=212 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(7.75,4.00,hp=2,windup,0.500) grub#1(8.25,4.00,hp=2,recovery,0.900) grub#2(8.00,3.92,hp=2,strike,0.050) | recover {'cause': 'strike', 'who': 1, 'side': 'right'}; windup {'who': 0, 'side': 'left'}
t=3.583 frame=215 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.650 stun_left=0.150 shots=0 | grub#0(7.75,4.00,hp=2,windup,0.450) grub#1(8.25,4.00,hp=2,recovery,0.850) grub#2(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 2, 'side': 'on you'}
t=4.033 frame=242 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,strike,0.150) grub#1(8.25,4.00,hp=2,recovery,0.400) grub#2(8.00,4.00,hp=2,recovery,0.450) | strike {'who': 0}
t=4.183 frame=251 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.050 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) grub#1(8.25,4.00,hp=2,recovery,0.250) grub#2(8.00,4.00,hp=2,recovery,0.300) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=4.233 frame=254 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.850) grub#1(8.25,4.00,hp=2,recovery,0.200) grub#2(8.00,4.00,hp=2,recovery,0.250) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.433 frame=266 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.650) grub#1(8.25,4.00,hp=2,windup,0.500) grub#2(8.00,4.00,hp=2,recovery,0.050) | windup {'who': 1, 'side': 'right'}
t=4.483 frame=269 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.600) grub#1(8.25,4.00,hp=2,windup,0.450) grub#2(8.00,4.00,hp=2,windup,0.500) | windup {'who': 2, 'side': 'on you'}
t=4.933 frame=296 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.150) grub#1(8.25,4.00,hp=2,strike,0.150) grub#2(8.00,4.00,hp=2,windup,0.050) | strike {'who': 1}
t=4.950 frame=297 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.750 frame=345 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.950 frame=417 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=15.017 frame=901 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.03,4.00,hp=2,approach,0.000) grub#1(14.97,4.00,hp=2,approach,0.000) grub#2(8.00,0.03,hp=2,approach,0.000) | run_start; room_loaded {'room': '1'}
t=16.383 frame=983 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(5.77,4.00,hp=2,approach,0.000) grub#1(12.23,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=16.883 frame=1013 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.500) grub#1(11.23,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,strike,0.150) | strike {'who': 2}; windup {'who': 0, 'side': 'left'}
t=16.933 frame=1016 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.450) grub#1(11.13,4.00,hp=2,approach,0.000) grub#2(8.00,3.08,hp=2,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=17.033 frame=1022 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.350) grub#1(10.93,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 2, 'side': 'above'}
t=17.383 frame=1043 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,strike,0.150) grub#1(10.23,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.550) | strike {'who': 0}
t=17.533 frame=1052 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.900) grub#1(9.93,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.400) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=17.733 frame=1064 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.700) grub#1(9.53,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=17.883 frame=1073 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.550) grub#1(9.25,4.00,hp=2,windup,0.500) grub#2(8.00,3.75,hp=2,recovery,0.050) | windup {'who': 1, 'side': 'right'}
t=17.933 frame=1076 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.500) grub#1(9.25,4.00,hp=2,windup,0.450) grub#2(8.00,3.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=18.383 frame=1103 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.050) grub#1(9.25,4.00,hp=2,strike,0.150) grub#2(8.00,3.75,hp=2,windup,0.050) | strike {'who': 1}
t=18.433 frame=1106 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(8.92,4.00,hp=2,strike,0.100) grub#2(8.00,3.75,hp=2,strike,0.150) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}; strike {'who': 2}
t=18.533 frame=1112 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(7.75,4.00,hp=2,windup,0.500) grub#1(8.25,4.00,hp=2,recovery,0.900) grub#2(8.00,3.92,hp=2,strike,0.050) | recover {'cause': 'strike', 'who': 1, 'side': 'right'}; windup {'who': 0, 'side': 'left'}
t=18.583 frame=1115 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.650 stun_left=0.150 shots=0 | grub#0(7.75,4.00,hp=2,windup,0.450) grub#1(8.25,4.00,hp=2,recovery,0.850) grub#2(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 2, 'side': 'on you'}
t=19.033 frame=1142 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,strike,0.150) grub#1(8.25,4.00,hp=2,recovery,0.400) grub#2(8.00,4.00,hp=2,recovery,0.450) | strike {'who': 0}
t=19.183 frame=1151 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.050 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) grub#1(8.25,4.00,hp=2,recovery,0.250) grub#2(8.00,4.00,hp=2,recovery,0.300) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=19.233 frame=1154 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.850) grub#1(8.25,4.00,hp=2,recovery,0.200) grub#2(8.00,4.00,hp=2,recovery,0.250) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=19.433 frame=1166 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.650) grub#1(8.25,4.00,hp=2,windup,0.500) grub#2(8.00,4.00,hp=2,recovery,0.050) | windup {'who': 1, 'side': 'right'}
t=19.483 frame=1169 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.600) grub#1(8.25,4.00,hp=2,windup,0.450) grub#2(8.00,4.00,hp=2,windup,0.500) | windup {'who': 2, 'side': 'on you'}
t=19.933 frame=1196 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.150) grub#1(8.25,4.00,hp=2,strike,0.150) grub#2(8.00,4.00,hp=2,windup,0.050) | strike {'who': 1}
t=19.950 frame=1197 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=20.000 frame=1200 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.750 stun_left=0.250 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | end
```
>>>END
