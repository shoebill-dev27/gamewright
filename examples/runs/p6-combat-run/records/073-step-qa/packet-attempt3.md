# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/68-studio-to-qa.md
next_seq: 70
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/70-qa-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/68-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 68
from: studio
to: qa
stage: Verify
outcome: routed
---
# 68: studio → qa — Verify the combat response change set (AC-1…AC-28, V-9…V-17) at 30 and 60 FPS

## Task

Verify the current build in `repo/` against the acceptance criteria in `design/combat.md` (AC-1…AC-28) and the player-visible criteria in `design/combat-visuals.md` (V-9…V-17, with earlier V items as regression). Run each check at both 30 and 60 FPS where the criterion depends on timing. Report pass/fail per criterion, plus regressions.

## Context

Goal G-001, "Combat feels monotonous". The Owner chose to rework existing enemy behavior first (D-002, Option A). A change set has just been built on the existing simulation: grub turn-taking and spacing between Wind-ups, a cap on grubs engaged near the player, shorter hit-stun, a body hit, dash facing, miss causes, a hit in Strike cancelling the strike, knockback of a grub on the player's tile, an `on you:` line, and attacker position in hit lines. The previous verification round (AC-1…AC-27 earlier set) passed or was settled by the Owner's suite runs (D-008, D-010). This round covers the new and changed criteria and checks the old ones for regressions.

## Findings

Nothing to forward from the implementation beyond how to exercise it. Verify from the spec, the criteria and the build.

How to exercise (from `project.md`; the project directory is the one containing `manual.md` and `repo/`):

- Tests: `python3 -m unittest discover -s tests` (run in `repo/`). The manual tests read `manual.md` at the project root, one level above `repo/`. Run the whole suite with it in place and report the counts and any failure by name.
- Player view: `python3 play.py --view player {script}`; trace view: `python3 play.py --view trace {script}`. Script format is in `manual.md`.
- Balance bots: `python3 bots.py {script}`. Run at both frame rates for reference data on room 1 and room 2 (clear time, hearts lost, actions used); report the numbers without judging balance.

Items left unobserved by earlier rounds, to check first-hand against the spec:

- The `(miss)` text with its cause, in the player view.
- Knockback of a grub standing on the player's tile in open floor (AC-28), and near a wall.
- A hit in Strike at 30 FPS (the earlier open point D-58-1; the spec rule is in `design/combat.md`).
- Engagement cap and Wind-up spacing in room 2 with the player standing still, at both frame rates.

Also read `manual.md` against V-15 and the AC-15 wording. The Owner may not yet have placed all draft text there (open Owner step); report what is and is not present, and whether any missing text is needed by a criterion. Do not edit `manual.md`.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-009: the manual phrase check ignores line wraps.
- D-010: AC-15 passed on the Owner's suite run (40/40) for the earlier build.
- D-011: grubs take turns, crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line for an enemy on the player's tile; hit lines name the attacker position.
- D-013: a grub on the player's tile is knocked back toward the side it is drawn on.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Do not edit the repo or `manual.md`. If something cannot be run in your environment, report exactly what is needed (for example the Owner running the suite, as in D-008) instead of guessing.
- A criterion failing for the second time goes to re-planning (orchestration, loop limits). Say in the report which criteria failed before, if the earlier reports show it.

## Open questions

None. If a criterion is undefined or ambiguous, say so and name it.

## Expected output

A verification report with per-criterion pass/fail (AC-1…AC-28, V-9…V-17, regressions), suite counts, bot numbers at both frame rates, and an explicit list of what you could not observe. Address the result to `studio` (the Studio composes the next step from it).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/ (build: run commands in project.md)
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-010-owner-ran-suite-ac15-passes.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: none (composed fresh without the implementer's assessment)
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

<<<FILE decisions/D-010-owner-ran-suite-ac15-passes.md
---
kind: decision
id: D-010
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-010: The Owner ran `run_tests` for the AC-15 rerun (Option A); 40/40 passes

## Decision

The Owner chose Option A of Escalation 48. The Owner ran `python3 -m unittest discover -s tests` in `repo/` with the unchanged `manual.md` beside it, and reported: Ran 40 tests, OK (40 of 40 passed, 0 failures).

AC-15 is therefore treated as passing. Together with 7g (39) and 7h (44), all Verify steps are done and Play (stage 8) opens. Limit: the run is the Owner's, not QA's. It was made in a sandbox on the Owner's behalf, against `manual.md` unchanged (D-009), and the result is the raw test output.

Owner's own words (2026-10-15): "A。manual.md は変更せず repo/ の隣に置いた環境で python3 -m unittest discover を実行しました（Owner の代理、サンドボックス内）。結果: Ran 40 tests — OK（40件中40件成功、失敗0）。"

No conditions were added by the Owner.

## Rationale

The test output itself is objective. It is the same procedure as D-008, and it clears the only open Verify item. Another QA round would have lacked the same input (`manual.md`, see 29, 40, 47).

## Alternatives considered

- Option B (the Owner places `manual.md` in QA's workspace, QA reruns): higher independence, but it was unclear whether the Owner could place the file there. It was not needed once A returned 40/40.

## Revisit when

The suite or `manual.md` changes after this run, so that AC-15 must be re-verified. Or a later build fails `ManualTest`. In that case the designer rules (D-009 "Revisit when").
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

Exit: 1 (0.2 s). Output:

```text
....................................EE........................
======================================================================
ERROR: test_manual_lists_glyphs_and_lines (test_game.ManualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 935, in test_manual_lists_glyphs_and_lines
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
  File "/work/tests/test_game.py", line 945, in test_on_screen_section_lists_x_and_the_practice_room
    text = MANUAL.read_text(encoding="utf-8")
  File "/usr/lib/python3.10/pathlib.py", line 1134, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
  File "/usr/lib/python3.10/pathlib.py", line 1119, in open
    return self._accessor.open(self, mode, buffering, encoding, errors,
FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'

======================================================================
FAIL: test_hit_stun_is_short (test_game.CrowdTest) (fps=30)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 282, in test_hit_stun_is_short
    self.assertTrue(game.invulnerable)
AssertionError: False is not true

======================================================================
FAIL: test_hit_stun_is_short (test_game.CrowdTest) (fps=60)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 282, in test_hit_stun_is_short
    self.assertTrue(game.invulnerable)
AssertionError: False is not true

----------------------------------------------------------------------
Ran 63 tests in 0.118s

FAILED (failures=2, errors=2)
```

### Round 1: @run/play/miss-far-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 10 4
end 1
0.05 attack
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
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.067  you swipe: (miss) too far
   [0.10 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  0.400  a grub rears back (right)
   [0.40 s] hearts 3/3
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
  0.967  YOU ARE HIT by a grub (right) — hearts 2/3
   [0.97 s] hearts 2/3
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
   [1.00 s] hearts 2/3
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
end at 1.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/miss-far-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 10 4
end 1
0.05 attack
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
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.050  you swipe: (miss) too far
   [0.07 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  0.383  a grub rears back (right)
   [0.38 s] hearts 3/3
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
  0.933  YOU ARE HIT by a grub (right) — hearts 2/3
   [0.93 s] hearts 2/3
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
   [1.00 s] hearts 2/3
on you: G biting soon (shown right)
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
end at 1.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/miss-side-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8 5
end 1
0.05 attack
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
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (below)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
  0.067  you swipe: (miss) not in front
   [0.10 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |        G)      |
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
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (below) — hearts 2/3
   [0.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown below)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown below)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/miss-side-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8 5
end 1
0.05 attack
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
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (below)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
  0.050  you swipe: (miss) not in front
   [0.07 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |        G)      |
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
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (below) — hearts 2/3
   [0.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown below)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown below)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/miss-none-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 2 4
spawn grub 12 4
end 1
0.05 attack
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
   |  P         g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.067  you swipe: (miss)
   [0.10 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |   )            |
   |  P)        g   |
   |   )            |
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
   |  P        g    |
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
   |  P       g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 1
```

### Round 1: @run/play/miss-none-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 2 4
spawn grub 12 4
end 1
0.05 attack
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
   |  P         g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.050  you swipe: (miss)
   [0.07 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |   )            |
   |  P)        g   |
   |   )            |
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
   |  P        g    |
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
   |  P       g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 3/3, enemies left 1
```

### Round 1: @run/play/knock-ontile-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
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
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown right)
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
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.23 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
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
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (right)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
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
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.333  YOU ARE HIT by a grub (right) — hearts 2/3
   [1.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/knock-ontile-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
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
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown right)
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
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
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
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (right)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
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
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.317  YOU ARE HIT by a grub (right) — hearts 2/3
   [1.32 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/trace/knock-ontile-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.233 frame=7 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.17,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'on you'}; knockback {'who': 0, 'on_tile': True}
t=0.800 frame=24 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.300 frame=39 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=1.333 frame=40 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.78,4.00,hp=1,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'right'}
t=1.467 frame=44 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.000 frame=60 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.350) | end
```

### Round 1: @run/trace/knock-ontile-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.217 frame=13 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.08,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'on you'}; knockback {'who': 0, 'on_tile': True}
t=0.800 frame=48 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.300 frame=78 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=1.317 frame=79 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.89,4.00,hp=1,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'right'}
t=1.450 frame=87 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.000 frame=120 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.117 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.350) | end
```

### Round 1: @run/play/knock-wall-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pg|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              PG|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.23 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pw|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pw|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (left)
   [0.80 s] hearts 3/3
on you: W biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              PW|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
on you: W biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              PW|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.333  YOU ARE HIT by a grub (left) — hearts 2/3
   [1.33 s] hearts 2/3
on you: W biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              PW|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pw|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pw|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pw|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/trace/knock-wall-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.217 frame=13 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(14.42,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'on you'}; knockback {'who': 0, 'on_tile': True}
t=0.800 frame=48 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=1.300 frame=78 room=empty phase=playing pos=(14.50,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(13.50,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=1.317 frame=79 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(13.61,4.00,hp=1,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left'}
t=1.450 frame=87 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(14.50,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.000 frame=120 room=empty phase=playing pos=(14.50,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.117 stun_left=0.000 shots=0 | grub#0(14.50,4.00,hp=1,recovery,0.350) | end
```

### Round 1: @run/trace/strike-hit-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 9.2 4
end 3
0.55 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.533 frame=16 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.98,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'right'}
t=0.600 frame=18 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.767 stun_left=0.117 shots=0 | grub#0(8.76,4.00,hp=2,strike,0.083) | ignored {'action': 'attack', 'reason': 'stunned'}
t=0.700 frame=21 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.20,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=1.367 frame=41 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,recovery,0.217) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.600 frame=48 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,windup,0.483) | windup {'who': 0, 'side': 'right'}
t=2.100 frame=63 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.18,4.00,hp=2,strike,0.133) | strike {'who': 0}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=2.233 frame=67 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.900 frame=87 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.000 frame=90 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.133) | end
```

### Round 1: @run/trace/strike-hit-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 9.2 4
end 3
0.55 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.550 frame=33 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.98,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'right'}
t=0.567 frame=34 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.783 stun_left=0.133 shots=0 | grub#0(8.87,4.00,hp=2,strike,0.100) | ignored {'action': 'attack', 'reason': 'stunned'}
t=0.667 frame=40 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.683 stun_left=0.033 shots=0 | grub#0(8.20,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=1.350 frame=81 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,recovery,0.217) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.567 frame=94 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=2.067 frame=124 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=2.083 frame=125 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.18,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=2.217 frame=133 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.883 frame=173 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.000 frame=180 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.117) | end
```

### Round 1: @run/trace/room2-still-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room 2
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=2 dt=0.03333
t=0.000 frame=0 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.00,1.00,hp=2,approach,0.000) grub#1(15.00,7.00,hp=2,approach,0.000) grub#2(14.00,0.00,hp=2,approach,0.000) grub#3(1.00,8.00,hp=2,approach,0.000) | setup
t=2.733 frame=82 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,windup,0.500) grub#1(9.98,4.85,hp=2,approach,0.000) grub#2(9.45,3.03,hp=2,approach,0.000) grub#3(5.75,5.29,hp=2,approach,0.000) | windup {'who': 0, 'side': 'top left'}
t=3.233 frame=97 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=3.300 frame=99 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.28,3.64,hp=2,strike,0.083) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left'}
t=3.400 frame=102 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.883) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=3.733 frame=112 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.550) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.500) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 2, 'side': 'top right'}
t=4.100 frame=123 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.183) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.133) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.233 frame=127 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.050) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,strike,0.150) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 2}
t=4.300 frame=129 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.67,3.55,hp=2,strike,0.083) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=4.400 frame=132 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.883) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 2, 'side': 'right'}
t=4.733 frame=142 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.500) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.550) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 0, 'side': 'left'}
t=5.100 frame=153 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.133) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.183) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.233 frame=157 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.050) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=5.267 frame=158 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.83,3.91,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0, 'pos': 'left'}; down
t=6.067 frame=182 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.83,3.91,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.267 frame=218 room=2 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.83,3.91,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=7.267 frame=218 room=2 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.83,3.91,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | end
```

### Round 1: @run/trace/room2-still-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room 2
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=2 dt=0.01667
t=0.000 frame=0 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.00,1.00,hp=2,approach,0.000) grub#1(15.00,7.00,hp=2,approach,0.000) grub#2(14.00,0.00,hp=2,approach,0.000) grub#3(1.00,8.00,hp=2,approach,0.000) | setup
t=2.733 frame=164 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,windup,0.500) grub#1(9.98,4.85,hp=2,approach,0.000) grub#2(9.45,3.03,hp=2,approach,0.000) grub#3(5.75,5.29,hp=2,approach,0.000) | windup {'who': 0, 'side': 'top left'}
t=3.233 frame=194 room=2 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.88,3.44,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=3.283 frame=197 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.18,3.59,hp=2,strike,0.100) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left'}
t=3.383 frame=203 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.900) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,waiting-spacing,0.000) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=3.733 frame=224 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.550) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.500) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 2, 'side': 'top right'}
t=4.083 frame=245 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.200) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,windup,0.150) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.233 frame=254 room=2 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,recovery,0.050) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(9.04,3.31,hp=2,strike,0.150) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 2}
t=4.283 frame=257 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.76,3.49,hp=2,strike,0.100) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'top right'}
t=4.383 frame=263 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.78,3.89,hp=2,waiting-spacing,0.000) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.900) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | recover {'cause': 'strike', 'who': 2, 'side': 'right'}
t=4.733 frame=284 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.500) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.550) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | windup {'who': 0, 'side': 'left'}
t=5.083 frame=305 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,windup,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.200) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.233 frame=314 room=2 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.78,3.89,hp=2,strike,0.150) grub#1(9.84,4.79,hp=2,waiting-cap,0.000) grub#2(8.21,3.86,hp=2,recovery,0.050) grub#3(6.26,4.99,hp=2,waiting-cap,0.000) | strike {'who': 0}
t=5.250 frame=315 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.80,3.90,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0, 'pos': 'left'}; down
t=6.050 frame=363 room=2 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.80,3.90,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=7.250 frame=435 room=2 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.80,3.90,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=7.250 frame=435 room=2 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.80,3.90,hp=2,approach,0.000) grub#1(9.84,4.79,hp=2,approach,0.000) grub#2(8.21,3.86,hp=2,approach,0.000) grub#3(6.26,4.99,hp=2,approach,0.000) | end
```

### Round 1: @run/trace/dashface-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 0 0
end 3
0.0 move right
0.2 stop
0.4 dash left
1.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,0.00,hp=2,approach,0.000) | setup
t=0.433 frame=13 room=empty phase=playing pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.79,0.37,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=0.667 frame=20 room=empty phase=playing pos=(4.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.17,0.63,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.233 frame=37 room=empty phase=playing pos=(4.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.00,1.40,hp=2,approach,0.000) | attack {'facing': 'left', 'hits': [], 'miss': None}
t=2.533 frame=76 room=empty phase=playing pos=(4.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.88,3.15,hp=2,windup,0.500) | windup {'who': 0, 'side': 'top left'}
t=3.000 frame=90 room=empty phase=playing pos=(4.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.88,3.15,hp=2,windup,0.033) | end
```

### Round 1: @run/play/dashface-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 0 0
end 3
0.0 move right
0.2 stop
0.4 dash left
1.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |g               |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.400  you dash left
   [0.50 s] hearts 3/3
   +----------------+
   | g              |
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  g             |
   |                |
   |                |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  you swipe: (miss)
   [1.22 s] hearts 3/3
   +----------------+
   |                |
   |  g             |
   |                |
   |                |
   |    (P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |  g             |
   |                |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |   g            |
   |                |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    g           |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.533  a grub rears back (top left)
   [2.53 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    G           |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    G           |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 1
```

### Round 1: @run/bots/room1-30 — `python3 bots.py {script}`

Script:

```text
room 1
fps 30
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room 1'
```

### Round 1: @run/bots/room1-60 — `python3 bots.py {script}`

Script:

```text
room 1
fps 60
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room 1'
```

### Round 1: @run/bots/room2-30 — `python3 bots.py {script}`

Script:

```text
room 2
fps 30
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room 2'
```

### Round 1: @run/bots/room2-60 — `python3 bots.py {script}`

Script:

```text
room 2
fps 60
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room 2'
```

### Round 2: @run/play/wall-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pg|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              PG|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              Pw|
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
   |             wP |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (left)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             WP |
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
   |             WP |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.317  YOU ARE HIT by a grub (left) — hearts 2/3
   [1.32 s] hearts 2/3
on you: W biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             WP |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             wP |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             wP |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             wP |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 2: @run/trace/stun-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 9.2 4
end 2.5
0.62 attack
0.65 dash
0.85 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.533 frame=16 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.98,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'right'}
t=0.667 frame=20 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(8.31,4.00,hp=2,strike,0.017) | ignored {'action': 'attack', 'reason': 'stunned'}
t=0.700 frame=21 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.20,4.00,hp=2,recovery,0.883) | ignored {'action': 'dash', 'reason': 'stunned'}; recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=0.900 frame=27 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.467 stun_left=0.000 shots=0 | grub#0(8.37,4.00,hp=1,recovery,0.683) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; knockback {'who': 0, 'on_tile': False}
t=1.367 frame=41 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,recovery,0.217) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.600 frame=48 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,windup,0.483) | windup {'who': 0, 'side': 'right'}
t=2.100 frame=63 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.09,4.00,hp=1,strike,0.133) | strike {'who': 0}
t=2.133 frame=64 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.87,4.00,hp=1,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=2.233 frame=67 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(8.20,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=2.500 frame=75 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.433 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=1,recovery,0.633) | end
```

### Round 2: @run/trace/stun-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 9.2 4
end 2.5
0.62 attack
0.65 dash
0.85 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.550 frame=33 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.98,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'right'}
t=0.650 frame=39 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(8.31,4.00,hp=2,strike,0.017) | ignored {'action': 'attack', 'reason': 'stunned'}
t=0.667 frame=40 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.683 stun_left=0.033 shots=0 | grub#0(8.20,4.00,hp=2,recovery,0.900) | ignored {'action': 'dash', 'reason': 'stunned'}; recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=0.867 frame=52 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.483 stun_left=0.000 shots=0 | grub#0(8.28,4.00,hp=1,recovery,0.700) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; knockback {'who': 0, 'on_tile': False}
t=1.350 frame=81 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,recovery,0.217) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.567 frame=94 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=2.067 frame=124 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=2.100 frame=126 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.98,4.00,hp=1,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=2.217 frame=133 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.683 stun_left=0.033 shots=0 | grub#0(8.20,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=2.500 frame=150 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.400 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=1,recovery,0.617) | end
```

### Round 2: @run/trace/strike-a-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 9.2 4
end 1.5
0.50 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.533 frame=16 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.37,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=1.500 frame=45 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.33,4.00,hp=1,approach,0.000) | end
```

### Round 2: @run/trace/strike-b-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 9.2 4
end 1.5
0.52 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.533 frame=16 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.37,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=1.500 frame=45 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.40,4.00,hp=1,approach,0.000) | end
```

### Round 2: @run/trace/strike-c-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 9.2 4
end 1.5
0.53 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.533 frame=16 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.37,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=1.500 frame=45 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.40,4.00,hp=1,approach,0.000) | end
```

### Round 2: @run/trace/strike-a-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 9.2 4
end 1.5
0.51 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.28,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=1.500 frame=90 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.40,4.00,hp=1,approach,0.000) | end
```

### Round 2: @run/trace/strike-b-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 9.2 4
end 1.5
0.533 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.517 frame=31 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.550 frame=33 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.17,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=1.500 frame=90 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.32,4.00,hp=1,approach,0.000) | end
```

### Round 2: @run/trace/cycle-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8 4
end 3
0.8 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.533 frame=16 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'on you'}
t=0.700 frame=21 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=0.833 frame=25 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.000 shots=0 | grub#0(8.17,4.00,hp=1,recovery,0.750) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; knockback {'who': 0, 'on_tile': True}
t=1.367 frame=41 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,recovery,0.217) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.600 frame=48 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,windup,0.483) | windup {'who': 0, 'side': 'right'}
t=2.100 frame=63 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.89,4.00,hp=1,strike,0.133) | strike {'who': 0}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=2.233 frame=67 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.900 frame=87 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.000 frame=90 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.133) | end
```

### Round 2: @run/trace/cycle-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8 4
end 3
0.8 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'on you'}
t=0.517 frame=31 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'on you'}
t=0.667 frame=40 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=0.817 frame=49 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.517 stun_left=0.000 shots=0 | grub#0(8.08,4.00,hp=1,recovery,0.750) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; knockback {'who': 0, 'on_tile': True}
t=1.333 frame=80 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.567 frame=94 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=2.067 frame=124 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.00,4.00,hp=1,strike,0.150) | strike {'who': 0}
t=2.083 frame=125 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.89,4.00,hp=1,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'right'}
t=2.217 frame=133 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=2.883 frame=173 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.233) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.000 frame=180 room=empty phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=1,recovery,0.117) | end
```

### Round 2: @run/trace/body-a-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8.2 4
end 1
0.05 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.100 frame=3 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.37,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=0.667 frame=20 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.000 frame=30 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,windup,0.167) | end
```

### Round 2: @run/trace/body-a-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8.2 4
end 1
0.05 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.20,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.067 frame=4 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.28,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=0.650 frame=39 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.000 frame=60 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.20,4.00,hp=1,windup,0.150) | end
```

### Round 2: @run/trace/body-br-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8.0 4
end 1
0.0 move right
0.1 stop
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.13,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=0.233 frame=7 room=empty phase=playing pos=(8.40,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.83,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'left'}; knockback {'who': 0, 'on_tile': False}
t=0.867 frame=26 room=empty phase=playing pos=(8.40,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.15,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=1.000 frame=30 room=empty phase=playing pos=(8.40,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.15,4.00,hp=1,windup,0.367) | end
```

### Round 2: @run/trace/body-br-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8.0 4
end 1
0.0 move right
0.1 stop
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.07,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=0.217 frame=13 room=empty phase=playing pos=(8.40,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.92,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'left'}; knockback {'who': 0, 'on_tile': False}
t=0.867 frame=52 room=empty phase=playing pos=(8.40,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.15,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=1.000 frame=60 room=empty phase=playing pos=(8.40,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.15,4.00,hp=1,windup,0.367) | end
```

### Round 2: @run/trace/body-bl-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8.0 4
end 1
0.0 move left
0.1 stop
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(7.87,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.233 frame=7 room=empty phase=playing pos=(7.60,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.17,4.00,hp=1,recovery,0.567) | attack {'facing': 'left', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=0.867 frame=26 room=empty phase=playing pos=(7.60,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.85,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.000 frame=30 room=empty phase=playing pos=(7.60,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.85,4.00,hp=1,windup,0.367) | end
```

### Round 2: @run/trace/body-bl-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8.0 4
end 1
0.0 move left
0.1 stop
0.2 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(7.93,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.217 frame=13 room=empty phase=playing pos=(7.60,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.08,4.00,hp=1,recovery,0.583) | attack {'facing': 'left', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=0.867 frame=52 room=empty phase=playing pos=(7.60,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.85,4.00,hp=1,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.000 frame=60 room=empty phase=playing pos=(7.60,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.85,4.00,hp=1,windup,0.367) | end
```

### Round 2: @run/trace/body-c-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8.0 4
end 1
0.0 move right
0.2 stop
0.3 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.13,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=0.333 frame=10 room=empty phase=playing pos=(8.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.200) | attack {'facing': 'right', 'hits': [], 'miss': 'not in front'}
t=0.533 frame=16 room=empty phase=playing pos=(8.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.567 frame=17 room=empty phase=playing pos=(8.80,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.18,4.00,hp=2,strike,0.117) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left'}
t=0.700 frame=21 room=empty phase=playing pos=(8.80,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.80,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=1.000 frame=30 room=empty phase=playing pos=(8.80,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(8.80,4.00,hp=2,recovery,0.583) | end
```

### Round 2: @run/trace/body-c-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8.0 4
end 1
0.0 move right
0.2 stop
0.3 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.07,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'left'}
t=0.317 frame=19 room=empty phase=playing pos=(8.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,windup,0.200) | attack {'facing': 'right', 'hits': [], 'miss': 'not in front'}
t=0.517 frame=31 room=empty phase=playing pos=(8.80,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.00,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=0.533 frame=32 room=empty phase=playing pos=(8.80,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(8.09,4.00,hp=2,strike,0.133) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'left'}
t=0.667 frame=40 room=empty phase=playing pos=(8.80,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.017 shots=0 | grub#0(8.80,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=1.000 frame=60 room=empty phase=playing pos=(8.80,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.333 stun_left=0.000 shots=0 | grub#0(8.80,4.00,hp=2,recovery,0.567) | end
```

### Round 2: @run/trace/dashdir-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 0 8
end 2.5
0.0 move up
0.1 stop
0.3 dash
1.0 attack
1.5 dash left
1.55 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,8.00,hp=2,approach,0.000) | setup
t=0.333 frame=10 room=empty phase=playing pos=(8.00,3.07) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.58,7.68,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=0.567 frame=17 room=empty phase=playing pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.93,7.37,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.033 frame=31 room=empty phase=playing pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.58,6.69,hp=2,approach,0.000) | attack {'facing': 'up', 'hits': [], 'miss': None}
t=1.533 frame=46 room=empty phase=playing pos=(7.47,0.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.27,5.97,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=1.767 frame=53 room=empty phase=playing pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.47,5.56,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end; attack {'facing': 'left', 'hits': [], 'miss': None}
t=2.500 frame=75 room=empty phase=playing pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.86,4.14,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/dashdir-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 0 8
end 2.5
0.0 move up
0.1 stop
0.3 dash
1.0 attack
1.5 dash left
1.55 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,8.00,hp=2,approach,0.000) | setup
t=0.317 frame=19 room=empty phase=playing pos=(8.00,3.33) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.56,7.70,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=0.550 frame=33 room=empty phase=playing pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.91,7.40,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.017 frame=61 room=empty phase=playing pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.56,6.72,hp=2,approach,0.000) | attack {'facing': 'up', 'hits': [], 'miss': None}
t=1.517 frame=91 room=empty phase=playing pos=(7.73,0.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.25,6.00,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=1.750 frame=105 room=empty phase=playing pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.47,5.60,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end; attack {'facing': 'left', 'hits': [], 'miss': None}
t=2.500 frame=150 room=empty phase=playing pos=(4.00,0.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.87,4.15,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/dist-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 0 8
end 1.2
0.1 dash right
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,8.00,hp=2,approach,0.000) | setup
t=0.133 frame=4 room=empty phase=playing pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.24,7.88,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.367 frame=11 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.68,7.72,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=0.533 frame=16 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.99,7.61,hp=2,approach,0.000) | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=1.200 frame=36 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.26,7.20,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/dist-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 0 8
end 1.2
0.1 dash right
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,8.00,hp=2,approach,0.000) | setup
t=0.117 frame=7 room=empty phase=playing pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.21,7.90,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.350 frame=21 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.64,7.73,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=0.517 frame=31 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.96,7.62,hp=2,approach,0.000) | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=1.200 frame=72 room=empty phase=playing pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.26,7.20,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/edge-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 2 4
spawn grub 0 8
end 1
0.1 dash left
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,8.00,hp=2,approach,0.000) | setup
t=0.133 frame=4 room=empty phase=playing pos=(1.47,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.11,7.76,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=0.367 frame=11 room=empty phase=playing pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.12,7.29,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.000 frame=30 room=empty phase=playing pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.07,6.03,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/edge-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 2 4
spawn grub 0 8
end 1
0.1 dash left
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.00,8.00,hp=2,approach,0.000) | setup
t=0.117 frame=7 room=empty phase=playing pos=(1.73,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.10,7.79,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=0.350 frame=21 room=empty phase=playing pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.13,7.33,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.000 frame=60 room=empty phase=playing pos=(0.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(0.08,6.03,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/far-knock-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8.6 4
end 0.45
0.1 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.60,4.00,hp=2,approach,0.000) | setup
t=0.033 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.60,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.133 frame=4 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.77,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=0.467 frame=14 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.60,4.00,hp=1,recovery,0.233) | end
```

### Round 2: @run/trace/far-knock-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8.6 4
end 0.45
0.1 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.60,4.00,hp=2,approach,0.000) | setup
t=0.017 frame=1 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.60,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=0.117 frame=7 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(8.68,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)], 'miss': None}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0, 'on_tile': False}
t=0.450 frame=27 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.60,4.00,hp=1,recovery,0.250) | end
```

### Round 2: @run/play/v11-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 8 4
spawn grub 9 4
end 1
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (on you) — hearts 2/3
   [0.57 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 2
```

### Round 2: @run/play/v11-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 8 4
spawn grub 9 4
end 1
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (on you) — hearts 2/3
   [0.53 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 2
```

### Round 2: @run/play/v14-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room empty
player 8 4
spawn grub 7 4
spawn grub 9 4
end 2
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
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (left)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
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
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (left) — hearts 2/3
   [0.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.033  a grub rears back (right)
   [1.03 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.567  YOU ARE HIT by a grub (right) — hearts 1/3
   [1.57 s] hearts 1/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.683  the grub is open (on you)
   [1.70 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 1/3, enemies left 2
```

### Round 2: @run/play/v14-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room empty
player 8 4
spawn grub 7 4
spawn grub 9 4
end 2
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
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (left)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
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
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (left) — hearts 2/3
   [0.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.017  a grub rears back (right)
   [1.02 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.533  YOU ARE HIT by a grub (right) — hearts 1/3
   [1.53 s] hearts 1/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.667  the grub is open (on you)
   [1.67 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 1/3, enemies left 2
```

### Round 2: @run/trace/room1-still-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room 1
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=1 dt=0.03333
t=0.000 frame=0 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.00,4.00,hp=2,approach,0.000) grub#1(15.00,4.00,hp=2,approach,0.000) grub#2(8.00,0.00,hp=2,approach,0.000) | setup
t=1.400 frame=42 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(5.80,4.00,hp=2,approach,0.000) grub#1(12.20,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=1.900 frame=57 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,waiting-spacing,0.000) grub#1(11.20,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,2.75,hp=2,strike,0.150) | strike {'who': 2}
t=1.967 frame=59 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(6.75,4.00,hp=2,waiting-spacing,0.000) grub#1(11.07,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.19,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'above'}
t=2.067 frame=62 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(6.75,4.00,hp=2,waiting-spacing,0.000) grub#1(10.87,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 2, 'side': 'above'}
t=2.400 frame=72 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.500) grub#1(10.20,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.550) | windup {'who': 0, 'side': 'left'}
t=2.767 frame=83 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.133) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.183) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.900 frame=87 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,strike,0.150) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.050) | strike {'who': 0}
t=2.967 frame=89 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.19,4.00,hp=2,strike,0.083) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,waiting-spacing,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'left'}
t=3.067 frame=92 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.883) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,waiting-spacing,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=3.400 frame=102 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.550) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=3.767 frame=113 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.183) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,windup,0.133) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.900 frame=117 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.050) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,strike,0.150) | strike {'who': 2}
t=3.933 frame=118 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.81,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0, 'pos': 'above'}; down
t=4.733 frame=142 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.81,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.933 frame=178 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.81,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=5.933 frame=178 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.81,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/room1-still-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room 1
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=1 dt=0.01667
t=0.000 frame=0 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(3.00,4.00,hp=2,approach,0.000) grub#1(15.00,4.00,hp=2,approach,0.000) grub#2(8.00,0.00,hp=2,approach,0.000) | setup
t=1.383 frame=83 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(5.77,4.00,hp=2,approach,0.000) grub#1(12.23,4.00,hp=2,approach,0.000) grub#2(8.00,2.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=1.883 frame=113 room=1 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,waiting-spacing,0.000) grub#1(11.23,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,2.75,hp=2,strike,0.150) | strike {'who': 2}
t=1.933 frame=116 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(6.75,4.00,hp=2,waiting-spacing,0.000) grub#1(11.13,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.08,hp=2,strike,0.100) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'above'}
t=2.033 frame=122 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(6.75,4.00,hp=2,waiting-spacing,0.000) grub#1(10.93,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 2, 'side': 'above'}
t=2.383 frame=143 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.500) grub#1(10.23,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.550) | windup {'who': 0, 'side': 'left'}
t=2.733 frame=164 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,windup,0.150) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.200) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.883 frame=173 room=1 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(6.75,4.00,hp=2,strike,0.150) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,recovery,0.050) | strike {'who': 0}
t=2.933 frame=176 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.08,4.00,hp=2,strike,0.100) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,waiting-spacing,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'left'}
t=3.033 frame=182 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.900) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,waiting-spacing,0.000) | recover {'cause': 'strike', 'who': 0, 'side': 'left'}
t=3.383 frame=203 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.550) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,windup,0.500) | windup {'who': 2, 'side': 'above'}
t=3.733 frame=224 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.200) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,windup,0.150) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.883 frame=233 room=1 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,recovery,0.050) grub#1(10.00,4.00,hp=2,waiting-cap,0.000) grub#2(8.00,3.75,hp=2,strike,0.150) | strike {'who': 2}
t=3.900 frame=234 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.78,hp=2,approach,0.000) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0, 'pos': 'above'}; down
t=4.700 frame=282 room=1 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.78,hp=2,approach,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.900 frame=354 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.78,hp=2,approach,0.000) | run_over {'rooms': 0, 'complete': False}
t=5.900 frame=354 room=1 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.75,4.00,hp=2,approach,0.000) grub#1(10.00,4.00,hp=2,approach,0.000) grub#2(8.00,3.78,hp=2,approach,0.000) | end
```

### Round 2: @run/trace/room5-still-30 — `python3 play.py --view trace {script}`

Script:

```text
fps 30
room 5
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=5 dt=0.03333
t=0.000 frame=0 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.00,1.00,hp=2,approach,0.000) grub#1(0.00,6.00,hp=2,approach,0.000) grub#2(4.00,8.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,1.000) spitter#4(15.00,8.00,hp=2,idle,1.800) | setup
t=1.000 frame=30 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.84,1.79,hp=2,approach,0.000) grub#1(1.94,5.51,hp=2,approach,0.000) grub#2(5.41,6.59,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,charge,0.800) spitter#4(15.00,8.00,hp=2,idle,0.800) | charge {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}
t=1.800 frame=54 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(4.31,2.42,hp=2,approach,0.000) grub#1(3.49,5.13,hp=2,approach,0.000) grub#2(6.55,5.45,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,recovery,0.600) spitter#4(15.00,8.00,hp=2,charge,0.800) | spit {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.233 frame=67 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(5.11,2.76,hp=2,approach,0.000) grub#1(4.33,4.92,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,windup,0.500) spitter#3(15.00,0.00,hp=2,recovery,0.167) spitter#4(15.00,8.00,hp=2,charge,0.367) | windup {'who': 2, 'side': 'bottom left, 1 tile'}
t=2.600 frame=78 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(5.78,3.05,hp=2,approach,0.000) grub#1(5.04,4.74,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,windup,0.133) spitter#3(15.00,0.00,hp=2,idle,0.900) spitter#4(15.00,8.00,hp=2,recovery,0.600) | spit {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.733 frame=82 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.02,3.15,hp=2,approach,0.000) grub#1(5.30,4.67,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,strike,0.150) spitter#3(15.00,0.00,hp=2,idle,0.767) spitter#4(15.00,8.00,hp=2,recovery,0.467) | strike {'who': 2}
t=2.800 frame=84 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=2 | grub#0(6.15,3.21,hp=2,approach,0.000) grub#1(5.43,4.64,hp=2,approach,0.000) grub#2(7.43,4.57,hp=2,strike,0.083) spitter#3(15.00,0.00,hp=2,idle,0.700) spitter#4(15.00,8.00,hp=2,recovery,0.400) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'bottom left, 1 tile'}
t=2.900 frame=87 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=2 | grub#0(6.33,3.28,hp=2,approach,0.000) grub#1(5.63,4.59,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,recovery,0.883) spitter#3(15.00,0.00,hp=2,idle,0.600) spitter#4(15.00,8.00,hp=2,recovery,0.300) | recover {'cause': 'strike', 'who': 2, 'side': 'left'}
t=3.233 frame=97 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.500) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.550) spitter#3(15.00,0.00,hp=2,idle,0.267) spitter#4(15.00,8.00,hp=2,idle,1.067) | windup {'who': 0, 'side': 'left, 1 tile'}
t=3.500 frame=105 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.100 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.233) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.283) spitter#3(15.00,0.00,hp=2,charge,0.800) spitter#4(15.00,8.00,hp=2,idle,0.800) | charge {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}
t=3.600 frame=108 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.133) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.183) spitter#3(15.00,0.00,hp=2,charge,0.700) spitter#4(15.00,8.00,hp=2,idle,0.700) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.733 frame=112 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,strike,0.150) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.050) spitter#3(15.00,0.00,hp=2,charge,0.567) spitter#4(15.00,8.00,hp=2,idle,0.567) | strike {'who': 0}
t=3.800 frame=114 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=2 | grub#0(7.26,3.68,hp=2,strike,0.083) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,waiting-spacing,0.000) spitter#3(15.00,0.00,hp=2,charge,0.500) spitter#4(15.00,8.00,hp=2,idle,0.500) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'left, 1 tile'}
t=3.900 frame=117 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.883) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,waiting-spacing,0.000) spitter#3(15.00,0.00,hp=2,charge,0.400) spitter#4(15.00,8.00,hp=2,idle,0.400) | recover {'cause': 'strike', 'who': 0, 'side': 'left, 1 tile'}
t=4.233 frame=127 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.367 stun_left=0.000 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.550) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,windup,0.500) spitter#3(15.00,0.00,hp=2,charge,0.067) spitter#4(15.00,8.00,hp=2,idle,0.067) | windup {'who': 2, 'side': 'left, 1 tile'}
t=4.300 frame=129 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 shots=3 | grub#0(7.77,3.90,hp=2,recovery,0.483) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,windup,0.433) spitter#3(15.00,0.00,hp=2,recovery,0.600) spitter#4(15.00,8.00,hp=2,charge,0.800) | spit {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=4.600 frame=138 room=5 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0, 'spitter': {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}}; down
t=5.400 frame=162 room=5 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.600 frame=198 room=5 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | run_over {'rooms': 0, 'complete': False}
t=6.600 frame=198 room=5 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | end
```

### Round 2: @run/trace/room5-still-60 — `python3 play.py --view trace {script}`

Script:

```text
fps 60
room 5
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(1.00,1.00,hp=2,approach,0.000) grub#1(0.00,6.00,hp=2,approach,0.000) grub#2(4.00,8.00,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,1.000) spitter#4(15.00,8.00,hp=2,idle,1.800) | setup
t=1.000 frame=60 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(2.84,1.79,hp=2,approach,0.000) grub#1(1.94,5.51,hp=2,approach,0.000) grub#2(5.41,6.59,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,charge,0.800) spitter#4(15.00,8.00,hp=2,idle,0.800) | charge {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}
t=1.800 frame=108 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(4.31,2.42,hp=2,approach,0.000) grub#1(3.49,5.13,hp=2,approach,0.000) grub#2(6.55,5.45,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,recovery,0.600) spitter#4(15.00,8.00,hp=2,charge,0.800) | spit {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.217 frame=133 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=1 | grub#0(5.07,2.75,hp=2,approach,0.000) grub#1(4.30,4.92,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,windup,0.500) spitter#3(15.00,0.00,hp=2,recovery,0.183) spitter#4(15.00,8.00,hp=2,charge,0.383) | windup {'who': 2, 'side': 'bottom left, 1 tile'}
t=2.600 frame=156 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(5.78,3.05,hp=2,approach,0.000) grub#1(5.04,4.74,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,windup,0.117) spitter#3(15.00,0.00,hp=2,idle,0.900) spitter#4(15.00,8.00,hp=2,recovery,0.600) | spit {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=2.717 frame=163 room=5 phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(5.99,3.14,hp=2,approach,0.000) grub#1(5.27,4.68,hp=2,approach,0.000) grub#2(7.12,4.88,hp=2,strike,0.150) spitter#3(15.00,0.00,hp=2,idle,0.783) spitter#4(15.00,8.00,hp=2,recovery,0.483) | strike {'who': 2}
t=2.767 frame=166 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=2 | grub#0(6.09,3.18,hp=2,approach,0.000) grub#1(5.37,4.66,hp=2,approach,0.000) grub#2(7.35,4.65,hp=2,strike,0.100) spitter#3(15.00,0.00,hp=2,idle,0.733) spitter#4(15.00,8.00,hp=2,recovery,0.433) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'pos': 'bottom left, 1 tile'}
t=2.867 frame=172 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=2 | grub#0(6.27,3.26,hp=2,approach,0.000) grub#1(5.56,4.61,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,recovery,0.900) spitter#3(15.00,0.00,hp=2,idle,0.633) spitter#4(15.00,8.00,hp=2,recovery,0.333) | recover {'cause': 'strike', 'who': 2, 'side': 'left'}
t=3.217 frame=193 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.500) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.550) spitter#3(15.00,0.00,hp=2,idle,0.283) spitter#4(15.00,8.00,hp=2,idle,1.083) | windup {'who': 0, 'side': 'left, 1 tile'}
t=3.500 frame=210 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.067 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.217) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.267) spitter#3(15.00,0.00,hp=2,charge,0.800) spitter#4(15.00,8.00,hp=2,idle,0.800) | charge {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}
t=3.567 frame=214 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,windup,0.150) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.200) spitter#3(15.00,0.00,hp=2,charge,0.733) spitter#4(15.00,8.00,hp=2,idle,0.733) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=3.717 frame=223 room=5 phase=playing pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=2 | grub#0(6.85,3.51,hp=2,strike,0.150) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,recovery,0.050) spitter#3(15.00,0.00,hp=2,charge,0.583) spitter#4(15.00,8.00,hp=2,idle,0.583) | strike {'who': 0}
t=3.767 frame=226 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=2 | grub#0(7.16,3.64,hp=2,strike,0.100) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,waiting-spacing,0.000) spitter#3(15.00,0.00,hp=2,charge,0.533) spitter#4(15.00,8.00,hp=2,idle,0.533) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1, 'pos': 'left, 1 tile'}
t=3.867 frame=232 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.050 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.900) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,waiting-spacing,0.000) spitter#3(15.00,0.00,hp=2,charge,0.433) spitter#4(15.00,8.00,hp=2,idle,0.433) | recover {'cause': 'strike', 'who': 0, 'side': 'left, 1 tile'}
t=4.217 frame=253 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.350 stun_left=0.000 shots=2 | grub#0(7.77,3.90,hp=2,recovery,0.550) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,windup,0.500) spitter#3(15.00,0.00,hp=2,charge,0.083) spitter#4(15.00,8.00,hp=2,idle,0.083) | windup {'who': 2, 'side': 'left, 1 tile'}
t=4.300 frame=258 room=5 phase=playing pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.267 stun_left=0.000 shots=3 | grub#0(7.77,3.90,hp=2,recovery,0.467) grub#1(6.06,4.49,hp=2,waiting-cap,0.000) grub#2(7.82,4.18,hp=2,windup,0.417) spitter#3(15.00,0.00,hp=2,recovery,0.600) spitter#4(15.00,8.00,hp=2,charge,0.800) | spit {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}; charge {'who': 4, 'spot': 'bottom right', 'dup': False, 'n': 2}
t=4.567 frame=274 room=5 phase=down pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.150 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 0, 'spitter': {'who': 3, 'spot': 'top right', 'dup': False, 'n': 1}}; down
t=5.367 frame=322 room=5 phase=down pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=6.567 frame=394 room=5 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | run_over {'rooms': 0, 'complete': False}
t=6.567 frame=394 room=5 phase=over pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(7.77,3.90,hp=2,approach,0.000) grub#1(6.06,4.49,hp=2,approach,0.000) grub#2(7.82,4.18,hp=2,approach,0.000) spitter#3(15.00,0.00,hp=2,idle,0.000) spitter#4(15.00,8.00,hp=2,idle,0.000) | end
```

### Round 2: @run/play/room2-view-30 — `python3 play.py --view player {script}`

Script:

```text
fps 30
room 2
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 2 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (top left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.300  YOU ARE HIT by a grub (left) — hearts 2/3
   [3.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       GP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (left)
   [3.40 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.733  a grub rears back (top right)
   [3.73 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.300  YOU ARE HIT by a grub (right) — hearts 1/3
   [4.30 s] hearts 1/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.383  the grub is open (right)
   [4.40 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.733  a grub rears back (left)
   [4.73 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  5.267  YOU ARE HIT by a grub (left) — hearts 0/3
  5.267  you went down
   [5.27 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
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
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```

### Round 2: @run/play/room2-view-60 — `python3 play.py --view player {script}`

Script:

```text
fps 60
room 2
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 2 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (top left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.283  YOU ARE HIT by a grub (left) — hearts 2/3
   [3.28 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       GP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (left)
   [3.38 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.733  a grub rears back (top right)
   [3.73 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.283  YOU ARE HIT by a grub (top right) — hearts 1/3
   [4.28 s] hearts 1/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.383  the grub is open (right)
   [4.38 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.733  a grub rears back (left)
   [4.73 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  5.250  YOU ARE HIT by a grub (left) — hearts 0/3
  5.250  you went down
   [5.25 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
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
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```

### Round 2: @run/bots/g-comment — `python3 bots.py {script}`

Script:

```text
# usage?
```

Exit: 0 (0.1 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
camper   room 2: cleared in 4.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
camper   room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper   room 4: NOT cleared (6.9 s); hearts lost 3 (hit by: shot 3); attacks 4, dashes 0
camper   room 5: NOT cleared (6.9 s); hearts lost 3 (hit by: shot 3); attacks 6, dashes 0
camper   total: cleared 2/5, hearts lost 9, dashes 0
walker   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   room 2: cleared in 5.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
walker   room 3: cleared in 9.0 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   room 4: cleared in 9.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
walker   room 5: cleared in 11.2 s; hearts lost 0 (hit by: none); attacks 10, dashes 0
walker   total: cleared 5/5, hearts lost 0, dashes 0
dodger   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
dodger   room 2: cleared in 5.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 0
dodger   room 3: cleared in 11.8 s; hearts lost 0 (hit by: none); attacks 6, dashes 4
dodger   room 4: cleared in 10.0 s; hearts lost 0 (hit by: none); attacks 8, dashes 1
dodger   room 5: cleared in 9.8 s; hearts lost 0 (hit by: none); attacks 10, dashes 2
dodger   total: cleared 5/5, hearts lost 0, dashes 7
reactive room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
reactive room 2: cleared in 6.7 s; hearts lost 0 (hit by: none); attacks 9, dashes 2
reactive room 3: cleared in 11.8 s; hearts lost 0 (hit by: none); attacks 6, dashes 4
reactive room 4: cleared in 12.9 s; hearts lost 0 (hit by: none); attacks 9, dashes 5
reactive room 5: cleared in 11.1 s; hearts lost 0 (hit by: none); attacks 11, dashes 2
reactive total: cleared 5/5, hearts lost 0, dashes 13
```

### Round 2: @run/bots/g-help — `python3 bots.py {script}`

Script:

```text
help
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'help'
```

### Round 2: @run/bots/g-eq — `python3 bots.py {script}`

Script:

```text
room=1 fps=30
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room=1 fps=30'
```

### Round 2: @run/bots/g-num — `python3 bots.py {script}`

Script:

```text
1 30
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read '1 30'
```

### Round 2: @run/bots/g-rooms — `python3 bots.py {script}`

Script:

```text
rooms 1
```

Exit: 0 (0.0 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
camper   total: cleared 1/1, hearts lost 0, dashes 0
walker   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
walker   total: cleared 1/1, hearts lost 0, dashes 0
dodger   room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
dodger   total: cleared 1/1, hearts lost 0, dashes 0
reactive room 1: cleared in 3.5 s; hearts lost 0 (hit by: none); attacks 6, dashes 0
reactive total: cleared 1/1, hearts lost 0, dashes 0
```

### Round 2: @run/bots/g-play — `python3 bots.py {script}`

Script:

```text
play room 1 fps 30
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'play room 1 fps 30'
```
>>>END
