# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
next_seq: 39
runs: tests, play, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/39-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/37-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 37
from: studio
to: qa
stage: Verify
outcome: routed
---
# 37: studio → qa — verify the rendering change (build 0.5) except the manual check

## Task

Verify the current build against AC-17 and AC-18 in `design/combat.md` (and the D-006 display ruling), and confirm that nothing else changed. Do not judge AC-15 (manual text): it is waiting on the Owner, so report `ManualTest` as not run, not as a failure.

## Context

G-001 (combat feels monotonous). The enemy rework is built. The last Build step changed only how the player view draws enemies: an enemy standing on the player's tile must never be hidden (AC-18, D-006), and enemy glyphs must be visible over the swipe arc. The simulation (`game.py`) is meant to be unchanged, so the timings, hearts and hit results from earlier verification should be identical. The previous QA pass (29) repeated scripts C1, C7 and C3 and captured raw output; those are the baseline.

## Findings

None to hand over. Work from the acceptance criteria and the build.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; the practice room is listed in the manual's On screen section.
- D-001: no new inputs.

## Constraints

- Play correctly at 30 and 60 FPS: run each check at both.
- Run through the project's commands (`run_tests`, `run_play`, `run_trace`, `run_bots`).
- `manual.md` may be missing from your workspace. If so, the two `ManualTest` errors are an environment matter. Do not count them against any AC.

## Open questions

None.

## Expected output

A pass/fail report per criterion, with exact scripts and the raw output you rely on. Cover:
1. AC-17 and AC-18 (grub and spitter on the player's tile, wind-up and strike draws, a down player, two enemies overlapping).
2. Repeats of C1, C7, C3 at 30 and 60 FPS compared with the earlier results: timings, hearts and hit results should be unchanged.
3. The hit draw with the swipe arc: the enemy glyph is visible over the arc.
4. Raw captures for the art director's visual re-check: grub on the player's tile in wind-up, strike and recovery draws, a spitter on the tile, a swipe after a miss, the 60 FPS charge-start draw, and one `--color` capture.
5. Anything not verifiable.

Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, manual.md, repo/ (build; run commands in project.md)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
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
# Combat design (build 0.5 target — Option A, G-001)

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text. Updated after QA's second round (handoff 29): overlap rule and AC-15 wording (D-006).

## Experience intent

Every enemy does something the player can read, answer and profit from. A grub is a threat with a beat: it approaches, winds up, strikes, then is open to a counter. A spitter is a threat on a rhythm that the player can dodge or break by walking up and hitting it. The player's attack visibly changes the enemy. Fights are decided by spacing and timing with attack and dash only (D-001, pillars 1 and 3).

## Conventions

- All timings are in seconds and must hold at 30 and 60 FPS (section "30 / 60 FPS").
- Distances are in tiles. The room is 16×9 (x 0–15, y 0–8).
- "Telegraph" means a change the player can see in the player view, at least one on-map change plus one text line. Threat colors are saturated orange/red. The on-map change must be visible in a cell the player can see: an enemy glyph is never hidden under `P` (see "Overlap with the player").
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

### Overlap with the player (F1 ruling, D-006)

- **Physics unchanged.** Enemies and the player have no collision. A grub's lunge and recovery may leave it within the player's tile, and the player may walk or dash onto an enemy. This adds no rule to movement, timing, damage or hit tests; all of those use true positions.
- **Display rule.** In the player view no enemy is ever hidden under `P`. The player is always drawn on their own cell. If an enemy's cell equals the player's cell, that enemy's glyph is drawn in the nearest free in-room cell next to the player (the cell on the side the enemy last approached or struck from first; otherwise right, left, above, below, in that order; if all four are occupied, the next free cell by distance). This is a display offset only.
- It applies in every state, so a grub in Recovery that is "open (on you)" is also visible and its counter can be read. It applies to both enemy types and to damaged glyphs.
- Two enemies sharing the player's cell are displaced to different cells.
- The text lines are unchanged ("(on you)" still prints). The displaced glyph is the on-map change that makes the telegraph complete.
- The immediate draws at Wind-up start, Strike and Recovery start (visuals spec principle 4) use this rule too.
- A displaced glyph does not mean the enemy has moved. A swipe hits by true position, so a swipe may hit an enemy drawn on a different side than the arc.

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
- **Binding wording (ruling, D-006):** the `x` marker and the practice room must both be listed in the `manual.md` section On screen (`manual.md#on-screen`). The mention in the Script table and in "Rooms and runs" does not satisfy this alone. AC-15 is worded to match.

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
- **Enemy on the player's tile:** see "Overlap with the player". It is drawn beside `P`; no gameplay effect.
- **Player down while an enemy shares the cell:** `x` is drawn on the player's cell and the enemy keeps its displaced cell.
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
- **AC-15 Practice room:** `room empty` works as described, and both `x` and the practice room are listed in `manual.md#on-screen` (the On screen section, not only the Script table or Rooms and runs).
- **AC-16 Room mix:** the trace setup rows match the layouts above.
- **AC-17 Frame rate:** AC-1…AC-14 and AC-18 pass at both frame rates, and the 30/60 comparison above holds.
- **AC-18 No hidden enemy:** in the practice room with an idle player and one grub at distance 4, run to 5.5 s, every draw that shows a living grub has a grub glyph in a cell different from the player's cell. Every "a grub rears back" line, including those marked "(on you)", comes with an uppercase `G` or `W` visible on the map in the draw made at that moment. Same for "the grub is open (on you)": a lowercase `g` or `w` is visible. Also, with `player 8 4` and `spawn spitter 8.2 4`, the draws show `P` and an `s` in a neighbouring cell; the spitter's `S` is visible beside `P` during its Charge. The trace shows no change to timings, hearts or positions compared with a build without the display rule (the events of AC-1…AC-4 stay within tolerance).

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A playtester can say, unprompted, what a grub is about to do before it bites, and describes a reason to move or dash.
- A playtester reacts to a projectile at least once (moves, dashes or approaches a spitter) and can tell the two spitters apart.
- Rooms 4 and 5 are described as different from each other and from rooms 1–3 by what the player does, not only by enemy count.
- The playtester can tell from the screen how many hits an enemy needs.
- Grubs are neither trivial nor unfair: the playtester takes some damage in rooms 4–5 but can explain how it happened. (If grubs read as trivial, or the dash seems unnecessary, retune within D-001.)
- A playtester who stands still can see on the map where the grub that bites them is, including when it is right on top of them.
- Observed in QA captures (no ruling): an idle player goes to zero hearts at about 5.0 s in the practice room and in room 1. This is expected for a player who does nothing; the playtest must show whether real players with attack and dash find the first rooms too harsh. Retune the **[tune]** values then.

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director. The art-director may review the choice of the displaced cell for readability (see D-006).
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

The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

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

<<<FILE decisions/D-006-overlap-display-and-practice-room-manual.md
---
kind: decision
id: D-006
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-006: Enemies may overlap the player but are never hidden; the practice room is listed in the On screen section

## Decision

1. **Overlap (F1).** Enemies and the player still have no collision. A grub may end a lunge or recovery within the player's tile, and the player may walk or dash onto an enemy. In the player view no enemy is hidden under `P`: an enemy sharing the player's cell is drawn in the nearest free cell beside the player (display offset only). Timings, hit tests, damage and positions are unchanged. Order of preference: the side it last came from, then right, left, above, below.
2. **AC-15.** The body text is binding: `x` and the practice room must both be listed in `manual.md#on-screen`. AC-15 in `design/combat.md` now says so.

## Rationale

- Pillar 3 requires every threat to be visible before it hurts. The telegraph convention needs an on-map change, which is lost when the glyph hides under `P`.
- A display rule is cheap and does not touch the tuned grub cycle. Keeping them apart would need collision or pushing rules and would change timings and the dash-through behavior (the dash passes through enemies by design).
- Showing the glyph in all states, not only in the telegraph, also helps the Recovery counter window, the point of Option A.
- The player reads the manual's On screen section for what marks mean. A practice room that is not listed there is hard to find, and the body text is the more specific statement of intent.

## Alternatives considered

- **Forbid overlap (separation or collision):** rejected; it changes timing and positioning rules and conflicts with the dash passing through enemies.
- **Draw the enemy over `P` when committed:** rejected; the player would vanish from the map when it matters most.
- **Change the player glyph on overlap:** rejected; it hides the enemy's position and state.
- **Keep the AC wording as the binding text:** rejected; it leaves the practice room undocumented where players look.

## Revisit when

- A playtest shows the displaced glyph is misread as the enemy's true position.
- Option B or movement changes make overlap common enough to justify a collision rule.
>>>END

<<<FILE goals/G-001-combat-monotony/29-qa-to-studio.md
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
