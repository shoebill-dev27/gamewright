# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/56-studio-to-game-designer.md
next_seq: 59
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/59-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-011-<name>.md
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

<<<FILE goals/G-001-combat-monotony/56-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 56
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 56: studio → game-designer — Update the spec with A1, A2, A3, A5 and draft the manual changes

## Task

Specify the cheap fixes from your diagnosis (53) in `design/combat.md`: A1 wind-up spacing, A2 shorter stun, A3 body-hit rule, and the A5 gaps (dash and facing; the distance-0 swipe rule if A3 is not taken). Give each player-observable acceptance criteria that hold at 30 and 60 FPS. Also draft the group B manual changes.

## Context

G-001 (combat monotony), Option A (D-002). Your diagnosis (53) put the harshness of rooms 1–2 down to rules and tuning that your authority covers. The second playtest (54) agrees: in room 2, four grubs arrived together, reared back about 0.3 s apart, ended up in a ring around the player and bit in turns; the player was down in about 6 s and one swipe hit one of three adjacent grubs. Grubs on the player's tile were also hard to read (see handoff 57 for the display side). QA is checking the dash distance, facing and swipe cases in parallel (55); its results arrive after this step and may add defects, so settle the unspecified cases by rule, not by what the build happens to do.

Studio decision on routing: D1 (facing change) and D2 (room 1 composition) are not routed to the director now, as you recommended.

## Findings

Points to cover beyond 53:

- Check A1 against the room 2 ring: with four grubs, does spacing plus A3 let a player escape or counter, or should some limit on grubs adjacent to the player also be considered? Decide within your authority.
- A4 (cone width) stays held back. State what result of a retest would bring it in.
- Manual draft (group B): the interrupt, the knockback, the dash distance, the hit stun, and clearer wording for a swipe that is too far. Draft it as text in your outgoing Handoff for the Owner to place (D-005, D-007 pattern); do not edit `manual.md`. Keep the phrases that `ManualTest` checks (D-009).
- A guideline for the retest: say what a skilled player should be able to do in room 1 and room 2, qualitatively, so the next Play and Review have something to judge against. Numeric thresholds only as acceptance criteria.

## Decisions already made

- D-001: one attack button plus dash; no new input without the Owner.
- D-002: Option A first; staggered arrival (part of B) deferred.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.

## Constraints

- All timings in seconds; hold at 30 and 60 FPS.
- Reuse existing systems (small team).
- Record a Decision (`make-decision`) for the A1–A3 package, since it constrains the build and Verify, including the alternatives you rejected (A4, D1, D2) and when to revisit.
- If you conclude the cheap fixes cannot work without a facing mechanic or a room composition change, hand back to `studio` with the reason; that goes to `game-director`.

## Open questions

- Does A1 alone handle the ring of grubs in room 2, or is a second rule needed?
- What should the dash do to facing?

## Expected output

An updated `design/combat.md` (new acceptance criteria numbered after AC-18), a Decision, the manual draft and a retest guideline. Outgoing Handoff addressed to `studio` (it routes to Build, and to the Owner if the manual changes).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md, design/combat-visuals.md, manual.md, project.md#constraints, goals/G-001-combat-monotony/54-playtester-to-studio.md (the second playtest report)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md
- Previous handoff: goals/G-001-combat-monotony/53-game-designer-to-studio.md
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE goals/G-001-combat-monotony/54-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 54
from: playtester
to: studio
stage: Play
outcome: done
---
# 54: playtester → studio — Observation report: room 2 by script, little else reached

## Task

Report what a first-time player experienced in the later rooms and with enemies other than the first room's grub, paying attention to combat.

## Context

Handoff 52 asked for a play session over the unseen parts of the game. I played by input script only (`python3 play.py --view player {script}`, using only the manual). Live play was not available. I used one scripted run. It was a blind script, so I could not react to the screen mid-run. The result is thin, and I say below what I did not see.

## Findings

### Method

- One scripted run: `room 2`, 30 fps, 20 s. The script was a swipe at 1 s, move right at 3 s, stop at 5 s, swipe at 5.5 s, dash left at 8 s, swipe at 10 s.
- I chose the moves in advance from the manual, so nothing was adjusted to what was on screen.
- I did not use the remaining run rounds. This report rests on that single run.

### What I saw and did not see

- **Seen:** the opening of room 2. It had four grubs, all `g`, placed around the edges. They drifted toward me from all sides and ended up around my tile.
- **Seen by accident:** room 1 again. My swipe at 10 s came after I went down, and "press attack to start again" restarted the run in room 1. It had three grubs. I did nothing there but stand still, and I went down at 14.97 s.
- **Not seen:**
  - rooms 3, 4 and 5 (I never cleared a room, "rooms cleared: 0" both times);
  - any spitter, so no `S`/`Z` charge, no `*` shot, and no "staggered";
  - a "room cleared" heal;
  - "run complete".
- **Never exercised:** the dash. It fired at 8 s, after I was already down, so I learned nothing about how it feels. I have no opinion on dash timing or recharge.
- **Reached with the manual's means:** `room 3`–`room 5` can be selected by script. I did not try them. I should have, since that is the direct way to see the later rooms and any spitters. This is the main gap in my report.

### Concrete moments (room 2, standing mostly still)

- 0–2.5 s: four grubs walked in from the corners and edges. Nothing was dangerous, and it was calm and readable. My early swipe at 1.0 s hit nothing ("(miss)") because everything was far away. That is my script's fault, not the game's.
- 2.73 s: "a grub rears back (left)", and the `G` showed up top-left of me. At 3.0 s a second one reared back on the right. Two threats were on screen within about 0.3 s of each other. The text cue and the capital `G` were easy to read.
- 3.38 s: "the grub is open (left)". I was not swiping then, so I missed the chance to counter.
- 3.57 s: first hit, 3/3 → 2/3. The attacker was a grub that had reared back about half a second earlier. I could have dodged, but my script could not react.
- 4.0–5.2 s: grubs sat directly left and right of me, taking turns biting. The log shows "open" and "rears back" calls every few tenths of a second. It felt like I was standing in a ring of grubs with no gap to leave through.
- 5.07 s: hit, 2/3 → 1/3.
- 5.5 s: my swipe hit one grub ("grub hit (1 left)"). A grub is therefore a two-hit enemy, and my swipe landed on only one of the three adjacent grubs.
- 5.87 s: hit again and down. Three hits, about 2.3 s after the first bite began, and no room cleared.
- Room 1 repeat, 11.4–14.97 s: the same pattern with three grubs. I was hit at 11.97 s, 13.47 s and 14.97 s and went down. In both runs I died without clearing anything, but I also did not try to play it.

### Did the fights feel different from each other?

Room 1 and room 2 fought the same way: grubs close in, rear back, bite and open up. Room 2 simply had one more grub. I cannot say anything about rooms 3–5 or other enemy types.

### Did my choices matter?

I can't judge this fairly, because I never reacted. Visible signs that they could matter:

- Each bite is announced by a "rears back" line, a capital `G`, and a delay of roughly half a second before the hit. That is enough time to dash or step away.
- A grub is "open" after biting, which invites a counter-swipe.

Signs that choices could matter less than they should:

- Several grubs arrive together and cycle their bites, so there always seems to be one about to bite. It felt like an "avoid the next bite" loop rather than a back-and-forth.
- The swipe only reaches a little more than one tile. With grubs on both sides, one swipe hit one grub.

### Unclear, unreadable or possibly unfair

- **Possibly short warning (medium, uncertain):** at 11.90 s the log shows "a grub rears back (left)" and the hit at 11.97 s. That is only about 0.07 s later. The other bites I could trace came about 0.5–0.65 s after their rear-back line. I can't tell if this was a different grub's earlier wind-up whose line I misattributed, or a real short warning. If real, it would be impossible to react to and would feel unfair.
- **Grubs on my tile (low–medium):** several lines read "the grub is open (on you)" or "rears back (on you)". Grubs seem to be able to stack on my tile. The screen then draws them beside me, so I could not tell which side the bite would come from, or where to swing. For an action player who relies on spacing, that is confusing.
- **Cornered (medium):** with grubs on both sides I was boxed in. I couldn't tell whether I could have walked out, since I did not try.

### Broken

Nothing was clearly broken in what I saw. The 11.97 s hit timing above is the one thing worth a second look.

### Positives

- The text cues ("rears back (left)", "the grub is open") and the capital/lowercase marks made it easy to follow what each grub was doing.
- The restart flow worked: after "run over", attack began a fresh run in room 1 with full hearts.
- Runs are short. I went down in about 6 s in room 2 and about 5 s in room 1, which suits a player who wants short, intense runs.

### Open player questions

- How are the later rooms different? Do they have spitters, and how many grubs?
- Can I dash out of the ring of grubs and counter from outside? I never tested it.
- Is the very short warning at 11.9 s real?

## Decisions already made

None.

## Constraints

I used only the player view and the manual. I read no source, tests or design files, and did not use the trace view or the bots.

## Open questions

- Please route a follow-up session that plays `room 3`, `room 4` and `room 5` directly, ideally live or with several short reactive scripts. It should dash and counter-swipe on the "rears back" cues, and it should place spitters with `room empty` if they are not in the early rooms. This report does not cover later rooms, spitters or the dash.

## Expected output

This report goes to `studio`, which decides whether to route a follow-up play session and whether to pass the experience issues to `game-designer` and the possibly short bite warning to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-playtester.md
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

<<<FILE goals/G-001-combat-monotony/53-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 53
from: game-designer
to: studio
stage: Route
outcome: done
---
# 53: game-designer → studio: Diagnosis of the room-1 play findings (handoff 51)

## Task

Route the options below by authority. `game-director` needs to decide the two items in group D, and the Studio should schedule one cheap re-check (see Expected output). The spec is not edited in this step.

## Context

G-001 (combat monotony), Option A (D-002). The playtester (50) went down twice in room 1 and saw nothing past it. This is my diagnosis from the report, the spec (`design/combat.md`, `design/combat-visuals.md`), `manual.md` and two runs.

**What I could and could not check.** I had no `run_trace` and no usable bot run.
- The `run_bots` round failed: `script line 1: cannot read 'room 1'`. The bots script format is not the play-script format, and no rounds are left. There is therefore **no passive-bot or active-bot reference**.
- I used two `run_play` scripts instead: a still player in room 1 (`room1-still`) and a one-grub probe in the practice room (`wind-up-swipe`).
- Everything about "how a competent player fares" is reasoning, not measurement.

## Findings

### 1. What the runs show

**Still player, room 1** (60 FPS). Hearts are lost at 1.93, 3.43 and 4.95 s, and the player goes down at 4.95 s.
- This matches the spec note "idle player down at about 5 s".
- The bites are 1.5 s apart. Several strikes (about 2.4–2.5 s, 4.0–4.2 s) fall inside the 0.8 s post-hit invulnerability and are absorbed.
- Wind-ups overlap as the report says: 2.883 and 2.933 s, and 3.53 s (left) overlapping the "above" grub's strike. Never more than 2 are committed at once, so the attack limit (AC-6) holds.
- All three grubs arrive within about 1.5 s of each other (rear-backs at 1.38, 1.88 and 2.88 s) because they start about the same distance away. That is why room 1 produces simultaneous threats.

**Swipe on a rearing grub** (practice room, one grub). A swipe 0.27 s into a wind-up (1.05 s):
- prints "grub hit (1 left)" and "the grub is open";
- the glyph drops from `G` to `w`;
- no heart is lost to that bite (AC-5 interrupt works).

The grub is **hittable during wind-up**. The tester's guess in 50 ("probably not hittable") is wrong, and the manual never says so.

**The "(miss)" results.** In my probe the two misses (1.5 s, 2.0 s) happened because the first hit knocked the grub back 1 tile. It stood about 2 tiles away, outside the 1.5-tile reach. "(miss)" was truthful.
- The tester's misses at 2.1 s and 4.0 s may be the same effect, or a facing error, or a swipe during Strike.
- My probe did **not** test a swipe during Strike or an adjacent Recovery. That case is unsettled.

### 2. Classification of the findings

| Finding | Spec-conforming? | Class |
|---|---|---|
| Loop is identical in room 1 | Yes. Room 1 is a teaching room (D-003) | Open: see §3 |
| Simultaneous rear-backs (0.03–0.05 s apart) | Yes. The limit is 2 at once, with no spacing rule | **Tuning / rule gap** |
| 3 hearts gone fast | Yes. The bites are at least 1.5 s apart for a still player, and 0.8 s apart after invulnerability for a moving one | **Tuning** (stacks with the rows above and below) |
| Stun 0.3 s blocks the counter | Yes, spec text | **Tuning** (sharpest complaint) |
| Swipe hits a winding-up grub; the tester thought it can't | The spec is fine, the manual is silent | **Manual** |
| Swipe "(miss)" next to a grub | Probably knockback or facing; "(miss)" is truthful | **Readability** (cause not fully settled) |
| Cannot turn without moving; swipes hit air after a dash | Yes. Facing is move-only | **Direction** (D-001 / facing) |
| Dash end point unclear; felt like 2–3 tiles | Spec says 4 tiles | **Unknown**: possible as-built difference or wall clamp. Needs `run_trace`. The manual gives no distance |
| Grub "on you" drawn beside `P` | Yes (D-006) | **Display / readability** |

### 3. Causes (design terms)

1. **No spacing between grub commitments.** The spec limits grubs to 2 in Wind-up/Strike but sets no minimum gap between wind-up starts. Three grubs with equal start distance converge together, so one safe response (step or dash) covers one grub. The 0.8 s invulnerability absorbs some bites but not enough to make this read as skill.
2. **Stun 0.3 s overlaps the counter window.** The best answer to a wind-up is to hit the grub in it (interrupt), but hit-stun removes that answer right after a hit. The wind-up is 0.5 s, so a 0.3 s stun leaves about 0.2 s. This explains the "unfair" feeling in 50.
3. **The best tools are not taught.** The manual says "step away or dash" for a wind-up and does not mention the interrupt, the knockback after a hit (grub ends about 2 tiles away, out of reach), or the dash distance. The tester therefore concluded the grub is unhittable.
4. **Facing is move-only, with unspecified edge cases.** Two spec gaps:
   - The spec does not say whether a dash changes facing.
   - The spec does not say whether an enemy at distance about 0 (a grub "on you") is inside the 90° cone, since it has no direction.

   Both feed the "I couldn't hit what was next to me" feeling.
5. **Monotony vs harshness.** In ~10 s of play every grub did the same loop. That is expected in a teaching room and does not show that monotony is solved or still present, because the tester died before any variation (rooms 2–5, spitter). Harshness is now masking the question. Only a survived run (52) can answer it.

### 4. Options

**A. Mine: rules and tuning (game-designer authority; changes the spec in the next step)**

- **A1. Wind-up spacing.** A grub may not start a Wind-up within 0.5 s of another grub's Wind-up start. This reuses the spitter stagger idea.
  - Addresses: pressure, simultaneous rear-backs.
  - Cost: a small rule. It must hold at 30 and 60 FPS (use seconds).
  - Risk: cluster fights become longer. It does not change the single-grub cycle.
  - Fit: pillar 3. No D-001 effect.
- **A2. Shorter stun.** 0.3 s → 0.15 s **[tune]**, or keep 0.3 s but let the swipe buffer and fire when the stun ends.
  - Addresses: the "can't hit back" frustration.
  - Risk: low. The invulnerability time is unchanged.
- **A3. Body hit rule.** An enemy within about 0.5 tile of the player (the "on you" case) is always hit by a swipe, regardless of facing.
  - Addresses: "on you" confusion and part of the facing complaint.
  - It does not change how the player turns.
- **A4. Cone width.** 90° → about 120° **[tune]** for more forgiveness.
  - Cost: low. Risk: it weakens positioning, so try it only if A3 is not enough.
- **A5. Spec gaps to close either way:** whether a dash changes facing, and the exact distance-0 swipe rule if A3 is not taken.

**B. Manual and clarity (no rule change; the Studio decides who edits `manual.md`)**

- State that a swipe during a rear-back cancels the bite (the best counter).
- State that a first hit knocks the grub back about a tile, so a follow-up may need a step forward.
- State the dash distance (about 4 tiles) and that a hit stuns for a moment.
- Add "(too far)" or similar wording to "(miss)" for a swipe when an enemy is within about 2.5 tiles. This is a display text matter.

**C. Art-director (display)**

- "On you" readability. Suggestion: the text line could name where the glyph is drawn ("open, on you, drawn right"), or the displaced glyph could be marked. This does not change D-006.
- Review whether "YOU ARE HIT by a grub" should say which grub (left or above).

**D. Needs `game-director` (not mine to choose)**

- **D1. Facing.** The tester's request ("turn without moving" or "swipe behind you") conflicts with D-001 for a new input. Variants that change the facing mechanic are all direction decisions:
  - Auto-face the nearest enemy on swipe.
  - A dash that keeps facing (a "backstep").
  - A 360° swipe.
  
  I recommend trying A3 and A4 first and escalating this only if the tester still reports it.
- **D2. Room 1 composition.** Options:
  - Fewer grubs. This breaks the spec's "3–6 enemies per room".
  - Uneven grub start distances. This is the "staggered arrival" that D-002 defers as part of Option B.
  
  A1 reaches a similar effect inside Option A, so I do not need either of these now.

### 5. Trade-offs in short

- A1 + A2 + A3 are cheap and keep the Option A reading (one telegraph, one answer). They may leave a still player's time-to-down near 5 s, which is fine because that is a reference value, not a target.
- B is nearly free and should happen regardless. The tester's central confusion (unhittable while winding up) is a manual gap.
- D1 and D2 are bigger changes. Taking them before the cheap fixes would change scope or direction on one session of scripted play.

## Decisions already made

- D-001: one attack button plus dash. A turn-without-moving input is not allowed without the Owner.
- D-002: Option A first; B (including staggered arrival) deferred.
- D-003: room mix is across rooms; zero hearts ends the run; clear heals 1.
- D-006: enemies may overlap the player and are never hidden.

## Constraints

- Everything stays within D-001. All timings are in seconds and must hold at 30 and 60 FPS.
- This note contains design-side reasoning. Do not forward it to a Playtester unchanged; give them only what they need to play.

## Open questions

- **Dash distance.** Does the as-built dash go 4 tiles? The tester saw 2–3. Needs `run_trace` (QA or the engineer).
- **Swipe during Strike or an adjacent Recovery.** Does it hit? My probe did not test it.
- **Does a dash change facing?** The spec is silent.
- **Can a skilled player survive room 1?** I have no bot data (the bots script failed). The next run should find the bots script format first.
- **Monotony.** Is it still present once players survive? Waiting for 52 (rooms 2–5, spitter).

## Expected output

The Studio, in order:

1. Route group D to `game-director` only if wanted now. My recommendation is not to.
2. Send group B to whoever owns the manual, and group C to `art-director`.
3. Next step for me: a design-spec update with A1, A2, A3 and A5 (A4 held back). It must also state the new acceptance criteria and keep the 30/60 FPS requirement.
4. After that, one new playtest of room 1 and one bots round with a correct script format (a passive bot and a reactive bot), to see whether room 1 is survivable.

## Sender assessment

**Recommendation:** A1 + A2 + A3 together, plus B and C. Hold D until a retest.

- **Confidence in the causes:**
  - High: the lack of spacing (confirmed in the still run) and the manual gap on the interrupt (confirmed by the probe).
  - Medium: the stun as the main frustration. Only the tester's report supports it, and no live reaction data exists.
  - Low: the dash distance and "(miss)" next to a grub. Untested.
- The tester's own caveat applies: timed scripts, no live reaction. Some failures are likely timing errors.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/51-studio-to-game-designer.md
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
