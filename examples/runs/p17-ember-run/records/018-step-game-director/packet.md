# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-first-playable-run/16-studio-to-game-director.md
next_seq: 17
runs: play (up to 3 rounds)
run_play: node play.js {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable-run/17-game-director-to-<recipient>.md
- decisions/D-003-<name>.md
- @run/<play>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-001-first-playable-run/16-studio-to-game-director.md
---
kind: handoff
goal: G-001
seq: 16
from: studio
to: game-director
stage: Review
outcome: routed
---
# 16: studio → game-director — review whether G-001's intent was met, from the evidence that exists

## Task

Judge whether Goal G-001 met its intent (a whole five-floor run playable from `repo/index.html`, honoring the three pillars), using the evidence below. Say plainly which parts are verified, which are not, and name the next issues as proposed Goals.

## Context

The Goal's Owner request: build a version that can be played from start to finish, in the browser. Design (30 checks), Plan, Build and Verify are done. Play ran once and was partial. The budget (19 operations) leaves room for this Review and the closing Route only. Do not ask for more stages: if more evidence is needed, name it as a proposed Goal or an Owner item.

## Findings

Evidence in hand (read the files in Load for detail):

- Verify (13): no defects found; `node --test` 49/49 green. QA did not see per-test results for checks 13, 14 (hand-made) and 26. Checks 27-30 (browser page) were not verifiable by any executor. The Art Director review was skipped.
- Play (15, partial): scripts only, seed 42, floor 1, 16 turns, no browser. Observed as a player: readable frame; refused moves cost nothing and say so; the `?`/`!` warnings and the Danger/THREAT lines for a cave moth were accurate; ember fell 1 per turn; one trivial fight. Possible presentation defect: earlier messages (arrival line, the moth fight) were repeated in later frames and made it hard to tell what had just happened (low to medium impact). Not observed at all: hounds, shades, the Gloom, braziers lit, items, floors 2-5, winning, dying, other seeds, run length (pillar 3: 15-30 minutes), whether the ember trade-off (pillar 2) feels real, balance.
- Design left balance unverified and asked Play to report it. Play could not.

## Decisions already made

- D-001: shared code is classic-script modules (UMD style).
- D-002: threat marks plus reach marks on the four neighbour tiles.

## Constraints

- Scope within the Goal is yours; the vision, pillars and Owner-made Decisions are not to be changed. If a verdict would require that, prepare an escalation instead.
- No new stages can be added (budget). The next issues are proposals for the Owner.
- Whether the repeated messages are a defect or intended depends on the manual and the design; check them before calling it a defect.

## Open questions

- Is the intent met, partly met, or not met, given that pillars 2 and 3 and floors 2-5 have no player-side evidence?
- Which next issues should be proposed, and in what order (e.g., a broader playtest across seeds and floors, a QA check of the message log, a human check of the browser page, balance)?

## Expected output

A Review verdict: `goal-met` or `goal-not-met` in `outcome` (explain "partly" in Findings). The handoff goes to `studio` (`to: studio`) as `17-game-director-to-studio.md`, and it lists the next issues as proposed Goals, the items that need the Owner (browser checks 27-30 especially), and what was and was not achieved, in wording the Studio can put in the Outcome. The Studio's Route then closes the Goal.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md (vision, player profile, constraints), design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, goals/G-001-first-playable-run/goal.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/15-playtester-to-studio.md (also read goals/G-001-first-playable-run/13-qa-to-studio.md for the Verify results)
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
runs: play, bots
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/review-outcome.md
---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
>>>END

<<<FILE project.md
---
kind: project
id: ember-hollow
name: Ember Hollow (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: node --test
run_play: node play.js {script}
run_trace: node play.js --trace {script}
---
# Project: Ember Hollow (new concept)

## Vision

A short turn-based roguelike. The player descends five floors of a cave carrying a single ember.
The ember is both light and time: its glow is how far the player can see, it dims a little every
turn, and only the braziers scattered through the floors rekindle it. The creatures of the hollow
live in the dark and react to the light. Floor 5 holds the creature that keeps the hollow dark;
beating it wins the run. Dying, or letting the ember go out, ends it.

Pillars:

1. **Every turn is a decision.** Move, wait, fight or use an item; every threat that can hurt the
   player next turn is visible and readable before it does.
2. **Light is the resource.** Seeing farther and having more time are the same thing; spending the
   ember is the core trade-off of a run.
3. **A run is short and different each time.** A whole run takes 15 to 30 minutes. Floors are made
   from a seed, so every seed is a different run, and the same seed is always the same run.

## Player profile

Players who enjoy short roguelikes: they like learning how each creature behaves and planning a
few turns ahead, and accept losing a run to learn from it. They play with a keyboard, or by
clicking, in a browser.

## Current state

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.

## Constraints

- The build is JavaScript for Node.js 20 and the browser, with no dependencies and no network
  use, in `repo/`. The game's rules live in code that both ways of playing share.
- **For people: a browser page.** `repo/index.html` opens straight from the file system (no
  server) and is played with the keyboard or the mouse. It draws the floor as a grid.
- **For the team: input scripts.** `run_play` (`node play.js {script}`) plays a script and prints
  what the player sees, as text, turn by turn; `run_trace` adds the internal state; `run_tests`
  (`node --test`) runs the build's tests. The script format (including how a run's seed is
  chosen) is the build's to define, in `repo/manual.md`, which ships with the build and is all a
  player is told.
- Deterministic: the same seed and the same commands always give the same run.

## Design index

None yet.
>>>END

<<<FILE design/game-spec.md
# Ember Hollow: game spec for the first complete run (G-001)

## 1. Intent

The player descends five floors with one ember. The ember is light and time. A brighter ember sees farther but burns the same per turn, and braziers are the only refill, so every detour for light or an item is paid for in ember. Each creature reacts to light in its own way. Every threat that can hurt the player on the next turn is already visible, with a visible warning when it is not simply adjacent. One run takes 15 to 30 minutes and ends in a win (the Gloom on floor 5 is defeated) or a loss.

This document is player-facing behavior only. The code structure, the script format and the rendering technology belong to the build. Numbers use Manhattan distance (|dx|+|dy|) unless stated otherwise.

## 2. The grid and turns

- Square tiles. Tile types: wall, floor, stairs up `<` (arrival point), stairs down `>`, brazier. Items and creatures sit on floor tiles.
- Movement and attacks are 4-directional (N, E, S, W). There are no diagonal moves or attacks. The one exception is the Gloom's slam area (section 7).
- The game is turn-based. One **turn** is: the player acts, then the effects of the action resolve, then the ember dims, then the creatures act in creature-id order (the order they were placed on the floor).
- Nothing depends on real time. All randomness comes from the run seed.

### Player actions (each takes exactly one turn unless stated)

| Action | Effect |
|---|---|
| Move | Step onto an adjacent walkable tile. Moving onto a brazier, an item or the down stairs triggers its effect (below). Moving into a wall does nothing and costs no turn. |
| Fight | Moving toward an adjacent creature attacks it instead of moving. It takes 2 damage. The player has no ranged attack. |
| Wait | Stay in place. It costs a turn and ember like any other action. |
| Use item | Use the item in an inventory slot (section 6). A refused use (see section 6) costs no turn. |

- Player HP is 12 at the start of the run. It carries across floors and has no natural regeneration.
- Ember carries across floors. A new floor does not refill it.
- Stairs down: stepping onto `>` ends the turn. The ember dims by 1 as normal, then the next floor starts with the player on its `<`. Creatures on the new floor do not act on the arrival turn. There is no going back up.

## 3. Ember and light

- **Ember value E**: integer 0 to 100. The run starts at E = 100.
- **Dimming**: after every turn in which the player acted (move, wait, fight, item use), E decreases by 1. Near the Gloom (see section 7), E decreases by 2.
- **Glow radius r** is a function of E:

| E | r |
|---|---|
| 80–100 | 6 |
| 60–79 | 5 |
| 40–59 | 4 |
| 20–39 | 3 |
| 1–19 | 2 |
| 0 | the run ends |

- **Visible tiles**: a tile is visible when it is within the glow (dx²+dy² ≤ (r+0.5)²) and a straight line of sight from the player to it is not blocked by a wall. Tiles next to the player are always visible. Because r is never below 2, every orthogonally adjacent tile and every tile at Manhattan distance 2 in a straight clear line is always visible.
- **Remembered tiles**: terrain, stairs, braziers and items that were seen stay on the map, drawn visibly dimmer than currently visible tiles. Creatures are shown only while visible, never from memory.
- **Brazier**: an unlit brazier is on each floor as a tile. When the player moves onto it:
  1. E = min(100, E + 60) (this happens before that turn's dimming).
  2. The brazier becomes lit and stays lit. A lit brazier has no further effect and can be walked over.
  3. **Flare**: every non-boss creature within Manhattan distance 7 that is visible after the rekindle is stunned for 2 turns. A stunned creature skips its next 2 actions, and a crouching hound's crouch is cancelled. The first skipped action is the one in the lighting turn's own creature phase, the second is in the next turn. The creature is labelled "stunned" in the frame after the lighting turn and acts again in the creature phase of the second turn after the lighting turn.
- **The ember goes out**: if E is 0 after the dimming, the run ends at once with the cause "The ember went out". Creatures do not act on that turn. The defeat of the Gloom on the same turn counts as a win, because the player's action resolves first.
- **Reading the ember**: the screen always shows E (number and bar), the current r, and the dimming rate ("dims 1/turn" or "dims 2/turn"). A message is shown when E first falls to 20, 10 and 5 or below, and when r shrinks ("Your light shrinks").

## 4. Creatures

General rules:
- Each creature either **moves one tile or acts, never both** in one turn, except the hound lunge (which is telegraphed one turn before).
- A creature cannot enter a tile with the player, another creature, a wall, a brazier, or stairs.
- "Toward the player" means one step along a shortest walkable path (ties broken in the order N, E, S, W). If no path exists or no step is free, the creature stays put.
- Creatures on a floor start where the floor generator places them (section 8) and do not follow the player downstairs.
- A creature whose HP reaches 0 is removed at once and does not act again.
- Visible creatures show their name or letter, HP, and state (idle, hunting, fleeing, crouching, stunned, staggered). A creature that can hurt the player on its next action is marked as a threat (see section 9).

| Creature | Letter | HP | Damage | Floors |
|---|---|---|---|---|
| Cave moth | `m` | 2 | 1 | 1–4 |
| Shade | `s` | 4 | 2 | 2–5 |
| Ash hound | `h` | 4 | 3 | 3–5 |
| The Gloom | `G` | 24 | 4 | 5 |

### Cave moth (reaction to light: drawn to it)
- If the shortest walkable path distance to the player is ≤ r + 3, it moves toward the player each turn. A brighter ember draws moths from farther away. Otherwise it stays still.
- If adjacent to the player at the start of its action, it attacks for 1 damage instead of moving.
- It teaches: brightness draws attention, and weak enemies can be fought in the open.

### Shade (reaction to light: fears bright light, strikes when it is dim)
- **While r ≥ 3** (E ≥ 20): a shade that is visible flees. It moves one step that increases its path distance from the player, or stays if there is none (cornered). A cornered shade adjacent to the player attacks for 2 damage. A shade that is not visible moves toward the player if its path distance is ≤ 12, so shades hover at the edge of the light and drift in and out of sight.
- **While r = 2** (E ≤ 19): shades are no longer afraid. Each shade moves toward the player, and attacks for 2 damage once adjacent at the start of its action.
- Because it moves or attacks and not both, a shade that steps adjacent can attack only on its next action. The player sees it adjacent first.
- It teaches: keep the ember up, and corner or leave shades when bright.

### Ash hound (reaction to light: ignores glow size, but a flare stuns it)
- Idle until the shortest path distance to the player is ≤ 6, then it hunts: moves one tile toward the player each turn.
- **Bite**: if adjacent at the start of its action, it attacks for 3 damage.
- **Lunge** (telegraphed): when a hound is at Manhattan distance exactly 2 in a straight row or column with an empty floor tile between it and the player, it **crouches** instead of moving, and shows a crouch mark and the line it threatens. On its next action it lunges: it moves up to 2 tiles along the line toward the player. If the player is still within 2 tiles in that line, the hound ends adjacent and the player takes 3 damage. If the player has left the line or is farther, the hound just moves up to 2 tiles toward the player and does not bite that turn. A lunge that cannot move (blocked) deals no damage. If the player stands directly adjacent to the hound when it acts, the hound simply bites for 3 (the adjacent-bite rule applies, and the line is irrelevant). "Blocked" means a wall or another creature stops the hound before it ends adjacent to the player.
- The crouch is always visible when it starts (distance 2 in a clear line), so the player always gets one turn to step out of the line, back away, or strike it first.
- It teaches: sidestep the line, or fight it from a corner.

## 5. Floors

- 5 floors. Floors 1–4 have `<` and `>`. Floor 5 has `<` and the boss arena, and no `>`.
- Floor sizes (tiles, width × height) and contents:

| Floor | Size | Creatures | Braziers | Items |
|---|---|---|---|---|
| 1 | 28 × 16 | 4 moths | 2 | 1 salve, 1 oil |
| 2 | 30 × 18 | 3 moths, 2 shades | 2 | 1 salve, 1 oil |
| 3 | 32 × 18 | 2 moths, 3 shades, 1 hound | 2 | 1 salve, 1 oil |
| 4 | 34 × 20 | 2 moths, 3 shades, 3 hounds | 2 | 1 salve, 1 oil |
| 5 | 30 × 18 | the Gloom, 2 shades, 1 hound | 3 (in the arena) | 1 salve, 1 oil |

- **Layout** is made of rooms joined by corridors (floors 1–4: 5 to 8 rooms; floor 5: a start room, a corridor, and a single open arena room of at least 14 × 10 tiles holding the Gloom and the 3 braziers). All walkable tiles are connected, so every item, brazier and exit is reachable by walking.
- **Stairs**: the shortest walking distance from `<` to `>` is at least 30 steps on floors 1–3 and at least 40 on floor 4. Floor 5 has the arena entrance at least 20 steps from `<`.
- **Braziers**: at least one brazier on each floor 1–4 is within 25 walking steps of `<`. The other is at least 10 steps from the first. Braziers are not on the shortest path from `<` to `>` for both of them (at least one needs a detour).
- **Creatures** are placed on floor tiles, at least 6 walking steps from `<`, not on items. The Gloom stands at the far end of the arena, at least 8 steps from the arena entrance.
- **Items** are on floor tiles, not on stairs or braziers, and at least one item per floor is not on the shortest path from `<` to `>`.
- **Seed**: a run is determined by its seed (an integer or text; the build defines how it is chosen). Floor n's layout, brazier positions, items and starting creature positions depend only on the seed and n, never on what the player did earlier. The same seed and the same commands always give the same run. Different seeds give different layouts (at least 9 of any 10 different seeds give different floor 1 layouts). The seed is always shown to the player.

## 6. Items

Inventory: 4 slots, one item per slot, items are picked up by walking onto them.

| Item | Effect |
|---|---|
| Salve | Restores 5 HP (up to 12). Refused with a message, at no cost, if HP is already 12. |
| Oil flask | Restores 30 ember (up to 100). Refused with a message, at no cost, if E is already 100. The effect happens before that turn's dimming. |

- Walking onto an item with a full inventory leaves the item on the floor and shows a message. The move still costs a turn.
- Using an item takes one turn, so creatures act.

## 7. Floor 5: the Gloom

The Gloom (`G`) keeps the hollow dark. It is a single 1-tile creature with 24 HP. It never leaves the arena unless pulled (it stalks the player if the player is in the arena, otherwise it stays).

- **Darkness drain**: while the Gloom is alive and within Manhattan distance 4 of the player at the end of a turn, the ember dims by an extra 1 that turn (2 total). The HUD shows "dims 2/turn" while this applies.
- **Cycle** (one state per turn):
  1. **Stalk**: while the player is not within Manhattan distance 2, it moves one tile toward the player each turn.
  2. **Gather** (telegraph): when the player is within Manhattan distance 2 at the start of its action, it stops and marks every tile in the 3×3 area around itself (diagonals included). It does not move this turn. The marked area stays visible.
  3. **Slam**: on its next action it deals 4 damage to the player if the player stands in the marked area, then becomes **staggered**.
  4. **Staggered**: for the next 3 turns it does nothing, and attacks against it deal 4 damage instead of 2. Then it returns to Stalk.
- The player can always avoid a slam: from any tile in the 3×3 area, one step in a straight line leaves it, unless walls block every such step.
- The Gloom is not stunned by flares. It is outside the 'non-boss creatures' rule.
- Because r is at least 2, the Gloom's gather is always visible when it starts (the player is within distance 2).
- **Win**: when the Gloom's HP reaches 0 the run ends in victory immediately, before the ember dims.

## 8. End of run

Three end states. Each shows a summary screen (browser) or summary lines (text output) with: the result, floor reached, turns taken, creatures defeated, final HP, final ember, and the seed.

| End | Trigger | Message |
|---|---|---|
| Victory | Gloom reaches 0 HP | "The Gloom breaks. Light returns to the hollow." |
| Dead | Player HP reaches 0 (checked after the creatures act) | "You fell on floor N." |
| Ember out | E reaches 0 after dimming | "The ember went out on floor N." |

- If HP 0 and ember 0 would both occur in one turn, "The ember went out" applies, because the ember check comes first and creatures never act.
- After an end state, no further commands change the game. The player can start a new run: same seed, or a new seed.

## 9. What the player can tell (screen contents)

The game is shown as a grid (browser page) and as text (`node play.js`). Both must give the same information:

1. **Map**: walls, floor, `<`, `>`, braziers (unlit vs. lit distinguishable), items (salve vs. oil distinguishable), the player, and visible creatures (type distinguishable). Visible tiles are clearly brighter than remembered tiles; unseen tiles are blank.
2. **Ember**: E as a number and a bar, the glow radius r, and the dimming rate.
3. **Health**: HP as current/12.
4. **Floor and turn**: floor number out of 5, and the number of turns taken.
5. **Inventory**: 4 slots, each showing the item or empty, with its key.
6. **Creatures**: for each visible creature, its type, HP, state, and position.
7. **Threats and reach** (decision D-002): all marks use the ember value the creatures will see, that is the current E minus this turn's dimming (1, or 2 near the Gloom). That E decides r, and so whether a shade is afraid.
   - **Threat mark**: a visible creature that can hurt the player at its next action, with the player where they stand now, is marked: an adjacent moth, an adjacent hound, a shade that is adjacent and either cornered or while r = 2, a crouching hound with its line, and the Gloom's marked area. The mark appears the same turn the threat becomes real (in text, e.g. `!`; in the browser, a visibly different highlight).
   - **Reach mark**: for each of the four orthogonal neighbour tiles the player could move onto, the screen shows which visible creatures would hurt the player at their next action if the player ended the turn on that tile (creatures themselves staying where they are). In text this is a line such as `Danger: N (m), E (h)`; in the browser, the tile gets a highlight and the creature letter. A tile that is a wall, holds a creature, or is the down stairs gets no reach mark (stairs end the turn with no creature phase). An unlit brazier tile gets no reach mark from creatures the flare stuns (every visible non-boss creature in range 7), but it does get one from the Gloom, which a flare does not stun. A lit brazier has no flare and is marked like a floor tile. The reach mark uses the same rules as the threat mark. It is a different display, not a different rule.
   - Every creature that is orthogonally adjacent to the player, or to a neighbour tile the player could move onto, is shown even if a wall blocks the line of sight to it, so a creature that can hurt the player after one step is never hidden.
   - Nothing that is unmarked on the tile where the player ends the turn can hurt the player next turn. A creature that only moves closer and cannot attack yet (for example a moth at distance 2) is not marked. It is seen adjacent, and marked, on the next turn.
8. **Messages**: the last 5 messages (attacks with damage, picked items, brazier lit, shrinking light, ember low, end of run).
9. **Seed**: shown at all times.

### Controls (browser)

- Keyboard: arrow keys or WASD to move or fight; `.` or Space to wait; `1`–`4` to use the item in that slot; `R` to restart with the same seed; `N` to start a new run with a new seed.
- Mouse: clicking an orthogonally adjacent tile moves or fights; clicking an inventory slot uses it; a Wait button; buttons for restart and new seed.
- Only the player's actions advance the game. Opening the page requires no server and no network.

## 10. Run shape

- Target: 15 to 30 minutes, which at an average of 2 to 4 seconds per decision is about 250 to 700 player turns.
- Ember supply: 100 at the start plus 11 braziers × 60 = 760 in total on offer, plus 5 oil flasks × 30. A direct walk uses about 40 turns per floor; a normal run with fights, detours and the boss fight is expected to use 300 to 600 turns, so ember is tight but not hopeless when the player lights about half of the braziers.
- Tuning is a first estimate. The Play step is expected to report where it is too easy or too hard, so numbers can be revised in the spec.

## 11. Edge cases and rules for simultaneous events

- Several creatures acting in one turn: in creature-id order. A creature killed earlier in the same turn (for example by the player) does not act.
- Creature phase and the ember out: the ember check comes before the creatures act, so a turn that empties the ember is never decided by creature damage.
- Descending with a stunned or adjacent creature: it does not follow.
- A lunging hound stopped by another creature: it moves as far as it can along the line; it bites only if it ends adjacent with the player still in the line.
- A brazier tile or the stairs can never be occupied by a creature, so a creature never blocks stairs or braziers.
- A flare stuns only creatures visible after the rekindle (radius computed from the new E), within Manhattan distance 7.
- Stunned or staggered creatures are still shown, labeled with their state, and not marked as a threat.
- Using an oil flask at a brazier tile cannot happen on the same turn (a move onto a brazier is the turn's action).
- A salve or oil flask used at 12 HP / 100 E is refused at no cost.
- A full inventory leaves the item where it lies.
- Fight on a creature that is at distance 1 diagonally is not possible (no diagonal actions).
- Marks and the player's step: the threat mark describes staying (Wait) or an action that does not move the player (a fight, an item use). The reach marks describe a move onto a neighbour tile. In both cases the damage a creature does in the creature phase was announced in the output before the action by the mark on the tile where the player ended the turn (D-002).
- A shade at E = 20 is still afraid now, but a Wait or step costs 1 E, so the creature phase sees E = 19 and r = 2. Its marks are already shown as a strike. Marks are computed from the E after dimming for this reason.

## 12. Out of scope

Saving, meta-progression, sound, mobile layouts, ranged player attacks, keys/doors, traps, more creatures or items than listed.
>>>END

<<<FILE design/acceptance-criteria.md
# Ember Hollow: acceptance criteria for the first complete run (G-001)

Rules referenced here are in `design/game-spec.md`. "Text output" means what `node play.js {script}` prints. "Page" means `repo/index.html` opened from the file system.

## A. Verification checks (QA, through text output unless marked Page)

### Ember and light
1. A new run shows E = 100 and r = 6, HP 12/12, floor 1/5.
2. After 1 wait on a quiet floor, E = 99; after 20 waits, E = 80 and r is still 6; after 21 waits, E = 79 and r = 5. r equals 6/5/4/3/2 at the E thresholds in spec section 3 (checked at E = 100, 80, 79, 60, 59, 40, 39, 20, 19, 1).
3. Moving, waiting, fighting and using an item each cost exactly 1 E. A refused action (wall, item refused at full HP/E) costs 0 E and does not advance the turn counter.
4. Stepping onto an unlit brazier at E = 30 gives E = 89 after the turn (30 + 60 − 1). At E = 80 it gives E = 99... (min 100 − 1). A lit brazier gives nothing on later visits.
5. Reaching E = 0 ends the run with "The ember went out" and the floor number. Creatures do not act on that turn (HP is unchanged by them).
6. A message is shown when E falls to 20, 10 and 5 or below, and when r drops.
7. Map memory: after walking away, previously seen tiles stay shown as remembered; creatures out of sight are not listed.
8. Oil flask: +30 E up to 100, then dimming; refused at E = 100 with no turn passing. Salve: +5 HP up to 12; refused at 12 HP with no turn passing.

### Creatures
9. Moth: with the player at path distance ≤ r + 3 it moves 1 tile toward the player per turn; beyond that it stays. Adjacent at the start of its action it deals exactly 1. Dies to 1 player hit (2 damage).
10. Shade, r ≥ 3: a visible shade moves away from the player (never closer) and deals no damage unless cornered and adjacent (2 damage). r = 2 (E ≤ 19): a shade moves toward the player and deals 2 damage when adjacent at the start of its action. Takes 2 player hits (4 HP).
11. Hound: starts hunting at path distance ≤ 6. At Manhattan distance 2 in a clear straight line it crouches and is marked as a threat with its line for exactly one turn. If the player leaves the line during that turn, no damage is dealt; if the player stays within 2 tiles in the line, the player takes exactly 3. Adjacent hound bites for 3. Takes 2 player hits.
12. A creature moves or attacks, never both in one turn (except the hound lunge). Verified by a turn log that shows a creature appearing adjacent one turn before its first attack.
13. Brazier flare: non-boss creatures visible within distance 7 after lighting skip exactly 2 actions: the one in the lighting turn's own creature phase and the one in the next turn. They are labeled stunned in the frame after the lighting turn and act again in the second turn after it. A crouching hound's crouch is cancelled.
14. Threat and reach marks (D-002): in every turn where the player takes damage from a creature, that creature was visible in the previous turn's output and carried a mark on the tile where the player ended the turn. That is a threat mark if the player did not move, or a reach mark on the neighbour tile the player moved onto. Over 20 scripted runs on different seeds, no damage comes from a creature that was not shown and marked this way before it hit. The test log lists each damage event with the case that applied (threat or reach). Also checked on hand-made scenarios: a step next to a moth, a hound and a shade at r = 2 each shows a reach mark before the step. A Wait at E = 20 beside a shade shows the threat mark as a strike, because the creature phase sees r = 2. A step onto the down stairs shows no reach mark. A step onto an unlit brazier shows no reach mark for creatures the flare stuns, but does show one for the Gloom if it would hurt; a lit brazier is marked like a floor tile.

### The Gloom and the win
15. On floor 5, the Gloom has 24 HP. While within Manhattan distance 4 of the player the ember loses 2 per turn and the output shows "dims 2/turn".
16. When the player is within distance 2 it shows a 3×3 marked area for one turn, then the next turn deals exactly 4 to a player standing in that area and 0 to a player outside it.
17. After a slam it is staggered for 3 turns and does nothing; hits on it during those turns deal 4 damage, otherwise 2.
18. Reducing the Gloom to 0 HP gives Victory at once, with the victory message and the summary (floor, turns, defeated count, HP, ember, seed). A scripted fight is possible in which the player wins with E ≤ 5.
19. HP 0 gives "You fell on floor N" and the summary. If HP 0 and E 0 would both happen in one turn, the result is "The ember went out".
20. After an end state further commands change nothing.

### Floors and seeds
21. Same seed + same commands → byte-identical text output on two runs. Same seed with different commands on floor 1 → floor 2 layout, items and creature start positions identical.
22. Of 10 different seeds, at least 9 give a different floor 1 layout.
23. For 50 seeds × floors 1–5: sizes match the table (spec section 5), all walkable tiles connected, creature, brazier and item counts match the table, `<`→`>` shortest path ≥ 30 (floors 1–3) / ≥ 40 (floor 4), at least one brazier within 25 steps of `<` on floors 1–4, no creature within 6 steps of `<`, floor 5 has no `>` and 3 braziers in the arena.
24. Descending: the player appears on `<` of the next floor with E and HP unchanged apart from that turn's dimming, and the floor number increases; the player cannot go back up.
25. Inventory holds 4 items; a fifth stays on the floor with a message.

### Run length
26. A scripted, reasonable run (walk to `>` while lighting braziers within 10 steps of the path, fight what blocks the way, fight the Gloom) of at least 3 different seeds takes between 250 and 700 player turns and reaches either Victory or a loss. At least one seed is won by a bot that follows the threat marks.

### Page (checked by looking at it)
27. `repo/index.html` opens from the file system with no server and shows the grid, ember bar with E and r, HP, floor n/5, turn count, inventory slots, the last 5 messages and the seed.
28. Arrow keys / WASD, `.` / Space, `1`–`4`, `R`, `N` work as in spec section 9. Clicking an adjacent tile moves or fights; clicking an inventory slot uses the item.
29. Visible tiles are clearly brighter than remembered tiles. As E falls through each threshold, the visible area visibly shrinks by about one tile of radius. Creature types are distinguishable at a glance. Threat marks are clearly visible and different from the normal creature display. Reach marks on the neighbour tiles are visible and distinct from the threat marks. A lit brazier differs from an unlit one.
30. The summary screen appears for each of the three end states with the fields from spec section 8, and a new run can be started from it.

## B. Experience signals (for Play and Review; not given to the Playtester as pass/fail)

- A new player understands from the first floor that the ember dims and braziers refill it, without a tutorial text beyond the manual.
- Within the first two floors the player can say what a moth and a shade do, and why shades keep their distance when the light is bright.
- The player makes at least one choice per floor of the form "detour for a brazier/item or save ember".
- The player is hurt by something they did not notice at most rarely; when it happens they can name the mark that warned them.
- The hound's crouch is understood the first time it is seen (the player steps out of the line, or strikes first).
- The Gloom fight reads as a rhythm: approach, gather, dodge, stagger, strike; and the extra drain makes the player feel the clock.
- A lost run leaves the player with a specific thing to do differently.
- A full run feels like 15–30 minutes; a second run on a new seed feels different, a repeat of the same seed feels familiar.
>>>END

<<<FILE repo/manual.md
# Ember Hollow: manual

You carry one ember down five floors. The ember is your light **and** your time: it loses 1 each turn you act
(2 while the Gloom is within 4 tiles). Braziers refill it (+60, once each). At 0 the run ends. Reach floor 5
and break the Gloom to win.

## Playing in the browser

Open `index.html` from the file system (no server needed).

- Arrow keys / WASD: move, or fight an adjacent creature (2 damage). `.` or Space: wait. `1`-`4`: use the item in that slot.
- `R`: restart with the same seed. `N`: new run with a new seed. Or type a seed in the box and press Start.
- Mouse: click an orthogonally adjacent tile to move or fight; click an inventory slot to use it; buttons for Wait, Restart, New seed.
- The seed is always shown. The same seed always gives the same floors. `index.html#my-seed` starts with the seed `my-seed`.
- Red marks (threat marks) show what can hurt you at its next action if you stay or fight (an adjacent biter, a crouching hound's line, the Gloom's gathered area).
- Dashed orange tiles with creature letters (reach marks) are the neighbour tiles where a visible creature would hurt you if you stepped there. The line `Danger: N (m), E (h)` under the map lists the same.

## Playing / scripting in text: `node play.js [--trace] <script>`

A script is a text file. `#` starts a comment (so a seed cannot contain `#`).

- The first non-comment line may be `seed <integer or text>`. No seed line means the default seed `hollow`.
- Every other non-space character is one command (spaces and newlines are only for readability):

| Char | Command |
|---|---|
| `w` `a` `s` `d` | move or fight north / west / south / east |
| `.` | wait |
| `1` `2` `3` `4` | use the item in that slot |

Example:

```
seed 42
dddd ss  # walk east, then south
..       # wait twice
```

`node play.js script.txt` prints the frame after every command; `-` reads the script from stdin.
`--trace` adds, per command, each creature's id, position, state, intent and path distance, the threats marked
before the action, the events with damage sources, E and the drain rate. Each damage line gives `case=threat` (the player
did not move) or `case=reach` (the player stepped onto a neighbour tile), `visibleBefore`, and `markedBefore`: whether the
creature was shown in the previous frame with the threat mark (threat) or the reach mark on the tile where the player ended
the turn (reach), per D-002. A command refused with no cost
(a wall, an item refused at full HP/E, an empty slot) prints its frame with "(refused: no turn passed)".
After an end state the summary lines are printed and later commands are ignored.

## Reading a frame

```
Floor 1/5 | Turn 12 | HP 12/12
Ember 87/100 [#################---] r=6 | dims 1/turn
Items: [1] salve  [2] empty  [3] empty  [4] empty
```

Map symbols: `@` you, `#` wall, `.` visible floor, `<` `>` stairs, `B` unlit brazier, `b` lit brazier, `+` salve, `o` oil,
`m` moth, `s` shade, `h` hound, `G` the Gloom. Remembered tiles are dimmer: `,` floor and `%` wall in text (terrain, stairs,
braziers and items stay shown). Unseen tiles are blank. Creatures are drawn only while visible.
`!` on the map marks a tile that is part of a marked danger (hound line, Gloom area). In the creature list a line starting
with `!` is a threat that can hurt you at its next action, with the reason.
`?` on the map marks a **reach mark**: a neighbour tile where stepping would get you hurt at the creatures' next action.
Under the map the line `Danger: N (m), E (h, s)` lists, per direction N/E/S/W, the creature letters that would hurt you if
you ended the turn on that neighbour tile (`Danger: none` when no step is marked). A wall, a tile holding a creature, the
down stairs never get a reach mark. An unlit brazier gets none from creatures the flare stuns, but does get one from the Gloom (not stunned) if it would hurt you there. Reach marks use the same planner as the creatures and the same ember
as they will see (current E minus this turn's dimming).
The last five messages and the seed are always printed.

## Rule readings the build chose (where the spec leaves room)

1. **Drain distance**: the Gloom's Manhattan distance is measured after the player's action (the player's position at the end of their half of the turn), before the creatures move.
2. **Path distance** (moth trigger r+3, hound 6, shade 12, "toward the player"): walking distance over all non-wall tiles, ignoring creatures. A creature's step must be a free floor tile (never a wall, brazier, stairs, the player or another creature); if the only shortest-path step is blocked it stays.
3. **Flare stun**: stunned = 2 skipped actions, counted from the creature phase of the lighting turn itself. A stunned creature is therefore labelled "stunned" in the frame after the lighting turn, skips its action in the lighting turn's own creature phase (first skipped action) and in the next turn (second), and acts in the creature phase of the second turn after the lighting turn (the third turn, counting the lighting turn as the first). Ratified by the game designer.
4. **Hound lunge**: with the player directly adjacent in the crouch line when it springs (the player stepped toward it), it bites for 3. A lunge blocked before it ends adjacent deals no damage. The hound hunts whenever the path distance is <= 6 (no memory of having hunted).
5. **Empty item slot**: using an empty slot is refused at no cost, with a message. Refused actions only add a message; turn, E, HP and position do not change.
6. **Threat marks** come from the same planner the creatures act with. Marked: an attack at the next action (adjacent moth/hound, shade that is cornered or at r=2), a crouched hound (always, with its line), the Gloom once it has gathered (with its area). A hound that is about to crouch is not marked yet. Stunned or staggered creatures are never marked.
   Marks and creature states use the ember after this turn's dimming (D-002), so at E = 20 a Wait beside a shade already shows the strike.
7. **Shade visibility** ("a visible shade flees") uses the visibility after the player's action and that turn's dimming.
8. Descending never triggers creature actions. A creature never follows.
9. **Reach marks** (D-002) are computed with `planAction` and a hypothetical player position (E after the dimming at that tile, visibility and path distances from that tile). A crouched hound counts only if the tile is on its line, within 2, and the tiles between are free. A creature orthogonally adjacent to the player or to a neighbour tile is listed even if a wall blocks line of sight.
10. **Lit brazier** (ratified by the game designer): the spec says "a brazier tile gets none" because of the flare. A lit brazier has no flare, so it gets reach marks like a floor tile; otherwise strict check 14 could not hold there.

## Not covered by this build

Saving, sound, mobile layout. Balance is a first estimate and unverified.
>>>END

<<<FILE goals/G-001-first-playable-run/goal.md
---
kind: goal
id: G-001
project: ember-hollow
status: active
created: 2026-10-26
budget: 19
---
# G-001: First complete playable run in the browser

## Owner request

> このコンセプトで、最初から最後まで通して遊べる版を作ってほしい。ブラウザで遊べるようにしてほしい

## Interpretation

Success condition: a person opens `repo/index.html` straight from the file system in a browser and can play one whole run with keyboard or mouse. The run starts on floor 1, passes through all five floors, and ends in one of the ways the vision names: beating the floor-5 creature (win), dying, or the ember going out. No setup, server or developer step is needed. The vision's pillars hold in that run: readable threats, light as the resource, a short seeded run (same seed gives the same run).

The team-side means from `project.md#constraints` also ship, because verification depends on them: `node play.js {script}`, `--trace`, `node --test`, and `repo/manual.md` (the script format and everything a player is told).

Out of scope (not requested): saving or resuming runs, meta-progression between runs, sound, mobile or touch layouts, network features, content beyond what one complete five-floor run needs, and any change to the vision or pillars.

## Unknowns

- Observe: skipped. No build exists and nothing is reported broken or off.
- Diagnose: skipped. There is no problem to explain.
- Decide: skipped. Design stayed inside the vision and Goal scope and raised no direction, priority or scope choice.
- Design: done. 30 checks; check 14 settled by D-002; flare stun timing, hound bite at distance 1, lit/unlit brazier reach marks ruled (handoff 10). Balance is unverified; Play must report it.
- Plan: done (handoff 03).
- Build: done (handoff 12). `node --test` passed 49/49.
- Verify: done, partial (handoff 13). No defects found; 49/49 green; per-test results for checks 13, 14 (hand-made) and 26 not seen by QA. Checks 27-30 (browser page) were not verifiable by any executor and stay open for the Owner. Art Director review skipped (budget; no executor can see the page).
- Play: done, partial (handoff 15). One seed (42), floor 1 only, 16 turns, scripts only, no browser. Seen: accurate moth warnings, free refused moves, ember 1/turn. Possible presentation defect: old messages repeat in later frames. Not observed: hounds, shades, Gloom, braziers lit, items, floors 2-5, win/loss, other seeds, run length, balance. A further round does not fit the budget.
- Review: open (game-director, handoff 16). Judges the intent from thin evidence, names the next issues (more play, stale messages, browser checks 27-30).

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md |
| 2 | Decide | game-director | make-decision | skipped | — |
| 3 | Plan | technical-director | technical-plan | done | 02-game-designer-to-technical-director.md |
| 4a | Build | gameplay-engineer | implement-change | done | 11-studio-to-gameplay-engineer.md |
| 4b | Design (check 14 question) | game-designer | write-design-spec | done | 04-studio-to-game-designer.md |
| 4c | Design (flare stun, hound bite) | game-designer | write-design-spec | done | 08-studio-to-game-designer.md |
| 5a | Verify | qa | verify-change | done | 13-qa-to-studio.md |
| 5b | Verify (visual) | art-director | visual-review | skipped | — |
| 6 | Play | playtester | playtest-session | done | 14-studio-to-playtester.md |
| 7 | Review | game-director | review-outcome | open | 16-studio-to-game-director.md |
| 8 | Next | studio | — | planned | — |

## Route changes

After Play (15, partial): thin evidence (floor 1, 16 turns). A second Play round would need 4 more operations after this Route; only 3 remain. So Review opens now (16) with the gaps stated; further play and the stale-message issue become proposed Goals. Budget: 16 of 19 used; Review, Close fit.

## Next action

Start step 7: `game-director` with `16-studio-to-game-director.md`. The Route after it closes the Goal (Outcome in Japanese, project.md Current state).

## Outcome

(open)
>>>END

<<<FILE decisions/D-001-classic-scripts-shared-rules.md
---
kind: decision
id: D-001
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-26
supersedes: none
---
# D-001: Shared code is plain classic-script modules (UMD style), not ES modules

## Decision

All code under `repo/src/` that both `play.js` and the page use is written as classic scripts with a small UMD wrapper. In Node it exports with `module.exports`. In the browser it attaches to one global namespace, `EmberHollow`. `repo/index.html` loads the files with ordinary `<script src="src/...">` tags in dependency order. No `import`/`export` syntax and no bundler anywhere in `repo/`. Only the page's own UI code (`repo/src/page.js`) is browser-only. The rules code never touches `window`, `document`, `Date`, `Math.random` or any other real-time or environmental input.

## Rationale

`repo/index.html` must open from the file system. Browsers block `<script type="module">` files loaded over `file://` (origin and CORS rules), so ES modules would break the one requirement the Owner stated. Classic scripts work from `file://` and under Node 20 without a build step, and they keep the "no dependencies" constraint.

## Alternatives considered

- ES modules: rejected because they fail on `file://`.
- A bundler or a generated single file: rejected because it adds a build step and a tool dependency, and the generated file would drift from the sources.
- Duplicating the rules for the page: rejected because the constraint requires shared rules code.

## Revisit when

The project gains a server, or a build step is allowed by the constraints.
>>>END

<<<FILE decisions/D-002-threat-and-reach-marks.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-26
supersedes: none
---
# D-002: threat marks plus reach marks on the four neighbour tiles

## Decision

Threat marks keep their meaning: a visible creature that can hurt the player at its next action, with the player where they stand. A new reach mark is added. Each of the four orthogonal neighbour tiles of the player is marked with the creature letter(s) that would hurt the player at their next action if the player ended the turn on that tile. All marks are computed with the ember as it will be after this turn's dimming (current E minus 1, or minus 2 near the Gloom). Check 14 is strict: every damaging creature had a mark on the tile where the player ended the turn, in the previous output.

Limits: reach marks cover only the four neighbours, not the whole map. No creature behaviour, number or content changes. A creature that is orthogonally adjacent to the player or to a neighbour tile the player could step on is always shown, even if a wall blocks line of sight.

## Rationale

Pillar 1 says every threat that can hurt the player next turn is readable before it does. Stepping next to a moth or a hound is a legal next-turn move that leads to damage. Leaving it unmarked would let a player be hurt by a rule they had no way to read. The mark costs no new content, and the same planner can produce it. It makes check 14 verifiable without exceptions.

## Alternatives considered

- Build's interim reading, with exceptions for the player's own move: it needs no change, but it contradicts the pillar in spirit and leaves check 14 weak.
- Marking every tile in the creature's reach across the map: more clutter and no extra benefit beyond the next step.

## Revisit when

Play shows that reach marks clutter the screen or that players ignore them, or a new creature has an area effect that the neighbour-only marks cannot express.
>>>END

<<<FILE goals/G-001-first-playable-run/15-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: playtester
to: studio
stage: Review
outcome: partial
---
# 15: playtester → studio — playtest report: seed 42, floor 1 only (about 16 turns)

## Task

Read the observation report in Findings. It covers a very short slice of play. Decide whether more play is needed before judging the game's feel.

## Context

I was asked to play the Ember Hollow build as a player, using only the manual, and report what I experienced. I used one batch of runs, played through scripts only. I did not reach the end of a run, and I saw only a small part of the game.

## Findings

### Method (what I actually did)

- I played through text scripts with `node play.js`. This was input automation, not live play. I could not react turn by turn within a script, only between batches.
- I used seed 42 only, in two scripts: one walking east and south around the start room, and one walking west for 16 turns.
- I could not open a browser, so I know nothing about `index.html`, mouse play, or how the page looks or feels.
- I did not use trace or internal-state output.
- I played no other seeds, never got past floor 1, and had no win or loss. My longest run was 16 turns.

### Session summary

- The start room is a closed 5×5 room with the way out to the west. I first walked east and south to look around, and found only walls.
- On the second script I went west along a corridor and met one cave moth. I fought it and killed it, ending at HP 11/12 and Ember 84/100 on turn 16. A lone unlit brazier (`B`) came into view far to the west, and I did not reach it.

### Concrete moments

1. **Start (turn 0).** I could tell where I was, and the frame was readable: floor, HP, ember bar, and "dims 1/turn". The `<` appeared on the tile I started on only after I moved off it. That is fine, but it was a small surprise.
2. **Bumping walls (turns 2–3 of the first script).** The frame is printed again with "(refused: no turn passed)". I understood at once that nothing was spent. This is clear and a relief.
3. **Stale messages.** The message "You descend into Ember Hollow with one ember." stayed at the bottom of the list through every frame. Later, "The cave moth hits you for 1 / You hit the cave moth for 2 / The cave moth dies" was repeated in the next three frames, long after the moth was dead. Because of this I couldn't tell from the list whether something had just happened or was old. After the kill I briefly wondered whether the moth was still hitting me. HP stayed at 11, which showed it was not. Impact: low to medium. It makes the event log hard to trust at a glance.
4. **The moth appears (turn 9).** A moth `m` showed up at the edge of sight, about 6 tiles west. The creature list said "hunting" with its position. It closed in one tile per turn while I kept walking toward it.
5. **The warning (turn 11).** The moth was two tiles away. A `?` appeared on the tile between us, and the line read `Danger: W (m)`. I could tell what would hurt me if I stepped there. I stepped there anyway to test it, and on turn 12 the moth hit me for 1 (HP 12 → 11). The warning was accurate. Once it was adjacent the frame marked it with `!` and "THREAT: hits for 1 at its next action".
6. **The fight (turns 12–13).** One attack killed the moth ("hit for 2, dies"). The fight was over in a turn and cost 1 HP. It felt trivial rather than tense, but this was one weak creature.
7. **Ember (turns 0–16).** Ember went 100 → 84, exactly 1 per turn. Walking, waiting and fighting all cost the same. I never saw the "2 per turn" drain, because I never got near a Gloom. I could not feel any light/time trade-off in 16 turns: no braziers reached, no items, no choice that cost ember beyond walking. Two waits in the first script cost the same as moving, which tells me waiting is never free.
8. **Map view.** The map scrolls with me, so the start room slid off to the right as I went west. Remembered tiles (`,` and `%`) showed where I'd been. I found this readable. The many blank lines under the map are a bit odd.

### Answers to the open questions

- **Could I tell what could hurt me next turn?** For the one moth I met, yes: the `?` mark, the Danger line, and the `!` threat line all agreed and were right. I can't say anything about hounds, shades or the Gloom.
- **Did the light and the passing of turns feel like a real trade-off?** I couldn't tell. In 16 turns of floor 1, with nothing pressing, the ember was just a slowly falling number. I don't know whether the 100 ember is generous or tight.
- **Was a run short and varied enough to want another?** I can't say. I did not finish a run, so I have no run length. My longest was 16 turns. Floor 1 on seed 42 started with an empty closed room, then a corridor and one moth, which felt quiet.
- **Anything broken?** I saw no crash or stuck state, and nothing contradicted the manual. The only oddity is the stale messages (moment 3), which look like a presentation problem, not a rule problem. One thing was not verified: after the moth died I did not see whether a dead creature's mark or list entry lingered. The frames showed "Creatures: none in sight", so I think it did not.

### Issues with impact

- Stale or repeated messages in the log. Impact: low to medium, confusing about what just happened.
- Nothing else observed.

### Positives

- Refused moves cost nothing and say so plainly.
- The danger warnings were accurate and easy to read.
- The frame is compact and quick to scan.

### What I could not observe

- Anything in the browser: keyboard, mouse, layout, colours, the page itself.
- Shades, hounds, the Gloom, items, lit braziers, stairs down, floors 2–5, winning, dying, other seeds.
- Whether runs are varied between seeds, and how long a full run takes.

## Decisions already made

None.

## Constraints

- I used only the manual and what the game printed. I read no source, tests or design documents, and used no trace output.
- I did not edit the build.
- This report holds only what I observed. Hypotheses are marked as such.

## Open questions

- Is a further play round wanted? It should cover several seeds, deeper floors, and reaching a brazier and an item. This round showed almost none of the game's tension.
- Should someone with a browser check `index.html`? I could not.

## Expected output

The Studio reads this report and decides on routing: experience issues to `game-designer`, defects to `qa`. The stale-message issue is the only candidate so far. It looks like a presentation defect.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: repo/manual.md; the build in repo/
- Decisions: none
- Previous handoff: goals/G-001-first-playable-run/14-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-first-playable-run/13-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 13
from: qa
to: studio
stage: Verify
outcome: partial
---
# 13: qa → studio — verification of the reach-mark Build: `node --test` green (49/49); checks 27-30 and play-level evidence for 14, 26 and 29 still missing

## Task

Decide the next step. All visible automated evidence is green, but I cannot give a full `pass`. Checks 27-30 need a human at `repo/index.html`. For checks 14, 13, 26 and 29 I have no first-hand play-level evidence beyond the tests. Route a Playtester step, or a human page check, as the Studio sees fit.

## Context

G-001. Handoff 12 asked QA to verify checks 14, 13, 26 and 29 and to regress checks 1-26. I used what the packet offered:
- The runtime's Build check of `node --test` on this exact build.
- One trace run (round 1, `seed42-walk`).

The trace run's output is truncated in the middle. I did not use the remaining rounds, because a blind script cannot reach a hound or Gloom situation. play.js can only start from a seed and walk, and the layout of seed 42 beyond the start room is not known to me. The hand-made scenarios exist only as test fixtures.

## Findings

Only what I observed is reported.

**Observed: `node --test`, exit 0 (runtime Build check)**
- Totals: tests 49, pass 49, fail 0, cancelled 0, skipped 0.
- The packet shows only the tail of the listing. Visible passing tests: the strict sampled-states test, checks 1-8, 19, 20 and 24, check 25, the two visibility tests, check 9.1-9.9, and the view/rules agreement test.
- Visible diagnostics from the strict check-14 test in `reach.test.js` (20 random-walk seeds `c14-*`):
  - "damage events: threat 12, reach 7".
  - Each event is listed with its case; the visible ones involve moths.
  - No unmarked damage was reported, and the test would fail on one.
- Not visible to me:
  - The names and results of the individual `g001-final`, `bots` (check 14 strict, check 26), `creatures`, `rules`, `floors`, `gloom` and `view` tests.
  - The bot damage-count diagnostic and the check-26 seed summary (turn counts, victory).
  - All of that is inside the 49/0 totals but I cannot cite it per test.

**Observed: trace run, seed 42 (round 1, first ~16 and last ~6 commands visible; the middle is cut)**
- The frame layout, the legend (including `? reach mark`) and the `Danger: none` line print as in manual.md.
- The refusal path works: walking into a wall prints "(refused: no turn passed)", the turn and E stay unchanged, and the trace shows `consumed=false ... drain=0/turn`.
- Using empty slots 1-4 added the messages "Slot N is empty." Turn count and E stayed at 31 and 69 across the refused commands (visible in the tail). I did not see the frames of the slot commands themselves, because they fall in the cut.
- Dimming and radius: E fell 1 per consumed turn. At turn 31, E = 69 and r = 5, with the message "Your light shrinks." I did not see the E = 80→79 step itself in the visible part. The values at E = 69 and the message are consistent with spec section 3.
- Trace format: `[trace] command N ("c") turn T consumed=... E=... drain=.../turn`, per-creature lines with pathdist, `threats before action`, `events`.
- No damage event occurred in the visible part, so I have not seen a `case=… markedBefore=…` line in a real run. That format is asserted only by the `g001-final` trace test, whose result I take from the 49/0 total.
- All four moths on floor 1 stayed idle with pathdist ≥ 18, so no creature interaction was exercised.

**Verdicts**

| Check | Verdict | Basis |
|---|---|---|
| 1-8, 19, 20, 24, 25 | pass | Named tests passed in the listing visible to me. |
| 9-12, 15-18, 21-23 | not individually observed | Presumably covered by the tests not visible in the truncated listing; no per-test evidence available. |
| 13 (flare timing) | not individually observed | The test is in `g001-final.test.js`; the visible output does not show it. It is covered only by the 49/0 total, not confirmed. |
| 14 (strict) | pass for the random-walk portion; hand-made cases not individually observed | See the random-walk evidence above. Unlit/lit brazier, Gloom, hound, shade-at-r=2 and stairs cases are in `reach.test.js` and `g001-final.test.js`, covered only by the 49/0 total. |
| 26 (run length, bot wins) | not individually observed | The test exists and the suite is green, but I did not see the seed summary, so I cannot state turn counts or the winning seed. |
| 29 (reach marks, visual) | code/text only | Text: the `?` glyph and `Danger:` line are in the legend and covered by test. The browser appearance was not seen. |
| 27, 28, 30 | not verifiable by text runs | A human must open `repo/index.html`. Reported as not verified, not passed. |

**Independent reading of the changed code (not an execution)**
- `view.js`:
  - An unlit brazier neighbour is evaluated with E = min(100, E+60) minus that tile's drain.
  - Creatures other than the Gloom are skipped there; the Gloom goes through `planAction` and `hurtsAt`.
  - Stairs, walls and creature tiles get no reach entry.
  - A lit brazier is treated like floor.
  - This matches spec section 9 item 7 and the check-14 text.
- `script.js` `stepLogged`:
  - `moved` is derived from the player position only.
  - A descent onto `>` changes the floor, so `moved` is true with a new floor's position. A descent has no creature phase, so no damage event arises. The random-walk test in `reach.test.js` guards this explicitly with `res.state.floor === st.floor`; `stepLogged` has no such guard. This is harmless unless a damage event ever occurs on a descent turn, which the spec rules out.
- Known gap 2 (neighbour tile whose creature is hidden by a wall): the "shown" filter includes creatures orthogonally adjacent to the player or a neighbour tile, so such a creature is evaluated for reach marks. I saw no dedicated scenario for it in the packet, and I did not verify it by running. Treat as unverified.
- Known gap 3 (random walks rarely meet hounds or the Gloom) stands. Bot runs presumably reach floor 5 where a bot wins, but I did not see this.

**Defects:** none found. I have not reproduced a failure.
**Spec gaps:** none found.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat plus reach marks, after-dimming E, strict check 14. Handoff 10 rulings applied (flare reading A, hound bite at distance 1, lit brazier marked, unlit brazier marked by the Gloom only).

## Constraints

- QA did not modify production code or tests.
- No criterion is passed that was not observed.
- Checks 27-30 need a human at `repo/index.html`; no text run can show them.
- Remaining QA means are two more runs, with a script only starting from a seed. Without a known route, they cannot reach a hound or Gloom situation. Further assurance of checks 13, 14 and 26 should come from a test listing that shows per-test results, not from more blind scripts.

## Open questions

- None for the Game Designer.
- For the Studio: is the 49/0 `node --test` result, with the per-test results for checks 13, 14 (hand-made) and 26 not visible to QA, enough to proceed to the Playtester? If the full listing is needed, a later QA step can request it through a `tests` run with the full listing (diagnostics included) on `reach.test.js`, `g001-final.test.js` and `bots.test.js`.

## Expected output

- Addressed to `studio`.
- Suggested next step: a Playtester step on `repo/manual.md` and `node play.js` for the experience signals, plus a human opening `repo/index.html` for checks 27-30.
- A fresh Playtester Handoff must be composed from permitted information only. It should carry no implementation details from this file, only the manual and the play/trace commands.
- If the Studio wants a full QA pass first, the follow-up QA step should run `node --test` with per-test output and read the check 13, 14 and 26 diagnostics.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, repo/play.js, repo/src/view.js, repo/src/script.js, repo/tests/g001-final.test.js, repo/tests/bots.test.js, repo/tests/reach.test.js; the build in repo/ (run commands in project.md)
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/12-gameplay-engineer-to-qa.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable-run/17-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
