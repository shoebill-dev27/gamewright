# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/74-studio-to-gameplay-engineer.md
next_seq: 75
runs: tests, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/75-gameplay-engineer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/74-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 74
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 74: studio → gameplay-engineer — Apply the five rulings of 73 and fix the failures from 70

## Task

Change the build so that it follows the five rulings in `73-game-designer-to-studio.md` (cell at an exact half tile, one meaning of "on you", side word of an enemy not on you, hit-line word fixed at Strike start, knockback of an on-you grub). Also fix the failing `CrowdTest.test_hit_stun_is_short` and the display defects from 70. Add or adjust tests for AC-28(b), AC-29 and AC-30.

## Context

G-001 (combat feels monotonous), Option A (D-002). AC-19…AC-28 were built in 67. QA's verification (70) failed on AC-17, AC-22 (suite), AC-28(b) at 30 FPS, V-10, V-14, V-16 and V-15 (manual text, which is an Owner step). Three spec gaps caused most of this. The game-designer settled them in 73 and D-014, and the criteria were changed in `design/combat.md` (AC-17, 28, 29, 30) and `design/combat-visuals.md` (V-10, 12, 14, 16, 18). No Plan stage is needed; the change is local to the existing simulation and display code.

## Findings

What to build (details and reasoning in 73 "Rulings"; the design documents hold the exact criteria):

1. **Cell rule.** `cell(v) = floor(v + 0.5 + 0.005)` per axis, for the player and for enemies. It replaces the `int(round(...))` in `cell_of`, which is float-noise sensitive at .5. A displayed side for an on-you enemy must be a cell inside the room (the `player 14.5` case: show and knock left from the first draw).
2. **On you.** True distance to the player ≤ 0.5 tile (the `BODY_HIT` radius, tolerance 1e-6). Use it for the `on you:` entry, the displaced glyph, "(on you)" in telegraph, open and hit lines, and the knockback. Remove the 0.05-tile `ON_TILE` test for text and knockback. A draw never has both a side word and an `on you:` entry for the same enemy.
3. **Side word of an enemy not on you.** From the cell offset to `P`. If it shares the player's cell, use the larger true-offset axis (tie: horizontal). The distance suffix rule is unchanged.
4. **Hit-line word.** For a grub, store the position word at the instant the Strike begins (end of Wind-up) and use it in the `hurt` event and the hit line. Do not use the lunge position at the damage tick. Spitter hit lines are unchanged.
5. **Knockback of an on-you grub.** Toward the side it is drawn on; end point 1.0 tile from the player's true position on that side. The normal case (more than 0.5 tile away) stays "straight away". `spawn grub 8 4` still ends at 9.00.

Also fix from 70:

- `CrowdTest.test_hit_stun_is_short` fails at both frame rates. Find out whether the test or the build is wrong. The spec is the 0.15 s hit-stun in D-011 and AC-22. If the build is wrong, fix the build. If the test is wrong, fix the test and say why in the build notes. If the spec itself is unclear, hand back `question`; do not decide.
- The 30 FPS display mismatch (D-A) and the hit-line word (D-C) are covered by rulings 1–4.
- The last suite run in your environment had two `ManualTest` errors from a missing `manual.md`. Make sure `manual.md` is available when you run `run_tests` (read it; do not edit it).

## Decisions already made

- D-001: no new buttons. D-002, D-004, D-005, D-007: Option A, single sequential change set, the Owner places manual text.
- D-011: grubs take turns, two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line and attacker position in hit lines.
- D-013: knockback of a grub on the player's tile (direction and end-point wording superseded by D-014 where they differ).
- D-014: one rule for cells, sides, "on you" and the hit-line word (the rulings above).

## Constraints

- Do not change any number (timings, the 0.5 tile radius, the cap, spacing). The only new use of a value is the "on you" radius, which equals the existing `BODY_HIT`.
- Must play correctly at both 30 and 60 FPS.
- Do not edit `manual.md` (the Owner's) or the design documents.
- No new input buttons. Reuse existing systems.
- If AC-2, 4, 5, 7, 11, 19, 21, 23–27 or AC-28 a/d/e stop passing because of your change, report it; do not change a number to fix it. AC-21 has a thin margin (1.97 s, limit 1.9).
- If the spec is ambiguous, contradictory or missing a case, stop and hand back `question` to `studio`.

## Open questions

- Which side is wrong in `test_hit_stun_is_short`, the test or the build (answer in the build notes)?

## Expected output

Build notes in an outgoing Handoff addressed to `studio` (so that the Studio can compose the QA step from permitted information). They must contain:

- what changed, by file;
- the `run_tests` result with `manual.md` present (count and any failures);
- trace or play evidence at 30 and 60 FPS for AC-28(b), AC-29 and AC-30;
- the answer to the open question;
- anything in the 73 "Previously passing behavior that changes" list that behaved differently than described.

Keep your own reasoning and self-test verdicts under `## Sender assessment`; it is removed before QA receives the Handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md (read only), repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py (build in repo/; run commands in project.md)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/73-game-designer-to-studio.md (read for the rulings; its Sender assessment is the designer's own reasoning), with failures in goals/G-001-combat-monotony/70-qa-to-studio.md
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

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text. Updated after QA's second round (handoff 29): overlap rule and AC-15 wording (D-006). Updated after playtests 50 and 54 (handoff 59): grub spacing and engagement cap, shorter hit-stun, body-hit rule, dash and facing rules, swipe cases, miss wording (D-011). Acceptance criteria AC-19 to AC-27 are new. Updated after the engineer's hand-back (63, answered in 65): knockback of a grub on the player's tile (D-013, AC-28), and rewrites of the dash-and-walls, Waiting and AC-23 passages (no rule change in those three). Updated after QA's verification (70, answered in 73): one rule for cells, sides and "on you" (D-014); knockback of an on-you grub reworded; AC-17, AC-28 reworded; AC-29 and AC-30 are new.

## Experience intent

Every enemy does something the player can read, answer and profit from. A grub is a threat with a beat: it approaches, winds up, strikes, then is open to a counter. A spitter is a threat on a rhythm that the player can dodge or break by walking up and hitting it. The player's attack visibly changes the enemy. Fights are decided by spacing and timing with attack and dash only (D-001, pillars 1 and 3). A group of grubs takes turns: the player always has a gap to answer in and is never boxed in by simultaneous bites.

## Conventions

- All timings are in seconds and must hold at 30 and 60 FPS (section "30 / 60 FPS").
- Distances are in tiles. The room is 16×9 (x 0–15, y 0–8).
- "Telegraph" means a change the player can see in the player view, at least one on-map change plus one text line. Threat colors are saturated orange/red. The on-map change must be visible in a cell the player can see: an enemy glyph is never hidden under `P` (see "Overlap with the player").
- Values marked **[tune]** are starting values the designer expects to adjust after a live playtest of the Option A build.
- "True position" is the simulated position of an enemy, not the cell where its glyph is drawn.
- Cells, sides, "on you" and position words follow one rule, "Cells, sides and 'on you'" below. Nothing else may define them.

## Cells, sides and "on you" (D-014)

One definition, used by the draw, every text line that names a position, the `on you:` line, the hit line and the knockback. It depends only on true positions and never on the frame rate.

1. **Cell of a position.** Per axis, `cell(v) = floor(v + 0.5 + 0.005)`. That is rounding to the nearest tile, where an exact .5 (and any value within 0.005 below it) goes to the larger index (right, down). Examples: 13.5 → 14; 14.5 → 15; 14.49 → 15; 14.49 − 0.01 → 14. Banker's rounding and bare float comparison at .5 are not allowed. The player is drawn in `cell(player)`.
2. **On you.** An enemy is *on you* when its true distance to the player is 0.5 tile or less (the body-hit radius of A3, same test, with a tolerance of 1e-6). Nothing else makes an enemy "on you". So a swipe always hits an enemy that is on you, and an enemy that can be missed is never called on you.
3. **Position word of an enemy not on you.** Let (cx, cy) be `cell(enemy) − cell(player)`. If both are 0 (same cell, but farther than 0.5 tile), use the unit step along the larger axis of the true offset (ties: horizontal) instead. Then: (±1 or more, 0) → `left` / `right`; (0, ±) → `above` / `below`; both non-zero → `top left`, `top right`, `bottom left`, `bottom right`. The word therefore always names the side of `P` on which the glyph is drawn.
4. **Position word of an enemy on you:** `on you`, in every line.
5. **Drawn cell.** A not-on-you enemy is drawn in `cell(enemy)`, except when that equals the player's cell: it is then drawn in the neighbour cell given by the step of rule 3. An on-you enemy is drawn in its own cell when that is a straight neighbour of the player's cell; otherwise (same cell or diagonal) it is drawn in a displaced straight neighbour: the side last approached or struck from, else right, left, above, below, in that order, taking only cells that are inside the room and free (if all four are taken, the next free cell by distance). The displaced cell is a display offset only. The `on you:` line states the side drawn.
6. **Frame rate.** The rules use true positions at the moment of the draw or line. Resting positions (a knocked-back grub at x=13.5, a waiting grub at 2.0 tiles) must give the same cell at 30 and 60 FPS.

Everything that says "same tile", "(on you)", "left", "right" and so on below means these rules.

## Player kit

- **Attack** (one button): a swipe in the facing direction.
  - Damage 1. Recovery 0.35 s.
  - Reach 1.5 tiles, in a 90° cone centred on the facing direction.
  - **Body-hit rule (A3):** an enemy whose true position is within 0.5 tile of the player (including distance 0, "on you") is hit by every swipe, whatever the facing. The swipe still draws its arc in the facing direction.
  - A swipe hits every enemy that is in the cone or inside the body-hit radius. Hitting two enemies with one swipe is intended and rewards positioning.
  - **Swipe in any enemy state:** a swipe resolves against true positions at the moment of the press, whatever state the enemy is in (Approach, waiting, Wind-up, Strike, Recovery). See the grub rules for what the hit does.
  - **Swipe result line and an on-you grub (Q2):** the result line is the same wherever the grub is: "you swipe: grub hit (1 left)". It never carries "(on you)". The position of an on-you grub is read from the `on you:` line.
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
- **Strike-start position (D-014):** when a Strike begins (the instant the Wind-up ends), the position word of the grub, by the rule in "Cells, sides and 'on you'", is fixed for that strike. The hit line of that strike uses this word (see visuals spec, "Hit lines name the attacker"). The grub does not move during Wind-up, so for a still player this is the same word as in the "rears back" line.
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

#### Knockback direction (Q1, D-013, reworded by D-014)

- **Normal case (not on you):** a grub farther than 0.5 tile from the player (true) is knocked back 1 tile straight away from the player, along the line from the player to the grub. A knockback toward an edge is clamped at the edge, the same way a dash is.
- **Grub on you (within 0.5 tile, rule 2 of "Cells, sides and 'on you'"):** it is knocked toward the side on which it is drawn (rule 5) and ends **1.0 tile from the player's true position on that side**, which is the cell where its glyph was already drawn. The player sees the grub step out to the side it was shown on, and nothing jumps to the other side. For a grub exactly on the player this is the same as moving 1 tile toward that side.
- **Display side and room edge:** the drawn side is chosen only among cells inside the room (rule 5), so a grub on a player at an edge is never shown outside the room. For the knockback, the end point (player + 1.0 in the side's direction) must be inside the room. If it is not, the next side in the order right, left, above, below with a valid end point is used, and the glyph must have been drawn on that side already: because the display side obeys the same in-room test, the two always agree. Example: `player 14.5 4` with a grub on the player's tile is drawn left of `P` from the first draw and ends at x 13.5; it is never drawn on the right.
- **Slots:** a grub knocked back from within 0.5 tile ends 1.0 tile from the player, so it stays inside 1.5 tiles and keeps counting toward the cap of 2. A first hit on an on-you grub does not free a slot. A grub hit from more than 0.5 tile away ends more than 1.5 tiles away only when it was at least 0.5 tile out (distance + 1.0 ≥ 1.5), which is always the case in the normal case, so it frees a slot.
- **Cycle:** knockback changes where the grub is, not its state or timers. The AC-4 timing (next bite no sooner than 1.5 s after the previous one for a still player) is unchanged. A knocked-back grub walks back in Approach if it is not in Recovery, or stays where it landed until Recovery ends.
- **Timing of the display:** the knockback takes 0.2 s. The immediate draw at the swipe may still show the grub on the tile with its `on you:` entry. A draw made 0.2 s or later after the hit shows it on the knockback side as a normal neighbor, with no `on you:` entry for it (V-17, AC-28). Resting at the end point (for example x 13.5) must show the same cell at 30 and 60 FPS (rule 1 and 6).

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

### Overlap with the player (F1 ruling, D-006; cells per D-014)

- **Physics unchanged.** Enemies and the player have no collision. A grub's lunge and recovery may leave it within the player's tile, and the player may walk or dash onto an enemy. This adds no rule to movement, timing, damage or hit tests; all of those use true positions.
- **Display rule.** In the player view no enemy is ever hidden under `P`. The player is always drawn on their own cell. Which cell an enemy is drawn in, including the displaced cell, is set by rule 5 of "Cells, sides and 'on you'". It applies when an enemy is on you, and also when an enemy is farther than 0.5 tile but still rounds to the player's cell.
- It applies in every state, so a grub in Recovery that is "open (on you)" is also visible and its counter can be read. It applies to both enemy types and to damaged glyphs.
- Two enemies sharing the player's cell are displaced to different cells.
- The text lines print the position words of the same rules ("(on you)" only for an enemy within 0.5 tile). The displaced glyph is the on-map change that makes the telegraph complete.
- The immediate draws at Wind-up start, Strike and Recovery start (visuals spec principle 4) use this rule too.
- A displaced glyph does not mean the enemy has moved. A swipe hits by true position, so a swipe may hit an enemy drawn on a different side than the arc. The body-hit rule makes this safe for an enemy "on you": it is always hit. An enemy that is displaced but farther than 0.5 tile is not "on you" and can be missed; its word is the side it is drawn on.
- The display side of an on-you grub is also the direction in which it is knocked back by the first hit (see "Knockback direction").

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
- **Grub knocked out of the engagement zone:** it frees a slot at once; it is Approach again and may be Waiting if the cap is full when it returns. A grub hit while on you is not knocked out of the zone (it ends 1.0 tile away), see "Knockback direction".
- **Player dashes through a grub in Wind-up:** the grub still completes its Wind-up, Strike (toward where the player stood when the wind-up ended) and Recovery; its strike misses if the player is more than 1.0 tile away.
- **Swipe at the same tick as a strike's damage:** the swipe resolves first (see "Player hits on a grub").
- **Dash into a wall or into the room edge:** stops at the edge, see Dash.
- **Spitter Charge canceled by a hit:** the projectile is not fired.
- **Enemy on you:** see "Cells, sides and 'on you'" and "Overlap with the player". It is drawn beside `P`; the body-hit rule means a swipe always hits it; the first hit knocks it onto the side it is drawn on.
- **Enemy at an exact half tile (x.5):** the cell rule decides; the result is the same at 30 and 60 FPS (rule 1 and 6).
- **Player at the room edge with an enemy on you:** the displaced cell is always inside the room.
- **Player down while an enemy shares the cell:** `x` is drawn on the player's cell and the enemy keeps its displaced cell.
- **Pause:** all timers freeze.

## 30 / 60 FPS (Q5)

- Every timer above runs on elapsed seconds, not frame counts. This includes the spacing window (1.0 s), the dash duration, the hit-stun (0.15 s) and the knockback (0.2 s).
- Tolerance: an event's trace timestamp may differ from its spec time by at most 0.04 s at 30 FPS and 0.02 s at 60 FPS.
- The Strike damage window (0.15 s) must cover at least 4 frames at 30 FPS.
- The hit-stun (0.15 s) is at least 4 frames at 30 FPS; it ends at the first tick at or after 0.15 s.
- Dash distance (4 tiles) may differ between 30 and 60 FPS by at most 0.25 tiles.
- Running the same script at `fps 30` and `fps 60` gives the same sequence of events, with timestamps within 0.07 s of each other.
- Displayed cells, position words, the `on you:` line and the hit-line word for a still player are identical at both rates (D-014). Positions that rest on a half tile are the case that most often breaks this.

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
- **AC-17 Frame rate:** AC-1…AC-14 and AC-18…AC-30 pass at both frame rates, and the 30/60 comparison above holds (including identical cells and position words, AC-29 and AC-30).
- **AC-18 No hidden enemy:** in the practice room with an idle player and one grub at distance 4, run to 5.5 s, every draw that shows a living grub has a grub glyph in a cell different from the player's cell. Every "a grub rears back" line, including those marked "(on you)", comes with an uppercase `G` or `W` visible on the map in the draw made at that moment. Same for "the grub is open (on you)": a lowercase `g` or `w` is visible. Also, with `player 8 4` and `spawn spitter 8.2 4`, the draws show `P` and an `s` in a neighbouring cell; the spitter's `S` is visible beside `P` during its Charge. The trace shows no change to timings, hearts or positions compared with a build without the display rule (the events of AC-1…AC-4 stay within tolerance).
- **AC-19 Wind-up spacing (A1):** in room 2 with a still player, run to 12 s (or until down): for every pair of grub Wind-up starts in the trace, the later one is at least 0.96 s after the earlier one at 60 FPS and 0.92 s at 30 FPS (1.0 s minus tolerance), whichever grubs they belong to. The same holds in room 1 and room 5. A room with a single grub shows the AC-2 cycle unchanged.
- **AC-20 Engagement cap:** in room 2 with a still player at x 8, y 4, the trace shows at no sample more than 2 grubs within 1.5 tiles of the player, from the start to the end of the run. The remaining grubs are present in the draws at about 2.0 tiles with lowercase glyphs and no "rears back" line until a slot frees.
- **AC-21 Turns, not a ring:** in room 2 with a still player, the time between the first and the third heart lost is at least 1.9 s. No two Wind-up starts fall within 1.0 s (AC-19), so the trace shows at most one grub in Wind-up or Strike at any sample.
- **AC-22 Hit-stun:** after a heart is lost, an attack pressed 0.05 s later prints "(stunned)" and does nothing. An attack pressed 0.25 s later swipes normally. A dash behaves the same way (subject to its cooldown). The stun lasts 0.15 s within tolerance. Invulnerability still ends 0.8 s after the hit.
- **AC-23 Body hit (A3):** three practice-room checks, each at both frame rates.
  - (a) On you: `player 8 4` and `spawn grub 8.2 4`, with no movement before the swipe (default facing). The swipe hits the grub and prints "grub hit (1 left)", whatever the facing.
  - (b) Just behind: `player 8 4`, `move right` then `stop` (facing right), and a grub spawned 0.4 tile to the left of the player's true position. The swipe hits it. Repeat with `move left` then `stop` and the grub 0.4 tile to the right.
  - (c) Further behind: with the same setups as (b), a grub 0.8 tile behind the player is not hit and the swipe prints "(miss) not in front".
- **AC-24 Dash and facing (A5):** in the practice room, `player 8 4`, face right (move right then stop), then `dash left`, then an attack after the dash: the arc is drawn as `(` (facing left). A `dash` without a direction while facing up leaves facing up. A queued attack pressed during a dash fires after it ends in the dash direction.
- **AC-25 Dash distance (A5):** in the practice room from `player 8 4`, `dash right` ends at 12.0 ± 0.25 on x at both frame rates and takes 0.25 s within tolerance. From `player 2 4`, `dash left` ends at the room edge (x 0, never outside the room), takes 0.25 s within tolerance even though it covers only 2 tiles, and the player takes no damage during it. Dash during the cooldown prints "(dash not ready)" and does nothing.
- **AC-26 Swipe during Strike and Recovery (A5):** with one grub in the practice room, a swipe pressed while the trace shows the grub in Strike hits it ("grub hit (1 left)") and no heart is lost to that strike if the swipe's tick comes at or before the damage tick. A swipe pressed while the grub is in Recovery and adjacent in front hits it. Neither case prints "(miss)". (Known: the cancel window is one tick wide, 0.033 s at 30 FPS; this is as written.)
- **AC-27 Miss wording (A5):** a swipe with a grub 2.0 tiles in front prints "(miss) too far". A swipe with a grub at 1.0 tile directly to the side (outside the cone) prints "(miss) not in front". A swipe with nothing within 2.5 tiles prints "(miss)" alone. All three also draw the arc.
- **AC-28 Knockback of an on-you grub (Q1, D-013, D-014):** in the practice room, one grub, a still player, and a swipe on the first hit. Read the true positions from the trace and the cells from the draws.
  - (a) `player 8 4`, `spawn grub 8 4`. The grub is shown on some side of `P` (the `on you:` line says which). After the first hit, a draw made 0.2 s or more later shows the damaged grub (`w`/`W`) at 1.0 ± 0.1 tile from the player, in the cell on that same side, with no `on you:` entry for it. The grub did not appear on any other side in any draw. The same with `spawn grub 8.2 4`: the grub ends 1.0 ± 0.1 tile from the player's true position, on the side shown.
  - (b) Edge: `player 14.5 4`, `spawn grub 14.5 4`. From the first draw to the hit the grub is shown **left** of `P` (never right; there is no cell to the right), and every text line names it "(on you)", never "(left)" or "(right)" at the same time as the on-you entry. After the first hit it ends at x 13.5 ± 0.1 (1.0 tile left of the player), inside the room, and a draw 0.2 s or later shows it left of `P` with no `on you:` entry, at both frame rates and with the same cell and the same words in both. It is never inside 0.9 tile of the player.
  - (c) With room 2 and two other grubs inside 1.5 tiles, a first hit on an on-you grub leaves it inside 1.5 tiles, so the trace shows no third grub entering the zone because of that hit. A first hit on a grub 0.6 tile or more away leaves it at 1.5 tiles or more.
  - (d) The grub's state timers are unchanged by the knockback (AC-4: next bite no sooner than 1.5 s after the previous one for a still player).
  - (e) A swipe result line for an on-you grub reads "you swipe: grub hit (1 left)" with no "(on you)" (Q2).
- **AC-29 Cell at an exact half tile (D-014):** practice room, a still player, the grub placed so that it rests (or is spawned) on a half-tile boundary; read the cells in the draws and the words in the text lines. Each at both frame rates; the results must be identical.
  - (a) `player 14.5 4`, `spawn grub 13.5 4`: the draw at 0 s and every later draw while the grub is still shows `g` in the cell immediately left of `P` (x column 14, `P` in column 15). Its "rears back" line says "(left)".
  - (b) `player 8.5 4`, `spawn grub 9.5 4` (right) and `spawn grub 7.5 4` in a second run (left): the first reads "right", the second "left"; neither is ever "on you" and neither is drawn on the other side of `P`.
  - (c) After AC-28(b) the knocked-back grub rests at x 13.5: its glyph stays in the same cell from 0.2 s after the hit until it starts to move, at both rates, and the words in the lines at that time name the same side.
- **AC-30 One meaning of "on you" and of the position words (D-014):**
  - (a) `player 8 4`, `spawn grub 8.2 4`, run to 4 s. In every draw, an enemy within 0.5 tile is called "on you" in every line and in the `on you:` line; no draw has a side word ("left", "right", …) and an `on you:` entry for the same enemy.
  - (b) `player 8.4 4`, grub placed at x 7.8 (0.6 tile left, same cell as `P`): the grub is not on you. It is drawn in the cell left of `P`, every line that names it says "left", and there is no `on you:` entry. A swipe facing right prints "(miss) not in front".
  - (c) In room 2 with a still player, run to 6 s. In every draw, the side word of every text line that names an enemy equals the side of `P` on which that enemy's glyph is drawn in the same draw. This is checked by reading the text, including the 3.38 s and 4.38 s "the grub is open" lines.
  - (d) Hit-line word: in room 2 with a still player, for every "YOU ARE HIT by a grub (…)" line the word equals the word of that grub's "rears back" line, and equals the side/corner of the `G` or `W` in the draw made at its Wind-up start. The 4.3 s hit of the 70 report reads the same word at 30 and 60 FPS (expected: the corner word, "top right").
  - (e) The scripted V-14 case (one grub left, one right, only the right strikes) still reads "(right)", and swapping the strikers swaps the word, at both rates.

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
- A playtester never describes the map and the text lines as saying different things about where a grub is.
- Observed in QA captures (no ruling): an idle player went to zero hearts at about 5.0 s in the practice room and in room 1 before these changes. That is expected for a player who does nothing. After A1 and the engagement cap the idle time to down is expected to be a little different; it is a reference value, not a target. Retune the **[tune]** values from live play.

### Retest guideline (design-side; for the next Play and Review, qualitative)

What a skilled player should be able to do. Numbers belong only in the acceptance criteria above.

- **Room 1 (3 grubs):** a skilled player who reads the cues can clear it and normally keeps most of their hearts. Damage comes from a misread cue or a mistimed dash, not from a bite they could not avoid. They can answer a rear-back by stepping out, by dashing through, or by hitting the winding-up grub, and then punish the open grub. After a hit they can swipe again quickly. A grub right on them can be hit.
- **Room 2 (4 grubs):** a skilled player can break the ring: only two grubs crowd them, bites come one at a time with a gap, and they can dash out to a side or a wall and fight the nearest grub from a free line. The room should still be a real fight where taking a hit or two is plausible, but a player who tries should clear it, usually with at least one heart left. A player who stands still loses; that is meant.
- Judge sameness only on a survived run. A player who cannot clear room 1 or 2 says nothing yet about monotony (see 53 and 54).
- Report from the retest, because they decide the held items: (1) swipes that print "(miss) not in front" while the player aimed at that grub (A4); (2) swipes aimed after a dash that hit air (facing, D1); (3) whether four grubs still arrive as one clump that feels like a wall (D2 / Option B); (4) whether a grub knocked off the player's tile stays in the fight too long, since it keeps its cap slot (D-013).

## Held back or rejected (see D-011, D-013, D-014)

- **A4 cone width 90° → about 120°:** held. It comes in if the retest shows that the "(miss) not in front" line appears on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or that testers report missing grubs standing diagonally in front after A3 is in. Then widen to 120° **[tune]** and add its AC.
- **D1 facing mechanic (turn without moving, auto-face, backstep dash, 360° swipe):** not taken. It goes to `game-director` only if the retest still reports swipes into air after dashes or turning trouble with A3 and the dash-facing rule in.
- **D2 room 1 composition (fewer grubs, staggered arrival):** not taken. A1 and the cap give the intended effect inside Option A.
- **Knockback of an on-tile grub along the player's facing, a fixed direction, or none:** not taken (D-013).
- **Cell-equality "on you", drawn-cell words from raw rounding, hit word from the damage-tick position:** not taken (D-014).

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director. The art-director may review the choice of the displaced cell for readability (see D-006) and the new wording of V-10, V-12, V-14 and V-18 (D-014).
- The as-built dash distance and the facing behavior after a dash are being checked by QA (55). Where the build differs from the rules above, the rules above stand and QA's result becomes a defect, unless QA shows a rule cannot be built.
- Whether the run has any progression after "run over" is outside this spec.
- If the repo already knocks an on-tile grub in some other direction, the engineer reports it at the next Build; the rule in "Knockback direction" stands.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-visuals.md
# Combat visuals (build 0.5 target, Option A, G-001)

Status: visual spec and review rulings from the art-director for `design/combat.md`. It changes no rules, timings or parameters. Wherever it names a glyph or color, it covers what `combat.md` leaves to "chosen in Build". Build may change a glyph only if it keeps the rules in this file and documents the change in `manual.md`. V-9 to V-17 and the sections "Enemy on the player's tile" and "Hit lines name the attacker" were added for G-001 handoff 57 (see D-012). Reworded after QA's verification (70, answered in 73, D-014): "Position words", "Enemy on the player's tile", "Hit lines name the attacker", V-10, V-12, V-14, V-16, and V-18 is new. The art-director reviews this wording at Verify.

## Intent

The player must be able to tell, from one frame of `run_play` and its text lines, what can hurt them now, what is about to hurt them, and what is open to a counter. Pillar 3: every threat is visible before it can hurt. The picture and the text lines never say different things about where an enemy is.

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

## Position words (one vocabulary for all lines; one definition, D-014)

Every line that names where an enemy is uses the same words. They come from the one rule in `combat.md`, "Cells, sides and 'on you'", and are taken at the moment the line prints (the hit line has its own moment, see below):

- `on you`: the enemy is within 0.5 tile of the player (true position). It is the same test as the swipe's body hit. It is not decided by which cell the glyph falls in.
- Otherwise the word names the side of `P` on which the glyph is drawn in the same draw: `left`, `right`, `above`, `below` for a straight neighbour or farther along a straight line, and the combined forms `top left`, `top right`, `bottom left`, `bottom right` for other positions. An enemy farther than 0.5 tile whose cell is the player's cell is drawn beside `P` on the side it is offset toward, and gets that side's word.
- So a grub 0.2 tile from the player reads `on you` in the text lines, has an entry in the `on you:` line, and is drawn beside `P`; it never reads a side word at the same time. A grub 0.6 tile away reads a side word, is drawn on that side, and has no `on you:` entry.
- If two enemies of the same type would get the same words in the same draw, add the distance in tiles to both, for example `left, 1 tile` and `left, 3 tiles`. Do not add a distance otherwise, so the lines already praised stay as they are.

## Text lines (telegraph and feedback)

- Every telegraph prints a line at the moment the uppercase glyph appears. The line must say which enemy when more than one can act:
  - grub: "a grub rears back (left)" or "(above)", relative to the player, using the position words above. A grub within 0.5 tile of the player reads "(on you)". If two grubs wind up on the same draw, print two lines.
  - spitter: "spitter (top right) charges" and "spitter (bottom right) charges", as in the spec.
- Spit lines name the spitter ("spitter (top right) spits"). There are never two identical lines.
- Grub Recovery start prints "the grub is open" with the position words, for example "the grub is open (left)" or "the grub is open (on you)". The 0.9 s counter window is the point of the rework, and in a still frame lowercase `g` looks the same as Approach.
- Swipe result lines follow the spec: "you swipe: grub hit (1 left)", "grub defeated", and the "(miss)", "(too soon)", "(stunned)", "(down)" reasons. They are unchanged by this spec. In the swipe line "(1 left)" is hit points remaining, so no position word is added there.
- Spitter stagger after a hit prints "spitter (top right) is staggered".

## Enemy on the player's tile

D-006 stands: an enemy that would sit in the player's cell is drawn in a free cell beside the player and is never hidden. That drawn cell is a display offset only. The playtesters read it as the enemy's real position and could not tell which side a bite would come from or where to swing. The fix is a status line that says outright that the enemy is on the player's tile and where it was drawn. The glyphs stay the same and the lines already praised stay the same.

"On the player's tile" means "on you" as defined in "Position words": within 0.5 tile of the player. (This replaces any reading by cell equality.)

- **On-you line.** In every draw in which one or more enemies are on you, a line `on you:` prints directly under the hearts line, above the room. It lists each such enemy once: its glyph as currently drawn, its state in words, and the side it was drawn on. Format:
  - `on you: G biting soon (shown right)`
  - `on you: g open (shown below)`
  - with two, separated by `;`: `on you: G biting soon (shown right); g open (shown left)`
  - The state words are `walking`, `biting soon` (Wind-up and Strike), `open` (Recovery), `charging` (spitter Charge), `idle`. Use `biting soon` for both Wind-up and Strike so the line never lags the glyph.
  - `(shown <side>)` uses `left`, `right`, `above`, `below`, the straight neighbour cell where the glyph is drawn. An on-you enemy is always drawn in a straight neighbour cell (`combat.md`, rule 5), inside the room.
  - When nobody is on you the line is absent, not blank, so its appearance itself means "something is on you".
  - An enemy that is not on you never has an entry, even when it is drawn next to `P` because it shares the cell.
- **Meaning of the displaced glyph.** The player reads the glyph beside `P` as "the one named on the `on you:` line" when the line is present. The attacker is on the player's tile, so a bite from it is not coming from the drawn side. The manual says this in one sentence (see V-15).
- **Telling a displaced enemy from a real neighbor.** In a color view the displaced glyph also gets a reverse-video (inverse) cell. This is only a reinforcement, and the on-you line carries the meaning without it. Shape and color of the letter do not change, so V-1, V-4 and V-6 are unaffected.
- **Telegraph and open lines** for an on-you grub keep the existing wording with "(on you)", for example "a grub rears back (on you)" and "the grub is open (on you)". They print in the same draw in which the on-you line shows the new state. A line never says "(on you)" for an enemy that has no `on you:` entry in that draw, and never gives a side word for one that has.
- **Color.** The on-you line text is lantern-colored, never orange/red. Only the glyph letter inside it takes the glyph's color from the glyph table.
- **Valid under the designer's swipe rule.** The on-you line reports where enemies are and their state. If a swipe hits a grub on you, the swipe result lines print as usual, and the enemy's disappearance and the on-you line follow the draw rules below.
- **When the enemy leaves or dies.** The on-you line updates in the same draw as the event that ends the overlap: the swipe that prints "grub defeated", the player's dash, or the grub leaving the 0.5-tile radius. The displaced glyph and its line entry do not remain for a later draw.

## Hit lines name the attacker

- When the player loses a heart, the line names the attacker and its position:
  - grub: `YOU ARE HIT by a grub (left)`, `YOU ARE HIT by a grub (on you)`, `YOU ARE HIT by a grub (above)`, `YOU ARE HIT by a grub (top right)`.
  - spit shot: `YOU ARE HIT by a spit shot from spitter (top right)`. The position is the spitter's position when the shot lands (spitters do not move); if the spitter is gone, `YOU ARE HIT by a spit shot`.
- **Which position (D-014).** For a grub, the word is the one fixed when its Strike began (`combat.md`, "Strike-start position"): the grub's position word relative to the player at the instant its Wind-up ended. It is not taken at the damage tick, because the lunge moves the grub by up to 1 tile and the tick at which it lands depends on the frame rate. The grub stands still during Wind-up, so for a still player this is the word in its "rears back" line and the place of its `G` in the draw made at Wind-up start.
- A draw made during the 0.15 s Strike may show the grub already lunged into a nearer cell. The hit line still names the position it struck from, which is the one the player was shown while it was winding up. This is intended.
- The position words and the ambiguity rule are those of "Position words". With a grub on each side, the line names the side of the grub that actually dealt the damage.
- The line prints in the same draw as the hearts line update, as it does now.
- The grub named in the line must have been an uppercase glyph (Wind-up) in that position in the draw made at its Wind-up start. This follows from the telegraph and is what V-14 checks.
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
- **V-9** (on-you line present) Practice room: `player 8 4` and `spawn grub 8 4`. In every draw in which the grub is on you (within 0.5 tile), a line starting `on you:` appears under the hearts line and names its glyph, state word and `(shown <side>)`. In every draw in which no enemy is on you, no `on you:` line appears.
- **V-10** (line matches the picture) In every draw with an `on you:` line, the glyph letter in the line is the letter in the cell beside `P` on the side the line states, and that letter matches the state (uppercase for `biting soon` and `charging`, lowercase for `walking`, `open` and `idle`). Also, no enemy that has an entry in the line is named by a side word in any text line of the same draw, and no text line says "(on you)" for an enemy without an entry. Verified by reading the text of the draw, with no color needed.
- **V-11** (real neighbor versus displaced) Practice room: one grub on you and a second grub on the tile immediately to the player's right. A draw shows both glyphs adjacent to `P` or beside it, and only one of them is named by an `on you:` entry. A reader of the text alone can say which grub is on their tile.
- **V-12** (telegraph from the tile) A grub within 0.5 tile of the player that winds up prints "a grub rears back (on you)" in the same draw in which its on-you entry changes to `G ... biting soon`. When it enters Recovery, the same holds with "the grub is open (on you)" and `g ... open`. For a grub 0.2 tile from the player in room 2 (QA's 3.38 s and 4.38 s case) the lines read "(on you)", never "(left)" or "(right)".
- **V-13** (hit line names the attacker) Every heart lost to a grub prints `YOU ARE HIT by a grub (<position>)`, and every heart lost to a shot names the spitter or reads "by a spit shot". A hit line is never printed without a position word for a grub.
- **V-14** (which grub) Practice room: one grub left of the player and one right, with only the right one striking. The hit line reads `(right)`. Swapping which grub strikes swaps the word. In general, for a still player the position named in the hit line is the word of that grub's "rears back" line and is the place of its `G` or `W` in the draw made at its Wind-up start. A draw made during the Strike may show the grub lunged; it is not compared.
- **V-15** (manual, written by Build) `manual.md#on-screen` lists the `on you:` line and says that a letter beside `P` named on that line is on the player's tile. `manual.md#what-you-hear-and-read` lists the position in the hit line, "(on you)" and the position words. (The Owner places the text; the proposed lines are in handoff 73.)
- **V-16** (both frame rates) V-9 to V-14 and V-18 hold identically at 30 and 60 FPS, including the cell of an enemy resting on a half tile and the position in the hit line. No timing, damage, position or hit test value changes, and no extra draw is added beyond principle 4. The on-you line comes from the state of the draw that prints it; the position in the hit line comes from the Strike-start position.
- **V-17** (overlap ends) In the draw that prints "grub defeated" for an on-you grub, and in the draw after a dash off the tile, the on-you entry for that grub and its displaced glyph are gone.
- **V-18** (words match the picture) In every draw, the side word of every text line that names an enemy equals the side or corner of `P` on which that enemy's glyph is drawn in the same draw (for lines printed at that moment). An enemy exactly on a half-tile boundary is drawn in the same cell at 30 and 60 FPS (for instance a grub resting at x 13.5 with the player at x 14.5 is always drawn left of `P`).

## Experience signals (for playtest and Review)

- A tester told that a grub is on them can say which grub it is, and no longer says the picture is "drawn beside me" with no way to read it.
- With grubs on both sides, a tester can say which one hit them without being told.
- The lines praised in the playtest report ("rears back (left)", the capital and lowercase marks) are still read as before. The new lines do not push them off the screen in room 2 with four grubs around the player.
- A tester does not notice a text line and the map disagreeing about which side a grub is on.

## Not checked

- Actual colors cannot be assessed from the text view. This spec fixes the intent and the glyph rules. The reverse-video cell for a displaced enemy is a reinforcement that needs a look in a color build. A review of the built player view is still needed.
- Whether the player's hit-invulnerability (0.8 s) and dash invulnerability need a visible cue is left open. Suggestion: `p` (lowercase) for `P` during invulnerability. This needs no rule change, but it is optional and is not in the acceptance criteria.
- The playtester's possibly short warning at 11.90 s to 11.97 s is not a visual finding. The new hit line (V-13, V-14) will make it easier to trace which grub it was, but whether the warning was real is for `qa` and `game-designer`.
- Whether a very crowded tile (three or more enemies on the player's tile) fits one `on you:` line at the room's text width. The spec lists each entry; wrapping to a second line is allowed if needed.
- A draw made during the 0.15 s Strike can show the lunged grub in a nearer cell than the hit line names (see "Hit lines name the attacker"). The art-director confirms at Verify that this reads acceptably.
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
BODY_HIT = 0.5  # an enemy this close is hit by every swipe, whatever the facing (A3)
MISS_NEAR = 2.5  # "(miss) too far" looks this far
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.15, 0.8

GRUB_HP, GRUB_SPEED = 2, 2.0
GRUB_RANGE = 1.25  # a grub this close to the player may start a wind-up
GRUB_WINDUP, GRUB_STRIKE, GRUB_RECOVERY, GRUB_CANCEL_RECOVERY = 0.5, 0.15, 0.9, 0.6
GRUB_STRIKE_REACH, GRUB_LUNGE = 1.0, 1.0
GRUB_SLOTS = 2  # grubs allowed in Wind-up or Strike at once (backstop)
GRUB_SPACING = 1.0  # a wind-up may not start within this of another grub's wind-up start (A1)
GRUB_CAP, CAP_ZONE, WAIT_DIST = 2, 1.5, 2.0  # engagement cap: grubs inside CAP_ZONE; hold distance
KNOCK_DISTANCE, KNOCK_TIME = 1.0, 0.2
ON_TILE = 0.05  # closer than this to the player = on the player's tile (knockback rule, D-013)

SPITTER_HP = 2
SPIT_CHARGE, SPIT_RECOVERY, SPIT_STAGGER = 0.8, 0.6, 1.0
SPIT_INTERVAL, SPIT_FIRST, SPIT_OFFSET = 2.5, 1.0, 0.8
SHOT_SPEED, SHOT_REACH = 3.0, 0.4

DOWN_DELAY, CLEAR_DELAY = 2.0, 1.5

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
# Order for the side of an enemy on the player's tile: right, left, above, below.
SIDE_ORDER = [(1, 0), (-1, 0), (0, -1), (0, 1)]

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


def cell_of(x, y):
    return int(round(x)), int(round(y))


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


class Shot(list):
    """[x, y, vx, vy] plus the spitter that fired it (for the hit line)."""

    owner = None


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
        self.wait = None  # grub Waiting: None, "cap" or "spacing"
        self.wait_since = None  # time a spacing-blocked grub started waiting
        self.last_windup = -math.inf  # absolute time of this grub's last Wind-up start
        self.side = None  # unit step from the player to the cell the enemy was last seen in

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
        self.wait = None
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
        self._track()

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
        self._track()

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)
        self._track()

    def _track(self):
        """Remember on which side of the player each enemy was last seen in another cell.

        This is the display side of D-006; the on-tile knockback (D-013) uses it too.
        """
        pc = cell_of(self.x, self.y)
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            ec = cell_of(enemy.x, enemy.y)
            if ec == pc:
                continue
            dx, dy = ec[0] - pc[0], ec[1] - pc[1]
            if abs(dx) >= abs(dy):
                enemy.side = (1 if dx > 0 else -1, 0)
            else:
                enemy.side = (0, 1 if dy > 0 else -1)

    def _who(self, enemy):
        dup = any(
            o is not enemy and o.kind == enemy.kind and o.spot == enemy.spot
            for o in self.enemies
        )
        return {"who": enemy.index, "spot": enemy.spot, "dup": dup, "n": enemy.nth + 1}

    def _pos(self, enemy):
        """Position words of an enemy relative to the player (design/combat-visuals.md)."""
        dx, dy = enemy.x - self.x, enemy.y - self.y
        if abs(dx) < ON_TILE and abs(dy) < ON_TILE:
            return "on you"
        if abs(dx) < 0.5 and abs(dy) < 0.5:
            horizontal = abs(dx) >= abs(dy)
        elif abs(dy) < 0.5:
            horizontal = True
        elif abs(dx) < 0.5:
            horizontal = False
        else:
            return ("top " if dy < 0 else "bottom ") + ("left" if dx < 0 else "right")
        if horizontal:
            return "left" if dx < 0 else "right"
        return "above" if dy < 0 else "below"

    def _pos_words(self, enemy):
        """Position words; a distance is added when another enemy of the type has the same words."""
        words = self._pos(enemy)
        if words != "on you" and any(
            o is not enemy and o.alive and o.kind == enemy.kind and self._pos(o) == words
            for o in self.enemies
        ):
            n = max(1, round(math.hypot(enemy.x - self.x, enemy.y - self.y)))
            words += f", {n} tile" + ("" if n == 1 else "s")
        return words

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
            # A dash with a direction sets facing; a dash without one leaves it unchanged.
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation ----------------------------------------------------------------------------

    def step(self):
        self._step()
        self._track()

    def _step(self):
        dt = self.dt
        t0 = self.t
        self.frame += 1
        t1 = self.t
        self.stun_left = max(0.0, self.stun_left - dt)
        if self.stun_left <= EPS:
            self.stun_left = 0.0
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
            # The dash timer runs on elapsed time; a wall only shortens the distance (A5).
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
            in_cone = dist <= ATTACK_REACH and along > 0 and abs(across) <= along
            if dist <= BODY_HIT or in_cone:
                enemy.hp -= 1
                struck.append(enemy)
                hits.append(
                    (enemy.kind, "defeated" if enemy.hp <= 0 else "hit", enemy.hp, enemy.index)
                )
        miss = None
        if not hits:
            dists = [
                math.hypot(e.x - self.x, e.y - self.y) for e in self.enemies if e.alive
            ]
            if any(d <= ATTACK_REACH for d in dists):
                miss = "not in front"
            elif any(d <= MISS_NEAR for d in dists):
                miss = "too far"
        self.log("attack", facing=_name(self.facing), hits=hits, miss=miss)
        for enemy in struck:
            self._after_hit(enemy)

    def _after_hit(self, enemy):
        if enemy.hp <= 0:
            enemy.state = "dead"
            return
        if enemy.kind == "grub":
            if enemy.state in ("windup", "strike"):
                # A hit cancels the wind-up or the rest of the strike (A5).
                enemy.state, enemy.timer, enemy.carry = "recovery", GRUB_CANCEL_RECOVERY, 0.0
                self.log(
                    "recover", cause="interrupted", who=enemy.index, side=self._pos_words(enemy)
                )
            self._knock(enemy)
        elif enemy.state == "charge":
            enemy.state = "stagger"
            enemy.next_charge = self.t + SPIT_STAGGER
            self.log("stagger", **self._who(enemy))

    def _knock(self, enemy):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        dist = math.hypot(dx, dy)
        speed = KNOCK_DISTANCE / KNOCK_TIME
        on_tile = dist < ON_TILE
        if not on_tile:
            # Straight away from the player; a push toward an edge is clamped like a dash.
            vx, vy = dx / dist * speed, dy / dist * speed
        else:
            # D-013: toward the display side, else the next side with 1 tile of clear room.
            order = ([enemy.side] if enemy.side else []) + [
                d for d in SIDE_ORDER if d != enemy.side
            ]
            chosen = order[0]
            for d in order:
                nx, ny = enemy.x + d[0] * KNOCK_DISTANCE, enemy.y + d[1] * KNOCK_DISTANCE
                if 0 <= nx <= ROOM_W - 1 and 0 <= ny <= ROOM_H - 1:
                    chosen = d
                    break
            vx, vy = chosen[0] * speed, chosen[1] * speed
        enemy.knock_v = (vx, vy)
        enemy.knock_left = KNOCK_TIME
        self.log("knockback", who=enemy.index, on_tile=on_tile)

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
        # The nearest grub moves first, so it takes a free engagement slot first.
        for grub in sorted(grubs, key=lambda g: (math.hypot(g.x - self.x, g.y - self.y), g.index)):
            self._grub_move(grub, grubs, dt)
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
            self.log(
                "recover", when=at, cause="strike", who=enemy.index, side=self._pos_words(enemy)
            )
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
            if reach <= GRUB_STRIKE_REACH and self._hurt("grub", enemy):
                enemy.struck = True

    def _grub_move(self, enemy, grubs, dt):
        enemy.wait = None
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
        inside = sum(
            1
            for o in grubs
            if o is not enemy
            and o.alive
            and math.hypot(o.x - self.x, o.y - self.y) <= CAP_ZONE + 1e-9
        )
        if dist > CAP_ZONE and inside >= GRUB_CAP:
            # Waiting because of the engagement cap: hold about WAIT_DIST from the player.
            enemy.wait = "cap"
            if dist > WAIT_DIST:
                step = min(GRUB_SPEED * dt, dist - WAIT_DIST)
            else:
                step = -min(GRUB_SPEED * dt, WAIT_DIST - dist)
            enemy.x, enemy.y = self._clamp(
                enemy.x + dx / dist * step, enemy.y + dy / dist * step
            )
            return
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
                    since = grub.wait_since if grub.wait_since is not None else t1
                    candidates.append((round(dist, 6), since, grub.index, grub))
        candidates.sort(key=lambda c: c[:3])
        for _, _, _, grub in candidates:
            start = t1 - grub.carry
            others = max(
                (o.last_windup for o in self.enemies if o is not grub and o.kind == "grub"),
                default=-math.inf,
            )
            if free <= 0 or start - others < GRUB_SPACING - EPS:
                grub.wait = grub.wait or "spacing"
                if grub.wait_since is None:
                    grub.wait_since = t1
                continue
            free -= 1
            grub.state = "windup"
            grub.timer = GRUB_WINDUP - grub.carry
            grub.last_windup = start
            grub.wait, grub.wait_since = None, None
            self.log("windup", when=start, who=grub.index, side=self._pos_words(grub))
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
        shot = Shot([enemy.x + vx * elapsed, enemy.y + vy * elapsed, vx, vy])
        shot.owner = enemy
        self.shots.append(shot)
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
                self._hurt("shot", getattr(shot, "owner", None))
                continue
            kept.append(shot)
        self.shots = kept if self.phase == "playing" else []

    # --- Player damage, down, clear and run flow -----------------------------------------------

    def _hurt(self, source, enemy=None):
        if self.invulnerable or self.hearts <= 0:
            return False
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        extra = {}
        if enemy is not None:
            if enemy.kind == "grub":
                extra["pos"] = self._pos_words(enemy)
            elif enemy.alive:
                extra["spitter"] = self._who(enemy)
        self.log("hurt", source=source, hearts=self.hearts, **extra)
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
        self._track()
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

from game import ATTACK_REACH, HEARTS, ROOM_H, ROOM_W, SIDE_ORDER, Game, cell_of

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots

RESET = "\033[0m"
INVERSE = "\033[7m"  # reverse video: marks an enemy drawn beside P that is really on P's tile
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
    "miss_cause": "you swipe: (miss) {cause}",
    "ignored_attack": "you swipe: ({reason})",
    "ignored_dash": "you dash: ({reason})",
    "ignored_other": "you cannot move: ({reason})",
    "dash": "you dash {direction}",
    "hurt": "YOU ARE HIT by {by} — hearts {hearts}/{max}",
    "down": "you went down",
    "cleared": "room cleared",
    "heal": "you catch your breath — hearts {hearts}/{max}",
    "run_complete": "run complete",
    "room_loaded": "room {room} begins",
    "run_start": "a new run begins",
    "run_over": "run over — rooms cleared: {rooms}",
    "run_over_complete": "run complete — rooms cleared: {rooms}",
    "restart": "press attack to start again",
    "on_you": "on you: {entries}",
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
        if lines:
            return lines
        if d.get("miss"):
            return [LINES["miss_cause"].format(cause=d["miss"])]
        return [LINES["miss"]]
    if kind == "ignored":
        key = {"attack": "ignored_attack", "dash": "ignored_dash"}.get(
            d["action"], "ignored_other"
        )
        return [LINES[key].format(reason=d["reason"])]
    if kind == "dash":
        return [LINES["dash"].format(direction=d["direction"])]
    if kind == "hurt":
        source = d["source"]
        if source == "grub":
            by = f"a grub ({d['pos']})" if "pos" in d else "a grub"
        elif source == "shot":
            by = "a spit shot"
            sp = d.get("spitter")
            if sp:
                num = f" {sp['n']}" if sp["dup"] else ""
                by += f" from spitter{num} ({sp['spot']})"
        else:
            by = f"a {source}"
        return [LINES["hurt"].format(by=by, hearts=d["hearts"], max=HEARTS)]
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


def glyph_key(enemy):
    key = enemy.kind
    if enemy.hp < enemy.max_hp:
        key += "_hurt"
    if enemy.committed:
        key += "_alert"
    return key


def state_word(enemy):
    if enemy.kind == "grub":
        return {"windup": "biting soon", "strike": "biting soon", "recovery": "open"}.get(
            enemy.state, "walking"
        )
    return "charging" if enemy.state == "charge" else "idle"


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

    def paint(self, key, inverse=False):
        char, color = GLYPHS[key]
        if not self.color:
            return char
        return f"{INVERSE if inverse else ''}{color}{char}{RESET}"

    # --- Display offset for enemies on the player's cell (D-006, AC-18; drawing only) ----------

    def free_cell(self, pc, taken, enemy):
        """Nearest free in-room cell beside the player for an enemy that shares the player's cell.

        Order: the side the enemy last came from, then right, left, above, below; if all four are
        taken, the free cell nearest to the player (ties: top row first, then left).
        """
        order = []
        pref = enemy.side
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
        """(player cell, {id(enemy): drawn cell}, [enemies on the player's cell])."""
        g = self.game
        pc = cell_of(g.x, g.y)
        living = [e for e in g.enemies if e.alive]
        placed, taken, on_tile = {}, {pc}, []
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
                on_tile.append(enemy)
        return pc, placed, on_tile

    def on_you_line(self, pc, placed, on_tile):
        entries = []
        for enemy in on_tile:
            cx, cy = placed[id(enemy)]
            dx, dy = cx - pc[0], cy - pc[1]
            if abs(dx) >= abs(dy):
                side = "right" if dx > 0 else "left"
            else:
                side = "below" if dy > 0 else "above"
            char = GLYPHS[glyph_key(enemy)][0]
            entries.append(f"{char} {state_word(enemy)} (shown {side})")
        return LINES["on_you"].format(entries="; ".join(entries))

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(col, row, key, inverse=False):
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = self.paint(key, inverse)

        pc, placed, on_tile = self.enemy_cells()
        if g.hearts <= 0:
            on_tile = []  # enemies stop acting when the player is down
        if g.arc_left > 0:
            # The arc fills only empty tiles: an enemy (or the player) always wins its cell.
            occupied = set(placed.values()) | {pc}
            for col, row in arc_tiles(g):
                if (col, row) not in occupied:
                    put(col, row, ARC_KEYS[g.arc_dir])
        for shot in g.shots:
            put(*cell_of(shot[0], shot[1]), "shot")
        shifted = {id(e) for e in on_tile} if g.hearts > 0 else set()
        for enemy in g.enemies:
            if enemy.alive:
                put(*placed[id(enemy)], glyph_key(enemy), inverse=id(enemy) in shifted)
        put(*pc, "player" if g.hearts > 0 else "down")
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        if on_tile:
            print(self.on_you_line(pc, placed, on_tile))
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

    def label(self, e):
        if e.kind == "grub" and e.state == "approach" and e.wait:
            return f"waiting-{e.wait}"
        return e.state

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} room={g.room} phase={g.phase} "
            f"pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f} shots={len(g.shots)}"
        )
        enemies = " ".join(
            f"{e.kind}#{e.index}({e.x:.2f},{e.y:.2f},hp={e.hp},{self.label(e)},{self.remaining(e):.3f})"
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
import math
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


def last_attack(game):
    return [d for _, k, d in game.events if k == "attack"][-1]


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

    def test_swipe_during_strike_cancels_it(self):  # AC-26
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.5, 4)
                run_until(game, "strike")
                self.assertEqual(game.enemies[0].state, "strike")
                game.press("attack")
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                self.assertEqual(grub.state, "recovery")
                self.assertAlmostEqual(grub.timer, 0.6, delta=0.01)
                self.assertEqual(len(last_attack(game)["hits"]), 1)
                self.assertIsNone(last_attack(game)["miss"])
                run(game, 1.0)
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
                self.assertGreaterEqual(peak, 1)

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


class CrowdTest(unittest.TestCase):
    """A1 wind-up spacing, the engagement cap and hit-stun (AC-19 to AC-22)."""

    def test_windup_spacing(self):  # AC-19
        for room in "125":
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    game = Game(fps=fps, room=room)
                    run(game, 12.0)
                    starts = sorted(times(game, "windup"))
                    self.assertGreaterEqual(len(starts), 2)
                    for a, b in zip(starts, starts[1:]):
                        self.assertGreaterEqual(b - a, 1.0 - tol(fps))

    def test_spacing_applies_between_grubs_only(self):
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "windup")
                run(game, 0.2)
                game.press("attack")  # interrupted: its next wind-up comes sooner than 1.0 s
                run(game, 3.0)
                starts = times(game, "windup")
                self.assertGreaterEqual(len(starts), 2)

    def test_engagement_cap(self):  # AC-20, AC-21
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="2")
                peak, saw_cap_wait = 0, False
                while game.t < 12.0 and game.phase == "playing":
                    game.step()
                    near = sum(
                        1 for e in game.enemies
                        if e.alive and math.hypot(e.x - game.x, e.y - game.y) <= 1.5 + 1e-9
                    )
                    peak = max(peak, near)
                    self.assertLessEqual(near, 2)
                    saw_cap_wait = saw_cap_wait or any(e.wait == "cap" for e in game.enemies)
                self.assertEqual(peak, 2)
                self.assertTrue(saw_cap_wait)
                hurts = times(game, "hurt")
                if len(hurts) >= 3:
                    self.assertGreaterEqual(hurts[2] - hurts[0], 1.9)

    def test_hit_stun_is_short(self):  # AC-22
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.spawn("grub", 8.5, 4)
                run_until(game, "hurt")
                hit = times(game, "hurt")[0]
                run(game, 0.05)
                game.press("attack")
                self.assertEqual(game.events[-1][2]["reason"], "stunned")
                run_to(game, hit + 0.25)
                swipes = len(times(game, "attack"))
                game.press("attack")
                self.assertEqual(len(times(game, "attack")), swipes + 1)
                run_to(game, hit + 0.79)
                self.assertTrue(game.invulnerable)
                run_to(game, hit + 0.85)
                self.assertFalse(game.invulnerable)


class SwipeTest(unittest.TestCase):
    def one_grub(self, gx, gy, facing=None, fps=60):
        game = Game(fps=fps, room="empty")
        game.place_player(8, 4)
        game.spawn("grub", gx, gy)
        if facing:
            game.press("move", facing)
            game.press("stop")
        return game

    def test_body_hit(self):  # AC-23
        for fps in FPS:
            with self.subTest(fps=fps, case="a"):
                game = self.one_grub(8.2, 4, fps=fps)
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, 1)
            for facing, gx in (("right", 7.6), ("left", 8.4)):
                with self.subTest(fps=fps, case="b", facing=facing):
                    game = self.one_grub(gx, 4, facing, fps)
                    game.press("attack")
                    self.assertEqual(game.enemies[0].hp, 1)
            for facing, gx in (("right", 7.2), ("left", 8.8)):
                with self.subTest(fps=fps, case="c", facing=facing):
                    game = self.one_grub(gx, 4, facing, fps)
                    game.press("attack")
                    self.assertEqual(game.enemies[0].hp, 2)
                    self.assertEqual(last_attack(game)["miss"], "not in front")

    def test_miss_wording(self):  # AC-27
        cases = (
            (10, 4, "too far", "you swipe: (miss) too far"),
            (8, 5, "not in front", "you swipe: (miss) not in front"),
            (8, 8, None, "you swipe: (miss)"),
        )
        for gx, gy, cause, line in cases:
            with self.subTest(gx=gx, gy=gy):
                game = self.one_grub(gx, gy)
                game.press("attack")
                self.assertEqual(last_attack(game)["miss"], cause)
                text = capture(f"room empty\nspawn grub {gx} {gy}\nplayer 8 4\n0 attack\nend 0.3\n")
                self.assertIn(line, [s for _, s in timed_lines(text)])
                self.assertIn(")", "".join(r for r in text.splitlines() if r.startswith("   |")))


class DashRulesTest(unittest.TestCase):
    def test_dash_sets_facing(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("move", "right")
        game.press("stop")
        game.press("dash", "left")
        run(game, 0.3)
        game.press("attack")
        self.assertEqual(last_attack(game)["facing"], "left")
        text = capture("room empty\nplayer 8 4\n0 move right\n0.1 stop\n0.3 dash left\n0.7 attack\nend 1\n")
        self.assertIn("(", "".join(r for r in text.splitlines() if r.startswith("   |")))

    def test_dash_without_direction_keeps_facing(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("move", "up")
        game.press("stop")
        game.press("dash")
        self.assertEqual(game.facing, (0, -1))

    def test_queued_attack_fires_in_dash_direction(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("dash", "down")
        run(game, 0.1)
        game.press("attack")
        run(game, 0.2)
        self.assertEqual(last_attack(game)["facing"], "down")

    def test_wall_dash_lasts_full_time_and_stays_invulnerable(self):  # AC-25
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                start = game.t
                game.press("dash", "left")
                while not times(game, "dash_end"):
                    self.assertTrue(game.invulnerable)
                    game.step()
                self.assertAlmostEqual(game.t - start, 0.25, delta=tol(fps))
                self.assertEqual(game.x, 0.0)

    def test_dash_right_ends_at_12(self):  # AC-25
        for fps in FPS:
            game = Game(fps=fps, room="empty")
            game.place_player(8, 4)
            game.press("dash", "right")
            run(game, 0.4)
            self.assertAlmostEqual(game.x, 12.0, delta=0.25)


class KnockbackTest(unittest.TestCase):
    """AC-28 (D-013)."""

    def swipe_on_tile(self, fps, px=8.0, side=None, at=0.2):
        game = Game(fps=fps, room="empty")
        game.place_player(px, 4)
        game.spawn("grub", px, 4)
        if side:
            game.enemies[0].side = side
        run(game, at)
        game.press("attack")
        return game

    def test_on_tile_grub_steps_to_its_display_side(self):  # AC-28 (a)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps)
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                run(game, 0.25)
                self.assertAlmostEqual(grub.x, 9.0, delta=0.1)
                self.assertAlmostEqual(grub.y, 4.0, delta=0.1)
                game = self.swipe_on_tile(fps, side=(0, 1))
                run(game, 0.25)
                self.assertAlmostEqual(game.enemies[0].y, 5.0, delta=0.1)

    def test_blocked_side_uses_the_next_side(self):  # AC-28 (b)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps, px=14.5, side=(1, 0))
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertLessEqual(grub.x, 15.0)
                self.assertGreaterEqual(math.hypot(grub.x - game.x, grub.y - game.y), 0.9)
                self.assertLess(grub.x, game.x)

    def test_slots_and_distance(self):  # AC-28 (c)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertLess(math.hypot(grub.x - game.x, grub.y - game.y), 1.5)
                far = Game(fps=fps, room="empty")
                far.place_player(8, 4)
                far.spawn("grub", 9.4, 4)
                far.press("attack")
                run(far, 0.2)
                g = far.enemies[0]
                self.assertGreaterEqual(math.hypot(g.x - far.x, g.y - far.y), 1.5)

    def test_knockback_keeps_timers(self):  # AC-28 (d)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "recover")
                run(game, 0.2)
                before = game.enemies[0].timer
                game.press("attack")
                self.assertEqual(game.enemies[0].state, "recovery")
                self.assertAlmostEqual(game.enemies[0].timer, before, delta=1e-9)

    def test_result_line_has_no_on_you(self):  # AC-28 (e), V-9, V-17
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\n0.2 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: grub hit (1 left)", lines)
        self.assertFalse(any(s.startswith("you swipe") and "(on you)" in s for s in lines))
        self.assertIn("on you: g walking (shown right)", text)
        last_draw = text.rsplit("hearts", 2)[-1]
        self.assertNotIn("on you:", last_draw)


class OnYouLineTest(unittest.TestCase):
    def test_line_present_only_while_on_tile(self):  # V-9, V-10
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\nend 1.2\n")
        self.assertRegex(text, r"(?m)^on you: [gG] [a-z ]+ \(shown (left|right|above|below)\)$")
        text = capture("room empty\nspawn grub 12 4\nplayer 8 4\nend 0.4\n")
        self.assertNotIn("on you:", text)

    def test_line_matches_the_picture(self):  # V-10
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\nend 4\n")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"on you: (\w) ([a-z ]+) \(shown (\w+)\)", line)
            if not m:
                continue
            glyph, word, side = m.groups()
            rows = [l[4:-1] for l in lines[i + 1 : i + 2 + ROOM_H] if l.startswith("   |")]
            (pc, pr), = find(rows, "Px")
            dc, dr = {"left": (-1, 0), "right": (1, 0), "above": (0, -1), "below": (0, 1)}[side]
            self.assertEqual(rows[pr + dr][pc + dc], glyph)
            self.assertEqual(glyph.isupper(), word == "biting soon")

    def test_hit_line_names_the_attacker(self):  # V-13, V-14
        text = capture("room empty\nspawn grub 12 4\nplayer 8 4\nend 3\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a grub (right)") for s in lines), lines)
        text = capture("room empty\nspawn grub 4 4\nplayer 8 4\nend 3\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a grub (left)") for s in lines), lines)

    def test_shot_hit_line_names_the_spitter(self):  # V-13
        text = capture("room empty\nspawn spitter 13 4\nplayer 8 4\nend 5\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a spit shot from spitter (") for s in lines), lines)


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

    def test_real_neighbour_versus_displaced(self):  # V-11
        text = capture("room empty\nspawn grub 8 4\nspawn grub 9 4\nplayer 8 4\nend 0.1\n")
        on_you = [l for l in text.splitlines() if l.startswith("on you:")]
        self.assertTrue(on_you)
        self.assertEqual(on_you[0].count("("), 1)

    def test_down_player_keeps_x_and_enemy_beside(self):  # AC-18
        game = Game(room="empty")
        game.place_player(8, 4)
        game.spawn("grub", 8.0, 4)
        down(game)
        out = play.Player(game)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out.start()
        self.assertNotIn("on you:", buf.getvalue())
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
                run(game, 0.32)  # the hit-stun (0.15 s) has passed
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

    def test_room_2_same_wind_up_order_at_both_rates(self):  # AC-17
        a, b = Game(fps=30, room="2"), Game(fps=60, room="2")
        run(a, 6.0)
        run(b, 6.0)
        wa = [d["who"] for _, k, d in a.events if k == "windup"]
        wb = [d["who"] for _, k, d in b.events if k == "windup"]
        self.assertEqual(wa, wb)


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

<<<FILE decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
---
kind: decision
id: D-014
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-014: One rule for cells, sides, "on you" and the hit-line word

## Decision

All of these come from true positions by one rule, written in `design/combat.md` ("Cells, sides and 'on you'") and used by the draw, the text lines, the `on you:` line, the hit line and the knockback:

1. **Cell at .5:** `cell(v) = floor(v + 0.5 + 0.005)`. An exact .5 (or within 0.005 below it) goes to the larger index (right, down). No banker's rounding, no raw float compare. The player is drawn in `cell(player)`.
2. **On you:** the enemy is within 0.5 tile of the player by true position (the body-hit radius, same test as the swipe). Not cell equality, and not the 0.05 tile used before for the text and knockback.
3. **Position word of an enemy not on you:** the side of `P` on which its glyph is drawn (cell offset; if it shares the player's cell but is farther than 0.5 tile, the side of its true offset). An on-you enemy reads "on you" in every line, has an entry in the `on you:` line, and is drawn in a free straight neighbour cell inside the room.
4. **Hit-line word for a grub:** the position word fixed at the instant its Strike began (the end of Wind-up), not the lunge position at the damage tick. For a still player this equals its "rears back" word and the place of its `G` in the Wind-up start draw.
5. **Knockback of an on-you grub:** toward the side it is drawn on, ending 1.0 tile from the player's true position on that side. The display side may only be an in-room cell, so a grub on a player at the edge (player 14.5) is drawn and knocked left.
6. Criteria: AC-17, AC-28 reworded; AC-29, AC-30 new in `design/combat.md`; V-10, V-12, V-14, V-16 reworded and V-18 new in `design/combat-visuals.md`.

Limits: no timing, damage, hit test, cap or spacing value changes. The spitter hit line keeps its wording (position when the shot lands). Colors and glyphs are untouched. It does not decide the manual text.

## Rationale

- QA found the same cause three times: the display and the text lines took a position from different places (rounding at a boundary, cell equality versus distance, lunge tick). The picture and the text must never contradict (pillar 3), so one definition feeds all of them.
- Round-half-to-larger with a small tolerance gives the same cell for a resting position at 30 and 60 FPS, because the tolerance is far larger than float noise and far smaller than a frame of movement.
- "On you" at 0.5 tile matches the swipe's body-hit radius. The playtest promise (A3) is that a grub "on you" can always be hit; a cell-based definition could call a grub 0.9 tile behind "on you" and then let the swipe miss it.
- The strike-start position is a fact fixed by the Wind-up: the grub stands still during it and the player saw it. The lunge position at the damage tick depends on which frame the damage lands in, so it cannot be the same at both rates.
- Reusing the display side for the knockback (D-013) keeps its promise that the grub steps out where it was shown, including the edge case that failed (player 14.5).

## Alternatives considered

- **Relative rounding (round the offset, ties away from the player):** rejected. At the room edge it can place a glyph outside the room (player 14.5, grub 15.0) or in the player's own cell.
- **Round half to even / leave to the build:** rejected. That is the cause of D-A.
- **"On you" = same drawn cell:** rejected. It makes the word depend on the player's absolute rounding, and a grub that a swipe can miss would be called "on you".
- **"On you" = 0.05 tile (the old text/knockback value):** rejected. A grub 0.2 tile away would show a side word and be drawn displaced, with no hint in the text, which was the original confusion D-012 fixed.
- **Hit word from the damage tick (as built):** rejected, it differs between 30 and 60 FPS. **Hit word from the last draw the player saw:** rejected, draws are every 0.5 s plus events, so that position depends on timing as well.
- **Freeze the drawn cell of a striking grub at its Strike-start cell:** rejected for now. It is a display lie of up to 1 tile for 0.15 s and a new rule; the art-director can reopen it at Verify if a lunged draw reads badly.
- **Knock an on-you grub straight away from the true offset:** rejected for offsets of 0.05–0.5 tile. It could land on the side opposite the drawn glyph (D-013).

## Revisit when

- A playtest or the art-director's review shows that a draw taken during the Strike, with the grub in a nearer cell than the hit line names, confuses players.
- Overlap or movement rules change (Option B), or the view gets two cells per tile.
- The tolerance of 0.005 tile ever lets two different resting positions share a cell at one rate and not the other.
>>>END

<<<FILE goals/G-001-combat-monotony/73-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 73
from: game-designer
to: studio
stage: Build (the Studio composes the step for gameplay-engineer)
outcome: done
---
# 73: game-designer → studio — Rulings for the three spec gaps (cell at .5, "on you", hit-line word); criteria changed

## Task

Compose the Build step for `gameplay-engineer`. The engineer applies the rulings below and fixes the failing suite test and the display defects from 70. QA then re-verifies the items listed under "QA must re-verify".

## Context

G-001, Option A (D-002). QA's verification (70) failed on three spec gaps (D-A, D-B, D-C). All three are settled in `design/combat.md` ("Cells, sides and 'on you'") and `design/combat-visuals.md`, and recorded in D-014. These are the first Design returns for these items (AC-19…AC-28 and V-9…V-17 were new at 70). I did not edit `manual.md` and did not run `play`/`bots`; the rulings come from reading 70 and `repo/game.py`.

## Findings

### Rulings

1. **Cell at .5 (Gap 1, D-A).** `cell(v) = floor(v + 0.5 + 0.005)` on each axis, used for the player and for enemies. An exact .5 (or up to 0.005 below it) goes to the larger index (right/down). The built code uses `int(round(...))` (`cell_of`), which is Python's round-half-even and is float-noise sensitive at .5, the likely reason for the 30 FPS mismatch. For QA's case the player (14.5) is cell 15 and the grub at 13.5 is cell 14, so the grub is drawn **left** at both rates. Also, the display side of an on-you enemy may only be a cell inside the room: for `player 14.5`, a grub on the tile cannot be shown to the right (cell 16 does not exist), so it is shown and knocked left from the first draw. AC-28(b) now says so.
2. **"On you" (Gap 2, D-B).** On you = true distance to the player ≤ 0.5 tile (the body-hit radius, same test as the swipe; tolerance 1e-6). It is defined once and used for the `on you:` entry, the displaced glyph, "(on you)" in telegraph/open/hit lines, and the knockback. The old 0.05-tile `ON_TILE` for text and knockback goes away. A grub 0.2 tile away now reads "(on you)" in every line, has an entry in the `on you:` line, and is drawn displaced; no draw has a side word and an entry for the same enemy. An enemy farther than 0.5 tile gets a side word and no entry, even when it shares the player's cell (it is then drawn in the cell on the side of its true offset, and that is the side the word names).
3. **Side/corner word of an enemy not on you.** From the cell offset to `P` (left/right/above/below for straight, corner words otherwise). If it shares the player's cell, the side of the larger true-offset axis (tie: horizontal). So the word always matches where the glyph is drawn (new V-18). The distance suffix rule is unchanged (compare words, as before).
4. **Hit-line word (Gap 3, D-C).** For a grub: the position word fixed at the instant the Strike begins (end of Wind-up), stored for that strike and used in the `hurt` event and the hit line. Not the lunge position at the damage tick. A still player gets the same word as in the "rears back" line. For QA's 4.3 s case the expected word is the corner word at both rates (the grub wound up from the top right). A draw made during the 0.15 s Strike may show the lunged glyph; the line still names the Wind-up position. Spitter hit lines are unchanged.
5. **Knockback of an on-you grub (D-013 reworded).** Direction: the side it is drawn on. End point: 1.0 tile from the player's true position on that side (so the glyph lands in the cell it was already drawn in). The normal case (more than 0.5 tile away) stays "straight away". Exactly on the tile the result is the same as before; the only behavioral change is for a grub 0.05–0.5 tile away (before: straight away from the true offset; now: toward its display side, ending 1.0 from the player).

### Changed criteria

- `design/combat.md`: **AC-17** (now AC-1…AC-30, adds identical cells/words), **AC-28** (a) adds the 0.2-tile case, (b) rewritten for the edge (`player 14.5`, shown left from the first draw, ends at x 13.5, same cell and words at both rates), **AC-29** (new, cell at an exact half tile: grub at x 13.5 with player 14.5; ±1 pairs at 8.5), **AC-30** (new, one meaning of on you and of position words, and the hit-line word). AC-23, AC-26 (note only) and the knockback text are reworded without changing their pass conditions.
- `design/combat-visuals.md`: **V-10** (adds: no side word for an entry, no "(on you)" without one), **V-12** (adds the 0.2-tile room 2 case), **V-14** (general sentence now compares with the Wind-up start draw), **V-16** (adds half-tile cells and the Strike-start word), **V-18** (new).
- Unchanged: V-9, V-11, V-13, V-17, V-1…V-8, and every other AC.

### QA must re-verify (both frame rates)

AC-17; AC-28 (a, b, and c if a room 2 on-you run is possible); AC-29; AC-30; V-10, V-12, V-14, V-16, V-18; V-15 after the Owner places the manual text. Also the items from 70 §6 that were not observed (AC-1, AC-3, AC-9, AC-10, AC-12, AC-14 real clear, AC-13 restart, V-2/V-4/V-7/V-8 spitter views) remain open for that round. AC-22 (suite part) is the engineer's `test_hit_stun_is_short` matter.

### Previously passing behavior that changes

- Knockback end point of a grub 0.05–0.5 tile from the player (see ruling 5). AC-28(a) as QA ran it (`spawn grub 8 4`) is unaffected: still 9.00.
- The `_pos`-based words: positions near cell borders may now be named by cell (matches the picture). Scripted left/right cases (V-14, V-11) are unaffected. The `ON_TILE` 0.05 test is replaced by the 0.5 test (the same as `BODY_HIT`) for words and knockback. No timing, damage, hit-test, cap or spacing value changes. AC-2, 4, 5, 7, 11, 19, 21, 23–27 and AC-28 a/d/e do not depend on these and should still pass. If the engineer finds that one does, report it back; do not change a number.
- AC-23(c) note: a grub 0.8 tile behind can share the player's cell (for example the player at x 8.4) and is not on you; it is drawn beside `P` on the side it is offset toward and a swipe prints "(miss) not in front". This is the scenario of AC-30(b).

### Notes for the Studio

- The strike cancel window (AC-26, D-58-1) is one tick wide (0.033 s at 30 FPS). No change; written as is. I added a known-note to AC-26.
- AC-21 has a thin margin (1.97 s, limit 1.9). No change; it will move if the engineer changes spacing or the cap, which these rulings do not.
- The art-director reviews the new wording at Verify (D-006 / D-012 stay valid). One point to look at: a draw during the Strike can show the lunged grub nearer than the hit line names (alternative rejected in D-014).
- This was not an escalation case: no direction, scope or pillar change.

### Final V-15 manual lines (for the Owner to place; manual.md not edited)

The existing draft (65, 71) holds for the glyph table, `x`, arcs, practice room and the `on you:` meaning; the points below replace or sharpen the position wording only.

For `manual.md#on-screen`:
- "If a grub is on you, a line starting `on you:` appears under your hearts. It lists each one with its letter, what it is doing (`walking`, `biting soon`, `open`, `charging`, `idle`) and the side where it is drawn, for example `on you: G biting soon (shown right)`. A letter beside `P` that is named on that line is on your own tile, not beside you. A grub that is on you is always hit by your swipe. When no line appears, nothing is on you."

For `manual.md#what-you-hear-and-read`:
- "Lines that tell you where an enemy is use the same words: `on you` (it is within half a tile of you), `left`, `right`, `above`, `below`, and `top left`, `top right`, `bottom left`, `bottom right`. The word names the side of `P` where the letter is drawn. When two enemies of the same kind would get the same word, a distance is added, for example `left, 1 tile`."
- "When you lose a heart the line says what hit you and where it came from: `YOU ARE HIT by a grub (left)`, `(on you)`, `(top right)`, or `YOU ARE HIT by a spit shot from spitter (top right)`. The place named is where the grub was when it started its bite, which is the place you saw it wind up."
- (Outdated line, not required by a criterion) "`(miss)` alone means nothing was within 2.5 tiles; `(miss) too far` means something is within 2.5 tiles but beyond your reach; `(miss) not in front` means something is within reach but outside your swing."

## Decisions already made

- D-001, D-005, D-007, D-011, D-012, D-013 as in 72.
- **D-014 (new):** the rulings above. D-013 stays in force; its direction/end-point wording is superseded by D-014 where they differ, as described in ruling 5.

## Constraints

- The engineer implements; I specify no code structure. Build must not change any number (timings, 0.5 tile, cap, spacing) beyond the new `on you` radius that equals the existing body-hit radius.
- Must play correctly at both 30 and 60 FPS. `manual.md` is the Owner's.

## Open questions

None for the designer. For the Studio: the art-director's review of the wording at Verify; the Owner's suite run and manual text (as in 70); the engineer's explanation of `CrowdTest.test_hit_stun_is_short`.

## Expected output

Build (`gameplay-engineer`): code changes for rulings 1–5 plus the failing test and the display defects from 70; trace/play evidence at 30 and 60 FPS for AC-28(b), AC-29 and AC-30 before handing to QA. Then Verify (`qa`) with the list above.

## Sender assessment

I am confident in rulings 1–3 and 5 (they follow from the cause that QA reported and from the code). Ruling 4 is a choice between the Strike-start position and the last draw the player saw; I took the Strike-start position because the grub stands still then and it does not depend on the frame. The residual risk is the visual mismatch of a lunged glyph in a draw made inside the 0.15 s Strike, noted for the art-director.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, repo/ (build)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/70-qa-to-studio.md
>>>END

<<<FILE goals/G-001-combat-monotony/70-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 70
from: qa
to: studio
stage: Verify (report to Studio; the Studio composes the next step)
outcome: fail
---
# 70: qa → studio — Verification report for the combat response change set (AC-1…AC-28, V-9…V-17) at 30 and 60 FPS: FAIL

## Task

Report the pass/fail result of verifying the current build in `repo/` against `design/combat.md` (AC-1…AC-28) and `design/combat-visuals.md` (V-9…V-17, earlier V items as regression) at 30 and 60 FPS. Route the failures. Verdict: **fail**. One failure is a genuine test failure, one is a frame-rate-dependent display defect, and one is a manual gap that criterion V-15 needs.

## Context

Handoff 68 asked for verification of the grub turn-taking, engagement cap, 0.15 s hit-stun, body hit, dash facing, miss causes, Strike cancel, on-tile knockback, `on you:` line and attacker position in hit lines. I verified from the spec, criteria and build only. All runs (tests, play, trace, bots) are in `@run-results`, and no rounds are left. I did not edit the repo or `manual.md`.

## Findings

### 1. Test suite (`python3 -m unittest discover -s tests`)

Ran 63 tests: **failures=2, errors=2**, so 59 passed. The earlier Owner run (D-010) was 40/40, so the suite has grown and that result does not carry over.

- `ManualTest.test_manual_lists_glyphs_and_lines`: ERROR, `FileNotFoundError: '/manual.md'`.
- `ManualTest.test_on_screen_section_lists_x_and_the_practice_room`: ERROR, same cause.
  - The tests look for `manual.md` one level above `repo/`, and it is not present in my environment. This is an environment gap, not a build result.
  - **AC-15 cannot be judged by me this round.** The Owner must run the suite with the unchanged `manual.md` in place (as in D-008 and D-010) and report counts and any failure by name.
  - By reading, `manual.md#on-screen` lists `x` (table row) and the practice room (paragraph), so AC-15's wording looks satisfied.
- `CrowdTest.test_hit_stun_is_short` (fps=30): FAIL at `tests/test_game.py` line 282, `assertTrue(game.invulnerable)` was False.
- `CrowdTest.test_hit_stun_is_short` (fps=60): same FAIL.
  - I cannot see the test source, so I cannot say whether the test or the build is wrong.
  - My own traces show the rule behaving as specified: invulnerable until 0.8 s after the hit (30 FPS: hit 0.567, ends 1.367; 60 FPS: hit 0.550, ends 1.350), and stun 0.15 s.
  - This is a failing test in the suite and counts as a failure of AC-22 and AC-17 until the engineer explains it.

### 2. Defects found by playing

**D-A (30 FPS only): the grub is drawn on the opposite side of its true position after a wall knockback. This breaks V-16, V-10 and the intent of AC-28(b) and D-013.**

Reproduce:
```
fps 30
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```
- Trace at 30 FPS: after the hit, the grub moves to x=14.33 and then 13.50 (left, 1.0 tile). It winds up at 0.800 with `side: left` and strikes with `pos: left`. The true positions satisfy AC-28(b): left, 1.0 tile, inside the room.
- Player view at 30 FPS: the draws at 0.50 s, 0.80 s, 1.00 s and 1.33 s still show `on you: w open (shown right)` / `on you: W biting soon (shown right)` and the glyph to the **right** of `P`, from 0.5 s until about 1.45 s.
  - In the same draws, the text lines say "a grub rears back (left)" and "YOU ARE HIT by a grub (left)". Picture and text contradict each other, and the grub appears to have jumped to the side the player was not shown.
- At 60 FPS the same script is correct. The 0.50 s draw shows `wP` with no `on you:` line, and 0.80 s shows `WP`, matching the text (left).
- Likely cause (QA's reading, not verified): the grub rests at exactly x=13.5, a half-tile boundary, so its cell differs between frame rates.
- The spec does not say how cells round at exactly .5. The engineer should check it, and the designer should say if the rule needs a line.

**D-B: position word "(left)" in a line while the same draw has an `on you:` entry for that grub (room 2).**
- 30 FPS, `room 2`, `end 6`: "the grub is open (left)" at 3.383, and the draw at 3.40 shows `on you: g open (shown left)`.
- The same happens at 4.383 with "(right)" and `on you: … g open (shown right)`.
- 60 FPS shows the same at 3.383 and 4.383.
- The text line takes its word from the true position (about 0.2 tile away, so "left"). The on-you line and the displaced glyph use cell equality.
- V-12 and "Position words" say "same tile as the player: on you", and a reader sees both "(left)" and an on-you entry.
- **Spec gap:** "same tile" is not defined as true-position-based or cell-based. The game-designer or art-director must decide (see Open questions).

**D-C: the hit-line position word differs between frame rates (room 2, around 4.3 s). This is V-16, and V-14's general sentence at 30 FPS.**
- 30 FPS: "YOU ARE HIT by a grub (right)" at 4.300 (trace `pos: right`, grub at 8.67,3.55). The draw before the hit (4.00) shows `G` at the top right.
- 60 FPS: "(top right)" at 4.283 (grub at 8.76,3.49). The draw before the hit shows `G` at the top right, so it matches.
- The word is taken from the lunge position at the damage tick, which differs between frame rates, so at 30 FPS the named position does not match the uppercase glyph in the draw before the hit.
- The scripted V-14 scenario (one grub left, one right) passes at both rates.

**D-D (Owner step, not a code defect): `manual.md` lacks the text that V-15 requires.**
- Not present:
  - The `on you:` line, and "a letter beside `P` named on that line is on your tile". The manual only says "drawn on a free tile next to you".
  - The position in the hit line ("YOU ARE HIT by a grub (left)"), "(on you)", and the position words, in `#what-you-hear-and-read`.
- Outdated: the manual still says "(miss)" means "nothing in reach". No criterion requires the miss causes ("too far", "not in front") to be in the manual, but the player-visible text now differs from the manual.
- Present and consistent: glyph table, `x`, arcs, the practice room in On screen (V-5, AC-15 wording).
- Needed by a criterion: V-15 (both parts). The Owner places the draft text (open Owner step). Then re-check V-15 and rerun the suite.

### 3. Per-criterion results

"Observed" means I saw it in this round's runs. Rows marked "not observed" were not re-run this round, so I cannot confirm them, and no regression was seen in the evidence I do have.

**AC list**

| ID | Result | Evidence |
|---|---|---|
| AC-1 | not observed (indirect: telegraph precedes the first bite by 0.5 s in all runs) | no distance-4 run |
| AC-2 | pass 30/60 | windup 0.5 (0.800→1.300), strike 0.15, recovery 0.9 on the 60 FPS trace (0.900 at recover) and 0.883 on the 30 FPS trace (0.9 minus one tick) |
| AC-3 | not observed | |
| AC-4 | pass 30/60 | `cycle` runs: bites at 0.567→2.100 (30, gap 1.53 s) and 0.533→2.083 (60, gap 1.55 s) after a counter hit in Recovery |
| AC-5 | pass 30/60 | `strike-a-30` and `far-knock`: hit in Windup, `recover interrupted` about 0.6 s, no heart lost |
| AC-6 | pass (sampled) | room 5 still: only one grub in Windup/Strike at each sampled row, both rates |
| AC-7 | pass 30/60 | room 5: charges at 1.000 and 1.800, repeats at 3.500 and 4.300 |
| AC-8 | partial | charge/spit rows name the spitter, no duplicates; player view of spitter not run |
| AC-9, AC-10, AC-12 | not observed | |
| AC-11 | pass | one reason per miss ("too far", "not in front", plain "(miss)"); "stunned" and "dash not ready" appear in the trace as ignored actions |
| AC-13 | partial | `you went down`, `x`, enemies stop, shots=0, `over` 2.0 s later (30: 5.267→7.267; 60: 5.250→7.250). Run-over screen text and attack-restart not observed |
| AC-14 | partial | practice room only: "grub defeated" then "room cleared". Heal, next-room load, same-tick clear and "run complete" not observed |
| AC-15 | **cannot judge, needs the Owner's run** | see §1 |
| AC-16 | pass for rooms 1, 2, 5 | setup rows match; rooms 3 and 4 not observed |
| AC-17 | **fail** | event timings agree within 0.02 s (e.g. room 2: windups 2.733/3.733/4.733 at both rates), but D-A and D-C break the 30/60 identity of the display and hit-line positions, and AC-22's suite test fails |
| AC-18 | partial | on-tile windup and open draws show `G`/`g` beside `P`. The distance-4 idle run to 5.5 s and the spitter `S` case were not run |
| AC-19 | pass 30/60 | wind-up starts in room 2 at 2.733, 3.733, 4.733 (both rates); room 1 at 1.400, 2.400, 3.400 (30) and 1.383, 2.383, 3.383 (60); room 5 at 2.233, 3.233, 4.233 (30). Gaps are 1.0 s. Single grub: AC-2 cycle unchanged |
| AC-20 | pass (sampled) | room 2: at the sampled rows at most 2 grubs are within 1.5 tiles, the others `waiting-cap` at about 2.0 (e.g. 3.233: g1 and g3 at 2.0). Not every tick is visible in the trace |
| AC-21 | pass, thin margin | first to third heart: 3.300→5.267 = 1.97 s (30), 3.283→5.250 = 1.97 s (60), limit 1.9. One grub committed at a time |
| AC-22 (behavior) | pass 30/60 | stun ends 0.15 s after the hit. Attack at +0.05 s and dash are "stunned". Attack at +0.28 s swipes. Invulnerability ends 0.8 s after the hit. Dash 0.25 s after the hit not exercised |
| AC-22 (suite) | **fail** | `CrowdTest.test_hit_stun_is_short` fails at both rates, see §1 |
| AC-23 | pass 30/60 | (a) on-tile and 0.2 tile: hit. (b) 0.4 tile behind, facing right and left: hit. (c) 0.8 tile behind: `miss: not in front` |
| AC-24 | pass 30/60 | `dash left` after facing right gives `facing: left` and `(` arc; `dash` with no direction after `move up` goes up and the attack faces up; an attack queued during a dash fires at dash end facing left |
| AC-25 | pass 30/60 | `dash right` from x=8 ends at 12.00; `dash left` from x=2 ends at 0.00; both last about 0.233 s (0.25 minus one tick); a second dash at +0.4 s is "dash not ready". Damage during a wall-shortened dash not exercised |
| AC-26 | pass 30/60 | a swipe on the first tick of Strike (30: 0.567; 60: 0.550) hits and cancels it, no heart lost, 0.6 s Recovery. A swipe in Recovery in front hits. No "(miss)" |
| AC-27 | pass 30/60 | "(miss) too far" (grub 2.0 ahead), "(miss) not in front" (grub 1.0 below), "(miss)" alone; arc drawn in all three |
| AC-28 (a) | pass 30/60 | `player 8 4`, `spawn grub 8 4`: shown right with `on you:`; after the hit the 0.23/0.22 s draw still shows it on the tile, the 0.50 s draw shows `w` right of `P` with no `on you:`; true position 9.00 (1.0 tile) |
| AC-28 (b) | true positions pass; **display fails at 30** | see D-A |
| AC-28 (c) | not observed | no room 2 run with an on-tile grub |
| AC-28 (d) | pass | knock-on-tile sequence shows state and timers unchanged; next bite is 1.5 s or more after the previous |
| AC-28 (e) | pass | "you swipe: grub hit (1 left)" without "(on you)" |

**V list**

| ID | Result |
|---|---|
| V-1 | pass for grubs; `w` in the hit draw |
| V-2 | pass for windup start and swipe draws at both rates; charge and projectile draws not observed |
| V-3 | pass |
| V-4 | pass for `g/w`, `G/W`; `s/z`, `S/Z` not observed |
| V-5 | pass by reading `manual.md` (glyph table, `x`, arcs) |
| V-6 | not assessable in the text view |
| V-7, V-8 | not observed this round (V-8: the trace shows `over` but the restart prompt was not seen in a player view) |
| V-9 | pass at 30/60 for the scripted case; absent when no one is on the tile |
| V-10 | pass in self-consistency; D-A shows the picture can contradict the true position |
| V-11 | pass 30/60 (`gPg`, only one entry in the on-you line, "shown left") |
| V-12 | pass for a grub truly on the tile; D-B for the room 2 case |
| V-13 | pass for grub hits (every line has a position); shot hit line not seen in a player view |
| V-14 | pass for the scripted left/right case at both rates; general sentence fails at 30 in room 2 (D-C) |
| V-15 | **fail** (D-D) |
| V-16 | **fail** (D-A, D-C) |
| V-17 | pass 30/60: on-tile grub defeated, and a dash off the tile (`dashoff`): the next draw has no entry and no displaced glyph |

### 4. Strike at 30 FPS (the open point D-58-1)

Observed first-hand. A swipe at 0.52 s and 0.53 s (processed at the first Strike tick, 0.567) hits the grub, cancels the strike and costs no heart. A swipe at 0.50 s hits it in its last Wind-up tick. A swipe after the damage tick (0.55 s) is "stunned", because the 0.15 s stun covers the rest of the 0.15 s Strike. In practice the cancel window is one tick (0.033 s at 30 FPS, 0.017–0.033 s at 60 FPS). That matches the written rule, but the designer may want to know it is this narrow.

### 5. Reference data from the balance bots (no balance judgement)

The script grammar needed was `fps N` and optionally `rooms N`. `room 1` is rejected ("cannot read"). The default is 60 FPS. Cells are clear time, hearts lost, attacks, dashes.

**60 FPS**

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 | Total |
|---|---|---|---|---|---|---|
| camper | 3.5 s, 0, 6, 0 | 4.5 s, 0, 6, 0 | NOT cleared 5.5 s, 3 lost (shots), 0, 0 | NOT cleared 6.9 s, 3 lost (shots), 4, 0 | NOT cleared 6.9 s, 3 lost (shots), 6, 0 | 2/5, 9 hearts, 0 dashes |
| walker | 3.5 s, 0, 6, 0 | 5.1 s, 0, 8, 0 | 9.0 s, 0, 6, 0 | 9.1 s, 0, 8, 0 | 11.2 s, 0, 10, 0 | 5/5, 0, 0 |
| dodger | 3.5 s, 0, 6, 0 | 5.1 s, 0, 8, 0 | 11.8 s, 0, 6, 4 | 10.0 s, 0, 8, 1 | 9.8 s, 0, 10, 2 | 5/5, 0, 7 |
| reactive | 3.5 s, 0, 6, 0 | 6.7 s, 0, 9, 2 | 11.8 s, 0, 6, 4 | 12.9 s, 0, 9, 5 | 11.1 s, 0, 11, 2 | 5/5, 0, 13 |

**30 FPS**

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 | Total |
|---|---|---|---|---|---|---|
| camper | 3.5 s, 0, 6, 0 | 4.5 s, 0, 6, 0 | NOT cleared 5.5 s, 3 lost (shots), 0, 0 | NOT cleared 6.9 s, 3 lost (shots), 4, 0 | NOT cleared 6.9 s, 3 lost (shots), 6, 0 | 2/5, 9 hearts, 0 dashes |
| walker | 3.5 s, 0, 6, 0 | 4.8 s, 0, 8, 0 | 9.2 s, 0, 6, 0 | 9.1 s, 0, 8, 0 | 12.3 s, 0, 10, 0 | 5/5, 0, 0 |
| dodger | 3.5 s, 0, 6, 0 | 4.8 s, 0, 8, 0 | 9.5 s, 0, 6, 2 | 10.1 s, 0, 8, 1 | 14.5 s, 0, 10, 6 | 5/5, 0, 9 |
| reactive | 3.5 s, 0, 6, 0 | 4.8 s, 0, 8, 0 | 9.5 s, 0, 6, 2 | 14.3 s, 0, 8, 6 | 11.1 s, 0, 10, 2 | 5/5, 0, 10 |

Idle-player reference (down time, a still player):

| Room | 30 FPS | 60 FPS |
|---|---|---|
| room 1 | about 3.93 s | about 3.90 s |
| room 2 | 5.27 s | 5.25 s |
| room 5 | 4.60 s | 4.57 s |

### 6. Could not observe

- Anything needing the Owner's suite run: the two `ManualTest` tests (AC-15) and any test that reads `manual.md`. Also the source of `test_hit_stun_is_short`.
- Not run this round: AC-1 (distance 4), AC-3 (dash away in wind-up), AC-9, AC-10, AC-12, AC-28(c).
- Not run this round: real-room clear with heal and next-room load (AC-14), "run complete", the run-over screen text, and the attack-restart (AC-13, V-8).
- No spitter player-view runs this round (V-2 charge/projectile draws, V-4 `s/z/S/Z`, V-7, shot hit line).
- Colors (V-6) are not assessable in the text view.
- Engagement cap at every tick (only trace samples at events and the 0.5 s draws were read).

### 7. Failed before?

From this packet alone: AC-15 failed once before on the line-wrap in `run over` (D-009) and was then settled by the Owner's run (D-010). I cannot confirm the earlier history of any other criterion, since the earlier reports are not in my packet. AC-19…AC-28 are new this round. The Studio should check the loop count for AC-17, AC-22, V-14 and V-16 against the earlier reports before routing.

## Decisions already made

- D-001: one attack button plus dash. No new inputs.
- D-009: the manual phrase check ignores line wraps.
- D-010: AC-15 passed on the Owner's run (40/40) for the earlier build. It does not cover the current 63-test suite.
- D-011: grubs take turns, crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line; hit lines name the attacker position.
- D-013: knockback of an on-tile grub toward its display side.

## Constraints

- Do not edit `manual.md`. The Owner places the draft text.
- No production changes by QA. All findings go to the engineer or designer.
- A criterion failing a second time goes to `technical-director` (check the loop counts in §7).
- Must play correctly at both 30 and 60 FPS. D-A, D-C and the suite failure are the reasons this fails.

## Open questions

1. **To `gameplay-engineer`:** why does `CrowdTest.test_hit_stun_is_short` fail at both frame rates when the traces show the rule correct? Is the test or the build wrong? Fix D-A (display side and cell at the half-tile boundary) so that the 30 and 60 FPS views match.
2. **To `game-designer` (spec gaps):**
   - Does "on you" in text lines and the hit line mean true-position same tile, or same drawn cell (D-B)?
   - Should the hit-line word come from the position at the damage tick, or from the glyph position in the draw before the hit (D-C)?
   - How do cells round at exactly .5 tile (D-A)?
3. **To the Owner:** run `python3 -m unittest discover -s tests` in `repo/` with the unchanged `manual.md` beside it and report counts and any failure by name (AC-15). Place the V-15 draft text in `manual.md`; QA will then recheck V-15.

## Expected output

The Studio composes the next step from this report. Route the failures to `gameplay-engineer` (suite failure, D-A, D-C) and `game-designer` (D-B and the position-word definitions). Route the manual text and the suite rerun to the Owner. After the fixes, QA re-verifies AC-17, AC-22, AC-28(b), V-10, V-14, V-15, V-16 at both frame rates, plus the "not observed" list in §6.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/ (build: run commands in project.md)
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-010-owner-ran-suite-ac15-passes.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/68-studio-to-qa.md
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
BODY_HIT = 0.5  # an enemy this close is hit by every swipe, whatever the facing (A3)
ON_YOU = BODY_HIT  # "on you" is the same test as the body hit (D-014)
ON_YOU_TOL = 1e-6
CELL_TOL = 0.005  # cell(v) = floor(v + 0.5 + CELL_TOL): an exact .5 goes to the larger index (D-014)
MISS_NEAR = 2.5  # "(miss) too far" looks this far
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.15, 0.8

GRUB_HP, GRUB_SPEED = 2, 2.0
GRUB_RANGE = 1.25  # a grub this close to the player may start a wind-up
GRUB_WINDUP, GRUB_STRIKE, GRUB_RECOVERY, GRUB_CANCEL_RECOVERY = 0.5, 0.15, 0.9, 0.6
GRUB_STRIKE_REACH, GRUB_LUNGE = 1.0, 1.0
GRUB_SLOTS = 2  # grubs allowed in Wind-up or Strike at once (backstop)
GRUB_SPACING = 1.0  # a wind-up may not start within this of another grub's wind-up start (A1)
GRUB_CAP, CAP_ZONE, WAIT_DIST = 2, 1.5, 2.0  # engagement cap: grubs inside CAP_ZONE; hold distance
KNOCK_DISTANCE, KNOCK_TIME = 1.0, 0.2

SPITTER_HP = 2
SPIT_CHARGE, SPIT_RECOVERY, SPIT_STAGGER = 0.8, 0.6, 1.0
SPIT_INTERVAL, SPIT_FIRST, SPIT_OFFSET = 2.5, 1.0, 0.8
SHOT_SPEED, SHOT_REACH = 3.0, 0.4

DOWN_DELAY, CLEAR_DELAY = 2.0, 1.5

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
# Order for the side of an enemy on the player's tile: right, left, above, below.
SIDE_ORDER = [(1, 0), (-1, 0), (0, -1), (0, 1)]

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


def cell1(v):
    """Cell of one coordinate (D-014): round to nearest, an exact .5 goes to the larger index."""
    return int(math.floor(v + 0.5 + CELL_TOL))


def cell_of(x, y):
    return cell1(x), cell1(y)


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


class Shot(list):
    """[x, y, vx, vy] plus the spitter that fired it (for the hit line)."""

    owner = None


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
        self.strike_pos = None  # grub: position word fixed when its Strike began (D-014)
        self.wait = None  # grub Waiting: None, "cap" or "spacing"
        self.wait_since = None  # time a spacing-blocked grub started waiting
        self.last_windup = -math.inf  # absolute time of this grub's last Wind-up start
        self.side = None  # unit step from the player to the cell the enemy was last seen in

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
        self.wait = None
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
        self._track()

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
        self._track()

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)
        self._track()

    def _track(self):
        """Remember on which side of the player each enemy was last seen in another cell.

        This is the display side of D-006; the on-you knockback (D-013, D-014) prefers it too.
        """
        pc = cell_of(self.x, self.y)
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            ec = cell_of(enemy.x, enemy.y)
            if ec == pc:
                continue
            dx, dy = ec[0] - pc[0], ec[1] - pc[1]
            if abs(dx) >= abs(dy):
                enemy.side = (1 if dx > 0 else -1, 0)
            else:
                enemy.side = (0, 1 if dy > 0 else -1)

    def _who(self, enemy):
        dup = any(
            o is not enemy and o.kind == enemy.kind and o.spot == enemy.spot
            for o in self.enemies
        )
        return {"who": enemy.index, "spot": enemy.spot, "dup": dup, "n": enemy.nth + 1}

    # --- Cells, sides and "on you" (D-014): the one definition ---------------------------------

    def is_on_you(self, enemy):
        """True distance to the player is at most the body-hit radius."""
        return math.hypot(enemy.x - self.x, enemy.y - self.y) <= ON_YOU + ON_YOU_TOL

    def _cell_offset(self, enemy):
        """Cell offset of an enemy not on you; the larger true-offset axis if it shares the cell."""
        pc = cell_of(self.x, self.y)
        ec = cell_of(enemy.x, enemy.y)
        cx, cy = ec[0] - pc[0], ec[1] - pc[1]
        if cx == 0 and cy == 0:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if abs(dx) >= abs(dy) - 1e-9:
                cx = 1 if dx > 0 else -1
            else:
                cy = 1 if dy > 0 else -1
        return cx, cy

    def _pos(self, enemy):
        """Position word of an enemy relative to the player (design/combat.md, D-014)."""
        if self.is_on_you(enemy):
            return "on you"
        cx, cy = self._cell_offset(enemy)
        if cy == 0:
            return "left" if cx < 0 else "right"
        if cx == 0:
            return "above" if cy < 0 else "below"
        return ("top " if cy < 0 else "bottom ") + ("left" if cx < 0 else "right")

    def _pos_words(self, enemy):
        """Position words; a distance is added when another enemy of the type has the same words."""
        words = self._pos(enemy)
        if words != "on you" and any(
            o is not enemy and o.alive and o.kind == enemy.kind and self._pos(o) == words
            for o in self.enemies
        ):
            n = max(1, round(math.hypot(enemy.x - self.x, enemy.y - self.y)))
            words += f", {n} tile" + ("" if n == 1 else "s")
        return words

    def _side_ok(self, d):
        """A side is usable when its cell and the knockback end point are inside the room."""
        pc = cell_of(self.x, self.y)
        c = (pc[0] + d[0], pc[1] + d[1])
        ex, ey = self.x + d[0] * KNOCK_DISTANCE, self.y + d[1] * KNOCK_DISTANCE
        return (
            0 <= c[0] < ROOM_W
            and 0 <= c[1] < ROOM_H
            and -EPS <= ex <= ROOM_W - 1 + EPS
            and -EPS <= ey <= ROOM_H - 1 + EPS
        )

    def layout(self):
        """Where each living enemy is drawn: (player cell, {id(enemy): cell}, [(enemy, side)]).

        The list holds the enemies on you, in room order, with the side (unit step) they are drawn
        on. The draw, the `on you:` line and the knockback all use this (rule 5 of D-014).
        """
        pc = cell_of(self.x, self.y)
        living = [e for e in self.enemies if e.alive]
        on_you = [e for e in living if self.is_on_you(e)]
        placed, taken = {}, {pc}
        for e in living:
            if any(e is o for o in on_you):
                continue
            cx, cy = self._cell_offset(e)
            c = (min(max(pc[0] + cx, 0), ROOM_W - 1), min(max(pc[1] + cy, 0), ROOM_H - 1))
            placed[id(e)] = c
            taken.add(c)
        entries = []
        for e in on_you:
            own = cell_of(e.x, e.y)
            d = (own[0] - pc[0], own[1] - pc[1])
            if d in SIDE_ORDER and own not in taken and self._side_ok(d):
                placed[id(e)] = own
                taken.add(own)
                entries.append((e, d))
                continue
            order = ([e.side] if e.side else []) + [s for s in SIDE_ORDER if s != e.side]
            chosen = None
            for s in order:
                c = (pc[0] + s[0], pc[1] + s[1])
                if c not in taken and self._side_ok(s):
                    chosen = (c, s)
                    break
            if chosen is None:
                free = sorted(
                    (math.hypot(col - pc[0], row - pc[1]), row, col)
                    for row in range(ROOM_H)
                    for col in range(ROOM_W)
                    if (col, row) not in taken
                )
                if free:
                    _, row, col = free[0]
                    dx, dy = col - pc[0], row - pc[1]
                    s = ((1 if dx > 0 else -1), 0) if abs(dx) >= abs(dy) else (0, (1 if dy > 0 else -1))
                    chosen = ((col, row), s)
                else:
                    chosen = (pc, (1, 0))
            placed[id(e)] = chosen[0]
            taken.add(chosen[0])
            entries.append((e, chosen[1]))
        return pc, placed, entries

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
            # A dash with a direction sets facing; a dash without one leaves it unchanged.
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation ----------------------------------------------------------------------------

    def step(self):
        self._step()
        self._track()

    def _step(self):
        dt = self.dt
        t0 = self.t
        self.frame += 1
        t1 = self.t
        self.stun_left = max(0.0, self.stun_left - dt)
        if self.stun_left <= EPS:
            self.stun_left = 0.0
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
            # The dash timer runs on elapsed time; a wall only shortens the distance (A5).
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
            in_cone = dist <= ATTACK_REACH and along > 0 and abs(across) <= along
            if dist <= BODY_HIT + ON_YOU_TOL or in_cone:
                enemy.hp -= 1
                struck.append(enemy)
                hits.append(
                    (enemy.kind, "defeated" if enemy.hp <= 0 else "hit", enemy.hp, enemy.index)
                )
        miss = None
        if not hits:
            dists = [
                math.hypot(e.x - self.x, e.y - self.y) for e in self.enemies if e.alive
            ]
            if any(d <= ATTACK_REACH for d in dists):
                miss = "not in front"
            elif any(d <= MISS_NEAR for d in dists):
                miss = "too far"
        self.log("attack", facing=_name(self.facing), hits=hits, miss=miss)
        for enemy in struck:
            self._after_hit(enemy)

    def _after_hit(self, enemy):
        if enemy.hp <= 0:
            enemy.state = "dead"
            return
        if enemy.kind == "grub":
            if enemy.state in ("windup", "strike"):
                # A hit cancels the wind-up or the rest of the strike (A5).
                enemy.state, enemy.timer, enemy.carry = "recovery", GRUB_CANCEL_RECOVERY, 0.0
                self.log(
                    "recover", cause="interrupted", who=enemy.index, side=self._pos_words(enemy)
                )
            self._knock(enemy)
        elif enemy.state == "charge":
            enemy.state = "stagger"
            enemy.next_charge = self.t + SPIT_STAGGER
            self.log("stagger", **self._who(enemy))

    def _knock(self, enemy):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        speed = KNOCK_DISTANCE / KNOCK_TIME
        on_you = self.is_on_you(enemy)
        if not on_you:
            # Straight away from the player; a push toward an edge is clamped like a dash.
            dist = math.hypot(dx, dy)
            vx, vy = dx / dist * speed, dy / dist * speed
        else:
            # D-014: toward the side it is drawn on, ending 1.0 tile from the player's true position.
            side = next((s for e, s in self.layout()[2] if e is enemy), (1, 0))
            tx, ty = self._clamp(
                self.x + side[0] * KNOCK_DISTANCE, self.y + side[1] * KNOCK_DISTANCE
            )
            vx, vy = (tx - enemy.x) / KNOCK_TIME, (ty - enemy.y) / KNOCK_TIME
        enemy.knock_v = (vx, vy)
        enemy.knock_left = KNOCK_TIME
        self.log("knockback", who=enemy.index, on_tile=on_you)

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
        # The nearest grub moves first, so it takes a free engagement slot first.
        for grub in sorted(grubs, key=lambda g: (math.hypot(g.x - self.x, g.y - self.y), g.index)):
            self._grub_move(grub, grubs, dt)
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
            # D-014: the hit line names the position the grub struck from, fixed now.
            enemy.strike_pos = self._pos_words(enemy)
            enemy.state, enemy.timer, enemy.struck = "strike", GRUB_STRIKE, False
            self.log("strike", when=at, who=enemy.index)
        elif enemy.state == "strike":
            enemy.state, enemy.timer = "recovery", GRUB_RECOVERY
            self.log(
                "recover", when=at, cause="strike", who=enemy.index, side=self._pos_words(enemy)
            )
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
            if reach <= GRUB_STRIKE_REACH and self._hurt("grub", enemy):
                enemy.struck = True

    def _grub_move(self, enemy, grubs, dt):
        enemy.wait = None
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
        inside = sum(
            1
            for o in grubs
            if o is not enemy
            and o.alive
            and math.hypot(o.x - self.x, o.y - self.y) <= CAP_ZONE + 1e-9
        )
        if dist > CAP_ZONE and inside >= GRUB_CAP:
            # Waiting because of the engagement cap: hold about WAIT_DIST from the player.
            enemy.wait = "cap"
            if dist > WAIT_DIST:
                step = min(GRUB_SPEED * dt, dist - WAIT_DIST)
            else:
                step = -min(GRUB_SPEED * dt, WAIT_DIST - dist)
            enemy.x, enemy.y = self._clamp(
                enemy.x + dx / dist * step, enemy.y + dy / dist * step
            )
            return
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
                    since = grub.wait_since if grub.wait_since is not None else t1
                    candidates.append((round(dist, 6), since, grub.index, grub))
        candidates.sort(key=lambda c: c[:3])
        for _, _, _, grub in candidates:
            start = t1 - grub.carry
            others = max(
                (o.last_windup for o in self.enemies if o is not grub and o.kind == "grub"),
                default=-math.inf,
            )
            if free <= 0 or start - others < GRUB_SPACING - EPS:
                grub.wait = grub.wait or "spacing"
                if grub.wait_since is None:
                    grub.wait_since = t1
                continue
            free -= 1
            grub.state = "windup"
            grub.timer = GRUB_WINDUP - grub.carry
            grub.last_windup = start
            grub.wait, grub.wait_since = None, None
            self.log("windup", when=start, who=grub.index, side=self._pos_words(grub))
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
        shot = Shot([enemy.x + vx * elapsed, enemy.y + vy * elapsed, vx, vy])
        shot.owner = enemy
        self.shots.append(shot)
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
                self._hurt("shot", getattr(shot, "owner", None))
                continue
            kept.append(shot)
        self.shots = kept if self.phase == "playing" else []

    # --- Player damage, down, clear and run flow -----------------------------------------------

    def _hurt(self, source, enemy=None):
        if self.invulnerable or self.hearts <= 0:
            return False
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        extra = {}
        if enemy is not None:
            if enemy.kind == "grub":
                # The word fixed at Strike start, never the lunge position at the damage tick.
                extra["pos"] = enemy.strike_pos or self._pos_words(enemy)
                extra["who"] = enemy.index
            elif enemy.alive:
                extra["spitter"] = self._who(enemy)
        self.log("hurt", source=source, hearts=self.hearts, **extra)
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
        self._track()
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

<<<FILE repo/play.py (proposed in a run round; not written)
"""Play an input script against the build and print the session.

usage: python3 play.py [--color] --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format is described in the project's manual.md. Color is only added with --color or
when the output is a terminal; the glyphs carry every state without it.
"""

import argparse
import sys

from game import ATTACK_REACH, HEARTS, ROOM_H, ROOM_W, Game, cell_of

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots

RESET = "\033[0m"
INVERSE = "\033[7m"  # reverse video: marks an enemy drawn beside P that is really on P's tile
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
SIDE_WORDS = {(1, 0): "right", (-1, 0): "left", (0, -1): "above", (0, 1): "below"}

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
    "miss_cause": "you swipe: (miss) {cause}",
    "ignored_attack": "you swipe: ({reason})",
    "ignored_dash": "you dash: ({reason})",
    "ignored_other": "you cannot move: ({reason})",
    "dash": "you dash {direction}",
    "hurt": "YOU ARE HIT by {by} — hearts {hearts}/{max}",
    "down": "you went down",
    "cleared": "room cleared",
    "heal": "you catch your breath — hearts {hearts}/{max}",
    "run_complete": "run complete",
    "room_loaded": "room {room} begins",
    "run_start": "a new run begins",
    "run_over": "run over — rooms cleared: {rooms}",
    "run_over_complete": "run complete — rooms cleared: {rooms}",
    "restart": "press attack to start again",
    "on_you": "on you: {entries}",
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
        if lines:
            return lines
        if d.get("miss"):
            return [LINES["miss_cause"].format(cause=d["miss"])]
        return [LINES["miss"]]
    if kind == "ignored":
        key = {"attack": "ignored_attack", "dash": "ignored_dash"}.get(
            d["action"], "ignored_other"
        )
        return [LINES[key].format(reason=d["reason"])]
    if kind == "dash":
        return [LINES["dash"].format(direction=d["direction"])]
    if kind == "hurt":
        source = d["source"]
        if source == "grub":
            by = f"a grub ({d['pos']})" if "pos" in d else "a grub"
        elif source == "shot":
            by = "a spit shot"
            sp = d.get("spitter")
            if sp:
                num = f" {sp['n']}" if sp["dup"] else ""
                by += f" from spitter{num} ({sp['spot']})"
        else:
            by = f"a {source}"
        return [LINES["hurt"].format(by=by, hearts=d["hearts"], max=HEARTS)]
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


def glyph_key(enemy):
    key = enemy.kind
    if enemy.hp < enemy.max_hp:
        key += "_hurt"
    if enemy.committed:
        key += "_alert"
    return key


def state_word(enemy):
    if enemy.kind == "grub":
        return {"windup": "biting soon", "strike": "biting soon", "recovery": "open"}.get(
            enemy.state, "walking"
        )
    return "charging" if enemy.state == "charge" else "idle"


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

    def paint(self, key, inverse=False):
        char, color = GLYPHS[key]
        if not self.color:
            return char
        return f"{INVERSE if inverse else ''}{color}{char}{RESET}"

    def on_you_line(self, entries):
        parts = []
        for enemy, side in entries:
            char = GLYPHS[glyph_key(enemy)][0]
            parts.append(f"{char} {state_word(enemy)} (shown {SIDE_WORDS[side]})")
        return LINES["on_you"].format(entries="; ".join(parts))

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(col, row, key, inverse=False):
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = self.paint(key, inverse)

        # One rule for cells, sides and "on you" (D-014): game.layout() feeds the picture and the
        # on-you line; the text lines use the same definitions.
        pc, placed, entries = g.layout()
        if g.hearts <= 0:
            entries = []  # enemies stop acting when the player is down
        if g.arc_left > 0:
            # The arc fills only empty tiles: an enemy (or the player) always wins its cell.
            occupied = set(placed.values()) | {pc}
            for col, row in arc_tiles(g):
                if (col, row) not in occupied:
                    put(col, row, ARC_KEYS[g.arc_dir])
        for shot in g.shots:
            put(*cell_of(shot[0], shot[1]), "shot")
        shifted = {id(e) for e, _ in entries}
        for enemy in g.enemies:
            if enemy.alive:
                put(*placed[id(enemy)], glyph_key(enemy), inverse=id(enemy) in shifted)
        put(*pc, "player" if g.hearts > 0 else "down")
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        if entries:
            print(self.on_you_line(entries))
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

    def label(self, e):
        if e.kind == "grub" and e.state == "approach" and e.wait:
            return f"waiting-{e.wait}"
        return e.state

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} room={g.room} phase={g.phase} "
            f"pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f} shots={len(g.shots)}"
        )
        enemies = " ".join(
            f"{e.kind}#{e.index}({e.x:.2f},{e.y:.2f},hp={e.hp},{self.label(e)},{self.remaining(e):.3f})"
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

<<<FILE repo/tests/test_game.py (proposed in a run round; not written)
import contextlib
import io
import math
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
import play  # noqa: E402
from game import DASH_DISTANCE, HEARTS, ROOM_H, ROOMS, START, Game, cell1  # noqa: E402

FPS = (30, 60)
REPO = Path(__file__).resolve().parent.parent


def _find_manual():
    # manual.md sits next to repo/ in the project directory (the Owner places it, D-005). Look in a
    # few nearby places so the suite also runs where repo/ is mounted somewhere else.
    for base in (REPO.parent, REPO, Path.cwd(), Path.cwd().parent):
        if (base / "manual.md").exists():
            return base / "manual.md"
    return REPO.parent / "manual.md"


MANUAL = _find_manual()


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


def cell_word(pc, c):
    """Position word of a drawn cell relative to the player's cell."""
    cx, cy = c[0] - pc[0], c[1] - pc[1]
    if cy == 0:
        return "left" if cx < 0 else "right"
    if cx == 0:
        return "above" if cy < 0 else "below"
    return ("top " if cy < 0 else "bottom ") + ("left" if cx < 0 else "right")


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


def last_attack(game):
    return [d for _, k, d in game.events if k == "attack"][-1]


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

    def test_swipe_during_strike_cancels_it(self):  # AC-26
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.5, 4)
                run_until(game, "strike")
                self.assertEqual(game.enemies[0].state, "strike")
                game.press("attack")
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                self.assertEqual(grub.state, "recovery")
                self.assertAlmostEqual(grub.timer, 0.6, delta=0.01)
                self.assertEqual(len(last_attack(game)["hits"]), 1)
                self.assertIsNone(last_attack(game)["miss"])
                run(game, 1.0)
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
                self.assertGreaterEqual(peak, 1)

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


class CrowdTest(unittest.TestCase):
    """A1 wind-up spacing, the engagement cap and hit-stun (AC-19 to AC-22)."""

    def test_windup_spacing(self):  # AC-19
        for room in "125":
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    game = Game(fps=fps, room=room)
                    run(game, 12.0)
                    starts = sorted(times(game, "windup"))
                    self.assertGreaterEqual(len(starts), 2)
                    for a, b in zip(starts, starts[1:]):
                        self.assertGreaterEqual(b - a, 1.0 - tol(fps))

    def test_spacing_applies_between_grubs_only(self):
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "windup")
                run(game, 0.2)
                game.press("attack")  # interrupted: its next wind-up comes sooner than 1.0 s
                run(game, 3.0)
                starts = times(game, "windup")
                self.assertGreaterEqual(len(starts), 2)

    def test_engagement_cap(self):  # AC-20, AC-21
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="2")
                peak, saw_cap_wait = 0, False
                while game.t < 12.0 and game.phase == "playing":
                    game.step()
                    near = sum(
                        1 for e in game.enemies
                        if e.alive and math.hypot(e.x - game.x, e.y - game.y) <= 1.5 + 1e-9
                    )
                    peak = max(peak, near)
                    self.assertLessEqual(near, 2)
                    saw_cap_wait = saw_cap_wait or any(e.wait == "cap" for e in game.enemies)
                self.assertEqual(peak, 2)
                self.assertTrue(saw_cap_wait)
                hurts = times(game, "hurt")
                if len(hurts) >= 3:
                    self.assertGreaterEqual(hurts[2] - hurts[0], 1.9)

    def test_hit_stun_is_short(self):  # AC-22
        # The checks sit at 0.75 s and 0.85 s after the hit. run_to() stops at the first frame at or
        # after the time asked for, so "0.79" (the earlier value) lands on the 0.80 s frame, where the
        # invulnerability has correctly just ended. That was the test's mistake, not the build's.
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.spawn("grub", 8.5, 4)
                run_until(game, "hurt")
                hit = times(game, "hurt")[0]
                run(game, 0.05)
                game.press("attack")
                self.assertEqual(game.events[-1][2]["reason"], "stunned")
                run_to(game, hit + 0.25)
                swipes = len(times(game, "attack"))
                game.press("attack")
                self.assertEqual(len(times(game, "attack")), swipes + 1)
                run_to(game, hit + 0.75)
                self.assertTrue(game.invulnerable)
                run_to(game, hit + 0.85)
                self.assertFalse(game.invulnerable)


class SwipeTest(unittest.TestCase):
    def one_grub(self, gx, gy, facing=None, fps=60):
        game = Game(fps=fps, room="empty")
        game.place_player(8, 4)
        game.spawn("grub", gx, gy)
        if facing:
            game.press("move", facing)
            game.press("stop")
        return game

    def test_body_hit(self):  # AC-23
        for fps in FPS:
            with self.subTest(fps=fps, case="a"):
                game = self.one_grub(8.2, 4, fps=fps)
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, 1)
            for facing, gx in (("right", 7.6), ("left", 8.4)):
                with self.subTest(fps=fps, case="b", facing=facing):
                    game = self.one_grub(gx, 4, facing, fps)
                    game.press("attack")
                    self.assertEqual(game.enemies[0].hp, 1)
            for facing, gx in (("right", 7.2), ("left", 8.8)):
                with self.subTest(fps=fps, case="c", facing=facing):
                    game = self.one_grub(gx, 4, facing, fps)
                    game.press("attack")
                    self.assertEqual(game.enemies[0].hp, 2)
                    self.assertEqual(last_attack(game)["miss"], "not in front")

    def test_miss_wording(self):  # AC-27
        cases = (
            (10, 4, "too far", "you swipe: (miss) too far"),
            (8, 5, "not in front", "you swipe: (miss) not in front"),
            (8, 8, None, "you swipe: (miss)"),
        )
        for gx, gy, cause, line in cases:
            with self.subTest(gx=gx, gy=gy):
                game = self.one_grub(gx, gy)
                game.press("attack")
                self.assertEqual(last_attack(game)["miss"], cause)
                text = capture(f"room empty\nspawn grub {gx} {gy}\nplayer 8 4\n0 attack\nend 0.3\n")
                self.assertIn(line, [s for _, s in timed_lines(text)])
                self.assertIn(")", "".join(r for r in text.splitlines() if r.startswith("   |")))


class DashRulesTest(unittest.TestCase):
    def test_dash_sets_facing(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("move", "right")
        game.press("stop")
        game.press("dash", "left")
        run(game, 0.3)
        game.press("attack")
        self.assertEqual(last_attack(game)["facing"], "left")
        text = capture("room empty\nplayer 8 4\n0 move right\n0.1 stop\n0.3 dash left\n0.7 attack\nend 1\n")
        self.assertIn("(", "".join(r for r in text.splitlines() if r.startswith("   |")))

    def test_dash_without_direction_keeps_facing(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("move", "up")
        game.press("stop")
        game.press("dash")
        self.assertEqual(game.facing, (0, -1))

    def test_queued_attack_fires_in_dash_direction(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("dash", "down")
        run(game, 0.1)
        game.press("attack")
        run(game, 0.2)
        self.assertEqual(last_attack(game)["facing"], "down")

    def test_wall_dash_lasts_full_time_and_stays_invulnerable(self):  # AC-25
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                start = game.t
                game.press("dash", "left")
                while not times(game, "dash_end"):
                    self.assertTrue(game.invulnerable)
                    game.step()
                self.assertAlmostEqual(game.t - start, 0.25, delta=tol(fps))
                self.assertEqual(game.x, 0.0)

    def test_dash_right_ends_at_12(self):  # AC-25
        for fps in FPS:
            game = Game(fps=fps, room="empty")
            game.place_player(8, 4)
            game.press("dash", "right")
            run(game, 0.4)
            self.assertAlmostEqual(game.x, 12.0, delta=0.25)


class KnockbackTest(unittest.TestCase):
    """AC-28 (D-013, D-014)."""

    def swipe_on_tile(self, fps, px=8.0, side=None, at=0.2, gx=None):
        game = Game(fps=fps, room="empty")
        game.place_player(px, 4)
        game.spawn("grub", px if gx is None else gx, 4)
        if side:
            game.enemies[0].side = side
        run(game, at)
        game.press("attack")
        return game

    def test_on_tile_grub_steps_to_its_display_side(self):  # AC-28 (a)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps)
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                run(game, 0.25)
                self.assertAlmostEqual(grub.x, 9.0, delta=0.1)
                self.assertAlmostEqual(grub.y, 4.0, delta=0.1)
                game = self.swipe_on_tile(fps, side=(0, 1))
                run(game, 0.25)
                self.assertAlmostEqual(game.enemies[0].y, 5.0, delta=0.1)

    def test_grub_02_tile_away_ends_one_tile_on_its_shown_side(self):  # AC-28 (a), D-014
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps, gx=8.2, at=0.0)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertAlmostEqual(grub.x, 9.0, delta=0.1)
                self.assertAlmostEqual(math.hypot(grub.x - game.x, grub.y - game.y), 1.0, delta=0.1)
                _, _, entries = game.layout()
                self.assertEqual(entries, [])

    def test_blocked_side_uses_the_next_side(self):  # AC-28 (b)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps, px=14.5, side=(1, 0))
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertLessEqual(grub.x, 15.0)
                self.assertGreaterEqual(math.hypot(grub.x - game.x, grub.y - game.y), 0.9)
                self.assertLess(grub.x, game.x)

    def test_edge_grub_is_shown_and_knocked_left(self):  # AC-28 (b), AC-29 (c)
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(
                    f"room empty\nfps {fps}\nspawn grub 14.5 4\nplayer 14.5 4\nend 0.1\n"
                )
                draw = next(v for k, v in parse_session(text) if k == "draw")
                self.assertEqual(find(draw, "P"), [(15, 4)])
                self.assertEqual(find(draw, "gGwW"), [(14, 4)])
                self.assertIn("on you: g walking (shown left)", text)
                self.assertNotIn("(shown right)", text)
                game = self.swipe_on_tile(fps, px=14.5)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertAlmostEqual(grub.x, 13.5, delta=0.1)
                pc, placed, entries = game.layout()
                self.assertEqual(pc, (15, 4))
                self.assertEqual(placed[id(grub)], (14, 4))
                self.assertEqual(entries, [])
                run(game, 2.0)
                words = [d["side"] for t, k, d in game.events if k == "windup" and t > 0.3]
                self.assertTrue(words)
                self.assertTrue(all(w == "left" for w in words), words)
                hits = [d["pos"] for _, k, d in game.events if k == "hurt"]
                self.assertTrue(all(h in ("on you", "left") for h in hits), hits)

    def test_slots_and_distance(self):  # AC-28 (c)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertLess(math.hypot(grub.x - game.x, grub.y - game.y), 1.5)
                far = Game(fps=fps, room="empty")
                far.place_player(8, 4)
                far.spawn("grub", 9.4, 4)
                far.press("attack")
                run(far, 0.2)
                g = far.enemies[0]
                self.assertGreaterEqual(math.hypot(g.x - far.x, g.y - far.y), 1.5)

    def test_knockback_keeps_timers(self):  # AC-28 (d)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "recover")
                run(game, 0.2)
                before = game.enemies[0].timer
                game.press("attack")
                self.assertEqual(game.enemies[0].state, "recovery")
                self.assertAlmostEqual(game.enemies[0].timer, before, delta=1e-9)

    def test_result_line_has_no_on_you(self):  # AC-28 (e), V-9, V-17
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\n0.2 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: grub hit (1 left)", lines)
        self.assertFalse(any(s.startswith("you swipe") and "(on you)" in s for s in lines))
        self.assertIn("on you: g walking (shown right)", text)
        last_draw = text.rsplit("hearts", 2)[-1]
        self.assertNotIn("on you:", last_draw)


class CellRuleTest(unittest.TestCase):
    """D-014: AC-29 (cell at an exact half tile) and AC-30 (one meaning of the words)."""

    def test_half_tile_cells(self):  # AC-29
        self.assertEqual([cell1(v) for v in (13.5, 14.5, 8.5, 7.5)], [14, 15, 9, 8])
        self.assertEqual(cell1(14.496), 15)
        self.assertEqual(cell1(14.49), 14)
        self.assertEqual(cell1(14.5 - 1e-12), 15)  # float noise at .5 does not matter
        self.assertEqual(cell1(14.5 + 1e-12), 15)
        self.assertEqual(cell1(13.5 - 1e-12), 14)

    def test_grub_resting_on_a_half_tile_is_drawn_left(self):  # AC-29 (a)
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(
                    f"room empty\nfps {fps}\nspawn grub 13.5 4\nplayer 14.5 4\nend 0.4\n"
                )
                draws = [v for k, v in parse_session(text) if k == "draw"]
                self.assertGreaterEqual(len(draws), 2)
                for rows in draws:
                    self.assertEqual(find(rows, "P"), [(15, 4)])
                    self.assertEqual(find(rows, "gGwW"), [(14, 4)])
                self.assertIn("a grub rears back (left)", [s for _, s in timed_lines(text)])
                self.assertNotIn("on you:", text)

    def test_one_tile_either_side_of_8_5(self):  # AC-29 (b)
        for fps in FPS:
            for gx, word in ((9.5, "right"), (7.5, "left")):
                with self.subTest(fps=fps, gx=gx):
                    text = capture(
                        f"room empty\nfps {fps}\nspawn grub {gx} 4\nplayer 8.5 4\nend 0.4\n"
                    )
                    self.assertIn(f"a grub rears back ({word})", [s for _, s in timed_lines(text)])
                    self.assertNotIn("on you", text)

    def test_shared_cell_beyond_half_tile_is_not_on_you(self):  # AC-30 (b)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8.4, 4)
                game.spawn("grub", 7.8, 4)
                grub = game.enemies[0]
                pc, placed, entries = game.layout()
                self.assertEqual(entries, [])
                self.assertEqual(game._pos(grub), "left")
                self.assertEqual(placed[id(grub)], (pc[0] - 1, pc[1]))
                game.press("attack")  # facing right by default
                self.assertEqual(last_attack(game)["miss"], "not in front")
                self.assertEqual(grub.hp, 2)
                text = capture(
                    f"room empty\nfps {fps}\nspawn grub 7.8 4\nplayer 8.4 4\nend 0.4\n"
                )
                self.assertNotIn("on you", text)

    def test_words_match_the_picture_every_tick(self):  # AC-30 (a), (c), V-18
        for fps in FPS:
            for room, extra in (("2", None), ("1", None), ("empty", (8, 4, 8.2, 4))):
                with self.subTest(fps=fps, room=room):
                    game = Game(fps=fps, room=room)
                    if extra:
                        game.place_player(extra[0], extra[1])
                        game.spawn("grub", extra[2], extra[3])
                    for _ in range(round(6 * fps)):
                        game.step()
                        pc, placed, entries = game.layout()
                        names = {id(e) for e, _ in entries}
                        for e in game.enemies:
                            if not e.alive:
                                continue
                            word = game._pos(e)
                            near = math.hypot(e.x - game.x, e.y - game.y) <= 0.5 + 1e-6
                            self.assertEqual(word == "on you", near)
                            self.assertEqual(near, id(e) in names)
                            if not near:
                                self.assertEqual(word, cell_word(pc, placed[id(e)]), (game.t, e.index))
                        for e, side in entries:
                            c = placed[id(e)]
                            self.assertEqual((c[0] - pc[0], c[1] - pc[1]), side)
                            self.assertTrue(0 <= c[0] < 16 and 0 <= c[1] < ROOM_H)

    def test_line_words_match_the_next_draw(self):  # AC-30 (c), V-18
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(f"room 2\nfps {fps}\nend 6\n")
                pending, checked = [], 0
                for kind, val in parse_session(text):
                    if kind == "line":
                        m = re.match(r"a grub rears back \((.+)\)$", val)
                        if m:
                            pending.append((m.group(1).split(",")[0], "GW"))
                        m = re.match(r"the grub is open \((.+)\)$", val)
                        if m:
                            pending.append((m.group(1).split(",")[0], "gw"))
                        continue
                    pcell = find(val, "Px")[0]
                    for word, chars in pending:
                        if word == "on you":
                            continue
                        words = {cell_word(pcell, c) for c in find(val, chars)}
                        self.assertIn(word, words, (word, val))
                        checked += 1
                    pending = []
                self.assertGreaterEqual(checked, 3)

    def test_hit_word_is_the_strike_start_word(self):  # AC-30 (d)
        seen = {}
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="2")
                run(game, 7.0)
                last, words = {}, []
                for _, kind, d in game.events:
                    if kind == "windup":
                        last[d["who"]] = d["side"]
                    elif kind == "hurt" and d["source"] == "grub":
                        self.assertEqual(d["pos"].split(",")[0], last[d["who"]].split(",")[0])
                        words.append(d["pos"].split(",")[0])
                self.assertGreaterEqual(len(words), 3)
                seen[fps] = words
        self.assertEqual(seen[30], seen[60])

    def test_hit_word_names_the_grub_that_struck(self):  # AC-30 (e), V-14
        for fps in FPS:
            for order, word in (((9.25, 6.75), "right"), ((6.75, 9.25), "left")):
                with self.subTest(fps=fps, word=word):
                    game = Game(fps=fps, room="empty")
                    game.place_player(8, 4)
                    for gx in order:
                        game.spawn("grub", gx, 4)
                    run(game, 1.0)
                    first = [d for _, k, d in game.events if k == "hurt"][0]
                    self.assertEqual(first["pos"], word)


class OnYouLineTest(unittest.TestCase):
    def test_line_present_only_while_on_tile(self):  # V-9, V-10
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\nend 1.2\n")
        self.assertRegex(text, r"(?m)^on you: [gG] [a-z ]+ \(shown (left|right|above|below)\)$")
        text = capture("room empty\nspawn grub 12 4\nplayer 8 4\nend 0.4\n")
        self.assertNotIn("on you:", text)

    def test_line_matches_the_picture(self):  # V-10
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\nend 4\n")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"on you: (\w) ([a-z ]+) \(shown (\w+)\)", line)
            if not m:
                continue
            glyph, word, side = m.groups()
            rows = [l[4:-1] for l in lines[i + 1 : i + 2 + ROOM_H] if l.startswith("   |")]
            (pc, pr), = find(rows, "Px")
            dc, dr = {"left": (-1, 0), "right": (1, 0), "above": (0, -1), "below": (0, 1)}[side]
            self.assertEqual(rows[pr + dr][pc + dc], glyph)
            self.assertEqual(glyph.isupper(), word == "biting soon")

    def test_hit_line_names_the_attacker(self):  # V-13, V-14
        text = capture("room empty\nspawn grub 12 4\nplayer 8 4\nend 3\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a grub (right)") for s in lines), lines)
        text = capture("room empty\nspawn grub 4 4\nplayer 8 4\nend 3\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a grub (left)") for s in lines), lines)

    def test_shot_hit_line_names_the_spitter(self):  # V-13
        text = capture("room empty\nspawn spitter 13 4\nplayer 8 4\nend 5\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a spit shot from spitter (") for s in lines), lines)


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

    def test_real_neighbour_versus_displaced(self):  # V-11
        text = capture("room empty\nspawn grub 8 4\nspawn grub 9 4\nplayer 8 4\nend 0.1\n")
        on_you = [l for l in text.splitlines() if l.startswith("on you:")]
        self.assertTrue(on_you)
        self.assertEqual(on_you[0].count("("), 1)

    def test_down_player_keeps_x_and_enemy_beside(self):  # AC-18
        game = Game(room="empty")
        game.place_player(8, 4)
        game.spawn("grub", 8.0, 4)
        down(game)
        out = play.Player(game)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out.start()
        self.assertNotIn("on you:", buf.getvalue())
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
                run(game, 0.32)  # the hit-stun (0.15 s) has passed
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

    def test_room_2_same_wind_up_order_at_both_rates(self):  # AC-17
        a, b = Game(fps=30, room="2"), Game(fps=60, room="2")
        run(a, 6.0)
        run(b, 6.0)
        wa = [d["who"] for _, k, d in a.events if k == "windup"]
        wb = [d["who"] for _, k, d in b.events if k == "windup"]
        self.assertEqual(wa, wb)


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

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 1 (0.2 s). Output:

```text
.............................................EE........................
======================================================================
ERROR: test_manual_lists_glyphs_and_lines (test_game.ManualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 1130, in test_manual_lists_glyphs_and_lines
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
  File "/work/tests/test_game.py", line 1140, in test_on_screen_section_lists_x_and_the_practice_room
    text = MANUAL.read_text(encoding="utf-8")
  File "/usr/lib/python3.10/pathlib.py", line 1134, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
  File "/usr/lib/python3.10/pathlib.py", line 1119, in open
    return self._accessor.open(self, mode, buffering, encoding, errors,
FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'

======================================================================
FAIL: test_line_words_match_the_next_draw (test_game.CellRuleTest) (fps=30)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 620, in test_line_words_match_the_next_draw
    self.assertGreaterEqual(checked, 3)
AssertionError: 2 not greater than or equal to 3

======================================================================
FAIL: test_line_words_match_the_next_draw (test_game.CellRuleTest) (fps=60)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 620, in test_line_words_match_the_next_draw
    self.assertGreaterEqual(checked, 3)
AssertionError: 2 not greater than or equal to 3

======================================================================
FAIL: test_edge_grub_is_shown_and_knocked_left (test_game.KnockbackTest) (fps=30)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 476, in test_edge_grub_is_shown_and_knocked_left
    self.assertTrue(all(w == "left" for w in words), words)
AssertionError: False is not true : ['left', 'on you']

======================================================================
FAIL: test_edge_grub_is_shown_and_knocked_left (test_game.KnockbackTest) (fps=60)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 476, in test_edge_grub_is_shown_and_knocked_left
    self.assertTrue(all(w == "left" for w in words), words)
AssertionError: False is not true : ['left', 'on you']

----------------------------------------------------------------------
Ran 73 tests in 0.170s

FAILED (failures=4, errors=2)
```

### Round 1: @run/trace/ac28b-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
player 14.5 4
spawn grub 14.5 4
0.2 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.233 frame=7 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.33,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'on you'}; knockback {'who': 0, 'on_tile': True}
t=0.800 frame=24 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=1.300 frame=39 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=1.333 frame=40 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(13.72,4.00,hp=1,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left', 'who': 0}
t=1.467 frame=44 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(14.50,4.00,hp=1,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.000 frame=60 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=1,recovery,0.350) | end
```

### Round 1: @run/trace/ac28b-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 14.5 4
spawn grub 14.5 4
0.2 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.217 frame=13 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.42,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'on you'}; knockback {'who': 0, 'on_tile': True}
t=0.800 frame=48 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=1.300 frame=78 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=1.317 frame=79 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(13.61,4.00,hp=1,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left', 'who': 0}
t=1.450 frame=87 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(14.50,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.000 frame=120 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.117 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=1,recovery,0.350) | end
```

### Round 1: @run/trace/ac29a-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
player 14.5 4
spawn grub 13.5 4
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=0.533 frame=16 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(13.72,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left', 'who': 0}
t=0.700 frame=21 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(14.50,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=1.000 frame=30 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,recovery,0.583) | end
```

### Round 1: @run/trace/ac29a-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
player 14.5 4
spawn grub 13.5 4
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=0.517 frame=31 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(13.61,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left', 'who': 0}
t=0.667 frame=40 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(14.50,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=1.000 frame=60 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,recovery,0.567) | end
```

### Round 1: @run/trace/ac30-room2-30 — `python3 play.py --view trace {script}`

Script:

```text
room 2
fps 30
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=2 dt=0.03333
t=0.000 frame=0 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.00,1.00,hp=2,approach,0.000) grub#1(15.00,7.00,hp=2,approach,0.000) grub#2(14.00,0.00,hp=2,approach,0.000) grub#3(1.00,8.00,hp=2,approach,0.000) | setup
t=2.733 frame=82 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,windup,0.500) grub#1(9.98,4.85,hp=2,approach,0.000) grub#2(9.45,3.03,hp=2,approach,0.000) grub#3(5.75,5.29,hp=2,approach,0.000) | windup {'who': 0, 'side': 'top left'}
t=3.233 frame=97 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=3.300 frame=99 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.28,3.64,hp=2,strike,0.083) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'top left', 'who': 0}
t=3.400 frame=102 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.883) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=3.733 frame=112 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.550) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.500) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 2, 'side': 'top right'}
t=4.100 frame=123 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.183) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.133) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.233 frame=127 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.050) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,strike,0.150) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 2}
t=4.300 frame=129 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.67,3.55,hp=2,strike,0.083) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'top right', 'who': 2}
t=4.400 frame=132 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.883) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 2, 'side': 'on you'}
t=4.733 frame=142 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.500) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.550) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 0, 'side': 'on you'}
t=5.100 frame=153 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.133) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.183) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.233 frame=157 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.050) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=5.267 frame=158 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.83,3.91,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0, 'pos': 'on you', 'who': 0}; down
t=6.000 frame=180 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.067 stun_left=0.000 shots=0 | grub#0(7.83,3.91,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | end
```

### Round 1: @run/trace/ac30-room2-60 — `python3 play.py --view trace {script}`

Script:

```text
room 2
fps 60
end 6
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=2 dt=0.01667
t=0.000 frame=0 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.00,1.00,hp=2,approach,0.000) grub#1(15.00,7.00,hp=2,approach,0.000) grub#2(14.00,0.00,hp=2,approach,0.000) grub#3(1.00,8.00,hp=2,approach,0.000) | setup
t=2.733 frame=164 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,windup,0.500) grub#1(9.98,4.85,hp=2,approach,0.000) grub#2(9.45,3.03,hp=2,approach,0.000) grub#3(5.75,5.29,hp=2,approach,0.000) | windup {'who': 0, 'side': 'top left'}
t=3.233 frame=194 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=3.283 frame=197 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.18,3.59,hp=2,strike,0.100) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'top left', 'who': 0}
t=3.383 frame=203 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.900) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=3.733 frame=224 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.550) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.500) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 2, 'side': 'top right'}
t=4.083 frame=245 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.200) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.150) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.233 frame=254 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.050) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,strike,0.150) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 2}
t=4.283 frame=257 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.76,3.49,hp=2,strike,0.100) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'top right', 'who': 2}
t=4.383 frame=263 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.900) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 2, 'side': 'on you'}
t=4.733 frame=284 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.500) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.550) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 0, 'side': 'on you'}
t=5.083 frame=305 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.200) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.233 frame=314 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.050) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=5.250 frame=315 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.80,3.90,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0, 'pos': 'on you', 'who': 0}; down
t=6.000 frame=360 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.050 stun_left=0.000 shots=0 | grub#0(7.80,3.90,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | end
```
>>>END
