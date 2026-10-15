# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/55-studio-to-qa.md
next_seq: 58
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/58-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/55-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 55
from: studio
to: qa
stage: Observe
outcome: routed
---
# 55: studio → qa — Check six open facts about the combat build and get bot reference data

## Task

Reproduce or settle the open facts below using `run_play`, `run_trace` and `run_bots`, and report each as it behaves in the build compared with `design/combat.md` and `manual.md`. Write a defect report with acceptance criteria for anything that contradicts the spec.

## Context

G-001 (combat feels monotonous). Two playtest sessions (room 1 in handoff 50; room 2 in 54) ended in quick defeats by scripted play, so the later combat has not been judged. Some of what the playtesters reported cannot be explained from the player view alone. Behavior that the spec does not cover is not a defect; report what happens so the designer can specify it.

## Findings

Facts to settle (the playtester's report, 54, is the previous Handoff):

1. **Possibly short bite warning.** In the room 2 session the run restarted in room 1 after defeat. The log showed "a grub rears back (left)" at 11.90 s and a heart lost at 11.97 s (30 fps), about 0.07 s later. Other bites came about 0.5–0.65 s after their "rears back" line. Use `run_trace` to tell whether any grub strikes sooner than the spec's wind-up allows, or whether the line belonged to a different grub. Repeat at 30 and 60 FPS.
2. **Dash distance.** How many tiles does a dash move in open floor, and next to a wall? A playtester judged it 2–3 tiles; the manual does not say. Compare with the spec.
3. **Facing.** Does a dash change the player's facing? After a dash, does a swipe hit enemies in the original facing, or the dash direction? (The spec may be silent; report what happens.)
4. **Swipe timing against grubs.** Does a swipe hit a grub that is (a) in Strike, (b) in Recovery while adjacent, (c) just after a first hit and knocked back? How many tiles does the knockback move it, and does the swipe print "(miss)" in the case where the grub is out of reach?
5. **Grub "on you".** When a grub shares the player's tile, does a swipe hit it regardless of facing? Report for each of the four facings.
6. **Bot reference data.** `run_bots` failed once with `script line 1: cannot read 'room 1'`: its script format differs from the play-script format. Find the right format (`repo/bots.py`, `repo/README.md`). Run a passive (idle) bot and, if available, a reactive bot on room 1, and on rooms 2–5 if possible. Report clear times, hearts lost and actions used, as numbers; do not judge balance.

## Decisions already made

- D-001: one attack button plus dash.
- D-003: zero hearts ends the run; a room clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.

## Constraints

- Everything must hold at both 30 and 60 FPS.
- Do not change the build. Report only.
- Run at most the rounds you need; say clearly which of the six items you could not settle.

## Open questions

- Which of the six facts contradict `design/combat.md` or `manual.md`, and which are simply unspecified?

## Expected output

A report in a Handoff addressed to `studio`, with: for each of the six items the observed behavior (with the script or trace you used), whether it matches the spec, and for each contradiction a defect with severity and acceptance criteria. Bot data as a table.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints, the build `repo/` (`repo/README.md`, `repo/bots.py`)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/54-playtester-to-studio.md
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS).
- `play.py`: runs an input script (`../manual.md`) and prints the player view or a trace.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger,reactive   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)

Each bot starts every room with full hearts and plays it on its own (no run flow).
"""

import math
import sys

from game import ATTACK_REACH, DIRECTIONS, HEARTS, ROOMS, Game


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
    """A shot that will reach the player within 0.7 s, if any."""
    for x, y, vx, vy in game.shots:
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


def camper(game):
    """Holds the starting spot: turns to the nearest enemy and swings when it is in reach."""
    enemy = _nearest(game)
    if enemy:
        _face_and_swing(game, enemy)


def walker(game):
    """Lets a nearby enemy come and swings, walks up to one further away, steps aside from shots."""
    enemy = _nearest(game)
    if not enemy:
        return
    shot = _incoming(game)
    distance = math.hypot(enemy.x - game.x, enemy.y - game.y)
    coming = enemy.kind == "grub" and distance < 2.5
    if shot:
        game.press("move", _sidestep(game, shot))
    elif distance > 1.1 and not coming:
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        _face_and_swing(game, enemy)


def dodger(game):
    """Plays like the walker, but dashes aside from incoming shots and away from two close enemies."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    shot = _incoming(game)
    close = [e for e in game.enemies if e.hp > 0 and math.hypot(e.x - game.x, e.y - game.y) < 1.3]
    if ready and shot:
        game.press("dash", _sidestep(game, shot))
    elif ready and len(close) >= 2:
        game.press("dash", _toward(game.x - close[0].x, game.y - close[0].y))
    else:
        walker(game)


def reactive(game):
    """Plays like the dodger, but also dashes away from a grub that is winding up nearby."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    winding = [
        e
        for e in game.enemies
        if e.hp > 0 and e.kind == "grub" and e.state == "windup"
        and math.hypot(e.x - game.x, e.y - game.y) < 2.0
    ]
    if ready and winding:
        e = min(winding, key=lambda g: math.hypot(g.x - game.x, g.y - game.y))
        game.press("dash", _toward(game.x - e.x, game.y - e.y))
    else:
        dodger(game)


BOTS = {"camper": camper, "walker": walker, "dodger": dodger, "reactive": reactive}


def play_room(bot, room, fps, limit):
    game = Game(fps=fps, room=room)
    while game.t < limit - 1e-9 and not game.cleared and game.hearts > 0:
        if game.stun_left <= 0:
            bot(game)
        game.step()
    counts = {}
    sources = {}
    for _, kind, details in game.events:
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "hurt":
            sources[details["source"]] = sources.get(details["source"], 0) + 1
    return {
        "cleared": game.cleared,
        "seconds": round(game.t, 2),
        "hearts_lost": counts.get("hurt", 0),
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
    }


def read_script(text):
    setup = {"bots": list(BOTS), "rooms": [r for r in ROOMS if r != "empty"], "fps": 60, "limit": 60.0}
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
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}")
    return setup


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {HEARTS} hearts each")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"])
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:8} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}"
            )
            total["cleared"] += r["cleared"]
            total["hearts_lost"] += r["hearts_lost"]
            total["dashes"] += r["dashes"]
        print(
            f"{name:8} total: cleared {total['cleared']}/{len(setup['rooms'])}, hearts lost "
            f"{total['hearts_lost']}, dashes {total['dashes']}"
        )


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

<<<FILE goals/G-001-combat-monotony/54-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 54
from: playtester
to: studio
stage: Play
outcome: done
---
# 54: playtester → studio — Observation report: room 2 by script, little else reached

## Task

Report what a first-time player experienced in the later rooms and with enemies other than the first room's grub, paying attention to combat.

## Context

Handoff 52 asked for a play session over the unseen parts of the game. I played by input script only (`python3 play.py --view player {script}`, using only the manual). Live play was not available. I used one scripted run. It was a blind script, so I could not react to the screen mid-run. The result is thin, and I say below what I did not see.

## Findings

### Method

- One scripted run: `room 2`, 30 fps, 20 s. The script was a swipe at 1 s, move right at 3 s, stop at 5 s, swipe at 5.5 s, dash left at 8 s, swipe at 10 s.
- I chose the moves in advance from the manual, so nothing was adjusted to what was on screen.
- I did not use the remaining run rounds. This report rests on that single run.

### What I saw and did not see

- **Seen:** the opening of room 2. It had four grubs, all `g`, placed around the edges. They drifted toward me from all sides and ended up around my tile.
- **Seen by accident:** room 1 again. My swipe at 10 s came after I went down, and "press attack to start again" restarted the run in room 1. It had three grubs. I did nothing there but stand still, and I went down at 14.97 s.
- **Not seen:**
  - rooms 3, 4 and 5 (I never cleared a room, "rooms cleared: 0" both times);
  - any spitter, so no `S`/`Z` charge, no `*` shot, and no "staggered";
  - a "room cleared" heal;
  - "run complete".
- **Never exercised:** the dash. It fired at 8 s, after I was already down, so I learned nothing about how it feels. I have no opinion on dash timing or recharge.
- **Reached with the manual's means:** `room 3`–`room 5` can be selected by script. I did not try them. I should have, since that is the direct way to see the later rooms and any spitters. This is the main gap in my report.

### Concrete moments (room 2, standing mostly still)

- 0–2.5 s: four grubs walked in from the corners and edges. Nothing was dangerous, and it was calm and readable. My early swipe at 1.0 s hit nothing ("(miss)") because everything was far away. That is my script's fault, not the game's.
- 2.73 s: "a grub rears back (left)", and the `G` showed up top-left of me. At 3.0 s a second one reared back on the right. Two threats were on screen within about 0.3 s of each other. The text cue and the capital `G` were easy to read.
- 3.38 s: "the grub is open (left)". I was not swiping then, so I missed the chance to counter.
- 3.57 s: first hit, 3/3 → 2/3. The attacker was a grub that had reared back about half a second earlier. I could have dodged, but my script could not react.
- 4.0–5.2 s: grubs sat directly left and right of me, taking turns biting. The log shows "open" and "rears back" calls every few tenths of a second. It felt like I was standing in a ring of grubs with no gap to leave through.
- 5.07 s: hit, 2/3 → 1/3.
- 5.5 s: my swipe hit one grub ("grub hit (1 left)"). A grub is therefore a two-hit enemy, and my swipe landed on only one of the three adjacent grubs.
- 5.87 s: hit again and down. Three hits, about 2.3 s after the first bite began, and no room cleared.
- Room 1 repeat, 11.4–14.97 s: the same pattern with three grubs. I was hit at 11.97 s, 13.47 s and 14.97 s and went down. In both runs I died without clearing anything, but I also did not try to play it.

### Did the fights feel different from each other?

Room 1 and room 2 fought the same way: grubs close in, rear back, bite and open up. Room 2 simply had one more grub. I cannot say anything about rooms 3–5 or other enemy types.

### Did my choices matter?

I can't judge this fairly, because I never reacted. Visible signs that they could matter:

- Each bite is announced by a "rears back" line, a capital `G`, and a delay of roughly half a second before the hit. That is enough time to dash or step away.
- A grub is "open" after biting, which invites a counter-swipe.

Signs that choices could matter less than they should:

- Several grubs arrive together and cycle their bites, so there always seems to be one about to bite. It felt like an "avoid the next bite" loop rather than a back-and-forth.
- The swipe only reaches a little more than one tile. With grubs on both sides, one swipe hit one grub.

### Unclear, unreadable or possibly unfair

- **Possibly short warning (medium, uncertain):** at 11.90 s the log shows "a grub rears back (left)" and the hit at 11.97 s. That is only about 0.07 s later. The other bites I could trace came about 0.5–0.65 s after their rear-back line. I can't tell if this was a different grub's earlier wind-up whose line I misattributed, or a real short warning. If real, it would be impossible to react to and would feel unfair.
- **Grubs on my tile (low–medium):** several lines read "the grub is open (on you)" or "rears back (on you)". Grubs seem to be able to stack on my tile. The screen then draws them beside me, so I could not tell which side the bite would come from, or where to swing. For an action player who relies on spacing, that is confusing.
- **Cornered (medium):** with grubs on both sides I was boxed in. I couldn't tell whether I could have walked out, since I did not try.

### Broken

Nothing was clearly broken in what I saw. The 11.97 s hit timing above is the one thing worth a second look.

### Positives

- The text cues ("rears back (left)", "the grub is open") and the capital/lowercase marks made it easy to follow what each grub was doing.
- The restart flow worked: after "run over", attack began a fresh run in room 1 with full hearts.
- Runs are short. I went down in about 6 s in room 2 and about 5 s in room 1, which suits a player who wants short, intense runs.

### Open player questions

- How are the later rooms different? Do they have spitters, and how many grubs?
- Can I dash out of the ring of grubs and counter from outside? I never tested it.
- Is the very short warning at 11.9 s real?

## Decisions already made

None.

## Constraints

I used only the player view and the manual. I read no source, tests or design files, and did not use the trace view or the bots.

## Open questions

- Please route a follow-up session that plays `room 3`, `room 4` and `room 5` directly, ideally live or with several short reactive scripts. It should dash and counter-swipe on the "rears back" cues, and it should place spitters with `room empty` if they are not in the early rooms. This report does not cover later rooms, spitters or the dash.

## Expected output

This report goes to `studio`, which decides whether to route a follow-up play session and whether to pass the experience issues to `game-designer` and the possibly short bite warning to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-playtester.md
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
### Round 1: @run/trace/grub-room1-idle-30 — `python3 play.py --view trace {script}`

Script:

```text
room 1
fps 30
end 16
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=1 dt=0.03333
t=0.000 frame=0 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.00,4.00,hp=2,approach,0.000) grub#1(15.00,4.00,hp=2,approach,0.000) grub#2(8.00,0.00,hp=2,approach,0.000) | setup
t=1.400 frame=42 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(5.80,4.00,hp=2,approach,0.000) grub#1(12.20,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=1.900 frame=57 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.500) grub#1(11.20,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,strike,0.150) | strike {'who': 2}; windup {'who': 0, 'side': 'left'}
t=1.967 frame=59 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.433) grub#1(11.07,4.00,hp=2,approach,0.000) grub#2(8.00,3.19,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.333) grub#1(10.87,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 2, 'side': 'above'}
t=2.400 frame=72 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,strike,0.150) grub#1(10.20,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.550) | strike {'who': 0}
t=2.567 frame=77 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.883) grub#1(9.87,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.383) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=2.767 frame=83 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.683) grub#1(9.47,4.00,hp=2,approach,0.000) grub#2(8.00,3.75,hp=2,recovery,0.183) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.900 frame=87 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.550) grub#1(9.25,4.00,hp=2,windup,0.500) grub#2(8.00,3.75,hp=2,recovery,0.050) | windup {'who': 1, 'side': 'right'}
t=2.967 frame=89 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.483) grub#1(9.25,4.00,hp=2,windup,0.433) grub#2(8.00,3.75,hp=2,windup,0.483) | windup {'who': 2, 'side': 'above'}
t=3.400 frame=102 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.050) grub#1(9.25,4.00,hp=2,strike,0.150) grub#2(8.00,3.75,hp=2,windup,0.050) | strike {'who': 1}
t=3.467 frame=104 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(8.81,4.00,hp=2,strike,0.083) grub#2(8.00,3.78,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}; strike {'who': 2}
t=3.567 frame=107 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(7.75,4.00,hp=2,windup,0.500) grub#1(8.25,4.00,hp=2,recovery,0.883) grub#2(8.00,3.94,hp=2,strike,0.033) | recover {'cause': 'strike', 'who': 1, 'side': 'right'}; windup {'who': 0, 'side': 'left'}
t=3.600 frame=108 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(7.75,4.00,hp=2,windup,0.467) grub#1(8.25,4.00,hp=2,recovery,0.850) grub#2(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 2, 'side': 'on you'}
t=4.067 frame=122 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,strike,0.150) grub#1(8.25,4.00,hp=2,recovery,0.383) grub#2(8.00,4.00,hp=2,recovery,0.433) | strike {'who': 0}
t=4.233 frame=127 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.883) grub#1(8.25,4.00,hp=2,recovery,0.217) grub#2(8.00,4.00,hp=2,recovery,0.267) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=4.267 frame=128 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.850) grub#1(8.25,4.00,hp=2,recovery,0.183) grub#2(8.00,4.00,hp=2,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.467 frame=134 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.650) grub#1(8.25,4.00,hp=2,windup,0.483) grub#2(8.00,4.00,hp=2,recovery,0.033) | windup {'who': 1, 'side': 'right'}
t=4.500 frame=135 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.617) grub#1(8.25,4.00,hp=2,windup,0.450) grub#2(8.00,4.00,hp=2,windup,0.500) | windup {'who': 2, 'side': 'on you'}
t=4.967 frame=149 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | strike {'who': 1}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.767 frame=173 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.967 frame=209 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=6.967 frame=209 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | end
```

### Round 1: @run/trace/grub-room1-idle-60 — `python3 play.py --view trace {script}`

Script:

```text
room 1
fps 60
end 16
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
t=6.950 frame=417 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.22,4.00,hp=2,approach,0.000) grub#2(8.00,4.00,hp=2,approach,0.000) | end
```

### Round 1: @run/trace/dash-open-and-wall — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
end 8
1 dash right
2 dash left
3 dash left
4 dash left
5 dash up
6 dash up
7 dash up
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | setup
t=1.017 frame=61 room=empty phase=playing pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=1.250 frame=75 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.017 frame=121 room=empty phase=playing pos=(11.73,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=2.250 frame=135 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.017 frame=181 room=empty phase=playing pos=(7.73,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=3.250 frame=195 room=empty phase=playing pos=(4.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=4.017 frame=241 room=empty phase=playing pos=(3.73,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=4.250 frame=255 room=empty phase=playing pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=5.017 frame=301 room=empty phase=playing pos=(0.00,3.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=5.250 frame=315 room=empty phase=playing pos=(0.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=6.017 frame=361 room=empty phase=playing pos=(0.00,0.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=6.250 frame=375 room=empty phase=playing pos=(0.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=7.017 frame=421 room=empty phase=playing pos=(0.00,0.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=7.250 frame=435 room=empty phase=playing pos=(0.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=8.000 frame=480 room=empty phase=playing pos=(0.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | end
```

### Round 1: @run/bots/ref60 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger,reactive
rooms 1-5
fps 60
limit 60
```

Exit: 0 (0.1 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
camper   room 2: cleared in 4.8 s; hearts lost 0 (hit by: none); attacks 7, dashes 0
camper   room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper   room 4: NOT cleared (6.9 s); hearts lost 3 (hit by: shot 3); attacks 4, dashes 0
camper   room 5: NOT cleared (6.9 s); hearts lost 3 (hit by: shot 3); attacks 6, dashes 0
camper   total: cleared 2/5, hearts lost 9, dashes 0
walker   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   room 2: cleared in 5.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
walker   room 3: cleared in 9.0 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   room 4: cleared in 9.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
walker   room 5: cleared in 11.2 s; hearts lost 0 (hit by: none); attacks 10, dashes 0
walker   total: cleared 5/5, hearts lost 0, dashes 0
dodger   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
dodger   room 2: cleared in 5.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
dodger   room 3: cleared in 11.8 s; hearts lost 0 (hit by: none); attacks 6, dashes 4
dodger   room 4: cleared in 10.0 s; hearts lost 0 (hit by: none); attacks 8, dashes 1
dodger   room 5: cleared in 9.8 s; hearts lost 0 (hit by: none); attacks 10, dashes 2
dodger   total: cleared 5/5, hearts lost 0, dashes 7
reactive room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
reactive room 2: cleared in 6.3 s; hearts lost 1 (hit by: grub 1); attacks 8, dashes 3
reactive room 3: cleared in 11.8 s; hearts lost 0 (hit by: none); attacks 6, dashes 4
reactive room 4: cleared in 12.9 s; hearts lost 0 (hit by: none); attacks 9, dashes 5
reactive room 5: cleared in 11.1 s; hearts lost 0 (hit by: none); attacks 11, dashes 2
reactive total: cleared 5/5, hearts lost 1, dashes 14
```

### Round 1: @run/play/dash-wall-view — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 14 4
end 4
1 dash right
2 dash right
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
   |              P |
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
   |              P |
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
   |              P |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  you dash right
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
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
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.000  you dash right
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
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
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 4.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/trace/dash30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
player 8 4
end 7
1 dash right
2 dash right
3 dash left
3.3 dash left
4 dash down
5 dash down
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | setup
t=1.033 frame=31 room=empty phase=playing pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=1.267 frame=38 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.033 frame=61 room=empty phase=playing pos=(12.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=2.267 frame=68 room=empty phase=playing pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.033 frame=91 room=empty phase=playing pos=(14.47,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=3.267 frame=98 room=empty phase=playing pos=(11.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.333 frame=100 room=empty phase=playing pos=(11.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=4.033 frame=121 room=empty phase=playing pos=(11.00,4.53) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=4.267 frame=128 room=empty phase=playing pos=(11.00,8.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=5.033 frame=151 room=empty phase=playing pos=(11.00,8.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=5.267 frame=158 room=empty phase=playing pos=(11.00,8.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=7.000 frame=210 room=empty phase=playing pos=(11.00,8.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | end
```

### Round 2: @run/play/facing-default — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn spitter 7.2 4
spawn spitter 8.8 4
end 0.8
0.1 attack
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
   |       sPs      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.100  you swipe: spitter hit (1 left)
   [0.12 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |       sPz      |
   |         )      |
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
   |       sPz      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 0.80 s: hearts 3/3, enemies left 2
```

### Round 2: @run/play/facing-dash60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn spitter 11 4
spawn spitter 13 4
end 1
0.1 move left
0.15 stop
0.3 dash right
0.8 attack
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
   |        P  s s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.300  you dash right
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           Pss  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  you swipe: spitter hit (1 left)
   [0.82 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           sPz  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter 1 (right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           SPz  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 2
```

### Round 2: @run/play/facing-dash30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn spitter 11 4
spawn spitter 13 4
end 1
0.1 move left
0.15 stop
0.3 dash right
0.8 attack
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
   |        P  s s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.300  you dash right
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           Pss  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  you swipe: spitter hit (1 left)
   [0.83 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           sPz  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter 1 (right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           SPz  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 2
```

### Round 2: @run/play/onyou-right — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 15 4
spawn grub 15 4
end 1
0.01 move right
0.2 attack
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
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
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
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (on you)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
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
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 1
```

### Round 2: @run/play/onyou-left — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 0 4
spawn grub 0 4
end 1
0.01 move left
0.2 attack
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
   |Pg              |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |PG              |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |Pw              |
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
   |Pw              |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (on you)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |PW              |
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
   |PW              |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 1
```

### Round 2: @run/play/onyou-up — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 0
spawn grub 8 0
end 1
0.01 move up
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
   +----------------+
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
   +----------------+
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (on you)
   [0.80 s] hearts 3/3
   +----------------+
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 1
```

### Round 2: @run/play/onyou-down — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 8
spawn grub 8 8
end 1
0.01 move down
0.2 attack
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
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   +----------------+
  0.800  a grub rears back (on you)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 1
```

### Round 2: @run/trace/strike-a — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 9.24 4
end 1.5
0.0 move right
0.02 stop
0.51 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.07,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.13,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(9.13,4.00,hp=1,strike,0.133) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=0.667 frame=40 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.24,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=1.333 frame=80 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.24,4.00,hp=1,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.500 frame=90 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.24,4.00,hp=1,recovery,0.067) | end
```

### Round 2: @run/trace/strike-b — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 9.24 4
end 1.5
0.0 move right
0.02 stop
0.54 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.07,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.13,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(9.13,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=0.567 frame=34 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.267 shots=0 | grub#0(8.91,4.00,hp=2,strike,0.100) | ignored {'action': 'attack', 'reason': 'stunned'}
t=0.667 frame=40 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.24,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=1.333 frame=80 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.24,4.00,hp=2,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.500 frame=90 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.24,4.00,hp=2,recovery,0.067) | end
```

### Round 2: @run/trace/recovery-knock — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 9.24 4
end 3
0.0 move right
0.02 stop
1.0 attack
1.4 attack
1.8 attack
2.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.07,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.13,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(9.13,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=0.667 frame=40 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.24,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=1.017 frame=61 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.317 stun_left=0.000 shots=0 | grub#0(8.32,4.00,hp=1,recovery,0.550) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
t=1.333 frame=80 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.24,4.00,hp=1,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.417 frame=85 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | attack {'facing': 'right', 'hits': [('grub', 'defeated', 0, 0)]}; cleared {'room': 'empty'}
t=1.817 frame=109 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | attack {'facing': 'right', 'hits': []}
t=2.217 frame=133 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | attack {'facing': 'right', 'hits': []}
t=3.000 frame=180 room=empty phase=playing pos=(8.13,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | end
```

### Round 2: @run/trace/idle-room2-60 — `python3 play.py --view trace {script}`

Script:

```text
room 2
fps 60
end 10
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=2 dt=0.01667
t=0.000 frame=0 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.00,1.00,hp=2,approach,0.000) grub#1(15.00,7.00,hp=2,approach,0.000) grub#2(14.00,0.00,hp=2,approach,0.000) grub#3(1.00,8.00,hp=2,approach,0.000) | setup
t=2.733 frame=164 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,windup,0.500) grub#1(9.98,4.85,hp=2,approach,0.000) grub#2(9.45,3.03,hp=2,approach,0.000) grub#3(5.75,5.29,hp=2,approach,0.000) | windup {'who': 0, 'side': 'left'}
t=2.983 frame=179 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,windup,0.250) grub#1(9.52,4.65,hp=2,approach,0.000) grub#2(9.04,3.31,hp=2,windup,0.500) grub#3(6.18,5.04,hp=2,approach,0.000) | windup {'who': 2, 'side': 'right'}
t=3.233 frame=194 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,strike,0.150) grub#1(9.15,4.49,hp=2,approach,0.000) grub#2(9.04,3.31,hp=2,windup,0.250) grub#3(6.61,4.79,hp=2,approach,0.000) | strike {'who': 0}
t=3.283 frame=197 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.18,3.59,hp=2,strike,0.100) grub#1(9.15,4.49,hp=2,approach,0.000) grub#2(9.04,3.31,hp=2,windup,0.200) grub#3(6.70,4.74,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.383 frame=203 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.900) grub#1(9.15,4.49,hp=2,windup,0.500) grub#2(9.04,3.31,hp=2,windup,0.100) grub#3(6.88,4.64,hp=2,approach,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}; windup {'who': 1, 'side': 'right'}
t=3.483 frame=209 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.600 stun_left=0.100 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.800) grub#1(9.15,4.49,hp=2,windup,0.400) grub#2(9.04,3.31,hp=2,strike,0.150) grub#3(6.91,4.62,hp=2,approach,0.000) | strike {'who': 2}
t=3.633 frame=218 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.450 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.650) grub#1(9.15,4.49,hp=2,windup,0.250) grub#2(8.21,3.86,hp=2,recovery,0.900) grub#3(6.91,4.62,hp=2,windup,0.500) | recover {'cause': 'strike', 'who': 2, 'side': 'right'}; windup {'who': 3, 'side': 'left'}
t=3.883 frame=233 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.400) grub#1(9.15,4.49,hp=2,strike,0.150) grub#2(8.21,3.86,hp=2,recovery,0.650) grub#3(6.91,4.62,hp=2,windup,0.250) | strike {'who': 1}
t=4.033 frame=242 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.050 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.250) grub#1(8.23,4.10,hp=2,recovery,0.900) grub#2(8.21,3.86,hp=2,recovery,0.500) grub#3(6.91,4.62,hp=2,windup,0.100) | recover {'cause': 'strike', 'who': 1, 'side': 'right'}
t=4.083 frame=245 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.200) grub#1(8.23,4.10,hp=2,recovery,0.850) grub#2(8.21,3.86,hp=2,recovery,0.450) grub#3(6.91,4.62,hp=2,windup,0.050) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.133 frame=248 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.150) grub#1(8.23,4.10,hp=2,recovery,0.800) grub#2(8.21,3.86,hp=2,recovery,0.400) grub#3(6.91,4.62,hp=2,strike,0.150) | strike {'who': 3}
t=4.183 frame=251 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.100) grub#1(8.23,4.10,hp=2,recovery,0.750) grub#2(8.21,3.86,hp=2,recovery,0.350) grub#3(7.20,4.45,hp=2,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.283 frame=257 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.500) grub#1(8.23,4.10,hp=2,recovery,0.650) grub#2(8.21,3.86,hp=2,recovery,0.250) grub#3(7.78,4.12,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 3, 'side': 'left'}; windup {'who': 0, 'side': 'left'}
t=4.533 frame=272 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.450 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.250) grub#1(8.23,4.10,hp=2,recovery,0.400) grub#2(8.21,3.86,hp=2,windup,0.500) grub#3(7.78,4.12,hp=2,recovery,0.650) | windup {'who': 2, 'side': 'right'}
t=4.783 frame=287 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,strike,0.150) grub#1(8.23,4.10,hp=2,recovery,0.150) grub#2(8.21,3.86,hp=2,windup,0.250) grub#3(7.78,4.12,hp=2,recovery,0.400) | strike {'who': 0}
t=4.933 frame=296 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.050 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) grub#1(8.23,4.10,hp=2,windup,0.500) grub#2(8.21,3.86,hp=2,windup,0.100) grub#3(7.78,4.12,hp=2,recovery,0.250) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}; windup {'who': 1, 'side': 'right'}
t=4.983 frame=299 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.850) grub#1(8.23,4.10,hp=2,windup,0.450) grub#2(8.21,3.86,hp=2,windup,0.050) grub#3(7.78,4.12,hp=2,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.033 frame=302 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.800) grub#1(8.23,4.10,hp=2,windup,0.400) grub#2(8.21,3.86,hp=2,strike,0.150) grub#3(7.78,4.12,hp=2,recovery,0.150) | strike {'who': 2}
t=5.050 frame=303 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.23,4.10,hp=2,approach,0.000) grub#2(8.18,3.88,hp=2,approach,0.000) grub#3(7.78,4.12,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.850 frame=351 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.23,4.10,hp=2,approach,0.000) grub#2(8.18,3.88,hp=2,approach,0.000) grub#3(7.78,4.12,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.050 frame=423 room=2 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.23,4.10,hp=2,approach,0.000) grub#2(8.18,3.88,hp=2,approach,0.000) grub#3(7.78,4.12,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=7.050 frame=423 room=2 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) grub#1(8.23,4.10,hp=2,approach,0.000) grub#2(8.18,3.88,hp=2,approach,0.000) grub#3(7.78,4.12,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/idle-room3-60 — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 60
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=3 dt=0.01667
t=0.000 frame=0 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,idle,1.000) spitter#1(14.00,7.00,hp=2,idle,1.800) spitter#2(2.00,7.00,hp=2,idle,2.600) | setup
t=1.000 frame=60 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,charge,0.800) spitter#1(14.00,7.00,hp=2,idle,0.800) spitter#2(2.00,7.00,hp=2,idle,1.600) | charge {'who': 0, 'spot': 'top left', 'dup': False, 'n': 1}
t=1.800 frame=108 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | spitter#0(2.00,1.00,hp=2,recovery,0.600) spitter#1(14.00,7.00,hp=2,charge,0.800) spitter#2(2.00,7.00,hp=2,idle,0.800) | spit {'who': 0, 'spot': 'top left', 'dup': False, 'n': 1}; charge {'who': 1, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.600 frame=156 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | spitter#0(2.00,1.00,hp=2,idle,0.900) spitter#1(14.00,7.00,hp=2,recovery,0.600) spitter#2(2.00,7.00,hp=2,charge,0.800) | spit {'who': 1, 'spot': 'bottom right', 'dup': False, 'n': 2}; charge {'who': 2, 'spot': 'bottom left', 'dup': False, 'n': 3}
t=3.400 frame=204 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=3 | spitter#0(2.00,1.00,hp=2,idle,0.100) spitter#1(14.00,7.00,hp=2,idle,0.900) spitter#2(2.00,7.00,hp=2,recovery,0.600) | spit {'who': 2, 'spot': 'bottom left', 'dup': False, 'n': 3}
t=3.500 frame=210 room=3 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=3 | spitter#0(2.00,1.00,hp=2,charge,0.800) spitter#1(14.00,7.00,hp=2,idle,0.800) spitter#2(2.00,7.00,hp=2,recovery,0.500) | charge {'who': 0, 'spot': 'top left', 'dup': False, 'n': 1}
t=3.917 frame=235 room=3 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=2 | spitter#0(2.00,1.00,hp=2,charge,0.383) spitter#1(14.00,7.00,hp=2,idle,0.383) spitter#2(2.00,7.00,hp=2,recovery,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.300 frame=258 room=3 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.417 stun_left=0.000 shots=3 | spitter#0(2.00,1.00,hp=2,recovery,0.600) spitter#1(14.00,7.00,hp=2,charge,0.800) spitter#2(2.00,7.00,hp=2,idle,0.800) | spit {'who': 0, 'spot': 'top left', 'dup': False, 'n': 1}; charge {'who': 1, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=4.717 frame=283 room=3 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=2 | spitter#0(2.00,1.00,hp=2,recovery,0.183) spitter#1(14.00,7.00,hp=2,charge,0.383) spitter#2(2.00,7.00,hp=2,idle,0.383) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=5.100 frame=306 room=3 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.417 stun_left=0.000 shots=3 | spitter#0(2.00,1.00,hp=2,idle,0.900) spitter#1(14.00,7.00,hp=2,recovery,0.600) spitter#2(2.00,7.00,hp=2,charge,0.800) | spit {'who': 1, 'spot': 'bottom right', 'dup': False, 'n': 2}; charge {'who': 2, 'spot': 'bottom left', 'dup': False, 'n': 3}
t=5.517 frame=331 room=3 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | spitter#0(2.00,1.00,hp=2,idle,0.000) spitter#1(14.00,7.00,hp=2,idle,0.000) spitter#2(2.00,7.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0}; down
t=6.317 frame=379 room=3 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,idle,0.000) spitter#1(14.00,7.00,hp=2,idle,0.000) spitter#2(2.00,7.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.517 frame=451 room=3 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,idle,0.000) spitter#1(14.00,7.00,hp=2,idle,0.000) spitter#2(2.00,7.00,hp=2,idle,0.000) | run_over {'rooms': 0, 'complete': False}
t=7.517 frame=451 room=3 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | spitter#0(2.00,1.00,hp=2,idle,0.000) spitter#1(14.00,7.00,hp=2,idle,0.000) spitter#2(2.00,7.00,hp=2,idle,0.000) | end
```

### Round 2: @run/trace/idle-room4-60 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 60
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=4 dt=0.01667
t=0.000 frame=0 room=4 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.00,4.00,hp=2,approach,0.000) grub#1(0.00,1.00,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,1.000) spitter#3(15.00,8.00,hp=2,idle,1.800) | setup
t=1.000 frame=60 room=4 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.00,4.00,hp=2,approach,0.000) grub#1(1.87,1.70,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,charge,0.800) spitter#3(15.00,8.00,hp=2,idle,0.800) | charge {'who': 2, 'spot': 'top right', 'dup': False, 'n': 1}
t=1.800 frame=108 room=4 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(4.60,4.00,hp=2,approach,0.000) grub#1(3.37,2.26,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,recovery,0.600) spitter#3(15.00,8.00,hp=2,charge,0.800) | spit {'who': 2, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 3, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.600 frame=156 room=4 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.20,4.00,hp=2,approach,0.000) grub#1(4.87,2.83,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.900) spitter#3(15.00,8.00,hp=2,recovery,0.600) | spit {'who': 3, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.883 frame=173 room=4 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.75,4.00,hp=2,windup,0.500) grub#1(5.40,3.02,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.617) spitter#3(15.00,8.00,hp=2,recovery,0.317) | windup {'who': 0, 'side': 'left'}
t=3.383 frame=203 room=4 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.75,4.00,hp=2,strike,0.150) grub#1(6.34,3.38,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.117) spitter#3(15.00,8.00,hp=2,idle,0.917) | strike {'who': 0}
t=3.433 frame=206 room=4 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=2 | grub#0(7.08,4.00,hp=2,strike,0.100) grub#1(6.43,3.41,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.067) spitter#3(15.00,8.00,hp=2,idle,0.867) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.500 frame=210 room=4 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 shots=2 | grub#0(7.53,4.00,hp=2,strike,0.033) grub#1(6.55,3.46,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,charge,0.800) spitter#3(15.00,8.00,hp=2,idle,0.800) | charge {'who': 2, 'spot': 'top right', 'dup': False, 'n': 1}
t=3.533 frame=212 room=4 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=2 | grub#0(7.75,4.00,hp=2,recovery,0.900) grub#1(6.62,3.48,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,charge,0.767) spitter#3(15.00,8.00,hp=2,idle,0.767) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=3.650 frame=219 room=4 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.583 stun_left=0.083 shots=2 | grub#0(7.75,4.00,hp=2,recovery,0.783) grub#1(6.83,3.56,hp=2,windup,0.500) spitter#2(15.00,0.00,hp=2,charge,0.650) spitter#3(15.00,8.00,hp=2,idle,0.650) | windup {'who': 1, 'side': 'left'}
t=4.150 frame=249 room=4 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.083 stun_left=0.000 shots=2 | grub#0(7.75,4.00,hp=2,recovery,0.283) grub#1(6.83,3.56,hp=2,strike,0.150) spitter#2(15.00,0.00,hp=2,charge,0.150) spitter#3(15.00,8.00,hp=2,idle,0.150) | strike {'who': 1}
t=4.233 frame=254 room=4 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=2 | grub#0(7.75,4.00,hp=2,recovery,0.200) grub#1(7.35,3.76,hp=2,strike,0.067) spitter#2(15.00,0.00,hp=2,charge,0.067) spitter#3(15.00,8.00,hp=2,idle,0.067) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.300 frame=258 room=4 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 shots=3 | grub#0(7.75,4.00,hp=2,recovery,0.133) grub#1(7.77,3.91,hp=2,recovery,0.900) spitter#2(15.00,0.00,hp=2,recovery,0.600) spitter#3(15.00,8.00,hp=2,charge,0.800) | spit {'who': 2, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 3, 'spot': 'bottom right', 'dup': False, 'n': 2}; recover {'cause': 'strike', 'who': 1, 'side': 'left'}
t=4.433 frame=266 room=4 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.600 stun_left=0.100 shots=3 | grub#0(7.75,4.00,hp=2,windup,0.500) grub#1(7.77,3.91,hp=2,recovery,0.767) spitter#2(15.00,0.00,hp=2,recovery,0.467) spitter#3(15.00,8.00,hp=2,charge,0.667) | windup {'who': 0, 'side': 'left'}
t=4.933 frame=296 room=4 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.100 stun_left=0.000 shots=3 | grub#0(7.75,4.00,hp=2,strike,0.150) grub#1(7.77,3.91,hp=2,recovery,0.267) spitter#2(15.00,0.00,hp=2,idle,1.067) spitter#3(15.00,8.00,hp=2,charge,0.167) | strike {'who': 0}
t=5.033 frame=302 room=4 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(7.92,4.00,hp=2,approach,0.000) grub#1(7.77,3.91,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.000) spitter#3(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.833 frame=350 room=4 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.92,4.00,hp=2,approach,0.000) grub#1(7.77,3.91,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.000) spitter#3(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.033 frame=422 room=4 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.92,4.00,hp=2,approach,0.000) grub#1(7.77,3.91,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.000) spitter#3(15.00,8.00,hp=2,idle,0.000) | run_over {'rooms': 0, 'complete': False}
t=7.033 frame=422 room=4 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.92,4.00,hp=2,approach,0.000) grub#1(7.77,3.91,hp=2,approach,0.000) spitter#2(15.00,0.00,hp=2,idle,0.000) spitter#3(15.00,8.00,hp=2,idle,0.000) | end
```

### Round 2: @run/trace/idle-room5-60 — `python3 play.py --view trace {script}`

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

### Round 2: @run/bots/ref30 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger,reactive
rooms 1-5
fps 30
limit 60
```

Exit: 0 (0.1 s). Output:

```text
bots at 30 FPS, up to 60 s per room, 3 hearts each
camper   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
camper   room 2: cleared in 4.9 s; hearts lost 0 (hit by: none); attacks 7, dashes 0
camper   room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper   room 4: NOT cleared (6.9 s); hearts lost 3 (hit by: shot 3); attacks 4, dashes 0
camper   room 5: NOT cleared (6.9 s); hearts lost 3 (hit by: shot 3); attacks 6, dashes 0
camper   total: cleared 2/5, hearts lost 9, dashes 0
walker   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   room 2: cleared in 4.8 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
walker   room 3: cleared in 9.2 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   room 4: cleared in 9.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
walker   room 5: cleared in 12.3 s; hearts lost 0 (hit by: none); attacks 10, dashes 0
walker   total: cleared 5/5, hearts lost 0, dashes 0
dodger   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
dodger   room 2: cleared in 4.8 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
dodger   room 3: cleared in 9.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 2
dodger   room 4: cleared in 10.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 1
dodger   room 5: cleared in 14.5 s; hearts lost 0 (hit by: none); attacks 10, dashes 6
dodger   total: cleared 5/5, hearts lost 0, dashes 9
reactive room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
reactive room 2: cleared in 4.8 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
reactive room 3: cleared in 9.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 2
reactive room 4: cleared in 14.3 s; hearts lost 0 (hit by: none); attacks 8, dashes 6
reactive room 5: cleared in 11.1 s; hearts lost 0 (hit by: none); attacks 10, dashes 2
reactive total: cleared 5/5, hearts lost 0, dashes 10
```
>>>END
