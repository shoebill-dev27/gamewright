# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/61-studio-to-gameplay-engineer.md
next_seq: 63
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/63-gameplay-engineer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/61-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 61
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 61: studio → gameplay-engineer — Build the combat spec update (AC-19…AC-27) and the "on you" / hit-source display (V-9…V-17)

## Task

Change the game in `repo/` per the current `design/combat.md` (designer's update in 59, with D-011) and the visual spec in `design/combat-visuals.md` (V-9…V-17, D-012). Add or update tests. Run the suite and report. Stop and hand back on any ambiguity; do not decide rules.

## Context

G-001 (combat monotony), Option A (D-002, D-004: reuse existing systems, one sequential change set). Earlier rounds found the fights repeat the same pattern and confusing in rooms 1 and 2. The designer's spec (59) and the art director's display spec (60) are now both ready. Build 0.4 is the current state. After you, QA verifies AC-1…AC-27 at 30 and 60 FPS.

## Findings

From the design (59, `design/combat.md`, D-011; read the file, it is authoritative):
- Wind-up spacing and an engagement cap: grubs take turns and crowd two deep.
- Hit-stun 0.15 s; a body hit rule; a dash sets facing and has an edge stop.
- Swipe has Strike and Recovery phases; a hit in Strike cancels it (settles D-58-1).
- Miss wording ("(miss)").
- AC-19…AC-27 are the new acceptance criteria.

From QA (58): there is no short bite warning (the "rears back" line belonged to another grub). A dash covers 4.00 tiles at 30 and 60 FPS. A dash sets facing. A grub "on you" is hit in all facings. Bot format and idle/bot reference data are in 58.

From the visual spec (60, `design/combat-visuals.md`): an `on you:` line under the hearts while an enemy shares the player's tile; attacker position in hit lines (`YOU ARE HIT by a grub (left)`, `(on you)`); the same position words in "is open" lines; inverse video for a displaced cell in a color view. These are display and text only.

## Decisions already made

- D-001: attack, dash and pause are the only buttons.
- D-002 / D-004: rework existing enemy behavior first; one sequential change set.
- D-006: enemies may overlap the player but are never hidden.
- D-011: grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line and attacker position in hit lines.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Reuse existing systems; no new input buttons.
- Do not edit `manual.md`. The Owner places manual text (D-005, D-007 pattern; step 62 is open in parallel). `ManualTest` (AC-15) may therefore fail or be blocked in your workspace, because the manual is not beside `repo/`. Report that result as it is; do not change the test or the manual to make it pass.
- Orange/red only for telegraphed glyphs and projectiles; on-you and hit lines are lantern-colored.

## Open questions

- Does the hit event know which grub dealt the damage and where it was when the hit landed (V-13, V-14)? If only the trace knows, say so.
- Can the player view print the extra `on you:` line and an inverse-video cell? If not, the line alone meets V-9…V-11.
- Knockback direction of a grub exactly on the player's tile is not covered by the spec (58). If `design/combat.md` does not cover it, hand back to `game-designer` through `studio`; do not choose.
- 59 asks for a report on the Waiting behavior of a blocked grub: is it local to existing systems? If not, say so and hand back for a technical plan (`technical-director`).
- Does a swipe that hits an on-tile grub print "(on you)" in its result line? The spec makes no claim; if the lines are ambiguous, ask the designer.

## Expected output

- The changed game, tests, and build notes: what changed, how to run it, and the full `run_tests` result.
- The answers to the open questions above and the Waiting-behavior report.
- Address the result to `studio` (QA verifies without your reasoning; keep your self-assessment under `## Sender assessment`).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-visuals.md, manual.md (read only), repo/ (run commands in project.md: run_tests, run_play, run_trace, run_bots)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/60-art-director-to-studio.md (also read goals/G-001-combat-monotony/58-qa-to-studio.md and goals/G-001-combat-monotony/59-game-designer-to-studio.md)
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

<<<FILE design/combat.md
# Combat design (build 0.5 target — Option A, G-001)

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text. Updated after QA's second round (handoff 29): overlap rule and AC-15 wording (D-006). Updated after playtests 50 and 54 (handoff 59): grub spacing and engagement cap, shorter hit-stun, body-hit rule, dash and facing rules, swipe cases, miss wording (D-011). Acceptance criteria AC-19 to AC-27 are new.

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
  - Rulings in "Attack feedback" below.
- **Facing:** movement sets facing to the movement direction. The player cannot turn without moving or dashing (D-001; see D-011 on why this is held).
- **Dash**: up to 4 tiles over 0.25 s, invulnerable for the full dash. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends. The dash passes through enemies and projectiles without harm.
  - **Dash direction:** `dash <dir>` goes in that direction. A dash without a direction goes the way the player faces.
  - **Dash and facing (A5):** a dash sets facing to the dash direction, like movement does. A queued attack fires in that direction. A dash without direction leaves facing unchanged.
  - **Dash and walls (A5):** a dash that would leave the room stops at the room edge; it is never cancelled. Distance dashed is the shorter of 4 tiles and the distance to the edge. It still takes 0.25 s at 4 tiles and proportionally less for a shorter dash is not required: the duration is 0.25 s in all cases and the invulnerability covers all of it.
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
| Waiting | until allowed | The grub is in range but blocked by the spacing rule or the engagement cap below. It stands still or holds position, harmless, normal glyph `g`/`w`. No text line. |
| Wind-up | 0.5 s **[tune]** | Starts when the grub is within 1.25 tiles of the player and the rules below allow it. The grub stops, and its glyph and color change (see "Feedback"). A text line "a grub rears back" prints. It deals no damage. |
| Strike | 0.15 s | A short lunge of up to 1 tile toward where the player stood when the wind-up ended. It damages the player once (1 heart) if the player is within 1.0 tile of the grub at any moment of the strike and is not invulnerable. |
| Recovery | 0.9 s **[tune]** | The grub stands still, "open". No damage. Its normal glyph returns. |

- Cycle with a player standing still: 0.5 + 0.15 + 0.9 = about 1.55 s per bite.
- **Wind-up spacing (A1):** a grub may not start a Wind-up within **1.0 s [tune]** of the start of any other grub's Wind-up (a cancelled or defeated grub's wind-up start still counts). A grub that is blocked becomes Waiting. When the window ends, the nearest Waiting grub starts first; ties go to the grub that has waited longest. With one grub in the room the rule has no effect. A grub's own cycle is unchanged.
- **Engagement cap (second rule, D-011):** at most **2** grubs may be within 1.5 tiles of the player at once, counted in every state, by true position. A grub that has reached 2.0 tiles from the player while two grubs are inside 1.5 tiles becomes Waiting at that distance and enters when a slot frees (a grub is defeated, or is knocked back or pushed out beyond 1.5 tiles). The nearest waiting grub enters first. A waiting grub follows a moving player so that it stays at 2.0 tiles or more. The cap limits where grubs move; it does not stop the player from walking or dashing next to more grubs, because there is no collision.
- **Attack limit (kept):** at most 2 grubs may be in Wind-up or Strike at the same time. With the 1.0 s spacing this is nearly always at most 1, but the limit is kept as a backstop.
- **Player hits on a grub:**
  - First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s and shows the damaged state.
  - A hit during Wind-up cancels the wind-up. The grub goes straight into a 0.6 s Recovery and does not strike.
  - **A hit during Strike (A5)** cancels the rest of the strike: if the strike has not yet damaged the player in that tick or earlier, no heart is lost. The grub goes into a 0.6 s Recovery. Player attacks resolve before enemy damage in each tick (same order as room clear).
  - A hit during Recovery or Approach/Waiting: damage and knockback as above; Recovery continues for its remaining time.
  - Second hit: the grub is defeated.
- Grubs never damage the player outside Strike, so the dash and spacing are the answers: step back, or dash through the wind-up, then counter in Recovery. Hitting a winding-up grub (interrupt) is the best answer.

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
- **Grub knocked out of the engagement zone:** it frees a slot at once; it is Approach again and may be Waiting if the cap is full when it returns.
- **Player dashes through a grub in Wind-up:** the grub still completes its Wind-up, Strike (toward where the player stood when the wind-up ended) and Recovery; its strike misses if the player is more than 1.0 tile away.
- **Swipe at the same tick as a strike's damage:** the swipe resolves first (see "Player hits on a grub").
- **Dash into a wall or into the room edge:** stops at the edge, see Dash.
- **Spitter Charge canceled by a hit:** the projectile is not fired.
- **Enemy on the player's tile:** see "Overlap with the player". It is drawn beside `P`; the body-hit rule means a swipe always hits it.
- **Player down while an enemy shares the cell:** `x` is drawn on the player's cell and the enemy keeps its displaced cell.
- **Pause:** all timers freeze.

## 30 / 60 FPS (Q5)

- Every timer above runs on elapsed seconds, not frame counts. This includes the spacing window (1.0 s), the dash duration and the hit-stun (0.15 s).
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
- **AC-17 Frame rate:** AC-1…AC-14 and AC-18…AC-27 pass at both frame rates, and the 30/60 comparison above holds.
- **AC-18 No hidden enemy:** in the practice room with an idle player and one grub at distance 4, run to 5.5 s, every draw that shows a living grub has a grub glyph in a cell different from the player's cell. Every "a grub rears back" line, including those marked "(on you)", comes with an uppercase `G` or `W` visible on the map in the draw made at that moment. Same for "the grub is open (on you)": a lowercase `g` or `w` is visible. Also, with `player 8 4` and `spawn spitter 8.2 4`, the draws show `P` and an `s` in a neighbouring cell; the spitter's `S` is visible beside `P` during its Charge. The trace shows no change to timings, hearts or positions compared with a build without the display rule (the events of AC-1…AC-4 stay within tolerance).
- **AC-19 Wind-up spacing (A1):** in room 2 with a still player, run to 12 s (or until down): for every pair of grub Wind-up starts in the trace, the later one is at least 0.96 s after the earlier one at 60 FPS and 0.92 s at 30 FPS (1.0 s minus tolerance), whichever grubs they belong to. The same holds in room 1 and room 5. A room with a single grub shows the AC-2 cycle unchanged.
- **AC-20 Engagement cap:** in room 2 with a still player at x 8, y 4, the trace shows at no sample more than 2 grubs within 1.5 tiles of the player, from the start to the end of the run. The remaining grubs are present in the draws at about 2.0 tiles with lowercase glyphs and no "rears back" line until a slot frees.
- **AC-21 Turns, not a ring:** in room 2 with a still player, the time between the first and the third heart lost is at least 1.9 s. No two Wind-up starts fall within 1.0 s (AC-19), so the trace shows at most one grub in Wind-up or Strike at any sample.
- **AC-22 Hit-stun:** after a heart is lost, an attack pressed 0.05 s later prints "(stunned)" and does nothing. An attack pressed 0.25 s later swipes normally. A dash behaves the same way (subject to its cooldown). The stun lasts 0.15 s within tolerance. Invulnerability still ends 0.8 s after the hit.
- **AC-23 Body hit (A3):** in the practice room, with `player 8 4` and `spawn grub 8.2 4` (no movement before the swipe, so facing is the default), a swipe hits the grub ("grub hit (1 left)"), whatever the facing. With the player moved to face the opposite direction first (move away 0.3 s then back is not needed: use `move left` then `stop`, and again with `move right`), the swipe still hits a grub placed at 0.4 tile behind. A grub at true distance 0.8 tile behind the player is not hit and prints "(miss) not in front".
- **AC-24 Dash and facing (A5):** in the practice room, `player 8 4`, face right (move right then stop), then `dash left`, then an attack after the dash: the arc is drawn as `(` (facing left). A `dash` without a direction while facing up leaves facing up. A queued attack pressed during a dash fires after it ends in the dash direction.
- **AC-25 Dash distance (A5):** in the practice room from `player 8 4`, `dash right` ends at 12.0 ± 0.25 on x at both frame rates and takes 0.25 s within tolerance. From `player 2 4`, `dash left` ends at the room edge (x 0, never outside the room) and the player takes no damage during it. Dash during the cooldown prints "(dash not ready)" and does nothing.
- **AC-26 Swipe during Strike and Recovery (A5):** with one grub in the practice room, a swipe pressed while the trace shows the grub in Strike hits it ("grub hit (1 left)") and no heart is lost to that strike if the swipe's tick comes at or before the damage tick. A swipe pressed while the grub is in Recovery and adjacent in front hits it. Neither case prints "(miss)".
- **AC-27 Miss wording (A5):** a swipe with a grub 2.0 tiles in front prints "(miss) too far". A swipe with a grub at 1.0 tile directly to the side (outside the cone) prints "(miss) not in front". A swipe with nothing within 2.5 tiles prints "(miss)" alone. All three also draw the arc.

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A playtester can say, unprompted, what a grub is about to do before it bites, and describes a reason to move or dash.
- A playtester reacts to a projectile at least once (moves, dashes or approaches a spitter) and can tell the two spitters apart.
- Rooms 4 and 5 are described as different from each other and from rooms 1–3 by what the player does, not only by enemy count.
- The playtester can tell from the screen how many hits an enemy needs.
- Grubs are neither trivial nor unfair: the playtester takes some damage in rooms 4–5 but can explain how it happened. (If grubs read as trivial, or the dash seems unnecessary, retune within D-001.)
- A playtester who stands still can see on the map where the grub that bites them is, including when it is right on top of them.
- A playtester in room 2 does not describe being boxed in by grubs on both sides with no way out.
- A playtester does not say they could not hit a grub that was next to or on them (A3).
- Observed in QA captures (no ruling): an idle player went to zero hearts at about 5.0 s in the practice room and in room 1 before these changes. That is expected for a player who does nothing. After A1 and the engagement cap the idle time to down is expected to be a little different; it is a reference value, not a target. Retune the **[tune]** values from live play.

### Retest guideline (design-side; for the next Play and Review, qualitative)

What a skilled player should be able to do. Numbers belong only in the acceptance criteria above.

- **Room 1 (3 grubs):** a skilled player who reads the cues can clear it and normally keeps most of their hearts. Damage comes from a misread cue or a mistimed dash, not from a bite they could not avoid. They can answer a rear-back by stepping out, by dashing through, or by hitting the winding-up grub, and then punish the open grub. After a hit they can swipe again quickly. A grub right on them can be hit.
- **Room 2 (4 grubs):** a skilled player can break the ring: only two grubs crowd them, bites come one at a time with a gap, and they can dash out to a side or a wall and fight the nearest grub from a free line. The room should still be a real fight where taking a hit or two is plausible, but a player who tries should clear it, usually with at least one heart left. A player who stands still loses; that is meant.
- Judge sameness only on a survived run. A player who cannot clear room 1 or 2 says nothing yet about monotony (see 53 and 54).
- Report from the retest, because they decide the held items: (1) swipes that print "(miss) not in front" while the player aimed at that grub (A4); (2) swipes aimed after a dash that hit air (facing, D1); (3) whether four grubs still arrive as one clump that feels like a wall (D2 / Option B).

## Held back or rejected (see D-011)

- **A4 cone width 90° → about 120°:** held. It comes in if the retest shows that the "(miss) not in front" line appears on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or that testers report missing grubs standing diagonally in front after A3 is in. Then widen to 120° **[tune]** and add its AC.
- **D1 facing mechanic (turn without moving, auto-face, backstep dash, 360° swipe):** not taken. It goes to `game-director` only if the retest still reports swipes into air after dashes or turning trouble with A3 and the dash-facing rule in.
- **D2 room 1 composition (fewer grubs, staggered arrival):** not taken. A1 and the cap give the intended effect inside Option A.

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director. The art-director may review the choice of the displaced cell for readability (see D-006).
- The as-built dash distance and the facing behavior after a dash are being checked by QA (55). Where the build differs from the rules above, the rules above stand and QA's result becomes a defect, unless QA shows a rule cannot be built.
- Whether the run has any progression after "run over" is outside this spec.

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

<<<FILE goals/G-001-combat-monotony/60-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 60
from: art-director
to: studio
stage: Build
outcome: done
---
# 60: art-director → studio — Visual spec for "on you" and "which grub hit you" (V-9 to V-17)

## Task

Route the visual spec in `design/combat-visuals.md` (new items V-9 to V-17) to Build with the designer's spec change from 56, then to Verify. The display must show when a grub is on the player's tile and which grub dealt a hit.

## Context

G-001 (combat monotony), Option A. Two playtesters in two sessions reported the same two confusions (from 57 and the report in 54):
- A grub on the player's tile ("the grub is open (on you)") is drawn beside the player (D-006), and the player could not tell which side the bite would come from or where to swing.
- "YOU ARE HIT by a grub" does not say which grub when several are around. Rooms 1 and 2 often have two to four close together.

The capital and lowercase marks and the "rears back (left)" lines were praised. They are kept unchanged.

## Findings

What the spec adds (all display and text; no rule, timing or parameter changed):

1. **`on you:` line** under the hearts, present only while an enemy shares the player's tile. It lists each such enemy with its glyph, a state word (`walking`, `biting soon`, `open`, `charging`, `idle`) and the cell it is drawn in, for example `on you: G biting soon (shown right)`. It answers the first open question: the displaced glyph is marked by text, and a reverse-video cell reinforces it in a color view. No glyph changes.
2. **Position in hit lines**: `YOU ARE HIT by a grub (left)`, `... (on you)`, or `... by a spit shot from spitter (top right)`. It answers the second open question. It uses the same position words as the existing lines. A distance in tiles is added only when two enemies of the same type would get identical words.
3. **Same position words for the "is open" line**: "the grub is open (left)", "(on you)".
4. **Order and timing**: no new draws beyond the existing principle 4; the on-you line and the hit position come from the state of the draw that prints them. They hold at 30 and 60 FPS.
5. **D-012** records the choice. D-006 is not reversed.

The spec's wording makes no claim about which enemies a swipe hits, so it stays valid whatever swipe rule 56 settles. Only the swipe result lines depend on that rule, and this spec leaves them unchanged.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; display offset only. Stands.
- D-012: `on you:` line and attacker position in hit lines (new, art-director).

## Constraints

- Visual and text changes only. If Build finds that naming the attacker needs a rule or timing change, hand back to `game-designer`.
- `manual.md` is not written by the art-director or by Build. The Owner places manual text (D-005, D-007 pattern); the Studio routes the V-15 text (`manual.md#on-screen`, `manual.md#what-you-hear-and-read`) to the Owner (62). (Corrected by the Studio at Route; the original said Build updates `manual.md`.)
- Art direction: orange/red only for telegraphed glyphs and projectiles. The on-you line text and the hit lines are lantern-colored, not orange/red. Only the glyph letter inside the on-you line uses its glyph color.

## Open questions

- **For Build:** Does the hit event know which grub dealt the damage, and where it was when the hit landed? V-13 and V-14 need that. If it is only known in the trace and not in the player-view event, say so; it is a Build question, not a rule change.
- **For Build:** Can the player view print one extra line under the hearts and give a displaced cell inverse video? If a plain view cannot, the line alone still meets V-9 to V-11.
- **For `game-designer` (informational):** the swipe rule in 56 should be reflected in the swipe result lines only. If a swipe that hits an on-tile grub should print "(on you)" in its line, the designer should say so; the visual spec does not require it.
- **For `qa`:** The possibly short bite warning at 11.90 s to 11.97 s in report 54 is not a visual issue. The new hit lines will help trace which grub it was.

## Expected output

- Build: implement V-9 to V-17 in the player view with the designer's spec. `manual.md` is placed by the Owner, not by Build.
- Verify (`qa`): check V-9 to V-17 by scripted sessions in the practice room, for example `player 8 4` with `spawn grub 8 4`, and a grub on the left and right with only one striking, at both `fps 30` and `fps 60`.
- Review: the experience signals at the end of the "Experience signals" section in `design/combat-visuals.md`. A visual review of the built view is still needed for the real colors.

## Sender assessment

I am fairly confident in the text-line approach. It is cheap, testable from the plain view and independent of the swipe rule. The least certain parts are whether a single `on you:` line stays readable with three or more enemies on the tile, and whether the hit event can name the attacker. Both are listed as open and are cheap to settle in Build.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-visuals.md, design/combat.md, manual.md, the build `repo/`
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/57-studio-to-art-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/58-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 58
from: qa
to: studio
stage: Observe
outcome: done
---
# 58: qa → studio — Six open facts settled (two partly); one low-severity contradiction, no short bite warning

## Task

Pass this report to `game-designer` for the spec gaps listed below and to `gameplay-engineer` if the designer rules on D-58-1. The build was not changed. All findings come from the trace and player views and the bot runs, at 60 FPS and 30 FPS unless noted.

## Context

G-001, handoff 55. I used two run rounds: 5 runs in the first and 17 in the second (labels in brackets below). I have one round left and did not use it. Items 4 and 5 are only partly settled; see "Not settled".

## Findings

### Summary

| # | Fact | Result | Against spec |
|---|---|---|---|
| 1 | Short bite warning | Not real. The "rears back" line belonged to a different grub. | Matches |
| 2 | Dash distance | 4.00 tiles in open floor at both frame rates. Clamped at walls. | Matches. Wall behaviour is unspecified. |
| 3 | Facing after dash | Dash sets facing to the dash direction. | Unspecified |
| 4 | Swipe vs grub states | (a) hits but gives no knockback; (b) hits, 1.0-tile knockback; (c) a second swipe hits. "(miss)" not seen first-hand. | One contradiction (D-58-1) |
| 5 | Grub on you | Hit in all four facings. | Matches. Knockback direction unsettled. |
| 6 | Bots | Format found. No idle bot exists, so idle runs came from the trace view. | n/a |

### 1. Possibly short bite warning (settled: no short warning)

Runs: `trace/grub-room1-idle-30` (`room 1`, `fps 30`, `end 16`) and `trace/grub-room1-idle-60` (same at `fps 60`).

- The playtester's session restarted room 1 about 10.0 s into the run. Idle room 1 at 30 FPS reproduces their log with a +10.0 s offset:

| Playtester log | Idle trace at 30 FPS | Trace +10 s |
|---|---|---|
| "rears back (left)" at 11.90 s | `windup who 0 side left` at 1.900 | 11.90 |
| heart lost at 11.97 s | `hurt` at 1.967 | 11.97 |
| hits at 13.47 s and 14.97 s | hurts at 3.467 and 4.967 | 13.47, 14.97 |

- The bite at 1.967 belongs to grub#2. Its wind-up (side `above`) started at 1.400 and its strike at 1.900 (0.500 s later).
- The "rears back (left)" line at 1.900 belongs to grub#0. That grub struck at 2.400 (0.500 s later) and hurt nobody, because the player was invulnerable.
- At 1.900 grub#2's strike and grub#0's wind-up started in the same tick. So the heart loss followed the "rears back" line by 0.067 s, but from another grub. The misread was by the playtester, and the build is correct.
- No grub strikes less than 0.500 s after its own wind-up in either trace, at 30 or 60 FPS. The pairs below were taken from the wind-up and strike rows:

| FPS | Grub | Wind-up start | Strike start |
|---|---|---|---|
| 30 | #2 | 1.400 | 1.900 |
| 30 | #0 | 1.900 | 2.400 |
| 30 | #1 | 2.900 | 3.400 |
| 30 | #2 | 2.967 | 3.467 |
| 60 | #2 | 1.383 | 1.883 |
| 60 | #0 | 1.883 | 2.383 |

- A heart is lost 0.05–0.07 s after strike start, while the lunge closes to 1.0 tile. That is 0.55–0.57 s after the wind-up line, which explains the playtester's "0.5–0.65 s" for the other bites.
- 30 vs 60 FPS: event order is identical and timestamps differ by at most 0.034 s (hurt 1.967 vs 1.933). The first down is at 4.967 vs 4.950. This is within the 0.07 s allowance.
- The "rears back (side)" line does not say which grub struck. With several grubs, a cue for one can coincide with a hit from another. This is a readability note for the designer, not a defect.

### 2. Dash distance (settled; wall behaviour is a spec gap)

Runs: `trace/dash-open-and-wall` (60 FPS) and `trace/dash30` (30 FPS), both in `room empty`; `play/dash-wall-view` (60 FPS).

- Open floor: 8→12 and 12→8 (60 FPS), and 8→12 and 15→11 (30 FPS). That is exactly 4.00 tiles at both frame rates, a difference of 0.00 against the 0.25 allowance. The dash lasts about 0.25 s (`dash_end` at 0.233 s after the first logged frame, which is 0.25 s from the press). Invulnerable for the whole dash.
- Next to a wall the dash is clamped at the room edge:
  - 12→15 moved 3 tiles.
  - 4→0 moved 4 tiles.
  - A dash from y=0 upward or from x=15 rightward moves 0 tiles but still prints "you dash right", turns on invulnerability for 0.25 s and spends the dash. In `play/dash-wall-view`, from 14 it moved 1 tile, and the second dash at the wall did not move.
- The spec says "4 tiles". It is silent on walls. The manual gives no distance, only "a quick burst".
- The playtester's "2–3 tiles" is not the build's behaviour. A likely cause is that the player view draws only every 0.5 s (hypothesis).
- Cooldown: a dash 0.3 s after another was refused with "(dash not ready)" (`dash30`). I did not measure the exact cooldown.

### 3. Facing (settled; spec silent)

Runs: `play/facing-default`, `play/facing-dash60` and `play/facing-dash30`.

- Default facing is right. With spitters at 7.2 and 8.8 either side of `P` at 8, a swipe at 0.1 s hit only the right one ("spitter hit (1 left)").
- A dash changes facing to the dash direction:
  - Spitters at 11 and 13; the player moved left briefly, then dashed right at 0.3 s. The dash passed through the spitter at 11.
  - At 0.8 s the player stood at about 12, with one spitter behind and one ahead. The swipe hit one spitter only ("spitter hit (1 left)"), the one ahead and to the right (`z` at x=13), not the one behind (`s` at x=11).
  - Results are identical at 30 and 60 FPS.
- Facing was inferred from which enemy was hit. The player view does not print facing.
- The spec says only "a swipe in the facing direction". Whether a dash sets facing is unspecified: spec gap, hand to `game-designer`.

### 4. Swipe timing against grubs (partly settled)

Runs: `trace/strike-a` (swipe at 0.51), `trace/strike-b` (swipe at 0.54) and `trace/recovery-knock` (swipes at 1.0, 1.4, 1.8 and 2.2), all at 60 FPS with a grub at 9.24 and the player at 8.

- **(a) In Strike.**
  - Strike began at 0.517. The swipe at 0.51 took effect in frame 32 (0.533) and hit the grub, which went to HP 1. The same tick shows `hurt`, so the player still lost a heart.
  - The grub did not stop: it kept its Strike and moved from 9.13 to 8.24 into Recovery.
  - No `knockback` event occurred in this run.
  - The strike damages the player 1–2 frames after it starts, and the player is stunned from that moment. A swipe pressed even 0.03 s later is rejected as `stunned` (`strike-b`: pressed at 0.54, rejected at 0.567).
  - A swipe can therefore hit a grub in Strike only on the same tick or frame as the strike starts.
- **(b) In Recovery, adjacent.**
  - The swipe at 1.0 (taken at 1.017) hit a grub at 8.24, 0.11 tiles from the player. HP went 2→1 and a `knockback` event fired.
  - The grub ended at 9.24 by 1.333, a push of exactly 1.00 tile (one frame at 1.017 moved it 0.08, consistent with 1 tile in 0.2 s). It stayed in Recovery with its timer running on.
- **(c) After the first hit.**
  - The second swipe at 1.4 (taken at 1.417) hit the grub at 9.24, 1.11 tiles from the player at 8.13 and within the 1.5 reach. It was defeated and "room cleared" printed.
  - Knockback of 1 tile does not move an adjacent grub out of reach.
- **"(miss)":** the trace shows `attack ... hits []` for swipes at 1.8 and 2.2 with no enemy left. I did not run the player view for a living grub out of reach, so I did not see the "(miss)" text myself. Handoff 54 saw "(miss)" at 1.0 s in room 2 with all grubs far away.
- **Input delay:** inputs sometimes take effect one or two frames after their script time (0.51→0.533, 0.54→0.567).

**D-58-1 (low): no knockback when the first hit lands in Strike.**
- Expected: `design/combat.md` says "First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s". It states no exception for Strike.
- Actual: the grub took the hit (HP 1, damaged state) but showed no `knockback` event and no push (`strike-a`). The Strike continued and still damaged the player.
- Conditions: 60 FPS only. I did not repeat at 30 FPS because the case needs a same-tick hit.
- Severity: low. The case is rare because of the timing above, and the effect is only that the grub is not pushed.
- Whether a hit in Strike should interrupt, knock back or be ignored is not specified (the spec defines wind-up cancel and defeat-mid-state only). **Hand to `game-designer`** for a ruling before the engineer acts.
- Acceptance criteria once ruled (conditions: at 30 and 60 FPS, the room and grub as in `strike-a`):
  1. A first hit that lands in a grub's Strike produces the ruled outcome (knockback of 1 tile, or an explicit exemption), and the trace shows it.
  2. The hit line "grub hit (1 left)" still prints.
  3. The strike's own damage follows the ruling.
  4. The Wind-up (AC-5), Recovery and defeat cases are unchanged.

### 5. Grub "on you" (settled for the swipe; knockback direction unsettled)

Runs: `play/onyou-right`, `play/onyou-left`, `play/onyou-up` and `play/onyou-down` (60 FPS; each has the grub spawned on the player's tile, a `move` in that direction at 0.01 and a swipe at 0.2).

- Right, left, up and down all print "you swipe: grub hit (1 left)" and "the grub is open (on you)" at 0.2.
- A swipe hits a grub on the player's tile whichever facing is used. That matches the spec's "true position" rule.
- The hit cancelled the wind-up, and the grub rewound to the next "rears back (on you)" at 0.8 s. That is 0.6 s of Recovery, as in AC-5.
- Display: the grub is drawn beside `P` (right of `P` at the left, top and bottom walls; left of `P` at the right wall), as D-006 requires.
- **Limitation:** every test placed the player at a wall (x=15, x=0, y=0, y=8), and the facing was set only by a `move` into that wall; I did not read it from the trace. The grub still printed "(on you)" at 0.8 s, 0.6 s after a hit that should have knocked it back 1 tile. A hypothesis, not a finding: when the grub is exactly on the player, the knockback direction is the facing direction, and my wall positions clamped it to no movement. Where an on-you grub is pushed in open floor is unsettled and is also a spec gap.

### 6. Bot reference data

- **Format:** the script keys are `bots <list>`, `rooms <range|list>`, `fps <30|60>` and `limit <seconds>`. The failed script used `room 1`, which the parser does not know. The key is `rooms`.
- `repo/README.md` lists only camper, walker and dodger. `reactive` exists in `bots.py` but is missing from the README (cosmetic).
- **No idle bot exists.** `camper` stands still but turns and swings at enemies in reach. For passive (idle) numbers I used the trace view with no inputs (`trace/idle-room2-60` … `idle-room5-60`, `grub-room1-idle-30` and `-60`).
- Bots start each room fresh with 3 hearts and no run flow (no carry-over, no heal, no 1.5 s transition). Their decisions depend on the frame step, so a bot run at 30 and 60 FPS can differ and cannot be used for AC-17.

**Idle player** (no actions; trace, 60 FPS unless noted):

| Room | Down at (s) | Hearts lost | Hit by | Actions |
|---|---|---|---|---|
| 1 | 4.95 (60), 4.97 (30) | 3 | grub 3 | 0 |
| 2 | 5.05 | 3 | grub 3 | 0 |
| 3 | 5.52 | 3 | shot 3 | 0 |
| 4 | 5.03 | 3 | grub 3 | 0 |
| 5 | 4.53 | 3 | grub 2, shot 1 | 0 |

**Bots, 60 FPS** (`bots/ref60`). Cells give clear time in s, hearts lost, attacks, dashes. "NOT" = not cleared; the bot went down.

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 |
|---|---|---|---|---|---|
| camper | 3.5, 0, 6, 0 | 4.8, 0, 7, 0 | NOT 5.5, 3 (shot), 0, 0 | NOT 6.9, 3 (shot), 4, 0 | NOT 6.9, 3 (shot), 6, 0 |
| walker | 3.5, 0, 6, 0 | 5.1, 0, 8, 0 | 9.0, 0, 6, 0 | 9.1, 0, 8, 0 | 11.2, 0, 10, 0 |
| dodger | 3.5, 0, 6, 0 | 5.1, 0, 8, 0 | 11.8, 0, 6, 4 | 10.0, 0, 8, 1 | 9.8, 0, 10, 2 |
| reactive | 3.5, 0, 6, 0 | 6.3, 1 (grub), 8, 3 | 11.8, 0, 6, 4 | 12.9, 0, 9, 5 | 11.1, 0, 11, 2 |

**Bots, 30 FPS** (`bots/ref30`):

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 |
|---|---|---|---|---|---|
| camper | 3.5, 0, 6, 0 | 4.9, 0, 7, 0 | NOT 5.5, 3 (shot), 0, 0 | NOT 6.9, 3 (shot), 4, 0 | NOT 6.9, 3 (shot), 6, 0 |
| walker | 3.5, 0, 6, 0 | 4.8, 0, 8, 0 | 9.2, 0, 6, 0 | 9.1, 0, 8, 0 | 12.3, 0, 10, 0 |
| dodger | 3.5, 0, 6, 0 | 4.8, 0, 8, 0 | 9.5, 0, 6, 2 | 10.1, 0, 8, 1 | 14.5, 0, 10, 6 |
| reactive | 3.5, 0, 6, 0 | 4.8, 0, 8, 0 | 9.5, 0, 6, 2 | 14.3, 0, 8, 6 | 11.1, 0, 10, 2 |

### Spec gaps for `game-designer` (not defects)

- Does a dash set facing? (Observed: yes.)
- What does a dash into a wall do? (Observed: it clamps, and a dash against the wall is spent without movement.)
- What happens to a grub hit during Strike (see D-58-1)?
- In which direction is a grub that stands exactly on the player knocked back?
- Should the "rears back" line name which grub it is, given that a cue and a hit from different grubs can coincide?
- `manual.md` gives no dash distance (optional documentation note).

### Not settled

- Item 4, "(miss)" text with a living grub out of reach: not seen in the player view first-hand. Only handoff 54's observation and the trace's empty hit list support it.
- Item 5, knockback of an on-you grub in open floor: not tested. A run with `player 8 4` and a grub on that tile would settle it.
- D-58-1 was observed at 60 FPS only.
- Idle runs for rooms 2–5 were done at 60 FPS only. The 30 FPS idle run covers room 1 only.

## Decisions already made

- D-001, D-003 and D-006 were respected. I changed no build files and made no balance judgement.

## Constraints

- The Studio must keep the cell contents of the bot tables as measured here.
- Do not read the bot numbers as AC-17 evidence (see item 6).

## Open questions

- Should I use the remaining run round to settle the "Not settled" items above, or does `game-designer` need to rule on the spec gaps first?

## Expected output

The Studio routes D-58-1 and the spec gaps to `game-designer`, and the rest to review.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, repo/bots.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/55-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/59-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 59
from: game-designer
to: studio
stage: Route
outcome: done
---
# 59: game-designer → studio — Spec updated with A1–A3 and A5; manual draft for the Owner; retest guideline

## Task

Route the updated `design/combat.md` and D-011 to Build, to Verify (acceptance criteria AC-19…AC-27) and to QA's open check (55). Send the manual draft below to the Owner to place in `manual.md` (D-005, D-007 pattern). Use the retest guideline for the next Play and Review. Nothing goes to `game-director` now.

## Context

G-001 (combat monotony), Option A (D-002). Handoff 56 asked for A1, A2, A3 and the A5 gaps, the ring question for room 2, A4's trigger, the manual draft and a retest guideline. I did not run `play` or `bots`: the changes are rules with acceptance criteria and the evidence I would add (still-player runs, 53) already exists. The retest needs a reactive player, which I cannot script.

## Findings

### What changed in `design/combat.md` (see D-011)

- **A1 wind-up spacing:** no grub starts a Wind-up within 1.0 s [tune] of another grub's Wind-up start (cancelled or defeated ones still count). A blocked grub is Waiting.
- **Second rule for the ring (answer to the open question):** A1 alone does not handle room 2. With four grubs it spaces the bites but still lets four grubs stand on all sides, and the tester felt "no gap to leave through". So at most 2 grubs may be within 1.5 tiles of the player at once; the others wait at 2.0 tiles. Result for a still player in room 2: at most 2 grubs close, one committed bite at a time, bites at least 1.0 s apart, and the player has a gap to dash or counter. The 2-in-Wind-up/Strike limit stays as a backstop.
- **A2:** hit-stun 0.3 s → 0.15 s [tune]. Invulnerability to 0.8 s is unchanged. No buffer.
- **A3 body hit:** an enemy within 0.5 tile of the player (distance 0 too) is hit by every swipe whatever the facing. This also closes the distance-0 swipe gap, so no separate rule is needed.
- **A5 dash and facing:** a dash with a direction sets facing to it (like movement). A dash without a direction keeps facing. A queued attack fires in the dash direction.
- **A5 dash distance:** up to 4 tiles in 0.25 s, stopping at the room edge, invulnerable throughout. QA's check (55) is judged against this rule.
- **A5 swipe cases:** a swipe resolves on true positions in every grub state. A hit during Strike cancels that strike (attacks resolve before enemy damage in a tick) and puts the grub in a 0.6 s Recovery. A swipe in Recovery hits normally.
- **A5 miss wording:** "(miss) too far" when an enemy is within 2.5 tiles but beyond reach; "(miss) not in front" when an enemy is within 1.5 tiles but outside the cone and the body radius; "(miss)" alone otherwise. The word "(miss)" is kept, so AC-11 and the manual's phrase still hold.
- **New acceptance criteria AC-19…AC-27** (spacing, cap, turns, hit-stun, body hit, dash and facing, dash distance, Strike/Recovery swipes, miss wording), each stated for `fps 30` and `fps 60`. AC-17 now covers them. AC-1…AC-18 are unchanged except the stun value inside the text, and AC-11 notes the miss causes.
- Room layouts, knockback, the grub cycle, spitters, the cone and reach are unchanged.

### A4 and the held items

- **A4 (120° cone) stays held.** It comes in if the retest's trace shows the "(miss) not in front" line on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or testers still report missing grubs standing diagonally in front after A3 is in. Then widen to 120° [tune] and add an AC.
- **D1 (facing mechanic)** goes to `game-director` only if the retest still reports swipes into air after dashes or trouble turning, with A3 and the dash-facing rule in. **D2 (room 1 composition)** only if four grubs still read as a wall after A1 and the cap. This is as agreed in 56; neither is routed now.
- The cheap fixes do not need a facing mechanic or a room composition change, so there is no hand-back to the Director.

### Manual draft for the Owner (group B; text only, `manual.md` not edited)

Keep every phrase `ManualTest` checks (glyphs, "run over — rooms cleared: N", "press attack to start again", "a grub rears back", "the grub is open", "(miss)", "(too soon)", "(stunned)", "(down)", "(dash not ready)", the On screen section with `x` and the practice room). The phrase check ignores line wraps (D-009). Suggested placement:

**1. Controls section: replace the Attack and Dash bullets with:**

- **Attack**: a short swipe in the direction you face. It reaches a little more than one tile in a wide cone and hits every enemy inside it. An enemy right next to you or on your tile is always hit, whichever way you face. After a swipe you must wait a moment before the next. You can swipe an enemy at any time, even while it rears back to bite: a hit on a grub that is rearing back stops that bite. This is the best answer to a bite.
- **Dash**: a quick burst of up to four tiles in a direction (or the way you face). You turn to face the way you dash. You cannot be hurt while dashing, and you can dash through enemies and shots. A dash stops at the wall. It needs a moment to recharge.
- **Getting hit** costs a heart and stuns you for a very short moment (less than a quarter of a second), during which you cannot move, swipe or dash. Then you are safe for a little under a second.

**2. Add to What you hear and read, after the swipe-result bullet:**

- The first hit on a grub or spitter knocks it back about a tile and leaves it hurt. It may be out of reach afterwards: step toward it to hit it again.
- A swipe that does nothing says why: "(miss)" nothing was hit; "(miss) too far" an enemy is near but out of reach, step closer; "(miss) not in front" an enemy is next to you but outside the swipe's cone, face it first; "(too soon)" you are still recovering from the last swipe; "(stunned)" you were just hit; "(down)" you are out of hearts. (Replace the existing bullet on swipes that do nothing with this one.)

**3. Add to the On screen paragraph (after the sentence on grubs drawn beside you):**

Grubs take turns: at most two crowd you at a time, and they do not start to bite at the same moment. A grub waiting for its turn stands a couple of tiles away as a small `g`.

Keep the practice-room paragraph and the `x` row as they are.

### Retest guideline (design-side, qualitative)

Also written into `design/combat.md` ("Retest guideline"). Do not forward it to a Playtester.

- **Room 1:** a skilled player who reads the cues clears it and usually keeps most hearts. Damage comes from a misread or mistimed dash, not from a bite they could not avoid. They can step out, dash through, or hit the winding-up grub, then punish the open grub. A grub on them can be hit.
- **Room 2:** a skilled player can break the ring: only two grubs crowd them, bites come one at a time, and they can dash to a side or wall and fight from a free line. It is a real fight where a hit or two is plausible, but a player who tries clears it, usually with at least one heart left. A player standing still loses.
- Judge monotony only on a survived run.
- Ask the retest to report: swipes with "(miss) not in front" where the player aimed at that grub (A4); swipes into air after a dash (D1); whether four grubs still arrive as one clump that feels like a wall (D2 / Option B).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: Option A first; staggered arrival (part of B) deferred.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.
- D-009: the `ManualTest` phrase check ignores line wraps.
- **D-011 (new):** the A1–A3 package, the engagement cap and the A5 rules; A4, D1 and D2 rejected for now with revisit triggers.

## Constraints

- All timings in seconds; hold at 30 and 60 FPS (spacing 1.0 s, stun 0.15 s and dash 0.25 s included).
- No new input (D-001). Reuse the existing grub states and timers.
- Do not forward this handoff, the retest guideline or the design spec to a Playtester unchanged (design-side content).

## Open questions

- **For QA (55):** results on dash distance, facing and swipe cases are to be checked against the rules above. Where the build differs, it is a defect, unless QA shows a rule cannot be built.
- **For Build:** report as built the Waiting behavior of a blocked grub (position held, following a moving player), and whether the display draws per principle 4 still hold with it.
- **For Verify / Review:** the values 1.0 s spacing, the cap of 2 and the 0.15 s stun are [tune]. Retune in this order if the retest says too harsh or too soft: spacing (0.8–1.5 s), cap (2 or 3), stun.
- **For the art-director (optional):** nothing new is required. The "(miss)" cause wording and the Waiting grubs use the existing glyphs; the art-director may review readability of the waiting grubs at 2.0 tiles.

## Expected output

- **Build:** implement the rules in `design/combat.md` (grub spacing and cap, stun 0.15 s, body hit, dash facing and edge stop, Strike/Recovery swipe handling, miss causes) and the AC-19…AC-27 checks.
- **Verify (QA):** run AC-1…AC-27 at both frame rates and settle the dash, facing and swipe cases against the spec.
- **Owner:** place the manual draft in `manual.md`; Verify then re-runs the full suite (D-008, D-009).
- **Play and Review:** one retest of rooms 1 and 2 by a reactive player (a live session, or several short reactive scripts), judged against the retest guideline. A `run_bots` round needs the bots script format; the earlier failure (53) was a format mismatch and should be checked first.

## Sender assessment

- **Confidence:**
  - High: spacing plus cap addresses the ring seen in 54, and the body-hit rule addresses "on you" swipes. Both follow from rules and from the still-player runs in 53.
  - Medium: 0.15 s stun and 1.0 s spacing are the right strength. They rest on one scripted playtest and no reactive data.
  - Low: dash facing as the fix for swipes into air. It is the minimal rule; the backstep variant is held for the Director.
- A still player in room 2 now meets bites at least 1.0 s apart (down about 2 s after the first bite at the earliest), so the idle reference time to down changes. It is a reference, not a target.
- No `play` or `bots` run was used in this step. The retest guideline is what a live or reactive session is judged against.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md
- Previous handoff: goals/G-001-combat-monotony/56-studio-to-game-designer.md
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
