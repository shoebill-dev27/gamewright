# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/22-studio-to-gameplay-engineer.md
next_seq: 23
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/23-gameplay-engineer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/22-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 22
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 22: studio → gameplay-engineer — confirm the placed `manual.md` with `run_tests`

## Task

The Owner has placed the draft `manual.md` at the project root, unchanged. Run `run_tests` (`python3 -m unittest discover -s tests` in `repo/`) and report whether all 34 tests pass, including `ManualTest`. Do not write `manual.md`.

## Context

Goal G-001 (combat feels monotonous). Build 0.5 code (T1–T7, T9) was finished in step 18, with 33/34 tests passing. The only open item, T8 `manual.md`, was blocked twice on write access (18, 20) and escalated to the Owner (21). The Owner chose Option A (D-005): the Draft `manual.md` from 18 was placed verbatim at the project root. `ManualTest` reads `REPO.parent / "manual.md"`. The next steps are Verify (`qa` and `art-director`, in parallel), then Play and Review.

## Findings

- The Owner's response and the choice are in `21-studio-to-owner.md` and D-005.
- The Draft `manual.md` text is in `18-gameplay-engineer-to-studio.md` under "Draft `manual.md`". The engineer's earlier reading found it consistent with the implementation, but it was never tested.
- `run_tests` was 33/34 before the manual was placed. The one failure was `ManualTest`.

## Decisions already made

- D-001: one attack button plus dash; no new buttons.
- D-002: Option A, rework existing enemy behavior first.
- D-003: room mix, zero hearts ends the run, room clear heals one heart.
- D-004: Option A as one sequential change set (item 5: the manual belongs to the gameplay-engineer).
- D-005: the Owner placed the draft `manual.md` unchanged (Option A of Escalation 21).

## Constraints

- Run only `run_tests`. Do not edit code, tests or `manual.md` unless the failure is in code you own and the fix is within spec AC-1…AC-17 and V-1…V-8 and the plan. The write access to `manual.md` was not granted (D-005 is a one-time placement).
- If `ManualTest` fails because of the text of the placed `manual.md`, do not edit it. Report the exact failing assertion, the line in `manual.md` it concerns, and the suggested corrected text, with outcome `question`, so the Studio can ask the Owner again. This would be a new input, not a repeat of the earlier block.
- If a different test fails, diagnose and fix it within your authority, or hand back per your contract if the spec is ambiguous.
- Must play correctly at 30 and 60 FPS (project constraints).

## Open questions

None.

## Expected output

A short build note in Findings of your outgoing Handoff: the test command, the result (pass/fail count, names of any failures) and any change you made, with a sha or file list if you changed anything. Address the result to `studio` (not to qa), because the Studio composes QA's fresh Handoff without the Sender assessment. Use `outcome: done` if 34/34 pass, otherwise `question` or `fail` as appropriate.

## Sender assessment

The Studio did not read the draft. The risk is small: the earlier reading found no contradiction and the Owner placed the text unchanged. Pause (F11) is not implemented; this is known and QA marks it not verifiable.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, manual.md, design/combat.md, design/combat-visuals.md, repo/README.md, repo/game.py, repo/tests/test_game.py, goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md, goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
- Decisions: decisions/D-004-option-a-single-change-set.md, decisions/D-005-owner-places-manual-draft.md
- Previous handoff: goals/G-001-combat-monotony/21-studio-to-owner.md
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS).
- `play.py`: runs an input script (`../manual.md`) and prints the player view or a trace.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.5: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. Every enemy timer runs on elapsed
seconds, and the leftover time of a tick is carried into the next state, so timings do not depend
on the frame rate.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY, ARC_TIME = 1.5, 0.35, 0.15
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

GRUB_HP, GRUB_SPEED = 2, 2.0
GRUB_RANGE = 1.25  # a grub this close to the player may start a wind-up
GRUB_WINDUP, GRUB_STRIKE, GRUB_RECOVERY, GRUB_CANCEL_RECOVERY = 0.5, 0.15, 0.9, 0.6
GRUB_STRIKE_REACH, GRUB_LUNGE = 1.0, 1.0
GRUB_SLOTS = 2  # grubs allowed in Wind-up or Strike at once
KNOCK_DISTANCE, KNOCK_TIME = 1.0, 0.2

SPITTER_HP = 2
SPIT_CHARGE, SPIT_RECOVERY, SPIT_STAGGER = 0.8, 0.6, 1.0
SPIT_INTERVAL, SPIT_FIRST, SPIT_OFFSET = 2.5, 1.0, 0.8
SHOT_SPEED, SHOT_REACH = 3.0, 0.4

DOWN_DELAY, CLEAR_DELAY = 2.0, 1.5

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOM_ORDER = ["1", "2", "3", "4", "5"]
ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("grub", 2, 1), ("grub", 15, 7), ("grub", 14, 0), ("grub", 1, 8)],
    "3": [("spitter", 2, 1), ("spitter", 14, 7), ("spitter", 2, 7)],
    "4": [("grub", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [
        ("grub", 1, 1),
        ("grub", 0, 6),
        ("grub", 4, 8),
        ("spitter", 15, 0),
        ("spitter", 15, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}


def spot_name(x, y):
    """Name of the 3x3 region of the room that holds (x, y)."""
    col = 0 if x < ROOM_W / 3 else (1 if x < 2 * ROOM_W / 3 else 2)
    row = 0 if y < ROOM_H / 3 else (1 if y < 2 * ROOM_H / 3 else 2)
    names = [
        ["top left", "top", "top right"],
        ["left", "center", "right"],
        ["bottom left", "bottom", "bottom right"],
    ]
    return names[row][col]


def segment_distance(a, b, p):
    """Closest distance between point p and the segment a-b."""
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    length = dx * dx + dy * dy
    if length < 1e-12:
        return math.hypot(px - ax, py - ay)
    u = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length))
    return math.hypot(px - (ax + u * dx), py - (ay + u * dy))


class Enemy:
    def __init__(self, kind, x, y, index=0, nth=0):
        if kind not in ("grub", "spitter"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.max_hp = GRUB_HP if kind == "grub" else SPITTER_HP
        self.hp = self.max_hp
        self.index = index  # position in the room's enemy list
        self.nth = nth  # position among enemies of the same kind (spawn order)
        self.spot = spot_name(self.x, self.y)
        # grub: approach, windup, strike, recovery.  spitter: idle, charge, recovery, stagger.
        self.state = "approach" if kind == "grub" else "idle"
        self.timer = 0.0  # grub: seconds left in the current state
        self.until = 0.0  # spitter: absolute time the current state ends
        self.next_charge = math.inf  # spitter: absolute time of its next Charge
        self.carry = 0.0  # grub: time already elapsed in this tick when a Recovery ended
        self.knock_left = 0.0
        self.knock_v = (0.0, 0.0)
        self.lunge_dir, self.lunge_speed = (0.0, 0.0), 0.0
        self.struck = False

    @property
    def alive(self):
        return self.hp > 0

    @property
    def committed(self):
        """True while the enemy is committed to hurting the player."""
        if self.kind == "grub":
            return self.state in ("windup", "strike")
        return self.state == "charge"

    def calm(self):
        """Back to a harmless state (used when the player goes down)."""
        self.knock_left = 0.0
        self.carry = 0.0
        self.struck = False
        if self.kind == "grub":
            self.state = "approach"
        else:
            self.state = "idle"
            self.next_charge = math.inf


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.practice = room == "empty"
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.arc_left, self.arc_dir = 0.0, (1, 0)
        self.queued_attack = False
        self.shots = []  # [x, y, vx, vy]
        self.events = []  # (time, kind, details)
        self.cleared = False  # the current room is cleared (until the next room loads)
        self.phase = "playing"  # playing, cleared (waiting), down, over
        self.down_left = self.clear_left = 0.0
        self.rooms_cleared = 0
        self.complete = False
        self.finished = False  # the session is over (practice room: 2 s after going down)
        self.room_start = 0.0
        self.enemies = []
        for spec in ROOMS[room]:
            self._add(*spec)

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, when=None, **details):
        self.events.append((self.t if when is None else when, kind, details))

    # --- Setup ---------------------------------------------------------------------------------

    def _add(self, kind, x, y):
        nth = sum(1 for e in self.enemies if e.kind == kind)
        enemy = Enemy(kind, x, y, index=len(self.enemies), nth=nth)
        if kind == "spitter":
            enemy.next_charge = max(
                self.room_start + SPIT_FIRST + SPIT_OFFSET * nth, self.t
            )
        self.enemies.append(enemy)

    def spawn(self, kind, x, y):
        self._add(kind, x, y)

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    def _who(self, enemy):
        dup = any(
            o is not enemy and o.kind == enemy.kind and o.spot == enemy.spot
            for o in self.enemies
        )
        return {"who": enemy.index, "spot": enemy.spot, "dup": dup, "n": enemy.nth + 1}

    def _side(self, enemy):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        if abs(dx) < 0.05 and abs(dy) < 0.05:
            return "on you"
        if abs(dx) >= abs(dy):
            return "left" if dx < 0 else "right"
        return "above" if dy < 0 else "below"

    # --- Input ---------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.finished:
            return
        if self.phase == "over":
            if action == "attack":
                self._new_run()
            return
        if self.hearts <= 0:
            if action == "attack":
                self.log("ignored", action=action, reason="down")
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
                self.log("ignored", action=action, reason="too soon")
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

    # --- Simulation ----------------------------------------------------------------------------

    def step(self):
        dt = self.dt
        t0 = self.t
        self.frame += 1
        t1 = self.t
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        self.arc_left = max(0.0, self.arc_left - dt)
        if self.finished or self.phase == "over":
            return
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= EPS:
                self.hurt_left = 0.0
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= EPS:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        if self.phase == "down":
            self.down_left -= dt
            if self.down_left <= EPS:
                self._end_down()
            return
        cleared_now = False
        if (
            self.phase == "playing"
            and not self.cleared
            and self.enemies
            and all(not e.alive for e in self.enemies)
        ):
            self._clear()
            cleared_now = True
        if self.phase == "playing":
            self._update_shots(dt)
            self._update_enemies(t0, t1, dt)
        elif self.phase == "cleared" and not cleared_now:
            self.clear_left -= dt
            if self.clear_left <= EPS:
                self._after_clear()

    # --- Player attack -------------------------------------------------------------------------

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        self.arc_left, self.arc_dir = ARC_TIME, self.facing
        fx, fy = self.facing
        struck, hits = [], []
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dx, dy = enemy.x - self.x, enemy.y - self.y
            dist = math.hypot(dx, dy)
            along = dx * fx + dy * fy
            across = dx * fy - dy * fx
            if dist <= ATTACK_REACH and (dist < 1e-9 or (along > 0 and abs(across) <= along)):
                enemy.hp -= 1
                struck.append(enemy)
                hits.append(
                    (enemy.kind, "defeated" if enemy.hp <= 0 else "hit", enemy.hp, enemy.index)
                )
        self.log("attack", facing=_name(self.facing), hits=hits)
        for enemy in struck:
            self._after_hit(enemy)

    def _after_hit(self, enemy):
        if enemy.hp <= 0:
            enemy.state = "dead"
            return
        if enemy.kind == "grub":
            if enemy.state == "windup":
                enemy.state, enemy.timer, enemy.carry = "recovery", GRUB_CANCEL_RECOVERY, 0.0
                self.log("recover", cause="interrupted", who=enemy.index, side=self._side(enemy))
            if enemy.state != "strike":
                self._knock(enemy)
        elif enemy.state == "charge":
            enemy.state = "stagger"
            enemy.next_charge = self.t + SPIT_STAGGER
            self.log("stagger", **self._who(enemy))

    def _knock(self, enemy):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        dist = math.hypot(dx, dy)
        if dist < 1e-9:
            dx, dy, dist = float(self.facing[0]), float(self.facing[1]), 1.0
        speed = KNOCK_DISTANCE / KNOCK_TIME
        enemy.knock_v = (dx / dist * speed, dy / dist * speed)
        enemy.knock_left = KNOCK_TIME
        self.log("knockback", who=enemy.index)

    # --- Enemies -------------------------------------------------------------------------------

    def _update_enemies(self, t0, t1, dt):
        for enemy in self.enemies:
            if enemy.alive and enemy.kind == "spitter":
                self._spitter(enemy, t0, t1)
                if self.phase != "playing":
                    return
        grubs = [e for e in self.enemies if e.alive and e.kind == "grub"]
        for grub in grubs:
            self._grub_timers(grub, t0, dt)
            if self.phase != "playing":
                return
        for grub in grubs:
            self._grub_move(grub, dt)
        self._assign_windups(grubs, t1)

    def _grub_timers(self, enemy, t0, dt):
        enemy.carry = 0.0
        left = dt
        while enemy.state in ("windup", "strike", "recovery") and left > 1e-12:
            use = max(0.0, min(left, enemy.timer))
            if enemy.state == "strike":
                self._lunge(enemy, use)
                if self.phase != "playing":
                    return
            enemy.timer -= use
            left -= use
            if enemy.timer <= EPS:
                self._grub_next(enemy, t0 + (dt - left))
                if enemy.state == "approach":
                    enemy.carry = left

    def _grub_next(self, enemy, at):
        if enemy.state == "windup":
            dx, dy = self.x - enemy.x, self.y - enemy.y
            dist = math.hypot(dx, dy)
            length = min(GRUB_LUNGE, dist)
            if dist > 1e-9 and length > 0:
                enemy.lunge_dir = (dx / dist, dy / dist)
                enemy.lunge_speed = length / GRUB_STRIKE
            else:
                enemy.lunge_dir, enemy.lunge_speed = (0.0, 0.0), 0.0
            enemy.state, enemy.timer, enemy.struck = "strike", GRUB_STRIKE, False
            self.log("strike", when=at, who=enemy.index)
        elif enemy.state == "strike":
            enemy.state, enemy.timer = "recovery", GRUB_RECOVERY
            self.log("recover", when=at, cause="strike", who=enemy.index, side=self._side(enemy))
        else:
            enemy.state = "approach"

    def _lunge(self, enemy, use):
        old = (enemy.x, enemy.y)
        if enemy.lunge_speed > 0 and use > 0:
            enemy.x, enemy.y = self._clamp(
                enemy.x + enemy.lunge_dir[0] * enemy.lunge_speed * use,
                enemy.y + enemy.lunge_dir[1] * enemy.lunge_speed * use,
            )
        if not enemy.struck:
            reach = segment_distance(old, (enemy.x, enemy.y), (self.x, self.y))
            if reach <= GRUB_STRIKE_REACH and self._hurt("grub"):
                enemy.struck = True

    def _grub_move(self, enemy, dt):
        if enemy.knock_left > 0:
            span = min(dt, enemy.knock_left)
            enemy.x, enemy.y = self._clamp(
                enemy.x + enemy.knock_v[0] * span, enemy.y + enemy.knock_v[1] * span
            )
            enemy.knock_left -= span
            if enemy.knock_left <= EPS:
                enemy.knock_left = 0.0
            return
        if enemy.state != "approach":
            return
        dx, dy = self.x - enemy.x, self.y - enemy.y
        dist = math.hypot(dx, dy)
        if dist > GRUB_RANGE:
            step = min(GRUB_SPEED * dt, dist - GRUB_RANGE)
            enemy.x, enemy.y = self._clamp(
                enemy.x + dx / dist * step, enemy.y + dy / dist * step
            )

    def _assign_windups(self, grubs, t1):
        free = GRUB_SLOTS - sum(1 for g in grubs if g.alive and g.state in ("windup", "strike"))
        candidates = []
        for grub in grubs:
            if grub.alive and grub.state == "approach" and grub.knock_left <= EPS:
                dist = math.hypot(self.x - grub.x, self.y - grub.y)
                if dist <= GRUB_RANGE + 1e-6:
                    candidates.append((dist, grub.index, grub))
        candidates.sort(key=lambda c: (c[0], c[1]))
        for _, _, grub in candidates[: max(0, free)]:
            grub.state = "windup"
            grub.timer = GRUB_WINDUP - grub.carry
            self.log("windup", when=t1 - grub.carry, who=grub.index, side=self._side(grub))
            grub.carry = 0.0
        for grub in grubs:
            grub.carry = 0.0

    def _spitter(self, enemy, t0, t1):
        for _ in range(6):
            if self.phase != "playing":
                return
            if enemy.state == "charge":
                if enemy.until > t1 + EPS:
                    return
                self._fire(enemy, enemy.until, t1)
            elif enemy.state == "recovery":
                if enemy.until > t1 + EPS:
                    return
                enemy.state = "idle"
            else:  # idle or stagger
                if enemy.next_charge > t1 + EPS:
                    return
                start = max(enemy.next_charge, t0)
                enemy.state = "charge"
                enemy.until = start + SPIT_CHARGE
                enemy.next_charge = start + SPIT_INTERVAL
                self.log("charge", when=start, **self._who(enemy))

    def _fire(self, enemy, at, t1):
        enemy.state = "recovery"
        enemy.until = at + SPIT_RECOVERY
        dx, dy = self.x - enemy.x, self.y - enemy.y
        dist = math.hypot(dx, dy)
        if dist <= 1e-9:
            self.log("spit_skipped", when=at, **self._who(enemy))
            return
        vx, vy = dx / dist * SHOT_SPEED, dy / dist * SHOT_SPEED
        elapsed = max(0.0, t1 - at)
        self.shots.append([enemy.x + vx * elapsed, enemy.y + vy * elapsed, vx, vy])
        self.log("spit", when=at, **self._who(enemy))

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and not self.invulnerable and self.hearts > 0:
                self._hurt("shot")
                continue
            kept.append(shot)
        self.shots = kept if self.phase == "playing" else []

    # --- Player damage, down, clear and run flow -----------------------------------------------

    def _hurt(self, source):
        if self.invulnerable or self.hearts <= 0:
            return False
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self._down()
        return True

    def _down(self):
        self.phase, self.down_left = "down", DOWN_DELAY
        self.shots = []
        self.queued_attack = False
        self.heading = (0, 0)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.calm()
        self.log("down")

    def _end_down(self):
        if self.practice:
            self.finished = True
            self.log("session_end")
        else:
            self.phase = "over"
            self.log("run_over", rooms=self.rooms_cleared, complete=False)

    def _clear(self):
        self.cleared = True
        self.shots = []
        self.log("cleared", room=self.room)
        if self.practice:
            return
        self.rooms_cleared += 1
        gained = self.hearts < HEARTS
        self.hearts = min(HEARTS, self.hearts + 1)
        self.log("heal", hearts=self.hearts, gained=gained)
        self.phase, self.clear_left = "cleared", CLEAR_DELAY
        if self.room == ROOM_ORDER[-1]:
            self.complete = True
            self.log("run_complete")

    def _after_clear(self):
        if self.complete:
            self.phase = "over"
            self.log("run_over", rooms=self.rooms_cleared, complete=True)
        else:
            self._load_room(str(int(self.room) + 1))

    def _load_room(self, room):
        self.room = room
        self.room_start = self.t
        self.enemies = []
        for spec in ROOMS[room]:
            self._add(*spec)
        self.shots = []
        self.x, self.y = START
        self.cleared = False
        self.phase = "playing"
        self.log("room_loaded", room=room)

    def _new_run(self):
        self.hearts, self.rooms_cleared, self.complete = HEARTS, 0, False
        self.heading, self.facing = (0, 0), (1, 0)
        self.queued_attack = False
        self.dash_left = self.dash_cooldown = 0.0
        self.hurt_left = self.stun_left = self.recovery = self.arc_left = 0.0
        self.invulnerable = False
        self.log("run_start")
        self._load_room("1")

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

<<<FILE goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 20
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 20: gameplay-engineer → studio — `manual.md` (T8) still cannot be written; escalate

## Task

Escalate to the Owner (or give a step write access to `manual.md`). This step could not write `manual.md`, so T8 is still open and nothing can go to QA yet.

## Context

G-001, Build of Option A (build 0.5). Handoff 19 asked this step to place the draft from handoff 18 at the project root as `manual.md` and then confirm `run_tests`. The write list for this step contains only this handoff, `repo/<path>`, and `@run` blocks. `manual.md` at the project root is not on it. The test (`ManualTest`) reads `REPO.parent / "manual.md"`, which is the project root. A file under `repo/` would not satisfy it. Handoff 19 told this step not to work around a missing write permission, so I did not place the file anywhere else, and I did not run the tests. Without `manual.md` they would fail the same way as in handoff 18.

## Findings

**`manual.md` could not be written.** It does not exist at the project root. This is the second time the same input has been handed back for this reason, so the Studio should escalate to the Owner.

What I could do without the file, by reading the draft against `repo/play.py` and `repo/tests/test_game.py`:

1. **Glyphs.** Every `GLYPHS` character is in the draft as a backticked entry: `P`, `x`, `g`, `G`, `w`, `W`, `s`, `S`, `z`, `Z`, `*`, `)`, `(`, `^`, `v`. This is what `ManualTest` checks.
2. **Phrases.** Each of the test's phrases appears in the draft: "room empty", "rears back", "is open", "charges", "spits", "run over", "press attack to start again", "(miss)", "(too soon)", "(stunned)", "(down)", "room cleared". I checked this by reading, not by running the test.
3. **Behavior.** I found nothing in the draft that contradicts the built game. The "(dash not ready)" wording, the heal, the 1.5 s of free input and the practice-room rules match `LINES` and the spec. The draft's "the grub is open" is a prefix of the built line "the grub is open ({side})", which is fine.
4. **Wording changes.** None were needed. The draft can be placed unchanged.
5. **Player-facing rule.** The draft names no internal states, plan IDs or acceptance-criterion numbers.

Not done: `run_tests` was not run, so the 34-test result is unconfirmed. The expected result is 34 of 34 once the draft is at the project root, but that has not been shown.

## Decisions already made

D-001…D-004 hold. D-004 item 5 assigns the manual to the gameplay-engineer in this change set. That needs write access to `manual.md`.

## Constraints

- Place the draft from handoff 18, section "Draft `manual.md`", unchanged at the project root.
- No code changes are needed.

## Open questions

- Who writes `manual.md`? Options:
  - (a) The Owner places the draft from handoff 18 at the project root by hand.
  - (b) The Studio re-runs the gameplay-engineer with `manual.md` on the write list.
- After either option, run `python3 -m unittest discover -s tests` and confirm 34 of 34 pass before composing the QA handoff.

## Expected output

Once `manual.md` exists and `run_tests` passes, the Studio composes the verification Handoff for QA without the Sender assessment.

## Sender assessment

- High confidence the draft passes `ManualTest`, from reading the test against the draft. This is not tested.
- AC-15 and V-5 stay unverifiable until the file exists.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-visuals.md, design/combat.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/19-studio-to-gameplay-engineer.md
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

<<<FILE decisions/D-005-owner-places-manual-draft.md
---
kind: decision
id: D-005
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-005: The Owner places the draft `manual.md` (Option A)

## Decision

For Escalation 21, the Owner chose **Option A**. The Draft `manual.md` from `goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md` ("Draft `manual.md`") was placed unchanged at the project root as `manual.md`.

Owner's own words (2026-10-15):

> A。18 の Draft manual.md を変更せずにプロジェクト直下の manual.md として置きました（Owner の代理として Studio の推奨案を採用）。

Conditions and limits:
- The file is the draft verbatim, with no edits. Whether it passes `ManualTest` (`REPO.parent / "manual.md"`) is still untested; the gameplay-engineer confirms this with `run_tests` (expected 34/34).
- The response says the Studio's recommendation was adopted on the Owner's behalf. The Studio treats this as the Owner's choice of A, as recorded in the Escalation.
- This is a one-time placement. It does not give the gameplay-engineer write access to `manual.md`. If later changes to `manual.md` are needed, they are a new question.

## Rationale

The draft was already checked against the implementation by reading, and placing it is quick and reversible. It unblocks AC-15 and V-5 without a change to the execution environment.

## Alternatives considered

- **B, give the gameplay-engineer write access:** matches D-004 item 5 but needs an environment change. Not chosen.
- **C, verify without `manual.md`:** AC-15, V-5 and `ManualTest` would stay unverified and the problem would return later. Not chosen.

## Revisit when

`run_tests` shows `ManualTest` failing on the placed draft, or QA/art-director find that the manual contradicts the build. Then `manual.md` needs another edit, which needs a write path (B) or another Owner action.
>>>END

<<<FILE goals/G-001-combat-monotony/21-studio-to-owner.md
---
kind: escalation
goal: G-001
seq: 21
from: studio
to: owner
status: resolved
decision: D-005
---
# 21: オーナーの判断が必要 — `manual.md` を誰がどうやって書くか

## Question

ビルド 0.5 のコードは完成しましたが、プロジェクト直下の `manual.md` を書ける担当がいません。Owner が手で置くか、書き込み権限を与えるか、`manual.md` なしで先へ進むかを選んでください。

## Why this needs the Owner

`manual.md` の作成が2回続けて同じ理由(書き込み権限がない)で差し戻されました(18 と 20)。その間に新しい入力はありません。`studio/orchestration.md` の Loop limits により、同じ入力不足を3回目も Role に回すことはできません。Owner への escalation が必要です。どの Role も作れない材料(書き込み権限)で作業が止まっているケースにも当たります。

状況:
- コード T1–T7, T9 は完了し、34 テスト中 33 が通っています(18)。
- 残りは T8 の `manual.md` だけです。ドラフトは `18-gameplay-engineer-to-studio.md` の "Draft `manual.md`" にあります。
- `ManualTest` は `REPO.parent / "manual.md"`(プロジェクト直下)を読みます。`repo/` 以下に置いても満たされません。
- QA の AC-15 と V-5 は `manual.md` に依存します。
- gameplay-engineer がドラフトを実装と照らし合わせて読んだ限り、矛盾はなく、そのまま置けるはずです。ただしテストは未実行です。

## Options

### Option A — Owner がドラフトを手で置く

Owner が 18 の "Draft `manual.md`" を、変更せずにプロジェクト直下へ `manual.md` として保存します。
コスト: Owner の手作業が1回。リスクは小さく、いつでも元に戻せます。
If chosen: Owner が置いたと返信したら、Studio は gameplay-engineer に `run_tests`(34/34 の確認)だけを依頼します。通れば QA(Sender assessment なしの新しい Handoff)と art-director(視覚レビュー)を並列で開きます。

### Option B — gameplay-engineer に `manual.md` の書き込み権限を与える

次の gameplay-engineer のステップの書き込み許可リストに `manual.md` を加えます。
コスト: 実行環境の設定変更。D-004 の項目5(マニュアルは gameplay-engineer の担当)に沿います。
If chosen: Studio は 19 と同じ内容で gameplay-engineer を再実行します(ドラフトを配置し、`run_tests` を確認)。通れば Option A と同じ Verify へ進みます。

### Option C — `manual.md` なしで Verify に進む

`manual.md` をいったん後回しにして、QA と art-director に進みます。
コスト: AC-15 と V-5 は検証不能になり、`ManualTest` が失敗したままです。後で同じ問題に戻ります。
If chosen: QA の Handoff に「AC-15・V-5・ManualTest は対象外」と明記して Verify を開きます。`manual.md` は最終 Review 前に再度 escalate します。

## Studio recommendation

Option A(手軽さを優先するなら)。実行環境の設定を変えられるなら Option B でも構いません。

## Reasoning

ドラフトは確認済みで、置くだけで済みます。Option A はすぐできて、Option B と結果は同じです。Option B は担当の筋は通りますが、設定変更が必要です。Option C は問題を先送りするだけで、AC-15・V-5 が未検証のまま Play と Review に進むことになるため勧めません。ドラフトの実装との整合は読んで確かめただけでテストは未実行ですが、置いた後に `run_tests` で確認できます。

## Meanwhile

Nothing; all remaining steps depend on this answer. (Verify、Play、Review はすべて `manual.md` の有無に依存します。)

## Owner decision required

A / B / C — 選択肢を返信してください(条件があれば併せて)。A の場合は、置き終わったことも知らせてください。

---

**Owner response (2026-10-15):** A。18 の Draft manual.md を変更せずにプロジェクト直下の manual.md として置きました（Owner の代理として Studio の推奨案を採用）。

**Resolved:** D-005 (`decisions/D-005-owner-places-manual-draft.md`).
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
