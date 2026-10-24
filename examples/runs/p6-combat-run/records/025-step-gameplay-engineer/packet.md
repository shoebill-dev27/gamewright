# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/19-studio-to-gameplay-engineer.md
next_seq: 20
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/20-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-combat-monotony/19-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 19
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 19: studio → gameplay-engineer — finish Build: write `manual.md` (T8) and confirm `run_tests`

## Task

Write `manual.md` at the project root (T8). Use the draft in handoff 18, section "Draft `manual.md`", and place it unchanged unless a statement in it contradicts the built game. Then run `run_tests` against the real layout and confirm that all 34 tests pass, `ManualTest` included. `manual.md` is the only file to write for this step; no code changes are expected.

## Context

G-001, Build of Option A (build 0.5). Handoff 18 reports T1–T7 and T9 done in `repo/`. T8 was blocked because `manual.md` was not writable in that step. This step exists to do T8 only, and `manual.md` is in scope here. AC-15 and V-5 depend on the manual, and QA cannot start until it exists.

## Findings

From handoff 18, the facts this step relies on:

- 33 of 34 tests passed; the one error was `ManualTest`, caused by the missing `manual.md`.
- The draft was written to contain the backticked glyphs and key phrases `ManualTest` checks. It has not been run against the real file.
- The glyph table, line strings and as-built values are in handoff 18 and in `repo/play.py` (`GLYPHS`, `LINES`).

## Decisions already made

D-001…D-004 hold. The manual is player-facing: it must not name internal states, plan IDs (F1–F11) or acceptance-criterion numbers.

## Constraints

- Write only `manual.md`. If `ManualTest` fails against the draft, or a draft statement contradicts the built behavior, fix the wording in `manual.md` only. If the test or the game would have to change, stop and report it; do not change code in this step.
- Keep the script format and controls consistent with `repo/play.py`.

## Open questions

- If `manual.md` still cannot be written, say so as the first line of Findings and set `outcome: question`. Do not retry or work around it; the Studio will then escalate to the Owner, since a second hand-back for the same input is not routed to a Role again.

## Expected output

An outgoing Handoff addressed to `studio` (so the Route can compose a fresh Handoff for QA without the Sender assessment), with `outcome: done` and Findings giving:

1. confirmation that `manual.md` exists at the project root;
2. the `run_tests` result (count and any failures);
3. any wording you changed from the draft and why.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: manual.md (to create), design/combat-visuals.md, design/combat.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE manual.md
# Lantern Depths — how to play build 0.4

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face).

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

`P` you, `g` grub, `s` spitter, `*` projectile. Hearts are shown above the room.
>>>END

<<<FILE design/combat-visuals.md
# Combat visuals (build 0.5 target, Option A, G-001)

Status: visual spec and review rulings from the art-director for `design/combat.md`. It changes no rules, timings or parameters. Wherever it names a glyph or color, it covers what `combat.md` leaves to "chosen in Build". Build may change a glyph only if it keeps the rules in this file and documents the change in `manual.md`.

## Intent

The player must be able to tell, from one frame of `run_play` and its text lines, what can hurt them now, what is about to hurt them, and what is open to a counter. Pillar 3: every threat is visible before it can hurt.

## Principles

1. **Glyph first, color second.** The view is text, so every state difference must show in the character or in a text line. Color only reinforces it. Nothing may depend on color alone.
2. **Uppercase means danger.** An uppercase enemy glyph in saturated orange/red means it is committed to hurting the player (Wind-up, Charge, Strike). A lowercase glyph means it is harmless right now.
3. **Orange/red is reserved for threats.** Use it only for telegraphed enemy glyphs and projectiles. The player, the swipe arc and the downed marker never use it. The lantern's warm light and the cold blue-black are the rest of the palette.
4. **The view must catch short telegraphs.** The room is drawn every 0.5 s. The grub Wind-up is exactly 0.5 s, so a frame could fall just before it starts and just after it ends. Draw the room immediately on each of these events, as it already does after a hit:
   - grub Wind-up start
   - spitter Charge start
   - projectile spawn
   - every swipe, including a miss
   - grub Recovery start
   - player down
   These extra draws do not change timing. If Build cannot do this cheaply, report it as an open question to `game-designer`; do not lengthen the telegraphs.

## Glyph table (player view, one cell per tile)

| Thing | State | Glyph | Color | Notes |
|---|---|---|---|---|
| Player | normal | `P` | warm lantern yellow-white | Never orange/red. |
| Player | down | `x` | desaturated cold gray-blue | Replaces `P`. It reads as "out", not as a threat. |
| Grub | Approach / Recovery, full HP | `g` | muted, desaturated warm gray | Harmless. Muted on purpose so the alarming color is saved for the telegraph. |
| Grub | Wind-up / Strike, full HP | `G` | saturated orange/red | The 0.5 s cue. |
| Grub | harmless, damaged (1 HP) | `w` | muted, with a visible tint change from `g` | |
| Grub | Wind-up / Strike, damaged | `W` | saturated orange/red | |
| Spitter | Idle / Recovery / staggered, full HP | `s` | muted, desaturated warm gray | Harmless. |
| Spitter | Charge, full HP | `S` | saturated orange/red | Held for the whole 0.8 s. |
| Spitter | harmless, damaged | `z` | muted, tinted | |
| Spitter | Charge, damaged | `Z` | saturated orange/red | |
| Projectile | in flight | `*` | saturated orange/red, brightest on the map | Visible from spawn to removal. |
| Swipe arc | 0.15 s | `)` facing right, `(` left, `^` up, `v` down, drawn on the tiles in reach | lantern yellow-white | See "Swipe arc". |

Rules:
- Case is the harmless/danger signal and the letter family is the enemy type, so a player learns two things: `g/w` are grubs, `s/z` are spitters.
- A hit on a winding-up grub cancels the wind-up. The glyph must drop to lowercase `w` in the same draw as the hit line.
- A defeated enemy disappears in the draw that prints "defeated".

## Text lines (telegraph and feedback)

- Every telegraph prints a line at the moment the uppercase glyph appears. The line must say which enemy when more than one can act:
  - grub: "a grub rears back (left)" or "(above)", relative to the player. If two grubs wind up on the same draw, print two lines.
  - spitter: "spitter (top right) charges" and "spitter (bottom right) charges", as in the spec.
- Spit lines name the spitter ("spitter (top right) spits"). There are never two identical lines.
- Grub Recovery start prints "the grub is open". The 0.9 s counter window is the point of the rework, and in a still frame lowercase `g` looks the same as Approach.
- Hit lines follow the spec: "you swipe: grub hit (1 left)", "grub defeated", and the "(miss)", "(too soon)", "(stunned)", "(down)" reasons.
- Spitter stagger after a hit prints "spitter (top right) is staggered".

## Swipe arc

- It is drawn on every swipe, hit or miss, for the 0.15 s of the spec, plus the immediate draw required by principle 4. Without that draw a 0.15 s arc would almost never appear in a 0.5 s frame.
- It covers the tiles inside reach (1.5 tiles, 90° cone) in the facing direction.
- It is lantern-colored, never orange/red, so it is not confused with a threat.
- A miss shows the same arc with "(miss)", so the player sees how far the swipe reached.

## Run-over, down and clear

- **Down:** `x` in the cold gray-blue replaces `P`. The line "you went down" prints. Projectiles disappear in the same draw.
- **Run-over screen:** plain, with nothing else on the map. Lines: "run over — rooms cleared: N", then "press attack to start again". The second line tells the player the restart input and does not change the rule.
- **Room cleared:** "room cleared" prints, projectiles disappear in the same draw, and the hearts line updates. In a scripted session the heal must be visible in the hearts line.
- **Run complete** uses the same screen layout as run-over, with "run complete" instead.

## Visual acceptance criteria

- **V-1** In every draw after a Wind-up or Charge begins, the committed enemy is an uppercase glyph (`G`, `W`, `S`, `Z`). In every harmless state it is lowercase.
- **V-2** The Wind-up start, the Charge start and each swipe have their own draw at that moment, at both 30 and 60 FPS.
- **V-3** At least one draw shows the grub's uppercase glyph before the first heart is lost to it (supports AC-1).
- **V-4** A full-HP and a damaged enemy of the same type can be told apart by glyph in the same state (`g`/`w`, `G`/`W`, `s`/`z`, `S`/`Z`).
- **V-5** `x`, the arc characters and the glyph table are listed in `manual.md#on-screen`.
- **V-6** No color besides the telegraphed enemy glyphs and `*` is saturated orange/red.
- **V-7** The two spitters can be told apart on the screen: each has its own named charge line and its own position.
- **V-8** The run-over screen shows the restart prompt.

## Not checked

- Actual colors cannot be assessed from the text view. This spec fixes the intent and the glyph rules. A review of the built player view is still needed.
- Whether the player's hit-invulnerability (0.8 s) and dash invulnerability need a visible cue is left open. Suggestion: `p` (lowercase) for `P` during invulnerability. This needs no rule change, but it is optional and is not in the acceptance criteria.
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

<<<FILE decisions/D-004-option-a-single-change-set.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-004: Build Option A as one sequential change set on the existing simulation

## Decision

1. The Option A rework (spec `design/combat.md`, build 0.5) is built as one change set by one engineer, in the order T1–T9 of handoff 14. There are no isolated code workspaces and no parallel code branches.
2. Timers stay on elapsed seconds using the existing countdown-float pattern, with the leftover time carried across state transitions.
3. The Strike damage check uses the swept (closest-approach) distance over each tick's movement, not a sample at the end of the tick.
4. Player-visible strings and glyph/color choices live in two data tables (`LINES`, `GLYPHS`). Late input from steps 12 (QA defect log) and 13 (art-director review) then needs only a data edit.
5. `manual.md` is updated by the gameplay-engineer in the same change set, after the tables are frozen.

## Rationale

- The behavior sits in one module. The trace, the player view and the bots all depend on its event vocabulary, so parallel branches would conflict or be written against a moving contract.
- The change is small and tightly coupled.
- Elapsed-second timers with carry keep timestamp errors under one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS), which meets the spec's tolerance without per-frame-rate code.
- The swept check removes a source of 30/60 FPS differences for the fastest motion (the 0.15 s lunge, 0.22 tile per frame at 30 FPS). It also keeps the "at least 4 frames" Strike requirement testable.

## Alternatives considered

- **Parallel workspaces** (simulation / rendering and trace / tests and manual): rejected for the reasons above.
- **Frame-count timers:** rejected, because the project constraint is correct play at both 30 and 60 FPS.
- **Sampled strike check:** rejected. It can flip a hit between frame rates in borderline cases.
- **A separate manual-update step by another role:** rejected. The strings and glyphs are known only at the end of Build, and the engineer already holds them.

## Revisit when

- A later phase (Option B, new enemy types) adds independent code areas, such as new enemy modules that do not share the event vocabulary.
- Build finds the simple elapsed-second carry cannot meet AC-17's 0.07 s cross-fps bound. Then add sub-frame carry for distance-triggered events, which would change the timer design.
>>>END

<<<FILE goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 18: gameplay-engineer → studio — Option A build 0.5: code done, `manual.md` (T8) blocked by write permission

## Task

Route the open point below, then compose the verification Handoff for QA. T1–T7 and T9 are done in `repo/`. T8 (`manual.md`) is not written, because `manual.md` is not on this step's write list. The manual text is drafted below so another step can place it unchanged. Nothing should go to QA until `manual.md` exists, because AC-15 and V-5 depend on it and `ManualTest` fails without it.

## Context

G-001, handoff 17. The build under change is `repo/` at sha e54837757611 (0.4). It is now version 0.5. Spec: `design/combat.md`, `design/combat-visuals.md`, D-003, and plan defaults F1–F11 from handoff 14.

## Findings

### What changed and where

- `repo/game.py` (T1–T3):
  - Grub and spitter state machines on elapsed seconds with leftover carry.
  - Slot allocator, swept strike check, knockback.
  - 90° cone swipe, with the arc kept as state.
  - Charge cancel and stagger.
  - Spitter schedule from room start.
  - Down, clear, room load, run-over and restart flow.
  - Practice-room rules.
- `repo/play.py` (T4, T5):
  - Trace has `room=`, `phase=` and `shots=` on the state line, and per enemy `kind#index(x,y,hp,state,timer)`.
  - Player view has the `GLYPHS` and `LINES` tables and draws on the event list `SNAPSHOT_EVENTS`.
  - Optional `--color`, which is also on when stdout is a TTY.
- `repo/bots.py` (T6): `hearts_lost` counts `hurt` events; a `reactive` bot is added. Shot shape and `cleared` meaning are unchanged.
- `repo/tests/test_game.py` (T7): rewritten, 34 tests, covering AC-1…AC-17 per the plan, at both frame rates.

### How to exercise

- Practice-room scripts (`spawn grub 12 4`, `player 8 4`) with `run_trace` and `run_play`, at `fps 30` and `fps 60`.
- Rooms 3–5 for spit lines.
- `python3 bots.py` scripts at `fps 30` and `fps 60`.

### Acceptance criteria addressed

AC-1…AC-17 and V-1…V-4, V-6…V-8, per the tests. The spit-line defect (handoff 15, criteria 1–5) is covered by `test_charge_lines_and_spit_lines_name_the_spitter` and `test_two_spitters_in_one_spot_get_numbers`. V-5 and AC-15 wait on `manual.md`. V-6 (color) needs the art-director's review of the built view.

### As-built values (handoff 14 section 5)

- Swipe: reach 1.5 tiles. Cone: `along > 0` and `|across| <= along`, axis-aligned facing. An enemy on top of the player is hit.
- Projectile speed 3.0 tiles/s. Hit radius 0.4 (unchanged).
- Grub speed 2.0 (F1). A grub in Approach holds at 1.25 tiles from the player and waits for a slot (F2).
- Strike lunge: up to 1.0 tile in 0.15 s toward where the player stood when Wind-up ended.
- Strike hit: closest approach ≤ 1.0 tile over each tick's segment, once per Strike.
- Knockback 1.0 tile over 0.2 s, clamped to the room.
- Spitter Recovery 0.6 s, Stagger 1.0 s, Charge 0.8 s, interval 2.5 s, first charge at 1.0 + 0.8·k s.
- Grub Wind-up 0.5 s, Strike 0.15 s, Recovery 0.9 s, cancelled-windup Recovery 0.6 s.
- Heal +1 (max 3). Down delay 2.0 s. Clear delay 1.5 s.
- Slots: 2.

Glyph table (`GLYPHS` in `play.py`):

| Thing | Glyph | Color |
|---|---|---|
| Player | `P` | lantern yellow-white |
| Player down | `x` | gray-blue |
| Projectile | `*` | bold red |
| Arc right, left, up, down | `)` `(` `^` `v` | lantern |
| Grub harmless, full or damaged | `g`, `w` | muted gray, tinted |
| Grub Wind-up/Strike, full or damaged | `G`, `W` | bold orange |
| Spitter harmless, full or damaged | `s`, `z` | muted gray, tinted |
| Spitter Charge, full or damaged | `S`, `Z` | bold orange |

Strings (`LINES`):
- "a grub rears back ({side})", "the grub is open ({side})"
- "spitter[ N] ({spot}) charges", "…spits", "…is staggered"
- "you swipe: {kind} hit ({left} left)", "{kind} defeated", "you swipe: (miss)"
- "you swipe: (too soon|stunned|down)", "you dash: (stunned|dash not ready)", "you cannot move: (stunned)"
- "you dash {direction}"
- "YOU ARE HIT by a {source} — hearts n/3"
- "you went down", "room cleared"
- "you catch your breath — hearts n/3" (printed only when a heart was gained)
- "run complete", "room {n} begins", "a new run begins"
- "run over — rooms cleared: N" or "run complete — rooms cleared: N", then "press attack to start again"

Position names come from a 3×3 grid. Two same-type enemies in one cell get a number ("spitter 1 (top right)").

### Gap defaults as built (F1–F11)

- **F1:** grub speed 2.0 (spec value).
- **F2:** an unslotted grub holds at 1.25 tiles.
- **F3:** a spitter on top of the player fires nothing; the trace logs `spit_skipped`.
- **F4:** no extra spacing after a stagger.
- **F5:** read as no two Charge starts and no two Fires within 0.5 s.
- **F6:** "room cleared", then "run complete", the heal, 1.5 s of free input, then the "run complete — rooms cleared: 5" screen.
- **F7:** the session stops at the run-over screen when no input is left. A later scripted attack restarts the run.
- **F8:** as in handoff 14.
- **F9 (overridden by 17 item 3):** glyphs, colors and wording follow `design/combat-visuals.md`. A damaged telegraphing enemy shows `W`/`Z`.
- **F10:** "you dash: (dash not ready)" and "(stunned)" for any input in stun.
- **F11:** no pause implemented.

Deviations and additions to flag:
- Extra lines not in the visual spec: "room N begins", "a new run begins", the heal line. The "the grub is open" line carries a side, like the wind-up line.
- The optional `p` invulnerability marker was not added (17: not unless the designer asks).
- `hearts_lost` in the bots output counts hurt events; the bots do not play a run.
- Extra draws on events were cheap and are built (17 item 1): hurt, swipe, wind-up, charge, spit, recover, down, cleared, room loaded, run start.

### Measured values

Not measured as numbers. The tests assert the bounds: timestamp error ≤ 0.04 s at 30 FPS and ≤ 0.02 s at 60 FPS, cross-fps difference ≤ 0.07 s, Strike evaluated in ≥ 4 ticks at 30 FPS for five carry offsets. All of those pass.

### Run results

- `run_tests` ran 34 tests in the run round. 33 passed. The one error is `ManualTest`, because `manual.md` was not in the run workspace (`/manual.md` not found). It should pass once `manual.md` is at the project root with the draft below. That has not been run yet.
- `run_bots` at `fps 30` and `fps 60`: every walker, dodger and reactive run clears all 5 rooms, losing 0 hearts (one heart lost by reactive in room 2 at 60 FPS). The camper is not cleared in rooms 3–5, as it stays still against spitters. Details are in the run results.

### Open question (blocks hand-off to QA)

- `manual.md` must be written, but this step cannot write it. Options: (a) the Studio gives a step write access to `manual.md` and places the draft below, or (b) re-run this role with `manual.md` on the write list. No code change is needed either way. Nothing else is blocked.

### Draft `manual.md` (player-facing; to be placed unchanged)

```markdown
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
```

## Decisions already made

D-001…D-004 hold; no new inputs were added.

## Constraints

- Correct at 30 and 60 FPS. The shot shape is `[x, y, vx, vy]`. `cleared` means "the current room is cleared".
- No rules, timings or parameters changed beyond the plan's defaults.

## Open questions

- The `manual.md` write access (above).
- Non-blocking for the designer at Review: F1, F6, F7. Also: the numbering used when two same-type enemies share a screen cell (a new string).
- Pause (F11) is not implemented; QA should mark it not verifiable.

## Expected output

The Studio resolves the `manual.md` write, confirms `run_tests` passes in the real layout, then composes the verification Handoff for QA without the Sender assessment.

## Sender assessment

- Root cause for the spit-line defect: `_who()` gives the spitter's position name and, when two spitters of one kind share a cell, a number. The spit and charge lines come from the same table, so a spit line can always be matched to its charge line. Event count is unchanged: one `spit` event per spitter that fired.
- Confidence is high on timings and flow because the tests cover them at both frame rates. The 0.07 s cross-fps check passed on one 6 s session, not on a wider set.
- `ManualTest` has not been run against a real `manual.md`. It checks only for backticked glyphs and key phrases. I wrote the draft to contain all of them, but I did not run it.
- Slot starvation (plan section 7) is still there by design; the live playtest should watch it.
- Not verified: the color rendering, which needs the art-director.

## Load

- Role: studio/roles/qa.md
- Skills: none specified
- Project: design/combat.md, design/combat-visuals.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
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
