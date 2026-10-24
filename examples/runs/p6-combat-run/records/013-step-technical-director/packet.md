# Studio operation packet

operation: Step
goal: G-001
role: technical-director
incoming_handoff: goals/G-001-combat-monotony/11-studio-to-technical-director.md
next_seq: 14

## You may write

- goals/G-001-combat-monotony/14-technical-director-to-<recipient>.md
- decisions/D-004-<name>.md

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

<<<FILE goals/G-001-combat-monotony/11-studio-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 11
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 11: studio → technical-director — Plan the Option A combat rework (build 0.5 target)

## Task

Write a technical plan for implementing the spec in `design/combat.md` (build 0.5 target, acceptance criteria AC-1…AC-17) and the room/run rules in D-003. Check feasibility, name risks, and set the sequencing, tests and any parallelization.

## Context

G-001: the Owner finds combat monotonous. Diagnosis: enemy behavior is single-state and untelegraphed. The Game Director chose Option A (D-002): rework existing enemy behavior first. The game-designer has now specified it. Summary of the spec's change:

- Grub: Approach → Wind-up (0.5 s, visible) → Strike (0.15 s) → Recovery (0.9 s). Harmless outside Strike. At most 2 grubs attack at once. A hit during Wind-up cancels the strike.
- Spitter: Charge (0.8 s, visible) → Fire → Recovery. A volley every 2.5 s, staggered per spitter. Aim locked at the end of the charge, so the shot can be dodged. Spitters can be approached and hit; a hit during Charge cancels the shot.
- Hit feedback: swipe arc, damaged state, remaining HP in the text, multi-hit allowed.
- Run and room rules (D-003): zero hearts stops enemies and removes projectiles, then a "run over" screen after 2.0 s, and attack starts a new run at room 1. Room clear gives +1 heart, hearts carry over, and the next room loads after 1.5 s. A room cannot clear while the player is down.
- "(nothing happens)" on attack is allowed but must always give a reason: miss, too soon, stunned, down.

Current build: `repo/` at sha e54837757611 (version 0.4). Run commands are in `project.md` (`run_tests`, `run_play`, `run_trace`, `run_bots`).

## Findings

The designer left these for you:

- Feasibility of the attack-slot limit (max 2 attacking grubs) and the spitter aim-lock is not checked.
- Swipe reach, cone width and projectile speed are targets; Build should report as-built values.
- Timings marked [tune] need a live playtest after Build.
- `manual.md` must be updated for: the practice room behavior, the `x` downed marker, the new glyphs/states, the swipe arc, the run-over screen, and the new attack messages. The designer could not edit it. Decide who does it in the plan (the engineer in the Build step is the likely owner) and include it as a task with the player-visible wording coming from the spec.
- Everything must behave correctly at 30 and 60 FPS (project constraint). The spec has a tolerance section; check that it is testable.

Parallel steps opened by the Studio at the same time as this one (their outputs may affect Build): a QA defect log for the duplicate spit line (12) and an art-director review of the new visual states (13). Plan around the possibility that the visual glyph/color notes change before Build starts.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002: rework existing enemy behavior first (Option A); Option B deferred; Option C out of scope.
- D-003: room mix is across rooms; zero hearts ends the run; room clear heals one heart.

## Constraints

- No new input buttons. Desktop, keyboard and gamepad.
- Correct at both 30 and 60 FPS.
- Small team: reuse the existing enemy, projectile and timer systems.
- Do not change the spec's player-facing behavior. If something is infeasible within the constraints, say so and hand back (see Expected output); do not redesign.

## Open questions

- Is the attack-slot limit and the aim-lock feasible as specified, with the existing systems?
- Is parallel work worthwhile, or is this one change set? (Isolated workspaces only if you decide independent code changes run in parallel.)
- How should AC-1…AC-17 be covered by tests, including frame-rate independence? Which can be run through `run_tests` or `run_bots`, and which need a play script?
- Who updates `manual.md`, and when?

## Expected output

A technical plan: approach, order of work, risks, tests per acceptance criterion, as-built values to report, manual update task. Address the result to `studio`. Recommended next recipient: `gameplay-engineer` (Build). If the spec is infeasible or underspecified, say so and name the case; the Studio will send it to `game-designer`.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/10-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
---
# Role: Technical Director

## Responsibility

Turns approved specs into technically feasible plans. Owns technical risk, architecture, test
strategy, sequencing, and whether work can safely run in parallel.

## Decides

- Technical approach and architecture within the project's constraints.
- Sequencing, task breakdown, and parallelization (including isolated code workspaces).
- Technical acceptance checks (e.g., performance budgets) that serve the spec.

## Must not

- Change the spec to suit the implementation — propose the change to `game-designer`.
- Decide game direction or player-facing behavior.
- Approve its own plan's results; QA verifies the build.

## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.

## Produces

- A plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
  decision with its reason.
- Technical Decisions where a real alternative was rejected.

## Hands back / escalates when

- The spec is infeasible within constraints → `game-designer`.
- The cost or scope exceeds what the Goal implies → `game-director`.
- The work is irreversible or high-risk → Owner, via an Escalation it prepares.

## Typical skills

technical-plan, make-decision, prepare-owner-escalation
>>>END

<<<FILE studio/skills/technical-plan.md
---
name: technical-plan
description: Turn an approved spec (or a technical problem) into an implementation plan with affected systems, ordered tasks, risks, test strategy, and a parallelization decision.
---
# Skill: Technical plan

Typical roles: technical-director.

## When to use

The approach is non-obvious, risky, touches several systems, or could be parallelized; or a
technical problem needs diagnosis.

## Inputs

The approved spec and acceptance criteria, project constraints, the repository.

## Method

1. Map spec items to affected systems. Find what already exists and can be reused.
2. Order the tasks; mark dependencies.
3. List risks with mitigations (performance, frame-rate dependence, data compatibility, save data).
4. Define the test strategy: what is automated, what QA checks manually.
5. Decide parallelization: parallel only for code changes that are independent; give the reason
   either way. Isolated workspaces only for parallel code changes.
6. Flag anything infeasible, much costlier than the Goal implies, or irreversible.

## Output

Plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
decision, flags.

## Do not

Change the spec to make the plan easier — propose the change instead.
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

<<<FILE goals/G-001-combat-monotony/10-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 10
from: game-designer
to: studio
stage: Specify
outcome: done
---
# 10: game-designer → studio — Option A spec written; rulings on questions 1–7

## Task

Decide whether Plan is needed, then route the spec to Build (`gameplay-engineer`). Route the other items below.

## Context

G-001: combat monotony. D-002 chose Option A. The spec is in `design/combat.md` (build 0.5 target) and the run/room rules are recorded in D-003. It was checked against the rooms 4–5 report (08) and QA's report (06). No bots or play runs were used; the spec is not verified against the build.

## Findings

### What the spec changes (Option A, D-002)

- **Grub:** Approach → Wind-up (0.5 s, visible) → Strike (0.15 s) → Recovery (0.9 s). It is harmless outside Strike. At most 2 grubs attack at once. A hit during Wind-up cancels the strike.
- **Spitter:** Charge (0.8 s, visible) → Fire → Recovery. A volley every 2.5 s, staggered per spitter. The aim is locked at the end of the charge, so the shot can be dodged. Spitters can be approached and hit, and a hit during Charge cancels the shot.
- **Hit feedback:** swipe arc, damaged state, remaining HP in the text, multi-hit allowed.
- This answers the 08 observations: spitters as scenery, projectiles never reacted to, grubs as the only pressure, the dash buying quiet seconds with no use.

### Rulings

1. **Room mix:** across rooms, not per room. Rooms 1–3 are not defects. Per-room mixing is Option B (D-003).
2. **Zero hearts:** enemies stop, projectiles vanish, 2.0 s later a "run over" screen, attack starts a new run at room 1.
3. **Room cleared:** hearts carry over, +1 heart on clear, 1.5 s later the next room loads. It cannot happen while the player is down.
4. **Practice room and `x` marker:** documented in `design/combat.md`. The manual needs updating (see below).
5. **30/60 FPS:** criteria AC-1…AC-17 and the tolerance section in the spec.
6. **"(nothing happens)":** intended, but must always give a reason: miss, too soon, stunned, down.
7. **Twice-printed spit line:** one line per spitter is expected, but identical lines make it read as a duplicate. It is a minor presentation defect. **Route to `qa`** to log it. The spec requires the line to name the spitter (AC-8).

### Checks against 08

- Rooms 4–5 had no variety beyond count, and the spitters were mirrored. The spec therefore staggers them and gives them a dodgeable shot. It does not change D-002's scope.
- The dash gave a live player nothing to do with the quiet seconds. The spec gives the quiet time a use (counter in Recovery, approach a spitter).
- This does not contradict the diagnosis, so no Director return is needed.

## Decisions already made

- D-001, D-002 (unchanged).
- D-003 (new): room mix across rooms; run-end rule; room clear heal.

## Constraints

- No new inputs. Timings in seconds. 30 and 60 FPS. Reuse existing enemy, projectile and timer systems.

## Open questions

- **Manual changes needed** (not on my write list): list the practice room behavior, the `x` marker, the new glyphs/states, the swipe arc, the run-over screen, and the new attack messages in `manual.md`.
- Swipe reach, cone width and projectile speed are targets. Build should report as-built values.
- Glyph/color choices need `art-director` review (threat colors saturated orange/red).
- Feasibility of the attack-slot limit and the aim-lock is not checked. Ask `technical-director` or Plan if there is doubt.
- Run progression after "run over" is not defined. It is outside this goal unless the Director wants it.
- All timings marked [tune] need a live playtest after Build, especially to see that grubs are not trivial and the dash still matters.

## Expected output

The Studio routes: Plan if wanted, then Build; `qa` for the duplicate spit line; `art-director` for the visual states. After Build, QA verifies AC-1…AC-17 at 30 and 60 FPS, then a live reactive playtest. Reopen Option B only if that playtest still shows sameness (D-002).

## Sender assessment

Confidence medium-high that the rules fix single-state, untelegraphed behavior. The effect size and the numbers are unproven until a live playtest.

## Load

- Role: studio/roles/qa.md or studio/roles/gameplay-engineer.md (per routing)
- Skills: none specified
- Project: design/combat.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/09-studio-to-game-designer.md
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
