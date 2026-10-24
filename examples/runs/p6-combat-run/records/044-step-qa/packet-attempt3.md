# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/38-studio-to-qa.md
next_seq: 40
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/40-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/38-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 38
from: studio
to: qa
stage: Verify
outcome: routed
---
# 38: studio → qa — Verify AC-15 (practice-room paragraph in `manual.md`) and run `ManualTest`

## Task

Verify AC-15 against the build and `manual.md`. Read the `## On screen` section of `manual.md` and check that it contains the practice-room paragraph below, word for word. Then run `run_tests` and report the result of the two `ManualTest` tests in particular.

## Context

Goal G-001 (combat feels monotonous) is in Verify. In earlier rounds `ManualTest` had no valid result: the QA and engineer workspaces lacked `manual.md`. The Owner has now added the paragraph (D-007). A separate Verify step (37) covers the other acceptance criteria and does not cover AC-15. Do not repeat that work except where AC-15 needs it.

## Findings

Nothing to report from earlier work for this check. The Owner states they appended the following paragraph at the end of `## On screen`:

> The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

This is the Owner's statement; verify it independently.

## Decisions already made

- D-005: the Owner places `manual.md` content. Roles do not edit it. Report problems, do not fix them.
- D-006: the practice room is listed in the On screen section; enemies may overlap the player but are never hidden.
- D-007: the Owner placed the paragraph above (Option A).

## Constraints

- `manual.md` must sit beside `repo/` in your workspace, because `ManualTest` reads it there. If it is missing, report that as a blocker. Do not call it a test failure.
- Do not edit `manual.md` or the build.
- Use the project's run commands: `run_tests`, and `run_play` / `run_trace` with your own input scripts.

## Open questions

- Is the paragraph present in `## On screen`, word for word and inside that section?
- Do the two `ManualTest` tests pass with `manual.md` placed?
- Does the behavior the paragraph describes match the build? Check with scripts: the practice room is not part of a run, enemies appear only where `spawn` places them, nothing heals, there is no next room, the session ends shortly after you go down, and an enemy on the player's tile is drawn on a free adjacent tile.

## Expected output

A pass/fail report on AC-15, covering the paragraph check, the `ManualTest` results, and the behavior checks, with raw command output as evidence. Address the result to `studio`. If anything cannot be run, say what is missing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: manual.md; design/combat.md (AC-15, AC-18); project.md#current-state; repo (build; use `run_tests`, `run_play`, `run_trace`)
- Decisions: decisions/D-005-owner-places-manual-draft.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-007-practice-room-paragraph-placed-by-owner.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
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

<<<FILE decisions/D-007-practice-room-paragraph-placed-by-owner.md
---
kind: decision
id: D-007
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-007: The Owner places the practice-room paragraph in `manual.md` (Option A)

## Decision

The Owner chose Option A of escalation 36. The Owner added the following paragraph to `manual.md`, in the `## On screen` section, at the end of the section, with no change to the wording:

> The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

Owner's words (2026-10-15): 「A。36 の段落を一字も変えずに manual.md の ## On screen セクションの末尾に追記しました（Owner の代理として Studio の推奨案を採用）。」

Limits:
- This settles only who places the paragraph and that Option A applies. It does not change D-005 (the Owner places `manual.md` content) or D-006 (the practice room is listed in the On screen section). Options B and C were not chosen.
- The placement is the Owner's statement. QA verifies it independently (AC-15, `ManualTest`) and does not take it on trust.
- The Owner's reply says the choice follows the Studio's recommendation, made on the Owner's behalf. The Studio records it as the Owner's decision as given.

## Rationale

The wording was already fixed by D-006 and AC-15, and only the file edit was missing. It is a small, reversible edit. Options B (a permanent change to write permissions or D-005) and C (overturning D-006) were out of proportion to the gap.

## Alternatives considered

- B: let roles edit `manual.md`. It changes the D-005 policy and needs an environment change, which is too much for one paragraph.
- C: drop the practice-room entry from AC-15. It reverses D-006 and needs a Design re-decision, which is unnecessary.

## Revisit when

- QA finds the paragraph missing, altered, or outside `## On screen`, or `ManualTest` still fails for a manual-related reason.
- Roles repeatedly need to edit `manual.md`. Then reconsider Option B and D-005.
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
.....................EE.................
======================================================================
ERROR: test_manual_lists_glyphs_and_lines (test_game.ManualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 625, in test_manual_lists_glyphs_and_lines
    text = MANUAL.read_text(encoding="utf-8")
  File "/usr/lib/python3.10/pathlib.py", line 1134, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
  File "/usr/lib/python3.10/pathlib.py", line 1119, in open
    return self._accessor.open(self, mode, buffering, encoding, errors,
FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'

======================================================================
ERROR: test_on_screen_section_lists_x_and_the_practice_room (test_game.ManualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 634, in test_on_screen_section_lists_x_and_the_practice_room
    text = MANUAL.read_text(encoding="utf-8")
  File "/usr/lib/python3.10/pathlib.py", line 1134, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
  File "/usr/lib/python3.10/pathlib.py", line 1119, in open
    return self._accessor.open(self, mode, buffering, encoding, errors,
FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'

----------------------------------------------------------------------
Ran 40 tests in 0.060s

FAILED (errors=2)
```

### Round 1: @run/play/grub-d4 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
end 5.5
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
   |        PG      |
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
   |        Pg      |
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
   |        Pg      |
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
  3.450  YOU ARE HIT by a grub — hearts 1/3
   [3.45 s] hearts 1/3
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
  3.583  the grub is open (on you)
   [3.58 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
  4.483  a grub rears back (on you)
   [4.48 s] hearts 1/3
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
   [4.50 s] hearts 1/3
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
  5.000  YOU ARE HIT by a grub — hearts 0/3
  5.000  you went down
   [5.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
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
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.50 s: hearts 0/3, enemies left 1
```

### Round 1: @run/trace/grub-d4 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 12 4
end 5.5
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
t=5.500 frame=330 room=empty phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | end
```

### Round 1: @run/play/spitter-on-tile — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
player 8 4
spawn spitter 8.2 4
end 3.5
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
   |        Ps      |
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
   |        Ps      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter (center) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PS      |
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
   |        PS      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  spitter (center) spits
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Ps      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.833  YOU ARE HIT by a shot — hearts 2/3
   [1.83 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Ps      |
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
   |        Ps      |
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
   |        Ps      |
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
   |        Ps      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  spitter (center) charges
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PS      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.50 s: hearts 2/3, enemies left 1
```

### Round 1: @run/trace/clear-practice — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 9 4
0.9 attack
1.3 attack
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.89,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=0.667 frame=40 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=0.917 frame=55 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.417 stun_left=0.000 shots=0 | grub#0(8.08,4.00,hp=1,recovery,0.650) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
t=1.317 frame=79 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.017 stun_left=0.000 shots=0 |  | attack {'facing': 'right', 'hits': [('grub', 'defeated', 0, 0)]}; cleared {'room': 'empty'}
t=1.333 frame=80 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.000 frame=360 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 |  | end
```

### Round 1: @run/play/down-practice — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
player 8 4
spawn grub 8.2 4
end 20
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
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (right)
   [0.02 s] hearts 3/3
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
   [0.50 s] hearts 3/3
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
  0.533  YOU ARE HIT by a grub — hearts 2/3
   [0.53 s] hearts 2/3
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
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
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
   [1.00 s] hearts 2/3
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
   [1.50 s] hearts 2/3
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
  1.567  a grub rears back (on you)
   [1.57 s] hearts 2/3
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
  2.083  YOU ARE HIT by a grub — hearts 1/3
   [2.08 s] hearts 1/3
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
  2.217  the grub is open (on you)
   [2.22 s] hearts 1/3
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
   [2.50 s] hearts 1/3
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
   [3.00 s] hearts 1/3
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
  3.117  a grub rears back (on you)
   [3.12 s] hearts 1/3
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
  3.633  YOU ARE HIT by a grub — hearts 0/3
  3.633  you went down
   [3.63 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
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
   |        xg      |
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
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.63 s: hearts 0/3, enemies left 1
```
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goals/G-001-combat-monotony/40-qa-to-studio.md: missing sections ['Constraints', 'Context', 'Decisions already made', 'Expected output', 'Findings', 'Open questions']
