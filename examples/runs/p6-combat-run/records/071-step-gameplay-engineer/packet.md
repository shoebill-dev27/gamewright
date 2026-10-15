# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/66-studio-to-gameplay-engineer.md
next_seq: 67
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/67-gameplay-engineer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/66-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 66
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 66: studio → gameplay-engineer — Build the combat response change set (re-issue of 61, with repo files and the Q1 answer)

## Task

Implement the approved spec in `design/combat.md` (AC-19…AC-28 and the parameters and rules they cover) and `design/combat-visuals.md` (V-9…V-17) on the existing simulation in `repo/`. Add tests, run the suite (`run_tests`), and report build notes.

## Context

G-001 (combat feels monotonous), Option A (D-002, D-004): rework existing enemy behavior as one sequential change set. Build 61 came back as a question (63) for two reasons: its packet had no `repo/` files, and the spec lacked the knockback direction of a grub at distance 0. The designer closed the gap in 65 (rule in D-013, criterion AC-28) and cleaned three passages (dash and walls, Waiting positions, AC-23). This packet names the repo files in Load. Read them directly.

## Findings

From 65, the points that change what you build:

- **Knockback (D-013, AC-28):** the first hit knocks a grub back 1 tile over 0.2 s. A grub 0.05 tile or more from the player is pushed straight away. A grub on the player's tile goes toward its display side (D-006): the side it last approached or struck from, otherwise right, left, above, below. That side needs 1 tile of clear room; if not, use the next side in that order. A push toward an edge is clamped at the edge, like the dash. Knockback does not change state or timers. A grub knocked back from distance 0 ends about 1.0 tile away and keeps its cap slot. A grub hit from 0.5 tile or more ends 1.5 tiles or more away and frees a slot.
- **Swipe result line** stays "you swipe: grub hit (1 left)" for every grub. An on-tile grub's position comes from the `on you:` line (AC-28(e)).
- **Dash and walls:** a dash always lasts 0.25 s with invulnerability for all of it, even when a wall shortens it. It is never cancelled by a wall. AC-25 checks 0.25 s on a 2-tile wall dash.
- **Waiting positions:** a cap-blocked grub holds at 2.0 tiles or more, backs off if the player approaches, follows to stay at about 2.0 tiles, and resumes Approach when a slot frees. A spacing-blocked grub approaches until within 1.25 tiles, then stands still until the window ends. If it is already inside 1.5 tiles, it stands where it is and counts toward the cap of 2.
- **AC-23** is split into (a) on tile at 0.2, (b) 0.4 tile behind, (c) 0.8 tile behind ("(miss) not in front"), with explicit scripts.
- No parameter value changed in this round.
- If the current code differs from any rule above (the on-tile knockback, the Waiting-follow behavior), report it in the build notes. The spec stands.

## Decisions already made

- D-001: no new input buttons.
- D-002, D-004: Option A, one sequential change set.
- D-005, D-007: the Owner places `manual.md` text. Do not edit `manual.md`.
- D-006: overlap display, and the display side used by the on-tile knockback.
- D-009: the `ManualTest` phrase check ignores line wraps.
- D-011: grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: the `on you:` line and the attacker's position in hit lines.
- D-013: knockback of a grub on the player's tile.

## Constraints

- Must play correctly at 30 and 60 FPS. Timers run on elapsed seconds, including the 0.2 s knockback.
- Prefer changes that reuse existing systems. If the Waiting behavior of a blocked grub is not local to existing systems, stop and report; a Plan step (11) may follow.
- Stop on spec ambiguity and hand back; do not decide.
- `manual.md` is Owner-placed. If `ManualTest` fails only because manual text from 59 or V-15 is not yet placed, report which phrases, and do not edit the manual.

## Open questions

None.

## Expected output

An outgoing Handoff addressed to `studio` (so the Studio can compose the QA and art-director Verify packets), with:

- the code and test changes in `repo/`, and the `run_tests` result;
- build notes: any spec/code mismatches found, the root cause of any defect, and anything you could not verify;
- a Sender assessment, which will be removed before QA receives it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md (read only), repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-option-a-single-change-set.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/65-game-designer-to-studio.md
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

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text. Updated after QA's second round (handoff 29): overlap rule and AC-15 wording (D-006). Updated after playtests 50 and 54 (handoff 59): grub spacing and engagement cap, shorter hit-stun, body-hit rule, dash and facing rules, swipe cases, miss wording (D-011). Acceptance criteria AC-19 to AC-27 are new. Updated after the engineer's hand-back (63, answered in 65): knockback of a grub on the player's tile (D-013, AC-28), and rewrites of the dash-and-walls, Waiting and AC-23 passages (no rule change in those three).

## Experience intent

Every enemy does something the player can read, answer and profit from. A grub is a threat with a beat: it approaches, winds up, strikes, then is open to a counter. A spitter is a threat on a rhythm that the player can dodge or break by walking up and hitting it. The player's attack visibly changes the enemy. Fights are decided by spacing and timing with attack and dash only (D-001, pillars 1 and 3). A group of grubs takes turns: the player always has a gap to answer in and is never boxed in by simultaneous bites.

## Conventions

- All timings are in seconds and must hold at 30 and 60 FPS (section "30 / 60 FPS").
- Distances are in tiles. The room is 16×9 (x 0–15, y 0–8).
- "Telegraph" means a change the player can see in the player view, at least one on-map change plus one text line. Threat colors are saturated orange/red. The on-map change must be visible in a cell the player can see: an enemy glyph is never hidden under `P` (see "Overlap with the player").
- Values marked **[tune]** are starting values the designer expects to adjust after a live playtest of the Option A build.
- "True position" is the simulated position of an enemy, not the cell where its glyph is drawn.

## Player kit

- **Attack** (one button): a swipe in the facing direction.
  - Damage 1. Recovery 0.35 s.
  - Reach 1.5 tiles, in a 90° cone centred on the facing direction.
  - **Body-hit rule (A3):** an enemy whose true position is within 0.5 tile of the player (including distance 0, "on you") is hit by every swipe, whatever the facing. The swipe still draws its arc in the facing direction.
  - A swipe hits every enemy that is in the cone or inside the body-hit radius. Hitting two enemies with one swipe is intended and rewards positioning.
  - **Swipe in any enemy state:** a swipe resolves against true positions at the moment of the press, whatever state the enemy is in (Approach, waiting, Wind-up, Strike, Recovery). See the grub rules for what the hit does.
  - **Swipe result line and an on-tile grub (Q2):** the result line is the same wherever the grub is: "you swipe: grub hit (1 left)". It never carries "(on you)". The position of an on-tile grub is read from the `on you:` line.
  - Rulings in "Attack feedback" below.
- **Facing:** movement sets facing to the movement direction. The player cannot turn without moving or dashing (D-001; see D-011 on why this is held).
- **Dash**: up to 4 tiles over 0.25 s, invulnerable for the full dash. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends. The dash passes through enemies and projectiles without harm.
  - **Dash direction:** `dash <dir>` goes in that direction. A dash without a direction goes the way the player faces.
  - **Dash and facing (A5):** a dash sets facing to the dash direction, like movement does. A queued attack fires in that direction. A dash without direction leaves facing unchanged.
  - **Dash and walls (A5):** a dash that would leave the room stops at the room edge and is never cancelled; it covers the shorter of 4 tiles and the distance to the edge, and every dash lasts exactly 0.25 s with invulnerability for all of it, even when a wall shortens it.
  - Dash starts from the player's true position; any partial tile is kept (no snapping to the grid).
- **Getting hit**: 1 heart of damage, then **0.15 s hit-stun (no input) [tune]** (was 0.3 s), then invulnerability until 0.8 s after the hit (unchanged).
- **Hearts**: 3 maximum.
- **Moving while attacking**: allowed. Movement continues during the 0.35 s recovery.

## Enemies

### Grub (HP 2)

States: **Approach → (Waiting) → Wind-up → Strike → Recovery → Approach**.

| State | Duration | Rules |
|---|---|---|
| Approach | until in range | Walks at the player at 2.0 tiles/s (as observed). Harmless. |
| Waiting | until allowed | The grub is blocked by the spacing rule or the engagement cap below. It is harmless, with normal glyph `g`/`w`, and prints no text line. What it does while waiting is set out under "Waiting positions". |
| Wind-up | 0.5 s **[tune]** | Starts when the grub is within 1.25 tiles of the player and the rules below allow it. The grub stops, and its glyph and color change (see "Feedback"). A text line "a grub rears back" prints. It deals no damage. |
| Strike | 0.15 s | A short lunge of up to 1 tile toward where the player stood when the wind-up ended. It damages the player once (1 heart) if the player is within 1.0 tile of the grub at any moment of the strike and is not invulnerable. |
| Recovery | 0.9 s **[tune]** | The grub stands still, "open". No damage. Its normal glyph returns. |

- Cycle with a player standing still: 0.5 + 0.15 + 0.9 = about 1.55 s per bite.
- **Wind-up spacing (A1):** a grub may not start a Wind-up within **1.0 s [tune]** of the start of any other grub's Wind-up (a cancelled or defeated grub's wind-up start still counts). A grub that is blocked becomes Waiting. When the window ends, the nearest Waiting grub starts first; ties go to the grub that has waited longest. With one grub in the room the rule has no effect. A grub's own cycle is unchanged.
- **Engagement cap (second rule, D-011):** at most **2** grubs may be within 1.5 tiles of the player at once, counted in every state, by true position. A grub that has reached 2.0 tiles from the player while two grubs are inside 1.5 tiles becomes Waiting at that distance and enters when a slot frees (a grub is defeated, or is knocked back or pushed out beyond 1.5 tiles). The nearest waiting grub enters first. The cap limits where grubs move; it does not stop the player from walking or dashing next to more grubs, because there is no collision.
- **Waiting positions (clarified, no rule change):**
  - *Blocked by the cap:* the grub holds at 2.0 tiles or more. If the player walks toward it, it backs off to stay at 2.0 tiles or more; if the player walks away, it follows to stay at about 2.0 tiles. When a slot frees it resumes Approach.
  - *Blocked by the spacing window only:* the grub keeps approaching until it is within 1.25 tiles, then stands still in place until the window ends. A grub that is already inside 1.5 tiles when it gets blocked stands still where it is. It does not retreat, and it counts as one of the two in the cap.
  - A grub between 1.25 and 2.0 tiles is therefore either still approaching (a slot is free), or on its way back to 2.0 tiles (cap full and it is outside 1.5 tiles). It is never standing still there.
- **Attack limit (kept):** at most 2 grubs may be in Wind-up or Strike at the same time. With the 1.0 s spacing this is nearly always at most 1, but the limit is kept as a backstop.
- **Player hits on a grub:**
  - First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s and shows the damaged state. Direction and room edge are set under "Knockback direction" below.
  - A hit during Wind-up cancels the wind-up. The grub goes straight into a 0.6 s Recovery and does not strike.
  - **A hit during Strike (A5)** cancels the rest of the strike: if the strike has not yet damaged the player in that tick or earlier, no heart is lost. The grub goes into a 0.6 s Recovery. Player attacks resolve before enemy damage in each tick (same order as room clear).
  - A hit during Recovery or Approach/Waiting: damage and knockback as above; Recovery continues for its remaining time.
  - Second hit: the grub is defeated.
- Grubs never damage the player outside Strike, so the dash and spacing are the answers: step back, or dash through the wind-up, then counter in Recovery. Hitting a winding-up grub (interrupt) is the best answer.

#### Knockback direction (Q1, D-013)

- **Normal case:** a grub whose true position is 0.05 tile or more from the player's is knocked back 1 tile straight away from the player, along the line from the player to the grub.
- **Grub on the player's tile (true distance under 0.05 tile):** it is knocked back 1 tile toward the side on which it is drawn, that is, the display side of "Overlap with the player" (the side it last approached or struck from, otherwise right, left, above, below). It therefore ends up in the cell where its glyph was already drawn. The player sees the grub step out to the side it was shown on, and nothing jumps to the other side.
- **Room edge:** the side must have at least 1 tile of clear room for the grub. If the display side has less, the grub is moved to the next side in the order right, left, above, below that does have 1 clear tile. A 16×9 room always has one. A normal-case knockback toward an edge is clamped at the edge, the same way a dash is.
- **Slots:** a grub knocked back from distance 0 ends about 1.0 tile from the player, so it stays inside 1.5 tiles and keeps counting toward the cap of 2. A first hit from distance 0 does not free a slot. A grub hit from 0.5 tile or more away ends 1.5 tiles or more away and does free one.
- **Cycle:** knockback changes where the grub is, not its state or timers. The AC-4 timing (next bite no sooner than 1.5 s after the previous one for a still player) is unchanged. A knocked-back grub walks back in Approach if it is not in Recovery, or stays where it landed until Recovery ends.
- **Timing of the display:** the knockback takes 0.2 s. The immediate draw at the swipe may still show the grub on the tile with its `on you:` entry. A draw made 0.2 s or later after the hit shows it on the knockback side as a normal neighbor, with no `on you:` entry for it (V-17, AC-28).

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
- The grub spacing and engagement rules do not apply to spitters.

### Group behavior

- A grub is never threatened by friendly projectiles. Projectiles only affect the player.
- Enemies do not block projectiles.
- Grubs take turns (spacing) and crowd at most two deep (cap). Grubs in the same room still all arrive at about the same time; staggered arrival stays Option B (D-002).

### Overlap with the player (F1 ruling, D-006)

- **Physics unchanged.** Enemies and the player have no collision. A grub's lunge and recovery may leave it within the player's tile, and the player may walk or dash onto an enemy. This adds no rule to movement, timing, damage or hit tests; all of those use true positions.
- **Display rule.** In the player view no enemy is ever hidden under `P`. The player is always drawn on their own cell. If an enemy's cell equals the player's cell, that enemy's glyph is drawn in the nearest free in-room cell next to the player (the cell on the side the enemy last approached or struck from first; otherwise right, left, above, below, in that order; if all four are occupied, the next free cell by distance). This is a display offset only.
- It applies in every state, so a grub in Recovery that is "open (on you)" is also visible and its counter can be read. It applies to both enemy types and to damaged glyphs.
- Two enemies sharing the player's cell are displaced to different cells.
- The text lines are unchanged ("(on you)" still prints). The displaced glyph is the on-map change that makes the telegraph complete.
- The immediate draws at Wind-up start, Strike and Recovery start (visuals spec principle 4) use this rule too.
- A displaced glyph does not mean the enemy has moved. A swipe hits by true position, so a swipe may hit an enemy drawn on a different side than the arc. The body-hit rule makes this safe for an enemy "on you": it is always hit.
- The display side is also the direction in which an on-tile grub is knocked back by the first hit (see "Knockback direction").

## Attack feedback (applies to all enemies)

- **Swipe is always visible.** Every swipe, hit or miss, draws a short arc on the map for 0.15 s in the facing direction.
- **Damaged state.** After 1 hit an enemy shows a distinct glyph/color, and the hit line states its remaining HP: "you swipe: grub hit (1 left)". A defeat prints "grub defeated".
- **Multi-hit.** A swipe that hits two enemies prints one hit line per enemy.
- **"(nothing happens)" ruling (Q6).** It is intended that a swipe sometimes does nothing, but never silently. It must say why:
  - "(miss)": the swipe landed but no enemy was hit. The line keeps the word "(miss)" and adds a cause when one is known (A5):
    - "(miss) too far": no enemy was hit, and at least one living enemy is within 2.5 tiles of the player but beyond the 1.5-tile reach.
    - "(miss) not in front": no enemy was hit, and at least one living enemy is within 1.5 tiles but outside the cone and outside the 0.5-tile body-hit radius.
    - "(miss)" alone otherwise. If both causes apply, "not in front" is printed.
  - "(too soon)": the 0.35 s recovery after the previous swipe has not finished.
  - "(stunned)": hit-stun, the first 0.15 s after taking a hit.
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
- Room 1 composition is not changed (D-011 rejects D2 for now).
- Per-room mixing, moving spitters and staggered grub arrival are Option B and stay deferred (D-002).
- A room ends when all enemies are defeated.

## Edge cases

- **Simultaneous hits on the player (grub strike and projectile in the same tick):** one heart is lost, and the 0.8 s invulnerability covers the other.
- **Player hit during an attack's recovery:** the recovery continues after the stun; the swipe shows "(stunned)" if pressed during stun.
- **Dash during stun:** ignored with "(stunned)". The stun is 0.15 s; a dash pressed after it is accepted if the cooldown allows ("(dash not ready)" otherwise).
- **Enemy defeated mid-state:** it stops acting at once. A defeated grub does not strike.
- **Two grubs wanting the same slot (spacing window, Wind-up limit or engagement cap):** the nearer grub takes the free slot; a tie goes to the grub that has waited longest.
- **Four grubs around a still player (room 2):** at most 2 are within 1.5 tiles, Wind-ups start at least 1.0 s apart, and the others wait at 2.0 tiles. The player has at least 1.0 s between committed bites to dash out or counter.
- **Grub knocked out of the engagement zone:** it frees a slot at once; it is Approach again and may be Waiting if the cap is full when it returns. A grub hit while on the player's tile is not knocked out of the zone (it ends about 1.0 tile away), see "Knockback direction".
- **Player dashes through a grub in Wind-up:** the grub still completes its Wind-up, Strike (toward where the player stood when the wind-up ended) and Recovery; its strike misses if the player is more than 1.0 tile away.
- **Swipe at the same tick as a strike's damage:** the swipe resolves first (see "Player hits on a grub").
- **Dash into a wall or into the room edge:** stops at the edge, see Dash.
- **Spitter Charge canceled by a hit:** the projectile is not fired.
- **Enemy on the player's tile:** see "Overlap with the player". It is drawn beside `P`; the body-hit rule means a swipe always hits it; the first hit knocks it onto the side it is drawn on.
- **Player down while an enemy shares the cell:** `x` is drawn on the player's cell and the enemy keeps its displaced cell.
- **Pause:** all timers freeze.

## 30 / 60 FPS (Q5)

- Every timer above runs on elapsed seconds, not frame counts. This includes the spacing window (1.0 s), the dash duration, the hit-stun (0.15 s) and the knockback (0.2 s).
- Tolerance: an event's trace timestamp may differ from its spec time by at most 0.04 s at 30 FPS and 0.02 s at 60 FPS.
- The Strike damage window (0.15 s) must cover at least 4 frames at 30 FPS.
- The hit-stun (0.15 s) is at least 4 frames at 30 FPS; it ends at the first tick at or after 0.15 s.
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
- **AC-11 Hit feedback:** each swipe prints exactly one outcome per enemy hit ("hit (1 left)", "defeated") or one reason ("miss", "too soon", "stunned", "down"). "(nothing happens)" never appears without a reason. A damaged enemy has a distinct glyph/color from a full-HP one. (The "(miss)" line may carry a cause, see AC-27.)
- **AC-12 Multi-hit:** one swipe with two grubs inside the cone prints two hit lines.
- **AC-13 Zero hearts:** after the third hit, "you went down" prints, `x` replaces `P`, enemies stop, projectiles vanish, and attack prints "(down)". After 2.0 s the run-over screen shows. Pressing attack there starts room 1 with 3 hearts.
- **AC-14 Room clear:** "room cleared" prints on the last defeat, projectiles vanish, hearts +1 (max 3), and the next room loads after 1.5 s. A clearing swipe at the same tick as a would-be strike results in no damage. Clearing room 5 prints "run complete".
- **AC-15 Practice room:** `room empty` works as described, and both `x` and the practice room are listed in `manual.md#on-screen` (the On screen section, not only the Script table or Rooms and runs).
- **AC-16 Room mix:** the trace setup rows match the layouts above.
- **AC-17 Frame rate:** AC-1…AC-14 and AC-18…AC-28 pass at both frame rates, and the 30/60 comparison above holds.
- **AC-18 No hidden enemy:** in the practice room with an idle player and one grub at distance 4, run to 5.5 s, every draw that shows a living grub has a grub glyph in a cell different from the player's cell. Every "a grub rears back" line, including those marked "(on you)", comes with an uppercase `G` or `W` visible on the map in the draw made at that moment. Same for "the grub is open (on you)": a lowercase `g` or `w` is visible. Also, with `player 8 4` and `spawn spitter 8.2 4`, the draws show `P` and an `s` in a neighbouring cell; the spitter's `S` is visible beside `P` during its Charge. The trace shows no change to timings, hearts or positions compared with a build without the display rule (the events of AC-1…AC-4 stay within tolerance).
- **AC-19 Wind-up spacing (A1):** in room 2 with a still player, run to 12 s (or until down): for every pair of grub Wind-up starts in the trace, the later one is at least 0.96 s after the earlier one at 60 FPS and 0.92 s at 30 FPS (1.0 s minus tolerance), whichever grubs they belong to. The same holds in room 1 and room 5. A room with a single grub shows the AC-2 cycle unchanged.
- **AC-20 Engagement cap:** in room 2 with a still player at x 8, y 4, the trace shows at no sample more than 2 grubs within 1.5 tiles of the player, from the start to the end of the run. The remaining grubs are present in the draws at about 2.0 tiles with lowercase glyphs and no "rears back" line until a slot frees.
- **AC-21 Turns, not a ring:** in room 2 with a still player, the time between the first and the third heart lost is at least 1.9 s. No two Wind-up starts fall within 1.0 s (AC-19), so the trace shows at most one grub in Wind-up or Strike at any sample.
- **AC-22 Hit-stun:** after a heart is lost, an attack pressed 0.05 s later prints "(stunned)" and does nothing. An attack pressed 0.25 s later swipes normally. A dash behaves the same way (subject to its cooldown). The stun lasts 0.15 s within tolerance. Invulnerability still ends 0.8 s after the hit.
- **AC-23 Body hit (A3):** three practice-room checks, each at both frame rates.
  - (a) On tile: `player 8 4` and `spawn grub 8.2 4`, with no movement before the swipe (default facing). The swipe hits the grub and prints "grub hit (1 left)", whatever the facing.
  - (b) Just behind: `player 8 4`, `move right` then `stop` (facing right), and a grub spawned 0.4 tile to the left of the player's true position. The swipe hits it. Repeat with `move left` then `stop` and the grub 0.4 tile to the right.
  - (c) Further behind: with the same setups as (b), a grub 0.8 tile behind the player is not hit and the swipe prints "(miss) not in front".
- **AC-24 Dash and facing (A5):** in the practice room, `player 8 4`, face right (move right then stop), then `dash left`, then an attack after the dash: the arc is drawn as `(` (facing left). A `dash` without a direction while facing up leaves facing up. A queued attack pressed during a dash fires after it ends in the dash direction.
- **AC-25 Dash distance (A5):** in the practice room from `player 8 4`, `dash right` ends at 12.0 ± 0.25 on x at both frame rates and takes 0.25 s within tolerance. From `player 2 4`, `dash left` ends at the room edge (x 0, never outside the room), takes 0.25 s within tolerance even though it covers only 2 tiles, and the player takes no damage during it. Dash during the cooldown prints "(dash not ready)" and does nothing.
- **AC-26 Swipe during Strike and Recovery (A5):** with one grub in the practice room, a swipe pressed while the trace shows the grub in Strike hits it ("grub hit (1 left)") and no heart is lost to that strike if the swipe's tick comes at or before the damage tick. A swipe pressed while the grub is in Recovery and adjacent in front hits it. Neither case prints "(miss)".
- **AC-27 Miss wording (A5):** a swipe with a grub 2.0 tiles in front prints "(miss) too far". A swipe with a grub at 1.0 tile directly to the side (outside the cone) prints "(miss) not in front". A swipe with nothing within 2.5 tiles prints "(miss)" alone. All three also draw the arc.
- **AC-28 Knockback of an on-tile grub (Q1, D-013):** in the practice room, one grub, a still player, and a swipe on the first hit. Read the true positions from the trace and the cells from the draws.
  - (a) `player 8 4`, `spawn grub 8 4`. The grub is shown on some side of `P` (the `on you:` line says which). After the first hit, a draw made 0.2 s or more later shows the damaged grub (`w`/`W`) at 1.0 ± 0.1 tile from the player, in the cell on that same side, with no `on you:` entry for it. The grub did not appear on any other side in any draw.
  - (b) With the grub's display side blocked by the room edge (`player 15 4`, `spawn grub 15 4`, grub last shown right is not possible; instead use `player 14.5 4` and a grub that approached from the right and sits on the player's tile), the first hit moves the grub to another side that has 1 tile clear (left, in this case). It never ends outside the room and never at less than 0.9 tile from the player.
  - (c) With room 2 and two other grubs inside 1.5 tiles, a first hit on an on-tile grub leaves it inside 1.5 tiles, so the trace shows no third grub entering the zone because of that hit. A first hit on a grub 0.6 tile or more away leaves it at 1.5 tiles or more.
  - (d) The grub's state timers are unchanged by the knockback (AC-4: next bite no sooner than 1.5 s after the previous one for a still player).
  - (e) A swipe result line for an on-tile grub reads "you swipe: grub hit (1 left)" with no "(on you)" (Q2).

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A playtester can say, unprompted, what a grub is about to do before it bites, and describes a reason to move or dash.
- A playtester reacts to a projectile at least once (moves, dashes or approaches a spitter) and can tell the two spitters apart.
- Rooms 4 and 5 are described as different from each other and from rooms 1–3 by what the player does, not only by enemy count.
- The playtester can tell from the screen how many hits an enemy needs.
- Grubs are neither trivial nor unfair: the playtester takes some damage in rooms 4–5 but can explain how it happened. (If grubs read as trivial, or the dash seems unnecessary, retune within D-001.)
- A playtester who stands still can see on the map where the grub that bites them is, including when it is right on top of them.
- A playtester in room 2 does not describe being boxed in by grubs on both sides with no way out.
- A playtester does not say they could not hit a grub that was next to or on them (A3).
- A playtester who hits a grub on top of them sees it step out to the side it was shown on, and does not describe it as jumping to somewhere unexpected.
- Observed in QA captures (no ruling): an idle player went to zero hearts at about 5.0 s in the practice room and in room 1 before these changes. That is expected for a player who does nothing. After A1 and the engagement cap the idle time to down is expected to be a little different; it is a reference value, not a target. Retune the **[tune]** values from live play.

### Retest guideline (design-side; for the next Play and Review, qualitative)

What a skilled player should be able to do. Numbers belong only in the acceptance criteria above.

- **Room 1 (3 grubs):** a skilled player who reads the cues can clear it and normally keeps most of their hearts. Damage comes from a misread cue or a mistimed dash, not from a bite they could not avoid. They can answer a rear-back by stepping out, by dashing through, or by hitting the winding-up grub, and then punish the open grub. After a hit they can swipe again quickly. A grub right on them can be hit.
- **Room 2 (4 grubs):** a skilled player can break the ring: only two grubs crowd them, bites come one at a time with a gap, and they can dash out to a side or a wall and fight the nearest grub from a free line. The room should still be a real fight where taking a hit or two is plausible, but a player who tries should clear it, usually with at least one heart left. A player who stands still loses; that is meant.
- Judge sameness only on a survived run. A player who cannot clear room 1 or 2 says nothing yet about monotony (see 53 and 54).
- Report from the retest, because they decide the held items: (1) swipes that print "(miss) not in front" while the player aimed at that grub (A4); (2) swipes aimed after a dash that hit air (facing, D1); (3) whether four grubs still arrive as one clump that feels like a wall (D2 / Option B); (4) whether a grub knocked off the player's tile stays in the fight too long, since it keeps its cap slot (D-013).

## Held back or rejected (see D-011, D-013)

- **A4 cone width 90° → about 120°:** held. It comes in if the retest shows that the "(miss) not in front" line appears on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or that testers report missing grubs standing diagonally in front after A3 is in. Then widen to 120° **[tune]** and add its AC.
- **D1 facing mechanic (turn without moving, auto-face, backstep dash, 360° swipe):** not taken. It goes to `game-director` only if the retest still reports swipes into air after dashes or turning trouble with A3 and the dash-facing rule in.
- **D2 room 1 composition (fewer grubs, staggered arrival):** not taken. A1 and the cap give the intended effect inside Option A.
- **Knockback of an on-tile grub along the player's facing, a fixed direction, or none:** not taken (D-013).

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director. The art-director may review the choice of the displaced cell for readability (see D-006).
- The as-built dash distance and the facing behavior after a dash are being checked by QA (55). Where the build differs from the rules above, the rules above stand and QA's result becomes a defect, unless QA shows a rule cannot be built.
- Whether the run has any progression after "run over" is outside this spec.
- If the repo already knocks an on-tile grub in some other direction, the engineer reports it at the next Build; the rule in "Knockback direction" stands.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-visuals.md
# Combat visuals (build 0.5 target, Option A, G-001)

Status: visual spec and review rulings from the art-director for `design/combat.md`. It changes no rules, timings or parameters. Wherever it names a glyph or color, it covers what `combat.md` leaves to "chosen in Build". Build may change a glyph only if it keeps the rules in this file and documents the change in `manual.md`. V-9 to V-17 and the sections "Enemy on the player's tile" and "Hit lines name the attacker" were added for G-001 handoff 57 (see D-012).

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

## Position words (one vocabulary for all lines)

Every line that names where an enemy is uses the same words, relative to the player and taken at the moment the line prints:

- Same tile as the player: `on you`.
- Straight neighbors and further along a straight line: `left`, `right`, `above`, `below`.
- Other positions: the combined form already used for spitters, `top left`, `top right`, `bottom left`, `bottom right`.
- If two enemies of the same type would get the same words in the same draw, add the distance in tiles to both, for example `left, 1 tile` and `left, 3 tiles`. Do not add a distance otherwise, so the lines already praised stay as they are.

## Text lines (telegraph and feedback)

- Every telegraph prints a line at the moment the uppercase glyph appears. The line must say which enemy when more than one can act:
  - grub: "a grub rears back (left)" or "(above)", relative to the player, using the position words above. A grub on the player's tile reads "(on you)". If two grubs wind up on the same draw, print two lines.
  - spitter: "spitter (top right) charges" and "spitter (bottom right) charges", as in the spec.
- Spit lines name the spitter ("spitter (top right) spits"). There are never two identical lines.
- Grub Recovery start prints "the grub is open" with the position words, for example "the grub is open (left)". The 0.9 s counter window is the point of the rework, and in a still frame lowercase `g` looks the same as Approach.
- Swipe result lines follow the spec: "you swipe: grub hit (1 left)", "grub defeated", and the "(miss)", "(too soon)", "(stunned)", "(down)" reasons. They are unchanged by this spec. In the swipe line "(1 left)" is hit points remaining, so no position word is added there.
- Spitter stagger after a hit prints "spitter (top right) is staggered".

## Enemy on the player's tile

D-006 stands: an enemy sharing the player's tile is drawn in the nearest free cell beside the player and is never hidden. That drawn cell is a display offset only. The playtesters read it as the enemy's real position and could not tell which side a bite would come from or where to swing. The fix is a status line that says outright that the enemy is on the player's tile and where it was drawn. The glyphs stay the same and the lines already praised stay the same.

- **On-you line.** In every draw in which one or more enemies share the player's tile, a line `on you:` prints directly under the hearts line, above the room. It lists each such enemy once: its glyph as currently drawn, its state in words, and the cell it was drawn in. Format:
  - `on you: G biting soon (shown right)`
  - `on you: g open (shown below)`
  - with two, separated by `;`: `on you: G biting soon (shown right); g open (shown left)`
  - The state words are `walking`, `biting soon` (Wind-up and Strike), `open` (Recovery), `charging` (spitter Charge), `idle`. Use `biting soon` for both Wind-up and Strike so the line never lags the glyph.
  - `(shown <side>)` uses `left`, `right`, `above`, `below`, which is the cell D-006 chose.
  - When nobody is on the player's tile the line is absent, not blank, so its appearance itself means "something is on you".
- **Meaning of the displaced glyph.** The player reads the glyph beside `P` as "the one named on the `on you:` line" when the line is present. The attacker is on the player's tile, so a bite from it is not coming from the drawn side. The manual says this in one sentence (see V-15).
- **Telling a displaced enemy from a real neighbor.** In a color view the displaced glyph also gets a reverse-video (inverse) cell. This is only a reinforcement, and the on-you line carries the meaning without it. Shape and color of the letter do not change, so V-1, V-4 and V-6 are unaffected.
- **Telegraph and open lines** for an on-tile grub keep the existing wording with "(on you)", for example "a grub rears back (on you)" and "the grub is open (on you)". They print in the same draw in which the on-you line shows the new state.
- **Color.** The on-you line text is lantern-colored, never orange/red. Only the glyph letter inside it takes the glyph's color from the glyph table.
- **Valid under the designer's swipe rule.** This spec makes no claim about which enemies a swipe hits. The on-you line reports where enemies are and their state, whatever the swipe rule is. If a swipe hits a grub on the player's tile, the swipe result lines print as usual, and the enemy's disappearance and the on-you line follow the draw rules below.
- **When the enemy leaves or dies.** The on-you line updates in the same draw as the event that ends the overlap: the swipe that prints "grub defeated", the player's dash, or the grub leaving the tile. The displaced glyph and its line entry do not remain for a later draw.

## Hit lines name the attacker

- When the player loses a heart, the line names the attacker and where it was when the hit landed:
  - grub: `YOU ARE HIT by a grub (left)`, `YOU ARE HIT by a grub (on you)`, `YOU ARE HIT by a grub (above)`.
  - spit shot: `YOU ARE HIT by a spit shot from spitter (top right)`. The position is the spitter's position at the moment of the hit; if the spitter is gone, `YOU ARE HIT by a spit shot`.
- The position words and the ambiguity rule are those of "Position words". With a grub on each side, the line names the side of the grub that actually dealt the damage.
- The line prints in the same draw as the hearts line update, as it does now.
- The grub named in the line must have been an uppercase glyph (Wind-up or Strike) on that position in the draw or draws before the hit. This follows from the telegraph and is what V-14 checks.
- The "hit" case already has its own line, so no second or duplicate line is printed for the same hit. If two grubs are striking on the same draw and only one hit lands, only that one is named.

## Swipe arc

- It is drawn on every swipe, hit or miss, for the 0.15 s of the spec, plus the immediate draw required by principle 4. Without that draw a 0.15 s arc would almost never appear in a 0.5 s frame.
- It covers the tiles inside reach (1.5 tiles, 90° cone) in the facing direction.
- It is lantern-colored, never orange/red, so it is not confused with a threat.
- A miss shows the same arc with "(miss)", so the player sees how far the swipe reached.

## Run-over, down and clear

- **Down:** `x` in the cold gray-blue replaces `P`. The line "you went down" prints. Projectiles disappear in the same draw. The on-you line disappears too, since no enemy acts.
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
- **V-9** (on-you line present) Practice room: `player 8 4` and `spawn grub 8 4`. In every draw in which the grub is on the player's tile, a line starting `on you:` appears under the hearts line and names its glyph, state word and `(shown <side>)`. In every draw in which no enemy is on the player's tile, no `on you:` line appears.
- **V-10** (line matches the picture) In every draw with an `on you:` line, the glyph letter in the line is the letter in the cell beside `P` on the side the line states, and that letter matches the state (uppercase for `biting soon` and `charging`, lowercase for `walking`, `open` and `idle`). Verified by reading the text of the draw, with no color needed.
- **V-11** (real neighbor versus displaced) Practice room: one grub on the player's tile and a second grub on the tile immediately to the player's right. A draw shows both glyphs adjacent to `P` or beside it, and only one of them is named by an `on you:` entry. A reader of the text alone can say which grub is on their tile.
- **V-12** (telegraph from the tile) A grub on the player's tile that winds up prints "a grub rears back (on you)" in the same draw in which its on-you entry changes to `G ... biting soon`. When it enters Recovery, the same holds with "the grub is open (on you)" and `g ... open`.
- **V-13** (hit line names the attacker) Every heart lost to a grub prints `YOU ARE HIT by a grub (<position>)`, and every heart lost to a shot names the spitter or reads "by a spit shot". A hit line is never printed without a position word for a grub.
- **V-14** (which grub) Practice room: one grub left of the player and one right, with only the right one striking. The hit line reads `(right)`. Swapping which grub strikes swaps the word. The position named in the hit line matches the position of an uppercase `G` or `W` in the draw before the hit.
- **V-15** (manual, written by Build) `manual.md#on-screen` lists the `on you:` line and says that a letter beside `P` named on that line is on the player's tile. `manual.md#what-you-hear-and-read` lists the position in the hit line, "(on you)" and the position words.
- **V-16** (both frame rates) V-9 to V-14 hold identically at 30 and 60 FPS. No timing, damage, position or hit test value changes, and no extra draw is added beyond principle 4. The on-you line and the position in the hit line come from the state of the draw that prints them.
- **V-17** (overlap ends) In the draw that prints "grub defeated" for an on-tile grub, and in the draw after a dash off the tile, the on-you entry for that grub and its displaced glyph are gone.

## Experience signals (for playtest and Review)

- A tester told that a grub is on them can say which grub it is, and no longer says the picture is "drawn beside me" with no way to read it.
- With grubs on both sides, a tester can say which one hit them without being told.
- The lines praised in the playtest report ("rears back (left)", the capital and lowercase marks) are still read as before. The new lines do not push them off the screen in room 2 with four grubs around the player.

## Not checked

- Actual colors cannot be assessed from the text view. This spec fixes the intent and the glyph rules. The reverse-video cell for a displaced enemy is a reinforcement that needs a look in a color build. A review of the built player view is still needed.
- Whether the player's hit-invulnerability (0.8 s) and dash invulnerability need a visible cue is left open. Suggestion: `p` (lowercase) for `P` during invulnerability. This needs no rule change, but it is optional and is not in the acceptance criteria.
- The playtester's possibly short warning at 11.90 s to 11.97 s is not a visual finding. The new hit line (V-13, V-14) will make it easier to trace which grub it was, but whether the warning was real is for `qa` and `game-designer`.
- Whether a very crowded tile (three or more enemies on the player's tile) fits one `on you:` line at the room's text width. The spec lists each entry; wrapping to a second line is allowed if needed.
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

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py [--color] --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format is described in the project's manual.md. Color is only added with --color or
when the output is a terminal; the glyphs carry every state without it.
"""

import argparse
import math
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

# Order tried for the cell beside the player when an enemy shares the player's cell
# (after the side the enemy last came from): right, left, above, below.
SIDE_ORDER = [(1, 0), (-1, 0), (0, -1), (0, 1)]

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


def cell_of(x, y):
    return int(round(x)), int(round(y))


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game, color=False):
        self.game, self.color = game, color
        self.seen, self.next_snapshot = 0, 0.0
        self.last_side = {}  # (room, enemy index) -> unit step from the player to the enemy

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.5 — room {g.room} — {g.fps} FPS")
        self.track()
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, snap = self.game, False
        self.track()
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

    # --- Display offset for enemies on the player's cell (D-006, AC-18; drawing only) ----------

    def track(self):
        """Remember on which side of the player each enemy was last seen in a different cell."""
        g = self.game
        pc = cell_of(g.x, g.y)
        for enemy in g.enemies:
            if not enemy.alive:
                continue
            ec = cell_of(enemy.x, enemy.y)
            if ec == pc:
                continue
            dx, dy = ec[0] - pc[0], ec[1] - pc[1]
            if abs(dx) >= abs(dy):
                side = (1 if dx > 0 else -1, 0)
            else:
                side = (0, 1 if dy > 0 else -1)
            self.last_side[(g.room, enemy.index)] = side

    def free_cell(self, pc, taken, enemy):
        """Nearest free in-room cell beside the player for an enemy that shares the player's cell.

        Order: the side the enemy last came from, then right, left, above, below; if all four are
        taken, the free cell nearest to the player (ties: top row first, then left).
        """
        g = self.game
        order = []
        pref = self.last_side.get((g.room, enemy.index))
        if pref:
            order.append(pref)
        order += [d for d in SIDE_ORDER if d != pref]
        for dx, dy in order:
            c = (pc[0] + dx, pc[1] + dy)
            if 0 <= c[0] < ROOM_W and 0 <= c[1] < ROOM_H and c not in taken:
                return c
        free = [
            (math.hypot(col - pc[0], row - pc[1]), row, col)
            for row in range(ROOM_H)
            for col in range(ROOM_W)
            if (col, row) not in taken
        ]
        if free:
            _, row, col = min(free)
            return (col, row)
        return pc  # no free cell in the whole room (not reachable with 3-6 enemies)

    def enemy_cells(self):
        """(player cell, {id(enemy): drawn cell}) for the living enemies."""
        g = self.game
        pc = cell_of(g.x, g.y)
        living = [e for e in g.enemies if e.alive]
        placed, taken = {}, {pc}
        for enemy in living:
            c = cell_of(enemy.x, enemy.y)
            if c != pc:
                placed[id(enemy)] = c
                taken.add(c)
        for enemy in living:
            if id(enemy) not in placed:
                c = self.free_cell(pc, taken, enemy)
                placed[id(enemy)] = c
                taken.add(c)
        return pc, placed

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(col, row, key):
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = self.paint(key)

        pc, placed = self.enemy_cells()
        if g.arc_left > 0:
            # The arc fills only empty tiles: an enemy (or the player) always wins its cell.
            occupied = set(placed.values()) | {pc}
            for col, row in arc_tiles(g):
                if (col, row) not in occupied:
                    put(col, row, ARC_KEYS[g.arc_dir])
        for shot in g.shots:
            put(*cell_of(shot[0], shot[1]), "shot")
        for enemy in g.enemies:
            if enemy.alive:
                key = enemy.kind
                if enemy.hp < enemy.max_hp:
                    key += "_hurt"
                if enemy.committed:
                    key += "_alert"
                put(*placed[id(enemy)], key)
        put(*pc, "player" if g.hearts > 0 else "down")
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
from game import DASH_DISTANCE, HEARTS, ROOM_H, ROOMS, START, Game  # noqa: E402

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


def parse_session(text):
    """Player-view output as an ordered list of ("line", text) and ("draw", [rows])."""
    items, grid = [], None
    for line in text.splitlines():
        if re.match(r"\s+\[\d+\.\d+ s\] hearts", line):
            grid = []
            continue
        if grid is not None and line.startswith("   |"):
            grid.append(line[4:-1])
            if len(grid) == ROOM_H:
                items.append(("draw", grid))
                grid = None
            continue
        m = re.match(r"\s*(\d+\.\d+)  (.+)$", line)
        if m:
            items.append(("line", m.group(2)))
    return items


def find(rows, chars):
    return [(c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch in chars]


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


class VisibilityTest(unittest.TestCase):
    """AC-18 (no enemy hidden under P) and F3 (enemy glyphs draw over the swipe arc)."""

    def test_grub_never_hidden_and_telegraphs_visible(self):  # AC-18
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(f"room empty\nfps {fps}\nspawn grub 12 4\nplayer 8 4\nend 5.5\n")
                needs, on_you_windup, on_you_open, draws = [], 0, 0, 0
                for kind, val in parse_session(text):
                    if kind == "line":
                        if "a grub rears back" in val:
                            needs.append("GW")
                            on_you_windup += "(on you)" in val
                        elif "the grub is open (on you)" in val:
                            needs.append("gw")
                            on_you_open += 1
                        continue
                    draws += 1
                    self.assertEqual(len(find(val, "gGwW")), 1, val)
                    self.assertTrue(find(val, "Px"), val)
                    for chars in needs:
                        self.assertTrue(find(val, chars), (chars, val))
                    needs = []
                self.assertGreater(draws, 5)
                self.assertGreater(on_you_windup, 0)  # the case the test is about does occur

    def test_spitter_on_player_is_drawn_beside_p(self):  # AC-18
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(f"room empty\nfps {fps}\nspawn spitter 8.2 4\nplayer 8 4\nend 3\n")
                saw_charge = False
                for kind, rows in parse_session(text):
                    if kind != "draw":
                        continue
                    p = find(rows, "P")
                    s = find(rows, "sS")
                    self.assertEqual((len(p), len(s)), (1, 1), rows)
                    self.assertEqual(abs(p[0][0] - s[0][0]) + abs(p[0][1] - s[0][1]), 1, rows)
                    saw_charge = saw_charge or bool(find(rows, "S"))
                self.assertTrue(saw_charge)

    def test_two_enemies_on_the_player_take_different_cells(self):  # AC-18
        text = capture("room empty\nfps 60\nspawn grub 8 4\nspawn grub 8.1 4\nplayer 8 4\nend 0.1\n")
        first = next(v for k, v in parse_session(text) if k == "draw")
        self.assertEqual(len(find(first, "g")), 2)
        self.assertEqual(len(find(first, "P")), 1)

    def test_down_player_keeps_x_and_enemy_beside(self):  # AC-18
        game = Game(room="empty")
        game.place_player(8, 4)
        game.spawn("grub", 8.0, 4)
        down(game)
        out = play.Player(game)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out.start()
        rows = next(v for k, v in parse_session(buf.getvalue()) if k == "draw")
        self.assertEqual(len(find(rows, "x")), 1)
        self.assertEqual(len(find(rows, "gw")), 1)

    def test_hit_draw_shows_damaged_glyph_over_the_arc(self):  # F3
        for fps in FPS:
            for gx in (9.2, 8.1):  # beside the player, and on the player's cell
                with self.subTest(fps=fps, gx=gx):
                    text = capture(
                        f"room empty\nfps {fps}\nspawn grub {gx} 4\nplayer 8 4\n0 attack\nend 1\n"
                    )
                    items = parse_session(text)
                    i = next(n for n, (k, v) in enumerate(items) if v == "you swipe: grub hit (1 left)")
                    rows = next(v for k, v in items[i:] if k == "draw")
                    self.assertTrue(find(rows, "w"), rows)
                    self.assertTrue(find(rows, ")"), rows)  # the arc still shows on empty tiles


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
    # manual.md sits next to repo/ in the project directory (the Owner places it, D-005).
    def test_manual_lists_glyphs_and_lines(self):  # AC-15, V-5
        text = MANUAL.read_text(encoding="utf-8")
        flat = " ".join(text.split())  # a hard-wrapped Markdown line must not hide a phrase
        for key, (char, _) in play.GLYPHS.items():
            self.assertIn(f"`{char}`", text, key)
        for phrase in ("room empty", "rears back", "is open", "charges", "spits",
                       "run over", "press attack to start again", "(miss)", "(too soon)",
                       "(stunned)", "(down)", "room cleared"):
            self.assertIn(phrase, flat, phrase)

    def test_on_screen_section_lists_x_and_the_practice_room(self):  # AC-15 (D-006)
        text = MANUAL.read_text(encoding="utf-8")
        start = text.index("## On screen")
        end = text.find("\n## ", start + 1)
        section = text[start : end if end != -1 else len(text)]
        self.assertIn("`x`", section)
        self.assertIn("The practice room (`room empty`)", section)
        self.assertIn("drawn on a free tile next to you", section)


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

<<<FILE decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md
---
kind: decision
id: D-009
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-009: The `ManualTest` phrase check ignores line wraps; `manual.md` stays unchanged

## Decision

`test_manual_lists_glyphs_and_lines` failed on `run over` only because `manual.md` wraps the line between `run` and `over`. The manual's content and the build's wording (`run over — rooms cleared: N`, `press attack to start again`) agree. The fix is in the test: the phrase check runs on whitespace-collapsed text (`" ".join(text.split())`). The glyph check, the phrase list and the other test stay as they are.

Limits:
- `manual.md` is not edited (D-005, D-007).
- No change to the build, D-001, D-003, D-006 or `design/combat.md`.
- AC-15 passes only when the full suite gives 40/40 with the unchanged `manual.md` beside `repo/` (D-008).

## Rationale

The manual is correct and the test was stricter than the spec's intent. Collapsing whitespace makes the test robust to Markdown hard wraps and avoids an Owner round-trip for a formatting detail.

## Alternatives considered

- Owner joins the two lines in `manual.md`: fixes this run, but breaks again on any rewrap.
- Change the build text: unnecessary; it already matches the manual.

## Revisit when

- The rerun shows another phrase missing or a different failure.
- A phrase the player needs is really absent from the manual.
>>>END

<<<FILE decisions/D-011-grub-turns-stun-body-hit-dash-facing.md
---
kind: decision
id: D-011
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-011: Grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing

## Decision

The A1–A3 package and the A5 gap rules, for `design/combat.md`:

1. **A1 wind-up spacing:** a grub may not start a Wind-up within 1.0 s [tune] of another grub's Wind-up start. A blocked grub waits.
2. **Engagement cap (added, the second rule):** at most 2 grubs within 1.5 tiles of the player at once, counted in every state. Others wait at 2.0 tiles. Without this, A1 alone would still leave four grubs on all sides of the player.
3. **A2 hit-stun:** 0.3 s → 0.15 s [tune]. Invulnerability until 0.8 s after the hit is unchanged. No input buffering.
4. **A3 body hit:** an enemy within 0.5 tile of the player (distance 0 included) is hit by every swipe, whatever the facing.
5. **A5 rules:**
   - A dash with a direction sets facing to that direction; a dash without a direction keeps facing.
   - A dash stops at the room edge (up to 4 tiles).
   - A swipe resolves against true positions in every grub state. A hit during Strike cancels the rest of that strike and puts the grub in a 0.6 s Recovery. Player attacks resolve before enemy damage within a tick.
   - "(miss)" gains a cause: "(miss) too far" (an enemy within 2.5 tiles, beyond reach) and "(miss) not in front" (an enemy within 1.5 tiles, outside the cone and the body radius).
6. New acceptance criteria are AC-19…AC-27, all at 30 and 60 FPS.

Limits:
- No new input (D-001). Knockback, the grub cycle (0.5 / 0.15 / 0.9 s), the 90° cone, reach and the room layouts are unchanged.
- Spitters are not affected.
- It does not decide the manual text; the Owner places the draft in handoff 59.
- It settles the unspecified dash and swipe cases by rule, so QA's results (55) are checked against these rules and not against what the build does.

## Rationale

- The second playtest (54) and the still-player runs (53) show four grubs arriving together and biting in turns from a ring, with no gap to answer in. A1 spaces the commitments. The cap keeps the ring from forming at all, so a swipe or a dash has a clear target and a clear exit. Both are rules on the existing grub states and reuse the spitter stagger idea.
- 1.0 s spacing is longer than the 0.65 s of Wind-up plus Strike, so at most one grub is committed at a time. It is also longer than the dash cooldown (0.6 s), so each bite can be answered with a dash, and equal to or longer than the 0.8 s invulnerability, so no bite is silently absorbed. The cost is that a still player is not saved by invulnerability overlap. That is fine, because a still player is a reference, not a target.
- Hit-stun at 0.3 s took away the best answer (hit the winding-up grub) right after being hit. 0.15 s is at least 4 frames at 30 FPS and still reads as a hit.
- The body-hit rule fixes "the grub is on me and I cannot hit it" without a facing mechanic. D-006 allows overlap and always displays the enemy, so a swipe must be able to hit it.
- Dash sets facing like movement does: the least change to an existing rule, with no new input. It leaves the "backstep" variant to the Director if the retest needs it.
- No escalation trigger fires: no pillar, D-001 or Goal change, small cost, tuning and rules only.

## Alternatives considered

- **A4 cone 120°:** rejected for now. It weakens positioning (pillar 1) and A3 already covers the nearest case. It comes in if the retest shows "(miss) not in front" on at least 1 in 4 swipes with an enemy in reach, or testers still report missing diagonal grubs.
- **D1 facing mechanic (turn in place, auto-face on swipe, backstep dash keeping facing, 360° swipe):** rejected for now. It is a direction decision and risks D-001. It goes to `game-director` if the retest still reports swipes into air after dashes after A3 and the dash-facing rule.
- **D2 room 1 composition (fewer grubs, uneven start distances):** rejected for now. Fewer than 3 enemies breaks the room spec, and uneven starts are staggered arrival, deferred as part of Option B (D-002). A1 and the cap reach a similar effect.
- **A1 alone (no cap):** rejected. Spacing alone still allows a ring of four grubs and the "cornered" feeling.
- **A cap of 1 grub near the player:** rejected. It removes the multi-hit and positioning play of groups and makes rooms 1 and 2 close to duels.
- **Spacing of 0.5 s:** rejected. With a 0.5 s wind-up the bites would follow each other without a gap.
- **Stun kept at 0.3 s with a buffered swipe:** rejected. It adds an input buffer for the swipe that must also work at both frame rates, with no gain over a shorter stun.
- **Dash keeps facing (backstep) now:** rejected for now, see D1.
- **Distance-0 swipe rule without A3 (enemy on you counts as inside the cone):** rejected. A3 covers it and also covers an enemy just behind the player.

## Revisit when

- The retest (room 1 and room 2 by a reactive player) shows a skilled player still cannot clear room 1 or 2 with hearts left, or the rooms become trivial. Retune spacing (0.8–1.5 s), the cap (2 or 3) and the stun first.
- The retest shows A4's trigger (see above) or D1's trigger.
- The retest shows four grubs still read as one clump that feels like a wall: consider D2 / Option B staggered arrival through `game-director`.
- QA's checks (55) show a rule above cannot be built as written.
- Option B is opened (room mix, moving spitters), which changes the grub crowding assumptions.
>>>END

<<<FILE decisions/D-012-on-you-line-for-displaced-enemies.md
---
kind: decision
id: D-012
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-012: Mark an enemy on the player's tile with an `on you:` line, and name the attacker's position in hit lines

## Decision

1. D-006 stands. An enemy sharing the player's tile is still drawn in the nearest free cell beside the player, and it is still never hidden.
2. When any enemy is on the player's tile, an `on you:` line under the hearts line names each one (glyph, state, and the cell it is drawn in). The line is absent when nobody is on the tile. In a color view the displaced glyph's cell is also reverse-video as a reinforcement.
3. Hit lines name the attacker and its position at the moment of the hit ("YOU ARE HIT by a grub (left)"). Position words are shared with the telegraph lines. A distance is added only where two enemies of the same type would otherwise get identical words.
4. Details and acceptance criteria are `design/combat-visuals.md` (V-9 to V-17).

## Rationale

- Two playtesters in two sessions could not tell which side a bite would come from or which grub hit them (G-001, handoff 57). Pillar 3 asks that threats be readable.
- A one-cell-per-tile text view has no room for a second mark on the same tile, so the clarity has to come from a text line. Principle 1 already allows state to be carried in text.
- It changes only display. No rule, timing or parameter changes. It reuses the existing glyphs, the "(on you)" wording and the position words, so the praised lines stay as they are.
- It does not depend on the designer's pending swipe rule. The line reports position and state, not what a swipe will hit.

## Alternatives considered

- **Change the glyph on overlap (a separate "overlap" glyph or marker character):** rejected. It drops the enemy's case-coded state, which is the reading players praised, and D-006 rejected a similar idea.
- **Replace `P` while an enemy is on the tile:** rejected in D-006. The player would vanish from the map.
- **Rely on reverse-video or color only:** rejected. Principle 1 forbids meaning that depends on color alone, and it cannot be verified from the text view.
- **Make the map wider (two cells per tile) to show the overlap side by side:** rejected for now. It reflows the room and the tests, and it is not a small change for a small team.
- **Only add "(on you)" to hit lines:** rejected. It does not help when the enemy is beside the player in the picture, which was the reported confusion.

## Revisit when

- A playtest after the build shows the player still misreads the drawn side, or the `on you:` line is not read.
- Overlap becomes frequent enough (Option B, movement changes, or the designer's swipe rule) that the line is on screen most of the time and adds noise.
- The view moves beyond text and glyphs, so a real overlap marker on the tile becomes possible.
>>>END

<<<FILE decisions/D-013-knockback-of-grub-on-players-tile.md
---
kind: decision
id: D-013
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-013: A grub on the player's tile is knocked back toward the side it is drawn on

## Decision

1. The first hit (HP 2→1) knocks a grub back 1 tile over 0.2 s. If its true position is 0.05 tile or more from the player's, the direction is straight away from the player. If it is on the player's tile, the direction is its display side from D-006 (the side it last approached or struck from, otherwise right, left, above, below), so it ends in the cell where it was already drawn.
2. If that side has less than 1 tile of clear room, the next side in the order right, left, above, below that has 1 clear tile is used. A knockback away from the player toward an edge is clamped at the edge, as a dash is.
3. A grub knocked back from distance 0 ends about 1.0 tile away, inside the 1.5-tile zone, and keeps its engagement slot. No state or timer changes.
4. Q2: the swipe result line is unchanged for an on-tile grub ("you swipe: grub hit (1 left)"). The position is read from the `on you:` line.
5. Acceptance: AC-28 in `design/combat.md`. V-17 in `design/combat-visuals.md` is unchanged and still applies.

## Rationale

- The display side is already stored and already what the player sees (D-006, D-012). The grub steps out to the cell it was shown in, so nothing jumps to a side the player was not told about.
- It is defined in every case, needs no new input, and reuses what exists (D-001, small team).
- The `on you:` line and the picture stay consistent after the hit: the entry goes away when the grub lands.
- Keeping the slot is the honest result of a 1-tile knockback from distance 0. It does not weaken the cap or the turns rule, and the grub that was on the player is still the nearest one to be countered.

## Alternatives considered

- **Along the player's facing:** rejected. Always defined, but the grub can jump to the side opposite its drawn cell, and a player who dashed or turned sees it land where nothing pointed. It also pushes the grub into the player's facing line, where its next bite becomes easier to stay in front of by accident.
- **Fixed direction (right, falling back to left):** rejected. Arbitrary to the player, and it contradicts the displayed side.
- **No knockback at distance 0:** rejected. It breaks "the first hit knocks back" for the case A3 makes common, and the grub would stay on the player and stay hard to read.
- **Knock it far enough to free a slot (1.5 tiles or more):** rejected. It would reward an on-you grub with a free escape from the cap, which changes the cap's tuned play, and needs a new distance.
- **Push the other way when blocked, instead of clamping:** adopted only for the on-tile case. For a grub that is not on the tile, clamping matches the dash and needs no new rule.

## Revisit when

- The retest shows testers misreading where the grub lands, or an on-tile grub that stays near the player too long, so the slot it keeps feels like a wall.
- The overlap display rule (D-006) or the `on you:` line (D-012) changes.
- Option B opens movement or collision changes for grubs.
>>>END

<<<FILE goals/G-001-combat-monotony/65-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 65
from: game-designer
to: studio
stage: Design
outcome: done
---
# 65: game-designer → studio — Q1 answered (knockback of an on-tile grub), Q2 accepted, three passages cleaned; re-issue the Build

## Task

Re-issue the Build to `gameplay-engineer` with the `repo/` files attached (the Studio's fix from 63), `design/combat.md` as updated here, and D-013. No question remains open for the engineer from 63.

## Context

G-001, Option A. The engineer's hand-back (63) found one spec gap (knockback direction at distance 0) and asked for three passages to be made readable. This step answers them. No input, scope or direction changed, so no Decide is needed.

## Findings

### Q1: Knockback of a grub on the player's tile (D-013)

- Rule: the first hit knocks the grub back 1 tile over 0.2 s. A grub 0.05 tile or more from the player is pushed straight away from the player. A grub on the player's tile (under 0.05 tile) is pushed toward its display side from D-006: the side it last approached or struck from, otherwise right, left, above, below. It ends up in the cell where its glyph was already drawn.
- Room edge: the side must have 1 tile of clear room. If not, use the next side in the order right, left, above, below that does. A push away from the player toward an edge is clamped at the edge, like the dash.
- Slots: from distance 0 the grub ends about 1.0 tile away, still inside 1.5 tiles, so the first hit does not free a cap slot. A grub hit from 0.5 tile or more away ends 1.5 tiles or more away and does free one. This answers the engineer's "freed slot" question.
- State and timers are not changed by the knockback. The AC-4 timing stays as written.
- Display: the knockback takes 0.2 s, so the immediate draw at the swipe may still show the grub on the tile with its `on you:` entry. A draw at 0.2 s or later shows it as a normal neighbor with no entry. V-17 is unchanged (it still covers "defeated" and the dash). The knockback case is checked in AC-28 in `combat.md`, so `combat-visuals.md` is not edited.
- The choice was made so the picture and the `on you:` line stay consistent: the grub steps to the side it was shown on. Options 1, 3 and 4 were rejected (reasons in D-013).
- Repo behavior: if the current code knocks an on-tile grub another way, report it at the Build. The rule here stands.
- New criterion: **AC-28** (a–e), included in AC-17's frame-rate scope.

### Q2: "(on you)" in the swipe result line

Accepted as proposed. The swipe line stays "you swipe: grub hit (1 left)" for every grub, wherever it is. The position of an on-tile grub comes from the `on you:` line. This is written into "Player kit" and AC-28(e).

### The three passages

- **Dash and walls:** confirmed. A dash always lasts 0.25 s, and invulnerability covers all of it, even when a wall shortens the dash. New sentence: "A dash that would leave the room stops at the room edge and is never cancelled; it covers the shorter of 4 tiles and the distance to the edge, and every dash lasts exactly 0.25 s with invulnerability for all of it, even when a wall shortens it." AC-25 now also checks the 0.25 s on a 2-tile wall dash.
- **Waiting distance:** your reading is right, and it is now written as "Waiting positions" under the grub rules:
  - Cap-blocked grub: holds at 2.0 tiles or more, backs off if the player approaches, follows to stay at about 2.0 tiles, and resumes Approach when a slot frees.
  - Spacing-blocked grub: keeps approaching until within 1.25 tiles, then stands still until the window ends. If already inside 1.5 tiles, it stands where it is and counts toward the cap of 2.
  - So a grub between 1.25 and 2.0 tiles is never standing still: it is either approaching because a slot is free, or on its way back to 2.0 tiles because the cap is full. No new rule; it is a clarification. If the code differs in the Waiting-follow behavior, say so at the Build.
- **AC-23:** separated into (a) on tile at 0.2 (hit), (b) 0.4 tile behind (hit) with the explicit script (`move right`, `stop`, and the mirror), (c) 0.8 tile behind ("(miss) not in front"). The "away 0.3 s then back" instruction is removed.

### Other changes in `design/combat.md`

- Status line, AC-17 (now AC-1…AC-14 and AC-18…AC-28), "Edge cases" (two knockback notes), 30/60 FPS (knockback 0.2 s is on elapsed seconds), retest report item (4), "Held back or rejected", and "Open questions".
- No parameter value changed.

## Decisions already made

- D-001, D-002 / D-004, D-006, D-011, D-012.
- New: D-013 (knockback of an on-tile grub).

## Constraints

- `manual.md` is untouched. See the manual text below for the Owner.
- Stays inside Option A and D-001. The knockback uses stored display side data and existing positions, with no new input; it works on elapsed seconds at 30 and 60 FPS.

## Open questions

None for the engineer. For the Owner/Studio: the manual text below, and whether the Owner wants it placed.

## Expected output

- The Studio re-issues the Build (61) to `gameplay-engineer` with `repo/` files, `design/combat.md`, `design/combat-visuals.md` (unchanged), D-011, D-012 and D-013, and this handoff as the previous one. The engineer implements AC-19…AC-28 and V-9…V-17, adds tests, runs the suite and hands to QA.
- Manual text for step 10-O (the Owner places it; I did not touch `manual.md`). Suggested line for On screen, near the `on you:` text (V-15): "When you hit a grub that is on top of you, it is pushed one step to the side where it was drawn, and the `on you:` line goes away."

## Sender assessment

- Confidence the rule is buildable: high; it needs the stored display side and a clear-room check. Risk is small and local: the order of "last approached side" versus the fallback order, which AC-28 pins down.
- The one cost to watch is that an on-tile grub keeps its slot after the first hit. If the retest shows it feels like a wall, the revisit is in D-013 (retune the cap or the distance, not the direction).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-visuals.md, manual.md (read only), repo/ (must be supplied)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/64-studio-to-game-designer.md
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
