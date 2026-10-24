# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/24-studio-to-qa.md
next_seq: 26
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/26-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/24-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 24
from: studio
to: qa
stage: Verify
outcome: routed
---
# 24: studio → qa — verify Build 0.5 against the combat spec (AC-1…AC-17)

## Task

Verify the current build in `repo/` against the acceptance criteria in `design/combat.md` (AC-1…AC-17) and the run and room rules in D-003. Check for regressions, including at both 30 and 60 FPS. Report pass/fail per criterion.

## Context

Goal G-001 (combat feels monotonous). Option A (D-002) reworks existing enemy behavior, built as one change set (D-004). Build 0.5 is ready for independent verification. This Handoff is composed by the Studio and contains no implementer reasoning. Verify from the spec and the build.

## Findings

- Build: `repo/`, run through the project's run commands: `run_tests`, `run_play`, `run_trace`, `run_bots` (see `project.md` front matter). Controls and script format are in `manual.md`.
- `run_tests` layout: `ManualTest` reads `manual.md` from the directory above `repo/`. Run the tests in a layout where `manual.md` sits next to `repo/`, as in the project directory. Report the `ManualTest` result separately. The Owner placed `manual.md` (D-005); one earlier test run in a layout without it errored with FileNotFoundError, so that test has no valid result yet.
- Known scope limit: the pause behavior (F11 in the plan) is not implemented. Mark it "not verifiable", not as a failure.
- AC-8 (the doubled spit line when two spitters print identical text) and AC-15 (`manual.md` content) are in scope.
- Visuals (colors, glyph readability; `design/combat-visuals.md`) are reviewed in parallel by the art-director. Check only what the acceptance criteria in `combat.md` state about them.

## Decisions already made

- D-002: Option A, rework existing enemy behavior first.
- D-003: room mix is across rooms; zero hearts ends the run; a room clear heals one heart.
- D-004: one sequential change set on the existing simulation.
- D-005: the Owner placed the draft `manual.md` unchanged.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Do not edit the build. Report failures with a script that reproduces them.

## Open questions

- If `manual.md` cannot be placed next to `repo/` in your workspace, say so exactly. Do not mark `ManualTest` pass or fail. Report it as blocked on the Owner.

## Expected output

A pass/fail report per criterion (AC-1…AC-17) plus the `run_tests` totals, regressions found, and items not verifiable, each with reproduction scripts for failures. Address the result to `studio`. The result is used to compose the playtester's Handoff without implementation history.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: project.md, design/combat.md, manual.md, repo/ (build), repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: none (composed by the Studio; earlier handoffs contain the implementer's self-assessment)
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

<<<FILE studio/skills/reproduce-defect.md
---
name: reproduce-defect
description: Reproduce a reported problem reliably and turn it into a precise defect report with acceptance criteria for the fix.
---
# Skill: Reproduce defect

Typical roles: qa. Any Role whose responsibility covers confirming a defect may use it.

## When to use

A problem is reported but has not been reproduced first-hand, or its conditions are unclear.

## Inputs

The report, how to run the build, the design documents that define expected behavior, the
project's supported platforms and settings.

## Method

1. Reproduce exactly as reported. Then vary one condition at a time (timing, input device, frame
   rate, platform, state) to find the minimal reliable steps and the boundary where it stops.
2. Name the source of "expected": cite the design document or Decision. If no source defines the
   expected behavior, it is a spec gap, not a defect — say so and hand back to `game-designer`.
3. Rate severity from the player's view (blocks progress / hurts the experience / cosmetic) and
   frequency.
4. Write acceptance criteria for the fix: observable checks, including the conditions you varied.

## Output

Defect report: steps, expected (with source), actual, conditions and boundary, severity, frequency,
acceptance criteria, evidence (logs, recordings, notes).

## Do not

Guess at code-level causes as fact; label any hypothesis as one. Do not fix the defect.
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
Ran 34 tests in 0.049s

FAILED (errors=1)
```

### Round 1: @run/trace/grub30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
spawn grub 12 4
player 8 4
end 5
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
t=5.000 frame=150 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | end
```

### Round 1: @run/trace/room5_60 — `python3 play.py --view trace {script}`

Script:

```text
room 5
fps 60
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.00,1.00,hp=2,approach,0.000) grub#1(0.00,6.00,hp=2,approach,0.000) grub#2(4.00,8.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,1.000) spitter#4(15.00,8.00,hp=2,idle,1.800) | setup
t=1.000 frame=60 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.84,1.79,hp=2,approach,0.000) grub#1(1.94,5.51,hp=2,approach,0.000) grub#2(5.41,6.59,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,charge,0.800) spitter#4(15.00,8.00,hp=2,idle,0.800) | charge {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}
t=1.800 frame=108 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(4.31,2.42,hp=2,approach,0.000) grub#1(3.49,5.13,hp=2,approach,0.000) grub#2(6.55,5.45,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,recovery,0.600) spitter#4(15.00,8.00,hp=2,charge,0.800) | spit {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.217 frame=133 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(5.07,2.75,hp=2,approach,0.000) grub#1(4.30,4.92,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,windup,0.500) spitter#3(15.00,0.00,hp=2,recovery,0.183) spitter#4(15.00,8.00,hp=2,charge,0.383) | windup {'who': 2, 'side': 'left'}
t=2.600 frame=156 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(5.78,3.05,hp=2,approach,0.000) grub#1(5.04,4.74,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,windup,0.117) spitter#3(15.00,0.00,hp=2,idle,0.900) spitter#4(15.00,8.00,hp=2,recovery,0.600) | spit {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.717 frame=163 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(5.99,3.14,hp=2,approach,0.000) grub#1(5.27,4.68,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,strike,0.150) spitter#3(15.00,0.00,hp=2,idle,0.783) spitter#4(15.00,8.00,hp=2,recovery,0.483) | strike {'who': 2}
t=2.767 frame=166 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=2 | grub#0(6.09,3.18,hp=2,approach,0.000) grub#1(5.37,4.66,hp=2,approach,0.000) grub#2(7.35,4.65,hp=2,strike,0.100) spitter#3(15.00,0.00,hp=2,idle,0.733) spitter#4(15.00,8.00,hp=2,recovery,0.433) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.867 frame=172 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=2 | grub#0(6.27,3.26,hp=2,approach,0.000) grub#1(5.56,4.61,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,recovery,0.900) spitter#3(15.00,0.00,hp=2,idle,0.633) spitter#4(15.00,8.00,hp=2,recovery,0.333) | recover {'cause': 'strike', 'who': 2, 'side': 'left'}
t=3.183 frame=191 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.383 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.500) grub#1(6.18,4.46,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,recovery,0.583) spitter#3(15.00,0.00,hp=2,idle,0.317) spitter#4(15.00,8.00,hp=2,recovery,0.017) | windup {'who': 0, 'side': 'left'}
t=3.500 frame=210 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.067 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.183) grub#1(6.79,4.30,hp=2,windup,0.500) grub#2(7.82,4.18,hp=2,recovery,0.267) spitter#3(15.00,0.00,hp=2,charge,0.800) spitter#4(15.00,8.00,hp=2,idle,0.800) | charge {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; windup {'who': 1, 'side': 'left'}
t=3.567 frame=214 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.117) grub#1(6.79,4.30,hp=2,windup,0.433) grub#2(7.82,4.18,hp=2,recovery,0.200) spitter#3(15.00,0.00,hp=2,charge,0.733) spitter#4(15.00,8.00,hp=2,idle,0.733) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.683 frame=221 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,strike,0.150) grub#1(6.79,4.30,hp=2,windup,0.317) grub#2(7.82,4.18,hp=2,recovery,0.083) spitter#3(15.00,0.00,hp=2,charge,0.617) spitter#4(15.00,8.00,hp=2,idle,0.617) | strike {'who': 0}
t=3.733 frame=224 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=2 | grub#0(7.16,3.64,hp=2,strike,0.100) grub#1(6.79,4.30,hp=2,windup,0.267) grub#2(7.82,4.18,hp=2,recovery,0.033) spitter#3(15.00,0.00,hp=2,charge,0.567) spitter#4(15.00,8.00,hp=2,idle,0.567) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.833 frame=230 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.900) grub#1(6.79,4.30,hp=2,windup,0.167) grub#2(7.82,4.18,hp=2,windup,0.500) spitter#3(15.00,0.00,hp=2,charge,0.467) spitter#4(15.00,8.00,hp=2,idle,0.467) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}; windup {'who': 2, 'side': 'left'}
t=4.000 frame=240 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.033 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.733) grub#1(6.79,4.30,hp=2,strike,0.150) grub#2(7.82,4.18,hp=2,windup,0.333) spitter#3(15.00,0.00,hp=2,charge,0.300) spitter#4(15.00,8.00,hp=2,idle,0.300) | strike {'who': 1}
t=4.150 frame=249 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.383 stun_left=0.000 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.583) grub#1(7.76,4.06,hp=2,recovery,0.900) grub#2(7.82,4.18,hp=2,windup,0.183) spitter#3(15.00,0.00,hp=2,charge,0.150) spitter#4(15.00,8.00,hp=2,idle,0.150) | recover {'cause': 'strike', 'who': 1, 'side': 'left'}
t=4.300 frame=258 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.233 stun_left=0.000 shots=3 | grub#0(7.77,3.90,hp=2,recovery,0.433) grub#1(7.76,4.06,hp=2,recovery,0.750) grub#2(7.82,4.18,hp=2,windup,0.033) spitter#3(15.00,0.00,hp=2,recovery,0.600) spitter#4(15.00,8.00,hp=2,charge,0.800) | spit {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=4.333 frame=260 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=3 | grub#0(7.77,3.90,hp=2,recovery,0.400) grub#1(7.76,4.06,hp=2,recovery,0.717) grub#2(7.82,4.18,hp=2,strike,0.150) spitter#3(15.00,0.00,hp=2,recovery,0.567) spitter#4(15.00,8.00,hp=2,charge,0.767) | strike {'who': 2}
t=4.483 frame=269 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.050 stun_left=0.000 shots=3 | grub#0(7.77,3.90,hp=2,recovery,0.250) grub#1(7.76,4.06,hp=2,recovery,0.567) grub#2(8.00,4.00,hp=2,recovery,0.900) spitter#3(15.00,0.00,hp=2,recovery,0.417) spitter#4(15.00,8.00,hp=2,charge,0.617) | recover {'cause': 'strike', 'who': 2, 'side': 'on you'}
t=4.533 frame=272 room=5 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(7.76,4.06,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=5.333 frame=320 room=5 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(7.76,4.06,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.533 frame=392 room=5 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(7.76,4.06,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | run_over {'rooms': 0, 'complete': False}
t=6.533 frame=392 room=5 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(7.76,4.06,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | end
```

### Round 1: @run/play/room4_30 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 30
end 6
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
   |   g    P       |
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
   |    g   P       |
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
   |   g            |
   |                |
   |     g  P       |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |    g           |
   |                |
   |     g  P       |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |     g          |
   |      g P       |
   |                |
   |                |
   |                |
   |               S|
   +----------------+
  2.600  spitter (bottom right) spits
   [2.60 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |     g          |
   |      g P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.900  a grub rears back (left)
   [2.90 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |     g          |
   |       GP       |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |      g         |
   |       GP       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.467  YOU ARE HIT by a grub — hearts 2/3
   [3.47 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |      g         |
   |       GP       |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.500  spitter (top right) charges
   [3.50 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |       g   *    |
   |       GP       |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
  3.550  the grub is open (left)
   [3.57 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |          *     |
   |       gP       |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
  3.667  a grub rears back (left)
   [3.67 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |          *     |
   |       GP       |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |               S|
   |                |
   |                |
   |         *      |
   |       GP       |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
  4.267  YOU ARE HIT by a grub — hearts 1/3
   [4.27 s] hearts 1/3
   +----------------+
   |               S|
   |                |
   |                |
   |                |
   |       GP*      |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
  4.300  spitter (top right) spits
  4.300  spitter (bottom right) charges
   [4.30 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |           *    |
   |                |
   |                |
   |               S|
   +----------------+
  4.317  the grub is open (left)
   [4.33 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |          *     |
   |                |
   |                |
   |               S|
   +----------------+
  4.450  a grub rears back (left)
   [4.47 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |          *     |
   |                |
   |                |
   |               S|
   +----------------+
   [4.50 s] hearts 1/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |        P       |
   |          *     |
   |                |
   |                |
   |               S|
   +----------------+
   [5.00 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |        P*      |
   |       *        |
   |                |
   |                |
   |               S|
   +----------------+
  5.067  YOU ARE HIT by a grub — hearts 0/3
  5.067  you went down
   [5.07 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        x       |
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
   |        x       |
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
   |        x       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```
>>>END
