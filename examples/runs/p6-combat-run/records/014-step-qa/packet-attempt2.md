# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
next_seq: 15
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/15-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/12-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 12
from: studio
to: qa
stage: Observe
outcome: routed
---
# 12: studio → qa — Reproduce and log the repeated spitter attack line

## Task

On the current build, reproduce the spitter attack text that appears to be printed twice, and write a defect report with severity and acceptance criteria.

## Context

During a playtest of rooms 4–5 the spitter's attack line looked doubled. Rooms 4–5 each have spitters that fire a pair of shots on a beat. The design documents say one line per spitter is expected, so two lines may be correct; the problem is that identical lines read as a duplicate. This is a presentation question. The spitter's behavior is about to be reworked (target `design/combat.md`, acceptance criterion AC-8, which requires the line to name the spitter), so the report should say what is observable on the current build, not propose a fix.

## Findings

Nothing yet beyond the observation above. Build under test: `repo/` at sha e54837757611.

## Decisions already made

None that bear on this defect.

## Constraints

- Use the project's run commands (`run_play`, `run_trace`, `run_bots` in `project.md`); a play session is an input script (`manual.md`).
- Check at both 30 and 60 FPS if the script format allows it; say so if it does not.
- Do not verify or comment on the rest of the Option A spec; that is a later step.

## Open questions

- Is the doubled line one event printed twice (a defect), or two spitters each printing their own line (one line per spitter)?
- Does it occur in room 4, room 5, or both? Does it change with the number of spitters?

## Expected output

A defect report (reproduction script, observed vs. expected, severity, acceptance criteria). Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints, goals/G-001-combat-monotony/08-playtester-to-game-designer.md
- Decisions: none
- Previous handoff: none
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE goals/G-001-combat-monotony/08-playtester-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 8
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 08: playtester → game-designer — Observation report: rooms 4 and 5

## Task

Read the observations below on rooms 4 and 5 and diagnose the combat experience. Nothing here is a cause or a fix.

## Context

G-001: the Owner finds combat monotonous. This is first-hand play evidence for rooms 4 and 5, taken with the player view only and `manual.md`.

## Findings

### Method

- Input-script automation with `python3 play.py --view player`. I did not play live and did not read source.
- Three runs in total:
  - room 4 idle (8 s)
  - room 5 idle (8 s)
  - room 4 with a short fight script: walk left, stop, four attacks, one dash right (8 s)
- The run budget ended there. **I did not play a fight in room 5** and I **never approached a spitter**. I did not run any further script to test dodging.
- Claims about room 5 come from the idle run only.

### Enemies, counts and behaviour over time

**Room 4**
- 2 grubs start on the left, at about (0,1) and (1,4).
- 2 spitters sit in the right-hand corners, at (15,0) and (15,8).
- The grubs walk steadily toward me, about 1 tile per half second. They reach me at about 5 s when I stand still.
- Spitters did not move at all during 8 s.
- Both spitters spit at the same moment, every 2 s (2.0, 4.0, 6.0, 8.0 s). Each spit is one `*` and the two always come as a mirrored pair.
- The projectiles drift leftward and toward the middle rows, closing on my row. In the idle run they passed above and below me, then bunched around my tile.
- **I was never hit by a projectile in any run.** All damage I saw came from grubs.
- Over time nothing changed except the grubs closing in. The spit rhythm was identical from the first spit to the last.

**Room 5**
- 3 grubs start on the left and bottom-left, at about (1,1), (0,6) and (4,8).
- 2 spitters sit in the right-hand corners, at the same spots as in room 4.
- Spit timing and look are the same as in room 4: a mirrored pair every 2 s.
- Idle, the grubs surrounded me and the first hit came at 4.2 s. I went down at 5.8 s.

### Do the rooms feel different?

- On paper, room 5 is room 4 plus one more grub, arriving from more directions. That is the only difference I could see.
- The spitters, the layout of the right edge and the spit pattern looked identical.
- In the idle runs, room 5 killed me about 1.1 s sooner (5.8 s against 6.95 s).
- I could not tell the two rooms apart by feel. I expect the same loop: grubs close in while the spitters repeat the same pair of shots on the same beat.

### First contact with each enemy type

**Grub**
- Visible from the start, walking at me in the open. There was no damage before I could see it coming.
- My responses are to hit it or dash away.
- In the fight run, the first hit on me came at 1.4 s. I was still walking left into the grubs, so it was my own approach.

**Spitter**
- Visible from the start in a corner. A text line "a spitter spits" appears at the moment of each shot.
- The `*` projectiles are visible and slow, a few tiles per second.
- I never got hit by one, so I cannot say what it feels like to take one or what it does.
- I could see the pattern, but I had no occasion to dodge it.

### How my choices affected the outcome

- Standing still ended in a loss in both rooms: down at 6.95 s in room 4 and at 5.8 s in room 5. I took no action in those runs.
- The grubs hit about every 0.8 s while next to me. Hits came at 5.35, 6.15 and 6.95 s in room 4, so a 3-heart bar lasts about 1.6 s once they are on me.
- In the room 4 fight script:
  - Walking toward the grubs cost me a heart straight away, at 1.4 s.
  - Swipes at 1.5 and 1.6 s showed "(nothing happens)".
  - The swipe at 2.0 s landed: "grub hit".
  - I took another hit at 2.2 s.
  - The swipe at 2.4 s showed "(nothing happens)".
  - The swipe at 2.8 s showed "grub defeated, grub hit".
  - The dash right at 3.2 s carried me about 3 tiles away and got me clear.
  - The remaining grub caught up by about 5.5 s while I stood still after the dash, and took my last heart at 6.4 s.
- Moving while shooting was never tested.
- Most of the fight I did nothing but wait. The dash bought me a few seconds of quiet and I did nothing with them. That was my choice in the script, not something the game asked of me.
- The projectiles gave me nothing to react to in these runs. Both rooms felt like "kill the grubs and ignore everything else."

### What I see when my attack lands

- The only feedback is a line of text: "you swipe: grub hit" or "grub defeated".
- On the room map nothing changes visually when a grub is hit.
- I cannot say from the screen how many hits a grub takes. In the room 4 fight, one grub was hit at 2.0 s and a "grub defeated" came at 2.8 s, so it looks like two swipes for one grub. The 2.8 s swipe also listed a second "grub hit", so that swipe seemed to hit two. I am not sure which grub was which.
- Swipes seem to have a gap: two of my four swipes did nothing. I could not tell whether they missed because of range or timing, or were blocked by a cooldown.
- Spitter hits to defeat: not observed.

### Can I approach a spitter?

- Not tested. They stay in the far corners and I never reached the right side.

### How many hits can I take

- 3 hearts. Each grub hit costs 1 heart.
- No projectile damage was observed.

### After going down

- The text says "you went down" and my `P` becomes `x`.
- The room keeps running. The grubs stay beside me and the spitters keep firing, with no game-over screen and no restart in the output.
- Clearing a room was never reached, so I have no observation of it.

### Confusing or odd

- "(nothing happens)" on attacks at 1.5, 1.6 and 2.4 s, with no stated reason.
- The "a spitter spits" line appears twice at each spit time. This looks like one line per spitter.
- "enemies left" at the end was 4 and 5 in the idle runs (every enemy still alive). It was 3 after the fight run (one grub killed).
- The same mirrored spit pair on the same 2 s beat made the spitters read as scenery. That is how it felt, not a measurement.

## Decisions already made

None.

## Constraints

- Observations are what a player could see in the player view and read in `manual.md`. Not tested: room 5 combat, approaching spitters, being hit by a projectile, clearing a room, and any dash used for dodging.

## Open questions

None.

## Expected output

The game-designer diagnoses from these observations (stage Diagnose).

## Load

- Role: studio/roles/game-designer.md
- Skills: none specified
- Project: project.md#player-profile
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/07-studio-to-playtester.md
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
### Round 1: @run/trace/r4-fps30 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 30
end 8
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=4 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,4.00,hp=2) grub(0.00,1.00,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | setup
t=2.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.40,4.00,hp=2) grub(2.25,1.84,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=4.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.80,4.00,hp=2) grub(4.49,2.69,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=5.333 frame=160 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.40,4.00,hp=2) grub(5.99,3.25,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=6.000 frame=180 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(6.74,3.53,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=6.133 frame=184 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.46,4.00,hp=2) grub(6.89,3.58,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=6.933 frame=208 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=7.733 frame=232 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=8.000 frame=240 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=8.000 frame=240 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | end
```

### Round 1: @run/trace/r4-fps60 — `python3 play.py --view trace {script}`

Script:

```text
room 4
fps 60
end 8
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=4 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,4.00,hp=2) grub(0.00,1.00,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | setup
t=2.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.40,4.00,hp=2) grub(2.25,1.84,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=4.000 frame=240 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.80,4.00,hp=2) grub(4.49,2.69,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=5.350 frame=321 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.42,4.00,hp=2) grub(6.01,3.25,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=6.000 frame=360 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.150 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(6.74,3.53,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=6.150 frame=369 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.46,4.00,hp=2) grub(6.91,3.59,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=6.950 frame=417 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=7.750 frame=465 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=8.000 frame=480 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=8.000 frame=480 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(7.49,3.81,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | end
```

### Round 1: @run/trace/r5-fps60 — `python3 play.py --view trace {script}`

Script:

```text
room 5
fps 60
end 8
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2) grub(0.00,6.00,hp=2) grub(4.00,8.00,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | setup
t=2.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.21,1.95,hp=2) grub(2.33,5.42,hp=2) grub(5.70,6.30,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=4.000 frame=240 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.41,2.89,hp=2) grub(4.66,4.84,hp=2) grub(7.39,4.61,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=4.217 frame=253 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.65,2.99,hp=2) grub(4.91,4.77,hp=2) grub(7.58,4.42,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=5.017 frame=301 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,3.37,hp=2) grub(5.84,4.54,hp=2) grub(7.62,4.38,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=5.817 frame=349 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.42,3.75,hp=2) grub(6.77,4.31,hp=2) grub(7.62,4.38,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=6.000 frame=360 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | grub(7.50,3.79,hp=2) grub(6.99,4.25,hp=2) grub(7.62,4.38,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=6.617 frame=397 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.50,3.79,hp=2) grub(7.48,4.13,hp=2) grub(7.62,4.38,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=8.000 frame=480 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.50,3.79,hp=2) grub(7.48,4.13,hp=2) grub(7.62,4.38,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=8.000 frame=480 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.50,3.79,hp=2) grub(7.48,4.13,hp=2) grub(7.62,4.38,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | end
```

### Round 1: @run/trace/one-spitter-fps60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 0
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,0.00,hp=2) | setup
t=2.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,0.00,hp=2) | spit
t=4.000 frame=240 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,0.00,hp=2) | spit
t=5.817 frame=349 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,0.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=6.000 frame=360 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | spitter(15.00,0.00,hp=2) | spit
t=6.000 frame=360 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | spitter(15.00,0.00,hp=2) | end
```

### Round 1: @run/trace/two-spitters-fps60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 0
spawn spitter 15 8
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | setup
t=2.000 frame=120 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=4.000 frame=240 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=5.817 frame=349 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=6.000 frame=360 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | spit; spit
t=6.000 frame=360 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 | spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | end
```

### Round 1: @run/play/r4-fps60 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
end 5
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.4 — room 4 — 60 FPS
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
   [1.00 s] hearts 3/3
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
   [1.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |  g             |
   |                |
   |   g    P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.000  a spitter spits
  2.000  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |  g             |
   |                |
   |   g    P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |               s|
   |              * |
   |   g            |
   |                |
   |    g   P       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |   g            |
   |                |
   |     g  P       |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g       *   |
   |                |
   |     g  P       |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
  4.000  a spitter spits
  4.000  a spitter spits
   [4.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |    g           |
   |      g P       |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |               s|
   |              * |
   |           *    |
   |     g          |
   |      g P       |
   |                |
   |           *    |
   |              * |
   |               s|
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |      g   *     |
   |       gP       |
   |          *     |
   |                |
   |             *  |
   |               s|
   +----------------+
end at 5.00 s: hearts 3/3, enemies left 4
```
>>>END
