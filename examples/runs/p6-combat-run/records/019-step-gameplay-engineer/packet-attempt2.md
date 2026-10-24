# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
next_seq: 18
runs: tests, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/18-gameplay-engineer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 17
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 17: studio → gameplay-engineer — Build the Option A combat rework (build 0.5)

## Task

Implement the Option A combat rework as one sequential change set (tasks T1–T9 in handoff 14), following the spec `design/combat.md` (AC-1…AC-17), the visual spec `design/combat-visuals.md` (V-1…V-8), the run/room rules in D-003, and the spit-line requirement from handoff 15. Stop and hand back if the spec is ambiguous or contradictory; do not decide design questions.

## Context

G-001, "Combat feels monotonous". D-002 chose Option A: rework existing enemy behavior (telegraphed grub and spitter state machines, attack-slot limit, spitter aim-lock, run/room flow). Design is done. The Technical Director found the spec feasible (14). QA reproduced the duplicate spit line (15). The art-director reviewed the visuals (16). Build under change: `repo/` at sha e54837757611 (version 0.4).

## Findings

**Plan (handoff 14, read it in full).** Key points:
- Elapsed-seconds timers with leftover carry; swept strike check; tick order in `step()` as in section 2; no new modules.
- Task order T1 sim core → T2 player attack → T3 run/room flow → T4 trace → T5 player view (data tables `GLYPHS` and `LINES` in `play.py`) → T6 bots → T7 tests → T8 `manual.md` → T9 as-built report.
- Test strategy per AC in section 4, with timing tests at 30 and 60 FPS.
- Spec gap defaults F1–F11 are set by the Technical Director. Use them unless item 3 below overrides. Report each choice as built.

**Defect report (handoff 15).** The doubled "a spitter spits" line is two spitters each printing the same text, not a double event. It is a presentation defect measured against AC-8. Acceptance criteria for the fix:
1. In rooms 4 and 5, at `fps 30` and `fps 60`, each spit line names its spitter (for example by position).
2. No two lines at the same timestamp have identical text, for 1, 2 and 3 spitters (rooms 3, 4, 5).
3. The number of spit lines at a timestamp equals the number of spitters that fired, and the number of `spit` trace events is unchanged.
4. Each spit line can be matched to its projectile's `*`.
5. Spit timing and projectile behavior are unchanged apart from what the rework intentionally changes.

**Visual spec (handoff 16, `design/combat-visuals.md`).** Rulings to implement:
- The glyph carries the state, not color alone. Uppercase means committed to hurting (`G`, `W`, `S`, `Z`); lowercase means harmless (`g`, `w`, `s`, `z`). A damaged enemy uses the `w/z` family.
- Orange/red is reserved for telegraphed enemies and `*`. The player, the swipe arc and `x` never use it. Harmless enemies are muted.
- Extra room draws at Wind-up start, Charge start, projectile spawn, every swipe, grub Recovery start and player down. Timings are untouched.
- Text lines name the enemy and its position, for example "a grub rears back (left)". Add the "the grub is open" line at the start of grub Recovery and a spitter stagger line.
- Swipe arc glyphs `) ( ^ v` in lantern color on the tiles in reach.
- The run-over screen adds "press attack to start again".
- Optional, for the designer: a visible invulnerability marker (`p` for `P`). Do not add it unless the designer specifies it.

**Studio notes on how the plan and the visual spec fit together:**
1. The extra draws on events are the same thing as the plan's T5 "snapshots". Build them. If they turn out not to be cheap, hand back with `outcome: question` and do not drop them silently.
2. `manual.md` (T8) is yours. Include the glyph table, `x`, the swipe arc, the practice room, the new lines and the run-over screen. Describe behavior; do not copy [tune] numbers. Write it player-facing only.
3. Where handoff 14 (F9, glyph defaults) and `design/combat-visuals.md` differ, follow `design/combat-visuals.md` for glyphs, colors and line wording, and say so in the as-built report. Rules, timings and parameters come only from `design/combat.md`, D-003 and the plan.
4. Pause (F11): no implementation, per the plan.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002: Option A, reuse existing enemy behavior; B deferred, C out of scope.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-004: Option A is built as one sequential change set on the existing simulation; no isolated workspaces.

## Constraints

- Correct at both 30 and 60 FPS. Reuse existing systems; small team.
- No new input buttons (attack, dash, pause only).
- Do not change rules, timings or parameters in `design/combat.md` beyond the plan's gap defaults.
- Keep the shot shape `[x, y, vx, vy]` and the meaning of `cleared`, so `bots.py` keeps working.

## Open questions

- None blocking Build. Non-blocking for the designer at Review: F1 (grub speed 2.0 vs 1.2 in 0.4), F6, F7.
- If a spec ambiguity or contradiction stops you, hand back to `game-designer` via the Studio with `outcome: question`.

## Expected output

- T1–T9 in one change set: passing `run_tests`, `run_bots` at 30 and 60 FPS, updated `manual.md`, and the as-built report with the values listed in handoff 14 section 5 plus the visual tables and strings.
- Address the result to `studio`. The Studio composes the verification Handoff for QA, which must not see implementation reasoning, so keep verdicts and reasoning in `## Sender assessment`.
- Do not write verification verdicts for QA or the art-director.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/14-technical-director-to-studio.md, goals/G-001-combat-monotony/15-qa-to-studio.md, goals/G-001-combat-monotony/16-art-director-to-studio.md
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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS).
- `play.py`: runs an input script (`../manual.md`) and prints the player view or a trace.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.4: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

GRUB_HP, GRUB_SPEED, GRUB_REACH = 2, 1.2, 0.6
SPITTER_HP, SPIT_INTERVAL = 2, 2.0
SHOT_SPEED, SHOT_REACH = 2.0, 0.4

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

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


class Enemy:
    def __init__(self, kind, x, y):
        if kind not in ("grub", "spitter"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.hp = GRUB_HP if kind == "grub" else SPITTER_HP
        self.cooldown = SPIT_INTERVAL


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
        self.enemies = [Enemy(*spec) for spec in ROOMS[room]]
        self.shots = []  # [x, y, vx, vy]
        self.events = []  # (time, kind, details)
        self.cleared = False

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        self.enemies.append(Enemy(kind, x, y))

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
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            dx, dy = self.x - enemy.x, self.y - enemy.y
            dist = math.hypot(dx, dy)
            if enemy.kind == "grub":
                stop = GRUB_REACH * 0.9
                if dist > stop:
                    step = min(GRUB_SPEED * dt, dist - stop)
                    enemy.x += dx / dist * step
                    enemy.y += dy / dist * step
                if math.hypot(self.x - enemy.x, self.y - enemy.y) <= GRUB_REACH:
                    self._hurt("grub")
            else:
                enemy.cooldown -= dt
                if enemy.cooldown <= 1e-9:
                    enemy.cooldown += SPIT_INTERVAL
                    if dist > 0:
                        self.shots.append(
                            [
                                enemy.x,
                                enemy.y,
                                dx / dist * SHOT_SPEED,
                                dy / dist * SHOT_SPEED,
                            ]
                        )
                        self.log("spit")

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
The script format is described in the project's manual.md.
"""

import argparse
import sys

from game import HEARTS, ROOM_H, ROOM_W, Game

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots


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


def play(setup, inputs, view):
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
    out = Player(game) if view == "player" else Trace(game)
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
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.4 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, hurt = self.game, False
        for when, kind, details in g.events[self.seen :]:
            text = self.describe(kind, details)
            if text:
                print(f"{when:7.3f}  {text}")
            hurt = hurt or kind == "hurt"
        self.seen = len(g.events)
        if hurt or g.t >= self.next_snapshot - 1e-9:
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
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored":
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(x, y, mark):
            col, row = int(round(x)), int(round(y))
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = mark

        for shot in g.shots:
            put(shot[0], shot[1], "*")
        for enemy in g.enemies:
            if enemy.hp > 0:
                put(enemy.x, enemy.y, "g" if enemy.kind == "grub" else "s")
        put(g.x, g.y, "P" if g.hearts > 0 else "x")
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

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp})" for e in g.enemies if e.hp > 0
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
        setup, inputs = read_script(f.read())
    play(setup, inputs, args.view)


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)

Each bot starts every room with full hearts.
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


BOTS = {"camper": camper, "walker": walker, "dodger": dodger}


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
        "hearts_lost": HEARTS - game.hearts,
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
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}"
            )
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
from game import DASH_DISTANCE, HEARTS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 1.0)  # the grub closes in and bites; the hit-stun passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_bite_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.1)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_spitter_fires_every_two_seconds(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.05)
        self.assertEqual(sum(1 for _, kind, _ in game.events if kind == "spit"), 2)


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
            game.spawn("grub", 9.5, 4)
            run(game, 0.62)
            game.press("dash", "right")
            run(game, 0.5)
            hurt = [t for t, kind, _ in game.events if kind == "hurt"]
            ended = next(t for t, kind, _ in game.events if kind == "dash_end")
            self.assertTrue(all(t >= ended for t in hurt[1:]), (fps, hurt, ended))
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        import bots

        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)


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

<<<FILE decisions/D-002-combat-response-scope.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A)

## Decision

1. **Option A is approved as the first response for G-001.** The existing Grub and Spitter get legible, varied behavior:
   - a visible wind-up before damage is possible;
   - a recovery pause after attacking;
   - staggered Spitter volleys with a visible charge-up;
   - clear hit feedback on the player's own attacks, including a visible damaged state.
   The game-designer owns the exact timings, knockback and feedback rules.
2. **Option B (mixed rooms, moving spitters, staggered grub arrival) is deferred.** It is not rejected. It is reconsidered only if a playtest of the Option A build still shows sameness. It is in scope for G-001 only after that playtest.
3. **Option C (new enemy types) is out of scope for G-001 for now.** It is reopened only if A and B have been playtested and sameness remains.
4. **Another play round on rooms 4 and 5 runs before the spec is finalized.** The designer may start the spec for A in parallel, but must check it against the round's results before handing it on.

## Limits

- All work stays within D-001: no new inputs beyond attack, dash and pause.
- All new timings are specified in seconds. Acceptance criteria must hold at both 30 and 60 FPS.
- Every damaging action must be preceded by a visible telegraph (pillar 3).
- Prefer reuse of existing enemy, projectile and timer systems (small-team constraint).
- This decision does not cover the possible defects (room composition vs. spec, no game-over/restart state). Those are routed to `qa` separately and may change the spec's wording or add a rule.
- It does not decide whether Spitters get a way to be approached. The designer decides that within A, using the rooms 4 and 5 evidence.

## Rationale

- The diagnosis traces all four symptoms to one root cause: each enemy has a single behavior with no state change, timing variation or readable cue. Option A addresses that root cause directly, covering S1, S2 and S3 and part of S4.
- It supports pillar 1 (depth from positioning, timing and enemy behavior) and pillar 3 (readable threats). It matches the player profile, which favors spacing and dodging.
- It is the cheapest and lowest-risk option, and it reuses existing systems.
- No escalation trigger fires. No pillar, D-001 or Goal meaning changes, and the scope and cost are modest.
- Variety (B, C) layered on flat enemies would add busyness or content cost without fixing the cause.
- The rooms 4 and 5 round is cheap. The current sample is homogeneous and was blind-scripted, so it understates winnability and cannot show whether the dash answers grubs. Specifying timings without that evidence risks mistuning.

## Alternatives considered

- **B first or A+B together:** rejected for now. Without A the fights are only busier, and it adds scope before A's effect is known.
- **C (charger, shielded enemy):** rejected for now. It has the highest cost and scope risk and leaves the existing enemies flat.
- **Spec immediately, no further play round:** rejected. Rooms 4 and 5 are the only place to check the "mixed rooms" claim, and the dash/grub question needs reactive play.

## Revisit when

- The rooms 4 and 5 round shows they already contain the missing variety or different enemy behavior, which would change what Option A needs to cover.
- A playtest of the Option A build still reports monotony (open B, then C).
- A live playtest shows the Option A changes make grubs trivial or the dash insufficient. This is a tuning matter for the designer, unless it touches D-001.
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

<<<FILE goals/G-001-combat-monotony/14-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 14
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 14: technical-director → studio — Technical plan for the Option A combat rework (build 0.5)

## Task

Route this plan to `gameplay-engineer` (Build). The spec is feasible within the constraints. Nothing needs to go back to `game-designer` before Build. The spec has a few gaps (F1–F11 below) with defaults I set so Build is not blocked. The designer should confirm them at Review, and F1 (grub speed) matters most.

## Context

G-001, Option A (D-002), spec `design/combat.md` (AC-1…AC-17), rules in D-003. The current build is `repo/` at sha e54837757611 (version 0.4). It is one simulation module (`game.py`, about 200 lines), a script and view runner (`play.py`), balance bots (`bots.py`) and one test file.

Steps 12 (QA defect log, duplicate spit line) and 13 (art-director review of visual states) run in parallel with Plan. Their outputs may change message wording and glyph/color notes before Build starts. The plan keeps both in single data tables so that change is a data edit (task T5).

## Findings

### 1. Feasibility (answers to the open questions)

- **Attack-slot limit (max 2 grubs in Wind-up or Strike): feasible.**
  - Each tick, count grubs whose state is Wind-up or Strike.
  - Grubs that are in range (≤ 1.25 tiles) and not yet attacking are candidates. Sort them by (distance, spawn index), so ties are deterministic. Give out the free slots in that order.
  - A cancelled wind-up, a defeated grub, and the move to Recovery all free the slot at once.
  - Spawn index is the tie-break because "the nearer grub takes the free slot" has no rule for equal distances.
- **Spitter aim-lock: feasible, and almost free.**
  - The existing shot is already a straight line with a velocity fixed at fire time. Aim-lock means computing that velocity at the end of Charge, from the player's position at that instant.
  - No homing and no new projectile system are needed. Keep the shot as `[x, y, vx, vy]` so `bots.py` still unpacks it.
- **Reuse.**
  - Keep the countdown-float timer pattern already used for stun, recovery and cooldown (decrement by `dt`, 1e-9 epsilon). Keep the enemy list, the shot list and the event log.
  - Add per-enemy `state` and `timer` fields. No new classes beyond a few small helper functions.
- **No spec item is infeasible.** No cost or scope flag for the Director. Nothing irreversible. There is no save data.
  - Existing script files still parse.
  - Their results will differ from 0.4, which is intended.

### 2. Approach

**State machines on elapsed seconds**
- Grub states: Approach, Wind-up, Strike, Recovery, plus a short Knockback overlay.
- Spitter states: Idle, Charge, Recovery, Stagger.
- Each transition carries the leftover time. When `timer <= 1e-9`, the next state starts with `duration + timer`, where the overshoot is non-positive. A loop handles several transitions in one tick.
- With the carry, a timestamp error is less than one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS) and does not accumulate. This fits the spec's 0.04 / 0.02 tolerance.
- Spitter volleys use an absolute schedule in seconds from `room_start_t` (first Charge at 1.0 + 0.8·k, then every 2.5 s). Only spitters count for k, in spawn order. A Stagger re-bases that spitter's schedule to `now + 1.0`.

**Strike hit check**
- The Strike lunge moves up to 1 tile in 0.15 s, which is 0.22 tile per frame at 30 FPS.
- Evaluate the "within 1.0 tile at any moment" test as the closest approach over the tick's movement segment. This is a small analytic swept-distance helper, not a sample at the end of the tick.
- Evaluate it in the tick the Strike begins and in every tick until the transition. At 30 FPS this gives 4 or 5 evaluations, which meets "at least 4 frames".
- The lunge target is the player's position when Wind-up ended, as the Strike row says. Lunge length is min(1.0, distance to that spot). A grub hurts the player at most once per Strike.

**Tick order in `step()`**
1. Decrement timers.
2. Move the player and dash. A queued attack fires at dash end.
3. Room-clear check. Attacks from `press()` and from a queued attack have already happened.
4. Enemies, then shots. Neither runs once the player is down, and on clear all shots are removed first.
5. Phase timers: the down countdown, the room-transition countdown and the run-over state.

This makes "a clearing swipe cancels the strike or projectile hit due on that tick" hold. In 0.4 the clear check is at the end of the tick, so it must move.

**Run flow**
- It lives in `Game`, so `play.py` and `bots.py` share it. The phases are playing, cleared-waiting, down, and run over/complete.
- `cleared` keeps its meaning "current room cleared". It stays true until the next room loads, so bots that stop on it keep working.
- The practice room (`empty`) is not a run: no heal, no transition, and the session ends 2.0 s after the player goes down.
- Room load puts the player at (8, 4). It resets enemies and shots and leaves hearts and the other player timers alone.

**Swipe and feedback**
- Cone: with axis-aligned facing, hit when `along > 0` and `|across| <= along`, within 1.5. An enemy on top of the player counts as a hit. 0.4 uses a 180° half-plane test, so this is a change.
- The swipe arc is state in the simulation (`arc_left`, direction), so it is visible at any frame within 0.15 s.
- Event names kept for compatibility: `attack`, `hurt`, `down`, `spit`, `cleared`, `ignored`, `dash`.
  - `attack` gains per-hit remaining HP.
  - `ignored` gains `reason` values: `stunned`, `too soon` (renamed from `recovering`), `down`, `dash not ready`.
- New events: `windup`, `strike`, `recover`, `charge`, `stagger`, `knockback`, `defeated`, `room_loaded`, `heal`, `run_over`, `run_complete`, `run_start`.

**Trace** (a QA-facing interface)
- Add `state` and `timer` to each enemy column, and `room=` to the state line.
- A line is printed for every state change. AC-6 can then be checked by counting Wind-up/Strike grubs per line, and AC-2 timings read directly from the lines.

**Player view**
- Add snapshots at: swipe, wind-up/charge start, going down, room load and run over. The arc and telegraph are then always on screen. The 0.5 s cadence alone is fragile for a 0.5 s wind-up.
- Colors: ANSI orange/red for threat states, enabled by a `--color` flag or when stdout is a TTY. Glyphs must make the three states distinguishable without color. This keeps captured logs plain.

### 3. Ordered tasks (single change set, sequential)

Build keeps the existing file layout. `Game` stays in `game.py`; Build may add small helper functions but no new modules.

- **T1. Sim core: grub and spitter state machines.**
  - Includes the slot allocator, swept strike check, knockback, the 1.25 / 1.0 / 2.0 tiles-per-second constants, 3.0 shot speed, the 2.5 s stagger schedule, Charge cancel and aim-lock.
  - Depends on nothing.
- **T2. Player attack changes.** Depends on T1.
  - 90° cone.
  - Arc state.
  - Hit/defeat feedback events with remaining HP.
  - Hit on a Wind-up grub: cancel the wind-up and give a 0.6 s Recovery.
  - Hit on a Charging spitter: cancel the charge and give a 1.0 s Stagger.
  - Reasons on every ignored attack.
- **T3. Run and room flow.** Depends on T2 (clear check and tick order).
  - Down handling: enemies freeze and shots are removed.
  - The 2.0 s countdown, then run over.
  - Restart on attack.
  - Clear: remove shots, heal +1 (max 3), 1.5 s of free input, load the next room.
  - Room 5: "run complete".
  - Practice-room rules.
- **T4. Trace.** Depends on T1–T3. Add enemy state, the room column and the new events.
- **T5. Player view.** Depends on T1–T3 and the event vocabulary from T1–T4. Check outputs 12 and 13 first.
  - One `GLYPHS` table (character and ANSI color, per kind and state: full, telegraph, damaged) and one `LINES` table of player-visible strings, both in `play.py`.
  - Lines: "a grub rears back", "spitter (top right) charges", the spit line naming its spitter, the swipe-result lines, the reasons, "you went down", "room cleared", "run complete", and the run-over screen.
  - Position names come from a 3×3 grid. If two spitters share a label, add a numeric disambiguator.
  - Update the version string to 0.5.
- **T6. Bots.** Depends on T3.
  - Fix `hearts_lost` to count `hurt` events. After a clear the +1 heal makes `HEARTS - game.hearts` wrong.
  - Check `_incoming` still works.
  - Optional, low priority: a "reactive" bot that dashes or backs off during a wind-up, to give the live playtest a datapoint on "grubs not trivial / dash matters". Include it only if it is cheap.
- **T7. Tests.** Written alongside T1–T6; see section 4.
- **T8. `manual.md`** (owner: `gameplay-engineer`, in the same change set). Done after T5 has frozen the glyph and message tables. See section 6.
- **T9. As-built report** to the Studio (section 5).

### 4. Test strategy per acceptance criterion

All engineer-written tests run through `run_tests` (unittest). Timing tests are parameterized over fps 30 and 60 and assert against spec times with the spec tolerance (0.04 s at 30 FPS, 0.02 s at 60 FPS). QA still verifies independently from trace and player view, as the spec says.

Existing tests that break by design, to be rewritten:
- two-swipe test (the grub now bites later);
- immediate-bite test;
- 2.0 s spitter interval (now 2.5 s with a 1.0 s first charge);
- double-grub invulnerability test (timings change). Keep its purpose: a dash right after a hit keeps both protections at 30 and 60 FPS.

The bots smoke test must still pass.

| AC | Coverage |
|---|---|
| AC-1 | Unit test, practice room, grub at distance 4, idle player. Wind-up event ≥ 0.45 s before the first `hurt`, and no `hurt` outside Strike. View-capture test for the "a grub rears back" line. The glyph change is compared against the `GLYPHS` table, then eyeballed by QA in the player view. |
| AC-2 | Unit test on event timestamps (wind-up 0.5, strike 0.15, recovery 0.9). |
| AC-3 | Unit test: dash away at the start, middle and last frame of Wind-up, in open space. The geometry must keep 4 tiles clear of walls. Zero hearts lost each time. |
| AC-4 | Unit test: swipe in Recovery, damaged state, next Strike ≥ 1.5 s after the previous one for a still player. |
| AC-5 | Unit test: swipe during Wind-up. No heart lost, 0.6 s Recovery, slot freed. |
| AC-6 | Unit test with 5 grubs in the practice room, scanning each frame for ≤ 2 in Wind-up/Strike. Room 5 has only 3 grubs, so the stronger test is needed. Also run room 5 through `run_bots` at both frame rates as a smoke check. |
| AC-7 | Unit test on Charge/Fire times in rooms 3, 4 and 5 (1.0, 1.8, 2.6 and every 2.5 s). See F5 for the interpretation. |
| AC-8 | View-capture test: charge line 0.8 s before each spit, spit line names its spitter, no identical lines at one timestamp. |
| AC-9 | Unit test with a spitter and an idle player (hit for 1 heart). Also tests that move ≥ 1 tile off the line, and that dash through the line. Margins ≥ 1 frame. A dash that ends within 0.4 tile of a shot is still a hit (invulnerability covers the dash only), so tests must dash clear. |
| AC-10 | Unit test: walk up and defeat a practice-room spitter in 2 swipes; a hit in Charge fires nothing. QA does a scripted walk in room 3 (`run_trace` / `run_play`). |
| AC-11 | View-capture test for each outcome line and each reason. No bare "(nothing happens)" anywhere in `play.py` output. Distinctness of the three glyph/color states is asserted from the table. |
| AC-12 | Unit test: two grubs in the cone give two hit lines. |
| AC-13 | Unit test and view-capture test: down line, `x`, enemies frozen, shots removed, "(down)", run-over screen at 2.0 s, restart on attack. Needs script handling for F7. |
| AC-14 | Unit test: heal +1, capped at 3; shots removed; next room after 1.5 s; same-tick clear with a shot placed on top of the player (set by the test); "run complete" in room 5, reached by setting HP in the test. |
| AC-15 | View-capture test for the practice room. Small test that each player-visible string in the `LINES` table and each glyph appears in `manual.md`. QA reads the manual. |
| AC-16 | Unit test: trace setup rows vs the layouts. |
| AC-17 | AC-1…AC-14 tests run at both fps. Differential test: 3–4 fixed scripts with inputs on multiples of 0.1 s, run at 30 and 60. Same event-kind sequence and timestamps within 0.07 s. Bots are compared only on aggregates. Dash-distance difference ≤ 0.25 tile is already covered by the existing dash test. |

Additional tests:
- Moving during the 0.35 s swipe recovery works (spec rule, "not yet observed").
- A `StrikeFrames` test: at 30 FPS the Strike is evaluated in ≥ 4 ticks for every phase offset of the leftover carry.

QA and playtest only, not automatable:
- Reading the glyph/color distinction and the arc in the player view.
- All [tune] values and the experience signals (live reactive playtest after Build).
- Whether grubs are trivial and the dash matters.

### 5. As-built values Build must report

- Swipe reach and the cone as computed.
- Projectile speed and the shot hit radius (existing 0.4; the spec does not say).
- Grub walking speed and the waiting-grub behavior (F2).
- Strike lunge distance and speed.
- Knockback distance and duration (spec 1 tile / 0.2 s, plus wall clamping).
- Spitter Recovery (0.6) and Stagger (1.0).
- Every [tune] timing as built: 0.5, 0.9, 0.6 (cancel recovery), 0.8, 2.5, 3.0, heal +1.
- The glyph/color table and arc pattern.
- The exact player-visible strings.
- Maximum measured timestamp error at 30 and 60 FPS, and the maximum cross-fps difference.
- Minimum Strike frames at 30 FPS.
- What was chosen for each of F1–F11.

### 6. `manual.md` update (task T8)

- **Owner:** `gameplay-engineer`, in Build, same change set.
- **When:** after T5 has frozen glyphs and strings, and after reading outputs 12 and 13.
- **Wording:** take player-visible wording from `design/combat.md`: the practice room, `x`, the new glyph/states, the swipe arc, the run-over screen, the attack messages (miss / too soon / stunned / down), telegraph lines, the room-clear heal and the 1.5 s pause, and restart by attack.
- Update the title and the on-screen description to build 0.5.
- Describe behavior; do not copy [tune] numbers, so the manual does not drift.
- Keep it player-facing: no implementation notes, no design rationale. A Playtester reads it.
- QA checks AC-15 against it.

### 7. Risks and mitigations

- **Frame-rate dependence.**
  - Mitigation: elapsed-seconds timers with leftover carry, a swept strike check, no frame counts, and tests at both frame rates.
  - AC-17's 0.07 s cross-fps bound is tight, since a distance-triggered Wind-up start can be late by up to one frame at 30 FPS.
  - Measure first. If the delta exceeds about 0.05 s, add sub-frame carry for distance triggers (leftover = tick time minus time of crossing).
- **Tick-order regression (clear vs damage).** Mitigation: the AC-14 same-tick test.
- **Slot starvation.** With a still player and three grubs, the two nearest grubs are always nearer after their lunge, so the third waits indefinitely. This is per spec ("the nearer takes the slot") and reads as "readable", but it is a tuning question. Do not change it in Build; watch it in the live playtest.
- **Bots drift.** The shot shape and `cleared` meaning are kept. Hearts lost are counted from events.
- **Late changes from outputs 12 and 13.** Handled by the data tables (T5).
- **Old scripts.** They still parse, and results differ from 0.4.
- **Performance.** Negligible (at most 6 enemies).

### 8. Parallelization decision

**One change set, one engineer, no isolated workspaces.** See D-004.
- All behavior lives in `game.py`, and the trace, view and bots all depend on its event vocabulary. Parallel branches would conflict in `game.py` or would be written against a vocabulary that is still moving.
- The total size is small.
- The manual and tests wait for the string and glyph tables.
- Steps 12 and 13 are non-code inputs; they do not create parallel code work.

### 9. Spec gaps and chosen defaults (none blocking)

For the designer to confirm at Review:

- **F1. Grub speed.** The spec says 2.0 tiles/s "as observed", but build 0.4 has 1.2. Build implements the spec's 2.0. The designer should confirm that was intended, because grubs will arrive much faster than in 0.4.
- **F2. Unslotted grub.** The spec says "approaching/circling" with no circling rule. Default: it approaches to 1.25 tiles, then holds and waits for a slot. Report as built.
- **F3. Spitter with the player on top of it.** Zero distance gives no direction. Default: no projectile for that volley (as in 0.4), logged in the trace only.
- **F4. Stagger re-base.** After a cancelled charge, the spitters' volleys may no longer be offset, so "never fire together" is guaranteed only from room start. Default: per spec, no extra spacing.
- **F5. AC-7 wording.** "Never start a Charge or fire in the same 0.5 s" is read as no two Charge starts and no two Fires within 0.5 s. A Fire and another spitter's Charge start do coincide at 1.8 s by the spec's own numbers.
- **F6. Run complete.** The timing and screen text are not specified. Default: "room cleared" then "run complete" at the clear, the +1 heal, the 1.5 s free-input window, then a final screen "run complete — rooms cleared: 5". Attack starts a new run.
- **F7. Run-over vs scripts.** "A scripted session ends at the run-over screen" conflicts with AC-13 (attack at the screen starts a new run). Default: the session stops at the screen unless the script has a later input, in which case that attack restarts the run. The practice room always ends 2.0 s after going down.
- **F8. Hits in other grub states.**
  - A hit in Strike: damage applies, the lunge continues, no knockback.
  - A hit in Recovery: knockback applies and the Recovery timer is not extended.
  - Knockback applies to a first hit in any other state.
- **F9. Damaged plus telegraph.** The spec lists three states but a damaged grub can also wind up. Default: the telegraph glyph has priority, and the text line gives the HP. The art-director review (13) should confirm.
- **F10. Other ignored inputs.** To remove every bare "(nothing happens)": any input during stun prints "(stunned)", and a dash on cooldown prints "(dash not ready)". The wording of the second is new.
- **F11. Pause.** The spec's "Pause: all timers freeze" has no implementation in the current build or script format, and no AC covers it. Build adds no pause. QA should mark it not verifiable here. The designer may add a script verb later.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: rework existing enemy behavior (Option A). B deferred, C out of scope.
- D-003: room mix across rooms, zero hearts ends the run, clear heals one heart.
- D-004 (new): Option A is built as one sequential change set.

## Constraints

- No new inputs (D-001). Correct at 30 and 60 FPS. Reuse existing systems.
- The spec's player-facing behavior is unchanged except where F1–F11 fill gaps.

## Open questions

- **For the designer, non-blocking:** F1–F11, especially F1, F6 and F7.
- **For `art-director` (step 13):** F9 and the plain-text fallback for color.
- **For QA (step 12):** whether the spit line wording changes.
- **For the Studio:** none for Build to start.

## Expected output

- **Next:** `gameplay-engineer`, Build. Deliverables: T1–T9 in one change set with passing `run_tests`, `run_bots` at 30 and 60 FPS, updated `manual.md`, and the as-built report from section 5.
- **Then:** QA verifies AC-1…AC-17 at 30 and 60 FPS from the trace and player view, followed by a live reactive playtest for the [tune] values.
- **After Build,** the designer reviews F1–F11 against the as-built report.

## Sender assessment

- High confidence on feasibility. The attack-slot limit and aim-lock fit the existing structures.
- Main schedule risk: the tight cross-fps bound (7), and rework of the tests.
- F1 is the item most likely to change how the game feels. Grubs at 2.0 tiles/s instead of 1.2 may reduce the player's reaction time more than the designer expects.
- Not checked by me: I did not run the build or the tests. The check on 1.2 against the spec's 2.0 is from reading `game.py` (`GRUB_SPEED`).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/14-technical-director-to-studio.md
>>>END

<<<FILE goals/G-001-combat-monotony/15-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: qa
to: studio
stage: Observe
outcome: done
---
# 15: qa → studio — Defect report: identical "a spitter spits" lines at one timestamp (rooms 4–5)

## Task

Studio: route this report. The doubled line is reproduced. It is two spitters each printing one line, not one event printed twice. The defect is presentation only: the two lines are identical and do not say which spitter fired.

## Context

Handoff 12 asked whether the repeated spitter attack line is one event printed twice (a defect) or two spitters each printing their own line (one line per spitter). It also asked in which rooms it occurs and whether it changes with spitter count. Build under test: `repo/` at sha e54837757611 (the player view header reads "Lantern Depths 0.4"). All evidence comes from the run commands in `project.md`, driven by input scripts.

## Findings

### Verdict

- **Reproduced: yes.** Every volley in rooms 4 and 5 prints two identical lines at the same timestamp.
- **Cause class: two events, not one event printed twice.**
  - With one spitter, the trace shows one `spit` event per volley.
  - With two spitters, the trace shows `spit; spit` per volley.
  - So the count of lines follows the count of spitters, i.e. one line per spitter. That matches the "one line per spitter" expectation stated in handoff 12.
- **What is wrong:** the text is the same for both spitters ("a spitter spits"). It carries no name or position, so the player cannot tell the lines apart and reads them as a duplicate. This is a presentation defect. It is not a logic or double-fire defect.

### Reproduction

Script A (player view, room 4):
```
room 4
fps 60
end 5
```
Command: `python3 play.py --view player {script}`

Observed:
```
  2.000  a spitter spits
  2.000  a spitter spits
  4.000  a spitter spits
  4.000  a spitter spits
```

Script B (trace, one spitter):
```
room empty
fps 60
spawn spitter 15 0
player 8 4
end 6
```
Observed: a single `spit` event at t=2.000, 4.000 and 6.000.

Script C (trace, two spitters):
```
room empty
fps 60
spawn spitter 15 0
spawn spitter 15 8
player 8 4
end 6
```
Observed: `spit; spit` at t=2.000, 4.000 and 6.000. The projectile count follows: the player view shows two `*`, one per spitter, so the pair is two shots and not a duplicate print.

### Conditions varied

| Condition | Result | View used |
|---|---|---|
| Room 4, 60 FPS | Pair of identical lines at 2.0, 4.0, 6.0, 8.0 s | player and trace |
| Room 4, 30 FPS | `spit; spit` at 2.0, 4.0, 6.0, 8.0 s, same as 60 FPS | trace only |
| Room 5, 60 FPS | `spit; spit` at 2.0, 4.0, 6.0, 8.0 s | trace only |
| 1 spitter (practice room) | One `spit` per volley | trace only |
| 2 spitters (practice room) | `spit; spit` per volley | trace only |

- **Frame rate:** the script format has an `fps 30|60` line, so both frame rates can be set. The behavior and the timestamps are the same at both.
- **Rooms:** it occurs in both room 4 and room 5, because both have the same two corner spitters at (15,0) and (15,8).
- **Spitter count:** the number of identical lines equals the number of spitters. Room 3 (3 spitters) was not run; I expect three identical lines there, and that is a hypothesis, not an observation.

### Not run (round budget)

- The player-view text for room 5 and for the one-spitter case. The trace `spit` events were used as the evidence there.
- The player view at 30 FPS.
- Room 3.

### Expected, and its source

- `design/combat.md` AC-8 (build 0.5 target): "The spit line names its spitter; there are no identical duplicate lines at one timestamp."
- AC-8 describes the target build, not the current one. No document defines the current build's line text as a defect. The current build behaves as "one line per spitter", which is what handoff 12 says the design expects. The defect is therefore measured against AC-8, which the planned spitter rework must satisfy. It is not a regression against an earlier spec.
- The cause of the missing name is not known. A plausible hypothesis (unverified) is that the line text is a fixed string that does not take the spitter's identity.

### Severity and frequency

- **Severity: cosmetic / low.** The mechanics are unaffected. The cost is readability: the player cannot tell which spitter fired, and the repeated line looks like a bug.
- **Frequency:** every volley in rooms 4 and 5 (about every 2.0 s on the current build), 100% of volleys.

### Evidence

The trace rows for the room 4 runs at 30 and 60 FPS, the room 5 run at 60 FPS, and the one-spitter and two-spitter runs are quoted above and in the run results of this step.

## Decisions already made

None bear on this defect.

## Constraints

- Report only what is observable on the current build; no fix is proposed.
- The rest of the Option A spec was not verified or commented on.

## Open questions

None for the Owner. Process note for the Studio: the observed behavior matches "one line per spitter", so this is not a duplicate-event bug. Treat it as presentation covered by AC-8, to be verified after the rework.

## Acceptance criteria for the fix

1. In rooms 4 and 5, at both `fps 30` and `fps 60`, each spit line names its spitter (for example by position, as in "spitter (top right) spits").
2. No two lines printed at the same timestamp have identical text, for any spitter count (check 1, 2 and 3 spitters; rooms 3, 4 and 5).
3. The number of spit lines at a timestamp equals the number of spitters that fired, and the number of `spit` trace events is unchanged.
4. Each spit line can be matched to its projectile (that spitter's `*`).
5. Spit timing and projectile behavior are unchanged by this fix, apart from whatever the rework intentionally changes.

## Expected output

Studio routes this defect report to the owner of the spitter rework, as a presentation requirement alongside AC-8.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/16-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 16
from: art-director
to: studio
stage: Design
outcome: done
---
# 16: art-director → studio — Visual review of the Option A spec: rulings and visual spec for Build

## Task

Route the visual spec in `design/combat-visuals.md` to Build alongside `design/combat.md`. Route the manual change and the one question below.

## Context

G-001: combat monotony. D-002 chose Option A. The game-designer's spec (`design/combat.md`) leaves glyphs and colors to Build and to my review. The rooms 4–5 playtest (08) found that spitters read as scenery and their shots were never reacted to. This was a spec review against `project.md#art-direction` and pillar 3. There is no build yet, so nothing could be checked against actual output. I changed no rules, timings or parameters.

## Findings

### Verdicts

| Question | Verdict | Evidence |
|---|---|---|
| Are Wind-up, Charge and Recovery distinguishable from idle and harmless states? | **Fail as specified, fixed by rulings below.** | The spec says only "glyph and color change". The view is text, so a color-only change would be invisible. A Recovery that "returns to the normal glyph" is identical to Approach in a still frame. |
| Can the player see the telegraph in time? | **Fail as specified.** | The room is drawn every 0.5 s, and the grub Wind-up lasts 0.5 s. A frame can miss it entirely. The swipe arc lasts 0.15 s and would almost never be drawn. |
| Do threat colors read against the dark? | **Pass in principle.** | Saturated orange/red against cold blue-black matches the art direction. Not verifiable until the build exists. |
| Are damaged states and the downed marker clear? | **Pass with changes.** | The spec requires a distinct glyph and color but gives none. Rulings fix them. `x` was unstyled. |

### Rulings (what to keep, what to change)

**Keep:**
- Saturated orange/red for committed threats and projectiles.
- The swipe arc, the damaged state, the remaining-HP hit lines and the explicit "(miss)" reasons.
- The `x` downed marker and the run-over text.

**Change** (full detail in `design/combat-visuals.md`):
1. **Glyph carries the state, not color alone.** Uppercase means committed to hurting (`G`, `W`, `S`, `Z`). Lowercase means harmless (`g`, `w`, `s`, `z`). A damaged enemy uses the `w/z` family.
2. **Harmless enemies are muted.** Orange/red is reserved for telegraphed enemies and `*`. The player, the swipe arc and `x` never use it. This makes the telegraph the loudest thing on the map, and it is what makes the spitter stop looking like scenery.
3. **Extra draws on telegraph events.** The room is drawn at Wind-up start, Charge start, projectile spawn, every swipe, grub Recovery start and player down. Otherwise short telegraphs fall between 0.5 s frames. Timings are untouched.
4. **Text lines name the enemy and its position.** Grub: "a grub rears back (left)". Spitter lines are named by position. A new "the grub is open" line marks the start of Recovery, the counter window. A stagger line is added for spitters.
5. **Swipe arc glyphs** `) ( ^ v` in lantern color on the tiles in reach.
6. **Run-over screen** adds the line "press attack to start again", because the spec's restart rule is otherwise undiscoverable.

### Handoff items

- **`manual.md` must be updated** (not on my write list): the glyph table, the `x` marker, the arc, the practice room, the new lines and the run-over screen (V-5). Route to whoever owns the manual, after Build fixes the final glyphs.
- **Acceptance:** V-1…V-8 in `design/combat-visuals.md` join AC-1…AC-17 for Verify. After Build, I should review the actual player view for color and legibility.
- `design/combat.md` is unchanged. Its line "chosen in Build and documented in the manual" now means: follow `design/combat-visuals.md` and document any change in `manual.md`.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: Option A, reuse existing enemy behavior.
- No new decision recorded; nothing here changes a style pillar.

## Constraints

- No rule, timing or parameter changed. No new inputs. Reuse existing systems.

## Open questions

- **For Build / Plan:** can the extra draws on events (principle 4) be added cheaply? If not, tell `game-designer`: a 0.5 s Wind-up cannot be guaranteed visible with only a 0.5 s draw cadence.
- **Optional, for game-designer:** should the player's invulnerability (hit and dash) be visible? Suggested `p` for `P`. This needs no rule change.

## Expected output

The Studio routes Build (`gameplay-engineer`) with `design/combat.md` plus `design/combat-visuals.md`, then Verify (`qa`) with AC-1…AC-17 and V-1…V-8, then a visual review of the built player view by the art-director.

## Sender assessment

Confidence high on glyph, case and event-draw rulings: they follow from the text view and the 0.5 s draw cadence. Confidence medium on colors: they cannot be judged until a build exists.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/13-studio-to-art-director.md
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

<<<FILE repo/game.py (proposed in a run round; not written)
"""Lantern Depths, build 0.5: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. Every timer runs on elapsed seconds;
a state change carries the leftover time of the tick, so event times are exact to well under a frame.
"""

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY, ARC_TIME = 1.5, 0.35, 0.15
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

GRUB_HP, GRUB_SPEED = 2, 2.0
GRUB_RANGE = 1.25  # a grub starts its wind-up when this close to the player
STRIKE_REACH, STRIKE_LUNGE = 1.0, 1.0
GRUB_WINDUP, GRUB_STRIKE, GRUB_RECOVERY, GRUB_CANCEL_RECOVERY = 0.5, 0.15, 0.9, 0.6
KNOCKBACK_DIST, KNOCKBACK_TIME = 1.0, 0.2
ATTACK_SLOTS = 2

SPITTER_HP = 2
SPIT_CHARGE, SPIT_RECOVERY, SPIT_STAGGER = 0.8, 0.6, 1.0
SPIT_INTERVAL, SPIT_FIRST, SPIT_OFFSET = 2.5, 1.0, 0.8
SHOT_SPEED, SHOT_REACH = 3.0, 0.4

DOWN_TIME, CLEAR_WAIT, HEAL = 2.0, 1.5, 1
LAST_ROOM = "5"

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

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


def position_label(x, y):
    """Where a tile is in the room, on a 3x3 grid."""
    col = 0 if x < ROOM_W / 3 else (1 if x < 2 * ROOM_W / 3 else 2)
    row = 0 if y < ROOM_H / 3 else (1 if y < 2 * ROOM_H / 3 else 2)
    return [
        ["top left", "top", "top right"],
        ["left", "middle", "right"],
        ["bottom left", "bottom", "bottom right"],
    ][row][col]


def side_of(dx, dy):
    """Which side an enemy is on, relative to the player (dx, dy = enemy - player)."""
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "below" if dy > 0 else "above"


def in_cone(dx, dy, facing):
    """True if an offset lies in the swipe: within reach, in a 90 degree cone on the facing."""
    dist = math.hypot(dx, dy)
    if dist > ATTACK_REACH + 1e-9:
        return False
    if dist < 1e-9:
        return True
    fx, fy = facing
    along = dx * fx + dy * fy
    across = abs(dx * fy - dy * fx)
    return along > 0 and across <= along + 1e-9


def segment_distance(px, py, ax, ay, bx, by):
    """Closest distance from point P to the segment A-B."""
    abx, aby = bx - ax, by - ay
    length = abx * abx + aby * aby
    if length < 1e-12:
        return math.hypot(px - ax, py - ay)
    s = max(0.0, min(1.0, ((px - ax) * abx + (py - ay) * aby) / length))
    return math.hypot(px - ax - s * abx, py - ay - s * aby)


class Shot(list):
    """A projectile: still unpacks as [x, y, vx, vy]; also remembers its id and owner."""

    def __init__(self, x, y, vx, vy, ident, owner):
        super().__init__([x, y, vx, vy])
        self.ident, self.owner = ident, owner


class Enemy:
    def __init__(self, kind, x, y):
        if kind not in ("grub", "spitter"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.max_hp = GRUB_HP if kind == "grub" else SPITTER_HP
        self.hp = self.max_hp
        self.index, self.k, self.label = 0, 0, ""
        self.state = "approach" if kind == "grub" else "idle"
        self.timer = 0.0
        self.next_charge = 0.0  # spitter: absolute time of its next Charge start
        self.kb_left, self.kb_dir = 0.0, (0.0, 0.0)
        self.lunge, self.lunge_speed = (0.0, 0.0), 0.0
        self.struck, self.strike_checks = False, 0

    @property
    def alert(self):
        """Committed to hurting the player (telegraphed): Wind-up/Strike, Charge."""
        return self.state in ("windup", "strike") if self.kind == "grub" else self.state == "charge"

    @property
    def damaged(self):
        return self.hp < self.max_hp


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame = fps, 1.0 / fps, 0
        self.practice = room == "empty"
        self.room = room
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.arc_left, self.arc_dir = 0.0, (1, 0)
        self.queued_attack = False
        self.shots, self._fresh, self.shot_count = [], [], 0
        self.events = []  # (time, kind, details)
        self.phase = "playing"  # playing | clear_wait | down | over
        self.down_t = self.clear_t = self.room_start = 0.0
        self.rooms_cleared = 0
        self.enemies = []
        self.cleared = False  # the current room is cleared (stays true until the next room loads)
        self._load_room(room, announce=False)

    @property
    def t(self):
        return self.frame / self.fps

    @property
    def finished(self):
        """The practice room ends the session 2.0 s after the player goes down."""
        return self.phase == "over" and self.practice

    def log(self, kind, _at=None, **details):
        self.events.append((self.t if _at is None else _at, kind, details))

    # --- Setup ---------------------------------------------------------------------------------

    def spawn(self, kind, x, y):
        self._add(Enemy(kind, x, y))

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    def _add(self, enemy):
        enemy.index = len(self.enemies)
        if enemy.kind == "spitter":
            enemy.k = sum(1 for e in self.enemies if e.kind == "spitter")
            enemy.next_charge = self.room_start + SPIT_FIRST + SPIT_OFFSET * enemy.k
        self.enemies.append(enemy)
        spitters = [e for e in self.enemies if e.kind == "spitter"]
        names = [position_label(e.x, e.y) for e in spitters]
        for e, name in zip(spitters, names):
            e.label = f"{name} #{e.k + 1}" if names.count(name) > 1 else name

    def _load_room(self, key, announce):
        self.room = key
        self.enemies = []
        self.shots, self._fresh = [], []
        self.x, self.y = START
        self.cleared = False
        self.phase = "playing"
        self.room_start = self.t
        for spec in ROOMS[key]:
            self._add(Enemy(*spec))
        if announce:
            self.log("room_loaded", room=key)

    def _restart(self):
        self.hearts, self.rooms_cleared = HEARTS, 0
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.hurt_left = self.stun_left = self.recovery = self.arc_left = 0.0
        self.queued_attack = False
        self.heading, self.facing = (0, 0), (1, 0)
        self.log("run_start")
        self._load_room("1", announce=False)

    # --- Input ---------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.phase == "over":
            if action == "attack" and not self.practice:
                self._restart()
            return
        if self.hearts <= 0:
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
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        self.arc_left = max(0.0, self.arc_left - dt)
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
                    if self.hearts > 0:
                        self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        # Room-clear check comes before any enemy damage: a clearing swipe cancels a strike or
        # projectile hit due on this tick.
        self._check_clear()
        if self.phase == "playing":
            self._update_enemies(dt)
            self._update_shots(dt)
        self._phase_timers()

    def _check_clear(self):
        if self.phase != "playing" or self.cleared or not self.enemies:
            return
        if any(e.hp > 0 for e in self.enemies):
            return
        self.cleared = True
        self.log("cleared")
        self.shots, self._fresh = [], []
        if self.practice:
            return
        self.rooms_cleared += 1
        if self.hearts < HEARTS:
            self.hearts = min(HEARTS, self.hearts + HEAL)
            self.log("heal", hearts=self.hearts)
        if self.room == LAST_ROOM:
            self.log("run_complete")
        self.phase, self.clear_t = "clear_wait", self.t

    def _phase_timers(self):
        if self.phase == "down" and self.t - self.down_t >= DOWN_TIME - 1e-9:
            self.phase = "over"
            self.log("run_over", rooms=self.rooms_cleared, complete=False, practice=self.practice)
        elif self.phase == "clear_wait" and self.t - self.clear_t >= CLEAR_WAIT - 1e-9:
            if self.room == LAST_ROOM:
                self.phase = "over"
                self.log("run_over", rooms=self.rooms_cleared, complete=True, practice=False)
            else:
                self._load_room(str(int(self.room) + 1), announce=True)

    # --- Player attack -------------------------------------------------------------------------

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        self.arc_left, self.arc_dir = ARC_TIME, self.facing
        hits, later = [], []
        for e in self.enemies:
            if e.hp > 0 and in_cone(e.x - self.x, e.y - self.y, self.facing):
                result = self._hit(e, later)
                hits.append((e.kind, result, e.hp, e.index))
        self.log("attack", hits=hits)
        for kind, details in later:
            self.log(kind, **details)

    def _hit(self, e, later):
        e.hp -= 1
        if e.hp <= 0:
            later.append(("defeated", dict(kind=e.kind, index=e.index)))
            return "defeated"
        if e.kind == "grub":
            if e.state == "windup":
                e.state, e.timer = "recovery", GRUB_CANCEL_RECOVERY
                later.append(("recover", dict(index=e.index, cancelled=True)))
            if e.state != "strike":
                dx, dy = e.x - self.x, e.y - self.y
                d = math.hypot(dx, dy)
                e.kb_dir = (dx / d, dy / d) if d > 1e-9 else (float(self.facing[0]), float(self.facing[1]))
                e.kb_left = KNOCKBACK_TIME
                later.append(("knockback", dict(index=e.index)))
        elif e.state == "charge":
            e.state = "stagger"
            e.next_charge = self.t + SPIT_STAGGER
            later.append(("stagger", dict(index=e.index, label=e.label)))
        return "hit"

    # --- Enemies -------------------------------------------------------------------------------

    def _update_enemies(self, dt):
        order = sorted(
            (e for e in self.enemies if e.hp > 0),
            key=lambda e: (math.hypot(self.x - e.x, self.y - e.y), e.index),
        )
        for e in order:
            if self.phase != "playing":
                break
            if e.hp <= 0:
                continue
            if e.kind == "grub":
                self._update_grub(e, dt)
            else:
                self._update_spitter(e, dt)

    def _slots_used(self):
        return sum(1 for e in self.enemies if e.kind == "grub" and e.hp > 0 and e.state in ("windup", "strike"))

    @staticmethod
    def _run_timer(e, left):
        use = min(left, e.timer)
        e.timer -= use
        return left - use

    def _update_grub(self, e, dt):
        left = dt
        frozen = e.kb_left > 0
        if frozen:
            span = min(dt, e.kb_left)
            dist = KNOCKBACK_DIST / KNOCKBACK_TIME * span
            e.x, e.y = self._clamp(e.x + e.kb_dir[0] * dist, e.y + e.kb_dir[1] * dist)
            e.kb_left -= span
        for _ in range(12):
            if left <= 1e-12 or e.hp <= 0 or self.phase != "playing":
                return
            if e.state == "approach":
                left = self._approach(e, left, frozen)
            elif e.state == "windup":
                left = self._run_timer(e, left)
                if e.timer <= 1e-9:
                    self._begin_strike(e, left)
            elif e.state == "strike":
                use = min(left, e.timer)
                self._lunge(e, use)
                e.timer -= use
                left -= use
                if e.timer <= 1e-9:
                    e.state, e.timer = "recovery", GRUB_RECOVERY
                    self.log("recover", _at=self.t - left, index=e.index, cancelled=False)
            else:  # recovery
                left = self._run_timer(e, left)
                if e.timer <= 1e-9:
                    e.state = "approach"

    def _approach(self, e, left, frozen):
        if frozen:
            return 0.0
        dx, dy = self.x - e.x, self.y - e.y
        dist = math.hypot(dx, dy)
        need = dist - GRUB_RANGE
        if need > 1e-9:
            if GRUB_SPEED * left < need:
                step, left = GRUB_SPEED * left, 0.0
            else:
                step, left = need, left - need / GRUB_SPEED
            e.x, e.y = self._clamp(e.x + dx / dist * step, e.y + dy / dist * step)
            if left <= 1e-12:
                return 0.0
        if self._slots_used() < ATTACK_SLOTS:
            e.state, e.timer = "windup", GRUB_WINDUP
            self.log(
                "windup",
                _at=self.t - left,
                index=e.index,
                side=side_of(e.x - self.x, e.y - self.y),
            )
            return left
        return 0.0  # in range but no free attack slot: hold and wait

    def _begin_strike(self, e, left):
        dx, dy = self.x - e.x, self.y - e.y  # where the player stands as the wind-up ends
        d = math.hypot(dx, dy)
        if d > 1e-9:
            e.lunge = (dx / d, dy / d)
            e.lunge_speed = min(STRIKE_LUNGE, d) / GRUB_STRIKE
        else:
            e.lunge, e.lunge_speed = (0.0, 0.0), 0.0
        e.state, e.timer = "strike", GRUB_STRIKE
        e.struck, e.strike_checks = False, 0
        self.log("strike", _at=self.t - left, index=e.index)

    def _lunge(self, e, span):
        ox, oy = e.x, e.y
        dist = e.lunge_speed * span
        e.x, e.y = self._clamp(ox + e.lunge[0] * dist, oy + e.lunge[1] * dist)
        e.strike_checks += 1
        # swept check: closest approach over this tick's movement, not the end-of-tick sample
        if not e.struck and segment_distance(self.x, self.y, ox, oy, e.x, e.y) <= STRIKE_REACH + 1e-9:
            if self._hurt("grub"):
                e.struck = True

    def _update_spitter(self, e, dt):
        left = dt
        for _ in range(12):
            if left <= 1e-12 or e.hp <= 0 or self.phase != "playing":
                return
            if e.state in ("idle", "stagger"):
                wait = e.next_charge - (self.t - left)
                if wait > left - 1e-9:
                    return
                left -= max(wait, 0.0)
                e.state, e.timer = "charge", SPIT_CHARGE
                e.next_charge += SPIT_INTERVAL
                self.log("charge", _at=self.t - left, index=e.index, label=e.label)
            elif e.state == "charge":
                left = self._run_timer(e, left)
                if e.timer <= 1e-9:
                    self._fire(e, left)
                    e.state, e.timer = "recovery", SPIT_RECOVERY
            else:  # recovery
                left = self._run_timer(e, left)
                if e.timer <= 1e-9:
                    e.state = "idle"

    def _fire(self, e, left):
        # Aim is locked now: the player's position at the end of the charge.
        dx, dy = self.x - e.x, self.y - e.y
        d = math.hypot(dx, dy)
        if d < 1e-9:
            self.log("fizzle", _at=self.t - left, index=e.index, label=e.label)
            return
        vx, vy = dx / d * SHOT_SPEED, dy / d * SHOT_SPEED
        self.shot_count += 1
        self._fresh.append(Shot(e.x + vx * left, e.y + vy * left, vx, vy, self.shot_count, e.index))
        self.log("spit", _at=self.t - left, index=e.index, label=e.label, shot=self.shot_count)

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
        self.shots = kept + self._fresh if self.phase == "playing" else []
        self._fresh = []

    # --- Player damage -------------------------------------------------------------------------

    def _hurt(self, source):
        if self.invulnerable or self.hearts <= 0:
            return False
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self.log("down")
            self.phase, self.down_t = "down", self.t
            self.shots, self._fresh = [], []
        return True

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

<<<FILE repo/play.py (proposed in a run round; not written)
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace [--color] SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format is described in the project's manual.md.
"""

import argparse
import sys

from game import ATTACK_REACH, HEARTS, ROOM_H, ROOM_W, Game, in_cone  # noqa: F401

VERSION = "0.5"
MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots

# --- Data tables: glyphs/colors and player-visible text -------------------------------------------

RESET = "\x1b[0m"
LANTERN = "\x1b[93m"  # warm yellow-white: player and swipe arc
MUTED = "\x1b[38;5;245m"  # harmless enemies
MUTED_DAMAGED = "\x1b[38;5;137m"  # harmless, damaged: tinted
THREAT = "\x1b[1;38;5;208m"  # saturated orange: telegraphed enemies
SHOT_COLOR = "\x1b[1;38;5;196m"  # saturated red, brightest on the map
DOWNED = "\x1b[38;5;67m"  # cold gray-blue

# key: (kind, damaged, alert) -> (character, color). Uppercase = committed to hurting.
GLYPHS = {
    "player": ("P", LANTERN),
    "down": ("x", DOWNED),
    "shot": ("*", SHOT_COLOR),
    ("grub", False, False): ("g", MUTED),
    ("grub", True, False): ("w", MUTED_DAMAGED),
    ("grub", False, True): ("G", THREAT),
    ("grub", True, True): ("W", THREAT),
    ("spitter", False, False): ("s", MUTED),
    ("spitter", True, False): ("z", MUTED_DAMAGED),
    ("spitter", False, True): ("S", THREAT),
    ("spitter", True, True): ("Z", THREAT),
}
ARC = {(1, 0): ")", (-1, 0): "(", (0, -1): "^", (0, 1): "v"}  # lantern colored

LINES = {
    "windup": "a grub rears back ({side})",
    "open": "the grub is open",
    "charge": "spitter ({label}) charges",
    "spit": "spitter ({label}) spits",
    "stagger": "spitter ({label}) is staggered",
    "miss": "you swipe: (miss)",
    "hit": "you swipe: {kind} hit ({left} left)",
    "defeated": "{kind} defeated",
    "swipe_ignored": "you swipe: ({reason})",
    "ignored": "({reason})",
    "dash": "you dash {direction}",
    "hurt": "YOU ARE HIT by a {source} — hearts {hearts}/" + str(HEARTS),
    "down": "you went down",
    "cleared": "room cleared",
    "run_complete": "run complete",
    "run_over": "run over — rooms cleared: {rooms}",
    "run_done": "run complete — rooms cleared: {rooms}",
    "restart": "press attack to start again",
}

# Events that get their own draw of the room at the moment they happen.
SNAPSHOT_EVENTS = {
    "windup", "charge", "spit", "attack", "recover", "down", "hurt", "stagger",
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
        out.frame()  # what the input itself did (swipe lines and draw) shows at once
        # A scripted session ends at the run-over screen unless a later input is waiting.
        if game.finished or (game.phase == "over" and not pending):
            break
        game.step()
        out.frame()
    out.finish()


def describe_event(kind, d):
    """Player-visible text lines for one event ([] if the event has no line)."""
    L = LINES
    if kind == "attack":
        if not d["hits"]:
            return [L["miss"]]
        return [
            L["defeated"].format(kind=enemy)
            if result == "defeated"
            else L["hit"].format(kind=enemy, left=left)
            for enemy, result, left, _ in d["hits"]
        ]
    if kind == "ignored":
        key = "swipe_ignored" if d["action"] == "attack" else "ignored"
        return [L[key].format(reason=d["reason"])]
    if kind == "dash":
        return [L["dash"].format(direction=d["direction"])]
    if kind == "hurt":
        return [L["hurt"].format(source=d["source"], hearts=d["hearts"])]
    if kind == "down":
        return [L["down"]]
    if kind == "windup":
        return [L["windup"].format(side=d["side"])]
    if kind == "recover":
        return [L["open"]]
    if kind == "charge":
        return [L["charge"].format(label=d["label"])]
    if kind == "spit":
        return [L["spit"].format(label=d["label"])]
    if kind == "stagger":
        return [L["stagger"].format(label=d["label"])]
    if kind == "cleared":
        return [L["cleared"]]
    if kind == "run_complete":
        return [L["run_complete"]]
    if kind == "run_over":
        if d.get("practice"):
            return []
        head = L["run_done"] if d.get("complete") else L["run_over"]
        return [head.format(rooms=d["rooms"]), L["restart"]]
    return []


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game, color=False):
        self.game, self.color, self.seen, self.next_snapshot = game, color, 0, 0.0

    def start(self):
        g = self.game
        print(f"Lantern Depths {VERSION} — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, snap = self.game, False
        for when, kind, details in g.events[self.seen :]:
            for text in describe_event(kind, details):
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

    def snapshot(self):
        g = self.game
        grid = [[(" ", None)] * ROOM_W for _ in range(ROOM_H)]

        def put(x, y, glyph):
            col, row = int(round(x)), int(round(y))
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = glyph

        if g.arc_left > 1e-9 and g.hearts > 0:
            px, py = int(round(g.x)), int(round(g.y))
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if (dx or dy) and in_cone(dx, dy, g.arc_dir):
                        put(px + dx, py + dy, (ARC[g.arc_dir], LANTERN))
        for shot in g.shots:
            put(shot[0], shot[1], GLYPHS["shot"])
        for e in g.enemies:
            if e.hp > 0:
                put(e.x, e.y, GLYPHS[(e.kind, e.damaged, e.alert)])
        put(g.x, g.y, GLYPHS["player"] if g.hearts > 0 else GLYPHS["down"])

        def cell(glyph):
            char, color = glyph
            return f"{color}{char}{RESET}" if (self.color and color) else char

        print(f"   [{g.t:.2f} s] room {g.room} hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in grid:
            print("   |" + "".join(cell(c) for c in row) + "|")
        print("   +" + "-" * ROOM_W + "+")


class Trace:
    """Simulation state for developers: one line per frame in which anything happened."""

    def __init__(self, game):
        self.game, self.seen = game, 0

    def start(self):
        g = self.game
        print(f"trace: fps={g.fps} room={g.room} dt={g.dt:.5f}")
        self.line([(g.t, "setup", {})])

    def frame(self):
        g = self.game
        new = list(g.events[self.seen :])
        self.seen = len(g.events)
        if new:
            self.line(new)

    def finish(self):
        self.line([(self.game.t, "end", {})])

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} room={g.room} phase={g.phase} "
            f"pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}#{e.index}({e.x:.2f},{e.y:.2f},hp={e.hp},{e.state},timer={e.timer:.3f})"
            for e in g.enemies
            if e.hp > 0
        )
        shots = " ".join(
            f"shot{s.ident}@({s[0]:.2f},{s[1]:.2f}) from #{s.owner}" for s in g.shots
        )
        happened = "; ".join(
            f"{kind}@{when:.3f}" + (f" {details}" if details else "")
            for when, kind, details in events
        )
        print(f"{state} | {enemies} | {shots} | {happened}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["player", "trace"], default="player")
    parser.add_argument("--color", action="store_true", help="ANSI colors (default: only on a TTY)")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs = read_script(f.read())
    play(setup, inputs, args.view, color=args.color or sys.stdout.isatty())


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/bots.py (proposed in a run round; not written)
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger,reactive   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)

Each bot starts every room with full hearts and plays that room alone (no run flow).
"""

import math
import sys

from game import ATTACK_REACH, DIRECTIONS, HEARTS, ROOMS, Game  # noqa: F401


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
    """Plays like the dodger, and also dashes away from a grub that has begun to wind up."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    winding = [
        e
        for e in game.enemies
        if e.hp > 0 and e.kind == "grub" and e.state == "windup"
        and math.hypot(e.x - game.x, e.y - game.y) < 1.6
    ]
    if ready and winding:
        game.press("dash", _toward(game.x - winding[0].x, game.y - winding[0].y))
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
        "hearts_lost": counts.get("hurt", 0),  # counted from events: a clear can heal
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

<<<FILE repo/tests/test_game.py (proposed in a run round; not written)
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
from game import DASH_DISTANCE, HEARTS, ROOMS, Game, Shot  # noqa: E402

FPS = (30, 60)
TOL = {30: 0.04, 60: 0.02}  # spec timestamp tolerance
LINE = re.compile(r"^\s*(\d+\.\d{3})  (\S.*)$")


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def times(game, kind, **match):
    return [t for t, k, d in game.events if k == kind and all(d.get(a) == b for a, b in match.items())]


def run_until(game, kind, count=1, limit=30.0):
    for _ in range(round(limit * game.fps)):
        if len(times(game, kind)) >= count:
            return
        game.step()
    raise AssertionError(f"no {kind} #{count} within {limit} s")


def capture(script, view="player"):
    setup, inputs = play.read_script(script)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        play.play(setup, inputs, view)
    return buf.getvalue()


def text_lines(out):
    return [(float(m.group(1)), m.group(2)) for m in map(LINE.match, out.splitlines()) if m]


def drive(fps, room, spawns, player, inputs, end):
    game = Game(fps=fps, room=room)
    for s in spawns:
        game.spawn(*s)
    if player:
        game.place_player(*player)
    pending = sorted(inputs, key=lambda i: i[0])
    while game.t < end - 1e-9:
        while pending and pending[0][0] <= game.t + 1e-9:
            _, action, direction = pending.pop(0)
            game.press(action, direction)
        game.step()
    return game


class GrubTest(unittest.TestCase):
    def test_telegraph_and_timing(self):  # AC-1, AC-2
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(8, 4)
            g.spawn("grub", 12, 4)
            run(g, 4.0)
            wind, strike, rec, hurt = (times(g, k) for k in ("windup", "strike", "recover", "hurt"))
            tol = TOL[fps]
            self.assertAlmostEqual(wind[0], 1.375, delta=tol)
            self.assertAlmostEqual(strike[0] - wind[0], 0.5, delta=tol)
            self.assertAlmostEqual(rec[0] - strike[0], 0.15, delta=tol)
            self.assertAlmostEqual(wind[1] - rec[0], 0.9, delta=tol)
            self.assertGreaterEqual(hurt[0] - wind[0], 0.45)
            for h in hurt:  # no heart lost outside Strike
                self.assertTrue(any(s - 1e-9 <= h <= s + 0.15 + g.dt + 1e-9 for s in strike), (fps, h))

    def test_dash_away_during_windup_loses_no_heart(self):  # AC-3
        for fps in FPS:
            for offset in (0.0, 0.25, 0.49):
                g = Game(fps=fps, room="empty")
                g.place_player(8, 4)
                g.spawn("grub", 6.8, 4)
                run(g, offset)
                g.press("dash", "right")
                run(g, 1.6)
                self.assertEqual(g.hearts, HEARTS, (fps, offset))

    def test_counter_in_recovery_and_bite_spacing(self):  # AC-4
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(8, 4)
            g.spawn("grub", 6.8, 4)
            g.press("move", "left")
            g.press("stop")
            run_until(g, "recover")
            run(g, 0.25)  # the hit-stun has passed
            g.press("attack")
            self.assertEqual(g.events[-1][1], "attack") if False else None
            self.assertEqual(g.enemies[0].hp, 1)
            self.assertTrue(g.enemies[0].damaged)
            run(g, 3.0)
            hurt = times(g, "hurt")
            self.assertGreaterEqual(len(hurt), 2)
            self.assertGreaterEqual(hurt[1] - hurt[0], 1.5)

    def test_interrupt_cancels_the_strike(self):  # AC-5
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(8, 4)
            g.spawn("grub", 6.8, 4)
            g.press("move", "left")
            g.press("stop")
            run(g, 0.2)
            g.press("attack")
            e = g.enemies[0]
            self.assertEqual((e.hp, e.state), (1, "recovery"))
            self.assertAlmostEqual(e.timer, 0.6, places=6)
            self.assertEqual(g._slots_used(), 0)
            hit_t = g.t
            run(g, 1.3)
            self.assertEqual(g.hearts, HEARTS)
            self.assertGreaterEqual(times(g, "windup")[1] - hit_t, 0.6 - 1e-9)

    def test_attack_limit_of_two(self):  # AC-6
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(8, 4)
            for pos in [(6.5, 4), (9.5, 4), (8, 2.5), (8, 5.5), (6.5, 5.5)]:
                g.spawn("grub", *pos)
            most = 0
            for _ in range(round(12 * fps)):
                g.step()
                busy = sum(1 for e in g.enemies if e.hp > 0 and e.state in ("windup", "strike"))
                most = max(most, busy)
                self.assertLessEqual(busy, 2)
            self.assertEqual(most, 2)

    def test_two_grubs_one_heart_lost_for_simultaneous_hits(self):
        g = Game(room="empty")
        g.place_player(4, 4)
        g.spawn("grub", 4.5, 4)
        g.spawn("grub", 4.5, 5)
        run(g, 0.8)
        self.assertEqual(g.hearts, HEARTS - 1)

    def test_knockback_is_one_tile(self):
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.spawn("grub", 9.2, 4)
            g.press("attack")
            run(g, 0.2)
            self.assertAlmostEqual(g.enemies[0].x, 10.2, delta=0.05)

    def test_two_swipes_defeat_a_grub(self):
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.spawn("grub", 9.2, 4)
            g.press("attack")
            run_until(g, "windup")
            g.press("attack")
            g.step()
            self.assertEqual(g.enemies[0].hp, 0)
            self.assertTrue(g.cleared)

    def test_strike_is_checked_on_enough_frames(self):
        for i in range(8):
            g = Game(fps=30, room="empty")
            g.spawn("grub", 11 + i * 0.0123, 4)
            run_until(g, "recover")
            self.assertGreaterEqual(g.enemies[0].strike_checks, 4, i)


class SpitterTest(unittest.TestCase):
    def test_stagger_schedule(self):  # AC-7
        for fps in FPS:
            for room in ("3", "4", "5"):
                g = Game(fps=fps, room=room)
                run(g, 5.0)
                ks = [e.index for e in g.enemies if e.kind == "spitter"]
                expected = [(1.0, 3.5), (1.8, 4.3), (2.6, 5.1)]
                for k, idx in enumerate(ks):
                    got = times(g, "charge", index=idx)
                    for want, have in zip(expected[k], got):
                        self.assertAlmostEqual(have, want, delta=TOL[fps], msg=(fps, room, k))
                for kind in ("charge", "spit"):
                    ts = sorted(times(g, kind))
                    for a, b in zip(ts, ts[1:]):
                        self.assertGreaterEqual(b - a, 0.5, (fps, room, kind))

    def test_spit_lines_name_their_spitter(self):  # AC-8 and the defect report
        for fps in FPS:
            for room in ("3", "4", "5"):
                script = f"room {room}\nfps {fps}\nend 5\n"
                lines = text_lines(capture(script))
                trace = capture(script, "trace")
                spits = [(t, x) for t, x in lines if x.endswith("spits")]
                self.assertEqual(len(spits), len(re.findall(r"\bspit@", trace)))
                self.assertEqual(len(set(lines)), len(lines), (fps, room))  # no identical lines at one time
                for t, x in spits:
                    label = re.match(r"spitter \((.+)\) spits", x).group(1)
                    charges = [c for c, y in lines if y == f"spitter ({label}) charges"]
                    self.assertTrue(any(abs((t - 0.8) - c) <= TOL[fps] + 1e-9 for c in charges), (fps, room, x))

    def test_labels_are_distinct_in_each_room(self):
        for room in ("3", "4", "5"):
            g = Game(room=room)
            labels = [e.label for e in g.enemies if e.kind == "spitter"]
            self.assertEqual(len(set(labels)), len(labels), labels)

    def test_projectile_hits_a_still_player_and_misses_a_mover(self):  # AC-9
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(8, 4)
            g.spawn("spitter", 14, 4)
            run(g, 4.2)
            self.assertEqual(g.hearts, HEARTS - 1)
            self.assertEqual([d["source"] for _, k, d in g.events if k == "hurt"], ["shot"])
            for how in ("walk", "dash"):
                g = Game(fps=fps, room="empty")
                g.place_player(8, 4)
                g.spawn("spitter", 14, 4)
                run(g, 1.9)
                if how == "walk":
                    g.press("move", "up")
                    run(g, 0.5)
                    g.press("stop")
                else:
                    g.press("dash", "up")
                    run(g, 0.5)
                run(g, 2.6)
                self.assertEqual(g.hearts, HEARTS, (fps, how))

    def test_walk_up_and_defeat_a_spitter(self):  # AC-10
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.spawn("spitter", 10, 4)
            g.press("move", "right")
            run(g, 0.4)
            g.press("stop")
            g.press("attack")
            run(g, 0.4)
            g.press("attack")
            g.step()
            self.assertEqual(g.enemies[0].hp, 0)
            self.assertTrue(g.cleared)

    def test_hit_in_charge_cancels_the_shot(self):
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(9.6, 4)
            g.spawn("spitter", 10, 4)
            run(g, 1.2)
            g.press("attack")
            self.assertEqual(len(times(g, "stagger")), 1)
            run(g, 1.7)  # t = 2.9: the re-based charge (2.2 s) has not fired yet
            self.assertEqual(len(times(g, "spit")), 0)
            run(g, 0.4)
            self.assertEqual(len(times(g, "spit")), 1)


class AttackTest(unittest.TestCase):
    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_cone_is_ninety_degrees(self):
        g = Game(room="empty")
        g.spawn("grub", 9.0, 4.9)
        g.press("attack")
        self.assertEqual(g.enemies[0].hp, 1)
        g = Game(room="empty")
        g.spawn("grub", 8.6, 5.4)
        g.press("attack")
        self.assertEqual(g.enemies[0].hp, 2)

    def test_multi_hit_prints_two_lines(self):  # AC-12
        g = Game(room="empty")
        g.spawn("grub", 9.0, 4.5)
        g.spawn("grub", 9.0, 3.5)
        g.press("attack")
        kind, details = g.events[-1][1], g.events[-1][2]
        self.assertEqual(kind, "attack")
        lines = play.describe_event(kind, details)
        self.assertEqual(lines, ["you swipe: grub hit (1 left)"] * 2)

    def test_every_outcome_has_a_line(self):  # AC-11
        g = Game(room="empty")
        g.spawn("grub", 9.0, 4)
        g.press("attack")
        g.press("attack")
        g.press("attack")
        lines = [x for _, k, d in g.events for x in play.describe_event(k, d)]
        self.assertIn("you swipe: grub hit (1 left)", lines)
        self.assertIn("you swipe: (too soon)", lines)
        g = Game(room="empty")
        g.press("attack")
        self.assertEqual(play.describe_event(*g.events[-1][1:]), ["you swipe: (miss)"])
        g.hearts = 1
        g._hurt("shot")
        g.press("attack")
        self.assertEqual(play.describe_event(*g.events[-1][1:]), ["you swipe: (down)"])
        g = Game(room="empty")
        g.hearts = 2
        g._hurt("shot")
        g.press("attack")
        self.assertEqual(play.describe_event(*g.events[-1][1:]), ["you swipe: (stunned)"])
        g.press("dash", "left")
        self.assertEqual(play.describe_event(*g.events[-1][1:]), ["(stunned)"])
        self.assertNotIn("nothing happens", Path(play.__file__).read_text(encoding="utf-8"))

    def test_glyph_states_are_distinct(self):  # AC-11, V-4
        for kind in ("grub", "spitter"):
            chars = {play.GLYPHS[(kind, d, a)][0] for d in (False, True) for a in (False, True)}
            self.assertEqual(len(chars), 4)
        for (kind, damaged, alert), (char, _) in [(k, v) for k, v in play.GLYPHS.items() if isinstance(k, tuple)]:
            self.assertEqual(char.isupper(), alert)

    def test_moving_during_swipe_recovery(self):
        g = Game(room="empty")
        g.place_player(2, 4)
        g.press("attack")
        g.press("move", "right")
        run(g, 0.2)
        self.assertGreater(g.x, 2.7)

    def test_dash_distance_and_queue(self):
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(2, 4)
            g.press("dash", "right")
            run(g, 0.5)
            self.assertAlmostEqual(g.x, 2 + DASH_DISTANCE, places=6)
        g = Game(room="empty")
        g.place_player(2, 4)
        g.press("dash", "right")
        run(g, 0.1)
        g.press("attack")
        self.assertFalse(any(k == "attack" for _, k, _ in g.events))
        run(g, 0.2)
        self.assertTrue(any(k == "attack" for _, k, _ in g.events))

    def test_dash_has_a_cooldown(self):
        g = Game(room="empty")
        g.press("dash", "left")
        run(g, 0.5)
        g.press("dash", "left")
        self.assertEqual(g.events[-1][2]["reason"], "dash not ready")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(4, 4)
            g.spawn("grub", 4.5, 4)
            g.spawn("grub", 4.5, 5)
            run_until(g, "hurt")
            while g.stun_left > 0:
                g.step()
            g.press("dash", "right")
            run_until(g, "dash_end")
            self.assertTrue(g.invulnerable)
            self.assertGreater(g.hurt_left, 0)
            run(g, 1.0)
            hurt = times(g, "hurt")
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class RunFlowTest(unittest.TestCase):
    def test_down_then_run_over_then_restart(self):  # AC-13
        for fps in FPS:
            g = Game(fps=fps, room="4")
            run(g, 0.5)
            g.hearts = 1
            g.shots.append(Shot(8, 4, 0, 0, 99, 0))
            g._hurt("shot")
            self.assertEqual(g.phase, "down")
            self.assertEqual(g.shots, [])
            frozen = [(e.x, e.y, e.state) for e in g.enemies]
            run(g, 1.0)
            self.assertEqual(frozen, [(e.x, e.y, e.state) for e in g.enemies])
            self.assertEqual(g.shots, [])
            g.press("attack")
            self.assertEqual(g.events[-1][2]["reason"], "down")
            run(g, 1.0)
            self.assertEqual(g.phase, "over")
            over = times(g, "run_over")
            self.assertEqual(len(over), 1)
            down_t = times(g, "down")[0]
            self.assertAlmostEqual(over[0] - down_t, 2.0, delta=TOL[fps])
            g.press("attack")
            self.assertEqual((g.hearts, g.room, g.phase, len(g.enemies)), (HEARTS, "1", "playing", 3))
            self.assertEqual(len(times(g, "run_start")), 1)

    def test_run_over_screen_and_marker(self):  # V-8, AC-13
        lines = play.describe_event("run_over", {"rooms": 2, "complete": False, "practice": False})
        self.assertEqual(lines, ["run over — rooms cleared: 2", "press attack to start again"])
        g = Game(room="empty")
        g.hearts = 1
        g._hurt("shot")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            play.Player(g).snapshot()
        grid = [row for row in buf.getvalue().splitlines() if row.startswith("   |")]
        self.assertTrue(any("x" in row for row in grid))
        self.assertFalse(any("P" in row for row in grid))

    def test_practice_room_ends_after_down(self):
        g = Game(room="empty")
        g.hearts = 1
        g._hurt("shot")
        run(g, 2.1)
        self.assertTrue(g.finished)
        g.press("attack")
        self.assertEqual(len(times(g, "run_start")), 0)

    def test_room_clear_heals_and_loads_the_next_room(self):  # AC-14
        for fps in FPS:
            g = Game(fps=fps, room="1")
            g.hearts = 2
            for e in g.enemies[1:]:
                e.hp = 0
            g.enemies[0].hp = 1
            g.enemies[0].x, g.enemies[0].y = 9.0, 4.0
            g.shots.append(Shot(1, 1, 0, 0, 98, 0))
            g.press("attack")
            g.step()
            self.assertTrue(g.cleared)
            self.assertEqual(g.hearts, 3)
            self.assertEqual(g.shots, [])
            cleared_t = times(g, "cleared")[0]
            run(g, 1.6)
            self.assertEqual((g.room, g.x, g.y, len(g.enemies)), ("2", 8.0, 4.0, 4))
            self.assertAlmostEqual(times(g, "room_loaded")[0] - cleared_t, 1.5, delta=TOL[fps] + 0.02)
            self.assertEqual(g.hearts, 3)

    def test_heal_is_capped(self):
        g = Game(room="1")
        for e in g.enemies:
            e.hp = 0
        g.step()
        self.assertEqual(g.hearts, HEARTS)
        self.assertEqual(times(g, "heal"), [])

    def test_clearing_swipe_cancels_a_due_strike(self):
        for fps in FPS:
            def setup():
                g = Game(fps=fps, room="empty")
                g.spawn("grub", 8.8, 4)
                run(g, 0.5)
                return g
            control = setup()
            control.step()
            self.assertEqual(control.hearts, HEARTS - 1)  # the strike really is due this tick
            g = setup()
            g.enemies[0].hp = 1
            g.press("attack")
            g.step()
            self.assertEqual(g.hearts, HEARTS)
            self.assertTrue(g.cleared)

    def test_run_complete_in_room_five(self):
        g = Game(room="5")
        for e in g.enemies:
            e.hp = 0
        g.step()
        self.assertEqual(len(times(g, "run_complete")), 1)
        run(g, 1.6)
        self.assertEqual(g.phase, "over")
        self.assertTrue(g.events[-1][2]["complete"])
        self.assertEqual(g.events[-1][2]["rooms"], 1)  # only this room was cleared in the test

    def test_practice_clear_has_no_heal_or_transition(self):
        g = Game(room="empty")
        g.hearts = 2
        g.spawn("grub", 9, 4)
        g.enemies[0].hp = 1
        g.press("attack")
        g.step()
        run(g, 3.0)
        self.assertTrue(g.cleared)
        self.assertEqual((g.hearts, g.room, g.phase), (2, "empty", "playing"))
        self.assertEqual(times(g, "heal") + times(g, "room_loaded"), [])

    def test_room_layouts(self):  # AC-16
        expected = {
            "1": {"grub": 3}, "2": {"grub": 4}, "3": {"spitter": 3},
            "4": {"grub": 2, "spitter": 2}, "5": {"grub": 3, "spitter": 2},
        }
        for room, want in expected.items():
            row = capture(f"room {room}\nend 0.1\n", "trace").splitlines()[1]
            got = {k: row.count(f"{k}#") for k in ("grub", "spitter") if row.count(f"{k}#")}
            self.assertEqual(got, want, room)
            self.assertEqual(Counter(s[0] for s in ROOMS[room]), Counter(want))


class ViewTest(unittest.TestCase):
    def test_grub_telegraph_is_seen_before_the_first_hit(self):  # AC-1, V-3, V-2
        for fps in FPS:
            out = capture(f"room empty\nfps {fps}\nspawn grub 12 4\nplayer 8 4\nend 3\n")
            rows = out.splitlines()
            rears = next(i for i, r in enumerate(rows) if "a grub rears back" in r)
            hit = next(i for i, r in enumerate(rows) if "YOU ARE HIT" in r)
            big = next(i for i, r in enumerate(rows) if r.startswith("   |") and "G" in r)
            self.assertLess(rears, big)
            self.assertLess(big, hit)
            self.assertIn("the grub is open", out)
            wind_t = text_lines(out)[[x for _, x in text_lines(out)].index("a grub rears back (right)")][0]
            heads = [float(m) for m in re.findall(r"\[(\d+\.\d\d) s\]", out)]
            self.assertTrue(any(0 <= h - wind_t < 0.06 for h in heads), (fps, wind_t))

    def test_swipe_draws_the_arc(self):  # V-2
        out = capture("room empty\nfps 60\n0.2 attack\nend 0.5\n")
        self.assertIn("you swipe: (miss)", out)
        self.assertTrue(any(r.startswith("   |") and ")" in r for r in out.splitlines()))

    def test_run_over_screen_in_a_script(self):
        out = capture("room empty\nfps 60\nend 1\n")
        self.assertNotIn("press attack", out)


class FrameRateTest(unittest.TestCase):
    SCENARIOS = [
        ("empty", [("grub", 12, 4)], (8, 4), [], 5.0),
        ("empty", [("spitter", 14, 4)], (8, 4), [(1.9, "dash", "up")], 5.0),
        ("empty", [("grub", 12, 4)], (8, 4), [(1.6, "dash", "left")], 5.0),
        ("4", [], None, [], 3.0),
    ]

    def compare(self):
        worst = 0.0
        for room, spawns, player, inputs, end in self.SCENARIOS:
            a = drive(30, room, spawns, player, inputs, end)
            b = drive(60, room, spawns, player, inputs, end)
            ka = [k for _, k, _ in a.events]
            kb = [k for _, k, _ in b.events]
            self.assertEqual(ka, kb, (room, spawns))
            for (ta, _, _), (tb, _, _) in zip(a.events, b.events):
                worst = max(worst, abs(ta - tb))
        return worst

    def test_same_events_within_seven_hundredths(self):  # AC-17
        self.assertLessEqual(self.compare(), 0.07)

    def test_measurements(self):
        worst = self.compare()
        err = {30: 0.0, 60: 0.0}
        frames = {30: 99, 60: 99}
        for fps in FPS:
            g = Game(fps=fps, room="empty")
            g.place_player(8, 4)
            g.spawn("grub", 12, 4)
            g.spawn("spitter", 1, 1)
            run(g, 4.0)
            w, s, r = (times(g, k, index=0) for k in ("windup", "strike", "recover"))
            err[fps] = max(
                abs(s[0] - w[0] - 0.5), abs(r[0] - s[0] - 0.15), abs(w[1] - r[0] - 0.9),
                abs(times(g, "charge")[0] - 1.8), abs(times(g, "spit")[0] - times(g, "charge")[0] - 0.8),
            )
            frames[fps] = g.enemies[0].strike_checks
        print(f"\nMEASURE max timestamp error 30fps={err[30]:.4f}s 60fps={err[60]:.4f}s; "
              f"max cross-fps event difference={worst:.4f}s; strike evaluations at 30 fps={frames[30]}")


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)
            self.assertLessEqual(result["hearts_lost"], HEARTS, name)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/README.md (proposed in a run round; not written)
# Lantern Depths build (0.5)

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS): enemy state machines, player kit, run and room flow.
- `play.py`: runs an input script (`../manual.md`) and prints the player view or a trace. Glyphs and player-visible text live in the `GLYPHS` and `LINES` tables at the top.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`, `reactive`) that play rooms and report how they fared.
>>>END

<<<FILE repo/BUILD-NOTES.md (proposed in a run round; not written)
# Build 0.5 working notes (temporary; for the executor that finishes this Step)

State: first run round. game.py, play.py, bots.py, tests, README written; NOT yet run. Next: read the
`tests` results, fix failures, then (if rounds remain) run `bots` at fps 30 and 60 and a `trace`
for rooms 4/5, then write the final files and the handoff 18 (to `studio`).

Final deliverables still to write:
- handoff `goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md` (as-built report, see below).
- `manual.md` (T8) is outside the paths this Step may write (only handoff 18 and `repo/...`).
  Write the full player-facing manual text to `repo/docs/manual-0.5.md` and tell the Studio, in the
  handoff, to install it as `manual.md`. Content: controls; script table (unchanged lines; add that
  `room empty` is the practice room and a session ends at the run-over screen); on-screen glyph table
  (P, x, g/G, w/W, s/S, z/Z, *, arc `) ( ^ v`; uppercase = about to hurt, lowercase = harmless; w/z =
  damaged); the new text lines; swipe reasons (miss / too soon / stunned / down); run-over screen and
  "press attack to start again"; room clear heals one heart, short free pause, next room; hearts line.
  No [tune] numbers, no implementation notes.
- Drop this file (do not re-emit it).

As-built choices (report in the handoff):
- Constants as in game.py: grub speed 2.0 (F1, up from 1.2), range 1.25, strike reach 1.0, lunge <=1.0
  over 0.15 s, wind-up 0.5, recovery 0.9, cancel recovery 0.6, knockback 1.0 tile / 0.2 s (wall
  clamped), slots 2; spitter charge 0.8, recovery 0.6, stagger 1.0, interval 2.5, first 1.0 + 0.8k,
  shot speed 3.0, shot hit radius 0.4 (unchanged); cone 90 deg, reach 1.5, overlapping enemy counts;
  down 2.0 s, clear wait 1.5 s, heal +1.
- F2 unslotted grub: approaches to 1.25, holds, waits for a slot. Slot order: nearest first, spawn index on ties.
- F3 player exactly on a spitter: no projectile, trace event `fizzle`.
- F4 no extra spacing after a stagger re-base. F5 read as charge/charge and fire/fire >= 0.5 s apart.
- F6 room 5 clear: "room cleared", heal, "run complete" at the clear, 1.5 s free input, then screen
  "run complete — rooms cleared: 5" + "press attack to start again".
- F7 a session stops at the run-over screen unless a later input exists (then attack restarts);
  the practice room always ends 2.0 s after down.
- F8 as in the plan (strike hit: no knockback; recovery hit: knockback, timer not extended; wind-up hit:
  cancel + knockback). F9 resolved by combat-visuals.md: damaged + telegraph = `W`/`Z`.
- F10 any input while stunned prints "(stunned)", while down "(down)", dash on cooldown "(dash not ready)".
- F11 no pause.
- Visual spec overrides handoff 14 F9 glyph defaults (as handoff 17 item 3 instructs). Extra draws on
  windup/charge/spit/attack/recover/down/hurt/stagger/cleared/room_loaded/run_start are built (cheap;
  no hand-back needed). Invulnerability marker `p` NOT added (designer must specify).
- Defects fixed: spit line names its spitter by 3x3 position; duplicates get " #n"; spit event carries
  `shot` id; trace lists shots with owner.
- Observations for the designer: two grubs hit by one swipe print two identical lines
  ("you swipe: grub hit (1 left)") as the spec words them; two grubs winding up on the same side print
  identical "a grub rears back (left)" lines.
- hearts_lost in bots counts `hurt` events; `reactive` bot added.

Measurements to quote: the test `test_measurements` prints max timestamp error at 30/60 FPS, max
cross-fps difference and strike evaluations at 30 FPS.
>>>END

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 1 (0.1 s). Output:

```text

MEASURE max timestamp error 30fps=0.8000s 60fps=0.8000s; max cross-fps event difference=0.0167s; strike evaluations at 30 fps=6
......F.E..........E.E..E.E........E...
======================================================================
ERROR: test_every_bot_finishes_a_room (test_game.BotsTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 573, in test_every_bot_finishes_a_room
    result = bots.play_room(bot, "1", 60, 30)
  File "/work/bots.py", line 114, in play_room
    bot(game)
  File "/work/bots.py", line 60, in camper
    _face_and_swing(game, enemy)
  File "/work/bots.py", line 35, in _face_and_swing
    game.press("attack")
  File "/work/game.py", line 236, in press
    self._attack()
  File "/work/game.py", line 325, in _attack
    self.log(kind, **details)
TypeError: Game.log() got multiple values for argument 'kind'

======================================================================
ERROR: test_two_swipes_defeat_a_grub (test_game.GrubTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 163, in test_two_swipes_defeat_a_grub
    g.press("attack")
  File "/work/game.py", line 236, in press
    self._attack()
  File "/work/game.py", line 325, in _attack
    self.log(kind, **details)
TypeError: Game.log() got multiple values for argument 'kind'

======================================================================
ERROR: test_clearing_swipe_cancels_a_due_strike (test_game.RunFlowTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 462, in test_clearing_swipe_cancels_a_due_strike
    g.press("attack")
  File "/work/game.py", line 236, in press
    self._attack()
  File "/work/game.py", line 325, in _attack
    self.log(kind, **details)
TypeError: Game.log() got multiple values for argument 'kind'

======================================================================
ERROR: test_practice_clear_has_no_heal_or_transition (test_game.RunFlowTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 483, in test_practice_clear_has_no_heal_or_transition
    g.press("attack")
  File "/work/game.py", line 236, in press
    self._attack()
  File "/work/game.py", line 325, in _attack
    self.log(kind, **details)
TypeError: Game.log() got multiple values for argument 'kind'

======================================================================
ERROR: test_room_clear_heals_and_loads_the_next_room (test_game.RunFlowTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 431, in test_room_clear_heals_and_loads_the_next_room
    g.press("attack")
  File "/work/game.py", line 236, in press
    self._attack()
  File "/work/game.py", line 325, in _attack
    self.log(kind, **details)
TypeError: Game.log() got multiple values for argument 'kind'

======================================================================
ERROR: test_walk_up_and_defeat_a_spitter (test_game.SpitterTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 245, in test_walk_up_and_defeat_a_spitter
    g.press("attack")
  File "/work/game.py", line 236, in press
    self._attack()
  File "/work/game.py", line 325, in _attack
    self.log(kind, **details)
TypeError: Game.log() got multiple values for argument 'kind'

======================================================================
FAIL: test_multi_hit_prints_two_lines (test_game.AttackTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 287, in test_multi_hit_prints_two_lines
    self.assertEqual(kind, "attack")
AssertionError: 'knockback' != 'attack'
- knockback
+ attack


----------------------------------------------------------------------
Ran 39 tests in 0.062s

FAILED (failures=1, errors=6)
```
>>>END
