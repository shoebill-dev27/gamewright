# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/13-studio-to-art-director.md
next_seq: 16

## You may write

- goals/G-001-combat-monotony/16-art-director-to-<recipient>.md
- design/<name>
- decisions/D-005-<name>.md

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

<<<FILE goals/G-001-combat-monotony/13-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 13
from: studio
to: art-director
stage: Design
outcome: routed
---
# 13: studio → art-director — Review the visuals of the Option A spec before Build

## Task

Review what the player will see under the Option A spec (glyphs, colors, states, telegraphs, swipe arc, run-over screen) for readability and consistency with the art direction, and give the visual rulings Build needs.

## Context

G-001: the Owner finds combat monotonous. The game-designer specified a rework of the grub and spitter behavior (D-002, Option A) in `design/combat.md`. The new behavior depends on telegraphs the player can read: the grub Wind-up (0.5 s), the spitter Charge (0.8 s), damaged states, the swipe arc, the downed marker and the run-over screen. Pillar 3 requires every threat to be visible before it can hurt the player. The game is a headless build shown as text; "what the player sees" is the `run_play` view.

## Findings

From the designer's hand-off: glyph and color choices in the spec need art-director review (threat colors saturated orange/red against the dark cave). The rooms 4–5 playtest (08) found that spitters read as scenery and their shots were never reacted to.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: Option A, reuse existing enemy behavior.

## Constraints

- Art direction in `project.md#art-direction`; small team, reuse existing systems.
- Do not change rules, timings or parameters; those belong to the game-designer. If a visual problem needs a rule change, say so as an open question.
- No new inputs.

## Open questions

- Is each telegraphed state (Wind-up, Charge, Recovery) distinguishable from the idle and harmless states in `run_play`?
- Do the threat glyphs/colors read against the dark, and are damaged states and the downed marker clear?

## Expected output

A short visual review with concrete rulings (what to keep, what to change), written in Findings of the outgoing Handoff, and edits to the visual parts of `design/combat.md` only if needed. Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md, studio/skills/write-design-spec.md
- Project: project.md#art-direction, project.md#vision, design/combat.md, manual.md, goals/G-001-combat-monotony/08-playtester-to-game-designer.md
- Decisions: decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/10-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/art-director.md
---
kind: role
id: art-director
writes: design/*, decisions/*
---
# Role: Art Director

## Responsibility

Owns visual expression and visual consistency: style, readability, and the clarity of everything
the player sees.

## Decides

- Visual direction within the vision: colors, shapes, effects, UI presentation for a change.
- Visual acceptance: whether a change is readable and consistent with the art direction.

## Must not

- Change gameplay rules or parameters — that is `game-designer`.
- Change the art style pillars of the vision — escalate.
- Write production code.

## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).

## Produces

- Visual spec for a change: what must be visible, how, and visual acceptance criteria.
- Visual review verdict with evidence.

## Hands back / escalates when

- The visual problem is really a rules problem → `game-designer`.
- A style pillar would change → `game-director`, for an Owner escalation.

## Typical skills

visual-review, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/visual-review.md
---
name: visual-review
description: Review what the player sees for readability and consistency with the project's art direction, producing a verdict with evidence.
---
# Skill: Visual review

Typical roles: art-director.

## When to use

A problem may be visual, or a change affects what the player sees.

## Inputs

The build or captures, the art direction in the Project Context, the spec's visual criteria.

## Method

1. Check readability first: can the player tell what matters (threats, interactables, state) at a
   glance, in every environment and lighting condition the game has?
2. Check consistency with the art direction: palette, shapes, effects, UI style.
3. Check the spec's visual acceptance criteria.
4. Separate visual issues from rule issues; route rule issues to `game-designer`.

## Output

Visual verdict: pass/fail per criterion, readability issues with evidence and where they occur,
consistency notes, proposed visual direction for fixes.

## Do not

Change gameplay rules. Do not judge by personal taste over the project's art direction.
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
>>>END

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
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
