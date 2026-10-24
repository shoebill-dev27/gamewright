# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/72-studio-to-game-designer.md
next_seq: 73
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/73-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-014-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-combat-monotony/72-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 72
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 72: studio → game-designer — Close three spec gaps found by Verify (cell rounding at .5, "on you", hit-line position word)

## Task

Settle three rule/display gaps that QA's verification (70) hit, so that the engineer can fix the build with no judgment calls. Write the rulings into `design/combat.md` and, where wording of V items must change, `design/combat-visuals.md`, with player-observable acceptance criteria that read the same at 30 and 60 FPS.

## Context

G-001 (combat feels monotonous), Option A (D-002). The change set AC-19…AC-28 and V-9…V-17 is built. QA's verification at 30 and 60 FPS failed (70). Besides the gaps below, QA found a suite failure (`CrowdTest.test_hit_stun_is_short`, fails at both rates while QA's traces show the rule correct) and a manual gap (V-15). The engineer takes those in the next Build, together with your rulings. This step is only for the three spec gaps. No criterion in this list has failed before (AC-19…AC-28 and V-9…V-17 are new), so this is the first Design return for them.

## Findings

All data is from QA's report (70, §2). Setups use the project's scripts (`python3 play.py --view player {script}`, `--view trace`).

**Gap 1 (D-A): how a position becomes a cell at exactly .5 tile.** Display fails at 30 FPS only; it matches the true positions at 60 FPS.
```
fps 30
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```
- True positions (trace, 30 FPS): the grub is knocked left, to x=14.33 and then 13.50, which is 1.0 tile left of the player, inside the room, as AC-28(b) and D-013 require. It winds up with `side: left` and strikes with `pos: left`.
- Player view (30 FPS): the draws at 0.50, 0.80, 1.00 and 1.33 s show `on you: w open (shown right)` / `on you: W biting soon (shown right)` with the glyph right of `P`, until about 1.45 s. The text lines in the same draws say "(left)". The picture and the text contradict each other.
- At 60 FPS: 0.50 s shows `wP` with no `on you:` line, 0.80 s shows `WP`, matching the text.
- QA's reading (not verified): the grub rests exactly on a half-tile boundary (x=13.5), so its drawn cell differs between frame rates. The spec has no rule for cells at exactly .5.

**Gap 2 (D-B): what "same tile as the player / on you" means.** V-12 and "Position words" say "same tile as the player: on you". The spec does not say whether that is true-position based or drawn-cell based.
- Room 2, `room 2`, `end 6`, at both frame rates: at 3.383 the text line reads "the grub is open (left)" while the draw at 3.40 shows `on you: g open (shown left)`; the same at 4.383 with "(right)" and `on you: … g open (shown right)`.
- The text word comes from the true position (about 0.2 tile away, so "left"); the `on you:` entry and the displaced glyph come from cell equality. A reader sees both "(left)" and an on-you entry for the same grub.

**Gap 3 (D-C): which position the hit-line word names.** V-14 says the hit line names the attacker's position; V-16 asks for identity across 30 and 60 FPS.
- Room 2 around 4.3 s. 30 FPS: "YOU ARE HIT by a grub (right)" at 4.300 (trace `pos: right`, grub at 8.67, 3.55); the draw just before (4.00) shows `G` at the top right. 60 FPS: "(top right)" at 4.283 (grub at 8.76, 3.49); the draw before shows `G` at the top right, so it matches.
- The word is taken from the lunge position at the damage tick, which differs between frame rates. At 30 FPS the named position does not match the uppercase glyph the player saw before the hit. The scripted left/right case of V-14 passes at both rates.

**Also relevant, no action required unless you want one:**
- Strike cancel (D-58-1, AC-26) at 30 FPS: the cancel window is one tick (0.033 s at 30 FPS, 0.017–0.033 s at 60 FPS). It matches the written rule; the designer may want to know it is this narrow.
- AC-21 passes with a thin margin: first to third heart 1.97 s at both rates, limit 1.9 s.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-005, D-007: the Owner places `manual.md` text. Do not edit `manual.md`.
- D-011: grubs take turns, crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line for displaced enemies; hit lines name the attacker's position.
- D-013: a grub on the player's tile is knocked back toward the side it is drawn on.

## Constraints

- The rulings must give identical displayed positions and position words at 30 and 60 FPS (the project must play correctly at both).
- Do not change parameters or behavior that QA saw pass (AC-2, 4, 5, 7, 11, 19, 21, 23–27, AC-28 a/d/e) unless a ruling cannot avoid it; list any such change explicitly.
- Prefer rules that reuse the existing systems (small team). No new inputs or screens.
- Keep "Readable threats" (pillar 3): a threat must be visible before it can hurt, and the picture and text lines must never contradict each other.
- If you judge a ruling to be mainly a visual/display call, decide it within the existing V items and the project's art direction. The art-director reviews the wording at Verify. If you cannot decide it within your authority, hand back with the reason; do not leave it open.

## Open questions

1. **Cell rule at .5 (Gap 1).** State a frame-rate-independent rule for how a position maps to a cell and to the shown side, including exact half-tile positions, and say how it applies to AC-28(b)/D-013 (knockback ends 1.0 tile left, so the grub must read as left of `P`).
2. **"On you" (Gap 2).** Define it once, for all uses (`on you:` entry, displaced glyph, position word in text lines, "(on you)" in the player's own hit line). Say how a grub about 0.2 tile away reads in the text, in the `on you:` line and in the picture, so no draw shows both a side word and an on-you entry for the same enemy.
3. **Hit-line word (Gap 3).** Say which position the hit line names (damage-tick position or the glyph position the player last saw) and how it stays consistent with the draw before the hit at both frame rates.
4. **Consequences.** List the AC and V items whose wording or criteria you changed (expected: AC-17, AC-28(b), V-10, V-12, V-14, V-16) so QA re-verifies exactly those, and whether the existing manual draft (65 and the proposal in 71) still holds. If position words or on-you wording changed, give the final text lines the Owner should place for V-15 (the Owner places them; you do not edit `manual.md`).
5. Record a Decision (`make-decision`) if a ruling constrains later work or rejects a real alternative.

## Expected output

Updated `design/combat.md` and, if needed, `design/combat-visuals.md`; a Decision if warranted; and a handoff addressed to `studio` (so the Studio can compose the Build step) that lists the rulings, the changed criteria, the items QA must re-verify, any previously passing behavior your rulings change, and the final V-15 manual lines if they changed. The next step is Build (`gameplay-engineer`), taking these rulings plus the failing suite test and the display defects from 70.

## Sender assessment

None (written by the Studio for routing).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, repo/game.py (read-only, to see the current rounding; the engineer changes code)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/70-qa-to-studio.md
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
runs: play, bots
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
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

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
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
